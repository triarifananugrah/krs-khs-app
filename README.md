```markdown
# Sistem Informasi KRS & KHS Mahasiswa
### Projek Pemrograman Framework 2 — Universitas Muhammadiyah Palu
**Dosen Pengampu:** Nursalim, S.Kom., M.Kom.

Aplikasi manajemen akademik kampus sederhana berbasis Python + MySQL menggunakan arsitektur **Model-View-Controller (MVC)** yang dilengkapi dengan fitur export dokumen ke dalam format PDF.

---

## Struktur File & Folder

```text
krs_khs_app/
├── database/        # File SQL (Struktur tabel & basis data)
├── config/          # Konfigurasi koneksi database MySQL
├── models/          # Logika Query database (Komponen Model - MVC)
├── controllers/     # Logika bisnis & alur aplikasi (Komponen Controller - MVC)
├── views/           # Tampilan antarmuka aplikasi (Komponen View - MVC)
├── reports/         # Generator modul pembuatan dokumen PDF
├── laporan/         # Folder otomatis untuk menampung output file PDF
├── requirements.txt # Daftar library Python yang wajib di-install
└── main.py          # File utama untuk menjalankan aplikasi

```

---

## Struktur Database & Relasi (ERD)

Terdapat relasi antar tabel pada database `dbakademik` sebagai berikut:

* **mahasiswa (1) ──────< krs (N)** *(Satu mahasiswa dapat memprogram banyak mata kuliah)*
* **matakuliah (1) ──────< krs (N)** *(Satu mata kuliah dapat diambil oleh banyak mahasiswa)*
* **mahasiswa (1) ──────< khs (N)** *(Satu mahasiswa memiliki banyak record nilai)*
* **matakuliah (1) ──────< khs (N)** *(Satu mata kuliah memiliki banyak daftar nilai)*

---

## Aturan Konversi Nilai & IP Semester

Sistem secara otomatis akan mengonversi nilai angka mahasiswa ke nilai huruf dan bobot berdasarkan standarisasi berikut:

| Nilai Angka | Nilai Huruf | Bobot | Keterangan |
| --- | --- | --- | --- |
| 85 – 100 | A | 4.00 | Sangat Baik |
| 75 – 84 | B | 3.00 | Baik |
| 65 – 74 | C | 2.00 | Cukup |
| 50 – 64 | D | 1.00 | Kurang |
| 0  – 49 | E | 0.00 | Gagal |

> **Rumus Kalkulasi IP Semester (IPS):**
> IP Semester = Σ(Bobot × SKS) / ΣSKS

---

## Fitur Utama Aplikasi

| Menu | Fitur |
| --- | --- |
| **Dashboard** | Menyajikan statistik ringkas jumlah total mahasiswa, dosen, mata kuliah, serta aktivitas KRS terkini. |
| **Mahasiswa** | CRUD data master mahasiswa lengkap + fitur pencarian (*search*). |
| **Dosen** | CRUD data master dosen lengkap + fitur pencarian (*search*). |
| **Mata Kuliah** | CRUD data master mata kuliah lengkap + fitur pencarian (*search*). |
| **Input KRS** | Proses pengisian dan pengelolaan Kartu Rencana Studi mahasiswa per semester berjalan. |
| **Input Nilai** | Input nilai angka mahasiswa yang otomatis dikonversi menjadi Nilai Huruf dan Bobot Mutu. |
| **Laporan KRS** | Menampilkan info rencana studi dan mengekspor dokumen resmi KRS ke format PDF berdasarkan NIM. |
| **Laporan KHS** | Menampilkan info hasil studi, kalkulasi IP Semester, dan mengekspor dokumen resmi KHS ke format PDF. |

---

## Cara Menjalankan Aplikasi

### 1. Persiapkan Database MySQL

Pastikan MySQL (via XAMPP / Laragon) sudah aktif, lalu import file database akademik yang berada di dalam folder proyek:

```bash
mysql -u root -p < database/dbakademik.sql

```

*(Sesuaikan konfigurasi host, user, dan password MySQL kamu di dalam file `config/db_config.py` jika diperlukan).*

### 2. Instalasi Library Python

Install dependensi library pihak ketiga yang dibutuhkan oleh aplikasi melalui terminal:

```bash
pip install -r requirements.txt

```

### 3. Menjalankan Sistem

Jalankan file utama aplikasi menggunakan Python:

```bash
python main.py

```

---

## Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python 3
* **Database Management:** MySQL
* **Arsitektur Kode:** Model-View-Controller (MVC)
* **Library Eksternal:** Sesuai yang tertera di `requirements.txt` (termasuk PDF Generator)

```

```
