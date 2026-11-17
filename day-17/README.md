# Day 17 — Kalkulator Pajak Penghasilan (PPh 21)

Proyek harian ke-17: kalkulator PPh 21 karyawan di terminal. Hitung
pajak dari gaji pokok, tunjangan tetap, dan bonus/THR; lengkap dengan
biaya jabatan, iuran pensiun, PTKP sesuai status, dan tarif progresif
Pasal 17, beserta rincian perhitungan dan gaji bersih tiap bulan.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-17
python3 pajak.py
```

Jalankan tanpa argumen untuk mode interaktif: program menanyakan gaji
pokok, tunjangan, bonus/THR, iuran pensiun, status PTKP, dan NPWP,
lalu menampilkan rincian perhitungan.

Langsung dari baris perintah:

```bash
python3 pajak.py cepat 10000000
python3 pajak.py cepat 20000000 --status K/1 --bonus 20000000
python3 pajak.py cepat 8000000 --tunjangan 500000 --iuran 100000
python3 pajak.py cepat 10000000 --tanpa-npwp
python3 pajak.py ptkp
python3 pajak.py tarif
```

## Cara perhitungan

1. **Penghasilan bruto setahun** = (gaji pokok + tunjangan) x 12 + bonus/THR.
2. **Biaya jabatan** = 5% dari bruto, maksimal Rp6.000.000 per tahun.
3. **Penghasilan neto** = bruto - biaya jabatan - iuran pensiun setahun.
4. **PKP** = neto - PTKP, dibulatkan ke bawah ke ribuan terdekat.
5. **PPh 21 setahun** = PKP x tarif progresif Pasal 17. Tanpa NPWP,
   pajak dinaikkan 20%.
6. **PPh 21 sebulan** = PPh setahun / 12; **gaji bersih** = gaji pokok
   + tunjangan - iuran pensiun - PPh sebulan.

## Perintah

| Perintah | Fungsi |
| --- | --- |
| `cepat <gaji>` | Hitung cepat dari gaji pokok bulanan (`--tunjangan`, `--bonus`, `--iuran`, `--status`, `--tanpa-npwp`). |
| `ptkp` | Tampilkan daftar PTKP per status. |
| `tarif` | Tampilkan tarif progresif PPh Pasal 17. |

## PTKP dan tarif

PTKP per tahun: TK/0 Rp54.000.000, K/0 Rp58.500.000, K/1
Rp63.000.000, K/2 Rp67.500.000, K/3 Rp72.000.000.

Tarif progresif PPh Pasal 17 (UU HPP): 5% untuk PKP s.d. Rp60 jt,
15% s.d. Rp250 jt, 25% s.d. Rp500 jt, 30% s.d. Rp5 miliar, 35% di
atas Rp5 miliar.

Hasilnya perkiraan saja. Tarif dan PTKP mengikuti Undang-Undang
Harmonisasi Peraturan Perpajakan (UU HPP); cek aturan terbaru
sebelum dipakai untuk pelaporan pajak yang sebenarnya.
