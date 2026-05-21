#!/usr/bin/env python3
"""
Kit minimale di template Flask riutilizzabili.

La mini-app usa dati in memoria per tenere il focus su pagine, template e CSS.
"""

from flask import Flask, flash, redirect, render_template, request, url_for


app = Flask(__name__)
app.config["SECRET_KEY"] = "template-minimali"


PROGETTI = [
    {
        "id": 1,
        "titolo": "Gestione palestra",
        "categoria": "sport",
        "stato": "in corso",
        "descrizione": "Schede, esercizi ed esecuzioni degli iscritti.",
    },
    {
        "id": 2,
        "titolo": "Biblioteca",
        "categoria": "servizi",
        "stato": "bozza",
        "descrizione": "Prestiti, libri, utenti e restituzioni.",
    },
    {
        "id": 3,
        "titolo": "Prenotazioni aula",
        "categoria": "universita",
        "stato": "idea",
        "descrizione": "Aule, fasce orarie, docenti e prenotazioni.",
    },
]

PROSSIMO_ID = 4


def prossimo_id():
    global PROSSIMO_ID
    valore = PROSSIMO_ID
    PROSSIMO_ID += 1
    return valore


def trova_progetto(progetto_id):
    return next((progetto for progetto in PROGETTI if progetto["id"] == progetto_id), None)


def valori_form():
    return {
        "titolo": request.form.get("titolo", "").strip(),
        "categoria": request.form.get("categoria", "").strip(),
        "stato": request.form.get("stato", "").strip(),
        "descrizione": request.form.get("descrizione", "").strip(),
    }


def valida_progetto(dati):
    errori = []
    if not dati["titolo"]:
        errori.append("Il titolo è obbligatorio.")
    if not dati["categoria"]:
        errori.append("La categoria è obbligatoria.")
    if dati["stato"] not in {"idea", "bozza", "in corso", "fatto"}:
        errori.append("Lo stato selezionato non è valido.")
    return errori


@app.get("/")
def home():
    statistiche = {
        "progetti": len(PROGETTI),
        "in_corso": sum(1 for progetto in PROGETTI if progetto["stato"] == "in corso"),
        "fatti": sum(1 for progetto in PROGETTI if progetto["stato"] == "fatto"),
    }
    return render_template("home.html", statistiche=statistiche)


@app.get("/dashboard")
def dashboard():
    statistiche = [
        ("Progetti", len(PROGETTI)),
        ("Idee", sum(1 for progetto in PROGETTI if progetto["stato"] == "idea")),
        ("Bozze", sum(1 for progetto in PROGETTI if progetto["stato"] == "bozza")),
        ("In corso", sum(1 for progetto in PROGETTI if progetto["stato"] == "in corso")),
    ]
    recenti = sorted(PROGETTI, key=lambda progetto: progetto["id"], reverse=True)[:3]
    return render_template("dashboard.html", statistiche=statistiche, recenti=recenti)


@app.get("/progetti")
def lista_progetti():
    return render_template("list.html", progetti=PROGETTI)


@app.route("/progetti/nuovo", methods=["GET", "POST"])
def nuovo_progetto():
    dati = {"titolo": "", "categoria": "", "stato": "idea", "descrizione": ""}
    errori = []

    if request.method == "POST":
        dati = valori_form()
        errori = valida_progetto(dati)
        if not errori:
            PROGETTI.append({"id": prossimo_id(), **dati})
            flash("Progetto creato.", "success")
            return redirect(url_for("lista_progetti"))

    return render_template(
        "form.html",
        titolo_pagina="Nuovo progetto",
        azione=url_for("nuovo_progetto"),
        progetto=dati,
        errori=errori,
    )


@app.get("/progetti/<int:progetto_id>")
def dettaglio_progetto(progetto_id):
    progetto = trova_progetto(progetto_id)
    if progetto is None:
        flash("Progetto non trovato.", "error")
        return redirect(url_for("lista_progetti"))
    return render_template("detail.html", progetto=progetto)


@app.route("/progetti/<int:progetto_id>/modifica", methods=["GET", "POST"])
def modifica_progetto(progetto_id):
    progetto = trova_progetto(progetto_id)
    if progetto is None:
        flash("Progetto non trovato.", "error")
        return redirect(url_for("lista_progetti"))

    dati = dict(progetto)
    errori = []

    if request.method == "POST":
        dati = valori_form()
        errori = valida_progetto(dati)
        if not errori:
            progetto.update(dati)
            flash("Progetto aggiornato.", "success")
            return redirect(url_for("dettaglio_progetto", progetto_id=progetto_id))

    return render_template(
        "form.html",
        titolo_pagina="Modifica progetto",
        azione=url_for("modifica_progetto", progetto_id=progetto_id),
        progetto=dati,
        errori=errori,
    )


@app.get("/progetti/<int:progetto_id>/elimina")
def conferma_eliminazione(progetto_id):
    progetto = trova_progetto(progetto_id)
    if progetto is None:
        flash("Progetto non trovato.", "error")
        return redirect(url_for("lista_progetti"))
    return render_template("confirm.html", progetto=progetto)


@app.post("/progetti/<int:progetto_id>/elimina")
def elimina_progetto(progetto_id):
    progetto = trova_progetto(progetto_id)
    if progetto is not None:
        PROGETTI.remove(progetto)
        flash("Progetto eliminato.", "success")
    return redirect(url_for("lista_progetti"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
