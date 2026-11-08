#!/usr/bin/env python3
"""Konverter Satuan — proyek harian ke-8.

Program terminal untuk mengubah satuan dalam 7 kategori: panjang, berat,
volume, suhu, waktu, kecepatan, dan data. Semua faktor konversi memakai
satuan dasar per kategori, kecuali suhu yang dihitung lewat Celsius karena
melibatkan pergeseran nol (offset), bukan sekadar perkalian.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

Cara memakai (mode perintah):

    python3 konversi.py panjang 5 km m
    python3 konversi.py suhu 100 C F
    python3 konversi.py berat 2.5 kg ons
    python3 konversi.py --daftar

Jalankan tanpa argumen untuk mode interaktif.
"""

import argparse
import sys

# Setiap kategori memetakan satuan -> faktor terhadap satuan dasar.
# Satuan dasar: meter, gram, liter, detik, meter/detik, byte.
KATEGORI = {
    "panjang": {
        "judul": "Panjang (satuan dasar: meter)",
        "satuan": {
            "mm": 0.001,
            "cm": 0.01,
            "m": 1.0,
            "km": 1000.0,
            "inci": 0.0254,
            "kaki": 0.3048,
            "yard": 0.9144,
            "mil": 1609.344,
        },
    },
    "berat": {
        "judul": "Berat (satuan dasar: gram)",
        "satuan": {
            "mg": 0.001,
            "g": 1.0,
            # Ons metrik Indonesia: 1 ons = 100 gram.
            "ons": 100.0,
            "kg": 1000.0,
            "pon": 453.59237,
            "ton": 1000000.0,
        },
    },
    "volume": {
        "judul": "Volume (satuan dasar: liter)",
        "satuan": {
            "ml": 0.001,
            "l": 1.0,
            "m3": 1000.0,
            "galon": 3.78541,
            # Sendok teh dan sendok makan ukuran dapur standar.
            "sdt": 0.005,
            "sdm": 0.015,
            "gelas": 0.25,
        },
    },
    "waktu": {
        "judul": "Waktu (satuan dasar: detik)",
        "satuan": {
            "detik": 1.0,
            "menit": 60.0,
            "jam": 3600.0,
            "hari": 86400.0,
            "minggu": 604800.0,
        },
    },
    "kecepatan": {
        "judul": "Kecepatan (satuan dasar: meter/detik)",
        "satuan": {
            "m/detik": 1.0,
            "km/jam": 1.0 / 3.6,
            "mph": 0.44704,
            "knot": 0.514444,
        },
    },
    "data": {
        "judul": "Data (satuan dasar: byte, kelipatan 1024)",
        "satuan": {
            "bit": 0.125,
            "B": 1.0,
            "KB": 1024.0,
            "MB": 1024.0 ** 2,
            "GB": 1024.0 ** 3,
            "TB": 1024.0 ** 4,
        },
    },
}

# Suhu tidak bisa memakai faktor saja, jadi ditangani terpisah.
# Rumus lewat Celsius: F = C x 9/5 + 32, K = C + 273.15, R = C x 4/5.
SUHU = ("C", "F", "K", "R")
NAMA_SUHU = {"C": "Celsius", "F": "Fahrenheit", "K": "Kelvin", "R": "Reamur"}


def ke_celsius(nilai, satuan):
    """Ubah suhu dari satuan apa pun ke Celsius."""
    if satuan == "C":
        return nilai
    if satuan == "F":
        return (nilai - 32.0) * 5.0 / 9.0
    if satuan == "K":
        return nilai - 273.15
    if satuan == "R":
        return nilai * 5.0 / 4.0
    raise ValueError("Satuan suhu tidak dikenal: %s" % satuan)


def dari_celsius(nilai, satuan):
    """Ubah suhu dari Celsius ke satuan apa pun."""
    if satuan == "C":
        return nilai
    if satuan == "F":
        return nilai * 9.0 / 5.0 + 32.0
    if satuan == "K":
        return nilai + 273.15
    if satuan == "R":
        return nilai * 4.0 / 5.0
    raise ValueError("Satuan suhu tidak dikenal: %s" % satuan)


def konversi(kategori, nilai, dari, ke):
    """Konversi nilai dari satu satuan ke satuan lain dalam satu kategori.

    Mengembalikan hasil sebagai float. Kategori "suhu" ditangani lewat
    Celsius; kategori lain lewat satuan dasar dengan perkalian faktor.
    """
    kategori = kategori.lower()
    if kategori == "suhu":
        dari = dari.upper()
        ke = ke.upper()
        if dari not in SUHU or ke not in SUHU:
            raise ValueError(
                "Satuan suhu harus salah satu dari: %s" % ", ".join(SUHU)
            )
        if dari == "K" and nilai < 0:
            raise ValueError("Suhu Kelvin tidak boleh di bawah 0.")
        hasil = dari_celsius(ke_celsius(nilai, dari), ke)
        if ke == "K" and hasil < 0:
            raise ValueError("Hasilnya di bawah 0 Kelvin, tidak mungkin.")
        return hasil

    if kategori not in KATEGORI:
        raise ValueError(
            "Kategori tidak dikenal: %s. Lihat --daftar." % kategori
        )
    satuan = KATEGORI[kategori]["satuan"]
    # Satuan panjang/berat/volume/waktu/kecepatan tidak peka huruf besar,
    # kecuali "data" karena B, KB, MB, GB, TB memakai huruf besar.
    if kategori != "data":
        dari = dari.lower()
        ke = ke.lower()
    if dari not in satuan:
        raise ValueError(
            "Satuan '%s' tidak ada di kategori %s." % (dari, kategori)
        )
    if ke not in satuan:
        raise ValueError(
            "Satuan '%s' tidak ada di kategori %s." % (ke, kategori)
        )
    if nilai < 0:
        raise ValueError("Nilai negatif tidak masuk akal untuk %s." % kategori)
    return nilai * satuan[dari] / satuan[ke]


def format_angka(nilai):
    """Tampilkan angka serapi mungkin: tanpa nol di belakang koma."""
    if nilai == int(nilai) and abs(nilai) < 10 ** 15:
        return str(int(nilai))
    teks = "%.6f" % nilai
    return teks.rstrip("0").rstrip(".")


def daftar_kategori():
    """Tampilkan semua kategori beserta satuannya."""
    print("Kategori dan satuan yang tersedia:\n")
    for nama in sorted(KATEGORI):
        info = KATEGORI[nama]
        print("%s: %s" % (nama, info["judul"]))
        print("  " + ", ".join(info["satuan"]))
        print()
    print("suhu: Suhu (Celsius, Fahrenheit, Kelvin, Reamur)")
    print("  " + ", ".join("%s (%s)" % (s, NAMA_SUHU[s]) for s in SUHU))


def daftar_satuan_kategori(kategori):
    """Tampilkan satuan dalam satu kategori."""
    kategori = kategori.lower()
    if kategori == "suhu":
        print("suhu: " + ", ".join(
            "%s (%s)" % (s, NAMA_SUHU[s]) for s in SUHU
        ))
        return
    if kategori not in KATEGORI:
        print("Kategori tidak dikenal: %s" % kategori)
        print("Lihat daftar lengkap dengan: python3 konversi.py --daftar")
        return
    info = KATEGORI[kategori]
    print("%s: %s" % (kategori, info["judul"]))
    print(", ".join(info["satuan"]))


def tanya(teks):
    """Minta masukan pengguna; kembalikan None bila pengguna membatalkan."""
    try:
        return input(teks).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def mode_interaktif():
    """Mode interaktif: pilih kategori, lalu konversi berulang kali."""
    print("=== Konverter Satuan ===")
    print("Ketik 'daftar' untuk melihat kategori, atau 'keluar' untuk berhenti.\n")
    while True:
        kategori = tanya("Kategori (panjang/berat/volume/suhu/waktu/kecepatan/data): ")
        if kategori is None or kategori.lower() in ("keluar", "exit", "q"):
            print("Sampai jumpa!")
            return
        if kategori.lower() == "daftar":
            daftar_kategori()
            print()
            continue
        if kategori.lower() not in KATEGORI and kategori.lower() != "suhu":
            print("Kategori tidak dikenal. Ketik 'daftar' untuk melihat pilihan.\n")
            continue

        nilai_teks = tanya("Nilai: ")
        if nilai_teks is None:
            print("Sampai jumpa!")
            return
        try:
            nilai = float(nilai_teks.replace(",", "."))
        except ValueError:
            print("Nilai harus berupa angka.\n")
            continue

        dari = tanya("Dari satuan: ")
        if dari is None:
            print("Sampai jumpa!")
            return
        ke = tanya("Ke satuan: ")
        if ke is None:
            print("Sampai jumpa!")
            return
        try:
            hasil = konversi(kategori, nilai, dari, ke)
        except ValueError as salah:
            print("Tidak bisa dikonversi: %s\n" % salah)
            continue
        print("%s %s = %s %s\n" % (
            format_angka(nilai), dari, format_angka(hasil), ke,
        ))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Konverter satuan di terminal (panjang, berat, volume, "
                    "suhu, waktu, kecepatan, data)."
    )
    parser.add_argument("kategori", nargs="?",
                        help="kategori: panjang, berat, volume, suhu, "
                             "waktu, kecepatan, data")
    parser.add_argument("nilai", nargs="?", type=float,
                        help="nilai yang dikonversi, contoh: 5")
    parser.add_argument("dari", nargs="?",
                        help="satuan asal, contoh: km")
    parser.add_argument("ke", nargs="?",
                        help="satuan tujuan, contoh: m")
    parser.add_argument("--daftar", action="store_true",
                        help="tampilkan semua kategori dan satuan")
    parser.add_argument("--kategori", dest="lihat_kategori", metavar="NAMA",
                        help="tampilkan satuan dalam satu kategori")
    args = parser.parse_args(argv)

    if args.daftar:
        daftar_kategori()
        return 0
    if args.lihat_kategori:
        daftar_satuan_kategori(args.lihat_kategori)
        return 0

    if args.kategori is None:
        mode_interaktif()
        return 0
    if args.nilai is None or args.dari is None or args.ke is None:
        parser.error("mode perintah butuh: KATEGORI NILAI DARI KE")
    try:
        hasil = konversi(args.kategori, args.nilai, args.dari, args.ke)
    except ValueError as salah:
        print("Tidak bisa dikonversi: %s" % salah, file=sys.stderr)
        return 1
    print("%s %s = %s %s" % (
        format_angka(args.nilai), args.dari, format_angka(hasil), args.ke,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
