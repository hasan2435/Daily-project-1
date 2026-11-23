# Day 23 — Kalkulator Biaya Listrik

Program terminal untuk menghitung biaya pemakaian listrik per alat
dan perkiraan tagihan bulanan dari golongan tarif rumah tangga
PLN. Catat alat-alat di rumah — lampu, kulkas, AC, TV, dan
lain-lain — lalu lihat berapa kWh dan rupiah yang dihabiskan
tiap alat, dan berapa total tagihannya.

Rumus dasarnya: kWh = watt × jam nyala per hari × hari / 1000,
lalu biaya energi = kWh × tarif per kWh golongan yang dipilih.

Untuk pelanggan pascabayar berlaku rekening minimum: tagihan
paling sedikit 40 jam nyala × daya tersambung × tarif. Kalau
pemakaianmu di bawah itu, tagihan dihitung dari rekening
minimum. Pelanggan token (prabayar) tidak kena rekening
minimum — pakai opsi `--token`.

## Cara menjalankan

```bash
cd day-23
python3 listrik.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka).

## Perintah

```bash
# Lihat daftar golongan tarif rumah tangga PLN
python3 listrik.py golongan

# Hitung cepat satu alat tanpa menyimpan (default golongan 1300 VA)
python3 listrik.py hitung 100 8
python3 listrik.py hitung 350 24 --golongan 2200
python3 listrik.py hitung 800 8 --tarif 1500

# Tambah alat ke daftar (watt, jam nyala per hari)
python3 listrik.py tambah "Kulkas" 150 24
python3 listrik.py tambah "AC 1 PK" 800 8
python3 listrik.py tambah "Lampu teras" 20 12

# Lihat daftar alat beserta kWh dan biayanya
python3 listrik.py daftar
python3 listrik.py daftar --golongan 2200

# Hitung total tagihan bulanan dari semua alat
python3 listrik.py total
python3 listrik.py total --golongan 2200 --ppj 5
python3 listrik.py total --token

# Simulasi hemat: kurangi jam nyala satu alat
python3 listrik.py hemat 2 4

# Hapus satu alat
python3 listrik.py hapus 3 --ya
```

Contoh: kulkas 150 watt nyala 24 jam sehari menghabiskan
108 kWh/bulan — pada golongan 1300 VA (Rp1.444,70/kWh) biayanya
sekitar Rp156.028/bulan. AC 800 watt nyala 8 jam sehari
menghabiskan 192 kWh/bulan, sekitar Rp277.382/bulan; bila
dikurangi jadi 4 jam sehari, hemat sekitar Rp138.691/bulan.

## Penyimpanan data

Data disimpan di berkas `listrik.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek,
jadi jangan ikut diunggah ke repositori.

## Catatan

- Golongan tarif yang dipakai: R-1 450 VA Rp415/kWh, R-1 900 VA
  Rp1.352/kWh, R-1 1300 VA dan 2200 VA Rp1.444,70/kWh, R-2/R-3
  Rp1.699,53/kWh. Tarif mengikuti yang umum dipublikasikan dan
  bisa berubah — cek tagihan terakhirmu, atau pakai `--tarif`
  untuk tarif sendiri.
- PPJ (Pajak Penerangan Jalan) besarnya ditentukan pemerintah
  daerah, umumnya 3–10%. Default 0; isi lewat `--ppj`.
- Rekening minimum hanya untuk pascabayar. Token/prabayar tidak
  kena minimum, jadi pakai `--token` pada perintah `total`.
- Jam nyala 0–24 jam per hari; hari per bulan 1–31 (default 30).
- Python standar saja, tanpa library tambahan.
