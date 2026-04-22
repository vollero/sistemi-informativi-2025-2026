"""
Utility condivise per la sandbox SQL del corso.
"""

import argparse
from pathlib import Path
import shutil
import sqlite3
import tempfile


BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "progetti"


def risolvi_dir_progetto(project=None):
    if project is None:
        return BASE_DIR

    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        raise FileNotFoundError(f"Progetto sandbox non trovato: {project}")

    return project_dir


def risolvi_percorsi_progetto(project=None):
    project_dir = risolvi_dir_progetto(project)
    return {
        "project": project,
        "label": "base" if project is None else project,
        "dir": project_dir,
        "runtime_dir": project_dir / "runtime",
        "db_path": project_dir / "runtime" / "sandbox.sqlite",
        "schema_path": project_dir / "schema.sql",
        "seed_path": project_dir / "seed.sql",
    }


def parser_argomenti_sandbox(
    descrizione,
    include_sql_file=False,
    include_project=False,
):
    parser = argparse.ArgumentParser(description=descrizione)
    if include_project:
        parser.add_argument(
            "--project",
            help="nome del progetto sandbox sotto labs/sql_sandbox/progetti/",
        )
    if include_sql_file:
        parser.add_argument("sql_file", help="file .sql da eseguire")
    return parser


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


def esegui_statement(conn, statement, echo=True):
    statement = statement.strip()
    if not statement:
        return

    if echo:
        print(f"\nSQL> {statement}")

    cursor = conn.execute(statement)
    if cursor.description is not None:
        stampa_righe(cursor)
    else:
        conn.commit()
        print(f"OK - righe coinvolte: {cursor.rowcount}")


def crea_database_base(project=None):
    percorsi = risolvi_percorsi_progetto(project)

    schema_path = percorsi["schema_path"]
    seed_path = percorsi["seed_path"]
    db_path = percorsi["db_path"]
    runtime_dir = percorsi["runtime_dir"]

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema non trovato: {schema_path}")
    if not seed_path.exists():
        raise FileNotFoundError(f"Seed non trovato: {seed_path}")

    runtime_dir.mkdir(parents=True, exist_ok=True)

    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(schema_path.read_text(encoding="utf-8"))
        conn.executescript(seed_path.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()

    return db_path


def crea_connessione_temporanea(project=None):
    percorsi = risolvi_percorsi_progetto(project)
    db_path = percorsi["db_path"]

    if not db_path.exists():
        if project is None:
            raise FileNotFoundError("Database di base non trovato. Eseguire prima reset_db.py")
        raise FileNotFoundError(
            f"Database del progetto '{project}' non trovato. Eseguire prima reset_db.py --project {project}"
        )

    temp_dir = tempfile.TemporaryDirectory(prefix="sql_sandbox_")
    temp_db = Path(temp_dir.name) / "sandbox.sqlite"
    shutil.copy2(db_path, temp_db)

    conn = sqlite3.connect(temp_db)
    conn.execute("PRAGMA foreign_keys = ON;")
    return temp_dir, conn


def formatta_errore_sql(exc):
    messaggio = str(exc).strip()
    suggerimenti = []

    testo = messaggio.lower()

    if "syntax error" in testo:
        suggerimenti.append("controlla parole chiave, virgole, parentesi e ordine delle clausole")
    if "incomplete input" in testo:
        suggerimenti.append("la query sembra incompleta: verifica di aver chiuso parentesi e di aver terminato con ';'")
    if "no such table" in testo:
        suggerimenti.append("controlla il nome della tabella e verifica di avere ricreato il database con reset_db.py")
    if "no such column" in testo:
        suggerimenti.append("controlla il nome della colonna o l'alias usato nella query")
    if "foreign key constraint failed" in testo:
        suggerimenti.append("la query viola un legame tra tabelle: una chiave esterna punta a una riga assente o protetta")
    if "unique constraint failed" in testo:
        suggerimenti.append("stai inserendo o aggiornando un valore che deve restare univoco")
    if "not null constraint failed" in testo:
        suggerimenti.append("un attributo obbligatorio sta ricevendo NULL")

    if not suggerimenti:
        return f"ERRORE SQL: {messaggio}"

    righe = [f"ERRORE SQL: {messaggio}", "Suggerimento:"]
    righe.extend(f"- {suggerimento}" for suggerimento in suggerimenti)
    return "\n".join(righe)
