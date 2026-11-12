# Day 12 — Pembagi Tagihan

Proyek harian ke-12: program terminal untuk membagi tagihan makan
bersama (atau tagihan apa pun) dengan adil. Ada tiga cara membagi:

- **Bagi rata** — total dibagi sama rata ke semua orang.
- **Bagi per item** — tiap orang memasukkan pesanannya sendiri; item
  bersama (misalnya parkir atau makanan yang dimakan bareng) dibagi
  rata, sedangkan service charge dan tip dibagi sebanding dengan
  subtotal tiap orang.
- **Bagi menurut persen** — tiap orang menanggung persentase yang
  disepakati, total persen harus 100.

Semua cara bisa ditambah service charge dan tip (tip dihitung dari
total awal + service charge), serta membulatkan bagian tiap orang ke
kelipatan 100, 500, atau 1000 supaya mudah ditransfer.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-12
python3 tagihan.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka: bagi rata,
bagi per item, bagi menurut persen).

Bagi rata, dengan service charge 10% dan tip 5%:

```bash
python3 tagihan.py rata 300000 3 --service 10 --tip 5
```

Bagi rata dengan pembulatan ke ribuan terdekat:

```bash
python3 tagihan.py rata 275000 4 --bulat 1000
```

Bagi menurut persen:

```bash
python3 tagihan.py persen 400000 --bagi "Ani=50, Budi=30, Cici=20"
python3 tagihan.py persen 400000 --bagi "Ani=50, Budi=30, Cici=20" --service 10
```

Bagi per item (interaktif, masukkan nama dan item tiap orang):

```bash
python3 tagihan.py item
python3 tagihan.py item --service 5 --tip 10
```

Item ditulis dengan format `nama item=harga`, dipisah koma, contoh:
`nasi goreng=25000, es teh=8000`. Kosongkan nama untuk selesai,
lalu masukkan item bersama bila ada.
