#!/usr/bin/env python3
"""Kalkulator Waktu Tidur — proyek harian ke-11.

Program terminal untuk menghitung jam tidur dan jam bangun yang ideal
berdasarkan siklus tidur 90 menit. Satu siklus tidur berlangsung
sekitar 90 menit; orang dewasa umumnya butuh 5-6 siklus (7,5-9 jam)
per malam. Program menghitung mundur dari jam bangun yang diinginkan
atau maju dari jam tidur, dengan memperhitungkan waktu yang dibutuhkan
untuk tertidur (default 15 menit).

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

Cara memakai (mode perintah):

    python3 tidur.py bangun 06:00
    python3 tidur.py tidur 23:00
    python3 tidur.py sekarang
    python3 tidur.py durasi 23:00 06:00
    python3 tidur.py bangun 06:30 --tertidur 20

Jalankan tanpa argumen untuk mode interaktif.

Ini panduan umum, bukan saran medis: kebutuhan tidur tiap orang
bisa berbeda, dan kualitas tidur sama pentingnya dengan lamanya.
"""

import argparse
import sys
from datetime import datetime, time, timedelta

# Satu siklus tidur sekitar 90 menit. Orang dewasa umumnya butuh 5-6
# siklus (7,5-9 jam); 3 siklus (4,5 jam) adalah batas bawah yang
# ditampilkan supaya masih ada pilihan bila memang terpaksa.
SIKLUS_MENIT = 90
SIKLUS_MIN = 3
SIKLUS_MAKS = 6
SIKLUS_DISARANKAN = (5, 6)
TERTIDUR_DEFAULT = 15
TERTIDUR_MAKS = 60


def jam_argumen(teks):
    """Ubah teks JJ:MM menjadi time; lempar ValueError bila salah."""
    try:
        jam, menit = teks.split(":")
        hasil = time(int(jam), int(menit))
    except ValueError:
        raise ValueError(
            "jam harus berformat JJ:MM, contoh 06:00 atau 23:30"
        )
    return hasil


def ke_menit(waktu):
    """Ubah time menjadi menit sejak tengah malam."""
    return waktu.hour * 60 + waktu.minute


def dari_menit(menit):
    """Ubah menit sejak tengah malam menjadi teks JJ:MM (melintasi
    tengah malam bila perlu)."""
    menit %= 24 * 60
    return f"{menit // 60:02d}:{menit % 60:02d}"


def format_durasi(menit):
    """Format jumlah menit menjadi 'X jam Y menit'."""
    jam, sisa = divmod(menit, 60)
    if jam == 0:
        return f"{sisa} menit"
    if sisa == 0:
        return f"{jam} jam"
    return f"{jam} jam {sisa} menit"


def keterangan_siklus(siklus):
    """Keterangan singkat untuk jumlah siklus tertentu."""
    if siklus in SIKLUS_DISARANKAN:
        return "disarankan"
    if siklus == 4:
        return "cukup, tapi kurang dari anjuran"
    return "minimal, usahakan lebih lama"


def saran_tidur(jam_bangun, tertidur):
    """Hitung jam tidur untuk tiap jumlah siklus, mundur dari jam
    bangun yang diinginkan. Kembalikan daftar (siklus, jam tidur,
    durasi tidur)."""
    bangun = ke_menit(jam_bangun)
    hasil = []
    for siklus in range(SIKLUS_MAKS, SIKLUS_MIN - 1, -1):
        durasi = siklus * SIKLUS_MENIT
        tidur = bangun - tertidur - durasi
        hasil.append((siklus, dari_menit(tidur), durasi))
    return hasil


def saran_bangun(jam_tidur, tertidur):
    """Hitung jam bangun untuk tiap jumlah siklus, maju dari jam
    tidur. Kembalikan daftar (siklus, jam bangun, durasi tidur)."""
    tidur = ke_menit(jam_tidur)
    hasil = []
    for siklus in range(SIKLUS_MAKS, SIKLUS_MIN - 1, -1):
        durasi = siklus * SIKLUS_MENIT
        bangun = tidur + tertidur + durasi
        hasil.append((siklus, dari_menit(bangun), durasi))
    return hasil


def hitung_durasi(jam_tidur, jam_bangun):
    """Hitung durasi tidur antara dua jam (melintasi tengah malam bila
    perlu). Kembalikan (menit, jumlah siklus)."""
    menit = (ke_menit(jam_bangun) - ke_menit(jam_tidur)) % (24 * 60)
    return menit, menit / SIKLUS_MENIT


def tampilkan_saran(judul, baris, kolom_waktu):
    """Tampilkan daftar saran siklus dalam bentuk tabel sederhana."""
    print(judul)
    print()
    print(f"{'Siklus':<8}{'Durasi':<18}{kolom_waktu:<12}Keterangan")
    print("-" * 60)
    for siklus, jam_teks, durasi in baris:
        print(
            f"{siklus} siklus "
            f"{format_durasi(durasi):<18}"
            f"{jam_teks:<12}"
            f"{keterangan_siklus(siklus)}"
        )
    print()
    print(
        "Bangun di akhir siklus terasa lebih segar daripada terbangun "
        "di tengah siklus."
    )


def perintah_bangun(jam_bangun, tertidur):
    """Tampilkan jam tidur yang disarankan untuk jam bangun tertentu."""
    baris = saran_tidur(jam_bangun, tertidur)
    tampilkan_saran(
        f"Supaya bangun pukul {jam_bangun.strftime('%H:%M')}, "
        f"tidurlah pukul (waktu tertidur ±{tertidur} menit):",
        baris,
        "Jam tidur",
    )


def perintah_tidur(jam_tidur, tertidur):
    """Tampilkan jam bangun yang disarankan untuk jam tidur tertentu."""
    baris = saran_bangun(jam_tidur, tertidur)
    tampilkan_saran(
        f"Kalau tidur pukul {jam_tidur.strftime('%H:%M')}, "
        f"bangunlah pukul (waktu tertidur ±{tertidur} menit):",
        baris,
        "Jam bangun",
    )


def perintah_sekarang(tertidur):
    """Tampilkan jam bangun bila tidur sekarang."""
    sekarang = datetime.now().time().replace(second=0, microsecond=0)
    baris = saran_bangun(sekarang, tertidur)
    tampilkan_saran(
        f"Kalau tidur sekarang ({sekarang.strftime('%H:%M')}), "
        f"bangunlah pukul (waktu tertidur ±{tertidur} menit):",
        baris,
        "Jam bangun",
    )


def perintah_durasi(jam_tidur, jam_bangun):
    """Tampilkan durasi tidur antara jam tidur dan jam bangun."""
    menit, siklus = hitung_durasi(jam_tidur, jam_bangun)
    print(
        f"Tidur {jam_tidur.strftime('%H:%M')} - "
        f"bangun {jam_bangun.strftime('%H:%M')}: "
        f"{format_durasi(menit)} "
        f"(±{siklus:.1f} siklus tidur)."
    )
    if siklus < SIKLUS_MIN:
        print("Itu kurang dari 3 siklus — tidurnya sangat pendek.")
    elif siklus < SIKLUS_DISARANKAN[0]:
        print("Itu di bawah anjuran 5-6 siklus (7,5-9 jam).")
    elif siklus <= SIKLUS_MAKS:
        print("Itu sudah dalam rentang anjuran 5-6 siklus (7,5-9 jam).")
    else:
        print("Itu lebih dari 6 siklus — tidur yang panjang.")


def baca_jam(pesan):
    """Minta jam JJ:MM dari pengguna; ulangi bila formatnya salah."""
    while True:
        teks = input(pesan).strip()
        try:
            return jam_argumen(teks)
        except ValueError as galat:
            print(galat)


def baca_tertidur():
    """Minta waktu tertidur (menit) dari pengguna; kosong = default."""
    while True:
        teks = input(
            f"Waktu yang dibutuhkan untuk tertidur dalam menit "
            f"(0-{TERTIDUR_MAKS}, kosong = {TERTIDUR_DEFAULT}): "
        ).strip()
        if not teks:
            return TERTIDUR_DEFAULT
        try:
            nilai = int(teks)
        except ValueError:
            print("Masukkan angka menit, contoh 15.")
            continue
        if not 0 <= nilai <= TERTIDUR_MAKS:
            print(f"Waktu tertidur harus antara 0 dan {TERTIDUR_MAKS} menit.")
            continue
        return nilai


def mode_interaktif():
    """Menu interaktif untuk pengguna yang menjalankan tanpa argumen."""
    print("Kalkulator Waktu Tidur")
    print("======================")
    print("Hitung jam tidur dan jam bangun ideal dari siklus 90 menit.")
    print()
    while True:
        print("1. Cari jam tidur (dari jam bangun)")
        print("2. Cari jam bangun (dari jam tidur)")
        print("3. Cari jam bangun (kalau tidur sekarang)")
        print("4. Hitung durasi tidur")
        print("0. Keluar")
        pilihan = input("Pilih menu (0-4): ").strip()
        print()
        if pilihan == "0":
            print("Selamat tidur, semoga bangun segar!")
            return
        if pilihan == "1":
            jam_bangun = baca_jam("Jam bangun yang diinginkan (JJ:MM): ")
            perintah_bangun(jam_bangun, baca_tertidur())
        elif pilihan == "2":
            jam_tidur = baca_jam("Jam tidur (JJ:MM): ")
            perintah_tidur(jam_tidur, baca_tertidur())
        elif pilihan == "3":
            perintah_sekarang(baca_tertidur())
        elif pilihan == "4":
            jam_tidur = baca_jam("Jam tidur (JJ:MM): ")
            jam_bangun = baca_jam("Jam bangun (JJ:MM): ")
            perintah_durasi(jam_tidur, jam_bangun)
        else:
            print("Pilihan tidak dikenal, coba lagi.")
        print()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Kalkulator Waktu Tidur: hitung jam tidur dan jam "
        "bangun ideal berdasarkan siklus tidur 90 menit."
    )
    # Opsi --tertidur tersedia di tiap subperintah supaya bisa ditulis
    # setelah nama perintah, contoh: tidur.py bangun 06:30 --tertidur 20.
    induk = argparse.ArgumentParser(add_help=False)
    induk.add_argument(
        "--tertidur", type=int, default=TERTIDUR_DEFAULT,
        help="Waktu yang dibutuhkan untuk tertidur, dalam menit "
        f"(0-{TERTIDUR_MAKS}, default {TERTIDUR_DEFAULT})",
    )
    parser.set_defaults(tertidur=TERTIDUR_DEFAULT)
    sub = parser.add_subparsers(dest="perintah")

    p_bangun = sub.add_parser(
        "bangun", parents=[induk],
        help="Cari jam tidur dari jam bangun yang diinginkan",
    )
    p_bangun.add_argument("jam", type=jam_argumen, help="Jam bangun (JJ:MM)")

    p_tidur = sub.add_parser(
        "tidur", parents=[induk], help="Cari jam bangun dari jam tidur"
    )
    p_tidur.add_argument("jam", type=jam_argumen, help="Jam tidur (JJ:MM)")

    sub.add_parser(
        "sekarang", parents=[induk],
        help="Cari jam bangun bila tidur sekarang",
    )

    p_durasi = sub.add_parser(
        "durasi", help="Hitung durasi tidur antara dua jam"
    )
    p_durasi.add_argument("tidur", type=jam_argumen, help="Jam tidur (JJ:MM)")
    p_durasi.add_argument("bangun", type=jam_argumen, help="Jam bangun (JJ:MM)")

    args = parser.parse_args(argv)
    if not 0 <= args.tertidur <= TERTIDUR_MAKS:
        parser.error(
            f"--tertidur harus antara 0 dan {TERTIDUR_MAKS} menit."
        )
    if args.perintah is None:
        mode_interaktif()
        return 0

    if args.perintah == "bangun":
        perintah_bangun(args.jam, args.tertidur)
    elif args.perintah == "tidur":
        perintah_tidur(args.jam, args.tertidur)
    elif args.perintah == "sekarang":
        perintah_sekarang(args.tertidur)
    elif args.perintah == "durasi":
        perintah_durasi(args.tidur, args.bangun)
    return 0


if __name__ == "__main__":
    sys.exit(main())
