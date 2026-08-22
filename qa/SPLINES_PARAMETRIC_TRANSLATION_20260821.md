# Parametric curves and Hermite interpolation boundary — 2026-08-21

Status: complete contiguous natural id-ID draft translation; independently
language-, terminology-, protected-surface-, and backend-verified; not yet built
or visually checked.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/splines-parametric.lyx`
  — 94,069 bytes, 5,806 physical lines, SHA-256
  `85f63d17074a7fcbb5768d67984aba093279949079feb87cd8886b7d8f08a1f9`.
- Indonesian target: `translation/lyx-id/splines-parametric.lyx`
  — 95,457 bytes, 5,807 physical lines, SHA-256
  `d905db0ee5db02f9e679546345ff586a282438120a66be0c511ff59e7202885c`.
- Contiguous reader boundary: all 121 top-level and 325 total layouts.
- This is file order 21 in the pinned master include sequence.

## Structural and language replay

- All 121 top-level layouts, 325 total layouts, 729 insets, header, controls,
  and EOF retain the source structure and remain balanced.
- All 432 Formula blocks and eight Graphics blocks are source-byte exact. Of 33
  CommandInsets, 32 are byte-exact and the companion-site link changes only its
  reader display; the target URI is exact.
- All nine tables retain their XML topology; eight are byte-exact and the ninth
  changes only the reader headers `Time`, `Distance`, and `Speed`.
- Twenty `LyX-Code` layouts remain byte-exact GPL code.
- Of 74 ERT blocks, eleven are exact, 62 correct the reader-visible grave accent
  in Bézier to its acute accent, and one localizes a digression title. One
  Description label intentionally moves an existing protected space before its
  Bézier accent ERT so natural Indonesian noun order renders as `kurva Bézier`;
  the blocks and counts are preserved and backend QA records this explicit
  token-order exception while returning `pass`.
- Independent whole-file review found no active English reader prose, no
  omission, and P1/P2/P3 target defects of 0/0/0.

## Source findings and terminology

`TTNA-ID-ADV-0195` through `TTNA-ID-ADV-0213` bind nineteen deduplicated source
findings. Three prose/orthographic issues are `corrected_in_target`; sixteen
mathematical, notation, definition, terminology, and pedagogical issues remain
`open_recorded`. No pinned Formula, table, reference target, graphic, or code
payload was silently changed.

The vocabulary is accepted through `TTNA-TERM-0383`, adding osculating and
Hermite polynomials, parametric curves/functions, Bézier and control-point
terminology, recursive/nested interpolation, control polygons, coordinate
systems, speed constraints, and related reusable concepts.

## Backend admission snapshot

The file-order-21 pack contains eight units, 121 English segments, 121 id-ID
localizations, 383 terms, and 455 relations. Its 3,123-byte manifest has
SHA-256
`e20e0f2c408c42871548b33caf71c025e94f4da8e3a10db5d97aa95ec8855262`.

All twenty-one packs and the combined lane were generated twice. All 294 pack
artifacts and fourteen merged artifacts matched byte-for-byte. The 9,211-byte
combined manifest has SHA-256
`037d488b5d1104abaabf9b9b9274291b4f112fb094e2a3b8f83bea8ff7fe15de`
and binds 14,949 unique records: 173 units, 2,453 source segments, 2,453 id-ID
localizations, 383 terms, 9,419 relations, twenty-one source/QA records, ten
assets and asset versions, two experiments, two rights records, one edition,
and one resource. Canonical JSONL, live hashes, relation/typed-FK closure,
rights, and evidence validation passed, as did all five backend tests. Later
admissions may supersede this global snapshot; use `CURRENT_STATE.json` for the
live cursor.

## Admission

Admitted as `structurally_verified` and `draft_translated`. Whole-book build,
visual review, corrected-edition deltas, and publication remain open.
