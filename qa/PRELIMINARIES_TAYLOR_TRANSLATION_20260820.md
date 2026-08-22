# Taylor-polynomial translation boundary — 2026-08-20

Status: complete contiguous natural id-ID draft translation; structurally and
mathematically surface-verified; not yet built or visually checked.

Historical seven-pack backend projection (not a live pointer): this pack had
108 lane-wide terms and 424 relations; its 2,534-byte
manifest is `b43066145e9190c61c573837772ca77eaacf0160a0895f8f2001fe4970a04b8b`.
The canonical seven-pack lane has 4,747 records and manifest SHA-256
`5c871137c341ffa666e8f7b7c6397fce2ca7e1cfa3fd0adfce40c1ddba1ed2d4`.
All backend/hash/next-action figures elsewhere in this receipt are boundary
history; consult `backend/manifests/lane_manifest.json` for live state.

## Exact boundary

- Source:
  `source/lqbrin-tea-time-numerical-1868821/preliminaries-taylor.lyx`
  - 66,001 bytes
  - SHA-256 `b36488f82b2a03959660c7236f78df3e41f3ba761251e178b1015dcf90b121c7`
- Indonesian target: `translation/lyx-id/preliminaries-taylor.lyx`
  - 68,440 bytes
  - SHA-256 `e13a431518911b69013584de4d2b4bf7518f5b1db7f53525b2b4c3904754d156`
- Both files contain exactly 3,974 source lines.
- Contiguous reader boundary: the complete included child, from `Section
  Taylor Polynomials` through the final exercise and source
  `finishexercises` marker.
- Indonesian headings include `Polinomial Taylor`, `Konsep Utama`, `Octave`,
  and `Latihan`.
- Next child in exact master include order:
  `preliminaries-convergence.lyx` (105,336 bytes; SHA-256
  `f7ffc429cccd5402adadac938a7a037797a95e96422f64023bda4ab430835b70`).

The pass translates the theorem and proof exposition, Taylor/Maclaurin and
remainder terminology, logarithm and trigonometric examples, captions, index
entries, both historical Brook Taylor digressions and quotation, the complete
Octave tutorial, explanatory pseudo-syntax, and every exercise. Executable
Octave sessions, mathematical formulas, labels, references, graphics paths,
and exercise/solution marker macros remain protected.

## Exact structural and protected-surface replay

- 140/140 top-level LyX layouts occur in identical order.
- 1,615/1,615 structural control lines are byte-identical and ordered
  identically.
- 468/468 Formula insets are byte-identical and ordered identically.
- 26/26 CommandInset blocks are byte-identical and ordered identically.
- 5/5 Graphics insets are byte-identical and ordered identically.
- 24/24 ERT blocks retain exact topology. Exactly two differ, both narrowly
  scoped reader-title localizations:
  `The original theorem of Brook Taylor` → `Teorema asli Brook Taylor`, and
  `Interpretation of the original theorem of Brook Taylor` → `Penafsiran
  teorema asli Brook Taylor`. All executable/verbatim and navigation macros
  are exact.
- 15/15 Index insets retain topology; 14 reader terms are localized and the
  remaining proper-name entry is unchanged.
- Strict UTF-8 parsing succeeds and the target contains zero U+FFFD
  characters.
- A scan over the backend's protected-placeholder target text found zero
  definite active untranslated English prose. Formula-internal English
  ordinal suffixes and `mbox` words remain exact by policy and are recorded in
  `00_control/ADVERSE_LEDGER.csv` for locale-aware derived rendering.
- No formula, mathematical identifier, label, cross-reference target,
  graphics path, or executable computation changed.

## Source findings retained without silent mutation

- In the proof, differentiation requires the denominator exponent `n+1` in
  the displayed `g'(xi)`, while the pinned source says `n-1`; the immediately
  following derivation confirms `n+1`.
- An exercise's `T_{100}(e^x)` notation is ambiguous and is preserved pending
  explicit mathematical correction review.
- The source's doubled dash and omitted leading zero before `.131` are
  separately recorded typography findings.

These findings are bound as TTNA-ID-ADV-0004 through TTNA-ID-ADV-0007. The
pinned authority remains unchanged.

## Backend pack and combined lane

The per-file pack at `backend/packs/preliminaries-taylor/` contains:

- 6 locale-neutral units;
- 140 English source segments and 140 id-ID localizations;
- 92 current lane-wide terminology records;
- 424 typed relations;
- exact edition/resource/source-file/rights/QA records.

Its manifest is 2,532 bytes, SHA-256
`a27cea09eabf2c7678b3a6594235f9fdb69235226808a3c02338ace09bdb404c`.

The current deterministic six-pack merge is
`backend/manifests/lane_manifest.json`, 4,109 bytes, SHA-256
`733df63c9e8edd9c102df2749d59e25875cfccf4955d2b8c269d72c483036039`.
It represents 3,801 unique records: 53 units, 724 English segments, 724 id-ID
localizations, 92 terms, 2,192 relations, six source files, six QA events,
two rights components, and the shared exact resource/edition. Every relation
endpoint resolves. The complete regeneration-and-merge replay is
byte-deterministic.

## Admission and next action

Admit this child as `structurally_verified` and `draft_translated`; build,
visual review, and whole-book terminology review remain open. The following
`preliminaries-convergence.lyx`, `preliminaries-recursion.lyx`, and
`roots-bisection.lyx` children are now also translated and emitted as file
orders 4–6; the stable identities from this boundary remain unchanged.
