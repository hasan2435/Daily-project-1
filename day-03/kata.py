#!/usr/bin/env python3
"""Penghitung Kata dan Waktu Baca.

Program terminal untuk menganalisis sebuah teks: jumlah karakter, kata,
kalimat, dan paragraf, rata-rata panjang kata, perkiraan waktu baca,
serta 10 kata yang paling sering muncul.

Sumber teks bisa berasal dari:
  1. Berkas teks yang disebut sebagai argumen, contoh: python3 kata.py artikel.txt
  2. Argumen --teks "..." untuk teks langsung.
  3. Mode interaktif: jalankan tanpa argumen, lalu tempel teks dan akhiri
     dengan baris kosong, atau tekan Ctrl+D (Linux/Mac) / Ctrl+Z lalu Enter
     (Windows) bila menempel banyak baris.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

# Kata umum bahasa Indonesia yang dikecualikan dari daftar kata teratas,
# supaya daftar itu menampilkan kata yang lebih bermakna.
KATA_UMUM = {
    "yang", "dan", "di", "ke", "dari", "untuk", "dengan", "pada", "adalah",
    "ini", "itu", "dalam", "sebagai", "oleh", "atau", "juga", "akan",
    "sudah", "telah", "saat", "ketika", "agar", "supaya", "karena",
    "sehingga", "namun", "tetapi", "jika", "kalau", "bisa", "dapat",
    "tidak", "bukan", "saya", "kami", "kita", "dia", "mereka", "nya",
    "lah", "pun", "saja", "sangat", "lebih", "paling", "serta",
}

KECEPATAN_BACA_PER_MENIT = 200


def ambil_kata(teks):
    """Kembalikan daftar kata (huruf kecil) dari teks."""
    return re.findall(r"[\w'-]+", teks.lower(), flags=re.UNICODE)


def analisis(teks):
    """Hitung statistik dasar dari teks dan kembalikan sebagai dict."""
    kata = ambil_kata(teks)
    kalimat = [s for s in re.split(r"[.!?]+", teks) if s.strip()]
    paragraf = [p for p in re.split(r"\n\s*\n", teks.strip()) if p.strip()]

    jumlah_kata = len(kata)
    rata_rata = sum(len(w) for w in kata) / jumlah_kata if jumlah_kata else 0
    total_detik = round(jumlah_kata / KECEPATAN_BACA_PER_MENIT * 60)
    menit, detik = divmod(total_detik, 60)

    bermakna = [w for w in kata if w not in KATA_UMUM]
    teratas = Counter(bermakna).most_common(10)

    return {
        "karakter": len(teks),
        "karakter_tanpa_spasi": len(re.sub(r"\s", "", teks)),
        "kata": jumlah_kata,
        "kalimat": len(kalimat),
        "paragraf": len(paragraf) if teks.strip() else 0,
        "rata_rata_panjang_kata": round(rata_rata, 2),
        "waktu_baca_menit": menit,
        "waktu_baca_detik": detik,
        "kata_teratas": teratas,
    }


def tampilkan(hasil):
    """Cetak hasil analisis dalam format yang mudah dibaca."""
    print("=== Hasil Analisis Teks ===")
    print(f"Karakter            : {hasil['karakter']}")
    print(f"Karakter (tanpa spasi): {hasil['karakter_tanpa_spasi']}")
    print(f"Kata                : {hasil['kata']}")
    print(f"Kalimat             : {hasil['kalimat']}")
    print(f"Paragraf            : {hasil['paragraf']}")
    print(f"Rata-rata panjang kata: {hasil['rata_rata_panjang_kata']} huruf")
    print(
        "Perkiraan waktu baca: "
        f"{hasil['waktu_baca_menit']} menit {hasil['waktu_baca_detik']} detik"
        f" (kecepatan {KECEPATAN_BACA_PER_MENIT} kata/menit)"
    )
    print()
    if hasil["kata_teratas"]:
        print("10 kata paling sering muncul (kata umum dikecualikan):")
        for kata, jumlah in hasil["kata_teratas"]:
            print(f"  - {kata}: {jumlah}x")
    else:
        print("Tidak ada kata bermakna yang bisa ditampilkan.")


def baca_interaktif():
    """Baca teks dari keyboard sampai baris kosong pertama atau EOF."""
    print("Tempel atau ketik teks, lalu tekan Enter pada baris kosong")
    print("untuk selesai (atau Ctrl+D / Ctrl+Z lalu Enter).")
    baris = []
    try:
        while True:
            satu_baris = input()
            if satu_baris == "":
                break
            baris.append(satu_baris)
    except EOFError:
        pass
    return "\n".join(baris)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Hitung kata, kalimat, dan perkiraan waktu baca sebuah teks."
    )
    parser.add_argument(
        "berkas",
        nargs="?",
        help="Berkas teks yang dianalisis (opsional).",
    )
    parser.add_argument(
        "--teks",
        help="Teks yang dianalisis langsung dari baris perintah.",
    )
    args = parser.parse_args(argv)

    if args.teks is not None:
        teks = args.teks
    elif args.berkas is not None:
        jalur = Path(args.berkas)
        if not jalur.is_file():
            print(f"Berkas tidak ditemukan: {args.berkas}", file=sys.stderr)
            return 1
        try:
            teks = jalur.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(
                "Berkas bukan teks UTF-8. Simpan sebagai teks biasa (.txt).",
                file=sys.stderr,
            )
            return 1
    else:
        teks = baca_interaktif()

    if not teks.strip():
        print("Teks kosong, tidak ada yang dianalisis.", file=sys.stderr)
        return 1

    tampilkan(analisis(teks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
