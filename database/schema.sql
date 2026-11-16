-- =========================================================
-- SIMPOS: Sistem Informasi Manajemen Produksi Kompos
-- Database schema PostgreSQL
-- Total: 9 tabel
--
-- Cara menjalankan:
--   python init_db.py
--
-- Catatan:
--   File ini ditujukan untuk inisialisasi database baru/kosong.
--   CREATE TABLE IF NOT EXISTS tidak mengubah struktur tabel lama.
-- =========================================================

-- 1. Pengguna aplikasi
CREATE TABLE IF NOT EXISTS pengguna (
    id_pengguna INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nama_pengguna VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role VARCHAR(30) NOT NULL
        CHECK (role IN ('Admin', 'Orang Lapangan')),
    status BOOLEAN NOT NULL DEFAULT TRUE
);

-- 2. Data pemasok bahan baku
CREATE TABLE IF NOT EXISTS pemasok (
    id_pemasok INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nama_pemasok VARCHAR(100) NOT NULL,
    jenis_pemasok VARCHAR(50) NOT NULL,
    no_telepon VARCHAR(20),
    alamat TEXT
);

-- 3. Master bahan baku dan stok
CREATE TABLE IF NOT EXISTS bahan_baku (
    id_bahan INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nama_bahan VARCHAR(100) NOT NULL UNIQUE,
    satuan VARCHAR(20) NOT NULL,
    stok NUMERIC(12, 2) NOT NULL DEFAULT 0
        CHECK (stok >= 0),
    keterangan TEXT
);

-- 4. Header penerimaan bahan baku.
-- Stok hanya boleh ditambahkan oleh proses aplikasi setelah status
-- verifikasi berubah menjadi 'Disetujui'.
CREATE TABLE IF NOT EXISTS penerimaan_bahan (
    id_penerimaan INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pemasok INTEGER NOT NULL
        REFERENCES pemasok(id_pemasok),
    tanggal DATE NOT NULL DEFAULT CURRENT_DATE,
    catatan TEXT,
    status_verifikasi VARCHAR(20) NOT NULL DEFAULT 'Menunggu'
        CHECK (status_verifikasi IN ('Menunggu', 'Disetujui', 'Ditolak')),
    catatan_verifikasi TEXT,
    tanggal_verifikasi TIMESTAMP
);

-- 5. Detail item bahan baku pada setiap penerimaan
CREATE TABLE IF NOT EXISTS detail_penerimaan (
    id_detail_penerimaan INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_penerimaan INTEGER NOT NULL
        REFERENCES penerimaan_bahan(id_penerimaan) ON DELETE CASCADE,
    id_bahan INTEGER NOT NULL
        REFERENCES bahan_baku(id_bahan),
    jumlah NUMERIC(12, 2) NOT NULL
        CHECK (jumlah > 0)
);

-- 6. Batch dan status produksi
CREATE TABLE IF NOT EXISTS batch_produksi (
    id_batch INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tanggal_mulai DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(30) NOT NULL DEFAULT 'Persiapan'
        CHECK (status IN ('Persiapan', 'Proses Produksi', 'Selesai')),
    catatan TEXT
);

-- 7. Bahan baku yang digunakan pada setiap batch
CREATE TABLE IF NOT EXISTS pemakaian_bahan (
    id_pemakaian INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_batch INTEGER NOT NULL
        REFERENCES batch_produksi(id_batch) ON DELETE CASCADE,
    id_bahan INTEGER NOT NULL
        REFERENCES bahan_baku(id_bahan),
    jumlah NUMERIC(12, 2) NOT NULL
        CHECK (jumlah > 0),
    UNIQUE (id_batch, id_bahan)
);

-- 8. Hasil produksi kompos.
-- Rendemen dihitung otomatis oleh PostgreSQL dalam satuan persen.
CREATE TABLE IF NOT EXISTS produk_kompos (
    id_produk INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_batch INTEGER NOT NULL UNIQUE
        REFERENCES batch_produksi(id_batch),
    tanggal_selesai DATE NOT NULL DEFAULT CURRENT_DATE,
    berat_hasil NUMERIC(12, 2) NOT NULL
        CHECK (berat_hasil >= 0),
    total_bahan NUMERIC(12, 2) NOT NULL
        CHECK (total_bahan > 0),
    rendemen NUMERIC(7, 2) GENERATED ALWAYS AS
        ((berat_hasil / NULLIF(total_bahan, 0)) * 100) STORED
);

-- 9. Hasil pengujian kualitas kompos
CREATE TABLE IF NOT EXISTS pengujian_kualitas (
    id_pengujian INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_produk INTEGER NOT NULL
        REFERENCES produk_kompos(id_produk) ON DELETE CASCADE,
    tanggal_uji DATE NOT NULL DEFAULT CURRENT_DATE,
    ph NUMERIC(4, 2)
        CHECK (ph BETWEEN 0 AND 14),
    kadar_air NUMERIC(5, 2)
        CHECK (kadar_air BETWEEN 0 AND 100),
    warna VARCHAR(50),
    tekstur VARCHAR(50),
    aroma VARCHAR(100),
    catatan TEXT
);

-- Indeks untuk membantu pencarian dan penyaringan data berdasarkan tanggal.
CREATE INDEX IF NOT EXISTS idx_penerimaan_tanggal
    ON penerimaan_bahan(tanggal);

CREATE INDEX IF NOT EXISTS idx_penerimaan_status
    ON penerimaan_bahan(status_verifikasi);

CREATE INDEX IF NOT EXISTS idx_batch_tanggal
    ON batch_produksi(tanggal_mulai);

CREATE INDEX IF NOT EXISTS idx_produk_tanggal
    ON produk_kompos(tanggal_selesai);
