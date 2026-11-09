#!/usr/bin/env python3
"""Kalkulator BMI & Kalori Harian — proyek harian ke-9.

Program terminal untuk menghitung Indeks Massa Tubuh (BMI) beserta
kategorinya, rentang berat badan ideal, kebutuhan kalori basal (BMR)
dengan rumus Mifflin-St Jeor, total kebutuhan kalori harian (TDEE)
berdasarkan tingkat aktivitas, dan target kalori untuk menurunkan,
mempertahankan, atau menaikkan berat badan.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

Cara memakai (mode perintah):

    python3 bmi.py bmi 70 170
    python3 bmi.py kalori 70 170 30 pria sedang
    python3 bmi.py kalori 55 160 25 wanita ringan --tujuan turun
    python3 bmi.py --daftar

Jalankan tanpa argumen untuk mode interaktif.

Catatan: hasil program ini adalah perkiraan untuk orang dewasa sehat,
bukan diagnosis medis. Konsultasikan ke dokter atau ahli gizi untuk
rencana yang personal, terutama bila ada kondisi kesehatan tertentu.
"""

import argparse
import sys

# Batas berat, tinggi, dan umur yang masih masuk akal untuk perhitungan.
BATAS = {
    "berat": (10.0, 500.0, "kg"),
    "tinggi": (50.0, 250.0, "cm"),
    "umur": (1, 120, "tahun"),
}

# Kategori BMI menurut WHO (batas atas eksklusif, kecuali yang terakhir).
# Untuk populasi Asia, risiko kesehatan sudah mulai naik sejak BMI 23.
KATEGORI_BMI = [
    (18.5, "Kurus", "Berat badan di bawah normal. Perhatikan asupan gizi."),
    (25.0, "Normal", "Berat badan sehat. Pertahankan pola makan dan gerak."),
    (30.0, "Berlebih", "Berat badan di atas normal. Waspada risiko kesehatan."),
    (float("inf"), "Obesitas", "Berat badan jauh di atas normal. Sebaiknya konsultasi dokter."),
]

# Tingkat aktivitas: kunci -> (label, pengali TDEE, penjelasan).
AKTIVITAS = {
    "sangat-ringan": (
        "Sangat ringan",
        1.2,
        "Hampir tidak bergerak; kerja duduk seharian, tanpa olahraga.",
    ),
    "ringan": (
        "Ringan",
        1.375,
        "Olahraga ringan 1-3 hari seminggu, atau banyak jalan kaki.",
    ),
    "sedang": (
        "Sedang",
        1.55,
        "Olahraga sedang 3-5 hari seminggu.",
    ),
    "aktif": (
        "Aktif",
        1.725,
        "Olahraga berat 6-7 hari seminggu, atau pekerjaan fisik.",
    ),
    "sangat-aktif": (
        "Sangat aktif",
        1.9,
        "Latihan sangat berat dua kali sehari, atau pekerjaan sangat fisik.",
    ),
}

# Asupan minimum yang masih aman sebagai patokan umum (kkal/hari).
KALORI_MINIMUM = {"pria": 1500, "wanita": 1200}

# Perubahan berat 0,5 kg per minggu setara kurang-lebih 500 kkal per hari.
LANGKAH_KALORI = 500


def galat(pesan):
    """Cetak pesan galat ke stderr dan keluar dengan kode 2."""
    print(f"Galat: {pesan}", file=sys.stderr)
    raise SystemExit(2)


def periksa_rentang(nama, nilai, batas):
    """Pastikan nilai berada dalam rentang wajar; bila tidak, berhenti."""
    rendah, tinggi, satuan = batas
    if not rendah <= nilai <= tinggi:
        galat(
            f"{nama} harus antara {rendah:g} dan {tinggi:g} {satuan} "
            f"(diberi {nilai:g} {satuan})."
        )


def normalisasi_jenis_kelamin(teks):
    """Terima berbagai ejaan jenis kelamin, kembalikan 'pria'/'wanita'."""
    kunci = teks.strip().lower()
    if kunci in ("pria", "laki-laki", "laki", "l"):
        return "pria"
    if kunci in ("wanita", "perempuan", "p", "w"):
        return "wanita"
    galat("jenis kelamin harus 'pria' atau 'wanita'.")


def normalisasi_aktivitas(teks):
    """Terima nama atau nomor tingkat aktivitas, kembalikan kuncinya."""
    kunci = teks.strip().lower().replace("_", "-").replace(" ", "-")
    if kunci in AKTIVITAS:
        return kunci
    urutan = list(AKTIVITAS)
    if kunci in ("1", "2", "3", "4", "5"):
        return urutan[int(kunci) - 1]
    galat(
        "aktivitas tidak dikenal. Pilih salah satu: "
        + ", ".join(urutan)
        + " (atau nomor 1-5)."
    )


def hitung_bmi(berat, tinggi_cm):
    """Kembalikan (BMI, label kategori, saran, berat ideal min, maks)."""
    tinggi_m = tinggi_cm / 100.0
    bmi = berat / (tinggi_m * tinggi_m)
    for batas, label, saran in KATEGORI_BMI:
        if bmi < batas:
            break
    ideal_min = 18.5 * tinggi_m * tinggi_m
    ideal_maks = 24.9 * tinggi_m * tinggi_m
    return bmi, label, saran, ideal_min, ideal_maks


def hitung_bmr(berat, tinggi_cm, umur, jenis_kelamin):
    """BMR dengan rumus Mifflin-St Jeor (kkal/hari)."""
    dasar = 10 * berat + 6.25 * tinggi_cm - 5 * umur
    return dasar + 5 if jenis_kelamin == "pria" else dasar - 161


def hitung_target(tdee, jenis_kelamin):
    """Kembalikan target kalori (turun, tahan, naik) dengan batas aman."""
    minimum = KALORI_MINIMUM[jenis_kelamin]
    turun = tdee - LANGKAH_KALORI
    peringatan = None
    if turun < minimum:
        turun = minimum
        peringatan = (
            f"Target turun berat badan dibatasi ke {minimum} kkal/hari "
            f"(batas aman umum untuk {jenis_kelamin}). Penurunan lebih "
            "cepat sebaiknya di bawah pengawasan ahli gizi."
        )
    return {"turun": turun, "tahan": tdee, "naik": tdee + LANGKAH_KALORI}, peringatan


def tampilkan_bmi(berat, tinggi_cm):
    """Tampilkan hasil perhitungan BMI dan berat ideal."""
    bmi, label, saran, ideal_min, ideal_maks = hitung_bmi(berat, tinggi_cm)
    print(f"Berat badan : {berat:g} kg")
    print(f"Tinggi badan: {tinggi_cm:g} cm")
    print(f"BMI         : {bmi:.1f} ({label})")
    print(f"Rentang berat ideal: {ideal_min:.1f} - {ideal_maks:.1f} kg")
    print(saran)
    if bmi >= 23 and bmi < 25:
        print(
            "Catatan: untuk populasi Asia, risiko kesehatan mulai naik "
            "sejak BMI 23 meski masih dalam kategori Normal WHO."
        )


def tampilkan_kalori(berat, tinggi_cm, umur, jenis_kelamin, aktivitas, tujuan):
    """Tampilkan BMR, TDEE, dan target kalori harian."""
    bmr = hitung_bmr(berat, tinggi_cm, umur, jenis_kelamin)
    label_aktivitas, pengali, _penjelasan = AKTIVITAS[aktivitas]
    tdee = bmr * pengali
    target, peringatan = hitung_target(tdee, jenis_kelamin)

    print(f"Jenis kelamin : {jenis_kelamin}")
    print(f"Umur          : {umur} tahun")
    print(f"Aktivitas     : {label_aktivitas} (x{pengali})")
    print(f"BMR           : {bmr:.0f} kkal/hari (kalori saat istirahat total)")
    print(f"TDEE          : {tdee:.0f} kkal/hari (kebutuhan harian)")
    print()
    print("Target kalori harian (perkiraan, -/+ 0,5 kg per minggu):")
    print(f"  Turun berat : {target['turun']:.0f} kkal/hari")
    print(f"  Tahan berat : {target['tahan']:.0f} kkal/hari")
    print(f"  Naik berat  : {target['naik']:.0f} kkal/hari")
    if peringatan:
        print()
        print("Peringatan: " + peringatan)
    if tujuan:
        print()
        print(
            f"Target yang dipilih ({tujuan}): "
            f"{target[tujuan]:.0f} kkal/hari."
        )


def tampilkan_daftar():
    """Tampilkan daftar kategori BMI dan tingkat aktivitas."""
    print("Kategori BMI (WHO):")
    batas_bawah = 0.0
    for batas, label, saran in KATEGORI_BMI:
        atas = "ke atas" if batas == float("inf") else f"sampai {batas}"
        print(f"  {batas_bawah:g} {atas}: {label} — {saran}")
        batas_bawah = batas
    print()
    print("Tingkat aktivitas (pengali TDEE):")
    for nomor, (kunci, (label, pengali, penjelasan)) in enumerate(
        AKTIVITAS.items(), start=1
    ):
        print(f"  {nomor}. {kunci} (x{pengali}) — {label}: {penjelasan}")


def tanya_angka(pesan, batas, bilangan_bulat=False):
    """Minta angka dari pengguna, ulangi sampai valid."""
    while True:
        try:
            mentah = input(pesan).strip().replace(",", ".")
            nilai = int(mentah) if bilangan_bulat else float(mentah)
        except ValueError:
            print("Masukkan angka yang benar.")
            continue
        rendah, tinggi, satuan = batas
        if not rendah <= nilai <= tinggi:
            print(
                f"Nilai harus antara {rendah:g} dan {tinggi:g} {satuan}."
            )
            continue
        return nilai


def tanya_teks(pesan, pilihan):
    """Minta teks dari pengguna, ulangi sampai cocok dengan pilihan."""
    while True:
        jawaban = input(pesan).strip().lower()
        if jawaban in pilihan:
            return jawaban
        print("Pilihan tidak dikenal, coba lagi.")


def mode_interaktif():
    """Panduan langkah demi langkah untuk pengguna baru."""
    print("=== Kalkulator BMI & Kalori Harian ===")
    print("Tekan Ctrl+C untuk berhenti kapan saja.")
    print()
    berat = tanya_angka("Berat badan (kg): ", BATAS["berat"])
    tinggi = tanya_angka("Tinggi badan (cm): ", BATAS["tinggi"])
    print()
    tampilkan_bmi(berat, tinggi)
    print()
    if tanya_teks("Hitung kebutuhan kalori juga? (ya/tidak): ", ("ya", "tidak")) == "tidak":
        return
    umur = tanya_angka("Umur (tahun): ", BATAS["umur"], bilangan_bulat=True)
    jenis_kelamin = normalisasi_jenis_kelamin(
        tanya_teks("Jenis kelamin (pria/wanita): ", ("pria", "wanita", "l", "p"))
    )
    print()
    tampilkan_daftar()
    print()
    aktivitas = normalisasi_aktivitas(
        input("Tingkat aktivitas (nama atau nomor 1-5): ")
    )
    print()
    tampilkan_kalori(berat, tinggi, umur, jenis_kelamin, aktivitas, tujuan=None)


def buat_parser():
    """Bangun parser argumen baris perintah."""
    parser = argparse.ArgumentParser(
        description=(
            "Kalkulator BMI & Kalori Harian: hitung BMI, BMR, TDEE, "
            "dan target kalori harian."
        )
    )
    parser.add_argument(
        "--daftar",
        action="store_true",
        help="tampilkan daftar kategori BMI dan tingkat aktivitas",
    )
    sub = parser.add_subparsers(dest="perintah")

    p_bmi = sub.add_parser("bmi", help="hitung BMI dan berat ideal")
    p_bmi.add_argument("berat", type=float, help="berat badan dalam kg")
    p_bmi.add_argument("tinggi", type=float, help="tinggi badan dalam cm")

    p_kal = sub.add_parser(
        "kalori", help="hitung BMR, TDEE, dan target kalori"
    )
    p_kal.add_argument("berat", type=float, help="berat badan dalam kg")
    p_kal.add_argument("tinggi", type=float, help="tinggi badan dalam cm")
    p_kal.add_argument("umur", type=int, help="umur dalam tahun")
    p_kal.add_argument("jenis_kelamin", help="pria atau wanita")
    p_kal.add_argument(
        "aktivitas",
        help="sangat-ringan, ringan, sedang, aktif, sangat-aktif (atau 1-5)",
    )
    p_kal.add_argument(
        "--tujuan",
        choices=("turun", "tahan", "naik"),
        help="sorot satu target kalori",
    )
    return parser


def utama(argv=None):
    """Titik masuk program."""
    parser = buat_parser()
    args = parser.parse_args(argv)

    if args.daftar:
        tampilkan_daftar()
        return

    if args.perintah is None:
        try:
            mode_interaktif()
        except KeyboardInterrupt:
            print("\nBerhenti. Sampai jumpa!")
        return

    periksa_rentang("Berat badan", args.berat, BATAS["berat"])
    periksa_rentang("Tinggi badan", args.tinggi, BATAS["tinggi"])

    if args.perintah == "bmi":
        tampilkan_bmi(args.berat, args.tinggi)
        return

    periksa_rentang("Umur", args.umur, BATAS["umur"])
    jenis_kelamin = normalisasi_jenis_kelamin(args.jenis_kelamin)
    aktivitas = normalisasi_aktivitas(args.aktivitas)
    tampilkan_kalori(
        args.berat,
        args.tinggi,
        args.umur,
        jenis_kelamin,
        aktivitas,
        args.tujuan,
    )


if __name__ == "__main__":
    utama()
