# Template Flask minimali

Questo laboratorio contiene una mini-app Flask costruita come kit di template
riutilizzabili. L'obiettivo è fornire agli studenti un punto di partenza semplice
per comporre i propri applicativi.

Il CSS è volutamente essenziale: pochi colori, pochi componenti, nessun framework
esterno.

## Avvio

Installare Flask se necessario:

```bash
python3 -m pip install -r labs/flask_template_minimali/requirements.txt
```

Avviare la mini-app:

```bash
python3 labs/flask_template_minimali/app.py
```

Aprire:

```text
http://127.0.0.1:5000
```

## Template inclusi

- `base.html`: struttura comune, barra di navigazione, messaggi e blocco `content`.
- `home.html`: home page con introduzione e card statistiche.
- `dashboard.html`: riepilogo con indicatori e record recenti.
- `list.html`: tabella di record con azione di dettaglio.
- `detail.html`: pagina dettaglio di un singolo record.
- `form.html`: form riutilizzabile per creazione e modifica.
- `confirm.html`: conferma prima di una cancellazione.

## CSS incluso

Il file `static/simple.css` contiene stili base per:

- barra di navigazione;
- contenitori;
- card;
- tabelle;
- form;
- pulsanti;
- messaggi;
- layout responsive semplice.

## Come riusare il kit

1. Copiare la cartella `templates/` nel proprio progetto Flask.
2. Copiare `static/simple.css`.
3. Tenere `base.html` come layout comune.
4. Far estendere gli altri template da `base.html`.
5. Adattare nomi di variabili, route e campi al proprio dominio.

Esempio:

```python
@app.get("/libri")
def lista_libri():
    return render_template("list.html", progetti=libri)
```

In un progetto reale conviene rinominare le variabili del template:

```text
progetti -> libri
progetto -> libro
```

## Composizione minima consigliata

Per un elaborato semplice bastano spesso:

- una home;
- una lista;
- un dettaglio;
- un form di creazione;
- un form di modifica;
- una conferma di eliminazione.

Questa struttura corrisponde a una normale CRUD applicativa.

## Limite intenzionale

La mini-app usa una lista Python in memoria, non un database. Questo serve a
tenere il focus sui template. Nei progetti degli studenti, la lista andrà
sostituita con query SQL o con funzioni di accesso ai dati.
