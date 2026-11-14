#!/usr/bin/env python3
"""Kuis Pengetahuan Umum di terminal.

Lima kategori soal pilihan ganda Bahasa Indonesia: umum, sains,
sejarah, geografi, dan olahraga. Soal dan pilihan jawaban diacak
setiap permainan, dan skor terbaik per kategori disimpan di berkas
``kuis.json`` pada folder tempat program dijalankan.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

Cara memakai:
    python3 kuis.py
    python3 kuis.py --kategori sains --jumlah 5
    python3 kuis.py --kategori campuran --jumlah 10
    python3 kuis.py --daftar
    python3 kuis.py skor
"""

import argparse
import json
import os
import random
import sys

BERKAS_SKOR = "kuis.json"
POIN_PER_SOAL = 10

# Tiap soal: (pertanyaan, [pilihan A, B, C, D], indeks jawaban benar,
#             penjelasan singkat).
# Jawaban benar selalu ditulis pertama di sini; urutan pilihan diacak
# saat soal ditampilkan.
SOAL = {
    "umum": [
        (
            "Apa bahasa resmi negara Indonesia?",
            ["Bahasa Indonesia", "Bahasa Jawa", "Bahasa Melayu",
             "Bahasa Inggris"],
            0,
            "Bahasa Indonesia ditetapkan sebagai bahasa resmi dalam "
            "UUD 1945 pasal 36.",
        ),
        (
            "Apa mata uang resmi Indonesia?",
            ["Rupiah", "Ringgit", "Baht", "Dolar"],
            0,
            "Rupiah adalah mata uang resmi Indonesia sejak 1946.",
        ),
        (
            "Berapa jumlah sila dalam Pancasila?",
            ["Lima", "Tiga", "Empat", "Enam"],
            0,
            "Pancasila terdiri dari lima sila.",
        ),
        (
            "Apa lagu kebangsaan Indonesia?",
            ["Indonesia Raya", "Garuda Pancasila", "Maju Tak Gentar",
             "Halo-Halo Bandung"],
            0,
            "Indonesia Raya diciptakan oleh Wage Rudolf Supratman dan "
            "dinyanyikan pertama kali pada 1928.",
        ),
        (
            "Kapan Indonesia memproklamasikan kemerdekaannya?",
            ["17 Agustus 1945", "20 Mei 1908", "28 Oktober 1928",
             "1 Juni 1945"],
            0,
            "Proklamasi dibacakan Soekarno pada 17 Agustus 1945.",
        ),
        (
            "Siapa presiden pertama Republik Indonesia?",
            ["Soekarno", "Soeharto", "B.J. Habibie", "Joko Widodo"],
            0,
            "Soekarno menjabat sebagai presiden pertama pada 1945-1967.",
        ),
        (
            "Apa lambang negara Indonesia?",
            ["Garuda Pancasila", "Banteng", "Komodo", "Elang Jawa"],
            0,
            "Garuda Pancasila dirancang oleh Sultan Hamid II dan "
            "diresmikan pada 1950.",
        ),
        (
            "Pulau Bali terkenal dengan julukan apa?",
            ["Pulau Dewata", "Pulau Seram", "Pulau Karang",
             "Pulau Emas"],
            0,
            "Bali dijuluki Pulau Dewata karena banyaknya pura dan "
            "kehidupan keagamaan Hindu yang kental.",
        ),
    ],
    "sains": [
        (
            "Apa rumus kimia air?",
            ["H2O", "CO2", "O2", "NaCl"],
            0,
            "Satu molekul air terdiri dari dua atom hidrogen dan satu "
            "atom oksigen.",
        ),
        (
            "Planet apa yang paling dekat dengan Matahari?",
            ["Merkurius", "Venus", "Mars", "Bumi"],
            0,
            "Merkurius adalah planet pertama dari Matahari.",
        ),
        (
            "Organ tubuh apa yang memompa darah ke seluruh tubuh?",
            ["Jantung", "Hati", "Paru-paru", "Ginjal"],
            0,
            "Jantung memompa darah melalui pembuluh darah ke seluruh "
            "tubuh.",
        ),
        (
            "Proses tumbuhan membuat makanan dengan bantuan cahaya "
            "matahari disebut?",
            ["Fotosintesis", "Respirasi", "Fermentasi", "Evaporasi"],
            0,
            "Fotosintesis mengubah air dan karbon dioksida menjadi "
            "glukosa dan oksigen.",
        ),
        (
            "Gaya yang menarik benda jatuh ke bumi disebut gaya?",
            ["Gravitasi", "Gesek", "Magnet", "Otot"],
            0,
            "Gravitasi bumi menarik semua benda bermassa ke arah "
            "pusat bumi.",
        ),
        (
            "Pada suhu berapa air mendidih di permukaan laut?",
            ["100 derajat Celsius", "90 derajat Celsius",
             "80 derajat Celsius", "120 derajat Celsius"],
            0,
            "Pada tekanan 1 atmosfer, air mendidih pada 100 derajat "
            "Celsius.",
        ),
        (
            "Hewan darat tercepat di dunia adalah?",
            ["Cheetah", "Kuda", "Rusa", "Singa"],
            0,
            "Cheetah bisa berlari hingga sekitar 100 km/jam dalam "
            "jarak pendek.",
        ),
        (
            "Unsur kimia dengan simbol O adalah?",
            ["Oksigen", "Emas", "Besi", "Hidrogen"],
            0,
            "O adalah simbol oksigen; emas bersimbol Au dan besi "
            "bersimbol Fe.",
        ),
    ],
    "sejarah": [
        (
            "Siapa saja proklamator kemerdekaan Indonesia?",
            ["Soekarno dan Mohammad Hatta", "Soekarno dan Soeharto",
             "Hatta dan Sjahrir", "Soekarno dan Tan Malaka"],
            0,
            "Soekarno membacakan naskah proklamasi didampingi "
            "Mohammad Hatta.",
        ),
        (
            "Candi Buddha terbesar di Indonesia adalah?",
            ["Borobudur", "Prambanan", "Penataran", "Mendut"],
            0,
            "Borobudur di Magelang dibangun sekitar abad ke-9 dan "
            "menjadi candi Buddha terbesar di dunia.",
        ),
        (
            "Kerajaan Hindu tertua di Indonesia adalah?",
            ["Kutai", "Majapahit", "Sriwijaya", "Tarumanagara"],
            0,
            "Kerajaan Kutai di Kalimantan Timur berdiri sekitar abad "
            "ke-4 Masehi.",
        ),
        (
            "Sumpah Pemuda diikrarkan pada tahun?",
            ["1928", "1908", "1945", "1918"],
            0,
            "Sumpah Pemuda diikrarkan pada 28 Oktober 1928.",
        ),
        (
            "Siapa penemu lampu pijar?",
            ["Thomas Alva Edison", "Albert Einstein", "Isaac Newton",
             "Alexander Graham Bell"],
            0,
            "Edison mematenkan lampu pijar yang praktis pada 1879.",
        ),
        (
            "Perang Diponegoro berlangsung pada tahun?",
            ["1825-1830", "1800-1805", "1873-1904", "1945-1949"],
            0,
            "Perang Diponegoro, dipimpin Pangeran Diponegoro, "
            "berlangsung 1825-1830.",
        ),
        (
            "Konferensi Asia Afrika pertama diadakan di kota?",
            ["Bandung", "Jakarta", "Yogyakarta", "Surabaya"],
            0,
            "Konferensi Asia Afrika 1955 diadakan di Bandung dan "
            "dihadiri 29 negara.",
        ),
        (
            "Siapa penulis buku 'Indonesia Menggugat'?",
            ["Soekarno", "Mohammad Hatta", "Sutan Sjahrir",
             "Tan Malaka"],
            0,
            "Soekarno menulis 'Indonesia Menggugat' sebagai pledoi "
            "dalam persidangan 1930.",
        ),
    ],
    "geografi": [
        (
            "Sungai terpanjang di dunia adalah?",
            ["Nil", "Amazon", "Yangtze", "Mississippi"],
            0,
            "Sungai Nil di Afrika panjangnya sekitar 6.650 km.",
        ),
        (
            "Gurun pasir terbesar di dunia adalah?",
            ["Sahara", "Gobi", "Kalahari", "Atacama"],
            0,
            "Gurun Sahara di Afrika Utara luasnya sekitar 9 juta "
            "km persegi.",
        ),
        (
            "Gunung tertinggi di dunia adalah?",
            ["Everest", "Kilimanjaro", "Elbrus", "Aconcagua"],
            0,
            "Everest di pegunungan Himalaya tingginya 8.849 meter.",
        ),
        (
            "Apa ibu kota Jepang?",
            ["Tokyo", "Osaka", "Kyoto", "Nagoya"],
            0,
            "Tokyo menjadi ibu kota Jepang sejak 1868.",
        ),
        (
            "Benua terbesar di dunia adalah?",
            ["Asia", "Afrika", "Eropa", "Amerika"],
            0,
            "Asia luasnya sekitar 44,6 juta km persegi.",
        ),
        (
            "Danau terbesar di Indonesia adalah?",
            ["Toba", "Sentani", "Poso", "Maninjau"],
            0,
            "Danau Toba di Sumatra Utara terbentuk dari letusan "
            "gunung berapi purba.",
        ),
        (
            "Negara terluas di dunia adalah?",
            ["Rusia", "Kanada", "Tiongkok", "Amerika Serikat"],
            0,
            "Rusia luasnya sekitar 17 juta km persegi.",
        ),
        (
            "Selat yang memisahkan Pulau Jawa dan Pulau Sumatra "
            "adalah?",
            ["Selat Sunda", "Selat Malaka", "Selat Bali",
             "Selat Lombok"],
            0,
            "Selat Sunda memisahkan ujung barat Jawa dan ujung "
            "tenggara Sumatra.",
        ),
    ],
    "olahraga": [
        (
            "Berapa jumlah pemain sepak bola satu tim di lapangan?",
            ["11 orang", "9 orang", "7 orang", "5 orang"],
            0,
            "Satu tim sepak bola terdiri dari 11 pemain, termasuk "
            "kiper.",
        ),
        (
            "Seni bela diri tradisional yang berasal dari Indonesia "
            "adalah?",
            ["Pencak silat", "Karate", "Taekwondo", "Judo"],
            0,
            "Pencak silat berasal dari Nusantara dan diakui UNESCO "
            "sebagai warisan budaya takbenda.",
        ),
        (
            "Olimpiade musim panas diadakan setiap berapa tahun?",
            ["4 tahun", "2 tahun", "3 tahun", "5 tahun"],
            0,
            "Olimpiade modern diadakan setiap empat tahun sejak 1896.",
        ),
        (
            "Apa nama induk organisasi sepak bola dunia?",
            ["FIFA", "FIBA", "ITTF", "BWF"],
            0,
            "FIFA (Federation Internationale de Football "
            "Association) berdiri pada 1904.",
        ),
        (
            "Olahraga yang memakai raket dan kok disebut?",
            ["Bulu tangkis", "Tenis meja", "Squash", "Tenis lapangan"],
            0,
            "Bulu tangkis memakai raket ringan dan kok berbulu.",
        ),
        (
            "Berapa lama waktu normal satu pertandingan sepak bola?",
            ["90 menit", "60 menit", "80 menit", "120 menit"],
            0,
            "Pertandingan sepak bola normal berlangsung 2 x 45 menit.",
        ),
        (
            "Siapa pemegang rekor dunia lari 100 meter putra?",
            ["Usain Bolt", "Carl Lewis", "Tyson Gay", "Justin Gatlin"],
            0,
            "Usain Bolt mencatat 9,58 detik pada Kejuaraan Dunia 2009 "
            "di Berlin.",
        ),
        (
            "Olahraga selancar dilakukan di atas?",
            ["Ombak laut", "Salju", "Es", "Pasir"],
            0,
            "Selancar adalah olahraga menunggangi ombak dengan papan "
            "seluncur.",
        ),
    ],
}

KATEGORI_LABEL = {
    "umum": "Pengetahuan Umum",
    "sains": "Sains",
    "sejarah": "Sejarah",
    "geografi": "Geografi",
    "olahraga": "Olahraga",
    "campuran": "Campuran (semua kategori)",
}

HURUF_JAWABAN = ["A", "B", "C", "D"]


def muat_skor():
    """Muat skor terbaik per kategori dari berkas, atau dict kosong."""
    if not os.path.exists(BERKAS_SKOR):
        return {}
    try:
        with open(BERKAS_SKOR, "r", encoding="utf-8") as berkas:
            data = json.load(berkas)
        if isinstance(data, dict):
            return data
    except (OSError, ValueError):
        pass
    return {}


def simpan_skor(skor):
    """Simpan skor terbaik per kategori ke berkas."""
    try:
        with open(BERKAS_SKOR, "w", encoding="utf-8") as berkas:
            json.dump(skor, berkas, ensure_ascii=False, indent=2)
    except OSError as err:
        print("Tidak bisa menyimpan skor: {}".format(err))


def nilai_akhir(benar, total):
    """Kembalikan predikat berdasarkan persentase jawaban benar."""
    if total == 0:
        return "Belum ada soal"
    persen = benar / total * 100
    if persen == 100:
        return "Sempurna!"
    if persen >= 80:
        return "Sangat Baik"
    if persen >= 60:
        return "Baik"
    if persen >= 40:
        return "Cukup"
    return "Perlu Belajar Lagi"


def pilih_soal(kategori, jumlah):
    """Ambil soal acak sebanyak jumlah dari kategori yang diminta."""
    if kategori == "campuran":
        kumpulan = []
        for daftar in SOAL.values():
            kumpulan.extend(daftar)
    else:
        kumpulan = list(SOAL[kategori])
    random.shuffle(kumpulan)
    return kumpulan[:jumlah]


def tanya(soal, nomor, total):
    """Tampilkan satu soal, baca jawaban, kembalikan True bila benar.

    Mengembalikan None bila pemain memilih berhenti (mengetik q).
    """
    pertanyaan, pilihan, benar, penjelasan = soal
    urutan = list(range(len(pilihan)))
    random.shuffle(urutan)
    posisi_benar = urutan.index(benar)

    print("\nSoal {}/{}: {}".format(nomor, total, pertanyaan))
    for posisi, indeks_asli in enumerate(urutan):
        print("  {}. {}".format(HURUF_JAWABAN[posisi], pilihan[indeks_asli]))

    while True:
        try:
            jawaban = input("Jawabanmu (A-D, q untuk berhenti): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        jawaban = jawaban.upper()
        if jawaban in ("Q", "KELUAR"):
            return None
        if jawaban in HURUF_JAWABAN:
            dipilih = HURUF_JAWABAN.index(jawaban)
            if dipilih == posisi_benar:
                print("Benar! +{} poin".format(POIN_PER_SOAL))
                print("Penjelasan: {}".format(penjelasan))
                return True
            print("Salah. Jawaban benar: {}. {}".format(
                HURUF_JAWABAN[posisi_benar], pilihan[benar]))
            print("Penjelasan: {}".format(penjelasan))
            return False
        print("Masukkan huruf A, B, C, atau D (atau q untuk berhenti).")


def main_kuis(kategori, jumlah):
    """Jalankan satu sesi kuis, kembalikan (benar, total)."""
    if kategori not in SOAL and kategori != "campuran":
        print("Kategori tidak dikenal: {}".format(kategori))
        print("Kategori yang tersedia: {}".format(
            ", ".join(sorted(SOAL))))
        return None

    maks = sum(len(v) for v in SOAL.values()) if kategori == "campuran" \
        else len(SOAL[kategori])
    if jumlah < 1:
        print("Jumlah soal minimal 1.")
        return None
    if jumlah > maks:
        print("Kategori {} hanya punya {} soal; memakai {} soal.".format(
            KATEGORI_LABEL[kategori], maks, maks))
        jumlah = maks

    soal_terpilih = pilih_soal(kategori, jumlah)
    print("\n=== Kuis {} ===".format(KATEGORI_LABEL[kategori]))
    print("{} soal, {} poin per jawaban benar.".format(
        jumlah, POIN_PER_SOAL))

    benar = 0
    dijawab = 0
    for nomor, soal in enumerate(soal_terpilih, start=1):
        hasil = tanya(soal, nomor, jumlah)
        if hasil is None:
            print("\nKuis dihentikan.")
            break
        dijawab += 1
        if hasil:
            benar += 1

    if dijawab == 0:
        return (0, 0)

    skor = benar * POIN_PER_SOAL
    print("\n=== Hasil ===")
    print("Benar: {}/{}".format(benar, dijawab))
    print("Skor: {} poin".format(skor))
    print("Predikat: {}".format(nilai_akhir(benar, dijawab)))

    if dijawab == jumlah:
        skor_lama = muat_skor()
        terbaik = skor_lama.get(kategori, 0)
        if skor > terbaik:
            skor_lama[kategori] = skor
            simpan_skor(skor_lama)
            print("Skor terbaik baru untuk kategori {}!".format(
                KATEGORI_LABEL[kategori]))
        else:
            print("Skor terbaik kategori {}: {} poin.".format(
                KATEGORI_LABEL[kategori], terbaik))
    return (benar, dijawab)


def daftar_kategori():
    """Tampilkan daftar kategori dan jumlah soal tiap kategori."""
    print("Kategori yang tersedia:")
    for kunci in sorted(SOAL):
        print("  {:<9} {} soal — {}".format(
            kunci, len(SOAL[kunci]), KATEGORI_LABEL[kunci]))
    total = sum(len(v) for v in SOAL.values())
    print("  {:<9} {} soal — {}".format(
        "campuran", total, KATEGORI_LABEL["campuran"]))


def tampilkan_skor():
    """Tampilkan skor terbaik yang tersimpan per kategori."""
    skor = muat_skor()
    if not skor:
        print("Belum ada skor tersimpan. Main dulu yuk!")
        return
    print("Skor terbaik per kategori:")
    for kunci in sorted(skor):
        label = KATEGORI_LABEL.get(kunci, kunci)
        print("  {:<28} {} poin".format(label, skor[kunci]))


def mode_interaktif():
    """Menu interaktif: pilih kategori dan jumlah soal."""
    print("=== Kuis Pengetahuan Umum ===")
    print("Uji pengetahuanmu lewat soal pilihan ganda!")
    daftar_kategori()
    tampilkan_skor()

    while True:
        print("\nPilih kategori (atau ketik q untuk keluar):")
        print("  1. Pengetahuan Umum")
        print("  2. Sains")
        print("  3. Sejarah")
        print("  4. Geografi")
        print("  5. Olahraga")
        print("  6. Campuran")
        print("  q. Keluar")
        try:
            pilihan = input("Pilihanmu: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            return
        pemetaan = {
            "1": "umum", "2": "sains", "3": "sejarah",
            "4": "geografi", "5": "olahraga", "6": "campuran",
        }
        if pilihan in ("q", "keluar"):
            print("Sampai jumpa!")
            return
        if pilihan in pemetaan:
            kategori = pemetaan[pilihan]
        elif pilihan in SOAL or pilihan == "campuran":
            kategori = pilihan
        else:
            print("Pilihan tidak dikenal, coba lagi.")
            continue

        maks = sum(len(v) for v in SOAL.values()) \
            if kategori == "campuran" else len(SOAL[kategori])
        try:
            teks_jumlah = input(
                "Berapa soal? (1-{}, default 5): ".format(maks)).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            return
        if teks_jumlah == "":
            jumlah = 5
        else:
            try:
                jumlah = int(teks_jumlah)
            except ValueError:
                print("Jumlah harus angka; memakai 5 soal.")
                jumlah = 5
        main_kuis(kategori, jumlah)

        try:
            lagi = input("\nMain lagi? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            return
        if lagi not in ("y", "ya"):
            print("Sampai jumpa!")
            return


def main(argv=None):
    """Titik masuk program."""
    parser = argparse.ArgumentParser(
        description="Kuis Pengetahuan Umum di terminal.")
    parser.add_argument(
        "--kategori", default=None,
        choices=["umum", "sains", "sejarah", "geografi", "olahraga",
                 "campuran"],
        help="kategori soal yang dimainkan")
    parser.add_argument(
        "--jumlah", type=int, default=5,
        help="jumlah soal (default: 5)")
    parser.add_argument(
        "--daftar", action="store_true",
        help="tampilkan daftar kategori lalu keluar")
    parser.add_argument(
        "perintah", nargs="?", default=None,
        help="perintah: skor (lihat skor terbaik)")
    args = parser.parse_args(argv)

    if args.daftar:
        daftar_kategori()
        return 0
    if args.perintah == "skor":
        tampilkan_skor()
        return 0
    if args.perintah is not None:
        parser.print_usage(sys.stderr)
        print("Perintah tidak dikenal: {}".format(args.perintah),
              file=sys.stderr)
        return 2
    if args.kategori is not None:
        hasil = main_kuis(args.kategori, args.jumlah)
        return 0 if hasil is not None else 1
    mode_interaktif()
    return 0


if __name__ == "__main__":
    sys.exit(main())
