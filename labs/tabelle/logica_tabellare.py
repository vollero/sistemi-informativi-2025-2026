"""
Sistemi Informativi — Lezione: Rappresentazione e Logica Tabellare
Running example: La Rubrica Telefonica

Questo script è pensato per essere eseguito cella per cella in Google Colab
o come script Python standalone.
"""

# ============================================================
# SEZIONE 1: Dati — la rubrica come lista di dizionari
# ============================================================

rubrica = [
    {"id": 1, "nome": "Mario",  "cognome": "Rossi",   "telefono": "06-1234567"},
    {"id": 2, "nome": "Luca",   "cognome": "Bianchi", "telefono": "02-9876543"},
    {"id": 3, "nome": "Anna",   "cognome": "Verdi",   "telefono": "081-5551234"},
    {"id": 4, "nome": "Mario",  "cognome": "Neri",    "telefono": "06-7654321"},
]

gruppi = [
    {"id_gruppo": 10, "nome_gruppo": "Lavoro"},
    {"id_gruppo": 20, "nome_gruppo": "Famiglia"},
    {"id_gruppo": 30, "nome_gruppo": "Università"},
]

appartenenza = [
    {"id_contatto": 1, "id_gruppo": 10},
    {"id_contatto": 1, "id_gruppo": 20},
    {"id_contatto": 2, "id_gruppo": 30},
    {"id_contatto": 3, "id_gruppo": 20},
    {"id_contatto": 4, "id_gruppo": 10},
]


# ============================================================
# SEZIONE 2: Funzione di stampa tabellare
# ============================================================

def stampa_tabella(righe, colonne=None):
    """Stampa una lista di dizionari in formato tabellare.

    Se colonne non è specificato, usa le chiavi della prima riga.
    """
    if not righe:
        print("(tabella vuota)")
        return
    if colonne is None:
        colonne = list(righe[0].keys())

    # Calcola la larghezza di ogni colonna
    larghezze = {}
    for col in colonne:
        valori = [str(r.get(col, "")) for r in righe]
        larghezze[col] = max(len(col), max(len(v) for v in valori))

    # Intestazione
    header = " | ".join(col.ljust(larghezze[col]) for col in colonne)
    separatore = "-+-".join("-" * larghezze[col] for col in colonne)
    print(header)
    print(separatore)

    # Righe
    for riga in righe:
        linea = " | ".join(str(riga.get(col, "")).ljust(larghezze[col]) for col in colonne)
        print(linea)
    print()


print("=== RUBRICA COMPLETA ===")
stampa_tabella(rubrica)


# ============================================================
# SEZIONE 3: Selezione (σ) — filtro per righe
# ============================================================

def selezione(tabella, condizione):
    """Restituisce le righe che soddisfano la funzione condizione.

    Parametri:
        tabella: lista di dizionari
        condizione: funzione che prende un dizionario e restituisce True/False
    """
    risultato = []
    for riga in tabella:
        if condizione(riga):
            risultato.append(riga)
    return risultato


# Esempio: contatti con prefisso romano (06)
contatti_roma = selezione(rubrica, lambda c: c["telefono"].startswith("06"))
print("=== σ(telefono LIKE '06%') rubrica ===")
stampa_tabella(contatti_roma)

# Esempio: contatti di nome Mario
mario = selezione(rubrica, lambda c: c["nome"] == "Mario")
print("=== σ(nome = 'Mario') rubrica ===")
stampa_tabella(mario)


# ============================================================
# SEZIONE 4: Proiezione (π) — filtro per colonne
# ============================================================

def proiezione(tabella, colonne):
    """Restituisce una nuova tabella con solo le colonne specificate.

    Parametri:
        tabella: lista di dizionari
        colonne: lista di stringhe (nomi delle colonne da mantenere)
    """
    risultato = []
    for riga in tabella:
        nuova_riga = {}
        for col in colonne:
            nuova_riga[col] = riga[col]
        risultato.append(nuova_riga)
    return risultato


# Esempio: solo nome e telefono
nome_tel = proiezione(rubrica, ["nome", "telefono"])
print("=== π(nome, telefono) rubrica ===")
stampa_tabella(nome_tel)


# ============================================================
# SEZIONE 5: Composizione σ + π
# ============================================================

# "Nome e telefono dei contatti romani"
# Prima selezione, poi proiezione
romani = selezione(rubrica, lambda c: c["telefono"].startswith("06"))
risultato = proiezione(romani, ["nome", "telefono"])
print("=== π(nome, telefono) σ(telefono LIKE '06%') rubrica ===")
stampa_tabella(risultato)


# ============================================================
# SEZIONE 6: Ordinamento
# ============================================================

def ordinamento(tabella, chiave, inverso=False):
    """Restituisce una copia della tabella ordinata per la colonna 'chiave'.

    Parametri:
        tabella: lista di dizionari
        chiave: nome della colonna per cui ordinare
        inverso: se True, ordine decrescente
    """
    return sorted(tabella, key=lambda riga: riga[chiave], reverse=inverso)


rubrica_per_cognome = ordinamento(rubrica, "cognome")
print("=== rubrica ORDER BY cognome ===")
stampa_tabella(rubrica_per_cognome)


# ============================================================
# SEZIONE 7: Join — congiunzione tra tabelle
# ============================================================

def join(tabella_sx, tabella_dx, chiave_sx, chiave_dx):
    """Join tra due tabelle (nested loop join).

    Per ogni riga di tabella_sx, cerca le righe in tabella_dx
    dove chiave_sx == chiave_dx e le fonde in un unico dizionario.
    """
    risultato = []
    for riga_s in tabella_sx:
        for riga_d in tabella_dx:
            if riga_s[chiave_sx] == riga_d[chiave_dx]:
                riga_fusa = {}
                riga_fusa.update(riga_s)
                riga_fusa.update(riga_d)
                risultato.append(riga_fusa)
    return risultato


# Step 1: rubrica ⋈ appartenenza (su id = id_contatto)
step1 = join(rubrica, appartenenza, "id", "id_contatto")

# Step 2: risultato ⋈ gruppi (su id_gruppo = id_gruppo)
step2 = join(step1, gruppi, "id_gruppo", "id_gruppo")

# Proiezione finale: nome, cognome, nome_gruppo
risultato_join = proiezione(step2, ["nome", "cognome", "nome_gruppo"])
print("=== rubrica ⋈ appartenenza ⋈ gruppi → π(nome, cognome, nome_gruppo) ===")
stampa_tabella(risultato_join)


# ============================================================
# SEZIONE 8: Vincoli di integrità
# ============================================================

def verifica_pk(tabella, colonna_pk):
    """Verifica che non ci siano valori duplicati nella colonna PK."""
    valori_visti = []
    for riga in tabella:
        valore = riga[colonna_pk]
        if valore in valori_visti:
            print(f"  ERRORE: valore duplicato PK = {valore}")
            return False
        valori_visti.append(valore)
    print(f"  OK: chiave primaria '{colonna_pk}' rispettata.")
    return True


def verifica_fk(tabella_figlia, colonna_fk, tabella_padre, colonna_pk):
    """Verifica che ogni valore FK esista nella tabella padre."""
    valori_padre = []
    for riga in tabella_padre:
        valori_padre.append(riga[colonna_pk])

    for riga in tabella_figlia:
        valore = riga[colonna_fk]
        if valore not in valori_padre:
            print(f"  ERRORE: FK violata — {colonna_fk}={valore} non esiste in {colonna_pk}")
            return False
    print(f"  OK: vincolo FK '{colonna_fk}' → '{colonna_pk}' rispettato.")
    return True


def verifica_not_null(tabella, colonne_obbligatorie):
    """Verifica che le colonne indicate non contengano valori None o stringa vuota."""
    for i, riga in enumerate(tabella):
        for col in colonne_obbligatorie:
            valore = riga.get(col)
            if valore is None or valore == "":
                print(f"  ERRORE: riga {i} ha {col} = {repr(valore)}")
                return False
    print(f"  OK: NOT NULL rispettato per {colonne_obbligatorie}.")
    return True


print("=== VERIFICA VINCOLI DI INTEGRITÀ ===")
verifica_pk(rubrica, "id")
verifica_pk(gruppi, "id_gruppo")
verifica_fk(appartenenza, "id_contatto", rubrica, "id")
verifica_fk(appartenenza, "id_gruppo", gruppi, "id_gruppo")
verifica_not_null(rubrica, ["nome", "cognome", "telefono"])


# ============================================================
# SEZIONE 9: Violazione di vincolo (dimostrazione)
# ============================================================

print("\n=== TENTATIVO DI INSERIMENTO CON FK INVALIDA ===")
appartenenza_con_errore = appartenenza + [{"id_contatto": 99, "id_gruppo": 10}]
verifica_fk(appartenenza_con_errore, "id_contatto", rubrica, "id")


# ============================================================
# TODO: Esercizi per lo studente
# ============================================================

# TODO 1: Aggiungere una colonna "email" a tutti i record della rubrica.
#          Poi aggiornare stampa_tabella per visualizzarla.

# TODO 2: Scrivere una selezione che restituisca i contatti
#          il cui cognome inizia per 'V'.
#          Suggerimento: usare la funzione selezione() con .startswith()

# TODO 3: Scrivere una funzione verifica_dominio(tabella, colonna, tipo_atteso)
#          che controlli che tutti i valori di una colonna siano del tipo giusto.
#          Esempio: verifica_dominio(rubrica, "id", int) → True

# TODO 4: Implementare una funzione inserisci_contatto(rubrica, nuovo_contatto)
#          che prima verifichi PK, NOT NULL e dominio, e solo se tutto ok
#          aggiunga il contatto alla rubrica.
