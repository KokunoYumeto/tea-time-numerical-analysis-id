#!/usr/bin/env python3
"""Generate the deterministic R015 Interoperability Envelope v0 pack.

The generator deliberately reads only the packs named by the current combined
manifest (excluding its own output), the exact task receipt, the bounded
adverse ledger, and explicitly configured artifact/build-manifest pairs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import uuid
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "1.0.0"
CONFIG_SCHEMA_ID = "ttna-interoperability-v0-config-v1"
GENERATOR_VERSION = "ttna-interoperability-v0-indexer-0.1.0"
RESOURCE_URL = "https://github.com/lqbrin/tea-time-numerical"
RESOURCE_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, RESOURCE_URL)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SOURCE_FILE_TOKEN = re.compile(r"(?i)([A-Za-z0-9_.-]+\.(?:lyx|tex))")


class InteropError(ValueError):
    """Fail-closed validation error for v0 inputs."""


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_id(kind: str, key: str) -> str:
    return "urn:uuid:" + str(uuid.uuid5(RESOURCE_NAMESPACE, f"{kind}|{key}"))


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InteropError(f"cannot read JSON {path}: {error}") from error
    if not isinstance(value, dict):
        raise InteropError(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(records, key=lambda item: item["id"])
    payload = "".join(canonical(record) + "\n" for record in ordered).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return {
        "path": path.as_posix(),
        "records": len(ordered),
        "bytes": len(payload),
        "sha256": sha256(payload),
    }


def exact_file(lane_root: Path, spec: dict[str, Any], label: str) -> tuple[Path, bytes]:
    for field in ("path", "bytes", "sha256"):
        if field not in spec:
            raise InteropError(f"{label} missing {field}")
    path = lane_root / spec["path"]
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise InteropError(f"cannot read {label} {path}: {error}") from error
    expected_hash = spec["sha256"]
    if not isinstance(expected_hash, str) or not HEX64.fullmatch(expected_hash):
        raise InteropError(f"{label} has invalid configured sha256")
    actual = sha256(payload)
    if len(payload) != spec["bytes"] or actual != expected_hash:
        raise InteropError(
            f"{label} exact-byte drift: expected {spec['bytes']} bytes/{expected_hash}, "
            f"got {len(payload)} bytes/{actual}"
        )
    return path, payload


def merge_record(index: dict[str, dict[str, Any]], record: dict[str, Any], source: Path) -> None:
    record_id = record.get("id")
    if not isinstance(record_id, str):
        raise InteropError(f"record without string id in {source}")
    existing = index.get(record_id)
    if existing is not None and canonical(existing) != canonical(record):
        raise InteropError(f"nonidentical stable-ID collision {record_id} in {source}")
    index[record_id] = record


def load_dependency_records(
    lane_root: Path, source_manifest_rel: str, output_pack_rel: str
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    manifest = read_json(lane_root / source_manifest_rel)
    packs = manifest.get("packs")
    if not isinstance(packs, list) or not packs:
        raise InteropError("source manifest has no pack inventory")
    output_resolved = (lane_root / output_pack_rel).resolve()
    records: dict[str, dict[str, Any]] = {}
    used_packs: list[str] = []
    for row in sorted(packs, key=lambda item: (item["file_order"], item["path"])):
        pack = (lane_root / row["path"]).resolve()
        if pack == output_resolved:
            continue
        if not pack.is_relative_to(lane_root.resolve()):
            raise InteropError(f"pack escapes lane root: {pack}")
        manifest_path = pack / "manifests" / "lane_manifest.json"
        if not manifest_path.is_file():
            raise InteropError(f"missing dependency pack manifest: {manifest_path}")
        used_packs.append(pack.relative_to(lane_root.resolve()).as_posix())
        for path in sorted(pack.rglob("*.jsonl"), key=lambda p: p.relative_to(pack).as_posix()):
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError) as error:
                raise InteropError(f"cannot read dependency JSONL {path}: {error}") from error
            for line_number, line in enumerate(lines, 1):
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    raise InteropError(f"invalid JSON at {path}:{line_number}: {error}") from error
                if not isinstance(record, dict):
                    raise InteropError(f"non-object JSON record at {path}:{line_number}")
                merge_record(records, record, path)
    return records, used_packs


def require_record(records: dict[str, dict[str, Any]], record_id: str, kind: str) -> dict[str, Any]:
    record = records.get(record_id)
    if record is None or record.get("record_type") != kind:
        actual = None if record is None else record.get("record_type")
        raise InteropError(f"required {kind} {record_id} missing or mistyped ({actual})")
    return record


def relation(from_id: str, rel: str, to_id: str, **extra: Any) -> dict[str, Any]:
    record = {
        "schema_id": "ttna-relation-v1",
        "schema_version": SCHEMA_VERSION,
        "id": stable_id("relation", f"{rel}|{from_id}|{to_id}"),
        "record_type": "relation",
        "from_id": from_id,
        "relation": rel,
        "to_id": to_id,
    }
    record.update(extra)
    return record


def extract_build_receipt(
    lane_root: Path, artifact: dict[str, Any], edition: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    artifact_path, artifact_bytes = exact_file(lane_root, artifact, f"artifact {artifact['role']}")
    manifest_spec = {
        "path": artifact["build_manifest_path"],
        "bytes": artifact["build_manifest_bytes"],
        "sha256": artifact["build_manifest_sha256"],
    }
    manifest_path, manifest_bytes = exact_file(
        lane_root, manifest_spec, f"build manifest for {artifact['role']}"
    )
    manifest = read_json(manifest_path)
    for key in ("schema_id", "recorded_date", "mode", "source_date_epoch", "toolchain", "pdf"):
        if key not in manifest:
            raise InteropError(f"build manifest {manifest_path} missing {key}")
    if manifest.get("source_commit") != edition.get("commit") or manifest.get("source_tree") != edition.get("tree"):
        raise InteropError(f"build manifest {manifest_path} does not bind the configured edition")
    pdf = manifest["pdf"]
    expected_pdf = {
        "path": artifact["path"],
        "bytes": len(artifact_bytes),
        "sha256": sha256(artifact_bytes),
    }
    for key, value in expected_pdf.items():
        if pdf.get(key) != value:
            raise InteropError(
                f"build manifest PDF {key} mismatch for {artifact_path}: {pdf.get(key)!r} != {value!r}"
            )
    if manifest.get("lyx_export", {}).get("exit_code") != 0:
        raise InteropError(f"build manifest records failed LyX export: {manifest_path}")
    if manifest.get("latexmk", {}).get("exit_code") != 0:
        raise InteropError(f"build manifest records failed latexmk: {manifest_path}")
    toolchain = manifest["toolchain"]
    required_toolchain = (
        "lyx_product_version",
        "lyx_bytes",
        "lyx_sha256",
        "latexmk_sha256",
        "cprotect_sty_sha256",
    )
    for key in required_toolchain:
        if key not in toolchain:
            raise InteropError(f"build manifest toolchain missing {key}: {manifest_path}")
    receipt = {
        "schema_id": manifest["schema_id"],
        "path": artifact["build_manifest_path"],
        "bytes": len(manifest_bytes),
        "sha256": sha256(manifest_bytes),
        "recorded_date": manifest["recorded_date"],
        "mode": manifest["mode"],
        "source_date_epoch": manifest["source_date_epoch"],
        "source_commit": manifest["source_commit"],
        "source_tree": manifest["source_tree"],
        "overlay_manifest": manifest.get("overlay_manifest"),
        "lyx_export_exit_code": 0,
        "latexmk_exit_code": 0,
    }
    exact_toolchain = {key: toolchain[key] for key in required_toolchain}
    exact_toolchain["identity_source"] = artifact["build_manifest_path"]
    return receipt, exact_toolchain


def make_program_and_course(
    config: dict[str, Any], task_spec: dict[str, Any], resource_id: str, edition_id: str, root_unit_id: str
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    program_cfg = config["program"]
    course_cfg = config["course"]
    program_id = stable_id("program", program_cfg["stable_key"])
    course_id = stable_id("course", course_cfg["stable_key"])
    evidence = {
        "path": task_spec["path"],
        "bytes": task_spec["bytes"],
        "sha256": task_spec["sha256"],
        "source_locator": task_spec["source_locator"],
    }
    program = {
        "schema_id": "ttna-program-v1",
        "schema_version": SCHEMA_VERSION,
        "id": program_id,
        "record_type": "program",
        "program_local_id": program_cfg["program_local_id"],
        "title": program_cfg["title"],
        "curriculum_version": program_cfg["curriculum_version"],
        "locale": config["locale"],
        "resource_id": resource_id,
        "edition_id": edition_id,
        "course_ids": [course_id],
        "evidence": evidence,
        "status": "active_experimental_envelope",
        "timestamp": None,
        "responsible_workflow": "R015 modular backend interoperability v0",
        "supersession_pointer": None,
        "unknown_fields": ["program_local_id", "title", "curriculum_version"],
    }
    course = {
        "schema_id": "ttna-course-v1",
        "schema_version": SCHEMA_VERSION,
        "id": course_id,
        "record_type": "course",
        "course_local_id": course_cfg["course_local_id"],
        "title": course_cfg["title"],
        "curriculum_role": course_cfg["curriculum_role"],
        "program_id": program_id,
        "resource_id": resource_id,
        "edition_id": edition_id,
        "root_unit_ids": [root_unit_id],
        "prerequisite_course_ids": course_cfg["prerequisite_course_ids"],
        "prerequisite_state": "unknown_not_present_in_evidence",
        "evidence": evidence,
        "status": "active_experimental_envelope",
        "timestamp": None,
        "responsible_workflow": "R015 modular backend interoperability v0",
        "supersession_pointer": None,
        "unknown_fields": ["title", "curriculum_role", "prerequisites"],
    }
    relations = [
        relation(program_id, "contains", course_id),
        relation(course_id, "uses_resource", resource_id),
        relation(course_id, "contains", root_unit_id, order=1),
    ]
    return program, course, relations


def make_concepts(
    config: dict[str, Any], records: dict[str, dict[str, Any]], resource_id: str, edition_id: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str], set[str], set[str]]:
    terms_by_local = {
        record.get("source_term_id"): record
        for record in records.values()
        if record.get("record_type") == "term"
    }
    relation_records = [r for r in records.values() if r.get("record_type") == "relation"]
    segment_to_terms: dict[str, set[str]] = defaultdict(set)
    segment_to_units: dict[str, set[str]] = defaultdict(set)
    for row in relation_records:
        if row.get("relation") == "uses_term":
            segment_to_terms[row["from_id"]].add(row["to_id"])
        elif row.get("relation") == "contains":
            target = records.get(row.get("to_id"))
            source = records.get(row.get("from_id"))
            if source and target and source.get("record_type") == "unit" and target.get("record_type") == "segment":
                segment_to_units[row["to_id"]].add(row["from_id"])

    concepts: list[dict[str, Any]] = []
    added_relations: list[dict[str, Any]] = []
    copied_term_ids: set[str] = set()
    copied_unit_ids: set[str] = set()
    copied_segment_ids: set[str] = set()
    for local_id in config["concept_term_local_ids"]:
        term = terms_by_local.get(local_id)
        if term is None:
            raise InteropError(f"configured concept evidence term is absent: {local_id}")
        if term.get("status") != "accepted" or term.get("source_locale") != "en-US":
            raise InteropError(f"configured concept term is not accepted en-US evidence: {local_id}")
        concept_id = stable_id("concept", f"accepted-term|{local_id}")
        concept = {
            "schema_id": "ttna-concept-v1",
            "schema_version": SCHEMA_VERSION,
            "id": concept_id,
            "record_type": "concept",
            "concept_local_id": f"TTNA-CONCEPT-{local_id.removeprefix('TTNA-TERM-')}",
            "resource_id": resource_id,
            "edition_id": edition_id,
            "locale_neutral": True,
            "source_label": term["source_term"],
            "source_locale": term["source_locale"],
            "definition": None,
            "concept_kind": "terminology_evidenced_concept_or_skill",
            "evidence_term_id": term["id"],
            "evidence": {
                "source_term_id": local_id,
                "source_locator": term["evidence"],
                "evidence_basis": "accepted source terminology plus existing segment uses_term relations",
            },
            "status": "evidenced",
            "timestamp": None,
            "responsible_workflow": "R015 modular backend interoperability v0",
            "supersession_pointer": None,
        }
        concepts.append(concept)
        copied_term_ids.add(term["id"])
        added_relations.append(relation(term["id"], "denotes", concept_id))

        evidence_by_unit: dict[str, set[str]] = defaultdict(set)
        for segment_id, term_ids in segment_to_terms.items():
            if term["id"] not in term_ids:
                continue
            for unit_id in segment_to_units.get(segment_id, set()):
                evidence_by_unit[unit_id].add(segment_id)
        if not evidence_by_unit:
            raise InteropError(f"concept term has no unit-contained uses_term evidence: {local_id}")
        for unit_id, segment_ids in sorted(evidence_by_unit.items()):
            copied_unit_ids.add(unit_id)
            copied_segment_ids.update(segment_ids)
            added_relations.append(
                relation(
                    unit_id,
                    "covers_concept",
                    concept_id,
                    evidence_segment_ids=sorted(segment_ids),
                )
            )
    return concepts, added_relations, copied_term_ids, copied_unit_ids, copied_segment_ids


def read_corrections(
    lane_root: Path,
    ledger_spec: dict[str, Any],
    records: dict[str, dict[str, Any]],
    resource_id: str,
    edition_id: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str]]:
    ledger_path, ledger_bytes = exact_file(lane_root, ledger_spec, "adverse ledger")
    try:
        text = ledger_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise InteropError(f"adverse ledger is not UTF-8: {error}") from error
    rows = list(csv.DictReader(text.splitlines()))
    required = {
        "event_id",
        "severity",
        "scope",
        "source_locator",
        "issue",
        "disposition",
        "status",
        "evidence",
    }
    if not rows or set(rows[0]) != required:
        raise InteropError(f"unexpected adverse-ledger columns: {sorted(set(rows[0]) if rows else set())}")
    source_files = {
        Path(record["source_path"]).name.casefold(): record
        for record in records.values()
        if record.get("record_type") == "source_file"
    }
    seen_events: set[str] = set()
    corrections: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []
    copied_source_file_ids: set[str] = set()
    for row_number, row in enumerate(rows, 2):
        event_id = row["event_id"]
        if not event_id or event_id in seen_events:
            raise InteropError(f"blank or duplicate adverse event at CSV row {row_number}: {event_id!r}")
        seen_events.add(event_id)
        filenames = sorted({match.casefold() for match in SOURCE_FILE_TOKEN.findall(row["source_locator"])})
        affected = sorted(
            {source_files[name]["id"] for name in filenames if name in source_files}
        )
        copied_source_file_ids.update(affected)
        row_payload = canonical(row).encode("utf-8")
        correction_id = stable_id("correction", event_id)
        correction = {
            "schema_id": "ttna-correction-v1",
            "schema_version": SCHEMA_VERSION,
            "id": correction_id,
            "record_type": "correction",
            "correction_local_id": event_id,
            "resource_id": resource_id,
            "edition_id": edition_id,
            "severity": row["severity"],
            "scope": row["scope"],
            "source_locator": row["source_locator"],
            "source_backed_defect": row["issue"],
            "target_correction_or_disposition": row["disposition"],
            "rationale": None,
            "evidence": row["evidence"],
            "status": row["status"],
            "translation_state": None,
            "source_ledger": {
                "path": ledger_spec["path"],
                "bytes": len(ledger_bytes),
                "sha256": sha256(ledger_bytes),
                "csv_row": row_number,
                "canonical_row_sha256": sha256(row_payload),
            },
            "affected_source_file_ids": affected,
            "affected_unit_ids": [],
            "affected_unit_mapping_status": "not_inferred_from_free-form_locator",
            "upstream_report_disposition": None,
            "timestamp": None,
            "responsible_workflow": "R015 adverse-ledger workflow",
            "supersession_pointer": None,
        }
        corrections.append(correction)
        for source_file_id in affected:
            relations.append(relation(correction_id, "corrects", source_file_id))
    return corrections, relations, copied_source_file_ids


def make_artifacts(
    lane_root: Path,
    config: dict[str, Any],
    records: dict[str, dict[str, Any]],
    program_id: str,
    course_id: str,
    resource_id: str,
    edition: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str]]:
    artifacts: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []
    copied_rights: set[str] = set()
    role_to_id: dict[str, str] = {}
    for spec in config["artifacts"]:
        role = spec["role"]
        if role in role_to_id:
            raise InteropError(f"duplicate artifact role: {role}")
        artifact_id = stable_id("artifact", spec["stable_key"])
        role_to_id[role] = artifact_id
        for rights_id in spec["rights_ids"]:
            require_record(records, rights_id, "rights")
            copied_rights.add(rights_id)
        receipt, toolchain = extract_build_receipt(lane_root, spec, edition)
        artifacts.append(
            {
                "schema_id": "ttna-artifact-v1",
                "schema_version": SCHEMA_VERSION,
                "id": artifact_id,
                "record_type": "artifact",
                "artifact_local_id": role,
                "artifact_role": role,
                "program_id": program_id,
                "course_id": course_id,
                "resource_id": resource_id,
                "edition_id": edition["id"],
                "locale": spec["locale"],
                "media_type": spec["media_type"],
                "path": spec["path"],
                "bytes": spec["bytes"],
                "sha256": spec["sha256"],
                "rights_ids": sorted(spec["rights_ids"]),
                "toolchain": toolchain,
                "build_receipt": receipt,
                "status": spec["status"],
                "timestamp": None,
                "responsible_workflow": "R015 deterministic edition build",
                "supersession_pointer": None,
            }
        )
        relations.append(relation(artifact_id, "built_from", edition["id"]))
    for spec in config["artifacts"]:
        supersedes_role = spec.get("supersedes_role")
        if supersedes_role is None:
            continue
        if supersedes_role not in role_to_id:
            raise InteropError(
                f"artifact {spec['role']} supersedes unknown role {supersedes_role}"
            )
        relations.append(
            relation(role_to_id[spec["role"]], "supersedes", role_to_id[supersedes_role])
        )
    return artifacts, relations, copied_rights


def copy_records(records: dict[str, dict[str, Any]], ids: Iterable[str], kind: str) -> list[dict[str, Any]]:
    return [require_record(records, record_id, kind) for record_id in sorted(set(ids))]


def build_pack(lane_root: Path, config_path: Path, out: Path) -> dict[str, Any]:
    config = read_json(config_path)
    if config.get("schema_id") != CONFIG_SCHEMA_ID or config.get("schema_version") != SCHEMA_VERSION:
        raise InteropError("unsupported interoperability config")
    task_spec = config["task_evidence"]
    exact_file(lane_root, task_spec, "task evidence")
    records, dependency_packs = load_dependency_records(
        lane_root, config["source_manifest"], config["output_pack"]
    )
    resource_id = config["resource_id"]
    edition_id = config["edition_id"]
    resource = require_record(records, resource_id, "resource")
    edition = require_record(records, edition_id, "edition")
    roots = [
        r
        for r in records.values()
        if r.get("record_type") == "unit"
        and r.get("source_local_id") == config["root_unit_source_local_id"]
    ]
    if len(roots) != 1:
        raise InteropError(f"expected exactly one work root, got {len(roots)}")
    root_unit = roots[0]
    program, course, curriculum_relations = make_program_and_course(
        config, task_spec, resource_id, edition_id, root_unit["id"]
    )
    concepts, concept_relations, term_ids, unit_ids, segment_ids = make_concepts(
        config, records, resource_id, edition_id
    )
    corrections, correction_relations, source_file_ids = read_corrections(
        lane_root, config["adverse_ledger"], records, resource_id, edition_id
    )
    artifacts, artifact_relations, rights_ids = make_artifacts(
        lane_root,
        config,
        records,
        program["id"],
        course["id"],
        resource_id,
        edition,
    )
    unit_ids.add(root_unit["id"])
    for unit_id in list(unit_ids):
        unit = require_record(records, unit_id, "unit")
        source_file_id = unit.get("source_file_id")
        if source_file_id is not None:
            source_file_ids.add(source_file_id)
        for rights_id in unit.get("rights_ids", [unit.get("rights_id")]):
            if rights_id is not None:
                rights_ids.add(rights_id)
    for segment_id in segment_ids:
        segment = require_record(records, segment_id, "segment")
        source_file_id = segment.get("source_file_id")
        if source_file_id is not None:
            source_file_ids.add(source_file_id)
        for rights_id in segment.get("rights_ids", [segment.get("rights_id")]):
            if rights_id is not None:
                rights_ids.add(rights_id)
    for source_file_id in list(source_file_ids):
        source_file = require_record(records, source_file_id, "source_file")
        for rights_id in source_file.get("rights_ids", [source_file.get("rights_id")]):
            if rights_id is not None:
                rights_ids.add(rights_id)

    groups: dict[str, list[dict[str, Any]]] = {
        "artifacts/artifacts.jsonl": artifacts,
        "authority/editions.jsonl": [edition],
        "authority/resources.jsonl": [resource],
        "corrections/corrections.jsonl": corrections,
        "curriculum/courses.jsonl": [course],
        "curriculum/programs.jsonl": [program],
        "rights/components.jsonl": copy_records(records, rights_ids, "rights"),
        "semantics/concepts.jsonl": concepts,
        "topology/relations.jsonl": (
            curriculum_relations + concept_relations + correction_relations + artifact_relations
        ),
        "topology/source_files.jsonl": copy_records(records, source_file_ids, "source_file"),
        "topology/units.jsonl": copy_records(records, unit_ids, "unit"),
        "translation/segments.en.jsonl": copy_records(records, segment_ids, "segment"),
        "translation/terms.id-ID.jsonl": copy_records(records, term_ids, "term"),
    }

    file_rows: list[dict[str, Any]] = []
    local_records: dict[str, dict[str, Any]] = {}
    for rel, group in sorted(groups.items()):
        for record in group:
            merge_record(local_records, record, out / rel)
        row = write_jsonl(out / rel, group)
        row["path"] = rel
        file_rows.append(row)
    known = set(local_records)
    for row in local_records.values():
        if row.get("record_type") == "relation":
            if row["from_id"] not in known or row["to_id"] not in known:
                raise InteropError(f"local pack relation is not closed: {row['id']}")
            for evidence_id in row.get("evidence_segment_ids", []):
                if evidence_id not in known:
                    raise InteropError(
                        f"local pack relation evidence is not closed: {row['id']} -> {evidence_id}"
                    )
    counts = Counter(record["record_type"] for record in local_records.values())
    config_bytes = config_path.read_bytes()
    manifest = {
        "schema_id": "ttna-lane-manifest-v1",
        "schema_version": SCHEMA_VERSION,
        "generator": GENERATOR_VERSION,
        "recorded_date": config["recorded_date"],
        "locale": config["locale"],
        "file_kind": "interoperability_envelope",
        "file_order": config["file_order"],
        "scope": f"{task_spec['path']} + {config['adverse_ledger']['path']}",
        "source_role": "modular_backend_interoperability_v0",
        "source_commit": edition["commit"],
        "source_tree": edition["tree"],
        "resource_id": resource_id,
        "edition_id": edition_id,
        "program_id": program["id"],
        "course_id": course["id"],
        "config_path": config_path.relative_to(lane_root).as_posix(),
        "config_bytes": len(config_bytes),
        "config_sha256": sha256(config_bytes),
        "dependency_packs": dependency_packs,
        "input_snapshot": {
            "task_evidence": task_spec,
            "adverse_ledger": config["adverse_ledger"],
            "artifacts": [
                {
                    "role": spec["role"],
                    "path": spec["path"],
                    "bytes": spec["bytes"],
                    "sha256": spec["sha256"],
                    "build_manifest_path": spec["build_manifest_path"],
                    "build_manifest_bytes": spec["build_manifest_bytes"],
                    "build_manifest_sha256": spec["build_manifest_sha256"],
                }
                for spec in config["artifacts"]
            ],
        },
        "counts": dict(sorted(counts.items())),
        "total_unique_records": len(local_records),
        "files": file_rows,
        "admission": {
            "exact_input_hash_gate": "pass",
            "artifact_build_receipt_gate": "pass",
            "correction_rows_complete": len(corrections),
            "local_relation_closure": "pass",
            "unknown_curriculum_fields_preserved_as_null": True,
        },
    }
    write_json(out / "manifests" / "lane_manifest.json", manifest)
    return manifest


def update_exact_input_specs(lane_root: Path, config: dict[str, Any]) -> None:
    for key in ("task_evidence", "adverse_ledger"):
        spec = config[key]
        payload = (lane_root / spec["path"]).read_bytes()
        spec["bytes"] = len(payload)
        spec["sha256"] = sha256(payload)


def bind_artifact(args: argparse.Namespace) -> None:
    lane_root = args.lane_root.resolve()
    config = read_json(args.base_config)
    if config.get("schema_id") != CONFIG_SCHEMA_ID:
        raise InteropError("unsupported base config")
    artifact_path = Path(args.artifact)
    manifest_path = Path(args.build_manifest)
    artifact_bytes = (lane_root / artifact_path).read_bytes()
    manifest_bytes = (lane_root / manifest_path).read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    pdf = manifest.get("pdf", {})
    exact = {
        "path": artifact_path.as_posix(),
        "bytes": len(artifact_bytes),
        "sha256": sha256(artifact_bytes),
    }
    if any(pdf.get(key) != value for key, value in exact.items()):
        raise InteropError("build manifest does not describe the supplied artifact exactly")
    inherited_rights = args.rights_id or config["artifacts"][0]["rights_ids"]
    new_spec = {
        "build_manifest_bytes": len(manifest_bytes),
        "build_manifest_path": manifest_path.as_posix(),
        "build_manifest_sha256": sha256(manifest_bytes),
        "bytes": len(artifact_bytes),
        "locale": args.locale,
        "media_type": args.media_type,
        "path": artifact_path.as_posix(),
        "rights_ids": sorted(inherited_rights),
        "role": args.role,
        "sha256": sha256(artifact_bytes),
        "stable_key": f"artifact/{args.role}",
        "status": args.status,
        "supersedes_role": args.supersedes_role,
    }
    config["artifacts"] = [row for row in config["artifacts"] if row["role"] != args.role]
    config["artifacts"].append(new_spec)
    config["artifacts"].sort(key=lambda row: row["role"])
    if args.refresh_inputs:
        update_exact_input_specs(lane_root, config)
    write_json(args.out_config, config)
    print(canonical(new_spec))


def refresh_inputs(args: argparse.Namespace) -> None:
    config = read_json(args.config)
    update_exact_input_specs(args.lane_root.resolve(), config)
    write_json(args.out_config, config)
    print(canonical({key: config[key] for key in ("task_evidence", "adverse_ledger")}))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    generate = sub.add_parser("generate", help="verify inputs and emit the v0 pack")
    generate.add_argument("--lane-root", required=True, type=Path)
    generate.add_argument("--config", required=True, type=Path)
    generate.add_argument("--out", required=True, type=Path)

    bind = sub.add_parser("bind-artifact", help="hash-bind or replace one artifact role")
    bind.add_argument("--lane-root", required=True, type=Path)
    bind.add_argument("--base-config", required=True, type=Path)
    bind.add_argument("--artifact", required=True)
    bind.add_argument("--build-manifest", required=True)
    bind.add_argument("--role", required=True)
    bind.add_argument("--locale", required=True)
    bind.add_argument("--status", required=True)
    bind.add_argument("--media-type", default="application/pdf")
    bind.add_argument("--rights-id", action="append")
    bind.add_argument("--supersedes-role")
    bind.add_argument("--refresh-inputs", action="store_true")
    bind.add_argument("--out-config", required=True, type=Path)

    refresh = sub.add_parser("refresh-inputs", help="rebind exact task/ledger input hashes")
    refresh.add_argument("--lane-root", required=True, type=Path)
    refresh.add_argument("--config", required=True, type=Path)
    refresh.add_argument("--out-config", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        if args.command == "generate":
            manifest = build_pack(args.lane_root.resolve(), args.config.resolve(), args.out.resolve())
            print(canonical(manifest))
        elif args.command == "bind-artifact":
            bind_artifact(args)
        else:
            refresh_inputs(args)
    except (InteropError, OSError, KeyError, TypeError, csv.Error, json.JSONDecodeError) as error:
        print(f"interoperability-v0 error: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
