# Day 11 — Kalkulator Waktu Tidur

Proyek harian ke-11: program terminal untuk menghitung jam tidur dan
jam bangun yang ideal berdasarkan siklus tidur 90 menit. Satu siklus
tidur berlangsung sekitar 90 menit; orang dewasa umumnya butuh 5-6
siklus (7,5-9 jam) per malam. Program menghitung mundur dari jam
bangun yang diinginkan atau maju dari jam tidur, dengan
memperhitungkan waktu yang dibutuhkan untuk tertidur (default
15 menit).

Bangun di akhir siklus terasa lebih segar daripada terbangun di
tengah siklus, jadi saran yang diberikan selalu jatuh tepat di
ujung siklus.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-11
python3 tidur.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka: cari jam
tidur, cari jam bangun, tidur sekarang, hitung durasi).

Cari jam tidur dari jam bangun yang diinginkan:

```bash
python3 tidur.py bangun 06:00
python3 tidur.py bangun 06:30 --tertidur 20
```

Cari jam bangun dari jam tidur, atau dari sekarang:

```bash
python3 tidur.py tidur 23:00
python3 tidur.py sekarang
```

Hitung durasi tidur antara dua jam (melintasi tengah malam bila
perlu):

```bash
python3 tidur.py durasi 23:00 06:00
```

Opsi `--tertidur` mengatur waktu yang dibutuhkan untuk tertidur,
dalam menit (0-60, default 15). Jam ditulis dengan format JJ:MM,
contoh `06:00` atau `23:30`.

Ini panduan umum, bukan saran medis: kebutuhan tidur tiap orang
bisa berbeda, dan kualitas tidur sama pentingnya dengan lamanya.
