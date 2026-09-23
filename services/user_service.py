"""
Modul services/user_service.py — Business logic pengelolaan pengguna.

Menyediakan operasi CRUD untuk data pengguna:
- Tambah pengguna baru (dengan validasi NIM unik)
- Lihat semua pengguna
- Cari pengguna berdasarkan NIM
- Cari pengguna berdasarkan ID
- Hapus pengguna (beserta face encoding terkait)
- Update face encoding pengguna
"""

import sqlite3

from models.user import User


class UserService:
    """
    Service untuk mengelola data pengguna.

    Semua operasi database menggunakan parameterized queries
    untuk keamanan.
    """

    def __init__(self, database):
        """
        Inisialisasi UserService.

        Args:
            database: Instance Database untuk operasi database.
        """
        self.db = database

    def add_user(self, nim, name, face_encoding=None):
        """
        Tambah pengguna baru.

        Args:
            nim: Nomor Induk Mahasiswa (harus unik).
            name: Nama lengkap pengguna.
            face_encoding: Data encoding wajah (bytes), opsional.

        Returns:
            tuple: (success: bool, message: str, user_id: int atau None)
        """
        # Validasi input
        if not nim or not nim.strip():
            return False, "NIM tidak boleh kosong.", None

        if not name or not name.strip():
            return False, "Nama tidak boleh kosong.", None

        nim = nim.strip()
        name = name.strip()

        # Cek NIM duplikat
        existing = self.get_user_by_nim(nim)
        if existing is not None:
            return False, f"NIM '{nim}' sudah terdaftar atas nama {existing.name}.", None

        # Insert ke database
        try:
            cursor = self.db.execute(
                "INSERT INTO users (nim, name, face_encoding) VALUES (?, ?, ?)",
                (nim, name, face_encoding)
            )
            user_id = cursor.lastrowid
            return True, f"Pengguna '{name}' berhasil ditambahkan.", user_id
        except sqlite3.IntegrityError:
            return False, f"NIM '{nim}' sudah terdaftar.", None
        except sqlite3.Error as e:
            return False, f"Gagal menambahkan pengguna: {e}", None

    def get_all_users(self):
        """
        Ambil semua data pengguna.

        Returns:
            list[User]: Daftar semua pengguna.
        """
        rows = self.db.fetch_all(
            "SELECT id, nim, name, face_encoding, created_at "
            "FROM users ORDER BY id"
        )
        return [User.from_row(row) for row in rows]

    def get_user_by_nim(self, nim):
        """
        Cari pengguna berdasarkan NIM.

        Args:
            nim: NIM yang dicari.

        Returns:
            User atau None: Data pengguna jika ditemukan.
        """
        if not nim or not nim.strip():
            return None

        row = self.db.fetch_one(
            "SELECT id, nim, name, face_encoding, created_at "
            "FROM users WHERE nim = ?",
            (nim.strip(),)
        )
        return User.from_row(row)

    def get_user_by_id(self, user_id):
        """
        Cari pengguna berdasarkan ID.

        Args:
            user_id: ID pengguna yang dicari.

        Returns:
            User atau None: Data pengguna jika ditemukan.
        """
        row = self.db.fetch_one(
            "SELECT id, nim, name, face_encoding, created_at "
            "FROM users WHERE id = ?",
            (user_id,)
        )
        return User.from_row(row)

    def delete_user(self, nim):
        """
        Hapus pengguna berdasarkan NIM.

        Menghapus data pengguna beserta data absensi terkait
        (menggunakan CASCADE dari foreign key).

        Args:
            nim: NIM pengguna yang akan dihapus.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not nim or not nim.strip():
            return False, "NIM tidak boleh kosong."

        nim = nim.strip()

        # Cek apakah user ada
        user = self.get_user_by_nim(nim)
        if user is None:
            return False, f"Pengguna dengan NIM '{nim}' tidak ditemukan."

        try:
            self.db.execute(
                "DELETE FROM users WHERE nim = ?",
                (nim,)
            )
            return True, f"Pengguna '{user.name}' (NIM: {nim}) berhasil dihapus."
        except sqlite3.Error as e:
            return False, f"Gagal menghapus pengguna: {e}"

    def update_face_encoding(self, user_id, face_encoding):
        """
        Update face encoding pengguna.

        Args:
            user_id: ID pengguna.
            face_encoding: Data encoding wajah baru (bytes).

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            self.db.execute(
                "UPDATE users SET face_encoding = ? WHERE id = ?",
                (face_encoding, user_id)
            )
            return True, "Face encoding berhasil diperbarui."
        except sqlite3.Error as e:
            return False, f"Gagal memperbarui face encoding: {e}"

    def get_all_users_with_encoding(self):
        """
        Ambil semua pengguna yang sudah memiliki face encoding.

        Returns:
            list[User]: Daftar pengguna yang memiliki face encoding.
        """
        rows = self.db.fetch_all(
            "SELECT id, nim, name, face_encoding, created_at "
            "FROM users WHERE face_encoding IS NOT NULL ORDER BY id"
        )
        return [User.from_row(row) for row in rows]

    def get_user_count(self):
        """
        Hitung jumlah pengguna terdaftar.

        Returns:
            int: Jumlah pengguna.
        """
        row = self.db.fetch_one("SELECT COUNT(*) as count FROM users")
        return row["count"] if row else 0
