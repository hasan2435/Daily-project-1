# Day 9 — Kalkulator BMI & Kalori Harian

Proyek harian ke-9: program terminal untuk menghitung Indeks Massa
Tubuh (BMI) beserta kategorinya dan rentang berat badan ideal, lalu
melanjutkan ke kebutuhan kalori: BMR dengan rumus Mifflin-St Jeor,
total kebutuhan kalori harian (TDEE) berdasarkan tingkat aktivitas,
dan target kalori untuk menurunkan, mempertahankan, atau menaikkan
berat badan sekitar 0,5 kg per minggu.

Kategori BMI mengikuti standar WHO, dengan catatan bahwa untuk
populasi Asia risiko kesehatan mulai naik sejak BMI 23. Target turun
berat badan dibatasi ke batas aman umum (1.200 kkal/hari untuk
wanita, 1.500 kkal/hari untuk pria) bila hasil hitungnya lebih rendah.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-09
python3 bmi.py
```

Jalankan tanpa argumen untuk mode interaktif (dipandu langkah demi
langkah: berat, tinggi, lalu pilihan menghitung kalori juga).

Hitung BMI saja:

```bash
python3 bmi.py bmi 70 170
```

Hitung kebutuhan kalori lengkap:

```bash
python3 bmi.py kalori 70 170 30 pria sedang
python3 bmi.py kalori 55 160 25 wanita ringan --tujuan turun
```

Melihat daftar kategori BMI dan tingkat aktivitas:

```bash
python3 bmi.py --daftar
```

Tingkat aktivitas yang tersedia: `sangat-ringan`, `ringan`, `sedang`,
`aktif`, `sangat-aktif` (atau nomor 1-5). Jenis kelamin ditulis
`pria` atau `wanita`.

Hasil program ini adalah perkiraan untuk orang dewasa sehat, bukan
diagnosis medis. Konsultasikan ke dokter atau ahli gizi untuk rencana
yang personal, terutama bila ada kondisi kesehatan tertentu.
