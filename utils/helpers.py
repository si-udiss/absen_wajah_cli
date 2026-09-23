"""
Modul utils/helpers.py — Fungsi-fungsi pembantu umum.

Berisi fungsi utilitas yang digunakan di berbagai bagian aplikasi.
"""

import os


def clear_screen():
    """Bersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """
    Tampilkan header dengan format yang konsisten.

    Args:
        title: Judul yang akan ditampilkan.
    """
    separator = "=" * 48
    print(f"\n{separator}")
    print(f" {title}")
    print(separator)


def print_separator():
    """Tampilkan garis pemisah."""
    print("-" * 48)


def print_success(message):
    """
    Tampilkan pesan sukses.

    Args:
        message: Pesan yang akan ditampilkan.
    """
    print(f"\n[SUKSES] {message}")


def print_error(message):
    """
    Tampilkan pesan error.

    Args:
        message: Pesan error yang akan ditampilkan.
    """
    print(f"\n[ERROR] {message}")


def print_warning(message):
    """
    Tampilkan pesan peringatan.

    Args:
        message: Pesan peringatan yang akan ditampilkan.
    """
    print(f"\n[PERINGATAN] {message}")


def print_info(message):
    """
    Tampilkan pesan informasi.

    Args:
        message: Pesan informasi yang akan ditampilkan.
    """
    print(f"\n[INFO] {message}")


def confirm_action(message):
    """
    Minta konfirmasi dari user (y/n).

    Args:
        message: Pesan konfirmasi.

    Returns:
        bool: True jika user menjawab 'y'.
    """
    while True:
        choice = input(f"\n{message} (y/n): ").strip().lower()
        if choice in ('y', 'n'):
            return choice == 'y'
        print("Input tidak valid. Masukkan 'y' atau 'n'.")


def press_enter_to_continue():
    """Tunggu user menekan Enter untuk melanjutkan."""
    input("\nTekan Enter untuk melanjutkan...")
