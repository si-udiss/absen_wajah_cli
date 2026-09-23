"""
Modul utils/camera.py — Utilitas akses webcam tanpa GUI.

Menyediakan fungsi untuk:
- Membuka dan menutup webcam
- Capture frame tanpa menampilkan window (tanpa cv2.imshow)
- Countdown melalui terminal sebelum capture

PENTING:
- TIDAK menggunakan cv2.imshow()
- TIDAK membuat window/GUI
- Semua interaksi melalui terminal/CLI
"""

import time
import sys

import cv2

from config import CAMERA_INDEX, CAPTURE_COUNTDOWN


def capture_frame(camera_index=None, countdown=None):
    """
    Capture satu frame dari webcam tanpa GUI.

    Proses:
    1. Buka webcam
    2. Tampilkan countdown di terminal
    3. Capture frame
    4. Release webcam

    Args:
        camera_index: Index kamera (default dari config).
        countdown: Durasi countdown dalam detik (default dari config).

    Returns:
        tuple: (success: bool, frame: numpy.ndarray atau None, message: str)
    """
    if camera_index is None:
        camera_index = CAMERA_INDEX
    if countdown is None:
        countdown = CAPTURE_COUNTDOWN

    cap = None
    try:
        # Buka webcam
        cap = cv2.VideoCapture(camera_index)

        if not cap.isOpened():
            return False, None, "Kamera tidak dapat dibuka. Pastikan webcam terhubung."

        # Biarkan kamera warm up
        # Baca beberapa frame untuk stabilisasi
        for _ in range(10):
            cap.read()

        # Countdown melalui terminal
        print()
        print("  Pastikan wajah berada di depan kamera.")
        print()
        print("  Capture dimulai dalam:")
        for i in range(countdown, 0, -1):
            sys.stdout.write(f"  {i}...\r")
            sys.stdout.flush()
            # Terus baca frame selama countdown agar buffer tidak stale
            cap.read()
            time.sleep(1)

        print("  Mengambil gambar...     ")

        # Capture frame
        ret, frame = cap.read()

        if not ret or frame is None:
            return False, None, "Gagal mengambil gambar dari kamera."

        return True, frame, "Gambar berhasil diambil."

    except Exception as e:
        return False, None, f"Error saat mengakses kamera: {e}"

    finally:
        # Pastikan kamera selalu di-release
        if cap is not None:
            cap.release()


def test_camera(camera_index=None):
    """
    Test apakah kamera tersedia dan bisa dibuka.

    Args:
        camera_index: Index kamera (default dari config).

    Returns:
        tuple: (available: bool, message: str)
    """
    if camera_index is None:
        camera_index = CAMERA_INDEX

    cap = None
    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            return False, "Kamera tidak tersedia."

        ret, frame = cap.read()
        if not ret or frame is None:
            return False, "Kamera terbuka tetapi tidak dapat membaca frame."

        return True, "Kamera tersedia dan berfungsi."

    except Exception as e:
        return False, f"Error saat menguji kamera: {e}"

    finally:
        if cap is not None:
            cap.release()
