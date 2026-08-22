# Polynomial-roots translation boundary — 2026-08-21

Status: complete contiguous natural id-ID draft translation; independently
language-, terminology-, and protected-surface-verified; not yet built or
visually checked.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/roots-polynomials.lyx`
  — 88,543 bytes, 5,410 physical lines, SHA-256
  `59c9ddb84b1169cc09af81383868baa516e25c9f8f2bbd90da7946c083d756f0`.
- Indonesian target: `translation/lyx-id/roots-polynomials.lyx`
  — 90,773 bytes, 5,418 physical lines, SHA-256
  `77ccf4d0cd6f3e008dbaa2851c9fc7056f1e147423d83e37302d9d66955cade4`.
- Contiguous reader boundary: all 158 top-level and 344 total layouts, covering
  polynomial evaluation and differentiation by synthetic division, Horner's
  method, deflation and factorization, Newton/Horner root finding, the alternate
  quadratic formula, Müller and Laguerre methods, exercises, and answers.
- Next child: `roots-bracketing.lyx` — 73,806 bytes, 4,595 lines, SHA-256
  `c9b73148bbd81a2f00d56a9cdb284b60c3062b6b1f1a05ce4c0ad67954c1d698`.

## Exact structural and protected-surface replay

- 158/158 top-level and 344/344 total layout pairs retain exact type and order.
- All 722 insets retain exact type and order.
- All 433 Formula and two Graphics blocks are byte-identical.
- All 24 labels, 19 references, citation keys, hyperlink targets, and structural
  control sequences are exact. All 33 typewriter spans and the verbatim Octave
  block remain source-exact.
- All 18 index payloads, reader-visible ERT title/index arguments, tables, and
  reader prose are localized. Protected English remains only inside source code,
  executable strings, identifiers, and macro syntax.
- Independent full-file audit found P1=0, P2=0, and P3=0.

## Source findings retained without silent mutation

`TTNA-ID-ADV-0086` through `TTNA-ID-ADV-0101` are 16 unique, deduplicated
source findings. Eight `corrected_in_target` rows record natural corrections to
reader prose or punctuation. Eight `open_recorded` rows retain pinned source
mathematics or specifications exactly, including the Horner recurrence,
factorization notation, Müller update, shifted-basis example, theorem condition,
deflation/output descriptions, and Newton exercise notation. No protected
mathematics or executable code was silently changed.

## Modular backend

The file-order-11 pack contains nine locale-neutral units, 158 English segments,
158 id-ID localizations, 204 lane-wide terms, and 636 relations. Its 2,532-byte
manifest has SHA-256
`f63050cc86630825087025a33dac53f370cd516798df5dfb980bf05d6502df7c`.

The deterministic eleven-pack lane contains 7,708 records: 90 units, 1,329
English segments, 1,329 id-ID localizations, 204 terms, 4,730 relations, eleven
source files, eleven QA events, two rights records, and the shared resource and
edition. The 5,562-byte canonical manifest has SHA-256
`cde8eb182244fda95ccca2702196bb502c85f8c5f33f1bb4b296967a31752194`.
All packs were regenerated twice against the same 204-term snapshot. The two
replays produced identical manifests. Schema, canonical JSONL, sorting, manifest
hash/count, exact pack-union, foreign-key, relation-endpoint, live LyX
re-extraction, and protected-token checks all passed with zero errors.

## Admission and next action

Admit this child as `structurally_verified` and `draft_translated`. Build,
visual review, corrected-edition deltas, and whole-book terminology review remain
open. Continue `roots-bracketing.lyx` from the durable live cursor.
