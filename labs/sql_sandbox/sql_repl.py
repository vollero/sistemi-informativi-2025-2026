"""
REPL interattiva per eseguire query SQL su una copia temporanea del database.
"""

import sqlite3
import sys

from sql_utils import crea_connessione_temporanea, esegui_statement, formatta_errore_sql


PROMPT = "sql> "
CONT_PROMPT = "...> "
COMANDI_SPECIALI = {".quit", ".exit", ".help"}


def stampa_aiuto():
    print("REPL SQL sandbox")
    print("Comandi disponibili:")
    print("  .help  mostra questo aiuto")
    print("  .quit  esce dalla REPL")
    print("  .exit  esce dalla REPL")
    print("Regole:")
    print("  - termina le query SQL con ';' anche se sono su piu' righe")
    print("  - la sessione lavora su una copia temporanea del database")
    print("  - Ctrl+C annulla la query corrente senza chiudere la REPL")
    print("Esempi:")
    print("  SELECT * FROM Contatti;")
    print("  SELECT nome, cognome FROM Contatti WHERE telefono IS NULL;")
    print("  INSERT INTO Contatti (id, nome, cognome, telefono)")
    print("  VALUES (6, 'Elena', 'Bruni', NULL);")
    print("Errori frequenti:")
    print("  - syntax error: di solito indica sintassi SQL malformata")
    print("  - no such table / no such column: nome errato di tabella o colonna")
    print("  - FOREIGN KEY constraint failed: modifica incoerente tra tabelle collegate")


def main():
    try:
        temp_dir, conn = crea_connessione_temporanea()
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(1)

    with temp_dir:
        print("REPL SQL sandbox")
        print("Database temporaneo creato da runtime/sandbox.sqlite")
        print("Le modifiche valgono solo per questa sessione.")
        print("Termina ogni query con ';'. Usa .help per l'aiuto, .quit per uscire.")

        buffer = []

        try:
            while True:
                prompt = PROMPT if not buffer else CONT_PROMPT
                try:
                    riga = input(prompt)
                except KeyboardInterrupt:
                    print()
                    if buffer:
                        buffer.clear()
                        print("Query corrente annullata.")
                    else:
                        print("Usa .quit per uscire dalla REPL.")
                    continue
                except EOFError:
                    print()
                    if buffer:
                        print("Query incompleta scartata prima dell'uscita.")
                    break

                comando = riga.strip()
                if not buffer and comando in COMANDI_SPECIALI:
                    if comando == ".help":
                        stampa_aiuto()
                        continue
                    break

                if not comando and not buffer:
                    continue

                if not comando and buffer:
                    print("Query ancora incompleta: termina con ';' oppure annulla con Ctrl+C.")
                    continue

                buffer.append(riga)
                statement = "\n".join(buffer).strip()

                if not sqlite3.complete_statement(statement):
                    continue

                try:
                    esegui_statement(conn, statement, echo=False)
                except sqlite3.DatabaseError as exc:
                    print(formatta_errore_sql(exc))

                buffer.clear()
        finally:
            conn.close()


if __name__ == "__main__":
    main()
