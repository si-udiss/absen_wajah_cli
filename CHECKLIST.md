
```text
Saya ingin membangun project perangkat lunak bernama:

"Sistem Absensi dengan Face Recognition"

Project ini dibuat untuk menyelesaikan masalah:
"Absensi yang tidak akurat dan dapat dimanipulasi."

TUJUAN PROJECT
---------------
Buat aplikasi absensi berbasis Python yang dapat melakukan verifikasi identitas pengguna menggunakan Face Recognition, kemudian mencatat kehadiran secara otomatis.

ATURAN PALING PENTING:
1. PROJECT HARUS 100% CLI / Command Line Interface.
2. JANGAN membuat GUI dalam bentuk apa pun.
3. JANGAN menggunakan Tkinter.
4. JANGAN menggunakan PyQt/PySide.
5. JANGAN menggunakan Streamlit.
6. JANGAN menggunakan Flask/FastAPI/Django.
7. JANGAN membuat website.
8. JANGAN membuat aplikasi Android/mobile.
9. JANGAN membuat frontend HTML/CSS/JavaScript.
10. Semua interaksi pengguna harus melalui terminal/command prompt.
11. Jangan membuat dashboard berbasis browser.
12. Jangan menambahkan fitur di luar scope tanpa meminta persetujuan terlebih dahulu.

Catatan:
Penggunaan webcam diperbolehkan untuk mengambil gambar wajah, tetapi aplikasi TIDAK BOLEH membuat GUI atau window aplikasi. Proses capture harus dikendalikan melalui CLI/terminal, misalnya dengan countdown dan OpenCV VideoCapture tanpa cv2.imshow().

==================================================
1. TEKNOLOGI
==================================================

Gunakan:

- Python 3.x
- OpenCV untuk akses webcam dan image processing
- face_recognition untuk face detection dan face encoding
- SQLite sebagai database lokal
- NumPy jika dibutuhkan
- pathlib/os untuk manajemen file
- datetime untuk tanggal dan waktu
- argparse jika diperlukan untuk command-line arguments
- pytest untuk testing jika memungkinkan

Prioritaskan library yang sederhana, stabil, dan mudah dijelaskan dalam laporan tugas kuliah.

Jangan menggunakan database server seperti MySQL/PostgreSQL untuk versi awal.
Gunakan SQLite agar project mudah dijalankan secara lokal.

==================================================
2. FITUR UTAMA
==================================================

Project minimal harus memiliki fitur:

A. REGISTRASI PENGGUNA

User/admin dapat melakukan:

- Menambahkan pengguna baru
- Memasukkan NIM/ID
- Memasukkan nama
- Mengambil foto wajah menggunakan webcam
- Mendeteksi wajah
- Memastikan hanya terdapat satu wajah pada frame yang digunakan
- Membuat face encoding
- Menyimpan data pengguna
- Menyimpan face encoding secara aman dan terstruktur

Validasi:
- NIM/ID tidak boleh duplikat
- Nama tidak boleh kosong
- Wajah harus terdeteksi
- Harus tepat satu wajah
- Jika tidak ada wajah, ulangi proses
- Jika lebih dari satu wajah, minta pengguna mengulangi capture

B. FACE RECOGNITION / ABSENSI

User memilih menu absensi.

Alur:

1. Sistem meminta user bersiap di depan kamera.
2. Sistem melakukan countdown melalui terminal.
3. Webcam mengambil frame.
4. Sistem mendeteksi wajah.
5. Sistem membuat face encoding.
6. Encoding dibandingkan dengan data wajah yang sudah terdaftar.
7. Jika wajah cocok dengan confidence/distance di bawah threshold:
   - tampilkan identitas pengguna
   - catat absensi
8. Jika wajah tidak cocok:
   - tampilkan "Wajah tidak dikenali"
   - jangan mencatat absensi.

Jangan meminta user memasukkan NIM setelah face recognition untuk menentukan identitas.
Identitas harus diperoleh dari hasil face recognition.

C. PENCATATAN ABSENSI

Setiap absensi minimal menyimpan:

- ID absensi
- User ID
- NIM
- Nama
- Tanggal
- Waktu
- Status

Status minimal:
- HADIR

Jika diperlukan, struktur dapat dipersiapkan agar nantinya bisa dikembangkan menjadi:
- TERLAMBAT
- IZIN
- SAKIT
- ALPHA

Tetapi jangan mengimplementasikan fitur yang belum diperlukan tanpa alasan.

D. PENCEGAHAN ABSENSI GANDA

Dalam satu hari, satu pengguna tidak boleh tercatat hadir berkali-kali.

Jika user yang sama sudah melakukan absensi pada hari tersebut:

"Tampilkan bahwa pengguna sudah melakukan absensi hari ini."

Jangan membuat record absensi baru.

E. DATA PENGGUNA

CLI harus menyediakan menu:

- Tambah pengguna
- Lihat daftar pengguna
- Cari pengguna berdasarkan NIM
- Hapus pengguna
- Kembali ke menu utama

Saat pengguna dihapus:
- data pengguna harus dihapus dari database
- face encoding terkait juga harus dihapus
- pertimbangkan foreign key atau mekanisme cleanup yang jelas

F. REKAP ABSENSI

CLI harus menyediakan:

- Lihat seluruh absensi
- Cari absensi berdasarkan NIM
- Filter berdasarkan tanggal
- Menampilkan jumlah kehadiran pengguna

Output harus rapi dalam terminal.

==================================================
3. STRUKTUR CLI
==================================================

Buat menu utama seperti:

========================================
 SISTEM ABSENSI FACE RECOGNITION
========================================

1. Registrasi Pengguna
2. Absensi
3. Data Pengguna
4. Rekap Absensi
5. Keluar

Pilih menu:

Setiap menu harus memiliki validasi input dan penanganan error.

Jangan menggunakan GUI.

Semua informasi harus ditampilkan melalui terminal.

==================================================
4. DATABASE
==================================================

Gunakan SQLite.

Minimal buat tabel:

users
-----
id
nim
name
face_encoding
created_at

attendance
----------
id
user_id
attendance_date
attendance_time
status
created_at

Buat constraint yang mencegah absensi ganda pada tanggal yang sama.

Contoh konsep:

UNIQUE(user_id, attendance_date)

Gunakan foreign key antara attendance.user_id dan users.id.

Jangan menyimpan data database secara hardcoded.

Buat database otomatis jika belum tersedia.

==================================================
5. FACE ENCODING
==================================================

Gunakan library face_recognition.

Gunakan konsep:

- face_locations()
- face_encodings()
- face_distance()
- compare_faces()

Gunakan threshold yang dapat dikonfigurasi, jangan hardcode di banyak tempat.

Contoh:

FACE_DISTANCE_THRESHOLD = 0.45

Tetapi buat threshold sebagai configuration constant sehingga mudah diuji dan diubah.

Jelaskan dalam dokumentasi bahwa threshold bukan jaminan keamanan absolut dan perlu pengujian menggunakan dataset wajah yang digunakan.

==================================================
6. WEBCAM TANPA GUI
==================================================

Ini sangat penting.

Webcam BOLEH digunakan.

Namun:

JANGAN menggunakan:
cv2.imshow()

JANGAN membuat window kamera.

Gunakan:
cv2.VideoCapture()

Proses capture dilakukan melalui terminal.

Contoh:

========================================
 REGISTRASI WAJAH
========================================

Nama : Yudhistira
NIM  : 123456

Pastikan wajah berada di depan kamera.

Capture dimulai dalam:
3...
2...
1...

Mengambil gambar...

Wajah terdeteksi.
Membuat face encoding...

Registrasi berhasil.

Jika kamera gagal:
- tampilkan pesan error
- release camera
- jangan crash

Pastikan camera.release() selalu dipanggil.

==================================================
7. PENYIMPANAN FACE ENCODING
==================================================

Pilih mekanisme penyimpanan yang sederhana dan jelas.

Face encoding dapat disimpan sebagai BLOB atau serialized data yang aman untuk project lokal.

Jika menggunakan pickle:
- jelaskan risiko keamanan pickle
- jangan melakukan unpickle terhadap file dari sumber tidak terpercaya.

Lebih baik pertimbangkan penyimpanan encoding sebagai BLOB/bytes di SQLite atau format numerik yang lebih terkontrol.

Prioritaskan keamanan dan kemudahan maintenance.

==================================================
8. STRUKTUR PROJECT
==================================================

Buat struktur modular, jangan membuat satu file Python berisi seluruh program.

Gunakan struktur seperti:

face-attendance/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── database.py
│   └── schema.sql
│
├── models/
│   ├── user.py
│   └── attendance.py
│
├── services/
│   ├── face_service.py
│   ├── attendance_service.py
│   └── user_service.py
│
├── cli/
│   ├── menu.py
│   ├── user_menu.py
│   ├── attendance_menu.py
│   └── report_menu.py
│
├── utils/
│   ├── camera.py
│   ├── validators.py
│   └── helpers.py
│
├── data/
│   └── attendance.db
│
└── tests/
    ├── test_user.py
    ├── test_attendance.py
    └── test_validators.py

Jika ada alasan teknis untuk mengubah struktur, jelaskan terlebih dahulu.

==================================================
9. ERROR HANDLING
==================================================

Aplikasi tidak boleh langsung crash karena kesalahan input user.

Tangani minimal:

- Input menu tidak valid
- NIM kosong
- NIM duplikat
- User tidak ditemukan
- Kamera tidak tersedia
- Kamera gagal dibuka
- Tidak ada wajah
- Lebih dari satu wajah
- Wajah tidak dikenali
- Database error
- User sudah melakukan absensi hari ini

Gunakan pesan error yang jelas dan mudah dipahami.

==================================================
10. KEAMANAN
==================================================

Perhatikan:

- Jangan menyimpan password karena sistem tidak membutuhkan login/password.
- Jangan mencetak face encoding ke terminal.
- Jangan memasukkan data biometrik ke log.
- Validasi input pengguna.
- Gunakan parameterized SQL query.
- Jangan menggunakan SQL string concatenation untuk input user.
- Jangan menggunakan eval().
- Jangan menggunakan exec() untuk input user.
- Tangani file dan database dengan benar.

Catatan:
Face recognition pada project ini digunakan sebagai mekanisme identifikasi, bukan sebagai jaminan keamanan absolut.

==================================================
11. TESTING
==================================================

Buat unit test untuk:

1. Registrasi user berhasil
2. NIM duplikat ditolak
3. User berhasil dicari
4. User berhasil dihapus
5. Absensi berhasil dicatat
6. Absensi kedua pada hari yang sama ditolak
7. User tidak ditemukan
8. Data absensi dapat dicari
9. Input invalid ditangani

Untuk face recognition, buat fungsi yang terpisah sehingga logic database/business logic dapat diuji tanpa webcam.

==================================================
12. README
==================================================

Buat README.md yang menjelaskan:

1. Nama project
2. Deskripsi
3. Masalah yang diselesaikan
4. Fitur
5. Teknologi
6. Struktur project
7. Cara instalasi
8. Cara membuat virtual environment
9. Cara install requirements
10. Cara menjalankan aplikasi
11. Cara registrasi wajah
12. Cara melakukan absensi
13. Cara melihat rekap
14. Cara menjalankan testing
15. Batasan project
16. Catatan keamanan

Contoh:

python -m venv .venv

Windows:
.venv\Scripts\activate

pip install -r requirements.txt

python app.py

==================================================
13. BATASAN PROJECT
==================================================

Project ini sengaja dibatasi.

TIDAK BOLEH menambahkan:

- GUI
- Website
- REST API
- Mobile application
- GPS/geolocation
- RFID
- QR Code
- Cloud service
- WhatsApp notification
- Email notification
- Machine learning training model custom
- Dashboard web

Fokus hanya pada:

Python + CLI + Webcam + Face Recognition + SQLite.

==================================================
14. TAHAP PENGERJAAN
==================================================

Jangan langsung membuat seluruh project sekaligus tanpa validasi.

Kerjakan bertahap:

PHASE 1
-------
- Buat struktur project
- Buat virtual environment instructions
- Buat requirements.txt
- Buat config.py
- Buat database initialization
- Buat schema SQLite
- Pastikan database dapat dibuat

PHASE 2
-------
- Implementasi User model/service
- Registrasi user
- CRUD user
- Validasi NIM
- Testing user

PHASE 3
-------
- Implementasi camera service
- Implementasi face encoding
- Capture wajah melalui webcam tanpa GUI
- Registrasi face encoding

PHASE 4
-------
- Implementasi face recognition
- Matching wajah
- Threshold
- Handling wajah tidak dikenal

PHASE 5
-------
- Implementasi attendance service
- Pencatatan tanggal dan waktu
- Pencegahan absensi ganda
- Rekap absensi

PHASE 6
-------
- Integrasikan seluruh CLI menu
- Error handling
- Testing
- README
- Final cleanup

Setelah setiap phase selesai:
1. Jalankan test.
2. Periksa error.
3. Pastikan aplikasi masih dapat dijalankan.
4. Tampilkan ringkasan perubahan.
5. Jangan melanjutkan ke fitur berikutnya jika phase sebelumnya belum stabil.

==================================================
15. OUTPUT YANG SAYA INGINKAN SEKARANG
==================================================

Untuk tahap pertama, JANGAN langsung membuat semua fitur.

Mulai dari PHASE 1.

Tugas pertama:

1. Analisis requirement di atas.
2. Buat struktur folder project.
3. Buat requirements.txt.
4. Buat config.py.
5. Buat database/database.py.
6. Buat database/schema.sql.
7. Buat app.py sederhana.
8. Implementasikan initialization SQLite.
9. Buat CLI menu utama sederhana.
10. Pastikan program dapat dijalankan menggunakan:

python app.py

11. Pastikan database otomatis dibuat jika belum ada.
12. Jalankan test/sanity check.
13. Berikan laporan singkat:
    - file yang dibuat
    - fungsi masing-masing file
    - cara menjalankan
    - hasil testing
    - masalah yang ditemukan

Jangan mengimplementasikan face recognition terlebih dahulu sebelum PHASE 1 selesai.

INGAT:
PROJECT INI FULL CLI.
JANGAN MEMBUAT GUI.
JANGAN MEMBUAT WEB.
JANGAN MEMBUAT API.
JANGAN MENAMBAHKAN FITUR DI LUAR SCOPE.
```

## Checklist pengerjaan project

### 🟢 Phase 1 — Foundation

* [ ] Struktur folder dibuat
* [ ] Virtual environment
* [ ] `requirements.txt`
* [ ] `config.py`
* [ ] SQLite database
* [ ] `users` table
* [ ] `attendance` table
* [ ] Database initialization
* [ ] CLI main menu
* [ ] Error handling dasar
* [ ] Program bisa `python app.py`

### 🟢 Phase 2 — User Management

* [ ] Registrasi user
* [ ] Input NIM
* [ ] Input nama
* [ ] Validasi NIM
* [ ] Cek NIM duplikat
* [ ] Lihat user
* [ ] Cari user
* [ ] Hapus user
* [ ] Testing CRUD

### 🟢 Phase 3 — Face Registration

* [ ] Open webcam menggunakan `cv2.VideoCapture()`
* [ ] **Tanpa `cv2.imshow()`**
* [ ] Countdown melalui terminal
* [ ] Capture image
* [ ] Face detection
* [ ] Validasi 1 wajah
* [ ] Generate face encoding
* [ ] Simpan encoding
* [ ] Error handling kamera

### 🟢 Phase 4 — Face Recognition

* [ ] Ambil frame webcam
* [ ] Generate encoding
* [ ] Compare dengan database
* [ ] Face distance
* [ ] Configurable threshold
* [ ] Wajah dikenali
* [ ] Wajah tidak dikenali
* [ ] Multiple faces handling

### 🟢 Phase 5 — Attendance

* [ ] Identitas diperoleh dari face recognition
* [ ] Catat tanggal
* [ ] Catat waktu
* [ ] Status HADIR
* [ ] Cegah double attendance
* [ ] Tampilkan hasil absensi

### 🟢 Phase 6 — Rekap

* [ ] Semua absensi
* [ ] Cari berdasarkan NIM
* [ ] Filter tanggal
* [ ] Jumlah kehadiran
* [ ] Output tabel CLI

### 🟢 Phase 7 — Testing

* [ ] Test user
* [ ] Test duplicate NIM
* [ ] Test attendance
* [ ] Test duplicate attendance
* [ ] Test user tidak ditemukan
* [ ] Test invalid input
* [ ] Test face recognition secara terpisah
* [ ] Test error kamera

### 🟢 Phase 8 — Dokumentasi

* [ ] README
* [ ] Installation
* [ ] Usage
* [ ] Struktur project
* [ ] Database
* [ ] Face recognition
* [ ] Testing
* [ ] Limitations
* [ ] Security notes

### Satu keputusan penting untuk project kalian

Karena ini **FULL CLI**, aku sangat menyarankan alurnya jangan seperti aplikasi GUI yang memaksa webcam menampilkan preview. Gunakan pola:

```text
CLI
 │
 ├── [1] Registrasi Pengguna
 │       │
 │       └── Webcam → Capture → Face Encoding → Database
 │
 ├── [2] Absensi
 │       │
 │       └── Webcam → Capture → Face Recognition
 │                              │
 │                              ├── Dikenali
 │                              │     └── Simpan Absensi
 │                              │
 │                              └── Tidak dikenali
 │                                    └── Tolak Absensi
 │
 ├── [3] Data Pengguna
 │
 ├── [4] Rekap Absensi
 │
 └── [5] Keluar
```