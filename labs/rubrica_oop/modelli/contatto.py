"""
modelli/contatto.py — La classe Contatto

PERCORSO DIDATTICO:
    Nella Lezione 3, un contatto era un dizionario "nudo":
        {"telefoni": [...], "email": [...], "citta": "Roma", "gruppo": "lavoro"}

    Problemi di questo approccio:
    1. Nessuna protezione: chiunque può scrivere rubrica["Mario"]["telefoni"] = "non una lista"
    2. La validazione è FUORI dal dato: formato_telefono_valido() è una funzione separata
    3. La struttura non è garantita: nulla impedisce di creare un contatto senza "telefoni"

    Soluzione: una CLASSE che incapsula dati + comportamento.
"""


class Contatto:
    """
    Rappresenta un contatto della rubrica.

    Information hiding:
        - Gli attributi con prefisso _ sono "privati per convenzione"
        - L'accesso esterno avviene tramite PROPERTY (interfaccia controllata)
        - La validazione è DENTRO l'oggetto, non fuori
    """

    # ---------------------------------------------------------------
    # COSTRUTTORE: inizializza lo stato interno
    # ---------------------------------------------------------------
    def __init__(self, nome, telefono, email="", citta="", gruppo="generale"):
        """
        Crea un nuovo contatto.

        Args:
            nome: nome completo (obbligatorio)
            telefono: primo numero di telefono (obbligatorio, viene validato)
            email: indirizzo email (opzionale)
            citta: città di residenza (opzionale)
            gruppo: gruppo di appartenenza (default: "generale")

        Raises:
            ValueError: se il telefono non è valido
        """
        # Attributi "privati" (convenzione Python: prefisso _)
        # Non si accede direttamente dall'esterno: si usano le property
        self._nome = nome
        self._telefoni = []
        self._email = []
        self._citta = citta
        self._gruppo = gruppo

        # Il primo telefono passa dalla validazione
        self.aggiungi_telefono(telefono)

        # Email opzionale
        if email:
            self.aggiungi_email(email)

    # ---------------------------------------------------------------
    # PROPERTY: interfaccia di lettura controllata
    # ---------------------------------------------------------------
    # Le property permettono di leggere gli attributi senza modificarli
    # direttamente. È il meccanismo Python per l'information hiding.

    @property
    def nome(self):
        """Il nome del contatto (sola lettura)."""
        return self._nome

    @property
    def telefoni(self):
        """
        Lista dei telefoni (restituisce una COPIA).

        Perché una copia? Se restituissimo il riferimento alla lista interna,
        il chiamante potrebbe modificarla direttamente, bypassando la validazione.

            contatto.telefoni.append("DATO_NON_VALIDO")  # Questo NON funziona con la copia

        Per aggiungere un telefono si DEVE usare aggiungi_telefono(), che valida.
        """
        return list(self._telefoni)  # copia difensiva

    @property
    def email(self):
        """Lista delle email (copia difensiva)."""
        return list(self._email)

    @property
    def citta(self):
        return self._citta

    @citta.setter
    def citta(self, nuova_citta):
        """La città è modificabile direttamente (non richiede validazione complessa)."""
        self._citta = nuova_citta

    @property
    def gruppo(self):
        return self._gruppo

    @gruppo.setter
    def gruppo(self, nuovo_gruppo):
        gruppi_validi = ["generale", "lavoro", "amici", "famiglia"]
        if nuovo_gruppo not in gruppi_validi:
            raise ValueError(f"Gruppo '{nuovo_gruppo}' non valido. Ammessi: {gruppi_validi}")
        self._gruppo = nuovo_gruppo

    # ---------------------------------------------------------------
    # METODI PUBBLICI: le operazioni consentite sul contatto
    # ---------------------------------------------------------------

    def aggiungi_telefono(self, numero):
        """
        Aggiunge un numero di telefono con validazione.

        Args:
            numero: stringa del numero di telefono

        Raises:
            ValueError: se il numero non è valido o è già presente
        """
        if not self._valida_telefono(numero):
            raise ValueError(f"'{numero}' non è un numero di telefono valido (min 6 cifre).")
        if numero in self._telefoni:
            raise ValueError(f"Il numero '{numero}' è già presente.")
        self._telefoni.append(numero)

    def rimuovi_telefono(self, numero):
        """
        Rimuove un numero di telefono.

        Raises:
            ValueError: se il numero non esiste o è l'ultimo (vincolo di integrità)
        """
        if numero not in self._telefoni:
            raise ValueError(f"Il numero '{numero}' non è presente.")
        if len(self._telefoni) == 1:
            raise ValueError("Impossibile rimuovere l'ultimo numero di telefono.")
        self._telefoni.remove(numero)

    def aggiungi_email(self, indirizzo):
        """Aggiunge un'email (validazione base: deve contenere @)."""
        if "@" not in indirizzo:
            raise ValueError(f"'{indirizzo}' non è un indirizzo email valido.")
        if indirizzo in self._email:
            raise ValueError(f"L'email '{indirizzo}' è già presente.")
        self._email.append(indirizzo)

    # ---------------------------------------------------------------
    # METODI PRIVATI: logica interna (non parte dell'interfaccia)
    # ---------------------------------------------------------------

    def _valida_telefono(self, numero):
        """
        Verifica che il numero contenga almeno 6 cifre.

        Il prefisso _ indica che questo metodo è "privato":
        è un dettaglio implementativo, non parte dell'interfaccia pubblica.
        Il chiamante esterno usa aggiungi_telefono(), non _valida_telefono().
        """
        solo_cifre = numero.replace("-", "").replace(" ", "").replace("+", "")
        if len(solo_cifre) < 6:
            return False
        return solo_cifre.isdigit()

    # ---------------------------------------------------------------
    # METODI SPECIALI (dunder methods): l'interfaccia Python
    # ---------------------------------------------------------------

    def __str__(self):
        """
        Rappresentazione leggibile per l'utente finale (print).

        Questo metodo viene chiamato automaticamente da:
            print(contatto)
            str(contatto)
            f"{contatto}"
        """
        linee = [f"=== {self._nome} ==="]
        linee.append(f"  Gruppo: {self._gruppo}")
        linee.append(f"  Città: {self._citta if self._citta else 'N/D'}")
        linee.append("  Telefoni:")
        for i, tel in enumerate(self._telefoni):
            linee.append(f"    [{i + 1}] {tel}")
        linee.append("  Email:")
        if not self._email:
            linee.append("    (nessuna)")
        else:
            for i, em in enumerate(self._email):
                linee.append(f"    [{i + 1}] {em}")
        return "\n".join(linee)

    def __repr__(self):
        """
        Rappresentazione tecnica per il programmatore (debug, REPL Python).

        Convenzione: dovrebbe produrre una stringa che ricrea l'oggetto.
        Viene usata nella console >>> e nei log.
        """
        return f"Contatto('{self._nome}', '{self._telefoni[0]}')"

    # ---------------------------------------------------------------
    # SERIALIZZAZIONE: convertire da/a dizionario (per JSON)
    # ---------------------------------------------------------------

    def to_dict(self):
        """
        Converte il contatto in un dizionario serializzabile in JSON.

        Nota: questo metodo NON salva su file. Produce solo il dizionario.
        La responsabilità del salvataggio è di un'altra classe (JsonStore).
        Questa separazione si chiama "Separation of Concerns".
        """
        return {
            "telefoni": list(self._telefoni),
            "email": list(self._email),
            "citta": self._citta,
            "gruppo": self._gruppo
        }

    @classmethod
    def from_dict(cls, nome, dati):
        """
        Crea un Contatto a partire da un dizionario (caricato da JSON).

        @classmethod: è un metodo della CLASSE, non dell'istanza.
        Si chiama con Contatto.from_dict(...), non con contatto.from_dict(...).
        È un pattern chiamato "factory method".

        Args:
            nome: il nome del contatto (era la chiave del dizionario)
            dati: il dizionario con i campi del contatto
        """
        # Prende il primo telefono per il costruttore
        primo_telefono = dati["telefoni"][0]
        contatto = cls(
            nome=nome,
            telefono=primo_telefono,
            citta=dati.get("citta", ""),
            gruppo=dati.get("gruppo", "generale")
        )
        # Aggiunge gli altri telefoni
        for tel in dati["telefoni"][1:]:
            contatto.aggiungi_telefono(tel)
        # Aggiunge le email
        for em in dati.get("email", []):
            contatto.aggiungi_email(em)
        return contatto


# ===================================================================
# TEST STANDALONE — esegui con: python -m modelli.contatto
# ===================================================================
if __name__ == "__main__":
    print("--- Creazione contatto ---")
    c = Contatto("Mario Rossi", "06-1234567", "mario@email.it", "Roma", "lavoro")
    print(c)

    print("\n--- Aggiunta secondo telefono ---")
    c.aggiungi_telefono("333-1112233")
    print(c)

    print("\n--- Information hiding: tentativo di accesso diretto ---")
    # c._telefoni.append("DATO_NON_VALIDO")  # Funziona ma VIOLA la convenzione
    # c.telefoni.append("DATO_NON_VALIDO")   # NON modifica l'originale (copia!)
    copia = c.telefoni
    copia.append("IGNORATO")
    print(f"Telefoni interni: {c.telefoni}")   # Non contiene "IGNORATO"
    print(f"Copia esterna:    {copia}")         # Contiene "IGNORATO"

    print("\n--- Validazione integrata ---")
    try:
        c.aggiungi_telefono("123")  # Troppo corto
    except ValueError as e:
        print(f"Errore catturato: {e}")

    try:
        c.gruppo = "invalido"
    except ValueError as e:
        print(f"Errore catturato: {e}")

    print("\n--- Serializzazione ---")
    d = c.to_dict()
    print(f"to_dict(): {d}")

    c2 = Contatto.from_dict("Mario Rossi", d)
    print(f"\nfrom_dict(): {c2}")
    print(f"repr(): {repr(c2)}")
