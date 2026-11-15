"""Fungsi pengelolaan data pemasok dan bahan baku."""

from db import get_connection


def list_suppliers():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM pemasok ORDER BY id_pemasok"
        ).fetchall()


def add_supplier(name, supplier_type, phone="", address=""):
    with get_connection() as conn:
        row = conn.execute(
            """INSERT INTO pemasok (nama_pemasok, jenis_pemasok, no_telepon, alamat)
               VALUES (%s, %s, %s, %s) RETURNING id_pemasok""",
            (name, supplier_type, phone or None, address or None),
        ).fetchone()
        return row["id_pemasok"]


def update_supplier(supplier_id, name, supplier_type, phone="", address=""):
    with get_connection() as conn:
        cursor = conn.execute(
            """UPDATE pemasok
               SET nama_pemasok=%s, jenis_pemasok=%s, no_telepon=%s, alamat=%s
               WHERE id_pemasok=%s""",
            (name, supplier_type, phone or None, address or None, supplier_id),
        )
        return cursor.rowcount > 0


def delete_supplier(supplier_id):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM pemasok WHERE id_pemasok=%s", (supplier_id,)
        )
        return cursor.rowcount > 0


def list_materials():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM bahan_baku ORDER BY nama_bahan"
        ).fetchall()


def add_material(name, unit, notes=""):
    with get_connection() as conn:
        row = conn.execute(
            """INSERT INTO bahan_baku (nama_bahan, satuan, keterangan)
               VALUES (%s, %s, %s) RETURNING id_bahan""",
            (name, unit, notes or None),
        ).fetchone()
        return row["id_bahan"]


def update_material(material_id, name, unit, notes=""):
    with get_connection() as conn:
        cursor = conn.execute(
            """UPDATE bahan_baku SET nama_bahan=%s, satuan=%s, keterangan=%s
               WHERE id_bahan=%s""",
            (name, unit, notes or None, material_id),
        )
        return cursor.rowcount > 0


def delete_material(material_id):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM bahan_baku WHERE id_bahan=%s", (material_id,)
        )
        return cursor.rowcount > 0
