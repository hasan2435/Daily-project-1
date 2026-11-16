# Day 16 — Pencatat Buku Bacaan

Proyek harian ke-16: pencatat buku bacaan di terminal. Tambah buku
dengan judul, penulis, total halaman, dan genre; catat halaman yang
sudah dibaca setiap hari; pantau progres tiap buku dengan bar progres;
tandai buku selesai; dan lihat statistik bacaan — total buku, halaman
yang sudah dibaca, rata-rata halaman buku selesai, dan genre terbanyak.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-16
python3 buku.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka).

Langsung dari baris perintah:

```bash
python3 buku.py tambah "Laskar Pelangi" "Andrea Hirata" 529 --genre novel
python3 buku.py tambah "Sapiens" "Yuval Noah Harari" 512 --genre sejarah
python3 buku.py baca 1 120
python3 buku.py daftar
python3 buku.py daftar --status aktif
python3 buku.py daftar --genre novel
python3 buku.py selesai 1
python3 buku.py statistik
python3 buku.py hapus 2 --ya
```

## Progres dan penyelesaian

Perintah `baca` menambah jumlah halaman yang dibaca ke buku
bersangkutan. Begitu halaman yang dibaca mencapai total halaman, buku
otomatis ditandai selesai beserta tanggal penyelesaiannya. Perintah
`selesai` juga bisa dipakai untuk menandai buku selesai secara manual.

Daftar buku diurutkan dengan buku yang belum selesai dulu, lalu
progres tertinggi. Bar progres menunjukkan persentase halaman yang
sudah dibaca, misal `[#####---------------] 23%`.

## Perintah

| Perintah | Fungsi |
| --- | --- |
| `tambah "Judul" "Penulis" <total>` | Tambah buku baru (`--genre`, `--catatan`). |
| `baca <id> <halaman>` | Catat halaman yang baru dibaca; selesai otomatis bila mencapai total. |
| `daftar` | Lihat semua buku (`--status aktif/selesai/semua`, `--genre`). |
| `selesai <id>` | Tandai buku selesai dibaca. |
| `statistik` | Total buku, halaman dibaca, rata-rata buku selesai, genre terbanyak. |
| `hapus <id>` | Hapus buku (`--ya` tanpa konfirmasi). |

## Data tersimpan

Buku disimpan di berkas `buku.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek,
jadi jangan ikut diunggah ke repositori.
