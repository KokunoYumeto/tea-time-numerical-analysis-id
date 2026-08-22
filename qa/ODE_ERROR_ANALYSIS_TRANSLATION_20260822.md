# ODE error-analysis boundary — 2026-08-22

Status: complete contiguous natural id-ID draft translation; independently
language-, terminology-, protected-surface-, and backend-verified; not yet built
or visually checked.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/ode-errorAnalysis.lyx`
  — 54,496 bytes, 2,688 LF-terminated physical lines, SHA-256
  `577fee9bf9cd9ab32cb46a5795b756b8259d16f03149740fcbea141af5778c03`.
- Indonesian target: `translation/lyx-id/ode-errorAnalysis.lyx`
  — 56,057 bytes, 2,688 LF-terminated physical lines, SHA-256
  `a942ba299650dd28c2d35c0e57ba312e5efb146bea18edf0a7ed7ef328722dff`.
- Contiguous reader boundary: source physical lines 85–2685, comprising all
  43 top-level and 92 total layouts; the exact 25-byte EOF stream at lines
  2686–2688 has SHA-256
  `24171f6b58774e39f41451d266dd78bb8a6fd873ab7324fb13478b37fd95ec8b`.
- This is file order 26 in the pinned master include sequence.

## Structural and language replay

- All 43 top-level layouts, 92 total layouts, and 353 inset pairs align; there
  are no deeper pairs. The 890-record topology descriptor has SHA-256
  `1e05dcfbbaa105b65d7abe9a97fa337a8b1e1ab152c71b0cde2b2b32c0d95f31`.
  The 1,391-record structural/control stream is source-exact, SHA-256
  `01d220e6257f8d13e02b562daa199684fe79245bc220060b76ff2b83775f2dab`.
- Exactly 380 physical lines differ, all authorized reader-visible prose. The
  aligned difference map has SHA-256
  `1665ed1103e4316695f109e24801008bbfd7dea782d1a1811edd5e5caa132f64`.
- All 250 Formula, 49 CommandInset, 20 ERT, 15 Index, and four fixed Space
  blocks are source-byte exact. The single Tabular structure remains exact
  apart from two translated visible cells inside two of its fourteen Text
  insets: `term` becomes `suku`, and `leads to condition` becomes
  `menghasilkan syarat`.
- Independent whole-file semantic replay found no active English reader prose,
  omission, or translation-introduced P1/P2/P3 defect. LyX identifiers,
  protected payloads, established method names, and the source-exact exercise
  marker `c` are explicitly excluded rather than counted as translated prose.

## Source findings and terminology

`TTNA-ID-ADV-0266` through `TTNA-ID-ADV-0277` bind twelve deduplicated
findings: four P1, two P2, and six P3. Nine remain source-faithfully
`open_recorded`; three bounded language repairs are `corrected_in_target`.
No pinned Formula, command, ERT, Index, table topology, or control payload was
silently changed. The 129,554-byte adverse ledger contains 276 rows and has
SHA-256
`65ee4814f96589862827b4a9b7c49cf799ac53246d660b0c16f80362ac64b889`.

The UTF-8/LF vocabulary is accepted through `TTNA-TERM-0524`, adding local
truncation error, partial derivatives, the two-variable Taylor theorem, stages,
conditions, ODE solvers, improved Euler and explicit trapezoidal methods,
Heun's third-order method, the classic Runge-Kutta method, RK4, and dependent
sets. Its 524 rows occupy 50,180 bytes and have SHA-256
`3ab1e5d953211b1fa0eaba3d8ed32cae79624b46fe63daaccf9429c7175c9033`.

## Backend admission snapshot

The file-order-26 text-only pack contains seven units, 43 English segments, 43
id-ID localizations, 524 terms, and 259 relations. Its protected-token shapes
match exactly. The 3,116-byte manifest has SHA-256
`3823325d3205c33f6f73514379c07572b6bf96318b583c06f7ebbba9f488cc31`.

The new pack and complete twenty-six-pack merge were each generated twice. All
fourteen pack artifacts and fourteen merged artifacts matched byte-for-byte;
typed foreign-key and relation closure passed. The 10,621-byte combined
manifest has SHA-256
`ddc0da8426f694bf25cc3a34542cd623a5d0294a5ea39890fb72d75c2f384509`
and binds 18,043 unique records: 214 units, 2,932 source segments, 2,932 id-ID
localizations, 524 terms, 11,363 relations, 26 source-file records, 26 QA-event
records, ten assets and asset versions, two experiments, two rights records,
one edition, and one resource. All five backend tests passed. Later admissions
may supersede this global snapshot; use `CURRENT_STATE.json` for the live
cursor.

## Admission

Admitted as `structurally_verified` and `draft_translated`. Whole-book build,
visual review, corrected-edition deltas, and publication remain open.
