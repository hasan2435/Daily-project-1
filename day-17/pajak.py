#!/usr/bin/env python3
"""Kalkulator Pajak Penghasilan (PPh 21) karyawan — Day 17.

Menghitung PPh 21 tahunan dan bulanan dari gaji pokok, tunjangan tetap,
dan bonus/THR, lengkap dengan rincian perhitungannya:

- Penghasilan bruto setahun
- Biaya jabatan 5% dari bruto, maksimal Rp6.000.000 per tahun
- Iuran pensiun sebagai pengurang
- PTKP sesuai status (TK/0 sampai K/3)
- PKP dibulatkan ke bawah ke ribuan terdekat
- Tarif progresif Pasal 17: 5%, 15%, 25%, 30%, 35%
- Tambahan 20% bila tidak punya NPWP

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.
Tarif dan PTKP mengikuti Undang-Undang Harmonisasi Peraturan
Perpajakan (UU HPP); cek aturan terbaru sebelum dipakai untuk
pelaporan pajak yang sebenarnya.
"""

import argparse
import sys

PTKP = {
    "TK/0": 54_000_000,   # Tidak kawin, tanpa tanggungan
    "K/0": 58_500_000,    # Kawin, tanpa tanggungan
    "K/1": 63_000_000,    # Kawin, 1 tanggungan
    "K/2": 67_500_000,    # Kawin, 2 tanggungan
    "K/3": 72_000_000,    # Kawin, 3 tanggungan
}

# (batas atas lapisan, tarif) — lapisan terakhir tanpa batas atas.
TARIF_PROGRESIF = [
    (60_000_000, 0.05),
    (250_000_000, 0.15),
    (500_000_000, 0.25),
    (5_000_000_000, 0.30),
    (float("inf"), 0.35),
]

BIAYA_JABATAN_PERSEN = 0.05
BIAYA_JABATAN_MAKS_TAHUN = 6_000_000


def rupiah(nilai):
    """Format angka menjadi string rupiah, misal Rp12.345.678."""
    return "Rp" + f"{int(round(nilai)):,}".replace(",", ".")


def hitung_pajak_progresif(pkp):
    """Hitung PPh dari PKP dengan tarif progresif.

    Mengembalikan (total pajak, rincian lapisan) dengan rincian berupa
    daftar (batas bawah, batas atas, tarif, pajak lapisan).
    """
    pajak = 0.0
    rincian = []
    batas_bawah = 0
    for batas_atas, tarif in TARIF_PROGRESIF:
        if pkp <= batas_bawah:
            break
        kena = min(pkp, batas_atas) - batas_bawah
        pajak_lapis = kena * tarif
        pajak += pajak_lapis
        rincian.append((batas_bawah, min(pkp, batas_atas), tarif, pajak_lapis))
        batas_bawah = batas_atas
    return pajak, rincian


def hitung(gaji_bulanan, tunjangan_bulanan=0, bonus_tahunan=0,
           iuran_pensiun_bulanan=0, status="TK/0", punya_npwp=True):
    """Hitung seluruh komponen PPh 21, kembalikan sebagai dict."""
    bruto = (gaji_bulanan + tunjangan_bulanan) * 12 + bonus_tahunan
    biaya_jabatan = min(bruto * BIAYA_JABATAN_PERSEN, BIAYA_JABATAN_MAKS_TAHUN)
    iuran_tahunan = iuran_pensiun_bulanan * 12
    neto = bruto - biaya_jabatan - iuran_tahunan
    ptkp = PTKP[status]
    pkp = max(0, neto - ptkp)
    pkp = (pkp // 1000) * 1000  # dibulatkan ke bawah ke ribuan terdekat
    pajak, rincian = hitung_pajak_progresif(pkp)
    tanpa_npwp = not punya_npwp
    if tanpa_npwp:
        pajak *= 1.20
    pajak_bulanan = pajak / 12
    gaji_bersih = gaji_bulanan + tunjangan_bulanan \
        - iuran_pensiun_bulanan - pajak_bulanan
    return {
        "bruto": bruto,
        "biaya_jabatan": biaya_jabatan,
        "iuran_tahunan": iuran_tahunan,
        "neto": neto,
        "ptkp": ptkp,
        "pkp": pkp,
        "pajak_tahunan": pajak,
        "pajak_bulanan": pajak_bulanan,
        "gaji_bersih": gaji_bersih,
        "rincian": rincian,
        "tanpa_npwp": tanpa_npwp,
        "status": status,
    }


def tampilkan(hasil):
    """Tampilkan rincian perhitungan PPh 21 ke terminal."""
    print()
    print("=" * 56)
    print("RINCIAN PPh 21".center(56))
    print("=" * 56)
    print(f"Status PTKP           : {hasil['status']}")
    print(f"Penghasilan bruto/thn : {rupiah(hasil['bruto'])}")
    print(f"Biaya jabatan (5%)    : -{rupiah(hasil['biaya_jabatan'])}")
    print(f"Iuran pensiun/thn     : -{rupiah(hasil['iuran_tahunan'])}")
    print(f"Penghasilan neto/thn  : {rupiah(hasil['neto'])}")
    print(f"PTKP                  : -{rupiah(hasil['ptkp'])}")
    print(f"PKP                   : {rupiah(hasil['pkp'])}")
    print("-" * 56)
    if hasil["pkp"] == 0:
        print("PKP nol — penghasilan di bawah PTKP, tidak ada pajak.")
    else:
        print("Perhitungan tarif progresif:")
        for bawah, atas, tarif, pajak_lapis in hasil["rincian"]:
            persen = int(tarif * 100)
            print(f"  {persen:>2}% x {rupiah(atas - bawah):>14} = {rupiah(pajak_lapis)}")
        if hasil["tanpa_npwp"]:
            print("  Tanpa NPWP: tarif dinaikkan 20%.")
    print("-" * 56)
    print(f"PPh 21 setahun        : {rupiah(hasil['pajak_tahunan'])}")
    print(f"PPh 21 sebulan        : {rupiah(hasil['pajak_bulanan'])}")
    print(f"Gaji bersih sebulan   : {rupiah(hasil['gaji_bersih'])}")
    print("=" * 56)
    print("Perkiraan saja. Tarif dan PTKP mengikuti UU HPP;")
    print("cek aturan terbaru sebelum dipakai untuk pelaporan.")
    print()


def tampilkan_ptkp():
    print()
    print("PTKP (Penghasilan Tidak Kena Pajak) per tahun:")
    print("-" * 46)
    keterangan = {
        "TK/0": "Tidak kawin, tanpa tanggungan",
        "K/0": "Kawin, tanpa tanggungan",
        "K/1": "Kawin, 1 tanggungan",
        "K/2": "Kawin, 2 tanggungan",
        "K/3": "Kawin, 3 tanggungan",
    }
    for status, nilai in PTKP.items():
        print(f"  {status:<6} {rupiah(nilai):>14}  — {keterangan[status]}")
    print()


def tampilkan_tarif():
    print()
    print("Tarif progresif PPh Pasal 17 (UU HPP):")
    print("-" * 46)
    print("  Lapisan PKP                    Tarif")
    print("  s.d. Rp60.000.000              5%")
    print("  > Rp60 jt s.d. Rp250 jt        15%")
    print("  > Rp250 jt s.d. Rp500 jt       25%")
    print("  > Rp500 jt s.d. Rp5 miliar     30%")
    print("  > Rp5 miliar                   35%")
    print()


def tanya_angka(pesan, default=0):
    """Minta angka dari pengguna; kosong berarti memakai default."""
    while True:
        jawaban = input(f"{pesan} [{rupiah(default)}]: ").strip()
        if jawaban == "":
            return default
        try:
            nilai = float(jawaban.replace(".", "").replace(",", "."))
        except ValueError:
            print("  Masukkan angka saja, misal 8000000.")
            continue
        if nilai < 0:
            print("  Nilai tidak boleh negatif.")
            continue
        return nilai


def tanya_status():
    while True:
        jawaban = input("Status PTKP (TK/0, K/0, K/1, K/2, K/3) [TK/0]: ").strip().upper()
        if jawaban == "":
            return "TK/0"
        if jawaban in PTKP:
            return jawaban
        print("  Status tidak dikenal. Pilih salah satu: TK/0, K/0, K/1, K/2, K/3.")


def tanya_npwp():
    while True:
        jawaban = input("Punya NPWP? (y/n) [y]: ").strip().lower()
        if jawaban in ("", "y", "ya"):
            return True
        if jawaban in ("n", "tidak"):
            return False
        print("  Jawab y atau n.")


def mode_interaktif():
    print()
    print("Kalkulator PPh 21 karyawan")
    print("Isi angka dalam rupiah per bulan, kecuali bonus (per tahun).")
    print("Tekan Enter untuk memakai nilai default.")
    print()
    gaji = tanya_angka("Gaji pokok per bulan", 0)
    tunjangan = tanya_angka("Tunjangan tetap per bulan", 0)
    bonus = tanya_angka("Bonus/THR per tahun", 0)
    iuran = tanya_angka("Iuran pensiun per bulan", 0)
    status = tanya_status()
    punya_npwp = tanya_npwp()
    hasil = hitung(gaji, tunjangan, bonus, iuran, status, punya_npwp)
    tampilkan(hasil)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Kalkulator Pajak Penghasilan (PPh 21) karyawan.")
    sub = parser.add_subparsers(dest="perintah")

    cepat = sub.add_parser("cepat", help="Hitung cepat dari gaji bulanan.")
    cepat.add_argument("gaji", type=float, help="Gaji pokok per bulan (Rp).")
    cepat.add_argument("--tunjangan", type=float, default=0,
                       help="Tunjangan tetap per bulan (Rp).")
    cepat.add_argument("--bonus", type=float, default=0,
                       help="Bonus/THR per tahun (Rp).")
    cepat.add_argument("--iuran", type=float, default=0,
                       help="Iuran pensiun per bulan (Rp).")
    cepat.add_argument("--status", default="TK/0", choices=sorted(PTKP),
                       help="Status PTKP (default TK/0).")
    cepat.add_argument("--tanpa-npwp", action="store_true",
                       help="Hitung dengan tambahan 20%% karena tanpa NPWP.")

    sub.add_parser("ptkp", help="Tampilkan daftar PTKP.")
    sub.add_parser("tarif", help="Tampilkan tarif progresif PPh Pasal 17.")

    args = parser.parse_args(argv)

    if args.perintah == "cepat":
        hasil = hitung(args.gaji, args.tunjangan, args.bonus, args.iuran,
                       args.status, not args.tanpa_npwp)
        tampilkan(hasil)
    elif args.perintah == "ptkp":
        tampilkan_ptkp()
    elif args.perintah == "tarif":
        tampilkan_tarif()
    else:
        mode_interaktif()
    return 0


if __name__ == "__main__":
    sys.exit(main())
