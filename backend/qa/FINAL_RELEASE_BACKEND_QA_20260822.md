# R015 final Indonesian release backend — QA receipt

Date: 2026-08-22  
Result: **PASS**

## Synchronized release inputs

- Final target corpus: 30 LyX files, path/hash-set SHA-256 `3aadfb2ba675a07f83df49dfdf1389a4da9278362c7a265ec08bcf9e45a3a469`.
- Locale preamble: 7,901 bytes, SHA-256 `6f7940443f59d93a4beb37b20dc2c5c9e7de62ba1dff3f2f9a2b8f0e8d76863b`.
- Terminology: 593 unique records.
- Final adverse ledger: 325 rows, 152,062 bytes, SHA-256 `668843fef72f9899302cf17c5800634efd3f73b63164b58cbc15b606ab5b0ee0`.
- Final PDF: `output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf`, 8,202,476 bytes, 387 pages, SHA-256 `cbc31e9e27fdee96845d78fa6a625bf956196001b7941ddf0f1232f5def46b45`.
- Final build manifest: 53,012 bytes, SHA-256 `9437f143c777ca447c5b199f0ea2a7df1e70b2afd7731839c43041ca018fd988`.
- Whole-corpus release QA: `qa/WHOLE_CORPUS_RELEASE_QA_20260822.md`, SHA-256 `d1b1da7eea68de58154903dde3c53a9e992dfd7eff1c779feefb75927d774665`.

All 31 translation/build-file packs were regenerated from these exact inputs. Each now carries the same 593-record terminology layer. The Heun and `cprotect` authority packs retain their separately pinned rights and provenance.

## Final artifact binding

`backend/tools/index_interop_v0.py bind-artifact` derived the artifact facts from the final PDF and build manifest, verified their internal agreement, refreshed the final ledger pin, and emitted:

- release configuration: `backend/config/interoperability_v0.release.json`, 3,115 bytes, SHA-256 `a1a70f0ddda50cd365e2a92f1363d9dca07e06d1a3b6234364cb871e330112cc`;
- artifact ID: `urn:uuid:0c82fceb-d875-53e8-94c9-a20dae5547cb`;
- artifact role: `id-ID-release-pdf`;
- locale/status: `id-ID` / `release_final`;
- exact PDF and build-manifest identities listed above.

The English reproducible baseline remains a second artifact with status `baseline_nonfinal`; it was not mislabeled or replaced.

The final independently mergeable interoperability pack contains 1,295 records. Its manifest is 6,528 bytes, SHA-256 `4286e17522baafe1e1b7299ff9f4573b0ad38abf4300dab9d4153e3efd57d8ce`.

## Final combined view

The deterministic merge of 34 explicit packs contains 28,172 unique records and 17,614 typed relations. Every relation endpoint and typed foreign key resolves.

Record counts:

- artifact 2; asset 15; asset_version 15; build_recipe 1;
- concept 12; correction 325; course 1; edition 1; experiment 2;
- localization 4,621; program 1; qa_event 31; relation 17,614;
- resource 1; rights 4; segment 4,621; source_file 31; term 593; unit 281.

Combined manifest: `backend/manifests/lane_manifest.json`, 14,060 bytes, SHA-256 `17ef5072077b5b438a883b6bd751ea31b2ec5651567db5d100dba39bf9497cb3`.

## Open exports and closed selection

- JSONL: 28,172 records, 22,050,690 bytes, SHA-256 `203ec965823817e79939f894f871ed6c0445534fbf3a6d06d1e0fa3566e16c79`.
- Lossless CSV: 28,172 records, 25,655,273 bytes, SHA-256 `a178ec16910340d8482034cd088e81c86805c1bc118f01c0162a934a498845c7`.
- Export manifest: 1,828 bytes, SHA-256 `81371e4279186bf61ee829b827cd17fad7e1de6d8f79c411d671d7b7629acd53`.
- JSONL/CSV semantic round trip: pass; UTF-8, LF, BOM-free; proprietary services required: false.
- `preface.layout.15` dependency-closed selection: 51 records, 28,896 bytes, SHA-256 `e06757514aaaa53960b7992381224dc2e7bf2a1e9f6923479d35177062a5666d`.
- Selection manifest: 2,549 bytes, SHA-256 `019b8b340e17eb96a55f4cd65d9c41acdd77bbd1c3171a1e5935ab4f732eb90e`; dangling relations/foreign keys: 0.

## Validation and replay

After making public export locators repository-relative, the complete backend unittest suite passed 20/20 in 48.706 seconds. It covers deterministic generators, typed standalone and combined merges, rights partitioning, exact code evidence, one-byte drift rejection for source/assets/archive/style, open-export round trip, and dependency closure. The final export and selection contain zero machine-local absolute path hits.

A second complete in-place regeneration from the same pinned final inputs was compared against the first before the cursor advanced:

- 34-pack inventory: 463 files, aggregate SHA-256 `e5b607e748cca264b0cf1a803733d1777334301e7afd56c5bbfe34ef4ea20377`, equal before/after;
- combined output: 20 files, aggregate SHA-256 `90d6328bacddd08dbf1b9c334ca3022ba3189cd70928a1b0e7bd80f3ab022e1e`, equal before/after;
- open export plus checked selection before the repository-relative locator improvement: 5 files, aggregate SHA-256 `b631c91c9dc5b6c3945fccb9fc2e608a85b4d448c493abf35680cfa4740dc09e`, equal before/after;
- final repository-relative open export plus checked selection: 5 files, aggregate SHA-256 `5930df559f0a6bd1b4814eef3a5d74c5c573a64ebdb595eadc3d31543a922cc2`; record payload hashes remain unchanged.

The backend therefore passes the final release synchronization, deterministic replay, round-trip, typed-closure, rights-boundary, and final-artifact gates.
