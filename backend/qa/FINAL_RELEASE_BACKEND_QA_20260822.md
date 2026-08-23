# R015 final Indonesian release backend — QA receipt

Date: 2026-08-23  
Result: **PASS**

## Synchronized release inputs

- Final target corpus: 30 LyX files, path/hash-set SHA-256 `8ef8425373bd8162db1919b6cba7e0d1100966ac803b17223ca8cb85f3cc13dc`.
- Locale preamble: 7,901 bytes, SHA-256 `6f7940443f59d93a4beb37b20dc2c5c9e7de62ba1dff3f2f9a2b8f0e8d76863b`.
- Terminology: 593 unique records.
- Final adverse ledger: 325 rows, 152,062 bytes, SHA-256 `668843fef72f9899302cf17c5800634efd3f73b63164b58cbc15b606ab5b0ee0`.
- Final PDF: `output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf`, 8,202,487 bytes, 387 pages, SHA-256 `d573b7233d0baa07381e2052a749757885db3a31fbfe695c5a4851ea42d91b6d`.
- Final build manifest: 52,937 bytes, SHA-256 `dbef9a5bb9680f6c072e1f26fe3f5ae8ba7e1ca955d9c3dd47f402d1bb9174ea`.
- Whole-corpus release QA: `qa/WHOLE_CORPUS_RELEASE_QA_20260822.md`, SHA-256 `e23bd3638148bd004f3fbe0938ee82fd65f298b1c4cf0a4b6b213f347687fd43`.

All 31 translation/build-file packs were regenerated from these exact inputs. Each now carries the same 593-record terminology layer. The Heun and `cprotect` authority packs retain their separately pinned rights and provenance.

## Final artifact binding

`backend/tools/index_interop_v0.py bind-artifact` derived the artifact facts from the final PDF and build manifest, verified their internal agreement, refreshed the final ledger pin, and emitted:

- release configuration: `backend/config/interoperability_v0.release.json`, 3,115 bytes, SHA-256 `4aafff99f18acd992041774e5c07cc6c1289fed2c2b8526b89f3f1d911b190d2`;
- artifact ID: `urn:uuid:0c82fceb-d875-53e8-94c9-a20dae5547cb`;
- artifact role: `id-ID-release-pdf`;
- locale/status: `id-ID` / `release_final`;
- exact PDF and build-manifest identities listed above.

The English reproducible baseline remains a second artifact with status `baseline_nonfinal`; it was not mislabeled or replaced.

The final independently mergeable interoperability pack contains 1,295 records. Its manifest is 6,528 bytes, SHA-256 `0fc900555159797b9fda4cf78b2fa7d63b12d685cdf1100c3fb6abae1eadda86`.

## Final combined view

The deterministic merge of 34 explicit packs contains 28,172 unique records and 17,614 typed relations. Every relation endpoint and typed foreign key resolves.

Record counts:

- artifact 2; asset 15; asset_version 15; build_recipe 1;
- concept 12; correction 325; course 1; edition 1; experiment 2;
- localization 4,621; program 1; qa_event 31; relation 17,614;
- resource 1; rights 4; segment 4,621; source_file 31; term 593; unit 281.

Combined manifest: `backend/manifests/lane_manifest.json`, 14,060 bytes, SHA-256 `9a6ccf6ebf1e579216d7a5d7dee70b0da6acd7e5ea6237325b45cada5318a9e0`.

## Open exports and closed selection

- JSONL: 28,172 records, 22,101,516 bytes, SHA-256 `0b4227c5fde67ba15388384c79d980ec361b65f7375b4d47928aad1be09edafe`.
- Lossless CSV: 28,172 records, 25,706,115 bytes, SHA-256 `383c21ed77a500faa72f0687d66f0a6c6abce2eb255dd675036df7de8384fa81`.
- Export manifest: 1,828 bytes, SHA-256 `efe11b75bf8ca805aa2f6d8db945310d294cc72039a69d5b2a46b2a6d3c7e2bd`.
- JSONL/CSV semantic round trip: pass; UTF-8, LF, BOM-free; proprietary services required: false.
- `preface.layout.15` dependency-closed selection: 51 records, 28,962 bytes, SHA-256 `5807d72c4857a679ef2f9beaa2e1bcbc5f3b1d3e869fe3242737fba25c70ef82`.
- Selection manifest: 2,549 bytes, SHA-256 `a9640d4824b5fa06399cdaecdd0ec8672430e3e64e44ecfb60440dd345144cef`; dangling relations/foreign keys: 0.

## Validation and replay

After making public export locators repository-relative, the complete backend unittest suite passed 20/20 in 169.114 seconds. It covers deterministic generators, typed standalone and combined merges, rights partitioning, exact code evidence, one-byte drift rejection for source/assets/archive/style, open-export round trip, and dependency closure. The final export and selection contain zero machine-local absolute path hits.

A second complete in-place regeneration from the same pinned final inputs was compared against the first before the cursor advanced:

- 34-pack inventory: 463 files, aggregate SHA-256 `e5b607e748cca264b0cf1a803733d1777334301e7afd56c5bbfe34ef4ea20377`, equal before/after;
- combined output: 20 files, aggregate SHA-256 `90d6328bacddd08dbf1b9c334ca3022ba3189cd70928a1b0e7bd80f3ab022e1e`, equal before/after;
- open export plus checked selection before the repository-relative locator improvement: 5 files, aggregate SHA-256 `b631c91c9dc5b6c3945fccb9fc2e608a85b4d448c493abf35680cfa4740dc09e`, equal before/after;
- final repository-relative open export plus checked selection: 5 files, aggregate SHA-256 `5930df559f0a6bd1b4814eef3a5d74c5c573a64ebdb595eadc3d31543a922cc2`; record payload hashes remain unchanged.

The backend therefore passes the final release synchronization, deterministic replay, round-trip, typed-closure, rights-boundary, and final-artifact gates.
