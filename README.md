```markdown
# Sistem Informasi KRS & KHS Mahasiswa
### Projek Pemrograman Framework 2 — Universitas Muhammadiyah Palu
**Dosen Pengampu:** Nursalim, S.Kom., M.Kom.

Aplikasi manajemen akademik kampus sederhana berbasis Python + MySQL menggunakan arsitektur **Model-View-Controller (MVC)** yang dilengkapi dengan fitur ekspor dokumen otomatis ke dalam format PDF.

---

## Struktur File & Folder

```text
krs_khs_app/
├── database/
│   └── dbakademik.sql       # Struktur skema basis data awal (DDL & DML)
├── config/
│   ├── __init__.py
│   └── db_config.py         # Konfigurasi parameter koneksi driver MySQL
├── models/                  # LAYER MODEL (Query database, manipulasi data & logic SQL)
│   ├── __init__.py
│   ├── dosen_model.py
│   ├── krs_model.py
│   ├── mahasiswa_model.py
│   ├── matakuliah_model.py
│   └── nilai_model.py
├── controllers/             # LAYER CONTROLLER (Jembatan logic bisnis data ke antarmuka)
│   ├── __init__.py
│   ├── controllers.py
│   └── mahasiswa_controller.py
├── views/                   # LAYER VIEW (Komponen GUI / antarmuka visual aplikasi)
│   ├── __init__.py
│   ├── base_view.py
│   ├── dashboard_view.py
│   ├── dosen_view.py
│   ├── krs_view.py
│   ├── laporan_khs_view.py
│   ├── laporan_krs_view.py
│   ├── mahasiswa_view.py
│   ├── matakuliah_view.py
│   └── nilai_view.py
├── reports/
│   ├── __init__.py
│   └── pdf_generator.py     # Engine generator dokumen PDF instan
├── laporan/                 # Direktori berkas cetak output (.pdf) KRS/KHS
├── requirements.txt         # Daftar dependensi & library eksternal Python
└── main.py                  # Entry-point utama untuk menjalankan aplikasi

```

---

## Struktur Database & Skema Tabel

Sistem dibangun menggunakan basis data relasional `dbakademik` dengan skema struktur data sebagai berikut:

### ERD (Entity Relationship Diagram)

```text
mahasiswa (1) ──────< krs (N) >────── (1) matakuliah
mahasiswa (1) ──────< khs (N) >────── (1) matakuliah

```

### 1. Tabel `mahasiswa`

| Kolom | Tipe | Keterangan |
| --- | --- | --- |
| `nim` | VARCHAR(15) | **Primary Key** — Nomor Induk Mahasiswa |
| `nama` | VARCHAR(100) | Nama lengkap mahasiswa |
| `jurusan` | VARCHAR(50) | Program studi / Jurusan |
| `semester` | INT | Semester aktif berjalan |

### 2. Tabel `dosen`

| Kolom | Tipe | Keterangan |
| --- | --- | --- |
| `nidn` | VARCHAR(15) | **Primary Key** — Nomor Induk Dosen Nasional |
| `nama` | VARCHAR(100) | Nama lengkap dosen beserta gelar |
| `prodi` | VARCHAR(50) | Homebase program studi dosen |

### 3. Tabel `matakuliah`

| Kolom | Tipe | Keterangan |
| --- | --- | --- |
| `kode_mk` | VARCHAR(10) | **Primary Key** — Kode unik mata kuliah |
| `nama_mk` | VARCHAR(100) | Nama mata kuliah |
| `sks` | INT | Bobot Satuan Kredit Semester |

### 4. Tabel `krs`

| Kolom | Tipe | Keterangan |
| --- | --- | --- |
| `id_krs` | INT | **Primary Key** — Auto Increment |
| `nim` | VARCHAR(15) | **Foreign Key** → `mahasiswa(nim)` |
| `kode_mk` | VARCHAR(10) | **Foreign Key** → `matakuliah(kode_mk)` |
| `semester_ambil` | INT | Periode semester pengambilan mata kuliah |

### 5. Tabel `khs`

| Kolom | Tipe | Keterangan |
| --- | --- | --- |
| `id_khs` | INT | **Primary Key** — Auto Increment |
| `nim` | VARCHAR(15) | **Foreign Key** → `mahasiswa(nim)` |
| `kode_mk` | VARCHAR(10) | **Foreign Key** → `matakuliah(kode_mk)` |
| `nilai_angka` | DECIMAL(5,2) | Nilai mentah objek angka (0.00 - 100.00) |
| `nilai_huruf` | VARCHAR(2) | Hasil konversi huruf (A / B / C / D / E) |

---

## Implementasi Query SQL Utama

### INSERT (Data Master)

```sql
INSERT INTO mahasiswa (nim, nama, jurusan, semester)
VALUES ('11111', 'Tri Arifan', 'Informatika', 4);

```

### SELECT + JOIN (Multi-Tabel KRS)

```sql
-- Menggabungkan 3 tabel untuk menghasilkan struktur data rencana studi
SELECT k.id_krs, m.nama AS nama_mahasiswa, mk.nama_mk, mk.sks, k.semester_ambil
FROM krs k
JOIN mahasiswa m ON k.nim = m.nim
JOIN matakuliah mk ON k.kode_mk = mk.kode_mk
WHERE m.nim = '11111';

```

### SELECT + WHERE + LIKE (Fitur Pencarian)

```sql
-- Pencarian data dosen secara fleksibel berdasarkan kriteria kata kunci
SELECT * FROM dosen 
WHERE nama LIKE '%Nursalim%' OR nidn LIKE '%1234%';

```

### UPDATE (Data Transaksional Nilai)

```sql
-- Pembaruan record nilai mahasiswa pada mata kuliah tertentu
UPDATE khs
SET nilai_angka = 87.50, nilai_huruf = 'A'
WHERE nim = '11111' AND kode_mk = 'IF201';

```

### Agregat & Kalkulasi IP Semester

```sql
-- Perhitungan total SKS dan rata-rata mutu nilai hasil studi mahasiswa
SELECT m.nim, m.nama, SUM(mk.sks) AS total_sks, 
       ROUND(SUM(kh.nilai_angka * mk.sks) / SUM(mk.sks), 2) AS indeks_prestasi
FROM khs kh
JOIN mahasiswa m ON kh.nim = m.nim
JOIN matakuliah mk ON kh.kode_mk = mk.kode_mk
GROUP BY m.nim;

```

---

## Standar Aturan Konversi Nilai & Mutu

Sistem melakukan evaluasi nilai secara otomatis berdasarkan rentang parameter nilai berikut:

| Rentang Nilai Angka | Nilai Huruf | Bobot | Keterangan Status |
| --- | --- | --- | --- |
| 85.00 – 100.00 | A | 4.00 | Lulus (Sangat Memuaskan) |
| 75.00 – 84.99 | B | 3.00 | Lulus (Baik) |
| 65.00 – 74.99 | C | 2.00 | Lulus (Cukup) |
| 50.00 – 64.99 | D | 1.00 | Lulus Bersyarat (Kurang) |
| 0.00 – 49.99 | E | 0.00 | Tidak Lulus (Gagal) |

> **Metode Perhitungan Indeks Prestasi Semester (IPS):**
> IP Semester = Σ(Bobot Mutu × SKS) / ΣSKS Total

---

## Fitur Utama Sistem

* **Dashboard Interaktif:** Menyajikan visualisasi data statistik ringkas jumlah mahasiswa aktif, dosen pengajar, mata kuliah, dan summary pengisian KRS.
* **Manajemen CRUD Master:** Manajemen penuh data (Create, Read, Update, Delete) yang responsif dan dilengkapi pencarian (*search*) komparatif.
* **Sistem KRS Kontrol:** Validasi pengisian kartu rencana studi mahasiswa berdasarkan batas maksimum beban SKS.
* **Automasi Transkrip KHS:** Input nilai transaksional angka langsung terkonversi otomatis menjadi predikat huruf mutu akurat.
* **Eksportir PDF Berkas Dokumen:** Pembuatan instan berkas cetak fisik berupa Kartu Rencana Studi dan Kartu Hasil Studi berformat PDF siap cetak.

---

## Cara Menjalankan Sistem

### 1. Tahap Persiapan & Impor Database

Pastikan layanan database server MySQL (via XAMPP / Laragon) telah aktif. Buat database baru bernama `dbakademik` lalu import skema SQL:

```bash
mysql -u root -p dbakademik < database/dbakademik.sql

```

*(Sesuaikan credentials akun database root host pada berkas `config/db_config.py`)*

### 2. Pemasangan Library Pendukung

Gunakan paket manajer pip untuk menginstal seluruh dependensi framework eksternal proyek:

```bash
pip install -r requirements.txt

```

### 3. Eksekusi Aplikasi

Jalankan file entry-point utama sistem untuk memuat visualisasi antarmuka aplikasi:

```bash
python main.py

```

---

## Spesifikasi Teknologi

| Komponen Sistem | Spesifikasi Teknologi |
| --- | --- |
| **Bahasa Pemrograman** | Python 3.x |
| **Penyimpanan Data** | MySQL Server v8.0 / v5.7 |
| **Arsitektur Perangkat Lunak** | Model-View-Controller (MVC) Pattern |
| **Library Interaksi Database** | Driver MySQL-Connector Python |
| **Modul Cetak Dokumen** | ReportLab PDF Library / Ekivalen |

```

```
