#!/usr/bin/env python3
"""Emit a deterministic backend pack for one hash-bound asset authority."""

from __future__ import annotations

import argparse
import json
import struct
import uuid
import zlib
from pathlib import Path, PurePosixPath
from typing import Any

import index_lyx_pair as shared


GENERATOR_VERSION = "ttna-asset-authority-indexer-0.1.0"
CONFIG_SCHEMA_ID = "ttna-asset-authority-map-v1"

RIGHTS_KEYS = {
    "attribution",
    "authority_path",
    "copyright_status",
    "id",
    "institutional_evidence_url",
    "institutional_rights_label",
    "manifest_url",
    "not_cc0",
    "record_type",
    "rights_statement",
    "rights_uri",
    "schema_id",
    "schema_version",
    "scope",
    "spdx_expression",
}
ASSET_KEYS = {
    "id",
    "logical_path",
    "media_type",
    "record_type",
    "resource_id",
    "rights_id",
    "schema_id",
    "schema_version",
}
VERSION_KEYS = {
    "acquisition_url",
    "asset_id",
    "authority_path",
    "edition_id",
    "height_px",
    "id",
    "normalization_id",
    "normalized_bytes",
    "normalized_sha256",
    "provenance_master_bytes",
    "provenance_master_path",
    "provenance_master_sha256",
    "provenance_master_url",
    "record_type",
    "resolution_dpi",
    "rights_id",
    "schema_id",
    "schema_version",
    "source_bytes",
    "source_path",
    "source_sha256",
    "width_px",
}
RELATION_KEYS = {
    "from_id",
    "id",
    "record_type",
    "relation",
    "schema_id",
    "schema_version",
    "to_id",
}


def require_exact_keys(
    value: dict[str, Any], expected: set[str], context: str
) -> None:
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unexpected " + ", ".join(extra))
        raise SystemExit(f"{context} keys invalid: {'; '.join(details)}")


def load_json(path: Path, context: str) -> tuple[dict[str, Any], bytes]:
    try:
        payload = path.read_bytes()
        value = json.loads(payload.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(f"cannot read {context} {path}: {error}") from error
    if not isinstance(value, dict):
        raise SystemExit(f"{context} root must be an object")
    return value, payload


def resolve_relative(root: Path, value: str, context: str) -> Path:
    if not isinstance(value, str) or not value:
        raise SystemExit(f"{context} must be a nonempty relative path")
    relative = PurePosixPath(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise SystemExit(f"{context} escapes the lane root")
    root_resolved = root.resolve()
    resolved = root.joinpath(*relative.parts).resolve()
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise SystemExit(f"{context} escapes the lane root")
    return resolved


def require_bound_bytes(
    path: Path, expected_bytes: int, expected_sha256: str, context: str
) -> bytes:
    payload = path.read_bytes()
    if len(payload) != expected_bytes:
        raise SystemExit(
            f"{context} byte-count drift: {len(payload)} != {expected_bytes}"
        )
    actual_sha256 = shared.digest_bytes(payload)
    if actual_sha256 != expected_sha256:
        raise SystemExit(
            f"{context} sha256 drift: {actual_sha256} != {expected_sha256}"
        )
    return payload


def png_metadata(payload: bytes) -> dict[str, int | float]:
    if payload[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("release asset is not a PNG")
    offset = 8
    width: int | None = None
    height: int | None = None
    x_ppm: int | None = None
    y_ppm: int | None = None
    unit: int | None = None
    saw_iend = False
    while offset < len(payload):
        if offset + 12 > len(payload):
            raise SystemExit("release PNG has a truncated chunk header")
        length = struct.unpack(">I", payload[offset : offset + 4])[0]
        chunk_type = payload[offset + 4 : offset + 8]
        data_start = offset + 8
        data_end = data_start + length
        crc_end = data_end + 4
        if crc_end > len(payload):
            raise SystemExit("release PNG has a truncated chunk")
        chunk_data = payload[data_start:data_end]
        stored_crc = struct.unpack(">I", payload[data_end:crc_end])[0]
        actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if actual_crc != stored_crc:
            raise SystemExit(f"release PNG chunk {chunk_type!r} has bad CRC")
        if chunk_type == b"IHDR":
            if length != 13 or width is not None:
                raise SystemExit("release PNG has an invalid IHDR")
            width, height = struct.unpack(">II", chunk_data[:8])
        elif chunk_type == b"pHYs":
            if length != 9 or x_ppm is not None:
                raise SystemExit("release PNG has an invalid pHYs chunk")
            x_ppm, y_ppm, unit = struct.unpack(">IIB", chunk_data)
        elif chunk_type == b"IEND":
            if length != 0 or crc_end != len(payload):
                raise SystemExit("release PNG has an invalid IEND")
            saw_iend = True
            break
        offset = crc_end
    if width is None or height is None or not saw_iend:
        raise SystemExit("release PNG lacks required structural chunks")
    if x_ppm is None or y_ppm is None or unit != 1 or x_ppm != y_ppm:
        raise SystemExit("release PNG lacks square, metre-based resolution metadata")
    return {
        "width_px": width,
        "height_px": height,
        "resolution_ppm": x_ppm,
        "resolution_dpi": x_ppm * 0.0254,
    }


def tiff_metadata(payload: bytes) -> dict[str, int | float]:
    if payload[:2] == b"II":
        endian = "<"
    elif payload[:2] == b"MM":
        endian = ">"
    else:
        raise SystemExit("provenance master is not a TIFF")
    if len(payload) < 8 or struct.unpack(endian + "H", payload[2:4])[0] != 42:
        raise SystemExit("provenance TIFF header is invalid")
    ifd_offset = struct.unpack(endian + "I", payload[4:8])[0]
    if ifd_offset + 2 > len(payload):
        raise SystemExit("provenance TIFF IFD offset is invalid")
    count = struct.unpack(endian + "H", payload[ifd_offset : ifd_offset + 2])[0]
    type_sizes = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8}
    values: dict[int, int | float] = {}
    for index in range(count):
        start = ifd_offset + 2 + index * 12
        if start + 12 > len(payload):
            raise SystemExit("provenance TIFF IFD is truncated")
        tag, value_type, value_count = struct.unpack(
            endian + "HHI", payload[start : start + 8]
        )
        size = type_sizes.get(value_type)
        if size is None or value_count < 1:
            continue
        total = size * value_count
        value_field = payload[start + 8 : start + 12]
        if total <= 4:
            raw = value_field[:total]
        else:
            value_offset = struct.unpack(endian + "I", value_field)[0]
            if value_offset + total > len(payload):
                raise SystemExit("provenance TIFF tag data is truncated")
            raw = payload[value_offset : value_offset + total]
        if value_type == 3:
            value: int | float = struct.unpack(endian + "H", raw[:2])[0]
        elif value_type == 4:
            value = struct.unpack(endian + "I", raw[:4])[0]
        elif value_type == 5:
            numerator, denominator = struct.unpack(endian + "II", raw[:8])
            if denominator == 0:
                raise SystemExit("provenance TIFF has zero rational denominator")
            value = numerator / denominator
        else:
            value = raw[0]
        values[tag] = value
    required_tags = {256, 257, 282, 283, 296}
    if not required_tags <= values.keys():
        raise SystemExit("provenance TIFF lacks required dimension/resolution tags")
    resolution_unit = int(values[296])
    factor = 1.0 if resolution_unit == 2 else 2.54 if resolution_unit == 3 else None
    if factor is None:
        raise SystemExit("provenance TIFF resolution is not physical")
    x_dpi = float(values[282]) * factor
    y_dpi = float(values[283]) * factor
    if abs(x_dpi - y_dpi) > 0.001:
        raise SystemExit("provenance TIFF resolution is not square")
    return {
        "width_px": int(values[256]),
        "height_px": int(values[257]),
        "resolution_dpi": x_dpi,
    }


def validate_record_base(
    record: dict[str, Any], schema_id: str, record_type: str
) -> None:
    if record.get("schema_id") != schema_id:
        raise SystemExit(f"{record_type} schema_id drift")
    if record.get("schema_version") != shared.SCHEMA_VERSION:
        raise SystemExit(f"{record_type} schema_version drift")
    if record.get("record_type") != record_type:
        raise SystemExit(f"{record_type} record_type drift")
    record_id = record.get("id")
    if not isinstance(record_id, str) or not record_id.startswith("urn:uuid:"):
        raise SystemExit(f"{record_type} id is not a UUID URN")
    try:
        uuid.UUID(record_id.removeprefix("urn:uuid:"))
    except ValueError as error:
        raise SystemExit(f"{record_type} id is not a UUID URN") from error


def resource_record() -> dict[str, Any]:
    resource_id = shared.stable_id("resource", shared.RESOURCE_URL)
    return {
        **shared.record_base("ttna-resource-v1", resource_id, "resource"),
        "resource_local_id": "R015",
        "course_local_id": "C110",
        "title": "Tea Time Numerical Analysis",
        "author": "Leon Q. Brin",
        "authority_url": shared.RESOURCE_URL,
    }


def edition_record(resource_id: str) -> dict[str, Any]:
    edition_id = shared.stable_id("edition", shared.EDITION_COMMIT)
    return {
        **shared.record_base("ttna-edition-v1", edition_id, "edition"),
        "resource_id": resource_id,
        "edition_label": "Third Edition",
        "tag": "v3.0",
        "commit": shared.EDITION_COMMIT,
        "tree": shared.EDITION_TREE,
        "source_locale": "en-US",
        "target_locale": "id-ID",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane-root", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    lane_root = args.lane_root.resolve()
    config_path = args.config.resolve()
    if config_path != lane_root and lane_root not in config_path.parents:
        raise SystemExit("asset-authority config must be inside the lane root")
    config, config_bytes = load_json(config_path, "asset-authority config")
    require_exact_keys(
        config,
        {
            "schema_id",
            "schema_version",
            "recorded_date",
            "file_order",
            "file_kind",
            "authority",
            "spdx_mapping",
            "stable_keys",
            "records",
        },
        "asset-authority config",
    )
    if config["schema_id"] != CONFIG_SCHEMA_ID:
        raise SystemExit("unsupported asset-authority config schema_id")
    if config["schema_version"] != shared.SCHEMA_VERSION:
        raise SystemExit("unsupported asset-authority config schema_version")
    if not isinstance(config["file_order"], int):
        raise SystemExit("asset-authority file_order must be an integer")
    if config["file_kind"] != "asset_authority":
        raise SystemExit("asset-authority file_kind must be asset_authority")

    authority = config["authority"]
    if not isinstance(authority, dict):
        raise SystemExit("asset-authority authority must be an object")
    require_exact_keys(
        authority, {"path", "bytes", "sha256"}, "asset-authority authority"
    )
    authority_path = resolve_relative(lane_root, authority["path"], "authority path")
    authority_bytes = require_bound_bytes(
        authority_path,
        authority["bytes"],
        authority["sha256"],
        "authority receipt",
    )
    try:
        receipt = json.loads(authority_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(f"cannot decode authority receipt: {error}") from error
    if receipt.get("schema_id") != "ttna-third-party-asset-authority-v1":
        raise SystemExit("authority receipt schema_id drift")

    spdx_mapping = config["spdx_mapping"]
    if not isinstance(spdx_mapping, dict):
        raise SystemExit("asset-authority spdx_mapping must be an object")
    require_exact_keys(
        spdx_mapping,
        {
            "receipt_expression",
            "backend_expression",
            "authority_url",
        },
        "asset-authority spdx_mapping",
    )
    if receipt["rights"]["spdx_expression"] != spdx_mapping["receipt_expression"]:
        raise SystemExit("authority receipt SPDX expression drift")
    if spdx_mapping["backend_expression"] != "CC-PDM-1.0":
        raise SystemExit("backend must use SPDX CC-PDM-1.0")
    if spdx_mapping["receipt_expression"] != spdx_mapping["backend_expression"]:
        raise SystemExit("authority receipt and backend SPDX expressions differ")
    if spdx_mapping["authority_url"] != "https://spdx.org/licenses/CC-PDM-1.0.html":
        raise SystemExit("SPDX authority URL drift")

    stable_keys = config["stable_keys"]
    if not isinstance(stable_keys, dict):
        raise SystemExit("asset-authority stable_keys must be an object")
    require_exact_keys(stable_keys, {"rights", "asset"}, "stable keys")

    records = config["records"]
    if not isinstance(records, dict):
        raise SystemExit("asset-authority records must be an object")
    require_exact_keys(
        records, {"rights", "asset", "asset_version", "version_of"}, "records"
    )
    rights = records["rights"]
    asset = records["asset"]
    version = records["asset_version"]
    relation = records["version_of"]
    for value, expected, context in (
        (rights, RIGHTS_KEYS, "rights record"),
        (asset, ASSET_KEYS, "asset record"),
        (version, VERSION_KEYS, "asset-version record"),
        (relation, RELATION_KEYS, "version_of record"),
    ):
        if not isinstance(value, dict):
            raise SystemExit(f"{context} must be an object")
        require_exact_keys(value, expected, context)
    validate_record_base(rights, "ttna-rights-v1", "rights")
    validate_record_base(asset, "ttna-asset-v1", "asset")
    validate_record_base(version, "ttna-asset-version-v1", "asset_version")
    validate_record_base(relation, "ttna-relation-v1", "relation")

    resource = resource_record()
    edition = edition_record(resource["id"])
    expected_rights_id = shared.stable_id("rights", stable_keys["rights"])
    expected_asset_id = shared.stable_id("asset", stable_keys["asset"])
    expected_version_id = shared.stable_id(
        "asset_version",
        f"{expected_asset_id}|sha256:{version['source_sha256']}",
    )
    expected_relation_id = shared.stable_id(
        "relation",
        f"{expected_version_id}|version_of|{expected_asset_id}",
    )
    expected_ids = {
        "rights": expected_rights_id,
        "asset": expected_asset_id,
        "asset_version": expected_version_id,
        "version_of": expected_relation_id,
    }
    actual_ids = {
        "rights": rights["id"],
        "asset": asset["id"],
        "asset_version": version["id"],
        "version_of": relation["id"],
    }
    if actual_ids != expected_ids:
        raise SystemExit(f"stable-ID drift: {actual_ids} != {expected_ids}")
    if stable_keys["asset"] != asset["logical_path"]:
        raise SystemExit("asset stable key differs from logical_path")
    if asset["resource_id"] != resource["id"]:
        raise SystemExit("asset resource_id drift")
    if version["edition_id"] != edition["id"]:
        raise SystemExit("asset-version edition_id drift")
    if asset["rights_id"] != rights["id"] or version["rights_id"] != rights["id"]:
        raise SystemExit("asset rights linkage drift")
    if version["asset_id"] != asset["id"]:
        raise SystemExit("asset-version asset_id drift")
    if relation["relation"] != "version_of":
        raise SystemExit("asset relation must be version_of")
    if relation["from_id"] != version["id"] or relation["to_id"] != asset["id"]:
        raise SystemExit("version_of endpoints drift")
    if rights["spdx_expression"] != spdx_mapping["backend_expression"]:
        raise SystemExit("backend rights SPDX expression drift")

    receipt_rights = receipt["rights"]
    for field in (
        "copyright_status",
        "rights_statement",
        "rights_uri",
        "not_cc0",
        "attribution",
    ):
        if rights[field] != receipt_rights[field]:
            raise SystemExit(f"backend rights {field} differs from authority receipt")
    institution = receipt["institution"]
    if rights["manifest_url"] != institution["iiif_manifest"]:
        raise SystemExit("backend manifest URL differs from authority receipt")
    if rights["institutional_evidence_url"] != institution["ddb_record"]:
        raise SystemExit("backend DDB URL differs from authority receipt")
    if rights["institutional_rights_label"] != "Public Domain Mark 1.0 (PDM)":
        raise SystemExit("backend institutional rights label drift")
    if receipt["source_context"]["missing_upstream_path"] != asset["logical_path"]:
        raise SystemExit("authority source context differs from asset logical_path")
    if asset["media_type"] != "image/png":
        raise SystemExit("authority asset media_type must be image/png")
    if rights["authority_path"] != authority["path"]:
        raise SystemExit("rights authority_path drift")
    if version["authority_path"] != authority["path"]:
        raise SystemExit("asset-version authority_path drift")

    release = receipt["release_derivative"]
    if release["path"] != version["source_path"]:
        raise SystemExit("release source_path drift")
    if release["url"] != version["acquisition_url"]:
        raise SystemExit("release acquisition_url drift")
    for receipt_field, version_field in (
        ("bytes", "source_bytes"),
        ("sha256", "source_sha256"),
        ("width_px", "width_px"),
        ("height_px", "height_px"),
        ("resolution_dpi", "resolution_dpi"),
    ):
        if release[receipt_field] != version[version_field]:
            raise SystemExit(f"release {receipt_field} differs from asset-version")
    if version["normalization_id"] != "binary-identity-v1":
        raise SystemExit("binary asset must use binary-identity-v1")
    if version["normalized_bytes"] != version["source_bytes"]:
        raise SystemExit("binary identity byte count drift")
    if version["normalized_sha256"] != version["source_sha256"]:
        raise SystemExit("binary identity hash drift")

    master = receipt["provenance_master"]
    for receipt_field, version_field in (
        ("path", "provenance_master_path"),
        ("url", "provenance_master_url"),
        ("bytes", "provenance_master_bytes"),
        ("sha256", "provenance_master_sha256"),
    ):
        if master[receipt_field] != version[version_field]:
            raise SystemExit(f"master {receipt_field} differs from asset-version")

    release_path = resolve_relative(lane_root, release["path"], "release path")
    master_path = resolve_relative(lane_root, master["path"], "master path")
    release_bytes = require_bound_bytes(
        release_path,
        release["bytes"],
        release["sha256"],
        "release asset",
    )
    master_bytes = require_bound_bytes(
        master_path,
        master["bytes"],
        master["sha256"],
        "provenance master",
    )
    release_metadata = png_metadata(release_bytes)
    master_metadata = tiff_metadata(master_bytes)
    for metadata, declaration, context in (
        (release_metadata, release, "release asset"),
        (master_metadata, master, "provenance master"),
    ):
        if metadata["width_px"] != declaration["width_px"]:
            raise SystemExit(f"{context} width drift")
        if metadata["height_px"] != declaration["height_px"]:
            raise SystemExit(f"{context} height drift")
        if abs(float(metadata["resolution_dpi"]) - declaration["resolution_dpi"]) > 0.001:
            raise SystemExit(f"{context} resolution drift")
    if release_metadata["resolution_ppm"] != 7874:
        raise SystemExit("release PNG pHYs drift")
    admission = receipt["admission"]
    if admission != {
        "rights_gate": "pass",
        "identity_gate": "pass_as_independent_replacement",
        "build_gate": "pass",
        "build_evidence": {
            "pdf": "output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf",
            "pdf_sha256": "cbc31e9e27fdee96845d78fa6a625bf956196001b7941ddf0f1232f5def46b45",
            "physical_pdf_page": 256,
            "render": "tmp/qa/cbc31e9e/high/page-256.png",
            "render_dpi": 150,
            "visual_result": "pass_legible_complete_framed",
        },
    }:
        raise SystemExit("authority admission state drift")

    outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (args.out / "authority" / "resources.jsonl", [resource]),
        (args.out / "authority" / "editions.jsonl", [edition]),
        (args.out / "rights" / "components.jsonl", [rights]),
        (args.out / "assets" / "assets.jsonl", [asset]),
        (args.out / "assets" / "versions.jsonl", [version]),
        (args.out / "topology" / "relations.jsonl", [relation]),
    ]
    shared.validate_local_relation_closure(outputs)
    expected_jsonl = {
        path.relative_to(args.out).as_posix() for path, _ in outputs
    }
    existing_jsonl = {
        path.relative_to(args.out).as_posix()
        for path in args.out.rglob("*.jsonl")
    } if args.out.exists() else set()
    unexpected_jsonl = sorted(existing_jsonl - expected_jsonl)
    if unexpected_jsonl:
        raise SystemExit(
            "asset-authority output contains unexpected JSONL: "
            + ", ".join(unexpected_jsonl)
        )

    if config_path.read_bytes() != config_bytes:
        raise SystemExit("asset-authority config changed during generation")
    if authority_path.read_bytes() != authority_bytes:
        raise SystemExit("authority receipt changed during generation")
    if release_path.read_bytes() != release_bytes:
        raise SystemExit("release asset changed during generation")
    if master_path.read_bytes() != master_bytes:
        raise SystemExit("provenance master changed during generation")
    for path, record_group in outputs:
        shared.write_jsonl(path, record_group)

    files: list[dict[str, Any]] = []
    for path, record_group in outputs:
        payload = path.read_bytes()
        files.append(
            {
                "path": path.relative_to(args.out).as_posix(),
                "bytes": len(payload),
                "sha256": shared.digest_bytes(payload),
                "records": len(record_group),
            }
        )
    config_relative = config_path.relative_to(lane_root).as_posix()
    manifest = {
        "schema_id": "ttna-lane-manifest-v1",
        "schema_version": shared.SCHEMA_VERSION,
        "generator": GENERATOR_VERSION,
        "recorded_date": config["recorded_date"],
        "resource_id": resource["id"],
        "edition_id": edition["id"],
        "locale": "id-ID",
        "source_commit": shared.EDITION_COMMIT,
        "source_tree": shared.EDITION_TREE,
        "scope": authority["path"],
        "file_order": config["file_order"],
        "file_kind": config["file_kind"],
        "source_role": "third_party_asset_authority",
        "config_path": config_relative,
        "config_sha256": shared.digest_bytes(config_bytes),
        "authority_sha256": shared.digest_bytes(authority_bytes),
        "admission": admission,
        "files": sorted(files, key=lambda item: item["path"]),
        "counts": {
            "resources": 1,
            "editions": 1,
            "rights": 1,
            "assets": 1,
            "asset_versions": 1,
            "relations": 1,
        },
    }
    shared.write_json(args.out / "manifests" / "lane_manifest.json", manifest)
    print(shared.canonical(manifest))


if __name__ == "__main__":
    main()
