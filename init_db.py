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
                    score NUMERIC DEFAULT 1000.00
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    creator_id INTEGER NOT NULL,
                    joiner_id INTEGER,
                    status TEXT NOT NULL DEFAULT 'waiting',
                    turn TEXT NOT NULL DEFAULT 'white',
                    board TEXT NOT NULL,
                    state INTEGER NOT NULL DEFAULT 1, -- 1 for ongoing, 2 for creator win, 3 for joiner win, 4 for draw 
                    move_index INTEGER NOT NULL DEFAULT 0, -- 0 for no move, 1 for first move, etc.
                    FOREIGN KEY (creator_id) REFERENCES users(id),
                    FOREIGN KEY (joiner_id) REFERENCES users(id)
                )
            """)

if __name__ == "__main__":
    create_db()
    init_db()
    print("Database created and initialized successfully.")