#!/usr/bin/env python3
"""Kalkulator Biaya Listrik — Day 23 Daily Project 1.

Hitung biaya pemakaian listrik per alat dan perkiraan tagihan
bulanan dari golongan tarif rumah tangga PLN. Tambah alat-alat
di rumah (lampu, kulkas, AC, TV, dan lain-lain), lihat berapa
kWh dan rupiah yang dihabiskan tiap alat, lalu total tagihannya.

Rumus dasar: kWh = watt x jam nyala per hari x hari / 1000.
Biaya energi = kWh x tarif per kWh golongan yang dipilih.

Untuk pelanggan pascabayar berlaku rekening minimum: tagihan
paling sedikit 40 jam nyala x daya tersambung x tarif. Kalau
pemakaianmu di bawah itu, tagihan dihitung dari rekening
minimum. Pelanggan token (prabayar) tidak kena rekening
minimum, pakai opsi --token.

Python standar saja, tanpa library tambahan.

Cara pakai:
    python3 listrik.py
    python3 listrik.py golongan
    python3 listrik.py hitung 100 8
    python3 listrik.py hitung 350 24 --golongan 2200
    python3 listrik.py tambah "Kulkas" 150 24
    python3 listrik.py tambah "AC 1 PK" 800 8
    python3 listrik.py daftar
    python3 listrik.py total
    python3 listrik.py total --golongan 2200 --ppj 5
    python3 listrik.py total --token
    python3 listrik.py hemat 2 4
    python3 listrik.py hapus 1 --ya

Jalankan tanpa argumen untuk mode interaktif (menu angka).

Data disimpan di berkas `listrik.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek.
"""

import argparse
import json
import os
import sys

BERKAS_DATA = "listrik.json"
HARI_SEBULAN = 30
JAM_MINIMUM = 40  # jam nyala untuk rekening minimum pascabayar

# Golongan tarif rumah tangga PLN (Rp per kWh).
# Tarif yang tercantum adalah tarif yang umum dipublikasikan;
# tarif bisa berubah, cek tagihan terakhir dan ubah lewat --tarif.
TARIF = [
    {"kode": "450", "nama": "R-1 450 VA (subsidi)", "daya": 450, "tarif": 415},
    {"kode": "900", "nama": "R-1 900 VA", "daya": 900, "tarif": 1352},
    {"kode": "1300", "nama": "R-1 1300 VA", "daya": 1300, "tarif": 1444.70},
    {"kode": "2200", "nama": "R-1 2200 VA", "daya": 2200, "tarif": 1444.70},
    {"kode": "3500", "nama": "R-2 3500 VA", "daya": 3500, "tarif": 1699.53},
    {"kode": "5500", "nama": "R-2 5500 VA", "daya": 5500, "tarif": 1699.53},
    {"kode": "6600", "nama": "R-3 di atas 6600 VA", "daya": 6600, "tarif": 1699.53},
]
TARIF_DEFAULT = "1300"


def rupiah(nilai):
    """Format angka menjadi Rp, contoh: Rp144.470."""
    return "Rp" + f"{round(nilai):,}".replace(",", ".")


def cari_golongan(kode):
    """Cari golongan dari kodenya, kembalikan None bila tidak ada."""
    for golongan in TARIF:
        if golongan["kode"] == str(kode):
            return golongan
    return None


def kwh_per_bulan(watt, jam_per_hari, hari=HARI_SEBULAN):
    """Hitung kWh sebulan dari watt dan jam nyala per hari."""
    return watt * jam_per_hari * hari / 1000


def rekening_minimum(golongan):
    """Rekening minimum pascabayar: 40 jam x daya (kVA) x tarif."""
    return JAM_MINIMUM * (golongan["daya"] / 1000) * golongan["tarif"]


def muat_data():
    """Muat daftar alat dari berkas JSON, kembalikan list kosong bila belum ada."""
    if not os.path.exists(BERKAS_DATA):
        return []
    try:
        with open(BERKAS_DATA, "r", encoding="utf-8") as berkas:
            data = json.load(berkas)
    except (json.JSONDecodeError, OSError) as galat:
        print(f"Tidak bisa membaca {BERKAS_DATA}: {galat}")
        return []
    if not isinstance(data, list):
        return []
    return data


def simpan_data(data):
    """Simpan daftar alat ke berkas JSON."""
    try:
        with open(BERKAS_DATA, "w", encoding="utf-8") as berkas:
            json.dump(data, berkas, indent=2, ensure_ascii=False)
    except OSError as galat:
        print(f"Tidak bisa menyimpan {BERKAS_DATA}: {galat}")
        sys.exit(1)


def id_berikutnya(data):
    """ID baru: satu lebih besar dari ID terbesar yang ada."""
    return max((alat["id"] for alat in data), default=0) + 1


def tambah_alat(data, nama, watt, jam, hari=HARI_SEBULAN):
    """Tambah satu alat ke daftar dan simpan."""
    alat = {
        "id": id_berikutnya(data),
        "nama": nama,
        "watt": watt,
        "jam": jam,
        "hari": hari,
    }
    data.append(alat)
    simpan_data(data)
    kwh = kwh_per_bulan(watt, jam, hari)
    print(f"Ditambah: [{alat['id']}] {nama} — {watt} watt, "
          f"{jam} jam/hari, {hari} hari/bulan")
    print(f"Pemakaian: {kwh:.2f} kWh/bulan.")
    return alat


def tampilkan_daftar(data, golongan=None):
    """Tampilkan daftar alat beserta kWh dan biayanya."""
    if not data:
        print("Belum ada alat. Tambah dulu dengan perintah 'tambah'.")
        return
    print(f"{'ID':<4} {'Alat':<20} {'Watt':>6} {'Jam/hari':>9} "
          f"{'kWh/bln':>9} {'Biaya/bln':>14}")
    print("-" * 68)
    total_kwh = 0
    total_biaya = 0
    for alat in data:
        kwh = kwh_per_bulan(alat["watt"], alat["jam"], alat["hari"])
        biaya = kwh * golongan["tarif"] if golongan else 0
        total_kwh += kwh
        total_biaya += biaya
        kolom_biaya = rupiah(biaya) if golongan else "-"
        print(f"{alat['id']:<4} {alat['nama']:<20} {alat['watt']:>6} "
              f"{alat['jam']:>9} {kwh:>9.2f} {kolom_biaya:>14}")
    print("-" * 68)
    print(f"Total: {total_kwh:.2f} kWh/bulan", end="")
    if golongan:
        print(f" — {rupiah(total_biaya)} biaya energi "
              f"(tarif {golongan['nama']}).")
    else:
        print(" (tambah --golongan untuk melihat biaya).")


def hitung_cepat(watt, jam, hari, golongan):
    """Hitung cepat satu alat tanpa menyimpan."""
    kwh = kwh_per_bulan(watt, jam, hari)
    biaya = kwh * golongan["tarif"]
    print(f"Alat {watt} watt, nyala {jam} jam/hari, {hari} hari/bulan:")
    print(f"  Pemakaian : {kwh:.2f} kWh/bulan")
    print(f"  Tarif     : {rupiah(golongan['tarif'])}/kWh "
          f"({golongan['nama']})")
    print(f"  Biaya     : {rupiah(biaya)}/bulan")
    print(f"  Per hari  : {rupiah(biaya / hari)}")
    return kwh, biaya


def hitung_total(data, golongan, ppj=0, token=False):
    """Hitung perkiraan tagihan bulanan dari semua alat yang tercatat."""
    if not data:
        print("Belum ada alat. Tambah dulu dengan perintah 'tambah'.")
        return None

    rincian = []
    total_kwh = 0
    for alat in data:
        kwh = kwh_per_bulan(alat["watt"], alat["jam"], alat["hari"])
        rincian.append((alat, kwh))
        total_kwh += kwh

    biaya_energi = total_kwh * golongan["tarif"]
    minimum = 0 if token else rekening_minimum(golongan)
    kena_minimum = (not token) and biaya_energi < minimum
    dasar = max(biaya_energi, minimum)
    pajak = dasar * ppj / 100
    total = dasar + pajak

    rincian.sort(key=lambda item: item[1], reverse=True)

    print(f"Golongan: {golongan['nama']} — {rupiah(golongan['tarif'])}/kWh")
    print(f"Jumlah alat: {len(data)}")
    print()
    print("Pemakaian per alat (diurutkan dari yang paling boros):")
    for alat, kwh in rincian:
        persen = (kwh / total_kwh * 100) if total_kwh else 0
        print(f"  [{alat['id']}] {alat['nama']:<20} {kwh:>8.2f} kWh "
              f"({persen:.1f}%) — {rupiah(kwh * golongan['tarif'])}")
    print()
    print(f"Total pemakaian : {total_kwh:.2f} kWh/bulan")
    print(f"Biaya energi    : {rupiah(biaya_energi)}")
    if token:
        print("Mode token (prabayar): tidak ada rekening minimum.")
    else:
        print(f"Rekening minimum: {rupiah(minimum)} "
              f"(40 jam x {golongan['daya']} VA)")
        if kena_minimum:
            print("  -> Pemakaian di bawah minimum, tagihan memakai "
                  "rekening minimum.")
    if ppj:
        print(f"PPJ {ppj:g}%          : {rupiah(pajak)}")
    print(f"Perkiraan tagihan: {rupiah(total)}/bulan")
    print(f"Rata-rata per hari: {rupiah(total / HARI_SEBULAN)}")
    if rincian:
        boros = rincian[0][0]
        print()
        print(f"Alat paling boros: {boros['nama']} "
              f"({rincian[0][1]:.2f} kWh/bulan). Coba kurangi jam nyalanya "
              f"dengan perintah 'hemat {boros['id']} <jam baru>'.")
    return total


def tampilkan_golongan():
    """Tampilkan daftar golongan tarif rumah tangga."""
    print("Golongan tarif rumah tangga PLN (Rp/kWh):")
    print(f"{'Kode':<7} {'Golongan':<22} {'Tarif':>12}")
    print("-" * 43)
    for golongan in TARIF:
        print(f"{golongan['kode']:<7} {golongan['nama']:<22} "
              f"{rupiah(golongan['tarif']):>12}")
    print()
    print("Tarif mengikuti yang umum dipublikasikan dan bisa berubah;")
    print("cek tagihan terakhirmu dan pakai --tarif untuk tarif lain.")


def simulasi_hemat(data, alat_id, jam_baru, golongan):
    """Simulasikan penghematan bila jam nyala satu alat dikurangi."""
    alat = next((a for a in data if a["id"] == alat_id), None)
    if alat is None:
        print(f"Tidak ada alat dengan ID {alat_id}.")
        return
    if jam_baru < 0 or jam_baru > 24:
        print("Jam nyala harus 0 sampai 24.")
        return
    if jam_baru >= alat["jam"]:
        print(f"Jam baru ({jam_baru}) tidak lebih kecil dari jam sekarang "
              f"({alat['jam']}). Tidak ada penghematan.")
        return
    kwh_lama = kwh_per_bulan(alat["watt"], alat["jam"], alat["hari"])
    kwh_baru = kwh_per_bulan(alat["watt"], jam_baru, alat["hari"])
    hemat_kwh = kwh_lama - kwh_baru
    hemat_rp = hemat_kwh * golongan["tarif"]
    print(f"{alat['nama']} ({alat['watt']} watt):")
    print(f"  Sekarang : {alat['jam']} jam/hari — {kwh_lama:.2f} kWh/bulan "
          f"({rupiah(kwh_lama * golongan['tarif'])})")
    print(f"  Bila jadi : {jam_baru} jam/hari — {kwh_baru:.2f} kWh/bulan "
          f"({rupiah(kwh_baru * golongan['tarif'])})")
    print(f"  Hemat     : {hemat_kwh:.2f} kWh/bulan — "
          f"{rupiah(hemat_rp)}/bulan, {rupiah(hemat_rp * 12)}/tahun")
    print("Catatan: ini simulasi satu alat saja, jam alat tidak diubah.")
    print(f"Untuk mengubahnya, hapus lalu tambah ulang alat ini.")


def hapus_alat(data, alat_id, yakin):
    """Hapus satu alat dari daftar."""
    alat = next((a for a in data if a["id"] == alat_id), None)
    if alat is None:
        print(f"Tidak ada alat dengan ID {alat_id}.")
        return
    if not yakin:
        print(f"Hapus [{alat['id']}] {alat['nama']}? Tambahkan --ya "
              "untuk mengonfirmasi.")
        return
    data.remove(alat)
    simpan_data(data)
    print(f"Dihapus: [{alat['id']}] {alat['nama']}.")


def tanya_angka(pesan, default=None, batas_min=None, batas_max=None,
                bilangan_bulat=False):
    """Minta angka dari pengguna di mode interaktif."""
    while True:
        tambahan = f" [{default}]" if default is not None else ""
        jawaban = input(f"{pesan}{tambahan}: ").strip()
        if not jawaban and default is not None:
            return default
        try:
            nilai = int(jawaban) if bilangan_bulat else float(jawaban)
        except ValueError:
            print("Masukkan angka yang valid.")
            continue
        if batas_min is not None and nilai < batas_min:
            print(f"Nilainya minimal {batas_min}.")
            continue
        if batas_max is not None and nilai > batas_max:
            print(f"Nilainya maksimal {batas_max}.")
            continue
        return nilai


def mode_interaktif():
    """Menu angka untuk pengguna yang menjalankan tanpa argumen."""
    data = muat_data()
    golongan = cari_golongan(TARIF_DEFAULT)
    while True:
        print()
        print("=== Kalkulator Biaya Listrik ===")
        print(f"Golongan aktif: {golongan['nama']} "
              f"({rupiah(golongan['tarif'])}/kWh)")
        print(f"Alat tercatat: {len(data)}")
        print("1. Tambah alat")
        print("2. Lihat daftar alat")
        print("3. Hitung total tagihan bulanan")
        print("4. Hitung cepat satu alat")
        print("5. Simulasi hemat (kurangi jam nyala)")
        print("6. Lihat daftar golongan tarif")
        print("7. Ganti golongan")
        print("8. Hapus alat")
        print("0. Keluar")
        pilihan = input("Pilih (0-8): ").strip()
        if pilihan == "0":
            print("Sampai jumpa.")
            break
        if pilihan == "1":
            nama = input("Nama alat: ").strip()
            if not nama:
                print("Nama alat tidak boleh kosong.")
                continue
            watt = tanya_angka("Daya (watt)", batas_min=1)
            jam = tanya_angka("Jam nyala per hari (0-24)", batas_min=0,
                              batas_max=24)
            hari = tanya_angka("Hari per bulan", default=HARI_SEBULAN,
                               batas_min=1, batas_max=31,
                               bilangan_bulat=True)
            data = muat_data()
            tambah_alat(data, nama, watt, jam, hari)
        elif pilihan == "2":
            tampilkan_daftar(muat_data(), golongan)
        elif pilihan == "3":
            ppj = tanya_angka("PPJ (%) — pajak penerangan jalan, 0 bila tidak ada",
                              default=0, batas_min=0, batas_max=100)
            jawaban = input("Pakai token/prabayar? (y/tidak) [tidak]: ").strip().lower()
            hitung_total(muat_data(), golongan, ppj=ppj,
                         token=jawaban in ("y", "ya"))
        elif pilihan == "4":
            watt = tanya_angka("Daya (watt)", batas_min=1)
            jam = tanya_angka("Jam nyala per hari (0-24)", batas_min=0,
                              batas_max=24)
            hitung_cepat(watt, jam, HARI_SEBULAN, golongan)
        elif pilihan == "5":
            data = muat_data()
            if not data:
                print("Belum ada alat.")
                continue
            tampilkan_daftar(data, golongan)
            alat_id = tanya_angka("ID alat", batas_min=1,
                                  bilangan_bulat=True)
            jam_baru = tanya_angka("Jam nyala baru per hari (0-24)",
                                   batas_min=0, batas_max=24)
            simulasi_hemat(data, int(alat_id), jam_baru, golongan)
        elif pilihan == "6":
            tampilkan_golongan()
        elif pilihan == "7":
            tampilkan_golongan()
            kode = input("Kode golongan baru: ").strip()
            baru = cari_golongan(kode)
            if baru is None:
                print("Kode golongan tidak dikenal.")
            else:
                golongan = baru
                print(f"Golongan aktif: {golongan['nama']}.")
        elif pilihan == "8":
            data = muat_data()
            if not data:
                print("Belum ada alat.")
                continue
            tampilkan_daftar(data, golongan)
            alat_id = tanya_angka("ID alat yang dihapus", batas_min=1,
                                  bilangan_bulat=True)
            hapus_alat(data, int(alat_id), yakin=True)
        else:
            print("Pilihan tidak dikenal, coba 0-8.")


def validasi_angka(nilai, nama, batas_min=None, batas_max=None):
    """Periksa angka argumen baris perintah, berhenti bila tidak valid."""
    if batas_min is not None and nilai < batas_min:
        print(f"{nama} minimal {batas_min}.")
        sys.exit(1)
    if batas_max is not None and nilai > batas_max:
        print(f"{nama} maksimal {batas_max}.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Kalkulator biaya listrik rumah tangga (tarif PLN).")
    sub = parser.add_subparsers(dest="perintah")

    p_hitung = sub.add_parser("hitung", help="hitung cepat satu alat")
    p_hitung.add_argument("watt", type=float, help="daya alat dalam watt")
    p_hitung.add_argument("jam", type=float, help="jam nyala per hari (0-24)")
    p_hitung.add_argument("--hari", type=int, default=HARI_SEBULAN,
                          help="hari per bulan (default 30)")
    p_hitung.add_argument("--golongan", default=TARIF_DEFAULT,
                          help="kode golongan, misal 1300 (default 1300)")
    p_hitung.add_argument("--tarif", type=float, default=None,
                          help="tarif Rp/kWh sendiri (mengganti golongan)")

    p_tambah = sub.add_parser("tambah", help="tambah alat ke daftar")
    p_tambah.add_argument("nama", help="nama alat, misal \"Kulkas\"")
    p_tambah.add_argument("watt", type=float, help="daya alat dalam watt")
    p_tambah.add_argument("jam", type=float, help="jam nyala per hari (0-24)")
    p_tambah.add_argument("--hari", type=int, default=HARI_SEBULAN,
                          help="hari per bulan (default 30)")

    p_daftar = sub.add_parser("daftar", help="lihat daftar alat")
    p_daftar.add_argument("--golongan", default=None,
                          help="kode golongan untuk menampilkan biaya")

    p_total = sub.add_parser("total", help="hitung total tagihan bulanan")
    p_total.add_argument("--golongan", default=TARIF_DEFAULT,
                         help="kode golongan (default 1300)")
    p_total.add_argument("--tarif", type=float, default=None,
                         help="tarif Rp/kWh sendiri (mengganti golongan)")
    p_total.add_argument("--ppj", type=float, default=0,
                         help="PPJ dalam persen (default 0)")
    p_total.add_argument("--token", action="store_true",
                         help="mode token/prabayar, tanpa rekening minimum")

    sub.add_parser("golongan", help="lihat daftar golongan tarif PLN")

    p_hemat = sub.add_parser("hemat", help="simulasi hemat dari satu alat")
    p_hemat.add_argument("id", type=int, help="ID alat")
    p_hemat.add_argument("jam_baru", type=float,
                         help="jam nyala baru per hari (0-24)")
    p_hemat.add_argument("--golongan", default=TARIF_DEFAULT,
                         help="kode golongan (default 1300)")
    p_hemat.add_argument("--tarif", type=float, default=None,
                         help="tarif Rp/kWh sendiri (mengganti golongan)")

    p_hapus = sub.add_parser("hapus", help="hapus satu alat")
    p_hapus.add_argument("id", type=int, help="ID alat")
    p_hapus.add_argument("--ya", action="store_true",
                         help="konfirmasi penghapusan")

    args = parser.parse_args()

    if args.perintah is None:
        mode_interaktif()
        return

    if args.perintah == "golongan":
        tampilkan_golongan()
        return

    golongan = None
    if args.perintah in ("hitung", "total", "hemat", "daftar"):
        kode = getattr(args, "golongan", None)
        if kode:
            golongan = cari_golongan(kode)
            if golongan is None:
                print(f"Golongan '{kode}' tidak dikenal. Lihat perintah "
                      "'golongan' untuk daftar kode.")
                sys.exit(1)
        tarif_manual = getattr(args, "tarif", None)
        if tarif_manual is not None:
            if tarif_manual <= 0:
                print("Tarif harus lebih dari nol.")
                sys.exit(1)
            golongan = {"kode": "manual", "nama": "Tarif manual",
                        "daya": golongan["daya"] if golongan else 1300,
                        "tarif": tarif_manual}

    if args.perintah == "hitung":
        validasi_angka(args.watt, "Daya", batas_min=1)
        validasi_angka(args.jam, "Jam nyala", batas_min=0, batas_max=24)
        validasi_angka(args.hari, "Hari", batas_min=1, batas_max=31)
        hitung_cepat(args.watt, args.jam, args.hari, golongan)
    elif args.perintah == "tambah":
        validasi_angka(args.watt, "Daya", batas_min=1)
        validasi_angka(args.jam, "Jam nyala", batas_min=0, batas_max=24)
        validasi_angka(args.hari, "Hari", batas_min=1, batas_max=31)
        tambah_alat(muat_data(), args.nama, args.watt, args.jam, args.hari)
    elif args.perintah == "daftar":
        tampilkan_daftar(muat_data(), golongan)
    elif args.perintah == "total":
        validasi_angka(args.ppj, "PPJ", batas_min=0, batas_max=100)
        hitung_total(muat_data(), golongan, ppj=args.ppj, token=args.token)
    elif args.perintah == "hemat":
        validasi_angka(args.jam_baru, "Jam baru", batas_min=0, batas_max=24)
        simulasi_hemat(muat_data(), args.id, args.jam_baru, golongan)
    elif args.perintah == "hapus":
        hapus_alat(muat_data(), args.id, yakin=args.ya)


if __name__ == "__main__":
    main()
