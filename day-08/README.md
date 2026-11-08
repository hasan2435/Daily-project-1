# Day 8 — Konverter Satuan

Proyek harian ke-8: program terminal untuk mengubah satuan dalam 7
kategori: panjang, berat, volume, suhu, waktu, kecepatan, dan data.
Suhu dihitung lewat Celsius karena melibatkan pergeseran nol, bukan
sekadar perkalian — termasuk Reamur yang masih dipakai di Indonesia.

Satuan yang tersedia antara lain km, mil, dan inci (panjang); kg, ons
metrik (1 ons = 100 gram), dan pon (berat); galon, sendok teh, dan
gelas (volume); knot dan mph (kecepatan); serta KB sampai TB dengan
kelipatan 1024 (data).

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-08
python3 konversi.py
```

Jalankan tanpa argumen untuk mode interaktif (pilih kategori, lalu
konversi berulang kali sampai mengetik `keluar`).

Mode perintah langsung:

```bash
python3 konversi.py panjang 5 km m
python3 konversi.py suhu 100 C F
python3 konversi.py berat 2.5 kg ons
python3 konversi.py data 1 GB MB
python3 konversi.py kecepatan 60 km/jam m/detik
```

Melihat daftar kategori dan satuan:

```bash
python3 konversi.py --daftar
python3 konversi.py --kategori suhu
python3 konversi.py --kategori panjang
```

Nilai negatif ditolak untuk semua kategori kecuali suhu, dan suhu
Kelvin tidak boleh di bawah 0. Tekan Ctrl+C untuk berhenti kapan saja.
