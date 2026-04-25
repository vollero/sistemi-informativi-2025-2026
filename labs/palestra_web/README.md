# Laboratorio Palestra Web

Seconda versione dell'applicazione palestra, con interfaccia web basata su Flask.

## Obiettivo

Mostrare lo stesso dominio del laboratorio REPL usando una piccola applicazione web:

- amministratore: CRUD su iscritti e istruttori
- istruttore: CRUD su esercizi, schede e righe della scheda
- iscritto: consultazione schede e CRUD sulle proprie esecuzioni

## Requisiti

- Python 3.12 o compatibile
- Flask

Se Flask non e' disponibile:

```bash
python3 -m pip install Flask
```

## Avvio

Dal repository:

```bash
python3 labs/palestra_web/app.py
```

Per ricreare il database del laboratorio:

```bash
python3 labs/palestra_web/app.py --reset
```

Poi aprire:

```text
http://127.0.0.1:5000
```

## Struttura

- `app.py` — applicazione Flask e route
- `schema.sql` — schema relazionale
- `seed.sql` — dati iniziali
- `templates/` — viste HTML Jinja
- `static/style.css` — stile dell'interfaccia

## Nota didattica

Il laboratorio evidenzia il passaggio da:

- modello relazionale
- vincoli e chiavi esterne
- CRUD applicative
- interfaccia utente con ruoli
