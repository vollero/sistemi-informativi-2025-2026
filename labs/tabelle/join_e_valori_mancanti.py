"""
Sistemi Informativi — Lezione: Join, valori mancanti e coerenza tra tabelle
Running example: Contatti, gruppi e appartenenze

Questo script estende il laboratorio sulla logica tabellare e mostra:
- come rimappare in Python le principali forme di join
- come distinguere campi vuoti e valori mancanti
- come ragionare sulla coerenza nelle operazioni CRUD tra tabelle collegate
"""


contatti = [
    {"id": 1, "nome": "Mario", "cognome": "Rossi", "telefono": "06-1234567"},
    {"id": 2, "nome": "Luca", "cognome": "Bianchi", "telefono": "02-9876543"},
    {"id": 3, "nome": "Anna", "cognome": "Verdi", "telefono": ""},
    {"id": 4, "nome": "Giulia", "cognome": "Neri", "telefono": "06-7654321"},
    {"id": 5, "nome": "Paolo", "cognome": "Serra", "telefono": None},
]

gruppi = [
    {"id_gruppo": 10, "nome_gruppo": "Lavoro"},
    {"id_gruppo": 20, "nome_gruppo": "Famiglia"},
    {"id_gruppo": 30, "nome_gruppo": "Universita"},
    {"id_gruppo": 40, "nome_gruppo": "Sport"},
]

appartenenza = [
    {"id_contatto": 1, "id_gruppo": 10},
    {"id_contatto": 1, "id_gruppo": 20},
    {"id_contatto": 2, "id_gruppo": 30},
    {"id_contatto": 4, "id_gruppo": 10},
    {"id_contatto": 6, "id_gruppo": 40},
]


def stampa_tabella(righe, colonne=None):
    """Stampa una lista di dizionari in formato tabellare."""
    if not righe:
        print("(tabella vuota)")
        return

    if colonne is None:
        colonne = list(righe[0].keys())

    larghezze = {}
    for colonna in colonne:
        valori = [formatta_valore(riga.get(colonna)) for riga in righe]
        larghezze[colonna] = max(len(colonna), max(len(valore) for valore in valori))

    intestazione = " | ".join(colonna.ljust(larghezze[colonna]) for colonna in colonne)
    separatore = "-+-".join("-" * larghezze[colonna] for colonna in colonne)
    print(intestazione)
    print(separatore)

    for riga in righe:
        linea = " | ".join(
            formatta_valore(riga.get(colonna)).ljust(larghezze[colonna])
            for colonna in colonne
        )
        print(linea)
    print()


def formatta_valore(valore):
    """Rende visibile la differenza tra stringa vuota e valore mancante."""
    if valore is None:
        return "None"
    if valore == "":
        return '""'
    return str(valore)


def unisci_righe(riga_sx, riga_dx, colonne_sx, colonne_dx):
    """Fonde due righe mantenendo esplicite le colonne attese."""
    riga = {}
    for colonna in colonne_sx:
        riga[colonna] = riga_sx.get(colonna) if riga_sx is not None else None
    for colonna in colonne_dx:
        riga[colonna] = riga_dx.get(colonna) if riga_dx is not None else None
    return riga


def inner_join(tabella_sx, tabella_dx, chiave_sx, chiave_dx):
    """Restituisce solo le righe che trovano corrispondenza in entrambe le tabelle."""
    risultato = []
    colonne_sx = list(tabella_sx[0].keys())
    colonne_dx = list(tabella_dx[0].keys())

    for riga_sx in tabella_sx:
        for riga_dx in tabella_dx:
            if riga_sx[chiave_sx] == riga_dx[chiave_dx]:
                risultato.append(unisci_righe(riga_sx, riga_dx, colonne_sx, colonne_dx))
    return risultato


def left_join(tabella_sx, tabella_dx, chiave_sx, chiave_dx):
    """Conserva tutte le righe della tabella di sinistra."""
    risultato = []
    colonne_sx = list(tabella_sx[0].keys())
    colonne_dx = list(tabella_dx[0].keys())

    for riga_sx in tabella_sx:
        trovata_corrispondenza = False
        for riga_dx in tabella_dx:
            if riga_sx[chiave_sx] == riga_dx[chiave_dx]:
                risultato.append(unisci_righe(riga_sx, riga_dx, colonne_sx, colonne_dx))
                trovata_corrispondenza = True
        if not trovata_corrispondenza:
            risultato.append(unisci_righe(riga_sx, None, colonne_sx, colonne_dx))
    return risultato


def right_join(tabella_sx, tabella_dx, chiave_sx, chiave_dx):
    """Conserva tutte le righe della tabella di destra."""
    return left_join(tabella_dx, tabella_sx, chiave_dx, chiave_sx)


def full_outer_join(tabella_sx, tabella_dx, chiave_sx, chiave_dx):
    """Conserva tutte le righe di entrambe le tabelle."""
    risultato = []
    colonne_sx = list(tabella_sx[0].keys())
    colonne_dx = list(tabella_dx[0].keys())
    indici_dx_usati = set()

    for riga_sx in tabella_sx:
        trovata_corrispondenza = False
        for indice_dx, riga_dx in enumerate(tabella_dx):
            if riga_sx[chiave_sx] == riga_dx[chiave_dx]:
                risultato.append(unisci_righe(riga_sx, riga_dx, colonne_sx, colonne_dx))
                trovata_corrispondenza = True
                indici_dx_usati.add(indice_dx)
        if not trovata_corrispondenza:
            risultato.append(unisci_righe(riga_sx, None, colonne_sx, colonne_dx))

    for indice_dx, riga_dx in enumerate(tabella_dx):
        if indice_dx not in indici_dx_usati:
            risultato.append(unisci_righe(None, riga_dx, colonne_sx, colonne_dx))

    return risultato


def proiezione(tabella, colonne):
    """Mantiene solo le colonne indicate."""
    risultato = []
    for riga in tabella:
        risultato.append({colonna: riga.get(colonna) for colonna in colonne})
    return risultato


def esiste(tabella, chiave, valore):
    """Controlla se esiste almeno una riga con chiave = valore."""
    for riga in tabella:
        if riga[chiave] == valore:
            return True
    return False


def ha_duplicati(tabella, colonne):
    """Controlla se esistono righe duplicate rispetto a un insieme di colonne."""
    valori_visti = set()
    for riga in tabella:
        chiave = tuple(riga[colonna] for colonna in colonne)
        if chiave in valori_visti:
            return True
        valori_visti.add(chiave)
    return False


def verifica_integrita_referenziale():
    """Mostra quali righe della tabella di collegamento non trovano riferimenti validi."""
    righe_non_valide = []
    for riga in appartenenza:
        contatto_valido = esiste(contatti, "id", riga["id_contatto"])
        gruppo_valido = esiste(gruppi, "id_gruppo", riga["id_gruppo"])
        if not contatto_valido or not gruppo_valido:
            righe_non_valide.append(
                {
                    "id_contatto": riga["id_contatto"],
                    "id_gruppo": riga["id_gruppo"],
                    "contatto_valido": contatto_valido,
                    "gruppo_valido": gruppo_valido,
                }
            )
    return righe_non_valide


def inserisci_appartenenza(id_contatto, id_gruppo):
    """Simula una CREATE su una tabella collegata con controlli di coerenza."""
    print(f"Tentativo INSERT appartenenza ({id_contatto}, {id_gruppo})")

    if not esiste(contatti, "id", id_contatto):
        print("  BLOCCATO: il contatto non esiste.")
        return
    if not esiste(gruppi, "id_gruppo", id_gruppo):
        print("  BLOCCATO: il gruppo non esiste.")
        return
    if esiste(appartenenza, "id_contatto", id_contatto):
        for riga in appartenenza:
            if riga["id_contatto"] == id_contatto and riga["id_gruppo"] == id_gruppo:
                print("  BLOCCATO: l'associazione e' gia' presente.")
                return

    appartenenza.append({"id_contatto": id_contatto, "id_gruppo": id_gruppo})
    print("  OK: associazione inserita.")


def aggiorna_id_contatto(id_vecchio, id_nuovo):
    """Simula una UPDATE su una chiave usata da altre tabelle."""
    print(f"Tentativo UPDATE contatti.id da {id_vecchio} a {id_nuovo}")

    if not esiste(contatti, "id", id_vecchio):
        print("  BLOCCATO: il contatto sorgente non esiste.")
        return
    if esiste(contatti, "id", id_nuovo):
        print("  BLOCCATO: il nuovo id e' gia' occupato.")
        return

    riferimenti_presenti = esiste(appartenenza, "id_contatto", id_vecchio)
    if riferimenti_presenti:
        print("  BLOCCATO: esistono righe collegate in appartenenza.")
        print("  MOTIVO: cambiare la chiave romperebbe i riferimenti.")
        return

    for contatto in contatti:
        if contatto["id"] == id_vecchio:
            contatto["id"] = id_nuovo
            print("  OK: id aggiornato.")
            return


def cancella_contatto(id_contatto):
    """Simula una DELETE con vincolo referenziale."""
    print(f"Tentativo DELETE contatto {id_contatto}")

    if esiste(appartenenza, "id_contatto", id_contatto):
        print("  BLOCCATO: il contatto e' ancora referenziato in appartenenza.")
        return

    for indice, contatto in enumerate(contatti):
        if contatto["id"] == id_contatto:
            del contatti[indice]
            print("  OK: contatto cancellato.")
            return

    print("  BLOCCATO: il contatto non esiste.")


def stampa_join_finale():
    """Mostra il join finale contatti -> appartenenza -> gruppi."""
    step1 = left_join(contatti, appartenenza, "id", "id_contatto")
    step2 = left_join(step1, gruppi, "id_gruppo", "id_gruppo")
    stampa_tabella(
        proiezione(step2, ["nome", "cognome", "telefono", "nome_gruppo"]),
        ["nome", "cognome", "telefono", "nome_gruppo"],
    )


print("=== CONTATTI ===")
stampa_tabella(contatti, ["id", "nome", "cognome", "telefono"])

print("=== APPARTENENZA ===")
stampa_tabella(appartenenza, ["id_contatto", "id_gruppo"])

print("=== GRUPPI ===")
stampa_tabella(gruppi, ["id_gruppo", "nome_gruppo"])

print("=== INNER JOIN contatti JOIN appartenenza ===")
stampa_tabella(
    inner_join(contatti, appartenenza, "id", "id_contatto"),
    ["id", "nome", "cognome", "telefono", "id_contatto", "id_gruppo"],
)

print("=== LEFT JOIN contatti LEFT JOIN appartenenza ===")
stampa_tabella(
    left_join(contatti, appartenenza, "id", "id_contatto"),
    ["id", "nome", "cognome", "telefono", "id_contatto", "id_gruppo"],
)

print("=== RIGHT JOIN contatti RIGHT JOIN appartenenza ===")
stampa_tabella(
    right_join(contatti, appartenenza, "id", "id_contatto"),
    ["id_contatto", "id_gruppo", "id", "nome", "cognome", "telefono"],
)

print("=== FULL OUTER JOIN contatti FULL OUTER JOIN appartenenza ===")
stampa_tabella(
    full_outer_join(contatti, appartenenza, "id", "id_contatto"),
    ["id", "nome", "cognome", "telefono", "id_contatto", "id_gruppo"],
)

print("=== LEFT JOIN finale con gruppi ===")
stampa_join_finale()

print("=== RIGHE CHE VIOLANO L'INTEGRITA' REFERENZIALE ===")
stampa_tabella(
    verifica_integrita_referenziale(),
    ["id_contatto", "id_gruppo", "contatto_valido", "gruppo_valido"],
)

print("=== TENTATIVI CRUD SU TABELLE COLLEGATE ===")
inserisci_appartenenza(3, 20)
inserisci_appartenenza(6, 10)
inserisci_appartenenza(1, 10)
aggiorna_id_contatto(1, 100)
cancella_contatto(2)
cancella_contatto(5)

print("=== STATO FINALE DELLE TABELLE ===")
print("Contatti")
stampa_tabella(contatti, ["id", "nome", "cognome", "telefono"])
print("Appartenenza")
stampa_tabella(appartenenza, ["id_contatto", "id_gruppo"])

print("=== JOIN FINALE DOPO LE OPERAZIONI ===")
stampa_join_finale()

print("=== OSSERVAZIONI DIDATTICHE ===")
print('1. telefono = "" indica campo noto ma non compilato.')
print("2. telefono = None indica valore assente o non disponibile.")
print("3. nome_gruppo = None indica che il join non ha trovato una corrispondenza.")
print("4. INSERT, UPDATE e DELETE su tabelle collegate richiedono controlli di coerenza.")
