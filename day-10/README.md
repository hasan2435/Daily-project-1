# Day 10 — Pencatat Kebiasaan Harian

Proyek harian ke-10: program terminal untuk mencatat kebiasaan yang
ingin dibangun setiap hari. Tambah kebiasaan dengan target mingguan
(1-7 hari), centang bila sudah dilakukan, dan pantau rangkaian hari
beruntun (streak) beserta ringkasan 7 hari terakhir.

Streak dihitung dari hari ini mundur; bila kebiasaan belum dicentang
hari ini, streak dihitung dari kemarin, supaya satu hari yang belum
dicentang tidak langsung memutus rangkaian yang sedang berjalan.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-10
python3 kebiasaan.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka: tambah,
centang, batalkan, daftar, ringkasan, hapus).

Tambah kebiasaan dan centang:

```bash
python3 kebiasaan.py tambah "Olahraga pagi" --target 5
python3 kebiasaan.py centang "Olahraga pagi"
python3 kebiasaan.py centang "Olahraga pagi" --tanggal 2026-11-09
```

Lihat daftar dan ringkasan:

```bash
python3 kebiasaan.py daftar
python3 kebiasaan.py ringkasan
```

Membatalkan centang dan menghapus kebiasaan:

```bash
python3 kebiasaan.py batal "Olahraga pagi"
python3 kebiasaan.py hapus "Olahraga pagi"
```

Nama kebiasaan tidak membedakan huruf besar dan kecil, jadi
`"olahraga pagi"` dianggap sama dengan `"Olahraga pagi"`. Target
mingguan 7 berarti setiap hari; isi 5 kalau mau libur dua hari
seminggu.

Data disimpan di berkas `kebiasaan.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek,
jadi jangan ikut diunggah ke repositori.
