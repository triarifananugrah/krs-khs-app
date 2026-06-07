from config.db_config import get_connection

class MatakuliahModel:
    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT kode_mk, nama_matakuliah, sks, semester FROM tbmatakuliah ORDER BY semester, kode_mk")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_by_kode(self, kode_mk):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbmatakuliah WHERE kode_mk=%s", (kode_mk,))
        row = cursor.fetchone()
        conn.close()
        return row

    def search(self, keyword):
        conn = get_connection()
        cursor = conn.cursor()
        q = f"%{keyword}%"
        cursor.execute("SELECT kode_mk, nama_matakuliah, sks, semester FROM tbmatakuliah WHERE kode_mk LIKE %s OR nama_matakuliah LIKE %s", (q, q))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_options(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT kode_mk, nama_matakuliah, sks FROM tbmatakuliah ORDER BY kode_mk")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbmatakuliah (kode_mk,nama_matakuliah,sks,semester) VALUES (%s,%s,%s,%s)", data)
        conn.commit()
        conn.close()

    def update(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tbmatakuliah SET nama_matakuliah=%s,sks=%s,semester=%s WHERE kode_mk=%s", data)
        conn.commit()
        conn.close()

    def delete(self, kode_mk):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbmatakuliah WHERE kode_mk=%s", (kode_mk,))
        conn.commit()
        conn.close()

    def count(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tbmatakuliah")
        c = cursor.fetchone()[0]
        conn.close()
        return c
