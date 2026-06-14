import sqlite3
from contextlib import closing

DB_NAME = "instances.db"


def init_db():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS instances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                instance_type TEXT NOT NULL,
                state TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def get_connection():
    return sqlite3.connect(DB_NAME)
