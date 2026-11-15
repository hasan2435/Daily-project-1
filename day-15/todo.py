#!/usr/bin/env python3
"""Daftar Tugas (To-Do List) di terminal.

Program terminal untuk mencatat tugas harian: tambah tugas dengan
prioritas, tenggat, dan tag; tandai selesai; edit; hapus; cari; dan
lihat ringkasan beserta tugas yang sudah lewat tenggat. Data disimpan
di berkas ``todo.json`` pada folder tempat program dijalankan.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

Cara memakai:

    python3 todo.py
    python3 todo.py tambah "Beli tiket kereta" --prioritas tinggi --tenggat 2026-11-20 --tag perjalanan
    python3 todo.py daftar
    python3 todo.py daftar --status aktif
    python3 todo.py selesai 1
    python3 todo.py edit 2 --prioritas rendah
    python3 todo.py cari kereta
    python3 todo.py ringkasan
    python3 todo.py hapus 3 --ya
    python3 todo.py bersihkan --ya

Jalankan tanpa argumen untuk mode interaktif (menu angka).
"""

import argparse
import json
import os
import sys
from datetime import date, datetime

NAMA_BERKAS = "todo.json"

PRIORITAS = ("tinggi", "sedang", "rendah")
BOBOT_PRIORITAS = {"tinggi": 0, "sedang": 1, "rendah": 2}
IKON_PRIORITAS = {"tinggi": "▲", "sedang": "◆", "rendah": "▽"}


def muat_data():
    """Muat data tugas dari berkas JSON; kembalikan struktur baru bila belum ada."""
    if not os.path.exists(NAMA_BERKAS):
        return {"tugas": [], "id_berikutnya": 1}
    try:
        with open(NAMA_BERKAS, "r", encoding="utf-8") as berkas:
            data = json.load(berkas)
    except (json.JSONDecodeError, OSError) as galat:
        print(f"Berkas {NAMA_BERKAS} rusak atau tidak bisa dibaca: {galat}")
        print("Memakai daftar kosong. Perbaiki atau hapus berkas itu bila datanya penting.")
        return {"tugas": [], "id_berikutnya": 1}
    if not isinstance(data, dict) or "tugas" not in data:
        return {"tugas": [], "id_berikutnya": 1}
    return data


def simpan_data(data):
    """Simpan data tugas ke berkas JSON."""
    try:
        with open(NAMA_BERKAS, "w", encoding="utf-8") as berkas:
            json.dump(data, berkas, ensure_ascii=False, indent=2)
    except OSError as galat:
        print(f"Gagal menyimpan ke {NAMA_BERKAS}: {galat}")
        sys.exit(1)


def parse_tanggal(teks):
    """Ubah teks YYYY-MM-DD menjadi date; kembalikan None bila format salah."""
    try:
        return datetime.strptime(teks, "%Y-%m-%d").date()
    except ValueError:
        return None


def validasi_tenggat(teks):
    """Periksa format tenggat; kembalikan tanggal atau None sambil mencetak pesan."""
    if teks is None:
        return None
    tanggal = parse_tanggal(teks)
    if tanggal is None:
        print(f"Tenggat '{teks}' tidak valid. Pakai format YYYY-MM-DD, contoh 2026-11-20.")
        sys.exit(1)
    return tanggal


def parse_tag(teks):
    """Pecah teks tag dipisah koma menjadi daftar tag yang rapi."""
    if not teks:
        return []
    return [bagian.strip() for bagian in teks.split(",") if bagian.strip()]


def cari_tugas(data, id_tugas):
    """Cari satu tugas berdasarkan ID; kembalikan None bila tidak ada."""
    for tugas in data["tugas"]:
        if tugas["id"] == id_tugas:
            return tugas
    return None


def sudah_lewat(tugas, hari_ini=None):
    """True bila tugas aktif dan tenggatnya sudah lewat hari ini."""
    if tugas["selesai"] or not tugas.get("tenggat"):
        return False
    hari_ini = hari_ini or date.today()
    tanggal = parse_tanggal(tugas["tenggat"])
    return tanggal is not None and tanggal < hari_ini


def urutkan(tugas_list):
    """Urutkan: tugas aktif dulu (prioritas, lalu tenggat, lalu ID), selesai di akhir."""
    def kunci(tugas):
        tenggat = tugas.get("tenggat") or "9999-12-31"
        if tugas["selesai"]:
            return (1, 0, tenggat, tugas["id"])
        return (0, BOBOT_PRIORITAS.get(tugas["prioritas"], 1), tenggat, tugas["id"])
    return sorted(tugas_list, key=kunci)


def format_tugas(tugas, hari_ini=None):
    """Satu baris tampilan tugas."""
    hari_ini = hari_ini or date.today()
    status = "[x]" if tugas["selesai"] else "[ ]"
    ikon = IKON_PRIORITAS.get(tugas["prioritas"], "◆")
    bagian = [f"{tugas['id']:>3}. {status} {ikon} {tugas['judul']}"]
    if tugas.get("tag"):
        bagian.append("[" + ", ".join(tugas["tag"]) + "]")
    if tugas.get("tenggat"):
        tanggal = parse_tanggal(tugas["tenggat"])
        if tanggal is None:
            bagian.append(f"(tenggat {tugas['tenggat']})")
        else:
            selisih = (tanggal - hari_ini).days
            if tugas["selesai"]:
                bagian.append(f"(tenggat {tugas['tenggat']})")
            elif selisih < 0:
                bagian.append(f"(TERLAMBAT {-selisih} hari, tenggat {tugas['tenggat']})")
            elif selisih == 0:
                bagian.append("(tenggat HARI INI)")
            elif selisih == 1:
                bagian.append("(tenggat besok)")
            else:
                bagian.append(f"(tenggat {tugas['tenggat']}, {selisih} hari lagi)")
    if tugas.get("catatan"):
        bagian.append(f"— {tugas['catatan']}")
    if tugas["selesai"] and tugas.get("selesai_pada"):
        bagian.append(f"(selesai {tugas['selesai_pada']})")
    return " ".join(bagian)


def perintah_tambah(args):
    """Tambah satu tugas baru."""
    validasi_tenggat(args.tenggat)
    data = muat_data()
    tugas = {
        "id": data["id_berikutnya"],
        "judul": args.judul.strip(),
        "prioritas": args.prioritas,
        "tenggat": args.tenggat,
        "tag": parse_tag(args.tag),
        "catatan": (args.catatan or "").strip(),
        "selesai": False,
        "dibuat": date.today().isoformat(),
        "selesai_pada": None,
    }
    if not tugas["judul"]:
        print("Judul tugas tidak boleh kosong.")
        sys.exit(1)
    data["tugas"].append(tugas)
    data["id_berikutnya"] += 1
    simpan_data(data)
    print(f"Tugas #{tugas['id']} ditambahkan:")
    print("  " + format_tugas(tugas))


def perintah_daftar(args):
    """Tampilkan daftar tugas sesuai filter."""
    data = muat_data()
    if not data["tugas"]:
        print("Belum ada tugas. Tambah dengan: python3 todo.py tambah \"Judul tugas\"")
        return
    tugas_list = data["tugas"]
    if args.status == "aktif":
        tugas_list = [t for t in tugas_list if not t["selesai"]]
    elif args.status == "selesai":
        tugas_list = [t for t in tugas_list if t["selesai"]]
    if args.prioritas:
        tugas_list = [t for t in tugas_list if t["prioritas"] == args.prioritas]
    if args.tag:
        tugas_list = [t for t in tugas_list if args.tag in t.get("tag", [])]
    if not tugas_list:
        print("Tidak ada tugas yang cocok dengan filter itu.")
        return
    hari_ini = date.today()
    print(f"Daftar tugas ({len(tugas_list)} tugas):")
    for tugas in urutkan(tugas_list):
        print("  " + format_tugas(tugas, hari_ini))
    aktif = sum(1 for t in tugas_list if not t["selesai"])
    terlambat = sum(1 for t in tugas_list if sudah_lewat(t, hari_ini))
    print(f"\nAktif: {aktif} | Selesai: {len(tugas_list) - aktif} | Terlambat: {terlambat}")


def perintah_selesai(args):
    """Tandai tugas selesai, atau batalkan tandanya dengan --batal."""
    data = muat_data()
    tugas = cari_tugas(data, args.id)
    if tugas is None:
        print(f"Tidak ada tugas dengan ID {args.id}.")
        sys.exit(1)
    if args.batal:
        if not tugas["selesai"]:
            print(f"Tugas #{args.id} memang belum selesai.")
            return
        tugas["selesai"] = False
        tugas["selesai_pada"] = None
        simpan_data(data)
        print(f"Tugas #{args.id} dikembalikan ke aktif:")
    else:
        if tugas["selesai"]:
            print(f"Tugas #{args.id} sudah selesai sebelumnya.")
            return
        tugas["selesai"] = True
        tugas["selesai_pada"] = date.today().isoformat()
        simpan_data(data)
        print(f"Tugas #{args.id} selesai. Kerja bagus!")
    print("  " + format_tugas(tugas))


def perintah_hapus(args):
    """Hapus satu tugas berdasarkan ID."""
    data = muat_data()
    tugas = cari_tugas(data, args.id)
    if tugas is None:
        print(f"Tidak ada tugas dengan ID {args.id}.")
        sys.exit(1)
    if not args.ya:
        jawaban = input(f"Hapus tugas #{args.id} \"{tugas['judul']}\"? (y/n): ").strip().lower()
        if jawaban not in ("y", "ya"):
            print("Dibatalkan.")
            return
    data["tugas"] = [t for t in data["tugas"] if t["id"] != args.id]
    simpan_data(data)
    print(f"Tugas #{args.id} \"{tugas['judul']}\" dihapus.")


def perintah_edit(args):
    """Ubah judul, prioritas, tenggat, tag, atau catatan tugas."""
    data = muat_data()
    tugas = cari_tugas(data, args.id)
    if tugas is None:
        print(f"Tidak ada tugas dengan ID {args.id}.")
        sys.exit(1)
    if args.judul is not None:
        if not args.judul.strip():
            print("Judul tugas tidak boleh kosong.")
            sys.exit(1)
        tugas["judul"] = args.judul.strip()
    if args.prioritas is not None:
        tugas["prioritas"] = args.prioritas
    if args.hapus_tenggat:
        tugas["tenggat"] = None
    elif args.tenggat is not None:
        validasi_tenggat(args.tenggat)
        tugas["tenggat"] = args.tenggat
    if args.tag is not None:
        tugas["tag"] = parse_tag(args.tag)
    if args.catatan is not None:
        tugas["catatan"] = args.catatan.strip()
    simpan_data(data)
    print(f"Tugas #{args.id} diperbarui:")
    print("  " + format_tugas(tugas))


def perintah_cari(args):
    """Cari tugas yang judul, catatan, atau tag-nya mengandung kata kunci."""
    data = muat_data()
    kata = args.kata_kunci.lower()
    hasil = [
        t for t in data["tugas"]
        if kata in t["judul"].lower()
        or kata in (t.get("catatan") or "").lower()
        or any(kata in tag.lower() for tag in t.get("tag", []))
    ]
    if not hasil:
        print(f"Tidak ada tugas yang mengandung '{args.kata_kunci}'.")
        return
    print(f"Ditemukan {len(hasil)} tugas untuk '{args.kata_kunci}':")
    for tugas in urutkan(hasil):
        print("  " + format_tugas(tugas))


def perintah_ringkasan(_args):
    """Tampilkan ringkasan: jumlah per status, per prioritas, dan tugas mendesak."""
    data = muat_data()
    tugas_list = data["tugas"]
    hari_ini = date.today()
    if not tugas_list:
        print("Belum ada tugas. Tambah dengan: python3 todo.py tambah \"Judul tugas\"")
        return
    aktif = [t for t in tugas_list if not t["selesai"]]
    selesai = [t for t in tugas_list if t["selesai"]]
    terlambat = [t for t in aktif if sudah_lewat(t, hari_ini)]
    hari_ini_list = [
        t for t in aktif
        if t.get("tenggat") and parse_tanggal(t["tenggat"]) == hari_ini
    ]
    print("Ringkasan tugas:")
    print(f"  Total: {len(tugas_list)} tugas")
    print(f"  Aktif: {len(aktif)} | Selesai: {len(selesai)}")
    for prioritas in PRIORITAS:
        jumlah = sum(1 for t in aktif if t["prioritas"] == prioritas)
        print(f"  Prioritas {prioritas}: {jumlah} aktif")
    print(f"  Terlambat: {len(terlambat)} tugas")
    print(f"  Tenggat hari ini: {len(hari_ini_list)} tugas")
    if terlambat:
        print("\nTugas yang sudah lewat tenggat:")
        for tugas in urutkan(terlambat):
            print("  " + format_tugas(tugas, hari_ini))
    mendesak = [
        t for t in aktif
        if t["prioritas"] == "tinggi" and not sudah_lewat(t, hari_ini)
    ]
    if mendesak:
        print("\nPrioritas tinggi yang masih aktif:")
        for tugas in urutkan(mendesak):
            print("  " + format_tugas(tugas, hari_ini))


def perintah_bersihkan(args):
    """Hapus semua tugas yang sudah selesai."""
    data = muat_data()
    selesai = [t for t in data["tugas"] if t["selesai"]]
    if not selesai:
        print("Tidak ada tugas selesai yang perlu dibersihkan.")
        return
    if not args.ya:
        jawaban = input(
            f"Hapus {len(selesai)} tugas yang sudah selesai? (y/n): "
        ).strip().lower()
        if jawaban not in ("y", "ya"):
            print("Dibatalkan.")
            return
    data["tugas"] = [t for t in data["tugas"] if not t["selesai"]]
    simpan_data(data)
    print(f"{len(selesai)} tugas selesai dihapus. Daftar jadi lebih rapi.")


def tanya(teks, default=""):
    """Minta masukan pengguna; kosong berarti pakai default."""
    jawaban = input(teks).strip()
    return jawaban if jawaban else default


def menu_interaktif():
    """Menu angka untuk pemakaian interaktif."""
    while True:
        print("\n=== Daftar Tugas ===")
        print("1. Tambah tugas")
        print("2. Lihat daftar tugas")
        print("3. Tandai tugas selesai")
        print("4. Edit tugas")
        print("5. Hapus tugas")
        print("6. Cari tugas")
        print("7. Ringkasan")
        print("8. Bersihkan tugas selesai")
        print("0. Keluar")
        pilihan = input("Pilih menu (0-8): ").strip()
        if pilihan == "0":
            print("Sampai jumpa! Semoga semua tugas selesai tepat waktu.")
            return
        if pilihan == "1":
            judul = tanya("Judul tugas: ")
            if not judul:
                print("Judul tidak boleh kosong.")
                continue
            prioritas = tanya("Prioritas (tinggi/sedang/rendah) [sedang]: ", "sedang").lower()
            if prioritas not in PRIORITAS:
                print("Prioritas tidak dikenal, dipakai 'sedang'.")
                prioritas = "sedang"
            tenggat = tanya("Tenggat (YYYY-MM-DD, kosong bila tidak ada): ") or None
            tag = tanya("Tag (pisah koma, kosong bila tidak ada): ")
            catatan = tanya("Catatan (kosong bila tidak ada): ")
            perintah_tambah(argparse.Namespace(
                judul=judul, prioritas=prioritas, tenggat=tenggat,
                tag=tag, catatan=catatan,
            ))
        elif pilihan == "2":
            perintah_daftar(argparse.Namespace(
                status="semua", prioritas=None, tag=None,
            ))
        elif pilihan == "3":
            try:
                id_tugas = int(tanya("ID tugas yang selesai: "))
            except ValueError:
                print("ID harus berupa angka.")
                continue
            perintah_selesai(argparse.Namespace(id=id_tugas, batal=False))
        elif pilihan == "4":
            try:
                id_tugas = int(tanya("ID tugas yang diedit: "))
            except ValueError:
                print("ID harus berupa angka.")
                continue
            data = muat_data()
            tugas = cari_tugas(data, id_tugas)
            if tugas is None:
                print(f"Tidak ada tugas dengan ID {id_tugas}.")
                continue
            print("Isi baru (kosong = tidak diubah):")
            judul = tanya(f"Judul [{tugas['judul']}]: ")
            prioritas = tanya(f"Prioritas [{tugas['prioritas']}]: ").lower()
            tenggat = tanya(f"Tenggat [{tugas.get('tenggat') or '-'}]: ")
            tag = tanya(f"Tag [{', '.join(tugas.get('tag', [])) or '-'}]: ")
            catatan = tanya(f"Catatan [{tugas.get('catatan') or '-'}]: ")
            perintah_edit(argparse.Namespace(
                id=id_tugas,
                judul=judul or None,
                prioritas=prioritas if prioritas in PRIORITAS else None,
                tenggat=tenggat or None,
                hapus_tenggat=False,
                tag=tag if tag else None,
                catatan=catatan if catatan else None,
            ))
        elif pilihan == "5":
            try:
                id_tugas = int(tanya("ID tugas yang dihapus: "))
            except ValueError:
                print("ID harus berupa angka.")
                continue
            perintah_hapus(argparse.Namespace(id=id_tugas, ya=False))
        elif pilihan == "6":
            kata = tanya("Kata kunci: ")
            if kata:
                perintah_cari(argparse.Namespace(kata_kunci=kata))
        elif pilihan == "7":
            perintah_ringkasan(argparse.Namespace())
        elif pilihan == "8":
            perintah_bersihkan(argparse.Namespace(ya=False))
        else:
            print("Pilihan tidak dikenal, coba lagi.")


def main(argv=None):
    """Titik masuk program."""
    parser = argparse.ArgumentParser(
        description="Daftar Tugas (To-Do List) di terminal.",
    )
    sub = parser.add_subparsers(dest="perintah")

    p_tambah = sub.add_parser("tambah", help="Tambah tugas baru.")
    p_tambah.add_argument("judul", help="Judul tugas.")
    p_tambah.add_argument("--prioritas", choices=list(PRIORITAS), default="sedang",
                          help="Prioritas tugas (default: sedang).")
    p_tambah.add_argument("--tenggat", help="Tenggat format YYYY-MM-DD.")
    p_tambah.add_argument("--tag", help="Tag dipisah koma, contoh: kerja,rumah.")
    p_tambah.add_argument("--catatan", help="Catatan tambahan untuk tugas.")
    p_tambah.set_defaults(func=perintah_tambah)

    p_daftar = sub.add_parser("daftar", help="Lihat daftar tugas.")
    p_daftar.add_argument("--status", choices=["semua", "aktif", "selesai"],
                          default="semua", help="Filter status (default: semua).")
    p_daftar.add_argument("--prioritas", choices=list(PRIORITAS),
                          help="Filter prioritas.")
    p_daftar.add_argument("--tag", help="Filter tag.")
    p_daftar.set_defaults(func=perintah_daftar)

    p_selesai = sub.add_parser("selesai", help="Tandai tugas selesai.")
    p_selesai.add_argument("id", type=int, help="ID tugas.")
    p_selesai.add_argument("--batal", action="store_true",
                           help="Batalkan tanda selesai.")
    p_selesai.set_defaults(func=perintah_selesai)

    p_hapus = sub.add_parser("hapus", help="Hapus satu tugas.")
    p_hapus.add_argument("id", type=int, help="ID tugas.")
    p_hapus.add_argument("--ya", action="store_true",
                         help="Hapus tanpa konfirmasi.")
    p_hapus.set_defaults(func=perintah_hapus)

    p_edit = sub.add_parser("edit", help="Ubah tugas yang sudah ada.")
    p_edit.add_argument("id", type=int, help="ID tugas.")
    p_edit.add_argument("--judul", help="Judul baru.")
    p_edit.add_argument("--prioritas", choices=list(PRIORITAS), help="Prioritas baru.")
    p_edit.add_argument("--tenggat", help="Tenggat baru format YYYY-MM-DD.")
    p_edit.add_argument("--hapus-tenggat", action="store_true",
                        help="Hapus tenggat tugas.")
    p_edit.add_argument("--tag", help="Tag baru dipisah koma.")
    p_edit.add_argument("--catatan", help="Catatan baru.")
    p_edit.set_defaults(func=perintah_edit)

    p_cari = sub.add_parser("cari", help="Cari tugas berdasarkan kata kunci.")
    p_cari.add_argument("kata_kunci", help="Kata kunci pencarian.")
    p_cari.set_defaults(func=perintah_cari)

    p_ringkasan = sub.add_parser("ringkasan", help="Tampilkan ringkasan tugas.")
    p_ringkasan.set_defaults(func=perintah_ringkasan)

    p_bersihkan = sub.add_parser("bersihkan", help="Hapus semua tugas yang sudah selesai.")
    p_bersihkan.add_argument("--ya", action="store_true",
                             help="Hapus tanpa konfirmasi.")
    p_bersihkan.set_defaults(func=perintah_bersihkan)

    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        menu_interaktif()
        return
    args.func(args)


if __name__ == "__main__":
    main()
