"""Membuat seluruh tabel SIMPOS dari database/schema.sql."""

from pathlib import Path

from db import get_connection


def initialize_database():
    schema_path = Path(__file__).resolve().parent / "database" / "schema.sql"
    sql = schema_path.read_text(encoding="utf-8")

    with get_connection() as conn:
        conn.execute(sql)

    print("Database SIMPOS berhasil diinisialisasi.")


if __name__ == "__main__":
    try:
        initialize_database()
    except Exception as exc:
        print(f"Gagal menginisialisasi database: {exc}")
