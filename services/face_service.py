"""
Modul services/face_service.py — Service untuk face detection dan recognition.

Menyediakan fungsi untuk:
- Mendeteksi wajah dalam frame
- Membuat face encoding
- Membandingkan face encoding
- Serialisasi/deserialisasi encoding untuk penyimpanan di database

Menggunakan library face_recognition.

CATATAN KEAMANAN:
- Face encoding disimpan sebagai BLOB di SQLite menggunakan numpy tobytes/frombuffer
- Tidak menggunakan pickle untuk keamanan
- Face recognition pada project ini digunakan sebagai mekanisme identifikasi,
  bukan sebagai jaminan keamanan absolut
- Threshold perlu pengujian dengan dataset wajah yang digunakan
"""

import numpy as np
import face_recognition

from config import FACE_DISTANCE_THRESHOLD


def detect_faces(frame):
    """
    Deteksi wajah dalam frame.

    Args:
        frame: numpy.ndarray (BGR image dari OpenCV).

    Returns:
        tuple: (face_count: int, face_locations: list, message: str)
    """
    try:
        # Konversi BGR (OpenCV) ke RGB (face_recognition) dan pastikan contiguous
        rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])

        # Deteksi lokasi wajah
        face_locations = face_recognition.face_locations(rgb_frame)
        face_count = len(face_locations)

        if face_count == 0:
            return 0, [], "Tidak ada wajah yang terdeteksi."
        elif face_count == 1:
            return 1, face_locations, "Satu wajah terdeteksi."
        else:
            return face_count, face_locations, (
                f"Terdeteksi {face_count} wajah. "
                "Pastikan hanya ada satu wajah di depan kamera."
            )

    except Exception as e:
        return 0, [], f"Error saat mendeteksi wajah: {e}"


def create_face_encoding(frame, face_locations=None):
    """
    Buat face encoding dari frame.

    Args:
        frame: numpy.ndarray (BGR image dari OpenCV).
        face_locations: Lokasi wajah (opsional, akan dideteksi jika None).

    Returns:
        tuple: (success: bool, encoding: numpy.ndarray atau None, message: str)
    """
    try:
        # Konversi BGR ke RGB dan pastikan contiguous
        rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])

        # Deteksi lokasi wajah jika belum ada
        if face_locations is None:
            face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) == 0:
            return False, None, "Tidak ada wajah yang terdeteksi."

        if len(face_locations) > 1:
            return False, None, (
                f"Terdeteksi {len(face_locations)} wajah. "
                "Pastikan hanya ada satu wajah."
            )

        # Buat encoding untuk wajah pertama (satu-satunya)
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(encodings) == 0:
            return False, None, "Gagal membuat face encoding."

        return True, encodings[0], "Face encoding berhasil dibuat."

    except Exception as e:
        return False, None, f"Error saat membuat face encoding: {e}"


def compare_faces(known_encoding, unknown_encoding, threshold=None):
    """
    Bandingkan dua face encoding.

    Args:
        known_encoding: numpy.ndarray encoding wajah yang sudah dikenal.
        unknown_encoding: numpy.ndarray encoding wajah yang akan dicocokkan.
        threshold: Batas jarak maksimum (default dari config).

    Returns:
        tuple: (is_match: bool, distance: float, message: str)
    """
    if threshold is None:
        threshold = FACE_DISTANCE_THRESHOLD

    try:
        # Hitung face distance
        distances = face_recognition.face_distance(
            [known_encoding], unknown_encoding
        )
        distance = distances[0]

        is_match = distance <= threshold

        if is_match:
            confidence = round((1 - distance) * 100, 2)
            message = f"Wajah cocok (confidence: {confidence}%, distance: {distance:.4f})"
        else:
            message = f"Wajah tidak cocok (distance: {distance:.4f}, threshold: {threshold})"

        return is_match, distance, message

    except Exception as e:
        return False, 1.0, f"Error saat membandingkan wajah: {e}"


def find_matching_user(unknown_encoding, registered_users, threshold=None):
    """
    Cari pengguna yang cocok dari daftar pengguna terdaftar.

    Args:
        unknown_encoding: numpy.ndarray encoding wajah yang akan dicocokkan.
        registered_users: List of User objects yang memiliki face encoding.
        threshold: Batas jarak maksimum (default dari config).

    Returns:
        tuple: (user: User atau None, distance: float, message: str)
    """
    if threshold is None:
        threshold = FACE_DISTANCE_THRESHOLD

    if not registered_users:
        return None, 1.0, "Tidak ada pengguna terdaftar dengan face encoding."

    best_match = None
    best_distance = 1.0

    for user in registered_users:
        if user.face_encoding is None:
            continue

        # Deserialize encoding dari database
        known_encoding = deserialize_encoding(user.face_encoding)
        if known_encoding is None:
            continue

        is_match, distance, _ = compare_faces(
            known_encoding, unknown_encoding, threshold
        )

        if is_match and distance < best_distance:
            best_match = user
            best_distance = distance

    if best_match is not None:
        confidence = round((1 - best_distance) * 100, 2)
        return best_match, best_distance, (
            f"Wajah dikenali: {best_match.name} "
            f"(NIM: {best_match.nim}, confidence: {confidence}%)"
        )
    else:
        return None, best_distance, "Wajah tidak dikenali."


def serialize_encoding(encoding):
    """
    Serialisasi face encoding ke bytes untuk penyimpanan di database.

    Menggunakan numpy tobytes() untuk keamanan (tidak menggunakan pickle).

    Args:
        encoding: numpy.ndarray face encoding.

    Returns:
        bytes: Encoding dalam format bytes.
    """
    if encoding is None:
        return None
    return encoding.astype(np.float64).tobytes()


def deserialize_encoding(encoding_bytes):
    """
    Deserialisasi face encoding dari bytes database.

    Args:
        encoding_bytes: bytes data encoding dari database.

    Returns:
        numpy.ndarray: Face encoding, atau None jika gagal.
    """
    if encoding_bytes is None:
        return None
    try:
        return np.frombuffer(encoding_bytes, dtype=np.float64)
    except Exception:
        return None
