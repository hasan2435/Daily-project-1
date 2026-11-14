# Day 14 — Kuis Pengetahuan Umum

Proyek harian ke-14: kuis pilihan ganda Bahasa Indonesia di terminal.
Ada 5 kategori — pengetahuan umum, sains, sejarah, geografi, dan
olahraga — masing-masing 8 soal, total 40 soal. Soal dan urutan
pilihan jawaban diacak setiap permainan, tiap jawaban langsung
diberi penjelasan singkat, dan skor terbaik per kategori disimpan
supaya bisa dipecahkan di permainan berikutnya.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-14
python3 kuis.py
```

Jalankan tanpa argumen untuk mode interaktif: pilih kategori lewat
menu angka, tentukan jumlah soal, lalu jawab dengan huruf A-D
(ketik `q` untuk berhenti di tengah kuis).

Main langsung dari baris perintah:

```bash
python3 kuis.py --kategori sains --jumlah 5
python3 kuis.py --kategori campuran --jumlah 10
```

Kategori yang tersedia: `umum`, `sains`, `sejarah`, `geografi`,
`olahraga`, dan `campuran` (gabungan semua kategori, 40 soal).
Jumlah soal default 5; bila melebihi jumlah soal kategori,
program memakai semua soal yang ada.

Lihat daftar kategori dan skor terbaik yang tersimpan:

```bash
python3 kuis.py --daftar
python3 kuis.py skor
```

## Penilaian

Tiap jawaban benar bernilai 10 poin. Predikat berdasarkan
persentase jawaban benar:

- 100%: Sempurna!
- 80-99%: Sangat Baik
- 60-79%: Baik
- 40-59%: Cukup
- di bawah 40%: Perlu Belajar Lagi

Skor terbaik hanya diperbarui bila kuis diselesaikan sampai soal
terakhir; berhenti di tengah kuis tidak mengubah skor tersimpan.

## Data tersimpan

Skor terbaik disimpan di berkas `kuis.json` pada folder tempat
program dijalankan. Berkas data itu milik pengguna, bukan bagian
dari proyek, jadi jangan ikut diunggah ke repositori.
