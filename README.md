# TrainMaster 🚀

TrainMaster adalah aplikasi untuk manajemen training model YOLO dengan tampilan GUI berbasis Tkinter. Dengan aplikasi ini, kamu bisa mengupload dataset, melakukan anotasi gambar, melakukan training model, hingga memanfaatkan webcam untuk prediksi.

---

## 💪 Anggota Tim
1. **Alnez Rainansantana	231524001**
2. **Carissa Amanda Chrisanty Lesmana	231524003**
3. **Farrel Zandra	231524007**
4. **Fitra Rifki Firdaus	231524008**
5. **Fitri Salwa	231524009**
6. **Fredy Kurniadi	231524010**
7. **Muhammad Rafif Genadratama	231524016**
8. **Nadia Rachma Yuninda	231524017**

---

## 🛠️ Library yang Dibutuhkan

Sebelum menjalankan aplikasi, pastikan kamu sudah menginstall library berikut di Python:

- **`ttkbootstrap`**: Untuk tampilan GUI yang modern dan responsif.
- **`tkinter`**: Untuk membuat antarmuka pengguna (GUI).
- **`messagebox`**: Untuk menampilkan pop-up notifikasi.

### Instalasi Library:

1. Pastikan kamu punya Python terinstall di komputer.
2. Jalankan perintah berikut untuk install **`ttkbootstrap`** dan **`tkinter`**:

```bash
pip install ttkbootstrap
Catatan: tkinter biasanya sudah terinstall dengan Python, jadi kamu nggak perlu install lagi.

🚀 Cara Menjalankan Aplikasi
Clone Repository:

Jika kamu belum meng-clone repositori, jalankan perintah berikut di terminal:

bash
Copy code
git clone https://github.com/username/repository.git
Masuk ke Folder Aplikasi:

Pindah ke folder project yang sudah kamu clone:

bash
Copy code
cd folder_project
Jalankan Aplikasi:

Cukup jalankan file main.py:

bash
Copy code
python main.py
Aplikasi akan terbuka di jendela baru, dan siap digunakan!

🧠 Paradigma yang Digunakan
Paradigma Pemrograman Berorientasi Objek (OOP)
Pada proyek ini, kita menggunakan Paradigma Pemrograman Berorientasi Objek (OOP). Paradigma ini fokus pada objek dan data, bukan hanya fungsi. Dengan OOP, setiap komponen aplikasi bisa dipandang sebagai objek dengan atribut dan metode yang saling berinteraksi.

Keuntungan OOP:
Modularitas: Dengan OOP, kita bisa membagi aplikasi ke dalam bagian-bagian kecil (kelas dan objek). Misalnya, ada kelas untuk halaman utama (HomePage), tombol-tombol, dan bahkan fitur khusus lainnya. Ini membuat kode lebih terstruktur dan mudah dipelihara.
Pemrograman yang Lebih Mudah Dikelola: Kelas dan objek memudahkan kita dalam mengelola dan memperbaiki kode. Setiap bagian aplikasi punya tugas spesifik, jadi gampang banget untuk memperbarui atau mengubah bagian tertentu tanpa merusak bagian lainnya.
Reusabilitas: Dengan OOP, kita bisa membuat kelas reusable. Misalnya, tombol yang digunakan di berbagai bagian aplikasi cukup dipanggil dari satu fungsi yang sama, membuat kode lebih ringkas.
Enkapsulasi: OOP memisahkan data dan logika, jadi kita bisa menyembunyikan detail implementasi dan hanya mengekspos interface yang diperlukan.
Dengan menggunakan OOP, aplikasi ini jadi lebih mudah dikembangkan dan dikembangkan lebih lanjut.

🌟 Kelebihan Paradigma OOP dalam Proyek Ini
Kemudahan Pengelolaan: OOP memungkinkan pembagian tugas dengan jelas, jadi setiap anggota tim bisa fokus pada bagian mereka masing-masing tanpa mengganggu yang lain.
Extensibility: OOP memudahkan pengembangan lebih lanjut. Misalnya, kita bisa dengan mudah menambah fitur baru (misalnya, halaman prediksi baru) tanpa banyak mengubah kode yang sudah ada.
Maintainability: Dengan pemisahan kode dalam bentuk objek, debugging dan pengujian bisa dilakukan dengan lebih efisien, karena kita hanya perlu fokus pada objek atau metode tertentu.

🎯 Fitur yang Ada
Upload Dataset - Upload gambar dan beri nama dataset.
Annotate Gambar - Buat label dan kotakin objek pada gambar.
Training Model - Kirim dataset yang sudah di-annotasi untuk pelatihan.
Prediksi dengan Webcam - Pilih dataset yang telah dilatih dan gunakan webcam untuk prediksi.

🚧 Pembaruan dan Perbaikan Selanjutnya
Integrasi dengan server untuk training model lebih besar.
Menambah fitur analisis hasil training.
Meningkatkan user experience (UX) dan responsivitas aplikasi.
