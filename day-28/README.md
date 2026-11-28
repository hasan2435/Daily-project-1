# Day 28 — Permainan Minesweeper di Terminal

Proyek harian ke-28: permainan Minesweeper di terminal. Buka kotak
satu per satu tanpa mengenai bom. Angka pada kotak yang terbuka
menunjukkan jumlah bom di delapan kotak sekitarnya; dari angka-angka
itulah letak bom bisa ditebak. Buka kotak kosong dan semua kotak
kosong di sekitarnya ikut terbuka otomatis.

Klik pertama selalu aman: bom baru dipasang setelah kotak pertama
dibuka, jadi tidak mungkin langsung kalah di langkah pertama.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-28
python3 minesweeper.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka): main baru,
demo komputer bermain sendiri, statistik, riwayat, atau daftar
tingkat kesulitan.

Permainan baru dari baris perintah:

```bash
python3 minesweeper.py main --kesulitan mudah
python3 minesweeper.py main --kesulitan sedang
python3 minesweeper.py main --kesulitan sulit --benih 42
```

Demo komputer bermain sendiri (langkah dipilih acak):

```bash
python3 minesweeper.py demo
python3 minesweeper.py demo --kesulitan mudah --benih 7
```

Lihat statistik dan riwayat:

```bash
python3 minesweeper.py statistik
python3 minesweeper.py riwayat
python3 minesweeper.py riwayat --jumlah 5
```

Lihat daftar tingkat kesulitan:

```bash
python3 minesweeper.py --daftar
```

Hapus semua statistik dan riwayat:

```bash
python3 minesweeper.py reset --ya
```

## Cara main

Di dalam permainan, ketik salah satu perintah ini lalu tekan Enter:

```text
buka 3 4    membuka kotak baris 3 kolom 4
tandai 3 4  memberi atau mencabut bendera di baris 3 kolom 4
keluar      berhenti bermain
```

Baris dan kolom dihitung mulai dari 1. Menang bila semua kotak yang
bukan bom sudah terbuka; kalah bila membuka kotak berisi bom.

Ada tiga tingkat kesulitan:

| Kesulitan | Papan  | Bom |
|-----------|--------|----:|
| mudah     | 9x9    |  10 |
| sedang    | 16x16  |  40 |
| sulit     | 16x30  |  99 |

## Contoh keluaran

```text
=== Minesweeper — mudah (9x9, 10 bom) ===
Perintah: buka <baris> <kolom> | tandai <baris> <kolom> | keluar
   1 2 3 4 5 6 7 8 9
1  . . . . . . . . .
2  . . . . . . . . .
3  . . . . . . . . .
4  . . . . . . . . .
5  . . . . . . . . .
6  . . . . . . . . .
7  . . . . . . . . .
8  . . . . . . . . .
9  . . . . . . . . .
Bom tersisa (perkiraan): 10  |  Terbuka: 0
> buka 5 5
   1 2 3 4 5 6 7 8 9
1  . . . . . . . . .
2  . . . . . . . . .
3  . . . . . . . . .
4  . . . . . . . . .
5  . . . . 2 . . . .
6  . . . . . . . . .
7  . . . . . . . . .
8  . . . . . . . . .
9  . . . . . . . . .
Bom tersisa (perkiraan): 10  |  Terbuka: 1
```

Contoh statistik setelah beberapa kali bermain:

```text
=== Statistik Minesweeper ===
Kesulitan   Main Menang  Win rate  Terbaik
----------------------------------------------
mudah          4      1     25.0%    01:12
sedang         2      0      0.0%        -
sulit          0      0      0.0%        -
----------------------------------------------
Total: 6 permainan, 1 menang (16.7%).
```

Simbol di papan: `.` kotak tertutup, `F` bendera, spasi kosong
untuk kotak terbuka tanpa bom di sekitarnya, angka untuk jumlah
bom tetangga, dan `*` untuk bom saat papan dibuka semua setelah
permainan selesai. Opsi `--benih` mengulang papan yang sama, cocok
untuk menantang teman dengan papan yang identik. Statistik (main,
menang, win rate, dan waktu terbaik per tingkat kesulitan) serta
riwayat 20 permainan terakhir disimpan di `minesweeper.json` pada
folder tempat program dijalankan; berkas data itu milik pengguna,
bukan bagian dari proyek.
