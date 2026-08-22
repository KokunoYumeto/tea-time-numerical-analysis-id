# R015 Modular Backend Interoperability Envelope v0 — QA receipt

Date: 2026-08-22
Result: historical pre-release-envelope pass. The required final PDF binding was
subsequently completed and is recorded in
`backend/qa/FINAL_RELEASE_BACKEND_QA_20260822.md`.

## Exact input snapshot

- Resource: R015, `urn:uuid:8fbaf4c5-6316-5159-89b9-787aa115c0dc`.
- Edition: upstream v3.0 commit
  `186882108a6da95c8dca5b81ce000fc3f8f3ca21`, tree
  `1e50d3756b695176008c602f0ee89712f5f32d10`,
  `urn:uuid:35b4350d-7202-5d47-8b85-5262d7ca441c`.
- Task evidence: `00_control/TASK.md`, 5,647 bytes, SHA-256
  `b68c37076755bbdf816021ae3635c95ac39b5ff4fe6aaa432dfd37a72a81418a`.
- Correction evidence: `00_control/ADVERSE_LEDGER.csv`, 152,062 bytes,
  SHA-256
  `668843fef72f9899302cf17c5800634efd3f73b63164b58cbc15b606ab5b0ee0`.
- Exact config: `backend/config/interoperability_v0.v1.json`, 2,314 bytes,
  SHA-256
  `ed8092c72a7ea779ee8267dd708cfcec8df581ab8ecee61d90ecb66b39470f57`.
- Final Heun authority pin admitted concurrently: 3,695-byte authority receipt,
  SHA-256
  `39bbf79cebe96967dabde26b62faf51c55d6ed1b0376000b3b46bf615f79a2dd`;
  its regenerated pack manifest is 2,543 bytes, SHA-256
  `b0282bf89b63640c1b50e23a5d4de76fd0e9a3d8c6bcd175f0f091dd4b3d982e`.

## Stable identities and non-invention boundary

- Program: `urn:uuid:f2771510-259f-55cc-a524-79d48fce6dba`.
- Course C110: `urn:uuid:a17f1fe0-73ca-5852-9ad3-d207c62467ea`.
- English baseline artifact:
  `urn:uuid:fb181a76-6aca-5346-96f2-9bf0aa4c2f9e`.
- The unknown program local ID/title/version, course title/curriculum role, and
  prerequisites are preserved as `null` or an empty list with an explicit
  unknown state. No curriculum prerequisites were inferred.
- The twelve locale-neutral concepts and their accepted terminology evidence
  are:

  - `TTNA-CONCEPT-0001` — numerical analysis —
    `urn:uuid:9e10a282-68a7-54bb-b695-bb5782bce208`.
  - `TTNA-CONCEPT-0002` — root finding —
    `urn:uuid:1aae3a27-ef0c-535a-937a-a9be88f585a0`.
  - `TTNA-CONCEPT-0003` — interpolation —
    `urn:uuid:86d14eff-8ae3-5a06-91f8-de04d0a0c1cc`.
  - `TTNA-CONCEPT-0004` — numerical calculus —
    `urn:uuid:e258f762-daf6-54b5-a8eb-21389bc4e13e`.
  - `TTNA-CONCEPT-0005` — differential equation —
    `urn:uuid:e7401260-f87e-57be-bd95-d06402807f5a`.
  - `TTNA-CONCEPT-0017` — round-off error —
    `urn:uuid:a789e491-204d-50d5-ae8a-5317bd3009f0`.
  - `TTNA-CONCEPT-0027` — Taylor series —
    `urn:uuid:96034853-d2ec-5bb5-8cbc-6d52ac756d97`.
  - `TTNA-CONCEPT-0075` — bisection method —
    `urn:uuid:fd07065d-072d-569f-8092-6b6a307493aa`.
  - `TTNA-CONCEPT-0121` — Newton's method —
    `urn:uuid:1017adea-ada2-5dd6-b475-f3a94d8f3919`.
  - `TTNA-CONCEPT-0286` — numerical integration —
    `urn:uuid:e525a9a8-0252-57f7-9269-10c44d07f6ac`.
  - `TTNA-CONCEPT-0396` — cubic spline —
    `urn:uuid:b83611ab-c502-5566-898b-3b780c4e9ee8`.
  - `TTNA-CONCEPT-0426` — ordinary differential equation —
    `urn:uuid:c3101588-a888-5fc6-a035-0564f7410d60`.

Every concept is linked to its exact accepted term and to units only through
existing `uses_term` evidence segments. The pack has 146 `covers_concept` and
12 `denotes` relations.

All 325 adverse-ledger rows are represented without converting open status into
an applied-change claim. Correction IDs are UUIDv5 values of the stable event
IDs; the bounded range is `TTNA-ID-ADV-0002`
(`urn:uuid:71bc4fbe-6152-579f-a99e-5f2828b150d9`) through
`TTNA-ID-ADV-0326`
(`urn:uuid:939d2619-fe35-5a6c-86d1-967e8078e3eb`). There are 326 exact
`corrects` file relations because one ledger row names two source files. No
affected semantic unit was guessed from a free-form locator.

## Exact artifact

The admitted artifact is explicitly `baseline_nonfinal`:

- `tmp/pdfs/en-baseline/TeaTimeNumericalAnalysis-en-baseline.pdf`;
- 8,186,285 bytes;
- SHA-256
  `17cd4abc74cff4934cc78a2f42378489829207f534ad9a051c45ad67b2b18180`;
- 371 pages according to its exact build receipt;
- build receipt `build/manifests/en-baseline-build.json`, 53,055 bytes,
  SHA-256
  `241285cb4f76d560c67c49b905b4be401fecf4dc7d9b86cc8ffaf74335cdefd5`;
- LyX 2.4.4 executable SHA-256
  `aa359efbfc16c509a7a91d1c347a6bb702a8fa6b686c0bba8210d058f80c460e`;
- latexmk SHA-256
  `23816f82608189d5aed0bcb4746a8ebc9931c5ce359140a63b6f7e058c516112`;
- cprotect style SHA-256
  `eafa24d80cff3bb804ed46af5f045d41d596f23c6d23e9cb7b01c15aa4efaef2`;
- LyX export and latexmk exit codes: both zero.

The generator compares the artifact bytes to both the config and the build
manifest, then records the manifest/toolchain identity. A single-byte mismatch
fails closed.

## Pack and combined view

The independently mergeable interoperability pack contains 1,293 unique
records: one artifact, 12 concepts, 325 corrections, one course, one edition,
one program, 488 relations, one resource, three rights records, 314 exact
evidence segments, 31 source files, 12 terms, and 103 units. The 488 relations
are one `built_from`, two `contains`, 326 `corrects`, 146 `covers_concept`,
12 `denotes`, and one `uses_resource`.

- Pack manifest: 6,083 bytes, SHA-256
  `20b585415f0fba4f0d721606934f5ecd12e99d15425c297a36397c173d7fc778`.
- Combined manifest: 14,060 bytes, SHA-256
  `f1f380b900454b221df3bdac483b3caa3906377ab1e9ecacc3392ca81d8238fb`.
- Combined view: 27,961 unique records and 17,423 typed relations.
- Combined record counts: artifact 1; asset 15; asset_version 15;
  build_recipe 1; concept 12; correction 325; course 1; edition 1;
  experiment 2; localization 4,621; program 1; qa_event 31; relation
  17,423; resource 1; rights 4; segment 4,621; source_file 31; term 574;
  unit 281.
- Every relation endpoint resolves, and merger 0.3.0 validates all new typed
  program/course/concept/artifact/correction foreign keys.

The 416 pre-existing pack JSONL files remained byte-identical. Their
path/size/SHA inventory aggregate before and after this work is
`12319f34f1617a149d5ffebf43d78d77d965449a5d54beb53a4a0dfa2853e92a`.
Only the final Heun pack manifest changed to admit its updated external receipt;
its JSONL records did not change.

## Open export and dependency-closed selection

- `backend/exports/interoperability-v0/records.jsonl`: 27,961 records,
  21,989,582 bytes, SHA-256
  `1e759692b87a32aa0e945889243a84c15495e60dc16b76d8a0b1dc6e5b7d9001`.
- `backend/exports/interoperability-v0/records.csv`: 27,961 records,
  25,575,690 bytes, SHA-256
  `b291dc98f7b4e4bb24941a2a3aaa11680d221b07ad4c920fa16a80383e4a4c5e`.
- Export manifest: 1,998 bytes, SHA-256
  `ee1f219f612c2a692db4a41b589f057ede359e143eee97dccdb6698a73c7ed71`.
- JSONL/CSV semantic round trip: pass; canonical semantic SHA-256 equals the
  JSONL SHA-256; UTF-8/LF/BOM-free checks pass.
- Proprietary services required: false.

The checked `preface.layout.15` selection starts with six reader segments and
closes through topology, translation, terminology, rights, QA, source-file,
edition, resource, course, and program dependencies to 51 records. Its JSONL is
28,896 bytes, SHA-256
`c9cc822342a265c06359548769919bd61ae63627205b31ed2a8bd495f09f77d2`.
The selection manifest is 2,634 bytes, SHA-256
`d03b51c59c76f2f6710f88fcbaed9c5b6c42799a178faeacb6b5ce85e4717fb0`.
All emitted relation endpoints and all emitted UUID foreign keys resolve;
unresolved dependency count is zero.

## Commands and test evidence

Primary commands:

```text
python -B backend/tools/index_interop_v0.py generate --lane-root . --config backend/config/interoperability_v0.v1.json --out backend/packs/interoperability-v0
python -B backend/tools/merge_packs.py [the 34 explicit --pack arguments recorded in backend/README.md] --out backend
python -B backend/tools/export_interop_v0.py export --manifest backend/manifests/lane_manifest.json --schema backend/schema/record.schema.json --out backend/exports/interoperability-v0
python -B backend/tools/export_interop_v0.py verify-round-trip --jsonl backend/exports/interoperability-v0/records.jsonl --csv backend/exports/interoperability-v0/records.csv
python -B backend/tools/export_interop_v0.py select --records backend/exports/interoperability-v0/records.jsonl --export-manifest backend/exports/interoperability-v0/manifest.json --unit-source-local-id preface.layout.15 --out backend/exports/interoperability-v0/selections/preface-online
python -B -m unittest discover -s backend/tests -p "test_*.py" -v
```

Full backend suite: 20/20 pass in 25.924 seconds. This includes deterministic
pack/export replay, standalone typed merges, JSONL/CSV round trip, one-byte
source/asset/archive/style drift rejection, and dependency-closure proof.

Independent two-directory replay results:

- interoperability pack: 14 files in each replay, aggregate SHA-256
  `9426d303b86930f46f6db6aa105ee8e08624031c42cc733f1e5f2c6ea916d6cb`
  in both;
- combined backend: 20 files in each replay, aggregate SHA-256
  `f5ea5f352a71f286969a2cb1ab1e8c2a77237ba5410c261df9d24aedd66ea231`
  in both;
- open export: three files in each replay, aggregate SHA-256
  `d774cffb1d39eb0387104ade0cf79d553ff3d6977bec4c1772c803b67224922a`
  in both.

## Required final-PDF artifact update

After the final id-ID release PDF and its exact build manifest are the chosen
release bytes, run the documented `bind-artifact` command in
`backend/README.md`. It hashes the two files, verifies the build manifest's PDF
entry, adds or replaces the stable `id-ID-release-pdf` role, and can refresh the
bounded ledger pin. Then regenerate the interoperability pack, rerun the
34-pack merge, regenerate/verify exports, and rerun the backend suite. This is
the only remaining artifact-layer update; the current baseline artifact is
intentionally not mislabeled as the Indonesian release.
