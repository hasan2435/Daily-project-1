# Day 21 — Permainan Sudoku di Terminal

Proyek harian ke-21: permainan Sudoku di terminal. Buat teka-teki
baru yang dijamin punya tepat satu solusi, mainkan langsung dengan
petunjuk dan batas kesalahan, atau selesaikan teka-teki dari luar.

```bash
cd day-21
python3 sudoku.py
python3 sudoku.py main --kesulitan sedang
python3 sudoku.py buat --kesulitan sulit
python3 sudoku.py buat --kesulitan mudah --solusi
python3 sudoku.py selesaikan 530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

Jalankan tanpa argumen untuk mode interaktif (menu angka).

## Fitur

- **Buat teka-teki** — papan 9x9 dibuat dengan backtracking acak,
  lalu sel dihapus satu per satu selama solusinya tetap unik.
- **Tiga tingkat kesulitan** — mudah (36 petunjuk), sedang (30
  petunjuk), sulit (25 petunjuk).
- **Main di terminal** — isi sel dengan `baris kolom angka`
  (contoh: `1 3 5`), hapus dengan `hapus 1 3`, tampilkan papan
  dengan `papan`.
- **Petunjuk** — isi satu sel kosong dengan jawaban benar, maksimal
  3 kali per permainan.
- **Cek isian** — periksa sel mana saja yang tidak cocok dengan
  solusi, tanpa mengisi jawabannya.
- **Batas kesalahan** — permainan berakhir setelah 3 kali salah
  isi, lalu solusinya ditampilkan.
- **Selesaikan teka-teki** — tempel string 81 karakter (angka 0-9,
  0 atau `.` untuk sel kosong) dan program mencari solusinya.
  Teka-teki tanpa solusi akan ditolak.

## Contoh permainan

```
    1 2 3   4 5 6   7 8 9
  +-------+-------+-------+
1 | 5 3 . | . 7 . | . . . |
2 | 6 . . | 1 9 5 | . . . |
3 | . 9 8 | . . . | . 6 . |
  +-------+-------+-------+
4 | 8 . . | . 6 . | . . 3 |
5 | 4 . . | 8 . 3 | . . 1 |
6 | 7 . . | . 2 . | . . 6 |
  +-------+-------+-------+
7 | . 6 . | . . . | 2 8 . |
8 | . . . | 4 1 9 | . . 5 |
9 | . . . | . 8 . | . 7 9 |
  +-------+-------+-------+

> 1 3 4
> cek
Sejauh ini semua isian benar. Lanjutkan!
```

## Catatan

- Petunjuk awal (angka tebal) tidak bisa diubah atau dihapus.
- Isian yang melanggar aturan baris, kolom, atau kotak 3x3 dihitung
  sebagai kesalahan dan ditandai `*`.
- Waktu bermain dihitung dari awal permainan sampai papan terisi penuh.
- Python standar saja, tanpa library tambahan.
