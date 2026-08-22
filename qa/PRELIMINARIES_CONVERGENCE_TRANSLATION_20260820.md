# Convergence translation boundary — 2026-08-20

Status: complete contiguous natural id-ID draft translation; structurally and
protected-surface verified; not yet built or visually checked.

Historical seven-pack backend projection (not a live pointer): this pack had
108 lane-wide terms and 369 relations; its 2,539-byte
manifest is `2b85dd8faeb7113ed6d5de084e709c49e6f5abf2de0b2c12c50b8a27fcd89d07`.
The canonical seven-pack lane has 4,747 records and manifest SHA-256
`5c871137c341ffa666e8f7b7c6397fce2ca7e1cfa3fd0adfce40c1ddba1ed2d4`.
All backend/hash/next-action figures elsewhere in this receipt are boundary
history; consult `backend/manifests/lane_manifest.json` for live state.

## Exact boundary

- Source:
  `source/lqbrin-tea-time-numerical-1868821/preliminaries-convergence.lyx`
  — 105,336 bytes, 6,348 lines, SHA-256
  `f7ffc429cccd5402adadac938a7a037797a95e96422f64023bda4ab430835b70`.
- Indonesian target:
  `translation/lyx-id/preliminaries-convergence.lyx`
  — 108,106 bytes, 6,355 lines, SHA-256
  `6013ef64749d1668f951756bae8d6b9d6ffe3f37ed67e7c789071a37582a962e`.
- Contiguous reader boundary: the complete included child, from section
  `Kecepatan` through its last exercise and `finishexercises` marker.
- All exposition, definitions, examples, table prose, reader-visible
  digression titles, index terms, Octave tutorial prose, and exercise prompts
  are Indonesian. Mathematical notation and executable code are preserved.

## Structural and protected-surface replay

- 125/125 top-level LyX layouts occur in identical order and with identical
  layout types.
- 2,892/2,892 backslash control lines and 3,265/3,265 backslash/XML structural
  lines are byte-identical and ordered identically.
- All 490 inset kinds occur in the same order.
- 361/361 Formula, 24/24 CommandInset, 14/14 Quotes, 8/8 nonbreaking-space,
  and 9/9 Separator insets are byte-identical. There are no Graphics insets.
- 46/46 ERT blocks retain topology. Exactly five differ, each solely in a
  reader-visible digression-title argument: order at most one, solving a
  recurrence, nonexistent order, approximating pi, and further material on
  `for` loops. Executable sessions and structural macros remain exact.
- 21/21 Index insets retain topology; 17 reader terms are localized and four
  code/proper-symbol entries remain unchanged.
- The sole LyX-Code exercise is byte-identical.
- Strict UTF-8 decoding succeeds with zero U+FFFD. The nonprotected semantic
  scan found no definite active English prose. Technical identifiers such as
  `for`, `first`, `last`, `disp`, and `.m`, plus English inside protected
  formulas/code/output, remain intentionally exact.

## Source findings retained without silent mutation

- The closed form in the recurrence digression uses exponent `n` after an
  initial datum at `n_0`; it requires `n-n_0` (or an equivalent coefficient).
- The claim using `a>b>=1` says both exponential sequences converge to zero,
  but `b=1` makes one sequence constantly 1.
- One Octave exercise overflows ordinary binary64 at `n=10` and evaluates an
  `Inf/Inf` expression; another requests `n=0` where its formula is `0/0`.
- Two upstream prose typos and protected formula/code language are recorded.

These findings are bound as `TTNA-ID-ADV-0008` through
`TTNA-ID-ADV-0013`; the pinned authority remains unchanged.

## Modular backend

The file-order-4 pack at `backend/packs/preliminaries-convergence/` contains
8 locale-neutral units, 125 English segments, 125 id-ID localizations, 92
current terminology records, and 368 typed relations. Its manifest is 2,537
bytes, SHA-256
`9539fafac1432df46e3235c94b94e9721f83f57a42b543e3bf6a3e0ed1660ae1`.

The current deterministic six-pack lane merge at
`backend/manifests/lane_manifest.json` contains 3,801 unique records: 53
units, 724 source segments, 724 id-ID localizations, 92 terms, 2,192
relations, six source files, six QA events, two rights records, and the
shared resource/edition. Every relation endpoint resolves. The manifest is
4,109 bytes, SHA-256
`733df63c9e8edd9c102df2749d59e25875cfccf4955d2b8c269d72c483036039`.

## Admission and next action

Admit this child as `structurally_verified` and `draft_translated`. Build,
visual review, and whole-book terminology review remain open. Six children are
now complete and emitted; continue the seventh child `roots-fixedpoint.lyx`
from layout 1 without changing existing stable IDs.
