"""
interfaccia/repl.py — Il REPL della rubrica in versione OOP

PERCORSO DIDATTICO:
    Nella Lezione precedente, il REPL era una funzione con un lungo if/elif.
    Qui diventa una CLASSE che:
    1. Incapsula lo stato della sessione (rubrica, store, flag modificata)
    2. Usa un dizionario di dispatch (metodi come valori)
    3. Separa l'interfaccia utente dalla logica di dominio

    La classe RubricaREPL conosce Rubrica e JsonStore, ma:
    - Rubrica NON conosce il REPL (non sa come viene usata)
    - JsonStore NON conosce il REPL (non sa chi lo chiama)

    Questa è la direzione delle dipendenze:
        RubricaREPL → Rubrica ← JsonStore
                  ↘            ↙
                    Contatto

    L'interfaccia (REPL) dipende dal modello (Rubrica/Contatto),
    mai il contrario. Se domani il REPL diventa una GUI web,
    Rubrica e Contatto non cambiano di una riga.
"""

from modelli import Contatto
from modelli import Rubrica
from persistenza import JsonStore


class RubricaREPL:
    """
    Interfaccia a linea di comando per la rubrica.

    Architettura: REPL con dispatch dictionary.
    Ogni comando del menu è un metodo della classe,
    mappato nel dizionario self._comandi.
    """

    VERSIONE = "3.0 (OOP)"

    def __init__(self, percorso_file="rubrica.json"):
        """
        Inizializza il REPL: carica la rubrica dal file.

        Args:
            percorso_file: percorso del file JSON di persistenza
        """
        self._store = JsonStore(percorso_file)
        self._rubrica = self._store.carica()
        self._modificata = False

        # Dizionario di dispatch: ogni chiave è un comando del menu,
        # ogni valore è il METODO (bound method) da eseguire.
        # Nota: self._cmd_aggiungi (senza parentesi) è un riferimento
        # alla funzione, non una chiamata.
        self._comandi = {
            "1": ("Aggiungi contatto", self._cmd_aggiungi),
            "2": ("Visualizza contatto", self._cmd_visualizza),
            "3": ("Mostra rubrica", self._cmd_mostra_tutti),
            "4": ("Aggiorna contatto", self._cmd_aggiorna),
            "5": ("Elimina contatto", self._cmd_elimina),
            "6": ("Cerca per nome", self._cmd_cerca_per_nome),
            "7": ("Cerca per numero", self._cmd_cerca_per_numero),
            "8": ("Filtra per gruppo", self._cmd_filtra_gruppo),  
            "9": ("Statistiche", self._cmd_statistiche),
            "10": ("Salva su file", self._cmd_salva),
        }

    # ---------------------------------------------------------------
    # IL CICLO REPL
    # ---------------------------------------------------------------

    def esegui(self):
        """
        Avvia il ciclo Read-Eval-Print-Loop.

        Questo è l'unico metodo pubblico "di ingresso".
        Tutto il resto è implementazione interna.
        """
        print(f"\n{'=' * 44}")
        print(f"  RUBRICA TELEFONICA v{self.VERSIONE}")
        print(f"  File: {self._store.percorso}")
        print(f"  Contatti caricati: {len(self._rubrica)}")
        print(f"{'=' * 44}")

        while True:
            # PRINT (menu)
            self._mostra_menu()

            # READ
            scelta = input("\nScegli (0-9): ").strip()

            # Condizione di uscita
            if scelta == "0":
                self._cmd_esci()
                break

            # EVAL (dispatch)
            if scelta in self._comandi:
                _, funzione = self._comandi[scelta]
                try:
                    funzione()  # Chiama il metodo associato
                except (ValueError, KeyError) as errore:
                    print(f"\n  Errore: {errore}")
                except KeyboardInterrupt:
                    print("\n  Operazione annullata.")
            else:
                print("  Scelta non valida.")

            # LOOP: il while ricomincia

    # ---------------------------------------------------------------
    # MENU
    # ---------------------------------------------------------------

    def _mostra_menu(self):
        """Genera il menu dinamicamente dal dizionario di dispatch."""
        print(f"\n{'─' * 44}")
        for codice, (etichetta, _) in sorted(self._comandi.items()):
            print(f"  {codice}. {etichetta}")
        print(f"   0. Salva ed esci")
        print(f"{'─' * 44}")

    # ---------------------------------------------------------------
    # COMANDI (metodi privati, uno per voce di menu)
    # ---------------------------------------------------------------

    def _cmd_aggiungi(self):
        """Comando: aggiungi un nuovo contatto."""
        nome = input("  Nome e cognome: ").strip()
        if not nome:
            print("  Nome obbligatorio.")
            return

        # Se il contatto esiste, aggiungi solo un telefono
        if nome in self._rubrica:
            telefono = input("  Contatto esistente. Nuovo telefono: ").strip()
            self._rubrica.aggiungi_telefono(nome, telefono)
            print(f"  Aggiunto telefono a {nome}.")
            self._modificata = True
            return

        telefono = input("  Telefono: ").strip()
        email = input("  Email (invio per saltare): ").strip()
        citta = input("  Città (invio per saltare): ").strip()
        gruppo = input("  Gruppo [generale/lavoro/amici/famiglia]: ").strip()
        if not gruppo:
            gruppo = "generale"

        contatto = Contatto(nome, telefono, email, citta, gruppo)
        self._rubrica.aggiungi(contatto)
        print(f"  Contatto '{nome}' creato.")
        self._modificata = True

    def _cmd_visualizza(self):
        """Comando: mostra un singolo contatto."""
        nome = input("  Nome: ").strip()
        contatto = self._rubrica.ottieni(nome)
        if contatto is None:
            print(f"  '{nome}' non trovato.")
        else:
            print()
            print(contatto)  # Usa Contatto.__str__

    def _cmd_mostra_tutti(self):
        """Comando: mostra l'intera rubrica."""
        print()
        print(self._rubrica)  # Usa Rubrica.__str__, che usa __iter__

    def _cmd_aggiorna(self):
        """Comando: aggiorna un campo di un contatto."""
        nome = input("  Nome: ").strip()
        if nome not in self._rubrica:  # Usa Rubrica.__contains__
            print(f"  '{nome}' non trovato.")
            return

        campo = input("  Campo [telefoni/email/citta/gruppo]: ").strip()

        if campo == "citta":
            valore = input("  Nuova città: ").strip()
            self._rubrica.aggiorna_citta(nome, valore)
        elif campo == "gruppo":
            valore = input("  Nuovo gruppo: ").strip()
            self._rubrica.aggiorna_gruppo(nome, valore)
        elif campo == "telefoni":
            valore = input("  Nuovo telefono da aggiungere: ").strip()
            self._rubrica.aggiungi_telefono(nome, valore)
        elif campo == "email":
            valore = input("  Nuova email da aggiungere: ").strip()
            self._rubrica[nome].aggiungi_email(valore)  # Usa __getitem__
        else:
            print(f"  Campo '{campo}' non valido.")
            return

        print(f"  {nome} aggiornato.")
        self._modificata = True

    def _cmd_elimina(self):
        """Comando: elimina un contatto con conferma."""
        nome = input("  Nome da eliminare: ").strip()
        if nome not in self._rubrica:
            print(f"  '{nome}' non trovato.")
            return

        conferma = input(f"  Eliminare '{nome}'? (s/n): ").strip().lower()
        if conferma == "s":
            self._rubrica.elimina(nome)
            print(f"  '{nome}' eliminato.")
            self._modificata = True
        else:
            print("  Annullato.")

    def _cmd_cerca_per_nome(self):
        """Comando: ricerca per nome parziale."""
        testo = input("  Testo da cercare: ").strip()
        risultati = self._rubrica.cerca(testo)
        if not risultati:
            print("  Nessun contatto trovato.")
        else:
            print(f"  Trovati {len(risultati)} contatti:\n")
            for contatto in risultati:
                print(contatto)
                print()

    def _cmd_cerca_per_numero(self):
        """Comando: ricerca per numero esatto."""
        numero = input("  Numero da cercare: ").strip()
        risultati = self._rubrica.cerca_numero(numero)
        if not risultati:
            print(f"  Nessun contatto trovato per il numero {numero}.")
        else:
            print(f"  Trovati {len(risultati)} contatti:\n")
            for contatto in risultati:
                print(contatto)
                print()



    def _cmd_filtra_gruppo(self):
        """Comando: filtra per gruppo."""
        gruppo = input("  Gruppo [generale/lavoro/amici/famiglia]: ").strip()
        risultati = self._rubrica.filtra_per_gruppo(gruppo)
        if not risultati:
            print(f"  Nessun contatto nel gruppo '{gruppo}'.")
        else:
            print(f"  Contatti nel gruppo '{gruppo}':")
            for contatto in risultati:
                print(f"    - {contatto.nome} ({contatto.citta})")

    def _cmd_statistiche(self):
        """Comando: mostra statistiche."""
        stats = self._rubrica.statistiche()
        if "errore" in stats:
            print(f"  {stats['errore']}")
            return
        print(f"\n  Contatti: {stats['totale_contatti']}")
        print(f"  Numeri di telefono: {stats['totale_telefoni']}")
        print(f"  Media numeri/contatto: {stats['media_telefoni']}")
        print(f"  Record: {stats['contatto_con_piu_numeri']} ({stats['max_numeri']} numeri)")
        print(f"  Gruppi: {stats['distribuzione_gruppi']}")

    def _cmd_salva(self):
        """Comando: salvataggio manuale."""
        if self._store.salva(self._rubrica):
            print(f"  Salvati {len(self._rubrica)} contatti.")
            self._modificata = False
        else:
            print("  Salvataggio fallito.")

    def _cmd_esci(self):
        """Gestisce l'uscita con salvataggio condizionale."""
        if self._modificata:
            risposta = input("\n  Modifiche non salvate. Salvare? (s/n/annulla): ").strip().lower()
            if risposta == "annulla":
                return  # Non esce (ma in esegui() il break è comunque dopo)
            if risposta == "s":
                self._cmd_salva()
        print("\n  Arrivederci!")


# ===================================================================
# TEST STANDALONE
# ===================================================================
if __name__ == "__main__":
    repl = RubricaREPL("test_repl.json")
    repl.esegui()
