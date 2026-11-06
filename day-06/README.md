# Day 6 — Kalkulator Bunga Majemuk & Simulasi Tabungan

Proyek harian ke-6: program terminal untuk mensimulasikan pertumbuhan
tabungan dengan bunga majemuk (bunga berbunga) dan setoran rutin bulanan.
Program bisa menghitung nilai akhir tabungan, berapa lama sampai dana
mencapai target, setoran bulanan yang dibutuhkan untuk mencapai target
dalam jangka waktu tertentu, serta tabel pertumbuhan tahunan.

Bunga dihitung majemuk per bulan (bunga tahunan dibagi 12), dan setoran
bulanan dihitung masuk di akhir bulan.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-06
python3 bunga.py
```

Jalankan tanpa argumen untuk mode interaktif dengan menu 1-4.

Menghitung nilai akhir tabungan:

```bash
python3 bunga.py tumbuh --pokok 1000000 --bunga 6 --tahun 5 --setoran 500000
```

Menghitung lama menuju target dana:

```bash
python3 bunga.py target --pokok 1000000 --bunga 6 --setoran 500000 --target 50000000
```

Menghitung setoran bulanan yang dibutuhkan:

```bash
python3 bunga.py setoran --pokok 1000000 --bunga 6 --tahun 5 --target 50000000
```

Menampilkan tabel pertumbuhan tahunan:

```bash
python3 bunga.py tabel --pokok 1000000 --bunga 6 --tahun 5 --setoran 500000
```

Angka uang boleh ditulis polos (`1000000`) atau memakai pemisah ribuan
(`1.000.000`). Bunga ditulis dalam persen per tahun, contoh: `6`
berarti 6% per tahun.

## Contoh keluaran

```text
$ python3 bunga.py tumbuh --pokok 1000000 --bunga 6 --tahun 5 --setoran 500000
=== Hasil Simulasi ===
Pokok awal     : Rp1.000.000
Setoran/bulan  : Rp500.000
Bunga          : 6% per tahun (majemuk bulanan)
Jangka waktu   : 5 tahun
Total disetor  : Rp31.000.000
Total bunga    : Rp5.233.865
Nilai akhir    : Rp36.233.865
Pertumbuhan    : 16.9% dari total setoran

$ python3 bunga.py target --pokok 1000000 --bunga 6 --setoran 500000 --target 50000000
=== Waktu Menuju Target ===
Pokok awal     : Rp1.000.000
Setoran/bulan  : Rp500.000
Bunga          : 6% per tahun (majemuk bulanan)
Target         : Rp50.000.000
Waktu          : 6 tahun 7 bulan (6.6 tahun)

$ python3 bunga.py setoran --pokok 1000000 --bunga 6 --tahun 5 --target 50000000
Setoran/bulan yang dibutuhkan: Rp697.307
untuk mencapai Rp50.000.000 dalam 5 tahun
dari pokok Rp1.000.000 dengan bunga 6% per tahun.
```

## Rumus yang dipakai

Dengan `r` = bunga tahunan / 100 / 12 (suku bunga bulanan) dan
`n` = jangka waktu dalam bulan:

- Nilai akhir = pokok x (1+r)^n + setoran x ((1+r)^n - 1) / r
- Bila bunga 0%, nilai akhir = pokok + setoran x n (tanpa bunga).

## Catatan

Hasil simulasi memakai asumsi bunga tetap selama jangka waktu dan
setoran masuk di akhir bulan. Bunga tabungan atau deposito asli bisa
berubah sewaktu-waktu, dan hasil di sini bukan janji keuntungan.
