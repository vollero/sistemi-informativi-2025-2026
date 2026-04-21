"""
Utility condivise per la sandbox SQL del corso.
"""

from pathlib import Path
import shutil
import sqlite3
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


def crea_connessione_temporanea():
    if not DB_PATH.exists():
        raise FileNotFoundError("Database di base non trovato. Eseguire prima reset_db.py")

    temp_dir = tempfile.TemporaryDirectory(prefix="sql_sandbox_")
    temp_db = Path(temp_dir.name) / "sandbox.sqlite"
    shutil.copy2(DB_PATH, temp_db)

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
