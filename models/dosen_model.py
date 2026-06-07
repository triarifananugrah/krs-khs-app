from config.db_config import get_connection

class DosenModel:
    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nuptk, nama_dosen, pendidikan_terakhir, jabatan_fungsional, jenis_kelamin, alamat FROM tbdosen ORDER BY nama_dosen")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_by_nuptk(self, nuptk):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbdosen WHERE nuptk=%s", (nuptk,))
        row = cursor.fetchone()
        conn.close()
        return row

    def search(self, keyword):
        conn = get_connection()
        cursor = conn.cursor()
        q = f"%{keyword}%"
        cursor.execute("SELECT nuptk, nama_dosen, pendidikan_terakhir, jabatan_fungsional, jenis_kelamin, alamat FROM tbdosen WHERE nuptk LIKE %s OR nama_dosen LIKE %s", (q, q))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_options(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nuptk, nama_dosen FROM tbdosen ORDER BY nama_dosen")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbdosen (nuptk,nama_dosen,pendidikan_terakhir,jabatan_fungsional,jenis_kelamin,alamat) VALUES (%s,%s,%s,%s,%s,%s)", data)
        conn.commit()
        conn.close()

    def update(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tbdosen SET nama_dosen=%s,pendidikan_terakhir=%s,jabatan_fungsional=%s,jenis_kelamin=%s,alamat=%s WHERE nuptk=%s", data)
        conn.commit()
        conn.close()

    def delete(self, nuptk):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbdosen WHERE nuptk=%s", (nuptk,))
        conn.commit()
        conn.close()

    def count(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tbdosen")
        c = cursor.fetchone()[0]
        conn.close()
        return c
