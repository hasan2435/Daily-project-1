#!/usr/bin/env python3
"""Permainan Minesweeper — Day 28 Daily Project 1.

Main Minesweeper di terminal: buka kotak satu per satu tanpa
mengenai bom. Angka pada kotak yang terbuka menunjukkan jumlah bom
di delapan kotak sekitarnya. Kotak kosong yang dibuka akan membuka
otomatis semua kotak kosong di sekitarnya.

Aturan mainnya:

    - Klik pertama selalu aman: bom baru dipasang setelah kotak
      pertama dibuka, jadi tidak mungkin langsung kalah.
    - Ketik `buka <baris> <kolom>` untuk membuka sebuah kotak.
    - Ketik `tandai <baris> <kolom>` untuk menandai atau mencabut
      bendera pada kotak yang dicurigai berisi bom.
    - Menang bila semua kotak yang bukan bom sudah terbuka.
    - Kalah bila membuka kotak berisi bom.

Ada tiga tingkat kesulitan: mudah (9x9, 10 bom), sedang (16x16,
40 bom), dan sulit (30x16, 99 bom). Baris dan kolom dihitung
mulai dari 1.

Statistik per tingkat kesulitan (main, menang, win rate, dan
waktu terbaik) serta riwayat 20 permainan terakhir disimpan
otomatis.

Python standar saja, tanpa library tambahan.

Cara pakai:
    python3 minesweeper.py
    python3 minesweeper.py main --kesulitan mudah
    python3 minesweeper.py main --kesulitan sedang --benih 7
    python3 minesweeper.py demo
    python3 minesweeper.py demo --kesulitan sulit --benih 42
    python3 minesweeper.py statistik
    python3 minesweeper.py riwayat
    python3 minesweeper.py riwayat --jumlah 5
    python3 minesweeper.py reset --ya
    python3 minesweeper.py --daftar

Jalankan tanpa argumen untuk mode interaktif (menu angka).

Data disimpan di berkas `minesweeper.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek.
"""

import argparse
import json
import os
import random
import sys
import time
from datetime import datetime

BERKAS_DATA = "minesweeper.json"
RIWAYAT_MAKS = 20

# Nama kesulitan -> (jumlah baris, jumlah kolom, jumlah bom).
KESULITAN = {
    "mudah": {"baris": 9, "kolom": 9, "bom": 10},
    "sedang": {"baris": 16, "kolom": 16, "bom": 40},
    "sulit": {"baris": 16, "kolom": 30, "bom": 99},
}

# Delapan arah di sekitar sebuah kotak.
ARAH = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def buat_papan(baris, kolom, jumlah_bom, aman=None, rng=None):
    """Buat papan baru. Tiap kotak: bom, terbuka, bendera, tetangga.

    `aman` adalah (baris, kolom) kotak pertama yang dibuka; bom
    tidak pernah dipasang di sana, supaya klik pertama selalu aman.
    """
    rng = rng or random
    papan = [
        [{"bom": False, "terbuka": False, "bendera": False, "tetangga": 0}
         for _ in range(kolom)]
        for _ in range(baris)
    ]
    semua = [(r, c) for r in range(baris) for c in range(kolom)]
    if aman is not None:
        semua.remove(aman)
    for r, c in rng.sample(semua, jumlah_bom):
        papan[r][c]["bom"] = True
    for r in range(baris):
        for c in range(kolom):
            papan[r][c]["tetangga"] = sum(
                1
                for dr, dc in ARAH
                if 0 <= r + dr < baris
                and 0 <= c + dc < kolom
                and papan[r + dr][c + dc]["bom"]
            )
    return papan


def kotak_sekitar(baris, kolom, r, c):
    """Daftar koordinat (r, c) delapan kotak di sekitar sebuah kotak."""
    return [
        (r + dr, c + dc)
        for dr, dc in ARAH
        if 0 <= r + dr < baris and 0 <= c + dc < kolom
    ]


def buka_kotak(papan, r, c):
    """Buka sebuah kotak dan, bila kosong, buka kotak sekitarnya.

    Mengembalikan jumlah kotak yang ikut terbuka, atau -1 bila
    kotak yang dibuka berisi bom.
    """
    kotak = papan[r][c]
    if kotak["terbuka"] or kotak["bendera"]:
        return 0
    kotak["terbuka"] = True
    if kotak["bom"]:
        return -1
    dibuka = 1
    if kotak["tetangga"] == 0:
        # Banjir: buka semua kotak kosong yang terhubung.
        tumpukan = [(r, c)]
        while tumpukan:
            br, bc = tumpukan.pop()
            for nr, nc in kotak_sekitar(len(papan), len(papan[0]), br, bc):
                tetangga = papan[nr][nc]
                if tetangga["terbuka"] or tetangga["bendera"] or tetangga["bom"]:
                    continue
                tetangga["terbuka"] = True
                dibuka += 1
                if tetangga["tetangga"] == 0:
                    tumpukan.append((nr, nc))
    return dibuka


def jumlah_terbuka(papan):
    """Jumlah kotak yang sudah terbuka."""
    return sum(1 for baris in papan for kotak in baris if kotak["terbuka"])


def jumlah_bendera(papan):
    """Jumlah bendera yang terpasang."""
    return sum(1 for baris in papan for kotak in baris if kotak["bendera"])


def cek_menang(papan, jumlah_bom):
    """Menang bila semua kotak yang bukan bom sudah terbuka."""
    total = len(papan) * len(papan[0])
    return jumlah_terbuka(papan) == total - jumlah_bom


def tampilkan_papan(papan, buka_semua=False):
    """Cetak papan ke terminal.

    Simbol: '.' kotak tertutup, 'F' bendera, ' ' kotak kosong
    terbuka, angka jumlah bom tetangga, '*' bom (bila dibuka).
    """
    baris = len(papan)
    kolom = len(papan[0])
    lebar = len(str(baris))
    print("   " + " ".join(f"{c + 1:>{lebar}}" for c in range(kolom)))
    for r in range(baris):
        sel = []
        for c in range(kolom):
            kotak = papan[r][c]
            if kotak["terbuka"] or buka_semua:
                if kotak["bom"]:
                    sel.append("*")
                elif kotak["tetangga"] == 0:
                    sel.append(" ")
                else:
                    sel.append(str(kotak["tetangga"]))
            elif kotak["bendera"]:
                sel.append("F")
            else:
                sel.append(".")
        print(f"{r + 1:>{lebar}}  " + " ".join(f"{s:>{lebar}}" for s in sel))


def muat_data():
    """Muat statistik dan riwayat dari berkas data."""
    data = {"statistik": {}, "riwayat": []}
    if os.path.exists(BERKAS_DATA):
        try:
            with open(BERKAS_DATA, "r", encoding="utf-8") as f:
                isi = json.load(f)
            if isinstance(isi, dict):
                data["statistik"] = isi.get("statistik", {}) or {}
                data["riwayat"] = isi.get("riwayat", []) or []
        except (OSError, ValueError):
            pass
    for nama in KESULITAN:
        data["statistik"].setdefault(
            nama, {"main": 0, "menang": 0, "waktu_terbaik": None}
        )
    return data


def simpan_data(data):
    """Simpan statistik dan riwayat ke berkas data."""
    try:
        with open(BERKAS_DATA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as err:
        print(f"Tidak bisa menyimpan data: {err}")


def catat_hasil(data, nama, menang, detik):
    """Catat satu permainan selesai ke statistik dan riwayat."""
    stat = data["statistik"].setdefault(
        nama, {"main": 0, "menang": 0, "waktu_terbaik": None}
    )
    stat["main"] += 1
    if menang:
        stat["menang"] += 1
        if stat["waktu_terbaik"] is None or detik < stat["waktu_terbaik"]:
            stat["waktu_terbaik"] = detik
    data["riwayat"].insert(
        0,
        {
            "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "kesulitan": nama,
            "hasil": "menang" if menang else "kalah",
            "waktu_detik": detik,
        },
    )
    data["riwayat"] = data["riwayat"][:RIWAYAT_MAKS]
    simpan_data(data)


def format_waktu(detik):
    """Format detik menjadi mm:ss."""
    if detik is None:
        return "-"
    return f"{int(detik) // 60:02d}:{int(detik) % 60:02d}"


def tampilkan_statistik(data):
    """Tampilkan tabel statistik per tingkat kesulitan."""
    print("=== Statistik Minesweeper ===")
    print(f"{'Kesulitan':<10} {'Main':>5} {'Menang':>6} {'Win rate':>9} {'Terbaik':>8}")
    print("-" * 46)
    total_main = 0
    total_menang = 0
    for nama in KESULITAN:
        stat = data["statistik"].get(nama, {"main": 0, "menang": 0, "waktu_terbaik": None})
        total_main += stat["main"]
        total_menang += stat["menang"]
        rate = (stat["menang"] / stat["main"] * 100) if stat["main"] else 0.0
        print(
            f"{nama:<10} {stat['main']:>5} {stat['menang']:>6} "
            f"{rate:>8.1f}% {format_waktu(stat['waktu_terbaik']):>8}"
        )
    print("-" * 46)
    rate = (total_menang / total_main * 100) if total_main else 0.0
    print(f"Total: {total_main} permainan, {total_menang} menang ({rate:.1f}%).")


def tampilkan_riwayat(data, jumlah=10):
    """Tampilkan riwayat permainan terakhir."""
    riwayat = data["riwayat"][:jumlah]
    if not riwayat:
        print("Belum ada riwayat permainan.")
        return
    print(f"=== Riwayat Minesweeper ({len(riwayat)} terakhir) ===")
    for entri in riwayat:
        print(
            f"{entri['tanggal']}  {entri['kesulitan']:<7} "
            f"{entri['hasil']:<6}  {format_waktu(entri['waktu_detik'])}"
        )


def tampilkan_daftar():
    """Tampilkan daftar tingkat kesulitan."""
    print("=== Tingkat Kesulitan ===")
    for nama, cfg in KESULITAN.items():
        print(
            f"{nama:<7} papan {cfg['baris']}x{cfg['kolom']}, "
            f"{cfg['bom']} bom"
        )
    print("\nContoh: python3 minesweeper.py main --kesulitan sedang")


def mainkan(nama, benih=None, interaktif=True, langkah_otomatis=None):
    """Jalankan satu permainan Minesweeper.

    `langkah_otomatis` dipakai mode demo: fungsi yang menerima
    papan dan mengembalikan (baris, kolom) kotak berikutnya, atau
    None bila tidak ada langkah lagi.
    Mengembalikan True bila menang, False bila kalah.
    """
    cfg = KESULITAN[nama]
    baris, kolom, jumlah_bom = cfg["baris"], cfg["kolom"], cfg["bom"]
    rng = random.Random(benih) if benih is not None else random
    papan = None
    mulai = None
    print(f"=== Minesweeper — {nama} ({baris}x{kolom}, {jumlah_bom} bom) ===")
    print("Perintah: buka <baris> <kolom> | tandai <baris> <kolom> | keluar")
    while True:
        if papan is None:
            # Papan kosong sampai klik pertama, supaya bom bisa
            # dipasang menghindari kotak pertama yang dibuka.
            papan = [
                [{"bom": False, "terbuka": False, "bendera": False, "tetangga": 0}
                 for _ in range(kolom)]
                for _ in range(baris)
            ]
        tampilkan_papan(papan)
        sisa = jumlah_bom - jumlah_bendera(papan)
        print(f"Bom tersisa (perkiraan): {sisa}  |  Terbuka: {jumlah_terbuka(papan)}")
        if langkah_otomatis is not None:
            langkah = langkah_otomatis(papan)
            if langkah is None:
                print("Demo berhenti: tidak ada langkah lagi.")
                return False
            r, c = langkah
            aksi = "buka"
            print(f"> buka {r + 1} {c + 1}")
        elif not interaktif:
            return False
        else:
            try:
                perintah = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nPermainan dibatalkan.")
                return False
            if perintah in ("keluar", "exit", "q"):
                print("Permainan dibatalkan.")
                return False
            bagian = perintah.split()
            if len(bagian) != 3 or bagian[0] not in ("buka", "tandai"):
                print("Perintah tidak dikenal. Contoh: buka 3 4")
                continue
            aksi = bagian[0]
            try:
                r = int(bagian[1]) - 1
                c = int(bagian[2]) - 1
            except ValueError:
                print("Baris dan kolom harus angka. Contoh: buka 3 4")
                continue
            if not (0 <= r < baris and 0 <= c < kolom):
                print(f"Di luar papan. Baris 1-{baris}, kolom 1-{kolom}.")
                continue
        if aksi == "tandai":
            kotak = papan[r][c]
            if kotak["terbuka"]:
                print("Kotak itu sudah terbuka, tidak bisa ditandai.")
                continue
            kotak["bendera"] = not kotak["bendera"]
            print(f"{'Diberi' if kotak['bendera'] else 'Dicabut'} bendera di {r + 1},{c + 1}.")
            continue
        # Aksi buka.
        kotak = papan[r][c]
        if kotak["terbuka"]:
            print("Kotak itu sudah terbuka.")
            continue
        if kotak["bendera"]:
            print("Kotak itu berbendera. Cabut dulu dengan: tandai "
                  f"{r + 1} {c + 1}")
            continue
        if mulai is None:
            mulai = time.time()
            papan = buat_papan(baris, kolom, jumlah_bom, aman=(r, c), rng=rng)
            kotak = papan[r][c]
        hasil = buka_kotak(papan, r, c)
        if hasil == -1:
            tampilkan_papan(papan, buka_semua=True)
            detik = int(time.time() - mulai)
            print(f"\n💥 BOOM! Kena bom di {r + 1},{c + 1} setelah "
                  f"{format_waktu(detik)}.")
            data = muat_data()
            catat_hasil(data, nama, False, detik)
            return False
        if cek_menang(papan, jumlah_bom):
            tampilkan_papan(papan, buka_semua=True)
            detik = int(time.time() - mulai)
            print(f"\n🎉 MENANG! Semua {jumlah_bom} bom berhasil dihindari "
                  f"dalam {format_waktu(detik)}.")
            data = muat_data()
            catat_hasil(data, nama, True, detik)
            return True


def langkah_acak(papan):
    """Pilih kotak tertutup tanpa bendera secara acak (untuk demo)."""
    pilihan = [
        (r, c)
        for r, baris in enumerate(papan)
        for c, kotak in enumerate(baris)
        if not kotak["terbuka"] and not kotak["bendera"]
    ]
    return random.choice(pilihan) if pilihan else None


def tanya(pesan):
    """Minta masukan teks dari pengguna."""
    try:
        return input(pesan).strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def menu_interaktif():
    """Menu angka untuk mode interaktif."""
    while True:
        print("\n=== Permainan Minesweeper ===")
        print("1. Main baru")
        print("2. Demo (komputer bermain sendiri)")
        print("3. Statistik")
        print("4. Riwayat")
        print("5. Daftar tingkat kesulitan")
        print("0. Keluar")
        pilihan = tanya("Pilih (0-5): ")
        if pilihan == "0" or pilihan == "":
            print("Sampai jumpa!")
            return
        if pilihan == "1":
            nama = tanya("Kesulitan (mudah/sedang/sulit) [mudah]: ") or "mudah"
            if nama not in KESULITAN:
                print("Kesulitan tidak dikenal.")
                continue
            mainkan(nama)
        elif pilihan == "2":
            nama = tanya("Kesulitan (mudah/sedang/sulit) [mudah]: ") or "mudah"
            if nama not in KESULITAN:
                print("Kesulitan tidak dikenal.")
                continue
            mainkan(nama, langkah_otomatis=langkah_acak)
        elif pilihan == "3":
            tampilkan_statistik(muat_data())
        elif pilihan == "4":
            tampilkan_riwayat(muat_data())
        elif pilihan == "5":
            tampilkan_daftar()
        else:
            print("Pilihan tidak dikenal.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Permainan Minesweeper di terminal."
    )
    parser.add_argument("--daftar", action="store_true",
                        help="tampilkan tingkat kesulitan")
    sub = parser.add_subparsers(dest="perintah")

    p_main = sub.add_parser("main", help="mulai permainan baru")
    p_main.add_argument("--kesulitan", default="mudah", choices=list(KESULITAN))
    p_main.add_argument("--benih", type=int, default=None,
                        help="benih acak (untuk mengulang papan yang sama)")

    p_demo = sub.add_parser("demo", help="komputer bermain sendiri")
    p_demo.add_argument("--kesulitan", default="mudah", choices=list(KESULITAN))
    p_demo.add_argument("--benih", type=int, default=None,
                        help="benih acak (untuk mengulang permainan yang sama)")

    sub.add_parser("statistik", help="tampilkan statistik permainan")

    p_riwayat = sub.add_parser("riwayat", help="tampilkan riwayat permainan")
    p_riwayat.add_argument("--jumlah", type=int, default=10)

    p_reset = sub.add_parser("reset", help="hapus statistik dan riwayat")
    p_reset.add_argument("--ya", action="store_true",
                         help="konfirmasi penghapusan")

    args = parser.parse_args(argv)
    if args.daftar:
        tampilkan_daftar()
        return 0
    if args.perintah == "main":
        if args.benih is not None:
            random.seed(args.benih)
        mainkan(args.kesulitan, benih=args.benih)
    elif args.perintah == "demo":
        if args.benih is not None:
            random.seed(args.benih)
        mainkan(args.kesulitan, benih=args.benih,
                langkah_otomatis=langkah_acak)
    elif args.perintah == "statistik":
        tampilkan_statistik(muat_data())
    elif args.perintah == "riwayat":
        tampilkan_riwayat(muat_data(), jumlah=args.jumlah)
    elif args.perintah == "reset":
        if not args.ya:
            print("Tambahkan --ya untuk mengonfirmasi penghapusan.")
            return 1
        try:
            os.remove(BERKAS_DATA)
        except FileNotFoundError:
            pass
        except OSError as err:
            print(f"Tidak bisa menghapus data: {err}")
            return 1
        print("Statistik dan riwayat sudah dihapus.")
    else:
        menu_interaktif()
    return 0


if __name__ == "__main__":
    sys.exit(main())
