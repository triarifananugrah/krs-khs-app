# Aplikasi KRS dan KHS Mahasiswa
**Universitas Muhammadiyah Palu**
Dosen: Nursalim, S.Kom., M.Kom.

---

## Cara Menjalankan

### 1. Persiapkan Database MySQL

Pastikan MySQL / XAMPP / Laragon sudah berjalan, lalu import database:

```bash
mysql -u root -p < database/dbakademik.sql
```

Atau buka **phpMyAdmin** → Import → pilih file `database/dbakademik.sql`

---

### 2. Sesuaikan Koneksi Database (jika perlu)

Edit file `config/db_config.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",       # isi jika ada password
    "database": "dbakademik"
}
```

---

### 3. Install Library Python

```bash
pip install -r requirements.txt
```

---

### 4. Jalankan Aplikasi

```bash
python main.py
```

---

## Fitur Aplikasi

| Menu | Fitur |
|------|-------|
| Dashboard | Statistik jumlah mahasiswa, dosen, mata kuliah, KRS |
| Mahasiswa | CRUD data mahasiswa lengkap + search |
| Dosen | CRUD data dosen + search |
| Mata Kuliah | CRUD mata kuliah + search |
| Input KRS | Input & kelola KRS mahasiswa |
| Input Nilai | Input nilai + konversi otomatis A/B/C/D/E |
| Laporan KRS | Tampil & export PDF KRS per NIM |
| Laporan KHS | Tampil & export PDF KHS + IP Semester |

---

## Struktur Folder

```
krs_khs_app/
├── database/        ← File SQL
├── config/          ← Koneksi database
├── controllers/     ← Logic aplikasi (MVC)
├── models/          ← Query database (MVC)
├── views/           ← Tampilan GUI (MVC)
├── reports/         ← Generator PDF
├── laporan/         ← Output PDF (dibuat otomatis)
├── main.py          ← Jalankan dari sini
└── requirements.txt
```

---

## Konversi Nilai

| Nilai Angka | Nilai Huruf | Bobot |
|-------------|-------------|-------|
| 85 – 100 | A | 4.00 |
| 75 – 84  | B | 3.00 |
| 65 – 74  | C | 2.00 |
| 50 – 64  | D | 1.00 |
| 0  – 49  | E | 0.00 |

**IP Semester = Total Mutu / Total SKS**
