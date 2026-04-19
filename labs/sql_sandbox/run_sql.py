"""
Esegue un file SQL su una copia temporanea del database di base.
"""

from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "runtime" / "sandbox.sqlite"


def stampa_righe(cursor):
    colonne = [descrizione[0] for descrizione in cursor.description]
    righe = cursor.fetchall()

    if not righe:
        print("(nessuna riga)")
        return

    larghezze = [len(colonna) for colonna in colonne]
    for riga in righe:
        for indice, valore in enumerate(riga):
            testo = "NULL" if valore is None else str(valore)
            larghezze[indice] = max(larghezze[indice], len(testo))

    header = " | ".join(colonne[i].ljust(larghezze[i]) for i in range(len(colonne)))
    separatore = "-+-".join("-" * larghezze[i] for i in range(len(colonne)))
    print(header)
    print(separatore)

    for riga in righe:
        print(
            " | ".join(
                ("NULL" if valore is None else str(valore)).ljust(larghezze[indice])
                for indice, valore in enumerate(riga)
            )
        )


def esegui_statement(conn, statement):
    statement = statement.strip()
    if not statement:
        return

    print(f"\nSQL> {statement}")
    cursor = conn.execute(statement)
    if cursor.description is not None:
        stampa_righe(cursor)
    else:
        conn.commit()
        print(f"OK - righe coinvolte: {cursor.rowcount}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 labs/sql_sandbox/run_sql.py <file.sql>")
        sys.exit(1)

    sql_file = Path(sys.argv[1]).resolve()
    if not sql_file.exists():
        print(f"File non trovato: {sql_file}")
        sys.exit(1)

    if not DB_PATH.exists():
        print("Database di base non trovato. Eseguire prima reset_db.py")
        sys.exit(1)

    with tempfile.TemporaryDirectory(prefix="sql_sandbox_") as temp_dir:
        temp_db = Path(temp_dir) / "sandbox.sqlite"
        shutil.copy2(DB_PATH, temp_db)

        conn = sqlite3.connect(temp_db)
        try:
            conn.execute("PRAGMA foreign_keys = ON;")
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
