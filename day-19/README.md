# Day 19 — Kalkulator Zakat

Kalkulator zakat di terminal: zakat penghasilan, zakat mal, zakat emas,
zakat perak, dan zakat fitrah. Python standar saja, tanpa library tambahan.

## Cara menjalankan

```bash
cd day-19
python3 zakat.py
python3 zakat.py penghasilan 12000000
python3 zakat.py penghasilan 15000000 --harga-emas 1600000
python3 zakat.py mal 200000000
python3 zakat.py emas 100
python3 zakat.py perak 700
python3 zakat.py fitrah 4
python3 zakat.py fitrah 4 --harga-beras 16000
python3 zakat.py nisab
```

Jalankan tanpa argumen untuk mode interaktif (menu angka).

## Aturan yang dipakai

- Kadar zakat: **2,5%** dari penghasilan atau harta yang sudah wajib zakat.
- Nisab emas: **85 gram**; nisab perak: **595 gram** (haul 1 tahun Hijriah).
- Nisab penghasilan: setara 85 gram emas per tahun, dibagi 12 per bulan.
- Zakat fitrah: **2,5 kg beras per jiwa** (atau senilai uangnya).

## Harga default

Harga emas, perak, dan beras mengikuti harga pasar saat ini, jadi ubah
dengan opsi `--harga-emas`, `--harga-perak`, atau `--harga-beras`:

| Harga | Default |
| --- | --- |
| Emas | Rp1.500.000/gram |
| Perak | Rp15.000/gram |
| Beras | Rp15.000/kg |

## Contoh hasil

Dengan harga default (emas Rp1.500.000/gram):

- Nisab penghasilan: 85 gram x Rp1.500.000 / 12 = **Rp10.625.000/bulan**.
  Gaji Rp12.000.000 sudah mencapai nisab, zakatnya **Rp300.000/bulan**.
- Total harta Rp200.000.000 sudah di atas nisab Rp127.500.000,
  zakat malnya **Rp5.000.000**.
- Emas 100 gram (di atas nisab 85 gram) senilai Rp150.000.000,
  zakatnya **Rp3.750.000**.
- Perak 700 gram (di atas nisab 595 gram) senilai Rp10.500.000,
  zakatnya **Rp262.500**.
- Zakat fitrah 4 jiwa: 10 kg beras, senilai **Rp150.000**.

## Perintah

| Perintah | Keterangan |
| --- | --- |
| `penghasilan <gaji>` | Zakat penghasilan bulanan dari gaji |
| `mal <harta>` | Zakat mal dari total harta (haul 1 tahun) |
| `emas <gram>` | Zakat emas dari jumlah gram yang dimiliki |
| `perak <gram>` | Zakat perak dari jumlah gram yang dimiliki |
| `fitrah <jiwa>` | Zakat fitrah 2,5 kg beras per jiwa |
| `nisab` | Lihat nisab dari harga emas/perak saat ini |

Mode interaktif juga menerima akhiran `jt`/`juta` dan `rb`/`ribu`
pada angka, contoh: `10jt` sama dengan 10000000.

## Catatan

Perhitungan ini memakai pendapat umum (nisab emas 85 gram, kadar 2,5%).
Untuk penyaluran dan kepastian hukum zakat, tanyakan ke amil atau
lembaga zakat terpercaya di daerahmu.
