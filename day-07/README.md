# Day 7 — Permainan Tebak Kata (Hangman)

Proyek harian ke-7: permainan tebak kata di terminal. Tebak kata Bahasa
Indonesia huruf demi huruf sebelum gambar orang-orangan selesai.
Ada 6 kategori kata (hewan, buah, kota, benda, makanan, profesi) dan
3 tingkat kesulitan yang mengatur panjang kata dan jumlah nyawa.

Menebak kata utuh yang benar langsung menang, tapi bila salah nyawa
berkurang 2. Skor dicatat per ronde, termasuk jumlah menang beruntun.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-07
python3 tebak.py
```

Jalankan tanpa argumen untuk mode interaktif (kategori dan kata dipilih
acak, kesulitan sedang).

Memilih kategori dan kesulitan:

```bash
python3 tebak.py --kategori hewan --kesulitan sulit
python3 tebak.py --kategori buah --kesulitan mudah
```

Mode dua pemain — satu orang memberi kata rahasia, teman yang menebak:

```bash
python3 tebak.py --kata kucing
```

Melihat daftar kategori:

```bash
python3 tebak.py --daftar
```

## Tingkat kesulitan

| Kesulitan | Panjang kata | Nyawa |
|-----------|--------------|-------|
| mudah     | 4–6 huruf    | 8     |
| sedang    | 7–9 huruf    | 6     |
| sulit     | 10+ huruf    | 4     |

Tekan Ctrl+C untuk berhenti kapan saja.
