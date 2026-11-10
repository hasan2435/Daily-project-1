#!/usr/bin/env python3
"""Pencatat Kebiasaan Harian — proyek harian ke-10.

Program terminal untuk mencatat kebiasaan yang ingin dibangun setiap
hari: tambah kebiasaan, centang bila sudah dilakukan hari ini, lihat
rangkaian hari beruntun (streak), dan ringkasan 7 hari terakhir.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.
Data kebiasaan disimpan di berkas ``kebiasaan.json`` pada folder tempat
program dijalankan. Berkas data itu milik pengguna, bukan bagian dari
proyek, jadi jangan ikut diunggah ke repositori.

Cara memakai (mode perintah):

    python3 kebiasaan.py tambah "Olahraga pagi" --target 5
    python3 kebiasaan.py centang "Olahraga pagi"
    python3 kebiasaan.py centang "Olahraga pagi" --tanggal 2026-11-09
    python3 kebiasaan.py batal "Olahraga pagi"
    python3 kebiasaan.py daftar
    python3 kebiasaan.py ringkasan
    python3 kebiasaan.py hapus "Olahraga pagi"

Jalankan tanpa argumen untuk mode interaktif.

Streak dihitung dari hari ini mundur: bila kebiasaan belum dicentang
hari ini, streak dihitung dari kemarin, supaya satu hari yang belum
dicentang tidak langsung memutus rangkaian yang sedang berjalan.
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

BERKAS_DATA = Path(__file__).with_name("kebiasaan.json")

# Batas yang masih masuk akal: nama tidak boleh kosong atau terlalu
# panjang, target mingguan antara 1 dan 7 hari.
NAMA_MAKSIMAL = 60
TARGET_MIN = 1
TARGET_MAKS = 7
HARI_RINGKASAN = 7


def muat_data():
    """Baca data kebiasaan dari berkas JSON; kembalikan dict kosong bila
    berkas belum ada atau isinya rusak."""
    if not BERKAS_DATA.exists():
        return {"kebiasaan": []}
    try:
        data = json.loads(BERKAS_DATA.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"kebiasaan": []}
    if not isinstance(data, dict) or not isinstance(data.get("kebiasaan"), list):
        return {"kebiasaan": []}
    return data


def simpan_data(data):
    """Simpan data kebiasaan ke berkas JSON."""
    BERKAS_DATA.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def cari_kebiasaan(data, nama):
    """Cari kebiasaan berdasarkan nama (tanpa membedakan huruf besar
    dan kecil); kembalikan None bila tidak ada."""
    nama_bersih = nama.strip().lower()
    for item in data["kebiasaan"]:
        if item["nama"].lower() == nama_bersih:
            return item
    return None


def tambah(data, nama, target):
    """Tambah kebiasaan baru. Kembalikan pesan hasil."""
    nama = nama.strip()
    if not nama:
        return "Nama kebiasaan tidak boleh kosong."
    if len(nama) > NAMA_MAKSIMAL:
        return f"Nama kebiasaan maksimal {NAMA_MAKSIMAL} karakter."
    if not TARGET_MIN <= target <= TARGET_MAKS:
        return f"Target mingguan harus antara {TARGET_MIN} dan {TARGET_MAKS} hari."
    if cari_kebiasaan(data, nama) is not None:
        return f'Kebiasaan "{nama}" sudah ada.'
    data["kebiasaan"].append(
        {"nama": nama, "target": target, "tanggal": []}
    )
    simpan_data(data)
    return f'Kebiasaan "{nama}" ditambahkan (target {target}x/minggu).'


def centang(data, nama, tanggal, batal=False):
    """Centang (atau batalkan centang) sebuah kebiasaan pada tanggal
    tertentu. Kembalikan pesan hasil."""
    item = cari_kebiasaan(data, nama)
    if item is None:
        return f'Kebiasaan "{nama}" tidak ditemukan. Tambah dulu dengan perintah tambah.'
    tanggal_teks = tanggal.isoformat()
    if tanggal > date.today():
        return "Tanggal tidak boleh di masa depan."
    if batal:
        if tanggal_teks not in item["tanggal"]:
            return f'"{item["nama"]}" belum dicentang pada {tanggal_teks}.'
        item["tanggal"].remove(tanggal_teks)
        simpan_data(data)
        return f'Centang "{item["nama"]}" pada {tanggal_teks} dibatalkan.'
    if tanggal_teks in item["tanggal"]:
        return f'"{item["nama"]}" sudah dicentang pada {tanggal_teks}.'
    item["tanggal"].append(tanggal_teks)
    item["tanggal"].sort()
    simpan_data(data)
    return f'"{item["nama"]}" dicentang pada {tanggal_teks}.'


def hapus(data, nama):
    """Hapus sebuah kebiasaan beserta seluruh riwayatnya."""
    item = cari_kebiasaan(data, nama)
    if item is None:
        return f'Kebiasaan "{nama}" tidak ditemukan.'
    data["kebiasaan"] = [
        keb for keb in data["kebiasaan"] if keb is not item
    ]
    simpan_data(data)
    return f'Kebiasaan "{item["nama"]}" dihapus.'


def hitung_streak(tanggal_tercentang, hari_ini):
    """Hitung rangkaian hari beruntun sampai hari ini (atau kemarin bila
    hari ini belum dicentang)."""
    tercentang = set(tanggal_tercentang)
    hari = hari_ini
    if hari.isoformat() not in tercentang:
        hari -= timedelta(days=1)
    streak = 0
    while hari.isoformat() in tercentang:
        streak += 1
        hari -= timedelta(days=1)
    return streak


def hitung_mingguan(tanggal_tercentang, hari_ini):
    """Hitung berapa hari kebiasaan dilakukan dalam 7 hari terakhir."""
    awal = hari_ini - timedelta(days=HARI_RINGKASAN - 1)
    return sum(
        1
        for teks in tanggal_tercentang
        if awal.isoformat() <= teks <= hari_ini.isoformat()
    )


def daftar(data, hari_ini):
    """Tampilkan daftar kebiasaan beserta status hari ini dan streak."""
    if not data["kebiasaan"]:
        return "Belum ada kebiasaan. Tambah dulu dengan perintah tambah."
    baris = ["Kebiasaan harian:", ""]
    for item in sorted(data["kebiasaan"], key=lambda k: k["nama"].lower()):
        sudah = hari_ini.isoformat() in item["tanggal"]
        status = "✓ hari ini" if sudah else "· belum hari ini"
        streak = hitung_streak(item["tanggal"], hari_ini)
        baris.append(
            f'- {item["nama"]} (target {item["target"]}x/minggu) — '
            f"{status}, streak {streak} hari"
        )
    return "\n".join(baris)


def ringkasan(data, hari_ini):
    """Tampilkan ringkasan 7 hari terakhir untuk setiap kebiasaan."""
    if not data["kebiasaan"]:
        return "Belum ada kebiasaan. Tambah dulu dengan perintah tambah."
    tanggal_7 = [
        hari_ini - timedelta(days=i)
        for i in range(HARI_RINGKASAN - 1, -1, -1)
    ]
    kepala = " " * 21 + "".join(f"{t.day:^3}" for t in tanggal_7)
    baris = [
        "Ringkasan 7 hari terakhir "
        f"({tanggal_7[0].isoformat()} s.d. {hari_ini.isoformat()}):",
        kepala,
        "",
    ]
    for item in sorted(data["kebiasaan"], key=lambda k: k["nama"].lower()):
        tercentang = set(item["tanggal"])
        simbol = "".join(
            " ✓ " if t.isoformat() in tercentang else " · "
            for t in tanggal_7
        )
        mingguan = hitung_mingguan(item["tanggal"], hari_ini)
        streak = hitung_streak(item["tanggal"], hari_ini)
        baris.append(
            f"{item['nama'][:20]:<20} {simbol} "
            f"{mingguan}/{HARI_RINGKASAN} hari, streak {streak}"
        )
    baris.append("")
    baris.append("✓ = dilakukan, · = belum dilakukan.")
    return "\n".join(baris)


def tanggal_argumen(teks):
    """Ubah teks YYYY-MM-DD menjadi date; lempar ValueError bila salah."""
    try:
        return date.fromisoformat(teks)
    except ValueError:
        raise ValueError("tanggal harus berformat YYYY-MM-DD, contoh 2026-11-10")


def mode_interaktif():
    """Menu interaktif untuk pengguna yang menjalankan tanpa argumen."""
    data = muat_data()
    hari_ini = date.today()
    print("Pencatat Kebiasaan Harian")
    print("========================")
    print("Bangun kebiasaan baik, satu centang setiap hari.")
    print()
    while True:
        print("1. Tambah kebiasaan")
        print("2. Centang hari ini")
        print("3. Batalkan centang hari ini")
        print("4. Lihat daftar kebiasaan")
        print("5. Ringkasan 7 hari terakhir")
        print("6. Hapus kebiasaan")
        print("0. Keluar")
        pilihan = input("Pilih menu (0-6): ").strip()
        print()
        if pilihan == "0":
            print("Sampai jumpa besok, jangan putus streak-nya!")
            return
        if pilihan == "1":
            nama = input("Nama kebiasaan: ").strip()
            target_teks = input("Target per minggu (1-7, kosong = 7): ").strip()
            try:
                target = int(target_teks) if target_teks else 7
            except ValueError:
                print("Target harus berupa angka.")
                print()
                continue
            print(tambah(data, nama, target))
        elif pilihan == "2":
            nama = input("Nama kebiasaan yang dicentang: ").strip()
            print(centang(data, nama, hari_ini))
        elif pilihan == "3":
            nama = input("Nama kebiasaan yang dibatalkan: ").strip()
            print(centang(data, nama, hari_ini, batal=True))
        elif pilihan == "4":
            print(daftar(data, hari_ini))
        elif pilihan == "5":
            print(ringkasan(data, hari_ini))
        elif pilihan == "6":
            nama = input("Nama kebiasaan yang dihapus: ").strip()
            print(hapus(data, nama))
        else:
            print("Pilihan tidak dikenal, coba lagi.")
        print()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Pencatat Kebiasaan Harian: bangun kebiasaan baik, "
        "satu centang setiap hari."
    )
    sub = parser.add_subparsers(dest="perintah")

    p_tambah = sub.add_parser("tambah", help="Tambah kebiasaan baru")
    p_tambah.add_argument("nama", help="Nama kebiasaan")
    p_tambah.add_argument(
        "--target", type=int, default=7,
        help="Target hari per minggu (1-7, default 7)",
    )

    p_centang = sub.add_parser("centang", help="Centang kebiasaan")
    p_centang.add_argument("nama", help="Nama kebiasaan")
    p_centang.add_argument(
        "--tanggal", type=tanggal_argumen, default=date.today(),
        help="Tanggal YYYY-MM-DD (default hari ini)",
    )

    p_batal = sub.add_parser("batal", help="Batalkan centang kebiasaan")
    p_batal.add_argument("nama", help="Nama kebiasaan")
    p_batal.add_argument(
        "--tanggal", type=tanggal_argumen, default=date.today(),
        help="Tanggal YYYY-MM-DD (default hari ini)",
    )

    sub.add_parser("daftar", help="Lihat daftar kebiasaan")
    sub.add_parser("ringkasan", help="Ringkasan 7 hari terakhir")

    p_hapus = sub.add_parser("hapus", help="Hapus kebiasaan")
    p_hapus.add_argument("nama", help="Nama kebiasaan")

    args = parser.parse_args(argv)
    if args.perintah is None:
        mode_interaktif()
        return 0

    data = muat_data()
    hari_ini = date.today()
    if args.perintah == "tambah":
        print(tambah(data, args.nama, args.target))
    elif args.perintah == "centang":
        print(centang(data, args.nama, args.tanggal))
    elif args.perintah == "batal":
        print(centang(data, args.nama, args.tanggal, batal=True))
    elif args.perintah == "daftar":
        print(daftar(data, hari_ini))
    elif args.perintah == "ringkasan":
        print(ringkasan(data, hari_ini))
    elif args.perintah == "hapus":
        print(hapus(data, args.nama))
    return 0


if __name__ == "__main__":
    sys.exit(main())
