#!/usr/bin/env python3
"""Pencatat Perawatan Kendaraan — Day 25 Daily Project 1.

Catat kendaraan (motor atau mobil) beserta riwayat perawatannya —
ganti oli, ganti ban, servis rem, dan lain-lain — lengkap dengan
biaya, kilometer saat servis, dan jadwal servis berikutnya.
Program juga mengingatkan servis yang sudah jatuh tempo dan pajak
STNK tahunan yang sebentar lagi habis.

Aturan pengingat yang dipakai:
    - Servis jatuh tempo bila kilometer berikutnya sudah tercapai,
      atau tanggal berikutnya sudah lewat.
    - Servis segera bila kilometer berikutnya tinggal 500 km lagi,
      atau tanggal berikutnya tinggal 30 hari lagi.
    - Pajak STNK diingatkan bila tinggal 30 hari lagi atau sudah lewat.

Python standar saja, tanpa library tambahan.

Cara pakai:
    python3 kendaraan.py
    python3 kendaraan.py tambah "Beat" motor "B 1234 ABC" 2020 --km 15000 --pajak 2027-03-15
    python3 kendaraan.py daftar
    python3 kendaraan.py servis 1 "Ganti oli" 85000 --km 15500 --berikutnya-km 17500
    python3 kendaraan.py servis 1 "Ganti ban belakang" 350000 --km 16000 --berikutnya-tanggal 2027-05-25
    python3 kendaraan.py riwayat 1
    python3 kendaraan.py ingat
    python3 kendaraan.py total
    python3 kendaraan.py total 1
    python3 kendaraan.py pajak 1 2027-03-15
    python3 kendaraan.py km 1 16000
    python3 kendaraan.py hapus 1 --ya

Jalankan tanpa argumen untuk mode interaktif (menu angka).

Data disimpan di berkas `kendaraan.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek.
"""

import argparse
import json
import os
import sys
from datetime import date, timedelta

BERKAS_DATA = "kendaraan.json"

# Jarak pengingat: servis dianggap "segera" bila tinggal segini lagi.
BATAS_KM_SEGERA = 500
BATAS_HARI_SEGERA = 30

JENIS_KENDARAAN = ("motor", "mobil")


def rupiah(nilai):
    """Format angka menjadi Rp, contoh: Rp85.000."""
    return "Rp" + f"{round(nilai):,}".replace(",", ".")


def format_km(nilai):
    """Format kilometer dengan pemisah ribuan, contoh: 15.500 km."""
    return f"{nilai:,} km".replace(",", ".")


def parse_tanggal(teks):
    """Ubah teks YYYY-MM-DD menjadi date, atau None bila salah format."""
    try:
        tahun, bulan, hari = (int(bagian) for bagian in teks.split("-"))
        return date(tahun, bulan, hari)
    except (ValueError, AttributeError):
        return None


def format_tanggal(tanggal):
    """Format date menjadi teks YYYY-MM-DD."""
    return tanggal.isoformat()


def muat_data():
    """Muat data kendaraan dari berkas JSON, atau data kosong."""
    if not os.path.exists(BERKAS_DATA):
        return {"kendaraan": []}
    try:
        with open(BERKAS_DATA, "r", encoding="utf-8") as berkas:
            data = json.load(berkas)
    except (json.JSONDecodeError, OSError):
        print(f"Berkas {BERKAS_DATA} rusak, mulai dari data kosong.")
        return {"kendaraan": []}
    if not isinstance(data, dict) or "kendaraan" not in data:
        return {"kendaraan": []}
    return data


def simpan_data(data):
    """Simpan data kendaraan ke berkas JSON."""
    with open(BERKAS_DATA, "w", encoding="utf-8") as berkas:
        json.dump(data, berkas, indent=2, ensure_ascii=False)


def cari_kendaraan(data, nomor):
    """Cari kendaraan berdasarkan nomor urut (mulai dari 1)."""
    if nomor < 1 or nomor > len(data["kendaraan"]):
        return None
    return data["kendaraan"][nomor - 1]


def minta_angka(pesan, default=None, minimal=None):
    """Minta masukan angka dari pengguna, dengan nilai default."""
    while True:
        teks = input(pesan).strip().replace(".", "").replace(",", "")
        if teks == "" and default is not None:
            return default
        try:
            nilai = int(teks)
        except ValueError:
            print("Masukkan angka yang benar.")
            continue
        if minimal is not None and nilai < minimal:
            print(f"Nilai minimal {minimal}.")
            continue
        return nilai


def minta_teks(pesan, default=None, wajib=False):
    """Minta masukan teks dari pengguna."""
    while True:
        teks = input(pesan).strip()
        if teks == "" and default is not None:
            return default
        if teks == "" and wajib:
            print("Tidak boleh kosong.")
            continue
        return teks


def minta_tanggal(pesan, default=None):
    """Minta masukan tanggal YYYY-MM-DD dari pengguna."""
    while True:
        teks = input(pesan).strip()
        if teks == "" and default is not None:
            return default
        tanggal = parse_tanggal(teks)
        if tanggal is None:
            print("Format tanggal salah, pakai YYYY-MM-DD (contoh: 2027-03-15).")
            continue
        return tanggal


def tambah_kendaraan(data, nama, jenis, plat, tahun, km, pajak):
    """Tambah satu kendaraan baru."""
    kendaraan = {
        "nama": nama,
        "jenis": jenis,
        "plat": plat,
        "tahun": tahun,
        "km": km,
        "pajak": format_tanggal(pajak) if pajak else None,
        "servis": [],
    }
    data["kendaraan"].append(kendaraan)
    simpan_data(data)
    print(f"Kendaraan ditambahkan: {nama} ({jenis}, {plat}, tahun {tahun}).")
    if pajak:
        print(f"Pajak STNK tahunan jatuh tempo {format_tanggal(pajak)}.")
    return kendaraan


def daftar_kendaraan(data):
    """Tampilkan semua kendaraan beserta ringkasannya."""
    if not data["kendaraan"]:
        print("Belum ada kendaraan. Tambah dulu dengan perintah tambah.")
        return
    print(f"{'No':>3}  {'Nama':<18} {'Jenis':<6} {'Plat':<12} {'Tahun':>5}  {'Km':>10}  {'Pajak STNK':<10}")
    print("-" * 78)
    for nomor, kendaraan in enumerate(data["kendaraan"], start=1):
        pajak = kendaraan.get("pajak") or "-"
        print(
            f"{nomor:>3}  {kendaraan['nama']:<18} {kendaraan['jenis']:<6} "
            f"{kendaraan['plat']:<12} {kendaraan['tahun']:>5}  "
            f"{format_km(kendaraan['km']):>10}  {pajak:<10}"
        )
    print(f"\nTotal {len(data['kendaraan'])} kendaraan.")


def tambah_servis(data, nomor, jenis_servis, biaya, km, tanggal, berikut_km, berikut_tanggal):
    """Catat satu riwayat servis untuk kendaraan tertentu."""
    kendaraan = cari_kendaraan(data, nomor)
    if kendaraan is None:
        print(f"Tidak ada kendaraan nomor {nomor}.")
        return False
    catatan = {
        "jenis": jenis_servis,
        "biaya": biaya,
        "km": km,
        "tanggal": format_tanggal(tanggal),
        "berikutnya_km": berikut_km,
        "berikutnya_tanggal": format_tanggal(berikut_tanggal) if berikut_tanggal else None,
    }
    kendaraan["servis"].append(catatan)
    if km is not None and km > kendaraan["km"]:
        kendaraan["km"] = km
    simpan_data(data)
    print(f"Servis dicatat: {jenis_servis} ({rupiah(biaya)}) untuk {kendaraan['nama']}.")
    if berikut_km:
        print(f"Servis berikutnya pada {format_km(berikut_km)}.")
    if berikut_tanggal:
        print(f"Servis berikutnya tanggal {format_tanggal(berikut_tanggal)}.")
    return True


def riwayat_servis(data, nomor):
    """Tampilkan riwayat servis satu kendaraan."""
    kendaraan = cari_kendaraan(data, nomor)
    if kendaraan is None:
        print(f"Tidak ada kendaraan nomor {nomor}.")
        return
    print(f"Riwayat servis {kendaraan['nama']} ({kendaraan['plat']}):")
    if not kendaraan["servis"]:
        print("Belum ada riwayat servis.")
        return
    total_biaya = 0
    for urutan, servis in enumerate(kendaraan["servis"], start=1):
        total_biaya += servis["biaya"]
        berikut = []
        if servis.get("berikutnya_km"):
            berikut.append(f"berikutnya {format_km(servis['berikutnya_km'])}")
        if servis.get("berikutnya_tanggal"):
            berikut.append(f"berikutnya {servis['berikutnya_tanggal']}")
        keterangan = "; ".join(berikut)
        if keterangan:
            keterangan = " (" + keterangan + ")"
        print(
            f"{urutan}. {servis['tanggal']} — {servis['jenis']}: "
            f"{rupiah(servis['biaya'])} pada {format_km(servis['km'])}{keterangan}"
        )
    print(f"Total biaya servis: {rupiah(total_biaya)} "
          f"({len(kendaraan['servis'])} kali servis).")


def status_servis(kendaraan, hari_ini):
    """Tentukan status pengingat servis terakhir tiap kendaraan.

    Mengembalikan daftar (tingkat, pesan) dengan tingkat:
    2 = jatuh tempo, 1 = segera, 0 = aman.
    """
    hasil = []
    if not kendaraan["servis"]:
        return hasil
    servis = kendaraan["servis"][-1]
    if servis.get("berikutnya_km"):
        selisih = servis["berikutnya_km"] - kendaraan["km"]
        if selisih <= 0:
            hasil.append((2, f"servis {servis['jenis']} sudah lewat "
                             f"{format_km(-selisih)} (batas {format_km(servis['berikutnya_km'])})"))
        elif selisih <= BATAS_KM_SEGERA:
            hasil.append((1, f"servis {servis['jenis']} tinggal {format_km(selisih)} lagi "
                             f"(batas {format_km(servis['berikutnya_km'])})"))
    if servis.get("berikutnya_tanggal"):
        batas = parse_tanggal(servis["berikutnya_tanggal"])
        selisih_hari = (batas - hari_ini).days
        if selisih_hari <= 0:
            hasil.append((2, f"servis {servis['jenis']} sudah lewat "
                             f"{-selisih_hari} hari (batas {servis['berikutnya_tanggal']})"))
        elif selisih_hari <= BATAS_HARI_SEGERA:
            hasil.append((1, f"servis {servis['jenis']} tinggal {selisih_hari} hari lagi "
                             f"(batas {servis['berikutnya_tanggal']})"))
    return hasil


def status_pajak(kendaraan, hari_ini):
    """Tentukan status pengingat pajak STNK tahunan.

    Mengembalikan (tingkat, pesan) atau None bila tidak ada tanggal pajak.
    Tingkat: 2 = lewat/lewat hari ini, 1 = segera, 0 = aman.
    """
    if not kendaraan.get("pajak"):
        return None
    batas = parse_tanggal(kendaraan["pajak"])
    if batas is None:
        return None
    selisih_hari = (batas - hari_ini).days
    if selisih_hari < 0:
        return (2, f"pajak STNK sudah lewat {-selisih_hari} hari "
                   f"(jatuh tempo {kendaraan['pajak']})")
    if selisih_hari <= BATAS_HARI_SEGERA:
        return (1, f"pajak STNK tinggal {selisih_hari} hari lagi "
                   f"(jatuh tempo {kendaraan['pajak']})")
    return (0, f"pajak STNK aman sampai {kendaraan['pajak']}")


def pengingat(data, hari_ini=None):
    """Tampilkan semua pengingat servis dan pajak STNK."""
    hari_ini = hari_ini or date.today()
    if not data["kendaraan"]:
        print("Belum ada kendaraan. Tambah dulu dengan perintah tambah.")
        return
    jatuh_tempo = []
    segera = []
    for nomor, kendaraan in enumerate(data["kendaraan"], start=1):
        label = f"{kendaraan['nama']} ({kendaraan['plat']})"
        for tingkat, pesan in status_servis(kendaraan, hari_ini):
            if tingkat == 2:
                jatuh_tempo.append(f"{label}: {pesan}")
            else:
                segera.append(f"{label}: {pesan}")
        pajak = status_pajak(kendaraan, hari_ini)
        if pajak:
            tingkat, pesan = pajak
            if tingkat == 2:
                jatuh_tempo.append(f"{label}: {pesan}")
            elif tingkat == 1:
                segera.append(f"{label}: {pesan}")
    print(f"Pengingat per {format_tanggal(hari_ini)}:")
    if jatuh_tempo:
        print("\nJATUH TEMPO:")
        for pesan in jatuh_tempo:
            print(f"  ! {pesan}")
    if segera:
        print("\nSEGERA:")
        for pesan in segera:
            print(f"  - {pesan}")
    if not jatuh_tempo and not segera:
        print("Semua aman, tidak ada servis atau pajak yang jatuh tempo.")


def total_biaya(data, nomor=None):
    """Tampilkan total biaya servis, per kendaraan atau semua."""
    if nomor is not None:
        kendaraan = cari_kendaraan(data, nomor)
        if kendaraan is None:
            print(f"Tidak ada kendaraan nomor {nomor}.")
            return
        total = sum(s["biaya"] for s in kendaraan["servis"])
        print(f"Total biaya servis {kendaraan['nama']}: {rupiah(total)} "
              f"({len(kendaraan['servis'])} kali servis).")
        return
    if not data["kendaraan"]:
        print("Belum ada kendaraan. Tambah dulu dengan perintah tambah.")
        return
    total_semua = 0
    print(f"{'No':>3}  {'Nama':<18} {'Servis':>6}  {'Total biaya':>14}")
    print("-" * 48)
    for nomor, kendaraan in enumerate(data["kendaraan"], start=1):
        total = sum(s["biaya"] for s in kendaraan["servis"])
        total_semua += total
        print(f"{nomor:>3}  {kendaraan['nama']:<18} {len(kendaraan['servis']):>6}  "
              f"{rupiah(total):>14}")
    print("-" * 48)
    print(f"Total semua kendaraan: {rupiah(total_semua)}.")


def ubah_pajak(data, nomor, tanggal):
    """Perbarui tanggal jatuh tempo pajak STNK tahunan."""
    kendaraan = cari_kendaraan(data, nomor)
    if kendaraan is None:
        print(f"Tidak ada kendaraan nomor {nomor}.")
        return False
    kendaraan["pajak"] = format_tanggal(tanggal)
    simpan_data(data)
    print(f"Pajak STNK {kendaraan['nama']} diperbarui ke {format_tanggal(tanggal)}.")
    return True


def ubah_km(data, nomor, km):
    """Perbarui kilometer kendaraan saat ini."""
    kendaraan = cari_kendaraan(data, nomor)
    if kendaraan is None:
        print(f"Tidak ada kendaraan nomor {nomor}.")
        return False
    kendaraan["km"] = km
    simpan_data(data)
    print(f"Kilometer {kendaraan['nama']} diperbarui ke {format_km(km)}.")
    return True


def hapus_kendaraan(data, nomor):
    """Hapus satu kendaraan beserta riwayat servisnya."""
    kendaraan = cari_kendaraan(data, nomor)
    if kendaraan is None:
        print(f"Tidak ada kendaraan nomor {nomor}.")
        return False
    del data["kendaraan"][nomor - 1]
    simpan_data(data)
    print(f"Kendaraan {kendaraan['nama']} ({kendaraan['plat']}) dihapus.")
    return True


def menu_interaktif():
    """Mode interaktif dengan menu angka."""
    data = muat_data()
    while True:
        print("\n=== Pencatat Perawatan Kendaraan ===")
        print("1. Tambah kendaraan")
        print("2. Lihat daftar kendaraan")
        print("3. Catat servis")
        print("4. Lihat riwayat servis")
        print("5. Lihat pengingat (servis & pajak STNK)")
        print("6. Lihat total biaya servis")
        print("7. Perbarui tanggal pajak STNK")
        print("8. Perbarui kilometer kendaraan")
        print("9. Hapus kendaraan")
        print("0. Keluar")
        pilihan = input("Pilih menu (0-9): ").strip()
        if pilihan == "0":
            print("Sampai jumpa, rawat kendaraanmu baik-baik.")
            break
        if pilihan == "1":
            nama = minta_teks("Nama kendaraan (contoh: Beat): ", wajib=True)
            jenis = minta_teks("Jenis (motor/mobil): ", wajib=True).lower()
            while jenis not in JENIS_KENDARAAN:
                print("Jenis harus motor atau mobil.")
                jenis = minta_teks("Jenis (motor/mobil): ", wajib=True).lower()
            plat = minta_teks("Nomor plat (contoh: B 1234 ABC): ", wajib=True).upper()
            tahun = minta_angka("Tahun kendaraan: ", minimal=1900)
            km = minta_angka("Kilometer saat ini: ", default=0, minimal=0)
            teks_pajak = input("Tanggal pajak STNK (YYYY-MM-DD, kosongkan bila belum tahu): ").strip()
            pajak = parse_tanggal(teks_pajak) if teks_pajak else None
            if teks_pajak and pajak is None:
                print("Format tanggal salah, pajak dikosongkan.")
            tambah_kendaraan(data, nama, jenis, plat, tahun, km, pajak)
        elif pilihan == "2":
            daftar_kendaraan(data)
        elif pilihan == "3":
            daftar_kendaraan(data)
            if not data["kendaraan"]:
                continue
            nomor = minta_angka("Nomor kendaraan: ", minimal=1)
            jenis_servis = minta_teks("Jenis servis (contoh: Ganti oli): ", wajib=True)
            biaya = minta_angka("Biaya servis (Rp): ", minimal=0)
            km = minta_angka("Kilometer saat servis: ", default=None, minimal=0)
            tanggal = minta_tanggal("Tanggal servis (YYYY-MM-DD): ", default=date.today())
            teks_km = input("Servis berikutnya pada km (kosongkan bila tidak ada): ").strip()
            berikut_km = None
            if teks_km:
                try:
                    berikut_km = int(teks_km.replace(".", ""))
                except ValueError:
                    print("Kilometer berikutnya tidak valid, dikosongkan.")
            teks_tanggal = input("Servis berikutnya tanggal (YYYY-MM-DD, kosongkan bila tidak ada): ").strip()
            berikut_tanggal = parse_tanggal(teks_tanggal) if teks_tanggal else None
            if teks_tanggal and berikut_tanggal is None:
                print("Format tanggal salah, tanggal berikutnya dikosongkan.")
            tambah_servis(data, nomor, jenis_servis, biaya, km, tanggal, berikut_km, berikut_tanggal)
        elif pilihan == "4":
            daftar_kendaraan(data)
            if not data["kendaraan"]:
                continue
            nomor = minta_angka("Nomor kendaraan: ", minimal=1)
            riwayat_servis(data, nomor)
        elif pilihan == "5":
            pengingat(data)
        elif pilihan == "6":
            total_biaya(data)
        elif pilihan == "7":
            daftar_kendaraan(data)
            if not data["kendaraan"]:
                continue
            nomor = minta_angka("Nomor kendaraan: ", minimal=1)
            tanggal = minta_tanggal("Tanggal pajak baru (YYYY-MM-DD): ")
            ubah_pajak(data, nomor, tanggal)
        elif pilihan == "8":
            daftar_kendaraan(data)
            if not data["kendaraan"]:
                continue
            nomor = minta_angka("Nomor kendaraan: ", minimal=1)
            km = minta_angka("Kilometer saat ini: ", minimal=0)
            ubah_km(data, nomor, km)
        elif pilihan == "9":
            daftar_kendaraan(data)
            if not data["kendaraan"]:
                continue
            nomor = minta_angka("Nomor kendaraan: ", minimal=1)
            yakin = input("Yakin hapus? Riwayat servis ikut terhapus (y/t): ").strip().lower()
            if yakin == "y":
                hapus_kendaraan(data, nomor)
            else:
                print("Dibatalkan.")
        else:
            print("Pilihan tidak dikenal, pilih 0-9.")


def main(argv=None):
    """Titik masuk program: mode perintah atau mode interaktif."""
    parser = argparse.ArgumentParser(
        description="Pencatat Perawatan Kendaraan: servis, biaya, dan pengingat pajak STNK."
    )
    sub = parser.add_subparsers(dest="perintah")

    p_tambah = sub.add_parser("tambah", help="Tambah kendaraan baru")
    p_tambah.add_argument("nama", help="Nama kendaraan, contoh: Beat")
    p_tambah.add_argument("jenis", choices=JENIS_KENDARAAN, help="motor atau mobil")
    p_tambah.add_argument("plat", help="Nomor plat, contoh: B 1234 ABC")
    p_tambah.add_argument("tahun", type=int, help="Tahun kendaraan")
    p_tambah.add_argument("--km", type=int, default=0, help="Kilometer saat ini")
    p_tambah.add_argument("--pajak", help="Tanggal pajak STNK (YYYY-MM-DD)")

    sub.add_parser("daftar", help="Lihat daftar kendaraan")

    p_servis = sub.add_parser("servis", help="Catat servis kendaraan")
    p_servis.add_argument("nomor", type=int, help="Nomor kendaraan dari daftar")
    p_servis.add_argument("jenis", help="Jenis servis, contoh: Ganti oli")
    p_servis.add_argument("biaya", type=int, help="Biaya servis (Rp)")
    p_servis.add_argument("--km", type=int, help="Kilometer saat servis")
    p_servis.add_argument("--tanggal", help="Tanggal servis (YYYY-MM-DD, default hari ini)")
    p_servis.add_argument("--berikutnya-km", type=int, help="Servis berikutnya pada km")
    p_servis.add_argument("--berikutnya-tanggal", help="Servis berikutnya tanggal (YYYY-MM-DD)")

    p_riwayat = sub.add_parser("riwayat", help="Lihat riwayat servis kendaraan")
    p_riwayat.add_argument("nomor", type=int, help="Nomor kendaraan dari daftar")

    sub.add_parser("ingat", help="Lihat pengingat servis dan pajak STNK")

    p_total = sub.add_parser("total", help="Lihat total biaya servis")
    p_total.add_argument("nomor", type=int, nargs="?", help="Nomor kendaraan (kosong = semua)")

    p_pajak = sub.add_parser("pajak", help="Perbarui tanggal pajak STNK")
    p_pajak.add_argument("nomor", type=int, help="Nomor kendaraan dari daftar")
    p_pajak.add_argument("tanggal", help="Tanggal pajak baru (YYYY-MM-DD)")

    p_km = sub.add_parser("km", help="Perbarui kilometer kendaraan")
    p_km.add_argument("nomor", type=int, help="Nomor kendaraan dari daftar")
    p_km.add_argument("km", type=int, help="Kilometer saat ini")

    p_hapus = sub.add_parser("hapus", help="Hapus kendaraan beserta riwayat servisnya")
    p_hapus.add_argument("nomor", type=int, help="Nomor kendaraan dari daftar")
    p_hapus.add_argument("--ya", action="store_true", help="Lewati konfirmasi")

    args = parser.parse_args(argv)
    if args.perintah is None:
        menu_interaktif()
        return 0

    data = muat_data()
    if args.perintah == "tambah":
        pajak = parse_tanggal(args.pajak) if args.pajak else None
        if args.pajak and pajak is None:
            print("Format tanggal pajak salah, pakai YYYY-MM-DD.")
            return 1
        tambah_kendaraan(data, args.nama, args.jenis, args.plat, args.tahun, args.km, pajak)
    elif args.perintah == "daftar":
        daftar_kendaraan(data)
    elif args.perintah == "servis":
        tanggal = parse_tanggal(args.tanggal) if args.tanggal else date.today()
        if args.tanggal and tanggal is None:
            print("Format tanggal servis salah, pakai YYYY-MM-DD.")
            return 1
        berikut_tanggal = parse_tanggal(args.berikutnya_tanggal) if args.berikutnya_tanggal else None
        if args.berikutnya_tanggal and berikut_tanggal is None:
            print("Format tanggal berikutnya salah, pakai YYYY-MM-DD.")
            return 1
        if not tambah_servis(data, args.nomor, args.jenis, args.biaya, args.km,
                             tanggal, args.berikutnya_km, berikut_tanggal):
            return 1
    elif args.perintah == "riwayat":
        riwayat_servis(data, args.nomor)
    elif args.perintah == "ingat":
        pengingat(data)
    elif args.perintah == "total":
        total_biaya(data, args.nomor)
    elif args.perintah == "pajak":
        tanggal = parse_tanggal(args.tanggal)
        if tanggal is None:
            print("Format tanggal salah, pakai YYYY-MM-DD.")
            return 1
        if not ubah_pajak(data, args.nomor, tanggal):
            return 1
    elif args.perintah == "km":
        if not ubah_km(data, args.nomor, args.km):
            return 1
    elif args.perintah == "hapus":
        if not args.ya:
            yakin = input("Yakin hapus? Riwayat servis ikut terhapus (y/t): ").strip().lower()
            if yakin != "y":
                print("Dibatalkan.")
                return 0
        if not hapus_kendaraan(data, args.nomor):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
