#!/usr/bin/env python3
"""Permainan Sudoku di Terminal — Day 21 Daily Project 1.

Buat teka-teki Sudoku baru, mainkan di terminal, minta petunjuk,
atau selesaikan teka-teki dari luar. Semua teka-teki yang dibuat
dijamin punya tepat satu solusi.

Python standar saja, tanpa library tambahan.

Cara pakai:
    python3 sudoku.py
    python3 sudoku.py main --kesulitan sedang
    python3 sudoku.py buat --kesulitan sulit
    python3 sudoku.py buat --kesulitan mudah --solusi
    python3 sudoku.py selesaikan 530070000600195000098000060800060003400803001700020006060000280000419005000080079

Jalankan tanpa argumen untuk mode interaktif (menu angka).

Perintah saat bermain:
    baris kolom angka   isi sel, contoh: 1 3 5
    hapus baris kolom   hapus isi sel, contoh: hapus 1 3
    petunjuk            isi satu sel kosong dengan jawaban benar (maks 3x)
    cek                 periksa apakah semua isian sejauh ini benar
    papan               tampilkan lagi papannya
    keluar              berhenti bermain
"""

import argparse
import random
import sys
import time

UKURAN = 9
KOTAK = 3

# Jumlah petunjuk awal per tingkat kesulitan.
PETUNJUK = {"mudah": 36, "sedang": 30, "sulit": 25}
BATAS_PETUNJUK = 3
MAKS_SALAH = 3


def papan_kosong():
    """Buat papan 9x9 berisi 0 (sel kosong)."""
    return [[0 for _ in range(UKURAN)] for _ in range(UKURAN)]


def salin(papan):
    return [baris[:] for baris in papan]


def boleh(papan, baris, kolom, angka):
    """Cek apakah angka boleh ditaruh di sel (baris, kolom)."""
    if angka in papan[baris]:
        return False
    for b in range(UKURAN):
        if papan[b][kolom] == angka:
            return False
    awal_baris = (baris // KOTAK) * KOTAK
    awal_kolom = (kolom // KOTAK) * KOTAK
    for b in range(awal_baris, awal_baris + KOTAK):
        for k in range(awal_kolom, awal_kolom + KOTAK):
            if papan[b][k] == angka:
                return False
    return True


def sel_kosong(papan):
    """Cari sel kosong pertama, atau None bila papan penuh."""
    for baris in range(UKURAN):
        for kolom in range(UKURAN):
            if papan[baris][kolom] == 0:
                return baris, kolom
    return None


def selesaikan_papan(papan, acak=False):
    """Isi papan dengan backtracking. Mengembalikan True bila terisi penuh."""
    kosong = sel_kosong(papan)
    if kosong is None:
        return True
    baris, kolom = kosong
    angka_angka = list(range(1, 10))
    if acak:
        random.shuffle(angka_angka)
    for angka in angka_angka:
        if boleh(papan, baris, kolom, angka):
            papan[baris][kolom] = angka
            if selesaikan_papan(papan, acak):
                return True
            papan[baris][kolom] = 0
    return False


def hitung_solusi(papan, batas=2):
    """Hitung jumlah solusi, berhenti begitu mencapai batas."""
    kosong = sel_kosong(papan)
    if kosong is None:
        return 1
    baris, kolom = kosong
    total = 0
    for angka in range(1, 10):
        if boleh(papan, baris, kolom, angka):
            papan[baris][kolom] = angka
            total += hitung_solusi(papan, batas)
            papan[baris][kolom] = 0
            if total >= batas:
                return total
    return total


def buat_papan_penuh():
    """Buat papan Sudoku yang terisi penuh secara acak."""
    papan = papan_kosong()
    selesaikan_papan(papan, acak=True)
    return papan


def buat_teka_teki(kesulitan="sedang"):
    """Buat teka-teki dengan tepat satu solusi.

    Mengembalikan (teka_teki, solusi).
    """
    solusi = buat_papan_penuh()
    teka_teki = salin(solusi)
    target = PETUNJUK[kesulitan]
    posisi = [(b, k) for b in range(UKURAN) for k in range(UKURAN)]
    random.shuffle(posisi)
    terisi = UKURAN * UKURAN
    for baris, kolom in posisi:
        if terisi <= target:
            break
        cadangan = teka_teki[baris][kolom]
        teka_teki[baris][kolom] = 0
        percobaan = salin(teka_teki)
        if hitung_solusi(percobaan, batas=2) != 1:
            teka_teki[baris][kolom] = cadangan
        else:
            terisi -= 1
    return teka_teki, solusi


def tampilkan(papan, tetap=None, salah=None):
    """Tampilkan papan dengan garis pembatas kotak 3x3.

    Sel 'tetap' (petunjuk awal) dicetak tebal, sel 'salah' ditandai *.
    """
    tetap = tetap or set()
    salah = salah or set()
    garis = "+-------+-------+-------+"
    print("    1 2 3   4 5 6   7 8 9")
    print("  " + garis)
    for baris in range(UKURAN):
        sel = []
        for kolom in range(UKURAN):
            nilai = papan[baris][kolom]
            if nilai == 0:
                teks = "."
            elif (baris, kolom) in salah:
                teks = f"{nilai}*"
            elif (baris, kolom) in tetap:
                teks = f"\033[1m{nilai}\033[0m"
            else:
                teks = str(nilai)
            sel.append(f"{teks:>2}")
        print(f"{baris + 1} |" + " ".join(sel[0:3]) + " | "
              + " ".join(sel[3:6]) + " | " + " ".join(sel[6:9]) + " |")
        if baris % KOTAK == KOTAK - 1:
            print("  " + garis)


def hitung_terisi(papan):
    return sum(1 for baris in papan for nilai in baris if nilai != 0)


def selaras_solusi(papan, solusi):
    """Kembalikan daftar sel terisi yang tidak cocok dengan solusi."""
    keliru = []
    for baris in range(UKURAN):
        for kolom in range(UKURAN):
            nilai = papan[baris][kolom]
            if nilai != 0 and nilai != solusi[baris][kolom]:
                keliru.append((baris, kolom))
    return keliru


def baca_teka_teki(teks):
    """Ubah string 81 karakter (0 atau . untuk kosong) menjadi papan."""
    teks = teks.strip().replace(".", "0")
    if len(teks) != 81 or any(c not in "0123456789" for c in teks):
        raise ValueError("Teka-teki harus 81 karakter angka 0-9 (0 atau . untuk sel kosong).")
    papan = papan_kosong()
    for i, c in enumerate(teks):
        papan[i // UKURAN][i % UKURAN] = int(c)
    return papan


def format_papan(papan):
    """Papan menjadi string 81 karakter (0 untuk kosong)."""
    return "".join(str(nilai) for baris in papan for nilai in baris)


def main_buat(args):
    kesulitan = args.kesulitan
    teka_teki, solusi = buat_teka_teki(kesulitan)
    print(f"Teka-teki Sudoku ({kesulitan}, {hitung_terisi(teka_teki)} petunjuk):")
    print()
    tampilkan(teka_teki, tetap={(b, k) for b in range(UKURAN)
                                for k in range(UKURAN)
                                if teka_teki[b][k] != 0})
    print()
    print("String teka-teki (untuk 'selesaikan'):")
    print(format_papan(teka_teki))
    if args.solusi:
        print()
        print("Solusi:")
        tampilkan(solusi)


def main_selesaikan(args):
    try:
        papan = baca_teka_teki(args.teka_teki)
    except ValueError as err:
        print(f"Error: {err}")
        sys.exit(1)
    if hitung_solusi(salin(papan), batas=2) == 0:
        print("Teka-teki ini tidak punya solusi.")
        sys.exit(1)
    if not selesaikan_papan(papan):
        print("Teka-teki ini tidak punya solusi.")
        sys.exit(1)
    print("Solusi:")
    tampilkan(papan)


def main_main(args):
    kesulitan = args.kesulitan
    teka_teki, solusi = buat_teka_teki(kesulitan)
    papan = salin(teka_teki)
    tetap = {(b, k) for b in range(UKURAN)
             for k in range(UKURAN) if teka_teki[b][k] != 0}
    salah = set()
    sisa_petunjuk = BATAS_PETUNJUK
    kesalahan = 0
    mulai = time.time()

    print(f"Sudoku {kesulitan} — {hitung_terisi(teka_teki)} petunjuk, "
          f"{MAKS_SALAH} kali salah, {BATAS_PETUNJUK} petunjuk tersedia.")
    print("Perintah: 'baris kolom angka', 'hapus baris kolom', "
          "'petunjuk', 'cek', 'papan', 'keluar'.")
    print()
    tampilkan(papan, tetap=tetap)

    while True:
        try:
            perintah = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nPermainan dihentikan.")
            return
        if not perintah:
            continue
        if perintah in ("keluar", "exit", "q"):
            print("Permainan dihentikan.")
            return
        if perintah == "papan":
            tampilkan(papan, tetap=tetap, salah=salah)
            continue
        if perintah == "cek":
            keliru = selaras_solusi(papan, solusi)
            if not keliru:
                print("Sejauh ini semua isian benar. Lanjutkan!")
            else:
                print(f"Ada {len(keliru)} isian yang salah:")
                for baris, kolom in keliru:
                    print(f"  - baris {baris + 1}, kolom {kolom + 1}")
            continue
        if perintah == "petunjuk":
            if sisa_petunjuk <= 0:
                print("Petunjuk sudah habis.")
                continue
            kosong = [(b, k) for b in range(UKURAN) for k in range(UKURAN)
                      if papan[b][k] == 0]
            if not kosong:
                print("Tidak ada sel kosong lagi.")
                continue
            baris, kolom = random.choice(kosong)
            papan[baris][kolom] = solusi[baris][kolom]
            salah.discard((baris, kolom))
            sisa_petunjuk -= 1
            print(f"Petunjuk: baris {baris + 1}, kolom {kolom + 1} = "
                  f"{solusi[baris][kolom]} (sisa {sisa_petunjuk}).")
            tampilkan(papan, tetap=tetap, salah=salah)
            if sel_kosong(papan) is None:
                break
            continue

        bagian = perintah.split()
        if bagian[0] == "hapus" and len(bagian) == 3:
            try:
                baris, kolom = int(bagian[1]) - 1, int(bagian[2]) - 1
            except ValueError:
                print("Format: hapus <baris> <kolom>, contoh: hapus 1 3")
                continue
            if not (0 <= baris < UKURAN and 0 <= kolom < UKURAN):
                print("Baris dan kolom harus 1-9.")
                continue
            if (baris, kolom) in tetap:
                print("Sel itu petunjuk awal, tidak bisa dihapus.")
                continue
            papan[baris][kolom] = 0
            salah.discard((baris, kolom))
            tampilkan(papan, tetap=tetap, salah=salah)
            continue

        if len(bagian) == 3:
            try:
                baris, kolom = int(bagian[0]) - 1, int(bagian[1]) - 1
                angka = int(bagian[2])
            except ValueError:
                print("Format: <baris> <kolom> <angka>, contoh: 1 3 5")
                continue
            if not (0 <= baris < UKURAN and 0 <= kolom < UKURAN):
                print("Baris dan kolom harus 1-9.")
                continue
            if not 1 <= angka <= 9:
                print("Angka harus 1-9.")
                continue
            if (baris, kolom) in tetap:
                print("Sel itu petunjuk awal, tidak bisa diubah.")
                continue
            if not boleh(papan, baris, kolom, angka):
                kesalahan += 1
                salah.add((baris, kolom))
                papan[baris][kolom] = angka
                print(f"Angka {angka} tidak boleh di baris {baris + 1}, "
                      f"kolom {kolom + 1} (kesalahan {kesalahan}/{MAKS_SALAH}).")
                tampilkan(papan, tetap=tetap, salah=salah)
                if kesalahan >= MAKS_SALAH:
                    print()
                    print("Kesalahan sudah 3 kali — permainan selesai.")
                    print("Solusinya:")
                    tampilkan(solusi)
                    return
                continue
            papan[baris][kolom] = angka
            salah.discard((baris, kolom))
            tampilkan(papan, tetap=tetap, salah=salah)
            if sel_kosong(papan) is None:
                break
            continue

        print("Perintah tidak dikenal. Contoh: 1 3 5 | hapus 1 3 | "
              "petunjuk | cek | papan | keluar")

    durasi = int(time.time() - mulai)
    menit, detik = divmod(durasi, 60)
    print()
    print(f"Selamat! Sudoku selesai dalam {menit} menit {detik} detik, "
          f"dengan {kesalahan} kesalahan dan {BATAS_PETUNJUK - sisa_petunjuk} "
          f"petunjuk terpakai.")


def menu_interaktif():
    while True:
        print()
        print("=== Sudoku ===")
        print("1. Main (mudah)")
        print("2. Main (sedang)")
        print("3. Main (sulit)")
        print("4. Buat teka-teki baru")
        print("5. Selesaikan teka-teki dari string")
        print("0. Keluar")
        try:
            pilihan = input("Pilih (0-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            return
        if pilihan == "0":
            print("Sampai jumpa!")
            return
        if pilihan in ("1", "2", "3"):
            kesulitan = {"1": "mudah", "2": "sedang", "3": "sulit"}[pilihan]
            main_main(argparse.Namespace(kesulitan=kesulitan))
        elif pilihan == "4":
            kesulitan = input("Kesulitan (mudah/sedang/sulit) [sedang]: ").strip().lower()
            if kesulitan not in PETUNJUK:
                kesulitan = "sedang"
            jawab = input("Tampilkan solusi juga? (y/n) [n]: ").strip().lower()
            main_buat(argparse.Namespace(kesulitan=kesulitan,
                                         solusi=jawab in ("y", "ya")))
        elif pilihan == "5":
            teks = input("Tempel string 81 karakter (0 atau . untuk kosong): ").strip()
            main_selesaikan(argparse.Namespace(teka_teki=teks))
        else:
            print("Pilihan tidak dikenal, coba lagi.")


def main():
    parser = argparse.ArgumentParser(
        description="Permainan Sudoku di terminal: buat, mainkan, atau selesaikan teka-teki.")
    sub = parser.add_subparsers(dest="perintah")

    p_main = sub.add_parser("main", help="mainkan Sudoku baru")
    p_main.add_argument("--kesulitan", choices=list(PETUNJUK),
                        default="sedang", help="tingkat kesulitan (default: sedang)")

    p_buat = sub.add_parser("buat", help="cetak teka-teki Sudoku baru")
    p_buat.add_argument("--kesulitan", choices=list(PETUNJUK),
                        default="sedang", help="tingkat kesulitan (default: sedang)")
    p_buat.add_argument("--solusi", action="store_true",
                        help="tampilkan juga solusinya")

    p_selesai = sub.add_parser("selesaikan", help="selesaikan teka-teki dari string 81 karakter")
    p_selesai.add_argument("teka_teki", help="81 karakter angka 0-9, 0 atau . untuk sel kosong")

    args = parser.parse_args()
    if args.perintah == "main":
        main_main(args)
    elif args.perintah == "buat":
        main_buat(args)
    elif args.perintah == "selesaikan":
        main_selesaikan(args)
    else:
        menu_interaktif()


if __name__ == "__main__":
    main()
