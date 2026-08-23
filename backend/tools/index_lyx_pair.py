#!/usr/bin/env python3
"""Emit deterministic modular-backend records for one aligned LyX file pair."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import uuid
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_VERSION = "1.0.0"
GENERATOR_VERSION = "ttna-lyx-indexer-0.3.1"
RESOURCE_URL = "https://github.com/lqbrin/tea-time-numerical"
RESOURCE_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, RESOURCE_URL)
EDITION_COMMIT = "186882108a6da95c8dca5b81ce000fc3f8f3ca21"
EDITION_TREE = "1e50d3756b695176008c602f0ee89712f5f32d10"
RECORDED_DATE = "2026-08-20"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_text(text: str) -> str:
    return digest_bytes(text.encode("utf-8"))


def stable_id(kind: str, key: str) -> str:
    return "urn:uuid:" + str(uuid.uuid5(RESOURCE_NAMESPACE, f"{kind}|{key}"))


def normalize_octave_text(text: str) -> str:
    """Normalize transport-only Octave text differences without changing code."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip(" \t") for line in normalized.split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def require_exact_keys(value: dict[str, Any], required: set[str], context: str) -> None:
    missing = sorted(required - set(value))
    if missing:
        raise SystemExit(f"{context} missing required keys: {', '.join(missing)}")


def load_code_evidence(path: Path) -> tuple[dict[str, Any], Path]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(f"cannot read code evidence {path}: {error}") from error
    if not isinstance(value, dict):
        raise SystemExit("code evidence root must be an object")
    require_exact_keys(
        value,
        {"schema_id", "schema_version", "normalizer", "path_root", "mappings", "experiments"},
        "code evidence",
    )
    if value["schema_id"] != "ttna-code-evidence-map-v1":
        raise SystemExit("unsupported code-evidence schema_id")
    if value["schema_version"] != SCHEMA_VERSION:
        raise SystemExit("unsupported code-evidence schema_version")
    normalizer = value["normalizer"]
    if not isinstance(normalizer, dict) or normalizer.get("id") != "octave-text-v1":
        raise SystemExit("code evidence must use octave-text-v1")
    if not isinstance(value["mappings"], list) or not isinstance(value["experiments"], list):
        raise SystemExit("code-evidence mappings and experiments must be arrays")

    mapping_segments: set[str] = set()
    mapping_locators: set[tuple[str, int, int]] = set()
    allowed_kinds = {"normalized_full_equal", "exact_excerpt", "documented_revision"}
    for index, mapping in enumerate(value["mappings"], 1):
        context = f"code-evidence mapping {index}"
        if not isinstance(mapping, dict):
            raise SystemExit(f"{context} must be an object")
        require_exact_keys(
            mapping,
            {
                "asset_normalized_bytes",
                "asset_normalized_sha256",
                "asset_path",
                "asset_raw_bytes",
                "asset_raw_sha256",
                "evidence_segments",
                "match_kind",
                "segment_id",
                "source_block_sha256",
                "source_locator",
                "source_normalized_bytes",
                "source_normalized_sha256",
                "source_rel",
                "source_text_bytes",
                "source_text_sha256",
            },
            context,
        )
        if mapping["match_kind"] not in allowed_kinds:
            raise SystemExit(f"{context} has unsupported match_kind")
        locator = mapping["source_locator"]
        if not isinstance(locator, dict):
            raise SystemExit(f"{context} source_locator must be an object")
        require_exact_keys(
            locator,
            {"layout", "layout_ordinal", "ert_ordinal", "start_line", "end_line"},
            f"{context} source_locator",
        )
        segment_id = mapping["segment_id"]
        locator_key = (
            mapping["source_rel"],
            locator["layout_ordinal"],
            locator["ert_ordinal"],
        )
        if segment_id in mapping_segments:
            raise SystemExit(f"ambiguous duplicate mapping for segment {segment_id}")
        if locator_key in mapping_locators:
            raise SystemExit(f"ambiguous duplicate mapping locator {locator_key}")
        mapping_segments.add(segment_id)
        mapping_locators.add(locator_key)
        if mapping["match_kind"] == "exact_excerpt":
            line_range = mapping.get("asset_line_range")
            if (
                not isinstance(line_range, list)
                or len(line_range) != 2
                or not all(isinstance(item, int) and item > 0 for item in line_range)
                or line_range[0] > line_range[1]
            ):
                raise SystemExit(f"{context} needs a positive asset_line_range")
        elif "asset_line_range" in mapping:
            raise SystemExit(f"{context} has asset_line_range outside exact_excerpt")
        if mapping["match_kind"] == "documented_revision" and not mapping.get(
            "declared_function"
        ):
            raise SystemExit(f"{context} needs declared_function")
        if not isinstance(mapping["evidence_segments"], list) or not mapping[
            "evidence_segments"
        ]:
            raise SystemExit(f"{context} needs explicit evidence_segments")

    experiment_keys: set[str] = set()
    for index, experiment in enumerate(value["experiments"], 1):
        context = f"code-evidence experiment {index}"
        if not isinstance(experiment, dict):
            raise SystemExit(f"{context} must be an object")
        require_exact_keys(
            experiment,
            {
                "experiment_key",
                "instruction_segments",
                "kind",
                "runner_segment_ids",
                "source_rel",
                "unit_id",
            },
            context,
        )
        key = experiment["experiment_key"]
        if key in experiment_keys:
            raise SystemExit(f"duplicate experiment_key {key}")
        experiment_keys.add(key)
        if experiment["kind"] not in {"script_run", "open_ended_challenge"}:
            raise SystemExit(f"{context} has unsupported kind")
        if not experiment["instruction_segments"] or not experiment["runner_segment_ids"]:
            raise SystemExit(f"{context} needs instructions and a runner segment")
        if experiment["kind"] == "script_run":
            if not experiment.get("invocation") or not experiment.get(
                "expected_output_segments"
            ):
                raise SystemExit(f"{context} needs invocation and expected output")
        elif "invocation" in experiment or "expected_output_segments" in experiment:
            raise SystemExit(
                f"{context} must not invent invocation or expected output for an open challenge"
            )

    root_value = value["path_root"]
    if not isinstance(root_value, str) or not root_value:
        raise SystemExit("code-evidence path_root must be a nonempty string")
    path_root = (path.parent / root_value).resolve()
    return value, path_root


def validated_relative_path(path_root: Path, relative: str, context: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts:
        raise SystemExit(f"{context} must be a contained POSIX-relative path")
    resolved = path_root.joinpath(*pure.parts).resolve()
    if not resolved.is_relative_to(path_root):
        raise SystemExit(f"{context} escapes code-evidence path_root")
    return resolved


def declared_octave_function(text: str) -> str | None:
    match = re.search(
        r"(?m)^\s*function\s+(?:\[[^\]]+\]\s*=\s*|[A-Za-z_]\w*\s*=\s*)?"
        r"([A-Za-z_]\w*)\s*\(",
        text,
    )
    return match.group(1) if match else None


def canonical(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(records, key=lambda item: item["id"])
    payload = "".join(canonical(record) + "\n" for record in ordered)
    path.write_text(payload, encoding="utf-8", newline="\n")


def matching_end(lines: list[str], start: int, begin: str, end: str) -> int:
    depth = 0
    for index in range(start, len(lines)):
        if lines[index].startswith(begin):
            depth += 1
        elif lines[index].startswith(end):
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"unclosed block beginning at line {start + 1}: {begin}")


def top_level_layouts(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    body = False
    layouts: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line == "\\begin_body":
            body = True
        elif line == "\\end_body":
            body = False
        elif body and line.startswith("\\begin_layout "):
            end = matching_end(lines, index, "\\begin_layout ", "\\end_layout")
            raw_lines = lines[index : end + 1]
            layouts.append(
                {
                    "ordinal": len(layouts) + 1,
                    "layout": line.removeprefix("\\begin_layout "),
                    "start_line": index + 1,
                    "end_line": end + 1,
                    "lines": raw_lines,
                    "raw": "\n".join(raw_lines) + "\n",
                }
            )
            index = end
        index += 1
    return layouts


def inset_payload(lines: list[str], start: int, end: int) -> str:
    keep: list[str] = []
    for line in lines[start + 1 : end]:
        if line.startswith("\\") or not line.strip() or line.startswith("status "):
            continue
        keep.append(line.strip())
    return " ".join(keep)


def decode_ert_latex(lines: list[str], start: int, end: int) -> str:
    """Decode the line-oriented LaTeX payload of one LyX ERT inset.

    LyX stores each LaTeX output line in a ``Plain Layout`` and represents a
    literal backslash with a standalone ``\\backslash`` control line.  Joining
    text within a layout and layouts with newlines gives a stable, useful code
    representation while the untouched inset bytes remain separately hashed.
    """

    output_lines: list[str] = []
    index = start + 1
    while index < end:
        if not lines[index].startswith("\\begin_layout "):
            index += 1
            continue
        layout_end = matching_end(lines, index, "\\begin_layout ", "\\end_layout")
        pieces: list[str] = []
        pending_backslashes = ""
        for line in lines[index + 1 : layout_end]:
            if line == "\\backslash":
                pending_backslashes += "\\"
            elif line.startswith("\\") or not line:
                continue
            else:
                pieces.append(pending_backslashes + line)
                pending_backslashes = ""
        pieces.append(pending_backslashes)
        output_lines.append("".join(pieces))
        index = layout_end + 1
    return "\n".join(output_lines)


def verbatim_code(latex: str) -> str | None:
    """Return code inside one real LaTeX verbatim environment, if present."""

    begin = "\\begin{verbatim}"
    end = "\\end{verbatim}"
    begin_at = latex.find(begin)
    if begin_at < 0:
        return None
    content_at = begin_at + len(begin)
    end_at = latex.find(end, content_at)
    if end_at < 0:
        return None
    return latex[content_at:end_at].strip("\n")


def embedded_verbatim_blocks(block: dict[str, Any]) -> list[dict[str, Any]]:
    """Find genuine verbatim-code ERTs using semantic-text inset ordinals.

    The traversal deliberately mirrors :func:`semantic_text`: recognised
    atomic insets are skipped as a unit, while container insets are traversed.
    ERT alone is never evidence of code; both verbatim environment delimiters
    must occur in the decoded ERT payload.
    """

    lines = block["lines"]
    blocks: list[dict[str, Any]] = []
    index = 1
    inset_ordinal = 0
    atomic_kinds = {
        "CommandInset",
        "Formula",
        "Graphics",
        "Index",
        "Quotes",
        "Separator",
        "VSpace",
        "space",
    }
    while index < len(lines) - 1:
        line = lines[index]
        if not line.startswith("\\begin_inset "):
            index += 1
            continue
        inset_end = matching_end(lines, index, "\\begin_inset ", "\\end_inset")
        header = line.removeprefix("\\begin_inset ")
        kind = header.split()[0]
        inset_ordinal += 1
        if kind == "ERT":
            raw = "\n".join(lines[index : inset_end + 1]) + "\n"
            latex = decode_ert_latex(lines, index, inset_end)
            code = verbatim_code(latex)
            if code is not None:
                blocks.append(
                    {
                        "ordinal": inset_ordinal,
                        "start_line": block["start_line"] + index,
                        "end_line": block["start_line"] + inset_end,
                        "raw": raw,
                        "raw_sha256": digest_text(raw),
                        "code": code,
                        "code_sha256": digest_text(code),
                        "protected_token": {
                            "ordinal": inset_ordinal,
                            "kind": "ERT",
                            "header": header,
                            "sha256": digest_text(raw),
                            "payload": inset_payload(lines, index, inset_end),
                        },
                    }
                )
            index = inset_end + 1
            continue
        if kind in atomic_kinds or (kind == "Flex" and header == "Flex URL"):
            index = inset_end + 1
            continue
        index += 1
    return blocks


def semantic_text(block: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    lines = block["lines"]
    pieces: list[str] = []
    protected: list[dict[str, Any]] = []
    index = 1  # skip the top-level begin_layout line
    inset_ordinal = 0
    metadata = re.compile(
        r'^(status |LatexCommand |target |literal |name |type |preview |placement |wide |sideways |<|rows=|columns=|alignment=|valignment=|usebox=)'
    )
    while index < len(lines) - 1:
        line = lines[index]
        if line.startswith("\\begin_layout "):
            # Separate reader text from adjacent nested layouts (for example,
            # distinct cells in a signature table) without altering words split
            # across ordinary LyX source lines.
            pieces.append(" ")
        elif line.startswith("\\begin_inset "):
            end = matching_end(lines, index, "\\begin_inset ", "\\end_inset")
            header = line.removeprefix("\\begin_inset ")
            kind = header.split()[0]
            raw = "\n".join(lines[index : end + 1]) + "\n"
            inset_ordinal += 1
            item: dict[str, Any] = {
                "ordinal": inset_ordinal,
                "kind": kind,
                "header": header,
                "sha256": digest_text(raw),
            }
            if kind == "ERT":
                item["payload"] = inset_payload(lines, index, end)
                pieces.append(f"{{{{ERT:{inset_ordinal}}}}}")
                protected.append(item)
                index = end + 1
                continue
            if kind == "CommandInset":
                command_kind = header.split(maxsplit=1)[1] if " " in header else ""
                item["command_kind"] = command_kind
                for candidate in lines[index : end + 1]:
                    match = re.match(r'^(target|name) "(.*)"$', candidate)
                    if match:
                        item[match.group(1)] = match.group(2)
                    reference = re.match(r'^reference "(.*)"$', candidate)
                    if reference:
                        item["reference"] = reference.group(1)
                    cite_key = re.match(r'^key "(.*)"$', candidate)
                    if cite_key:
                        item["key"] = cite_key.group(1)
                if command_kind == "href":
                    pieces.append(f"{{{{HREF:{inset_ordinal}}}}}")
                elif command_kind == "ref":
                    pieces.append(f"{{{{REF:{inset_ordinal}}}}}")
                elif command_kind == "citation":
                    pieces.append(f"{{{{CITE:{inset_ordinal}}}}}")
                protected.append(item)
                index = end + 1
                continue
            if kind == "Formula":
                pieces.append(f"{{{{MATH:{inset_ordinal}}}}}")
                protected.append(item)
                index = end + 1
                continue
            if kind == "Graphics":
                pieces.append(f"{{{{GRAPHIC:{inset_ordinal}}}}}")
                protected.append(item)
                index = end + 1
                continue
            if kind == "Index":
                protected.append(item)
                index = end + 1
                continue
            if kind == "Quotes":
                quote_kind = header.split(maxsplit=1)[1] if " " in header else ""
                pieces.append("“" if quote_kind.endswith("ld") else "”")
                protected.append(item)
                index = end + 1
                continue
            if kind == "Flex" and header == "Flex URL":
                item["payload"] = inset_payload(lines, index, end)
                pieces.append(item["payload"])
                protected.append(item)
                index = end + 1
                continue
            if kind in {"Separator", "VSpace", "space"}:
                protected.append(item)
                index = end + 1
                continue
            protected.append(item)
            index += 1
            continue
        if line.startswith("\\SpecialChar "):
            name = line.removeprefix("\\SpecialChar ")
            pieces.append("…" if name == "ldots" else f"{{{{SPECIAL:{name}}}}}")
        elif line.startswith("\\") or not line.strip() or metadata.match(line):
            pass
        else:
            pieces.append(line)
        index += 1
    text = re.sub(r"\s+", " ", "".join(pieces)).strip()
    return text, protected


def record_base(schema_id: str, record_id: str, record_type: str) -> dict[str, Any]:
    return {
        "schema_id": schema_id,
        "schema_version": SCHEMA_VERSION,
        "id": record_id,
        "record_type": record_type,
    }


def heading_rank(layout: str) -> int | None:
    clean = layout.rstrip("*")
    return {
        "Chapter": 1,
        "Section": 2,
        "Subsection": 3,
        "Subsubsection": 4,
    }.get(clean)


def heading_kind(layout: str) -> str:
    return layout.rstrip("*").lower()


def validated_segment_references(
    references: list[dict[str, Any]],
    segment_by_id: dict[str, dict[str, Any]],
    context: str,
) -> list[str]:
    ids: list[str] = []
    for index, reference in enumerate(references, 1):
        if not isinstance(reference, dict):
            raise SystemExit(f"{context} reference {index} must be an object")
        require_exact_keys(
            reference,
            {"id", "source_text_sha256"},
            f"{context} reference {index}",
        )
        segment = segment_by_id.get(reference["id"])
        if segment is None:
            raise SystemExit(f"{context} missing segment {reference['id']}")
        if segment["source_text_sha256"] != reference["source_text_sha256"]:
            raise SystemExit(f"{context} segment hash drift: {reference['id']}")
        ids.append(reference["id"])
    if len(ids) != len(set(ids)):
        raise SystemExit(f"{context} contains duplicate segment references")
    return ids


def add_unique_record(
    records: dict[str, dict[str, Any]], record: dict[str, Any], context: str
) -> None:
    prior = records.get(record["id"])
    if prior is not None and canonical(prior) != canonical(record):
        raise SystemExit(f"{context} stable-ID collision: {record['id']}")
    records[record["id"]] = record


def build_code_evidence_layer(
    evidence: dict[str, Any],
    path_root: Path,
    source_rel: str,
    resource_id: str,
    edition_id: str,
    source_file_id: str,
    text_rights_id: str,
    code_rights_id: str,
    segments: list[dict[str, Any]],
    units: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    int,
]:
    segment_by_id = {item["id"]: item for item in segments}
    unit_by_id = {item["id"]: item for item in units}
    asset_by_id: dict[str, dict[str, Any]] = {}
    version_by_id: dict[str, dict[str, Any]] = {}
    relation_by_id: dict[str, dict[str, Any]] = {}
    experiment_by_id: dict[str, dict[str, Any]] = {}
    version_by_segment: dict[str, str] = {}
    normalizer_id = evidence["normalizer"]["id"]
    source_mappings = sorted(
        (
            item
            for item in evidence["mappings"]
            if item["source_rel"].replace("\\", "/") == source_rel
        ),
        key=lambda item: item["segment_id"],
    )

    relation_for_match = {
        "normalized_full_equal": "normalized_equivalent_to",
        "exact_excerpt": "exact_excerpt_of",
        "documented_revision": "documented_revision_of",
    }
    for mapping in source_mappings:
        context = f"mapping {mapping['segment_id']}"
        segment = segment_by_id.get(mapping["segment_id"])
        if segment is None:
            raise SystemExit(f"{context} is missing from generated source segments")
        if segment.get("semantic_slot") != "code_block":
            raise SystemExit(f"{context} does not identify a code segment")
        if segment["source_locator"] != mapping["source_locator"]:
            raise SystemExit(f"{context} source locator drift")
        source_bytes = segment["source_text"].encode("utf-8")
        source_normalized = normalize_octave_text(segment["source_text"])
        source_normalized_bytes = source_normalized.encode("utf-8")
        checks = {
            "source_text_bytes": len(source_bytes),
            "source_text_sha256": digest_bytes(source_bytes),
            "source_block_sha256": segment["source_block_sha256"],
            "source_normalized_bytes": len(source_normalized_bytes),
            "source_normalized_sha256": digest_bytes(source_normalized_bytes),
        }
        for field, observed in checks.items():
            if mapping[field] != observed:
                raise SystemExit(
                    f"{context} {field} drift: expected {mapping[field]!r}, observed {observed!r}"
                )

        evidence_segment_ids = validated_segment_references(
            mapping["evidence_segments"], segment_by_id, context
        )
        asset_relative = mapping["asset_path"].replace("\\", "/")
        asset_path = validated_relative_path(path_root, asset_relative, f"{context} asset_path")
        try:
            asset_bytes = asset_path.read_bytes()
            asset_text = asset_bytes.decode("utf-8")
        except (OSError, UnicodeDecodeError) as error:
            raise SystemExit(f"{context} cannot read UTF-8 asset {asset_relative}: {error}") from error
        asset_normalized = normalize_octave_text(asset_text)
        asset_normalized_bytes = asset_normalized.encode("utf-8")
        asset_checks = {
            "asset_raw_bytes": len(asset_bytes),
            "asset_raw_sha256": digest_bytes(asset_bytes),
            "asset_normalized_bytes": len(asset_normalized_bytes),
            "asset_normalized_sha256": digest_bytes(asset_normalized_bytes),
        }
        for field, observed in asset_checks.items():
            if mapping[field] != observed:
                raise SystemExit(
                    f"{context} {field} drift: expected {mapping[field]!r}, observed {observed!r}"
                )

        match_kind = mapping["match_kind"]
        if match_kind == "normalized_full_equal":
            if source_normalized_bytes != asset_normalized_bytes:
                raise SystemExit(f"{context} is not a normalized full-file match")
        elif match_kind == "exact_excerpt":
            start, end = mapping["asset_line_range"]
            asset_lines = asset_normalized.split("\n")
            if end > len(asset_lines):
                raise SystemExit(f"{context} excerpt line range exceeds asset")
            excerpt = "\n".join(asset_lines[start - 1 : end]).encode("utf-8")
            if source_normalized_bytes != excerpt:
                raise SystemExit(f"{context} is not the declared exact excerpt")
        else:
            declared = mapping["declared_function"]
            if declared_octave_function(segment["source_text"]) != declared:
                raise SystemExit(f"{context} source function declaration drift")
            if declared_octave_function(asset_text) != declared:
                raise SystemExit(f"{context} asset function declaration drift")

        asset_id = stable_id("asset", asset_relative)
        version_id = stable_id(
            "asset_version", f"{asset_id}|sha256:{mapping['asset_raw_sha256']}"
        )
        asset_record = {
            **record_base("ttna-asset-v1", asset_id, "asset"),
            "resource_id": resource_id,
            "logical_path": asset_relative,
            "media_type": "text/x-octave",
            "runtime": "GNU Octave",
            "rights_id": code_rights_id,
        }
        version_record = {
            **record_base("ttna-asset-version-v1", version_id, "asset_version"),
            "asset_id": asset_id,
            "edition_id": edition_id,
            "source_path": asset_relative,
            "source_bytes": len(asset_bytes),
            "source_sha256": digest_bytes(asset_bytes),
            "normalization_id": normalizer_id,
            "normalized_bytes": len(asset_normalized_bytes),
            "normalized_sha256": digest_bytes(asset_normalized_bytes),
            "rights_id": code_rights_id,
        }
        add_unique_record(asset_by_id, asset_record, context)
        add_unique_record(version_by_id, version_record, context)
        version_by_segment[segment["id"]] = version_id

        version_relation = {
            **record_base(
                "ttna-relation-v1",
                stable_id("relation", f"{version_id}|version_of|{asset_id}"),
                "relation",
            ),
            "relation": "version_of",
            "from_id": version_id,
            "to_id": asset_id,
        }
        add_unique_record(relation_by_id, version_relation, context)
        mapping_relation_name = relation_for_match[match_kind]
        mapping_relation = {
            **record_base(
                "ttna-relation-v1",
                stable_id(
                    "relation",
                    f"{segment['id']}|{mapping_relation_name}|{version_id}",
                ),
                "relation",
            ),
            "relation": mapping_relation_name,
            "from_id": segment["id"],
            "to_id": version_id,
            "match_kind": match_kind,
            "normalization_id": normalizer_id,
            "evidence_segment_ids": evidence_segment_ids,
        }
        if match_kind == "exact_excerpt":
            mapping_relation["asset_line_range"] = mapping["asset_line_range"]
        if match_kind == "documented_revision":
            mapping_relation["declared_function"] = mapping["declared_function"]
        add_unique_record(relation_by_id, mapping_relation, context)

    source_experiments = sorted(
        (
            item
            for item in evidence["experiments"]
            if item["source_rel"].replace("\\", "/") == source_rel
        ),
        key=lambda item: item["experiment_key"],
    )
    for spec in source_experiments:
        context = f"experiment {spec['experiment_key']}"
        unit_id = spec["unit_id"]
        if unit_id not in unit_by_id:
            raise SystemExit(f"{context} missing unit {unit_id}")
        instruction_ids = validated_segment_references(
            spec["instruction_segments"], segment_by_id, context
        )
        runner_segment_ids = spec["runner_segment_ids"]
        if len(runner_segment_ids) != len(set(runner_segment_ids)):
            raise SystemExit(f"{context} contains duplicate runner segments")
        runner_version_ids: list[str] = []
        for runner_segment_id in runner_segment_ids:
            if runner_segment_id not in segment_by_id:
                raise SystemExit(f"{context} missing runner segment {runner_segment_id}")
            version_id = version_by_segment.get(runner_segment_id)
            if version_id is None:
                raise SystemExit(
                    f"{context} runner segment lacks an exact code-evidence mapping: "
                    f"{runner_segment_id}"
                )
            runner_version_ids.append(version_id)
        output_ids = validated_segment_references(
            spec.get("expected_output_segments", []), segment_by_id, context
        )
        parameter_ids = validated_segment_references(
            spec.get("parameter_evidence_segments", []), segment_by_id, context
        )

        experiment_id = stable_id("experiment", spec["experiment_key"])
        experiment_record = {
            **record_base("ttna-experiment-v1", experiment_id, "experiment"),
            "resource_id": resource_id,
            "edition_id": edition_id,
            "source_file_id": source_file_id,
            "unit_id": unit_id,
            "experiment_key": spec["experiment_key"],
            "kind": spec["kind"],
            "instruction_segment_ids": instruction_ids,
            "runner_segment_ids": runner_segment_ids,
            "runner_asset_version_ids": runner_version_ids,
            "rights_mode": "mixed",
            "rights_ids": [text_rights_id, code_rights_id],
        }
        if "invocation" in spec:
            experiment_record["invocation"] = spec["invocation"]
        if output_ids:
            experiment_record["expected_output_segment_ids"] = output_ids
        if parameter_ids:
            experiment_record["parameter_evidence_segment_ids"] = parameter_ids
        for optional_field in ("objective_code", "result_mode"):
            if optional_field in spec:
                experiment_record[optional_field] = spec[optional_field]
        add_unique_record(experiment_by_id, experiment_record, context)

        relation_specs: list[tuple[str, str]] = [("scoped_to", unit_id)]
        relation_specs.extend(("defined_by", item) for item in instruction_ids)
        relation_specs.extend(("uses", item) for item in runner_version_ids)
        relation_specs.extend(("presented_by", item) for item in runner_segment_ids)
        relation_specs.extend(("expected_output", item) for item in output_ids)
        relation_specs.extend(
            ("parameterized_by_evidence", item) for item in parameter_ids
        )
        for relation_name, to_id in relation_specs:
            relation = {
                **record_base(
                    "ttna-relation-v1",
                    stable_id(
                        "relation", f"{experiment_id}|{relation_name}|{to_id}"
                    ),
                    "relation",
                ),
                "relation": relation_name,
                "from_id": experiment_id,
                "to_id": to_id,
            }
            add_unique_record(relation_by_id, relation, context)

    return (
        list(asset_by_id.values()),
        list(version_by_id.values()),
        list(experiment_by_id.values()),
        list(relation_by_id.values()),
        len(source_mappings),
    )


def validate_local_relation_closure(outputs: list[tuple[Path, list[dict[str, Any]]]]) -> None:
    records = [record for _, group in outputs for record in group]
    by_id = {record["id"]: record for record in records}
    if len(by_id) != len(records):
        raise SystemExit("pack contains duplicate stable IDs")
    for record in records:
        if record["record_type"] != "relation":
            continue
        if record["from_id"] not in by_id or record["to_id"] not in by_id:
            raise SystemExit(f"unresolved local relation: {record['id']}")
        for evidence_id in record.get("evidence_segment_ids", []):
            if evidence_id not in by_id:
                raise SystemExit(
                    f"unresolved relation evidence segment: {record['id']} {evidence_id}"
                )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--source-rel", required=True)
    parser.add_argument("--target-rel", required=True)
    parser.add_argument("--terms-csv", required=True, type=Path)
    parser.add_argument("--code-evidence", required=True, type=Path)
    parser.add_argument("--file-order", required=True, type=int)
    parser.add_argument("--file-kind", default="included_file")
    parser.add_argument("--source-role", default="included_child")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    code_evidence, evidence_path_root = load_code_evidence(args.code_evidence)

    source_bytes = args.source.read_bytes()
    target_bytes = args.target.read_bytes()
    source_text = source_bytes.decode("utf-8")
    target_text = target_bytes.decode("utf-8")
    source_layouts = top_level_layouts(source_text)
    target_layouts = top_level_layouts(target_text)
    source_shape = [item["layout"] for item in source_layouts]
    target_shape = [item["layout"] for item in target_layouts]
    if source_shape != target_shape:
        raise SystemExit("source/target top-level LyX layout topology differs")

    source_embedded_by_layout = {
        block["ordinal"]: embedded_verbatim_blocks(block) for block in source_layouts
    }
    target_embedded_by_layout = {
        block["ordinal"]: embedded_verbatim_blocks(block) for block in target_layouts
    }
    for ordinal in source_embedded_by_layout:
        source_ordinals = [item["ordinal"] for item in source_embedded_by_layout[ordinal]]
        target_ordinals = [item["ordinal"] for item in target_embedded_by_layout[ordinal]]
        if source_ordinals != target_ordinals:
            raise SystemExit(
                "source/target embedded verbatim-code topology differs "
                f"at top-level layout {ordinal}"
            )
    source_has_code = any(item["layout"] == "LyX-Code" for item in source_layouts) or any(
        source_embedded_by_layout.values()
    )

    resource_id = stable_id("resource", RESOURCE_URL)
    edition_id = stable_id("edition", EDITION_COMMIT)
    work_unit_id = stable_id("unit", "work")
    file_key = args.source_rel.replace("\\", "/")
    source_file_id = stable_id("source_file", file_key)
    file_unit_id = stable_id("unit", file_key)
    text_rights_id = stable_id("rights", "CC-BY-SA-4.0|book-text")
    code_rights_id = stable_id("rights", "GPL-3.0-or-later|code")

    resources = [
        {
            **record_base("ttna-resource-v1", resource_id, "resource"),
            "resource_local_id": "R015",
            "course_local_id": "C110",
            "title": "Tea Time Numerical Analysis",
            "author": "Leon Q. Brin",
            "authority_url": RESOURCE_URL,
        }
    ]
    editions = [
        {
            **record_base("ttna-edition-v1", edition_id, "edition"),
            "resource_id": resource_id,
            "edition_label": "Third Edition",
            "tag": "v3.0",
            "commit": EDITION_COMMIT,
            "tree": EDITION_TREE,
            "source_locale": "en-US",
            "target_locale": "id-ID",
        }
    ]
    source_file_record = {
        **record_base("ttna-source-file-v1", source_file_id, "source_file"),
        "edition_id": edition_id,
        "source_path": args.source_rel.replace("\\", "/"),
        "source_bytes": len(source_bytes),
        "source_sha256": digest_bytes(source_bytes),
        "target_path": args.target_rel.replace("\\", "/"),
        "target_bytes": len(target_bytes),
        "target_sha256": digest_bytes(target_bytes),
        "format": "LyX 2.3 / format 544",
        "role": args.source_role,
        "rights_id": text_rights_id,
    }
    if source_has_code:
        source_file_record.update(
            {
                "rights_mode": "mixed",
                "rights_ids": [text_rights_id, code_rights_id],
                "content_kinds": ["text", "code"],
            }
        )
    source_files = [source_file_record]

    work_unit_record = {
        **record_base("ttna-unit-v1", work_unit_id, "unit"),
        "edition_id": edition_id,
        "kind": "work",
        "source_local_id": "TeaTimeNumericalAnalysis",
        "parent_id": None,
        "order": 1,
        "rights_id": text_rights_id,
    }
    file_unit_record = {
        **record_base("ttna-unit-v1", file_unit_id, "unit"),
        "edition_id": edition_id,
        "kind": args.file_kind,
        "source_file_id": source_file_id,
        "source_local_id": Path(args.source_rel).name,
        "parent_id": work_unit_id,
        "order": args.file_order,
        "rights_id": text_rights_id,
    }
    if source_has_code:
        file_unit_record.update(
            {
                "rights_mode": "mixed",
                "rights_ids": [text_rights_id, code_rights_id],
                "content_kinds": ["text", "code"],
            }
        )
    units: list[dict[str, Any]] = [work_unit_record, file_unit_record]
    relations: list[dict[str, Any]] = []
    segments: list[dict[str, Any]] = []
    localizations: list[dict[str, Any]] = []
    relations.append(
        {
            **record_base("ttna-relation-v1", stable_id("relation", f"{work_unit_id}|contains|{file_unit_id}"), "relation"),
            "relation": "contains",
            "from_id": work_unit_id,
            "to_id": file_unit_id,
            "order": args.file_order,
        }
    )

    heading_stack: dict[int, str] = {}
    current_parent = file_unit_id
    segment_order_by_parent: dict[str, int] = {}
    unit_order_by_parent: dict[str, int] = {}
    mixed_unit_ids: set[str] = {file_unit_id} if source_has_code else set()

    for source_block, target_block in zip(source_layouts, target_layouts):
        source_value, source_protected = semantic_text(source_block)
        target_value, target_protected = semantic_text(target_block)
        ordinal = source_block["ordinal"]
        layout = source_block["layout"]
        rank = heading_rank(layout)
        if rank is not None:
            for stale_rank in [item for item in heading_stack if item >= rank]:
                heading_stack.pop(stale_rank)
            parent_id = heading_stack[max(heading_stack)] if heading_stack else file_unit_id
            unit_id = stable_id("unit", f"{file_key}|layout:{ordinal}|{layout}")
            unit_order_by_parent[parent_id] = unit_order_by_parent.get(parent_id, 0) + 1
            units.append(
                {
                    **record_base("ttna-unit-v1", unit_id, "unit"),
                    "edition_id": edition_id,
                    "kind": heading_kind(layout),
                    "source_file_id": source_file_id,
                    "source_local_id": f"{Path(args.source_rel).stem}.layout.{ordinal}",
                    "parent_id": parent_id,
                    "order": unit_order_by_parent[parent_id],
                    "source_title": source_value,
                    "rights_id": text_rights_id,
                }
            )
            relations.append(
                {
                    **record_base("ttna-relation-v1", stable_id("relation", f"{parent_id}|contains|{unit_id}"), "relation"),
                    "relation": "contains",
                    "from_id": parent_id,
                    "to_id": unit_id,
                    "order": unit_order_by_parent[parent_id],
                }
            )
            heading_stack[rank] = unit_id
            current_parent = unit_id
            role = "title"
        else:
            current_parent = heading_stack[max(heading_stack)] if heading_stack else file_unit_id
            role = {
                "Itemize": "list_item",
                "Enumerate": "list_item",
                "LyX-Code": "code_block",
            }.get(layout, "paragraph")
            if not source_value and source_block["raw"] != target_block["raw"]:
                role = "navigation_ert"

        if not source_value and source_block["raw"] == target_block["raw"]:
            continue

        segment_key = f"{file_key}|layout:{ordinal}|{role}"
        segment_id = stable_id("segment", segment_key)
        localization_id = stable_id("localization", f"{segment_id}|id-ID")
        segment_order_by_parent[current_parent] = segment_order_by_parent.get(current_parent, 0) + 1
        source_protected_shape = [item["kind"] for item in source_protected]
        target_protected_shape = [item["kind"] for item in target_protected]
        segment_rights_id = code_rights_id if role == "code_block" else text_rights_id
        if role == "code_block":
            mixed_unit_ids.add(current_parent)
        segments.append(
            {
                **record_base("ttna-segment-v1", segment_id, "segment"),
                "edition_id": edition_id,
                "unit_id": current_parent,
                "source_file_id": source_file_id,
                "source_locator": {
                    "layout_ordinal": ordinal,
                    "layout": layout,
                    "start_line": source_block["start_line"],
                    "end_line": source_block["end_line"],
                },
                "semantic_slot": role,
                "order": segment_order_by_parent[current_parent],
                "source_locale": "en-US",
                "source_text": source_value,
                "source_text_sha256": digest_text(source_value),
                "source_block_sha256": digest_text(source_block["raw"]),
                "protected_tokens": source_protected,
                "rights_id": segment_rights_id,
                "translation_state": "source_frozen",
            }
        )
        changed = source_value != target_value or source_block["raw"] != target_block["raw"]
        localizations.append(
            {
                **record_base("ttna-localization-v1", localization_id, "localization"),
                "segment_id": segment_id,
                "source_segment_sha256": digest_text(source_value),
                "locale": "id-ID",
                "target_path": args.target_rel.replace("\\", "/"),
                "target_locator": {
                    "layout_ordinal": ordinal,
                    "layout": target_block["layout"],
                    "start_line": target_block["start_line"],
                    "end_line": target_block["end_line"],
                },
                "target_text": target_value,
                "target_text_sha256": digest_text(target_value),
                "target_block_sha256": digest_text(target_block["raw"]),
                "protected_tokens": target_protected,
                "protected_token_shape_equal": source_protected_shape == target_protected_shape,
                "workflow_state": "translated" if changed else "translated_unchanged",
                "structure_state": "structurally_verified",
                "math_state": "not_applicable",
                "language_state": "draft_translated",
                "build_state": "not_built",
                "publication_state": "unpublished",
                "interchange_state": "structurally_verified",
                "provenance": "OpenAI Codex gpt-5.6-sol, Ultra, at the user's request",
            }
        )
        relations.append(
            {
                **record_base("ttna-relation-v1", stable_id("relation", f"{current_parent}|contains|{segment_id}"), "relation"),
                "relation": "contains",
                "from_id": current_parent,
                "to_id": segment_id,
                "order": segment_order_by_parent[current_parent],
            }
        )
        relations.append(
            {
                **record_base("ttna-relation-v1", stable_id("relation", f"{localization_id}|translates|{segment_id}"), "relation"),
                "relation": "translates",
                "from_id": localization_id,
                "to_id": segment_id,
            }
        )

        target_code_by_ordinal = {
            item["ordinal"]: item for item in target_embedded_by_layout[ordinal]
        }
        for source_code in source_embedded_by_layout[ordinal]:
            target_code = target_code_by_ordinal[source_code["ordinal"]]
            ert_ordinal = source_code["ordinal"]
            code_key = (
                f"{file_key}|layout:{ordinal}|ert:{ert_ordinal}|embedded_verbatim_code"
            )
            code_segment_id = stable_id("segment", code_key)
            code_localization_id = stable_id(
                "localization", f"{code_segment_id}|id-ID"
            )
            code_changed = (
                source_code["code"] != target_code["code"]
                or source_code["raw"] != target_code["raw"]
            )
            code_order = segment_order_by_parent[current_parent]
            source_code_shape = [source_code["protected_token"]["kind"]]
            target_code_shape = [target_code["protected_token"]["kind"]]
            segments.append(
                {
                    **record_base(
                        "ttna-segment-v1", code_segment_id, "segment"
                    ),
                    "edition_id": edition_id,
                    "unit_id": current_parent,
                    "source_file_id": source_file_id,
                    "source_locator": {
                        "layout_ordinal": ordinal,
                        "layout": layout,
                        "ert_ordinal": ert_ordinal,
                        "start_line": source_code["start_line"],
                        "end_line": source_code["end_line"],
                    },
                    "semantic_slot": "code_block",
                    "code_origin": "embedded_ert",
                    "code_environment": "verbatim",
                    "embedded_in_segment_id": segment_id,
                    "order": code_order,
                    "suborder": ert_ordinal,
                    "source_locale": "en-US",
                    "source_text": source_code["code"],
                    "source_text_sha256": source_code["code_sha256"],
                    "source_block_sha256": source_code["raw_sha256"],
                    "source_ert_sha256": source_code["raw_sha256"],
                    "protected_tokens": [source_code["protected_token"]],
                    "rights_id": code_rights_id,
                    "translation_state": "source_frozen",
                }
            )
            localizations.append(
                {
                    **record_base(
                        "ttna-localization-v1",
                        code_localization_id,
                        "localization",
                    ),
                    "segment_id": code_segment_id,
                    "source_segment_sha256": source_code["code_sha256"],
                    "locale": "id-ID",
                    "target_path": args.target_rel.replace("\\", "/"),
                    "target_locator": {
                        "layout_ordinal": ordinal,
                        "layout": target_block["layout"],
                        "ert_ordinal": ert_ordinal,
                        "start_line": target_code["start_line"],
                        "end_line": target_code["end_line"],
                    },
                    "target_text": target_code["code"],
                    "target_text_sha256": target_code["code_sha256"],
                    "target_block_sha256": target_code["raw_sha256"],
                    "target_ert_sha256": target_code["raw_sha256"],
                    "protected_tokens": [target_code["protected_token"]],
                    "protected_token_shape_equal": source_code_shape
                    == target_code_shape,
                    "workflow_state": (
                        "translated" if code_changed else "translated_unchanged"
                    ),
                    "structure_state": "structurally_verified",
                    "math_state": "not_applicable",
                    "language_state": "not_applicable",
                    "code_state": "modified" if code_changed else "unchanged",
                    "build_state": "not_built",
                    "publication_state": "unpublished",
                    "interchange_state": "structurally_verified",
                    "provenance": "OpenAI Codex gpt-5.6-sol, Ultra, at the user's request",
                }
            )
            relations.append(
                {
                    **record_base(
                        "ttna-relation-v1",
                        stable_id(
                            "relation",
                            f"{current_parent}|contains|{code_segment_id}",
                        ),
                        "relation",
                    ),
                    "relation": "contains",
                    "from_id": current_parent,
                    "to_id": code_segment_id,
                    "order": code_order,
                    "suborder": ert_ordinal,
                }
            )
            relations.append(
                {
                    **record_base(
                        "ttna-relation-v1",
                        stable_id(
                            "relation",
                            f"{code_localization_id}|translates|{code_segment_id}",
                        ),
                        "relation",
                    ),
                    "relation": "translates",
                    "from_id": code_localization_id,
                    "to_id": code_segment_id,
                }
            )
            mixed_unit_ids.add(current_parent)

    unit_by_id = {item["id"]: item for item in units}
    pending_mixed_units = list(mixed_unit_ids)
    while pending_mixed_units:
        unit_id = pending_mixed_units.pop()
        if unit_id == work_unit_id:
            continue
        unit = unit_by_id[unit_id]
        unit.update(
            {
                "rights_mode": "mixed",
                "rights_ids": [text_rights_id, code_rights_id],
                "content_kinds": ["text", "code"],
            }
        )
        parent_id = unit.get("parent_id")
        if parent_id and parent_id != work_unit_id and parent_id not in mixed_unit_ids:
            mixed_unit_ids.add(parent_id)
            pending_mixed_units.append(parent_id)

    rights = [
        {
            **record_base("ttna-rights-v1", text_rights_id, "rights"),
            "spdx_expression": "CC-BY-SA-4.0",
            "scope": "book prose, mathematical exposition, and Indonesian translation subject to component review",
            "authority_path": "source/lqbrin-tea-time-numerical-1868821/COPYING.txt",
            "attribution": "Leon Q. Brin, Tea Time Numerical Analysis, Third Edition",
            "modification_notice_required": True,
            "share_alike_required": True,
        },
        {
            **record_base("ttna-rights-v1", code_rights_id, "rights"),
            "spdx_expression": "GPL-3.0-or-later",
            "scope": "code printed within and accompanying the textbook electronically",
            "authority_path": "source/lqbrin-tea-time-numerical-1868821/COPYING.txt",
            "source_required": True,
        },
    ]

    terms: list[dict[str, Any]] = []
    with args.terms_csv.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            term_id = stable_id("term", row["term_id"])
            terms.append(
                {
                    **record_base("ttna-term-v1", term_id, "term"),
                    "source_term_id": row["term_id"],
                    "source_locale": "en-US",
                    "source_term": row["source_term"],
                    "locale": "id-ID",
                    "preferred": row["preferred_id"],
                    "variants": [item for item in row["variants"].split("|") if item],
                    "rejected": [item for item in row["rejected"].split("|") if item],
                    "scope": row["scope"],
                    "evidence": row["evidence"],
                    "status": row["status"],
                }
            )
            needle = row["source_term"].casefold()
            for segment in segments:
                if needle in segment["source_text"].casefold():
                    relations.append(
                        {
                            **record_base(
                                "ttna-relation-v1",
                                stable_id("relation", f"{segment['id']}|uses_term|{term_id}"),
                                "relation",
                            ),
                            "relation": "uses_term",
                            "from_id": segment["id"],
                            "to_id": term_id,
                        }
                    )

    assets, asset_versions, experiments, evidence_relations, mapping_count = (
        build_code_evidence_layer(
            code_evidence,
            evidence_path_root,
            file_key,
            resource_id,
            edition_id,
            source_file_id,
            text_rights_id,
            code_rights_id,
            segments,
            units,
        )
    )
    relations.extend(evidence_relations)

    qa_event_id = stable_id("qa_event", f"{file_key}|structure-v1")
    qa_events = [
        {
            **record_base("ttna-qa-event-v1", qa_event_id, "qa_event"),
            "qa_type": "topology",
            "source_file_id": source_file_id,
            "result": "pass",
            "checks": {
                "top_level_layout_count": len(source_layouts),
                "top_level_layout_sequence_equal": True,
                "emitted_segment_count": len(segments),
                "code_segment_count": sum(
                    item["semantic_slot"] == "code_block" for item in segments
                ),
                "embedded_verbatim_code_segment_count": sum(
                    item.get("code_origin") == "embedded_ert" for item in segments
                ),
                "mixed_rights": source_has_code,
                "code_evidence_mapping_count": mapping_count,
                "asset_count": len(assets),
                "asset_version_count": len(asset_versions),
                "experiment_count": len(experiments),
                "protected_token_shapes_equal": all(
                    item["protected_token_shape_equal"] for item in localizations
                ),
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
        (args.out / "translation" / "localizations.id-ID.jsonl", localizations),
        (args.out / "translation" / "terms.id-ID.jsonl", terms),
        (args.out / "assets" / "assets.jsonl", assets),
        (args.out / "assets" / "versions.jsonl", asset_versions),
        (args.out / "experiments" / "experiments.jsonl", experiments),
        (args.out / "rights" / "components.jsonl", rights),
        (args.out / "qa" / "events.jsonl", qa_events),
    ]
    validate_local_relation_closure(outputs)
    for path, records in outputs:
        write_jsonl(path, records)

    files: list[dict[str, Any]] = []
    for path, records in outputs:
        payload = path.read_bytes()
        files.append(
            {
                "path": path.relative_to(args.out).as_posix(),
                "bytes": len(payload),
                "sha256": digest_bytes(payload),
                "records": len(records),
            }
        )
    manifest = {
        "schema_id": "ttna-lane-manifest-v1",
        "schema_version": SCHEMA_VERSION,
        "generator": GENERATOR_VERSION,
        "recorded_date": RECORDED_DATE,
        "resource_id": resource_id,
        "edition_id": edition_id,
        "locale": "id-ID",
        "source_commit": EDITION_COMMIT,
        "source_tree": EDITION_TREE,
        "scope": args.source_rel.replace("\\", "/"),
        "file_order": args.file_order,
        "file_kind": args.file_kind,
        "files": sorted(files, key=lambda item: item["path"]),
        "counts": {
            "top_level_layouts": len(source_layouts),
            "units": len(units),
            "segments": len(segments),
            "localizations": len(localizations),
            "relations": len(relations),
            "terms": len(terms),
            "assets": len(assets),
            "asset_versions": len(asset_versions),
            "experiments": len(experiments),
        },
    }
    write_json(args.out / "manifests" / "lane_manifest.json", manifest)
    print(canonical(manifest))


if __name__ == "__main__":
    main()
