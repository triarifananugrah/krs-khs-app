-- ============================================================
--  Database  : dbakademik
--  Dosen     : Nursalim, S.Kom., M.Kom.
--  Kampus    : Universitas Muhammadiyah Palu
-- ============================================================

CREATE DATABASE IF NOT EXISTS dbakademik
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dbakademik;

-- ─────────────────────────────────────────────
--  TABEL MAHASISWA
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tbmahasiswa (
  nim            CHAR(10)     PRIMARY KEY,
  nama_mahasiswa VARCHAR(100) NOT NULL,
  prodi          VARCHAR(50)  NOT NULL,
  jenis_kelamin  ENUM('L','P') NOT NULL,
  tempat_lahir   VARCHAR(50),
  tanggal_lahir  DATE,
  alamat         VARCHAR(100),
  desa_kelurahan VARCHAR(50),
  kecamatan      VARCHAR(50),
  kabupaten_kota VARCHAR(50),
  provinsi       VARCHAR(50)
);

-- ─────────────────────────────────────────────
--  TABEL DOSEN
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tbdosen (
  nuptk            CHAR(15) PRIMARY KEY,
  nama_dosen       VARCHAR(100) NOT NULL,
  pendidikan_terakhir ENUM('S2','S3') NOT NULL,
  jabatan_fungsional  ENUM('Asisten Ahli','Lektor','Lektor Kepala','Guru Besar') NOT NULL,
  jenis_kelamin    ENUM('L','P') NOT NULL,
  alamat           VARCHAR(100)
);

-- ─────────────────────────────────────────────
--  TABEL MATA KULIAH
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tbmatakuliah (
  kode_mk          CHAR(12) PRIMARY KEY,
  nama_matakuliah  VARCHAR(150) NOT NULL,
  sks              INT NOT NULL,
  semester         ENUM('I','II','III','IV','V','VI','VII','VIII') NOT NULL
);

-- ─────────────────────────────────────────────
--  TABEL KRS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tbkrs (
  id_krs   INT AUTO_INCREMENT PRIMARY KEY,
  nim      CHAR(10) NOT NULL,
  kode_mk  CHAR(12) NOT NULL,
  kelas    VARCHAR(5),
  ruang    VARCHAR(10),
  hari     ENUM('Senin','Selasa','Rabu','Kamis','Jumat','Sabtu') NOT NULL,
  jam      TIME NOT NULL,
  nuptk    CHAR(15) NOT NULL,
  FOREIGN KEY (nim)     REFERENCES tbmahasiswa(nim) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (kode_mk) REFERENCES tbmatakuliah(kode_mk) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (nuptk)   REFERENCES tbdosen(nuptk)   ON UPDATE CASCADE ON DELETE CASCADE
);

-- ─────────────────────────────────────────────
--  TABEL NILAI
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tbnilai (
  id_nilai    INT AUTO_INCREMENT PRIMARY KEY,
  id_krs      INT NOT NULL,
  nilai_angka DECIMAL(5,2) NOT NULL,
  nilai_huruf VARCHAR(2)   NOT NULL,
  bobot       DECIMAL(3,2) NOT NULL,
  mutu        DECIMAL(5,2) NOT NULL,
  FOREIGN KEY (id_krs) REFERENCES tbkrs(id_krs) ON UPDATE CASCADE ON DELETE CASCADE
);

-- ─────────────────────────────────────────────
--  DATA DUMMY
-- ─────────────────────────────────────────────

INSERT INTO tbdosen VALUES
('1234567890000001','Nursalim, S.Kom., M.Kom.','S2','Lektor','L','Jl. Tadulako No.1, Palu'),
('1234567890000002','Dr. Rahma Dewi, M.T.','S3','Lektor Kepala','P','Jl. Pramuka No.5, Palu'),
('1234567890000003','Ahmad Fauzi, S.T., M.Kom.','S2','Asisten Ahli','L','Jl. Diponegoro No.10, Palu');

INSERT INTO tbmatakuliah VALUES
('IF101','Basis Data',3,'III'),
('IF102','Pemrograman Python',3,'III'),
('IF103','Jaringan Komputer',3,'IV'),
('IF104','Algoritma dan Struktur Data',3,'II'),
('IF105','Sistem Operasi',2,'IV'),
('IF106','Rekayasa Perangkat Lunak',3,'V'),
('IF107','Kecerdasan Buatan',3,'VI');

INSERT INTO tbmahasiswa VALUES
('2024001001','Muhammad Rizki','Informatika','L','Palu','2004-03-15','Jl. Mawar No.1','Lere','Palu Barat','Kota Palu','Sulawesi Tengah'),
('2024001002','Siti Nurhaliza','Informatika','P','Donggala','2004-07-22','Jl. Melati No.3','Birobuli','Palu Selatan','Kota Palu','Sulawesi Tengah'),
('2024001003','Bagas Prasetyo','Informatika','L','Poso','2003-11-10','Jl. Anggrek No.7','Talise','Mantikulore','Kota Palu','Sulawesi Tengah'),
('2024001004','Dewi Rahayu','Sistem Informasi','P','Palu','2004-01-05','Jl. Kamboja No.2','Tondo','Mantikulore','Kota Palu','Sulawesi Tengah'),
('2024001005','Eko Santoso','Sistem Informasi','L','Parigi','2003-08-30','Jl. Kenanga No.9','Palupi','Tatanga','Kota Palu','Sulawesi Tengah');

INSERT INTO tbkrs (nim,kode_mk,kelas,ruang,hari,jam,nuptk) VALUES
('2024001001','IF101','A','R101','Senin','08:00:00','1234567890000001'),
('2024001001','IF102','A','R102','Rabu','10:00:00','1234567890000002'),
('2024001001','IF104','A','R103','Jumat','08:00:00','1234567890000003'),
('2024001002','IF101','A','R101','Senin','08:00:00','1234567890000001'),
('2024001002','IF102','A','R102','Rabu','10:00:00','1234567890000002'),
('2024001003','IF101','B','R104','Selasa','09:00:00','1234567890000001'),
('2024001003','IF104','B','R105','Kamis','11:00:00','1234567890000003'),
('2024001004','IF102','B','R106','Senin','13:00:00','1234567890000002'),
('2024001005','IF101','A','R101','Senin','08:00:00','1234567890000001'),
('2024001005','IF104','A','R103','Jumat','08:00:00','1234567890000003');

INSERT INTO tbnilai (id_krs,nilai_angka,nilai_huruf,bobot,mutu) VALUES
(1,88,'A',4.00,12.00),
(2,76,'B',3.00,9.00),
(3,65,'C',2.00,6.00),
(4,91,'A',4.00,12.00),
(5,80,'B',3.00,9.00),
(6,72,'C',2.00,6.00),
(7,85,'A',4.00,12.00),
(8,55,'D',1.00,3.00),
(9,78,'B',3.00,9.00),
(10,90,'A',4.00,12.00);
