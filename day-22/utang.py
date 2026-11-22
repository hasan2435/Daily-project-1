#!/usr/bin/env python3
"""Pencatat Utang & Piutang — Day 22 Daily Project 1.

Catat siapa berutang ke siapa, berapa sisanya, dan kapan jatuh
temponya. Dua jenis catatan:

  utang    — kita berutang ke orang lain (kita yang harus bayar)
  piutang  — orang lain berutang ke kita (kita yang menagih)

Pembayaran bisa dicicil: tiap pembayaran mengurangi sisa dan
dicatat riwayatnya. Kalau sisa sudah nol, catatan otomatis lunas.

Python standar saja, tanpa library tambahan.

Cara pakai:
    python3 utang.py
    python3 utang.py tambah utang Budi 500000 --jatuh-tempo 2026-12-22
    python3 utang.py tambah piutang Ani 250000 --catatan "Talang tiket"
    python3 utang.py daftar
    python3 utang.py daftar --jenis piutang --status aktif
    python3 utang.py bayar 1 200000
    python3 utang.py total
    python3 utang.py jatuh-tempo
    python3 utang.py jatuh-tempo --hari 7
    python3 utang.py detail 1
    python3 utang.py hapus 2 --ya

Jalankan tanpa argumen untuk mode interaktif (menu angka).

Data disimpan di berkas `utang.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek.
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta

BERKAS_DATA = "utang.json"
FORMAT_TANGGAL = "%Y-%m-%d"


def rupiah(nilai):
    """Format angka menjadi Rp, contoh: Rp500.000."""
    return "Rp" + f"{int(nilai):,}".replace(",", ".")


def hari_ini():
    return date.today()


def parse_tanggal(teks, nama="tanggal"):
    """Ubah teks YYYY-MM-DD menjadi date, atau None bila kosong."""
    if not teks:
        return None
    try:
        return datetime.strptime(teks, FORMAT_TANGGAL).date()
    except ValueError:
        raise ValueError(
            f"{nama} harus berformat YYYY-MM-DD, contoh: 2026-12-22."
        )


def format_tanggal(tanggal):
    if tanggal is None:
        return "-"
    return tanggal.strftime(FORMAT_TANGGAL)


def tanggal_dari_iso(teks):
    if not teks:
        return None
    return datetime.strptime(teks, FORMAT_TANGGAL).date()


def muat_data():
    """Baca utang.json; kembalikan dict {berikutnya, catatan}."""
    if not os.path.exists(BERKAS_DATA):
        return {"berikutnya": 1, "catatan": []}
    try:
        with open(BERKAS_DATA, "r", encoding="utf-8") as berkas:
            data = json.load(berkas)
    except (json.JSONDecodeError, OSError) as galat:
        print(f"Berkas {BERKAS_DATA} rusak atau tidak bisa dibaca: {galat}")
        sys.exit(1)
    if not isinstance(data, dict) or "catatan" not in data:
        print(f"Berkas {BERKAS_DATA} formatnya tidak dikenal.")
        sys.exit(1)
    return data


def simpan_data(data):
    with open(BERKAS_DATA, "w", encoding="utf-8") as berkas:
        json.dump(data, berkas, ensure_ascii=False, indent=2)
        berkas.write("\n")


def cari_catatan(data, nomor):
    for catatan in data["catatan"]:
        if catatan["id"] == nomor:
            return catatan
    return None


def status_catatan(catatan):
    """Kembalikan 'LUNAS', 'LEWAT TEMPO', atau 'Aktif'."""
    if catatan["sisa"] <= 0:
        return "LUNAS"
    jatuh_tempo = tanggal_dari_iso(catatan.get("jatuh_tempo"))
    if jatuh_tempo is not None and jatuh_tempo < hari_ini():
        return "LEWAT TEMPO"
    return "Aktif"


def sisa_hari(catatan):
    """Jumlah hari sampai jatuh tempo (negatif bila sudah lewat)."""
    jatuh_tempo = tanggal_dari_iso(catatan.get("jatuh_tempo"))
    if jatuh_tempo is None:
        return None
    return (jatuh_tempo - hari_ini()).days


def tambah(jenis, nama, jumlah, tanggal=None, jatuh_tempo=None, catatan=""):
    if jenis not in ("utang", "piutang"):
        print("Jenis harus 'utang' atau 'piutang'.")
        return 1
    if jumlah <= 0:
        print("Jumlah harus lebih dari nol.")
        return 1
    tanggal_catatan = tanggal or hari_ini()
    if jatuh_tempo is not None and jatuh_tempo < tanggal_catatan:
        print("Peringatan: jatuh tempo lebih awal dari tanggal catatan.")
    data = muat_data()
    baru = {
        "id": data["berikutnya"],
        "jenis": jenis,
        "nama": nama,
        "jumlah_awal": jumlah,
        "sisa": jumlah,
        "tanggal": format_tanggal(tanggal_catatan),
        "jatuh_tempo": (
            jatuh_tempo.strftime(FORMAT_TANGGAL) if jatuh_tempo else None
        ),
        "catatan": catatan,
        "riwayat": [],
    }
    data["catatan"].append(baru)
    data["berikutnya"] += 1
    simpan_data(data)
    label = "Utang ke" if jenis == "utang" else "Piutang dari"
    print(f"Ditambahkan #{baru['id']}: {label} {nama} sebesar {rupiah(jumlah)}.")
    if jatuh_tempo is not None:
        print(f"Jatuh tempo: {format_tanggal(jatuh_tempo)}.")
    return 0


def daftar(jenis=None, status="aktif", nama=None):
    data = muat_data()
    hasil = data["catatan"]
    if jenis is not None:
        hasil = [c for c in hasil if c["jenis"] == jenis]
    if nama:
        hasil = [c for c in hasil if nama.lower() in c["nama"].lower()]
    if status == "aktif":
        hasil = [c for c in hasil if c["sisa"] > 0]
    elif status == "lunas":
        hasil = [c for c in hasil if c["sisa"] <= 0]
    elif status != "semua":
        print("Status harus 'aktif', 'lunas', atau 'semua'.")
        return 1
    if not hasil:
        print("Tidak ada catatan yang cocok.")
        return 0
    hasil.sort(key=lambda c: (c["sisa"] <= 0, c.get("jatuh_tempo") or "9999"))
    print(f"{'ID':<4}{'Jenis':<9}{'Nama':<18}{'Sisa':<14}{'Jatuh tempo':<13}Status")
    print("-" * 70)
    for c in hasil:
        jatuh = c.get("jatuh_tempo") or "-"
        print(
            f"{c['id']:<4}{c['jenis']:<9}{c['nama']:<18}"
            f"{rupiah(c['sisa']):<14}{jatuh:<13}{status_catatan(c)}"
        )
    print("-" * 70)
    total = sum(c["sisa"] for c in hasil)
    print(f"Total sisa ({len(hasil)} catatan): {rupiah(total)}")
    return 0


def bayar(nomor, jumlah, tanggal=None):
    if jumlah <= 0:
        print("Jumlah pembayaran harus lebih dari nol.")
        return 1
    data = muat_data()
    catatan = cari_catatan(data, nomor)
    if catatan is None:
        print(f"Tidak ada catatan dengan ID {nomor}.")
        return 1
    if catatan["sisa"] <= 0:
        print(f"Catatan #{nomor} sudah lunas.")
        return 1
    if jumlah > catatan["sisa"]:
        print(
            f"Jumlah melebihi sisa {rupiah(catatan['sisa'])}. "
            "Bayar tepat sebesar sisa untuk melunasi."
        )
        return 1
    tanggal_bayar = tanggal or hari_ini()
    catatan["sisa"] -= jumlah
    catatan["riwayat"].append(
        {
            "tanggal": format_tanggal(tanggal_bayar),
            "jumlah": jumlah,
            "keterangan": "bayar" if catatan["jenis"] == "utang" else "terima",
        }
    )
    simpan_data(data)
    if catatan["jenis"] == "utang":
        print(f"Dibayar {rupiah(jumlah)} ke {catatan['nama']}.")
    else:
        print(f"Diterima {rupiah(jumlah)} dari {catatan['nama']}.")
    if catatan["sisa"] == 0:
        print(f"Catatan #{nomor} LUNAS. Selesai!")
    else:
        print(f"Sisa: {rupiah(catatan['sisa'])}.")
    return 0


def total():
    data = muat_data()
    aktif = [c for c in data["catatan"] if c["sisa"] > 0]
    total_utang = sum(c["sisa"] for c in aktif if c["jenis"] == "utang")
    total_piutang = sum(c["sisa"] for c in aktif if c["jenis"] == "piutang")
    lunas = len(data["catatan"]) - len(aktif)
    print("Ringkasan Utang & Piutang")
    print("-" * 40)
    print(f"Total utang aktif (kita harus bayar) : {rupiah(total_utang)}")
    print(f"Total piutang aktif (kita menagih)   : {rupiah(total_piutang)}")
    print(f"Posisi bersih (piutang - utang)      : {rupiah(total_piutang - total_utang)}")
    print(f"Catatan aktif: {len(aktif)}, sudah lunas: {lunas}")
    if total_piutang - total_utang >= 0:
        print("Posisi bersih positif: lebih banyak yang berutang ke kita.")
    else:
        print("Posisi bersih negatif: kita lebih banyak berutang.")
    print()
    print("Per orang (sisa aktif):")
    per_orang = {}
    for c in aktif:
        kunci = (c["nama"], c["jenis"])
        per_orang[kunci] = per_orang.get(kunci, 0) + c["sisa"]
    if not per_orang:
        print("  (belum ada catatan aktif)")
    for (nama, jenis), sisa in sorted(per_orang.items()):
        label = "utang ke" if jenis == "utang" else "piutang dari"
        print(f"  {label} {nama}: {rupiah(sisa)}")
    return 0


def jatuh_tempo(hari=7):
    data = muat_data()
    aktif = [c for c in data["catatan"] if c["sisa"] > 0]
    lewat = [c for c in aktif if (sisa_hari(c) or 0) < 0]
    dekat = [
        c
        for c in aktif
        if sisa_hari(c) is not None and 0 <= sisa_hari(c) <= hari
    ]
    tanpa_tempo = [c for c in aktif if sisa_hari(c) is None]
    if lewat:
        print(f"Sudah lewat jatuh tempo ({len(lewat)}):")
        for c in sorted(lewat, key=sisa_hari):
            label = "utang ke" if c["jenis"] == "utang" else "piutang dari"
            print(
                f"  #{c['id']} {label} {c['nama']}: {rupiah(c['sisa'])}, "
                f"jatuh tempo {c['jatuh_tempo']} ({-sisa_hari(c)} hari lalu)"
            )
    if dekat:
        print(f"Jatuh tempo dalam {hari} hari ke depan ({len(dekat)}):")
        for c in sorted(dekat, key=sisa_hari):
            label = "utang ke" if c["jenis"] == "utang" else "piutang dari"
            kapan = "hari ini" if sisa_hari(c) == 0 else f"{sisa_hari(c)} hari lagi"
            print(
                f"  #{c['id']} {label} {c['nama']}: {rupiah(c['sisa'])}, "
                f"jatuh tempo {c['jatuh_tempo']} ({kapan})"
            )
    if not lewat and not dekat:
        print(f"Tidak ada yang jatuh tempo dalam {hari} hari ke depan.")
    if tanpa_tempo:
        print(
            f"Catatan: {len(tanpa_tempo)} catatan aktif tanpa tanggal "
            "jatuh tempo."
        )
    return 0


def detail(nomor):
    data = muat_data()
    catatan = cari_catatan(data, nomor)
    if catatan is None:
        print(f"Tidak ada catatan dengan ID {nomor}.")
        return 1
    label = "Utang (kita berutang)" if catatan["jenis"] == "utang" else "Piutang (orang berutang ke kita)"
    print(f"Catatan #{catatan['id']} — {label}")
    print("-" * 40)
    print(f"Nama        : {catatan['nama']}")
    print(f"Jumlah awal : {rupiah(catatan['jumlah_awal'])}")
    print(f"Sisa        : {rupiah(catatan['sisa'])}")
    print(f"Tanggal     : {catatan['tanggal']}")
    print(f"Jatuh tempo : {catatan.get('jatuh_tempo') or '-'}")
    print(f"Status      : {status_catatan(catatan)}")
    if catatan.get("catatan"):
        print(f"Catatan     : {catatan['catatan']}")
    print("Riwayat pembayaran:")
    if not catatan["riwayat"]:
        print("  (belum ada pembayaran)")
    for r in catatan["riwayat"]:
        kata = "Bayar" if r["keterangan"] == "bayar" else "Terima"
        print(f"  {r['tanggal']}: {kata} {rupiah(r['jumlah'])}")
    return 0


def hapus(nomor, ya=False):
    data = muat_data()
    catatan = cari_catatan(data, nomor)
    if catatan is None:
        print(f"Tidak ada catatan dengan ID {nomor}.")
        return 1
    label = "utang ke" if catatan["jenis"] == "utang" else "piutang dari"
    if not ya:
        jawab = input(
            f"Hapus #{nomor} ({label} {catatan['nama']}, "
            f"sisa {rupiah(catatan['sisa'])})? (y/n): "
        ).strip().lower()
        if jawab not in ("y", "ya"):
            print("Dibatalkan.")
            return 0
    data["catatan"] = [c for c in data["catatan"] if c["id"] != nomor]
    simpan_data(data)
    print(f"Catatan #{nomor} dihapus.")
    return 0


def tanya(teks, wajib=False):
    while True:
        jawab = input(teks).strip()
        if jawab or not wajib:
            return jawab
        print("Tidak boleh kosong.")


def tanya_angka(teks):
    while True:
        jawab = input(teks).strip().replace(".", "").replace(",", "")
        try:
            nilai = int(jawab)
        except ValueError:
            print("Masukkan angka, contoh: 500000.")
            continue
        if nilai <= 0:
            print("Jumlah harus lebih dari nol.")
            continue
        return nilai


def tanya_tanggal(teks, boleh_kosong=True):
    while True:
        jawab = input(teks).strip()
        if not jawab and boleh_kosong:
            return None
        try:
            return parse_tanggal(jawab)
        except ValueError as galat:
            print(galat)


def menu_interaktif():
    print("=== Pencatat Utang & Piutang ===")
    print("Ketik nomor menu, atau 0 untuk keluar.")
    while True:
        print()
        print("1. Tambah utang (kita berutang)")
        print("2. Tambah piutang (orang berutang ke kita)")
        print("3. Lihat daftar")
        print("4. Bayar / terima pembayaran")
        print("5. Ringkasan total")
        print("6. Cek jatuh tempo")
        print("7. Lihat detail catatan")
        print("8. Hapus catatan")
        print("0. Keluar")
        pilih = input("Pilih: ").strip()
        if pilih == "0":
            print("Sampai jumpa.")
            return 0
        if pilih in ("1", "2"):
            jenis = "utang" if pilih == "1" else "piutang"
            nama = tanya("Nama orang: ", wajib=True)
            jumlah = tanya_angka("Jumlah (Rp): ")
            jatuh = tanya_tanggal(
                "Jatuh tempo (YYYY-MM-DD, kosong bila tidak ada): "
            )
            catatan = tanya("Catatan (opsional): ")
            tambah(jenis, nama, jumlah, jatuh_tempo=jatuh, catatan=catatan)
        elif pilih == "3":
            daftar(status="semua")
        elif pilih == "4":
            daftar(status="aktif")
            try:
                nomor = int(input("ID catatan: ").strip())
            except ValueError:
                print("ID harus angka.")
                continue
            jumlah = tanya_angka("Jumlah dibayar/diterima (Rp): ")
            bayar(nomor, jumlah)
        elif pilih == "5":
            total()
        elif pilih == "6":
            jatuh_tempo()
        elif pilih == "7":
            try:
                nomor = int(input("ID catatan: ").strip())
            except ValueError:
                print("ID harus angka.")
                continue
            detail(nomor)
        elif pilih == "8":
            try:
                nomor = int(input("ID catatan: ").strip())
            except ValueError:
                print("ID harus angka.")
                continue
            hapus(nomor)
        else:
            print("Pilihan tidak dikenal.")
    return 0


def utama(argv=None):
    parser = argparse.ArgumentParser(
        description="Pencatat Utang & Piutang di terminal."
    )
    sub = parser.add_subparsers(dest="perintah")

    p_tambah = sub.add_parser("tambah", help="Tambah catatan utang/piutang.")
    p_tambah.add_argument("jenis", choices=["utang", "piutang"])
    p_tambah.add_argument("nama")
    p_tambah.add_argument("jumlah", type=int)
    p_tambah.add_argument("--tanggal")
    p_tambah.add_argument("--jatuh-tempo")
    p_tambah.add_argument("--catatan", default="")

    p_daftar = sub.add_parser("daftar", help="Lihat daftar catatan.")
    p_daftar.add_argument("--jenis", choices=["utang", "piutang"])
    p_daftar.add_argument(
        "--status", choices=["aktif", "lunas", "semua"], default="aktif"
    )
    p_daftar.add_argument("--nama")

    p_bayar = sub.add_parser("bayar", help="Bayar utang / terima piutang.")
    p_bayar.add_argument("id", type=int)
    p_bayar.add_argument("jumlah", type=int)
    p_bayar.add_argument("--tanggal")

    sub.add_parser("total", help="Ringkasan total utang, piutang, posisi bersih.")

    p_jatuh = sub.add_parser("jatuh-tempo", help="Cek yang jatuh tempo.")
    p_jatuh.add_argument("--hari", type=int, default=7)

    p_detail = sub.add_parser("detail", help="Lihat detail satu catatan.")
    p_detail.add_argument("id", type=int)

    p_hapus = sub.add_parser("hapus", help="Hapus satu catatan.")
    p_hapus.add_argument("id", type=int)
    p_hapus.add_argument("--ya", action="store_true")

    args = parser.parse_args(argv)
    if args.perintah is None:
        return menu_interaktif()
    try:
        if args.perintah == "tambah":
            return tambah(
                args.jenis,
                args.nama,
                args.jumlah,
                tanggal=parse_tanggal(args.tanggal, "tanggal"),
                jatuh_tempo=parse_tanggal(args.jatuh_tempo, "jatuh tempo"),
                catatan=args.catatan,
            )
        if args.perintah == "daftar":
            return daftar(args.jenis, args.status, args.nama)
        if args.perintah == "bayar":
            return bayar(
                args.id,
                args.jumlah,
                tanggal=parse_tanggal(args.tanggal, "tanggal"),
            )
        if args.perintah == "total":
            return total()
        if args.perintah == "jatuh-tempo":
            if args.hari < 0:
                print("Jumlah hari tidak boleh negatif.")
                return 1
            return jatuh_tempo(args.hari)
        if args.perintah == "detail":
            return detail(args.id)
        if args.perintah == "hapus":
            return hapus(args.id, ya=args.ya)
    except ValueError as galat:
        print(galat)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(utama())
