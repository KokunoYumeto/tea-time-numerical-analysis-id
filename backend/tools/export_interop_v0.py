#!/usr/bin/env python3
"""Deterministic, open Interoperability Envelope v0 exports and selections."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "0.1.0"
EXPORTER_VERSION = "ttna-interoperability-v0-exporter-0.1.0"
FOLLOW_OUTBOUND = {
    "built_from",
    "covers_concept",
    "denotes",
    "documented_revision_of",
    "exact_excerpt_of",
    "extracted_from",
    "generated_by",
    "generated_from",
    "normalized_equivalent_to",
    "supersedes",
    "uses",
    "uses_resource",
    "uses_term",
    "version_of",
}
FOLLOW_INBOUND = {
    "corrects",
    "defined_by",
    "expected_output",
    "parameterized_by_evidence",
    "presented_by",
    "scoped_to",
    "translates",
}
REVERSE_FOREIGN_KEY_TYPES = {"correction", "experiment", "localization", "qa_event"}
REVERSE_DEPENDENCY_FIELDS = {
    "correction": ("affected_source_file_ids", "affected_unit_ids"),
    "experiment": ("source_file_id", "unit_id"),
    "localization": ("segment_id",),
    "qa_event": ("source_file_id",),
}


class ExportError(ValueError):
    """Fail-closed export or selection error."""


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(records, key=lambda record: record["id"])
    payload = "".join(canonical(record) + "\n" for record in ordered).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return {"path": path.name, "records": len(ordered), "bytes": len(payload), "sha256": sha256(payload)}


def parse_jsonl_bytes(payload: bytes, label: str) -> list[dict[str, Any]]:
    if payload.startswith(b"\xef\xbb\xbf") or b"\r" in payload:
        raise ExportError(f"{label} must be BOM-free UTF-8 with LF line endings")
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ExportError(f"{label} is not UTF-8: {error}") from error
    if payload and not text.endswith("\n"):
        raise ExportError(f"{label} must end with LF")
    records: list[dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), 1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ExportError(f"invalid JSON in {label}:{number}: {error}") from error
        if not isinstance(record, dict):
            raise ExportError(f"non-object record in {label}:{number}")
        records.append(record)
    return records


def index_records(records: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str):
            raise ExportError("record missing string id")
        prior = by_id.get(record_id)
        if prior is not None and canonical(prior) != canonical(record):
            raise ExportError(f"nonidentical duplicate ID: {record_id}")
        by_id[record_id] = record
    return by_id


def load_records_from_manifest(manifest_path: Path) -> dict[str, dict[str, Any]]:
    try:
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ExportError(f"cannot read source manifest {manifest_path}: {error}") from error
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ExportError("source manifest files must be an array")
    data_root = manifest_path.parent.parent
    all_records: list[dict[str, Any]] = []
    for row in files:
        path = data_root / row["path"]
        try:
            payload = path.read_bytes()
        except OSError as error:
            raise ExportError(f"cannot read manifested file {path}: {error}") from error
        actual = (len(payload), sha256(payload))
        expected = (row["bytes"], row["sha256"])
        if actual != expected:
            raise ExportError(
                f"one-byte/source drift for {path}: expected {expected[0]} bytes/{expected[1]}, "
                f"got {actual[0]} bytes/{actual[1]}"
            )
        records = parse_jsonl_bytes(payload, str(path))
        if len(records) != row["records"]:
            raise ExportError(f"record-count drift for {path}")
        all_records.extend(records)
    by_id = index_records(all_records)
    expected_total = manifest.get("total_unique_records")
    if expected_total is not None and len(by_id) != expected_total:
        raise ExportError(
            f"source manifest unique-count drift: {len(by_id)} != {expected_total}"
        )
    return by_id


def csv_payload(records: list[dict[str, Any]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["id", "record_type", "record_json"])
    for record in records:
        writer.writerow([record["id"], record["record_type"], canonical(record)])
    return stream.getvalue().encode("utf-8")


def parse_csv_payload(payload: bytes, label: str) -> list[dict[str, Any]]:
    if payload.startswith(b"\xef\xbb\xbf") or b"\r" in payload:
        raise ExportError(f"{label} must be BOM-free UTF-8 with LF line endings")
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ExportError(f"{label} is not UTF-8: {error}") from error
    rows = csv.DictReader(io.StringIO(text, newline=""))
    if rows.fieldnames != ["id", "record_type", "record_json"]:
        raise ExportError(f"unexpected CSV columns in {label}: {rows.fieldnames}")
    records: list[dict[str, Any]] = []
    for number, row in enumerate(rows, 2):
        try:
            record = json.loads(row["record_json"])
        except json.JSONDecodeError as error:
            raise ExportError(f"invalid record_json at {label}:{number}: {error}") from error
        if record.get("id") != row["id"] or record.get("record_type") != row["record_type"]:
            raise ExportError(f"CSV projection mismatch at {label}:{number}")
        records.append(record)
    return records


def verify_round_trip(jsonl_path: Path, csv_path: Path) -> dict[str, Any]:
    jsonl_bytes = jsonl_path.read_bytes()
    csv_bytes = csv_path.read_bytes()
    jsonl_records = parse_jsonl_bytes(jsonl_bytes, str(jsonl_path))
    csv_records = parse_csv_payload(csv_bytes, str(csv_path))
    jsonl_canonical = [canonical(record) for record in jsonl_records]
    csv_canonical = [canonical(record) for record in csv_records]
    if jsonl_canonical != csv_canonical:
        raise ExportError("JSONL/CSV round trip is not lossless or order-stable")
    if jsonl_canonical != sorted(jsonl_canonical, key=lambda line: json.loads(line)["id"]):
        raise ExportError("export records are not sorted by stable ID")
    return {
        "records": len(jsonl_records),
        "semantic_sha256": sha256(("\n".join(jsonl_canonical) + "\n").encode("utf-8")),
        "jsonl_sha256": sha256(jsonl_bytes),
        "csv_sha256": sha256(csv_bytes),
        "round_trip_equal": True,
        "utf8_lf": True,
    }


def portable_locator(path: Path) -> str:
    """Prefer a workspace-relative public locator without changing identity."""
    resolved = path.resolve()
    try:
        return resolved.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def export_lane(manifest_path: Path, schema_path: Path, out: Path) -> dict[str, Any]:
    by_id = load_records_from_manifest(manifest_path)
    ordered = sorted(by_id.values(), key=lambda record: record["id"])
    jsonl_row = write_jsonl(out / "records.jsonl", ordered)
    csv_bytes = csv_payload(ordered)
    (out / "records.csv").parent.mkdir(parents=True, exist_ok=True)
    (out / "records.csv").write_bytes(csv_bytes)
    csv_row = {
        "path": "records.csv",
        "records": len(ordered),
        "bytes": len(csv_bytes),
        "sha256": sha256(csv_bytes),
    }
    round_trip = verify_round_trip(out / "records.jsonl", out / "records.csv")
    manifest_bytes = manifest_path.read_bytes()
    schema_bytes = schema_path.read_bytes()
    counts = Counter(record["record_type"] for record in ordered)
    export_manifest = {
        "schema_id": "ttna-interoperability-export-v0",
        "schema_version": SCHEMA_VERSION,
        "exporter": EXPORTER_VERSION,
        "encoding": "UTF-8",
        "line_endings": "LF",
        "ordering": "record.id ascending; canonical JSON object keys ascending",
        "source_manifest": {
            "path": portable_locator(manifest_path),
            "bytes": len(manifest_bytes),
            "sha256": sha256(manifest_bytes),
        },
        "record_schema": {
            "path": portable_locator(schema_path),
            "bytes": len(schema_bytes),
            "sha256": sha256(schema_bytes),
        },
        "outputs": [jsonl_row, csv_row],
        "record_counts": dict(sorted(counts.items())),
        "total_unique_records": len(ordered),
        "round_trip": round_trip,
        "proprietary_services_required": False,
    }
    write_json(out / "manifest.json", export_manifest)
    return export_manifest


def urn_references(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, str):
        if value.startswith("urn:uuid:"):
            refs.add(value)
    elif isinstance(value, list):
        for item in value:
            refs.update(urn_references(item))
    elif isinstance(value, dict):
        for key, item in value.items():
            if key != "id":
                refs.update(urn_references(item))
    return refs


def reverse_dependency_references(record: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    for field in REVERSE_DEPENDENCY_FIELDS.get(record.get("record_type"), ()):
        refs.update(urn_references(record.get(field)))
    return refs


def select_dependency_closed(
    by_id: dict[str, dict[str, Any]], root_unit_ids: list[str]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    for root_id in root_unit_ids:
        record = by_id.get(root_id)
        if record is None or record.get("record_type") != "unit":
            raise ExportError(f"selection root is not a unit: {root_id}")
    relations = [record for record in by_id.values() if record.get("record_type") == "relation"]
    out_rel: dict[str, list[dict[str, Any]]] = defaultdict(list)
    in_rel: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in relations:
        out_rel[row["from_id"]].append(row)
        in_rel[row["to_id"]].append(row)
    reverse_refs: dict[str, set[str]] = defaultdict(set)
    for record in by_id.values():
        if record.get("record_type") in REVERSE_FOREIGN_KEY_TYPES:
            for ref in reverse_dependency_references(record):
                if ref in by_id:
                    reverse_refs[ref].add(record["id"])

    selected: set[str] = set(root_unit_ids)
    content_units: set[str] = set(root_unit_ids)
    content_segments: set[str] = set()
    context_units: set[str] = set()
    selected_relations: set[str] = set()

    content_queue = deque(root_unit_ids)
    while content_queue:
        source_id = content_queue.popleft()
        for row in out_rel.get(source_id, []):
            if row.get("relation") != "contains":
                continue
            target = by_id[row["to_id"]]
            if target.get("record_type") not in {"unit", "segment"}:
                continue
            selected_relations.add(row["id"])
            selected.add(target["id"])
            if target["record_type"] == "unit" and target["id"] not in content_units:
                content_units.add(target["id"])
                content_queue.append(target["id"])
            elif target["record_type"] == "segment":
                content_segments.add(target["id"])

    selected.update(selected_relations)
    changed = True
    while changed:
        changed = False
        snapshot = list(selected)
        for record_id in snapshot:
            record = by_id[record_id]
            for ref in urn_references(record):
                if ref in by_id and ref not in selected:
                    selected.add(ref)
                    if by_id[ref].get("record_type") == "unit":
                        context_units.add(ref)
                    changed = True
            for reverse_id in reverse_refs.get(record_id, set()):
                if reverse_id not in selected:
                    selected.add(reverse_id)
                    changed = True
            for row in out_rel.get(record_id, []):
                rel_type = row.get("relation")
                if rel_type in FOLLOW_OUTBOUND:
                    if row["to_id"] not in selected:
                        selected.add(row["to_id"])
                        changed = True
                    if row["id"] not in selected_relations:
                        selected_relations.add(row["id"])
                        selected.add(row["id"])
                        changed = True
            for row in in_rel.get(record_id, []):
                rel_type = row.get("relation")
                if rel_type in FOLLOW_INBOUND or (
                    rel_type == "contains"
                    and by_id[row["from_id"]].get("record_type") in {"course", "program", "unit"}
                ):
                    if row["from_id"] not in selected:
                        selected.add(row["from_id"])
                        if by_id[row["from_id"]].get("record_type") == "unit":
                            context_units.add(row["from_id"])
                        changed = True
                    if row["id"] not in selected_relations:
                        selected_relations.add(row["id"])
                        selected.add(row["id"])
                        changed = True
        for row in relations:
            if (
                row["from_id"] in selected
                and row["to_id"] in selected
                and row["id"] not in selected
            ):
                selected_relations.add(row["id"])
                selected.add(row["id"])
                changed = True
    for row in relations:
        if row["id"] in selected and (row["from_id"] not in selected or row["to_id"] not in selected):
            raise ExportError(f"selection has dangling relation: {row['id']}")
    unresolved = sorted(
        {
            ref
            for record_id in selected
            for ref in urn_references(by_id[record_id])
            if ref not in selected
        }
    )
    if unresolved:
        raise ExportError(f"selection has unresolved foreign keys: {unresolved[:3]}")
    selected_records = sorted((by_id[record_id] for record_id in selected), key=lambda r: r["id"])
    proof = {
        "root_unit_ids": sorted(root_unit_ids),
        "content_unit_ids": sorted(content_units),
        "content_segment_ids": sorted(content_segments),
        "context_unit_ids": sorted(context_units - content_units),
        "followed_outbound_relation_types": sorted(FOLLOW_OUTBOUND),
        "followed_inbound_relation_types": sorted(FOLLOW_INBOUND),
        "reverse_foreign_key_record_types": sorted(REVERSE_FOREIGN_KEY_TYPES),
        "all_emitted_relation_endpoints_present": True,
        "all_foreign_keys_resolve": True,
        "unresolved_dependencies": [],
    }
    return selected_records, proof


def load_export_records(records_path: Path, manifest_path: Path | None) -> dict[str, dict[str, Any]]:
    payload = records_path.read_bytes()
    if manifest_path is not None:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        rows = [row for row in manifest.get("outputs", []) if row.get("path") == records_path.name]
        if len(rows) != 1:
            raise ExportError(f"export manifest does not identify {records_path.name}")
        expected = (rows[0]["bytes"], rows[0]["sha256"])
        actual = (len(payload), sha256(payload))
        if actual != expected:
            raise ExportError(f"export record drift: {actual} != {expected}")
    return index_records(parse_jsonl_bytes(payload, str(records_path)))


def select_command(
    records_path: Path,
    export_manifest_path: Path | None,
    unit_ids: list[str],
    unit_source_local_ids: list[str],
    out: Path,
) -> dict[str, Any]:
    by_id = load_export_records(records_path, export_manifest_path)
    roots = list(unit_ids)
    for local_id in unit_source_local_ids:
        matches = [
            record["id"]
            for record in by_id.values()
            if record.get("record_type") == "unit" and record.get("source_local_id") == local_id
        ]
        if len(matches) != 1:
            raise ExportError(f"unit source-local ID {local_id!r} matched {len(matches)} records")
        roots.append(matches[0])
    roots = sorted(set(roots))
    if not roots:
        raise ExportError("select requires at least one unit root")
    selected, proof = select_dependency_closed(by_id, roots)
    records_row = write_jsonl(out / "records.jsonl", selected)
    payload = (out / "records.jsonl").read_bytes()
    counts = Counter(record["record_type"] for record in selected)
    source_payload = records_path.read_bytes()
    manifest = {
        "schema_id": "ttna-dependency-closed-selection-v0",
        "schema_version": SCHEMA_VERSION,
        "exporter": EXPORTER_VERSION,
        "source_records": {
            "path": portable_locator(records_path),
            "bytes": len(source_payload),
            "sha256": sha256(source_payload),
        },
        "selection": proof,
        "output": records_row,
        "record_counts": dict(sorted(counts.items())),
        "total_unique_records": len(selected),
        "semantic_sha256": sha256(payload),
        "proprietary_services_required": False,
    }
    write_json(out / "manifest.json", manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    export = sub.add_parser("export")
    export.add_argument("--manifest", required=True, type=Path)
    export.add_argument("--schema", required=True, type=Path)
    export.add_argument("--out", required=True, type=Path)

    verify = sub.add_parser("verify-round-trip")
    verify.add_argument("--jsonl", required=True, type=Path)
    verify.add_argument("--csv", required=True, type=Path)

    select = sub.add_parser("select")
    select.add_argument("--records", required=True, type=Path)
    select.add_argument("--export-manifest", type=Path)
    select.add_argument("--unit-id", action="append", default=[])
    select.add_argument("--unit-source-local-id", action="append", default=[])
    select.add_argument("--out", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        if args.command == "export":
            result = export_lane(args.manifest.resolve(), args.schema.resolve(), args.out.resolve())
        elif args.command == "verify-round-trip":
            result = verify_round_trip(args.jsonl.resolve(), args.csv.resolve())
        else:
            result = select_command(
                args.records.resolve(),
                args.export_manifest.resolve() if args.export_manifest else None,
                args.unit_id,
                args.unit_source_local_id,
                args.out.resolve(),
            )
        print(canonical(result))
    except (ExportError, OSError, KeyError, TypeError, csv.Error, json.JSONDecodeError) as error:
        print(f"interoperability-v0 export error: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
