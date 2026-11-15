# Rancangan Sistem SIMPOS

## 1. Gambaran Umum

SIMPOS (Sistem Informasi Manajemen Produksi Kompos) digunakan untuk mencatat dan memantau persediaan bahan baku serta proses produksi kompos.

Sistem berfokus pada alur bahan baku masuk, bahan digunakan untuk produksi, hasil produksi dicatat, lalu kualitas kompos diuji.

## 2. Aktor Sistem

### Orang Lapangan
- Mencatat penerimaan bahan baku.
- Mencatat penggunaan bahan untuk produksi.
- Mencatat hasil produksi kompos.
- Memasukkan hasil pengujian kualitas.
- Melihat status dan riwayat kegiatan.

### Admin/Supervisor
- Mengelola data pemasok dan bahan baku.
- Memeriksa dan menyetujui atau menolak penerimaan bahan baku.
- Memantau proses produksi.
- Memeriksa data hasil produksi dan pengujian.
- Melihat laporan persediaan dan produksi.

## 3. Alur Utama

1. Orang Lapangan memasukkan data penerimaan bahan baku.
2. Admin/Supervisor memeriksa data penerimaan.
3. Jika disetujui, sistem menambahkan jumlah bahan ke stok. Jika ditolak, stok tidak berubah.
4. Orang Lapangan membuat batch produksi dan mencatat bahan yang digunakan.
5. Sistem memeriksa stok. Jika cukup, stok dikurangi sesuai jumlah pemakaian.
6. Setelah produksi selesai, Orang Lapangan mencatat berat hasil kompos.
7. Sistem menghitung rendemen berdasarkan perbandingan berat hasil kompos dengan total bahan yang digunakan.
8. Orang Lapangan mencatat hasil pengujian kualitas, seperti pH, kadar air, warna, tekstur, dan aroma.
9. Admin/Supervisor memantau data dan laporan.

## 4. Data yang Dikelola

Rancangan basis data terdiri dari delapan tabel:

| Tabel | Kegunaan |
|---|---|
| `pemasok` | Menyimpan informasi pemasok bahan baku. |
| `bahan_baku` | Menyimpan data bahan baku dan jumlah stok. |
| `penerimaan_bahan` | Menyimpan transaksi penerimaan bahan baku dan informasi verifikasi. |
| `detail_penerimaan` | Menyimpan rincian bahan dan jumlah dalam setiap penerimaan. |
| `batch_produksi` | Menyimpan informasi setiap batch produksi. |
| `pemakaian_bahan` | Menyimpan bahan dan jumlah yang digunakan dalam batch. |
| `produk_kompos` | Menyimpan hasil produksi dan rendemen. |
| `pengujian_kualitas` | Menyimpan hasil pengujian kualitas kompos. |

## 5. Batasan Sistem

- Aplikasi menggunakan Python berbasis CLI dan PostgreSQL.
- Pengujian kualitas dimasukkan secara manual.
- Sistem tidak mencakup penjualan, pembayaran, distribusi, atau integrasi eksternal.
- Pemilihan peran ditujukan sebagai pembatas menu sederhana, bukan sistem autentikasi kompleks.
- Status produksi direncanakan sederhana: Persiapan, Proses Produksi, dan Selesai.

## 6. Catatan Implementasi

Dokumen ini menjelaskan rancangan yang disepakati. Implementasi kode perlu disesuaikan secara bertahap, khususnya pemisahan menu berdasarkan peran, verifikasi penerimaan sebelum stok bertambah, dan penyederhanaan status produksi. Jangan menganggap seluruh alur tersebut sudah aktif sebelum perubahan kode dan pengujian selesai.
