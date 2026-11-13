# Day 13 — Kalkulator IPK & Nilai Kuliah

Proyek harian ke-13: program terminal untuk menghitung Indeks Prestasi
Kumulatif (IPK) dari mata kuliah yang diambil. Tiap mata kuliah punya
jumlah SKS dan nilai — bisa huruf (A sampai E) atau angka 0-100 yang
otomatis dikonversi ke huruf. IPK dihitung tertimbang SKS, lengkap
dengan predikat kelulusan dan perhitungan IPK semester depan yang
dibutuhkan untuk mencapai target IPK kumulatif.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-13
python3 ipk.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka: tambah mata
kuliah, lihat daftar & IPK, hapus, hitung target IPK, lihat skala
nilai).

Tambah mata kuliah (nilai huruf atau angka):

```bash
python3 ipk.py tambah "Matematika Diskrit" 3 A
python3 ipk.py tambah "Fisika Dasar" 2 85
```

Menambah mata kuliah dengan nama yang sama akan memperbarui SKS dan
nilainya.

Lihat daftar mata kuliah dan IPK:

```bash
python3 ipk.py daftar
python3 ipk.py ipk
```

Hapus mata kuliah:

```bash
python3 ipk.py hapus "Fisika Dasar"
```

Hitung IPK semester depan yang dibutuhkan untuk mencapai target IPK
kumulatif (dipakai data mata kuliah yang tersimpan):

```bash
python3 ipk.py target 3.5 20
```

Artinya: dengan 20 SKS semester depan, berapa IPK semester yang
dibutuhkan supaya IPK kumulatif menjadi 3.5. Bila belum ada data
tersimpan, isi SKS dan IPK saat ini secara manual:

```bash
python3 ipk.py target 3.5 20 --sks-saat-ini 40 --ipk 3.2
```

Konversi satu nilai angka ke huruf, dan lihat skala nilai:

```bash
python3 ipk.py konversi 82
python3 ipk.py skala
```

## Skala nilai

Skala yang dipakai program (angka -> huruf, bobot):

- A: 85-100, bobot 4.0
- AB: 80-84, bobot 3.5
- B: 75-79, bobot 3.0
- BC: 70-74, bobot 2.5
- C: 60-69, bobot 2.0
- D: 50-59, bobot 1.0
- E: 0-49, bobot 0.0

Skala tiap kampus bisa berbeda — cek aturan kampusmu bila skalanya
tidak sama.

## Predikat kelulusan

- IPK >= 3.50: Dengan Pujian (Cumlaude)
- IPK 3.00-3.49: Sangat Memuaskan
- IPK 2.75-2.99: Memuaskan
- IPK 2.00-2.74: Cukup
- IPK < 2.00: Kurang

## Data tersimpan

Data mata kuliah disimpan di berkas `ipk.json` pada folder tempat
program dijalankan. Berkas data itu milik pengguna, bukan bagian dari
proyek, jadi jangan ikut diunggah ke repositori.
