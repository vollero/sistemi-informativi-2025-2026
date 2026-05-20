#!/usr/bin/env python3
"""
Demo progressive di interfacce web con Flask.

Il laboratorio e' volutamente indipendente dall'app palestra: ogni pagina mette
in evidenza un singolo concetto dell'interfaccia web.
"""

from copy import deepcopy

from flask import Flask, flash, redirect, render_template, request, url_for


app = Flask(__name__)
app.config["SECRET_KEY"] = "demo-flask-interfacce"


ISCRITTI = [
    {"nome": "Alice", "cognome": "Conti", "obiettivo": "forza"},
    {"nome": "Marco", "cognome": "De Santis", "obiettivo": "ricondizionamento"},
    {"nome": "Sara", "cognome": "Leoni", "obiettivo": "mobilita'"},
]

SCHEDE = [
    {"titolo": "Forza base", "esercizi": 5, "stato": "attiva"},
    {"titolo": "Core stability", "esercizi": 4, "stato": "bozza"},
    {"titolo": "Recupero funzionale", "esercizi": 6, "stato": "attiva"},
]

COMPONENTI = [
    {
        "nome": "Pannello",
        "html": "<section>",
        "ruolo": "raggruppa informazioni correlate",
    },
    {
        "nome": "Link",
        "html": "<a>",
        "ruolo": "genera navigazione verso una route",
    },
    {
        "nome": "Campo input",
        "html": "<input>",
        "ruolo": "raccoglie un valore da inviare al server",
    },
    {
        "nome": "Pulsante",
        "html": "<button>",
        "ruolo": "attiva una azione o invia un form",
    },
]

TASK_INIZIALI = [
    {"id": 1, "titolo": "Disegnare la home", "stato": "da fare"},
    {"id": 2, "titolo": "Definire le route principali", "stato": "in corso"},
    {"id": 3, "titolo": "Collegare un form a una POST", "stato": "fatto"},
]
TASKS = deepcopy(TASK_INIZIALI)
PROSSIMO_ID = 4


@app.get("/")
def index():
    demo = [
        ("01", "Pagina statica", "HTML, layout e DOM iniziale", url_for("demo_pagina_statica")),
        ("02", "Template dinamico", "Dati Python renderizzati con Jinja", url_for("demo_template")),
        ("03", "Componenti grafici", "Mappa tra oggetti visibili e tag HTML", url_for("demo_componenti")),
        ("04", "Form GET/POST", "Submit, request.form, validazione e risposta", url_for("demo_form")),
        ("05", "Eventi DOM", "Click e input gestiti nel browser", url_for("demo_eventi")),
        ("06", "Mini CRUD", "Creazione ed eliminazione in memoria", url_for("demo_crud")),
    ]
    return render_template("index.html", demo=demo)


@app.get("/demo/01-pagina-statica")
def demo_pagina_statica():
    return render_template("demo_static.html")


@app.get("/demo/02-template")
def demo_template():
    return render_template("demo_template.html", iscritti=ISCRITTI, schede=SCHEDE)


@app.get("/demo/03-componenti")
def demo_componenti():
    return render_template("demo_components.html", componenti=COMPONENTI)


@app.route("/demo/04-form", methods=["GET", "POST"])
def demo_form():
    risultato = None
    errori = []

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        ruolo = request.form.get("ruolo", "").strip()
        nota = request.form.get("nota", "").strip()

        if not nome:
            errori.append("Il nome e' obbligatorio.")
        if ruolo not in {"amministratore", "istruttore", "iscritto"}:
            errori.append("Selezionare un ruolo valido.")

        if not errori:
            risultato = {
                "nome": nome,
                "ruolo": ruolo,
                "nota": nota or "nessuna nota inserita",
            }

    return render_template("demo_form.html", risultato=risultato, errori=errori)


@app.get("/demo/05-eventi")
def demo_eventi():
    return render_template("demo_events.html", schede=SCHEDE)


@app.route("/demo/06-crud", methods=["GET", "POST"])
def demo_crud():
    global PROSSIMO_ID

    if request.method == "POST":
        titolo = request.form.get("titolo", "").strip()
        stato = request.form.get("stato", "da fare").strip()

        if not titolo:
            flash("Il titolo dell'attivita' e' obbligatorio.", "error")
            return redirect(url_for("demo_crud"))

        TASKS.append({"id": PROSSIMO_ID, "titolo": titolo, "stato": stato})
        PROSSIMO_ID += 1
        flash("Attivita' aggiunta alla lista in memoria.", "success")
        return redirect(url_for("demo_crud"))

    return render_template("demo_crud.html", tasks=TASKS)


@app.post("/demo/06-crud/<int:task_id>/delete")
def demo_crud_delete(task_id):
    global TASKS
    TASKS = [task for task in TASKS if task["id"] != task_id]
    flash("Attivita' rimossa dalla lista in memoria.", "success")
    return redirect(url_for("demo_crud"))


@app.post("/demo/06-crud/reset")
def demo_crud_reset():
    global TASKS, PROSSIMO_ID
    TASKS = deepcopy(TASK_INIZIALI)
    PROSSIMO_ID = 4
    flash("Lista ripristinata.", "success")
    return redirect(url_for("demo_crud"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
