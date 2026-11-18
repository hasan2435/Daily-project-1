# Day 18 — Kalkulator Cicilan Kredit

Proyek harian ke-18: kalkulator cicilan kredit (KPR, kredit kendaraan,
pinjaman pribadi) di terminal. Hitung cicilan bulanan tetap dengan
sistem anuitas (bunga efektif), lihat tabel amortisasi, simulasikan
pelunasan dipercepat dengan setoran ekstra, bandingkan dua penawaran
kredit, dan bandingkan bunga flat dengan anuitas.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-18
python3 cicilan.py
```

Jalankan tanpa argumen untuk mode interaktif: program menampilkan
menu angka, lalu menanyakan pokok pinjaman, bunga per tahun, tenor,
dan setoran tambahan bila perlu.

Langsung dari baris perintah:

```bash
python3 cicilan.py hitung 100000000 12 12
python3 cicilan.py tabel 100000000 12 12
python3 cicilan.py lunas 100000000 12 12 2000000
python3 cicilan.py banding 100000000 10 12 12 24
python3 cicilan.py flat 100000000 12 12
```

## Cara perhitungan

Cicilan anuitas dihitung dengan rumus:

```
r = bunga tahunan / 12 / 100
cicilan = pokok * r * (1 + r)^n / ((1 + r)^n - 1)
```

dengan `n` = tenor dalam bulan. Bila bunga 0%, cicilan = pokok / tenor.
Tiap bulan, bagian bunga = sisa pokok x r dan bagian pokok = cicilan
- bagian bunga; sisa pokok berkurang sampai Rp0 di bulan terakhir.

## Perintah

| Perintah | Fungsi |
| --- | --- |
| `hitung <pokok> <bunga> <tenor>` | Cicilan bulanan, total dibayar, dan total bunga. |
| `tabel <pokok> <bunga> <tenor>` | Tabel amortisasi per tahun; rincian per bulan bila tenor s.d. 24 bulan. |
| `lunas <pokok> <bunga> <tenor> <tambahan>` | Simulasi pelunasan dipercepat dengan setoran ekstra tiap bulan: berapa bulan lebih cepat lunas dan berapa bunga yang dihemat. |
| `banding <pokok> <bunga1> <tenor1> <bunga2> <tenor2>` | Bandingkan dua penawaran kredit berdasarkan cicilan, total bayar, dan total bunga. |
| `flat <pokok> <bunga> <tenor>` | Bandingkan bunga flat dengan anuitas pada bunga nominal yang sama. |

## Contoh

Pinjaman Rp100.000.000, bunga 12% per tahun, tenor 12 bulan:

- Cicilan: Rp8.884.879/bulan, total dibayar Rp106.618.546, total bunga Rp6.618.546.
- Tambah setoran Rp2.000.000/bulan: lunas dalam 10 bulan, hemat bunga Rp1.187.461.
- Bunga flat 12% untuk pinjaman yang sama: cicilan Rp9.333.333/bulan, total bunga Rp12.000.000 — lebih mahal dari anuitas karena bunga flat dihitung dari pokok awal setiap bulan.

Hasilnya perkiraan saja; suku bunga, biaya, dan ketentuan tiap
bank/leasing berbeda — cek penawaran resminya sebelum memutuskan.
