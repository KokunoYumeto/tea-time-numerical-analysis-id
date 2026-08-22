# Fixed-point iteration translation boundary — 2026-08-20

Status: complete contiguous natural id-ID draft translation; independently
language- and protected-surface-verified; not yet built or visually checked.

The backend and next-action figures below record the seven-pack boundary and
are not a live pointer after later children; consult
`backend/manifests/lane_manifest.json` and `00_control/CURRENT_CURSOR.json` for
current state.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/roots-fixedpoint.lyx`
  — 79,455 bytes, 4,657 physical lines, SHA-256
  `a63198a74eedad235f2ebd6f84167fb2d496a9a32c20f7a78ab496c0fe67a499`.
- Indonesian target: `translation/lyx-id/roots-fixedpoint.lyx`
  — 81,449 bytes, 4,653 physical lines, SHA-256
  `bf830bd8f0163f400ccb7c2d9516f5c550c830f626865181f291199648426589`.
- Contiguous reader boundary: all 154 top-level layouts, from `Iterasi Titik
  Tetap` through the complete exposition, theorems, proofs, pseudocode, Octave
  material, exercises, answers, and final source marker.
- Next child in pinned master order: `roots-orderOfConvergence.lyx` — 106,660
  bytes, SHA-256
  `29ec9217f46e5d3db113dbc7c4cfa6b0aeea0cd17b1bcaf8f3142e98142b741e`.

All active exposition, instructions, captions, index entries, exercise prompts,
and answers are natural Indonesian. Mathematical formulas, numerical values,
labels, references, graphics paths, typewriter tokens, executable code, and
hidden source notes remain protected.

## Exact structural and protected-surface replay

- 154/154 top-level layout types retain exact type and order.
- 485/485 Formula and 17/17 Graphics insets are byte-identical.
- All 28 ERT blocks retain their source topology; 26 are byte-identical. The
  two declared reader-facing localizations are the manual index redirect and
  the digression title `Sebuah kuadrat yang menarik`.
- All 71 CommandInsets retain their source topology; 70 are byte-identical.
  The sole declared change localizes a hyperlink display name to `situs
  pendamping` while preserving its target exactly.
- All 2,105 backslash control and markup records are byte-identical and ordered
  identically. Labels, references, citations, graphics paths, and all 11
  typewriter runs are exact.
- Strict UTF-8 succeeds. A complete active-reader scan found zero untranslated
  English prose outside protected executable syntax and proper terms.
- Independent final and post-fix reviews found no P1, P2, or P3 translation
  defect.

## Source findings retained without silent mutation

`TTNA-ID-ADV-0027` through `TTNA-ID-ADV-0036` record source-level mathematical,
pedagogical, specification, encoding, quantifier, grammar, and typography
findings. The P2 items cover missing absolute-value bars in a Mean Value
Theorem proof, an unjustified tolerance-as-error claim, three incorrect
denominators in the final answer, and an overbroad nonconvergence statement.
Protected mathematical and executable surfaces remain pinned. Two harmless
reader-facing source ambiguities are explicitly repaired in Indonesian and
recorded as `corrected_in_target`.

## Modular backend

The file-order-7 pack at `backend/packs/roots-fixedpoint/` contains eight
locale-neutral units, 154 English segments, 154 id-ID localizations, 108
lane-wide terms, and 610 typed relations. Its 2,530-byte manifest has SHA-256
`634f1574a829f337e3838fb9f74f80378c172d251942eec214c8d396af2354a9`.

The deterministic seven-pack merge at `backend/manifests/lane_manifest.json`
contains 4,747 unique records: 60 units, 878 English segments, 878 id-ID
localizations, 108 terms, 2,805 relations, seven source files, seven QA events,
two rights records, and the shared exact resource/edition. Every relation
endpoint resolves. The 4,389-byte manifest has SHA-256
`5c871137c341ffa666e8f7b7c6397fce2ca7e1cfa3fd0adfce40c1ddba1ed2d4`;
two consecutive fixed-point regeneration and lane-merge runs were
byte-identical. An independent replay then schema-validated all 10,172 pack
and combined JSONL occurrences, reproduced every live LyX record, and found
zero unresolved relation or foreign-key endpoint.

## Admission and next action

Admit this child as `structurally_verified` and `draft_translated`. Build,
visual review, corrected-edition deltas, and whole-book terminology review
remain open. Seed and translate the eighth child,
`roots-orderOfConvergence.lyx`, from layout 1 without changing stable
identities already admitted.
