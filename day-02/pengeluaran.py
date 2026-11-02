#!/usr/bin/env python3
"""Pencatat Pengeluaran Harian.

Program terminal kecil untuk mencatat pengeluaran sehari-hari dan
melihat totalnya, baik total keseluruhan maupun per kategori.

Hanya memakai pustaka standar Python, tanpa library tambahan.
Data disimpan di berkas pengeluaran.json pada folder tempat program
dijalankan, sehingga data tidak ikut terbawa saat berkas program
disalin ke tempat lain.

Penggunaan:
    python3 pengeluaran.py                  # menu interaktif
    python3 pengeluaran.py tambah 50000 makan "Makan siang"
    python3 pengeluaran.py tambah 25000 transport --tanggal 2026-11-02
    python3 pengeluaran.py daftar
    python3 pengeluaran.py daftar --kategori makan
    python3 pengeluaran.py total
    python3 pengeluaran.py total --dari 2026-11-01 --sampai 2026-11-30
    python3 pengeluaran.py hapus 2 --ya
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

DATA_FILE = Path("pengeluaran.json")


def parse_nominal(teks):
    """Ubah teks nominal menjadi bilangan bulat rupiah.

    Menerima '50000', '50.000', 'Rp 50.000', dan '50000,50'.
    """
    bersih = teks.strip().lower().replace("rp", "").replace(" ", "")
    bersih = bersih.replace(".", "").replace(",", ".")
    try:
        nilai = float(bersih)
    except ValueError:
        raise ValueError("Nominal tidak valid: %r" % teks)
    if nilai <= 0:
        raise ValueError("Nominal harus lebih dari 0.")
    return int(nilai) if nilai.is_integer() else nilai


def parse_tanggal(teks):
    """Validasi tanggal berformat YYYY-MM-DD, kembalikan teks yang sama."""
    try:
        tahun, bulan, hari = (int(bagian) for bagian in teks.split("-"))
        date(tahun, bulan, hari)
    except (ValueError, AttributeError):
        raise ValueError("Tanggal harus berformat YYYY-MM-DD, contoh: 2026-11-02")
    return teks


def muat_data():
    """Baca daftar pengeluaran dari berkas JSON, atau [] jika belum ada."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open(encoding="utf-8") as berkas:
            data = json.load(berkas)
    except (json.JSONDecodeError, OSError) as err:
        print("Berkas data rusak atau tidak bisa dibaca: %s" % err, file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, list):
        print("Berkas data tidak berisi daftar pengeluaran.", file=sys.stderr)
        sys.exit(1)
    return data


def simpan_data(data):
    """Simpan daftar pengeluaran ke berkas JSON."""
    with DATA_FILE.open("w", encoding="utf-8") as berkas:
        json.dump(data, berkas, indent=2, ensure_ascii=False)
        berkas.write("\n")


def format_rupiah(nilai):
    """Format angka menjadi teks rupiah, contoh: Rp50.000."""
    if isinstance(nilai, float) and not nilai.is_integer():
        return "Rp{:,.2f}".format(nilai).replace(",", "X").replace(".", ",").replace("X", ".")
    return "Rp{:,}".format(int(nilai)).replace(",", ".")


def urutkan(data):
    """Urutkan pengeluaran berdasarkan tanggal, lalu urutan input."""
    return sorted(enumerate(data), key=lambda item: (item[1]["tanggal"], item[0]))


def saring(data, kategori=None, dari_tanggal=None, sampai_tanggal=None):
    """Saring pengeluaran berdasarkan kategori dan rentang tanggal."""
    hasil = []
    for item in data:
        if kategori and item["kategori"].lower() != kategori.lower():
            continue
        if dari_tanggal and item["tanggal"] < dari_tanggal:
            continue
        if sampai_tanggal and item["tanggal"] > sampai_tanggal:
            continue
        hasil.append(item)
    return hasil


def perintah_tambah(args):
    data = muat_data()
    try:
        nominal = parse_nominal(args.nominal)
        tanggal = parse_tanggal(args.tanggal) if args.tanggal else date.today().isoformat()
    except ValueError as err:
        print("Gagal: %s" % err, file=sys.stderr)
        return 1
    data.append({
        "tanggal": tanggal,
        "kategori": args.kategori,
        "nominal": nominal,
        "keterangan": args.keterangan,
    })
    simpan_data(data)
    print("Tercatat: %s | %s | %s | %s" % (tanggal, args.kategori, format_rupiah(nominal), args.keterangan))
    return 0


def perintah_daftar(args):
    data = saring(muat_data(), args.kategori, args.dari, args.sampai)
    if not data:
        print("Belum ada pengeluaran yang cocok.")
        return 0
    # Penomoran mengikuti urutan tampil (tanggal, lalu urutan input).
    tampil = sorted(data, key=lambda item: item["tanggal"])
    for nomor, item in enumerate(tampil, start=1):
        print("%d. %s | %-12s | %12s | %s" % (
            nomor, item["tanggal"], item["kategori"],
            format_rupiah(item["nominal"]), item["keterangan"]))
    print("Total %d pengeluaran: %s" % (len(tampil), format_rupiah(sum(i["nominal"] for i in tampil))))
    return 0


def perintah_total(args):
    data = saring(muat_data(), args.kategori, args.dari, args.sampai)
    if not data:
        print("Belum ada pengeluaran yang cocok.")
        return 0
    total = sum(item["nominal"] for item in data)
    print("Total: %s (%d pengeluaran)" % (format_rupiah(total), len(data)))
    print("Per kategori:")
    per_kategori = {}
    for item in data:
        per_kategori[item["kategori"]] = per_kategori.get(item["kategori"], 0) + item["nominal"]
    for kategori in sorted(per_kategori):
        print("  %-12s %s" % (kategori, format_rupiah(per_kategori[kategori])))
    return 0


def perintah_hapus(args):
    data = muat_data()
    tampil = [item for _, item in urutkan(data)]
    if not 1 <= args.nomor <= len(tampil):
        print("Nomor tidak ada. Lihat daftar dengan: python3 pengeluaran.py daftar", file=sys.stderr)
        return 1
    target = tampil[args.nomor - 1]
    if not args.ya:
        jawab = input("Hapus %s | %s | %s? (y/N) " % (
            target["tanggal"], target["kategori"], format_rupiah(target["nominal"]))).strip().lower()
        if jawab not in ("y", "ya"):
            print("Dibatalkan.")
            return 0
    data.remove(target)
    simpan_data(data)
    print("Dihapus: %s | %s | %s" % (target["tanggal"], target["kategori"], format_rupiah(target["nominal"])))
    return 0


def menu_interaktif():
    """Menu sederhana untuk pemakaian tanpa argumen baris perintah."""
    while True:
        print("\n=== Pencatat Pengeluaran Harian ===")
        print("1. Tambah pengeluaran")
        print("2. Lihat daftar")
        print("3. Lihat total")
        print("4. Hapus pengeluaran")
        print("0. Keluar")
        pilihan = input("Pilih [0-4]: ").strip()
        if pilihan == "0":
            print("Sampai jumpa!")
            return 0
        if pilihan == "1":
            nominal = input("Nominal (contoh: 50000): ").strip()
            kategori = input("Kategori (contoh: makan): ").strip() or "Lainnya"
            keterangan = input("Keterangan: ").strip() or "-"
            tanggal = input("Tanggal [YYYY-MM-DD, kosong = hari ini]: ").strip() or None
            perintah_tambah(argparse.Namespace(
                nominal=nominal, kategori=kategori, keterangan=keterangan, tanggal=tanggal))
        elif pilihan == "2":
            perintah_daftar(argparse.Namespace(kategori=None, dari=None, sampai=None))
        elif pilihan == "3":
            perintah_total(argparse.Namespace(kategori=None, dari=None, sampai=None))
        elif pilihan == "4":
            perintah_daftar(argparse.Namespace(kategori=None, dari=None, sampai=None))
            try:
                nomor = int(input("Nomor yang dihapus: ").strip())
            except ValueError:
                print("Nomor harus berupa angka.")
                continue
            perintah_hapus(argparse.Namespace(nomor=nomor, ya=False))
        else:
            print("Pilihan tidak dikenal, coba lagi.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Pencatat Pengeluaran Harian.")
    sub = parser.add_subparsers(dest="perintah")

    tambah = sub.add_parser("tambah", help="Tambah satu pengeluaran.")
    tambah.add_argument("nominal", help="Nominal, contoh: 50000 atau 50.000")
    tambah.add_argument("kategori", help="Kategori, contoh: makan")
    tambah.add_argument("keterangan", nargs="?", default="-", help="Keterangan singkat")
    tambah.add_argument("--tanggal", help="Tanggal YYYY-MM-DD (default: hari ini)")

    daftar = sub.add_parser("daftar", help="Tampilkan daftar pengeluaran.")
    daftar.add_argument("--kategori", help="Saring berdasarkan kategori")
    daftar.add_argument("--dari", help="Tanggal mulai YYYY-MM-DD")
    daftar.add_argument("--sampai", help="Tanggal akhir YYYY-MM-DD")

    total = sub.add_parser("total", help="Tampilkan total pengeluaran.")
    total.add_argument("--kategori", help="Saring berdasarkan kategori")
    total.add_argument("--dari", help="Tanggal mulai YYYY-MM-DD")
    total.add_argument("--sampai", help="Tanggal akhir YYYY-MM-DD")

    hapus = sub.add_parser("hapus", help="Hapus pengeluaran berdasarkan nomor di daftar.")
    hapus.add_argument("nomor", type=int, help="Nomor dari perintah daftar")
    hapus.add_argument("--ya", action="store_true", help="Lewati konfirmasi")

    args = parser.parse_args(argv)
    if args.perintah is None:
        return menu_interaktif()
    if args.perintah == "tambah":
        return perintah_tambah(args)
    if args.perintah == "daftar":
        return perintah_daftar(args)
    if args.perintah == "total":
        return perintah_total(args)
    if args.perintah == "hapus":
        return perintah_hapus(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
