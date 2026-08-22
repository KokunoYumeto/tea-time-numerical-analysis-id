# Bisection translation boundary — 2026-08-20

Status: complete contiguous natural id-ID draft translation; independently
language- and protected-surface-verified; not yet built or visually checked.

Historical seven-pack backend projection (not a live pointer): this pack had
108 lane-wide terms and 517 relations; its 2,531-byte manifest is
`93926e68dfc075ef2ef14186fc9aac35101321e4ab034c181c61f890212d0752`.
The canonical seven-pack lane has 4,747 records and manifest SHA-256
`5c871137c341ffa666e8f7b7c6397fce2ca7e1cfa3fd0adfce40c1ddba1ed2d4`.
All backend/hash/next-action figures elsewhere in this receipt are boundary
history; consult `backend/manifests/lane_manifest.json` for live state.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/roots-bisection.lyx`
  — 98,708 bytes, 6,443 lines, SHA-256
  `4a744f52428ef8cba92498111575794c60b1eb682a23729d7b5c9a758fd906d3`.
- Indonesian target: `translation/lyx-id/roots-bisection.lyx`
  — 101,465 bytes, 6,449 lines, SHA-256
  `9a2553905a418c3cf17ea7f3f0c119be8ffe8c2756eb985ab6706d70a65ff543`.
- Contiguous reader boundary: all 168 top-level layouts, from `Pencarian
  Akar` and `Metode Bagi Dua` through the complete exposition, pseudocode,
  Octave implementation, key concepts, exercises, answers, and final source
  marker.
- Next child in pinned master order: `roots-fixedpoint.lyx` — 79,455 bytes,
  SHA-256
  `a63198a74eedad235f2ebd6f84167fb2d496a9a32c20f7a78ab496c0fe67a499`.

All active exposition, instructions, captions, tables, index entries, exercise
prompts, and answers are natural Indonesian. Mathematical formulas, numerical
values, labels, references, graphics paths, typewriter tokens, executable code,
and hidden source notes remain protected.

## Exact structural and protected-surface replay

- 168/168 top-level and 442/442 total layouts retain exact type and order.
- 802/802 insets retain their source topology; begin/end stacks are balanced.
- All 2,978 backslash control lines and all 402 table/XML topology lines are
  byte-identical and ordered identically.
- 477/477 Formula and 3/3 Graphics insets are byte-identical.
- All 22 labels and 21 references are exact. The sole hyperlink target is
  exact; only its reader-visible display name is localized.
- All 86 typewriter runs are exact. Of 34 ERT blocks, 33 are byte-identical;
  the sole difference is the declared reader-visible manual index term.
- Index text, captions, footnotes, and three reader-text tables are localized;
  two math-only tables remain exact.
- Strict UTF-8 succeeds. A complete active-reader scan found zero untranslated
  English prose outside protected executable syntax and proper terms.
- Independent final review found no P1, P2, or P3 translation defect.

## Source findings retained without silent mutation

`TTNA-ID-ADV-0019` through `TTNA-ID-ADV-0026` record source-level mathematical,
specification, pedagogy, encoding, and typography findings. These include the
missing subtraction in a logarithm-error expression, strict/non-strict bound
wording, incorrect endpoint arguments, a stopping explanation referring to an
undefined variable and the wrong pseudocode step, a Unicode minus embedded in
math text, output-name inconsistency, a non-bracketing exercise interval, and
the source punctuation `value?:`. Mathematical/code surfaces remain pinned;
only the harmless punctuation defect is explicitly corrected in the target.

## Modular backend

The file-order-6 pack at `backend/packs/roots-bisection/` contains 10
locale-neutral units, 168 English segments, 168 id-ID localizations, 92
lane-wide terms, and 517 typed relations. Its 2,529-byte manifest has SHA-256
`937bed3867db5e0c2486b41bd569188b85d3943dad4748a8547388326241dc50`.

The deterministic six-pack merge at `backend/manifests/lane_manifest.json`
contains 3,801 unique records: 53 units, 724 English segments, 724 id-ID
localizations, 92 terms, 2,192 relations, six source files, six QA events, two
rights records, and the shared exact resource/edition. Every relation endpoint
resolves. The 4,109-byte manifest has SHA-256
`733df63c9e8edd9c102df2749d59e25875cfccf4955d2b8c269d72c483036039`;
two consecutive full regenerations and merges were byte-identical.

## Admission and next action

Admit this child as `structurally_verified` and `draft_translated`. Build,
visual review, and whole-book terminology review remain open. Seed and translate
the seventh child, `roots-fixedpoint.lyx`, from layout 1 without changing the
stable identities already admitted.
