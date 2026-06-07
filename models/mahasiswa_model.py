from config.db_config import get_connection

class MahasiswaModel:
    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nim, nama_mahasiswa, prodi, jenis_kelamin, tempat_lahir, tanggal_lahir, alamat, desa_kelurahan, kecamatan, kabupaten_kota, provinsi FROM tbmahasiswa ORDER BY nim")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_by_nim(self, nim):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbmahasiswa WHERE nim=%s", (nim,))
        row = cursor.fetchone()
        conn.close()
        return row

    def search(self, keyword):
        conn = get_connection()
        cursor = conn.cursor()
        q = f"%{keyword}%"
        cursor.execute("SELECT nim, nama_mahasiswa, prodi, jenis_kelamin, tempat_lahir, tanggal_lahir, alamat, desa_kelurahan, kecamatan, kabupaten_kota, provinsi FROM tbmahasiswa WHERE nim LIKE %s OR nama_mahasiswa LIKE %s OR prodi LIKE %s", (q, q, q))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tbmahasiswa (nim,nama_mahasiswa,prodi,jenis_kelamin,tempat_lahir,tanggal_lahir,alamat,desa_kelurahan,kecamatan,kabupaten_kota,provinsi)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, data)
        conn.commit()
        conn.close()

    def update(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tbmahasiswa SET nama_mahasiswa=%s,prodi=%s,jenis_kelamin=%s,tempat_lahir=%s,
            tanggal_lahir=%s,alamat=%s,desa_kelurahan=%s,kecamatan=%s,kabupaten_kota=%s,provinsi=%s
            WHERE nim=%s
        """, data)
        conn.commit()
        conn.close()

    def delete(self, nim):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbmahasiswa WHERE nim=%s", (nim,))
        conn.commit()
        conn.close()

    def count(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tbmahasiswa")
        c = cursor.fetchone()[0]
        conn.close()
        return c
