# Preface translation boundary — 2026-08-20

Status: complete contiguous draft translation; structurally verified; not yet
built or visually checked.

Historical seven-pack backend projection (not a live pointer): this pack had
108 lane-wide terms and 92 relations; its 2,514-byte
manifest is `b846984227febdabac3174f8bf8fc8ab2d749f5e942d3bb8132ddfc8ca34a5fd`.
The canonical seven-pack lane has 4,747 records and manifest SHA-256
`5c871137c341ffa666e8f7b7c6397fce2ca7e1cfa3fd0adfce40c1ddba1ed2d4`.
All backend/hash/next-action figures elsewhere in this receipt are boundary
history; consult `backend/manifests/lane_manifest.json` for live state.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/preface.lyx`
  - 17,942 bytes
  - SHA-256 `6311a41ac9b47e05e4b13eaf897ba3a2b6752a468ae17a241d4e49ecbae50083`
- Indonesian target: `translation/lyx-id/preface.lyx`
  - 19,048 bytes
  - SHA-256 `3a7bde438fca589225493b204e2015e72480801561ed83194094525c97a77b8d`
- Contiguous reader boundary: the complete front-matter child, from
  `Chapter* Preface` through the final paragraph of `Acknowledgments`, now
  rendered in source as `Prakata` through `Ucapan Terima Kasih`.
- The next untranslated child in master include order is
  `preliminaries-errors.lyx`.

The pass translated every reader-facing paragraph, heading, subheading, and
table-of-contents/header label in this child. Proper names, the book title,
URLs, contact address, product names, source-era service claims, and the
solution-marker macros remain faithful. No source-authority byte was edited.

## Structural and language checks

- 37/37 top-level LyX layouts occur in the identical order.
- All 284 source/target LyX control lines are byte-identical and ordered
  identically.
- Begin/end, layout, and inset counts match (86 begin commands, 87 end
  commands, 49 total layout blocks including nested layouts, 32 insets).
- All 33 emitted segment pairs retain identical protected-token kind shapes.
  The `hasasolution` and `haspartwithsolution` ERT macros and every hyperlink
  target are unchanged. Five ERT navigation labels are intentionally localized
  and hash-bound in the localization records.
- Strict UTF-8 check found zero U+FFFD characters.
- A bounded active-English lead scan found no untranslated prose; its two hits
  were the non-rendered LyX generator comment and the product name `Octave
  Online`. This is not yet a final independent language review.
- The preface contains no mathematical formula surface. Mathematical QA is
  therefore not applicable at this boundary.
- No LyX/PDF build or visual claim is made; the local machine does not yet have
  the pinned LyX toolchain.

## Modular backend emitted from this boundary

Generator: `backend/tools/index_lyx_pair.py`, 23,837 bytes, SHA-256
`cdd7ad06e1dba7002d57bf3cb05a271d984b0942bc86511939f660017912e15c`.
The initial pack was migrated to the general multi-file pack layout without
changing its persistent unit or segment IDs. Two consecutive current runs
produced the same manifest bytes.

The boundary-era manifest was SHA-256
`27f0c0055e5833e942aa7a67546bf9fcf3e71bf8de3b0e64dbd90f34354228e6`.
Because terminology is intentionally lane-global, later contiguous children
refresh the derived term projection without changing preface identities.
The current `backend/packs/preface/manifests/lane_manifest.json` is 2,512
bytes, SHA-256
`75e973b56d3ae42355c0556c91d090bcace5106d2fe4fc5516c76b6567b8cfae`.

The pack contains:

- 1 resource and 1 exact edition record;
- 1 source-file/version record binding both LyX files;
- 9 locale-neutral units (work, front-matter file, chapter, four sections,
  two subsubsections);
- 33 source segments and 33 id-ID localization records;
- 92 current lane-wide terminology records;
- 91 typed relations, including containment, translation, and term use;
- 2 component-scoped rights records (CC-BY-SA-4.0 prose and
  GPL-3.0-or-later code);
- 1 topology QA event.

Across 10 JSONL files the current pack has 264 record occurrences with stable
UUIDv5 URNs.
Every relation endpoint resolves. JSONL is canonicalized with sorted keys and
LF; the manifest records each file's byte count, record count, and SHA-256.
The generic record schema is at `backend/schema/record.schema.json`.

## Admission and next action

This boundary is admitted as `structurally_verified` and remains
`draft_translated`, `not_built`, `unpublished`. Six included files are now
complete; continue from the current cursor while extending the same stable
backend rather than replacing this pack or regenerating identities from
Indonesian wording.
