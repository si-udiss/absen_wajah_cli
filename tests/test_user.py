"""
Test Phase 2 — User Management.

Test untuk memverifikasi:
1. Registrasi user berhasil
2. NIM duplikat ditolak
3. User berhasil dicari berdasarkan NIM
4. User berhasil dicari berdasarkan ID
5. User berhasil dihapus
6. User tidak ditemukan
7. Input invalid ditangani
8. Daftar semua user
9. Update face encoding
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import Database
from services.user_service import UserService
from models.user import User


class TestUserService:
    """Test CRUD operasi pengguna."""

    def _setup(self):
        """Buat database dan service sementara untuk testing."""
        temp_dir = tempfile.mkdtemp()
        temp_db = os.path.join(temp_dir, "test_user.db")
        db = Database(db_path=temp_db)
        service = UserService(db)
        return db, service, temp_db

    def test_add_user_success(self):
        """Test menambahkan pengguna berhasil."""
        _, service, temp_db = self._setup()
        try:
            success, message, user_id = service.add_user("12345", "Test User")
            assert success, f"Seharusnya berhasil: {message}"
            assert user_id is not None
            assert "berhasil" in message.lower()
        finally:
            os.remove(temp_db)

    def test_add_user_duplicate_nim(self):
        """Test NIM duplikat ditolak."""
        _, service, temp_db = self._setup()
        try:
            service.add_user("12345", "User 1")
            success, message, user_id = service.add_user("12345", "User 2")
            assert not success, "Seharusnya NIM duplikat ditolak"
            assert user_id is None
            assert "sudah terdaftar" in message.lower()
        finally:
            os.remove(temp_db)

    def test_add_user_empty_nim(self):
        """Test NIM kosong ditolak."""
        _, service, temp_db = self._setup()
        try:
            success, message, _ = service.add_user("", "Test User")
            assert not success
            assert "kosong" in message.lower()
        finally:
            os.remove(temp_db)

    def test_add_user_empty_name(self):
        """Test nama kosong ditolak."""
        _, service, temp_db = self._setup()
        try:
            success, message, _ = service.add_user("12345", "")
            assert not success
            assert "kosong" in message.lower()
        finally:
            os.remove(temp_db)

    def test_add_user_whitespace_nim(self):
        """Test NIM hanya whitespace ditolak."""
        _, service, temp_db = self._setup()
        try:
            success, message, _ = service.add_user("   ", "Test User")
            assert not success
        finally:
            os.remove(temp_db)

    def test_get_user_by_nim(self):
        """Test mencari pengguna berdasarkan NIM."""
        _, service, temp_db = self._setup()
        try:
            service.add_user("12345", "Yudhistira")
            user = service.get_user_by_nim("12345")
            assert user is not None
            assert user.nim == "12345"
            assert user.name == "Yudhistira"
        finally:
            os.remove(temp_db)

    def test_get_user_by_nim_not_found(self):
        """Test mencari pengguna yang tidak ada."""
        _, service, temp_db = self._setup()
        try:
            user = service.get_user_by_nim("99999")
            assert user is None
        finally:
            os.remove(temp_db)

    def test_get_user_by_nim_empty(self):
        """Test mencari dengan NIM kosong."""
        _, service, temp_db = self._setup()
        try:
            user = service.get_user_by_nim("")
            assert user is None
        finally:
            os.remove(temp_db)

    def test_get_user_by_id(self):
        """Test mencari pengguna berdasarkan ID."""
        _, service, temp_db = self._setup()
        try:
            _, _, user_id = service.add_user("12345", "Yudhistira")
            user = service.get_user_by_id(user_id)
            assert user is not None
            assert user.id == user_id
            assert user.nim == "12345"
        finally:
            os.remove(temp_db)

    def test_get_all_users(self):
        """Test mengambil semua pengguna."""
        _, service, temp_db = self._setup()
        try:
            service.add_user("111", "User A")
            service.add_user("222", "User B")
            service.add_user("333", "User C")
            users = service.get_all_users()
            assert len(users) == 3
        finally:
            os.remove(temp_db)

    def test_get_all_users_empty(self):
        """Test daftar pengguna kosong."""
        _, service, temp_db = self._setup()
        try:
            users = service.get_all_users()
            assert len(users) == 0
        finally:
            os.remove(temp_db)

    def test_delete_user(self):
        """Test menghapus pengguna."""
        _, service, temp_db = self._setup()
        try:
            service.add_user("12345", "Yudhistira")
            success, message = service.delete_user("12345")
            assert success, f"Seharusnya berhasil: {message}"
            assert "berhasil" in message.lower()

            # Pastikan user sudah tidak ada
            user = service.get_user_by_nim("12345")
            assert user is None
        finally:
            os.remove(temp_db)

    def test_delete_user_not_found(self):
        """Test menghapus pengguna yang tidak ada."""
        _, service, temp_db = self._setup()
        try:
            success, message = service.delete_user("99999")
            assert not success
            assert "tidak ditemukan" in message.lower()
        finally:
            os.remove(temp_db)

    def test_delete_user_empty_nim(self):
        """Test menghapus dengan NIM kosong."""
        _, service, temp_db = self._setup()
        try:
            success, message = service.delete_user("")
            assert not success
        finally:
            os.remove(temp_db)

    def test_update_face_encoding(self):
        """Test update face encoding pengguna."""
        _, service, temp_db = self._setup()
        try:
            _, _, user_id = service.add_user("12345", "Yudhistira")

            # Simulasi face encoding (bytes)
            fake_encoding = b"fake_face_encoding_data"
            success, message = service.update_face_encoding(user_id, fake_encoding)
            assert success

            # Verifikasi encoding tersimpan
            user = service.get_user_by_id(user_id)
            assert user.face_encoding is not None
            assert user.face_encoding == fake_encoding
        finally:
            os.remove(temp_db)

    def test_get_users_with_encoding(self):
        """Test mengambil pengguna yang sudah punya face encoding."""
        _, service, temp_db = self._setup()
        try:
            _, _, id1 = service.add_user("111", "User A")
            _, _, id2 = service.add_user("222", "User B")
            service.add_user("333", "User C")

            # Hanya user A dan B yang punya encoding
            service.update_face_encoding(id1, b"encoding_a")
            service.update_face_encoding(id2, b"encoding_b")

            users = service.get_all_users_with_encoding()
            assert len(users) == 2
        finally:
            os.remove(temp_db)

    def test_get_user_count(self):
        """Test menghitung jumlah pengguna."""
        _, service, temp_db = self._setup()
        try:
            assert service.get_user_count() == 0
            service.add_user("111", "User A")
            assert service.get_user_count() == 1
            service.add_user("222", "User B")
            assert service.get_user_count() == 2
            service.delete_user("111")
            assert service.get_user_count() == 1
        finally:
            os.remove(temp_db)


class TestUserModel:
    """Test model User."""

    def test_user_creation(self):
        """Test membuat instance User."""
        user = User(id=1, nim="12345", name="Yudhistira")
        assert user.id == 1
        assert user.nim == "12345"
        assert user.name == "Yudhistira"

    def test_user_str(self):
        """Test string representation User."""
        user = User(nim="12345", name="Yudhistira")
        assert "12345" in str(user)
        assert "Yudhistira" in str(user)

    def test_user_from_row_none(self):
        """Test User.from_row dengan None."""
        user = User.from_row(None)
        assert user is None
