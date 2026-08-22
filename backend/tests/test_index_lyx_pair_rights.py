from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


BACKEND = Path(__file__).resolve().parents[1]
INDEXER_PATH = BACKEND / "tools" / "index_lyx_pair.py"
SPEC = importlib.util.spec_from_file_location("ttna_index_lyx_pair", INDEXER_PATH)
assert SPEC and SPEC.loader
INDEXER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INDEXER)


VERBATIM_ERT = r"""\begin_inset ERT
status open

\begin_layout Plain Layout

\backslash
begin{verbatim}
\end_layout

\begin_layout Plain Layout

x = 1;
\end_layout

\begin_layout Plain Layout

y = x + 2;
\end_layout

\begin_layout Plain Layout

\backslash
end{verbatim}
\end_layout

\end_inset"""


def control_ert(name: str, body: str = "") -> str:
    suffix = f"\n{body}" if body else ""
    return rf"""\begin_inset ERT
status open

\begin_layout Plain Layout

\backslash
{name}{suffix}
\end_layout

\end_inset"""


def fixture(prose: str) -> str:
    return rf"""#LyX fixture
\begin_body
\begin_layout Standard
{prose}
{VERBATIM_ERT}
 follows.
\end_layout

\begin_layout LyX-Code
disp(x)
\end_layout

\begin_layout Standard
Digression control:
{control_ert('begin{digression}', 'not executable')}
\end_layout

\begin_layout Standard
Pseudocode control:
{control_ert('begin{pseudocode}{Demo}', 'STATE x')}
\end_layout

\begin_layout Standard
Rule control:
{control_ert('hrulefill')}
\end_layout

\begin_layout Standard
Index control:
{control_ert('index{root}')}
\end_layout
\end_body
"""


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class MixedRightsIndexerTest(unittest.TestCase):
    def run_indexer(self, root: Path, output_name: str) -> Path:
        source = root / "source.lyx"
        target = root / "target.lyx"
        terms = root / "terms.csv"
        source.write_text(fixture("An executable example:"), encoding="utf-8", newline="\n")
        target.write_text(fixture("Contoh yang dapat dijalankan:"), encoding="utf-8", newline="\n")
        terms.write_text(
            "term_id,source_term,preferred_id,variants,rejected,scope,evidence,status\n"
            "TTNA-TERM-TEST,absent term,istilah absen,,,test,fixture,accepted\n",
            encoding="utf-8",
            newline="\n",
        )
        evidence = root / "backend" / "config" / "code_evidence.v1.json"
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text(
            json.dumps(
                {
                    "experiments": [],
                    "mappings": [],
                    "normalizer": {"id": "octave-text-v1"},
                    "path_root": "../..",
                    "schema_id": "ttna-code-evidence-map-v1",
                    "schema_version": "1.0.0",
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        output = root / output_name
        subprocess.run(
            [
                sys.executable,
                "-B",
                str(INDEXER_PATH),
                "--source",
                str(source),
                "--target",
                str(target),
                "--source-rel",
                "source/fixture.lyx",
                "--target-rel",
                "translation/fixture.lyx",
                "--terms-csv",
                str(terms),
                "--code-evidence",
                str(evidence),
                "--file-order",
                "1",
                "--out",
                str(output),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return output

    def test_strict_verbatim_classification(self) -> None:
        self.assertEqual(
            INDEXER.verbatim_code("\\begin{verbatim}\nx = 1;\n\\end{verbatim}"),
            "x = 1;",
        )
        for control in (
            "\\begin{digression}\ntext\n\\end{digression}",
            "\\begin{pseudocode}{Demo}\nSTATE x\n\\end{pseudocode}",
            "\\hrulefill",
            "\\index{root}",
            "begin{verbatim} without a LyX-decoded backslash",
            "\\begin{verbatim}\nmissing closing delimiter",
        ):
            self.assertIsNone(INDEXER.verbatim_code(control))

    def test_mixed_rights_records_are_additive_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = self.run_indexer(root, "out-a")
            second = self.run_indexer(root, "out-b")

            first_files = {
                path.relative_to(first).as_posix(): path.read_bytes()
                for path in first.rglob("*")
                if path.is_file()
            }
            second_files = {
                path.relative_to(second).as_posix(): path.read_bytes()
                for path in second.rglob("*")
                if path.is_file()
            }
            self.assertEqual(first_files, second_files)

            manifest = json.loads(
                (first / "manifests" / "lane_manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(manifest["generator"], "ttna-lyx-indexer-0.3.1")
            self.assertEqual(manifest["counts"]["segments"], 7)
            self.assertEqual(manifest["counts"]["localizations"], 7)
            self.assertEqual(manifest["counts"]["assets"], 0)
            self.assertEqual(manifest["counts"]["asset_versions"], 0)
            self.assertEqual(manifest["counts"]["experiments"], 0)

            rights = read_jsonl(first / "rights" / "components.jsonl")
            rights_by_spdx = {item["spdx_expression"]: item["id"] for item in rights}
            text_rights_id = rights_by_spdx["CC-BY-SA-4.0"]
            code_rights_id = rights_by_spdx["GPL-3.0-or-later"]

            source_file = read_jsonl(first / "topology" / "source_files.jsonl")[0]
            self.assertEqual(source_file["rights_mode"], "mixed")
            self.assertEqual(
                source_file["rights_ids"], [text_rights_id, code_rights_id]
            )
            units = read_jsonl(first / "topology" / "units.jsonl")
            file_unit = next(item for item in units if item["kind"] == "included_file")
            work_unit = next(item for item in units if item["kind"] == "work")
            self.assertEqual(file_unit["rights_mode"], "mixed")
            self.assertEqual(file_unit["rights_ids"], [text_rights_id, code_rights_id])
            self.assertNotIn("rights_mode", work_unit)

            segments = read_jsonl(first / "translation" / "segments.en.jsonl")
            localizations = read_jsonl(
                first / "translation" / "localizations.id-ID.jsonl"
            )
            localization_by_segment = {
                item["segment_id"]: item for item in localizations
            }

            surrounding_id = INDEXER.stable_id(
                "segment", "source/fixture.lyx|layout:1|paragraph"
            )
            surrounding = next(item for item in segments if item["id"] == surrounding_id)
            self.assertEqual(surrounding["rights_id"], text_rights_id)
            self.assertIn("{{ERT:1}}", surrounding["source_text"])
            self.assertNotIn("code_origin", surrounding)

            embedded_id = INDEXER.stable_id(
                "segment",
                "source/fixture.lyx|layout:1|ert:1|embedded_verbatim_code",
            )
            embedded = next(item for item in segments if item["id"] == embedded_id)
            self.assertEqual(embedded["rights_id"], code_rights_id)
            self.assertEqual(embedded["code_origin"], "embedded_ert")
            self.assertEqual(embedded["code_environment"], "verbatim")
            self.assertEqual(embedded["embedded_in_segment_id"], surrounding_id)
            self.assertEqual(embedded["source_text"], "x = 1;\ny = x + 2;")
            self.assertEqual(
                embedded["source_text_sha256"],
                hashlib.sha256(embedded["source_text"].encode("utf-8")).hexdigest(),
            )
            self.assertEqual(
                embedded["source_block_sha256"], embedded["source_ert_sha256"]
            )
            self.assertEqual(
                [item["kind"] for item in embedded["protected_tokens"]], ["ERT"]
            )

            embedded_localization = localization_by_segment[embedded_id]
            self.assertEqual(
                embedded_localization["target_text"], embedded["source_text"]
            )
            self.assertEqual(
                embedded_localization["target_text_sha256"],
                embedded["source_text_sha256"],
            )
            self.assertEqual(
                embedded_localization["target_block_sha256"],
                embedded["source_block_sha256"],
            )
            self.assertTrue(embedded_localization["protected_token_shape_equal"])
            self.assertEqual(
                embedded_localization["workflow_state"], "translated_unchanged"
            )
            self.assertEqual(embedded_localization["code_state"], "unchanged")
            self.assertEqual(embedded_localization["language_state"], "not_applicable")

            explicit = next(
                item
                for item in segments
                if item["source_locator"]["layout"] == "LyX-Code"
            )
            self.assertEqual(explicit["rights_id"], code_rights_id)
            self.assertNotIn("code_origin", explicit)
            self.assertEqual(
                localization_by_segment[explicit["id"]]["workflow_state"],
                "translated_unchanged",
            )

            embedded_segments = [
                item for item in segments if item.get("code_origin") == "embedded_ert"
            ]
            self.assertEqual([item["id"] for item in embedded_segments], [embedded_id])
            self.assertFalse(any(item["record_type"] == "experiment" for item in segments))

            relations = read_jsonl(first / "topology" / "relations.jsonl")
            all_records = []
            for path in first.rglob("*.jsonl"):
                all_records.extend(read_jsonl(path))
            known_ids = {item["id"] for item in all_records}
            self.assertTrue(
                all(
                    item["from_id"] in known_ids and item["to_id"] in known_ids
                    for item in relations
                )
            )
            self.assertTrue(
                any(
                    item["relation"] == "contains"
                    and item["from_id"] == file_unit["id"]
                    and item["to_id"] == embedded_id
                    for item in relations
                )
            )
            self.assertTrue(
                any(
                    item["relation"] == "translates"
                    and item["from_id"] == embedded_localization["id"]
                    and item["to_id"] == embedded_id
                    for item in relations
                )
            )

            qa = read_jsonl(first / "qa" / "events.jsonl")[0]
            self.assertEqual(qa["checks"]["code_segment_count"], 2)
            self.assertEqual(
                qa["checks"]["embedded_verbatim_code_segment_count"], 1
            )
            self.assertTrue(qa["checks"]["mixed_rights"])
            self.assertTrue(qa["checks"]["protected_token_shapes_equal"])


if __name__ == "__main__":
    unittest.main()
