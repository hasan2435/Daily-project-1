#!/usr/bin/env python3
"""Day 7 - Permainan Tebak Kata (Hangman) di terminal.

Tebak kata Bahasa Indonesia huruf demi huruf sebelum gambar
orang-orangan selesai. Ada 6 kategori kata dan 3 tingkat kesulitan.

Cara menjalankan:
    python3 tebak.py
    python3 tebak.py --kategori hewan --kesulitan sulit
    python3 tebak.py --kata kucing
    python3 tebak.py --daftar

Mode dua pemain: beri kata rahasia lewat --kata, lalu temanmu
yang menebak. Kata hanya boleh berisi huruf a-z.
"""

import argparse
import random
import sys

KATA = {
    "hewan": [
        "kucing", "anjing", "gajah", "harimau", "jerapah", "kelinci",
        "kuda", "sapi", "kambing", "buaya", "ular", "elang", "merpati",
        "lumba", "paus", "beruang", "serigala", "rusa", "monyet",
        "tupai", "landak", "kelelawar", "kanguru", "pinguin",
    ],
    "buah": [
        "mangga", "pisang", "apel", "jeruk", "anggur", "pepaya",
        "nanas", "melon", "semangka", "durian", "rambutan", "salak",
        "alpukat", "stroberi", "belimbing", "jambu", "kelapa",
        "cempedak", "manggis", "sirsak",
    ],
    "kota": [
        "jakarta", "bandung", "surabaya", "medan", "makassar",
        "yogyakarta", "semarang", "palembang", "balikpapan",
        "denpasar", "malang", "bogor", "bekasi", "tangerang",
        "pontianak", "manado", "padang", "pekanbaru", "solo",
    ],
    "benda": [
        "meja", "kursi", "lemari", "lampu", "cermin", "bantal",
        "selimut", "payung", "sepatu", "tas", "jam", "kunci",
        "gunting", "pensil", "penghapus", "penggaris", "komputer",
        "televisi", "kulkas", "kipas",
    ],
    "makanan": [
        "nasi", "rendang", "sate", "bakso", "soto", "gado",
        "pecel", "rawon", "opor", "pempek", "rujak", "lotek",
        "ketoprak", "martabak", "lumpia", "onde", "klepon",
        "serabi", "bubur", "mie",
    ],
    "profesi": [
        "dokter", "guru", "polisi", "tentara", "pilot", "nelayan",
        "petani", "koki", "sopir", "penjahit", "tukang", "arsitek",
        "pengacara", "wartawan", "seniman", "penyanyi", "atlet",
        "perawat", "bidan", "apoteker",
    ],
}

KESULITAN = {
    "mudah": {"min": 4, "maks": 6, "nyawa": 8},
    "sedang": {"min": 7, "maks": 9, "nyawa": 6},
    "sulit": {"min": 10, "maks": 99, "nyawa": 4},
}

# Gambar orang-orangan berdasarkan jumlah kesalahan (0 sampai 6).
GAMBAR = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========""",
]


def pilih_kata(kategori, kesulitan):
    """Pilih kata acak dari kategori sesuai rentang panjang kesulitan."""
    aturan = KESULITAN[kesulitan]
    calon = [k for k in KATA[kategori]
             if aturan["min"] <= len(k) <= aturan["maks"]]
    if not calon:
        calon = KATA[kategori]
    return random.choice(calon)


def tampilkan_kata(kata, tebakan):
    """Tampilkan kata dengan huruf yang belum ditebak sebagai garis."""
    return " ".join(huruf if huruf in tebakan else "_" for huruf in kata)


def tampilkan_gambar(salah, nyawa):
    """Tampilkan gambar sesuai jumlah kesalahan, diskalakan ke 7 tahap."""
    # Skalakan jumlah kesalahan ke indeks gambar 0..6.
    maks_tahap = len(GAMBAR) - 1
    indeks = min(maks_tahap, round(salah / nyawa * maks_tahap)) if nyawa else maks_tahap
    print(GAMBAR[indeks])


def minta_tebakan(tebakan):
    """Minta satu huruf atau satu kata utuh dari pemain."""
    while True:
        jawaban = input("Tebak satu huruf (atau kata utuh): ").strip().lower()
        if not jawaban:
            print("Masukkan dulu satu huruf atau satu kata.")
            continue
        if not jawaban.isalpha():
            print("Hanya huruf a-z, tanpa angka atau simbol.")
            continue
        if len(jawaban) == 1 and jawaban in tebakan:
            print(f"Huruf '{jawaban}' sudah ditebak. Coba huruf lain.")
            continue
        return jawaban


def mainkan_satu(kata, nyawa, kategori):
    """Satu ronde permainan. Mengembalikan True bila pemain menang."""
    tebakan = set()
    salah = 0
    print(f"\nKategori: {kategori} | Panjang kata: {len(kata)} huruf | Nyawa: {nyawa}")

    while salah < nyawa:
        tampilkan_gambar(salah, nyawa)
        print(f"\nKata: {tampilkan_kata(kata, tebakan)}")
        print(f"Nyawa tersisa: {nyawa - salah}")
        print("Huruf sudah ditebak:", ", ".join(sorted(tebakan)) or "-")

        jawaban = minta_tebakan(tebakan)

        if len(jawaban) > 1:
            # Tebakan kata utuh: benar langsung menang, salah habiskan 2 nyawa.
            if jawaban == kata:
                print(f"\nTepat! Katanya memang '{kata}'.")
                return True
            salah += 2
            print(f"\nBukan '{jawaban}'. Nyawa berkurang 2.")
        else:
            tebakan.add(jawaban)
            if jawaban in kata:
                print(f"\nAda huruf '{jawaban}'!")
            else:
                salah += 1
                print(f"\nTidak ada huruf '{jawaban}'.")

        if all(huruf in tebakan for huruf in kata):
            tampilkan_gambar(salah, nyawa)
            print(f"\nKata: {tampilkan_kata(kata, tebakan)}")
            print(f"\nMenang! Katanya adalah '{kata}'.")
            return True

    tampilkan_gambar(salah, nyawa)
    print(f"\nKalah. Katanya adalah '{kata}'.")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Permainan Tebak Kata (Hangman) di terminal.")
    parser.add_argument("--kategori", choices=sorted(KATA),
                        help="kategori kata (acak bila tidak diisi)")
    parser.add_argument("--kesulitan", choices=sorted(KESULITAN),
                        default="sedang",
                        help="mudah, sedang, atau sulit (default: sedang)")
    parser.add_argument("--kata",
                        help="kata rahasia untuk mode dua pemain (a-z saja)")
    parser.add_argument("--daftar", action="store_true",
                        help="tampilkan daftar kategori dan keluar")
    args = parser.parse_args()

    if args.daftar:
        print("Kategori yang tersedia:")
        for nama in sorted(KATA):
            print(f"  - {nama} ({len(KATA[nama])} kata)")
        print("\nTingkat kesulitan: mudah, sedang, sulit.")
        return 0

    if args.kata:
        kata_rahasia = args.kata.strip().lower()
        if not kata_rahasia.isalpha():
            print("Kata rahasia hanya boleh berisi huruf a-z.")
            return 1
        kategori = args.kategori or "kata sendiri"
    else:
        kategori = args.kategori or random.choice(list(KATA))
        kata_rahasia = pilih_kata(kategori, args.kesulitan)

    nyawa = KESULITAN[args.kesulitan]["nyawa"]

    print("=" * 40)
    print("  PERMAINAN TEBAK KATA")
    print("=" * 40)
    print("Tebak huruf demi huruf. Menebak kata utuh yang")
    print("salah mengurangi 2 nyawa. Ketik Ctrl+C untuk keluar.")

    menang_total = 0
    kalah_total = 0
    beruntun = 0

    while True:
        menang = mainkan_satu(kata_rahasia, nyawa, kategori)
        if menang:
            menang_total += 1
            beruntun += 1
        else:
            kalah_total += 1
            beruntun = 0

        poin = (nyawa * 10 + len(kata_rahasia) * 5) if menang else 0
        print(f"\nSkor ronde ini: {poin} poin")
        print(f"Menang: {menang_total} | Kalah: {kalah_total} | "
              f"Menang beruntun: {beruntun}")

        lagi = input("\nMain lagi? (y/n): ").strip().lower()
        if lagi not in ("y", "ya"):
            print("\nTerima kasih sudah bermain!")
            return 0

        if not args.kata:
            kategori = args.kategori or random.choice(list(KATA))
            kata_rahasia = pilih_kata(kategori, args.kesulitan)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nPermainan dihentikan. Sampai jumpa!")
        sys.exit(0)
