import sqlite3
import os
import hashlib

DB_PATH = "data/users.db"

def init_auth_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                    (email, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def validate_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return False
    
    return hash_password(password) == row[0]
