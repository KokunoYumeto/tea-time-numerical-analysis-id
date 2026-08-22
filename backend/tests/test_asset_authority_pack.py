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
INDEXER = BACKEND / "tools" / "index_asset_authority.py"
MERGER = BACKEND / "tools" / "merge_packs.py"
CONFIG = BACKEND / "config" / "heun1900_asset_authority.v1.json"
CHECKED_PACK = BACKEND / "packs" / "heun1900-page30"

EXPECTED_IDS = {
    "rights": "urn:uuid:5602adce-6069-5b8f-b5b8-c8a3fe5762f4",
    "asset": "urn:uuid:c34746a0-acc2-55d9-a22d-70c557bc544f",
    "asset_version": "urn:uuid:60ad7244-854b-55ab-8aa7-2c2addb0fe40",
    "relation": "urn:uuid:3b90425a-f4ea-5094-a1de-92558f30191c",
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
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]


class AssetAuthorityPackTest(unittest.TestCase):
    def test_checked_pack_replays_byte_exactly_twice(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "first"
            second = root / "second"
            run_indexer(LANE, CONFIG, first)
            run_indexer(LANE, CONFIG, second)
            self.assertEqual(file_bytes(first), file_bytes(second))
            self.assertEqual(file_bytes(first), file_bytes(CHECKED_PACK))

    def test_exact_records_and_standalone_typed_merge(self) -> None:
        rights = read_jsonl(CHECKED_PACK / "rights" / "components.jsonl")
        assets = read_jsonl(CHECKED_PACK / "assets" / "assets.jsonl")
        versions = read_jsonl(CHECKED_PACK / "assets" / "versions.jsonl")
        relations = read_jsonl(CHECKED_PACK / "topology" / "relations.jsonl")
        self.assertEqual([record["id"] for record in rights], [EXPECTED_IDS["rights"]])
        self.assertEqual([record["id"] for record in assets], [EXPECTED_IDS["asset"]])
        self.assertEqual(
            [record["id"] for record in versions], [EXPECTED_IDS["asset_version"]]
        )
        self.assertEqual(
            [record["id"] for record in relations], [EXPECTED_IDS["relation"]]
        )
        self.assertEqual(rights[0]["spdx_expression"], "CC-PDM-1.0")
        self.assertEqual(
            versions[0]["source_sha256"],
            "d34c3f99ae1740e9ac7f97bec473b44a3d28353ae503bda1c2bf55e4ee8999d7",
        )
        self.assertEqual(relations[0]["relation"], "version_of")
        self.assertEqual(relations[0]["from_id"], versions[0]["id"])
        self.assertEqual(relations[0]["to_id"], assets[0]["id"])

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
                (combined / "manifests" / "lane_manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(manifest["record_counts"]["asset"], 1)
            self.assertEqual(manifest["record_counts"]["asset_version"], 1)
            self.assertEqual(manifest["record_counts"]["rights"], 1)
            self.assertEqual(manifest["record_counts"]["relation"], 1)
            self.assertEqual(manifest["total_unique_records"], 6)
            self.assertTrue(manifest["all_relation_endpoints_resolve"])

    def test_one_byte_release_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            lane = Path(temporary) / "lane"
            config_target = lane / CONFIG.relative_to(LANE)
            config_target.parent.mkdir(parents=True)
            shutil.copyfile(CONFIG, config_target)
            config = json.loads(CONFIG.read_text(encoding="utf-8"))
            authority_relative = Path(config["authority"]["path"])
            authority_target = lane / authority_relative
            authority_target.parent.mkdir(parents=True)
            shutil.copyfile(LANE / authority_relative, authority_target)
            receipt = json.loads(authority_target.read_text(encoding="utf-8"))
            for key in ("provenance_master", "release_derivative"):
                relative = Path(receipt[key]["path"])
                target = lane / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(LANE / relative, target)
            release = lane / receipt["release_derivative"]["path"]
            payload = release.read_bytes()
            release.write_bytes(payload[:-1] + bytes([payload[-1] ^ 1]))

            completed = run_indexer(
                lane,
                config_target,
                lane / "backend" / "packs" / "drift",
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("release asset sha256 drift", completed.stderr)


if __name__ == "__main__":
    unittest.main()
