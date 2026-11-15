# SIMPOS
**Sistem Informasi Manajemen Produksi Kompos**

SIMPOS adalah aplikasi berbasis Python dan PostgreSQL untuk mencatat dan memantau persediaan bahan baku serta proses produksi kompos.

Tujuan SIMPOS adalah membantu kegiatan produksi kompos agar data bahan baku yang masuk, bahan yang digunakan, hasil produksi, dan hasil pengujian kualitas tersimpan dengan rapi.

## Pengguna Sistem

SIMPOS dirancang untuk memiliki dua jenis pengguna:

1. **Orang Lapangan**  
   Mencatat kegiatan yang dilakukan di lapangan, seperti penerimaan bahan baku, penggunaan bahan untuk produksi, hasil produksi, dan pengujian kualitas kompos.

2. **Admin/Supervisor**  
   Mengelola data pemasok dan bahan baku, memeriksa serta menyetujui penerimaan bahan baku, memantau kegiatan produksi, dan melihat laporan.

Pembagian peran ini merupakan rancangan hak akses sistem. Implementasi pemilihan peran dan pembatasan menu masih perlu diselesaikan pada tahap pengembangan berikutnya.

## Fitur Utama

- Pengelolaan data pemasok.
- Pengelolaan data bahan baku.
- Pencatatan penerimaan bahan baku.
- Verifikasi penerimaan bahan baku oleh Admin/Supervisor.
- Pemantauan stok bahan baku.
- Pencatatan penggunaan bahan untuk produksi.
- Pencatatan batch dan hasil produksi kompos.
- Perhitungan rendemen produksi.
- Pencatatan hasil pengujian kualitas kompos.
- Laporan persediaan dan produksi.

## Alur Kerja Singkat

1. Orang Lapangan mencatat bahan baku yang diterima.
2. Admin/Supervisor memeriksa data penerimaan.
3. Setelah disetujui, jumlah bahan ditambahkan ke stok.
4. Orang Lapangan mencatat bahan yang digunakan dalam batch produksi.
5. Sistem memeriksa ketersediaan dan mengurangi stok sesuai pemakaian.
6. Orang Lapangan mencatat hasil produksi kompos.
7. Orang Lapangan mencatat hasil pengujian kualitas.
8. Admin/Supervisor memantau data dan laporan.

## Teknologi

- **Python** sebagai bahasa pemrograman.
- **PostgreSQL** sebagai sistem manajemen basis data.
- **Command Line Interface (CLI)** sebagai antarmuka aplikasi.

## Kebutuhan

- Python 3.10+
- PostgreSQL 14+
- Paket Python pada `requirements.txt`

## Menjalankan Aplikasi

1. Buat database PostgreSQL, misalnya `simpos_db`.
2. Salin `.env.example` menjadi `.env`, lalu sesuaikan kredensial database.
3. Buat dan aktifkan virtual environment.
4. Pasang dependensi: `pip install -r requirements.txt`.
5. Buat tabel: `python init_db.py`.
6. Jalankan aplikasi: `python main.py`.

Aplikasi mencoba memuat file `.env` secara otomatis jika tersedia.

## Struktur Proyek

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

## Ruang Lingkup

SIMPOS berfokus pada pencatatan persediaan bahan baku dan proses produksi kompos. Sistem tidak mencakup penjualan, pembayaran, distribusi produk, maupun integrasi dengan layanan eksternal.

Pengujian kualitas dicatat berdasarkan input manual pengguna. Aplikasi tidak melakukan pengukuran menggunakan sensor atau alat laboratorium.

## Catatan Pengembangan

Rancangan sistem menggunakan dua peran, yaitu Orang Lapangan dan Admin/Supervisor. Beberapa bagian rancangan, seperti pemilihan peran, verifikasi penerimaan sebelum stok bertambah, dan penyederhanaan status produksi, masih perlu diselaraskan dengan implementasi program.
