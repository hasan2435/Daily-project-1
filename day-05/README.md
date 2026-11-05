# Day 5 — Kalkulator Tanggal

Proyek harian ke-5: program terminal untuk urusan tanggal sehari-hari.
Program bisa menghitung selisih dua tanggal (termasuk jumlah hari kerja
Senin-Jumat), menggeser tanggal maju atau mundur sejumlah hari (biasa
atau hanya hari kerja), mencari nama hari dari sebuah tanggal, dan
menghitung usia sekarang serta hari menuju ulang tahun berikut.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.
Format tanggal yang diterima: `YYYY-MM-DD` (contoh `2026-11-05`) atau
`DD/MM/YYYY` (contoh `05/11/2026`).

## Cara menjalankan

```bash
cd day-05
python3 tanggal.py
```

Jalankan tanpa argumen untuk mode interaktif dengan menu 1-4.

Menghitung selisih dua tanggal:

```bash
python3 tanggal.py selisih 2026-11-05 2026-12-25
```

Menggeser tanggal 30 hari ke depan, atau 10 hari kerja ke depan:

```bash
python3 tanggal.py tambah 2026-11-05 30
python3 tanggal.py tambah 2026-11-05 10 --kerja
```

Mencari nama hari dari tanggal:

```bash
python3 tanggal.py hari 2026-11-05
```

Menghitung menuju ulang tahun berikut (tanggal acuan bisa diubah
dengan `--hari-ini` agar hasilnya bisa diuji):

```bash
python3 tanggal.py ultah 2000-01-15
python3 tanggal.py ultah 2000-01-15 --hari-ini 2026-11-05
```

## Contoh keluaran

```text
$ python3 tanggal.py selisih 2026-11-05 2026-12-25
Dari  : Kamis, 5 November 2026
Ke    : Jumat, 25 Desember 2026
Jarak : 50 hari (ke depan)
Hari kerja (Senin-Jumat): 36 hari
Minggu: 7 minggu penuh + 1 hari

$ python3 tanggal.py hari 2026-11-05
Kamis, 5 November 2026
```

## Catatan

Hari kerja di sini berarti Senin sampai Jumat, tanpa memotong hari
libur nasional — tanggal merah tidak diperhitungkan. Ulang tahun
29 Februari dirayakan pada 28 Februari di tahun biasa.
