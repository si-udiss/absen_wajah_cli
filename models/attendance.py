"""
Modul models/attendance.py — Model data absensi.

Representasi data kehadiran pengguna dalam aplikasi.
"""


class Attendance:
    """
    Model data absensi.

    Attributes:
        id: ID unik absensi (auto-increment).
        user_id: ID pengguna yang melakukan absensi.
        attendance_date: Tanggal absensi (format: YYYY-MM-DD).
        attendance_time: Waktu absensi (format: HH:MM:SS).
        status: Status kehadiran (default: HADIR).
        created_at: Timestamp pembuatan record.
        nim: NIM pengguna (dari JOIN query).
        name: Nama pengguna (dari JOIN query).
    """

    def __init__(self, id=None, user_id=None, attendance_date=None,
                 attendance_time=None, status=None, created_at=None,
                 nim=None, name=None):
        self.id = id
        self.user_id = user_id
        self.attendance_date = attendance_date
        self.attendance_time = attendance_time
        self.status = status
        self.created_at = created_at
        self.nim = nim
        self.name = name

    @classmethod
    def from_row(cls, row):
        """
        Buat instance Attendance dari sqlite3.Row.

        Args:
            row: sqlite3.Row hasil query database.

        Returns:
            Attendance: Instance Attendance baru, atau None jika row None.
        """
        if row is None:
            return None

        keys = row.keys()
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            attendance_date=row["attendance_date"],
            attendance_time=row["attendance_time"],
            status=row["status"],
            created_at=row["created_at"],
            nim=row["nim"] if "nim" in keys else None,
            name=row["name"] if "name" in keys else None,
        )

    def __repr__(self):
        return (
            f"Attendance(id={self.id}, user_id={self.user_id}, "
            f"date='{self.attendance_date}', status='{self.status}')"
        )

    def __str__(self):
        return (
            f"{self.attendance_date} {self.attendance_time} - "
            f"{self.status}"
        )
