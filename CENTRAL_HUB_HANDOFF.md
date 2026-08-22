---
schema_id: ttna-id-central-hub-handoff-v1
schema_version: 1.0.0
status: awaiting_individual_release
hub_destination: null
hub_destination_note: "TBD — tujuan hub Bahasa matematika belum tercatat; jangan membuat URL atau DOI."
---

# Handoff Hub Pusat — R015 / C110

Dokumen ini menyiapkan integrasi edisi individual ke hub Bahasa matematika
setelah transaksi GitHub dan Zenodo selesai. Ketiadaan tujuan hub dicatat
secara eksplisit sebagai `null`; hal itu bukan blocker untuk menjaga satu
rilis individual yang tidak duplikatif.

## Identitas stabil

- Sumber daya: `R015`
- Mata kuliah: `C110`
- Judul: *Tea Time Numerical Analysis — Edisi Bahasa Indonesia (Edisi Ketiga)*
- Locale: `id-ID`
- Versi/tag: `3.0-id.1` / `v3.0-id.1`
- Slug individual: `tea-time-numerical-analysis-id`
- Resource UUID: `urn:uuid:8fbaf4c5-6316-5159-89b9-787aa115c0dc`
- Edition UUID: `urn:uuid:35b4350d-7202-5d47-8b85-5262d7ca441c`

## Data yang diteruskan setelah publikasi

Handoff final harus menambahkan, dari bukti publik yang telah dibaca kembali:

1. URL repositori, commit, tag, dan rilis individual;
2. DOI konsep dan DOI versi Zenodo;
3. inventaris artefak publik beserta ukuran byte dan SHA-256;
4. ringkasan QA final dan bukti build reproducible;
5. batas lisensi komponen dan provenance aset Heun;
6. tautan backend modular serta identifier resource/edition di atas.

Jangan membuat repositori atau record Zenodo hub baru hanya untuk mengisi
template ini. Hub yang sah harus ditentukan dari tujuan program yang nyata.
