# SIMPOS
**Sistem Informasi Manajemen Produksi Kompos**

SIMPOS adalah aplikasi berbasis Python dan PostgreSQL untuk mencatat dan memantau persediaan bahan baku serta proses produksi kompos.

## Pengguna Sistem

SIMPOS memiliki dua role:

1. **Admin/Supervisor**: mengelola pemasok dan bahan baku, memverifikasi penerimaan, memantau stok dan produksi, melihat laporan, serta membuat dan menonaktifkan akun Orang Lapangan.
2. **Orang Lapangan**: mencatat penerimaan bahan, melihat stok, membuat batch produksi, memperbarui status produksi, mencatat hasil produksi, dan memasukkan hasil pengujian kualitas.

Aplikasi menyediakan login dan logout. Pendaftaran publik tidak tersedia; akun Orang Lapangan dibuat oleh Admin melalui menu Manajemen Pengguna.

## Fitur Utama

- Login dengan password yang disimpan dalam bentuk hash PBKDF2-HMAC-SHA256.
- Pembatasan menu berdasarkan role Admin dan Orang Lapangan.
- Pengelolaan data pemasok dan bahan baku.
- Pencatatan penerimaan bahan dengan status Menunggu, Disetujui, atau Ditolak.
- Stok hanya bertambah setelah penerimaan disetujui Admin.
- Pencatatan penggunaan bahan dan batch produksi.
- Status produksi: Persiapan, Proses Produksi, dan Selesai.
- Pencatatan hasil kompos dan perhitungan rendemen otomatis.
- Pencatatan hasil pengujian kualitas kompos.
- Laporan persediaan dan produksi.

## Alur Kerja

1. Orang Lapangan login dan mencatat penerimaan bahan baku.
2. Penerimaan tersimpan dengan status Menunggu dan belum menambah stok.
3. Admin login, memeriksa penerimaan, lalu menyetujui atau menolaknya.
4. Jika disetujui, stok bahan baku bertambah sesuai detail penerimaan.
5. Orang Lapangan membuat batch dan mencatat bahan yang digunakan. Sistem memeriksa stok dan menguranginya.
6. Orang Lapangan memperbarui status batch sampai Selesai.
7. Hasil produksi dan pengujian kualitas dicatat.
8. Admin memantau stok, aktivitas produksi, dan laporan.

## Teknologi

- Python 3.10+
- PostgreSQL 14+
- psycopg 3
- python-dotenv
- Command Line Interface (CLI)

## Persiapan dan Menjalankan Aplikasi

1. Clone repository:
   `git clone https://github.com/mashirowannabe/SIMPOS.git`
2. Masuk ke folder project:
   `cd SIMPOS`
3. Buat database PostgreSQL bernama `simpos`.
4. Salin `.env.example` menjadi `.env`.
5. Isi konfigurasi database dan akun Admin awal di `.env`:
   - `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
   - `ADMIN_NAME`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`
6. Pastikan `ADMIN_PASSWORD` minimal 8 karakter dan ganti nilai contoh dengan password milikmu.
7. Pasang dependensi:
   `python -m pip install -r requirements.txt`
8. Buat tabel dan akun Admin awal:
   `python init_db.py`
9. Jalankan aplikasi:
   `python main.py`
10. Login menggunakan `ADMIN_USERNAME` dan `ADMIN_PASSWORD` yang kamu atur di file `.env`.

**Penting:** file `.env` tidak boleh diunggah ke GitHub. File tersebut sudah dicantumkan di `.gitignore`. Jangan menggunakan password contoh pada penggunaan sebenarnya.

## Data Contoh

File `database/seed_data.sql` berisi data contoh yang saling berelasi untuk pemasok, bahan baku, penerimaan, detail penerimaan, batch, pemakaian bahan, produk kompos, dan pengujian kualitas.

Jalankan file tersebut melalui Query Tool pgAdmin setelah `python init_db.py` berhasil. File data contoh ditujukan untuk dijalankan satu kali pada database kosong agar tidak membuat data duplikat. Akun Admin dibuat oleh `init_db.py`, bukan oleh file seed.

## Struktur Proyek

```
SIMPOS/
├── database/
│   ├── schema.sql
│   └── seed_data.sql
├── services/
│   ├── auth.py
│   ├── master_data.py
│   ├── inventory.py
│   ├── production.py
│   └── reports.py
├── .env.example
├── .gitignore
├── db.py
├── init_db.py
├── main.py
└── requirements.txt
```

## Ruang Lingkup

SIMPOS berfokus pada pencatatan persediaan bahan baku dan proses produksi kompos. Sistem tidak mencakup penjualan, pembayaran, distribusi produk, maupun integrasi dengan layanan eksternal.

Pengujian kualitas dicatat berdasarkan input manual pengguna. Aplikasi tidak melakukan pengukuran menggunakan sensor atau alat laboratorium.
