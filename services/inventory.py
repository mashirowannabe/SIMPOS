"""Pencatatan penerimaan bahan baku dan verifikasi stok."""
from db import get_connection

def receive_materials(supplier_id, items, notes=""):
    """Simpan penerimaan berstatus Menunggu; stok belum ditambahkan."""
    if not items:
        raise ValueError("Penerimaan harus memiliki minimal satu bahan.")
    with get_connection() as conn:
        receipt = conn.execute(
            """INSERT INTO penerimaan_bahan (id_pemasok, catatan)
               VALUES (%s, %s) RETURNING id_penerimaan""",
            (supplier_id, notes or None)
        ).fetchone()
        receipt_id = receipt["id_penerimaan"]
        for material_id, quantity in items:
            if quantity <= 0:
                raise ValueError("Jumlah penerimaan harus lebih dari nol.")
            conn.execute(
                """INSERT INTO detail_penerimaan (id_penerimaan, id_bahan, jumlah)
                   VALUES (%s, %s, %s)""", (receipt_id, material_id, quantity)
            )
    return receipt_id

def list_receipts():
    with get_connection() as conn:
        return conn.execute(
            """SELECT p.id_penerimaan, p.tanggal, s.nama_pemasok,
                      p.status_verifikasi, p.catatan_verifikasi,
                      COUNT(d.id_detail_penerimaan) AS jumlah_item
               FROM penerimaan_bahan p
               JOIN pemasok s ON s.id_pemasok = p.id_pemasok
               LEFT JOIN detail_penerimaan d ON d.id_penerimaan = p.id_penerimaan
               GROUP BY p.id_penerimaan, p.tanggal, s.nama_pemasok,
                        p.status_verifikasi, p.catatan_verifikasi
               ORDER BY p.tanggal DESC, p.id_penerimaan DESC"""
        ).fetchall()

def review_receipt(receipt_id, decision, notes=""):
    """Setujui/tolak penerimaan. Stok bertambah hanya saat disetujui."""
    if decision not in ("Disetujui", "Ditolak"):
        raise ValueError("Keputusan harus Disetujui atau Ditolak.")
    with get_connection() as conn:
        receipt = conn.execute(
            "SELECT status_verifikasi FROM penerimaan_bahan WHERE id_penerimaan = %s FOR UPDATE",
            (receipt_id,)
        ).fetchone()
        if receipt is None:
            raise ValueError("Penerimaan tidak ditemukan.")
        if receipt["status_verifikasi"] != "Menunggu":
            raise ValueError("Penerimaan ini sudah pernah diverifikasi.")
        if decision == "Disetujui":
            details = conn.execute(
                "SELECT id_bahan, jumlah FROM detail_penerimaan WHERE id_penerimaan = %s",
                (receipt_id,)
            ).fetchall()
            if not details:
                raise ValueError("Penerimaan tidak memiliki rincian bahan.")
            for item in details:
                conn.execute(
                    "UPDATE bahan_baku SET stok = stok + %s WHERE id_bahan = %s",
                    (item["jumlah"], item["id_bahan"])
                )
        conn.execute(
            """UPDATE penerimaan_bahan
               SET status_verifikasi = %s, catatan_verifikasi = %s,
                   tanggal_verifikasi = CURRENT_TIMESTAMP
               WHERE id_penerimaan = %s""",
            (decision, notes or None, receipt_id)
        )
    return True
