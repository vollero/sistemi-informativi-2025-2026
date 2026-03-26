"""
modelli/rubrica.py — La classe Rubrica

PERCORSO DIDATTICO:
    Nella versione procedurale, la rubrica era un semplice dict globale.
    Le funzioni CRUD (aggiungi_contatto, mostra_contatto, ...) operavano
    su questo dizionario ricevuto come parametro.

    Problemi:
    1. Il dizionario è "nudo": nessuna protezione sulla sua struttura
    2. Le funzioni sono sparse: non c'è un posto unico dove cercare le operazioni
    3. Non si può iterare "naturalmente" (for contatto in rubrica: ...)

    La classe Rubrica risolve tutto questo e introduce i PROTOCOLLI Python:
    - __len__      → len(rubrica)
    - __contains__ → "Mario" in rubrica
    - __iter__     → for contatto in rubrica: ...
    - __getitem__  → rubrica["Mario"]
"""

from modelli import Contatto
# from contatto import Contatto


class Rubrica:
    """
    Collezione di contatti con interfaccia Pythonica.

    Implementa i protocolli Python per comportarsi come una collezione nativa:
    si può usare len(), in, for, e l'accesso con [].

    L'iteratore è il cuore di questa classe: permette di scrivere
        for contatto in rubrica:
            print(contatto.nome)
    esattamente come si farebbe con una lista o un dizionario.
    """

    def __init__(self):
        """Crea una rubrica vuota."""
        self._contatti = {}  # dict interno: {nome: Contatto}

    # ---------------------------------------------------------------
    # CRUD: Create, Read, Update, Delete
    # ---------------------------------------------------------------

    def aggiungi(self, contatto):
        """
        Aggiunge un contatto alla rubrica.
        Se il nome esiste già, solleva un'eccezione.

        Args:
            contatto: istanza di Contatto

        Raises:
            TypeError: se l'argomento non è un Contatto
            ValueError: se il nome è già presente
        """
        if not isinstance(contatto, Contatto):
            raise TypeError("Atteso un oggetto Contatto.")
        if contatto.nome in self._contatti:
            raise ValueError(f"Il contatto '{contatto.nome}' esiste già.")
        self._contatti[contatto.nome] = contatto

    def ottieni(self, nome):
        """
        Restituisce il contatto con il nome dato, o None.

        Equivalente a dict.get(): non solleva eccezioni se il nome non esiste.
        """
        return self._contatti.get(nome)

    def aggiorna_citta(self, nome, nuova_citta):
        """Aggiorna la città di un contatto esistente."""
        contatto = self._get_o_errore(nome)
        contatto.citta = nuova_citta

    def aggiorna_gruppo(self, nome, nuovo_gruppo):
        """Aggiorna il gruppo di un contatto esistente."""
        contatto = self._get_o_errore(nome)
        contatto.gruppo = nuovo_gruppo

    def aggiungi_telefono(self, nome, numero):
        """Aggiunge un telefono a un contatto esistente."""
        contatto = self._get_o_errore(nome)
        contatto.aggiungi_telefono(numero)

    def rimuovi_telefono(self, nome, numero):
        """Rimuove un telefono da un contatto esistente."""
        contatto = self._get_o_errore(nome)
        contatto.rimuovi_telefono(numero)

    def elimina(self, nome):
        """
        Elimina un contatto dalla rubrica.

        Raises:
            KeyError: se il contatto non esiste
        """
        if nome not in self._contatti:
            raise KeyError(f"Contatto '{nome}' non trovato.")
        del self._contatti[nome]

    # ---------------------------------------------------------------
    # RICERCA E FILTRI
    # ---------------------------------------------------------------

    def cerca(self, testo):
        """
        Cerca contatti il cui nome contiene 'testo' (case-insensitive).
        Restituisce una LISTA di oggetti Contatto.
        """
        testo_lower = testo.lower()
        return [c for c in self._contatti.values() if testo_lower in c.nome.lower()]

    def cerca_numero(self, numero):
        
        #
        # Costruzione lista in modo esplicito
        #
        #lista_contatti_trovati = []
        #
        #for contatto in self:
        #    if numero in contatto.telefoni:
        #        lista_contatti_trovati.append(contatto)
        #
        #return lista_contatti_trovati

        #
        # Costruzione lista con list comprehension
        #
        return [c for c in self if numero in c.telefoni]

    def filtra_per_gruppo(self, gruppo):
        """Restituisce i contatti appartenenti a un dato gruppo."""
        return [c for c in self._contatti.values() if c.gruppo == gruppo]

    def statistiche(self):
        """
        Restituisce un dizionario con le statistiche della rubrica.

        Nota: usa len(self) e itera con for c in self — cioè usa
        i protocolli __len__ e __iter__ definiti sotto.
        """
        if len(self) == 0:
            return {"errore": "Rubrica vuota"}

        totale_tel = 0
        max_tel = 0
        contatto_max = ""
        gruppi = {}

        for contatto in self:  # Usa __iter__!
            n = len(contatto.telefoni)
            totale_tel += n
            if n > max_tel:
                max_tel = n
                contatto_max = contatto.nome
            g = contatto.gruppo
            gruppi[g] = gruppi.get(g, 0) + 1

        return {
            "totale_contatti": len(self),
            "totale_telefoni": totale_tel,
            "media_telefoni": round(totale_tel / len(self), 2),
            "contatto_con_piu_numeri": contatto_max,
            "max_numeri": max_tel,
            "distribuzione_gruppi": gruppi,
        }

    # ---------------------------------------------------------------
    # METODO PRIVATO (helper)
    # ---------------------------------------------------------------

    def _get_o_errore(self, nome):
        """Restituisce il contatto o solleva KeyError."""
        contatto = self._contatti.get(nome)
        if contatto is None:
            raise KeyError(f"Contatto '{nome}' non trovato.")
        return contatto

    # ---------------------------------------------------------------
    # PROTOCOLLI PYTHON — rendere Rubrica una "collezione"
    # ---------------------------------------------------------------

    def __len__(self):
        """
        Protocollo "Sized": permette di usare len(rubrica).

        >>> r = Rubrica()
        >>> len(r)
        0
        """
        return len(self._contatti)

    def __contains__(self, nome):
        """
        Protocollo "Container": permette di usare 'in'.

        >>> "Mario Rossi" in rubrica
        True

        Python chiama questo metodo automaticamente quando scrivete:
            if "Mario" in rubrica: ...
        """
        return nome in self._contatti

    def __getitem__(self, nome):
        """
        Protocollo "Subscriptable": permette l'accesso con [].

        >>> contatto = rubrica["Mario Rossi"]

        Solleva KeyError se il nome non esiste (come un dict normale).
        """
        if nome not in self._contatti:
            raise KeyError(f"Contatto '{nome}' non trovato.")
        return self._contatti[nome]

    def __iter__(self):
        """
        Protocollo "Iterable": permette di usare for...in.

        >>> for contatto in rubrica:
        ...     print(contatto.nome)

        PATTERN ITERATORE:
        Questo è uno dei design pattern più importanti in informatica.
        L'idea: chi usa la collezione non ha bisogno di sapere COME
        i dati sono organizzati internamente (dict? lista? database?).
        Sa solo che può iterare con for.

        yield produce un elemento alla volta (lazy evaluation):
        non crea una lista completa in memoria, ma genera ogni
        contatto al momento in cui serve. Per una rubrica piccola
        non fa differenza, ma per milioni di record è fondamentale.

        I contatti vengono restituiti in ordine alfabetico per nome.
        """
        for nome in sorted(self._contatti.keys()):
            yield self._contatti[nome]

    def __str__(self):
        """Rappresentazione leggibile dell'intera rubrica."""
        if len(self) == 0:
            return "La rubrica è vuota."
        linee = [f"--- RUBRICA ({len(self)} contatti) ---\n"]
        for contatto in self:  # Usa __iter__
            linee.append(str(contatto))  # Usa Contatto.__str__
            linee.append("")
        return "\n".join(linee)

    # ---------------------------------------------------------------
    # SERIALIZZAZIONE
    # ---------------------------------------------------------------

    def to_dict(self):
        """Converte l'intera rubrica in un dizionario serializzabile."""
        return {c.nome: c.to_dict() for c in self}

    @classmethod
    def from_dict(cls, dati):
        """
        Factory method: crea una Rubrica da un dizionario.

        Args:
            dati: dizionario {nome: {telefoni: [...], ...}}
        """
        rubrica = cls()
        for nome, info in dati.items():
            contatto = Contatto.from_dict(nome, info)
            rubrica.aggiungi(contatto)
        return rubrica


# ===================================================================
# TEST STANDALONE — esegui con: python -m modelli.rubrica
# ===================================================================
if __name__ == "__main__":
    r = Rubrica()

    # Creazione contatti
    r.aggiungi(
        Contatto("Mario Rossi", "06-1234567", "mario@email.it", "Roma", "lavoro")
    )
    r.aggiungi(Contatto("Anna Verdi", "02-9876543", "anna@email.it", "Milano", "amici"))
    r.aggiungi(
        Contatto("Luca Bianchi", "081-5551234", "luca@studio.it", "Napoli", "lavoro")
    )

    # Aggiungiamo numeri extra
    r.aggiungi_telefono("Mario Rossi", "333-1112233")
    r.aggiungi_telefono("Luca Bianchi", "347-9998877")

    # --- Protocollo Sized ---
    print(f"len(rubrica) = {len(r)}")

    # --- Protocollo Container ---
    print(f"'Mario Rossi' in rubrica = {'Mario Rossi' in r}")
    print(f"'Nessuno' in rubrica = {'Nessuno' in r}")

    # --- Protocollo Subscriptable ---
    print(f"\nrubrica['Anna Verdi']:")
    print(r["Anna Verdi"])

    # --- Protocollo Iterable (PATTERN ITERATORE) ---
    print("\n--- Iterazione con for ---")
    for contatto in r:
        print(f"  {contatto.nome} — {contatto.citta} — {len(contatto.telefoni)} tel")

    # --- Ricerca ---
    print("\n--- Cerca 'Rossi' ---")
    for c in r.cerca("ROSSI"):
        print(f"  Trovato: {c.nome}")

    # --- Statistiche ---
    print(f"\n--- Statistiche ---")
    stats = r.statistiche()
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # --- Serializzazione ---
    print(f"\n--- to_dict ---")
    d = r.to_dict()
    print(f"Chiavi: {list(d.keys())}")
    print(f"Valori: {list(d.values())}")

    r2 = Rubrica.from_dict(d)
    print(f"\nRicostruita da dict: {len(r2)} contatti")
    print(r2)

    r2.elimina("Luca Bianchi")
    print()
    print(r)
    print()
    print(r2)
