
import sqlite3
import json
import os

DB_PATH = os.path.join("data", "history.db")

def init_db():
    """Create data folder and history table if not exists."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            method TEXT,
            headers TEXT,
            body TEXT,
            status INTEGER,
            response TEXT,
            time_taken REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_history(url, method, headers, body, response, status, time_taken):
    """
    Save a request/response to SQLite.
    - headers and body will be stored as JSON strings (if not None).
    - response saved truncated to a reasonable length to avoid DB bloat.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO history (url, method, headers, body, status, response, time_taken, timestamp) VALUES (?,?,?,?,?,?,?,datetime('now'))",
            (
                url,
                method,
                json.dumps(headers) if headers is not None else None,
                json.dumps(body) if body is not None else None,
                status,
                (response[:2000] if isinstance(response, str) else str(response)),
                time_taken
            )
        )
        conn.commit()
    finally:
        conn.close()

def get_all_history():
    """
    Return a list of recent history rows.
    Each row is: (id, method, url, status, time_taken, timestamp)
    This matches how main_window.py displays the list.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, method, url, status, time_taken, timestamp FROM history ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_history_by_id(entry_id):
    """
    Return the full row for a given id:
    (id, url, method, headers, body, status, response, time_taken, timestamp)
    This order is expected by main_window.py's load_selected_request.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, url, method, headers, body, status, response, time_taken, timestamp FROM history WHERE id = ?", (entry_id,))
    row = c.fetchone()
    conn.close()
    return row
