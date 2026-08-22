#!/usr/bin/env python3
"""Merge deterministic per-file backend packs into one canonical lane view."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def canonical(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(canonical(item) + "\n" for item in sorted(records, key=lambda item: item["id"]))
    path.write_text(payload, encoding="utf-8", newline="\n")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def require_typed_target(
    record: dict[str, Any],
    field: str,
    expected_type: str,
    by_id: dict[str, dict[str, Any]],
) -> None:
    target_id = record.get(field)
    if not isinstance(target_id, str):
        raise SystemExit(f"{record['id']} missing typed foreign key {field}")
    target = by_id.get(target_id)
    if target is None:
        raise SystemExit(f"{record['id']} unresolved foreign key {field}: {target_id}")
    if target["record_type"] != expected_type:
        raise SystemExit(
            f"{record['id']} {field} targets {target['record_type']}, expected {expected_type}"
        )


def require_typed_targets(
    record: dict[str, Any],
    field: str,
    expected_type: str,
    by_id: dict[str, dict[str, Any]],
    required: bool = True,
) -> None:
    values = record.get(field)
    if values is None and not required:
        return
    if not isinstance(values, list) or (required and not values):
        raise SystemExit(f"{record['id']} missing typed foreign-key array {field}")
    if len(values) != len(set(values)):
        raise SystemExit(f"{record['id']} has duplicate foreign keys in {field}")
    for target_id in values:
        target = by_id.get(target_id)
        if target is None:
            raise SystemExit(f"{record['id']} unresolved foreign key {field}: {target_id}")
        if target["record_type"] != expected_type:
            raise SystemExit(
                f"{record['id']} {field} targets {target['record_type']}, expected {expected_type}"
            )


def validate_evidence_layer_types(by_id: dict[str, dict[str, Any]]) -> None:
    relation_types: dict[str, set[tuple[str, str]]] = {
        "version_of": {("asset_version", "asset")},
        "normalized_equivalent_to": {("segment", "asset_version")},
        "exact_excerpt_of": {("segment", "asset_version")},
        "documented_revision_of": {("segment", "asset_version")},
        "scoped_to": {("experiment", "unit")},
        "defined_by": {("experiment", "segment")},
        "uses": {("experiment", "asset_version")},
        "presented_by": {("experiment", "segment")},
        "expected_output": {("experiment", "segment")},
        "parameterized_by_evidence": {("experiment", "segment")},
        "extracted_from": {("asset_version", "asset_version")},
        "generated_from": {("asset_version", "asset_version")},
        "generated_by": {("asset_version", "build_recipe")},
        "contains": {
            ("program", "course"),
            ("course", "unit"),
            ("unit", "unit"),
            ("unit", "segment"),
        },
        "uses_resource": {("course", "resource")},
        "denotes": {("term", "concept")},
        "covers_concept": {("unit", "concept")},
        "built_from": {("artifact", "edition")},
        "corrects": {("correction", "source_file"), ("correction", "unit")},
        "supersedes": {("artifact", "artifact"), ("correction", "correction")},
    }
    for record in by_id.values():
        record_type = record["record_type"]
        if record_type == "asset":
            require_typed_target(record, "resource_id", "resource", by_id)
            require_typed_target(record, "rights_id", "rights", by_id)
        elif record_type == "asset_version":
            require_typed_target(record, "asset_id", "asset", by_id)
            require_typed_target(record, "edition_id", "edition", by_id)
            require_typed_target(record, "rights_id", "rights", by_id)
        elif record_type == "experiment":
            require_typed_target(record, "resource_id", "resource", by_id)
            require_typed_target(record, "edition_id", "edition", by_id)
            require_typed_target(record, "source_file_id", "source_file", by_id)
            require_typed_target(record, "unit_id", "unit", by_id)
            require_typed_targets(record, "instruction_segment_ids", "segment", by_id)
            require_typed_targets(record, "runner_segment_ids", "segment", by_id)
            require_typed_targets(
                record, "runner_asset_version_ids", "asset_version", by_id
            )
            require_typed_targets(
                record,
                "expected_output_segment_ids",
                "segment",
                by_id,
                required=False,
            )
            require_typed_targets(
                record,
                "parameter_evidence_segment_ids",
                "segment",
                by_id,
                required=False,
            )
            require_typed_targets(record, "rights_ids", "rights", by_id)
        elif record_type == "build_recipe":
            require_typed_target(record, "resource_id", "resource", by_id)
            require_typed_target(record, "edition_id", "edition", by_id)
            require_typed_target(record, "rights_id", "rights", by_id)
            require_typed_targets(
                record, "input_asset_version_ids", "asset_version", by_id
            )
            require_typed_targets(
                record, "output_asset_version_ids", "asset_version", by_id
            )
        elif record_type == "relation":
            for evidence_id in record.get("evidence_segment_ids", []):
                target = by_id.get(evidence_id)
                if target is None or target["record_type"] != "segment":
                    raise SystemExit(
                        f"{record['id']} has unresolved or mistyped evidence segment {evidence_id}"
                    )
            allowed = relation_types.get(record["relation"])
            if allowed is not None:
                from_record = by_id[record["from_id"]]
                to_record = by_id[record["to_id"]]
                actual = (from_record["record_type"], to_record["record_type"])
                if actual not in allowed:
                    expected = ", ".join(
                        f"{source}->{target}" for source, target in sorted(allowed)
                    )
                    raise SystemExit(
                        f"{record['id']} relation {record['relation']} has endpoint types "
                        f"{from_record['record_type']}->{to_record['record_type']}, "
                        f"expected one of {expected}"
                    )


def require_exact_digest_fields(record: dict[str, Any], context: str) -> None:
    value = record.get("bytes")
    digest = record.get("sha256")
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise SystemExit(f"{record['id']} invalid byte count in {context}")
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
    ):
        raise SystemExit(f"{record['id']} invalid SHA-256 in {context}")


def validate_interoperability_v0_types(by_id: dict[str, dict[str, Any]]) -> None:
    for record in by_id.values():
        record_type = record["record_type"]
        if record_type == "program":
            require_typed_target(record, "resource_id", "resource", by_id)
            require_typed_target(record, "edition_id", "edition", by_id)
            require_typed_targets(record, "course_ids", "course", by_id)
        elif record_type == "course":
            require_typed_target(record, "program_id", "program", by_id)
            require_typed_target(record, "resource_id", "resource", by_id)
            require_typed_target(record, "edition_id", "edition", by_id)
            require_typed_targets(record, "root_unit_ids", "unit", by_id)
            require_typed_targets(
                record, "prerequisite_course_ids", "course", by_id, required=False
            )
        elif record_type == "concept":
            require_typed_target(record, "resource_id", "resource", by_id)
            require_typed_target(record, "edition_id", "edition", by_id)
            require_typed_target(record, "evidence_term_id", "term", by_id)
            if record.get("locale_neutral") is not True:
                raise SystemExit(f"{record['id']} concept is not explicitly locale-neutral")
        elif record_type == "artifact":
            require_typed_target(record, "program_id", "program", by_id)
            require_typed_target(record, "course_id", "course", by_id)
            require_typed_target(record, "resource_id", "resource", by_id)
            require_typed_target(record, "edition_id", "edition", by_id)
            require_typed_targets(record, "rights_ids", "rights", by_id)
            require_exact_digest_fields(record, "artifact")
            receipt = record.get("build_receipt")
            if not isinstance(receipt, dict):
                raise SystemExit(f"{record['id']} missing build receipt")
            receipt_record = {"id": record["id"], **receipt}
            require_exact_digest_fields(receipt_record, "artifact build receipt")
            toolchain = record.get("toolchain")
            required_toolchain = {
                "lyx_product_version",
                "lyx_bytes",
                "lyx_sha256",
                "latexmk_sha256",
                "cprotect_sty_sha256",
                "identity_source",
            }
            if not isinstance(toolchain, dict) or not required_toolchain.issubset(toolchain):
                raise SystemExit(f"{record['id']} incomplete artifact toolchain identity")
        elif record_type == "correction":
            require_typed_target(record, "resource_id", "resource", by_id)
            require_typed_target(record, "edition_id", "edition", by_id)
            require_typed_targets(
                record, "affected_source_file_ids", "source_file", by_id, required=False
            )
            require_typed_targets(
                record, "affected_unit_ids", "unit", by_id, required=False
            )
            ledger = record.get("source_ledger")
            if not isinstance(ledger, dict):
                raise SystemExit(f"{record['id']} missing correction source ledger")
            ledger_record = {"id": record["id"], **ledger}
            require_exact_digest_fields(ledger_record, "correction source ledger")
            if not isinstance(record.get("status"), str) or not record["status"]:
                raise SystemExit(f"{record['id']} missing correction status")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", action="append", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    by_path: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    global_by_id: dict[str, dict[str, Any]] = {}
    pack_rows: list[dict[str, Any]] = []

    for pack in args.pack:
        manifest_path = pack / "manifests" / "lane_manifest.json"
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes)
        pack_rows.append(
            {
                "path": pack.as_posix(),
                "scope": manifest["scope"],
                "file_order": manifest["file_order"],
                "manifest_bytes": len(manifest_bytes),
                "manifest_sha256": sha256(manifest_bytes),
            }
        )
        for path in sorted(pack.rglob("*.jsonl"), key=lambda item: item.relative_to(pack).as_posix()):
            rel = path.relative_to(pack).as_posix()
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                record = json.loads(line)
                record_id = record["id"]
                existing = global_by_id.get(record_id)
                if existing is not None and canonical(existing) != canonical(record):
                    raise SystemExit(
                        f"stable-ID collision with nonidentical records: {record_id} "
                        f"at {path}:{line_number}"
                    )
                global_by_id[record_id] = record
                prior = by_path[rel].get(record_id)
                if prior is not None and canonical(prior) != canonical(record):
                    raise SystemExit(f"path-local duplicate mismatch: {rel} {record_id}")
                by_path[rel][record_id] = record

    known_ids = set(global_by_id)
    relations = [record for record in global_by_id.values() if record["record_type"] == "relation"]
    for relation in relations:
        if relation["from_id"] not in known_ids or relation["to_id"] not in known_ids:
            raise SystemExit(f"unresolved relation: {relation['id']}")
    validate_evidence_layer_types(global_by_id)
    validate_interoperability_v0_types(global_by_id)

    output_rows: list[dict[str, Any]] = []
    for rel, index in sorted(by_path.items()):
        path = args.out / rel
        records = list(index.values())
        write_jsonl(path, records)
        payload = path.read_bytes()
        output_rows.append(
            {
                "path": rel,
                "records": len(records),
                "bytes": len(payload),
                "sha256": sha256(payload),
            }
        )

    counts = Counter(record["record_type"] for record in global_by_id.values())
    manifest = {
        "schema_id": "ttna-combined-lane-manifest-v1",
        "schema_version": "1.0.0",
        "generator": "ttna-pack-merger-0.3.0",
        "source_commit": "186882108a6da95c8dca5b81ce000fc3f8f3ca21",
        "source_tree": "1e50d3756b695176008c602f0ee89712f5f32d10",
        "locale": "id-ID",
        "packs": sorted(pack_rows, key=lambda item: item["file_order"]),
        "files": output_rows,
        "record_counts": dict(sorted(counts.items())),
        "total_unique_records": len(global_by_id),
        "all_relation_endpoints_resolve": True,
    }
    write_json(args.out / "manifests" / "lane_manifest.json", manifest)
    print(canonical(manifest))


if __name__ == "__main__":
    main()
