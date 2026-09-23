"""
Modul services/attendance_service.py — Business logic pencatatan absensi.

Menyediakan operasi untuk:
- Mencatat absensi (dengan pencegahan duplikat per hari)
- Cek apakah user sudah absen hari ini
- Lihat seluruh absensi
- Cari absensi berdasarkan NIM
- Filter absensi berdasarkan tanggal
- Menghitung jumlah kehadiran pengguna
"""

import sqlite3
from datetime import date, datetime

from models.attendance import Attendance
from config import STATUS_HADIR


class AttendanceService:
    """
    Service untuk mengelola data absensi.

    Semua operasi database menggunakan parameterized queries.
    """

    def __init__(self, database):
        """
        Inisialisasi AttendanceService.

        Args:
            database: Instance Database untuk operasi database.
        """
        self.db = database

    def record_attendance(self, user_id):
        """
        Catat absensi pengguna.

        Mencegah absensi ganda pada hari yang sama melalui
        UNIQUE constraint di database.

        Args:
            user_id: ID pengguna yang melakukan absensi.

        Returns:
            tuple: (success: bool, message: str)
        """
        today = date.today().isoformat()
        now = datetime.now().strftime("%H:%M:%S")

        # Cek apakah sudah absen hari ini
        already_attended = self.has_attended_today(user_id)
        if already_attended:
            return False, "Pengguna sudah melakukan absensi hari ini."

        try:
            self.db.execute(
                "INSERT INTO attendance (user_id, attendance_date, attendance_time, status) "
                "VALUES (?, ?, ?, ?)",
                (user_id, today, now, STATUS_HADIR)
            )
            return True, f"Absensi berhasil dicatat pada {today} pukul {now}."
        except sqlite3.IntegrityError:
            return False, "Pengguna sudah melakukan absensi hari ini."
        except sqlite3.Error as e:
            return False, f"Gagal mencatat absensi: {e}"

    def has_attended_today(self, user_id):
        """
        Cek apakah pengguna sudah absen hari ini.

        Args:
            user_id: ID pengguna.

        Returns:
            bool: True jika sudah absen hari ini.
        """
        today = date.today().isoformat()
        row = self.db.fetch_one(
            "SELECT id FROM attendance WHERE user_id = ? AND attendance_date = ?",
            (user_id, today)
        )
        return row is not None

    def get_all_attendance(self):
        """
        Ambil seluruh data absensi dengan informasi pengguna.

        Returns:
            list[Attendance]: Daftar semua absensi.
        """
        rows = self.db.fetch_all(
            "SELECT a.id, a.user_id, a.attendance_date, a.attendance_time, "
            "a.status, a.created_at, u.nim, u.name "
            "FROM attendance a "
            "JOIN users u ON a.user_id = u.id "
            "ORDER BY a.attendance_date DESC, a.attendance_time DESC"
        )
        return [Attendance.from_row(row) for row in rows]

    def get_attendance_by_nim(self, nim):
        """
        Cari absensi berdasarkan NIM pengguna.

        Args:
            nim: NIM pengguna.

        Returns:
            list[Attendance]: Daftar absensi pengguna.
        """
        rows = self.db.fetch_all(
            "SELECT a.id, a.user_id, a.attendance_date, a.attendance_time, "
            "a.status, a.created_at, u.nim, u.name "
            "FROM attendance a "
            "JOIN users u ON a.user_id = u.id "
            "WHERE u.nim = ? "
            "ORDER BY a.attendance_date DESC, a.attendance_time DESC",
            (nim,)
        )
        return [Attendance.from_row(row) for row in rows]

    def get_attendance_by_date(self, target_date):
        """
        Filter absensi berdasarkan tanggal.

        Args:
            target_date: Tanggal yang dicari (format: YYYY-MM-DD).

        Returns:
            list[Attendance]: Daftar absensi pada tanggal tersebut.
        """
        rows = self.db.fetch_all(
            "SELECT a.id, a.user_id, a.attendance_date, a.attendance_time, "
            "a.status, a.created_at, u.nim, u.name "
            "FROM attendance a "
            "JOIN users u ON a.user_id = u.id "
            "WHERE a.attendance_date = ? "
            "ORDER BY a.attendance_time ASC",
            (target_date,)
        )
        return [Attendance.from_row(row) for row in rows]

    def get_attendance_count_by_user(self, user_id):
        """
        Hitung jumlah kehadiran pengguna.

        Args:
            user_id: ID pengguna.

        Returns:
            int: Jumlah kehadiran.
        """
        row = self.db.fetch_one(
            "SELECT COUNT(*) as count FROM attendance WHERE user_id = ?",
            (user_id,)
        )
        return row["count"] if row else 0

    def get_attendance_summary(self):
        """
        Ambil ringkasan kehadiran semua pengguna.

        Returns:
            list[dict]: Daftar ringkasan {nim, name, total_hadir}.
        """
        rows = self.db.fetch_all(
            "SELECT u.nim, u.name, COUNT(a.id) as total_hadir "
            "FROM users u "
            "LEFT JOIN attendance a ON u.id = a.user_id "
            "GROUP BY u.id "
            "ORDER BY u.nim"
        )
        return [
            {
                "nim": row["nim"],
                "name": row["name"],
                "total_hadir": row["total_hadir"],
            }
            for row in rows
        ]
