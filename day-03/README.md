# Day 3 — Penghitung Kata dan Waktu Baca

Proyek harian ke-3: program terminal untuk menganalisis sebuah teks.
Program menghitung jumlah karakter, kata, kalimat, dan paragraf,
rata-rata panjang kata, perkiraan waktu baca, serta 10 kata yang
paling sering muncul (kata umum bahasa Indonesia dikecualikan dari
daftar teratas supaya hasilnya lebih bermakna).

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-03
python3 kata.py
```

Jalankan tanpa argumen untuk mode interaktif: tempel atau ketik teks,
lalu tekan Enter pada baris kosong untuk selesai.

Menganalisis berkas teks:

```bash
python3 kata.py artikel.txt
```

Menganalisis teks langsung dari baris perintah:

```bash
python3 kata.py --teks "Belajar setiap hari, sedikit demi sedikit, tapi konsisten."
```

## Contoh keluaran

```text
=== Hasil Analisis Teks ===
Karakter            : 58
Karakter (tanpa spasi): 51
Kata                : 8
Kalimat             : 1
Paragraf            : 1
Rata-rata panjang kata: 6.0 huruf
Perkiraan waktu baca: 0 menit 2 detik (kecepatan 200 kata/menit)

10 kata paling sering muncul (kata umum dikecualikan):
  - sedikit: 2x
  - belajar: 1x
  - setiap: 1x
  - hari: 1x
  - demi: 1x
  - tapi: 1x
  - konsisten: 1x
```

Perkiraan waktu baca memakai kecepatan 200 kata per menit.
