#!/usr/bin/env python3
"""
Applicazione web Flask per il laboratorio palestra.
"""

from pathlib import Path
import sqlite3
import sys

from flask import Flask, flash, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = BASE_DIR / "runtime"
DB_PATH = RUNTIME_DIR / "palestra.sqlite"
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"


app = Flask(__name__)
app.config["SECRET_KEY"] = "laboratorio-palestra-web"


ENTITIES = {
    "iscritti": {
        "table": "Iscritti",
        "pk": "id_iscritto",
        "title": "Iscritti",
        "role": "admin",
        "columns": ["id_iscritto", "nome", "cognome", "data_nascita", "data_iscrizione"],
        "fields": [
            ("id_iscritto", "ID", "number", True),
            ("nome", "Nome", "text", True),
            ("cognome", "Cognome", "text", True),
            ("data_nascita", "Data nascita", "date", True),
            ("data_iscrizione", "Data iscrizione", "date", True),
        ],
        "order": "cognome, nome",
    },
    "istruttori": {
        "table": "Istruttori",
        "pk": "id_istruttore",
        "title": "Istruttori",
        "role": "admin",
        "columns": ["id_istruttore", "nome", "cognome", "specializzazione"],
        "fields": [
            ("id_istruttore", "ID", "number", True),
            ("nome", "Nome", "text", True),
            ("cognome", "Cognome", "text", True),
            ("specializzazione", "Specializzazione", "text", False),
        ],
        "order": "cognome, nome",
    },
    "esercizi": {
        "table": "Esercizi",
        "pk": "id_esercizio",
        "title": "Esercizi",
        "role": "trainer",
        "columns": ["id_esercizio", "nome_esercizio", "categoria", "descrizione"],
        "fields": [
            ("id_esercizio", "ID", "number", True),
            ("nome_esercizio", "Nome esercizio", "text", True),
            ("categoria", "Categoria", "text", False),
            ("descrizione", "Descrizione", "text", False),
        ],
        "order": "nome_esercizio",
    },
}


def init_db(reset=False):
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    if reset and DB_PATH.exists():
        DB_PATH.unlink()
    if DB_PATH.exists():
        return

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.executescript(SEED_PATH.read_text(encoding="utf-8"))
        conn.commit()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def rows(sql, params=()):
    with get_db() as conn:
        return conn.execute(sql, params).fetchall()


def row(sql, params=()):
    with get_db() as conn:
        return conn.execute(sql, params).fetchone()


def execute(sql, params=()):
    with get_db() as conn:
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor.lastrowid


def form_value(name, field_type):
    value = request.form.get(name, "").strip()
    if value == "":
        return None
    if field_type == "number":
        return int(value)
    return value


def entity_config(name):
    config = ENTITIES.get(name)
    if config is None:
        raise KeyError(name)
    return config


@app.errorhandler(sqlite3.IntegrityError)
def handle_integrity_error(exc):
    flash(f"Operazione bloccata dai vincoli del database: {exc}", "error")
    return redirect(request.referrer or url_for("index"))


@app.get("/")
def index():
    stats = {
        "iscritti": row("SELECT COUNT(*) AS total FROM Iscritti")["total"],
        "istruttori": row("SELECT COUNT(*) AS total FROM Istruttori")["total"],
        "schede": row("SELECT COUNT(*) AS total FROM SchedeAllenamento")["total"],
        "esecuzioni": row("SELECT COUNT(*) AS total FROM Esecuzioni")["total"],
    }
    return render_template("index.html", stats=stats)


@app.get("/admin")
def admin_home():
    return render_template("role.html", role="amministratore", cards=[
        ("Iscritti", "Gestione iscritti della palestra", url_for("entity_list", name="iscritti")),
        ("Istruttori", "Gestione istruttori e specializzazioni", url_for("entity_list", name="istruttori")),
    ])


@app.get("/trainer")
def trainer_home():
    return render_template("role.html", role="istruttore", cards=[
        ("Esercizi", "Archivio esercizi disponibili", url_for("entity_list", name="esercizi")),
        ("Schede", "Schede di allenamento assegnate", url_for("schede_list")),
    ])


@app.get("/member")
def member_home():
    iscritti = rows("SELECT id_iscritto, nome, cognome FROM Iscritti ORDER BY cognome, nome")
    return render_template("member_select.html", iscritti=iscritti)


@app.get("/entity/<name>")
def entity_list(name):
    config = entity_config(name)
    data = rows(
        f"SELECT {', '.join(config['columns'])} FROM {config['table']} ORDER BY {config['order']}"
    )
    return render_template("entity_list.html", config=config, rows=data, name=name)


@app.route("/entity/<name>/new", methods=["GET", "POST"])
def entity_new(name):
    config = entity_config(name)
    if request.method == "POST":
        columns = [field[0] for field in config["fields"]]
        values = [form_value(field[0], field[2]) for field in config["fields"]]
        placeholders = ", ".join("?" for _ in columns)
        execute(
            f"INSERT INTO {config['table']} ({', '.join(columns)}) VALUES ({placeholders})",
            values,
        )
        flash(f"{config['title']} aggiornato.", "success")
        return redirect(url_for("entity_list", name=name))
    return render_template("entity_form.html", config=config, item=None, name=name)


@app.route("/entity/<name>/<int:item_id>/edit", methods=["GET", "POST"])
def entity_edit(name, item_id):
    config = entity_config(name)
    item = row(f"SELECT * FROM {config['table']} WHERE {config['pk']} = ?", (item_id,))
    if item is None:
        flash("Record non trovato.", "error")
        return redirect(url_for("entity_list", name=name))

    if request.method == "POST":
        fields = [field for field in config["fields"] if field[0] != config["pk"]]
        assignments = ", ".join(f"{field[0]} = ?" for field in fields)
        values = [form_value(field[0], field[2]) for field in fields]
        values.append(item_id)
        execute(f"UPDATE {config['table']} SET {assignments} WHERE {config['pk']} = ?", values)
        flash("Record aggiornato.", "success")
        return redirect(url_for("entity_list", name=name))
    return render_template("entity_form.html", config=config, item=item, name=name)


@app.post("/entity/<name>/<int:item_id>/delete")
def entity_delete(name, item_id):
    config = entity_config(name)
    execute(f"DELETE FROM {config['table']} WHERE {config['pk']} = ?", (item_id,))
    flash("Record eliminato.", "success")
    return redirect(url_for("entity_list", name=name))


@app.get("/schede")
def schede_list():
    data = rows(
        """
        SELECT
            s.id_scheda,
            s.titolo,
            i.nome || ' ' || i.cognome AS iscritto,
            it.nome || ' ' || it.cognome AS istruttore,
            s.data_inizio,
            s.data_fine,
            s.attiva
        FROM SchedeAllenamento s
        JOIN Iscritti i ON s.id_iscritto = i.id_iscritto
        JOIN Istruttori it ON s.id_istruttore = it.id_istruttore
        ORDER BY s.id_scheda
        """
    )
    return render_template("schede_list.html", schede=data)


@app.route("/schede/new", methods=["GET", "POST"])
def scheda_new():
    if request.method == "POST":
        execute(
            """
            INSERT INTO SchedeAllenamento (
                id_scheda, id_iscritto, id_istruttore, titolo, data_inizio, data_fine, attiva
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(request.form["id_scheda"]),
                int(request.form["id_iscritto"]),
                int(request.form["id_istruttore"]),
                request.form["titolo"].strip(),
                request.form["data_inizio"],
                request.form.get("data_fine") or None,
                int(request.form.get("attiva", "0")),
            ),
        )
        flash("Scheda creata.", "success")
        return redirect(url_for("schede_list"))
    return render_template("scheda_form.html", scheda=None, iscritti=iscritti_options(), istruttori=istruttori_options())


@app.route("/schede/<int:scheda_id>/edit", methods=["GET", "POST"])
def scheda_edit(scheda_id):
    scheda = row("SELECT * FROM SchedeAllenamento WHERE id_scheda = ?", (scheda_id,))
    if scheda is None:
        flash("Scheda non trovata.", "error")
        return redirect(url_for("schede_list"))
    if request.method == "POST":
        execute(
            """
            UPDATE SchedeAllenamento
            SET id_iscritto = ?, id_istruttore = ?, titolo = ?, data_inizio = ?, data_fine = ?, attiva = ?
            WHERE id_scheda = ?
            """,
            (
                int(request.form["id_iscritto"]),
                int(request.form["id_istruttore"]),
                request.form["titolo"].strip(),
                request.form["data_inizio"],
                request.form.get("data_fine") or None,
                int(request.form.get("attiva", "0")),
                scheda_id,
            ),
        )
        flash("Scheda aggiornata.", "success")
        return redirect(url_for("schede_list"))
    return render_template("scheda_form.html", scheda=scheda, iscritti=iscritti_options(), istruttori=istruttori_options())


@app.post("/schede/<int:scheda_id>/delete")
def scheda_delete(scheda_id):
    execute("DELETE FROM SchedeAllenamento WHERE id_scheda = ?", (scheda_id,))
    flash("Scheda eliminata.", "success")
    return redirect(url_for("schede_list"))


@app.get("/schede/<int:scheda_id>")
def scheda_detail(scheda_id):
    scheda = row(
        """
        SELECT
            s.*,
            i.nome || ' ' || i.cognome AS iscritto,
            it.nome || ' ' || it.cognome AS istruttore
        FROM SchedeAllenamento s
        JOIN Iscritti i ON s.id_iscritto = i.id_iscritto
        JOIN Istruttori it ON s.id_istruttore = it.id_istruttore
        WHERE s.id_scheda = ?
        """,
        (scheda_id,),
    )
    if scheda is None:
        flash("Scheda non trovata.", "error")
        return redirect(url_for("schede_list"))
    dettagli = scheda_rows(scheda_id)
    return render_template("scheda_detail.html", scheda=scheda, dettagli=dettagli)


@app.route("/schede/<int:scheda_id>/rows/new", methods=["GET", "POST"])
def scheda_row_new(scheda_id):
    if request.method == "POST":
        execute(
            """
            INSERT INTO SchedaEsercizi (
                id_scheda, ordine_esecuzione, id_esercizio, serie, ripetizioni,
                carico_suggerito, durata_secondi, recupero_secondi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            scheda_row_values(scheda_id),
        )
        flash("Esercizio aggiunto alla scheda.", "success")
        return redirect(url_for("scheda_detail", scheda_id=scheda_id))
    return render_template("scheda_row_form.html", scheda_id=scheda_id, item=None, esercizi=esercizi_options())


@app.route("/schede/<int:scheda_id>/rows/<int:ordine>/edit", methods=["GET", "POST"])
def scheda_row_edit(scheda_id, ordine):
    item = row(
        "SELECT * FROM SchedaEsercizi WHERE id_scheda = ? AND ordine_esecuzione = ?",
        (scheda_id, ordine),
    )
    if item is None:
        flash("Riga scheda non trovata.", "error")
        return redirect(url_for("scheda_detail", scheda_id=scheda_id))
    if request.method == "POST":
        values = list(scheda_row_values(scheda_id, include_order=False))
        values.extend([scheda_id, ordine])
        execute(
            """
            UPDATE SchedaEsercizi
            SET id_esercizio = ?, serie = ?, ripetizioni = ?, carico_suggerito = ?, durata_secondi = ?, recupero_secondi = ?
            WHERE id_scheda = ? AND ordine_esecuzione = ?
            """,
            values,
        )
        flash("Riga scheda aggiornata.", "success")
        return redirect(url_for("scheda_detail", scheda_id=scheda_id))
    return render_template("scheda_row_form.html", scheda_id=scheda_id, item=item, esercizi=esercizi_options())


@app.post("/schede/<int:scheda_id>/rows/<int:ordine>/delete")
def scheda_row_delete(scheda_id, ordine):
    execute(
        "DELETE FROM SchedaEsercizi WHERE id_scheda = ? AND ordine_esecuzione = ?",
        (scheda_id, ordine),
    )
    flash("Riga scheda eliminata.", "success")
    return redirect(url_for("scheda_detail", scheda_id=scheda_id))


@app.get("/member/<int:iscritto_id>")
def member_dashboard(iscritto_id):
    iscritto = row("SELECT * FROM Iscritti WHERE id_iscritto = ?", (iscritto_id,))
    if iscritto is None:
        flash("Iscritto non trovato.", "error")
        return redirect(url_for("member_home"))
    schede = rows(
        "SELECT id_scheda, titolo, data_inizio, data_fine, attiva FROM SchedeAllenamento WHERE id_iscritto = ? ORDER BY data_inizio DESC",
        (iscritto_id,),
    )
    esecuzioni = member_execution_rows(iscritto_id)
    return render_template("member_dashboard.html", iscritto=iscritto, schede=schede, esecuzioni=esecuzioni)


@app.route("/member/<int:iscritto_id>/esecuzioni/new", methods=["GET", "POST"])
def execution_new(iscritto_id):
    iscritto = row("SELECT * FROM Iscritti WHERE id_iscritto = ?", (iscritto_id,))
    if iscritto is None:
        flash("Iscritto non trovato.", "error")
        return redirect(url_for("member_home"))
    if request.method == "POST":
        execute(
            """
            INSERT INTO Esecuzioni (
                id_esecuzione, id_iscritto, id_scheda, ordine_esecuzione,
                data_esecuzione, carico_effettivo, ripetizioni_effettive, nota
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            execution_values(iscritto_id),
        )
        flash("Esecuzione registrata.", "success")
        return redirect(url_for("member_dashboard", iscritto_id=iscritto_id))
    return render_template("execution_form.html", iscritto=iscritto, item=None, options=member_exercise_options(iscritto_id))


@app.route("/member/<int:iscritto_id>/esecuzioni/<int:execution_id>/edit", methods=["GET", "POST"])
def execution_edit(iscritto_id, execution_id):
    iscritto = row("SELECT * FROM Iscritti WHERE id_iscritto = ?", (iscritto_id,))
    item = row(
        "SELECT * FROM Esecuzioni WHERE id_esecuzione = ? AND id_iscritto = ?",
        (execution_id, iscritto_id),
    )
    if iscritto is None or item is None:
        flash("Esecuzione non trovata.", "error")
        return redirect(url_for("member_home"))
    if request.method == "POST":
        execute(
            """
            UPDATE Esecuzioni
            SET id_scheda = ?, ordine_esecuzione = ?, data_esecuzione = ?, carico_effettivo = ?, ripetizioni_effettive = ?, nota = ?
            WHERE id_esecuzione = ? AND id_iscritto = ?
            """,
            execution_update_values(execution_id, iscritto_id),
        )
        flash("Esecuzione aggiornata.", "success")
        return redirect(url_for("member_dashboard", iscritto_id=iscritto_id))
    return render_template("execution_form.html", iscritto=iscritto, item=item, options=member_exercise_options(iscritto_id))


@app.post("/member/<int:iscritto_id>/esecuzioni/<int:execution_id>/delete")
def execution_delete(iscritto_id, execution_id):
    execute(
        "DELETE FROM Esecuzioni WHERE id_esecuzione = ? AND id_iscritto = ?",
        (execution_id, iscritto_id),
    )
    flash("Esecuzione eliminata.", "success")
    return redirect(url_for("member_dashboard", iscritto_id=iscritto_id))


def iscritti_options():
    return rows("SELECT id_iscritto, nome, cognome FROM Iscritti ORDER BY cognome, nome")


def istruttori_options():
    return rows("SELECT id_istruttore, nome, cognome FROM Istruttori ORDER BY cognome, nome")


def esercizi_options():
    return rows("SELECT id_esercizio, nome_esercizio FROM Esercizi ORDER BY nome_esercizio")


def scheda_rows(scheda_id):
    return rows(
        """
        SELECT
            se.ordine_esecuzione,
            e.nome_esercizio,
            se.serie,
            se.ripetizioni,
            se.carico_suggerito,
            se.durata_secondi,
            se.recupero_secondi
        FROM SchedaEsercizi se
        JOIN Esercizi e ON se.id_esercizio = e.id_esercizio
        WHERE se.id_scheda = ?
        ORDER BY se.ordine_esecuzione
        """,
        (scheda_id,),
    )


def optional_int(name):
    value = request.form.get(name, "").strip()
    return None if value == "" else int(value)


def optional_float(name):
    value = request.form.get(name, "").strip()
    return None if value == "" else float(value)


def scheda_row_values(scheda_id, include_order=True):
    base = [
        int(request.form["id_esercizio"]),
        int(request.form["serie"]),
        optional_int("ripetizioni"),
        optional_float("carico_suggerito"),
        optional_int("durata_secondi"),
        optional_int("recupero_secondi"),
    ]
    if include_order:
        return [scheda_id, int(request.form["ordine_esecuzione"]), *base]
    return base


def member_execution_rows(iscritto_id):
    return rows(
        """
        SELECT
            ex.id_esecuzione,
            ex.data_esecuzione,
            ex.id_scheda,
            ex.ordine_esecuzione,
            e.nome_esercizio,
            ex.carico_effettivo,
            ex.ripetizioni_effettive,
            ex.nota
        FROM Esecuzioni ex
        JOIN SchedaEsercizi se ON ex.id_scheda = se.id_scheda
            AND ex.ordine_esecuzione = se.ordine_esecuzione
        JOIN Esercizi e ON se.id_esercizio = e.id_esercizio
        WHERE ex.id_iscritto = ?
        ORDER BY ex.data_esecuzione DESC, ex.id_esecuzione DESC
        """,
        (iscritto_id,),
    )


def member_exercise_options(iscritto_id):
    return rows(
        """
        SELECT
            s.id_scheda,
            se.ordine_esecuzione,
            s.titolo,
            e.nome_esercizio
        FROM SchedeAllenamento s
        JOIN SchedaEsercizi se ON s.id_scheda = se.id_scheda
        JOIN Esercizi e ON se.id_esercizio = e.id_esercizio
        WHERE s.id_iscritto = ?
        ORDER BY s.data_inizio DESC, se.ordine_esecuzione
        """,
        (iscritto_id,),
    )


def execution_values(iscritto_id):
    return (
        int(request.form["id_esecuzione"]),
        iscritto_id,
        int(request.form["id_scheda"]),
        int(request.form["ordine_esecuzione"]),
        request.form["data_esecuzione"],
        optional_float("carico_effettivo"),
        optional_int("ripetizioni_effettive"),
        request.form.get("nota") or None,
    )


def execution_update_values(execution_id, iscritto_id):
    return (
        int(request.form["id_scheda"]),
        int(request.form["ordine_esecuzione"]),
        request.form["data_esecuzione"],
        optional_float("carico_effettivo"),
        optional_int("ripetizioni_effettive"),
        request.form.get("nota") or None,
        execution_id,
        iscritto_id,
    )


if __name__ == "__main__":
    init_db(reset="--reset" in sys.argv)
    app.run(debug=True, use_reloader=False)
