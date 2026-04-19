# SQL Sandbox

Sandbox SQL minimale per il corso di Sistemi Informativi.

Obiettivi:

- provare query SQL in locale
- evitare installazioni pesanti
- ripartire rapidamente da uno stato noto
- eseguire i test su una copia temporanea del database

## Requisiti

- Python 3.12 o compatibile

Opzionale:

- `sqlite3` da riga di comando

La sandbox funziona gia' con la sola standard library di Python.

## Struttura

- `schema.sql` — definizione delle tabelle
- `seed.sql` — dati iniziali
- `reset_db.py` — ricrea il database di base
- `run_sql.py` — esegue un file `.sql` su una copia temporanea
- `esempi/` — query di esempio
- `esercizi/` — schede di lavoro guidate per gli studenti

## Uso minimo

Ricreare il database di base:

```bash
python3 labs/sql_sandbox/reset_db.py
```

Eseguire una query di esempio in sandbox:

```bash
python3 labs/sql_sandbox/run_sql.py labs/sql_sandbox/esempi/01_select_base.sql
```

Esempi utili per il seguito del corso:

- `06_select_where_order_by.sql`
- `07_contatti_senza_telefono.sql`
- `08_count_contatti.sql`
- `09_group_by_gruppi.sql`
- `10_group_by_having.sql`
- `11_insert_contatto_valido.sql`
- `12_insert_appartenenza_valida.sql`
- `13_insert_appartenenza_invalida_fk.sql`
- `14_update_telefono_contatto.sql`
- `15_delete_contatto_referenziato.sql`
- `16_delete_contatto_libero.sql`

Schede di lavoro:

- `esercizi/01-query-di-base.md`
- `esercizi/02-aggregazioni.md`
- `esercizi/03-modifiche-dati-e-vincoli.md`

## Idea di sicurezza

`run_sql.py` non lavora direttamente sul database di base. Prima crea una copia temporanea e poi esegue li' le istruzioni SQL.

Questo permette di:

- provare `INSERT`, `UPDATE`, `DELETE`
- osservare errori e vincoli
- ricominciare da capo in pochi secondi
