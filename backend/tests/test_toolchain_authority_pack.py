from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


BACKEND = Path(__file__).resolve().parents[1]
LANE = BACKEND.parent
INDEXER = BACKEND / "tools" / "index_toolchain_authority.py"
MERGER = BACKEND / "tools" / "merge_packs.py"
CONFIG = BACKEND / "config" / "cprotect_toolchain_authority.v1.json"
CHECKED_PACK = BACKEND / "packs" / "cprotect-1.0f"

EXPECTED_IDS = {
    "rights": "urn:uuid:74d169c6-4423-5211-bff7-f7f5e2243ec9",
    "archive_asset": "urn:uuid:386006c1-ae53-5cfe-9691-16ed08dd88f9",
    "source_asset": "urn:uuid:646b7b5c-d967-5e87-8a7a-9d157ba1c109",
    "installer_asset": "urn:uuid:8f2a3b75-57e6-531e-941d-9e21154e0e19",
    "style_asset": "urn:uuid:fb8841b6-c14b-5cc4-b7fe-aa045cc7b85c",
    "archive_version": "urn:uuid:9ed3ef95-a1c8-50e0-ae59-b4d83e7916cc",
    "source_version": "urn:uuid:6177e682-41bd-5313-8252-a7fa4a9bf544",
    "installer_version": "urn:uuid:814c2fdf-940e-5aae-869d-608ea7bcf2be",
    "style_version": "urn:uuid:2da33f4c-89e2-59f3-a8f4-3078a28528d7",
    "build_recipe": "urn:uuid:5d5f2455-0375-5469-9b95-21614f56d447",
}


def run_indexer(
    lane_root: Path,
    config: Path,
    output: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-B",
            str(INDEXER),
            "--lane-root",
            str(lane_root),
            "--config",
            str(config),
            "--out",
            str(output),
        ],
        check=check,
        capture_output=True,
        text=True,
    )


def file_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def copy_authority_closure(lane: Path) -> Path:
    config_target = lane / CONFIG.relative_to(LANE)
    config_target.parent.mkdir(parents=True)
    shutil.copyfile(CONFIG, config_target)
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    authority_relative = Path(config["authority"]["path"])
    authority_target = lane / authority_relative
    authority_target.parent.mkdir(parents=True)
    shutil.copyfile(LANE / authority_relative, authority_target)
    receipt = json.loads(authority_target.read_text(encoding="utf-8"))
    paths = {receipt["archive"]["path"]}
    paths.update(item["local_path"] for item in receipt["archive"]["members"])
    paths.update(item["path"] for item in receipt["work_files"])
    for value in sorted(paths):
        relative = Path(value)
        target = lane / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(LANE / relative, target)
    return config_target


class ToolchainAuthorityPackTest(unittest.TestCase):
    def test_checked_pack_replays_byte_exactly_twice(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "first"
            second = root / "second"
            run_indexer(LANE, CONFIG, first)
            run_indexer(LANE, CONFIG, second)
            self.assertEqual(file_bytes(first), file_bytes(second))
            self.assertEqual(file_bytes(first), file_bytes(CHECKED_PACK))

    def test_exact_records_and_typed_standalone_merge(self) -> None:
        rights = read_jsonl(CHECKED_PACK / "rights" / "components.jsonl")
        assets = read_jsonl(CHECKED_PACK / "assets" / "assets.jsonl")
        versions = read_jsonl(CHECKED_PACK / "assets" / "versions.jsonl")
        recipes = read_jsonl(CHECKED_PACK / "build" / "recipes.jsonl")
        relations = read_jsonl(CHECKED_PACK / "topology" / "relations.jsonl")
        self.assertEqual([item["id"] for item in rights], [EXPECTED_IDS["rights"]])
        self.assertEqual({item["id"] for item in assets}, {
            EXPECTED_IDS["archive_asset"],
            EXPECTED_IDS["source_asset"],
            EXPECTED_IDS["installer_asset"],
            EXPECTED_IDS["style_asset"],
        })
        self.assertEqual({item["id"] for item in versions}, {
            EXPECTED_IDS["archive_version"],
            EXPECTED_IDS["source_version"],
            EXPECTED_IDS["installer_version"],
            EXPECTED_IDS["style_version"],
        })
        self.assertEqual([item["id"] for item in recipes], [EXPECTED_IDS["build_recipe"]])
        self.assertEqual(rights[0]["spdx_expression"], "LPPL-1.3c+")
        self.assertTrue(rights[0]["redistribution_permitted"])
        self.assertTrue(rights[0]["preserve_complete_work_required"])
        self.assertEqual(len(relations), 9)
        self.assertEqual(
            {(item["relation"], item["from_id"], item["to_id"]) for item in relations if item["relation"] == "generated_by"},
            {("generated_by", EXPECTED_IDS["style_version"], EXPECTED_IDS["build_recipe"])},
        )

        with tempfile.TemporaryDirectory() as temporary:
            combined = Path(temporary) / "combined"
            subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(MERGER),
                    "--pack",
                    str(CHECKED_PACK),
                    "--out",
                    str(combined),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            manifest = json.loads(
                (combined / "manifests" / "lane_manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["record_counts"]["asset"], 4)
            self.assertEqual(manifest["record_counts"]["asset_version"], 4)
            self.assertEqual(manifest["record_counts"]["build_recipe"], 1)
            self.assertEqual(manifest["record_counts"]["rights"], 1)
            self.assertEqual(manifest["record_counts"]["relation"], 9)
            self.assertEqual(manifest["total_unique_records"], 21)
            self.assertTrue(manifest["all_relation_endpoints_resolve"])

    def test_one_byte_archive_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            lane = Path(temporary) / "lane"
            config_target = copy_authority_closure(lane)
            config = json.loads(config_target.read_text(encoding="utf-8"))
            receipt = json.loads((lane / config["authority"]["path"]).read_text(encoding="utf-8"))
            archive = lane / receipt["archive"]["path"]
            payload = archive.read_bytes()
            archive.write_bytes(payload[:-1] + bytes([payload[-1] ^ 1]))
            completed = run_indexer(
                lane, config_target, lane / "backend" / "packs" / "drift", check=False
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("toolchain archive sha256 drift", completed.stderr)

    def test_one_byte_generated_style_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            lane = Path(temporary) / "lane"
            config_target = copy_authority_closure(lane)
            config = json.loads(config_target.read_text(encoding="utf-8"))
            receipt = json.loads((lane / config["authority"]["path"]).read_text(encoding="utf-8"))
            style_row = next(
                item for item in receipt["work_files"] if item["role"] == "generated_installable_style"
            )
            style = lane / style_row["path"]
            payload = style.read_bytes()
            style.write_bytes(bytes([payload[0] ^ 1]) + payload[1:])
            completed = run_indexer(
                lane, config_target, lane / "backend" / "packs" / "drift", check=False
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("generated_installable_style sha256 drift", completed.stderr)

    def test_declared_tex_recipe_reproduces_checked_style(self) -> None:
        tex = shutil.which("tex")
        if tex is None:
            self.skipTest("TeX is not installed")
        source_root = LANE / "authority" / "toolchain" / "cprotect-1.0f" / "package" / "cprotect"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copyfile(source_root / "cprotect.dtx", root / "cprotect.dtx")
            shutil.copyfile(source_root / "cprotect.ins", root / "cprotect.ins")
            completed = subprocess.run(
                [tex, "-interaction=nonstopmode", "-halt-on-error", "cprotect.ins"],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertEqual(
                (root / "cprotect.sty").read_bytes(),
                (source_root / "cprotect.sty").read_bytes(),
            )


if __name__ == "__main__":
    unittest.main()
