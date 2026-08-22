# Hak Komponen dan Provenance

Dokumen ini menetapkan batas hak untuk rilis `3.0-id.1`. Tidak ada satu
lisensi blanket yang menggantikan hak setiap komponen.

## Pemetaan komponen

| Komponen | Lingkup | Ekspresi/status | Otoritas |
| --- | --- | --- | --- |
| Buku dan adaptasi | Prosa, eksposisi matematika, gambar buku, dan adaptasi Bahasa Indonesia | `CC-BY-SA-4.0` | `source/lqbrin-tea-time-numerical-1868821/COPYING.txt` dan `license-ccbysa.txt` |
| Kode | Kode yang tercetak dalam buku dan kode elektronik pendamping | `GPL-3.0-or-later` | `source/lqbrin-tea-time-numerical-1868821/COPYING.txt` dan `license-gpl3.txt` |
| Aset Heun 1900 | Pindaian GDZ `PPN599415665_0045`, scan `00000036`, serta turunan rilis yang diperoleh secara independen | Public Domain Mark 1.0; backend `CC-PDM-1.0`; bukan CC0 | `authority/third_party/heun1900/ASSET_AUTHORITY.json` |
| `cprotect` | Paket build `cprotect` jika didistribusikan bersama rilis | `LPPL-1.3c+` | `authority/toolchain/cprotect-1.0f/package/cprotect/README.txt` |

## Atribusi dan pemberitahuan perubahan

Karya asal: Leon Q. Brin, *Tea Time Numerical Analysis*, Third Edition,
upstream [`lqbrin/tea-time-numerical`](https://github.com/lqbrin/tea-time-numerical),
rilis `v3.0`, commit
`186882108a6da95c8dca5b81ce000fc3f8f3ca21`, tree
`1e50d3756b695176008c602f0ee89712f5f32d10`.

Rilis `3.0-id.1` adalah adaptasi Bahasa Indonesia. Perubahan mencakup
lokalisasi permukaan pembaca dan metadata bahasa, backend modular
netral-lokal, perbaikan portabilitas build yang dibatasi, serta penggantian
independen untuk aset Heun yang tidak terdapat dalam arsip upstream. Tidak ada
klaim bahwa byte aset Heun yang hilang telah direkonstruksi.

Dukungan produksi dan penyiapan teknis: **OpenAI Codex atas permintaan
Floris**. Kredit ini tidak menyatakan identitas penerjemah.

## Provenance aset Heun

- Karya: Karl Heun, “Neue Methode zur approximativen Integration der
  Differentialgleichungen einer unabhängigen Veränderlichen,” *Zeitschrift
  für Mathematik und Physik* 45 (1900), halaman cetak 30, Formula VI.
- Institusi: Niedersächsische Staats- und Universitätsbibliothek Göttingen /
  GDZ.
- Manifest IIIF:
  <https://gdz.sub.uni-goettingen.de/iiif/presentation/PPN599415665_0045/manifest>
- Bukti institusional:
  <https://www.deutsche-digitale-bibliothek.de/item/5G33CMRMVBIFAAP3I2UDRHI3D3WMAHD2>
- Pernyataan hak:
  <https://creativecommons.org/publicdomain/mark/1.0/>

## Aturan metadata record

Zenodo menggunakan `CC-BY-SA-4.0` sebagai lisensi tingkat-record karena
artefak utama adalah buku/adaptasi. `GPL-3.0-or-later`, `CC-PDM-1.0`, dan
`LPPL-1.3c+` tetap berlaku hanya pada komponen yang disebutkan di atas. Paket
final harus menyertakan teks lisensi dan ledger hak komponen; metadata Zenodo
tidak boleh ditafsirkan sebagai pelisensian ulang.
