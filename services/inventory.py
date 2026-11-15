"""Pencatatan penerimaan bahan baku dan stok."""

from db import get_connection


def receive_materials(supplier_id, items, notes=""):
    """Simpan satu penerimaan berisi banyak bahan dan tambahkan stok.

    items adalah list tuple (id_bahan, jumlah).
    Seluruh proses berada dalam satu transaksi: jika satu langkah gagal,
    semua perubahan dibatalkan.
    """
    if not items:
        raise ValueError("Penerimaan harus memiliki minimal satu bahan.")

    with get_connection() as conn:
        receipt = conn.execute(
            """INSERT INTO penerimaan_bahan (id_pemasok, catatan)
               VALUES (%s, %s) RETURNING id_penerimaan""",
            (supplier_id, notes or None),
        ).fetchone()
        receipt_id = receipt["id_penerimaan"]

        for material_id, quantity in items:
            if quantity <= 0:
                raise ValueError("Jumlah penerimaan harus lebih dari nol.")
            conn.execute(
                """INSERT INTO detail_penerimaan
                   (id_penerimaan, id_bahan, jumlah) VALUES (%s, %s, %s)""",
                (receipt_id, material_id, quantity),
            )
            conn.execute(
                "UPDATE bahan_baku SET stok = stok + %s WHERE id_bahan = %s",
                (quantity, material_id),
            )

    return receipt_id


def list_receipts():
    with get_connection() as conn:
        return conn.execute(
            """SELECT p.id_penerimaan, p.tanggal, s.nama_pemasok,
                      COUNT(d.id_detail_penerimaan) AS jumlah_item
               FROM penerimaan_bahan p
               JOIN pemasok s ON s.id_pemasok = p.id_pemasok
               LEFT JOIN detail_penerimaan d ON d.id_penerimaan = p.id_penerimaan
               GROUP BY p.id_penerimaan, p.tanggal, s.nama_pemasok
               ORDER BY p.tanggal DESC, p.id_penerimaan DESC"""
        ).fetchall()
