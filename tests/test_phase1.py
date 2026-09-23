"""
Test Phase 1 — Foundation.

Test untuk memverifikasi:
1. Database dapat dibuat otomatis
2. Tabel users dan attendance ada
3. Schema sesuai spesifikasi
4. Validator input berfungsi
5. Config terload dengan benar
"""

import os
import sys
import sqlite3
import tempfile

# Tambahkan root project ke path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    DATABASE_PATH,
    SCHEMA_FILE,
    FACE_DISTANCE_THRESHOLD,
    APP_NAME,
    DATA_DIR,
)
from database.database import Database
from utils.validators import validate_nim, validate_name, validate_menu_input


class TestConfig:
    """Test konfigurasi aplikasi."""

    def test_database_path_configured(self):
        """Test bahwa path database sudah dikonfigurasi."""
        assert DATABASE_PATH is not None
        assert str(DATABASE_PATH).endswith("attendance.db")

    def test_schema_file_exists(self):
        """Test bahwa file schema SQL ada."""
        assert SCHEMA_FILE.exists(), f"Schema file tidak ditemukan: {SCHEMA_FILE}"

    def test_face_threshold_valid(self):
        """Test bahwa threshold face distance valid."""
        assert 0.0 < FACE_DISTANCE_THRESHOLD < 1.0

    def test_app_name_configured(self):
        """Test bahwa nama aplikasi sudah dikonfigurasi."""
        assert APP_NAME is not None
        assert len(APP_NAME) > 0


class TestDatabase:
    """Test database initialization dan operasi dasar."""

    def _create_temp_db(self):
        """Buat database sementara untuk testing."""
        temp_dir = tempfile.mkdtemp()
        temp_db = os.path.join(temp_dir, "test_attendance.db")
        return temp_db

    def test_database_auto_create(self):
        """Test bahwa database dibuat otomatis."""
        temp_db = self._create_temp_db()
        try:
            db = Database(db_path=temp_db)
            assert os.path.exists(temp_db), "Database file tidak dibuat"
        finally:
            if os.path.exists(temp_db):
                os.remove(temp_db)

    def test_users_table_exists(self):
        """Test bahwa tabel users ada."""
        temp_db = self._create_temp_db()
        try:
            db = Database(db_path=temp_db)
            result = db.fetch_one(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
            )
            assert result is not None, "Tabel users tidak ditemukan"
        finally:
            if os.path.exists(temp_db):
                os.remove(temp_db)

    def test_attendance_table_exists(self):
        """Test bahwa tabel attendance ada."""
        temp_db = self._create_temp_db()
        try:
            db = Database(db_path=temp_db)
            result = db.fetch_one(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='attendance'"
            )
            assert result is not None, "Tabel attendance tidak ditemukan"
        finally:
            if os.path.exists(temp_db):
                os.remove(temp_db)

    def test_users_table_columns(self):
        """Test bahwa tabel users memiliki kolom yang benar."""
        temp_db = self._create_temp_db()
        try:
            db = Database(db_path=temp_db)
            columns = db.fetch_all("PRAGMA table_info(users)")
            column_names = [col["name"] for col in columns]
            assert "id" in column_names
            assert "nim" in column_names
            assert "name" in column_names
            assert "face_encoding" in column_names
            assert "created_at" in column_names
        finally:
            if os.path.exists(temp_db):
                os.remove(temp_db)

    def test_attendance_table_columns(self):
        """Test bahwa tabel attendance memiliki kolom yang benar."""
        temp_db = self._create_temp_db()
        try:
            db = Database(db_path=temp_db)
            columns = db.fetch_all("PRAGMA table_info(attendance)")
            column_names = [col["name"] for col in columns]
            assert "id" in column_names
            assert "user_id" in column_names
            assert "attendance_date" in column_names
            assert "attendance_time" in column_names
            assert "status" in column_names
            assert "created_at" in column_names
        finally:
            if os.path.exists(temp_db):
                os.remove(temp_db)

    def test_nim_unique_constraint(self):
        """Test bahwa NIM memiliki UNIQUE constraint."""
        temp_db = self._create_temp_db()
        try:
            db = Database(db_path=temp_db)
            # Insert pertama harus berhasil
            db.execute(
                "INSERT INTO users (nim, name) VALUES (?, ?)",
                ("12345", "Test User")
            )
            # Insert kedua dengan NIM sama harus gagal
            try:
                db.execute(
                    "INSERT INTO users (nim, name) VALUES (?, ?)",
                    ("12345", "Test User 2")
                )
                assert False, "Seharusnya NIM duplikat ditolak"
            except sqlite3.IntegrityError:
                pass  # Expected
        finally:
            if os.path.exists(temp_db):
                os.remove(temp_db)

    def test_attendance_unique_constraint(self):
        """Test bahwa absensi ganda pada hari yang sama ditolak."""
        temp_db = self._create_temp_db()
        try:
            db = Database(db_path=temp_db)
            # Insert user
            db.execute(
                "INSERT INTO users (nim, name) VALUES (?, ?)",
                ("12345", "Test User")
            )
            user = db.fetch_one("SELECT id FROM users WHERE nim = ?", ("12345",))
            user_id = user["id"]

            # Insert absensi pertama
            db.execute(
                "INSERT INTO attendance (user_id, attendance_date, attendance_time, status) "
                "VALUES (?, ?, ?, ?)",
                (user_id, "2026-09-23", "08:00:00", "HADIR")
            )

            # Insert absensi kedua pada hari yang sama harus gagal
            try:
                db.execute(
                    "INSERT INTO attendance (user_id, attendance_date, attendance_time, status) "
                    "VALUES (?, ?, ?, ?)",
                    (user_id, "2026-09-23", "09:00:00", "HADIR")
                )
                assert False, "Seharusnya absensi ganda ditolak"
            except sqlite3.IntegrityError:
                pass  # Expected
        finally:
            if os.path.exists(temp_db):
                os.remove(temp_db)

    def test_foreign_key_enforcement(self):
        """Test bahwa foreign key antara attendance dan users berlaku."""
        temp_db = self._create_temp_db()
        try:
            db = Database(db_path=temp_db)
            # Insert absensi tanpa user yang valid harus gagal
            try:
                db.execute(
                    "INSERT INTO attendance (user_id, attendance_date, attendance_time, status) "
                    "VALUES (?, ?, ?, ?)",
                    (999, "2026-09-23", "08:00:00", "HADIR")
                )
                assert False, "Seharusnya foreign key constraint dilanggar"
            except sqlite3.IntegrityError:
                pass  # Expected
        finally:
            if os.path.exists(temp_db):
                os.remove(temp_db)

    def test_cascade_delete(self):
        """Test bahwa menghapus user juga menghapus data absensinya."""
        temp_db = self._create_temp_db()
        try:
            db = Database(db_path=temp_db)
            # Insert user dan absensi
            db.execute(
                "INSERT INTO users (nim, name) VALUES (?, ?)",
                ("12345", "Test User")
            )
            user = db.fetch_one("SELECT id FROM users WHERE nim = ?", ("12345",))
            user_id = user["id"]

            db.execute(
                "INSERT INTO attendance (user_id, attendance_date, attendance_time, status) "
                "VALUES (?, ?, ?, ?)",
                (user_id, "2026-09-23", "08:00:00", "HADIR")
            )

            # Hapus user
            db.execute("DELETE FROM users WHERE id = ?", (user_id,))

            # Cek absensi juga terhapus (CASCADE)
            attendance = db.fetch_all(
                "SELECT * FROM attendance WHERE user_id = ?", (user_id,)
            )
            assert len(attendance) == 0, "Data absensi seharusnya ikut terhapus"
        finally:
            if os.path.exists(temp_db):
                os.remove(temp_db)


class TestValidators:
    """Test fungsi validasi input."""

    def test_valid_nim(self):
        """Test NIM yang valid."""
        is_valid, _ = validate_nim("12345")
        assert is_valid

    def test_empty_nim(self):
        """Test NIM kosong."""
        is_valid, _ = validate_nim("")
        assert not is_valid

    def test_none_nim(self):
        """Test NIM None."""
        is_valid, _ = validate_nim(None)
        assert not is_valid

    def test_whitespace_nim(self):
        """Test NIM hanya whitespace."""
        is_valid, _ = validate_nim("   ")
        assert not is_valid

    def test_valid_name(self):
        """Test nama yang valid."""
        is_valid, _ = validate_name("Yudhistira")
        assert is_valid

    def test_empty_name(self):
        """Test nama kosong."""
        is_valid, _ = validate_name("")
        assert not is_valid

    def test_none_name(self):
        """Test nama None."""
        is_valid, _ = validate_name(None)
        assert not is_valid

    def test_valid_menu_input(self):
        """Test input menu yang valid."""
        is_valid, _ = validate_menu_input("1", ["1", "2", "3", "4", "5"])
        assert is_valid

    def test_invalid_menu_input(self):
        """Test input menu yang tidak valid."""
        is_valid, _ = validate_menu_input("6", ["1", "2", "3", "4", "5"])
        assert not is_valid

    def test_empty_menu_input(self):
        """Test input menu kosong."""
        is_valid, _ = validate_menu_input("", ["1", "2", "3", "4", "5"])
        assert not is_valid
