#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return "<!DOCTYPE html>\
<html>\
<head>\
<title>Gestione Palestra</title>\
</head>\
<body>\
\
<h1>Scegli il ruolo</h1>\
<a href=\"/admin\">Admin</a><BR>\
<a href=\"/istruttori\">Istruttori</a><BR>\
<a href=\"/utenti\">Utenti</a><BR>\
\
</body>\
</html>"

@app.get("/admin")
def admin():
    return "Inizio gestione amministratore"

@app.get("/istruttori")
def istruttori():
    return "Inizio gestione istruttori"

@app.get("/utenti")
def utenti():
    return "Inizio gestione utenti"

if __name__ == "__main__":
    app.run(debug=True)
