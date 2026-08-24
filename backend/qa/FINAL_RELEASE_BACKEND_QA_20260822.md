# R015 final Indonesian release backend — QA receipt

Date: 2026-08-23
Current-byte integrity refresh: 2026-08-24
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

- release configuration: `backend/config/interoperability_v0.release.json`, 3,115 bytes, SHA-256 `9c66a55082b2b272b5ccda9e0f3c53924c8adb75af02286a604912bf1d220121`;
- artifact ID: `urn:uuid:0c82fceb-d875-53e8-94c9-a20dae5547cb`;
- artifact role: `id-ID-release-pdf`;
- locale/status: `id-ID` / `release_final`;
- exact PDF and build-manifest identities listed above.

The English reproducible baseline remains a second artifact with status `baseline_nonfinal`; it was not mislabeled or replaced.

The final independently mergeable interoperability pack contains 1,295 records. Its manifest is 6,528 bytes, SHA-256 `3bb6f0cb65f3c14da49b30c6922efb0985ed300791509b474087a47581c71403`.

## Final combined view

The deterministic merge of 34 explicit packs contains 28,172 unique records and 17,614 typed relations. Every relation endpoint and typed foreign key resolves.

Record counts:

- artifact 2; asset 15; asset_version 15; build_recipe 1;
- concept 12; correction 325; course 1; edition 1; experiment 2;
- localization 4,621; program 1; qa_event 31; relation 17,614;
- resource 1; rights 4; segment 4,621; source_file 31; term 593; unit 281.

Combined manifest: `backend/manifests/lane_manifest.json`, 14,060 bytes, SHA-256 `e11119d2e7ab1118ab75ea986c05d441cc22391d4ce44e6fce7bcf0b3c357301`.

## Open exports and closed selection

- JSONL: 28,172 records, 22,101,516 bytes, SHA-256 `2e02218c5b47d730ed510be1fa910ae826592d850a2db244aacc8e618e0a9d32`.
- Lossless CSV: 28,172 records, 25,706,115 bytes, SHA-256 `7e490edae2e6246363339116a0290e374eef6ab6bb01132f16a2f6cf4e5da42d`.
- Export manifest: 1,828 bytes, SHA-256 `6517e18a26e87293a1961862a837439d937a6ecd4f0bab9082ab5a4a8d4677ef`.
- JSONL/CSV semantic round trip: pass; UTF-8, LF, BOM-free; proprietary services required: false.
- `preface.layout.15` dependency-closed selection: 51 records, 28,962 bytes, SHA-256 `5807d72c4857a679ef2f9beaa2e1bcbc5f3b1d3e869fe3242737fba25c70ef82`.
- Selection manifest: 2,549 bytes, SHA-256 `2319878a544183fe8c5ab2d783d87bcd5c62c1d23884c02cc3ea33b0ac0c4c84`; dangling relations/foreign keys: 0.

## Validation and replay

For the `3.0-id.2-r1` integrity replay on 2026-08-24, the complete backend unittest suite passed 20/20 in 23.231 seconds. It covers deterministic generators, typed standalone and combined merges, rights partitioning, exact code evidence, one-byte drift rejection for source/assets/archive/style, open-export round trip, and dependency closure. The final export and selection contain zero machine-local absolute path hits.

A second complete in-place regeneration from the same pinned final inputs was compared against the first before the cursor advanced:

- interoperability pack: 14 files / 1,435,117 bytes, aggregate SHA-256 `e9bf9bf936f29e686c23e0eaaf6287cf3ed565113a3d66f56a4c81e82a6a5412`, equal before/after;
- combined output: 20 files / 22,115,576 bytes, aggregate SHA-256 `347a5f566bedc7216febe35acb6321575388b9cf0dd622e4d2ad0fdb0c41f12e`, equal before/after;
- open export plus checked selection: 5 files / 47,840,970 bytes, aggregate SHA-256 `7c3315870a4a54d87f204b75e8f494f7865acd470cf68add6dbdfd823b305a12`, equal before/after.

The backend therefore passes the final release synchronization, deterministic replay, round-trip, typed-closure, rights-boundary, and final-artifact gates.
