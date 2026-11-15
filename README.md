# SIMPOS
**Sistem Informasi Manajemen Produksi Kompos**

SIMPOS merupakan aplikasi berbasis Python dan PostgreSQL yang digunakan untuk membantu pengelolaan persediaan bahan baku dan proses produksi kompos.

Aplikasi ini memiliki dua jenis pengguna, yaitu Orang Lapangan dan Admin/Supervisor. Orang Lapangan bertugas mencatat penerimaan bahan baku, penggunaan bahan dalam produksi, hasil produksi, serta pengujian kualitas kompos. Sementara itu, Admin/Supervisor bertugas mengelola data, memverifikasi penerimaan bahan baku, dan memantau aktivitas produksi.

**Fitur utama:**
- Pengelolaan data pemasok dan bahan baku.
- Pencatatan dan verifikasi penerimaan bahan baku.
- Pemantauan stok bahan baku.
- Pencatatan penggunaan bahan untuk produksi.
- Pencatatan hasil produksi kompos.
- Pengujian kualitas kompos.
- Laporan persediaan dan produksi.

SIMPOS dikembangkan menggunakan Python sebagai bahasa pemrograman dan PostgreSQL sebagai sistem manajemen basis data.

## Kebutuhan
- Python 3.10+
- PostgreSQL 14+
- Paket Python pada `requirements.txt`

## Menjalankan aplikasi
1. Buat database PostgreSQL, misalnya `simpos_db`.
2. Salin `.env.example` menjadi `.env`, lalu sesuaikan kredensial database.
3. Buat dan aktifkan virtual environment.
4. Pasang dependensi: `pip install -r requirements.txt`.
5. Buat tabel: `python init_db.py`.
6. Jalankan aplikasi: `python main.py`.

Aplikasi juga mencoba memuat file `.env` secara otomatis jika tersedia.

## Struktur proyek
```
SIMPOS/
├── database/
│   └── schema.sql
├── services/
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

## Catatan ruang lingkup
SIMPOS adalah proyek pembelajaran Algoritma 1. Pengujian kualitas dicatat berdasarkan input manual pengguna; aplikasi tidak mengukur kualitas menggunakan sensor atau alat laboratorium. Aplikasi belum mencakup penjualan, pembayaran, maupun distribusi produk.
