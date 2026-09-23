# Sistem Absensi Face Recognition

Sistem absensi berbasis Python Command Line Interface (CLI) menggunakan Face Recognition. Project ini dirancang untuk menyelesaikan masalah "Absensi yang tidak akurat dan dapat dimanipulasi".

## Fitur Utama

*   **100% CLI**: Tidak ada GUI/Window yang mengganggu (bahkan untuk capture webcam).
*   **Registrasi Pengguna & Wajah**: Registrasi data pengguna beserta wajahnya menggunakan webcam.
*   **Absensi Cepat**: Cukup hadapkan wajah ke kamera untuk melakukan verifikasi dan pencatatan absensi.
*   **Anti-Duplikasi**: Pencegahan absensi ganda pada hari yang sama.
*   **Data Pengguna**: Fitur CRUD data pengguna melalui terminal.
*   **Rekapitulasi Absensi**: Penampilan riwayat absensi, pencarian, filter, dan jumlah kehadiran.
*   **SQLite Database**: Penyimpanan data lokal, aman, tanpa instalasi server database.

## Teknologi

*   Python 3.x
*   OpenCV (`opencv-python`)
*   Face Recognition (`face_recognition`, `dlib`)
*   NumPy
*   SQLite
*   Pytest (Untuk testing)

## Batasan Project

1.  **Hanya CLI**: Tidak ada GUI (Tkinter/PyQt) atau Frontend Web (Flask/Django).
2.  **Webcam Tanpa Window**: Pengambilan gambar dari webcam dilakukan murni lewat command line tanpa fungsi `cv2.imshow()`.
3.  **Identifikasi Identitas**: Input identitas saat absen ditiadakan, sepenuhnya mengandalkan pengenalan wajah.

## Keamanan

*   Data encoding wajah disimpan dalam bentuk BLOB `bytes` (serialisasi via NumPy), **TIDAK MENGGUNAKAN** `pickle` demi mencegah celah injeksi kode.
*   Menggunakan parameterized queries di SQLite untuk menghindari SQL Injection.

## Struktur Project

```text
absen_wajah_cli/
│
├── app.py                   # Entry point aplikasi
├── config.py                # Konfigurasi sistem
├── requirements.txt         # Daftar dependencies
├── README.md                # Dokumentasi ini
│
├── database/                # Logika SQLite
│   ├── database.py
│   └── schema.sql
│
├── models/                  # Struktur data
│   ├── user.py
│   └── attendance.py
│
├── services/                # Business logic
│   ├── user_service.py
│   ├── face_service.py
│   └── attendance_service.py
│
├── cli/                     # Antarmuka Command Line
│   ├── menu.py
│   ├── user_menu.py
│   └── report_menu.py
│
├── utils/                   # Fungsi bantuan
│   ├── camera.py
│   ├── validators.py
│   └── helpers.py
│
├── data/                    # Penyimpanan Database
│   └── attendance.db
│
└── tests/                   # Unit test
    ├── test_phase1.py
    ├── test_user.py
    └── test_attendance.py
```

## Cara Instalasi

1.  **Clone / Unduh Project Ini**
    ```bash
    git clone https://github.com/si-udiss/absen_wajah_cli.git
    cd absen_wajah_cli
    ```

2.  **Buat Virtual Environment (Sangat Disarankan)**
    ```bash
    python -m venv .venv
    ```

3.  **Aktivasi Virtual Environment**
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    *   **Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```

4.  **Install Requirements**
    ```bash
    pip install -r requirements.txt
    ```
    *(Catatan: Menginstal library `face_recognition` / `dlib` di Windows mungkin memerlukan C++ Build Tools terpasang pada komputer Anda).*

## Cara Menjalankan Aplikasi

Setelah semua requirement terinstall dan berada dalam virtual environment, jalankan:

```bash
python app.py
```

## Panduan Penggunaan Singkat

1.  **Registrasi Wajah:**
    *   Pilih menu `[1] Registrasi Pengguna` di halaman awal.
    *   Masukkan NIM dan Nama yang valid.
    *   Sistem akan menghidupkan kamera dan memulai _countdown_. Pastikan wajah Anda jelas berada di depan kamera.
    *   Sistem akan merekam 1 wajah dan melakukan generate face encoding.

2.  **Melakukan Absensi:**
    *   Pilih menu `[2] Absensi`.
    *   Sistem akan membuka kamera tanpa meminta NIM.
    *   Jika wajah cocok dengan database, sistem akan menyapa dengan Nama dan mencatat kehadiran Anda di hari tersebut.

3.  **Melihat Rekap:**
    *   Pilih menu `[4] Rekap Absensi`.
    *   Pilih menu untuk melihat semua absensi, atau cari berdasarkan tanggal/NIM.

## Cara Menjalankan Testing

Pastikan telah menginstal library `pytest` dari `requirements.txt`.

Jalankan seluruh test suite menggunakan:
```bash
python -m pytest tests/ -v
```
