"""
Accesso SQLite per il laboratorio palestra REPL.
"""

import os
from pathlib import Path
import sqlite3

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:  # dipendenza richiesta solo nella versione containerizzata
    psycopg = None
    dict_row = None


BASE_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = BASE_DIR / "runtime"
DB_PATH = RUNTIME_DIR / "palestra.sqlite"
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"

INTEGRITY_ERRORS = (sqlite3.IntegrityError,)
if psycopg is not None:
    INTEGRITY_ERRORS = (*INTEGRITY_ERRORS, psycopg.IntegrityError)


def _adatta_sql(sql):
    if os.environ.get("DATABASE_URL"):
        return sql.replace("?", "%s")
    return sql


class PalestraDatabase:
    def __init__(self):
        self.database_url = os.environ.get("DATABASE_URL")
        self.db_path = DB_PATH
        self.schema_path = SCHEMA_PATH
        self.seed_path = SEED_PATH

    def initialize(self, reset=False):
        if self.database_url:
            if psycopg is None:
                raise RuntimeError("DATABASE_URL impostato, ma il pacchetto psycopg non e' installato.")
            with self.connect() as conn:
                conn.execute("SELECT 1")
            self.db_path = "PostgreSQL tramite DATABASE_URL"
            return

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
        if self.database_url:
            return psycopg.connect(self.database_url, row_factory=dict_row)

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def query(self, sql, params=()):
        with self.connect() as conn:
            return conn.execute(_adatta_sql(sql), params).fetchall()

    def query_one(self, sql, params=()):
        with self.connect() as conn:
            return conn.execute(_adatta_sql(sql), params).fetchone()

    def execute(self, sql, params=()):
        with self.connect() as conn:
            cursor = conn.execute(_adatta_sql(sql), params)
            conn.commit()
            return getattr(cursor, "lastrowid", None), cursor.rowcount
