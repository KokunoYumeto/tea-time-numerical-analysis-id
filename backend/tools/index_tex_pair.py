#!/usr/bin/env python3
"""Emit a deterministic backend pack for one aligned TeX reader-string map."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

import index_lyx_pair as shared


GENERATOR_VERSION = "ttna-tex-indexer-0.1.0"
MAP_SCHEMA_ID = "ttna-tex-reader-map-v1"

TOKEN_RE = re.compile(
    r"(?P<math>(?<!\\)\$(?:\\.|[^$])*(?<!\\)\$)"
    r"|(?P<linebreak>\\\\(?:\[[^\]]*\])?)"
    r"|(?P<command>\\[A-Za-z@]+)"
    r"|(?P<symbol>\\.)"
    r"|(?P<parameter>#[1-9])"
)


def load_reader_map(path: Path) -> tuple[dict[str, Any], bytes]:
    payload = path.read_bytes()
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(f"cannot decode TeX reader map {path}: {error}") from error
    if not isinstance(value, dict):
        raise SystemExit("TeX reader map root must be an object")
    shared.require_exact_keys(
        value,
        {
            "schema_id",
            "schema_version",
            "source_path",
            "source_bytes",
            "source_sha256",
            "units",
            "segments",
        },
        "TeX reader map",
    )
    if value["schema_id"] != MAP_SCHEMA_ID:
        raise SystemExit("unsupported TeX reader-map schema_id")
    if value["schema_version"] != shared.SCHEMA_VERSION:
        raise SystemExit("unsupported TeX reader-map schema_version")
    if not isinstance(value["units"], list) or not value["units"]:
        raise SystemExit("TeX reader map must declare units")
    if not isinstance(value["segments"], list) or not value["segments"]:
        raise SystemExit("TeX reader map must declare segments")

    unit_keys: set[str] = set()
    unit_orders: set[int] = set()
    for index, unit in enumerate(value["units"], 1):
        if not isinstance(unit, dict):
            raise SystemExit(f"TeX reader-map unit {index} must be an object")
        shared.require_exact_keys(
            unit,
            {"key", "kind", "source_local_id", "order"},
            f"TeX reader-map unit {index}",
        )
        if (
            not isinstance(unit["key"], str)
            or not unit["key"]
            or unit["key"] in unit_keys
        ):
            raise SystemExit(f"invalid or duplicate TeX reader-map unit key at {index}")
        if (
            not isinstance(unit["order"], int)
            or unit["order"] < 1
            or unit["order"] in unit_orders
        ):
            raise SystemExit(f"invalid or duplicate TeX reader-map unit order at {index}")
        unit_keys.add(unit["key"])
        unit_orders.add(unit["order"])

    segment_keys: set[str] = set()
    segment_lines: set[int] = set()
    segment_orders: set[tuple[str, int]] = set()
    for index, segment in enumerate(value["segments"], 1):
        if not isinstance(segment, dict):
            raise SystemExit(f"TeX reader-map segment {index} must be an object")
        shared.require_exact_keys(
            segment,
            {
                "key",
                "unit_key",
                "line",
                "prefix",
                "suffix",
                "semantic_slot",
                "order",
            },
            f"TeX reader-map segment {index}",
        )
        if (
            not isinstance(segment["key"], str)
            or not segment["key"]
            or segment["key"] in segment_keys
        ):
            raise SystemExit(f"invalid or duplicate TeX reader-map segment key at {index}")
        if segment["unit_key"] not in unit_keys:
            raise SystemExit(
                f"TeX reader-map segment {segment['key']} has unknown unit_key"
            )
        if (
            not isinstance(segment["line"], int)
            or segment["line"] < 1
            or segment["line"] in segment_lines
        ):
            raise SystemExit(
                f"invalid or duplicate TeX reader-map line for {segment['key']}"
            )
        order_key = (segment["unit_key"], segment["order"])
        if (
            not isinstance(segment["order"], int)
            or segment["order"] < 1
            or order_key in segment_orders
        ):
            raise SystemExit(
                f"invalid or duplicate unit-local order for {segment['key']}"
            )
        if not isinstance(segment["prefix"], str) or not isinstance(
            segment["suffix"], str
        ):
            raise SystemExit(f"TeX reader-map affixes must be strings: {segment['key']}")
        segment_keys.add(segment["key"])
        segment_lines.add(segment["line"])
        segment_orders.add(order_key)
    return value, payload


def extract_fragment(line: str, annotation: dict[str, Any], side: str) -> str:
    prefix = annotation["prefix"]
    suffix = annotation["suffix"]
    end = len(line) - len(suffix) if suffix else len(line)
    if (
        not line.startswith(prefix)
        or not line.endswith(suffix)
        or end < len(prefix)
    ):
        raise SystemExit(
            f"{side} line {annotation['line']} violates reader-map affixes "
            f"for {annotation['key']}"
        )
    return line[len(prefix) : end]


def protected_tokens(text: str) -> list[dict[str, Any]]:
    tokens: list[dict[str, Any]] = []
    kind_map = {
        "math": "TeXMath",
        "linebreak": "TeXLineBreak",
        "command": "TeXCommand",
        "symbol": "TeXControlSymbol",
        "parameter": "TeXParameter",
    }
    for ordinal, match in enumerate(TOKEN_RE.finditer(text), 1):
        value = match.group(0)
        tokens.append(
            {
                "ordinal": ordinal,
                "kind": kind_map[match.lastgroup or "symbol"],
                "value": value,
                "sha256": shared.digest_text(value),
            }
        )
    return tokens


def rights_records() -> list[dict[str, Any]]:
    text_rights_id = shared.stable_id("rights", "CC-BY-SA-4.0|book-text")
    code_rights_id = shared.stable_id("rights", "GPL-3.0-or-later|code")
    return [
        {
            **shared.record_base("ttna-rights-v1", text_rights_id, "rights"),
            "spdx_expression": "CC-BY-SA-4.0",
            "scope": (
                "book prose, mathematical exposition, and Indonesian translation "
                "subject to component review"
            ),
            "authority_path": "source/lqbrin-tea-time-numerical-1868821/COPYING.txt",
            "attribution": "Leon Q. Brin, Tea Time Numerical Analysis, Third Edition",
            "modification_notice_required": True,
            "share_alike_required": True,
        },
        {
            **shared.record_base("ttna-rights-v1", code_rights_id, "rights"),
            "spdx_expression": "GPL-3.0-or-later",
            "scope": "code printed within and accompanying the textbook electronically",
            "authority_path": "source/lqbrin-tea-time-numerical-1868821/COPYING.txt",
            "source_required": True,
        },
    ]


def term_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            records.append(
                {
                    **shared.record_base(
                        "ttna-term-v1",
                        shared.stable_id("term", row["term_id"]),
                        "term",
                    ),
                    "source_term_id": row["term_id"],
                    "source_locale": "en-US",
                    "source_term": row["source_term"],
                    "locale": "id-ID",
                    "preferred": row["preferred_id"],
                    "variants": [
                        item for item in row["variants"].split("|") if item
                    ],
                    "rejected": [
                        item for item in row["rejected"].split("|") if item
                    ],
                    "scope": row["scope"],
                    "evidence": row["evidence"],
                    "status": row["status"],
                }
            )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--source-rel", required=True)
    parser.add_argument("--target-rel", required=True)
    parser.add_argument("--terms-csv", required=True, type=Path)
    parser.add_argument("--reader-map", required=True, type=Path)
    parser.add_argument("--file-order", required=True, type=int)
    parser.add_argument("--file-kind", default="build_preamble")
    parser.add_argument("--source-role", default="build_preamble")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    reader_map, reader_map_bytes = load_reader_map(args.reader_map)
    source_rel = args.source_rel.replace("\\", "/")
    target_rel = args.target_rel.replace("\\", "/")
    if reader_map["source_path"] != source_rel:
        raise SystemExit("TeX reader map source_path does not match --source-rel")

    source_bytes = args.source.read_bytes()
    target_bytes = args.target.read_bytes()
    if len(source_bytes) != reader_map["source_bytes"]:
        raise SystemExit("source byte count does not match TeX reader map")
    if shared.digest_bytes(source_bytes) != reader_map["source_sha256"]:
        raise SystemExit("source hash does not match TeX reader map")
    try:
        source_text = source_bytes.decode("utf-8")
        target_text = target_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise SystemExit(f"TeX pair must be UTF-8: {error}") from error
    if "\r" in source_text or "\r" in target_text:
        raise SystemExit("TeX pair must use LF line endings")
    source_lines = source_text.splitlines()
    target_lines = target_text.splitlines()
    if len(source_lines) != len(target_lines):
        raise SystemExit("source/target TeX line counts differ")

    annotated_lines = {item["line"] for item in reader_map["segments"]}
    changed_lines = {
        index
        for index, pair in enumerate(zip(source_lines, target_lines), 1)
        if pair[0] != pair[1]
    }
    unannotated_changed_lines = sorted(changed_lines - annotated_lines)
    if unannotated_changed_lines:
        raise SystemExit(
            "target changes outside reader map: "
            + ",".join(str(item) for item in unannotated_changed_lines)
        )

    resource_id = shared.stable_id("resource", shared.RESOURCE_URL)
    edition_id = shared.stable_id("edition", shared.EDITION_COMMIT)
    work_unit_id = shared.stable_id("unit", "work")
    file_key = source_rel
    source_file_id = shared.stable_id("source_file", file_key)
    file_unit_id = shared.stable_id("unit", file_key)
    text_rights_id = shared.stable_id("rights", "CC-BY-SA-4.0|book-text")

    resources = [
        {
            **shared.record_base("ttna-resource-v1", resource_id, "resource"),
            "resource_local_id": "R015",
            "course_local_id": "C110",
            "title": "Tea Time Numerical Analysis",
            "author": "Leon Q. Brin",
            "authority_url": shared.RESOURCE_URL,
        }
    ]
    editions = [
        {
            **shared.record_base("ttna-edition-v1", edition_id, "edition"),
            "resource_id": resource_id,
            "edition_label": "Third Edition",
            "tag": "v3.0",
            "commit": shared.EDITION_COMMIT,
            "tree": shared.EDITION_TREE,
            "source_locale": "en-US",
            "target_locale": "id-ID",
        }
    ]
    source_files = [
        {
            **shared.record_base(
                "ttna-source-file-v1", source_file_id, "source_file"
            ),
            "edition_id": edition_id,
            "source_path": source_rel,
            "source_bytes": len(source_bytes),
            "source_sha256": shared.digest_bytes(source_bytes),
            "target_path": target_rel,
            "target_bytes": len(target_bytes),
            "target_sha256": shared.digest_bytes(target_bytes),
            "format": "TeX/LaTeX preamble",
            "role": args.source_role,
            "rights_id": text_rights_id,
        }
    ]

    work_unit = {
        **shared.record_base("ttna-unit-v1", work_unit_id, "unit"),
        "edition_id": edition_id,
        "kind": "work",
        "source_local_id": "TeaTimeNumericalAnalysis",
        "parent_id": None,
        "order": 1,
        "rights_id": text_rights_id,
    }
    file_unit = {
        **shared.record_base("ttna-unit-v1", file_unit_id, "unit"),
        "edition_id": edition_id,
        "kind": args.file_kind,
        "source_file_id": source_file_id,
        "source_local_id": Path(source_rel).name,
        "parent_id": work_unit_id,
        "order": args.file_order,
        "rights_id": text_rights_id,
    }
    units: list[dict[str, Any]] = [work_unit, file_unit]
    relations: list[dict[str, Any]] = [
        {
            **shared.record_base(
                "ttna-relation-v1",
                shared.stable_id(
                    "relation", f"{work_unit_id}|contains|{file_unit_id}"
                ),
                "relation",
            ),
            "relation": "contains",
            "from_id": work_unit_id,
            "to_id": file_unit_id,
            "order": args.file_order,
        }
    ]

    unit_ids: dict[str, str] = {}
    for item in sorted(reader_map["units"], key=lambda value: value["order"]):
        unit_id = shared.stable_id("unit", f"{file_key}|tex-unit:{item['key']}")
        unit_ids[item["key"]] = unit_id
        units.append(
            {
                **shared.record_base("ttna-unit-v1", unit_id, "unit"),
                "edition_id": edition_id,
                "kind": item["kind"],
                "source_file_id": source_file_id,
                "source_local_id": item["source_local_id"],
                "parent_id": file_unit_id,
                "order": item["order"],
                "rights_id": text_rights_id,
            }
        )
        relations.append(
            {
                **shared.record_base(
                    "ttna-relation-v1",
                    shared.stable_id(
                        "relation", f"{file_unit_id}|contains|{unit_id}"
                    ),
                    "relation",
                ),
                "relation": "contains",
                "from_id": file_unit_id,
                "to_id": unit_id,
                "order": item["order"],
            }
        )

    segments: list[dict[str, Any]] = []
    localizations: list[dict[str, Any]] = []
    token_shape_mismatch_ids: list[str] = []
    token_value_mismatch_ids: list[str] = []
    changed_segment_count = 0
    for item in sorted(
        reader_map["segments"],
        key=lambda value: (unit_ids[value["unit_key"]], value["order"]),
    ):
        line_number = item["line"]
        source_line = source_lines[line_number - 1]
        target_line = target_lines[line_number - 1]
        source_value = extract_fragment(source_line, item, "source")
        target_value = extract_fragment(target_line, item, "target")
        source_tokens = protected_tokens(source_value)
        target_tokens = protected_tokens(target_value)
        source_shape = [token["kind"] for token in source_tokens]
        target_shape = [token["kind"] for token in target_tokens]
        source_values = [token["value"] for token in source_tokens]
        target_values = [token["value"] for token in target_tokens]
        shape_equal = source_shape == target_shape
        values_equal = source_values == target_values

        segment_id = shared.stable_id(
            "segment", f"{file_key}|tex-segment:{item['key']}"
        )
        localization_id = shared.stable_id(
            "localization", f"{segment_id}|id-ID"
        )
        unit_id = unit_ids[item["unit_key"]]
        source_math = [
            token["value"] for token in source_tokens if token["kind"] == "TeXMath"
        ]
        target_math = [
            token["value"] for token in target_tokens if token["kind"] == "TeXMath"
        ]
        if source_math or target_math:
            math_state = (
                "verified_exact"
                if source_math == target_math
                else "localized_reader_ordinal"
            )
        else:
            math_state = "not_applicable"
        changed = source_value != target_value or source_line != target_line
        changed_segment_count += int(changed)
        if not shape_equal:
            token_shape_mismatch_ids.append(localization_id)
        if not values_equal:
            token_value_mismatch_ids.append(localization_id)

        locator = {
            "line": line_number,
            "start_line": line_number,
            "end_line": line_number,
            "tex_context": item["key"],
        }
        segments.append(
            {
                **shared.record_base("ttna-segment-v1", segment_id, "segment"),
                "edition_id": edition_id,
                "unit_id": unit_id,
                "source_file_id": source_file_id,
                "source_locator": locator,
                "semantic_slot": item["semantic_slot"],
                "representation": "tex_reader_fragment",
                "order": item["order"],
                "source_locale": "en-US",
                "source_text": source_value,
                "source_text_sha256": shared.digest_text(source_value),
                "source_block_sha256": shared.digest_text(source_line + "\n"),
                "protected_tokens": source_tokens,
                "rights_id": text_rights_id,
                "translation_state": "source_frozen",
            }
        )
        localizations.append(
            {
                **shared.record_base(
                    "ttna-localization-v1", localization_id, "localization"
                ),
                "segment_id": segment_id,
                "source_segment_sha256": shared.digest_text(source_value),
                "locale": "id-ID",
                "target_path": target_rel,
                "target_locator": locator,
                "target_text": target_value,
                "target_text_sha256": shared.digest_text(target_value),
                "target_block_sha256": shared.digest_text(target_line + "\n"),
                "protected_tokens": target_tokens,
                "protected_token_shape_equal": shape_equal,
                "protected_token_values_equal": values_equal,
                "workflow_state": (
                    "translated" if changed else "translated_unchanged"
                ),
                "structure_state": "structurally_verified",
                "math_state": math_state,
                "formatting_state": (
                    "protected_exact" if values_equal else "reader_format_localized"
                ),
                "language_state": "draft_translated",
                "build_state": "not_built",
                "publication_state": "unpublished",
                "interchange_state": "structurally_verified",
                "provenance": "OpenAI Codex gpt-5.6-sol, Ultra, at the user's request",
            }
        )
        relations.extend(
            [
                {
                    **shared.record_base(
                        "ttna-relation-v1",
                        shared.stable_id(
                            "relation", f"{unit_id}|contains|{segment_id}"
                        ),
                        "relation",
                    ),
                    "relation": "contains",
                    "from_id": unit_id,
                    "to_id": segment_id,
                    "order": item["order"],
                },
                {
                    **shared.record_base(
                        "ttna-relation-v1",
                        shared.stable_id(
                            "relation",
                            f"{localization_id}|translates|{segment_id}",
                        ),
                        "relation",
                    ),
                    "relation": "translates",
                    "from_id": localization_id,
                    "to_id": segment_id,
                },
            ]
        )

    terms = term_records(args.terms_csv)
    for term in terms:
        needle = term["source_term"].casefold()
        for segment in segments:
            if needle in segment["source_text"].casefold():
                relations.append(
                    {
                        **shared.record_base(
                            "ttna-relation-v1",
                            shared.stable_id(
                                "relation",
                                f"{segment['id']}|uses_term|{term['id']}",
                            ),
                            "relation",
                        ),
                        "relation": "uses_term",
                        "from_id": segment["id"],
                        "to_id": term["id"],
                    }
                )

    qa_event_id = shared.stable_id(
        "qa_event", f"{file_key}|tex-reader-map-v1"
    )
    qa_events = [
        {
            **shared.record_base(
                "ttna-qa-event-v1", qa_event_id, "qa_event"
            ),
            "qa_type": "topology",
            "source_file_id": source_file_id,
            "result": "pass",
            "checks": {
                "source_line_count": len(source_lines),
                "target_line_count": len(target_lines),
                "line_count_equal": True,
                "annotated_reader_segment_count": len(segments),
                "changed_reader_segment_count": changed_segment_count,
                "changed_physical_line_count": len(changed_lines),
                "unannotated_changed_line_count": 0,
                "reader_affixes_exact": True,
                "protected_token_shapes_equal": not token_shape_mismatch_ids,
                "protected_token_shape_mismatch_count": len(
                    token_shape_mismatch_ids
                ),
                "protected_token_shape_mismatch_localization_ids": sorted(
                    token_shape_mismatch_ids
                ),
                "protected_token_value_mismatch_count": len(
                    token_value_mismatch_ids
                ),
                "protected_token_value_mismatch_localization_ids": sorted(
                    token_value_mismatch_ids
                ),
                "reader_map_sha256": shared.digest_bytes(reader_map_bytes),
            },
            "witness": GENERATOR_VERSION,
        }
    ]

    outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (args.out / "authority" / "resources.jsonl", resources),
        (args.out / "authority" / "editions.jsonl", editions),
        (args.out / "topology" / "source_files.jsonl", source_files),
        (args.out / "topology" / "units.jsonl", units),
        (args.out / "topology" / "relations.jsonl", relations),
        (args.out / "translation" / "segments.en.jsonl", segments),
        (
            args.out / "translation" / "localizations.id-ID.jsonl",
            localizations,
        ),
        (args.out / "translation" / "terms.id-ID.jsonl", terms),
        (args.out / "assets" / "assets.jsonl", []),
        (args.out / "assets" / "versions.jsonl", []),
        (args.out / "experiments" / "experiments.jsonl", []),
        (args.out / "rights" / "components.jsonl", rights_records()),
        (args.out / "qa" / "events.jsonl", qa_events),
    ]
    shared.validate_local_relation_closure(outputs)

    if args.source.read_bytes() != source_bytes or args.target.read_bytes() != target_bytes:
        raise SystemExit("input changed during TeX pack generation")
    for path, records in outputs:
        shared.write_jsonl(path, records)

    files: list[dict[str, Any]] = []
    for path, records in outputs:
        payload = path.read_bytes()
        files.append(
            {
                "path": path.relative_to(args.out).as_posix(),
                "bytes": len(payload),
                "sha256": shared.digest_bytes(payload),
                "records": len(records),
            }
        )
    manifest = {
        "schema_id": "ttna-lane-manifest-v1",
        "schema_version": shared.SCHEMA_VERSION,
        "generator": GENERATOR_VERSION,
        "recorded_date": shared.RECORDED_DATE,
        "resource_id": resource_id,
        "edition_id": edition_id,
        "locale": "id-ID",
        "source_commit": shared.EDITION_COMMIT,
        "source_tree": shared.EDITION_TREE,
        "scope": source_rel,
        "file_order": args.file_order,
        "file_kind": args.file_kind,
        "source_role": args.source_role,
        "reader_map": args.reader_map.as_posix(),
        "reader_map_sha256": shared.digest_bytes(reader_map_bytes),
        "files": sorted(files, key=lambda item: item["path"]),
        "counts": {
            "top_level_layouts": 0,
            "annotated_reader_segments": len(segments),
            "changed_reader_segments": changed_segment_count,
            "units": len(units),
            "segments": len(segments),
            "localizations": len(localizations),
            "relations": len(relations),
            "terms": len(terms),
            "assets": 0,
            "asset_versions": 0,
            "experiments": 0,
        },
    }
    shared.write_json(args.out / "manifests" / "lane_manifest.json", manifest)
    print(shared.canonical(manifest))


if __name__ == "__main__":
    main()
