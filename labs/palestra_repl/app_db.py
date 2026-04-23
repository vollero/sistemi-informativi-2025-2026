"""
Accesso SQLite per il laboratorio palestra REPL.
"""

from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = BASE_DIR / "runtime"
DB_PATH = RUNTIME_DIR / "palestra.sqlite"
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"


class PalestraDatabase:
    def __init__(self):
        self.db_path = DB_PATH
        self.schema_path = SCHEMA_PATH
        self.seed_path = SEED_PATH

    def initialize(self, reset=False):
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

        if reset and self.db_path.exists():
            self.db_path.unlink()

        if self.db_path.exists():
            return

        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.executescript(self.schema_path.read_text(encoding="utf-8"))
            conn.executescript(self.seed_path.read_text(encoding="utf-8"))
            conn.commit()
        finally:
            conn.close()

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def query(self, sql, params=()):
        with self.connect() as conn:
            return conn.execute(sql, params).fetchall()

    def query_one(self, sql, params=()):
        with self.connect() as conn:
            return conn.execute(sql, params).fetchone()

    def execute(self, sql, params=()):
        with self.connect() as conn:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.lastrowid, cursor.rowcount
