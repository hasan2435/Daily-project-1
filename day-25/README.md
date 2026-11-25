# Day 25 — Pencatat Perawatan Kendaraan

Program terminal untuk mencatat kendaraan (motor atau mobil) beserta
riwayat perawatannya — ganti oli, ganti ban, servis rem, dan
lain-lain — lengkap dengan biaya, kilometer saat servis, dan jadwal
servis berikutnya. Program juga mengingatkan servis yang sudah
jatuh tempo dan pajak STNK tahunan yang sebentar lagi habis.

Aturan pengingat yang dipakai:

- Servis jatuh tempo bila kilometer berikutnya sudah tercapai, atau
  tanggal berikutnya sudah lewat.
- Servis dianggap segera bila kilometer berikutnya tinggal 500 km
  lagi, atau tanggal berikutnya tinggal 30 hari lagi.
- Pajak STNK diingatkan bila tinggal 30 hari lagi atau sudah lewat.

## Cara menjalankan

```bash
cd day-25
python3 kendaraan.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka).

## Perintah

```bash
# Tambah kendaraan (nama, jenis motor/mobil, plat, tahun)
python3 kendaraan.py tambah "Beat" motor "B 1234 ABC" 2020 --km 15000 --pajak 2027-03-15
python3 kendaraan.py tambah "Avanza" mobil "B 5678 DEF" 2019 --km 82000 --pajak 2027-01-10

# Lihat daftar kendaraan
python3 kendaraan.py daftar

# Catat servis (jenis servis, biaya; jadwal berikutnya opsional)
python3 kendaraan.py servis 1 "Ganti oli" 85000 --km 15500 --berikutnya-km 17500
python3 kendaraan.py servis 1 "Ganti ban belakang" 350000 --km 16000 --berikutnya-tanggal 2027-05-25
python3 kendaraan.py servis 2 "Tune up" 450000 --km 82500 --berikutnya-km 87500 --berikutnya-tanggal 2027-02-10

# Lihat riwayat servis satu kendaraan
python3 kendaraan.py riwayat 1

# Lihat pengingat servis dan pajak STNK
python3 kendaraan.py ingat

# Lihat total biaya servis (semua kendaraan, atau satu kendaraan)
python3 kendaraan.py total
python3 kendaraan.py total 1

# Perbarui tanggal pajak STNK tahunan
python3 kendaraan.py pajak 1 2027-03-15

# Perbarui kilometer kendaraan saat ini
python3 kendaraan.py km 1 16000

# Hapus satu kendaraan beserta riwayat servisnya
python3 kendaraan.py hapus 1 --ya
```

Contoh: motor Beat ganti oli Rp85.000 pada 15.500 km dengan servis
berikutnya di 17.500 km. Begitu kilometer motor mencapai 17.000 km,
perintah `ingat` sudah memberi peringatan "segera"; begitu mencapai
17.500 km, peringatannya berubah menjadi "jatuh tempo". Bila pajak
STNK jatuh tempo 15 Maret 2027, peringatan mulai muncul sejak
13 Februari 2027 (30 hari sebelumnya).

## Penyimpanan data

Data disimpan di berkas `kendaraan.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek,
jadi jangan ikut diunggah ke repositori.

## Catatan

- Kilometer kendaraan otomatis diperbarui bila kilometer saat servis
  lebih besar dari kilometer yang tercatat.
- Pengingat servis memakai jadwal dari servis terakhir yang dicatat;
  catat servis baru bila jadwalnya berubah.
- Pajak STNK yang dicatat adalah pajak tahunan. Pajak lima tahunan
  (ganti plat) tidak dihitung otomatis — catat tanggalnya sebagai
  servis dengan jenis "Ganti plat 5 tahunan" bila perlu diingatkan.
- Python standar saja, tanpa library tambahan.
