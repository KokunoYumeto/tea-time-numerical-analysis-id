from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


BACKEND = Path(__file__).resolve().parents[1]
LANE = BACKEND.parent
INDEXER = BACKEND / "tools" / "index_lyx_pair.py"
MERGER = BACKEND / "tools" / "merge_packs.py"
CONFIG = BACKEND / "config" / "code_evidence.v1.json"
TERMS = LANE / "00_control" / "TERMINOLOGY.csv"
SOURCE_PREFIX = "source/lqbrin-tea-time-numerical-1868821/"
TARGET_PREFIX = "translation/lyx-id/"

MAPPED_FILES = {
    "interpolation-challenge.lyx": 13,
    "preliminaries-convergence.lyx": 3,
    "preliminaries-recursion.lyx": 5,
    "preliminaries-taylor.lyx": 6,
    "roots-bisection.lyx": 7,
    "roots-bracketing.lyx": 8,
    "roots-orderOfConvergence.lyx": 11,
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def run_indexer(
    root: Path,
    filename: str,
    file_order: int,
    output_name: str,
    config: Path = CONFIG,
    check: bool = True,
) -> tuple[Path, subprocess.CompletedProcess[str]]:
    output = root / output_name
    command = [
        sys.executable,
        "-B",
        str(INDEXER),
        "--source",
        str(LANE / SOURCE_PREFIX / filename),
        "--target",
        str(LANE / TARGET_PREFIX / filename),
        "--source-rel",
        SOURCE_PREFIX + filename,
        "--target-rel",
        TARGET_PREFIX + filename,
        "--terms-csv",
        str(TERMS),
        "--code-evidence",
        str(config),
        "--file-order",
        str(file_order),
        "--out",
        str(output),
    ]
    completed = subprocess.run(command, check=check, capture_output=True, text=True)
    return output, completed


def records_under(root: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in root.rglob("*.jsonl"):
        records.extend(read_jsonl(path))
    return records


class CodeEvidenceLayerTest(unittest.TestCase):
    def test_all_proven_mappings_experiments_and_typed_closure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packs: list[Path] = []
            all_records: list[dict[str, object]] = []
            for filename, file_order in MAPPED_FILES.items():
                pack, _ = run_indexer(
                    root,
                    filename,
                    file_order,
                    "pack-" + filename.removesuffix(".lyx"),
                )
                packs.append(pack)
                pack_records = records_under(pack)
                ids = {record["id"] for record in pack_records}
                self.assertEqual(len(ids), len(pack_records))
                for relation in (
                    record
                    for record in pack_records
                    if record["record_type"] == "relation"
                ):
                    self.assertIn(relation["from_id"], ids)
                    self.assertIn(relation["to_id"], ids)
                    for evidence_id in relation.get("evidence_segment_ids", []):
                        self.assertIn(evidence_id, ids)
                all_records.extend(pack_records)

            mapping_relations = [
                record
                for record in all_records
                if record.get("relation")
                in {
                    "normalized_equivalent_to",
                    "exact_excerpt_of",
                    "documented_revision_of",
                }
            ]
            self.assertEqual(
                Counter(record["relation"] for record in mapping_relations),
                Counter(
                    {
                        "normalized_equivalent_to": 5,
                        "exact_excerpt_of": 1,
                        "documented_revision_of": 5,
                    }
                ),
            )
            excerpt = next(
                record
                for record in mapping_relations
                if record["relation"] == "exact_excerpt_of"
            )
            self.assertEqual(excerpt["asset_line_range"], [1, 12])
            documented = [
                record
                for record in mapping_relations
                if record["relation"] == "documented_revision_of"
            ]
            self.assertEqual(
                Counter(record["declared_function"] for record in documented),
                Counter(
                    {
                        "bisection": 1,
                        "bisectionWhile": 2,
                        "bracketedNewton": 1,
                        "falsePosition": 1,
                    }
                ),
            )

            assets = {
                record["id"]: record
                for record in all_records
                if record["record_type"] == "asset"
            }
            versions = {
                record["id"]: record
                for record in all_records
                if record["record_type"] == "asset_version"
            }
            self.assertEqual(len(assets), 10)
            self.assertEqual(len(versions), 10)
            self.assertNotIn("rootFindingChallenge.m", "\n".join(
                str(item["logical_path"]) for item in assets.values()
            ))
            self.assertNotIn("deflate.m", "\n".join(
                str(item["logical_path"]) for item in assets.values()
            ))

            experiments = {
                record["experiment_key"]: record
                for record in all_records
                if record["record_type"] == "experiment"
            }
            self.assertEqual(set(experiments), {
                "preliminaries-taylor/experiment1-script-run",
                "interpolation-challenge/find-six-roots",
            })
            experiment1 = experiments["preliminaries-taylor/experiment1-script-run"]
            self.assertEqual(experiment1["invocation"], "experiment1")
            self.assertEqual(
                experiment1["expected_output_segment_ids"],
                ["urn:uuid:6d50df59-fc0a-5e2e-bc24-e9635f8c92c1"],
            )
            challenge = experiments["interpolation-challenge/find-six-roots"]
            self.assertEqual(challenge["result_mode"], "open_ended")
            self.assertNotIn("invocation", challenge)
            self.assertNotIn("expected_output_segment_ids", challenge)

            combined = root / "combined"
            command = [sys.executable, "-B", str(MERGER)]
            for pack in packs:
                command.extend(["--pack", str(pack)])
            command.extend(["--out", str(combined)])
            subprocess.run(command, check=True, capture_output=True, text=True)
            manifest = json.loads(
                (combined / "manifests" / "lane_manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(manifest["generator"], "ttna-pack-merger-0.3.0")
            self.assertEqual(manifest["record_counts"]["asset"], 10)
            self.assertEqual(manifest["record_counts"]["asset_version"], 10)
            self.assertEqual(manifest["record_counts"]["experiment"], 2)
            self.assertTrue(manifest["all_relation_endpoints_resolve"])

    def test_deterministic_pack_and_cross_pack_asset_version_dedup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first, _ = run_indexer(
                root,
                "preliminaries-recursion.lyx",
                MAPPED_FILES["preliminaries-recursion.lyx"],
                "first",
            )
            second, _ = run_indexer(
                root,
                "preliminaries-recursion.lyx",
                MAPPED_FILES["preliminaries-recursion.lyx"],
                "second",
            )
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

            combined = root / "combined"
            subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(MERGER),
                    "--pack",
                    str(first),
                    "--pack",
                    str(second),
                    "--out",
                    str(combined),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            manifest = json.loads(
                (combined / "manifests" / "lane_manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(manifest["record_counts"]["asset"], 2)
            self.assertEqual(manifest["record_counts"]["asset_version"], 2)

    def test_one_byte_asset_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = json.loads(CONFIG.read_text(encoding="utf-8"))
            config_path = root / "backend" / "config" / "code_evidence.v1.json"
            config_path.parent.mkdir(parents=True)
            config_path.write_text(
                json.dumps(config, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            relative = Path(
                "source/lqbrin-tea-time-numerical-1868821/octave/fractalInterpolator.m"
            )
            asset = root / relative
            asset.parent.mkdir(parents=True)
            original = LANE / relative
            shutil.copyfile(original, asset)
            raw = asset.read_bytes()
            asset.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))

            _, completed = run_indexer(
                root,
                "interpolation-challenge.lyx",
                MAPPED_FILES["interpolation-challenge.lyx"],
                "drift-output",
                config=config_path,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("asset_raw_sha256 drift", completed.stderr)


if __name__ == "__main__":
    unittest.main()
