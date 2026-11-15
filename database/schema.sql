-- SIMPOS database schema (PostgreSQL)
-- Jalankan melalui: python init_db.py

CREATE TABLE IF NOT EXISTS pemasok (
    id_pemasok INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nama_pemasok VARCHAR(100) NOT NULL,
    jenis_pemasok VARCHAR(50) NOT NULL,
    no_telepon VARCHAR(20),
    alamat TEXT
);

CREATE TABLE IF NOT EXISTS bahan_baku (
    id_bahan INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nama_bahan VARCHAR(100) NOT NULL UNIQUE,
    satuan VARCHAR(20) NOT NULL,
    stok NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (stok >= 0),
    keterangan TEXT
);

CREATE TABLE IF NOT EXISTS penerimaan_bahan (
    id_penerimaan INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pemasok INTEGER NOT NULL REFERENCES pemasok(id_pemasok),
    tanggal DATE NOT NULL DEFAULT CURRENT_DATE,
    catatan TEXT
);

CREATE TABLE IF NOT EXISTS detail_penerimaan (
    id_detail_penerimaan INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_penerimaan INTEGER NOT NULL REFERENCES penerimaan_bahan(id_penerimaan) ON DELETE CASCADE,
    id_bahan INTEGER NOT NULL REFERENCES bahan_baku(id_bahan),
    jumlah NUMERIC(12, 2) NOT NULL CHECK (jumlah > 0)
);

CREATE TABLE IF NOT EXISTS batch_produksi (
    id_batch INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tanggal_mulai DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(30) NOT NULL DEFAULT 'Persiapan'
        CHECK (status IN ('Persiapan', 'Fermentasi', 'Pematangan', 'Selesai')),
    catatan TEXT
);

CREATE TABLE IF NOT EXISTS pemakaian_bahan (
    id_pemakaian INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_batch INTEGER NOT NULL REFERENCES batch_produksi(id_batch) ON DELETE CASCADE,
    id_bahan INTEGER NOT NULL REFERENCES bahan_baku(id_bahan),
    jumlah NUMERIC(12, 2) NOT NULL CHECK (jumlah > 0),
    UNIQUE (id_batch, id_bahan)
);

CREATE TABLE IF NOT EXISTS produk_kompos (
    id_produk INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_batch INTEGER NOT NULL UNIQUE REFERENCES batch_produksi(id_batch),
    tanggal_selesai DATE NOT NULL DEFAULT CURRENT_DATE,
    berat_hasil NUMERIC(12, 2) NOT NULL CHECK (berat_hasil >= 0),
    total_bahan NUMERIC(12, 2) NOT NULL CHECK (total_bahan > 0),
    rendemen NUMERIC(5, 2) GENERATED ALWAYS AS
        ((berat_hasil / NULLIF(total_bahan, 0)) * 100) STORED
);

CREATE TABLE IF NOT EXISTS pengujian_kualitas (
    id_pengujian INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_produk INTEGER NOT NULL REFERENCES produk_kompos(id_produk) ON DELETE CASCADE,
    tanggal_uji DATE NOT NULL DEFAULT CURRENT_DATE,
    ph NUMERIC(4, 2) CHECK (ph BETWEEN 0 AND 14),
    kadar_air NUMERIC(5, 2) CHECK (kadar_air BETWEEN 0 AND 100),
    warna VARCHAR(50),
    tekstur VARCHAR(50),
    aroma VARCHAR(100),
    catatan TEXT
);

CREATE INDEX IF NOT EXISTS idx_penerimaan_tanggal ON penerimaan_bahan(tanggal);
CREATE INDEX IF NOT EXISTS idx_batch_tanggal ON batch_produksi(tanggal_mulai);
CREATE INDEX IF NOT EXISTS idx_produk_tanggal ON produk_kompos(tanggal_selesai);
