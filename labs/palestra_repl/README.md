# Laboratorio Palestra REPL

Applicazione didattica a linea di comando per la gestione di una piccola base dati di palestra.

## Obiettivo

Mostrare come uno schema relazionale venga usato dentro una semplice applicazione con ruoli diversi:

- `amministratore`:
  - CRUD su `Istruttori`
  - CRUD su `Iscritti`
- `istruttore`:
  - CRUD su `Esercizi`
  - CRUD su `SchedeAllenamento`
  - CRUD sugli esercizi contenuti nella scheda
- `iscritto`:
  - CRUD su `Esecuzioni`

## Avvio

Dal repository:

```bash
python3 labs/palestra_repl/main.py
```

Per ricreare da zero il database locale del laboratorio:

```bash
python3 labs/palestra_repl/main.py --reset
```

## Struttura

- `schema.sql` — struttura della base dati
- `seed.sql` — dati iniziali
- `app_db.py` — bootstrap e accesso SQLite
- `app_repl.py` — interfaccia REPL e menu per ruolo
- `main.py` — punto di ingresso

## Punto didattico

Questo laboratorio e' indipendente dalla sandbox SQL generale:

- ha un proprio database locale
- crea lo schema automaticamente
- usa operazioni applicative guidate, non query scritte manualmente

Serve quindi a collegare:

- modello relazionale
- vincoli
- operazioni CRUD
- logica di un'applicazione con ruoli
