# Hak Komponen dan Provenance

Dokumen ini menetapkan batas hak untuk rilis `3.0-id.2`. Tidak ada satu
lisensi blanket yang menggantikan hak setiap komponen.

## Pemetaan komponen

| Komponen | Lingkup | Ekspresi/status | Otoritas |
| --- | --- | --- | --- |
| Buku dan adaptasi | Prosa, eksposisi matematika, gambar buku, dan adaptasi Bahasa Indonesia | `CC-BY-SA-4.0` | `LICENSES/UPSTREAM-COPYING.txt` dan `LICENSES/CC-BY-SA-4.0.txt` |
| Kode | Kode yang tercetak dalam buku dan kode elektronik pendamping | `GPL-3.0-or-later` | `LICENSES/UPSTREAM-COPYING.txt` dan `LICENSES/GPL-3.0.txt` |
| Aset Heun 1900 | Pindaian GDZ `PPN599415665_0045`, scan `00000036`, serta turunan rilis yang diperoleh secara independen | Public Domain Mark 1.0; backend `CC-PDM-1.0`; bukan CC0 | `authority/third_party/heun1900/ASSET_AUTHORITY.json` |
| `cprotect` | Paket build `cprotect` jika didistribusikan bersama rilis | `LPPL-1.3c+` | `LICENSES/LPPL-1.3c.txt` dan `authority/toolchain/cprotect-1.0f/package/cprotect/README.txt` |

## Atribusi dan pemberitahuan perubahan

Karya asal: Leon Q. Brin, *Tea Time Numerical Analysis*, Third Edition,
upstream [`lqbrin/tea-time-numerical`](https://github.com/lqbrin/tea-time-numerical),
rilis `v3.0`, commit
`186882108a6da95c8dca5b81ce000fc3f8f3ca21`, tree
`1e50d3756b695176008c602f0ee89712f5f32d10`.

Rilis `3.0-id.2` adalah adaptasi Bahasa Indonesia. Perubahan mencakup
lokalisasi permukaan pembaca dan metadata bahasa, backend modular
netral-lokal, perbaikan portabilitas build yang dibatasi, serta penggantian
independen untuk aset Heun yang tidak terdapat dalam arsip upstream. Tidak ada
klaim bahwa byte aset Heun yang hilang telah direkonstruksi.

Dukungan QA terminologi, produksi, dan penyiapan teknis:
**OpenAI Codex gpt-5.6-sol, Ultra**, atas permintaan pengguna. Kredit ini tidak
menyatakan identitas penerjemah dan tidak menggantikan kredit penulis atau
kontributor manusia.

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
