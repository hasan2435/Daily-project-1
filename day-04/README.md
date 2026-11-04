# Day 4 — Generator Kata Sandi Aman

Proyek harian ke-4: program terminal untuk membuat kata sandi acak
yang kuat dan menilai kekuatan kata sandi yang sudah ada.
Kata sandi dibuat dengan modul `secrets` dari pustaka standar Python,
yang dirancang untuk keperluan kriptografi.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-04
python3 password.py
```

Secara default program membuat 1 kata sandi sepanjang 16 karakter,
lengkap dengan skor dan label kekuatannya.

Membuat kata sandi dengan panjang dan jumlah tertentu:

```bash
python3 password.py --panjang 20 --jumlah 5
```

Membuat kata sandi tanpa simbol dan tanpa karakter yang mudah tertukar:

```bash
python3 password.py --tanpa-simbol --tanpa-ambigu
```

Menilai kekuatan kata sandi yang sudah ada:

```bash
python3 password.py --nilai "KataSandi123!"
```

## Penilaian kekuatan

Skor 0–100 dihitung dari tiga hal:

- Panjang (sampai 40 poin): 2 poin per karakter sampai 20 karakter.
- Keragaman karakter (sampai 40 poin): 10 poin untuk tiap kelompok
  yang dipakai — huruf kecil, huruf besar, angka, dan simbol.
- Keunikan (sampai 20 poin): proporsi karakter yang berbeda di dalam
  kata sandi.

Labelnya: di bawah 40 = Lemah, 40–59 = Sedang, 60–79 = Kuat,
80 ke atas = Sangat Kuat.

## Contoh keluaran

```text
$ python3 password.py --panjang 16 --jumlah 2
aB3$kQ9!xZ2#mN7p  (92/100, Sangat Kuat)
tR8&vL1@pW4#sD6q  (92/100, Sangat Kuat)

$ python3 password.py --nilai "rahasia"
Kata sandi : rahasia
Panjang    : 7 karakter
Skor       : 38/100 (Lemah)
```

## Catatan keamanan

Jangan memakai kata sandi hasil program ini untuk akun yang sudah
memakai kata sandi itu sebelumnya, dan jangan membagikan kata sandi
ke orang lain. Program ini tidak menyimpan kata sandi ke berkas apa pun.
