"""Koneksi PostgreSQL untuk SIMPOS."""

import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass


def get_connection():
    """Membuka koneksi PostgreSQL menggunakan konfigurasi environment."""
    required = ["DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            "Konfigurasi database belum lengkap: " + ", ".join(missing)
            + ". Salin .env.example menjadi .env dan isi nilainya."
        )

    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        row_factory=dict_row,
    )
