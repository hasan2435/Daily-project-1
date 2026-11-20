#!/usr/bin/env python3
"""Kalkulator Diskon & Promo Belanja — Day 20 Daily Project 1.

Menghitung harga akhir belanja dari terminal: diskon persen tunggal,
diskon bertingkat (misal 50% + 20% tidak sama dengan 70%), potongan
nominal, PPN, cashback, sampai membandingkan dua promo sekaligus.

Python standar saja, tanpa library tambahan.

Cara pakai (mode perintah):
    python3 diskon.py diskon 250000 30
    python3 diskon.py bertingkat 250000 50 20
    python3 diskon.py potong 250000 50000
    python3 diskon.py total 250000 --diskon 30 --ppn 11 --cashback 10000
    python3 diskon.py banding 250000 "30%" "50%+20%"
    python3 diskon.py hemat 250000 30

Jalankan tanpa argumen untuk mode interaktif (menu angka).
"""

import argparse
import sys


def rupiah(nilai):
    """Format angka menjadi string rupiah, misal 125000 -> 'Rp125.000'."""
    nilai = int(round(nilai))
    return "Rp" + f"{nilai:,}".replace(",", ".")


def persen_str(persen):
    """Format persen tanpa nol berlebih, misal 30.0 -> '30%'."""
    if persen == int(persen):
        return f"{int(persen)}%"
    return f"{persen:g}%"


def hitung_diskon(harga, persen):
    """Diskon persen tunggal. Mengembalikan (harga_akhir, hemat)."""
    if harga < 0:
        raise ValueError("Harga tidak boleh negatif.")
    if not 0 <= persen <= 100:
        raise ValueError("Diskon harus 0-100%.")
    hemat = harga * persen / 100
    return harga - hemat, hemat


def hitung_bertingkat(harga, daftar_persen):
    """Diskon bertingkat: tiap persen dihitung dari harga hasil tahap sebelumnya.

    Contoh: harga 250.000, diskon 50% lalu 20% -> 250.000 x 0,5 x 0,8
    = 100.000 (hemat 150.000), bukan diskon 70% = 75.000.
    Mengembalikan (harga_akhir, hemat, rincian_tahap).
    """
    if harga < 0:
        raise ValueError("Harga tidak boleh negatif.")
    for persen in daftar_persen:
        if not 0 <= persen <= 100:
            raise ValueError("Setiap diskon harus 0-100%.")
    sisa = harga
    rincian = []
    for persen in daftar_persen:
        potongan = sisa * persen / 100
        sisa -= potongan
        rincian.append((persen, potongan, sisa))
    return sisa, harga - sisa, rincian


def hitung_potong(harga, nominal):
    """Potongan nominal tetap. Mengembalikan (harga_akhir, hemat)."""
    if harga < 0 or nominal < 0:
        raise ValueError("Harga dan potongan tidak boleh negatif.")
    if nominal > harga:
        raise ValueError("Potongan tidak boleh lebih besar dari harga.")
    return harga - nominal, nominal


def hitung_total(harga, diskon=0.0, ppn=0.0, cashback=0.0):
    """Hitung total bayar: harga - diskon persen, + PPN, - cashback.

    PPN dihitung dari harga setelah diskon. Cashback dipotong terakhir
    dan tidak boleh membuat total negatif.
    Mengembalikan dict berisi rincian perhitungan.
    """
    if harga < 0 or diskon < 0 or ppn < 0 or cashback < 0:
        raise ValueError("Semua nilai tidak boleh negatif.")
    if not 0 <= diskon <= 100:
        raise ValueError("Diskon harus 0-100%.")
    if ppn > 100:
        raise ValueError("PPN maksimal 100%.")
    hemat_diskon = harga * diskon / 100
    setelah_diskon = harga - hemat_diskon
    nilai_ppn = setelah_diskon * ppn / 100
    total = setelah_diskon + nilai_ppn - cashback
    if total < 0:
        total = 0
    return {
        "harga_awal": harga,
        "diskon_persen": diskon,
        "hemat_diskon": hemat_diskon,
        "setelah_diskon": setelah_diskon,
        "ppn_persen": ppn,
        "nilai_ppn": nilai_ppn,
        "cashback": cashback,
        "total": total,
        "hemat_total": harga - total,
    }


def uraikan_promo(teks):
    """Uraikan teks promo menjadi daftar langkah.

    Format yang diterima, dipisah tanda '+':
      '30%'    -> satu diskon persen
      '50000'  -> satu potongan nominal (rupiah)
      '30%+10%'   -> diskon bertingkat
      '20%+50000' -> diskon persen lalu potongan nominal
    Mengembalikan daftar tuple ('persen', nilai) atau ('nominal', nilai).
    """
    langkah = []
    for bagian in teks.replace(" ", "").split("+"):
        if not bagian:
            raise ValueError(f"Promo tidak valid: '{teks}'.")
        if bagian.endswith("%"):
            try:
                nilai = float(bagian[:-1])
            except ValueError:
                raise ValueError(f"Promo tidak valid: '{teks}'.")
            if not 0 <= nilai <= 100:
                raise ValueError("Diskon persen harus 0-100%.")
            langkah.append(("persen", nilai))
        else:
            try:
                nilai = float(bagian)
            except ValueError:
                raise ValueError(f"Promo tidak valid: '{teks}'.")
            if nilai < 0:
                raise ValueError("Potongan nominal tidak boleh negatif.")
            langkah.append(("nominal", nilai))
    return langkah


def terapkan_promo(harga, teks_promo):
    """Terapkan promo (teks, lihat uraikan_promo) ke harga.

    Mengembalikan (harga_akhir, hemat, rincian_langkah).
    """
    if harga < 0:
        raise ValueError("Harga tidak boleh negatif.")
    langkah = uraikan_promo(teks_promo)
    sisa = harga
    rincian = []
    for jenis, nilai in langkah:
        if jenis == "persen":
            potongan = sisa * nilai / 100
            sisa -= potongan
            rincian.append((f"Diskon {persen_str(nilai)}", potongan, sisa))
        else:
            if nilai > sisa:
                raise ValueError(
                    f"Potongan {rupiah(nilai)} lebih besar dari sisa harga {rupiah(sisa)}."
                )
            sisa -= nilai
            rincian.append((f"Potongan {rupiah(nilai)}", nilai, sisa))
    return sisa, harga - sisa, rincian


def tampilkan_rincian(judul, harga_awal, rincian, harga_akhir):
    print(f"\n{judul}")
    print("-" * 46)
    print(f"Harga awal : {rupiah(harga_awal)}")
    for label, potongan, sisa in rincian:
        print(f"{label:<22} -{rupiah(potongan):>12} -> {rupiah(sisa)}")
    print("-" * 46)
    print(f"Harga akhir: {rupiah(harga_akhir)}")
    print(f"Kamu hemat : {rupiah(harga_awal - harga_akhir)} "
          f"({(harga_awal - harga_akhir) / harga_awal * 100:.1f}% dari harga awal)")


def baca_angka(teks, minimal=None, maksimal=None):
    try:
        nilai = float(teks.replace(".", "").replace(",", "."))
    except ValueError:
        return None
    if minimal is not None and nilai < minimal:
        return None
    if maksimal is not None and nilai > maksimal:
        return None
    return nilai


def mode_interaktif():
    print("=== Kalkulator Diskon & Promo Belanja ===")
    print("1. Diskon persen tunggal")
    print("2. Diskon bertingkat (misal 50% + 20%)")
    print("3. Potongan nominal (rupiah)")
    print("4. Total bayar (diskon + PPN + cashback)")
    print("5. Bandingkan dua promo")
    print("0. Keluar")
    while True:
        pilihan = input("\nPilih menu (0-5): ").strip()
        if pilihan == "0":
            print("Sampai jumpa, selamat berbelanja dengan bijak!")
            return
        if pilihan not in {"1", "2", "3", "4", "5"}:
            print("Pilihan tidak dikenal, coba lagi.")
            continue
        harga = baca_angka(input("Harga awal (Rp): "), minimal=0)
        if harga is None:
            print("Harga tidak valid.")
            continue
        try:
            if pilihan == "1":
                persen = baca_angka(input("Diskon (%): "), minimal=0, maksimal=100)
                if persen is None:
                    print("Diskon harus 0-100%.")
                    continue
                akhir, hemat = hitung_diskon(harga, persen)
                tampilkan_rincian(f"Diskon {persen_str(persen)}",
                                  harga, [(f"Diskon {persen_str(persen)}", hemat, akhir)], akhir)
            elif pilihan == "2":
                teks = input("Diskon bertingkat, pisah koma (misal 50,20): ")
                daftar = [baca_angka(x.strip(), minimal=0, maksimal=100) for x in teks.split(",")]
                if any(x is None for x in daftar) or not daftar:
                    print("Diskon harus angka 0-100, pisahkan dengan koma.")
                    continue
                akhir, _, rincian = hitung_bertingkat(harga, daftar)
                tampilkan_rincian("Diskon bertingkat",
                                  harga,
                                  [(f"Diskon {persen_str(p)}", pot, sisa) for p, pot, sisa in rincian],
                                  akhir)
            elif pilihan == "3":
                nominal = baca_angka(input("Potongan (Rp): "), minimal=0)
                if nominal is None:
                    print("Potongan tidak valid.")
                    continue
                akhir, hemat = hitung_potong(harga, nominal)
                tampilkan_rincian("Potongan nominal",
                                  harga, [(f"Potongan {rupiah(nominal)}", hemat, akhir)], akhir)
            elif pilihan == "4":
                diskon = baca_angka(input("Diskon (%) [0]: ") or "0", minimal=0, maksimal=100)
                ppn = baca_angka(input("PPN (%) [0]: ") or "0", minimal=0, maksimal=100)
                cashback = baca_angka(input("Cashback (Rp) [0]: ") or "0", minimal=0)
                if diskon is None or ppn is None or cashback is None:
                    print("Ada nilai yang tidak valid.")
                    continue
                hasil = hitung_total(harga, diskon, ppn, cashback)
                print("\nRincian total bayar")
                print("-" * 46)
                print(f"Harga awal : {rupiah(hasil['harga_awal'])}")
                print(f"Diskon {persen_str(diskon)} : -{rupiah(hasil['hemat_diskon'])}")
                print(f"PPN {persen_str(ppn)}     : +{rupiah(hasil['nilai_ppn'])}")
                print(f"Cashback   : -{rupiah(cashback)}")
                print("-" * 46)
                print(f"Total bayar: {rupiah(hasil['total'])}")
                print(f"Kamu hemat : {rupiah(hasil['hemat_total'])}")
            elif pilihan == "5":
                promo_a = input('Promo A (misal "30%" atau "50%+20%"): ')
                promo_b = input('Promo B (misal "25%+10000"): ')
                akhir_a, hemat_a, _ = terapkan_promo(harga, promo_a)
                akhir_b, hemat_b, _ = terapkan_promo(harga, promo_b)
                print("\nPerbandingan promo")
                print("-" * 46)
                print(f"Promo A ({promo_a}): {rupiah(akhir_a)}  (hemat {rupiah(hemat_a)})")
                print(f"Promo B ({promo_b}): {rupiah(akhir_b)}  (hemat {rupiah(hemat_b)})")
                if akhir_a < akhir_b:
                    print(f"Promo A lebih murah {rupiah(akhir_b - akhir_a)}.")
                elif akhir_b < akhir_a:
                    print(f"Promo B lebih murah {rupiah(akhir_a - akhir_b)}.")
                else:
                    print("Kedua promo sama murahnya.")
        except ValueError as err:
            print(f"Gagal menghitung: {err}")


def buat_parser():
    parser = argparse.ArgumentParser(
        description="Kalkulator Diskon & Promo Belanja — hitung harga akhir belanja dari terminal."
    )
    sub = parser.add_subparsers(dest="perintah")

    p = sub.add_parser("diskon", help="Diskon persen tunggal.")
    p.add_argument("harga", type=float, help="Harga awal (Rp).")
    p.add_argument("persen", type=float, help="Diskon 0-100 (%).")

    p = sub.add_parser("bertingkat", help="Diskon bertingkat, misal 50 lalu 20.")
    p.add_argument("harga", type=float, help="Harga awal (Rp).")
    p.add_argument("persen", type=float, nargs="+", help="Daftar diskon 0-100 (%), berurutan.")

    p = sub.add_parser("potong", help="Potongan nominal tetap (Rp).")
    p.add_argument("harga", type=float, help="Harga awal (Rp).")
    p.add_argument("nominal", type=float, help="Potongan (Rp).")

    p = sub.add_parser("total", help="Total bayar: diskon + PPN - cashback.")
    p.add_argument("harga", type=float, help="Harga awal (Rp).")
    p.add_argument("--diskon", type=float, default=0.0, help="Diskon 0-100 (%) (default 0).")
    p.add_argument("--ppn", type=float, default=0.0, help="PPN 0-100 (%) (default 0).")
    p.add_argument("--cashback", type=float, default=0.0, help="Cashback (Rp) (default 0).")

    p = sub.add_parser("banding", help="Bandingkan dua promo, misal '30%' vs '50%+20%'.")
    p.add_argument("harga", type=float, help="Harga awal (Rp).")
    p.add_argument("promo_a", help='Promo A, misal "30%" atau "50%+20%".')
    p.add_argument("promo_b", help='Promo B, misal "25%+10000".')

    p = sub.add_parser("hemat", help="Tampilkan jumlah hemat dari diskon persen.")
    p.add_argument("harga", type=float, help="Harga awal (Rp).")
    p.add_argument("persen", type=float, help="Diskon 0-100 (%).")

    return parser


def main(argv=None):
    parser = buat_parser()
    args = parser.parse_args(argv)
    if args.perintah is None:
        mode_interaktif()
        return 0
    try:
        if args.perintah == "diskon":
            akhir, hemat = hitung_diskon(args.harga, args.persen)
            tampilkan_rincian(f"Diskon {persen_str(args.persen)}",
                              args.harga, [(f"Diskon {persen_str(args.persen)}", hemat, akhir)], akhir)
        elif args.perintah == "bertingkat":
            akhir, _, rincian = hitung_bertingkat(args.harga, args.persen)
            tampilkan_rincian("Diskon bertingkat",
                              args.harga,
                              [(f"Diskon {persen_str(p)}", pot, sisa) for p, pot, sisa in rincian],
                              akhir)
        elif args.perintah == "potong":
            akhir, hemat = hitung_potong(args.harga, args.nominal)
            tampilkan_rincian("Potongan nominal",
                              args.harga, [(f"Potongan {rupiah(args.nominal)}", hemat, akhir)], akhir)
        elif args.perintah == "total":
            hasil = hitung_total(args.harga, args.diskon, args.ppn, args.cashback)
            print("\nRincian total bayar")
            print("-" * 46)
            print(f"Harga awal : {rupiah(hasil['harga_awal'])}")
            print(f"Diskon {persen_str(args.diskon)} : -{rupiah(hasil['hemat_diskon'])}")
            print(f"PPN {persen_str(args.ppn)}     : +{rupiah(hasil['nilai_ppn'])}")
            print(f"Cashback   : -{rupiah(hasil['cashback'])}")
            print("-" * 46)
            print(f"Total bayar: {rupiah(hasil['total'])}")
            print(f"Kamu hemat : {rupiah(hasil['hemat_total'])}")
        elif args.perintah == "banding":
            akhir_a, hemat_a, _ = terapkan_promo(args.harga, args.promo_a)
            akhir_b, hemat_b, _ = terapkan_promo(args.harga, args.promo_b)
            print("\nPerbandingan promo")
            print("-" * 46)
            print(f"Promo A ({args.promo_a}): {rupiah(akhir_a)}  (hemat {rupiah(hemat_a)})")
            print(f"Promo B ({args.promo_b}): {rupiah(akhir_b)}  (hemat {rupiah(hemat_b)})")
            if akhir_a < akhir_b:
                print(f"Promo A lebih murah {rupiah(akhir_b - akhir_a)}.")
            elif akhir_b < akhir_a:
                print(f"Promo B lebih murah {rupiah(akhir_a - akhir_b)}.")
            else:
                print("Kedua promo sama murahnya.")
        elif args.perintah == "hemat":
            akhir, hemat = hitung_diskon(args.harga, args.persen)
            print(f"Harga {rupiah(args.harga)} diskon {persen_str(args.persen)}: "
                  f"bayar {rupiah(akhir)}, hemat {rupiah(hemat)}.")
    except ValueError as err:
        print(f"Gagal menghitung: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
