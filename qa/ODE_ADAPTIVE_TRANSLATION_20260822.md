# ODE adaptive-methods boundary — 2026-08-22

Status: complete contiguous natural id-ID draft translation; independently
language-, terminology-, protected-surface-, and backend-verified; not yet built
or visually checked.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/ode-adaptive.lyx`
  — 181,652 bytes, 11,372 LF-terminated physical lines, SHA-256
  `2e324b88a692b7808c10a8a3407fe53881bbfc216355d98cae8ffe5842a3c053`.
- Indonesian target: `translation/lyx-id/ode-adaptive.lyx`
  — 182,974 bytes, 11,372 LF-terminated physical lines, SHA-256
  `9e1fb82f0b13195d402e9bb19895faa91f7bdf8d47ed257c03746d3f6957369e`.
- The contiguous reader boundary is physical lines 102–11,369: 179,459
  source bytes, SHA-256
  `bd9ef41d85674ebcffaa09b4deaef4ede148a4a251b4e291aa3a8324d7a8041b`,
  and 180,781 target bytes, SHA-256
  `2b39a8a6a1c51b8f8693f4d45382bd197490f5d9e1e0470a9d0d29ec0b27f912`.
  The 2,168-byte prefix at lines 1–101 and 25-byte EOF stream at lines
  11,370–11,372 remain source-exact, with SHA-256 respectively
  `011b98267ec73ae929e7c142c3ca5c6d5d76b697cb7abca5c5a97a558ca3de1c`
  and `24171f6b58774e39f41451d266dd78bb8a6fd873ab7324fb13478b37fd95ec8b`.
- This is file order 27 in the pinned master include sequence.

## Structural and language replay

- All 76 outer reader layouts, 888 total layouts, 1,489 inset pairs, and 22
  deeper pairs align. The 4,798-event topology has SHA-256
  `b24b7f7ad7c97a660d818face384771b0e12b6d238048de5b21bf4e1cdd1e076`;
  the 6,878-record control projection has SHA-256
  `374e9229a68cb134b77bb6009db3e43c6b16617325c9567d3764102b62d44e68`.
- Exactly 472 aligned physical lines differ: 457 direct prose lines, nine
  Index payloads, three reader-visible ERT payloads, and three table Text
  cells. The diff manifest has SHA-256
  `1c922226b517d5ce7ed1ce06c0223acf3fb45596a813ff858e8a94307999d82c`.
  The other 10,900 lines are source-exact.
- All 575 Formula, 87 CommandInset (35 labels, 47 references, five
  citations), four Graphics, and two LyX-Code blocks are byte-exact. Quotes,
  separators, fixed spaces, and the typewriter payloads `x(1001)` and
  `y(1001)` are exact. Three ERT payloads, eleven Index blocks, and one table
  are changed only on authorized reader-visible text; their topology and
  protected controls remain exact.
- Independent whole-file review found no active untranslated English,
  omission, or translation-introduced P1/P2/P3 defect. Proper names,
  abbreviations, identifiers, protected source-name payloads, and executable
  code are explicitly excluded rather than misclassified as prose.

## Source findings and terminology

`TTNA-ID-ADV-0278` through `TTNA-ID-ADV-0304` bind 27 deduplicated findings:
nine P1, six P2, and twelve P3. Fifteen remain source-faithfully
`open_recorded`; twelve bounded language repairs are `corrected_in_target`.
The inherited absent Heun graphic remains the separate full-build blocker
`TTNA-ID-ADV-0003`; the source-aligned Graphics block is unchanged. The final
141,346-byte adverse ledger contains 303 sequential unique rows and has
SHA-256
`4c9e9611851c94edc55ec7d5614f5168d3afbab47dcbc4fa3ea51a976d9632c3`.

The UTF-8/LF vocabulary is accepted through `TTNA-TERM-0551`. The new terms
cover adaptive and embedded Runge–Kutta methods, Butcher tableaux, safety
factors, stiff ODEs, equilibria, adaptive solvers, and the named 3/8 rule. The
last term's four rendered occurrences are necessarily split around protected
Formula insets. The registry has 551 sequential unique accepted rows, occupies
52,758 bytes, and has SHA-256
`bec557ac3166ff405bbeda9a41653f0d17c0237a6f16314cc39f0f335303cbad`.

## Backend admission snapshot

The file-order-27 mixed-rights pack contains seven units, 145 English
segments, 145 id-ID localizations, 551 terms, and 537 relations. All 145
protected-token shapes match; 143 segments are CC-BY-SA-4.0 text and two
source-exact code segments are GPL-3.0-or-later. Its 3,117-byte manifest has
SHA-256
`10f7ff01a01de1e2aa0a41aaa015f9dbae8233b24bbd62159bb138756079faf1`.

The pack and complete twenty-seven-pack merge were each generated twice. All
fourteen pack artifacts and fourteen merged artifacts matched byte-for-byte;
typed foreign-key and relation closure passed. The 10,900-byte combined
manifest has SHA-256
`0ca74abf9dde63e7bdf0408cba002c8f5d1661984580c1e2f583b915a6a58302`
and binds 18,905 unique records: 220 units, 3,077 source segments, 3,077 id-ID
localizations, 551 terms, 11,900 relations, 27 source-file records, 27 QA-event
records, ten assets and asset versions, two experiments, two rights records,
one edition, and one resource. All five backend tests passed. Later admissions
may supersede this global snapshot; use `CURRENT_STATE.json` for the live
cursor.

## Admission

Admitted as `structurally_verified` and `draft_translated`. Whole-book build,
visual review, corrected-edition deltas, and publication remain open.
