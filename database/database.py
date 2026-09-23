"""
Modul database untuk manajemen koneksi dan operasi SQLite.

Modul ini menyediakan class Database yang menangani:
- Pembuatan database otomatis jika belum ada
- Inisialisasi schema dari file SQL
- Eksekusi query dengan parameterized queries
- Manajemen koneksi database
"""

import sqlite3
from pathlib import Path

from config import DATABASE_PATH, SCHEMA_FILE, DATA_DIR


class Database:
    """
    Class untuk mengelola koneksi dan operasi database SQLite.

    Database dan tabel akan dibuat otomatis saat pertama kali
    di-inisialisasi jika belum ada.
    """

    def __init__(self, db_path=None):
        """
        Inisialisasi database.

        Args:
            db_path: Path ke file database. Jika None, menggunakan
                     path dari config.py.
        """
        self.db_path = db_path or DATABASE_PATH
        self._ensure_data_directory()
        self._init_database()

    def _ensure_data_directory(self):
        """Pastikan directory data/ ada."""
        data_dir = Path(self.db_path).parent
        data_dir.mkdir(parents=True, exist_ok=True)

    def _init_database(self):
        """
        Inisialisasi database dengan menjalankan schema SQL.

        Membuat tabel-tabel yang diperlukan jika belum ada.
        """
        schema_path = SCHEMA_FILE
        if not schema_path.exists():
            raise FileNotFoundError(
                f"File schema tidak ditemukan: {schema_path}"
            )

        schema_sql = schema_path.read_text(encoding="utf-8")

        conn = self.get_connection()
        try:
            # Aktifkan foreign key support
            conn.execute("PRAGMA foreign_keys = ON")
            conn.executescript(schema_sql)
            conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal inisialisasi database: {e}")
            raise
        finally:
            conn.close()

    def get_connection(self):
        """
        Buat dan kembalikan koneksi database baru.

        Returns:
            sqlite3.Connection: Objek koneksi database.

        Raises:
            sqlite3.Error: Jika gagal membuat koneksi.
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            # Aktifkan foreign key support untuk setiap koneksi
            conn.execute("PRAGMA foreign_keys = ON")
            # Gunakan Row factory agar hasil query bisa diakses
            # dengan nama kolom
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal membuka koneksi database: {e}")
            raise

    def execute(self, query, params=None):
        """
        Eksekusi query SQL (INSERT, UPDATE, DELETE).

        Menggunakan parameterized query untuk keamanan.

        Args:
            query: String SQL query dengan placeholder (?).
            params: Tuple parameter untuk query.

        Returns:
            sqlite3.Cursor: Cursor hasil eksekusi.

        Raises:
            sqlite3.Error: Jika terjadi error saat eksekusi.
        """
        conn = self.get_connection()
        try:
            cursor = conn.execute(query, params or ())
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def fetch_one(self, query, params=None):
        """
        Eksekusi query dan ambil satu baris hasil.

        Args:
            query: String SQL query dengan placeholder (?).
            params: Tuple parameter untuk query.

        Returns:
            sqlite3.Row atau None: Satu baris hasil query.
        """
        conn = self.get_connection()
        try:
            cursor = conn.execute(query, params or ())
            return cursor.fetchone()
        finally:
            conn.close()

    def fetch_all(self, query, params=None):
        """
        Eksekusi query dan ambil seluruh baris hasil.

        Args:
            query: String SQL query dengan placeholder (?).
            params: Tuple parameter untuk query.

        Returns:
            list[sqlite3.Row]: Daftar baris hasil query.
        """
        conn = self.get_connection()
        try:
            cursor = conn.execute(query, params or ())
            return cursor.fetchall()
        finally:
            conn.close()
