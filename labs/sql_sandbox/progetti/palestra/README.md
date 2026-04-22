# Sandbox SQL: Progetto Palestra

Sandbox dedicata al dominio delle schede di allenamento in palestra.

## Obiettivo

Permette di lavorare su un modello dati che include:

- iscritti
- istruttori
- esercizi
- schede di allenamento
- esercizi contenuti in una scheda
- esecuzioni reali svolte in palestra

## Avvio rapido

Ricreare il database del progetto:

```bash
python3 labs/sql_sandbox/reset_db.py --project palestra
```

Eseguire una query di esempio:

```bash
python3 labs/sql_sandbox/run_sql.py --project palestra \
    labs/sql_sandbox/progetti/palestra/esempi/01-schede-attive.sql
```

Aprire la REPL:

```bash
python3 labs/sql_sandbox/sql_repl.py --project palestra
```

## File principali

- `schema.sql`
- `seed.sql`
- `esempi/`

## Domande didattiche utili

- come distinguere la scheda assegnata dalle esecuzioni reali?
- perche' serve una tabella separata per gli esercizi contenuti in una scheda?
- quali join servono per ricostruire una scheda completa?
