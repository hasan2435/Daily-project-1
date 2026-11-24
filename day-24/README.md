# Day 24 — Kalkulator HPP & Harga Jual

Program terminal untuk menghitung harga pokok produksi (HPP) per
unit bagi usaha kecil — misalnya jualan kopi, makanan, atau
kerajinan — lalu menentukan harga jual dari margin keuntungan
yang diinginkan, titik impas (BEP), dan perkiraan laba bulanan.

Rumus yang dipakai:

- HPP per unit = bahan baku + tenaga kerja + overhead per unit
- Harga jual = HPP × (1 + margin / 100)
- BEP (unit) = biaya tetap bulanan / (harga jual − HPP per unit)
- BEP (rupiah) = BEP unit × harga jual
- Laba bulanan = (harga jual − HPP) × unit terjual − biaya tetap

Biaya tetap adalah biaya yang keluar tiap bulan walau tidak ada
yang terjual: sewa tempat, gaji tetap, listrik, dan lain-lain.
Biaya variabel (bahan, tenaga kerja per unit, overhead per unit)
hanya keluar bila ada produksi.

## Cara menjalankan

```bash
cd day-24
python3 hpp.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka).

## Perintah

```bash
# Hitung cepat tanpa menyimpan (bahan, tenaga, overhead per unit)
python3 hpp.py cepat 5000 2000 1000
python3 hpp.py cepat 5000 2000 1000 --margin 40

# Tambah produk (bahan, tenaga, overhead per unit; biaya tetap dan target bulanan)
python3 hpp.py tambah "Kopi Gula Aren" 5000 2000 1000 --tetap 1500000 --target 300
python3 hpp.py tambah "Brownies" 8000 1500 500 --tetap 1000000 --target 200

# Lihat daftar produk beserta HPP dan harga jual saran (margin 30%)
python3 hpp.py daftar

# Hitung HPP dan harga jual satu produk
python3 hpp.py hpp 1
python3 hpp.py hpp 1 --margin 40
python3 hpp.py hpp 1 --harga 15000

# Hitung margin dari harga jual yang sudah ditentukan
python3 hpp.py jual 1 15000

# Hitung titik impas (BEP) produk
python3 hpp.py bep 1
python3 hpp.py bep 1 --harga 15000

# Hitung laba bulanan pada sejumlah unit terjual
python3 hpp.py laba 1 300
python3 hpp.py laba 1 300 --harga 15000

# Bandingkan dua harga jual: margin, laba, dan BEP tiap harga
python3 hpp.py banding 1 12000 15000 --unit 300

# Hapus satu produk
python3 hpp.py hapus 1 --ya
```

Contoh: Kopi Gula Aren dengan bahan Rp5.000, tenaga kerja
Rp2.000, dan overhead Rp1.000 per gelas punya HPP Rp8.000.
Dengan margin 30%, harga jualnya Rp10.400 dan keuntungan
Rp2.400 per gelas. Bila biaya tetap Rp1.500.000/bulan, BEP-nya
625 gelas/bulan — jadi dengan target 300 gelas/bulan masih rugi
Rp780.000/bulan. Naikkan harga ke Rp15.000 (margin 87,5%),
BEP turun jadi 215 gelas/bulan dan laba pada target 300 gelas
menjadi Rp600.000/bulan.

## Penyimpanan data

Data disimpan di berkas `hpp.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek,
jadi jangan ikut diunggah ke repositori.

## Catatan

- Margin default 30% bila tidak diisi lewat `--margin` atau
  `--harga`.
- BEP dihitung dengan pembulatan ke atas ke unit utuh: unit
  ke-(BEP+1) dan seterusnya adalah keuntungan.
- Bila harga jual tidak lebih besar dari HPP, BEP tidak ada —
  usaha tidak akan pernah impas pada harga itu.
- Perbandingan dua harga memakai volume jual yang sama; harga
  lebih tinggi bisa menurunkan volume jual di dunia nyata.
- Python standar saja, tanpa library tambahan.
