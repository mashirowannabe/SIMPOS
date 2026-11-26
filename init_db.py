"""Membuat tabel SIMPOS dan menyiapkan akun Admin awal."""
import os
from pathlib import Path
from db import get_connection
from services.auth import hash_password

def initialize_database():
    schema_path = Path(__file__).resolve().parent / "database" / "schema.sql"
    sql = schema_path.read_text(encoding="utf-8")
    with get_connection() as conn:
        conn.execute(sql)
        admin_username = os.getenv("ADMIN_USERNAME", "admin").strip()
        existing = conn.execute(
            "SELECT id_pengguna FROM pengguna WHERE username = %s",
            (admin_username,)
        ).fetchone()
        if existing is None:
            admin_password = os.getenv("ADMIN_PASSWORD", "")
            if not admin_password:
                raise RuntimeError(
                    "ADMIN_PASSWORD belum diatur di .env. Isi ADMIN_NAME, ADMIN_USERNAME, "
                    "dan ADMIN_PASSWORD, lalu jalankan kembali python init_db.py."
                )
            password_hash = hash_password(admin_password)
            conn.execute(
                """INSERT INTO pengguna (nama_pengguna, username, password, role)
                   VALUES (%s, %s, %s, 'Admin')""",
                (os.getenv("ADMIN_NAME", "Administrator"), admin_username, password_hash)
            )
            print(f"Akun Admin awal berhasil dibuat dengan username: {admin_username}")
        else:
            print(f"Akun Admin '{admin_username}' sudah tersedia; tidak diubah.")
    print("Database SIMPOS berhasil diinisialisasi.")

if __name__ == "__main__":
    try:
        initialize_database()
    except Exception as exc:
        print(f"Gagal menginisialisasi database: {exc}")
