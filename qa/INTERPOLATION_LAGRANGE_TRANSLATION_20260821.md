# Lagrange interpolation translation boundary — 2026-08-21

Status: complete contiguous natural id-ID draft translation; language-,
terminology-, protected-surface-, and evidence-linked-backend-verified; not yet
built or visually checked.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/interpolation-lagrange.lyx`
  — 94,889 bytes, 5,833 physical lines, SHA-256
  `5f2d2f37ddf5934e340034558649b00c6458a0e8418546c83323ad5bb1d99e07`.
- Indonesian target: `translation/lyx-id/interpolation-lagrange.lyx`
  — 96,124 bytes, 5,833 physical lines, SHA-256
  `ed865e82cf5cb8ae2a1cf9cd38b9881b07daf9ad21ba3070b7c4cfff5fa9beb4`.
- Contiguous reader boundary: all 124 top-level and 318 total layouts, covering
  the Lagrange form, interpolation error, Sidi and Neville methods, uniqueness,
  Octave implementation, key concepts, exercises, and answers.
- Next child: `interpolation-newton.lyx` — pinned source 84,163 bytes, 5,197
  lines, SHA-256
  `49e7ffee21836c1362daae13920f0c88ce5e0e0bfbeabefb633db5ba02a7ddf9`.
  Its target is translated through top-level layout 60: 84,365 bytes, 5,196
  lines, SHA-256
  `d5d163fc7baa68e9ea08e8f849a123dd654bec1fb1d998e0955cdfe19b7bcc43`.
  Resume at layout 61; layouts 61–118 are still source-identical.

## Structural and protected-surface replay

- All 124 top-level and 318 total layout pairs retain exact type and order; all
  864 insets retain exact type and order.
- All 576 Formula blocks and eight Graphics blocks are byte-identical.
- All 25 labels, 23 references, the citation key, hyperlink target, tables,
  figures, and structural controls retain their source topology. The visible
  hyperlink label is localized as `situs pendamping` while its URL is exact.
- Of 28 ERT blocks, only three reader-facing title/index payloads are localized:
  the Bernstein-polynomial title and the Sidi/Neville cross-index entries.
  Executable ERT remains exact.
- The embedded `nevilles` program is represented separately as one
  GPL-3.0-or-later code segment and an unchanged id-ID localization; surrounding
  prose remains CC-BY-SA-4.0. It is not linked to a companion asset because no
  exact evidence row currently establishes that identity.
- The final terminology pass uses 268 accepted stable terms. After six bounded
  consistency repairs, no active English reader prose or P1/P2/P3 translation
  defect remains outside protected formula, code, identifier, and control
  payloads.

## Source findings retained without silent mathematical mutation

`TTNA-ID-ADV-0124` through `TTNA-ID-ADV-0135` bind twelve distinct upstream
findings. Eight P2 mathematical, cardinality, notation, theorem, or algorithm
issues remain `open_recorded`; two P3 notation/alignment items also remain
open; two unambiguous P3 prose defects are `corrected_in_target`. Pinned Formula
bytes were not changed. Mathematical corrections remain reserved for an
explicit corrected-edition layer.

## Modular backend, code assets, and experiments

The file-order-14 pack contains nine locale-neutral units, 125 English segments
and 125 id-ID localizations: 124 aligned reader-layout segments plus the one
additive GPL code segment. It contains 268 terms and 511 relations. Its
3,127-byte manifest has SHA-256
`e54ab945e1e519ea2eb7ef02566f8322403e4901fe5c8278199f18f9c8c5fd01`.

Generator `ttna-lyx-indexer-0.3.0` and merger
`ttna-pack-merger-0.2.0` produced the complete fourteen-pack lane twice with
zero byte differences. The 7,140-byte canonical manifest has SHA-256
`188b75688bd8fd77277d515053b4c4f3c57eae3034fee50c1d6f0a6f0eb82c82`.
It binds 9,841 unique records: 116 units, 1,631 English segments, 1,631 id-ID
localizations, 268 terms, 10 Octave assets, 10 exact asset versions, two
experiments, 6,141 relations, fourteen source files, fourteen QA events, two
rights records, and the shared resource and edition. Every relation endpoint
and typed evidence-layer foreign key closes.

`backend/config/code_evidence.v1.json` admits only eleven hash-pinned mappings:
five normalized full-file equalities, one exact line-bounded excerpt, and five
documented revisions, resolving to ten assets. It rejects byte drift,
ambiguous fragments, missing locators, and title-only similarity. The two
experiment records are the fully specified `experiment1` script run and the
open-ended six-root interpolation challenge; no result is invented for the
latter. No `rootFindingChallenge.m`, `deflate`, or ambiguous-fragment relation
is asserted.

## Admission and next action

Admit this child as `structurally_verified` and `draft_translated`. Whole-book
build, visual review, corrected-edition deltas, broader asset/experiment
coverage, and publication remain open. Continue
`translation/lyx-id/interpolation-newton.lyx` from top-level layout 61.
