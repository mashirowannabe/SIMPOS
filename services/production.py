"""Pencatatan batch produksi, hasil kompos, dan pengujian."""

from db import get_connection

VALID_STATUSES = {"Persiapan", "Fermentasi", "Pematangan", "Selesai"}


def create_batch(items, notes=""):
    """Membuat batch dan memakai stok bahan secara atomik.

    items adalah list tuple (id_bahan, jumlah).
    """
    if not items:
        raise ValueError("Batch harus menggunakan minimal satu bahan.")

    with get_connection() as conn:
        batch = conn.execute(
            """INSERT INTO batch_produksi (catatan)
               VALUES (%s) RETURNING id_batch""",
            (notes or None,),
        ).fetchone()
        batch_id = batch["id_batch"]

        for material_id, quantity in items:
            if quantity <= 0:
                raise ValueError("Jumlah pemakaian harus lebih dari nol.")

            material = conn.execute(
                """SELECT nama_bahan, stok FROM bahan_baku
                   WHERE id_bahan=%s FOR UPDATE""",
                (material_id,),
            ).fetchone()
            if material is None:
                raise ValueError(f"Bahan dengan ID {material_id} tidak ditemukan.")
            if material["stok"] < quantity:
                raise ValueError(
                    f"Stok {material['nama_bahan']} tidak mencukupi. "
                    f"Tersedia {material['stok']}."
                )

            conn.execute(
                """INSERT INTO pemakaian_bahan (id_batch, id_bahan, jumlah)
                   VALUES (%s, %s, %s)""",
                (batch_id, material_id, quantity),
            )
            conn.execute(
                "UPDATE bahan_baku SET stok = stok - %s WHERE id_bahan = %s",
                (quantity, material_id),
            )

    return batch_id


def list_batches():
    with get_connection() as conn:
        return conn.execute(
            """SELECT b.id_batch, b.tanggal_mulai, b.status,
                      COALESCE(SUM(pb.jumlah), 0) AS total_bahan
               FROM batch_produksi b
               LEFT JOIN pemakaian_bahan pb ON pb.id_batch = b.id_batch
               GROUP BY b.id_batch
               ORDER BY b.id_batch DESC"""
        ).fetchall()


def update_batch_status(batch_id, status):
    if status not in VALID_STATUSES:
        raise ValueError("Status tidak valid.")
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE batch_produksi SET status=%s WHERE id_batch=%s",
            (status, batch_id),
        )
        return cursor.rowcount > 0


def record_product(batch_id, output_weight):
    if output_weight <= 0:
        raise ValueError("Berat hasil harus lebih dari nol.")

    with get_connection() as conn:
        batch = conn.execute(
            """SELECT b.id_batch, b.status, COALESCE(SUM(pb.jumlah), 0) AS total_bahan
               FROM batch_produksi b
               LEFT JOIN pemakaian_bahan pb ON pb.id_batch=b.id_batch
               WHERE b.id_batch=%s
               GROUP BY b.id_batch""",
            (batch_id,),
        ).fetchone()
        if batch is None:
            raise ValueError("Batch tidak ditemukan.")
        if batch["status"] != "Selesai":
            raise ValueError("Status batch harus Selesai sebelum hasil dicatat.")
        if batch["total_bahan"] <= 0:
            raise ValueError("Batch belum memiliki catatan pemakaian bahan.")

        product = conn.execute(
            """INSERT INTO produk_kompos (id_batch, berat_hasil, total_bahan)
               VALUES (%s, %s, %s) RETURNING id_produk, rendemen""",
            (batch_id, output_weight, batch["total_bahan"]),
        ).fetchone()
        return product


def list_products():
    with get_connection() as conn:
        return conn.execute(
            """SELECT pk.id_produk, pk.id_batch, pk.tanggal_selesai,
                      pk.berat_hasil, pk.total_bahan, pk.rendemen
               FROM produk_kompos pk ORDER BY pk.id_produk DESC"""
        ).fetchall()


def record_quality(product_id, ph=None, moisture=None, color="", texture="", aroma="", notes=""):
    if ph is not None and not 0 <= ph <= 14:
        raise ValueError("pH harus berada pada rentang 0 sampai 14.")
    if moisture is not None and not 0 <= moisture <= 100:
        raise ValueError("Kadar air harus berada pada rentang 0 sampai 100 persen.")

    with get_connection() as conn:
        row = conn.execute(
            """INSERT INTO pengujian_kualitas
               (id_produk, ph, kadar_air, warna, tekstur, aroma, catatan)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               RETURNING id_pengujian""",
            (product_id, ph, moisture, color or None, texture or None,
             aroma or None, notes or None),
        ).fetchone()
        return row["id_pengujian"]
