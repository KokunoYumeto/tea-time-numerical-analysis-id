#!/usr/bin/env python3
"""Emit a deterministic backend pack for one hash-bound toolchain closure."""

from __future__ import annotations

import argparse
import json
import uuid
import zipfile
from pathlib import Path
from typing import Any

import index_asset_authority as asset_shared
import index_lyx_pair as shared


GENERATOR_VERSION = "ttna-toolchain-authority-indexer-0.1.0"
CONFIG_SCHEMA_ID = "ttna-toolchain-authority-map-v1"
AUTHORITY_SCHEMA_ID = "ttna-toolchain-authority-v1"
EXPECTED_SPDX_EXPRESSION = "LPPL-1.3c+"
EXPECTED_SPDX_ID = "LPPL-1.3c"

RIGHTS_KEYS = {
    "authority_path",
    "copyright",
    "id",
    "maintenance_status",
    "maintainer",
    "preserve_complete_work_required",
    "record_type",
    "redistribution_permitted",
    "schema_id",
    "schema_version",
    "scope",
    "spdx_expression",
}
ASSET_KEYS = {
    "component_name",
    "component_version",
    "id",
    "logical_path",
    "media_type",
    "record_type",
    "resource_id",
    "rights_id",
    "role",
    "schema_id",
    "schema_version",
}
VERSION_KEYS = {
    "asset_id",
    "authority_path",
    "edition_id",
    "id",
    "normalization_id",
    "normalized_bytes",
    "normalized_sha256",
    "provenance",
    "record_type",
    "rights_id",
    "schema_id",
    "schema_version",
    "source_bytes",
    "source_path",
    "source_sha256",
}
RECIPE_KEYS = {
    "command",
    "edition_id",
    "id",
    "input_asset_version_ids",
    "name",
    "output_asset_version_ids",
    "record_type",
    "resource_id",
    "rights_id",
    "schema_id",
    "schema_version",
    "source_instruction",
    "verification",
    "working_directory",
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


def require_exact_keys(value: dict[str, Any], expected: set[str], context: str) -> None:
    asset_shared.require_exact_keys(value, expected, context)


def require_list(value: Any, context: str, length: int | None = None) -> list[Any]:
    if not isinstance(value, list):
        raise SystemExit(f"{context} must be an array")
    if length is not None and len(value) != length:
        raise SystemExit(f"{context} must have exactly {length} entries")
    return value


def require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise SystemExit(f"{context} must be a nonempty string")
    return value


def require_line_range(value: Any, line_count: int, context: str) -> tuple[int, int]:
    values = require_list(value, context, 2)
    if not all(isinstance(item, int) for item in values):
        raise SystemExit(f"{context} must contain integers")
    start, end = values
    if start < 1 or end < start or end > line_count:
        raise SystemExit(f"{context} is outside its evidence file")
    return start, end


def validate_record_base(record: dict[str, Any], schema_id: str, record_type: str) -> None:
    asset_shared.validate_record_base(record, schema_id, record_type)


def validate_uuid_array(value: Any, context: str) -> list[str]:
    values = require_list(value, context)
    if not values or len(values) != len(set(values)):
        raise SystemExit(f"{context} must be a nonempty unique array")
    for item in values:
        if not isinstance(item, str) or not item.startswith("urn:uuid:"):
            raise SystemExit(f"{context} contains a non-UUID URN")
        try:
            uuid.UUID(item.removeprefix("urn:uuid:"))
        except ValueError as error:
            raise SystemExit(f"{context} contains a non-UUID URN") from error
    return values


def validate_receipt(lane_root: Path, receipt: dict[str, Any]) -> dict[str, bytes]:
    require_exact_keys(
        receipt,
        {
            "admission",
            "archive",
            "derivation",
            "license",
            "package",
            "recorded_date",
            "schema_id",
            "schema_version",
            "work_files",
        },
        "toolchain authority receipt",
    )
    if receipt["schema_id"] != AUTHORITY_SCHEMA_ID:
        raise SystemExit("toolchain authority schema_id drift")
    if receipt["schema_version"] != shared.SCHEMA_VERSION:
        raise SystemExit("toolchain authority schema_version drift")

    package = receipt["package"]
    if not isinstance(package, dict):
        raise SystemExit("toolchain package must be an object")
    require_exact_keys(
        package,
        {"catalog_url", "maintainer", "name", "release_date", "version"},
        "toolchain package",
    )
    if package != {
        "catalog_url": "https://ctan.org/pkg/cprotect",
        "maintainer": "Bruno Le Floch",
        "name": "cprotect",
        "release_date": "2026-04-17",
        "version": "1.0f",
    }:
        raise SystemExit("cprotect package identity drift")

    admission = receipt["admission"]
    if admission != {
        "derivation_gate": "pass_byte_exact",
        "identity_gate": "pass",
        "redistribution_gate": "pass_unmodified_archive_and_exact_generated_file",
        "rights_gate": "pass",
    }:
        raise SystemExit("toolchain admission state drift")

    archive = receipt["archive"]
    if not isinstance(archive, dict):
        raise SystemExit("toolchain archive must be an object")
    require_exact_keys(
        archive,
        {"bytes", "members", "path", "sha256", "source_url"},
        "toolchain archive",
    )
    if archive["source_url"] != "https://mirrors.ctan.org/macros/latex/contrib/cprotect.zip":
        raise SystemExit("cprotect CTAN archive URL drift")
    archive_path = asset_shared.resolve_relative(lane_root, archive["path"], "archive path")
    archive_bytes = asset_shared.require_bound_bytes(
        archive_path, archive["bytes"], archive["sha256"], "toolchain archive"
    )

    members = require_list(archive["members"], "archive members", 3)
    member_rows: dict[str, dict[str, Any]] = {}
    for row in members:
        if not isinstance(row, dict):
            raise SystemExit("archive member must be an object")
        require_exact_keys(
            row, {"bytes", "local_path", "path", "sha256"}, "archive member"
        )
        member_path = require_string(row["path"], "archive member path")
        if member_path in member_rows:
            raise SystemExit(f"duplicate archive member {member_path}")
        member_rows[member_path] = row
    expected_member_names = {
        "cprotect/README",
        "cprotect/cprotect.dtx",
        "cprotect/cprotect.pdf",
    }
    if set(member_rows) != expected_member_names:
        raise SystemExit("cprotect archive member inventory drift")

    bound: dict[str, bytes] = {archive["path"]: archive_bytes}
    try:
        with zipfile.ZipFile(archive_path, "r") as archive_handle:
            file_infos = [item for item in archive_handle.infolist() if not item.is_dir()]
            directory_names = {item.filename for item in archive_handle.infolist() if item.is_dir()}
            if directory_names != {"cprotect/"}:
                raise SystemExit("cprotect archive directory inventory drift")
            if {item.filename for item in file_infos} != expected_member_names:
                raise SystemExit("cprotect archive file inventory drift")
            for info in file_infos:
                if info.flag_bits & 0x1:
                    raise SystemExit(f"encrypted archive member {info.filename}")
                row = member_rows[info.filename]
                payload = archive_handle.read(info)
                if info.file_size != row["bytes"] or len(payload) != row["bytes"]:
                    raise SystemExit(f"archive member {info.filename} byte-count drift")
                if shared.digest_bytes(payload) != row["sha256"]:
                    raise SystemExit(f"archive member {info.filename} sha256 drift")
                local_path = asset_shared.resolve_relative(
                    lane_root, row["local_path"], f"local {info.filename} path"
                )
                local_payload = asset_shared.require_bound_bytes(
                    local_path,
                    row["bytes"],
                    row["sha256"],
                    f"local {info.filename}",
                )
                if local_payload != payload:
                    raise SystemExit(f"local {info.filename} differs from archive member")
                bound[row["local_path"]] = local_payload
    except (OSError, zipfile.BadZipFile) as error:
        raise SystemExit(f"cannot validate cprotect archive: {error}") from error

    work_files = require_list(receipt["work_files"], "toolchain work files", 3)
    expected_roles = {
        "canonical_source",
        "generated_installer",
        "generated_installable_style",
    }
    seen_roles: set[str] = set()
    for row in work_files:
        if not isinstance(row, dict):
            raise SystemExit("toolchain work file must be an object")
        require_exact_keys(row, {"bytes", "path", "role", "sha256"}, "toolchain work file")
        role = require_string(row["role"], "toolchain work-file role")
        if role in seen_roles:
            raise SystemExit(f"duplicate toolchain work-file role {role}")
        seen_roles.add(role)
        path = asset_shared.resolve_relative(lane_root, row["path"], f"{role} path")
        bound[row["path"]] = asset_shared.require_bound_bytes(
            path, row["bytes"], row["sha256"], role
        )
    if seen_roles != expected_roles:
        raise SystemExit("toolchain work-file roles drift")

    license_row = receipt["license"]
    if not isinstance(license_row, dict):
        raise SystemExit("toolchain license must be an object")
    require_exact_keys(
        license_row,
        {
            "copyright",
            "declared_grant",
            "evidence",
            "maintenance_status",
            "maintainer",
            "redistribution_basis",
            "spdx_authority_url",
            "spdx_expression",
            "spdx_license_id",
            "spdx_or_later_encoding",
        },
        "toolchain license",
    )
    if license_row["spdx_expression"] != EXPECTED_SPDX_EXPRESSION:
        raise SystemExit("cprotect SPDX expression drift")
    if license_row["spdx_license_id"] != EXPECTED_SPDX_ID:
        raise SystemExit("cprotect SPDX license identifier drift")
    if license_row["spdx_authority_url"] != "https://spdx.org/licenses/LPPL-1.3c.html":
        raise SystemExit("cprotect SPDX authority URL drift")
    if license_row["maintenance_status"] != "maintained" or license_row["maintainer"] != "Bruno Le Floch":
        raise SystemExit("cprotect maintenance identity drift")
    evidence_rows = require_list(license_row["evidence"], "license evidence", 2)
    evidence_text: dict[str, list[str]] = {}
    for row in evidence_rows:
        if not isinstance(row, dict):
            raise SystemExit("license evidence entry must be an object")
        require_exact_keys(row, {"line_range", "path", "sha256"}, "license evidence entry")
        path_value = require_string(row["path"], "license evidence path")
        path = asset_shared.resolve_relative(lane_root, path_value, "license evidence path")
        payload = path.read_bytes()
        if shared.digest_bytes(payload) != row["sha256"]:
            raise SystemExit(f"license evidence {path_value} sha256 drift")
        try:
            lines = payload.decode("utf-8").splitlines()
        except UnicodeDecodeError as error:
            raise SystemExit(f"license evidence {path_value} is not UTF-8") from error
        start, end = require_line_range(row["line_range"], len(lines), "license evidence line range")
        evidence_text[path_value] = lines[start - 1 : end]
    readme_path = "authority/toolchain/cprotect-1.0f/package/cprotect/README"
    dtx_path = "authority/toolchain/cprotect-1.0f/package/cprotect/cprotect.dtx"
    if evidence_text.get(readme_path) != [
        "Released under the LaTeX Project Public License v1.3c or later",
        "See http://www.latex-project.org/lppl.txt",
    ]:
        raise SystemExit("cprotect README license evidence drift")
    dtx_evidence = "\n".join(evidence_text.get(dtx_path, []))
    for required in (
        "Copyright (C) 2010-2011, 2026 by Bruno Le Floch",
        "version 1.3c of this license or (at your option) any later",
        'This work is "maintained"',
        "This work consists of the file  cprotect.dtx",
        "cprotect.sty.",
    ):
        if required not in dtx_evidence:
            raise SystemExit(f"cprotect DTX license evidence lacks {required!r}")

    dtx_text = bound[dtx_path].decode("utf-8")
    if "\\ProvidesPackage{cprotect}[2026/04/17 v1.0f (Bruno Le Floch)]" not in dtx_text:
        raise SystemExit("cprotect DTX package identity drift")
    if "\\file{\\jobname.sty}{\\from{\\jobname.dtx}{package}}" not in dtx_text:
        raise SystemExit("cprotect DTX docstrip recipe drift")
    style_path = "authority/toolchain/cprotect-1.0f/package/cprotect/cprotect.sty"
    style_text = bound[style_path].decode("utf-8")
    if "\\ProvidesPackage{cprotect}[2026/04/17 v1.0f (Bruno Le Floch)]" not in style_text:
        raise SystemExit("cprotect generated style identity drift")

    derivation = receipt["derivation"]
    if not isinstance(derivation, dict):
        raise SystemExit("toolchain derivation must be an object")
    require_exact_keys(
        derivation,
        {
            "command",
            "declared_by_line_range",
            "declared_by_path",
            "input_paths",
            "output_path",
            "verification",
        },
        "toolchain derivation",
    )
    if derivation["command"] != [
        "tex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "cprotect.ins",
    ]:
        raise SystemExit("cprotect derivation command drift")
    if derivation["input_paths"] != [
        dtx_path,
        "authority/toolchain/cprotect-1.0f/package/cprotect/cprotect.ins",
    ] or derivation["output_path"] != style_path:
        raise SystemExit("cprotect derivation input/output drift")
    if derivation["declared_by_path"] != readme_path or derivation["declared_by_line_range"] != [19, 30]:
        raise SystemExit("cprotect derivation evidence locator drift")
    verification = derivation["verification"]
    if not isinstance(verification, dict):
        raise SystemExit("toolchain derivation verification must be an object")
    require_exact_keys(
        verification,
        {
            "byte_equal_to_checked_output",
            "command_exit_code",
            "engine_identity",
            "output_bytes",
            "output_sha256",
            "verified_date",
        },
        "toolchain derivation verification",
    )
    if verification["command_exit_code"] != 0 or verification["byte_equal_to_checked_output"] is not True:
        raise SystemExit("cprotect derivation verification did not pass")
    if verification["output_bytes"] != len(bound[style_path]) or verification["output_sha256"] != shared.digest_bytes(bound[style_path]):
        raise SystemExit("cprotect derivation output binding drift")

    return bound


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane-root", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    lane_root = args.lane_root.resolve()
    config_path = args.config.resolve()
    if config_path != lane_root and lane_root not in config_path.parents:
        raise SystemExit("toolchain config must be inside the lane root")
    config, config_bytes = asset_shared.load_json(config_path, "toolchain config")
    require_exact_keys(
        config,
        {
            "authority",
            "file_kind",
            "file_order",
            "recorded_date",
            "records",
            "schema_id",
            "schema_version",
            "spdx_mapping",
            "stable_keys",
        },
        "toolchain config",
    )
    if config["schema_id"] != CONFIG_SCHEMA_ID or config["schema_version"] != shared.SCHEMA_VERSION:
        raise SystemExit("unsupported toolchain config schema")
    if config["file_kind"] != "toolchain_authority" or not isinstance(config["file_order"], int):
        raise SystemExit("toolchain file kind/order drift")

    authority = config["authority"]
    if not isinstance(authority, dict):
        raise SystemExit("toolchain authority binding must be an object")
    require_exact_keys(authority, {"bytes", "path", "sha256"}, "toolchain authority binding")
    authority_path = asset_shared.resolve_relative(lane_root, authority["path"], "authority path")
    authority_bytes = asset_shared.require_bound_bytes(
        authority_path, authority["bytes"], authority["sha256"], "toolchain authority receipt"
    )
    try:
        receipt = json.loads(authority_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(f"cannot decode toolchain authority receipt: {error}") from error
    if not isinstance(receipt, dict):
        raise SystemExit("toolchain authority receipt root must be an object")
    bound_files = validate_receipt(lane_root, receipt)
    if config["recorded_date"] != receipt["recorded_date"]:
        raise SystemExit("config/receipt recorded_date drift")

    spdx = config["spdx_mapping"]
    if not isinstance(spdx, dict):
        raise SystemExit("SPDX mapping must be an object")
    require_exact_keys(
        spdx,
        {"authority_url", "backend_expression", "license_id", "receipt_expression"},
        "SPDX mapping",
    )
    expected_spdx = {
        "authority_url": "https://spdx.org/licenses/LPPL-1.3c.html",
        "backend_expression": EXPECTED_SPDX_EXPRESSION,
        "license_id": EXPECTED_SPDX_ID,
        "receipt_expression": EXPECTED_SPDX_EXPRESSION,
    }
    if spdx != expected_spdx or receipt["license"]["spdx_expression"] != spdx["receipt_expression"]:
        raise SystemExit("cprotect SPDX mapping drift")

    stable_keys = config["stable_keys"]
    if not isinstance(stable_keys, dict):
        raise SystemExit("toolchain stable keys must be an object")
    require_exact_keys(stable_keys, {"assets", "build_recipe", "rights"}, "toolchain stable keys")
    asset_keys = stable_keys["assets"]
    if not isinstance(asset_keys, dict):
        raise SystemExit("toolchain asset stable keys must be an object")
    require_exact_keys(asset_keys, {"archive", "installer", "source", "style"}, "toolchain asset stable keys")

    records = config["records"]
    if not isinstance(records, dict):
        raise SystemExit("toolchain records must be an object")
    require_exact_keys(records, {"assets", "build_recipe", "relations", "rights", "versions"}, "toolchain records")
    rights = records["rights"]
    assets = require_list(records["assets"], "toolchain assets", 4)
    versions = require_list(records["versions"], "toolchain versions", 4)
    recipe = records["build_recipe"]
    relations = require_list(records["relations"], "toolchain relations", 9)
    if not isinstance(rights, dict) or not isinstance(recipe, dict):
        raise SystemExit("toolchain rights/recipe records must be objects")
    require_exact_keys(rights, RIGHTS_KEYS, "toolchain rights record")
    require_exact_keys(recipe, RECIPE_KEYS, "toolchain build-recipe record")
    validate_record_base(rights, "ttna-rights-v1", "rights")
    validate_record_base(recipe, "ttna-build-recipe-v1", "build_recipe")
    for asset in assets:
        if not isinstance(asset, dict):
            raise SystemExit("toolchain asset record must be an object")
        require_exact_keys(asset, ASSET_KEYS, "toolchain asset record")
        validate_record_base(asset, "ttna-asset-v1", "asset")
    for version in versions:
        if not isinstance(version, dict):
            raise SystemExit("toolchain asset-version record must be an object")
        require_exact_keys(version, VERSION_KEYS, "toolchain asset-version record")
        validate_record_base(version, "ttna-asset-version-v1", "asset_version")
    for relation in relations:
        if not isinstance(relation, dict):
            raise SystemExit("toolchain relation record must be an object")
        require_exact_keys(relation, RELATION_KEYS, "toolchain relation record")
        validate_record_base(relation, "ttna-relation-v1", "relation")

    resource = asset_shared.resource_record()
    edition = asset_shared.edition_record(resource["id"])
    expected_rights_id = shared.stable_id("rights", stable_keys["rights"])
    if rights["id"] != expected_rights_id:
        raise SystemExit("toolchain rights stable-ID drift")
    if rights["authority_path"] != authority["path"] or rights["spdx_expression"] != EXPECTED_SPDX_EXPRESSION:
        raise SystemExit("toolchain rights authority/SPDX drift")
    if rights["maintenance_status"] != receipt["license"]["maintenance_status"] or rights["maintainer"] != receipt["license"]["maintainer"]:
        raise SystemExit("toolchain rights maintenance metadata drift")
    if rights["redistribution_permitted"] is not True or rights["preserve_complete_work_required"] is not True:
        raise SystemExit("toolchain redistribution safeguards drift")

    key_by_path = {value: name for name, value in asset_keys.items()}
    if len(key_by_path) != 4:
        raise SystemExit("toolchain asset stable keys are not unique")
    asset_by_id: dict[str, dict[str, Any]] = {}
    for asset in assets:
        logical_path = asset["logical_path"]
        if logical_path not in key_by_path:
            raise SystemExit(f"undeclared toolchain asset path {logical_path}")
        expected_id = shared.stable_id("asset", logical_path)
        if asset["id"] != expected_id:
            raise SystemExit(f"toolchain asset stable-ID drift for {logical_path}")
        if asset["resource_id"] != resource["id"] or asset["rights_id"] != rights["id"]:
            raise SystemExit(f"toolchain asset linkage drift for {logical_path}")
        if asset["component_name"] != "cprotect" or asset["component_version"] != "1.0f":
            raise SystemExit(f"toolchain asset component identity drift for {logical_path}")
        asset_by_id[asset["id"]] = asset
    if len(asset_by_id) != 4:
        raise SystemExit("duplicate toolchain asset IDs")

    expected_paths = set(asset_keys.values())
    if set(bound_files) != expected_paths | {
        "authority/toolchain/cprotect-1.0f/package/cprotect/README",
        "authority/toolchain/cprotect-1.0f/package/cprotect/cprotect.pdf",
    }:
        raise SystemExit("toolchain bound-file closure drift")
    version_by_id: dict[str, dict[str, Any]] = {}
    for version in versions:
        path_value = version["source_path"]
        if path_value not in expected_paths:
            raise SystemExit(f"undeclared toolchain version path {path_value}")
        asset = asset_by_id.get(version["asset_id"])
        if asset is None or asset["logical_path"] != path_value:
            raise SystemExit(f"toolchain asset-version linkage drift for {path_value}")
        payload = bound_files[path_value]
        payload_hash = shared.digest_bytes(payload)
        expected_id = shared.stable_id("asset_version", f"{asset['id']}|sha256:{payload_hash}")
        if version["id"] != expected_id:
            raise SystemExit(f"toolchain asset-version stable-ID drift for {path_value}")
        if version["edition_id"] != edition["id"] or version["rights_id"] != rights["id"]:
            raise SystemExit(f"toolchain asset-version foreign-key drift for {path_value}")
        if version["authority_path"] != authority["path"]:
            raise SystemExit(f"toolchain asset-version authority drift for {path_value}")
        if version["source_bytes"] != len(payload) or version["source_sha256"] != payload_hash:
            raise SystemExit(f"toolchain asset-version source binding drift for {path_value}")
        if version["normalization_id"] != "binary-identity-v1" or version["normalized_bytes"] != len(payload) or version["normalized_sha256"] != payload_hash:
            raise SystemExit(f"toolchain asset-version normalization drift for {path_value}")
        if not isinstance(version["provenance"], dict) or not version["provenance"]:
            raise SystemExit(f"toolchain asset-version provenance missing for {path_value}")
        version_by_id[version["id"]] = version
    if len(version_by_id) != 4:
        raise SystemExit("duplicate toolchain asset-version IDs")

    expected_recipe_id = shared.stable_id("build_recipe", stable_keys["build_recipe"])
    if recipe["id"] != expected_recipe_id:
        raise SystemExit("toolchain build-recipe stable-ID drift")
    if recipe["resource_id"] != resource["id"] or recipe["edition_id"] != edition["id"] or recipe["rights_id"] != rights["id"]:
        raise SystemExit("toolchain build-recipe foreign-key drift")
    inputs = validate_uuid_array(recipe["input_asset_version_ids"], "build-recipe inputs")
    outputs = validate_uuid_array(recipe["output_asset_version_ids"], "build-recipe outputs")
    version_by_path = {item["source_path"]: item for item in versions}
    expected_inputs = [
        version_by_path[asset_keys["source"]]["id"],
        version_by_path[asset_keys["installer"]]["id"],
    ]
    expected_outputs = [version_by_path[asset_keys["style"]]["id"]]
    if inputs != expected_inputs or outputs != expected_outputs:
        raise SystemExit("toolchain build-recipe input/output drift")
    if recipe["command"] != receipt["derivation"]["command"] or recipe["source_instruction"] != {
        "path": receipt["derivation"]["declared_by_path"],
        "line_range": receipt["derivation"]["declared_by_line_range"],
        "sha256": shared.digest_bytes(bound_files[receipt["derivation"]["declared_by_path"]]),
    }:
        raise SystemExit("toolchain build-recipe evidence drift")
    if recipe["verification"] != {
        "byte_exact": True,
        "engine_identity": receipt["derivation"]["verification"]["engine_identity"],
        "exit_code": 0,
        "verified_date": receipt["derivation"]["verification"]["verified_date"],
    }:
        raise SystemExit("toolchain build-recipe verification drift")

    expected_triples: set[tuple[str, str, str]] = set()
    for version in versions:
        expected_triples.add((version["id"], "version_of", version["asset_id"]))
    archive_version = version_by_path[asset_keys["archive"]]["id"]
    source_version = version_by_path[asset_keys["source"]]["id"]
    installer_version = version_by_path[asset_keys["installer"]]["id"]
    style_version = version_by_path[asset_keys["style"]]["id"]
    expected_triples.update(
        {
            (source_version, "extracted_from", archive_version),
            (installer_version, "generated_from", source_version),
            (style_version, "generated_from", source_version),
            (style_version, "generated_from", installer_version),
            (style_version, "generated_by", recipe["id"]),
        }
    )
    actual_triples: set[tuple[str, str, str]] = set()
    known_ids = set(asset_by_id) | set(version_by_id) | {rights["id"], recipe["id"], resource["id"], edition["id"]}
    for relation in relations:
        triple = (relation["from_id"], relation["relation"], relation["to_id"])
        if triple in actual_triples:
            raise SystemExit(f"duplicate toolchain relation triple {triple}")
        actual_triples.add(triple)
        expected_id = shared.stable_id("relation", "|".join(triple))
        if relation["id"] != expected_id:
            raise SystemExit(f"toolchain relation stable-ID drift for {triple}")
        if relation["from_id"] not in known_ids or relation["to_id"] not in known_ids:
            raise SystemExit(f"toolchain relation endpoint does not resolve for {triple}")
    if actual_triples != expected_triples:
        raise SystemExit("toolchain provenance relation set drift")

    output_groups: list[tuple[Path, list[dict[str, Any]]]] = [
        (args.out / "authority" / "resources.jsonl", [resource]),
        (args.out / "authority" / "editions.jsonl", [edition]),
        (args.out / "rights" / "components.jsonl", [rights]),
        (args.out / "assets" / "assets.jsonl", assets),
        (args.out / "assets" / "versions.jsonl", versions),
        (args.out / "build" / "recipes.jsonl", [recipe]),
        (args.out / "topology" / "relations.jsonl", relations),
    ]
    shared.validate_local_relation_closure(output_groups)
    expected_jsonl = {path.relative_to(args.out).as_posix() for path, _ in output_groups}
    existing_jsonl = {
        path.relative_to(args.out).as_posix() for path in args.out.rglob("*.jsonl")
    } if args.out.exists() else set()
    unexpected_jsonl = sorted(existing_jsonl - expected_jsonl)
    if unexpected_jsonl:
        raise SystemExit("toolchain output contains unexpected JSONL: " + ", ".join(unexpected_jsonl))

    if config_path.read_bytes() != config_bytes:
        raise SystemExit("toolchain config changed during generation")
    if authority_path.read_bytes() != authority_bytes:
        raise SystemExit("toolchain authority receipt changed during generation")
    for path_value, payload in bound_files.items():
        path = asset_shared.resolve_relative(lane_root, path_value, "bound file path")
        if path.read_bytes() != payload:
            raise SystemExit(f"toolchain bound file changed during generation: {path_value}")
    for path, group in output_groups:
        shared.write_jsonl(path, group)

    files: list[dict[str, Any]] = []
    for path, group in output_groups:
        payload = path.read_bytes()
        files.append(
            {
                "path": path.relative_to(args.out).as_posix(),
                "bytes": len(payload),
                "sha256": shared.digest_bytes(payload),
                "records": len(group),
            }
        )
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
        "source_role": "release_toolchain_authority",
        "config_path": config_path.relative_to(lane_root).as_posix(),
        "config_sha256": shared.digest_bytes(config_bytes),
        "authority_sha256": shared.digest_bytes(authority_bytes),
        "admission": receipt["admission"],
        "files": sorted(files, key=lambda item: item["path"]),
        "counts": {
            "resources": 1,
            "editions": 1,
            "rights": 1,
            "assets": 4,
            "asset_versions": 4,
            "build_recipes": 1,
            "relations": 9,
        },
    }
    shared.write_json(args.out / "manifests" / "lane_manifest.json", manifest)
    print(shared.canonical(manifest))


if __name__ == "__main__":
    main()
