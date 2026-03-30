import sqlite3
import datetime

DB_NAME = "scan_history.db"

def init_db():
    """Initializes the SQLite database and creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            text_snippet TEXT,
            prediction TEXT,
            confidence REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_scan(text, prediction, confidence):
    """Logs a scan result into the database."""
    snippet = text[:50] + "..." if len(text) > 50 else text
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO history (timestamp, text_snippet, prediction, confidence) VALUES (?, ?, ?, ?)",
        (timestamp, snippet, prediction, confidence)
    )
    conn.commit()
    conn.close()

def get_history():
    """Retrieves all past scans."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, text_snippet, prediction, confidence FROM history ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return rows