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
| Versi | `3.0-id.2` |
| Tag | `v3.0-id.2` |
| Tanggal rilis | `2026-08-23` |
| Slug repositori | `tea-time-numerical-analysis-id` |
| Repositori | <https://github.com/KokunoYumeto/tea-time-numerical-analysis-id> |
| DOI versi | <https://doi.org/10.5281/zenodo.22062071> |
| DOI konsep | <https://doi.org/10.5281/zenodo.22054085> |
| Penulis karya asal | Leon Q. Brin |
| Rilis upstream | [`lqbrin/tea-time-numerical` `v3.0`](https://github.com/lqbrin/tea-time-numerical/releases/tag/v3.0) |
| Commit upstream | `186882108a6da95c8dca5b81ce000fc3f8f3ca21` |
| Tree upstream | `1e50d3756b695176008c602f0ee89712f5f32d10` |

## Bukti rilis lokal yang diterima

| Bukti | Identitas tepat |
| --- | --- |
| PDF pembaca | `output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf`; 8.202.487 byte; 387 halaman; SHA-256 `d573b7233d0baa07381e2052a749757885db3a31fbfe695c5a4851ea42d91b6d` |
| Manifest build | `build/manifests/id-ID-build.json`; 52.937 byte; SHA-256 `dbef9a5bb9680f6c072e1f26fe3f5ae8ba7e1ca955d9c3dd47f402d1bb9174ea` |
| QA terminologi eksternal | `qa/EXTERNAL_INDONESIAN_TERMINOLOGY_QA_20260822.md`; 6.577 byte; SHA-256 `af709475f228a4ff60ff5972fd30a18452ba46d627c7754c934f928ca01e6918` |
| Backend final | 28.172 record / 17.614 relasi; `backend/manifests/lane_manifest.json`; SHA-256 `78db2d770201f33e6c8a56b28ba3a01295bb2de24424ce474bd003817ca5ae04` |
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

Dukungan QA terminologi, produksi, dan penyiapan teknis diberikan oleh
**OpenAI Codex gpt-5.6-sol, Ultra**, atas permintaan pengguna. Pernyataan ini
bukan atribusi identitas penerjemah dan tidak menggantikan atribusi Leon Q.
Brin sebagai penulis karya asal.

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

## Status rilis patch

`3.0-id.2` mempertahankan seluruh cakupan edisi lengkap `3.0-id.1` dan
menambahkan QA terminologi lapangan Bahasa Indonesia. Preferred term sekarang
memakai `galat mutlak`, `galat pemotongan`, dan `galat pemotongan lokal`,
dengan pembedaan eksplisit dari *chopping*. Rilis ini memakai lineage Zenodo,
repositori GitHub, dan item Figshare yang sama; jangan membuat record atau
repositori duplikat.

Metadata sitasi tersedia di [CITATION.cff](CITATION.cff), metadata deposit di
[zenodo-metadata.json](metadata/zenodo-metadata.json), dan catatan rilis di
[RELEASE_NOTES.md](RELEASE_NOTES.md).
