"""
Modul cli/menu.py — Menu utama aplikasi.

Menampilkan menu utama CLI dan mengarahkan user ke sub-menu
berdasarkan pilihan.
"""

from config import APP_NAME
from utils.helpers import (
    print_header,
    print_error,
    print_info,
    print_success,
    print_warning,
    press_enter_to_continue,
)
from utils.validators import validate_nim, validate_name, validate_menu_input
from cli.user_menu import show_user_menu
from cli.report_menu import show_report_menu
from services.user_service import UserService
from services.attendance_service import AttendanceService
from services.face_service import (
    detect_faces,
    create_face_encoding,
    serialize_encoding,
    find_matching_user,
)
from utils.camera import capture_frame


def show_main_menu(db):
    """
    Tampilkan dan jalankan menu utama aplikasi.

    Args:
        db: Instance Database untuk diteruskan ke sub-menu.
    """
    while True:
        print_header(APP_NAME)
        print()
        print("  1. Registrasi Pengguna")
        print("  2. Absensi")
        print("  3. Data Pengguna")
        print("  4. Rekap Absensi")
        print("  5. Keluar")
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
            _menu_registrasi(db)
        elif choice == "2":
            _menu_absensi(db)
        elif choice == "3":
            show_user_menu(db)
        elif choice == "4":
            show_report_menu(db)
        elif choice == "5":
            print("\nTerima kasih telah menggunakan sistem absensi.")
            print("Sampai jumpa!\n")
            break


def _menu_registrasi(db):
    """
    Menu registrasi pengguna lengkap dengan face capture.

    Alur:
    1. Input NIM dan nama
    2. Validasi input
    3. Capture wajah via webcam (tanpa GUI)
    4. Deteksi wajah (harus tepat 1)
    5. Buat face encoding
    6. Simpan pengguna + encoding ke database
    """
    user_service = UserService(db)

    print_header("REGISTRASI PENGGUNA")
    print()

    # Input NIM
    nim = input("  NIM  : ").strip()
    is_valid, message = validate_nim(nim)
    if not is_valid:
        print_error(message)
        press_enter_to_continue()
        return

    # Cek NIM duplikat
    existing = user_service.get_user_by_nim(nim)
    
    name = ""
    is_updating_face = False
    
    if existing is not None:
        if existing.face_encoding is not None:
            print_error(f"NIM '{nim}' sudah terdaftar dan wajah sudah diregistrasi atas nama {existing.name}.")
            press_enter_to_continue()
            return
        else:
            print_info(f"Pengguna ditemukan (Nama: {existing.name}). Melanjutkan registrasi wajah...")
            name = existing.name
            is_updating_face = True
    else:
        # Input Nama
        name = input("  Nama : ").strip()
        is_valid, message = validate_name(name)
        if not is_valid:
            print_error(message)
            press_enter_to_continue()
            return

    # Capture wajah
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        print(f"\n  Percobaan capture wajah ({attempt}/{max_attempts})")

        success, frame, msg = capture_frame()

        if not success:
            print_error(msg)
            if attempt < max_attempts:
                retry = input("\n  Coba lagi? (y/n): ").strip().lower()
                if retry != 'y':
                    print_info("Registrasi dibatalkan.")
                    press_enter_to_continue()
                    return
                continue
            else:
                print_error("Gagal mengambil gambar setelah beberapa percobaan.")
                press_enter_to_continue()
                return

        # Deteksi wajah
        face_count, face_locations, msg = detect_faces(frame)
        print(f"  {msg}")

        if face_count == 0:
            print_warning("Tidak ada wajah terdeteksi.")
            if attempt < max_attempts:
                retry = input("\n  Coba lagi? (y/n): ").strip().lower()
                if retry != 'y':
                    print_info("Registrasi dibatalkan.")
                    press_enter_to_continue()
                    return
                continue
            else:
                print_error("Gagal mendeteksi wajah setelah beberapa percobaan.")
                press_enter_to_continue()
                return

        if face_count > 1:
            print_warning("Pastikan hanya ada satu wajah di depan kamera.")
            if attempt < max_attempts:
                retry = input("\n  Coba lagi? (y/n): ").strip().lower()
                if retry != 'y':
                    print_info("Registrasi dibatalkan.")
                    press_enter_to_continue()
                    return
                continue
            else:
                print_error("Terlalu banyak wajah terdeteksi.")
                press_enter_to_continue()
                return

        # Buat face encoding
        print("  Membuat face encoding...")
        enc_success, encoding, enc_msg = create_face_encoding(
            frame, face_locations
        )

        if not enc_success:
            print_error(enc_msg)
            if attempt < max_attempts:
                retry = input("\n  Coba lagi? (y/n): ").strip().lower()
                if retry != 'y':
                    print_info("Registrasi dibatalkan.")
                    press_enter_to_continue()
                    return
                continue
            else:
                print_error("Gagal membuat face encoding.")
                press_enter_to_continue()
                return

        # Serialisasi encoding untuk penyimpanan
        encoding_bytes = serialize_encoding(encoding)

        # Simpan pengguna ke database
        if is_updating_face:
            add_success, add_msg = user_service.update_face_encoding(existing.id, encoding_bytes)
        else:
            add_success, add_msg, user_id = user_service.add_user(
                nim, name, encoding_bytes
            )

        if add_success:
            print_success("Registrasi berhasil!")
            print(f"\n  NIM  : {nim}")
            print(f"  Nama : {name}")
            print(f"  Wajah: Terdaftar")
        else:
            print_error(add_msg)

        press_enter_to_continue()
        return

    # Jika semua percobaan gagal
    print_error("Registrasi gagal setelah semua percobaan.")
    press_enter_to_continue()


def _menu_absensi(db):
    """
    Menu absensi pengguna (Face Recognition).

    Alur:
    1. Ambil daftar pengguna terdaftar yang punya encoding wajah.
    2. Capture wajah via webcam.
    3. Deteksi dan encoding wajah.
    4. Cari kecocokan wajah.
    5. Jika cocok, catat absensi.
    """
    user_service = UserService(db)
    attendance_service = AttendanceService(db)

    print_header("ABSENSI")
    print()

    # Ambil pengguna terdaftar
    registered_users = user_service.get_all_users_with_encoding()

    if not registered_users:
        print_error("Belum ada pengguna terdaftar dengan data wajah.")
        press_enter_to_continue()
        return

    print("  Siapkan diri Anda di depan kamera.")
    
    # Capture wajah
    success, frame, msg = capture_frame()
    if not success:
        print_error(msg)
        press_enter_to_continue()
        return

    # Deteksi dan buat encoding
    print("  Memproses wajah...")
    enc_success, unknown_encoding, enc_msg = create_face_encoding(frame)

    if not enc_success:
        print_error(enc_msg)
        press_enter_to_continue()
        return

    # Cari kecocokan wajah
    print("  Mencocokkan wajah...")
    match_user, distance, match_msg = find_matching_user(
        unknown_encoding, registered_users
    )

    if match_user is None:
        print_error(match_msg)
        press_enter_to_continue()
        return

    print_success(match_msg)

    # Catat absensi
    record_success, record_msg = attendance_service.record_attendance(match_user.id)

    if record_success:
        print_success(record_msg)
    else:
        print_error(record_msg)

    press_enter_to_continue()
