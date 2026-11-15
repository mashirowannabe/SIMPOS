"""Laporan ringkas SIMPOS."""

from db import get_connection


def stock_report():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id_bahan, nama_bahan, stok, satuan FROM bahan_baku ORDER BY stok DESC, nama_bahan"
        ).fetchall()


def production_report():
    with get_connection() as conn:
        return conn.execute(
            """SELECT COUNT(*) AS jumlah_batch,
                      COUNT(pk.id_produk) AS batch_menghasilkan_produk,
                      COALESCE(SUM(pk.berat_hasil), 0) AS total_kompos_kg,
                      COALESCE(AVG(pk.rendemen), 0) AS rata_rendemen
               FROM batch_produksi b
               LEFT JOIN produk_kompos pk ON pk.id_batch=b.id_batch"""
        ).fetchone()
