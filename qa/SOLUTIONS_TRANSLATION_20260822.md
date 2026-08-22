# Selected solutions boundary — 2026-08-22

Status: complete contiguous natural id-ID draft translation; independently
language-, terminology-, protected-surface-, and backend-verified; not yet built
or visually checked.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/solutions.lyx`
  — 537,458 bytes, 30,694 LF-terminated physical lines, SHA-256
  `3a067a637025d85362ca88c57f7ce16b978472ee265e22551b4ffda1ff97fa39`.
- Indonesian target: `translation/lyx-id/solutions.lyx`
  — 548,245 bytes, 30,694 LF-terminated physical lines, SHA-256
  `9ae88015316f7e27e912caa74e57a05a093834047b45b5105815b2f479a6a1cc`.
- The contiguous translated body is physical lines 102–30,692: 535,270
  source bytes, SHA-256
  `55aa82eabb628562ce3fd056a0cebf84a0165e1eea46e4163f01886e2e400676`,
  and 546,057 target bytes, SHA-256
  `011f7ed5d05274832aee04732540160f25033b1002998e2d4c561820374afdb2`.
  The 2,164-byte prefix at lines 1–101 and 24-byte EOF stream at lines
  30,693–30,694 remain source-exact, with SHA-256 respectively
  `b1b3102a22bc9240228197c95a5bbfd99a0139a9ed30b7f51edfd025b8599529`
  and `ef98bc1f7b0b758d9df4e4335d9bbdc8ffbfeff55b9a97c0aec692c54b7794fa`.
- This is file order 28 in the pinned master include sequence.

## Structural and language replay

- All 237 outer reader layouts, 2,157 total layouts, 3,973 inset pairs, and
  103 deeper pairs align. The 12,466-event topology is source/target exact,
  SHA-256
  `87b37fbb838e612ef66499a1c009b6973278f320606337d5d240e245d06110e5`.
- Exactly 3,357 aligned physical lines differ: 3,331 ordinary reader-prose
  lines, sixteen table Text cells, four Index payloads, four Caption payloads,
  and two reader-visible ERT brace arguments. The diff manifest has SHA-256
  `e74ee6839616d56fdb9027c01799a306fc8cbec626b91aa0deb556096295b22d`.
- All 2,716 Formula, 319 CommandInset (305 references, seven labels, seven
  links), 48 Graphics, and 549 LyX-Code blocks are byte-exact. The 104
  typewriter records and 15,533-record control/XML stream are exact. All 28
  tables retain 129 rows, 622 cells, and 1,720 exact XML lines. Of 54 ERTs,
  only the two reader-visible chapter-title arguments at lines 125 and 132 are
  localized; masking those payloads reproduces the exact source stream.
- Independent whole-file review found no active untranslated English,
  omission, semantic drift, or translation-introduced P1/P2/P3 defect.
  Exercise markers, SI units, proper names, Indonesian-valid cognates,
  protected identifiers, and executable code are explicitly excluded rather
  than misclassified as prose.

## Source findings and terminology

`TTNA-ID-ADV-0305` through `TTNA-ID-ADV-0316` bind twelve new deduplicated
findings: three P1, one P2, and eight P3. The three mathematical P1 findings
and the order/degree P2 finding remain source-faithfully `open_recorded`; eight
bounded language repairs are `corrected_in_target`. Recurrences of the friction
overgeneralization and two-word `can not` form extend `TTNA-ID-ADV-0226` and
`TTNA-ID-ADV-0299` rather than creating duplicates. The final 145,899-byte
adverse ledger contains 315 sequential unique rows and has SHA-256
`deb6a09de32b083e1ef8ab5d7bc90e6337b34fa9b7f38094559bfd8a87b949f2`.

The UTF-8/LF vocabulary is accepted through `TTNA-TERM-0564`. It adds selected
exercises, graphing calculators, asymptotes, deflated polynomials, valid
brackets, endpoints, return-value arrays, points of estimation, quadrature
rules, and weighted averages. The existing five-point-formula concept is
extended at `TTNA-TERM-0321` rather than duplicated. The registry has 564
sequential unique accepted rows, occupies 53,931 bytes, and has SHA-256
`785f3901ef408fb8534cf19329b89930834eff588f426f8a9a28b9e9c8680d43`.

## Backend admission snapshot

The file-order-28 mixed-rights pack contains 27 units, 953 English segments,
953 id-ID localizations, 564 terms, and 3,211 relations. All 953
protected-token shapes match; 487 segments are CC-BY-SA-4.0 text and 466
source-exact code segments are GPL-3.0-or-later. Its 3,122-byte manifest has
SHA-256
`d776eb7c1a828e0507f86856d34d909cf14f6589d608895738784a9de5dbf736`.

Because one historical terminology row was canonically extended, all 28 packs
were regenerated twice from their exact final source/target pairs. All 392
canonical pack artifacts matched their 392 replay artifacts byte-for-byte.
The complete twenty-eight-pack merge was then generated twice; all fourteen
merged artifacts matched, typed foreign-key and relation closure passed, and
all five backend tests passed.

The 11,173-byte combined manifest has SHA-256
`b5c0e3922890e0f6ea825d7dd9b380253ef224dc9edeb500172cf499f92d9dce`
and binds 24,385 unique records: 246 units, 4,030 source segments, 4,030 id-ID
localizations, 564 terms, 15,433 relations, 28 source-file records, 28 QA-event
records, ten assets and asset versions, two experiments, two rights records,
one edition, and one resource. Later admissions may supersede this global
snapshot; use `CURRENT_STATE.json` for the live cursor.

## Admission

Admitted as `structurally_verified` and `draft_translated`. Whole-book build,
visual review, corrected-edition deltas, and publication remain open.
