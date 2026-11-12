#!/usr/bin/env python3
"""Pembagi Tagihan — proyek harian ke-12.

Program terminal untuk membagi tagihan makan bersama (atau tagihan apa
pun) dengan adil: bagi rata, bagi per item pesanan, atau bagi menurut
persentase yang disepakati. Bisa menambahkan service charge dan tip,
lalu membulatkan bagian tiap orang ke kelipatan tertentu supaya mudah
ditransfer.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

Cara memakai (mode perintah):

    python3 tagihan.py rata 300000 3
    python3 tagihan.py rata 300000 3 --service 10 --tip 5
    python3 tagihan.py rata 275000 4 --bulat 1000
    python3 tagihan.py persen 400000 --bagi "Ani=50, Budi=30, Cici=20"
    python3 tagihan.py item
    python3 tagihan.py item --service 5 --tip 10

Jalankan tanpa argumen untuk mode interaktif.
"""

import argparse
import math
import sys


def format_rupiah(nilai):
    """Format angka menjadi tulisan rupiah, contoh: Rp275.000."""
    nilai = int(round(nilai))
    return "Rp" + f"{nilai:,}".replace(",", ".")


def bulatkan_ke_atas(nilai, kelipatan):
    """Bulatkan nilai ke atas ke kelipatan terdekat."""
    if kelipatan <= 0:
        return nilai
    return math.ceil(nilai / kelipatan) * kelipatan


def tambah_service_dan_tip(total, service_pct, tip_pct):
    """Hitung total akhir beserta rincian service charge dan tip.

    Service charge dihitung dari total awal, lalu tip dihitung dari
    total awal + service charge.
    """
    service = total * service_pct / 100
    tip = (total + service) * tip_pct / 100
    return total + service + tip, service, tip


def tampilkan_rincian(total_awal, service, tip, total_akhir):
    print(f"Total awal     : {format_rupiah(total_awal)}")
    if service:
        print(f"Service charge : {format_rupiah(service)}")
    if tip:
        print(f"Tip            : {format_rupiah(tip)}")
    print(f"Total akhir    : {format_rupiah(total_akhir)}")
    print("-" * 40)


def bagi_rata(total, orang, service_pct, tip_pct, bulat):
    """Bagi total tagihan sama rata ke sejumlah orang."""
    if total <= 0:
        print("Total tagihan harus lebih dari 0.")
        return 1
    if orang < 2:
        print("Bagi rata butuh minimal 2 orang.")
        return 1
    total_akhir, service, tip = tambah_service_dan_tip(
        total, service_pct, tip_pct
    )
    per_orang = total_akhir / orang
    per_orang_bulat = bulatkan_ke_atas(per_orang, bulat)

    tampilkan_rincian(total, service, tip, total_akhir)
    print(f"Dibagi {orang} orang, masing-masing:")
    print(f"  {format_rupiah(per_orang)}", end="")
    if bulat > 0 and per_orang_bulat != per_orang:
        selisih = (per_orang_bulat - per_orang) * orang
        print(f" -> dibulatkan ke {format_rupiah(per_orang_bulat)}")
        print(f"  (kelebihan {format_rupiah(selisih)} dari pembulatan)")
    else:
        print()
    return 0


def urai_pembagian_persen(teks):
    """Urai 'Ani=50, Budi=30' menjadi daftar (nama, persen)."""
    hasil = []
    for bagian in teks.split(","):
        bagian = bagian.strip()
        if not bagian:
            continue
        if "=" not in bagian:
            raise ValueError(f"Format salah: '{bagian}' (pakai Nama=persen)")
        nama, persen = bagian.rsplit("=", 1)
        nama = nama.strip()
        persen = float(persen.strip())
        if not nama:
            raise ValueError("Nama tidak boleh kosong.")
        if persen <= 0:
            raise ValueError(f"Persen {nama} harus lebih dari 0.")
        hasil.append((nama, persen))
    if len(hasil) < 2:
        print("Bagi persen butuh minimal 2 orang.")
        return None
    total_persen = sum(p for _, p in hasil)
    if abs(total_persen - 100) > 0.01:
        print(f"Total persen harus 100, sekarang {total_persen:g}.")
        return None
    return hasil


def bagi_persen(total, teks_bagi, service_pct, tip_pct, bulat):
    """Bagi total tagihan menurut persentase tiap orang."""
    if total <= 0:
        print("Total tagihan harus lebih dari 0.")
        return 1
    try:
        pembagian = urai_pembagian_persen(teks_bagi)
    except ValueError as err:
        print(f"Error: {err}")
        return 1
    if pembagian is None:
        return 1
    total_akhir, service, tip = tambah_service_dan_tip(
        total, service_pct, tip_pct
    )
    tampilkan_rincian(total, service, tip, total_akhir)
    for nama, persen in pembagian:
        bagian = total_akhir * persen / 100
        bagian_bulat = bulatkan_ke_atas(bagian, bulat)
        teks = f"  {nama:<15} {persen:g}%  : {format_rupiah(bagian)}"
        if bulat > 0 and bagian_bulat != bagian:
            teks += f" -> {format_rupiah(bagian_bulat)}"
        print(teks)
    return 0


def minta_angka(prompt, minimal=0):
    """Minta angka dari pengguna sampai valid."""
    while True:
        try:
            nilai = float(input(prompt).replace(".", "").replace(",", "."))
        except ValueError:
            print("  Masukkan angka yang valid.")
            continue
        if nilai < minimal:
            print(f"  Nilai minimal {minimal:g}.")
            continue
        return nilai


def minta_persen(prompt):
    """Minta persen 0-100 dari pengguna (kosong = 0)."""
    while True:
        teks = input(prompt).strip()
        if teks == "":
            return 0.0
        try:
            nilai = float(teks.replace(",", "."))
        except ValueError:
            print("  Masukkan angka yang valid.")
            continue
        if nilai < 0 or nilai > 100:
            print("  Persen harus 0-100.")
            continue
        return nilai


def mode_item(service_pct, tip_pct, bulat):
    """Bagi per item: tiap orang memasukkan pesanannya sendiri.

    Item bersama (misalnya pajak parkir atau makanan yang dimakan
    bareng) dibagi rata ke semua orang. Service charge dan tip
    dibagi sebanding dengan subtotal tiap orang.
    """
    print("=== Bagi Per Item ===")
    print("Masukkan nama dan item pesanannya. Item ditulis")
    print("'nama item=harga', dipisah koma. Kosongkan nama untuk selesai.")
    print()

    orang = []  # daftar (nama, [(item, harga), ...])
    while True:
        nama = input("Nama orang (kosong = selesai): ").strip()
        if not nama:
            break
        if any(n == nama for n, _ in orang):
            print("  Nama sudah dipakai, pakai nama lain.")
            continue
        teks_item = input(f"  Item {nama} (contoh: nasi goreng=25000, es teh=8000): ").strip()
        item = []
        for bagian in teks_item.split(","):
            bagian = bagian.strip()
            if not bagian:
                continue
            if "=" not in bagian:
                print(f"  Lewati '{bagian}' (pakai format nama=harga).")
                continue
            nama_item, harga = bagian.rsplit("=", 1)
            try:
                harga = float(harga.strip().replace(".", "").replace(",", "."))
            except ValueError:
                print(f"  Lewati '{bagian}' (harga bukan angka).")
                continue
            if harga < 0:
                print(f"  Lewati '{bagian}' (harga tidak boleh negatif).")
                continue
            item.append((nama_item.strip(), harga))
        orang.append((nama, item))
        subtotal = sum(h for _, h in item)
        print(f"  Subtotal {nama}: {format_rupiah(subtotal)}")

    if len(orang) < 2:
        print("Bagi per item butuh minimal 2 orang.")
        return 1

    print()
    teks_bersama = input(
        "Item bersama (contoh: parkir=10000, kerupuk=15000) [kosong = tidak ada]: "
    ).strip()
    bersama = 0.0
    for bagian in teks_bersama.split(","):
        bagian = bagian.strip()
        if not bagian or "=" not in bagian:
            continue
        _, harga = bagian.rsplit("=", 1)
        try:
            bersama += float(harga.strip().replace(".", "").replace(",", "."))
        except ValueError:
            continue

    subtotal_semua = sum(sum(h for _, h in item) for _, item in orang)
    total_awal = subtotal_semua + bersama
    total_akhir, service, tip = tambah_service_dan_tip(
        total_awal, service_pct, tip_pct
    )
    print()
    tampilkan_rincian(total_awal, service, tip, total_akhir)

    bersama_per_orang = bersama / len(orang)
    print("Bagian tiap orang (termasuk item bersama dan bagiannya dari")
    print("service charge + tip, sebanding dengan subtotal):")
    for nama, item in orang:
        subtotal = sum(h for _, h in item)
        dasar = subtotal + bersama_per_orang
        # Service + tip dibagi sebanding dengan dasar tiap orang.
        bagian = dasar + (service + tip) * (dasar / total_awal) if total_awal else 0
        bagian_bulat = bulatkan_ke_atas(bagian, bulat)
        teks = f"  {nama:<15} : {format_rupiah(bagian)}"
        if bulat > 0 and bagian_bulat != bagian:
            teks += f" -> {format_rupiah(bagian_bulat)}"
        print(teks)
        for nama_item, harga in item:
            print(f"      - {nama_item}: {format_rupiah(harga)}")
    if bersama:
        print(f"  Item bersama {format_rupiah(bersama)} dibagi rata: "
              f"{format_rupiah(bersama_per_orang)} per orang.")
    return 0


def mode_interaktif():
    print("=== Pembagi Tagihan ===")
    print("1. Bagi rata")
    print("2. Bagi per item pesanan")
    print("3. Bagi menurut persen")
    print("0. Keluar")
    pilihan = input("Pilih (0-3): ").strip()
    if pilihan == "0":
        return 0
    if pilihan not in ("1", "2", "3"):
        print("Pilihan tidak dikenal.")
        return 1

    total = None
    if pilihan in ("1", "3"):
        total = minta_angka("Total tagihan (Rp): ", minimal=1)
    service = minta_persen("Service charge (%) [kosong = 0]: ")
    tip = minta_persen("Tip (%) [kosong = 0]: ")
    teks_bulat = input("Bulatkan ke kelipatan (100/500/1000) [kosong = tidak]: ").strip()
    bulat = 0
    if teks_bulat:
        try:
            bulat = int(teks_bulat)
            if bulat <= 0:
                bulat = 0
        except ValueError:
            bulat = 0
    print()

    if pilihan == "1":
        orang = int(minta_angka("Jumlah orang: ", minimal=2))
        return bagi_rata(total, orang, service, tip, bulat)
    if pilihan == "2":
        return mode_item(service, tip, bulat)
    teks_bagi = input('Pembagian (contoh: Ani=50, Budi=30, Cici=20): ').strip()
    return bagi_persen(total, teks_bagi, service, tip, bulat)


def buat_parser():
    parser = argparse.ArgumentParser(
        description="Pembagi tagihan: bagi rata, per item, atau per persen."
    )
    sub = parser.add_subparsers(dest="perintah")

    p_rata = sub.add_parser("rata", help="Bagi total sama rata.")
    p_rata.add_argument("total", type=float, help="Total tagihan (Rp).")
    p_rata.add_argument("orang", type=int, help="Jumlah orang.")
    p_rata.add_argument("--service", type=float, default=0.0,
                        help="Service charge dalam persen (default 0).")
    p_rata.add_argument("--tip", type=float, default=0.0,
                        help="Tip dalam persen (default 0).")
    p_rata.add_argument("--bulat", type=int, default=0,
                        help="Bulatkan bagian tiap orang ke kelipatan ini.")

    p_persen = sub.add_parser("persen", help="Bagi menurut persentase.")
    p_persen.add_argument("total", type=float, help="Total tagihan (Rp).")
    p_persen.add_argument("--bagi", required=True,
                          help='Contoh: "Ani=50, Budi=30, Cici=20".')
    p_persen.add_argument("--service", type=float, default=0.0)
    p_persen.add_argument("--tip", type=float, default=0.0)
    p_persen.add_argument("--bulat", type=int, default=0)

    p_item = sub.add_parser("item", help="Bagi per item pesanan (interaktif).")
    p_item.add_argument("--service", type=float, default=0.0)
    p_item.add_argument("--tip", type=float, default=0.0)
    p_item.add_argument("--bulat", type=int, default=0)
    return parser


def main(argv=None):
    parser = buat_parser()
    args = parser.parse_args(argv)
    if args.perintah is None:
        return mode_interaktif()
    if args.perintah == "rata":
        return bagi_rata(args.total, args.orang, args.service, args.tip,
                         args.bulat)
    if args.perintah == "persen":
        return bagi_persen(args.total, args.bagi, args.service, args.tip,
                           args.bulat)
    return mode_item(args.service, args.tip, args.bulat)


if __name__ == "__main__":
    sys.exit(main())
