"""
Ricrea il database SQLite di base della sandbox SQL.
"""

from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = BASE_DIR / "runtime"
DB_PATH = RUNTIME_DIR / "sandbox.sqlite"
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"


def main():
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.executescript(SEED_PATH.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()

    print(f"Database ricreato in: {DB_PATH}")


if __name__ == "__main__":
    main()
