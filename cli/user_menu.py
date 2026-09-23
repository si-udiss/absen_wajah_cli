"""
Modul cli/user_menu.py — Sub-menu pengelolaan data pengguna.

Menyediakan antarmuka CLI untuk:
- Tambah pengguna (tanpa face encoding, akan dilengkapi di Phase 3)
- Lihat daftar pengguna
- Cari pengguna berdasarkan NIM
- Hapus pengguna
"""

from services.user_service import UserService
from utils.helpers import (
    print_header,
    print_separator,
    print_success,
    print_error,
    print_info,
    print_warning,
    confirm_action,
    press_enter_to_continue,
)
from utils.validators import validate_nim, validate_name, validate_menu_input


def show_user_menu(db):
    """
    Tampilkan sub-menu data pengguna.

    Args:
        db: Instance Database.
    """
    user_service = UserService(db)

    while True:
        print_header("DATA PENGGUNA")
        print()
        print("  1. Tambah Pengguna")
        print("  2. Lihat Daftar Pengguna")
        print("  3. Cari Pengguna (NIM)")
        print("  4. Hapus Pengguna")
        print("  5. Kembali ke Menu Utama")
        print()

        choice = input("  Pilih menu: ").strip()

        is_valid, message = validate_menu_input(
            choice, ["1", "2", "3", "4", "5"]
        )

        if not is_valid:
            print_error(message)
            press_enter_to_continue()
            continue

        if choice == "1":
            _tambah_pengguna(user_service)
        elif choice == "2":
            _lihat_pengguna(user_service)
        elif choice == "3":
            _cari_pengguna(user_service)
        elif choice == "4":
            _hapus_pengguna(user_service)
        elif choice == "5":
            break


def _tambah_pengguna(user_service):
    """
    Form tambah pengguna baru.

    Catatan: Face encoding akan ditambahkan di Phase 3
    melalui menu Registrasi Pengguna di menu utama.
    """
    print_header("TAMBAH PENGGUNA")
    print()

    # Input NIM
    nim = input("  NIM  : ").strip()
    is_valid, message = validate_nim(nim)
    if not is_valid:
        print_error(message)
        press_enter_to_continue()
        return

    # Input Nama
    name = input("  Nama : ").strip()
    is_valid, message = validate_name(name)
    if not is_valid:
        print_error(message)
        press_enter_to_continue()
        return

    # Tambah pengguna (tanpa face encoding dulu)
    success, message, user_id = user_service.add_user(nim, name)

    if success:
        print_success(message)
        print_info(
            "Untuk mendaftarkan wajah, gunakan menu "
            "'Registrasi Pengguna' di menu utama."
        )
    else:
        print_error(message)

    press_enter_to_continue()


def _lihat_pengguna(user_service):
    """Tampilkan daftar semua pengguna."""
    print_header("DAFTAR PENGGUNA")
    print()

    users = user_service.get_all_users()

    if not users:
        print_info("Belum ada pengguna terdaftar.")
        press_enter_to_continue()
        return

    # Header tabel
    print(f"  {'No':<4} {'NIM':<15} {'Nama':<25} {'Wajah':<10} {'Terdaftar'}")
    print_separator()

    for i, user in enumerate(users, 1):
        face_status = "✓" if user.face_encoding else "✗"
        created = user.created_at[:10] if user.created_at else "-"
        print(f"  {i:<4} {user.nim:<15} {user.name:<25} {face_status:<10} {created}")

    print_separator()
    print(f"  Total: {len(users)} pengguna")

    press_enter_to_continue()


def _cari_pengguna(user_service):
    """Cari pengguna berdasarkan NIM."""
    print_header("CARI PENGGUNA")
    print()

    nim = input("  Masukkan NIM: ").strip()

    is_valid, message = validate_nim(nim)
    if not is_valid:
        print_error(message)
        press_enter_to_continue()
        return

    user = user_service.get_user_by_nim(nim)

    if user is None:
        print_warning(f"Pengguna dengan NIM '{nim}' tidak ditemukan.")
    else:
        print()
        print_separator()
        print(f"  ID         : {user.id}")
        print(f"  NIM        : {user.nim}")
        print(f"  Nama       : {user.name}")
        face_status = "Terdaftar" if user.face_encoding else "Belum terdaftar"
        print(f"  Wajah      : {face_status}")
        print(f"  Terdaftar  : {user.created_at}")
        print_separator()

    press_enter_to_continue()


def _hapus_pengguna(user_service):
    """Hapus pengguna berdasarkan NIM."""
    print_header("HAPUS PENGGUNA")
    print()

    nim = input("  Masukkan NIM yang akan dihapus: ").strip()

    is_valid, message = validate_nim(nim)
    if not is_valid:
        print_error(message)
        press_enter_to_continue()
        return

    # Cek user ada
    user = user_service.get_user_by_nim(nim)
    if user is None:
        print_warning(f"Pengguna dengan NIM '{nim}' tidak ditemukan.")
        press_enter_to_continue()
        return

    # Tampilkan data user yang akan dihapus
    print(f"\n  Data pengguna yang akan dihapus:")
    print(f"  NIM  : {user.nim}")
    print(f"  Nama : {user.name}")

    # Konfirmasi
    if not confirm_action("Apakah Anda yakin ingin menghapus pengguna ini?"):
        print_info("Penghapusan dibatalkan.")
        press_enter_to_continue()
        return

    success, message = user_service.delete_user(nim)

    if success:
        print_success(message)
    else:
        print_error(message)

    press_enter_to_continue()
