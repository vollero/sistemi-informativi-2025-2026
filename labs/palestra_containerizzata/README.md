# Laboratorio Palestra Containerizzata

Questo laboratorio usa lo stesso dominio dell'app palestra, ma sposta la
persistenza da SQLite a PostgreSQL e separa le parti applicative in container.

## Architettura

Servizi definiti in `docker-compose.yml`:

- `db`: PostgreSQL con database `palestra`, schema e dati iniziali precaricati.
- `web`: interfaccia Flask per amministratore, istruttore e iscritto.
- `repl`: interfaccia testuale a ruoli che usa lo stesso database PostgreSQL.

Le due interfacce applicative non hanno dati propri: leggono e scrivono entrambe
sul servizio `db`. Questo consente di mostrare in modo concreto che
l'interfaccia e la persistenza sono parti separate e sostituibili.

## Avvio rapido

Dal repository:

```bash
cd labs/palestra_containerizzata
docker compose build
docker compose up -d db web
```

Aprire l'interfaccia web:

```text
http://localhost:5000
```

Avviare la REPL applicativa:

```bash
docker compose run --rm repl
```

Verificare i container attivi:

```bash
docker compose ps
```

Leggere i log:

```bash
docker compose logs -f db
docker compose logs -f web
```

Fermare il laboratorio mantenendo il volume dati:

```bash
docker compose down
```

Fermare il laboratorio eliminando anche il database persistente:

```bash
docker compose down -v
```

## Caricamento del database

Al primo avvio del container `db`, PostgreSQL esegue automaticamente:

- `db/init/01_schema.sql`
- `db/init/02_seed.sql`

Questa inizializzazione avviene solo quando il volume PostgreSQL e' vuoto. Se il
volume esiste gia', i file di init non vengono rieseguiti.

Per ricreare schema e dati da zero senza eliminare il volume:

```bash
docker compose exec db psql -U palestra -d palestra -f /lab/db/init/01_schema.sql
docker compose exec db psql -U palestra -d palestra -f /lab/db/init/02_seed.sql
```

Per ripartire completamente da un database nuovo:

```bash
docker compose down -v
docker compose up -d db web
```

## Connessione al container PostgreSQL

Entrare in `psql` dentro il container:

```bash
docker compose exec db psql -U palestra -d palestra
```

Il servizio espone PostgreSQL anche sulla porta locale `5433`. Se sul computer
host e' installato `psql`, ci si puo' collegare senza entrare nel container:

```bash
PGPASSWORD=palestra psql -h localhost -p 5433 -U palestra -d palestra
```

Comandi utili dentro `psql`:

```sql
\dt
\d Iscritti
\d SchedeAllenamento
\d SchedaEsercizi
\d Esecuzioni
SELECT current_database(), current_user;
```

Eseguire una query direttamente da shell:

```bash
docker compose exec db psql -U palestra -d palestra -c "SELECT * FROM Iscritti ORDER BY cognome;"
```

Eseguire un file di query montato nel container:

```bash
docker compose exec db psql -U palestra -d palestra -f /lab/db/queries/02_join_schede_attive.sql
```

Eseguire tutti gli esempi disponibili:

```bash
docker compose exec db psql -U palestra -d palestra -f /lab/db/queries/01_ispezione_schema.sql
docker compose exec db psql -U palestra -d palestra -f /lab/db/queries/02_join_schede_attive.sql
docker compose exec db psql -U palestra -d palestra -f /lab/db/queries/03_filtri_subquery.sql
docker compose exec db psql -U palestra -d palestra -f /lab/db/queries/04_transazione_rollback.sql
docker compose exec db psql -U palestra -d palestra -f /lab/db/queries/05_transazione_savepoint.sql
```

## Ispezione dei singoli container

Entrare nel container PostgreSQL con una shell:

```bash
docker compose exec db sh
```

Entrare nel container web:

```bash
docker compose exec web sh
```

Dentro il container web, il codice applicativo si trova in:

```text
/app/labs/palestra_web
```

Aprire una shell nel container REPL senza avviare il menu:

```bash
docker compose run --rm --entrypoint sh repl
```

Dentro il container REPL, il codice applicativo si trova in:

```text
/app/labs/palestra_repl
```

Controllare la connessione usata dalle app:

```bash
docker compose exec web sh -c 'printenv DATABASE_URL'
docker compose run --rm --entrypoint sh repl -c 'printenv DATABASE_URL'
```

## Sequenza didattica suggerita

1. Avviare `db` e `web`, aprire la dashboard web e mostrare i dati iniziali.
2. Aprire `psql` e mostrare che le stesse tabelle sono disponibili nel DBMS.
3. Eseguire `02_join_schede_attive.sql` per collegare schema relazionale e vista applicativa.
4. Avviare la REPL e creare o aggiornare un'iscrizione.
5. Tornare in `psql` e verificare che la modifica sia persistita in PostgreSQL.
6. Usare l'interfaccia web per aggiungere una esecuzione.
7. Eseguire query con JOIN e filtri per leggere il cambiamento lato DBMS.
8. Eseguire gli script sulle transazioni per distinguere `COMMIT`, `ROLLBACK` e `SAVEPOINT`.

## Query libere da provare in psql

Conteggio delle righe principali:

```sql
SELECT 'Iscritti' AS tabella, COUNT(*) FROM Iscritti
UNION ALL
SELECT 'Istruttori', COUNT(*) FROM Istruttori
UNION ALL
SELECT 'SchedeAllenamento', COUNT(*) FROM SchedeAllenamento
UNION ALL
SELECT 'Esecuzioni', COUNT(*) FROM Esecuzioni;
```

Schede attive con istruttore e iscritto:

```sql
SELECT
    s.id_scheda,
    s.titolo,
    i.nome || ' ' || i.cognome AS iscritto,
    it.nome || ' ' || it.cognome AS istruttore
FROM SchedeAllenamento s
JOIN Iscritti i ON s.id_iscritto = i.id_iscritto
JOIN Istruttori it ON s.id_istruttore = it.id_istruttore
WHERE s.attiva = 1
ORDER BY s.id_scheda;
```

Prova di vincolo referenziale:

```sql
INSERT INTO SchedeAllenamento (
    id_scheda, id_iscritto, id_istruttore, titolo, data_inizio, data_fine, attiva
) VALUES (
    9999, 999, 10, 'Scheda non valida', '2026-05-13', NULL, 1
);
```

Transazione manuale:

```sql
BEGIN;

INSERT INTO Iscritti (id_iscritto, nome, cognome, data_nascita, data_iscrizione)
VALUES (50, 'Luca', 'Container', '2001-01-01', '2026-05-13');

SELECT * FROM Iscritti WHERE id_iscritto = 50;

ROLLBACK;

SELECT * FROM Iscritti WHERE id_iscritto = 50;
```
