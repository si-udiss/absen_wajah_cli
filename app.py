"""
Sistem Absensi dengan Face Recognition — Entry Point

Aplikasi absensi berbasis CLI yang menggunakan face recognition
untuk verifikasi identitas pengguna.

Cara menjalankan:
    python app.py

Author: Yudhistira
"""

import sys

from config import APP_NAME, APP_VERSION
from database.database import Database
from cli.menu import show_main_menu
from utils.helpers import print_error, print_success


def initialize():
    """
    Inisialisasi aplikasi.

    - Membuat database jika belum ada
    - Menjalankan schema untuk membuat tabel

    Returns:
        Database: Instance database yang sudah diinisialisasi,
                  atau None jika gagal.
    """
    try:
        db = Database()
        print_success("Database berhasil diinisialisasi.")
        return db
    except FileNotFoundError as e:
        print_error(f"File tidak ditemukan: {e}")
        return None
    except Exception as e:
        print_error(f"Gagal inisialisasi aplikasi: {e}")
        return None


def main():
    """Entry point utama aplikasi."""
    print(f"\n{'=' * 48}")
    print(f" {APP_NAME} v{APP_VERSION}")
    print(f"{'=' * 48}")
    print("\nMemulai aplikasi...")

    # Inisialisasi database
    db = initialize()
    if db is None:
        print_error("Aplikasi tidak dapat dimulai.")
        sys.exit(1)

    # Jalankan menu utama dengan database instance
    try:
        show_main_menu(db)
    except KeyboardInterrupt:
        print("\n\nAplikasi dihentikan oleh pengguna.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Terjadi kesalahan: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
