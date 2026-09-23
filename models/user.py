"""
Modul models/user.py — Model data pengguna.

Representasi data pengguna dalam aplikasi.
"""


class User:
    """
    Model data pengguna.

    Attributes:
        id: ID unik pengguna (auto-increment dari database).
        nim: Nomor Induk Mahasiswa, harus unik.
        name: Nama lengkap pengguna.
        face_encoding: Data encoding wajah (bytes/BLOB), bisa None.
        created_at: Timestamp pembuatan record.
    """

    def __init__(self, id=None, nim=None, name=None,
                 face_encoding=None, created_at=None):
        self.id = id
        self.nim = nim
        self.name = name
        self.face_encoding = face_encoding
        self.created_at = created_at

    @classmethod
    def from_row(cls, row):
        """
        Buat instance User dari sqlite3.Row.

        Args:
            row: sqlite3.Row hasil query database.

        Returns:
            User: Instance User baru, atau None jika row None.
        """
        if row is None:
            return None
        return cls(
            id=row["id"],
            nim=row["nim"],
            name=row["name"],
            face_encoding=row["face_encoding"],
            created_at=row["created_at"],
        )

    def __repr__(self):
        return f"User(id={self.id}, nim='{self.nim}', name='{self.name}')"

    def __str__(self):
        return f"{self.nim} - {self.name}"
