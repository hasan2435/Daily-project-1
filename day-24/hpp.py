#!/usr/bin/env python3
"""Kalkulator HPP & Harga Jual — Day 24 Daily Project 1.

Hitung harga pokok produksi (HPP) per unit untuk usaha kecil —
misalnya jualan kopi, makanan, atau kerajinan — lalu tentukan
harga jual dari margin keuntungan yang diinginkan, titik impas
(BEP), dan perkiraan laba bulanan.

Rumus yang dipakai:
    HPP per unit = bahan baku + tenaga kerja + overhead per unit
    Harga jual   = HPP x (1 + margin / 100)
    BEP (unit)   = biaya tetap bulanan / (harga jual - HPP per unit)
    BEP (rupiah) = BEP unit x harga jual
    Laba bulanan = (harga jual - HPP) x unit terjual - biaya tetap

Biaya tetap adalah biaya yang keluar tiap bulan walau tidak ada
yang terjual: sewa tempat, gaji tetap, listrik, dan lain-lain.
Biaya variabel (bahan, tenaga kerja per unit, overhead per unit)
hanya keluar bila ada produksi.

Python standar saja, tanpa library tambahan.

Cara pakai:
    python3 hpp.py
    python3 hpp.py cepat 5000 2000 1000 --margin 30
    python3 hpp.py tambah "Kopi Gula Aren" 5000 2000 1000 --tetap 1500000 --target 300
    python3 hpp.py daftar
    python3 hpp.py hpp 1
    python3 hpp.py hpp 1 --margin 40
    python3 hpp.py jual 1 15000
    python3 hpp.py bep 1
    python3 hpp.py bep 1 --harga 15000
    python3 hpp.py laba 1 300
    python3 hpp.py laba 1 300 --harga 15000
    python3 hpp.py banding 1 12000 15000 --unit 300
    python3 hpp.py hapus 1 --ya

Jalankan tanpa argumen untuk mode interaktif (menu angka).

Data disimpan di berkas `hpp.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek.
"""

import argparse
import json
import math
import os
import sys

BERKAS_DATA = "hpp.json"


def rupiah(nilai):
    """Format angka menjadi Rp, contoh: Rp15.000."""
    return "Rp" + f"{round(nilai):,}".replace(",", ".")


def persen(nilai):
    """Format angka menjadi persen dengan satu angka di belakang koma."""
    return f"{nilai:.1f}%"


def hitung_hpp(bahan, tenaga, overhead):
    """HPP per unit: jumlah semua biaya variabel per unit."""
    return bahan + tenaga + overhead


def harga_dari_margin(hpp, margin):
    """Harga jual dari HPP dan margin keuntungan dalam persen."""
    return hpp * (1 + margin / 100)


def margin_dari_harga(hpp, harga):
    """Margin keuntungan dalam persen dari HPP dan harga jual."""
    if hpp <= 0:
        return 0
    return (harga - hpp) / hpp * 100


def hitung_bep(biaya_tetap, harga, hpp):
    """BEP dalam unit dan rupiah.

    Kembalikan (unit, rupiah) atau (None, None) bila harga jual
    tidak lebih besar dari HPP, karena tidak akan pernah impas.
    """
    selisih = harga - hpp
    if selisih <= 0:
        return None, None
    unit = math.ceil(biaya_tetap / selisih)
    return unit, unit * harga


def hitung_laba(harga, hpp, biaya_tetap, unit_terjual):
    """Laba (atau rugi) bulanan dari penjualan sejumlah unit."""
    return (harga - hpp) * unit_terjual - biaya_tetap


def muat_data():
    """Muat daftar produk dari berkas JSON, kembalikan list kosong bila belum ada."""
    if not os.path.exists(BERKAS_DATA):
        return []
    try:
        with open(BERKAS_DATA, "r", encoding="utf-8") as berkas:
            data = json.load(berkas)
    except (json.JSONDecodeError, OSError) as galat:
        print(f"Tidak bisa membaca {BERKAS_DATA}: {galat}")
        return []
    if not isinstance(data, list):
        return []
    return data


def simpan_data(data):
    """Simpan daftar produk ke berkas JSON."""
    try:
        with open(BERKAS_DATA, "w", encoding="utf-8") as berkas:
            json.dump(data, berkas, indent=2, ensure_ascii=False)
    except OSError as galat:
        print(f"Tidak bisa menyimpan {BERKAS_DATA}: {galat}")
        sys.exit(1)


def id_berikutnya(data):
    """ID baru: satu lebih besar dari ID terbesar yang ada."""
    return max((produk["id"] for produk in data), default=0) + 1


def cari_produk(data, produk_id):
    """Cari produk dari ID-nya, kembalikan None bila tidak ada."""
    return next((p for p in data if p["id"] == produk_id), None)


def tampilkan_hpp_produk(produk, margin=None, harga=None):
    """Tampilkan rincian HPP, harga jual, BEP, dan laba satu produk."""
    hpp = hitung_hpp(produk["bahan"], produk["tenaga"], produk["overhead"])
    if harga is None:
        margin = 30 if margin is None else margin
        harga = harga_dari_margin(hpp, margin)
    else:
        margin = margin_dari_harga(hpp, harga)

    print(f"Produk: {produk['nama']}")
    print(f"  Bahan baku /unit : {rupiah(produk['bahan'])}")
    print(f"  Tenaga kerja/unit: {rupiah(produk['tenaga'])}")
    print(f"  Overhead /unit   : {rupiah(produk['overhead'])}")
    print(f"  HPP /unit        : {rupiah(hpp)}")
    print(f"  Biaya tetap/bln  : {rupiah(produk['tetap'])}")
    print(f"  Target jual/bln  : {produk['target']} unit")
    print()
    print(f"  Harga jual       : {rupiah(harga)}")
    print(f"  Keuntungan /unit : {rupiah(harga - hpp)} "
          f"(margin {persen(margin)})")

    unit_bep, rupiah_bep = hitung_bep(produk["tetap"], harga, hpp)
    if unit_bep is None:
        print("  BEP              : tidak pernah impas — harga jual "
              "tidak lebih besar dari HPP.")
    else:
        print(f"  BEP              : {unit_bep} unit/bulan "
              f"({rupiah(rupiah_bep)} omzet)")
        if produk["target"] >= unit_bep:
            print(f"  Target {produk['target']} unit sudah di atas BEP "
                  f"({unit_bep} unit).")
        else:
            print(f"  Target {produk['target']} unit masih di bawah BEP "
                  f"({unit_bep} unit) — naikkan harga atau volume jual.")

    laba = hitung_laba(harga, hpp, produk["tetap"], produk["target"])
    print(f"  Laba pada target : {rupiah(laba)}/bulan "
          f"({'untung' if laba >= 0 else 'rugi'})")
    return hpp, harga


def tambah_produk(data, nama, bahan, tenaga, overhead, tetap, target):
    """Tambah satu produk ke daftar dan simpan."""
    produk = {
        "id": id_berikutnya(data),
        "nama": nama,
        "bahan": bahan,
        "tenaga": tenaga,
        "overhead": overhead,
        "tetap": tetap,
        "target": target,
    }
    data.append(produk)
    simpan_data(data)
    hpp = hitung_hpp(bahan, tenaga, overhead)
    print(f"Ditambah: [{produk['id']}] {nama} — HPP {rupiah(hpp)}/unit, "
          f"biaya tetap {rupiah(tetap)}/bulan, target {target} unit/bulan.")
    return produk


def tampilkan_daftar(data):
    """Tampilkan daftar produk beserta HPP dan harga jual sarannya."""
    if not data:
        print("Belum ada produk. Tambah dulu dengan perintah 'tambah'.")
        return
    print(f"{'ID':<4} {'Produk':<20} {'HPP/unit':>12} "
          f"{'Jual 30%':>12} {'BEP':>8} {'Target':>7}")
    print("-" * 68)
    for produk in data:
        hpp = hitung_hpp(produk["bahan"], produk["tenaga"],
                         produk["overhead"])
        harga = harga_dari_margin(hpp, 30)
        unit_bep, _ = hitung_bep(produk["tetap"], harga, hpp)
        kolom_bep = f"{unit_bep}" if unit_bep is not None else "-"
        print(f"{produk['id']:<4} {produk['nama']:<20} {rupiah(hpp):>12} "
              f"{rupiah(harga):>12} {kolom_bep:>8} {produk['target']:>7}")
    print("-" * 68)
    print("Kolom 'Jual 30%' adalah harga jual dengan margin 30% dari HPP.")


def hitung_cepat(bahan, tenaga, overhead, margin):
    """Hitung cepat HPP dan harga jual tanpa menyimpan."""
    hpp = hitung_hpp(bahan, tenaga, overhead)
    harga = harga_dari_margin(hpp, margin)
    print(f"Bahan baku /unit : {rupiah(bahan)}")
    print(f"Tenaga kerja/unit: {rupiah(tenaga)}")
    print(f"Overhead /unit   : {rupiah(overhead)}")
    print(f"HPP /unit        : {rupiah(hpp)}")
    print(f"Harga jual (margin {persen(margin)}): {rupiah(harga)}")
    print(f"Keuntungan /unit : {rupiah(harga - hpp)}")
    return hpp, harga


def tampilkan_bep(data, produk_id, harga=None, margin=None):
    """Tampilkan BEP satu produk pada harga tertentu."""
    produk = cari_produk(data, produk_id)
    if produk is None:
        print(f"Tidak ada produk dengan ID {produk_id}.")
        return
    hpp = hitung_hpp(produk["bahan"], produk["tenaga"], produk["overhead"])
    if harga is None:
        margin = 30 if margin is None else margin
        harga = harga_dari_margin(hpp, margin)
    print(f"{produk['nama']} — HPP {rupiah(hpp)}/unit, "
          f"biaya tetap {rupiah(produk['tetap'])}/bulan, "
          f"harga jual {rupiah(harga)} (margin {persen(margin_dari_harga(hpp, harga))}).")
    unit_bep, rupiah_bep = hitung_bep(produk["tetap"], harga, hpp)
    if unit_bep is None:
        print("Tidak pernah impas: harga jual tidak lebih besar dari HPP.")
        return
    print(f"BEP: {unit_bep} unit/bulan, setara omzet {rupiah(rupiah_bep)}/bulan.")
    print(f"Artinya: jual {unit_bep} unit sebulan baru balik modal; "
          f"unit ke-{unit_bep + 1} dan seterusnya adalah keuntungan.")
    if produk["target"]:
        laba = hitung_laba(harga, hpp, produk["tetap"], produk["target"])
        print(f"Pada target {produk['target']} unit/bulan: "
              f"laba {rupiah(laba)}/bulan.")


def tampilkan_laba(data, produk_id, unit_terjual, harga=None, margin=None):
    """Tampilkan laba bulanan satu produk pada sejumlah unit terjual."""
    produk = cari_produk(data, produk_id)
    if produk is None:
        print(f"Tidak ada produk dengan ID {produk_id}.")
        return
    hpp = hitung_hpp(produk["bahan"], produk["tenaga"], produk["overhead"])
    if harga is None:
        margin = 30 if margin is None else margin
        harga = harga_dari_margin(hpp, margin)
    omzet = harga * unit_terjual
    biaya_variabel = hpp * unit_terjual
    laba = hitung_laba(harga, hpp, produk["tetap"], unit_terjual)
    print(f"{produk['nama']} — {unit_terjual} unit terjual "
          f"dengan harga {rupiah(harga)}:")
    print(f"  Omzet          : {rupiah(omzet)}")
    print(f"  Biaya variabel : {rupiah(biaya_variabel)} "
          f"({unit_terjual} x {rupiah(hpp)})")
    print(f"  Biaya tetap    : {rupiah(produk['tetap'])}")
    print(f"  Laba kotor     : {rupiah(omzet - biaya_variabel)}")
    print(f"  Laba bersih    : {rupiah(laba)}/bulan "
          f"({'untung' if laba >= 0 else 'rugi'})")
    if laba < 0:
        unit_bep, _ = hitung_bep(produk["tetap"], harga, hpp)
        if unit_bep is not None:
            print(f"  Supaya impas, jual minimal {unit_bep} unit/bulan.")


def bandingkan_harga(data, produk_id, harga1, harga2, unit):
    """Bandingkan dua harga jual: margin, BEP, dan laba tiap harga."""
    produk = cari_produk(data, produk_id)
    if produk is None:
        print(f"Tidak ada produk dengan ID {produk_id}.")
        return
    hpp = hitung_hpp(produk["bahan"], produk["tenaga"], produk["overhead"])
    print(f"{produk['nama']} — HPP {rupiah(hpp)}/unit, "
          f"biaya tetap {rupiah(produk['tetap'])}/bulan, "
          f"dibandingkan pada {unit} unit/bulan:")
    print(f"{'':<18} {rupiah(harga1):>14} {rupiah(harga2):>14}")
    print("-" * 48)
    for label, nilai1, nilai2 in [
        ("Margin", persen(margin_dari_harga(hpp, harga1)),
         persen(margin_dari_harga(hpp, harga2))),
        ("Untung /unit", rupiah(harga1 - hpp), rupiah(harga2 - hpp)),
        ("Laba /bulan",
         rupiah(hitung_laba(harga1, hpp, produk["tetap"], unit)),
         rupiah(hitung_laba(harga2, hpp, produk["tetap"], unit))),
    ]:
        print(f"{label:<18} {nilai1:>14} {nilai2:>14}")
    unit1, _ = hitung_bep(produk["tetap"], harga1, hpp)
    unit2, _ = hitung_bep(produk["tetap"], harga2, hpp)
    print(f"{'BEP (unit/bln)':<18} "
          f"{(str(unit1) if unit1 is not None else '-'):>14} "
          f"{(str(unit2) if unit2 is not None else '-'):>14}")
    print()
    if harga2 > harga1:
        selisih = hitung_laba(harga2, hpp, produk["tetap"], unit) - \
            hitung_laba(harga1, hpp, produk["tetap"], unit)
        print(f"Harga {rupiah(harga2)} memberi laba {rupiah(selisih)} "
              f"lebih besar per bulan — bila volume jual tetap {unit} unit. "
              f"Ingat, harga lebih tinggi bisa menurunkan volume jual.")


def hapus_produk(data, produk_id, yakin):
    """Hapus satu produk dari daftar."""
    produk = cari_produk(data, produk_id)
    if produk is None:
        print(f"Tidak ada produk dengan ID {produk_id}.")
        return
    if not yakin:
        print(f"Hapus [{produk['id']}] {produk['nama']}? Tambahkan --ya "
              "untuk mengonfirmasi.")
        return
    data.remove(produk)
    simpan_data(data)
    print(f"Dihapus: [{produk['id']}] {produk['nama']}.")


def tanya_angka(pesan, default=None, batas_min=None, bilangan_bulat=False):
    """Minta angka dari pengguna di mode interaktif."""
    while True:
        tambahan = f" [{default}]" if default is not None else ""
        jawaban = input(f"{pesan}{tambahan}: ").strip()
        if not jawaban and default is not None:
            return default
        try:
            nilai = int(jawaban) if bilangan_bulat else float(jawaban)
        except ValueError:
            print("Masukkan angka yang valid.")
            continue
        if batas_min is not None and nilai < batas_min:
            print(f"Nilainya minimal {batas_min}.")
            continue
        return nilai


def mode_interaktif():
    """Menu angka untuk pengguna yang menjalankan tanpa argumen."""
    while True:
        data = muat_data()
        print()
        print("=== Kalkulator HPP & Harga Jual ===")
        print(f"Produk tercatat: {len(data)}")
        print("1. Tambah produk")
        print("2. Lihat daftar produk")
        print("3. Hitung HPP dan harga jual produk")
        print("4. Hitung cepat (tanpa menyimpan)")
        print("5. Hitung BEP produk")
        print("6. Hitung laba bulanan produk")
        print("7. Bandingkan dua harga jual")
        print("8. Hapus produk")
        print("0. Keluar")
        pilihan = input("Pilih (0-8): ").strip()
        if pilihan == "0":
            print("Sampai jumpa.")
            break
        if pilihan == "1":
            nama = input("Nama produk: ").strip()
            if not nama:
                print("Nama produk tidak boleh kosong.")
                continue
            bahan = tanya_angka("Bahan baku per unit (Rp)", batas_min=0)
            tenaga = tanya_angka("Tenaga kerja per unit (Rp)", batas_min=0)
            overhead = tanya_angka("Overhead per unit (Rp)", batas_min=0)
            tetap = tanya_angka("Biaya tetap per bulan (Rp)", batas_min=0)
            target = tanya_angka("Target penjualan per bulan (unit)",
                                 default=100, batas_min=0,
                                 bilangan_bulat=True)
            tambah_produk(muat_data(), nama, bahan, tenaga, overhead,
                          tetap, int(target))
        elif pilihan == "2":
            tampilkan_daftar(data)
        elif pilihan == "3":
            if not data:
                print("Belum ada produk.")
                continue
            tampilkan_daftar(data)
            produk_id = tanya_angka("ID produk", batas_min=1,
                                    bilangan_bulat=True)
            produk = cari_produk(data, int(produk_id))
            if produk is None:
                print(f"Tidak ada produk dengan ID {int(produk_id)}.")
                continue
            margin = tanya_angka("Margin keuntungan (%)", default=30,
                                 batas_min=0)
            tampilkan_hpp_produk(produk, margin=margin)
        elif pilihan == "4":
            bahan = tanya_angka("Bahan baku per unit (Rp)", batas_min=0)
            tenaga = tanya_angka("Tenaga kerja per unit (Rp)", batas_min=0)
            overhead = tanya_angka("Overhead per unit (Rp)", batas_min=0)
            margin = tanya_angka("Margin keuntungan (%)", default=30,
                                 batas_min=0)
            hitung_cepat(bahan, tenaga, overhead, margin)
        elif pilihan == "5":
            if not data:
                print("Belum ada produk.")
                continue
            tampilkan_daftar(data)
            produk_id = tanya_angka("ID produk", batas_min=1,
                                    bilangan_bulat=True)
            harga = tanya_angka("Harga jual (Rp, 0 = pakai margin 30%)",
                                default=0, batas_min=0)
            tampilkan_bep(data, int(produk_id),
                          harga=(harga if harga else None))
        elif pilihan == "6":
            if not data:
                print("Belum ada produk.")
                continue
            tampilkan_daftar(data)
            produk_id = tanya_angka("ID produk", batas_min=1,
                                    bilangan_bulat=True)
            unit = tanya_angka("Unit terjual per bulan", batas_min=0,
                               bilangan_bulat=True)
            harga = tanya_angka("Harga jual (Rp, 0 = pakai margin 30%)",
                                default=0, batas_min=0)
            tampilkan_laba(data, int(produk_id), int(unit),
                           harga=(harga if harga else None))
        elif pilihan == "7":
            if not data:
                print("Belum ada produk.")
                continue
            tampilkan_daftar(data)
            produk_id = tanya_angka("ID produk", batas_min=1,
                                    bilangan_bulat=True)
            harga1 = tanya_angka("Harga pertama (Rp)", batas_min=1)
            harga2 = tanya_angka("Harga kedua (Rp)", batas_min=1)
            unit = tanya_angka("Unit terjual per bulan", default=100,
                               batas_min=0, bilangan_bulat=True)
            bandingkan_harga(data, int(produk_id), harga1, harga2, int(unit))
        elif pilihan == "8":
            if not data:
                print("Belum ada produk.")
                continue
            tampilkan_daftar(data)
            produk_id = tanya_angka("ID produk yang dihapus", batas_min=1,
                                    bilangan_bulat=True)
            hapus_produk(data, int(produk_id), yakin=True)
        else:
            print("Pilihan tidak dikenal, coba 0-8.")


def validasi_angka(nilai, nama, batas_min=None, batas_max=None):
    """Periksa angka argumen baris perintah, berhenti bila tidak valid."""
    if batas_min is not None and nilai < batas_min:
        print(f"{nama} minimal {batas_min}.")
        sys.exit(1)
    if batas_max is not None and nilai > batas_max:
        print(f"{nama} maksimal {batas_max}.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Kalkulator HPP dan harga jual untuk usaha kecil.")
    sub = parser.add_subparsers(dest="perintah")

    p_cepat = sub.add_parser("cepat", help="hitung cepat tanpa menyimpan")
    p_cepat.add_argument("bahan", type=float,
                         help="biaya bahan baku per unit (Rp)")
    p_cepat.add_argument("tenaga", type=float,
                         help="biaya tenaga kerja per unit (Rp)")
    p_cepat.add_argument("overhead", type=float,
                         help="biaya overhead per unit (Rp)")
    p_cepat.add_argument("--margin", type=float, default=30,
                         help="margin keuntungan dalam persen (default 30)")

    p_tambah = sub.add_parser("tambah", help="tambah produk ke daftar")
    p_tambah.add_argument("nama", help="nama produk, misal \"Kopi Gula Aren\"")
    p_tambah.add_argument("bahan", type=float,
                          help="biaya bahan baku per unit (Rp)")
    p_tambah.add_argument("tenaga", type=float,
                          help="biaya tenaga kerja per unit (Rp)")
    p_tambah.add_argument("overhead", type=float,
                          help="biaya overhead per unit (Rp)")
    p_tambah.add_argument("--tetap", type=float, default=0,
                          help="biaya tetap per bulan (Rp, default 0)")
    p_tambah.add_argument("--target", type=int, default=100,
                          help="target penjualan per bulan, unit (default 100)")

    sub.add_parser("daftar", help="lihat daftar produk")

    p_hpp = sub.add_parser("hpp", help="hitung HPP dan harga jual produk")
    p_hpp.add_argument("id", type=int, help="ID produk")
    p_hpp.add_argument("--margin", type=float, default=None,
                       help="margin keuntungan dalam persen (default 30)")
    p_hpp.add_argument("--harga", type=float, default=None,
                       help="harga jual sendiri (Rp), mengganti margin")

    p_jual = sub.add_parser("jual", help="hitung margin dari harga jual")
    p_jual.add_argument("id", type=int, help="ID produk")
    p_jual.add_argument("harga", type=float, help="harga jual (Rp)")

    p_bep = sub.add_parser("bep", help="hitung titik impas (BEP) produk")
    p_bep.add_argument("id", type=int, help="ID produk")
    p_bep.add_argument("--harga", type=float, default=None,
                       help="harga jual (Rp), default dari margin 30%")
    p_bep.add_argument("--margin", type=float, default=None,
                       help="margin keuntungan dalam persen")

    p_laba = sub.add_parser("laba", help="hitung laba bulanan produk")
    p_laba.add_argument("id", type=int, help="ID produk")
    p_laba.add_argument("unit", type=int,
                        help="unit terjual per bulan")
    p_laba.add_argument("--harga", type=float, default=None,
                        help="harga jual (Rp), default dari margin 30%")
    p_laba.add_argument("--margin", type=float, default=None,
                        help="margin keuntungan dalam persen")

    p_banding = sub.add_parser("banding", help="bandingkan dua harga jual")
    p_banding.add_argument("id", type=int, help="ID produk")
    p_banding.add_argument("harga1", type=float, help="harga pertama (Rp)")
    p_banding.add_argument("harga2", type=float, help="harga kedua (Rp)")
    p_banding.add_argument("--unit", type=int, default=100,
                           help="unit terjual per bulan (default 100)")

    p_hapus = sub.add_parser("hapus", help="hapus satu produk")
    p_hapus.add_argument("id", type=int, help="ID produk")
    p_hapus.add_argument("--ya", action="store_true",
                         help="konfirmasi penghapusan")

    args = parser.parse_args()

    if args.perintah is None:
        mode_interaktif()
        return

    if args.perintah == "cepat":
        validasi_angka(args.bahan, "Bahan baku", batas_min=0)
        validasi_angka(args.tenaga, "Tenaga kerja", batas_min=0)
        validasi_angka(args.overhead, "Overhead", batas_min=0)
        validasi_angka(args.margin, "Margin", batas_min=0)
        hitung_cepat(args.bahan, args.tenaga, args.overhead, args.margin)
    elif args.perintah == "tambah":
        validasi_angka(args.bahan, "Bahan baku", batas_min=0)
        validasi_angka(args.tenaga, "Tenaga kerja", batas_min=0)
        validasi_angka(args.overhead, "Overhead", batas_min=0)
        validasi_angka(args.tetap, "Biaya tetap", batas_min=0)
        validasi_angka(args.target, "Target", batas_min=0)
        tambah_produk(muat_data(), args.nama, args.bahan, args.tenaga,
                      args.overhead, args.tetap, args.target)
    elif args.perintah == "daftar":
        tampilkan_daftar(muat_data())
    elif args.perintah == "hpp":
        validasi_angka(args.margin, "Margin", batas_min=0) \
            if args.margin is not None else None
        validasi_angka(args.harga, "Harga", batas_min=1) \
            if args.harga is not None else None
        produk = cari_produk(muat_data(), args.id)
        if produk is None:
            print(f"Tidak ada produk dengan ID {args.id}.")
            sys.exit(1)
        tampilkan_hpp_produk(produk, margin=args.margin, harga=args.harga)
    elif args.perintah == "jual":
        validasi_angka(args.harga, "Harga", batas_min=1)
        produk = cari_produk(muat_data(), args.id)
        if produk is None:
            print(f"Tidak ada produk dengan ID {args.id}.")
            sys.exit(1)
        tampilkan_hpp_produk(produk, harga=args.harga)
    elif args.perintah == "bep":
        validasi_angka(args.harga, "Harga", batas_min=1) \
            if args.harga is not None else None
        validasi_angka(args.margin, "Margin", batas_min=0) \
            if args.margin is not None else None
        tampilkan_bep(muat_data(), args.id, harga=args.harga,
                      margin=args.margin)
    elif args.perintah == "laba":
        validasi_angka(args.unit, "Unit terjual", batas_min=0)
        validasi_angka(args.harga, "Harga", batas_min=1) \
            if args.harga is not None else None
        validasi_angka(args.margin, "Margin", batas_min=0) \
            if args.margin is not None else None
        tampilkan_laba(muat_data(), args.id, args.unit, harga=args.harga,
                       margin=args.margin)
    elif args.perintah == "banding":
        validasi_angka(args.harga1, "Harga pertama", batas_min=1)
        validasi_angka(args.harga2, "Harga kedua", batas_min=1)
        validasi_angka(args.unit, "Unit", batas_min=0)
        bandingkan_harga(muat_data(), args.id, args.harga1, args.harga2,
                         args.unit)
    elif args.perintah == "hapus":
        hapus_produk(muat_data(), args.id, yakin=args.ya)


if __name__ == "__main__":
    main()
