# Demo Flask per interfacce web

Questa cartella contiene una serie di demo progressive per introdurre lo
sviluppo di interfacce web con Flask.

Le demo sono volutamente piccole e indipendenti dall'app palestra: servono a
isolare i concetti prima di rileggerli in un'applicazione piu' completa.

## Avvio

Installare Flask se non e' gia' disponibile:

```bash
python3 -m pip install -r labs/flask_interfacce_demo/requirements.txt
```

Avviare il server:

```bash
python3 labs/flask_interfacce_demo/app.py
```

Aprire:

```text
http://127.0.0.1:5000
```

## Demo disponibili

- `01 Pagina statica`: HTML, layout e DOM iniziale.
- `02 Template dinamico`: dati Python renderizzati con Jinja.
- `03 Componenti grafici`: mappa tra oggetti visibili e tag HTML.
- `04 Form GET/POST`: submit, `request.form`, validazione e risposta.
- `05 Eventi DOM`: click e input gestiti nel browser.
- `06 Mini CRUD`: creazione ed eliminazione in memoria con Post/Redirect/Get.

## Lettura didattica

Per ogni demo ricostruire sempre questa catena:

```text
oggetto grafico
  -> evento utente
      -> richiesta HTTP o evento DOM locale
          -> route Flask / JavaScript
              -> template o modifica del DOM
                  -> risultato visibile
```

## File principali

- `app.py`: route Flask e dati di esempio.
- `templates/`: pagine Jinja.
- `static/style.css`: stile comune delle demo.
- `static/events.js`: eventi DOM della demo 05.

## Nota

La demo CRUD usa una lista Python in memoria. I dati non sono persistenti e si
perdono al riavvio del server. Questa scelta e' intenzionale: l'obiettivo e'
mostrare il ciclo dell'interfaccia, non introdurre un nuovo database.
