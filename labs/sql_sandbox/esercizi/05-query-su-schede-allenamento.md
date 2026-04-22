# Esercizio Guidato 5

Tema: query SQL sul modello palestra

Usa la sandbox del progetto `palestra`.

## Preparazione

```bash
python3 labs/sql_sandbox/reset_db.py --project palestra
```

Per eseguire un file SQL:

```bash
python3 labs/sql_sandbox/run_sql.py --project palestra <file.sql>
```

Per aprire la REPL:

```bash
python3 labs/sql_sandbox/sql_repl.py --project palestra
```

## Esercizio 1

Mostrare tutte le schede attive con:

- nome e cognome dell'iscritto
- titolo della scheda
- nome e cognome dell'istruttore

## Esercizio 2

Mostrare il dettaglio della scheda `1000` con:

- ordine di esecuzione
- nome esercizio
- serie
- ripetizioni
- carico suggerito

## Esercizio 3

Mostrare lo storico delle esecuzioni dell'iscritto `1`.

Domanda guida:

- perche' qui non basta una sola tabella?

## Esercizio 4

Contare quante esecuzioni risultano registrate per ciascun esercizio.

Domanda guida:

- quale join serve per mantenere anche gli esercizi mai eseguiti?

## Esercizio 5

Mostrare solo gli esercizi con almeno due esecuzioni registrate.

Domanda guida:

- perche' qui serve `HAVING` e non `WHERE`?
