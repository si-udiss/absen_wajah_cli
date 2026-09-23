"""
Modul utils/validators.py — Validasi input pengguna.

Berisi fungsi-fungsi untuk memvalidasi input dari terminal.
"""


def validate_nim(nim):
    """
    Validasi format NIM.

    Args:
        nim: String NIM yang akan divalidasi.

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not nim or not nim.strip():
        return False, "NIM tidak boleh kosong."

    nim = nim.strip()

    if not nim.isalnum():
        return False, "NIM hanya boleh berisi huruf dan angka."

    return True, "NIM valid."


def validate_name(name):
    """
    Validasi nama pengguna.

    Args:
        name: String nama yang akan divalidasi.

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Nama tidak boleh kosong."

    return True, "Nama valid."


def validate_menu_input(choice, valid_options):
    """
    Validasi input menu.

    Args:
        choice: String input dari user.
        valid_options: List pilihan yang valid.

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not choice or not choice.strip():
        return False, "Input tidak boleh kosong."

    if choice.strip() not in valid_options:
        options_str = ", ".join(valid_options)
        return False, f"Pilihan tidak valid. Pilihan yang tersedia: {options_str}"

    return True, "Input valid."
