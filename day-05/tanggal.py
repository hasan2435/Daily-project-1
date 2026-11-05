#!/usr/bin/env python3
"""Kalkulator Tanggal — proyek harian ke-5.

Program terminal untuk urusan tanggal sehari-hari, hanya memakai
pustaka standar Python (datetime, argparse, sys):

1. selisih  : hitung jarak dua tanggal, termasuk jumlah hari kerja.
2. tambah   : geser tanggal maju/mundur sejumlah hari.
3. hari     : cari nama hari dari sebuah tanggal.
4. ultah    : hitung usia sekarang dan hari menuju ulang tahun berikut.

Format tanggal yang diterima: YYYY-MM-DD (contoh 2026-11-05) atau
DD/MM/YYYY (contoh 05/11/2026).

Jalankan tanpa argumen untuk mode interaktif.
"""

import argparse
import sys
from datetime import date, datetime, timedelta

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]


def parse_tanggal(teks):
    """Ubah teks menjadi date; terima YYYY-MM-DD atau DD/MM/YYYY."""
    teks = teks.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(teks, fmt).date()
        except ValueError:
            continue
    raise ValueError(
        "Format tanggal tidak dikenali: {!r}. Pakai YYYY-MM-DD "
        "atau DD/MM/YYYY.".format(teks)
    )


def tampilkan(tanggal):
    """Tampilkan tanggal dalam format Indonesia, misal Kamis, 5 November 2026."""
    return "{}, {} {} {}".format(
        HARI[tanggal.weekday()], tanggal.day, BULAN[tanggal.month - 1], tanggal.year
    )


def hitung_hari_kerja(awal, akhir):
    """Hitung hari Senin-Jumat di antara dua tanggal (tidak termasuk tanggal akhir)."""
    if akhir < awal:
        awal, akhir = akhir, awal
    total = 0
    berjalan = awal
    while berjalan < akhir:
        if berjalan.weekday() < 5:
            total += 1
        berjalan += timedelta(days=1)
    return total


def perintah_selisih(awal, akhir):
    jarak = abs((akhir - awal).days)
    kerja = hitung_hari_kerja(awal, akhir)
    arah = "ke depan" if akhir >= awal else "ke belakang"
    print("Dari  : {}".format(tampilkan(awal)))
    print("Ke    : {}".format(tampilkan(akhir)))
    print("Jarak : {} hari ({})".format(jarak, arah))
    print("Hari kerja (Senin-Jumat): {} hari".format(kerja))
    if jarak:
        print("Minggu: {} minggu penuh + {} hari".format(jarak // 7, jarak % 7))


def perintah_tambah(tanggal, jumlah, hanya_kerja=False):
    if not hanya_kerja:
        hasil = tanggal + timedelta(days=jumlah)
    else:
        # Geser hanya lewat hari kerja; jumlah negatif berjalan mundur.
        arah = 1 if jumlah >= 0 else -1
        sisa = abs(jumlah)
        hasil = tanggal
        while sisa:
            hasil += timedelta(days=arah)
            if hasil.weekday() < 5:
                sisa -= 1
    print("Awal  : {}".format(tampilkan(tanggal)))
    print("Geser : {} hari{}".format(jumlah, " kerja" if hanya_kerja else ""))
    print("Hasil : {}".format(tampilkan(hasil)))
    return hasil


def perintah_ultah(lahir, hari_ini):
    # Ulang tahun tahun ini; 29 Februari dirayakan 28 Februari di tahun biasa.
    try:
        tahun_ini = lahir.replace(year=hari_ini.year)
    except ValueError:
        tahun_ini = date(hari_ini.year, 2, 28)
    if tahun_ini < hari_ini:
        try:
            berikut = lahir.replace(year=hari_ini.year + 1)
        except ValueError:
            berikut = date(hari_ini.year + 1, 2, 28)
        usia = hari_ini.year - lahir.year
    else:
        berikut = tahun_ini
        usia = hari_ini.year - lahir.year - (1 if tahun_ini > hari_ini else 0)
    sisa = (berikut - hari_ini).days
    print("Tanggal lahir : {}".format(tampilkan(lahir)))
    print("Usia sekarang : {} tahun".format(usia))
    if sisa == 0:
        print("Selamat ulang tahun! Hari ini berusia {} tahun.".format(usia + 1))
    else:
        print("Ulang tahun berikut: {} ({} hari lagi, usia {})".format(
            tampilkan(berikut), sisa, usia + 1))


def mode_interaktif():
    print("=== Kalkulator Tanggal ===")
    print("1. Selisih dua tanggal")
    print("2. Tambah/kurang hari dari tanggal")
    print("3. Cari nama hari dari tanggal")
    print("4. Hitung menuju ulang tahun")
    pilihan = input("Pilih (1-4): ").strip()
    try:
        if pilihan == "1":
            perintah_selisih(
                parse_tanggal(input("Tanggal awal: ")),
                parse_tanggal(input("Tanggal akhir: ")),
            )
        elif pilihan == "2":
            tanggal = parse_tanggal(input("Tanggal awal: "))
            jumlah = int(input("Jumlah hari (negatif untuk mundur): "))
            kerja = input("Hanya hari kerja? (y/t): ").strip().lower() == "y"
            perintah_tambah(tanggal, jumlah, kerja)
        elif pilihan == "3":
            tanggal = parse_tanggal(input("Tanggal: "))
            print(tampilkan(tanggal))
        elif pilihan == "4":
            perintah_ultah(
                parse_tanggal(input("Tanggal lahir: ")), date.today()
            )
        else:
            print("Pilihan tidak dikenal.")
    except ValueError as err:
        print("Gagal: {}".format(err))
        sys.exit(1)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Kalkulator tanggal di terminal.")
    sub = parser.add_subparsers(dest="perintah")

    p = sub.add_parser("selisih", help="hitung jarak dua tanggal")
    p.add_argument("awal")
    p.add_argument("akhir")

    p = sub.add_parser("tambah", help="geser tanggal sejumlah hari")
    p.add_argument("tanggal")
    p.add_argument("jumlah", type=int)
    p.add_argument("--kerja", action="store_true",
                   help="hitung hanya hari kerja (Senin-Jumat)")

    p = sub.add_parser("hari", help="cari nama hari dari tanggal")
    p.add_argument("tanggal")

    p = sub.add_parser("ultah", help="hitung menuju ulang tahun berikut")
    p.add_argument("lahir")
    p.add_argument("--hari-ini", default=None,
                   help="tanggal acuan YYYY-MM-DD (default: hari ini)")

    args = parser.parse_args(argv)
    try:
        if args.perintah is None:
            mode_interaktif()
        elif args.perintah == "selisih":
            perintah_selisih(parse_tanggal(args.awal), parse_tanggal(args.akhir))
        elif args.perintah == "tambah":
            perintah_tambah(parse_tanggal(args.tanggal), args.jumlah, args.kerja)
        elif args.perintah == "hari":
            print(tampilkan(parse_tanggal(args.tanggal)))
        elif args.perintah == "ultah":
            acuan = parse_tanggal(args.hari_ini) if args.hari_ini else date.today()
            perintah_ultah(parse_tanggal(args.lahir), acuan)
    except ValueError as err:
        print("Gagal: {}".format(err))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
