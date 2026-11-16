#!/usr/bin/env python3
"""Pencatat Buku Bacaan — Day 16.

Program terminal untuk mencatat buku yang sedang dibaca: tambah buku,
catat halaman yang sudah dibaca, pantau progres tiap buku, tandai
selesai, dan lihat statistik bacaan. Hanya memakai pustaka standar
Python, tanpa pustaka tambahan.

Cara menjalankan:
    python3 buku.py
    python3 buku.py tambah "Laskar Pelangi" "Andrea Hirata" 529
    python3 buku.py baca 1 120
    python3 buku.py daftar
    python3 buku.py selesai 1
    python3 buku.py statistik

Data disimpan di berkas buku.json pada folder tempat program dijalankan.
"""

import argparse
import json
import os
import sys
from datetime import date

DATA_FILE = "buku.json"

BAR_PANJANG = 20


def muat_data():
    """Baca data buku dari berkas JSON, kembalikan list (kosong bila belum ada)."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"Peringatan: {DATA_FILE} rusak atau tidak bisa dibaca, mulai dari kosong.")
        return []
    if not isinstance(data, list):
        return []
    return data


def simpan_data(data):
    """Simpan data buku ke berkas JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def id_berikutnya(data):
    """ID baru = ID terbesar yang ada + 1."""
    return max((b["id"] for b in data), default=0) + 1


def cari_buku(data, buku_id):
    """Cari buku berdasarkan ID, kembalikan dict atau None."""
    for buku in data:
        if buku["id"] == buku_id:
            return buku
    return None


def persen(buku):
    """Persentase halaman yang sudah dibaca (0-100)."""
    if buku["total"] <= 0:
        return 0.0
    return min(100.0, buku["dibaca"] / buku["total"] * 100)


def bar_progres(p):
    """Bar progres teks, misal [##########----------] 50%."""
    terisi = int(round(p / 100 * BAR_PANJANG))
    return "[" + "#" * terisi + "-" * (BAR_PANJANG - terisi) + f"] {p:.0f}%"


def tampilkan_buku(buku, tampilkan_tanggal=True):
    """Tampilkan satu buku beserta progresnya."""
    status = "SELESAI" if buku["selesai"] else "dibaca"
    print(f"{buku['id']}. {buku['judul']} — {buku['penulis']}")
    if buku.get("genre"):
        print(f"   Genre: {buku['genre']}")
    print(f"   {bar_progres(persen(buku))}  {buku['dibaca']}/{buku['total']} halaman  [{status}]")
    if tampilkan_tanggal:
        mulai = buku.get("mulai") or "-"
        selesai = buku.get("tanggal_selesai") or "-"
        print(f"   Mulai: {mulai}   Selesai: {selesai}")
    if buku.get("catatan"):
        print(f"   Catatan: {buku['catatan']}")


def perintah_tambah(args):
    data = muat_data()
    if args.total <= 0:
        print("Total halaman harus lebih dari 0.")
        return 1
    buku = {
        "id": id_berikutnya(data),
        "judul": args.judul,
        "penulis": args.penulis,
        "total": args.total,
        "dibaca": 0,
        "genre": args.genre or "",
        "catatan": args.catatan or "",
        "mulai": date.today().isoformat(),
        "selesai": False,
        "tanggal_selesai": None,
    }
    data.append(buku)
    simpan_data(data)
    print(f"Buku #{buku['id']} ditambahkan: {buku['judul']} — {buku['penulis']} ({buku['total']} halaman).")
    return 0


def perintah_baca(args):
    data = muat_data()
    buku = cari_buku(data, args.id)
    if buku is None:
        print(f"Tidak ada buku dengan ID {args.id}.")
        return 1
    if buku["selesai"]:
        print(f"Buku '{buku['judul']}' sudah selesai dibaca.")
        return 1
    if args.halaman <= 0:
        print("Jumlah halaman harus lebih dari 0.")
        return 1
    buku["dibaca"] += args.halaman
    if buku["dibaca"] >= buku["total"]:
        buku["dibaca"] = buku["total"]
        buku["selesai"] = True
        buku["tanggal_selesai"] = date.today().isoformat()
        simpan_data(data)
        print(f"Selamat! Kamu menyelesaikan '{buku['judul']}' ({buku['total']} halaman).")
    else:
        simpan_data(data)
        sisa = buku["total"] - buku["dibaca"]
        print(f"Progres '{buku['judul']}': {bar_progres(persen(buku))} — sisa {sisa} halaman.")
    return 0


def perintah_daftar(args):
    data = muat_data()
    if not data:
        print("Belum ada buku. Tambah dulu dengan: python3 buku.py tambah \"Judul\" \"Penulis\" 300")
        return 0
    daftar = data
    if args.status == "aktif":
        daftar = [b for b in data if not b["selesai"]]
    elif args.status == "selesai":
        daftar = [b for b in data if b["selesai"]]
    if args.genre:
        daftar = [b for b in daftar if b.get("genre", "").lower() == args.genre.lower()]
    if not daftar:
        print("Tidak ada buku yang cocok dengan filter itu.")
        return 0
    # Urutkan: yang belum selesai dulu, lalu progres tertinggi.
    daftar = sorted(daftar, key=lambda b: (b["selesai"], -persen(b)))
    print(f"Daftar buku ({len(daftar)}):")
    print("=" * 60)
    for buku in daftar:
        tampilkan_buku(buku)
        print("-" * 60)
    return 0


def perintah_selesai(args):
    data = muat_data()
    buku = cari_buku(data, args.id)
    if buku is None:
        print(f"Tidak ada buku dengan ID {args.id}.")
        return 1
    if buku["selesai"]:
        print(f"Buku '{buku['judul']}' sudah ditandai selesai.")
        return 0
    buku["dibaca"] = buku["total"]
    buku["selesai"] = True
    buku["tanggal_selesai"] = date.today().isoformat()
    simpan_data(data)
    print(f"'{buku['judul']}' ditandai selesai.")
    return 0


def perintah_hapus(args):
    data = muat_data()
    buku = cari_buku(data, args.id)
    if buku is None:
        print(f"Tidak ada buku dengan ID {args.id}.")
        return 1
    if not args.ya:
        jawab = input(f"Hapus '{buku['judul']}'? (y/n): ").strip().lower()
        if jawab not in ("y", "ya"):
            print("Dibatalkan.")
            return 0
    data.remove(buku)
    simpan_data(data)
    print(f"Buku '{buku['judul']}' dihapus.")
    return 0


def perintah_statistik(_args):
    data = muat_data()
    if not data:
        print("Belum ada buku. Tambah dulu dengan: python3 buku.py tambah \"Judul\" \"Penulis\" 300")
        return 0
    selesai = [b for b in data if b["selesai"]]
    aktif = [b for b in data if not b["selesai"]]
    total_halaman = sum(b["dibaca"] for b in data)
    target_halaman = sum(b["total"] for b in data)
    print("Statistik bacaan")
    print("=" * 60)
    print(f"Total buku dicatat : {len(data)}")
    print(f"Selesai dibaca     : {len(selesai)}")
    print(f"Sedang dibaca      : {len(aktif)}")
    print(f"Halaman dibaca     : {total_halaman} dari {target_halaman}")
    if target_halaman:
        print(f"Progres keseluruhan: {total_halaman / target_halaman * 100:.1f}%")
    if selesai:
        rata = sum(b["total"] for b in selesai) / len(selesai)
        print(f"Rata-rata halaman buku selesai: {rata:.0f}")
    if aktif:
        print()
        print("Sedang dibaca:")
        for buku in sorted(aktif, key=lambda b: -persen(b)):
            print(f"  - {buku['judul']}: {bar_progres(persen(buku))}")
    # Genre terbanyak
    genre_hitung = {}
    for buku in data:
        g = buku.get("genre") or "tanpa genre"
        genre_hitung[g] = genre_hitung.get(g, 0) + 1
    if len(genre_hitung) > 1 or "tanpa genre" not in genre_hitung:
        favorit = max(genre_hitung.items(), key=lambda kv: kv[1])
        print(f"\nGenre terbanyak: {favorit[0]} ({favorit[1]} buku)")
    return 0


def mode_interaktif():
    """Menu angka interaktif."""
    while True:
        print()
        print("=== Pencatat Buku Bacaan ===")
        print("1. Tambah buku")
        print("2. Catat halaman dibaca")
        print("3. Lihat daftar buku")
        print("4. Tandai buku selesai")
        print("5. Statistik bacaan")
        print("6. Hapus buku")
        print("0. Keluar")
        pilihan = input("Pilih menu (0-6): ").strip()
        if pilihan == "0":
            print("Sampai jumpa di halaman berikutnya!")
            return 0
        if pilihan == "1":
            judul = input("Judul buku: ").strip()
            penulis = input("Penulis: ").strip()
            genre = input("Genre (boleh kosong): ").strip()
            try:
                total = int(input("Total halaman: ").strip())
            except ValueError:
                print("Total halaman harus berupa angka.")
                continue
            if not judul or not penulis:
                print("Judul dan penulis wajib diisi.")
                continue
            args = argparse.Namespace(judul=judul, penulis=penulis, total=total,
                                      genre=genre, catatan="")
            perintah_tambah(args)
        elif pilihan == "2":
            try:
                buku_id = int(input("ID buku: ").strip())
                halaman = int(input("Halaman yang dibaca hari ini: ").strip())
            except ValueError:
                print("ID dan halaman harus berupa angka.")
                continue
            perintah_baca(argparse.Namespace(id=buku_id, halaman=halaman))
        elif pilihan == "3":
            perintah_daftar(argparse.Namespace(status="semua", genre=None))
        elif pilihan == "4":
            try:
                buku_id = int(input("ID buku: ").strip())
            except ValueError:
                print("ID harus berupa angka.")
                continue
            perintah_selesai(argparse.Namespace(id=buku_id))
        elif pilihan == "5":
            perintah_statistik(None)
        elif pilihan == "6":
            try:
                buku_id = int(input("ID buku: ").strip())
            except ValueError:
                print("ID harus berupa angka.")
                continue
            perintah_hapus(argparse.Namespace(id=buku_id, ya=False))
        else:
            print("Pilihan tidak dikenal, coba lagi.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Pencatat Buku Bacaan — catat buku, pantau progres, dan lihat statistik bacaan."
    )
    sub = parser.add_subparsers(dest="perintah")

    p_tambah = sub.add_parser("tambah", help="Tambah buku baru.")
    p_tambah.add_argument("judul", help="Judul buku.")
    p_tambah.add_argument("penulis", help="Nama penulis.")
    p_tambah.add_argument("total", type=int, help="Total halaman buku.")
    p_tambah.add_argument("--genre", default="", help="Genre buku, misal novel, sejarah.")
    p_tambah.add_argument("--catatan", default="", help="Catatan singkat tentang buku.")
    p_tambah.set_defaults(func=perintah_tambah)

    p_baca = sub.add_parser("baca", help="Catat halaman yang baru dibaca.")
    p_baca.add_argument("id", type=int, help="ID buku.")
    p_baca.add_argument("halaman", type=int, help="Jumlah halaman yang dibaca.")
    p_baca.set_defaults(func=perintah_baca)

    p_daftar = sub.add_parser("daftar", help="Lihat daftar buku.")
    p_daftar.add_argument("--status", choices=["semua", "aktif", "selesai"], default="semua")
    p_daftar.add_argument("--genre", default=None, help="Tampilkan hanya genre tertentu.")
    p_daftar.set_defaults(func=perintah_daftar)

    p_selesai = sub.add_parser("selesai", help="Tandai buku selesai dibaca.")
    p_selesai.add_argument("id", type=int, help="ID buku.")
    p_selesai.set_defaults(func=perintah_selesai)

    p_hapus = sub.add_parser("hapus", help="Hapus buku dari daftar.")
    p_hapus.add_argument("id", type=int, help="ID buku.")
    p_hapus.add_argument("--ya", action="store_true", help="Hapus tanpa konfirmasi.")
    p_hapus.set_defaults(func=perintah_hapus)

    p_stat = sub.add_parser("statistik", help="Lihat statistik bacaan.")
    p_stat.set_defaults(func=perintah_statistik)

    args = parser.parse_args(argv)
    if not args.perintah:
        return mode_interaktif()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
