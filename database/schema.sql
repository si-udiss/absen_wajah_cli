-- ============================================
-- Schema Database Sistem Absensi Face Recognition
-- ============================================

-- Tabel pengguna
-- Menyimpan data pengguna termasuk face encoding
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nim TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    face_encoding BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel absensi
-- Menyimpan catatan kehadiran pengguna
-- UNIQUE constraint pada (user_id, attendance_date) mencegah
-- absensi ganda pada hari yang sama
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    attendance_date DATE NOT NULL,
    attendance_time TIME NOT NULL,
    status TEXT NOT NULL DEFAULT 'HADIR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, attendance_date)
);

-- Index untuk mempercepat pencarian
CREATE INDEX IF NOT EXISTS idx_users_nim ON users(nim);
CREATE INDEX IF NOT EXISTS idx_attendance_user_id ON attendance(user_id);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(attendance_date);
