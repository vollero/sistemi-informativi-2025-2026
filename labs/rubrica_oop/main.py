#!/usr/bin/env python3
"""
main.py — Punto di ingresso dell'applicazione Rubrica OOP

Esecuzione:
    cd rubrica_oop
    python main.py                    # usa rubrica.json nella directory corrente
    python main.py --file mia.json    # specifica un file diverso

Struttura del progetto:
    rubrica_oop/
    ├── main.py                  ← Sei qui. Punto di ingresso.
    ├── modelli/
    │   ├── __init__.py
    │   ├── contatto.py          ← Classe Contatto (dati + validazione)
    │   └── rubrica.py           ← Classe Rubrica (collezione + protocolli Python)
    ├── persistenza/
    │   ├── __init__.py
    │   └── json_store.py        ← Classe JsonStore (salvataggio/caricamento)
    ├── interfaccia/
    │   ├── __init__.py
    │   └── repl.py              ← Classe RubricaREPL (menu interattivo)
    └── rubrica.json             ← Dati (generato automaticamente)

Architettura a 3 livelli:
    [Interfaccia]  →  [Logica di dominio]  ←  [Persistenza]
     RubricaREPL       Rubrica, Contatto       JsonStore

    Le frecce indicano la direzione delle dipendenze:
    - L'interfaccia CONOSCE il modello
    - La persistenza CONOSCE il modello
    - Il modello NON conosce né interfaccia né persistenza
"""

import sys
from interfaccia import RubricaREPL

def main():
    # Gestione argomenti da riga di comando (opzionale)
    percorso = "rubrica.json"
    if "--file" in sys.argv:
        indice = sys.argv.index("--file")
        if indice + 1 < len(sys.argv):
            percorso = sys.argv[indice + 1]

    # Avvia l'applicazione
    app = RubricaREPL(percorso)
    app.esegui()

if __name__ == "__main__":
    main()
