"""
Esegue un file SQL su una copia temporanea del database di base.
"""

from pathlib import Path
import sqlite3
import sys

from sql_utils import crea_connessione_temporanea, esegui_statement, parser_argomenti_sandbox


def main():
    parser = parser_argomenti_sandbox(
        "Esegue un file SQL su una copia temporanea del database",
        include_sql_file=True,
        include_project=True,
    )
    args = parser.parse_args()

    sql_file = Path(args.sql_file).resolve()
    if not sql_file.exists():
        print(f"File non trovato: {sql_file}")
        sys.exit(1)

    try:
        temp_dir, conn = crea_connessione_temporanea(args.project)
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(1)

    with temp_dir:
        try:
            contenuto = sql_file.read_text(encoding="utf-8")
            statements = [parte for parte in contenuto.split(";") if parte.strip()]
            for statement in statements:
                esegui_statement(conn, statement + ";")
        except sqlite3.DatabaseError as exc:
            print(f"ERRORE SQL: {exc}")
            sys.exit(2)
        finally:
            conn.close()


if __name__ == "__main__":
    main()
