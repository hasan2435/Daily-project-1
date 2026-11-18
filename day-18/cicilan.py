#!/usr/bin/env python3
"""Kalkulator Cicilan Kredit - Day 18.

Hitung cicilan bulanan pinjaman (KPR, kredit kendaraan, pinjaman
pribadi) dengan sistem anuitas, lihat tabel amortisasi, simulasikan
pelunasan dipercepat, dan bandingkan dua penawaran kredit.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

Cara pakai:
    python3 cicilan.py
    python3 cicilan.py hitung 100000000 12 12
    python3 cicilan.py tabel 100000000 12 12
    python3 cicilan.py lunas 100000000 12 12 2000000
    python3 cicilan.py banding 100000000 10 12 12 24
    python3 cicilan.py flat 100000000 12 12
"""

import argparse
import sys


def format_rp(nilai):
    """Format angka menjadi rupiah, misal 1000000 -> 'Rp1.000.000'."""
    nilai = int(round(nilai))
    teks = f"{abs(nilai):,}".replace(",", ".")
    return f"Rp{teks}" if nilai >= 0 else f"-Rp{teks}"


def cicilan_anuitas(pokok, bunga_tahunan, tenor_bulan):
    """Cicilan bulanan tetap dengan bunga anuitas (efektif).

    bunga_tahunan dalam persen per tahun, tenor_bulan dalam bulan.
    """
    if pokok <= 0:
        raise ValueError("Pokok pinjaman harus lebih dari 0.")
    if bunga_tahunan < 0:
        raise ValueError("Bunga tidak boleh negatif.")
    if tenor_bulan <= 0:
        raise ValueError("Tenor harus lebih dari 0 bulan.")
    suku_bulan = bunga_tahunan / 100.0 / 12.0
    if suku_bulan == 0:
        return pokok / tenor_bulan
    faktor = (1 + suku_bulan) ** tenor_bulan
    return pokok * suku_bulan * faktor / (faktor - 1)


def cicilan_flat(pokok, bunga_tahunan, tenor_bulan):
    """Cicilan bulanan dengan bunga flat (bunga dihitung dari pokok awal)."""
    if pokok <= 0:
        raise ValueError("Pokok pinjaman harus lebih dari 0.")
    if bunga_tahunan < 0:
        raise ValueError("Bunga tidak boleh negatif.")
    if tenor_bulan <= 0:
        raise ValueError("Tenor harus lebih dari 0 bulan.")
    total_bunga = pokok * (bunga_tahunan / 100.0) * (tenor_bulan / 12.0)
    return (pokok + total_bunga) / tenor_bulan, total_bunga


def amortisasi(pokok, bunga_tahunan, tenor_bulan, tambahan=0.0):
    """Hasilkan daftar angsuran bulanan.

    Tiap baris: (bulan, cicilan, bagian_bunga, bagian_pokok, sisa).
    `tambahan` adalah setoran ekstra tiap bulan untuk pelunasan
    dipercepat; 0 berarti cicilan normal sampai tenor habis.
    """
    suku_bulan = bunga_tahunan / 100.0 / 12.0
    cicilan = cicilan_anuitas(pokok, bunga_tahunan, tenor_bulan)
    sisa = float(pokok)
    baris = []
    bulan = 0
    while sisa > 0.005 and bulan < tenor_bulan * 5 + 60:
        bulan += 1
        bunga_bulan = sisa * suku_bulan
        bayar = cicilan + tambahan
        if bayar > sisa + bunga_bulan:
            bayar = sisa + bunga_bulan
        bagian_pokok = bayar - bunga_bulan
        sisa -= bagian_pokok
        if sisa < 0.005:
            sisa = 0.0
        baris.append((bulan, bayar, bunga_bulan, bagian_pokok, sisa))
        if sisa == 0.0:
            break
    return baris


def ringkasan(pokok, bunga_tahunan, tenor_bulan):
    """Hitung ringkasan kredit: cicilan, total bayar, total bunga."""
    cicilan = cicilan_anuitas(pokok, bunga_tahunan, tenor_bulan)
    total_bayar = cicilan * tenor_bulan
    return cicilan, total_bayar, total_bayar - pokok


def tampilkan_ringkasan(pokok, bunga_tahunan, tenor_bulan):
    cicilan, total_bayar, total_bunga = ringkasan(pokok, bunga_tahunan,
                                                  tenor_bulan)
    print()
    print("=== Ringkasan Kredit ===")
    print(f"Pokok pinjaman : {format_rp(pokok)}")
    print(f"Bunga tahunan  : {bunga_tahunan:g}% (anuitas/efektif)")
    print(f"Tenor          : {tenor_bulan} bulan "
          f"({tenor_bulan / 12:g} tahun)")
    print(f"Cicilan/bulan  : {format_rp(cicilan)}")
    print(f"Total dibayar  : {format_rp(total_bayar)}")
    print(f"Total bunga    : {format_rp(total_bunga)}")
    print(f"Bunga/pokok    : {total_bunga / pokok * 100:.1f}% dari pokok")
    return cicilan, total_bayar, total_bunga


def tampilkan_tabel(pokok, bunga_tahunan, tenor_bulan):
    baris = amortisasi(pokok, bunga_tahunan, tenor_bulan)
    tampilkan_ringkasan(pokok, bunga_tahunan, tenor_bulan)
    print()
    print("=== Tabel Amortisasi (per tahun) ===")
    print(f"{'Tahun':>5} {'Cicilan':>16} {'Bunga':>16} "
          f"{'Pokok':>16} {'Sisa':>16}")
    tahun = {}
    for bulan, bayar, bunga, bagian_pokok, sisa in baris:
        thn = (bulan - 1) // 12 + 1
        akum = tahun.setdefault(thn, [0.0, 0.0, 0.0, 0.0])
        akum[0] += bayar
        akum[1] += bunga
        akum[2] += bagian_pokok
        akum[3] = sisa
    for thn in sorted(tahun):
        cicil, bunga, bagian_pokok, sisa = tahun[thn]
        print(f"{thn:>5} {format_rp(cicil):>16} {format_rp(bunga):>16} "
              f"{format_rp(bagian_pokok):>16} {format_rp(sisa):>16}")
    if tenor_bulan <= 24:
        print()
        print("=== Rincian per bulan ===")
        print(f"{'Bln':>4} {'Cicilan':>16} {'Bunga':>16} "
              f"{'Pokok':>16} {'Sisa':>16}")
        for bulan, bayar, bunga, bagian_pokok, sisa in baris:
            print(f"{bulan:>4} {format_rp(bayar):>16} "
                  f"{format_rp(bunga):>16} {format_rp(bagian_pokok):>16} "
                  f"{format_rp(sisa):>16}")


def tampilkan_lunas(pokok, bunga_tahunan, tenor_bulan, tambahan):
    cicilan, total_bayar, total_bunga = ringkasan(pokok, bunga_tahunan,
                                                  tenor_bulan)
    baris = amortisasi(pokok, bunga_tahunan, tenor_bulan, tambahan)
    bulan_lunas = len(baris)
    total_cepat = sum(b[1] for b in baris)
    bunga_cepat = total_cepat - pokok
    print()
    print("=== Simulasi Pelunasan Dipercepat ===")
    print(f"Pokok pinjaman : {format_rp(pokok)}")
    print(f"Bunga tahunan  : {bunga_tahunan:g}%")
    print(f"Cicilan normal : {format_rp(cicilan)} "
          f"selama {tenor_bulan} bulan")
    print(f"Tambahan/bulan : {format_rp(tambahan)} "
          f"(total bayar {format_rp(cicilan + tambahan)}/bulan)")
    print()
    print(f"Lunas dalam    : {bulan_lunas} bulan "
          f"({bulan_lunas / 12:.1f} tahun)")
    print(f"Lebih cepat    : {tenor_bulan - bulan_lunas} bulan")
    print(f"Total dibayar  : {format_rp(total_cepat)}")
    print(f"Total bunga    : {format_rp(bunga_cepat)}")
    print(f"Hemat bunga    : {format_rp(total_bunga - bunga_cepat)} "
          f"({(total_bunga - bunga_cepat) / total_bunga * 100:.1f}% "
          f"dari bunga normal)")
    if bulan_lunas >= tenor_bulan:
        print("Tambahan terlalu kecil untuk mempercepat pelunasan.")


def tampilkan_banding(pokok, bunga1, tenor1, bunga2, tenor2):
    cicil1, total1, bunga_total1 = ringkasan(pokok, bunga1, tenor1)
    cicil2, total2, bunga_total2 = ringkasan(pokok, bunga2, tenor2)
    print()
    print("=== Bandingkan Dua Penawaran ===")
    print(f"Pokok pinjaman : {format_rp(pokok)}")
    print()
    print(f"{'':>16} {'A':>18} {'B':>18}")
    print(f"{'Bunga/tahun':>16} {bunga1:>17g}% {bunga2:>17g}%")
    print(f"{'Tenor':>16} {tenor1:>15} bln {tenor2:>15} bln")
    print(f"{'Cicilan/bulan':>16} {format_rp(cicil1):>18} "
          f"{format_rp(cicil2):>18}")
    print(f"{'Total dibayar':>16} {format_rp(total1):>18} "
          f"{format_rp(total2):>18}")
    print(f"{'Total bunga':>16} {format_rp(bunga_total1):>18} "
          f"{format_rp(bunga_total2):>18}")
    print()
    if total1 < total2:
        selisih_bulan = cicil1 - cicil2
        if selisih_bulan >= 0:
            print(f"Penawaran A lebih murah {format_rp(total2 - total1)} "
                  f"(cicilan A {format_rp(selisih_bulan)}/bulan lebih "
                  f"mahal).")
        else:
            print(f"Penawaran A lebih murah {format_rp(total2 - total1)} "
                  f"(cicilan A {format_rp(-selisih_bulan)}/bulan lebih "
                  f"murah).")
    elif total2 < total1:
        selisih_bulan = cicil2 - cicil1
        if selisih_bulan >= 0:
            print(f"Penawaran B lebih murah {format_rp(total1 - total2)} "
                  f"(cicilan B {format_rp(selisih_bulan)}/bulan lebih "
                  f"mahal).")
        else:
            print(f"Penawaran B lebih murah {format_rp(total1 - total2)} "
                  f"(cicilan B {format_rp(-selisih_bulan)}/bulan lebih "
                  f"murah).")
    else:
        print("Kedua penawaran sama total biayanya.")
    print("Catatan: cicilan yang lebih kecil belum tentu lebih murah — "
          "cek total bunga.")


def tampilkan_flat(pokok, bunga_tahunan, tenor_bulan):
    cicil_flat, total_bunga_flat = cicilan_flat(pokok, bunga_tahunan,
                                                tenor_bulan)
    cicil_efektif, total_efektif, total_bunga_efektif = ringkasan(
        pokok, bunga_tahunan, tenor_bulan)
    print()
    print("=== Bunga Flat vs Anuitas (Efektif) ===")
    print(f"Pokok pinjaman : {format_rp(pokok)}")
    print(f"Bunga tahunan  : {bunga_tahunan:g}%")
    print(f"Tenor          : {tenor_bulan} bulan")
    print()
    print(f"Cicilan flat   : {format_rp(cicil_flat)}/bulan, "
          f"total bunga {format_rp(total_bunga_flat)}")
    print(f"Cicilan efektif: {format_rp(cicil_efektif)}/bulan, "
          f"total bunga {format_rp(total_bunga_efektif)}")
    print()
    print(f"Flat lebih mahal {format_rp(total_bunga_flat - total_bunga_efektif)} "
          f"dari anuitas pada bunga nominal yang sama, karena bunga flat "
          f"dihitung dari pokok awal setiap bulan.")


def baca_angka(pesan, minimum=None):
    while True:
        mentah = input(pesan).strip().replace(".", "").replace(",", ".")
        try:
            nilai = float(mentah)
        except ValueError:
            print("Masukkan angka yang benar, contoh: 100000000")
            continue
        if minimum is not None and nilai < minimum:
            print(f"Nilainya minimal {minimum}.")
            continue
        return nilai


def mode_interaktif():
    print("=== Kalkulator Cicilan Kredit ===")
    print("1. Hitung cicilan bulanan")
    print("2. Tabel amortisasi")
    print("3. Simulasi pelunasan dipercepat")
    print("4. Bandingkan dua penawaran")
    print("5. Bunga flat vs anuitas")
    print("0. Keluar")
    pilihan = input("Pilih (0-5): ").strip()
    if pilihan == "0":
        return
    if pilihan == "4":
        pokok = baca_angka("Pokok pinjaman (Rp): ", 1)
        print("Penawaran A:")
        bunga1 = baca_angka("  Bunga per tahun (%): ", 0)
        tenor1 = int(baca_angka("  Tenor (bulan): ", 1))
        print("Penawaran B:")
        bunga2 = baca_angka("  Bunga per tahun (%): ", 0)
        tenor2 = int(baca_angka("  Tenor (bulan): ", 1))
        tampilkan_banding(pokok, bunga1, tenor1, bunga2, tenor2)
        return
    pokok = baca_angka("Pokok pinjaman (Rp): ", 1)
    bunga = baca_angka("Bunga per tahun (%): ", 0)
    tenor = int(baca_angka("Tenor (bulan): ", 1))
    if pilihan == "1":
        tampilkan_ringkasan(pokok, bunga, tenor)
    elif pilihan == "2":
        tampilkan_tabel(pokok, bunga, tenor)
    elif pilihan == "3":
        tambahan = baca_angka("Tambahan bayar per bulan (Rp): ", 1)
        tampilkan_lunas(pokok, bunga, tenor, tambahan)
    elif pilihan == "5":
        tampilkan_flat(pokok, bunga, tenor)
    else:
        print("Pilihan tidak dikenal.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Kalkulator cicilan kredit (anuitas) di terminal.")
    sub = parser.add_subparsers(dest="perintah")

    p_hitung = sub.add_parser("hitung", help="Hitung cicilan bulanan.")
    p_hitung.add_argument("pokok", type=float)
    p_hitung.add_argument("bunga", type=float)
    p_hitung.add_argument("tenor", type=int)

    p_tabel = sub.add_parser("tabel", help="Tampilkan tabel amortisasi.")
    p_tabel.add_argument("pokok", type=float)
    p_tabel.add_argument("bunga", type=float)
    p_tabel.add_argument("tenor", type=int)

    p_lunas = sub.add_parser("lunas",
                             help="Simulasi pelunasan dipercepat.")
    p_lunas.add_argument("pokok", type=float)
    p_lunas.add_argument("bunga", type=float)
    p_lunas.add_argument("tenor", type=int)
    p_lunas.add_argument("tambahan", type=float)

    p_banding = sub.add_parser("banding",
                               help="Bandingkan dua penawaran kredit.")
    p_banding.add_argument("pokok", type=float)
    p_banding.add_argument("bunga1", type=float)
    p_banding.add_argument("tenor1", type=int)
    p_banding.add_argument("bunga2", type=float)
    p_banding.add_argument("tenor2", type=int)

    p_flat = sub.add_parser("flat",
                            help="Bandingkan bunga flat dan anuitas.")
    p_flat.add_argument("pokok", type=float)
    p_flat.add_argument("bunga", type=float)
    p_flat.add_argument("tenor", type=int)

    args = parser.parse_args(argv)
    try:
        if args.perintah == "hitung":
            tampilkan_ringkasan(args.pokok, args.bunga, args.tenor)
        elif args.perintah == "tabel":
            tampilkan_tabel(args.pokok, args.bunga, args.tenor)
        elif args.perintah == "lunas":
            tampilkan_lunas(args.pokok, args.bunga, args.tenor,
                            args.tambahan)
        elif args.perintah == "banding":
            tampilkan_banding(args.pokok, args.bunga1, args.tenor1,
                              args.bunga2, args.tenor2)
        elif args.perintah == "flat":
            tampilkan_flat(args.pokok, args.bunga, args.tenor)
        else:
            mode_interaktif()
    except ValueError as err:
        print(f"Galat: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
