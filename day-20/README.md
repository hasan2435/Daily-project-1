# Day 20 — Kalkulator Diskon & Promo Belanja

Proyek harian ke-20: program terminal untuk menghitung harga akhir
belanja — diskon persen tunggal, diskon bertingkat, potongan nominal,
total bayar dengan PPN dan cashback, sampai membandingkan dua promo.

```bash
cd day-20
python3 diskon.py
python3 diskon.py diskon 250000 30
python3 diskon.py bertingkat 250000 50 20
python3 diskon.py potong 250000 50000
python3 diskon.py total 250000 --diskon 30 --ppn 11 --cashback 10000
python3 diskon.py banding 250000 "30%" "50%+20%"
python3 diskon.py hemat 250000 30
```

Jalankan tanpa argumen untuk mode interaktif (menu angka).

## Fitur

- **Diskon persen tunggal** — harga setelah dipotong sekian persen.
- **Diskon bertingkat** — tiap persen dihitung dari harga hasil tahap
  sebelumnya. Contoh: harga Rp250.000 diskon 50% lalu 20% menjadi
  Rp100.000 (hemat Rp150.000), bukan diskon 70% (Rp75.000).
- **Potongan nominal** — potongan tetap dalam rupiah.
- **Total bayar** — gabungkan diskon persen, PPN (dihitung dari harga
  setelah diskon), lalu kurangi cashback.
- **Bandingkan promo** — bandingkan dua promo sekaligus. Promo ditulis
  seperti `"30%"`, `"50%+20%"`, atau `"20%+50000"` (diskon persen lalu
  potongan nominal).
- **Hemat** — tampilkan cepat jumlah hemat dari satu diskon persen.

## Contoh

Harga Rp250.000, diskon 30%, PPN 11%, cashback Rp10.000:

- Setelah diskon 30%: Rp175.000
- PPN 11% dari Rp175.000: +Rp19.250
- Cashback: -Rp10.000
- **Total bayar: Rp184.250** (hemat Rp65.750)

## Catatan

- Diskon persen harus 0–100%; potongan nominal tidak boleh lebih besar
  dari harga.
- PPN dihitung dari harga setelah diskon, sesuai praktik umum toko.
- Python standar saja, tanpa library tambahan.
