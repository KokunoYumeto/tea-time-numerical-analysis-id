# R015 modular translation backend

This backend is additive to the frozen LyX source. Canonical semantic records
are deterministic UTF-8/LF JSON or JSONL. CSV and SQLite are derived exchange
views and will be generated only after their logical round trips are covered.

Stable identities use UUIDv5 under a fixed namespace derived from the official
resource URL. Identity is distinct from mutable wording, page numbers, and
content hashes. Source hashes identify exact versions; localized expressions
attach to persistent locale-neutral units and segments.

The per-file packs cover the TeX build preamble, the LyX master, and all 29
included LyX children. The established child command remains:

```text
python backend/tools/index_lyx_pair.py --source source/lqbrin-tea-time-numerical-1868821/preface.lyx --target translation/lyx-id/preface.lyx --source-rel source/lqbrin-tea-time-numerical-1868821/preface.lyx --target-rel translation/lyx-id/preface.lyx --terms-csv 00_control/TERMINOLOGY.csv --code-evidence backend/config/code_evidence.v1.json --file-order 1 --file-kind included_file --out backend/packs/preface
```

The non-child build inputs use explicit roles rather than being mislabeled as
included children:

```text
python -B backend/tools/index_tex_pair.py --source source/lqbrin-tea-time-numerical-1868821/preamble.tex --target translation/lyx-id/preamble.tex --source-rel source/lqbrin-tea-time-numerical-1868821/preamble.tex --target-rel translation/lyx-id/preamble.tex --terms-csv 00_control/TERMINOLOGY.csv --reader-map backend/config/preamble_reader_map.v1.json --file-order -1 --file-kind build_preamble --source-role build_preamble --out backend/packs/preamble
python -B backend/tools/index_lyx_pair.py --source source/lqbrin-tea-time-numerical-1868821/TeaTimeNumericalAnalysis.lyx --target translation/lyx-id/TeaTimeNumericalAnalysis.lyx --source-rel source/lqbrin-tea-time-numerical-1868821/TeaTimeNumericalAnalysis.lyx --target-rel translation/lyx-id/TeaTimeNumericalAnalysis.lyx --terms-csv 00_control/TERMINOLOGY.csv --code-evidence backend/config/code_evidence.v1.json --file-order 0 --file-kind master_file --source-role master --out backend/packs/TeaTimeNumericalAnalysis
```

The independently acquired Heun page is admitted through a dedicated,
hash-bound authority map. The generator verifies the authority receipt, TIFF
master, PNG derivative, image metadata, UUIDv5 keys, SPDX mapping, and local
relation closure before emitting any backend records:

```text
python -B backend/tools/index_asset_authority.py --lane-root . --config backend/config/heun1900_asset_authority.v1.json --out backend/packs/heun1900-page30
```

The release-pinned `cprotect` 1.0f closure is admitted separately from the
book and image rights. Its generator verifies the byte-exact official CTAN
archive and complete member inventory, the extracted DTX, generated installer
and installable style, primary LPPL notice locations, SPDX `LPPL-1.3c+`
mapping, deterministic UUIDv5 records, provenance relations, and the recorded
byte-exact TeX recipe before emitting any records:

```text
python -B backend/tools/index_toolchain_authority.py --lane-root . --config backend/config/cprotect_toolchain_authority.v1.json --out backend/packs/cprotect-1.0f
```

The generator refuses source/target layout-topology drift. It emits resource,
edition, source-file, unit, relation, segment, localization, rights, QA, and
manifest records, plus asset/version and experiment records only when exact
evidence is declared. LyX insets are kept as protected tokens; translated ERT
navigation labels are hash-bound rather than flattened into prose.

Each child is emitted into `backend/packs/<source-stem>`. The canonical lane
view is a deterministic merge from the lane root:

```text
python -B backend/tools/merge_packs.py --pack backend/packs/preamble --pack backend/packs/TeaTimeNumericalAnalysis --pack backend/packs/preface --pack backend/packs/preliminaries-errors --pack backend/packs/preliminaries-taylor --pack backend/packs/preliminaries-convergence --pack backend/packs/preliminaries-recursion --pack backend/packs/roots-bisection --pack backend/packs/roots-fixedpoint --pack backend/packs/roots-orderOfConvergence --pack backend/packs/roots-newtonsMethod --pack backend/packs/roots-moreConvergenceDiagrams --pack backend/packs/roots-polynomials --pack backend/packs/roots-bracketing --pack backend/packs/interpolation-challenge --pack backend/packs/interpolation-lagrange --pack backend/packs/interpolation-newton --pack backend/packs/calculus-rudiments --pack backend/packs/calculus-undeterminedCoefficients --pack backend/packs/calculus-errors --pack backend/packs/calculus-composite --pack backend/packs/calculus-richardsons --pack backend/packs/splines-parametric --pack backend/packs/splines-cubic --pack backend/packs/ode-pendulum --pack backend/packs/ode-taylor --pack backend/packs/ode-rungeKutta --pack backend/packs/ode-errorAnalysis --pack backend/packs/ode-adaptive --pack backend/packs/solutions --pack backend/packs/answers --pack backend/packs/heun1900-page30 --pack backend/packs/cprotect-1.0f --pack backend/packs/interoperability-v0 --out backend
```

The merger deduplicates only byte-semantically identical stable IDs, rejects
identity collisions, and requires every relation endpoint to resolve.

The current complete backend snapshot has 31 build-file packs (TeX preamble,
LyX master, and 29 included children), one independent asset-authority pack,
one release-toolchain authority pack, and one interoperability-envelope pack.
It contains 281 locale-neutral units, 4,621 English source segments, 4,621
id-ID localizations, 593 terminology records, 15 assets, 15 hash-bound asset
versions, one build recipe, two evidenced experiments, one program, one course,
12 terminology-evidenced locale-neutral concepts, 325 adverse-ledger correction
records, one exact nonfinal baseline artifact, one final Indonesian PDF artifact,
and 17,614 typed relations (28,172 unique records in total). Its exact
manifest is `manifests/lane_manifest.json`, SHA-256
`9a6ccf6ebf1e579216d7a5d7dee70b0da6acd7e5ea6237325b45cada5318a9e0`;
every generation is replayed twice before the cursor advances. Formula, label,
reference, graphic, and executable-code bytes remain protected. Reader-visible
Index content and narrowly scoped digression title arguments may be localized
while retaining their inset/control topology.

Two explicitly audited reader-localization exceptions are represented rather
than hidden. In the TeX preamble's active `titleHGP` tagline, the English
typographic ordinal `$3^{rd}$` becomes natural Indonesian `ke-3`; the reader-map
records that formatting-token change while proving exact surrounding TeX
affixes. In addition,
in `splines-parametric.lyx` layout 37, Indonesian noun order moves the preserved
nonbreaking-space inset ahead of the preserved reader-visible Bézier accent ERT.
The corresponding localization therefore records
`protected_token_shape_equal=false`; the other 4,619 localization token-kind
sequences match.

Generator `ttna-lyx-indexer-0.3.1` adds an explicit source-role contract for the
master while retaining the 0.3.0 child-pack semantics. Generator
`ttna-tex-indexer-0.1.0` binds preamble reader fragments to the pinned
`preamble_reader_map.v1.json` instead of pretending TeX is LyX. The LyX indexer
assigns explicit `LyX-Code` layouts and
genuine ERT-wrapped `verbatim` programs to GPL-3.0-or-later code segments while
retaining the surrounding prose as CC-BY-SA-4.0. The current lane contains 830
GPL-scoped code segments. It marks eighteen source
files plus their containing units as mixed-rights; thirteen files remain
text/build-only. Merger `ttna-pack-merger-0.3.0` validates typed foreign keys for
the evidence and interoperability layers in addition to global identity and
relation closure.
Control-only ERT—including digression, pseudocode, index, and rule macros—is not
classified as executable code.

Generator `ttna-asset-authority-indexer-0.1.0` emits the Heun page-30 PDM
component as one asset, one binary-identity version, one `CC-PDM-1.0` rights
record, and one typed `version_of` relation. Its authority pack is independently
mergeable because it repeats the canonical resource and edition records, which
the full merger byte-semantically deduplicates.

Generator `ttna-toolchain-authority-indexer-0.1.0` emits four `cprotect` 1.0f
assets and four byte-identity versions for the official CTAN archive, canonical
DTX, generated installer, and generated style; one LPPL rights record; one
typed build recipe; and nine typed identity/extraction/generation relations.
The valid SPDX expression is `LPPL-1.3c+`: SPDX lists `LPPL-1.3c`, and its unary
`+` operator encodes the package's explicit “or later” grant. The source release
must preserve the complete, unmodified CTAN archive alongside the byte-exact
generated style.

`config/code_evidence.v1.json` is the canonical fail-closed bridge between
embedded programs and companion Octave files. It records eleven exact mappings
to ten assets: five normalized full-file equalities, one exact line-bounded
excerpt, and five explicitly documented revisions. No filename, title, or fuzzy
similarity is accepted as evidence. The two current experiment records are the
fully specified `experiment1` script run (including invocation and expected
output) and the open-ended six-root interpolation challenge (with no invented
output). Other code and experiments remain unlinked until equally exact evidence
is available.

## Interoperability Envelope v0

`config/interoperability_v0.v1.json` is the reviewed, exact-input map for the
experimental common envelope. The generator fails closed on any task-evidence,
adverse-ledger, artifact, or build-manifest byte drift. It deliberately leaves
the unknown program name/version, C110 title/curriculum role, and prerequisites
as JSON `null` or an empty list with an explicit unknown state. It does not
invent curriculum structure. The twelve concept records are justified only by
accepted English source terms and existing `uses_term` segment evidence; unit
`covers_concept` relations carry those exact evidence-segment IDs.

All rows in the bounded adverse ledger are represented, including open rows.
Their original status is retained, so a `correction` record does not claim that
an open source defect was changed. Free-form locators are mapped to exact source
files only when they name one; affected semantic units stay empty instead of
being guessed. Generate the independently mergeable pack with:

```text
python -B backend/tools/index_interop_v0.py generate --lane-root . --config backend/config/interoperability_v0.v1.json --out backend/packs/interoperability-v0
```

One admitted artifact is the stable 371-page English reproducible baseline,
explicitly marked `baseline_nonfinal`: 8,186,285 bytes, SHA-256
`17cd4abc74cff4934cc78a2f42378489829207f534ad9a051c45ad67b2b18180`.
Its record binds the PDF to the exact 53,055-byte build receipt (SHA-256
`241285cb4f76d560c67c49b905b4be401fecf4dc7d9b86cc8ffaf74335cdefd5`)
and the recorded LyX, latexmk, and cprotect identities. It is not the release
artifact. The final `id-ID-release-pdf` artifact is
`urn:uuid:0c82fceb-d875-53e8-94c9-a20dae5547cb`: 8,202,487 bytes, 387 pages,
SHA-256 `d573b7233d0baa07381e2052a749757885db3a31fbfe695c5a4851ea42d91b6d`,
status `release_final`. It binds build manifest SHA-256
`dbef9a5bb9680f6c072e1f26fe3f5ae8ba7e1ca955d9c3dd47f402d1bb9174ea`.

The final artifact role was bound without manually transcribing byte counts or
hashes. `--refresh-inputs` also rebound the final bounded adverse-ledger
snapshot. The resulting release configuration is
`config/interoperability_v0.release.json`, SHA-256
`4aafff99f18acd992041774e5c07cc6c1289fed2c2b8526b89f3f1d911b190d2`.
The audited commands are:

```text
python -B backend/tools/index_interop_v0.py bind-artifact --lane-root . --base-config backend/config/interoperability_v0.v1.json --artifact output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf --build-manifest build/manifests/id-ID-build.json --role id-ID-release-pdf --locale id-ID --status release_final --refresh-inputs --out-config backend/config/interoperability_v0.release.json
python -B backend/tools/index_interop_v0.py generate --lane-root . --config backend/config/interoperability_v0.release.json --out backend/packs/interoperability-v0
```

The canonical merge and open exports were then regenerated:

```text
python -B backend/tools/export_interop_v0.py export --manifest backend/manifests/lane_manifest.json --schema backend/schema/record.schema.json --out backend/exports/interoperability-v0
python -B backend/tools/export_interop_v0.py verify-round-trip --jsonl backend/exports/interoperability-v0/records.jsonl --csv backend/exports/interoperability-v0/records.csv
```

The JSONL is canonical stable-ID order. The CSV is a lossless open projection
with `id`, `record_type`, and canonical `record_json` columns, so nested records
round-trip without a proprietary database. A later language can select one
unit or several module roots and follow the declared relation/foreign-key policy
to a dependency-closed, independently queryable JSONL subset:

```text
python -B backend/tools/export_interop_v0.py select --records backend/exports/interoperability-v0/records.jsonl --export-manifest backend/exports/interoperability-v0/manifest.json --unit-source-local-id preface.layout.15 --out backend/exports/interoperability-v0/selections/preface-online
```

The selection manifest proves that every emitted relation endpoint and every
UUID foreign key resolves, records the exact followed relation classes, and
requires no proprietary service. The checked example selects six reader
segments from the “Online (in the cloud)” subsubsection and closes to 51 records.
