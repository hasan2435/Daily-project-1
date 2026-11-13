#!/usr/bin/env python3
"""Kalkulator IPK & Nilai Kuliah — proyek harian ke-13.

Program terminal untuk menghitung Indeks Prestasi Kumulatif (IPK)
dari mata kuliah yang diambil: tiap mata kuliah punya jumlah SKS dan
nilai (huruf A sampai E, atau angka 0-100 yang otomatis dikonversi).
IPK dihitung tertimbang SKS, lengkap dengan predikat kelulusan dan
perhitungan IPK semester depan yang dibutuhkan untuk mencapai target
IPK kumulatif.

Skala nilai angka ke huruf (cek aturan kampusmu, skala tiap kampus
bisa berbeda; skala ini yang dipakai program):

    A  : 85-100  -> 4.0
    AB : 80-84   -> 3.5
    B  : 75-79   -> 3.0
    BC : 70-74   -> 2.5
    C  : 60-69   -> 2.0
    D  : 50-59   -> 1.0
    E  : 0-49    -> 0.0

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

Cara memakai (mode perintah):

    python3 ipk.py tambah "Matematika Diskrit" 3 A
    python3 ipk.py tambah "Fisika Dasar" 2 85
    python3 ipk.py daftar
    python3 ipk.py hapus "Fisika Dasar"
    python3 ipk.py ipk
    python3 ipk.py target 3.5 20
    python3 ipk.py target 3.5 20 --sks-saat-ini 40 --ipk 3.2
    python3 ipk.py konversi 82
    python3 ipk.py skala

Jalankan tanpa argumen untuk mode interaktif. Data mata kuliah
disimpan di berkas ipk.json pada folder tempat program dijalankan.
"""

import argparse
import json
import os
import sys

BERKAS_DATA = "ipk.json"

# (huruf, nilai angka terendah, bobot), urut dari yang tertinggi.
SKALA = [
    ("A", 85, 4.0),
    ("AB", 80, 3.5),
    ("B", 75, 3.0),
    ("BC", 70, 2.5),
    ("C", 60, 2.0),
    ("D", 50, 1.0),
    ("E", 0, 0.0),
]

HURUF_KE_BOBOT = {huruf: bobot for huruf, _, bobot in SKALA}


def angka_ke_huruf(nilai):
    """Ubah nilai angka 0-100 menjadi (huruf, bobot)."""
    for huruf, batas, bobot in SKALA:
        if nilai >= batas:
            return huruf, bobot
    return "E", 0.0


def urai_nilai(teks):
    """Urai nilai dari pengguna menjadi (huruf, bobot, angka).

    Menerima huruf (A, AB, B, BC, C, D, E, besar/kecil) atau angka
    0-100 (boleh desimal, contoh: 82 atau 82.5).
    """
    teks = teks.strip().upper()
    if teks in HURUF_KE_BOBOT:
        return teks, HURUF_KE_BOBOT[teks], None
    try:
        angka = float(teks.replace(",", "."))
    except ValueError:
        raise ValueError(
            f"Nilai '{teks}' tidak dikenal. Pakai huruf A-E "
            "atau angka 0-100."
        )
    if angka < 0 or angka > 100:
        raise ValueError("Nilai angka harus di antara 0 dan 100.")
    huruf, bobot = angka_ke_huruf(angka)
    return huruf, bobot, angka


def muat_data():
    """Muat daftar mata kuliah dari berkas JSON, kosong bila belum ada."""
    if not os.path.exists(BERKAS_DATA):
        return []
    try:
        with open(BERKAS_DATA, "r", encoding="utf-8") as berkas:
            data = json.load(berkas)
    except (OSError, json.JSONDecodeError):
        print(f"Berkas {BERKAS_DATA} rusak atau tidak bisa dibaca.")
        return []
    if not isinstance(data, list):
        print(f"Isi {BERKAS_DATA} tidak sesuai format.")
        return []
    return data


def simpan_data(data):
    """Simpan daftar mata kuliah ke berkas JSON."""
    try:
        with open(BERKAS_DATA, "w", encoding="utf-8") as berkas:
            json.dump(data, berkas, ensure_ascii=False, indent=2)
    except OSError as err:
        print(f"Gagal menyimpan {BERKAS_DATA}: {err}")
        return False
    return True


def hitung_ipk(data):
    """Hitung (total SKS, total bobot x SKS, IPK) dari daftar mata kuliah."""
    total_sks = sum(item["sks"] for item in data)
    total_bobot = sum(item["bobot"] * item["sks"] for item in data)
    ipk = total_bobot / total_sks if total_sks > 0 else 0.0
    return total_sks, total_bobot, ipk


def predikat(ipk):
    """Predikat kelulusan dari IPK."""
    if ipk >= 3.5:
        return "Dengan Pujian (Cumlaude)"
    if ipk >= 3.0:
        return "Sangat Memuaskan"
    if ipk >= 2.75:
        return "Memuaskan"
    if ipk >= 2.0:
        return "Cukup"
    return "Kurang"


def tampilkan_daftar(data):
    """Tampilkan tabel mata kuliah beserta ringkasan IPK."""
    if not data:
        print("Belum ada mata kuliah. Tambahkan dulu dengan perintah:")
        print('  python3 ipk.py tambah "Nama Mata Kuliah" 3 A')
        return
    print(f"{'Mata kuliah':<28}{'SKS':>5}  {'Nilai':>6}  {'Bobot':>5}")
    print("-" * 48)
    for item in sorted(data, key=lambda x: x["nama"].lower()):
        nilai = item["nilai"]
        if item.get("angka") is not None:
            nilai = f"{nilai} ({item['angka']:g})"
        print(
            f"{item['nama']:<28}{item['sks']:>5}  {nilai:>6}  "
            f"{item['bobot']:>5.1f}"
        )
    print("-" * 48)
    total_sks, _, ipk = hitung_ipk(data)
    print(f"Total SKS : {total_sks}")
    print(f"IPK       : {ipk:.2f} ({predikat(ipk)})")


def perintah_tambah(nama, sks, nilai_teks):
    """Tambah mata kuliah baru, atau perbarui bila namanya sudah ada."""
    if sks <= 0:
        print("Jumlah SKS harus lebih dari 0.")
        return 1
    if sks > 6:
        print("Jumlah SKS per mata kuliah umumnya maksimal 6.")
        return 1
    try:
        huruf, bobot, angka = urai_nilai(nilai_teks)
    except ValueError as err:
        print(err)
        return 1
    data = muat_data()
    for item in data:
        if item["nama"].lower() == nama.lower():
            item["sks"] = sks
            item["nilai"] = huruf
            item["bobot"] = bobot
            item["angka"] = angka
            if not simpan_data(data):
                return 1
            print(f"Diperbarui: {nama} — {sks} SKS, nilai {huruf}.")
            return 0
    data.append(
        {"nama": nama, "sks": sks, "nilai": huruf, "bobot": bobot,
         "angka": angka}
    )
    if not simpan_data(data):
        return 1
    print(f"Ditambahkan: {nama} — {sks} SKS, nilai {huruf}.")
    return 0


def perintah_hapus(nama):
    """Hapus mata kuliah berdasarkan nama."""
    data = muat_data()
    sisa = [item for item in data if item["nama"].lower() != nama.lower()]
    if len(sisa) == len(data):
        print(f"Mata kuliah '{nama}' tidak ditemukan.")
        return 1
    if not simpan_data(sisa):
        return 1
    print(f"Dihapus: {nama}.")
    return 0


def perintah_ipk():
    """Tampilkan ringkasan IPK saat ini."""
    data = muat_data()
    if not data:
        print("Belum ada mata kuliah. Tambahkan dulu dengan perintah:")
        print('  python3 ipk.py tambah "Nama Mata Kuliah" 3 A')
        return 1
    tampilkan_daftar(data)
    return 0


def perintah_target(target, sks_depan, sks_saat_ini, ipk_saat_ini):
    """Hitung IPK semester depan yang dibutuhkan untuk mencapai target.

    Bila SKS dan IPK saat ini tidak diberikan, dipakai data mata kuliah
    yang tersimpan.
    """
    if target < 0 or target > 4.0:
        print("Target IPK harus di antara 0 dan 4.0.")
        return 1
    if sks_depan <= 0:
        print("SKS semester depan harus lebih dari 0.")
        return 1
    if sks_saat_ini is None or ipk_saat_ini is None:
        data = muat_data()
        if not data:
            print("Belum ada data mata kuliah. Tambahkan dulu, atau isi")
            print("SKS dan IPK saat ini dengan opsi --sks-saat-ini dan --ipk.")
            return 1
        sks_saat_ini, _, ipk_saat_ini = hitung_ipk(data)
    total_bobot_kini = ipk_saat_ini * sks_saat_ini
    sks_total = sks_saat_ini + sks_depan
    butuh = (target * sks_total - total_bobot_kini) / sks_depan
    ipk_maks = (total_bobot_kini + 4.0 * sks_depan) / sks_total

    print(f"IPK saat ini : {ipk_saat_ini:.2f} ({sks_saat_ini} SKS)")
    print(f"Target IPK    : {target:.2f} setelah {sks_depan} SKS lagi")
    if butuh <= 0:
        print("Target sudah tercapai — IPK semester depan berapa pun")
        print("tidak akan menurunkan IPK di bawah target.")
    elif butuh > 4.0:
        print(f"Tidak mungkin: butuh IPK semester {butuh:.2f}, sedangkan")
        print("nilai tertinggi adalah 4.0.")
        print(f"Dengan IPK semester 4.0, IPK akhir maksimal {ipk_maks:.2f}.")
    else:
        print(f"Butuh IPK semester depan: {butuh:.2f}")
        for huruf, _, bobot in reversed(SKALA):
            if bobot >= butuh:
                print(f"Artinya rata-rata nilai minimal {huruf} "
                      f"(bobot {bobot:g}).")
                break
        print(f"Dengan IPK semester 4.0, IPK akhir maksimal {ipk_maks:.2f}.")
    return 0


def perintah_konversi(nilai_teks):
    """Tampilkan huruf dan bobot dari satu nilai angka."""
    try:
        angka = float(nilai_teks.replace(",", "."))
    except ValueError:
        print(f"'{nilai_teks}' bukan angka.")
        return 1
    if angka < 0 or angka > 100:
        print("Nilai angka harus di antara 0 dan 100.")
        return 1
    huruf, bobot = angka_ke_huruf(angka)
    print(f"{angka:g} -> {huruf} (bobot {bobot:g})")
    return 0


def tampilkan_skala():
    """Tampilkan tabel konversi nilai angka ke huruf."""
    print("Skala nilai (angka -> huruf, bobot):")
    for i, (huruf, batas, bobot) in enumerate(SKALA):
        # Batas atas = satu di bawah batas huruf di atasnya; A sampai 100.
        atas = 100 if i == 0 else SKALA[i - 1][1] - 1
        print(f"  {huruf:<3} {batas}-{atas:<5} bobot {bobot:g}")
    print("Skala tiap kampus bisa berbeda; cek aturan kampusmu.")


def tanya(teks, wajib=True):
    """Minta masukan teks; kosong mengembalikan None bila tidak wajib."""
    jawaban = input(teks).strip()
    if not jawaban and not wajib:
        return None
    return jawaban


def mode_interaktif():
    """Menu interaktif berbasis angka."""
    while True:
        print("\n=== Kalkulator IPK & Nilai Kuliah ===")
        print("1. Tambah/ubah mata kuliah")
        print("2. Lihat daftar & IPK")
        print("3. Hapus mata kuliah")
        print("4. Hitung target IPK semester depan")
        print("5. Lihat skala nilai")
        print("6. Keluar")
        pilihan = input("Pilih (1-6): ").strip()
        if pilihan == "1":
            nama = tanya("Nama mata kuliah: ")
            if not nama:
                print("Nama tidak boleh kosong.")
                continue
            try:
                sks = int(tanya("Jumlah SKS: "))
            except (TypeError, ValueError):
                print("SKS harus berupa bilangan bulat.")
                continue
            nilai = tanya("Nilai (huruf A-E atau angka 0-100): ")
            if not nilai:
                print("Nilai tidak boleh kosong.")
                continue
            perintah_tambah(nama, sks, nilai)
        elif pilihan == "2":
            tampilkan_daftar(muat_data())
        elif pilihan == "3":
            nama = tanya("Nama mata kuliah yang dihapus: ")
            if nama:
                perintah_hapus(nama)
        elif pilihan == "4":
            try:
                target = float(tanya("Target IPK (0-4): ").replace(",", "."))
                sks_depan = int(tanya("SKS semester depan: "))
            except (TypeError, ValueError):
                print("Target dan SKS harus berupa angka.")
                continue
            perintah_target(target, sks_depan, None, None)
        elif pilihan == "5":
            tampilkan_skala()
        elif pilihan == "6":
            print("Sampai jumpa, semoga IPK-nya naik!")
            return 0
        else:
            print("Pilihan tidak dikenal, pilih 1-6.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Kalkulator IPK & Nilai Kuliah."
    )
    sub = parser.add_subparsers(dest="perintah")

    p_tambah = sub.add_parser("tambah", help="tambah/ubah mata kuliah")
    p_tambah.add_argument("nama", help="nama mata kuliah")
    p_tambah.add_argument("sks", type=int, help="jumlah SKS")
    p_tambah.add_argument("nilai", help="huruf A-E atau angka 0-100")

    sub.add_parser("daftar", help="tampilkan daftar & IPK")
    sub.add_parser("ipk", help="tampilkan ringkasan IPK")

    p_hapus = sub.add_parser("hapus", help="hapus mata kuliah")
    p_hapus.add_argument("nama", help="nama mata kuliah")

    p_target = sub.add_parser(
        "target", help="IPK semester depan untuk mencapai target IPK"
    )
    p_target.add_argument("target", type=float, help="target IPK (0-4)")
    p_target.add_argument("sks", type=int, help="SKS semester depan")
    p_target.add_argument(
        "--sks-saat-ini", dest="sks_saat_ini", type=int, default=None,
        help="SKS yang sudah ditempuh (bila tidak pakai data tersimpan)",
    )
    p_target.add_argument(
        "--ipk", dest="ipk_saat_ini", type=float, default=None,
        help="IPK saat ini (bila tidak pakai data tersimpan)",
    )

    p_konversi = sub.add_parser("konversi", help="angka 0-100 ke huruf")
    p_konversi.add_argument("nilai", help="nilai angka 0-100")

    sub.add_parser("skala", help="tampilkan skala nilai")

    args = parser.parse_args(argv)
    if args.perintah is None:
        return mode_interaktif()
    if args.perintah == "tambah":
        return perintah_tambah(args.nama, args.sks, args.nilai)
    if args.perintah == "daftar":
        tampilkan_daftar(muat_data())
        return 0
    if args.perintah == "hapus":
        return perintah_hapus(args.nama)
    if args.perintah == "ipk":
        return perintah_ipk()
    if args.perintah == "target":
        return perintah_target(
            args.target, args.sks, args.sks_saat_ini, args.ipk_saat_ini
        )
    if args.perintah == "konversi":
        return perintah_konversi(args.nilai)
    if args.perintah == "skala":
        tampilkan_skala()
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
