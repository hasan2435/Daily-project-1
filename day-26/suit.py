#!/usr/bin/env python3
"""Permainan Batu Gunting Kertas — Day 26 Daily Project 1.

Main batu gunting kertas melawan komputer di terminal. Pilih
batu, gunting, atau kertas; komputer memilih secara acak. Aturan
klasiknya:

    - Batu mengalahkan gunting.
    - Gunting mengalahkan kertas.
    - Kertas mengalahkan batu.
    - Pilihan sama berarti seri.

Mode permainan:
    - Pertandingan (best of): main sampai ada yang pertama mencapai
      target kemenangan, misal best of 5 berarti pertama menang 3.
      Ronde seri tidak dihitung, jadi pertandingan bisa lebih panjang.
    - Ronde cepat: satu ronde saja, cocok untuk penentuan cepat.
    - Tanpa batas: main terus sampai memilih berhenti.

Statistik permainan (menang, kalah, seri, win rate, streak, dan
pilihan yang paling sering dipakai) disimpan otomatis, begitu juga
riwayat 50 pertandingan terakhir.

Python standar saja, tanpa library tambahan.

Cara pakai:
    python3 suit.py
    python3 suit.py main --ronde 5
    python3 suit.py main --ronde 3
    python3 suit.py cepat batu
    python3 suit.py cepat gunting
    python3 suit.py statistik
    python3 suit.py riwayat
    python3 suit.py riwayat --jumlah 5
    python3 suit.py reset --ya
    python3 suit.py --daftar

Jalankan tanpa argumen untuk mode interaktif (menu angka).

Data disimpan di berkas `suit.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek.
"""

import argparse
import json
import os
import random
import sys
from collections import Counter
from datetime import datetime

BERKAS_DATA = "suit.json"

PILIHAN = ("batu", "gunting", "kertas")
ALIAS = {
    "b": "batu",
    "g": "gunting",
    "k": "kertas",
    "batu": "batu",
    "gunting": "gunting",
    "kertas": "kertas",
}
# Pilihan apa yang dikalahkan oleh kunci: batu mengalahkan gunting, dst.
MENANG_ATAS = {
    "batu": "gunting",
    "gunting": "kertas",
    "kertas": "batu",
}
EMOJI = {
    "batu": "✊",
    "gunting": "✌️",
    "kertas": "✋",
}
MAKS_RIWAYAT = 50

# Komentar ringan sesuai hasil ronde, dipilih acak.
KOMENTAR_MENANG = [
    "Bagus! Komputer tidak menyangka.",
    "Kena! Pilihanmu tepat.",
    "Mantap, satu poin untukmu.",
    "Komputer sampai bingung memilih.",
]
KOMENTAR_KALAH = [
    "Komputer menang ronde ini.",
    "Wah, komputer membaca pikiranmu.",
    "Ronde ini milik komputer.",
    "Coba lagi, belum rezekimu.",
]
KOMENTAR_SERI = [
    "Seri! Kalian kompak sekali.",
    "Pikiran yang sama, ronde diulang.",
    "Seri, tidak ada yang dapat poin.",
]


def data_kosong():
    """Kembalikan struktur data statistik yang masih kosong."""
    return {
        "total_ronde": 0,
        "menang": 0,
        "kalah": 0,
        "seri": 0,
        "streak": 0,
        "streak_terbaik": 0,
        "pilihan": {nama: 0 for nama in PILIHAN},
        "riwayat": [],
    }


def muat_data():
    """Muat statistik dari berkas JSON, atau data kosong bila belum ada."""
    if not os.path.exists(BERKAS_DATA):
        return data_kosong()
    try:
        with open(BERKAS_DATA, "r", encoding="utf-8") as berkas:
            data = json.load(berkas)
    except (json.JSONDecodeError, OSError):
        return data_kosong()
    # Lengkapi kunci yang mungkin belum ada di berkas lama.
    dasar = data_kosong()
    for kunci in dasar:
        data.setdefault(kunci, dasar[kunci])
    return data


def simpan_data(data):
    """Simpan statistik ke berkas JSON."""
    try:
        with open(BERKAS_DATA, "w", encoding="utf-8") as berkas:
            json.dump(data, berkas, indent=2, ensure_ascii=False)
    except OSError as galat:
        print(f"Gagal menyimpan data: {galat}")


def normalkan_pilihan(teks):
    """Ubah input pengguna menjadi nama pilihan, atau None bila tidak dikenal."""
    if teks is None:
        return None
    return ALIAS.get(teks.strip().lower())


def hasil_ronde(pemain, komputer):
    """Tentukan hasil ronde: 'menang', 'kalah', atau 'seri' dari sisi pemain."""
    if pemain == komputer:
        return "seri"
    if MENANG_ATAS[pemain] == komputer:
        return "menang"
    return "kalah"


def alasan_menang(pemenang, pecundang):
    """Jelaskan kenapa satu pilihan mengalahkan yang lain."""
    pasangan = {
        ("batu", "gunting"): "Batu menghancurkan gunting.",
        ("gunting", "kertas"): "Gunting memotong kertas.",
        ("kertas", "batu"): "Kertas membungkus batu.",
    }
    return pasangan.get((pemenang, pecundang), "")


def catat_ronde(data, pemain, komputer, hasil):
    """Catat satu ronde ke statistik dan riwayat."""
    data["total_ronde"] += 1
    data["pilihan"][pemain] += 1
    if hasil == "menang":
        data["menang"] += 1
        data["streak"] += 1
        data["streak_terbaik"] = max(data["streak_terbaik"], data["streak"])
    elif hasil == "kalah":
        data["kalah"] += 1
        data["streak"] = 0
    else:
        data["seri"] += 1
    data["riwayat"].append({
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pemain": pemain,
        "komputer": komputer,
        "hasil": hasil,
    })
    data["riwayat"] = data["riwayat"][-MAKS_RIWAYAT:]
    simpan_data(data)


def mainkan_ronde(data, pemain, tampilkan=True):
    """Mainkan satu ronde dengan pilihan pemain, kembalikan hasilnya."""
    komputer = random.choice(PILIHAN)
    hasil = hasil_ronde(pemain, komputer)
    catat_ronde(data, pemain, komputer, hasil)
    if tampilkan:
        print(f"\nKamu     : {EMOJI[pemain]} {pemain}")
        print(f"Komputer : {EMOJI[komputer]} {komputer}")
        if hasil == "seri":
            print("Hasil    : Seri!")
            print(random.choice(KOMENTAR_SERI))
        else:
            pemenang = pemain if hasil == "menang" else komputer
            pecundang = komputer if hasil == "menang" else pemain
            print(f"Hasil    : {'Kamu menang!' if hasil == 'menang' else 'Komputer menang!'}")
            print(alasan_menang(pemenang, pecundang))
            komentar = KOMENTAR_MENANG if hasil == "menang" else KOMENTAR_KALAH
            print(random.choice(komentar))
    return hasil


def tanya_pilihan():
    """Minta pilihan ke pengguna sampai valid, atau None bila berhenti."""
    while True:
        teks = input("Pilihanmu (batu/gunting/kertas, atau 'keluar'): ").strip()
        if teks.lower() in ("keluar", "q", "exit"):
            return None
        pilihan = normalkan_pilihan(teks)
        if pilihan:
            return pilihan
        print("Pilihan tidak dikenal. Coba: batu, gunting, atau kertas.")


def perintah_main(data, ronde):
    """Mainkan satu pertandingan best of N ronde."""
    if ronde < 1 or ronde % 2 == 0:
        print("Jumlah ronde harus bilangan ganjil, misal 3, 5, atau 7.")
        return 1
    target = ronde // 2 + 1
    skor_kamu = 0
    skor_komputer = 0
    nomor = 0
    print(f"\n=== Pertandingan Best of {ronde} ===")
    print(f"Yang pertama menang {target} ronde menjadi juara.")
    print("Ketik 'keluar' untuk berhenti di tengah pertandingan.\n")
    while skor_kamu < target and skor_komputer < target:
        nomor += 1
        print(f"--- Ronde {nomor} ---")
        print(f"Skor: Kamu {skor_kamu} - {skor_komputer} Komputer")
        pilihan = tanya_pilihan()
        if pilihan is None:
            print("\nPertandingan dihentikan.")
            print(f"Skor akhir: Kamu {skor_kamu} - {skor_komputer} Komputer")
            return 0
        hasil = mainkan_ronde(data, pilihan)
        if hasil == "menang":
            skor_kamu += 1
        elif hasil == "kalah":
            skor_komputer += 1
        print(f"Skor: Kamu {skor_kamu} - {skor_komputer} Komputer")
    print("\n=== Hasil Pertandingan ===")
    if skor_kamu > skor_komputer:
        print(f"🎉 Kamu juara! Skor akhir {skor_kamu} - {skor_komputer}.")
    else:
        print(f"Komputer juara. Skor akhir {skor_kamu} - {skor_komputer}.")
        print("Ayo balas di pertandingan berikutnya!")
    return 0


def perintah_cepat(data, pilihan_teks):
    """Mainkan satu ronde cepat dari baris perintah."""
    pilihan = normalkan_pilihan(pilihan_teks)
    if not pilihan:
        print("Pilihan tidak dikenal. Coba: batu, gunting, atau kertas.")
        return 1
    mainkan_ronde(data, pilihan)
    return 0


def perintah_statistik(data):
    """Tampilkan statistik permainan yang tersimpan."""
    total = data["total_ronde"]
    print("\n=== Statistik Batu Gunting Kertas ===")
    if total == 0:
        print("Belum ada ronde yang dimainkan.")
        print("Jalankan `python3 suit.py main --ronde 5` untuk mulai bermain.")
        return 0
    diputuskan = data["menang"] + data["kalah"]
    win_rate = (data["menang"] / diputuskan * 100) if diputuskan else 0
    print(f"Total ronde : {total}")
    print(f"Menang      : {data['menang']}")
    print(f"Kalah       : {data['kalah']}")
    print(f"Seri        : {data['seri']}")
    print(f"Win rate    : {win_rate:.1f}% (dari {diputuskan} ronde yang diputuskan)")
    print(f"Streak menang saat ini : {data['streak']}")
    print(f"Streak menang terbaik  : {data['streak_terbaik']}")
    print("\nPilihan yang kamu pakai:")
    for nama in PILIHAN:
        jumlah = data["pilihan"].get(nama, 0)
        persen = (jumlah / total * 100) if total else 0
        bar = "█" * round(persen / 5)
        print(f"  {EMOJI[nama]} {nama:<8} {jumlah:>3}x ({persen:4.1f}%) {bar}")
    hitung = Counter(data["pilihan"])
    favorit = hitung.most_common(1)[0][0] if total else None
    if favorit:
        print(f"\nPilihan favoritmu: {favorit}.")
    return 0


def perintah_riwayat(data, jumlah):
    """Tampilkan riwayat pertandingan terakhir."""
    riwayat = data["riwayat"]
    print("\n=== Riwayat Pertandingan ===")
    if not riwayat:
        print("Belum ada riwayat. Main dulu yuk!")
        return 0
    for entri in riwayat[-jumlah:]:
        simbol = {"menang": "✅", "kalah": "❌", "seri": "🤝"}[entri["hasil"]]
        print(f"{entri['waktu']}  {simbol} Kamu {entri['pemain']} vs "
              f"Komputer {entri['komputer']} ({entri['hasil']})")
    return 0


def perintah_reset(data, ya):
    """Hapus semua statistik dan riwayat yang tersimpan."""
    if not ya:
        jawab = input("Hapus semua statistik dan riwayat? (y/n): ").strip().lower()
        if jawab not in ("y", "ya"):
            print("Dibatalkan.")
            return 0
    data_baru = data_kosong()
    data.clear()
    data.update(data_baru)
    simpan_data(data)
    print("Statistik dan riwayat sudah dihapus.")
    return 0


def tampilkan_daftar():
    """Tampilkan aturan dan pilihan permainan."""
    print("\n=== Batu Gunting Kertas ===")
    print("Aturan:")
    print("  ✊ Batu mengalahkan ✌️ Gunting.")
    print("  ✌️ Gunting mengalahkan ✋ Kertas.")
    print("  ✋ Kertas mengalahkan ✊ Batu.")
    print("  Pilihan sama berarti seri, ronde diulang di pertandingan.")
    print("\nPilihan: batu (b), gunting (g), kertas (k).")
    print("\nContoh:")
    print("  python3 suit.py main --ronde 5")
    print("  python3 suit.py cepat batu")
    print("  python3 suit.py statistik")


def mode_interaktif(data):
    """Menu angka untuk bermain tanpa argumen baris perintah."""
    print("=== Batu Gunting Kertas ===")
    print("Main melawan komputer. Siapa yang pertama menang 3 ronde?")
    while True:
        print("\nMenu:")
        print("  1. Pertandingan (best of 5)")
        print("  2. Pertandingan (best of 3)")
        print("  3. Ronde cepat (1 ronde)")
        print("  4. Main tanpa batas (berhenti kapan saja)")
        print("  5. Statistik")
        print("  6. Riwayat")
        print("  0. Keluar")
        pilihan_menu = input("Pilih menu (0-6): ").strip()
        if pilihan_menu == "0":
            print("Terima kasih sudah bermain!")
            return 0
        if pilihan_menu == "1":
            perintah_main(data, 5)
        elif pilihan_menu == "2":
            perintah_main(data, 3)
        elif pilihan_menu == "3":
            pilihan = tanya_pilihan()
            if pilihan:
                mainkan_ronde(data, pilihan)
        elif pilihan_menu == "4":
            print("\n=== Mode Tanpa Batas ===")
            print("Main terus sampai kamu ketik 'keluar'.\n")
            while True:
                pilihan = tanya_pilihan()
                if pilihan is None:
                    break
                mainkan_ronde(data, pilihan)
            print(f"\nSkor sesi ini tersimpan. Total ronde: {data['total_ronde']}.")
        elif pilihan_menu == "5":
            perintah_statistik(data)
        elif pilihan_menu == "6":
            perintah_riwayat(data, 10)
        else:
            print("Menu tidak dikenal, coba lagi.")
    return 0


def main(argv=None):
    """Titik masuk program."""
    parser = argparse.ArgumentParser(
        description="Permainan Batu Gunting Kertas melawan komputer."
    )
    parser.add_argument("--daftar", action="store_true",
                        help="tampilkan aturan dan pilihan permainan")
    sub = parser.add_subparsers(dest="perintah")

    p_main = sub.add_parser("main", help="mainkan pertandingan best of N ronde")
    p_main.add_argument("--ronde", type=int, default=5,
                        help="jumlah ronde, bilangan ganjil (default: 5)")

    p_cepat = sub.add_parser("cepat", help="mainkan satu ronde cepat")
    p_cepat.add_argument("pilihan", help="batu, gunting, atau kertas")

    sub.add_parser("statistik", help="tampilkan statistik permainan")

    p_riwayat = sub.add_parser("riwayat", help="tampilkan riwayat pertandingan")
    p_riwayat.add_argument("--jumlah", type=int, default=10,
                           help="jumlah entri terakhir (default: 10)")

    p_reset = sub.add_parser("reset", help="hapus statistik dan riwayat")
    p_reset.add_argument("--ya", action="store_true",
                         help="hapus tanpa konfirmasi")

    args = parser.parse_args(argv)

    if args.daftar:
        tampilkan_daftar()
        return 0

    data = muat_data()

    if args.perintah is None:
        return mode_interaktif(data)
    if args.perintah == "main":
        return perintah_main(data, args.ronde)
    if args.perintah == "cepat":
        return perintah_cepat(data, args.pilihan)
    if args.perintah == "statistik":
        return perintah_statistik(data)
    if args.perintah == "riwayat":
        return perintah_riwayat(data, args.jumlah)
    if args.perintah == "reset":
        return perintah_reset(data, args.ya)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
