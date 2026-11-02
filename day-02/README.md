# Day 2 — Pencatat Pengeluaran Harian

Proyek harian ke-2: program terminal untuk mencatat pengeluaran dan
melihat totalnya, baik total keseluruhan maupun per kategori.

## Jalankan

```bash
cd day-02
python3 pengeluaran.py
```

Tanpa argumen, program membuka menu interaktif. Bisa juga langsung
dari baris perintah:

```bash
python3 pengeluaran.py tambah 50000 makan "Makan siang"
python3 pengeluaran.py tambah 25000 transport --tanggal 2026-11-02
python3 pengeluaran.py daftar
python3 pengeluaran.py daftar --kategori makan
python3 pengeluaran.py total
python3 pengeluaran.py total --dari 2026-11-01 --sampai 2026-11-30
python3 pengeluaran.py hapus 2 --ya
```

## Catatan

- Hanya Python standar, tanpa library tambahan.
- Data disimpan di berkas `pengeluaran.json` pada folder tempat program
  dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek,
  jadi jangan ikut diunggah ke repositori.
- Nominal bisa ditulis `50000`, `50.000`, atau `Rp 50.000`.
- Tanggal memakai format `YYYY-MM-DD`; kalau tidak diisi, dipakai
  tanggal hari ini.
