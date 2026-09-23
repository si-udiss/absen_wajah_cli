"""
Modul cli/report_menu.py — Sub-menu rekap absensi.

Menyediakan antarmuka CLI untuk:
- Lihat seluruh absensi
- Cari absensi berdasarkan NIM
- Filter absensi berdasarkan tanggal
- Menampilkan jumlah kehadiran pengguna
"""

from services.attendance_service import AttendanceService
from utils.helpers import (
    print_header,
    print_separator,
    print_error,
    print_info,
    print_warning,
    press_enter_to_continue,
)
from utils.validators import validate_menu_input, validate_nim


def show_report_menu(db):
    """
    Tampilkan sub-menu rekap absensi.

    Args:
        db: Instance Database.
    """
    attendance_service = AttendanceService(db)

    while True:
        print_header("REKAP ABSENSI")
        print()
        print("  1. Lihat Seluruh Absensi")
        print("  2. Cari Berdasarkan NIM")
        print("  3. Filter Berdasarkan Tanggal")
        print("  4. Jumlah Kehadiran Per Pengguna")
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
            _lihat_semua_absensi(attendance_service)
        elif choice == "2":
            _cari_absensi_nim(attendance_service)
        elif choice == "3":
            _filter_absensi_tanggal(attendance_service)
        elif choice == "4":
            _jumlah_kehadiran(attendance_service)
        elif choice == "5":
            break


def _print_attendance_table(records):
    """
    Tampilkan data absensi dalam format tabel.

    Args:
        records: List of Attendance objects.
    """
    if not records:
        print_info("Tidak ada data absensi.")
        return

    print()
    print(f"  {'No':<4} {'NIM':<15} {'Nama':<20} {'Tanggal':<12} {'Waktu':<10} {'Status'}")
    print_separator()

    for i, record in enumerate(records, 1):
        nim = record.nim or "-"
        name = record.name or "-"
        print(
            f"  {i:<4} {nim:<15} {name:<20} "
            f"{record.attendance_date:<12} {record.attendance_time:<10} "
            f"{record.status}"
        )

    print_separator()
    print(f"  Total: {len(records)} record")


def _lihat_semua_absensi(attendance_service):
    """Tampilkan seluruh data absensi."""
    print_header("SELURUH ABSENSI")

    records = attendance_service.get_all_attendance()
    _print_attendance_table(records)

    press_enter_to_continue()


def _cari_absensi_nim(attendance_service):
    """Cari absensi berdasarkan NIM."""
    print_header("CARI ABSENSI BERDASARKAN NIM")
    print()

    nim = input("  Masukkan NIM: ").strip()

    is_valid, message = validate_nim(nim)
    if not is_valid:
        print_error(message)
        press_enter_to_continue()
        return

    records = attendance_service.get_attendance_by_nim(nim)

    if not records:
        print_warning(f"Tidak ada data absensi untuk NIM '{nim}'.")
    else:
        print(f"\n  Absensi untuk NIM: {nim} ({records[0].name})")
        _print_attendance_table(records)

    press_enter_to_continue()


def _filter_absensi_tanggal(attendance_service):
    """Filter absensi berdasarkan tanggal."""
    print_header("FILTER ABSENSI BERDASARKAN TANGGAL")
    print()
    print("  Format tanggal: YYYY-MM-DD (contoh: 2026-09-23)")

    target_date = input("  Masukkan tanggal: ").strip()

    # Validasi format tanggal sederhana
    if not target_date or len(target_date) != 10:
        print_error("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
        press_enter_to_continue()
        return

    try:
        # Validasi bahwa tanggal valid
        parts = target_date.split("-")
        if len(parts) != 3:
            raise ValueError
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        from datetime import date
        date(year, month, day)  # Akan raise ValueError jika tidak valid
    except (ValueError, IndexError):
        print_error("Tanggal tidak valid. Gunakan format YYYY-MM-DD.")
        press_enter_to_continue()
        return

    records = attendance_service.get_attendance_by_date(target_date)

    if not records:
        print_warning(f"Tidak ada data absensi pada tanggal {target_date}.")
    else:
        print(f"\n  Absensi tanggal: {target_date}")
        _print_attendance_table(records)

    press_enter_to_continue()


def _jumlah_kehadiran(attendance_service):
    """Tampilkan jumlah kehadiran per pengguna."""
    print_header("JUMLAH KEHADIRAN PER PENGGUNA")
    print()

    summary = attendance_service.get_attendance_summary()

    if not summary:
        print_info("Belum ada pengguna terdaftar.")
        press_enter_to_continue()
        return

    print(f"  {'No':<4} {'NIM':<15} {'Nama':<25} {'Total Hadir'}")
    print_separator()

    for i, item in enumerate(summary, 1):
        print(
            f"  {i:<4} {item['nim']:<15} {item['name']:<25} "
            f"{item['total_hadir']}"
        )

    print_separator()
    print(f"  Total pengguna: {len(summary)}")

    press_enter_to_continue()
