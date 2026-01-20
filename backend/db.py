import sqlite3

DB_FILE = "fitness.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        height REAL DEFAULT 0,
        weight REAL DEFAULT 0,
        arm_length REAL DEFAULT 0
    )
    """)

    # repetitions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS repetitions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        timestamp REAL,
        distance REAL,
        speed REAL,
        valid INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Baza de date initializata")
