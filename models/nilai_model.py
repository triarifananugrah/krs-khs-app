from config.db_config import get_connection

class NilaiModel:
    def konversi(self, nilai_angka):
        n = float(nilai_angka)
        if n >= 85: return "A", 4.00
        elif n >= 75: return "B", 3.00
        elif n >= 65: return "C", 2.00
        elif n >= 50: return "D", 1.00
        else: return "E", 0.00

    def get_by_nim(self, nim):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT n.id_nilai, k.id_krs, m.nim, m.nama_mahasiswa, m.prodi,
                   mk.kode_mk, mk.nama_matakuliah, mk.sks,
                   n.nilai_angka, n.nilai_huruf, n.bobot, n.mutu
            FROM tbnilai n
            JOIN tbkrs k        ON n.id_krs = k.id_krs
            JOIN tbmahasiswa m  ON k.nim = m.nim
            JOIN tbmatakuliah mk ON k.kode_mk = mk.kode_mk
            WHERE m.nim = %s
        """, (nim,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_by_id_krs(self, id_krs):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbnilai WHERE id_krs=%s", (id_krs,))
        row = cursor.fetchone()
        conn.close()
        return row

    def get_all_with_detail(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT n.id_nilai, m.nim, m.nama_mahasiswa, mk.nama_matakuliah,
                   mk.sks, n.nilai_angka, n.nilai_huruf, n.bobot, n.mutu
            FROM tbnilai n
            JOIN tbkrs k        ON n.id_krs = k.id_krs
            JOIN tbmahasiswa m  ON k.nim = m.nim
            JOIN tbmatakuliah mk ON k.kode_mk = mk.kode_mk
            ORDER BY m.nim
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert(self, id_krs, nilai_angka):
        conn = get_connection()
        cursor = conn.cursor()
        nilai_huruf, bobot = self.konversi(nilai_angka)
        cursor.execute("""
            SELECT mk.sks FROM tbkrs k
            JOIN tbmatakuliah mk ON k.kode_mk = mk.kode_mk
            WHERE k.id_krs = %s
        """, (id_krs,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            raise Exception("Data KRS tidak ditemukan")
        sks = result[0]
        mutu = sks * bobot
        cursor.execute("""
            INSERT INTO tbnilai (id_krs, nilai_angka, nilai_huruf, bobot, mutu)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_krs, nilai_angka, nilai_huruf, bobot, mutu))
        conn.commit()
        conn.close()
        return nilai_huruf, bobot, mutu

    def update(self, id_nilai, id_krs, nilai_angka):
        conn = get_connection()
        cursor = conn.cursor()
        nilai_huruf, bobot = self.konversi(nilai_angka)
        cursor.execute("SELECT mk.sks FROM tbkrs k JOIN tbmatakuliah mk ON k.kode_mk=mk.kode_mk WHERE k.id_krs=%s", (id_krs,))
        result = cursor.fetchone()
        sks = result[0] if result else 0
        mutu = sks * bobot
        cursor.execute("UPDATE tbnilai SET nilai_angka=%s,nilai_huruf=%s,bobot=%s,mutu=%s WHERE id_nilai=%s",
                       (nilai_angka, nilai_huruf, bobot, mutu, id_nilai))
        conn.commit()
        conn.close()

    def delete(self, id_nilai):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbnilai WHERE id_nilai=%s", (id_nilai,))
        conn.commit()
        conn.close()

    def hitung_ip(self, data_khs):
        total_sks = sum(r[7] for r in data_khs)
        total_mutu = sum(r[11] for r in data_khs)
        ip = round(total_mutu / total_sks, 2) if total_sks > 0 else 0
        return total_sks, total_mutu, ip
