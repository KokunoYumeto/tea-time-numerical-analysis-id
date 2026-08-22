# Interpolation challenge translation boundary — 2026-08-21

Status: complete contiguous natural id-ID draft translation; language-,
terminology-, protected-surface-, and mixed-rights-backend-verified; not yet
built or visually checked.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/interpolation-challenge.lyx`
  — 27,159 bytes, 1,539 physical lines, SHA-256
  `5baa7e6f20819e05041258776b19a01c1f33f13653c1665f7ceea50256f37de7`.
- Indonesian target: `translation/lyx-id/interpolation-challenge.lyx`
  — 27,803 bytes, 1,541 physical lines, SHA-256
  `238c535ea46819bf1a0530b0afd7a45a08fd3fdbdb6786d852528d997e4b85ce`.
- Contiguous reader boundary: all 24 top-level and 97 total layouts, covering
  the root-finding challenge, fractal interpolation construction, the function,
  antiderivative and derivative, exact/approximate evaluation, the Octave
  program, and answers.
- Next child: `interpolation-lagrange.lyx` — 94,889 bytes, 5,833 lines,
  SHA-256
  `5f2d2f37ddf5934e340034558649b00c6458a0e8418546c83323ad5bb1d99e07`.
  Its contiguous layouts 1–30 are already translated; resume at layout 31.

## Exact structural and protected-surface replay

- 24/24 top-level and 97/97 total layout pairs retain exact type and order.
- All 163 insets retain exact type and order.
- All 138 Formula and three Graphics blocks are byte-identical.
- All six labels, five references, the citation key, hyperlink target, two
  floats, two captions, and structural control sequences retain their source
  topology. The complete ERT-wrapped Octave program remains byte-identical.
- Of three ERT blocks, only the reader-visible digression title is localized;
  the closing control and raw ERT-wrapped verbatim program remain exact. The
  hyperlink display name is localized while its target is unchanged.
- A final bounded prose and terminology pass found no active English residue
  outside code, identifiers, formula syntax, and macro controls, with
  P1=0, P2=0, and P3=0.

## Source findings retained without silent mutation

`TTNA-ID-ADV-0119` through `TTNA-ID-ADV-0123` are five unique P3 source
findings. All are `corrected_in_target`: a category error concerning a function
versus its graph, duplicated punctuation, a missing article, an incorrect
determiner, and singular/plural disagreement. No mathematical formula,
identifier, citation, or executable-code byte was changed.

## Modular backend and rights

The file-order-13 pack contains eight locale-neutral units, 25 English segments
and 25 id-ID localizations: 24 aligned reader-layout segments plus one additive
GPL-scoped embedded-code segment. It also contains 247 lane-wide terms and 99
relations. Its 2,528-byte manifest has SHA-256
`223257db6beb6dfbd84acef2cb9ff94303de013c2c54327e5b5cdf72fa351eeb`.

The deterministic thirteen-pack lane contains 8,957 records: 108 units, 1,506
English segments, 1,506 id-ID localizations, 247 terms, 5,560 relations,
thirteen source files, thirteen QA events, two rights records, and the shared
resource and edition. The 6,241-byte canonical manifest has SHA-256
`7619e6e7c9f56079fb5e0bfa5dc1cc54982eb2213e43e61c88e843b2c50ff72c`.
All thirteen packs were regenerated twice against the same 247-term snapshot;
the two replays produced identical manifests.

Generator `ttna-lyx-indexer-0.2.0` now separates real ERT-wrapped verbatim code
and explicit `LyX-Code` layouts into GPL-3.0-or-later code segments while prose
remains CC-BY-SA-4.0. Across the admitted lane it emits 54 GPL-scoped code
segments—52 embedded verbatim programs and two explicit code layouts—and marks
ten source files and their containing units as mixed-rights. It does not infer
code from control-only ERT. Distinct experiment entities and links to companion
`.m` assets remain open; the present receipt does not claim that layer exists.
The challenge program's normalized code payload is 1,603 bytes, SHA-256
`6bc31603ec8d8483836cc3fa0a1ccea4baf4d764be069508496360b6b856d219`;
its source and target code entities are unchanged and hash-identical.

## Admission and next action

Admit this child as `structurally_verified` and `draft_translated`. Build,
visual review, corrected-edition deltas, experiment/asset linkage, and
whole-book terminology review remain open. Continue
`translation/lyx-id/interpolation-lagrange.lyx` from top-level layout 31.
