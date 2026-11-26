# Rancangan Sistem SIMPOS

## 1. Gambaran Umum

SIMPOS (Sistem Informasi Manajemen Produksi Kompos) digunakan untuk mencatat dan memantau persediaan bahan baku serta proses produksi kompos.

Sistem berfokus pada alur bahan baku masuk, bahan digunakan untuk produksi, hasil produksi dicatat, lalu kualitas kompos diuji.

## 2. Aktor dan Hak Akses

SIMPOS menggunakan login dengan dua role. Pendaftaran publik tidak tersedia.

### Orang Lapangan
- Login menggunakan akun yang dibuat Admin.
- Mencatat penerimaan bahan baku.
- Melihat informasi stok bahan baku.
- Mencatat penggunaan bahan untuk produksi.
- Membuat batch dan memperbarui status produksi.
- Mencatat hasil produksi kompos.
- Memasukkan hasil pengujian kualitas.
- Melihat riwayat batch dan hasil produksi.

### Admin/Supervisor
- Login menggunakan akun Admin.
- Mengelola data pemasok dan bahan baku.
- Memeriksa dan menyetujui atau menolak penerimaan bahan baku.
- Memantau stok dan proses produksi.
- Memeriksa hasil produksi dan pengujian.
- Melihat laporan persediaan dan produksi.
- Membuat akun Orang Lapangan dan mengaktifkan atau menonaktifkan akun.

## 3. Autentikasi

- Akun Admin awal dibuat oleh `init_db.py` berdasarkan konfigurasi `ADMIN_NAME`, `ADMIN_USERNAME`, dan `ADMIN_PASSWORD` pada file lokal `.env`.
- Password disimpan sebagai hash PBKDF2-HMAC-SHA256 dengan salt acak.
- Admin membuat akun Orang Lapangan melalui menu Manajemen Pengguna.
- Akun nonaktif tidak dapat login.
- Pengguna dapat logout untuk mengakhiri sesi CLI.

## 4. Alur Utama

1. Orang Lapangan login dan memasukkan data penerimaan bahan baku.
2. Penerimaan disimpan dengan status Menunggu; stok belum berubah.
3. Admin memeriksa penerimaan dan memilih Disetujui atau Ditolak.
4. Jika disetujui, sistem menambahkan jumlah bahan ke stok. Jika ditolak, stok tidak berubah.
5. Orang Lapangan membuat batch produksi dan mencatat bahan yang digunakan.
6. Sistem memeriksa ketersediaan stok. Jika cukup, stok dikurangi sesuai jumlah pemakaian.
7. Orang Lapangan memperbarui status batch: Persiapan, Proses Produksi, lalu Selesai.
8. Setelah batch selesai, Orang Lapangan mencatat berat hasil kompos.
9. Sistem menghitung rendemen berdasarkan perbandingan berat hasil kompos dengan total bahan yang digunakan.
10. Orang Lapangan mencatat hasil pengujian kualitas, seperti pH, kadar air, warna, tekstur, dan aroma.
11. Admin memantau data dan laporan.

## 5. Struktur Basis Data

Rancangan basis data terdiri dari sembilan tabel:

| Tabel | Kegunaan |
|---|---|
| `pengguna` | Menyimpan akun, username, password hash, role, dan status akun. |
| `pemasok` | Menyimpan informasi pemasok bahan baku. |
| `bahan_baku` | Menyimpan data bahan baku dan jumlah stok. |
| `penerimaan_bahan` | Menyimpan transaksi penerimaan dan informasi verifikasi. |
| `detail_penerimaan` | Menyimpan rincian bahan dan jumlah dalam setiap penerimaan. |
| `batch_produksi` | Menyimpan informasi setiap batch produksi. |
| `pemakaian_bahan` | Menyimpan bahan dan jumlah yang digunakan dalam batch. |
| `produk_kompos` | Menyimpan hasil produksi dan rendemen. |
| `pengujian_kualitas` | Menyimpan hasil pengujian kualitas kompos. |

## 6. Batasan Sistem

- Aplikasi menggunakan Python berbasis CLI dan PostgreSQL.
- Pengujian kualitas dimasukkan secara manual.
- Sistem tidak mencakup penjualan, pembayaran, distribusi, atau integrasi eksternal.
- Pembatasan akses dilakukan melalui menu CLI berdasarkan role pengguna.
- Sistem tidak menyediakan pendaftaran akun publik; akun Orang Lapangan dikelola Admin.
