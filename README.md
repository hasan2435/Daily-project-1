# Daily Project 1

Seri ini: satu proyek kecil baru setiap hari, bebas topik, yang penting konsisten upload.
Semua proyek memakai Python standar saja, tanpa library tambahan, dan bisa dijalankan di terminal/VSCode.

## Daftar proyek

- Day 1 — Pomodoro Timer: timer Pomodoro di terminal (`pomodoro.py`).
- Day 2 — Pencatat Pengeluaran Harian: catat pengeluaran dan lihat totalnya (`day-02/pengeluaran.py`).
- Day 3 — Penghitung Kata dan Waktu Baca: analisis teks, hitung kata dan perkiraan waktu baca (`day-03/kata.py`).
- Day 4 — Generator Kata Sandi Aman: buat kata sandi acak yang kuat dan nilai kekuatannya (`day-04/password.py`).
- Day 5 — Kalkulator Tanggal: selisih tanggal, geser hari, nama hari, dan hitung menuju ulang tahun (`day-05/tanggal.py`).
- Day 6 — Kalkulator Bunga Majemuk: simulasi tabungan dengan bunga majemuk, hitung nilai akhir, lama menuju target, dan setoran bulanan (`day-06/bunga.py`).
- Day 7 — Permainan Tebak Kata: tebak kata Bahasa Indonesia huruf demi huruf, 6 kategori dan 3 tingkat kesulitan (`day-07/tebak.py`).

- Day 8 — Konverter Satuan: ubah satuan panjang, berat, volume, suhu, waktu, kecepatan, dan data (`day-08/konversi.py`).

- Day 9 — Kalkulator BMI & Kalori Harian: hitung BMI, BMR, TDEE, dan target kalori harian (`day-09/bmi.py`).

- Day 10 — Pencatat Kebiasaan Harian: catat kebiasaan, centang harian, streak, dan ringkasan 7 hari terakhir (`day-10/kebiasaan.py`).

- Day 11 — Kalkulator Waktu Tidur: hitung jam tidur dan jam bangun ideal dari siklus tidur 90 menit (`day-11/tidur.py`).

- Day 12 — Pembagi Tagihan: bagi tagihan makan bersama secara rata, per item pesanan, atau menurut persen, dengan service charge, tip, dan pembulatan (`day-12/tagihan.py`).

- Day 13 — Kalkulator IPK & Nilai Kuliah: hitung IPK tertimbang SKS dari nilai huruf atau angka 0-100, lengkap dengan predikat dan target IPK semester depan (`day-13/ipk.py`).

- Day 14 — Kuis Pengetahuan Umum: kuis pilihan ganda Bahasa Indonesia, 5 kategori dan 40 soal, soal dan pilihan diacak, skor terbaik tersimpan (`day-14/kuis.py`).

- Day 15 — Daftar Tugas (To-Do List): catat tugas dengan prioritas, tenggat, tag, dan catatan; tandai selesai dan pantau tugas yang terlambat (`day-15/todo.py`).

- Day 16 — Pencatat Buku Bacaan: catat buku yang dibaca, pantau progres halaman, tandai selesai, dan lihat statistik bacaan (`day-16/buku.py`).

- Day 17 — Kalkulator Pajak Penghasilan (PPh 21): hitung PPh 21 tahunan dan bulanan karyawan dari gaji, tunjangan, dan bonus, lengkap dengan PTKP, biaya jabatan, dan tarif progresif (`day-17/pajak.py`).

- Day 18 — Kalkulator Cicilan Kredit: hitung cicilan bulanan pinjaman (anuitas), tabel amortisasi, simulasi pelunasan dipercepat, dan bandingkan dua penawaran kredit (`day-18/cicilan.py`).

- Day 19 — Kalkulator Zakat: hitung zakat penghasilan, zakat mal (emas, perak, tabungan, dagang), dan zakat fitrah, lengkap dengan nisab (`day-19/zakat.py`).

- Day 20 — Kalkulator Diskon & Promo Belanja: hitung harga akhir belanja — diskon persen, diskon bertingkat, potongan nominal, PPN, cashback, dan banding dua promo (`day-20/diskon.py`).

- Day 21 — Permainan Sudoku di Terminal: buat teka-teki Sudoku baru dengan solusi unik, mainkan di terminal, atau selesaikan teka-teki dari luar (`day-21/sudoku.py`).

- Day 22 — Pencatat Utang & Piutang: catat utang dan piutang per orang, bayar bertahap sampai lunas, pantau jatuh tempo, dan lihat posisi bersih (`day-22/utang.py`).

- Day 23 — Kalkulator Biaya Listrik: hitung biaya listrik per alat dan tagihan bulanan dari golongan tarif PLN, lengkap dengan rekening minimum dan simulasi hemat (`day-23/listrik.py`).

## Day 1 — Pomodoro Timer

Proyek harian ke-1: timer Pomodoro di terminal.

```bash
python3 pomodoro.py
python3 pomodoro.py 15 3
```

Default: 25 menit fokus, 5 menit istirahat, 4 putaran.
Tekan Ctrl+C untuk berhenti.

## Day 2 — Pencatat Pengeluaran Harian

Proyek harian ke-2: program terminal untuk mencatat pengeluaran dan melihat totalnya, baik total keseluruhan maupun per kategori.

```bash
cd day-02
python3 pengeluaran.py
python3 pengeluaran.py tambah 50000 makan "Makan siang"
python3 pengeluaran.py daftar
python3 pengeluaran.py total
```

Data disimpan di berkas `pengeluaran.json` pada folder tempat program dijalankan. Berkas data itu milik pengguna, bukan bagian dari proyek, jadi jangan ikut diunggah ke repositori.
Detail lengkap ada di `day-02/README.md`.

## Day 3 — Penghitung Kata dan Waktu Baca

Proyek harian ke-3: program terminal untuk menganalisis sebuah teks:
jumlah karakter, kata, kalimat, dan paragraf, rata-rata panjang kata,
perkiraan waktu baca (200 kata/menit), serta 10 kata paling sering muncul.

```bash
cd day-03
python3 kata.py
python3 kata.py artikel.txt
python3 kata.py --teks "Belajar setiap hari, sedikit demi sedikit, tapi konsisten."
```

Jalankan tanpa argumen untuk mode interaktif.
Detail lengkap ada di `day-03/README.md`.

## Day 4 — Generator Kata Sandi Aman

Proyek harian ke-4: program terminal untuk membuat kata sandi acak
yang kuat (modul `secrets` dari pustaka standar Python) dan menilai
kekuatan kata sandi yang sudah ada dengan skor 0–100.

```bash
cd day-04
python3 password.py
python3 password.py --panjang 20 --jumlah 5
python3 password.py --nilai "KataSandi123!"
```

Secara default program membuat 1 kata sandi sepanjang 16 karakter.
Detail lengkap ada di `day-04/README.md`.

## Day 5 — Kalkulator Tanggal

Proyek harian ke-5: program terminal untuk menghitung selisih dua
tanggal (termasuk jumlah hari kerja Senin-Jumat), menggeser tanggal
maju/mundur sejumlah hari, mencari nama hari dari tanggal, dan
menghitung usia serta hari menuju ulang tahun berikut.

```bash
cd day-05
python3 tanggal.py
python3 tanggal.py selisih 2026-11-05 2026-12-25
python3 tanggal.py tambah 2026-11-05 10 --kerja
python3 tanggal.py hari 2026-11-05
python3 tanggal.py ultah 2000-01-15
```

Jalankan tanpa argumen untuk mode interaktif.
Detail lengkap ada di `day-05/README.md`.

## Day 6 — Kalkulator Bunga Majemuk

Proyek harian ke-6: program terminal untuk mensimulasikan pertumbuhan
tabungan dengan bunga majemuk dan setoran rutin bulanan: hitung nilai
akhir, lama menuju target dana, setoran bulanan yang dibutuhkan, dan
tabel pertumbuhan tahunan.

```bash
cd day-06
python3 bunga.py
python3 bunga.py tumbuh --pokok 1000000 --bunga 6 --tahun 5 --setoran 500000
python3 bunga.py target --pokok 1000000 --bunga 6 --setoran 500000 --target 50000000
python3 bunga.py setoran --pokok 1000000 --bunga 6 --tahun 5 --target 50000000
python3 bunga.py tabel --pokok 1000000 --bunga 6 --tahun 5 --setoran 500000
```

Jalankan tanpa argumen untuk mode interaktif. Bunga dihitung majemuk
per bulan, setoran masuk di akhir bulan.
Detail lengkap ada di `day-06/README.md`.

## Day 7 — Permainan Tebak Kata

Proyek harian ke-7: permainan tebak kata di terminal. Tebak kata Bahasa
Indonesia huruf demi huruf sebelum gambar orang-orangan selesai. Ada
6 kategori kata (hewan, buah, kota, benda, makanan, profesi) dan
3 tingkat kesulitan yang mengatur panjang kata dan jumlah nyawa.

```bash
cd day-07
python3 tebak.py
python3 tebak.py --kategori hewan --kesulitan sulit
python3 tebak.py --kata kucing
python3 tebak.py --daftar
```

Jalankan tanpa argumen untuk mode interaktif. Menebak kata utuh yang
salah mengurangi 2 nyawa. Detail lengkap ada di `day-07/README.md`.


## Day 8 — Konverter Satuan

Proyek harian ke-8: program terminal untuk mengubah satuan dalam 7
kategori: panjang, berat, volume, suhu, waktu, kecepatan, dan data.
Suhu dihitung lewat Celsius, termasuk Reamur; data memakai kelipatan
1024, dari bit sampai TB.

```bash
cd day-08
python3 konversi.py
python3 konversi.py panjang 5 km m
python3 konversi.py suhu 100 C F
python3 konversi.py berat 2.5 kg ons
python3 konversi.py data 1 GB MB
python3 konversi.py --daftar
```

Jalankan tanpa argumen untuk mode interaktif. Detail lengkap ada di
`day-08/README.md`.

## Day 9 — Kalkulator BMI & Kalori Harian

Proyek harian ke-9: program terminal untuk menghitung BMI beserta
kategorinya dan rentang berat badan ideal, lalu kebutuhan kalori:
BMR dengan rumus Mifflin-St Jeor, TDEE berdasarkan tingkat aktivitas,
dan target kalori untuk menurunkan, mempertahankan, atau menaikkan
berat badan sekitar 0,5 kg per minggu.

```bash
cd day-09
python3 bmi.py
python3 bmi.py bmi 70 170
python3 bmi.py kalori 70 170 30 pria sedang
python3 bmi.py kalori 55 160 25 wanita ringan --tujuan turun
python3 bmi.py --daftar
```

Jalankan tanpa argumen untuk mode interaktif. Detail lengkap ada di
`day-09/README.md`.

## Day 10 — Pencatat Kebiasaan Harian

Proyek harian ke-10: program terminal untuk mencatat kebiasaan yang
ingin dibangun setiap hari: tambah kebiasaan dengan target mingguan,
centang bila sudah dilakukan, dan pantau streak (rangkaian hari
beruntun) beserta ringkasan 7 hari terakhir.

```bash
cd day-10
python3 kebiasaan.py
python3 kebiasaan.py tambah "Olahraga pagi" --target 5
python3 kebiasaan.py centang "Olahraga pagi"
python3 kebiasaan.py daftar
python3 kebiasaan.py ringkasan
```

Jalankan tanpa argumen untuk mode interaktif. Data disimpan di
`kebiasaan.json` pada folder tempat program dijalankan; berkas data
itu milik pengguna, bukan bagian dari proyek. Detail lengkap ada di
`day-10/README.md`.

## Day 11 — Kalkulator Waktu Tidur

Proyek harian ke-11: program terminal untuk menghitung jam tidur dan
jam bangun yang ideal berdasarkan siklus tidur 90 menit. Satu siklus
tidur berlangsung sekitar 90 menit; orang dewasa umumnya butuh 5-6
siklus (7,5-9 jam) per malam. Program menghitung mundur dari jam
bangun yang diinginkan atau maju dari jam tidur, dengan
memperhitungkan waktu yang dibutuhkan untuk tertidur (default
15 menit).

```bash
cd day-11
python3 tidur.py
python3 tidur.py bangun 06:00
python3 tidur.py tidur 23:00
python3 tidur.py sekarang
python3 tidur.py durasi 23:00 06:00
```

Jalankan tanpa argumen untuk mode interaktif. Opsi `--tertidur`
mengatur waktu yang dibutuhkan untuk tertidur (0-60 menit, default
15). Detail lengkap ada di `day-11/README.md`.

## Day 12 — Pembagi Tagihan

Proyek harian ke-12: program terminal untuk membagi tagihan makan
bersama dengan adil: bagi rata, bagi per item pesanan, atau bagi
menurut persentase yang disepakati. Bisa ditambah service charge dan
tip (tip dihitung dari total awal + service charge), serta
membulatkan bagian tiap orang ke kelipatan tertentu supaya mudah
ditransfer.

```bash
cd day-12
python3 tagihan.py
python3 tagihan.py rata 300000 3 --service 10 --tip 5
python3 tagihan.py rata 275000 4 --bulat 1000
python3 tagihan.py persen 400000 --bagi "Ani=50, Budi=30, Cici=20"
python3 tagihan.py item
```

Jalankan tanpa argumen untuk mode interaktif. Detail lengkap ada di
`day-12/README.md`.

## Day 13 — Kalkulator IPK & Nilai Kuliah

Proyek harian ke-13: program terminal untuk menghitung IPK dari mata
kuliah yang diambil: tiap mata kuliah punya jumlah SKS dan nilai huruf
(A sampai E) atau angka 0-100 yang otomatis dikonversi ke huruf.
IPK dihitung tertimbang SKS, lengkap dengan predikat kelulusan dan
perhitungan IPK semester depan yang dibutuhkan untuk mencapai target
IPK kumulatif.

```bash
cd day-13
python3 ipk.py
python3 ipk.py tambah "Matematika Diskrit" 3 A
python3 ipk.py tambah "Fisika Dasar" 2 85
python3 ipk.py daftar
python3 ipk.py ipk
python3 ipk.py target 3.5 20
python3 ipk.py konversi 82
```

Jalankan tanpa argumen untuk mode interaktif. Data disimpan di
`ipk.json` pada folder tempat program dijalankan; berkas data itu
milik pengguna, bukan bagian dari proyek. Skala konversi angka ke
huruf: A 85-100, AB 80-84, B 75-79, BC 70-74, C 60-69, D 50-59,
E 0-49 (cek aturan kampusmu, skala tiap kampus bisa berbeda).
Detail lengkap ada di `day-13/README.md`.

## Day 14 — Kuis Pengetahuan Umum

Proyek harian ke-14: kuis pilihan ganda Bahasa Indonesia di terminal.
Ada 5 kategori — pengetahuan umum, sains, sejarah, geografi, dan
olahraga — masing-masing 8 soal, total 40 soal. Soal dan urutan
pilihan jawaban diacak setiap permainan, tiap jawaban langsung
diberi penjelasan singkat, dan skor terbaik per kategori disimpan
supaya bisa dipecahkan di permainan berikutnya.

```bash
cd day-14
python3 kuis.py
python3 kuis.py --kategori sains --jumlah 5
python3 kuis.py --kategori campuran --jumlah 10
python3 kuis.py --daftar
python3 kuis.py skor
```

Jalankan tanpa argumen untuk mode interaktif. Tiap jawaban benar
bernilai 10 poin; predikat dihitung dari persentase jawaban benar.
Skor terbaik disimpan di `kuis.json` pada folder tempat program
dijalankan; berkas data itu milik pengguna, bukan bagian dari
proyek. Detail lengkap ada di `day-14/README.md`.

## Day 15 — Daftar Tugas (To-Do List)

Proyek harian ke-15: daftar tugas di terminal dengan prioritas,
tenggat, tag, dan catatan. Tugas bisa ditambah, dilihat, ditandai
selesai, diedit, dihapus, dicari, dan dibersihkan bila sudah selesai.
Program menandai tugas yang sudah lewat tenggat dan menampilkan
ringkasan jumlah tugas aktif, selesai, dan terlambat.

```bash
cd day-15
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
```

Jalankan tanpa argumen untuk mode interaktif (menu angka). Prioritas
ada tiga tingkat: tinggi, sedang (default), dan rendah. Tugas
disimpan di `todo.json` pada folder tempat program dijalankan; berkas
data itu milik pengguna, bukan bagian dari proyek. Detail lengkap ada
di `day-15/README.md`.

## Day 16 — Pencatat Buku Bacaan

Proyek harian ke-16: pencatat buku bacaan di terminal. Tambah buku
dengan judul, penulis, total halaman, dan genre; catat halaman yang
sudah dibaca setiap hari; pantau progres tiap buku dengan bar progres;
tandai buku selesai; dan lihat statistik bacaan — total buku, halaman
yang sudah dibaca, rata-rata halaman buku selesai, dan genre terbanyak.

```bash
cd day-16
python3 buku.py
python3 buku.py tambah "Laskar Pelangi" "Andrea Hirata" 529 --genre novel
python3 buku.py baca 1 120
python3 buku.py daftar
python3 buku.py daftar --status aktif
python3 buku.py selesai 1
python3 buku.py statistik
python3 buku.py hapus 2 --ya
```

Jalankan tanpa argumen untuk mode interaktif (menu angka). Perintah
`baca` menambah halaman yang dibaca; begitu mencapai total halaman,
buku otomatis ditandai selesai beserta tanggalnya. Buku disimpan di
`buku.json` pada folder tempat program dijalankan; berkas data itu
milik pengguna, bukan bagian dari proyek. Detail lengkap ada di
`day-16/README.md`.

## Day 17 — Kalkulator Pajak Penghasilan (PPh 21)

Proyek harian ke-17: kalkulator PPh 21 karyawan di terminal. Hitung
pajak dari gaji pokok, tunjangan tetap, dan bonus/THR; lengkap dengan
biaya jabatan, iuran pensiun, PTKP sesuai status, dan tarif progresif
Pasal 17, beserta gaji bersih yang diterima tiap bulan.

```bash
cd day-17
python3 pajak.py
python3 pajak.py cepat 10000000
python3 pajak.py cepat 20000000 --status K/1 --bonus 20000000
python3 pajak.py cepat 10000000 --tanpa-npwp
python3 pajak.py ptkp
python3 pajak.py tarif
```

Jalankan tanpa argumen untuk mode interaktif. Tarif dan PTKP
mengikuti UU HPP; cek aturan terbaru sebelum dipakai untuk pelaporan.
Detail lengkap ada di `day-17/README.md`.

## Day 18 — Kalkulator Cicilan Kredit

Proyek harian ke-18: kalkulator cicilan kredit (KPR, kredit kendaraan,
pinjaman pribadi) di terminal. Hitung cicilan bulanan tetap dengan
sistem anuitas (bunga efektif), lihat tabel amortisasi, simulasikan
pelunasan dipercepat dengan setoran ekstra, bandingkan dua penawaran
kredit, dan bandingkan bunga flat dengan anuitas.

```bash
cd day-18
python3 cicilan.py
python3 cicilan.py hitung 100000000 12 12
python3 cicilan.py tabel 100000000 12 12
python3 cicilan.py lunas 100000000 12 12 2000000
python3 cicilan.py banding 100000000 10 12 12 24
python3 cicilan.py flat 100000000 12 12
```

Jalankan tanpa argumen untuk mode interaktif. Pinjaman Rp100 jt,
bunga 12%/tahun, tenor 12 bulan: cicilan Rp8.884.879/bulan, total
bunga Rp6.618.546; tambah setoran Rp2 jt/bulan, lunas 2 bulan lebih
cepat dan hemat bunga Rp1.187.461. Detail lengkap ada di
`day-18/README.md`.

## Day 19 — Kalkulator Zakat

Proyek harian ke-19: kalkulator zakat di terminal. Hitung zakat
penghasilan bulanan dari gaji, zakat mal dari total harta (emas,
perak, tabungan, atau dagang) yang sudah mencapai nisab dan haul
satu tahun, serta zakat fitrah 2,5 kg beras per jiwa. Nisab dihitung
dari harga emas per gram yang bisa diubah lewat opsi `--harga-emas`.

```bash
cd day-19
python3 zakat.py
python3 zakat.py penghasilan 12000000
python3 zakat.py penghasilan 15000000 --harga-emas 1600000
python3 zakat.py mal 200000000
python3 zakat.py emas 100
python3 zakat.py perak 700
python3 zakat.py fitrah 4
python3 zakat.py fitrah 4 --harga-beras 16000
python3 zakat.py nisab
```

Jalankan tanpa argumen untuk mode interaktif. Zakat penghasilan dan
zakat mal sebesar 2,5% bila sudah mencapai nisab (85 gram emas);
zakat fitrah 2,5 kg beras per jiwa. Harga emas default
Rp1.500.000/gram dan harga beras default Rp15.000/kg — ubah sesuai
harga saat ini. Detail lengkap ada di `day-19/README.md`.

## Day 20 — Kalkulator Diskon & Promo Belanja

Proyek harian ke-20: program terminal untuk menghitung harga akhir
belanja — diskon persen tunggal, diskon bertingkat, potongan nominal,
total bayar dengan PPN dan cashback, sampai membandingkan dua promo.

```bash
cd day-20
python3 diskon.py
python3 diskon.py diskon 250000 30
python3 diskon.py bertingkat 250000 50 20
python3 diskon.py potong 250000 50000
python3 diskon.py total 250000 --diskon 30 --ppn 11 --cashback 10000
python3 diskon.py banding 250000 "30%" "50%+20%"
python3 diskon.py hemat 250000 30
```

Jalankan tanpa argumen untuk mode interaktif. Diskon bertingkat
dihitung tahap demi tahap: harga Rp250.000 diskon 50% lalu 20%
menjadi Rp100.000, bukan Rp75.000. Promo bisa digabung, misal
`"20%+50000"`. Detail lengkap ada di `day-20/README.md`.
## Day 21 — Permainan Sudoku di Terminal

Proyek harian ke-21: permainan Sudoku di terminal. Buat teka-teki
baru yang dijamin punya tepat satu solusi, mainkan langsung dengan
petunjuk dan batas kesalahan, atau selesaikan teka-teki dari luar.

```bash
cd day-21
python3 sudoku.py
python3 sudoku.py main --kesulitan sedang
python3 sudoku.py buat --kesulitan sulit
python3 sudoku.py buat --kesulitan mudah --solusi
python3 sudoku.py selesaikan 530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

Jalankan tanpa argumen untuk mode interaktif. Ada tiga tingkat
kesulitan (mudah 36 petunjuk, sedang 30, sulit 25), maksimal 3
petunjuk dan 3 kali salah isi per permainan. Detail lengkap ada di
`day-21/README.md`.

## Day 22 — Pencatat Utang & Piutang

Proyek harian ke-22: pencatat utang dan piutang di terminal. Catat
utang (kita berutang) dan piutang (orang berutang ke kita) per orang
dengan tanggal jatuh tempo, bayar atau terima pembayaran secara
bertahap sampai lunas, dan pantau mana yang sudah lewat jatuh tempo.

```bash
cd day-22
python3 utang.py
python3 utang.py tambah utang Budi 500000 --jatuh-tempo 2026-12-22
python3 utang.py tambah piutang Ani 250000 --catatan "Talang tiket"
python3 utang.py daftar
python3 utang.py bayar 1 200000
python3 utang.py total
python3 utang.py jatuh-tempo
python3 utang.py detail 1
```

Jalankan tanpa argumen untuk mode interaktif. Data disimpan di
`utang.json` pada folder tempat program dijalankan; berkas data itu
milik pengguna, bukan bagian dari proyek. Detail lengkap ada di
`day-22/README.md`.

## Day 23 — Kalkulator Biaya Listrik

Proyek harian ke-23: kalkulator biaya listrik di terminal. Catat
alat-alat di rumah beserta daya dan jam nyalanya, lalu hitung
berapa kWh dan rupiah yang dihabiskan tiap alat dan berapa
perkiraan tagihan bulanannya dari golongan tarif rumah tangga
PLN, lengkap dengan rekening minimum pascabayar dan simulasi
hemat bila jam nyala dikurangi.

```bash
cd day-23
python3 listrik.py
python3 listrik.py golongan
python3 listrik.py hitung 150 24
python3 listrik.py tambah "Kulkas" 150 24
python3 listrik.py tambah "AC 1 PK" 800 8
python3 listrik.py daftar --golongan 1300
python3 listrik.py total
python3 listrik.py total --golongan 2200 --ppj 5
python3 listrik.py total --token
python3 listrik.py hemat 2 4
```

Jalankan tanpa argumen untuk mode interaktif. Contoh: kulkas
150 watt nyala 24 jam sehari menghabiskan 108 kWh/bulan, sekitar
Rp156.028/bulan pada golongan 1300 VA. Data disimpan di
`listrik.json` pada folder tempat program dijalankan; berkas data
itu milik pengguna, bukan bagian dari proyek. Detail lengkap ada
di `day-23/README.md`.
