# QA Terminologi Eksternal Bahasa Indonesia — 2026-08-22

## Hasil

Pencarian arXiv tidak menemukan sumber berbahasa Indonesia dengan sumber TeX
yang sekaligus representatif untuk bidang analisis numerik inti. Satu sumber
TeX berbahasa Indonesia yang benar-benar dapat diunduh dan dibongkar,
arXiv:0807.4609 karya A. B. Mutiara, diperiksa langsung tetapi ditolak sebagai
otoritas istilah utama karena membahas kinerja klaster dan simulasi dinamika
molekular, bukan analisis numerik inti. Paket sumber 155.496 byte memiliki
SHA-256
`80c2f414b9269d15aaf92db71e7b355ff96301a18e7fc5dbe67d7dbbdc86241c`;
berkas TeX 31.672 byte memiliki SHA-256
`79d96864286223614ec257e42b32811b3b53fcf7075626c726ed1d08495e5a15`.
TeX tersebut memuat `\usepackage[bahasa]{babel}` dan istilah komputasi yang
sah, tetapi juga bentuk lemah seperti `tehnik`, `analisa`, dan `efektifitas`.

Sesuai instruksi fallback, pembanding utama adalah lima bab *Metode Numerik*
karya Rinaldi Munir (Penerbit Informatika Bandung, 2003) dari situs resmi
STEI-ITB: Bab 2, 3, 5, 6, dan 8. Kelima PDF—317 halaman total—diekstraksi
seluruhnya dan halaman representatif diperiksa secara visual. Identitas URL,
byte, halaman, serta SHA-256 tercatat dalam
`authority/external_terminology/EXTERNAL_TERMINOLOGY_SOURCE_RECEIPT.json`.

## Perbandingan istilah

| Konsep | Edisi sebelum QA | Bukti Munir | Keputusan |
| --- | --- | --- | --- |
| absolute error | `galat absolut` (79), `galat mutlak` (1) | `galat mutlak` (11), `galat absolut` (0) | Ubah preferred menjadi `galat mutlak`; pertahankan `galat absolut` sebagai varian. |
| truncation error | `galat pemenggalan` / `galat pemenggalan lokal` | `galat pemotongan` (20), termasuk untuk metode Euler, kuadratur, dan galat lokal | Ubah menjadi `galat pemotongan` / `galat pemotongan lokal`. |
| chopping | sumber Inggris memakai `chopped` untuk pemotongan digit titik-mengambang | Munir memakai `pemenggalan` untuk operasi digit tersebut | Pertahankan `pemenggalan` khusus untuk *chopping*; jangan jadikan sinonim truncation error. |
| approximation | `hampiran` | `hampiran` (166), `aproksimasi` (1) | Pertahankan `hampiran`; `aproksimasi` tetap varian. |
| iteration | `iterasi` | Munir memakai `lelaran` (227); materi resmi UNY/UGM memperlihatkan `iterasi` | Pertahankan `iterasi`; catat `lelaran` sebagai varian register, bukan preferred. |
| Newton/secant | `metode Newton`; `metode sekan` | `Metode Newton-Raphson`; `metode secant` | Pertahankan bentuk edisi yang setia pada nama sumber; catat bentuk bukti sebagai varian. |
| bisection | `metode bagi dua` | `metode bagidua`; UNY memakai `metode bagi dua` | Pertahankan `metode bagi dua`. |
| convergence | keluarga `kekonvergenan`; sifat `konvergen` | `kekonvergenan` dan `konvergensi` sama-sama muncul | Pertahankan keluarga istilah edisi demi konsistensi. |
| interpolation/spline | `interpolasi`; `splin` (`spline` sebagai varian) | `interpolasi polinom`, `polinom interpolasi`, dan `spline` | Tidak ada perubahan preferred. |
| integration/quadrature | `integrasi numerik`; `kuadratur` | `integrasi numerik` (65), `kuadratur` (14), khususnya Gauss | Pertahankan keduanya dan jangan samakan semua integrasi dengan kuadratur. |
| ODE/Runge-Kutta/step size | `persamaan diferensial biasa (PDB)`; `Runge-Kutta`; `ukuran langkah` | 40 / 61 / 26 kemunculan | Tidak ada perubahan. |

## Dasar semantik dua koreksi

Pada sumber Inggris, *truncation error* adalah galat algoritmik akibat
penggantian deret dengan jumlah parsial atau akibat pemotongan orde suatu
metode. Itu sama dengan penggunaan `galat pemotongan` dalam bab Munir. Sumber
Inggris juga membahas nilai titik-mengambang yang *chopped*; Munir memakai
`pemenggalan` untuk operasi digit ini. Pembedaan tersebut lebih tepat daripada
memakai `pemenggalan` untuk kedua konsep.

`Galat mutlak` juga selaras secara matematis dengan ledger edisi yang sudah
memakai `nilai mutlak` untuk *absolute value*. Koreksi ini menghilangkan satu
ketidakkonsistenan internal sekaligus mengikuti bukti lapangan.

## Provenance model dan kredit

Dukungan QA terminologi, produksi, dan penyiapan teknis untuk revisi ini
menggunakan **OpenAI Codex gpt-5.6-sol, Ultra**, atas permintaan pengguna.
Identifikasi model ini tidak menggantikan atau menyiratkan kredit penulis,
penerjemah, atau kontributor manusia. Penulis karya asal tetap Leon Q. Brin;
seluruh kredit sumber dan kontributor yang sudah ada dipertahankan.

## Status propagasi

Propagasi kanonik selesai dan lulus gerbang berikut:

- `00_control/TERMINOLOGY.csv` tetap berisi 593 term ID stabil. Preferred
  `absolute error`, `truncation error`, dan `local truncation error` sekarang
  masing-masing adalah `galat mutlak`, `galat pemotongan`, dan
  `galat pemotongan lokal`. Bentuk lama tercatat sebagai varian atau rejected
  form sesuai maknanya.
- Delapan belas berkas LyX menerima 79 penggantian frasa `galat absolut` dan
  48 penggantian `pemenggalan`; audit lanjutan memperbaiki 14 token matematika
  `absolut` yang tersembunyi oleh inset/index serta satu bentuk berimbuhan
  `absolutnya`. Identifier referensi internal Inggris seperti
  `ex:absoluteError` tetap byte-utuh.
- Seluruh 31 paket terjemahan/build diregenerasi. Backend agregat tetap
  memiliki 28.172 record unik: 4.621 segmen Inggris, 4.621 lokalisasi id-ID,
  593 record istilah, dan 17.614 relasi dengan endpoint lengkap. Manifest
  `backend/manifests/lane_manifest.json` berukuran 14.060 byte dan memiliki
  SHA-256
  `e11119d2e7ab1118ab75ea986c05d441cc22391d4ce44e6fce7bcf0b3c357301`.
- Semua 4.621 lokalisasi menyimpan provenance
  `OpenAI Codex gpt-5.6-sol, Ultra, at the user's request`; tidak ada baris
  provenance yang menyimpang.
- Ekspor JSONL/CSV 28.172-record lulus round-trip semantik dan UTF-8/LF.
  Seluruh 20 pengujian backend lulus pada replay final.
- PDF final `output/pdf/Tea-Time-Numerical-Analysis-id-ID.pdf` berukuran
  8.202.487 byte, 387 halaman, SHA-256
  `d573b7233d0baa07381e2052a749757885db3a31fbfe695c5a4851ea42d91b6d`.
  Manifest build 52.937 byte memiliki SHA-256
  `dbef9a5bb9680f6c072e1f26fe3f5ae8ba7e1ca955d9c3dd47f402d1bb9174ea`.
- Ekstraksi teks PDF menemukan 82 `galat mutlak`, 39 frasa tepat
  `galat pemotongan`, dan nol bentuk keluarga `absolut*` atau
  `pemenggalan*` pada permukaan pembaca. Halaman PDF 13, 18, 246, 347, 377,
  dan 387 lulus inspeksi visual pada definisi, analisis PDB, jawaban, dan
  indeks.

Rilis patch yang memuat QA ini menggunakan versi `3.0-id.2` dalam lineage
publik yang sama; DOI Zenodo telah diprareservasi sebagai
`10.5281/zenodo.22062071` sebelum transaksi file final.
