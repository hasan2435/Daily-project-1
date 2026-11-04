#!/usr/bin/env python3
"""Generator Kata Sandi Aman dan Penilai Kekuatannya.

Program terminal untuk membuat kata sandi acak yang kuat dan menilai
kekuatan kata sandi yang sudah ada. Kata sandi dibuat dengan modul
``secrets`` dari pustaka standar Python, yang dirancang untuk keperluan
kriptografi, bukan sekadar acak biasa.

Fitur:
  - Panjang kata sandi bisa diatur (default 16 karakter).
  - Bisa membuat beberapa kata sandi sekaligus.
  - Memastikan setiap kata sandi memuat minimal satu karakter dari tiap
    kelompok yang diaktifkan (huruf kecil, huruf besar, angka, simbol).
  - Opsi untuk menonaktifkan angka, huruf besar, atau simbol.
  - Opsi untuk mengecualikan karakter yang mudah tertukar, seperti
    huruf l, I, O dan angka 1, 0.
  - Mode penilaian: beri skor 0-100 dan label untuk kata sandi apa pun.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.
"""

import argparse
import secrets
import string
import sys

HURUF_KECIL = string.ascii_lowercase
HURUF_BESAR = string.ascii_uppercase
ANGKA = string.digits
SIMBOL = "!@#$%^&*()-_=+[]{};:,.<>?"
KARAKTER_AMBIGU = set("l1IO0")

PANJANG_DEFAULT = 16
PANJANG_MINIMUM = 4
PANJANG_MAKSIMUM = 128


def kelompok_aktif(tanpa_angka, tanpa_huruf_besar, tanpa_simbol,
                   tanpa_ambigu):
    """Kembalikan daftar kelompok karakter yang dipakai."""
    kelompok = [HURUF_KECIL]
    if not tanpa_huruf_besar:
        kelompok.append(HURUF_BESAR)
    if not tanpa_angka:
        kelompok.append(ANGKA)
    if not tanpa_simbol:
        kelompok.append(SIMBOL)
    if tanpa_ambigu:
        kelompok = [
            "".join(c for c in g if c not in KARAKTER_AMBIGU)
            for g in kelompok
        ]
    return [g for g in kelompok if g]


def buat_satu(panjang, kelompok):
    """Buat satu kata sandi, minimal satu karakter dari tiap kelompok."""
    if panjang < len(kelompok):
        raise ValueError(
            f"Panjang minimal {len(kelompok)} agar tiap kelompok "
            "kebagian satu karakter."
        )
    semua = "".join(kelompok)
    # Satu karakter wajib dari tiap kelompok, sisanya acak dari gabungan.
    wajib = [secrets.choice(g) for g in kelompok]
    sisa = [secrets.choice(semua) for _ in range(panjang - len(kelompok))]
    acak = wajib + sisa
    # Acak urutannya supaya karakter wajib tidak selalu di depan.
    for i in range(len(acak) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        acak[i], acak[j] = acak[j], acak[i]
    return "".join(acak)


def nilai_kekuatan(kata_sandi):
    """Beri skor 0-100 dan label untuk sebuah kata sandi."""
    skor = 0
    panjang = len(kata_sandi)

    # Panjang: sampai 40 poin, 2 poin per karakter sampai 20 karakter.
    skor += min(panjang, 20) * 2

    # Keragaman karakter: sampai 40 poin, 10 poin per kelompok.
    kelompok_ditemukan = 0
    if any(c in HURUF_KECIL for c in kata_sandi):
        kelompok_ditemukan += 1
    if any(c in HURUF_BESAR for c in kata_sandi):
        kelompok_ditemukan += 1
    if any(c in ANGKA for c in kata_sandi):
        kelompok_ditemukan += 1
    if any(c in SIMBOL for c in kata_sandi):
        kelompok_ditemukan += 1
    skor += kelompok_ditemukan * 10

    # Bonus keunikan: sampai 20 poin berdasarkan proporsi karakter unik.
    if kata_sandi:
        unik = len(set(kata_sandi))
        skor += round(unik / panjang * 20)

    skor = min(skor, 100)
    if skor < 40:
        label = "Lemah"
    elif skor < 60:
        label = "Sedang"
    elif skor < 80:
        label = "Kuat"
    else:
        label = "Sangat Kuat"
    return skor, label


def tampilkan_penilaian(kata_sandi):
    """Cetak skor dan label untuk sebuah kata sandi."""
    skor, label = nilai_kekuatan(kata_sandi)
    print(f"Kata sandi : {kata_sandi}")
    print(f"Panjang    : {len(kata_sandi)} karakter")
    print(f"Skor       : {skor}/100 ({label})")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Buat kata sandi acak yang kuat atau nilai kekuatannya."
    )
    parser.add_argument(
        "--panjang", type=int, default=PANJANG_DEFAULT,
        help=f"Panjang kata sandi (default: {PANJANG_DEFAULT}).",
    )
    parser.add_argument(
        "--jumlah", type=int, default=1,
        help="Jumlah kata sandi yang dibuat (default: 1).",
    )
    parser.add_argument(
        "--tanpa-angka", action="store_true",
        help="Jangan pakai angka.",
    )
    parser.add_argument(
        "--tanpa-huruf-besar", action="store_true",
        help="Jangan pakai huruf besar.",
    )
    parser.add_argument(
        "--tanpa-simbol", action="store_true",
        help="Jangan pakai simbol.",
    )
    parser.add_argument(
        "--tanpa-ambigu", action="store_true",
        help="Kecualikan karakter yang mudah tertukar (l, 1, I, O, 0).",
    )
    parser.add_argument(
        "--nilai", metavar="KATA_SANDI",
        help="Nilai kekuatan kata sandi yang diberikan, tanpa membuat baru.",
    )
    args = parser.parse_args(argv)

    if args.nilai is not None:
        if not args.nilai:
            print("Kata sandi yang dinilai tidak boleh kosong.",
                  file=sys.stderr)
            return 1
        tampilkan_penilaian(args.nilai)
        return 0

    if not PANJANG_MINIMUM <= args.panjang <= PANJANG_MAKSIMUM:
        print(
            f"Panjang harus antara {PANJANG_MINIMUM} dan "
            f"{PANJANG_MAKSIMUM}.",
            file=sys.stderr,
        )
        return 1
    if args.jumlah < 1:
        print("Jumlah minimal 1.", file=sys.stderr)
        return 1

    kelompok = kelompok_aktif(
        args.tanpa_angka, args.tanpa_huruf_besar,
        args.tanpa_simbol, args.tanpa_ambigu,
    )
    if not kelompok:
        print("Tidak ada kelompok karakter yang tersisa.", file=sys.stderr)
        return 1

    try:
        for _ in range(args.jumlah):
            kata_sandi = buat_satu(args.panjang, kelompok)
            skor, label = nilai_kekuatan(kata_sandi)
            print(f"{kata_sandi}  ({skor}/100, {label})")
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
