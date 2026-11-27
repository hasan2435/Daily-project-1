# Day 27 — Permainan Ular Tangga

Proyek harian ke-27: permainan ular tangga di terminal untuk 2-4
pemain, manusia melawan manusia atau melawan komputer. Papan 10x10
berisi 7 tangga dan 7 ular; yang pertama mendarat tepat di kotak
100 menang.

Aturan mainnya: setiap pemain mulai dari luar papan (posisi 0) dan
bergiliran melempar dadu. Mendarat tepat di kaki tangga berarti naik
ke ujung tangga, mendarat tepat di kepala ular berarti turun ke ekor
ular. Melempar angka 6 mendapat giliran lempar lagi, tapi tiga kali
angka 6 berturut-turut membuat giliran hangus dan pemain kembali ke
posisi awal gilirannya. Lemparan yang melewati kotak 100 tidak
bergerak — harus mendarat tepat di 100.

Papan dicetak dengan arah bolak-balik seperti papan sungguhan: baris
bawah 1-10 dari kiri ke kanan, baris di atasnya 20-11 dari kanan ke
kiri, dan seterusnya. Tanda ▲ menandai kaki tangga, ▼ menandai kepala
ular, dan huruf awal nama menandai posisi tiap pemain.

Statistik kemenangan tiap nama pemain dan riwayat 20 permainan
terakhir disimpan otomatis, jadi bisa dilihat siapa yang paling
sering menang.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-27
python3 ular_tangga.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka): main baru,
demo komputer melawan komputer, lihat papan, statistik, riwayat, atau
daftar ular dan tangga.

Permainan baru dari baris perintah:

```bash
python3 ular_tangga.py main --pemain "Ani,Budi" --komputer 1
python3 ular_tangga.py main --pemain "Ani,Budi"
python3 ular_tangga.py main --komputer 2
```

Demo komputer melawan komputer (tanpa perlu menekan Enter):

```bash
python3 ular_tangga.py demo
python3 ular_tangga.py demo --pemain 3
```

Lihat papan, statistik, dan riwayat:

```bash
python3 ular_tangga.py papan
python3 ular_tangga.py statistik
python3 ular_tangga.py riwayat
python3 ular_tangga.py riwayat --jumlah 5
```

Lihat daftar semua ular dan tangga:

```bash
python3 ular_tangga.py --daftar
```

Hapus semua statistik dan riwayat:

```bash
python3 ular_tangga.py reset --ya
```

## Contoh keluaran

```text
=== Permainan Ular Tangga ===
Pemain: Ani, Komputer 1 (komputer)
Yang pertama mendarat tepat di kotak 100 menang.

Giliran Ani, tekan Enter untuk melempar dadu...
Ani melempar: ⚂ (3)
Ani: 0 -> 3
Komputer 1 melempar: ⚀ (1)
Komputer 1: 0 -> 1
...
Ani melempar: ⚁ (2)
Ani: 92 -> 94
Komputer 1 melempar: ⚃ (4)
Komputer 1: 94 -> 98
Ani melempar: ⚅ (6)
Dapat 6, lempar lagi!
Ani: 94 -> 100

🎉 Ani MENANG! Sampai di kotak 100 setelah 67 lemparan dadu.
```

Contoh statistik setelah beberapa kali bermain:

```text
=== Statistik Ular Tangga ===
Pemain                Main Menang  Win rate
--------------------------------------------
Ani                      5      3     60.0%
Komputer 1               5      2     40.0%
--------------------------------------------
Total permainan tercatat: 5 (total partisipasi pemain: 10)
```

Daftar tangga dan ular di papan:

| Tangga (naik) | Ular (turun) |
|--------------:|-------------:|
| 4 → 25        | 27 → 5       |
| 13 → 46       | 43 → 18      |
| 33 → 49       | 55 → 25      |
| 42 → 63       | 66 → 45      |
| 50 → 69       | 76 → 58      |
| 62 → 81       | 89 → 53      |
| 74 → 92       | 99 → 41      |

Jumlah pemain 2-4 orang. Nama pemain tidak boleh sama, dan huruf
pertamanya dipakai sebagai penanda posisi di papan. Statistik dan
riwayat disimpan di `ular_tangga.json` pada folder tempat program
dijalankan; berkas data itu milik pengguna, bukan bagian dari proyek.
