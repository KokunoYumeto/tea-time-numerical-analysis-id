from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


BACKEND = Path(__file__).resolve().parents[1]
INDEXER_PATH = BACKEND / "tools" / "index_tex_pair.py"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]


class TexPairIndexerTest(unittest.TestCase):
    def prepare(self, root: Path) -> tuple[Path, Path, Path, Path]:
        source = root / "source.tex"
        target = root / "target.tex"
        terms = root / "terms.csv"
        reader_map = root / "reader-map.json"
        source_text = (
            "\\newcommand{\\titleX}{Tea Time\\\\[.2\\baselineskip]"
            "Numerical Analysis}\n"
            "{\\itshape Experiences in Mathematics, $3^{rd}$ edition}\\par\n"
            "UNCHANGED\n"
        )
        target_text = (
            "\\newcommand{\\titleX}{Tea Time\\\\[.2\\baselineskip]"
            "Numerical Analysis}\n"
            "{\\itshape Pengalaman dalam Matematika, edisi ke-3}\\par\n"
            "UNCHANGED\n"
        )
        source.write_text(source_text, encoding="utf-8", newline="\n")
        target.write_text(target_text, encoding="utf-8", newline="\n")
        terms.write_text(
            "term_id,source_term,preferred_id,variants,rejected,scope,evidence,status\n"
            "TTNA-TERM-TEST,numerical analysis,analisis numerik,,,test,fixture,accepted\n",
            encoding="utf-8",
            newline="\n",
        )
        source_bytes = source.read_bytes()
        reader_map.write_text(
            json.dumps(
                {
                    "schema_id": "ttna-tex-reader-map-v1",
                    "schema_version": "1.0.0",
                    "source_path": "source/fixture.tex",
                    "source_bytes": len(source_bytes),
                    "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
                    "units": [
                        {
                            "key": "titleX",
                            "kind": "title_template",
                            "source_local_id": "fixture.titleX",
                            "order": 1,
                        }
                    ],
                    "segments": [
                        {
                            "key": "titleX.title",
                            "unit_key": "titleX",
                            "line": 1,
                            "prefix": "\\newcommand{\\titleX}{",
                            "suffix": "}",
                            "semantic_slot": "title",
                            "order": 1,
                        },
                        {
                            "key": "titleX.tagline",
                            "unit_key": "titleX",
                            "line": 2,
                            "prefix": "{\\itshape ",
                            "suffix": "}\\par",
                            "semantic_slot": "subtitle",
                            "order": 2,
                        },
                    ],
                },
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return source, target, terms, reader_map

    def run_indexer(
        self,
        root: Path,
        output_name: str,
        *,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        source, target, terms, reader_map = self.prepare(root)
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(INDEXER_PATH),
                "--source",
                str(source),
                "--target",
                str(target),
                "--source-rel",
                "source/fixture.tex",
                "--target-rel",
                "translation/fixture.tex",
                "--terms-csv",
                str(terms),
                "--reader-map",
                str(reader_map),
                "--file-order",
                "-1",
                "--file-kind",
                "build_preamble",
                "--source-role",
                "build_preamble",
                "--out",
                str(root / output_name),
            ],
            check=check,
            capture_output=True,
            text=True,
        )

    def test_emits_reader_fragments_and_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.run_indexer(root, "out-a")
            self.run_indexer(root, "out-b")
            first = root / "out-a"
            second = root / "out-b"
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
            self.assertEqual(manifest["generator"], "ttna-tex-indexer-0.1.0")
            self.assertEqual(manifest["counts"]["segments"], 2)
            self.assertEqual(manifest["counts"]["localizations"], 2)
            self.assertEqual(manifest["counts"]["changed_reader_segments"], 1)

            source_file = read_jsonl(
                first / "topology" / "source_files.jsonl"
            )[0]
            self.assertEqual(source_file["format"], "TeX/LaTeX preamble")
            self.assertEqual(source_file["role"], "build_preamble")

            localizations = read_jsonl(
                first / "translation" / "localizations.id-ID.jsonl"
            )
            self.assertEqual(
                sum(not item["protected_token_shape_equal"] for item in localizations),
                1,
            )
            qa_event = read_jsonl(first / "qa" / "events.jsonl")[0]
            self.assertEqual(
                qa_event["checks"]["protected_token_shape_mismatch_count"], 1
            )
            self.assertEqual(
                qa_event["checks"]["unannotated_changed_line_count"], 0
            )

    def test_rejects_change_outside_reader_map(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, target, _, _ = self.prepare(root)
            target.write_text(
                target.read_text(encoding="utf-8").replace(
                    "UNCHANGED", "UNMAPPED CHANGE"
                ),
                encoding="utf-8",
                newline="\n",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(INDEXER_PATH),
                    "--source",
                    str(source),
                    "--target",
                    str(target),
                    "--source-rel",
                    "source/fixture.tex",
                    "--target-rel",
                    "translation/fixture.tex",
                    "--terms-csv",
                    str(root / "terms.csv"),
                    "--reader-map",
                    str(root / "reader-map.json"),
                    "--file-order",
                    "-1",
                    "--out",
                    str(root / "out"),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("target changes outside reader map: 3", result.stderr)


if __name__ == "__main__":
    unittest.main()
