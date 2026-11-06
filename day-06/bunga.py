#!/usr/bin/env python3
"""Kalkulator Bunga Majemuk & Simulasi Tabungan.

Proyek harian ke-6: program terminal untuk mensimulasikan pertumbuhan
tabungan dengan bunga majemuk (bunga berbunga) dan setoran rutin bulanan.

Fitur:
  1. Hitung nilai akhir tabungan setelah sejumlah tahun.
  2. Hitung berapa lama sampai dana mencapai target tertentu.
  3. Hitung setoran bulanan yang dibutuhkan untuk mencapai target.
  4. Tabel pertumbuhan tahunan (pokok, setoran, bunga, dan total).

Bunga dihitung majemuk per bulan (bunga tahunan dibagi 12), dan setoran
bulanan dihitung masuk di akhir bulan. Hanya memakai pustaka standar
Python, tanpa pustaka tambahan.

Cara memakai (mode interaktif):
    python3 bunga.py

Cara memakai (baris perintah):
    python3 bunga.py tumbuh --pokok 1000000 --bunga 6 --tahun 5 --setoran 500000
    python3 bunga.py target --pokok 1000000 --bunga 6 --setoran 500000 --target 50000000
    python3 bunga.py setoran --pokok 1000000 --bunga 6 --tahun 5 --target 50000000
    python3 bunga.py tabel --pokok 1000000 --bunga 6 --tahun 5 --setoran 500000

Angka uang boleh ditulis polos (1000000) atau memakai pemisah ribuan
(1.000.000). Bunga ditulis dalam persen per tahun, contoh: 6 berarti 6%.
"""

import argparse
import math
import sys


# ---------------------------------------------------------------------------
# Format dan parsing angka
# ---------------------------------------------------------------------------

def format_rupiah(nilai):
    """Format angka menjadi teks rupiah, contoh: 1234567 -> 'Rp1.234.567'.

    Nilai negatif diberi tanda minus di depan Rp.
    """
    bulat = int(round(nilai))
    tanda = "-" if bulat < 0 else ""
    angka = f"{abs(bulat):,}".replace(",", ".")
    return f"{tanda}Rp{angka}"


def parse_uang(teks):
    """Ubah teks menjadi angka (float).

    Menerima '1000000', '1.000.000', 'Rp1.000.000', '1,5' (1,5 juta
    ditulis 1500000 saja lebih aman, tapi koma desimal juga diterima),
    serta spasi dan garis bawah sebagai pemisah ribuan.
    """
    teks = teks.strip().lower().replace("rp", "").replace(" ", "").replace("_", "")
    if not teks:
        raise ValueError("masukan kosong")
    if "." in teks and "," in teks:
        # Contoh: 1.000.000,50 -> titik ribuan, koma desimal.
        teks = teks.replace(".", "").replace(",", ".")
    elif "," in teks:
        # Hanya koma: anggap koma desimal, contoh: 1,5
        teks = teks.replace(",", ".")
    elif teks.count(".") > 1:
        # Beberapa titik: anggap pemisah ribuan, contoh: 1.000.000
        teks = teks.replace(".", "")
    return float(teks)


# ---------------------------------------------------------------------------
# Rumus bunga majemuk (compounding bulanan, setoran di akhir bulan)
# ---------------------------------------------------------------------------

def _suku_bunga_bulanan(bunga_tahunan):
    return bunga_tahunan / 100.0 / 12.0


def hitung_nilai_akhir(pokok, bunga_tahunan, tahun, setoran=0.0):
    """Nilai akhir tabungan setelah `tahun` tahun.

    pokok        : dana awal (Rp)
    bunga_tahunan: persen per tahun, contoh 6 berarti 6% per tahun
    tahun        : jangka waktu dalam tahun (boleh desimal, contoh 2.5)
    setoran      : setoran rutin tiap bulan (Rp, default 0)
    """
    if tahun < 0 or pokok < 0 or setoran < 0 or bunga_tahunan < 0:
        raise ValueError("pokok, bunga, tahun, dan setoran tidak boleh negatif")
    r = _suku_bunga_bulanan(bunga_tahunan)
    n = tahun * 12.0
    if r == 0:
        return pokok + setoran * n
    faktor = (1.0 + r) ** n
    return pokok * faktor + setoran * (faktor - 1.0) / r


def hitung_tahun_ke_target(pokok, bunga_tahunan, setoran, target):
    """Berapa tahun sampai dana mencapai `target`.

    Mengembalikan jumlah tahun (float), 0.0 bila target sudah tercapai,
    atau None bila target tidak akan pernah tercapai (misalnya tanpa
    bunga dan tanpa setoran, sedangkan target di atas pokok).
    """
    if target <= pokok:
        return 0.0
    if bunga_tahunan < 0 or pokok < 0 or setoran < 0:
        raise ValueError("pokok, bunga, dan setoran tidak boleh negatif")
    r = _suku_bunga_bulanan(bunga_tahunan)
    if r == 0:
        if setoran == 0:
            return None
        return (target - pokok) / setoran / 12.0
    # Selesaikan (1+r)^n dari rumus nilai akhir:
    #   target = pokok*x + setoran*(x-1)/r, dengan x = (1+r)^n
    #   x = (target + setoran/r) / (pokok + setoran/r)
    x = (target + setoran / r) / (pokok + setoran / r)
    if x <= 1.0:
        return 0.0
    return math.log(x) / math.log(1.0 + r) / 12.0


def hitung_setoran(pokok, bunga_tahunan, tahun, target):
    """Setoran bulanan yang dibutuhkan agar dana mencapai `target`
    dalam `tahun` tahun. Mengembalikan 0 bila pokok saja sudah cukup
    (dengan bunga) untuk mencapai target.
    """
    if tahun <= 0:
        raise ValueError("jangka waktu harus lebih dari 0 tahun")
    if bunga_tahunan < 0 or pokok < 0:
        raise ValueError("pokok dan bunga tidak boleh negatif")
    r = _suku_bunga_bulanan(bunga_tahunan)
    n = tahun * 12.0
    if r == 0:
        kurang = target - pokok
        return max(0.0, kurang / n)
    faktor = (1.0 + r) ** n
    kurang = target - pokok * faktor
    if kurang <= 0:
        return 0.0
    return kurang * r / (faktor - 1.0)


def tabel_pertumbuhan(pokok, bunga_tahunan, tahun, setoran=0.0):
    """Daftar pertumbuhan per tahun.

    Mengembalikan list berisi tuple (tahun_ke, nilai_akhir,
    total_setoran_kumulatif, total_bunga_kumulatif). Tahun dibulatkan
    ke bawah untuk baris tabel; bila jangka waktu bukan bilangan bulat,
    baris terakhir memakai tahun penuh terakhir yang terlewati.
    """
    if tahun < 1:
        raise ValueError("tabel butuh jangka waktu minimal 1 tahun")
    baris = []
    tahun_penuh = int(tahun)
    for t in range(1, tahun_penuh + 1):
        nilai = hitung_nilai_akhir(pokok, bunga_tahunan, t, setoran)
        total_setoran = pokok + setoran * 12 * t
        baris.append((t, nilai, total_setoran, nilai - total_setoran))
    return baris


# ---------------------------------------------------------------------------
# Tampilan hasil
# ---------------------------------------------------------------------------

def tampilkan_ringkasan(pokok, bunga_tahunan, tahun, setoran, nilai_akhir):
    total_setoran = pokok + setoran * 12 * tahun
    total_bunga = nilai_akhir - total_setoran
    print("=== Hasil Simulasi ===")
    print(f"Pokok awal     : {format_rupiah(pokok)}")
    print(f"Setoran/bulan  : {format_rupiah(setoran)}")
    print(f"Bunga          : {bunga_tahunan:g}% per tahun (majemuk bulanan)")
    print(f"Jangka waktu   : {tahun:g} tahun")
    print(f"Total disetor  : {format_rupiah(total_setoran)}")
    print(f"Total bunga    : {format_rupiah(total_bunga)}")
    print(f"Nilai akhir    : {format_rupiah(nilai_akhir)}")
    if total_setoran > 0:
        print(f"Pertumbuhan    : {100.0 * (nilai_akhir - total_setoran) / total_setoran:.1f}% dari total setoran")


def tampilkan_tabel(pokok, bunga_tahunan, tahun, setoran):
    baris = tabel_pertumbuhan(pokok, bunga_tahunan, tahun, setoran)
    print(f"=== Tabel Pertumbuhan ({bunga_tahunan:g}% per tahun, setoran {format_rupiah(setoran)}/bulan) ===")
    print(f"{'Tahun':>5}  {'Nilai Akhir':>14}  {'Total Disetor':>14}  {'Bunga Didapat':>14}")
    for t, nilai, total_setoran, total_bunga in baris:
        print(f"{t:>5}  {format_rupiah(nilai):>14}  {format_rupiah(total_setoran):>14}  {format_rupiah(total_bunga):>14}")


def tampilkan_target(pokok, bunga_tahunan, setoran, target, tahun):
    if tahun is None:
        print(f"Target {format_rupiah(target)} tidak akan tercapai")
        print("dengan pokok, bunga, dan setoran tersebut.")
        print("Naikkan setoran atau cari bunga yang lebih tinggi.")
        return
    tahun_penuh = int(tahun)
    bulan_sisa = int(round((tahun - tahun_penuh) * 12))
    if bulan_sisa == 12:
        tahun_penuh += 1
        bulan_sisa = 0
    print("=== Waktu Menuju Target ===")
    print(f"Pokok awal     : {format_rupiah(pokok)}")
    print(f"Setoran/bulan  : {format_rupiah(setoran)}")
    print(f"Bunga          : {bunga_tahunan:g}% per tahun (majemuk bulanan)")
    print(f"Target         : {format_rupiah(target)}")
    print(f"Waktu          : {tahun_penuh} tahun {bulan_sisa} bulan ({tahun:.1f} tahun)")


# ---------------------------------------------------------------------------
# Mode interaktif
# ---------------------------------------------------------------------------

def baca_angka(pesan, boleh_nol=True, default=None):
    """Baca angka dari pengguna, ulangi bila masukan tidak valid."""
    while True:
        try:
            teks = input(pesan).strip()
            if default is not None and teks == "":
                return default
            nilai = parse_uang(teks)
        except ValueError:
            print("  Masukan tidak valid, coba lagi (contoh: 1000000).")
            continue
        if nilai < 0 or (not boleh_nol and nilai == 0):
            print("  Nilai harus lebih dari 0, coba lagi.")
            continue
        return nilai


def mode_interaktif():
    print("=== Kalkulator Bunga Majemuk & Simulasi Tabungan ===")
    print("Bunga dihitung majemuk per bulan; setoran masuk di akhir bulan.")
    while True:
        print()
        print("Menu:")
        print("  1. Hitung nilai akhir tabungan")
        print("  2. Hitung lama menuju target dana")
        print("  3. Hitung setoran bulanan yang dibutuhkan")
        print("  4. Tabel pertumbuhan tahunan")
        print("  0. Keluar")
        pilihan = input("Pilih menu (0-4): ").strip()
        if pilihan == "0":
            print("Sampai jumpa, tetap konsisten menabung!")
            return
        if pilihan not in ("1", "2", "3", "4"):
            print("Pilihan tidak ada, pilih 0-4.")
            continue
        pokok = baca_angka("Pokok awal (Rp): ")
        bunga = baca_angka("Bunga per tahun (%): ")
        if pilihan == "1":
            tahun = baca_angka("Jangka waktu (tahun): ", boleh_nol=False)
            setoran = baca_angka("Setoran per bulan (Rp, Enter = 0): ", default=0.0)
            nilai = hitung_nilai_akhir(pokok, bunga, tahun, setoran)
            print()
            tampilkan_ringkasan(pokok, bunga, tahun, setoran, nilai)
        elif pilihan == "2":
            setoran = baca_angka("Setoran per bulan (Rp, Enter = 0): ", default=0.0)
            target = baca_angka("Target dana (Rp): ", boleh_nol=False)
            tahun = hitung_tahun_ke_target(pokok, bunga, setoran, target)
            print()
            tampilkan_target(pokok, bunga, setoran, target, tahun)
        elif pilihan == "3":
            tahun = baca_angka("Jangka waktu (tahun): ", boleh_nol=False)
            target = baca_angka("Target dana (Rp): ", boleh_nol=False)
            perlu = hitung_setoran(pokok, bunga, tahun, target)
            print()
            if perlu == 0:
                print("Pokok awal saja sudah cukup mencapai target")
                print("dengan bunga tersebut, tanpa setoran tambahan.")
            else:
                print("=== Setoran Bulanan yang Dibutuhkan ===")
                print(f"Pokok awal     : {format_rupiah(pokok)}")
                print(f"Bunga          : {bunga:g}% per tahun (majemuk bulanan)")
                print(f"Jangka waktu   : {tahun:g} tahun")
                print(f"Target         : {format_rupiah(target)}")
                print(f"Setoran/bulan  : {format_rupiah(perlu)}")
        elif pilihan == "4":
            tahun = baca_angka("Jangka waktu (tahun): ", boleh_nol=False)
            setoran = baca_angka("Setoran per bulan (Rp, Enter = 0): ", default=0.0)
            print()
            tampilkan_tabel(pokok, bunga, tahun, setoran)


# ---------------------------------------------------------------------------
# Baris perintah
# ---------------------------------------------------------------------------

def _tambah_argumen_umum(parser):
    parser.add_argument("--pokok", type=parse_uang, default=0.0,
                        help="dana awal dalam rupiah (default: 0)")
    parser.add_argument("--bunga", type=float, default=6.0,
                        help="bunga per tahun dalam persen (default: 6)")
    parser.add_argument("--setoran", type=parse_uang, default=0.0,
                        help="setoran rutin tiap bulan dalam rupiah (default: 0)")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Kalkulator bunga majemuk & simulasi tabungan.")
    sub = parser.add_subparsers(dest="perintah")

    p_tumbuh = sub.add_parser("tumbuh", help="hitung nilai akhir tabungan")
    _tambah_argumen_umum(p_tumbuh)
    p_tumbuh.add_argument("--tahun", type=float, required=True,
                          help="jangka waktu dalam tahun")

    p_target = sub.add_parser("target", help="hitung lama menuju target dana")
    _tambah_argumen_umum(p_target)
    p_target.add_argument("--target", type=parse_uang, required=True,
                          help="target dana dalam rupiah")

    p_setoran = sub.add_parser("setoran", help="hitung setoran bulanan yang dibutuhkan")
    _tambah_argumen_umum(p_setoran)
    p_setoran.add_argument("--tahun", type=float, required=True,
                           help="jangka waktu dalam tahun")
    p_setoran.add_argument("--target", type=parse_uang, required=True,
                           help="target dana dalam rupiah")

    p_tabel = sub.add_parser("tabel", help="tabel pertumbuhan tahunan")
    _tambah_argumen_umum(p_tabel)
    p_tabel.add_argument("--tahun", type=float, required=True,
                         help="jangka waktu dalam tahun")

    args = parser.parse_args(argv)
    if args.perintah is None:
        try:
            mode_interaktif()
        except (KeyboardInterrupt, EOFError):
            print("\nDibatalkan.")
        return 0

    if args.bunga < 0 or args.pokok < 0 or args.setoran < 0:
        print("Error: pokok, bunga, dan setoran tidak boleh negatif.", file=sys.stderr)
        return 2

    if args.perintah == "tumbuh":
        if args.tahun <= 0:
            print("Error: jangka waktu harus lebih dari 0 tahun.", file=sys.stderr)
            return 2
        nilai = hitung_nilai_akhir(args.pokok, args.bunga, args.tahun, args.setoran)
        tampilkan_ringkasan(args.pokok, args.bunga, args.tahun, args.setoran, nilai)
    elif args.perintah == "target":
        if args.target <= 0:
            print("Error: target harus lebih dari 0.", file=sys.stderr)
            return 2
        tahun = hitung_tahun_ke_target(args.pokok, args.bunga, args.setoran, args.target)
        tampilkan_target(args.pokok, args.bunga, args.setoran, args.target, tahun)
    elif args.perintah == "setoran":
        if args.tahun <= 0 or args.target <= 0:
            print("Error: jangka waktu dan target harus lebih dari 0.", file=sys.stderr)
            return 2
        perlu = hitung_setoran(args.pokok, args.bunga, args.tahun, args.target)
        if perlu == 0:
            print("Pokok awal saja sudah cukup mencapai target")
            print("dengan bunga tersebut, tanpa setoran tambahan.")
        else:
            print(f"Setoran/bulan yang dibutuhkan: {format_rupiah(perlu)}")
            print(f"untuk mencapai {format_rupiah(args.target)} dalam {args.tahun:g} tahun")
            print(f"dari pokok {format_rupiah(args.pokok)} dengan bunga {args.bunga:g}% per tahun.")
    elif args.perintah == "tabel":
        if args.tahun < 1:
            print("Error: tabel butuh jangka waktu minimal 1 tahun.", file=sys.stderr)
            return 2
        tampilkan_tabel(args.pokok, args.bunga, args.tahun, args.setoran)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
