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
    Capture satu frame dari webcam dengan memunculkan popup (GUI).

    Proses:
    1. Buka webcam
    2. Tampilkan window cv2.imshow
    3. Lakukan countdown sambil menampilkan live preview
    4. Capture frame
    5. Tutup window & release webcam

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
        # Buka webcam (Gunakan CAP_DSHOW di Windows untuk menghindari hang)
        if sys.platform == 'win32':
            cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            if not cap.isOpened():
                cap = cv2.VideoCapture(camera_index)
        else:
            cap = cv2.VideoCapture(camera_index)

        if not cap.isOpened():
            return False, None, "Kamera tidak dapat dibuka. Pastikan webcam terhubung."

        # Biarkan kamera warm up
        for _ in range(10):
            cap.read()

        print("\n  Membuka kamera... (Lihat popup window)")
        print("  Pastikan wajah berada di depan kamera.")
        
        window_name = "Camera Preview - Face Recognition"
        
        # Countdown loop
        start_time = time.time()
        captured_frame = None
        
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                return False, None, "Gagal mengambil gambar dari kamera."
                
            # Hitung sisa waktu
            elapsed = time.time() - start_time
            remaining = int(countdown - elapsed) + 1
            
            # Buat copy frame untuk ditambahkan teks (agar frame asli bersih)
            display_frame = frame.copy()
            
            if remaining > 0:
                text = f"Memotret dalam: {remaining}..."
                color = (0, 255, 255) # Kuning
            else:
                text = "Mengambil gambar..."
                color = (0, 255, 0) # Hijau
                
            # Tambahkan teks ke display_frame
            cv2.putText(
                display_frame, text, (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA
            )
            
            cv2.imshow(window_name, display_frame)
            
            # Perbarui window dan cek tombol (tekan 'q' untuk batal)
            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                cv2.destroyWindow(window_name)
                return False, None, "Dibatalkan oleh pengguna."
                
            if remaining <= 0:
                captured_frame = frame.copy()
                break

        # Tutup window
        cv2.destroyWindow(window_name)
        cv2.waitKey(1) # Penting untuk mencegah auto-close/crash di Windows

        if captured_frame is not None:
            return True, captured_frame, "Gambar berhasil diambil."
        else:
            return False, None, "Gagal menangkap frame."

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
        if sys.platform == 'win32':
            cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            if not cap.isOpened():
                cap = cv2.VideoCapture(camera_index)
        else:
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
