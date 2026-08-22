# Bracketing methods translation boundary — 2026-08-21

Status: complete contiguous natural id-ID draft translation; language-,
terminology-, and protected-surface-verified; not yet built or visually checked.

## Exact boundary

- Source: `source/lqbrin-tea-time-numerical-1868821/roots-bracketing.lyx`
  — 73,806 bytes, 4,595 physical lines, SHA-256
  `c9b73148bbd81a2f00d56a9cdb284b60c3062b6b1f1a05ce4c0ad67954c1d698`.
- Indonesian target: `translation/lyx-id/roots-bracketing.lyx`
  — 75,044 bytes, 4,600 physical lines, SHA-256
  `1662e04708a333c520b43e0c19c87e5f857ebb93173d455d4658ed07cf8ebd87`.
- Contiguous reader boundary: all 101 top-level and 375 total layouts, covering
  bracketing principles, false position, bracketed Newton and secant variants,
  inverse quadratic interpolation, Brent-style hybridization, pseudocode,
  implementations, key concepts, exercises, and answers.
- Next child: `interpolation-challenge.lyx` — 27,159 bytes, 1,539 lines,
  SHA-256
  `5baa7e6f20819e05041258776b19a01c1f33f13653c1665f7ceea50256f37de7`.

## Exact structural and protected-surface replay

- 101/101 top-level and 375/375 total layout pairs retain exact type and order.
- All 499 insets retain exact type and order.
- All 256 Formula and three Graphics blocks are byte-identical.
- Labels, references, hyperlink targets, executable Octave, typewriter and
  verbatim payloads, table topology, and structural control sequences remain
  source-exact.
- Reader prose, captions, index payloads, hyperlink display names, and
  reader-visible ERT title/index arguments are localized. Protected English
  remains only inside source code, identifiers, formula syntax, and macros.
- The final bounded language and terminology replay found P1=0, P2=0, and P3=0.

## Source findings retained without silent mutation

`TTNA-ID-ADV-0102` through `TTNA-ID-ADV-0118` are 17 unique, deduplicated
source findings. Nine `corrected_in_target` rows record natural grammar,
terminology, spacing, punctuation, and clarity repairs. Eight `open_recorded`
rows retain pinned mathematics, program behavior, pseudocode interfaces, and
exercise boundaries exactly. The open findings include the `f`/`g` symbol,
iteration limits, an undefined output symbol, an inverse-quadratic denominator,
a stopping-criterion inequality, and two exercise-domain/boundary conditions.
No protected mathematics or executable code was silently changed.

## Modular backend

The file-order-12 pack contains twelve locale-neutral units, 101 English
segments, 101 id-ID localizations, 222 lane-wide terms, and 488 relations. Its
2,533-byte manifest has SHA-256
`913412bbb8db90978a441c3c4292f553713bf22c722689e1a830272252b45b82`.

The deterministic twelve-pack lane contains 8,431 records: 101 units, 1,430
English segments, 1,430 id-ID localizations, 222 terms, 5,220 relations, twelve
source files, twelve QA events, two rights records, and the shared resource and
edition. The 5,843-byte canonical manifest has SHA-256
`4b65be35d786158ef3317ff4fd70a5b2e46e33fae45e2450cde0e61f73009bbf`.
All twelve packs were regenerated twice against the same 222-term snapshot;
the two replays produced identical manifests.

The v1 backend records the CC-BY-SA-4.0 text and GPL-3.0-or-later code rights
separately at corpus level, but it does not yet split verbatim code embedded in
a mixed LyX layout into its own GPL-scoped segment entity. Consequently this
boundary is deterministic and license-aware, but not yet a claim of granular
text/code rights separation. That generator/schema enhancement remains open and
must be completed before final modular publication.

## Admission and next action

Admit this child as `structurally_verified` and `draft_translated`. Build,
visual review, corrected-edition deltas, granular code-entity rights assignment,
and whole-book terminology review remain open. Continue the complete 24-layout
`interpolation-challenge.lyx` child.
