# Catatan Rilis — 3.0-id.1

Tag yang dituju: `v3.0-id.1`

Tanggal rilis: `2026-08-22`

## Ringkasan

`3.0-id.1` adalah versi pertama edisi Bahasa Indonesia mandiri dari *Tea Time
Numerical Analysis*, Edisi Ketiga, karya Leon Q. Brin.
Basis sumbernya adalah upstream `v3.0` pada commit
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

## Kompatibilitas dan provenance

Hubungan LyX–LaTeX tetap dipertahankan. Kode GNU Octave dan permukaan verbatim
tetap berada dalam lingkup `GPL-3.0-or-later`; adaptasi buku berada dalam
lingkup `CC-BY-SA-4.0`. Edisi ini tidak mengklaim rekonstruksi byte aset Heun
yang diabaikan upstream: aset tersebut adalah turunan rilis yang diperoleh
secara independen dari sumber institusional.

## Bukti rilis yang diterima

- PDF pembaca: `output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf`, 8.202.476
  byte, 387 halaman, SHA-256
  `cbc31e9e27fdee96845d78fa6a625bf956196001b7941ddf0f1232f5def46b45`.
- Manifest build: `build/manifests/id-ID-build.json`, 53.012 byte, SHA-256
  `9437f143c777ca447c5b199f0ea2a7df1e70b2afd7731839c43041ca018fd988`.
- Receipt QA seluruh korpus: `qa/WHOLE_CORPUS_RELEASE_QA_20260822.md`, SHA-256
  `d1b1da7eea68de58154903dde3c53a9e992dfd7eff1c779feefb75927d774665`.
- Backend modular final: 28.172 record dan 17.614 relasi; manifest SHA-256
  `17ef5072077b5b438a883b6bd751ea31b2ec5651567db5d100dba39bf9497cb3`;
  20/20 pengujian dan replay deterministik lulus.
- Closure LaTeX portabel yang dikemas membangun kembali PDF rilis secara
  byte-identik; lihat `qa/PORTABLE_RELEASE_SOURCE_QA_20260822.md`.
- Repositori: <https://github.com/KokunoYumeto/tea-time-numerical-analysis-id>.
- DOI versi: <https://doi.org/10.5281/zenodo.22054086>.

## Kredit produksi

Penulis karya asal: Leon Q. Brin.

Dukungan produksi dan penyiapan teknis: OpenAI Codex atas permintaan Floris.
Kredit ini tidak menyatakan identitas penerjemah yang tidak tercatat.

## Gerbang rilis

Bukti PDF/build/QA dan paket sumber/backend telah diterima. Zenodo record
`22054086` dipublikasikan pada DOI versi `10.5281/zenodo.22054086` dan DOI
konsep `10.5281/zenodo.22054085`; seluruh tiga aset publik lulus pembacaan balik
anonim. Setelah akun tujuan dipulihkan, branch `main` dan tag anotasi
`v3.0-id.1` berhasil didorong ke repositori GitHub yang sudah ditetapkan. Rilis
GitHub memakai PDF, paket sumber/backend, dan manifest checksum yang sama persis
dengan artefak terverifikasi. Edisi kerja Figshare reader-first juga tersedia
pada <https://doi.org/10.6084/m9.figshare.33314724.v2>. Bukti lengkap tercatat
dalam `FINALIZATION_GATE.json` dan `PUBLICATION_RECEIPT.json`.
