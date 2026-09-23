"""
Konfigurasi aplikasi Sistem Absensi Face Recognition.

File ini berisi seluruh konstanta dan konfigurasi yang digunakan
oleh aplikasi. Semua nilai yang dapat dikonfigurasi dipusatkan
di sini agar mudah diubah dan di-maintain.
"""

from pathlib import Path

# ==============================================
# PATH CONFIGURATION
# ==============================================

# Root directory project
BASE_DIR = Path(__file__).resolve().parent

# Directory untuk menyimpan data (database)
DATA_DIR = BASE_DIR / "data"

# Path file database SQLite
DATABASE_PATH = DATA_DIR / "attendance.db"

# ==============================================
# DATABASE CONFIGURATION
# ==============================================

# Nama file schema SQL
SCHEMA_FILE = BASE_DIR / "database" / "schema.sql"

# ==============================================
# FACE RECOGNITION CONFIGURATION
# ==============================================

# Threshold untuk face distance.
# Semakin kecil nilainya, semakin ketat pencocokan wajah.
# Nilai default: 0.45
# Range yang disarankan: 0.4 - 0.6
# CATATAN: Threshold ini bukan jaminan keamanan absolut
# dan perlu pengujian dengan dataset wajah yang digunakan.
FACE_DISTANCE_THRESHOLD = 0.45

# ==============================================
# WEBCAM CONFIGURATION
# ==============================================

# Index kamera (0 = kamera default)
CAMERA_INDEX = 0

# Durasi countdown sebelum capture (dalam detik)
CAPTURE_COUNTDOWN = 3

# ==============================================
# ATTENDANCE CONFIGURATION
# ==============================================

# Status absensi yang tersedia
STATUS_HADIR = "HADIR"

# ==============================================
# APPLICATION INFO
# ==============================================

APP_NAME = "SISTEM ABSENSI FACE RECOGNITION"
APP_VERSION = "1.0.0"
