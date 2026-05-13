# Esercizio Guidato 6

Tema: comandi SQL principali e transazioni

## Preparazione

Sandbox base:

```bash
python3 labs/sql_sandbox/reset_db.py
```

Sandbox palestra:

```bash
python3 labs/sql_sandbox/reset_db.py --project palestra
```

## Parte 1: schema

Esegui:

```bash
python3 labs/sql_sandbox/run_sql.py labs/sql_sandbox/esempi/17_schema_crud.sql
```

Domande guida:

- quale tabella viene creata?
- quale chiave esterna collega la nuova tabella a `Contatti`?
- perche' il `DROP TABLE` finale non danneggia il database di base?

## Parte 2: dati

Esegui:

```bash
python3 labs/sql_sandbox/run_sql.py labs/sql_sandbox/esempi/18_data_crud.sql
```

Domande guida:

- quali istruzioni realizzano `Create`, `Read`, `Update`, `Delete`?
- come cambia il risultato dopo ogni istruzione?
- che ruolo ha `WHERE` in `UPDATE` e `DELETE`?

## Parte 3: join, filtri e select innestate

Esegui:

```bash
python3 labs/sql_sandbox/run_sql.py --project palestra \
    labs/sql_sandbox/progetti/palestra/esempi/06-join-filtri-subquery.sql
```

Poi esegui:

```bash
python3 labs/sql_sandbox/run_sql.py --project palestra \
    labs/sql_sandbox/progetti/palestra/esempi/07-select-innestata-esecuzioni.sql
```

Domande guida:

- quali tabelle vengono ricomposte dai join?
- quale filtro usa una select innestata?
- dove viene usato `HAVING` invece di `WHERE`?

## Parte 4: transazioni

Esegui:

```bash
python3 labs/sql_sandbox/run_sql.py labs/sql_sandbox/esempi/19_transaction_rollback.sql
```

Poi:

```bash
python3 labs/sql_sandbox/run_sql.py labs/sql_sandbox/esempi/20_transaction_commit.sql
```

Infine:

```bash
python3 labs/sql_sandbox/run_sql.py --project palestra \
    labs/sql_sandbox/progetti/palestra/esempi/09-transazione-savepoint.sql
```

Domande guida:

- che differenza osservi tra `ROLLBACK` e `COMMIT`?
- a cosa serve un `SAVEPOINT`?
- perche' una transazione e' utile quando una operazione logica richiede piu' istruzioni SQL?
