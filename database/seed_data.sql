-- =========================================================
-- DATA CONTOH SIMPOS
-- Jalankan SEKALI setelah schema dan akun Admin dibuat:
--   psql / pgAdmin Query Tool -> database simpos -> buka file ini -> F5
--
-- Membuat:
--   1 akun Admin dibuat terpisah oleh init_db.py dari konfigurasi .env
--   2 pemasok, 2 bahan baku, 2 penerimaan, 4 detail penerimaan,
--   2 batch, 4 pemakaian bahan, 2 produk kompos, 2 pengujian kualitas.
--
-- Penerimaan pertama Disetujui dan stoknya ditambahkan.
-- Penerimaan kedua Menunggu sehingga belum menambah stok.
-- Jangan jalankan file ini berulang kali karena akan menambah data duplikat.
-- =========================================================

DO $$
DECLARE
    v_supplier1 INTEGER;
    v_supplier2 INTEGER;
    v_material1 INTEGER;
    v_material2 INTEGER;
    v_receipt1 INTEGER;
    v_receipt2 INTEGER;
    v_batch1 INTEGER;
    v_batch2 INTEGER;
    v_product1 INTEGER;
    v_product2 INTEGER;
BEGIN
    INSERT INTO pemasok (nama_pemasok, jenis_pemasok, no_telepon, alamat)
    VALUES ('Kelompok Tani Sumber Makmur', 'Limbah pertanian', '081234567801', 'Desa Sumberrejo')
    RETURNING id_pemasok INTO v_supplier1;

    INSERT INTO pemasok (nama_pemasok, jenis_pemasok, no_telepon, alamat)
    VALUES ('UD Tani Sejahtera', 'Bahan organik', '081234567802', 'Desa Sukamaju')
    RETURNING id_pemasok INTO v_supplier2;

    INSERT INTO bahan_baku (nama_bahan, satuan, stok, keterangan)
    VALUES ('Jerami padi', 'kg', 0, 'Limbah sisa panen padi')
    RETURNING id_bahan INTO v_material1;

    INSERT INTO bahan_baku (nama_bahan, satuan, stok, keterangan)
    VALUES ('Sekam padi', 'kg', 0, 'Hasil samping penggilingan padi')
    RETURNING id_bahan INTO v_material2;

    INSERT INTO penerimaan_bahan (id_pemasok, tanggal, catatan, status_verifikasi, tanggal_verifikasi)
    VALUES (v_supplier1, CURRENT_DATE - 7, 'Penerimaan bahan untuk contoh produksi', 'Disetujui', CURRENT_TIMESTAMP)
    RETURNING id_penerimaan INTO v_receipt1;

    INSERT INTO detail_penerimaan (id_penerimaan, id_bahan, jumlah)
    VALUES (v_receipt1, v_material1, 100), (v_receipt1, v_material2, 50);

    UPDATE bahan_baku SET stok = stok + 100 WHERE id_bahan = v_material1;
    UPDATE bahan_baku SET stok = stok + 50 WHERE id_bahan = v_material2;

    INSERT INTO penerimaan_bahan (id_pemasok, tanggal, catatan, status_verifikasi)
    VALUES (v_supplier2, CURRENT_DATE, 'Penerimaan menunggu pemeriksaan Admin', 'Menunggu')
    RETURNING id_penerimaan INTO v_receipt2;

    INSERT INTO detail_penerimaan (id_penerimaan, id_bahan, jumlah)
    VALUES (v_receipt2, v_material1, 80), (v_receipt2, v_material2, 40);

    INSERT INTO batch_produksi (tanggal_mulai, status, catatan)
    VALUES (CURRENT_DATE - 5, 'Selesai', 'Contoh produksi kompos batch pertama')
    RETURNING id_batch INTO v_batch1;

    INSERT INTO batch_produksi (tanggal_mulai, status, catatan)
    VALUES (CURRENT_DATE - 2, 'Selesai', 'Contoh produksi kompos batch kedua')
    RETURNING id_batch INTO v_batch2;

    INSERT INTO pemakaian_bahan (id_batch, id_bahan, jumlah)
    VALUES
        (v_batch1, v_material1, 40),
        (v_batch1, v_material2, 20),
        (v_batch2, v_material1, 30),
        (v_batch2, v_material2, 15);

    UPDATE bahan_baku SET stok = stok - 70 WHERE id_bahan = v_material1;
    UPDATE bahan_baku SET stok = stok - 35 WHERE id_bahan = v_material2;

    INSERT INTO produk_kompos (id_batch, tanggal_selesai, berat_hasil, total_bahan)
    VALUES (v_batch1, CURRENT_DATE - 1, 36, 60)
    RETURNING id_produk INTO v_product1;

    INSERT INTO produk_kompos (id_batch, tanggal_selesai, berat_hasil, total_bahan)
    VALUES (v_batch2, CURRENT_DATE, 27, 45)
    RETURNING id_produk INTO v_product2;

    INSERT INTO pengujian_kualitas
        (id_produk, tanggal_uji, ph, kadar_air, warna, tekstur, aroma, catatan)
    VALUES
        (v_product1, CURRENT_DATE, 6.8, 35.00, 'Cokelat kehitaman', 'Remah', 'Aroma tanah', 'Contoh hasil pengujian pertama'),
        (v_product2, CURRENT_DATE, 7.0, 32.50, 'Cokelat', 'Gembur', 'Aroma kompos matang', 'Contoh hasil pengujian kedua');
END $$;
