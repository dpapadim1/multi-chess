import os
import sqlite3
from contextlib import closing

DATABASE = os.path.join('src', 'database', 'multi_chess.db')

def create_db():
    if not os.path.exists(os.path.dirname(DATABASE)):
        os.makedirs(os.path.dirname(DATABASE))
    with closing(sqlite3.connect(DATABASE)) as conn:
        with open('schema.sql') as f:
            conn.executescript(f.read())
        conn.commit()

def init_db():
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    cash NUMERIC DEFAULT 10000.00
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS owned_shares (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    symbol TEXT NOT NULL,
                    number INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

if __name__ == "__main__":
    create_db()
    init_db()
    print("Database created and initialized successfully.")