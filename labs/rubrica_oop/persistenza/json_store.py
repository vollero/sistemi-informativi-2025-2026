"""
persistenza/json_store.py — Persistenza su file JSON

PERCORSO DIDATTICO:
    Nella lezione precedente procedurale, carica_rubrica() e salva_rubrica() 
    erano funzioni "sciolte". In questa versione OOP, la persistenza diventa
    una CLASSE con una responsabilità ben definita.

    Principio: SEPARATION OF CONCERNS (Separazione delle responsabilità)
    - La classe Rubrica gestisce i contatti (logica di dominio)
    - La classe JsonStore gestisce il salvataggio/caricamento (persistenza)
    - La classe RubricaREPL gestisce l'interazione con l'utente (interfaccia)

    Ognuna fa UNA cosa e la fa bene. Se domani volessimo salvare su database
    invece che su JSON, basterebbe sostituire JsonStore con una classe
    DatabaseStore — senza toccare Rubrica né il REPL.
"""

import json
from modelli import Rubrica


class JsonStore:
    """
    Gestisce il salvataggio e il caricamento della rubrica su file JSON.

    Incapsula il nome del file e i parametri di formattazione,
    così il chiamante non deve preoccuparsi dei dettagli.
    """

    def __init__(self, percorso_file="rubrica.json"):
        """
        Args:
            percorso_file: percorso del file JSON (default: rubrica.json)
        """
        self._percorso = percorso_file

    @property
    def percorso(self):
        """Il percorso del file (sola lettura)."""
        return self._percorso

    def salva(self, rubrica):
        """
        Salva la rubrica su file JSON.

        Flusso: Rubrica → .to_dict() → json.dump() → file

        Args:
            rubrica: istanza di Rubrica

        Returns:
            True se il salvataggio è riuscito, False altrimenti
        """
        try:
            dati = rubrica.to_dict()
            file_output = open(self._percorso, "w", encoding="utf-8")
            json.dump(dati, file_output, indent=2, ensure_ascii=False)
            file_output.close()
            return True
        except (IOError, TypeError) as errore:
            print(f"Errore di salvataggio: {errore}")
            return False

    def carica(self):
        """
        Carica la rubrica da file JSON.

        Flusso: file → json.load() → Rubrica.from_dict() → Rubrica

        Returns:
            un'istanza di Rubrica (vuota se il file non esiste o è corrotto)
        """
        try:
            file_input = open(self._percorso, "r", encoding="utf-8")
            dati = json.load(file_input)
            file_input.close()
            rubrica = Rubrica.from_dict(dati)
            print(f"Caricati {len(rubrica)} contatti da '{self._percorso}'.")
            return rubrica
        except FileNotFoundError:
            print(f"File '{self._percorso}' non trovato. Rubrica vuota.")
            return Rubrica()
        except json.JSONDecodeError:
            print(f"File '{self._percorso}' corrotto. Rubrica vuota.")
            return Rubrica()
        except (KeyError, ValueError) as errore:
            print(f"Dati non validi in '{self._percorso}': {errore}. Rubrica vuota.")
            return Rubrica()

    def esiste(self):
        """Verifica se il file della rubrica esiste."""
        try:
            f = open(self._percorso, "r")
            f.close()
            return True
        except FileNotFoundError:
            return False


# ===================================================================
# TEST STANDALONE
# ===================================================================
if __name__ == "__main__":
    from modelli import Contatto

    # Crea rubrica di test
    r = Rubrica()
    r.aggiungi(Contatto("Mario Rossi", "06-1234567", "mario@email.it", "Roma", "lavoro"))
    r.aggiungi(Contatto("Anna Verdi", "02-9876543", "anna@email.it", "Milano", "amici"))

    # Salva
    store = JsonStore("test_rubrica.json")
    successo = store.salva(r)
    print(f"Salvataggio: {'OK' if successo else 'FALLITO'}")

    # Ricarica
    r2 = store.carica()
    print(f"\nRubrica ricaricata:")
    print(r2)
