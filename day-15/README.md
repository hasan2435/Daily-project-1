# Day 15 — Daftar Tugas (To-Do List)

Proyek harian ke-15: daftar tugas di terminal dengan prioritas,
tenggat, tag, dan catatan. Tugas bisa ditambah, dilihat, ditandai
selesai, diedit, dihapus, dicari, dan dibersihkan bila sudah selesai.
Program menandai tugas yang sudah lewat tenggat dan menampilkan
ringkasan jumlah tugas aktif, selesai, dan terlambat.

Hanya memakai pustaka standar Python, tanpa pustaka tambahan.

## Cara menjalankan

```bash
cd day-15
python3 todo.py
```

Jalankan tanpa argumen untuk mode interaktif (menu angka).

Langsung dari baris perintah:

```bash
python3 todo.py tambah "Beli tiket kereta" --prioritas tinggi --tenggat 2026-11-20 --tag perjalanan
python3 todo.py tambah "Bayar listrik" --prioritas sedang --tenggat 2026-11-15 --tag rumah --catatan "sebelum jam 5 sore"
python3 todo.py daftar
python3 todo.py daftar --status aktif
python3 todo.py daftar --prioritas tinggi
python3 todo.py daftar --tag rumah
python3 todo.py selesai 1
python3 todo.py selesai 1 --batal
python3 todo.py edit 2 --prioritas rendah
python3 todo.py cari kereta
python3 todo.py ringkasan
python3 todo.py hapus 3 --ya
python3 todo.py bersihkan --ya
```

## Prioritas dan tenggat

Prioritas ada tiga tingkat: `tinggi` (▲), `sedang` (◆), dan `rendah`
(▽); bila tidak diisi, prioritasnya `sedang`. Daftar tugas diurutkan
berdasarkan prioritas, lalu tenggat, lalu nomor ID — tugas selesai
selalu tampil di akhir.

Tenggat ditulis dengan format `YYYY-MM-DD`. Tugas aktif yang
tenggatnya sudah lewat ditandai `TERLAMBAT` beserta jumlah harinya,
tugas bertenggat hari ini ditandai `tenggat HARI INI`, dan tugas
bertenggat besok ditandai `tenggat besok`.

## Perintah

| Perintah | Fungsi |
| --- | --- |
| `tambah "Judul"` | Tambah tugas baru (`--prioritas`, `--tenggat`, `--tag`, `--catatan`). |
| `daftar` | Lihat semua tugas (`--status aktif/selesai/semua`, `--prioritas`, `--tag`). |
| `selesai <id>` | Tandai tugas selesai (`--batal` untuk membatalkan). |
| `edit <id>` | Ubah judul, prioritas, tenggat, tag, atau catatan (`--hapus-tenggat` untuk menghapus tenggat). |
| `hapus <id>` | Hapus satu tugas (`--ya` tanpa konfirmasi). |
| `cari <kata>` | Cari tugas berdasarkan judul, catatan, atau tag. |
| `ringkasan` | Jumlah tugas per status dan prioritas, tugas terlambat, dan prioritas tinggi yang masih aktif. |
| `bersihkan` | Hapus semua tugas yang sudah selesai (`--ya` tanpa konfirmasi). |

## Data tersimpan

Tugas disimpan di berkas `todo.json` pada folder tempat program
dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek,
jadi jangan ikut diunggah ke repositori.
