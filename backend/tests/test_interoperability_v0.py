from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import export_interop_v0 as exporter  # noqa: E402
import index_interop_v0 as indexer  # noqa: E402


LANE_ROOT = Path(__file__).resolve().parents[2]
CONFIG = LANE_ROOT / "backend" / "config" / "interoperability_v0.v1.json"
COMBINED_MANIFEST = LANE_ROOT / "backend" / "manifests" / "lane_manifest.json"
SCHEMA = LANE_ROOT / "backend" / "schema" / "record.schema.json"


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class InteroperabilityV0Tests(unittest.TestCase):
    def test_stable_identities_are_exact(self) -> None:
        self.assertEqual(
            indexer.stable_id("program", "program/R015/id-ID/v3.0"),
            "urn:uuid:f2771510-259f-55cc-a524-79d48fce6dba",
        )
        self.assertEqual(
            indexer.stable_id("course", "course/C110"),
            "urn:uuid:a17f1fe0-73ca-5852-9ad3-d207c62467ea",
        )
        self.assertEqual(
            indexer.stable_id("artifact", "artifact/english-baseline-pdf"),
            "urn:uuid:fb181a76-6aca-5346-96f2-9bf0aa4c2f9e",
        )

    def test_pack_generation_is_deterministic_and_locally_closed(self) -> None:
        with tempfile.TemporaryDirectory() as first_tmp, tempfile.TemporaryDirectory() as second_tmp:
            first = Path(first_tmp) / "pack"
            second = Path(second_tmp) / "pack"
            first_manifest = indexer.build_pack(LANE_ROOT, CONFIG, first)
            second_manifest = indexer.build_pack(LANE_ROOT, CONFIG, second)
            self.assertEqual(tree_bytes(first), tree_bytes(second))
            self.assertEqual(first_manifest, second_manifest)
            self.assertEqual(first_manifest["admission"]["correction_rows_complete"], 325)
            self.assertEqual(first_manifest["admission"]["local_relation_closure"], "pass")

    def test_jsonl_csv_round_trip_and_export_determinism(self) -> None:
        with tempfile.TemporaryDirectory() as first_tmp, tempfile.TemporaryDirectory() as second_tmp:
            first = Path(first_tmp) / "export"
            second = Path(second_tmp) / "export"
            first_manifest = exporter.export_lane(COMBINED_MANIFEST, SCHEMA, first)
            second_manifest = exporter.export_lane(COMBINED_MANIFEST, SCHEMA, second)
            self.assertEqual(tree_bytes(first), tree_bytes(second))
            self.assertEqual(first_manifest, second_manifest)
            proof = exporter.verify_round_trip(first / "records.jsonl", first / "records.csv")
            self.assertTrue(proof["round_trip_equal"])
            self.assertTrue(proof["utf8_lf"])

    def test_one_byte_source_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "backend"
            data = root / "sample.jsonl"
            manifests = root / "manifests"
            manifests.mkdir(parents=True)
            payload = b'{"id":"urn:uuid:00000000-0000-0000-0000-000000000000","record_type":"unit"}\n'
            data.write_bytes(payload)
            manifest = {
                "files": [
                    {
                        "path": "sample.jsonl",
                        "records": 1,
                        "bytes": len(payload),
                        "sha256": hashlib.sha256(payload).hexdigest(),
                    }
                ],
                "total_unique_records": 1,
            }
            manifest_path = manifests / "lane_manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8", newline="\n")
            exporter.load_records_from_manifest(manifest_path)
            changed = bytearray(payload)
            changed[2] = ord("J")
            data.write_bytes(bytes(changed))
            with self.assertRaisesRegex(exporter.ExportError, "one-byte/source drift"):
                exporter.load_records_from_manifest(manifest_path)

    def test_dependency_closed_unit_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            export_dir = Path(temporary) / "export"
            selection_dir = Path(temporary) / "selection"
            full_manifest = exporter.export_lane(COMBINED_MANIFEST, SCHEMA, export_dir)
            selection = exporter.select_command(
                export_dir / "records.jsonl",
                export_dir / "manifest.json",
                [],
                ["preface.layout.15"],
                selection_dir,
            )
            proof = selection["selection"]
            self.assertTrue(proof["all_emitted_relation_endpoints_present"])
            self.assertTrue(proof["all_foreign_keys_resolve"])
            self.assertEqual(proof["unresolved_dependencies"], [])
            self.assertLess(selection["total_unique_records"], full_manifest["total_unique_records"])
            selected = exporter.parse_jsonl_bytes(
                (selection_dir / "records.jsonl").read_bytes(), "selection"
            )
            kinds = {record["record_type"] for record in selected}
            self.assertTrue({"program", "course", "resource", "edition", "unit", "segment"} <= kinds)


if __name__ == "__main__":
    unittest.main()
