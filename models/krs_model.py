from config.db_config import get_connection

class KrsModel:
    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT k.id_krs, m.nim, m.nama_mahasiswa, mk.kode_mk, mk.nama_matakuliah,
                   mk.sks, k.kelas, k.ruang, k.hari, k.jam, d.nama_dosen
            FROM tbkrs k
            JOIN tbmahasiswa m  ON k.nim = m.nim
            JOIN tbmatakuliah mk ON k.kode_mk = mk.kode_mk
            JOIN tbdosen d      ON k.nuptk = d.nuptk
            ORDER BY m.nim, mk.kode_mk
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_by_nim(self, nim):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT k.id_krs, m.nim, m.nama_mahasiswa, m.prodi,
                   mk.kode_mk, mk.nama_matakuliah, mk.sks,
                   k.kelas, k.ruang, k.hari, k.jam, d.nuptk, d.nama_dosen
            FROM tbkrs k
            JOIN tbmahasiswa m  ON k.nim = m.nim
            JOIN tbmatakuliah mk ON k.kode_mk = mk.kode_mk
            JOIN tbdosen d      ON k.nuptk = d.nuptk
            WHERE m.nim = %s
        """, (nim,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_by_id(self, id_krs):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbkrs WHERE id_krs=%s", (id_krs,))
        row = cursor.fetchone()
        conn.close()
        return row

    def insert(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbkrs (nim,kode_mk,kelas,ruang,hari,jam,nuptk) VALUES (%s,%s,%s,%s,%s,%s,%s)", data)
        conn.commit()
        conn.close()

    def update(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tbkrs SET nim=%s,kode_mk=%s,kelas=%s,ruang=%s,hari=%s,jam=%s,nuptk=%s WHERE id_krs=%s", data)
        conn.commit()
        conn.close()

    def delete(self, id_krs):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbkrs WHERE id_krs=%s", (id_krs,))
        conn.commit()
        conn.close()

    def count(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tbkrs")
        c = cursor.fetchone()[0]
        conn.close()
        return c

    def search(self, keyword):
        conn = get_connection()
        cursor = conn.cursor()
        q = f"%{keyword}%"
        cursor.execute("""
            SELECT k.id_krs, m.nim, m.nama_mahasiswa, mk.kode_mk, mk.nama_matakuliah,
                   mk.sks, k.kelas, k.ruang, k.hari, k.jam, d.nama_dosen
            FROM tbkrs k
            JOIN tbmahasiswa m  ON k.nim = m.nim
            JOIN tbmatakuliah mk ON k.kode_mk = mk.kode_mk
            JOIN tbdosen d      ON k.nuptk = d.nuptk
            WHERE m.nim LIKE %s OR m.nama_mahasiswa LIKE %s OR mk.nama_matakuliah LIKE %s
        """, (q, q, q))
        rows = cursor.fetchall()
        conn.close()
        return rows
