# Catatan Rilis — 3.0-id.2

Tag yang dituju: `v3.0-id.2`

Tanggal rilis: `2026-08-23`

## Ringkasan

`3.0-id.2` adalah rilis patch terminologi untuk edisi Bahasa Indonesia mandiri
yang lengkap dari *Tea Time Numerical Analysis*, Edisi Ketiga, karya Leon Q.
Brin. Seluruh cakupan pembaca `3.0-id.1` dipertahankan. Basis sumbernya tetap
upstream `v3.0` pada commit
`186882108a6da95c8dca5b81ce000fc3f8f3ca21` dan tree
`1e50d3756b695176008c602f0ee89712f5f32d10`.

## Cakupan edisi

- Lokalisasi `id-ID` untuk permukaan pembaca buku, termasuk materi awal,
  bab-bab utama, latihan, jawaban, dan solusi.
- Pemeliharaan rumus, angka, identifier, label silang, struktur pedagogis,
  sitasi, dan kode yang dapat dieksekusi.
- Backend modular netral-lokal dengan identifier stabil, unit dan segmen yang
  dapat dipilih, relasi dependensi, terminology, hak komponen, dan bukti QA.
- Overlay build mandiri yang mengganti path mesin upstream secara terukur tanpa
  menulis ulang sumber otoritatif.
- Penggantian independen untuk aset Heun 1900 yang hilang dari arsip upstream,
  dengan provenance GDZ/SUB Göttingen dan Public Domain Mark 1.0.
- Pemisahan eksplisit antara lisensi buku/adaptasi, kode, aset domain publik,
  dan dependensi build.
- QA istilah lapangan Bahasa Indonesia dengan inspeksi sumber TeX arXiv dan
  fallback representatif *Metode Numerik* karya Rinaldi Munir dari STEI-ITB.
- Pembakuan `galat mutlak`, `galat pemotongan`, dan `galat pemotongan lokal`,
  termasuk pemisahan semantik *truncation* dari *chopping*.
- Provenance model eksplisit: `OpenAI Codex gpt-5.6-sol, Ultra`.

## Kompatibilitas dan provenance

Hubungan LyX–LaTeX tetap dipertahankan. Kode GNU Octave dan permukaan verbatim
tetap berada dalam lingkup `GPL-3.0-or-later`; adaptasi buku berada dalam
lingkup `CC-BY-SA-4.0`. Edisi ini tidak mengklaim rekonstruksi byte aset Heun
yang diabaikan upstream: aset tersebut adalah turunan rilis yang diperoleh
secara independen dari sumber institusional.

## Bukti rilis yang diterima

- PDF pembaca: `output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf`, 8.202.487
  byte, 387 halaman, SHA-256
  `d573b7233d0baa07381e2052a749757885db3a31fbfe695c5a4851ea42d91b6d`.
- Manifest build: `build/manifests/id-ID-build.json`, 52.937 byte, SHA-256
  `dbef9a5bb9680f6c072e1f26fe3f5ae8ba7e1ca955d9c3dd47f402d1bb9174ea`.
- Receipt QA terminologi eksternal:
  `qa/EXTERNAL_INDONESIAN_TERMINOLOGY_QA_20260822.md`, 6.577 byte, SHA-256
  `af709475f228a4ff60ff5972fd30a18452ba46d627c7754c934f928ca01e6918`.
- Backend modular final: 28.172 record dan 17.614 relasi; manifest SHA-256
  `78db2d770201f33e6c8a56b28ba3a01295bb2de24424ce474bd003817ca5ae04`;
  20/20 pengujian dan replay deterministik lulus.
- Closure LaTeX portabel yang dikemas membangun kembali PDF rilis secara
  byte-identik; lihat `qa/PORTABLE_RELEASE_SOURCE_QA_20260822.md`.
- Repositori: <https://github.com/KokunoYumeto/tea-time-numerical-analysis-id>.
- DOI versi: <https://doi.org/10.5281/zenodo.22062071>.

## Kredit produksi

Penulis karya asal: Leon Q. Brin.

Dukungan QA terminologi, produksi, dan penyiapan teknis:
OpenAI Codex gpt-5.6-sol, Ultra, atas permintaan pengguna.
Kredit ini tidak menyatakan identitas penerjemah yang tidak tercatat.

## Gerbang rilis

Build 387 halaman, ekstraksi teks seluruh PDF, inspeksi visual halaman
representatif, replay backend deterministik, round-trip ekspor, dan 20/20
pengujian backend lulus. Patch ini diterbitkan dalam lineage Zenodo konsep
`10.5281/zenodo.22054085`, repositori GitHub yang sama, dan item Figshare yang
sama; receipt publikasi terpisah mencatat pembacaan balik anonim setiap byte.
