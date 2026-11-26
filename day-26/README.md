# Day 26 — Permainan Batu Gunting Kertas

Proyek harian ke-26: permainan batu gunting kertas melawan komputer
di terminal. Pilih batu, gunting, atau kertas; komputer memilih secara
acak. Aturan klasiknya: batu mengalahkan gunting, gunting mengalahkan
kertas, kertas mengalahkan batu, dan pilihan yang sama berarti seri.

Ada tiga cara bermain: pertandingan best of 3/5/7 (yang pertama
mencapai target kemenangan menjadi juara, ronde seri tidak dihitung),
ronde cepat satu kali main, dan mode tanpa batas sampai memilih
berhenti. Statistik permainan — total ronde, menang, kalah, seri,
win rate, streak menang, dan pilihan yang paling sering dipakai —
disimpan otomatis, begitu juga riwayat 50 pertandingan terakhir.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-26
python3 suit.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka): pertandingan
best of 5 atau best of 3, ronde cepat, mode tanpa batas, statistik,
atau riwayat.

Pertandingan best of 5 dari baris perintah:

```bash
python3 suit.py main --ronde 5
python3 suit.py main --ronde 3
```

Satu ronde cepat:

```bash
python3 suit.py cepat batu
python3 suit.py cepat gunting
python3 suit.py cepat kertas
```

Statistik dan riwayat:

```bash
python3 suit.py statistik
python3 suit.py riwayat
python3 suit.py riwayat --jumlah 5
```

Lihat aturan permainan:

```bash
python3 suit.py --daftar
```

Hapus semua statistik dan riwayat:

```bash
python3 suit.py reset --ya
```

## Contoh keluaran

```text
=== Pertandingan Best of 5 ===
Yang pertama menang 3 ronde menjadi juara.
Ketik 'keluar' untuk berhenti di tengah pertandingan.

--- Ronde 1 ---
Skor: Kamu 0 - 0 Komputer
Pilihanmu (batu/gunting/kertas, atau 'keluar'): gunting

Kamu     : ✌️ gunting
Komputer : ✋ kertas
Hasil    : Kamu menang!
Gunting memotong kertas.
Bagus! Komputer tidak menyangka.
Skor: Kamu 1 - 0 Komputer
```

Contoh statistik setelah beberapa kali bermain:

```text
=== Statistik Batu Gunting Kertas ===
Total ronde : 12
Menang      : 7
Kalah       : 4
Seri        : 1
Win rate    : 63.6% (dari 11 ronde yang diputuskan)
Streak menang saat ini : 2
Streak menang terbaik  : 3

Pilihan yang kamu pakai:
  ✊ batu       5x (41.7%) ████████
  ✌️ gunting    4x (33.3%) ███████
  ✋ kertas     3x (25.0%) █████

Pilihan favoritmu: batu.
```

Jumlah ronde pertandingan harus bilangan ganjil (3, 5, 7, dan
seterusnya). Statistik dan riwayat disimpan di `suit.json` pada folder
tempat program dijalankan; berkas data itu milik pengguna, bukan bagian
dari proyek.
