#!/usr/bin/env python3
"""Kalkulator Zakat — Day 19 Daily Project 1.

Menghitung zakat penghasilan, zakat mal (emas, perak, tabungan, dagang),
dan zakat fitrah dari terminal. Python standar saja, tanpa library tambahan.

Aturan yang dipakai:
- Kadar zakat: 2,5% dari harta atau penghasilan yang sudah wajib zakat.
- Nisab emas: 85 gram; nisab perak: 595 gram (haul 1 tahun Hijriah).
- Nisab penghasilan: setara 85 gram emas per tahun, dibagi 12 per bulan.
- Zakat fitrah: 2,5 kg beras per jiwa (atau senilai uangnya).

Harga emas, perak, dan beras mengikuti harga pasar saat ini, jadi bisa
diubah lewat opsi baris perintah. Nilai default di bawah ini hanya
perkiraan dan wajib diganti dengan harga saat menghitung yang sebenarnya.
"""

import argparse
import sys

KADAR_ZAKAT = 0.025
NISAB_EMAS_GRAM = 85
NISAB_PERAK_GRAM = 595
FITRAH_KG_PER_JIWA = 2.5
HARGA_EMAS_DEFAULT = 1_500_000   # rupiah per gram
HARGA_PERAK_DEFAULT = 15_000     # rupiah per gram
HARGA_BERAS_DEFAULT = 15_000     # rupiah per kg


def rupiah(nilai):
    """Format angka menjadi rupiah, contoh: 1500000 -> 'Rp1.500.000'."""
    nilai = int(round(nilai))
    teks = f"{abs(nilai):,}".replace(",", ".")
    return f"-Rp{teks}" if nilai < 0 else f"Rp{teks}"


def baca_angka(teks):
    """Ubah masukan pengguna menjadi float.

    Menerima pemisah ribuan titik dan desimal koma, serta akhiran
    'jt'/'juta' (x1.000.000) dan 'rb'/'ribu' (x1.000).
    Contoh: '10jt' -> 10000000.0, '1.500.000' -> 1500000.0.
    """
    teks = teks.strip().lower().replace(" ", "")
    if not teks:
        raise ValueError("masukan kosong")
    pengali = 1
    for akhiran, kali in (("juta", 1_000_000), ("jt", 1_000_000),
                         ("ribu", 1_000), ("rb", 1_000)):
        if teks.endswith(akhiran):
            teks = teks[: -len(akhiran)]
            pengali = kali
            break
    teks = teks.replace(".", "").replace(",", ".")
    return float(teks) * pengali


def tanya_angka(pesan, minimum=0):
    """Minta angka dari pengguna sampai mendapat nilai yang valid."""
    while True:
        try:
            nilai = baca_angka(input(pesan))
        except ValueError:
            print("  Masukan tidak dikenali, coba lagi (contoh: 10000000 atau 10jt).")
            continue
        if nilai <= minimum:
            print(f"  Nilainya harus lebih dari {minimum}.")
            continue
        return nilai


def garis():
    print("-" * 56)


def tampilkan_judul(judul):
    garis()
    print(judul)
    garis()


def nisab_tahunan(harga_emas):
    return NISAB_EMAS_GRAM * harga_emas


def nisab_bulanan(harga_emas):
    return nisab_tahunan(harga_emas) / 12


def hitung_zakat_penghasilan(gaji, harga_emas):
    """Zakat penghasilan bulanan: 2,5% bila gaji mencapai nisab bulanan."""
    nisab = nisab_bulanan(harga_emas)
    wajib = gaji >= nisab
    zakat = KADAR_ZAKAT * gaji if wajib else 0.0
    return {"nisab": nisab, "wajib": wajib, "zakat": zakat}


def hitung_zakat_mal(harta, harga_emas):
    """Zakat mal: 2,5% bila total harta mencapai nisab dan sudah 1 haul."""
    nisab = nisab_tahunan(harga_emas)
    wajib = harta >= nisab
    zakat = KADAR_ZAKAT * harta if wajib else 0.0
    return {"nisab": nisab, "wajib": wajib, "zakat": zakat}


def hitung_zakat_emas(gram, harga_emas):
    """Zakat emas: 2,5% dari nilai emas bila mencapai 85 gram."""
    nilai = gram * harga_emas
    wajib = gram >= NISAB_EMAS_GRAM
    zakat = KADAR_ZAKAT * nilai if wajib else 0.0
    return {"nisab_gram": NISAB_EMAS_GRAM, "nilai": nilai,
            "wajib": wajib, "zakat": zakat}


def hitung_zakat_perak(gram, harga_perak):
    """Zakat perak: 2,5% dari nilai perak bila mencapai 595 gram."""
    nilai = gram * harga_perak
    wajib = gram >= NISAB_PERAK_GRAM
    zakat = KADAR_ZAKAT * nilai if wajib else 0.0
    return {"nisab_gram": NISAB_PERAK_GRAM, "nilai": nilai,
            "wajib": wajib, "zakat": zakat}


def hitung_zakat_fitrah(jiwa, harga_beras):
    """Zakat fitrah: 2,5 kg beras per jiwa, bisa dibayar senilai uangnya."""
    kg = jiwa * FITRAH_KG_PER_JIWA
    return {"kg": kg, "uang": kg * harga_beras}


def laporan_penghasilan(gaji, harga_emas):
    hasil = hitung_zakat_penghasilan(gaji, harga_emas)
    tampilkan_judul("Zakat Penghasilan (per bulan)")
    print(f"Harga emas        : {rupiah(harga_emas)}/gram")
    print(f"Nisab bulanan     : {rupiah(hasil['nisab'])}")
    print(f"Gaji bulanan      : {rupiah(gaji)}")
    if hasil["wajib"]:
        print(f"Status            : WAJIB zakat (gaji mencapai nisab)")
        print(f"Zakat per bulan   : {rupiah(hasil['zakat'])}")
        print(f"Zakat per tahun   : {rupiah(hasil['zakat'] * 12)}")
    else:
        kurang = hasil["nisab"] - gaji
        print("Status            : BELUM WAJIB zakat")
        print(f"Kurang {rupiah(kurang)} lagi untuk mencapai nisab.")
    garis()


def laporan_mal(harta, harga_emas):
    hasil = hitung_zakat_mal(harta, harga_emas)
    tampilkan_judul("Zakat Mal (tabungan / dagang / harta simpanan)")
    print(f"Harga emas        : {rupiah(harga_emas)}/gram")
    print(f"Nisab (85 gr emas): {rupiah(hasil['nisab'])}")
    print(f"Total harta       : {rupiah(harta)}")
    if hasil["wajib"]:
        print("Status            : WAJIB zakat (mencapai nisab, haul 1 tahun)")
        print(f"Zakat yang dibayar: {rupiah(hasil['zakat'])}")
    else:
        kurang = hasil["nisab"] - harta
        print("Status            : BELUM WAJIB zakat")
        print(f"Kurang {rupiah(kurang)} lagi untuk mencapai nisab.")
    garis()


def laporan_emas(gram, harga_emas):
    hasil = hitung_zakat_emas(gram, harga_emas)
    tampilkan_judul("Zakat Emas")
    print(f"Emas dimiliki     : {gram:g} gram")
    print(f"Harga emas        : {rupiah(harga_emas)}/gram")
    print(f"Nilai emas        : {rupiah(hasil['nilai'])}")
    print(f"Nisab emas        : {hasil['nisab_gram']} gram")
    if hasil["wajib"]:
        print("Status            : WAJIB zakat")
        print(f"Zakat yang dibayar: {rupiah(hasil['zakat'])}")
    else:
        print("Status            : BELUM WAJIB zakat")
        print(f"Kurang {hasil['nisab_gram'] - gram:g} gram lagi untuk mencapai nisab.")
    garis()


def laporan_perak(gram, harga_perak):
    hasil = hitung_zakat_perak(gram, harga_perak)
    tampilkan_judul("Zakat Perak")
    print(f"Perak dimiliki    : {gram:g} gram")
    print(f"Harga perak       : {rupiah(harga_perak)}/gram")
    print(f"Nilai perak       : {rupiah(hasil['nilai'])}")
    print(f"Nisab perak       : {hasil['nisab_gram']} gram")
    if hasil["wajib"]:
        print("Status            : WAJIB zakat")
        print(f"Zakat yang dibayar: {rupiah(hasil['zakat'])}")
    else:
        print("Status            : BELUM WAJIB zakat")
        print(f"Kurang {hasil['nisab_gram'] - gram:g} gram lagi untuk mencapai nisab.")
    garis()


def laporan_fitrah(jiwa, harga_beras):
    hasil = hitung_zakat_fitrah(jiwa, harga_beras)
    tampilkan_judul("Zakat Fitrah")
    print(f"Jumlah jiwa       : {int(jiwa)} orang")
    print(f"Harga beras       : {rupiah(harga_beras)}/kg")
    print(f"Beras yang dibayar: {hasil['kg']:g} kg (2,5 kg/jiwa)")
    print(f"Senilai uang      : {rupiah(hasil['uang'])}")
    garis()


def laporan_nisab(harga_emas, harga_perak):
    tampilkan_judul("Nisab Saat Ini")
    print(f"Harga emas        : {rupiah(harga_emas)}/gram")
    print(f"Harga perak       : {rupiah(harga_perak)}/gram")
    print(f"Nisab emas        : {NISAB_EMAS_GRAM} gram = {rupiah(nisab_tahunan(harga_emas))}")
    print(f"Nisab perak       : {NISAB_PERAK_GRAM} gram = {rupiah(NISAB_PERAK_GRAM * harga_perak)}")
    print(f"Nisab penghasilan : {rupiah(nisab_bulanan(harga_emas))}/bulan")
    print(f"                  ({rupiah(nisab_tahunan(harga_emas))}/tahun)")
    print("Kadar zakat       : 2,5%")
    print("Zakat fitrah      : 2,5 kg beras/jiwa")
    garis()


def menu_interaktif():
    print("Kalkulator Zakat — ketik angka menu, 0 untuk keluar.")
    while True:
        print()
        print("1. Zakat penghasilan")
        print("2. Zakat mal (tabungan / dagang)")
        print("3. Zakat emas")
        print("4. Zakat perak")
        print("5. Zakat fitrah")
        print("6. Lihat nisab saat ini")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()
        print()
        if pilihan == "0":
            print("Semoga bermanfaat.")
            return
        if pilihan == "1":
            gaji = tanya_angka("Gaji bulanan (Rp): ")
            harga = tanya_angka(f"Harga emas/gram [default {rupiah(HARGA_EMAS_DEFAULT)}]: ",
                                minimum=0) if input(
                "Pakai harga emas lain? (y/tidak, Enter = default): ").strip().lower() in ("y", "ya") else HARGA_EMAS_DEFAULT
            laporan_penghasilan(gaji, harga)
        elif pilihan == "2":
            harta = tanya_angka("Total harta yang sudah 1 haul (Rp): ")
            laporan_mal(harta, HARGA_EMAS_DEFAULT)
        elif pilihan == "3":
            gram = tanya_angka("Emas yang dimiliki (gram): ")
            laporan_emas(gram, HARGA_EMAS_DEFAULT)
        elif pilihan == "4":
            gram = tanya_angka("Perak yang dimiliki (gram): ")
            laporan_perak(gram, HARGA_PERAK_DEFAULT)
        elif pilihan == "5":
            jiwa = tanya_angka("Jumlah jiwa: ")
            laporan_fitrah(jiwa, HARGA_BERAS_DEFAULT)
        elif pilihan == "6":
            laporan_nisab(HARGA_EMAS_DEFAULT, HARGA_PERAK_DEFAULT)
        else:
            print("Pilihan tidak ada, coba lagi.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Kalkulator Zakat: penghasilan, mal, emas, perak, dan fitrah.")
    sub = parser.add_subparsers(dest="perintah")

    p = sub.add_parser("penghasilan", help="zakat penghasilan bulanan")
    p.add_argument("gaji", type=float, help="gaji bulanan (Rp)")
    p.add_argument("--harga-emas", type=float, default=HARGA_EMAS_DEFAULT,
                   help=f"harga emas per gram (default {HARGA_EMAS_DEFAULT})")

    p = sub.add_parser("mal", help="zakat mal dari total harta (haul 1 tahun)")
    p.add_argument("harta", type=float, help="total harta (Rp)")
    p.add_argument("--harga-emas", type=float, default=HARGA_EMAS_DEFAULT,
                   help=f"harga emas per gram (default {HARGA_EMAS_DEFAULT})")

    p = sub.add_parser("emas", help="zakat emas")
    p.add_argument("gram", type=float, help="emas yang dimiliki (gram)")
    p.add_argument("--harga-emas", type=float, default=HARGA_EMAS_DEFAULT,
                   help=f"harga emas per gram (default {HARGA_EMAS_DEFAULT})")

    p = sub.add_parser("perak", help="zakat perak")
    p.add_argument("gram", type=float, help="perak yang dimiliki (gram)")
    p.add_argument("--harga-perak", type=float, default=HARGA_PERAK_DEFAULT,
                   help=f"harga perak per gram (default {HARGA_PERAK_DEFAULT})")

    p = sub.add_parser("fitrah", help="zakat fitrah")
    p.add_argument("jiwa", type=float, help="jumlah jiwa")
    p.add_argument("--harga-beras", type=float, default=HARGA_BERAS_DEFAULT,
                   help=f"harga beras per kg (default {HARGA_BERAS_DEFAULT})")

    p = sub.add_parser("nisab", help="lihat nisab dari harga emas/perak saat ini")
    p.add_argument("--harga-emas", type=float, default=HARGA_EMAS_DEFAULT,
                   help=f"harga emas per gram (default {HARGA_EMAS_DEFAULT})")
    p.add_argument("--harga-perak", type=float, default=HARGA_PERAK_DEFAULT,
                   help=f"harga perak per gram (default {HARGA_PERAK_DEFAULT})")

    args = parser.parse_args(argv)
    if args.perintah is None:
        menu_interaktif()
        return 0

    if args.perintah == "penghasilan":
        if args.gaji <= 0:
            parser.error("gaji harus lebih dari 0")
        laporan_penghasilan(args.gaji, args.harga_emas)
    elif args.perintah == "mal":
        if args.harta <= 0:
            parser.error("harta harus lebih dari 0")
        laporan_mal(args.harta, args.harga_emas)
    elif args.perintah == "emas":
        if args.gram <= 0:
            parser.error("gram harus lebih dari 0")
        laporan_emas(args.gram, args.harga_emas)
    elif args.perintah == "perak":
        if args.gram <= 0:
            parser.error("gram harus lebih dari 0")
        laporan_perak(args.gram, args.harga_perak)
    elif args.perintah == "fitrah":
        if args.jiwa <= 0 or args.jiwa != int(args.jiwa):
            parser.error("jiwa harus bilangan bulat lebih dari 0")
        laporan_fitrah(args.jiwa, args.harga_beras)
    elif args.perintah == "nisab":
        laporan_nisab(args.harga_emas, args.harga_perak)
    return 0


if __name__ == "__main__":
    sys.exit(main())
