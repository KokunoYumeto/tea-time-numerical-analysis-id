# Accuracy and errors translation boundary — 2026-08-20

Status: complete contiguous draft translation; structurally and
mathematically surface-verified; not yet built or visually checked.

Historical seven-pack backend projection (not a live pointer): this pack had
108 lane-wide terms and 462 relations; its 2,536-byte
manifest is `e87b98515855c26d856edcba3751a2cb33d69a59d5adfa94ace8264912a814ce`.
The canonical seven-pack lane has 4,747 records and manifest SHA-256
`5c871137c341ffa666e8f7b7c6397fce2ca7e1cfa3fd0adfce40c1ddba1ed2d4`.
All backend/hash/next-action figures elsewhere in this receipt are boundary
history; consult `backend/manifests/lane_manifest.json` for live state.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/preliminaries-errors.lyx`
  - 82,768 bytes
  - SHA-256 `0cac16b113657752ae0da8dacf94753f5da8ec337e1b327977428b46331612b8`
- Indonesian target:
  `translation/lyx-id/preliminaries-errors.lyx`
  - 84,277 bytes
  - SHA-256 `f332a4343f0687f8b954420179bf4e1eb39c7ee09139fd05ccca77589d6211ea`
- Contiguous reader boundary: the complete included child, beginning with
  `Chapter Preliminaries` / `Section Accuracy`, continuing through measuring
  and sourcing error, all three experiments, the Lorenz digression, key
  concepts, Octave exposition and verbatim sessions, and every exercise,
  ending at the source `finishexercises` marker.
- Indonesian headings begin `Pendahuluan` / `Akurasi` and include `Mengukur
  Galat`, `Sumber Galat`, `Konsep Utama`, and `Latihan`.
- Next child in exact master include order: `preliminaries-taylor.lyx`.

The pass translates all active prose, headings, table captions and headings,
index terms, historical quotation text, experiment instructions, and exercise
statements. Octave commands, prompts, computed output, formulas, labels,
references, citations, URLs, product and personal names remain protected.

## Exact structural and protected-surface replay

- 138/138 top-level LyX layouts occur in identical order.
- 2,247/2,247 LyX control lines are byte-identical and ordered identically.
- Begin/end command counts match at 991/992.
- 354/354 Formula insets are byte-identical and ordered identically.
- 37/37 CommandInset blocks (labels, references, citations) are byte-identical
  and ordered identically.
- 41/41 ERT blocks retain their positions and structure. Exactly two payloads
  differ, both intentional reader-label localizations:
  `IEEE Standard 754` → `Standar IEEE 754`, and `Chaos` → `Kekacauan`.
  All verbatim Octave sessions and exercise/solution marker macros are exact.
- 24/24 Index insets retain topology; 22 are localized and two proper-name or
  product entries remain unchanged.
- Strict UTF-8 contains zero U+FFFD characters.
- A bounded active-text scan found zero definite untranslated English residue;
  `Massachusetts Institute of Technology` is an intentional proper name.
- No mathematical expression, identifier, cross-reference target, citation
  key, or Octave computation changed.

## Backend pack and combined lane

The per-file pack at `backend/packs/preliminaries-errors/` contains:

- 16 units;
- 138 source segments and 138 id-ID localizations;
- 25 boundary-era terminology records;
- 450 boundary-era typed relations;
- exact edition/resource/source-file/rights/QA records.

Its boundary-era manifest was 2,532 bytes, SHA-256
`8b4a38082f15ec9eafd11a1f488588b02362bf5319559df02a8ddea0d6b05767`.
After the lane-global terminology projection was refreshed by later children,
the current manifest is 2,534 bytes, SHA-256
`a7670670e0e09269eccb507dbe3dac7057d6189fd3dfd78f876d31b6e1d580eb`;
it contains 92 terminology records and 461 typed relations without changing
the 16 unit or 138 segment/localization identities.

At this two-child boundary, the deterministic merge written to the reusable
`backend/manifests/lane_manifest.json` path was 2,952 bytes, SHA-256
`fa1c8243e4027d22aae77ce221dc2c984a23071645ec9b1e37bdf781bf19195b`.
It represents 936 unique records: 24 units, 171 source segments, 171 id-ID
localizations, 25 terms, 537 relations, two source files, two QA events, two
rights components, and the shared exact resource/edition. Every relation
endpoint resolves. Two complete regeneration-and-merge passes were
byte-deterministic. The reusable path is now superseded by the current
six-child manifest recorded in the bisection boundary receipt. The current
errors pack contains 851 record occurrences.

## Admission and next action

Admit this child as `structurally_verified` and `draft_translated`; build and
independent language/visual review remain open. Six included files are now
complete; continue from the current cursor without changing persistent IDs
from this boundary.
