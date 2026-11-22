# Day 22 — Pencatat Utang & Piutang

Program terminal untuk mencatat utang dan piutang per orang: siapa,
berapa sisanya, dan kapan jatuh temponya. Pembayaran bisa dicicil —
tiap pembayaran mengurangi sisa dan tersimpan riwayatnya. Kalau sisa
sudah nol, catatan otomatis lunas.

Dua jenis catatan:

- **utang** — kita berutang ke orang lain (kita yang harus bayar).
- **piutang** — orang lain berutang ke kita (kita yang menagih).

## Cara menjalankan

```bash
cd day-22
python3 utang.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka).

## Perintah

```bash
# Tambah catatan (jatuh tempo opsional, format YYYY-MM-DD)
python3 utang.py tambah utang Budi 500000 --jatuh-tempo 2026-12-22
python3 utang.py tambah piutang Ani 250000 --catatan "Talang tiket"

# Lihat daftar (default: yang masih aktif)
python3 utang.py daftar
python3 utang.py daftar --jenis piutang --status aktif
python3 utang.py daftar --status semua
python3 utang.py daftar --nama Budi

# Bayar utang, atau terima pembayaran piutang (bisa dicicil)
python3 utang.py bayar 1 200000

# Ringkasan: total utang, total piutang, posisi bersih, per orang
python3 utang.py total

# Cek yang sudah lewat atau akan jatuh tempo (default 7 hari ke depan)
python3 utang.py jatuh-tempo
python3 utang.py jatuh-tempo --hari 30

# Lihat detail satu catatan beserta riwayat pembayarannya
python3 utang.py detail 1

# Hapus satu catatan
python3 utang.py hapus 2 --ya
```

Contoh: utang ke Budi Rp500.000, dibayar Rp200.000, sisanya
Rp300.000. Posisi bersih = total piutang aktif dikurangi total
utang aktif; positif berarti lebih banyak orang berutang ke kita.

## Penyimpanan data

Data disimpan di berkas `utang.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek,
jadi jangan ikut diunggah ke repositori.

## Catatan

- Jumlah harus lebih dari nol; pembayaran tidak boleh melebihi sisa.
- Tanggal memakai format `YYYY-MM-DD`.
- Catatan yang sudah lunas tidak muncul di daftar aktif, tapi tetap
  bisa dilihat dengan `--status lunas` atau `--status semua`.
- Python standar saja, tanpa library tambahan.
