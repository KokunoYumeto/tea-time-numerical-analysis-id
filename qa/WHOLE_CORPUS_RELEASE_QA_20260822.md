# Whole-Corpus Release QA — Bahasa Indonesia (`id-ID`)

Date: 2026-08-23  
Result: **PASS**  
Scope: all 30 translated LyX files, the locale-specific preamble, the complete 387-page PDF, and the deterministic build closure.

## Artifact identity

- PDF: `output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf`
- Bytes: `8,202,487`
- SHA-256: `d573b7233d0baa07381e2052a749757885db3a31fbfe695c5a4851ea42d91b6d`
- Pages: `387`
- Build manifest: `build/manifests/id-ID-build.json`
- Build-manifest bytes: `52,937`
- Build-manifest SHA-256: `dbef9a5bb9680f6c072e1f26fe3f5ae8ba7e1ca955d9c3dd47f402d1bb9174ea`
- Upstream commit: `186882108a6da95c8dca5b81ce000fc3f8f3ca21`
- Upstream tree: `1e50d3756b695176008c602f0ee89712f5f32d10`
- Final 30-file translated-LyX path/hash set: `8ef8425373bd8162db1919b6cba7e0d1100966ac803b17223ca8cb85f3cc13dc`
- Locale preamble: `translation/lyx-id/preamble.tex`, 7,901 bytes, SHA-256 `6f7940443f59d93a4beb37b20dc2c5c9e7de62ba1dff3f2f9a2b8f0e8d76863b`

## Deterministic build

Two complete, independent invocations of `build/tools/Build-Edition.ps1 -Mode id-ID` passed with LyX and `latexmk` exit code 0. Each exported exactly 30 TeX files and assembled the same 289-file dependency closure. Both invocations produced the exact PDF and manifest identities above. The second run was therefore byte-for-byte reproducible.

The pinned toolchain evidence in the build manifest records LyX 2.4.4, LyX SHA-256 `aa359efbfc16c509a7a91d1c347a6bb702a8fa6b686c0bba8210d058f80c460e`, and `cprotect.sty` SHA-256 `eafa24d80cff3bb804ed46af5f045d41d596f23c6d23e9cb7b01c15aa4efaef2`.

## Source-language, topology, and mathematics audit

- 12,641 source/target Formula pairs: count-exact.
- 92 Formula pairs contain intended reader-facing localization; after masking natural-language annotations, ordinal morphology, and connectors, normalized nontext differences: 0.
- TeX control-sequence mismatches: 0.
- Numeric-token mismatches: 0.
- 21,271 paired insets, 11,216 paired layouts, and 401 deeper structural pairs: 0 stack/topology errors.
- Source/target class counts are exact: 1,953 CommandInset, 307 Graphics, 365 Index, 1,118 ERT, and 845 LyX-Code instances.
- All 307 Graphics payloads are exact; all 845 LyX-Code blocks are exact.
- The 39 differing CommandInset pairs are limited to permitted reader-display payloads for links, citations, and index entries; unpermitted differences: 0.
- Protected labels, reference targets, identifiers, and executable strings remain exact, including `eq:trapezoidal-ode` and `crumpet:eApproximate`.
- Replacement characters, mojibake, and actionable reader-visible English in the authored target: 0.
- Terminology ledger: 593 unique rows.

## Rendered-text audit

- Extraction: `tmp/pdfs/id-ID-final/Tea-Time-Numerical-Analysis-id-ID.txt`
- Bytes: `1,017,000`
- SHA-256: `4a8379c82efde9b3db44a1b58a83cc1300c5cd3c91b2cbe09fe75131e4b30cf9`
- Form feeds: 387.
- Unicode replacement characters: 0.
- English generated `varioref` phrases: 0.
- `Crumpet` reader hits: 0; `Kudapan` hits: 41.
- Residual English tokens are confined to preserved code comments, executable identifiers/variables, bibliography titles, official proper names, URLs, and quoted software/UI literals. Specifically reviewed exceptions include three `subinterval` code comments, five ordinal tokens in code comments/bibliography, one legacy ODE method name in a code comment, and two `error=` code variables.

## PDF structure, logs, fonts, and images

- `pdfinfo` reports 387 pages, unencrypted; all 387 page-size rows are exactly 612 × 792 pt (US Letter).
- `pdfimages -list` reports 341 image objects.
- All core document fonts are embedded. Eight unembedded Standard Helvetica objects originate in imported figure PDFs.
- Poppler reported missing local display-font fallbacks (`Symbol`, Arial/Helvetica Narrow variants, and Arial Unicode) while rasterizing imported graphics. The affected page 353 rendered cleanly at 150 dpi; axes, labels, curves, captions, and bounds are intact.
- Final TeX log: 0 fatal errors, 0 unresolved references, and 0 unresolved citations.
- Diagnostic-only layout messages: 47 overfull boxes, 17 underfull boxes, and 57 inherited duplicate-destination warnings. The all-page visual sweep found no clipping, overlap, or lost content at those locations.
- The inherited BibTeX warning for a month without a year in `goldberg` remains bibliographic-source metadata, not a build or rendering failure.

## Visual QA

Every page was rasterized at 36 dpi into `tmp/qa/d573b7/pages-low/` and inspected across 25 contact sheets in `tmp/qa/d573b7/contact/`. No page is clipped, missing, corrupt, or unexpectedly blank; section pagination, display equations, tables, code blocks, plots, bibliography, and index remain complete.

The following physical PDF pages were also rendered and inspected at 150 dpi in `tmp/qa/d573b7/high/`: 1 (title), 5 (contents), 9 (preface), 24 (`Kudapan` heading), 176 (intentional rotated table), 256 (Heun 1900 scan), 353 (font-warning figure page), 383 (bibliography), and 387 (final index page). All pass.

The Heun scan on physical page 256 is legible, complete, and fully framed. Its final authority receipt is `authority/third_party/heun1900/ASSET_AUTHORITY.json`, 3,695 bytes, SHA-256 `39bbf79cebe96967dabde26b62faf51c55d6ed1b0376000b3b46bf615f79a2dd`; the admitted PNG SHA-256 is `d34c3f99ae1740e9ac7f97bec473b44a3d28353ae503bda1c2bf55e4ee8999d7`.

## Release gate

The Indonesian PDF passes source integrity, translation-language, mathematical invariance, build-closure, reproducibility, PDF-structure, text-extraction, font/image, and whole-corpus visual gates. It is admitted as the release artifact identified above.
