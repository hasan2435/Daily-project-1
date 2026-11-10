# Daily Project 1

Seri ini: satu proyek kecil baru setiap hari, bebas topik, yang penting konsisten upload.
Semua proyek memakai Python standar saja, tanpa library tambahan, dan bisa dijalankan di terminal/VSCode.

## Daftar proyek

- Day 1 — Pomodoro Timer: timer Pomodoro di terminal (`pomodoro.py`).
- Day 2 — Pencatat Pengeluaran Harian: catat pengeluaran dan lihat totalnya (`day-02/pengeluaran.py`).
- Day 3 — Penghitung Kata dan Waktu Baca: analisis teks, hitung kata dan perkiraan waktu baca (`day-03/kata.py`).
- Day 4 — Generator Kata Sandi Aman: buat kata sandi acak yang kuat dan nilai kekuatannya (`day-04/password.py`).
- Day 5 — Kalkulator Tanggal: selisih tanggal, geser hari, nama hari, dan hitung menuju ulang tahun (`day-05/tanggal.py`).
- Day 6 — Kalkulator Bunga Majemuk: simulasi tabungan dengan bunga majemuk, hitung nilai akhir, lama menuju target, dan setoran bulanan (`day-06/bunga.py`).
- Day 7 — Permainan Tebak Kata: tebak kata Bahasa Indonesia huruf demi huruf, 6 kategori dan 3 tingkat kesulitan (`day-07/tebak.py`).

- Day 8 — Konverter Satuan: ubah satuan panjang, berat, volume, suhu, waktu, kecepatan, dan data (`day-08/konversi.py`).

- Day 9 — Kalkulator BMI & Kalori Harian: hitung BMI, BMR, TDEE, dan target kalori harian (`day-09/bmi.py`).

- Day 10 — Pencatat Kebiasaan Harian: catat kebiasaan, centang harian, streak, dan ringkasan 7 hari terakhir (`day-10/kebiasaan.py`).

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

## Day 4 — Generator Kata Sandi Aman

Proyek harian ke-4: program terminal untuk membuat kata sandi acak
yang kuat (modul `secrets` dari pustaka standar Python) dan menilai
kekuatan kata sandi yang sudah ada dengan skor 0–100.

```bash
cd day-04
python3 password.py
python3 password.py --panjang 20 --jumlah 5
python3 password.py --nilai "KataSandi123!"
```

Secara default program membuat 1 kata sandi sepanjang 16 karakter.
Detail lengkap ada di `day-04/README.md`.

## Day 5 — Kalkulator Tanggal

Proyek harian ke-5: program terminal untuk menghitung selisih dua
tanggal (termasuk jumlah hari kerja Senin-Jumat), menggeser tanggal
maju/mundur sejumlah hari, mencari nama hari dari tanggal, dan
menghitung usia serta hari menuju ulang tahun berikut.

```bash
cd day-05
python3 tanggal.py
python3 tanggal.py selisih 2026-11-05 2026-12-25
python3 tanggal.py tambah 2026-11-05 10 --kerja
python3 tanggal.py hari 2026-11-05
python3 tanggal.py ultah 2000-01-15
```

Jalankan tanpa argumen untuk mode interaktif.
Detail lengkap ada di `day-05/README.md`.

## Day 6 — Kalkulator Bunga Majemuk

Proyek harian ke-6: program terminal untuk mensimulasikan pertumbuhan
tabungan dengan bunga majemuk dan setoran rutin bulanan: hitung nilai
akhir, lama menuju target dana, setoran bulanan yang dibutuhkan, dan
tabel pertumbuhan tahunan.

```bash
cd day-06
python3 bunga.py
python3 bunga.py tumbuh --pokok 1000000 --bunga 6 --tahun 5 --setoran 500000
python3 bunga.py target --pokok 1000000 --bunga 6 --setoran 500000 --target 50000000
python3 bunga.py setoran --pokok 1000000 --bunga 6 --tahun 5 --target 50000000
python3 bunga.py tabel --pokok 1000000 --bunga 6 --tahun 5 --setoran 500000
```

Jalankan tanpa argumen untuk mode interaktif. Bunga dihitung majemuk
per bulan, setoran masuk di akhir bulan.
Detail lengkap ada di `day-06/README.md`.

## Day 7 — Permainan Tebak Kata

Proyek harian ke-7: permainan tebak kata di terminal. Tebak kata Bahasa
Indonesia huruf demi huruf sebelum gambar orang-orangan selesai. Ada
6 kategori kata (hewan, buah, kota, benda, makanan, profesi) dan
3 tingkat kesulitan yang mengatur panjang kata dan jumlah nyawa.

```bash
cd day-07
python3 tebak.py
python3 tebak.py --kategori hewan --kesulitan sulit
python3 tebak.py --kata kucing
python3 tebak.py --daftar
```

Jalankan tanpa argumen untuk mode interaktif. Menebak kata utuh yang
salah mengurangi 2 nyawa. Detail lengkap ada di `day-07/README.md`.


## Day 8 — Konverter Satuan

Proyek harian ke-8: program terminal untuk mengubah satuan dalam 7
kategori: panjang, berat, volume, suhu, waktu, kecepatan, dan data.
Suhu dihitung lewat Celsius, termasuk Reamur; data memakai kelipatan
1024, dari bit sampai TB.

```bash
cd day-08
python3 konversi.py
python3 konversi.py panjang 5 km m
python3 konversi.py suhu 100 C F
python3 konversi.py berat 2.5 kg ons
python3 konversi.py data 1 GB MB
python3 konversi.py --daftar
```

Jalankan tanpa argumen untuk mode interaktif. Detail lengkap ada di
`day-08/README.md`.

## Day 9 — Kalkulator BMI & Kalori Harian

Proyek harian ke-9: program terminal untuk menghitung BMI beserta
kategorinya dan rentang berat badan ideal, lalu kebutuhan kalori:
BMR dengan rumus Mifflin-St Jeor, TDEE berdasarkan tingkat aktivitas,
dan target kalori untuk menurunkan, mempertahankan, atau menaikkan
berat badan sekitar 0,5 kg per minggu.

```bash
cd day-09
python3 bmi.py
python3 bmi.py bmi 70 170
python3 bmi.py kalori 70 170 30 pria sedang
python3 bmi.py kalori 55 160 25 wanita ringan --tujuan turun
python3 bmi.py --daftar
```

Jalankan tanpa argumen untuk mode interaktif. Detail lengkap ada di
`day-09/README.md`.

## Day 10 — Pencatat Kebiasaan Harian

Proyek harian ke-10: program terminal untuk mencatat kebiasaan yang
ingin dibangun setiap hari: tambah kebiasaan dengan target mingguan,
centang bila sudah dilakukan, dan pantau streak (rangkaian hari
beruntun) beserta ringkasan 7 hari terakhir.

```bash
cd day-10
python3 kebiasaan.py
python3 kebiasaan.py tambah "Olahraga pagi" --target 5
python3 kebiasaan.py centang "Olahraga pagi"
python3 kebiasaan.py daftar
python3 kebiasaan.py ringkasan
```

Jalankan tanpa argumen untuk mode interaktif. Data disimpan di
`kebiasaan.json` pada folder tempat program dijalankan; berkas data
itu milik pengguna, bukan bagian dari proyek. Detail lengkap ada di
`day-10/README.md`.
