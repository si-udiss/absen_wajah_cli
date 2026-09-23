"""
Test Phase 4, 5, 6 — Attendance and Reports.

Test untuk memverifikasi:
1. Absensi dicatat dengan benar
2. Pencegahan double attendance (1 hari 1 kali per user)
3. Ambil semua absensi
4. Ambil absensi by NIM
5. Filter absensi by date
6. Jumlah kehadiran per pengguna
"""

import os
import sys
import tempfile
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import Database
from services.user_service import UserService
from services.attendance_service import AttendanceService
from models.attendance import Attendance


class TestAttendanceService:
    """Test CRUD dan logic absensi."""

    def _setup(self):
        """Buat database dan services sementara untuk testing."""
        temp_dir = tempfile.mkdtemp()
        temp_db = os.path.join(temp_dir, "test_attendance_service.db")
        db = Database(db_path=temp_db)
        user_service = UserService(db)
        attendance_service = AttendanceService(db)
        return db, user_service, attendance_service, temp_db

    def test_record_attendance_success(self):
        """Test mencatat absensi berhasil."""
        _, user_service, attendance_service, temp_db = self._setup()
        try:
            _, _, user_id = user_service.add_user("12345", "Yudhistira")
            success, message = attendance_service.record_attendance(user_id)
            
            assert success, f"Seharusnya berhasil mencatat absensi: {message}"
            assert "berhasil" in message.lower()
            
            # Verifikasi di DB
            records = attendance_service.get_all_attendance()
            assert len(records) == 1
            assert records[0].user_id == user_id
            assert records[0].nim == "12345"
            assert records[0].status == "HADIR"
        finally:
            os.remove(temp_db)

    def test_record_attendance_duplicate(self):
        """Test mencatat absensi ganda pada hari yang sama ditolak."""
        _, user_service, attendance_service, temp_db = self._setup()
        try:
            _, _, user_id = user_service.add_user("12345", "Yudhistira")
            
            # Absensi pertama
            success1, _ = attendance_service.record_attendance(user_id)
            assert success1
            
            # Absensi kedua (hari ini)
            success2, message2 = attendance_service.record_attendance(user_id)
            assert not success2, "Seharusnya absensi ganda ditolak"
            assert "sudah" in message2.lower()
            
            # Verifikasi record hanya ada 1
            records = attendance_service.get_all_attendance()
            assert len(records) == 1
        finally:
            os.remove(temp_db)

    def test_has_attended_today(self):
        """Test fungsi cek apakah sudah absen hari ini."""
        _, user_service, attendance_service, temp_db = self._setup()
        try:
            _, _, user_id = user_service.add_user("12345", "Yudhistira")
            
            # Belum absen
            assert not attendance_service.has_attended_today(user_id)
            
            # Setelah absen
            attendance_service.record_attendance(user_id)
            assert attendance_service.has_attended_today(user_id)
        finally:
            os.remove(temp_db)

    def test_get_attendance_by_nim(self):
        """Test filter absensi berdasarkan NIM."""
        _, user_service, attendance_service, temp_db = self._setup()
        try:
            _, _, id1 = user_service.add_user("111", "User A")
            _, _, id2 = user_service.add_user("222", "User B")
            
            attendance_service.record_attendance(id1)
            attendance_service.record_attendance(id2)
            
            records_111 = attendance_service.get_attendance_by_nim("111")
            assert len(records_111) == 1
            assert records_111[0].nim == "111"
            
            records_999 = attendance_service.get_attendance_by_nim("999")
            assert len(records_999) == 0
        finally:
            os.remove(temp_db)

    def test_get_attendance_by_date(self):
        """Test filter absensi berdasarkan tanggal."""
        _, user_service, attendance_service, temp_db = self._setup()
        try:
            _, _, id1 = user_service.add_user("111", "User A")
            attendance_service.record_attendance(id1)
            
            today_str = date.today().isoformat()
            
            records_today = attendance_service.get_attendance_by_date(today_str)
            assert len(records_today) == 1
            assert records_today[0].user_id == id1
            
            records_other = attendance_service.get_attendance_by_date("2020-01-01")
            assert len(records_other) == 0
        finally:
            os.remove(temp_db)

    def test_get_attendance_count_by_user(self):
        """Test menghitung jumlah kehadiran spesifik user."""
        _, user_service, attendance_service, temp_db = self._setup()
        try:
            _, _, id1 = user_service.add_user("111", "User A")
            
            assert attendance_service.get_attendance_count_by_user(id1) == 0
            
            attendance_service.record_attendance(id1)
            assert attendance_service.get_attendance_count_by_user(id1) == 1
        finally:
            os.remove(temp_db)

    def test_get_attendance_summary(self):
        """Test mengambil summary kehadiran semua user."""
        _, user_service, attendance_service, temp_db = self._setup()
        try:
            _, _, id1 = user_service.add_user("111", "User A")
            _, _, id2 = user_service.add_user("222", "User B")
            
            attendance_service.record_attendance(id1)
            
            summary = attendance_service.get_attendance_summary()
            assert len(summary) == 2
            
            # User A punya 1 absen
            user_a_summary = next(s for s in summary if s["nim"] == "111")
            assert user_a_summary["total_hadir"] == 1
            
            # User B punya 0 absen
            user_b_summary = next(s for s in summary if s["nim"] == "222")
            assert user_b_summary["total_hadir"] == 0
        finally:
            os.remove(temp_db)
