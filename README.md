# Daily Project 1

Seri ini: satu proyek kecil baru setiap hari, bebas topik, yang penting konsisten upload.
Semua proyek memakai Python standar saja, tanpa library tambahan, dan bisa dijalankan di terminal/VSCode.

## Daftar proyek

- Day 1 — Pomodoro Timer: timer Pomodoro di terminal (`pomodoro.py`).
- Day 2 — Pencatat Pengeluaran Harian: catat pengeluaran dan lihat totalnya (`day-02/pengeluaran.py`).
- Day 3 — Penghitung Kata dan Waktu Baca: analisis teks, hitung kata dan perkiraan waktu baca (`day-03/kata.py`).

## Day 1 — Pomodoro Timer

Proyek harian ke-1: timer Pomodoro di terminal.

```bash
python3 pomodoro.py
python3 pomodoro.py 15 3
```

Default: 25 menit fokus, 5 menit istirahat, 4 putaran.
Tekan Ctrl+C untuk berhenti.

## Day 2 — Pencatat Pengeluaran Harian

Proyek harian ke-2: program terminal untuk mencatat pengeluaran dan melihat totalnya, baik total keseluruhan maupun per kategori.

```bash
cd day-02
python3 pengeluaran.py
python3 pengeluaran.py tambah 50000 makan "Makan siang"
python3 pengeluaran.py daftar
python3 pengeluaran.py total
```

Data disimpan di berkas `pengeluaran.json` pada folder tempat program dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek, jadi jangan ikut diunggah ke repositori.
Detail lengkap ada di `day-02/README.md`.

## Day 3 — Penghitung Kata dan Waktu Baca

Proyek harian ke-3: program terminal untuk menganalisis sebuah teks:
jumlah karakter, kata, kalimat, dan paragraf, rata-rata panjang kata,
perkiraan waktu baca (200 kata/menit), serta 10 kata paling sering muncul.

```bash
cd day-03
python3 kata.py
python3 kata.py artikel.txt
python3 kata.py --teks "Belajar setiap hari, sedikit demi sedikit, tapi konsisten."
```

Jalankan tanpa argumen untuk mode interaktif.
Detail lengkap ada di `day-03/README.md`.
