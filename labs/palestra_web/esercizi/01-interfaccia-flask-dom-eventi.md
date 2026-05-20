# Esercizio: leggere l'interfaccia Flask della palestra

Obiettivo: collegare pagina visibile, DOM, route Flask, template, eventi e query.

## Prima fase: demo isolate

Prima di leggere l'app palestra completa, avviare le demo progressive:

```bash
python3 labs/flask_interfacce_demo/app.py
```

Aprire:

```text
http://127.0.0.1:5000
```

Usare le demo per riconoscere separatamente:

- pagina statica e DOM;
- template dinamico con Jinja;
- componenti grafici;
- form GET/POST;
- eventi DOM;
- mini CRUD con redirect.

## Preparazione

Avviare l'app web locale:

```bash
python3 labs/palestra_web/app.py --reset
```

Aprire:

```text
http://127.0.0.1:5000
```

## 1. Home e DOM

Osservare la home nel browser.

Individuare nel file `templates/index.html`:

- il titolo principale;
- i tre pannelli dei ruoli;
- i valori statistici;
- i link generati con `url_for`.

Domande:

- quale tag HTML rappresenta un pannello cliccabile?
- quale attributo contiene la destinazione del click?
- quali valori sono inseriti dal server tramite Jinja?

## 2. Dalla route al template

Nel file `app.py`, cercare la funzione:

```python
def index():
```

Ricostruire il flusso:

```text
GET /
  -> index()
      -> query di conteggio
          -> render_template("index.html", stats=stats)
```

Domande:

- quali dati vengono letti dal database?
- dove vengono inseriti nel template?
- quale HTML finale riceve il browser?

## 3. Click su un ruolo

Cliccare "Amministratore".

Seguire il percorso nel codice:

```text
click sul link
  -> GET /admin
      -> admin_home()
          -> role.html
```

Domande:

- dove viene definito l'URL `/admin`?
- quale template viene usato?
- quali informazioni vengono passate al template?

## 4. Lista generica

Aprire la lista degli iscritti.

Seguire:

```text
GET /entity/iscritti
  -> entity_list("iscritti")
      -> configurazione ENTITIES["iscritti"]
          -> SELECT ...
              -> entity_list.html
```

Domande:

- perche' la stessa route puo' funzionare anche per istruttori ed esercizi?
- quali campi vengono mostrati nella tabella?
- dove viene definito l'ordinamento?

## 5. Form e POST

Aprire il form per creare un nuovo iscritto.

Compilare un record di prova:

```text
id: 99
nome: Test
cognome: Web
data nascita: 2001-01-01
data iscrizione: 2026-05-19
```

Seguire:

```text
GET /entity/iscritti/new
  -> mostra form

POST /entity/iscritti/new
  -> legge request.form
      -> INSERT
          -> flash
              -> redirect alla lista
```

Domande:

- quali tag `input` generano i valori?
- come Flask legge quei valori?
- perche' dopo il POST viene fatto un redirect?

## 6. Evento e vincolo

Provare a creare un iscritto con lo stesso `id_iscritto` gia' usato.

Osservare:

- messaggio nel browser;
- errore gestito in Flask;
- vincolo di chiave primaria nel database.

Domande:

- l'errore nasce nel browser, in Flask o nel database?
- perche' l'interfaccia deve comunque mostrarlo in modo comprensibile?

## 7. Traccia finale

Scegliere una delle seguenti azioni:

- creare un nuovo esercizio;
- aggiornare una scheda;
- registrare una esecuzione come iscritto.

Per l'azione scelta, scrivere una traccia di flusso:

```text
oggetto grafico
  -> evento
      -> richiesta HTTP
          -> route Flask
              -> dati letti da request.form
                  -> query SQL
                      -> redirect / template
                          -> DOM finale
```
