# SIMPOS
**Sistem Informasi Manajemen Produksi Pupuk Kompos dari Limbah Pertanian**

Aplikasi CLI sederhana menggunakan **Python** dan **PostgreSQL** untuk mencatat pemasok, bahan baku, penerimaan bahan, batch produksi, hasil kompos, dan pengujian kualitas.

## Fitur
- CRUD pemasok dan bahan baku.
- Pencatatan penerimaan bahan baku yang memperbarui stok.
- Pencatatan batch dan pemakaian beberapa bahan.
- Validasi stok dan pengurangan stok secara transaksional.
- Pencatatan hasil produksi dan perhitungan rendemen.
- Pencatatan hasil pengujian kualitas.
- Laporan ringkas stok dan produksi.

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
