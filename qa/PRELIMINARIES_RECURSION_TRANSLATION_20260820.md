# Recursive-procedures translation boundary — 2026-08-20

Status: complete contiguous natural id-ID draft translation; independently
language- and protected-surface-verified; not yet built or visually checked.

Historical seven-pack backend projection (not a live pointer): this pack had
108 lane-wide terms and 331 relations; its 2,536-byte
manifest is `fa12c7c3d2e5041a3911500a3bf2539c391912a3319a39c11cae4c37856ae7a5`.
The canonical seven-pack lane has 4,747 records and manifest SHA-256
`5c871137c341ffa666e8f7b7c6397fce2ca7e1cfa3fd0adfce40c1ddba1ed2d4`.
All backend/hash/next-action figures elsewhere in this receipt are boundary
history; consult `backend/manifests/lane_manifest.json` for live state.

## Exact boundary

- Source:
  `source/lqbrin-tea-time-numerical-1868821/preliminaries-recursion.lyx`
  — 50,965 bytes, 2,978 lines, SHA-256
  `e00adc252f80d878ecdf7b7d4a4fc63d4e19ca0e2522bf596ab9ee065c29614f`.
- Indonesian target:
  `translation/lyx-id/preliminaries-recursion.lyx`
  — 53,610 bytes, 2,985 lines, SHA-256
  `94ffe033b24b691896d036ce40532ceb74833f8d7ab4e18408abd21f5edb5a34`.
- Contiguous reader boundary: all 120 top-level layouts, from `Prosedur
  Rekursif` through the complete exercises and source `finishexercises`
  marker.
- Next child in the pinned master include order: `roots-bisection.lyx`.

The pass translates the magician dialogue, tromino construction and induction
argument, custom and recursive Octave-function exposition, examples, captions,
index text, and all exercises. Formulas, identifiers, labels, references,
graphics, code, prompts, output, and structural macros remain protected.

## Structural and protected-surface replay

- 120/120 top-level layouts occur in identical order and with identical types.
- 1,297 source/target backslash-control lines retain exact order and bytes.
- 156/156 Formula and 5/5 Graphics insets are byte-identical.
- All 34 CommandInsets retain their targets and topology: 32 are wholly exact;
  two hyperlink display names are intentionally localized to `situs
  pendamping` while their URLs remain exact.
- All 30 ERT blocks retain topology. The sole intended difference is one
  reader-visible digression title; executable ERT remains exact.
- Six Index insets retain topology: five reader terms are localized and the
  proper-name entry `Golomb` remains unchanged.
- All 28 typewriter runs, 16 Quotes insets, and 15 Separators retain their
  source bytes. Three figure captions are localized without changing Float or
  Graphics structure.
- Final post-polish replay found zero unexplained protected-surface differences
  and zero definite active-English prose residue. Strict UTF-8 succeeds with
  zero U+FFFD or NUL characters.

## Source findings retained explicitly

`TTNA-ID-ADV-0014` through `TTNA-ID-ADV-0018` record the source's factorial
base-case mismatch, under-specified recurrence domain, malformed two-case
exercise sentence, typography defects, and protected ordinal/numeric/code
localization surfaces. Reader-facing typography and the malformed connective
are naturally corrected in Indonesian and explicitly marked
`corrected_in_target`; mathematical formulas and executable code are not
silently changed.

## Modular backend

The file-order-5 pack at `backend/packs/preliminaries-recursion/` contains 9
locale-neutral units, 120 English segments, 120 id-ID localizations, 92
lane-wide terminology records, and 331 typed relations. Its manifest is 2,534
bytes, SHA-256
`2fee8963012c320696c6de38b534c20f5741be9d691d3daa90cb3400a12b9dce`.

The deterministic six-pack merge at `backend/manifests/lane_manifest.json`
contains 3,801 unique records: 53 units, 724 source segments, 724 id-ID
localizations, 92 terms, 2,192 relations, six source files, six QA events,
two rights records, and the shared resource/edition. Every relation endpoint
resolves. The 4,109-byte manifest has SHA-256
`733df63c9e8edd9c102df2749d59e25875cfccf4955d2b8c269d72c483036039`;
two consecutive regeneration-and-merge passes were byte-identical.

## Admission and next action

Admit this complete child as `structurally_verified` and `draft_translated`.
Build, visual review, and whole-book terminology review remain open. The sixth
child is complete and admitted; continue the seventh child,
`roots-fixedpoint.lyx`, from layout 1.
