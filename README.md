# Tea Time Numerical Analysis — Edisi Bahasa Indonesia (Edisi Ketiga)

Ini adalah rilis publik edisi Bahasa Indonesia yang mandiri dari *Tea Time
Numerical Analysis* karya Leon Q. Brin. Edisi ini
diturunkan dari rilis upstream `v3.0` dan mempertahankan batas yang dapat
diaudit antara buku, kode, aset pihak ketiga, dan dependensi build.

## Identitas rilis

| Bidang | Nilai |
| --- | --- |
| Sumber daya / mata kuliah | `R015` / `C110` |
| Bahasa | `id-ID` (Zenodo: `ind`) |
| Versi | `3.0-id.1` |
| Tag | `v3.0-id.1` |
| Tanggal rilis | `2026-08-22` |
| Slug repositori | `tea-time-numerical-analysis-id` |
| Repositori | <https://github.com/KokunoYumeto/tea-time-numerical-analysis-id> |
| DOI versi | <https://doi.org/10.5281/zenodo.22054086> |
| DOI konsep | <https://doi.org/10.5281/zenodo.22054085> |
| Penulis karya asal | Leon Q. Brin |
| Rilis upstream | [`lqbrin/tea-time-numerical` `v3.0`](https://github.com/lqbrin/tea-time-numerical/releases/tag/v3.0) |
| Commit upstream | `186882108a6da95c8dca5b81ce000fc3f8f3ca21` |
| Tree upstream | `1e50d3756b695176008c602f0ee89712f5f32d10` |

## Bukti rilis lokal yang diterima

| Bukti | Identitas tepat |
| --- | --- |
| PDF pembaca | `output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf`; 8.202.476 byte; 387 halaman; SHA-256 `cbc31e9e27fdee96845d78fa6a625bf956196001b7941ddf0f1232f5def46b45` |
| Manifest build | `build/manifests/id-ID-build.json`; 53.012 byte; SHA-256 `9437f143c777ca447c5b199f0ea2a7df1e70b2afd7731839c43041ca018fd988` |
| QA seluruh korpus | `qa/WHOLE_CORPUS_RELEASE_QA_20260822.md`; SHA-256 `d1b1da7eea68de58154903dde3c53a9e992dfd7eff1c779feefb75927d774665` |
| Backend final | 28.172 record / 17.614 relasi; `backend/manifests/lane_manifest.json`; SHA-256 `17ef5072077b5b438a883b6bd751ea31b2ec5651567db5d100dba39bf9497cb3` |
| Build sumber portabel | `qa/PORTABLE_RELEASE_SOURCE_QA_20260822.md`; menghasilkan kembali PDF byte-identik |

## Build portabel

Paket sumber menyertakan closure LaTeX 289 berkas yang tepat di
`source/latex-id-ID/`. Dengan PowerShell 7, instalasi TeX/`latexmk`, dan
dependensi yang tercatat, jalankan:

```powershell
pwsh build/Build-PDF.ps1
```

Skrip membangun di `build/work/id-ID/`, menetapkan epoch sumber yang dipin,
dan menyalin PDF ke `output/pdf/` tanpa mengubah sumber rilis.

## Pemberitahuan adaptasi

Edisi ini merupakan adaptasi Bahasa Indonesia dari *Tea Time Numerical
Analysis*, Edisi Ketiga. Perubahan meliputi lokalisasi permukaan pembaca,
metadata bahasa, backend modular yang netral-lokal, dan tooling build yang
portabel. Rumus, identitas matematis, struktur latihan–solusi, sitasi, serta
permukaan kode yang dapat dieksekusi dipertahankan sesuai sumber yang dipin.

Dukungan produksi dan penyiapan teknis diberikan oleh **OpenAI Codex atas
permintaan Floris**. Pernyataan ini bukan atribusi identitas penerjemah dan
tidak menggantikan atribusi Leon Q. Brin sebagai penulis karya asal.

## Batas hak

Metadata tingkat-record menggunakan `CC-BY-SA-4.0` untuk buku dan adaptasi
Bahasa Indonesianya. Hal itu tidak melisensikan ulang komponen lain:

- prosa, eksposisi matematika, gambar buku, dan adaptasi Bahasa Indonesia:
  `CC-BY-SA-4.0`;
- kode yang tercetak maupun menyertai buku: `GPL-3.0-or-later`;
- pengganti independen pindaian halaman Karl Heun: Public Domain Mark 1.0,
  direpresentasikan sebagai `CC-PDM-1.0` dan bukan CC0;
- dependensi build `cprotect`, jika disertakan: `LPPL-1.3c+`.

Lihat [COMPONENT_RIGHTS_AND_PROVENANCE.md](COMPONENT_RIGHTS_AND_PROVENANCE.md)
untuk atribusi, lingkup, dan bukti provenance yang lengkap.

## Status finalisasi

PDF, manifest build, receipt QA, backend, dan paket sumber telah dibekukan.
Record Zenodo `22054086` dipublikasikan pada DOI versi
<https://doi.org/10.5281/zenodo.22054086> dalam lineage DOI konsep
<https://doi.org/10.5281/zenodo.22054085>; ketiga aset publik telah diunduh
kembali tanpa autentikasi dan cocok byte demi byte. Commit rilis lokal
`ae9f99262032fca3c62e6cbcfea1cc1e966b1a74` dan tag `v3.0-id.1` siap, tetapi
GitHub menolak push dengan HTTP 403 karena akun tujuan ditangguhkan.
`FINALIZATION_GATE.json` dan `PUBLICATION_RECEIPT.json` adalah bukti mesin yang
otoritatif; jangan membuat repositori duplikat.

Metadata sitasi tersedia di [CITATION.cff](CITATION.cff), metadata deposit di
[zenodo-metadata.json](zenodo-metadata.json), dan catatan rilis di
[RELEASE_NOTES.md](RELEASE_NOTES.md).
