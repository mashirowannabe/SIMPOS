"""Autentikasi dan pengelolaan akun pengguna SIMPOS."""
import hashlib
import hmac
import secrets
from db import get_connection

_ITERATIONS = 310_000

def hash_password(password):
    if len(password) < 8:
        raise ValueError("Password minimal 8 karakter.")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)
    return "pbkdf2_sha256$" + str(_ITERATIONS) + "$" + salt.hex() + "$" + digest.hex()

def verify_password(password, stored_hash):
    try:
        algorithm, iterations, salt_hex, digest_hex = stored_hash.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        calculated = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations))
        return hmac.compare_digest(calculated.hex(), digest_hex)
    except (ValueError, TypeError):
        return False

def authenticate(username, password):
    with get_connection() as conn:
        user = conn.execute(
            """SELECT id_pengguna, nama_pengguna, username, password, role, status
               FROM pengguna WHERE username = %s""", (username.strip(),)
        ).fetchone()
    if not user or not user["status"] or not verify_password(password, user["password"]):
        return None
    return {key: user[key] for key in ("id_pengguna", "nama_pengguna", "username", "role")}

def create_user(name, username, password, role="Orang Lapangan"):
    if role not in ("Admin", "Orang Lapangan"):
        raise ValueError("Role tidak valid.")
    if not name.strip() or not username.strip():
        raise ValueError("Nama dan username wajib diisi.")
    password_hash = hash_password(password)
    with get_connection() as conn:
        row = conn.execute(
            """INSERT INTO pengguna (nama_pengguna, username, password, role)
               VALUES (%s, %s, %s, %s) RETURNING id_pengguna""",
            (name.strip(), username.strip(), password_hash, role)
        ).fetchone()
        return row["id_pengguna"]

def list_users():
    with get_connection() as conn:
        return conn.execute(
            """SELECT id_pengguna, nama_pengguna, username, role, status
               FROM pengguna ORDER BY id_pengguna"""
        ).fetchall()

def set_user_status(user_id, active, current_user_id=None):
    if current_user_id is not None and user_id == current_user_id and not active:
        raise ValueError("Admin tidak dapat menonaktifkan akunnya sendiri.")
    with get_connection() as conn:
        cursor = conn.execute("UPDATE pengguna SET status = %s WHERE id_pengguna = %s", (active, user_id))
        return cursor.rowcount > 0
