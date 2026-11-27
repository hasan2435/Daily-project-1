#!/usr/bin/env python3
"""Permainan Ular Tangga — Day 27 Daily Project 1.

Main ular tangga di terminal untuk 2-4 pemain, manusia melawan
manusia atau melawan komputer. Papan 10x10 berisi 7 tangga dan
7 ular. Aturan klasiknya:

    - Setiap pemain mulai dari luar papan (posisi 0) dan bergiliran
      melempar dadu.
    - Mendarat tepat di kaki tangga berarti naik ke ujung tangga.
    - Mendarat tepat di kepala ular berarti turun ke ekor ular.
    - Melempar angka 6 mendapat giliran lempar lagi; tiga kali
      angka 6 berturut-turut membuat giliran hangus.
    - Pemenangnya adalah yang pertama mendarat tepat di kotak 100.
      Lemparan yang melewati 100 tidak bergerak.

Papan dicetak dengan arah bolak-balik seperti papan sungguhan:
baris bawah 1-10 dari kiri ke kanan, baris di atasnya 20-11 dari
kanan ke kiri, dan seterusnya. Tanda panah naik (naik tangga) dan
panah turun (turun ular) menandai kotak istimewa, huruf awal nama
menandai posisi tiap pemain.

Statistik kemenangan tiap nama pemain dan riwayat 20 permainan
terakhir disimpan otomatis.

Python standar saja, tanpa library tambahan.

Cara pakai:
    python3 ular_tangga.py
    python3 ular_tangga.py main --pemain "Ani,Budi" --komputer 1
    python3 ular_tangga.py demo
    python3 ular_tangga.py demo --pemain 3
    python3 ular_tangga.py papan
    python3 ular_tangga.py statistik
    python3 ular_tangga.py riwayat
    python3 ular_tangga.py riwayat --jumlah 5
    python3 ular_tangga.py reset --ya
    python3 ular_tangga.py --daftar

Jalankan tanpa argumen untuk mode interaktif (menu angka).

Data disimpan di berkas `ular_tangga.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek.
"""

import argparse
import json
import os
import random
import sys
from datetime import datetime

BERKAS_DATA = "ular_tangga.json"
TARGET = 100
JUMLAH_PEMAIN_MIN = 2
JUMLAH_PEMAIN_MAKS = 4
RIWAYAT_MAKS = 20

# Kaki tangga -> ujung tangga.
TANGGA = {
    4: 25,
    13: 46,
    33: 49,
    42: 63,
    50: 69,
    62: 81,
    74: 92,
}

# Kepala ular -> ekor ular.
ULAR = {
    27: 5,
    43: 18,
    55: 25,
    66: 45,
    76: 58,
    89: 53,
    99: 41,
}

MUKA_DADU = ("", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅")

KOMENTAR_NAIK = (
    "Naik tangga! Lumayan, potong jalan.",
    "Tangga! Langsung melesat ke atas.",
    "Dapat tangga, hoki banget.",
)

KOMENTAR_TURUN = (
    "Kena ular! Turun jauh, sabar ya.",
    "Aduh, ular! Balik ke bawah lagi.",
    "Digigit ular, turunnya jauh sekali.",
)


def muat_data():
    """Muat statistik dan riwayat dari berkas JSON, atau data kosong."""
    if not os.path.exists(BERKAS_DATA):
        return {"pemain": {}, "riwayat": []}
    try:
        with open(BERKAS_DATA, "r", encoding="utf-8") as berkas:
            data = json.load(berkas)
        if not isinstance(data, dict):
            return {"pemain": {}, "riwayat": []}
        data.setdefault("pemain", {})
        data.setdefault("riwayat", [])
        return data
    except (OSError, ValueError):
        return {"pemain": {}, "riwayat": []}


def simpan_data(data):
    """Simpan statistik dan riwayat ke berkas JSON."""
    try:
        with open(BERKAS_DATA, "w", encoding="utf-8") as berkas:
            json.dump(data, berkas, ensure_ascii=False, indent=2)
    except OSError as galat:
        print(f"Tidak bisa menyimpan data: {galat}")


def lempar_dadu():
    """Kocok dadu 6 sisi, kembalikan angka 1-6."""
    return random.randint(1, 6)


def nomor_kotak(baris, kolom):
    """Nomor kotak pada baris (0 = paling bawah) dan kolom (0-9)."""
    awal = baris * 10 + 1
    if baris % 2 == 0:
        return awal + kolom
    return awal + (9 - kolom)


def tampilkan_papan(posisi_pemain):
    """Cetak papan 10x10 beserta posisi tiap pemain.

    posisi_pemain: dict nama pemain -> nomor kotak (0 = belum masuk).
    """
    print()
    print("=== Papan Ular Tangga ===")
    print("▲ = kaki tangga, ▼ = kepala ular, huruf = posisi pemain.")
    print()
    for baris in range(9, -1, -1):
        sel = []
        for kolom in range(10):
            nomor = nomor_kotak(baris, kolom)
            isi = str(nomor)
            if nomor in TANGGA:
                isi += "▲"
            elif nomor in ULAR:
                isi += "▼"
            for nama, posisi in posisi_pemain.items():
                if posisi == nomor:
                    isi += nama[0].upper()
            sel.append(f"{isi:>6}")
        print(" ".join(sel))
    print()
    for nama, posisi in posisi_pemain.items():
        tempat = "di luar papan" if posisi == 0 else f"kotak {posisi}"
        print(f"  {nama}: {tempat}")
    print()


def daftar_ular_tangga():
    """Tampilkan semua tangga dan ular beserta tujuannya."""
    print()
    print("=== Daftar Tangga (naik) ===")
    for awal in sorted(TANGGA):
        print(f"  {awal:3d} -> {TANGGA[awal]:3d}  (naik {TANGGA[awal] - awal} kotak)")
    print()
    print("=== Daftar Ular (turun) ===")
    for awal in sorted(ULAR):
        print(f"  {awal:3d} -> {ULAR[awal]:3d}  (turun {awal - ULAR[awal]} kotak)")
    print()
    print("Total: 7 tangga dan 7 ular di papan 1-100.")
    print("Pemenang adalah yang pertama mendarat tepat di kotak 100.")


def tanya(teks, bawaan=""):
    """Minta masukan; kembalikan bawaan bila kosong."""
    jawaban = input(teks).strip()
    return jawaban if jawaban else bawaan


def tanya_angka(teks, bawaan, minimum, maksimum):
    """Minta masukan angka dalam rentang; kembalikan bawaan bila kosong."""
    while True:
        jawaban = input(teks).strip()
        if not jawaban:
            return bawaan
        try:
            angka = int(jawaban)
        except ValueError:
            print("Masukkan angka, ya.")
            continue
        if angka < minimum or angka > maksimum:
            print(f"Masukkan angka {minimum}-{maksimum}.")
            continue
        return angka

def buat_pemain_interaktif():
    """Susun daftar pemain lewat pertanyaan di terminal."""
    jumlah = tanya_angka(
        f"Berapa pemain? ({JUMLAH_PEMAIN_MIN}-{JUMLAH_PEMAIN_MAKS}) [2]: ",
        2, JUMLAH_PEMAIN_MIN, JUMLAH_PEMAIN_MAKS,
    )
    pemain = []
    nama_pakai = set()
    for nomor in range(1, jumlah + 1):
        while True:
            nama = tanya(f"Nama pemain {nomor} [Pemain {nomor}]: ",
                         f"Pemain {nomor}").strip()
            if nama.lower() in nama_pakai:
                print("Nama itu sudah dipakai, pilih nama lain.")
                continue
            nama_pakai.add(nama.lower())
            break
        jenis = tanya(f"  {nama} manusia atau komputer? (m/k) [m]: ",
                      "m").lower()
        pemain.append({
            "nama": nama,
            "komputer": jenis.startswith("k"),
            "posisi": 0,
        })
    return pemain


def buat_pemain_cli(nama_arg, jumlah_komputer):
    """Susun daftar pemain dari argumen baris perintah."""
    nama_list = [n.strip() for n in nama_arg.split(",") if n.strip()] \
        if nama_arg else []
    pemain = []
    for nama in nama_list:
        pemain.append({"nama": nama, "komputer": False, "posisi": 0})
    for nomor in range(1, jumlah_komputer + 1):
        pemain.append({
            "nama": f"Komputer {nomor}",
            "komputer": True,
            "posisi": 0,
        })
    if not pemain:
        pemain = [
            {"nama": "Kamu", "komputer": False, "posisi": 0},
            {"nama": "Komputer 1", "komputer": True, "posisi": 0},
        ]
    return pemain


def giliran_pemain(pemain, interaktif, hitung_giliran):
    """Jalankan satu giliran untuk satu pemain.

    Mengembalikan True bila pemain mencapai kotak 100 (menang).
    Menangani lemparan 6 berulang dan giliran hangus setelah tiga
    kali angka 6 berturut-turut.
    """
    nama = pemain["nama"]
    posisi_awal = pemain["posisi"]
    enam_berturut = 0
    while True:
        if pemain["komputer"] or not interaktif:
            if interaktif:
                input(f"Giliran {nama} (komputer), tekan Enter... ")
        else:
            input(f"Giliran {nama}, tekan Enter untuk melempar dadu... ")
        dadu = lempar_dadu()
        hitung_giliran[0] += 1
        print(f"{nama} melempar: {MUKA_DADU[dadu]} ({dadu})")
        if dadu == 6:
            enam_berturut += 1
            if enam_berturut >= 3:
                pemain["posisi"] = posisi_awal
                print("Tiga kali angka 6 berturut-turut! Giliran hangus, "
                      f"{nama} kembali ke kotak {posisi_awal}.")
                return False
            print("Dapat 6, lempar lagi!")
            # Lemparan 6 tetap bergerak dulu, baru lempar lagi.
        else:
            enam_berturut = 0

        posisi_lama = pemain["posisi"]
        tujuan = posisi_lama + dadu
        if tujuan > TARGET:
            butuh = TARGET - posisi_lama
            print(f"Butuh tepat {butuh} untuk sampai di 100. "
                  f"{nama} tetap di kotak {posisi_lama}.")
        else:
            pemain["posisi"] = tujuan
            print(f"{nama}: {posisi_lama} -> {tujuan}")
            if tujuan in TANGGA:
                naik = TANGGA[tujuan]
                print(f"{random.choice(KOMENTAR_NAIK)} "
                      f"{nama} naik tangga {tujuan} -> {naik}!")
                pemain["posisi"] = naik
            elif tujuan in ULAR:
                turun = ULAR[tujuan]
                print(f"{random.choice(KOMENTAR_TURUN)} "
                      f"{nama} turun ular {tujuan} -> {turun}.")
                pemain["posisi"] = turun
            if pemain["posisi"] == TARGET:
                return True
        if dadu != 6:
            return False
        # Angka 6: ulangi lemparan dalam giliran yang sama.


def mainkan_permainan(pemain, interaktif=True, tampil_papan=True):
    """Mainkan satu permainan penuh sampai ada pemenang.

    Mengembalikan (pemenang, jumlah_lemparan).
    """
    print()
    print("=== Permainan Ular Tangga ===")
    print("Pemain:", ", ".join(
        f"{p['nama']}{' (komputer)' if p['komputer'] else ''}"
        for p in pemain))
    print(f"Yang pertama mendarat tepat di kotak {TARGET} menang.")
    if tampil_papan:
        tampilkan_papan({p["nama"]: p["posisi"] for p in pemain})
    hitung_giliran = [0]
    while True:
        for pemain_saat_ini in pemain:
            menang = giliran_pemain(pemain_saat_ini, interaktif,
                                    hitung_giliran)
            if tampil_papan:
                tampilkan_papan({p["nama"]: p["posisi"] for p in pemain})
            if menang:
                print()
                print(f"🎉 {pemain_saat_ini['nama']} MENANG! "
                      f"Sampai di kotak 100 setelah "
                      f"{hitung_giliran[0]} lemparan dadu.")
                return pemain_saat_ini, hitung_giliran[0]


def catat_hasil(data, pemain, pemenang, jumlah_lemparan):
    """Perbarui statistik dan riwayat, lalu simpan."""
    for p in pemain:
        nama = p["nama"]
        stat = data["pemain"].setdefault(
            nama, {"main": 0, "menang": 0})
        stat["main"] += 1
        if p is pemenang:
            stat["menang"] += 1
    data["riwayat"].insert(0, {
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pemain": [p["nama"] for p in pemain],
        "pemenang": pemenang["nama"],
        "lemparan": jumlah_lemparan,
    })
    data["riwayat"] = data["riwayat"][:RIWAYAT_MAKS]
    simpan_data(data)


def tampilkan_statistik(data):
    """Tampilkan tabel kemenangan tiap nama pemain."""
    print()
    print("=== Statistik Ular Tangga ===")
    if not data["pemain"]:
        print("Belum ada permainan yang tercatat. Main dulu, yuk!")
        return
    print(f"{'Pemain':<20} {'Main':>5} {'Menang':>6} {'Win rate':>9}")
    print("-" * 44)
    urutan = sorted(data["pemain"].items(),
                    key=lambda item: (-item[1]["menang"], item[0].lower()))
    for nama, stat in urutan:
        main = stat["main"]
        menang = stat["menang"]
        persen = (menang / main * 100) if main else 0
        print(f"{nama:<20} {main:>5} {menang:>6} {persen:>8.1f}%")
    total_main = sum(s["main"] for s in data["pemain"].values())
    total_menang = sum(s["menang"] for s in data["pemain"].values())
    print("-" * 44)
    print(f"Total permainan tercatat: {total_menang} "
          f"(total partisipasi pemain: {total_main})")


def tampilkan_riwayat(data, jumlah=10):
    """Tampilkan riwayat permainan terakhir."""
    print()
    print("=== Riwayat Permainan ===")
    if not data["riwayat"]:
        print("Belum ada permainan yang tercatat.")
        return
    for entri in data["riwayat"][:jumlah]:
        pemain = ", ".join(entri["pemain"])
        print(f"  {entri['tanggal']} — {entri['pemenang']} menang "
              f"({entri['lemparan']} lemparan) | {pemain}")

def perintah_main(args):
    """Perintah `main`: permainan baru dari baris perintah."""
    pemain = buat_pemain_cli(args.pemain, args.komputer)
    if len(pemain) < JUMLAH_PEMAIN_MIN:
        print(f"Butuh minimal {JUMLAH_PEMAIN_MIN} pemain. "
              f"Tambahkan --komputer atau nama pemain lain.")
        return 1
    if len(pemain) > JUMLAH_PEMAIN_MAKS:
        print(f"Maksimal {JUMLAH_PEMAIN_MAKS} pemain.")
        return 1
    nama_list = [p["nama"].lower() for p in pemain]
    if len(set(nama_list)) != len(nama_list):
        print("Nama pemain tidak boleh sama.")
        return 1
    data = muat_data()
    pemenang, lemparan = mainkan_permainan(pemain, interaktif=True)
    catat_hasil(data, pemain, pemenang, lemparan)
    return 0


def perintah_demo(args):
    """Perintah `demo`: semua pemain komputer, tanpa jeda tanya."""
    jumlah = args.pemain
    pemain = [
        {"nama": f"Komputer {nomor}", "komputer": True, "posisi": 0}
        for nomor in range(1, jumlah + 1)
    ]
    data = muat_data()
    pemenang, lemparan = mainkan_permainan(
        pemain, interaktif=False, tampil_papan=False)
    print()
    print("Posisi akhir:")
    for p in pemain:
        print(f"  {p['nama']}: kotak {p['posisi']}")
    catat_hasil(data, pemain, pemenang, lemparan)
    return 0


def perintah_reset(args):
    """Perintah `reset`: hapus semua statistik dan riwayat."""
    if not args.ya:
        print("Perintah ini menghapus semua statistik dan riwayat.")
        print("Jalankan lagi dengan --ya bila yakin.")
        return 1
    if os.path.exists(BERKAS_DATA):
        os.remove(BERKAS_DATA)
    print("Statistik dan riwayat sudah dihapus.")
    return 0


def menu_interaktif():
    """Menu angka utama saat program dijalankan tanpa argumen."""
    data = muat_data()
    while True:
        print()
        print("=== Ular Tangga ===")
        print("1. Main baru")
        print("2. Demo (komputer vs komputer)")
        print("3. Lihat papan")
        print("4. Statistik")
        print("5. Riwayat permainan")
        print("6. Daftar ular & tangga")
        print("0. Keluar")
        pilihan = tanya("Pilih (0-6): ").strip()
        if pilihan == "0":
            print("Sampai jumpa di permainan berikutnya!")
            return 0
        if pilihan == "1":
            pemain = buat_pemain_interaktif()
            pemenang, lemparan = mainkan_permainan(pemain, interaktif=True)
            data = muat_data()
            catat_hasil(data, pemain, pemenang, lemparan)
        elif pilihan == "2":
            jumlah = tanya_angka(
                f"Berapa pemain komputer? "
                f"({JUMLAH_PEMAIN_MIN}-{JUMLAH_PEMAIN_MAKS}) [2]: ",
                2, JUMLAH_PEMAIN_MIN, JUMLAH_PEMAIN_MAKS)
            pemain = [
                {"nama": f"Komputer {nomor}", "komputer": True, "posisi": 0}
                for nomor in range(1, jumlah + 1)
            ]
            pemenang, lemparan = mainkan_permainan(
                pemain, interaktif=False, tampil_papan=False)
            print()
            print("Posisi akhir:")
            for p in pemain:
                print(f"  {p['nama']}: kotak {p['posisi']}")
            data = muat_data()
            catat_hasil(data, pemain, pemenang, lemparan)
        elif pilihan == "3":
            tampilkan_papan({})
        elif pilihan == "4":
            tampilkan_statistik(muat_data())
        elif pilihan == "5":
            tampilkan_riwayat(muat_data())
        elif pilihan == "6":
            daftar_ular_tangga()
        else:
            print("Pilihan tidak dikenal, coba 0-6.")


def bangun_parser():
    """Susun parser argumen baris perintah."""
    parser = argparse.ArgumentParser(
        description="Permainan Ular Tangga di terminal (Day 27).")
    parser.add_argument(
        "--daftar", action="store_true",
        help="tampilkan daftar ular dan tangga lalu keluar")
    sub = parser.add_subparsers(dest="perintah")

    p_main = sub.add_parser("main", help="main permainan baru")
    p_main.add_argument(
        "--pemain", default="",
        help='nama pemain manusia, pisah koma, contoh: "Ani,Budi"')
    p_main.add_argument(
        "--komputer", type=int, default=0,
        help="jumlah pemain komputer yang ditambahkan (0-4)")
    p_main.set_defaults(fungsi=perintah_main)

    p_demo = sub.add_parser("demo", help="demo komputer vs komputer")
    p_demo.add_argument(
        "--pemain", type=int, default=2,
        help="jumlah pemain komputer (2-4, default 2)")
    p_demo.set_defaults(fungsi=perintah_demo)

    p_papan = sub.add_parser("papan", help="tampilkan papan kosong")
    p_papan.set_defaults(
        fungsi=lambda args: (tampilkan_papan({}), 0)[1])

    p_stat = sub.add_parser("statistik", help="tampilkan statistik")
    p_stat.set_defaults(
        fungsi=lambda args: (tampilkan_statistik(muat_data()), 0)[1])

    p_riwayat = sub.add_parser("riwayat", help="tampilkan riwayat")
    p_riwayat.add_argument(
        "--jumlah", type=int, default=10,
        help="jumlah entri yang ditampilkan (default 10)")
    p_riwayat.set_defaults(
        fungsi=lambda args: (tampilkan_riwayat(muat_data(), args.jumlah),
                             0)[1])

    p_reset = sub.add_parser("reset", help="hapus statistik dan riwayat")
    p_reset.add_argument("--ya", action="store_true",
                         help="konfirmasi penghapusan")
    p_reset.set_defaults(fungsi=perintah_reset)
    return parser


def main(argv=None):
    """Titik masuk program."""
    parser = bangun_parser()
    args = parser.parse_args(argv)
    if args.daftar:
        daftar_ular_tangga()
        return 0
    if hasattr(args, "fungsi"):
        if args.perintah == "demo" and not (
                JUMLAH_PEMAIN_MIN <= args.pemain <= JUMLAH_PEMAIN_MAKS):
            print(f"Jumlah pemain demo harus "
                  f"{JUMLAH_PEMAIN_MIN}-{JUMLAH_PEMAIN_MAKS}.")
            return 1
        if args.perintah == "main" and not (
                0 <= args.komputer <= JUMLAH_PEMAIN_MAKS):
            print("Jumlah pemain komputer harus 0-4.")
            return 1
        return args.fungsi(args)
    return menu_interaktif()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (EOFError, KeyboardInterrupt):
        print("\nPermainan dihentikan. Sampai jumpa!")
        sys.exit(0)
