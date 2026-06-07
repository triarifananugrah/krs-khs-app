import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "dbakademik"
}

def get_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def test_connection():
    try:
        conn = get_connection()
        if conn.is_connected():
            print("[OK] Koneksi ke database berhasil.")
            conn.close()
            return True
    except Error as e:
        print(f"[GAGAL] Koneksi gagal: {e}")
        return False
