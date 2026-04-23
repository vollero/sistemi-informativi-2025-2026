"""
REPL applicativa del laboratorio palestra.
"""

import sqlite3


def stampa_tabella(righe, colonne):
    if not righe:
        print("  (nessuna riga)")
        return

    larghezze = [len(colonna) for colonna in colonne]
    valori = []

    for riga in righe:
        record = []
        for indice, colonna in enumerate(colonne):
            valore = riga[colonna]
            testo = "NULL" if valore is None else str(valore)
            larghezze[indice] = max(larghezze[indice], len(testo))
            record.append(testo)
        valori.append(record)

    header = " | ".join(colonne[i].ljust(larghezze[i]) for i in range(len(colonne)))
    separatore = "-+-".join("-" * larghezze[i] for i in range(len(colonne)))
    print(f"  {header}")
    print(f"  {separatore}")
    for record in valori:
        print("  " + " | ".join(record[i].ljust(larghezze[i]) for i in range(len(colonne))))


class PalestraREPL:
    def __init__(self, db):
        self.db = db
        self.ruoli = {
            "1": ("amministratore", self._sessione_amministratore),
            "2": ("istruttore", self._sessione_istruttore),
            "3": ("iscritto", self._sessione_iscritto),
        }

    def esegui(self):
        print("\n============================================")
        print("  LABORATORIO PALESTRA REPL")
        print(f"  Database: {self.db.db_path}")
        print("============================================")

        while True:
            print("\nRuoli disponibili:")
            print("  1. amministratore")
            print("  2. istruttore")
            print("  3. iscritto")
            print("  0. esci")

            scelta = input("\nSeleziona ruolo: ").strip()
            if scelta == "0":
                print("Chiusura laboratorio.")
                return

            if scelta not in self.ruoli:
                print("Scelta non valida.")
                continue

            _, funzione = self.ruoli[scelta]
            try:
                funzione()
            except sqlite3.IntegrityError as exc:
                print(f"\nErrore di vincolo: {exc}")
            except KeyboardInterrupt:
                print("\nOperazione annullata.")

    def _sessione_amministratore(self):
        comandi = {
            "1": ("mostra iscritti", self._mostra_iscritti),
            "2": ("crea iscritto", self._crea_iscritto),
            "3": ("aggiorna iscritto", self._aggiorna_iscritto),
            "4": ("elimina iscritto", self._elimina_iscritto),
            "5": ("mostra istruttori", self._mostra_istruttori),
            "6": ("crea istruttore", self._crea_istruttore),
            "7": ("aggiorna istruttore", self._aggiorna_istruttore),
            "8": ("elimina istruttore", self._elimina_istruttore),
        }
        self._esegui_menu_ruolo("amministratore", comandi)

    def _sessione_istruttore(self):
        comandi = {
            "1": ("mostra esercizi", self._mostra_esercizi),
            "2": ("crea esercizio", self._crea_esercizio),
            "3": ("aggiorna esercizio", self._aggiorna_esercizio),
            "4": ("elimina esercizio", self._elimina_esercizio),
            "5": ("mostra schede", self._mostra_schede),
            "6": ("crea scheda", self._crea_scheda),
            "7": ("aggiorna scheda", self._aggiorna_scheda),
            "8": ("elimina scheda", self._elimina_scheda),
            "9": ("dettaglio scheda", self._dettaglio_scheda),
            "10": ("aggiungi esercizio a scheda", self._aggiungi_esercizio_a_scheda),
            "11": ("aggiorna esercizio di scheda", self._aggiorna_esercizio_di_scheda),
            "12": ("rimuovi esercizio da scheda", self._rimuovi_esercizio_da_scheda),
        }
        self._esegui_menu_ruolo("istruttore", comandi)

    def _sessione_iscritto(self):
        utente = self._scegli_iscritto()
        if utente is None:
            return

        nome = f"{utente['nome']} {utente['cognome']}"
        comandi = {
            "1": ("mostra le mie schede", lambda: self._mostra_schede_iscritto(utente["id_iscritto"])),
            "2": ("mostra le mie esecuzioni", lambda: self._mostra_esecuzioni_iscritto(utente["id_iscritto"])),
            "3": ("registra esecuzione", lambda: self._crea_esecuzione(utente["id_iscritto"])),
            "4": ("aggiorna esecuzione", lambda: self._aggiorna_esecuzione(utente["id_iscritto"])),
            "5": ("elimina esecuzione", lambda: self._elimina_esecuzione(utente["id_iscritto"])),
        }
        self._esegui_menu_ruolo(f"iscritto: {nome}", comandi)

    def _esegui_menu_ruolo(self, titolo, comandi):
        while True:
            print(f"\n--- Menu {titolo} ---")
            for codice, (etichetta, _) in comandi.items():
                print(f"  {codice}. {etichetta}")
            print("  0. torna al menu ruoli")

            scelta = input("\nScelta: ").strip()
            if scelta == "0":
                return

            if scelta not in comandi:
                print("Scelta non valida.")
                continue

            try:
                comandi[scelta][1]()
            except sqlite3.IntegrityError as exc:
                print(f"Errore di vincolo: {exc}")

    def _prompt(self, etichetta, default=None, allow_empty=False):
        suffix = f" [{default}]" if default not in (None, "") else ""
        valore = input(f"  {etichetta}{suffix}: ").strip()
        if valore:
            return valore
        if default is not None:
            return default
        if allow_empty:
            return ""
        print("  Valore obbligatorio.")
        return self._prompt(etichetta, default=default, allow_empty=allow_empty)

    def _prompt_int(self, etichetta, default=None):
        testo = self._prompt(etichetta, default=None if default is None else str(default), allow_empty=default is not None)
        if testo == "" and default is not None:
            return default
        try:
            return int(testo)
        except ValueError:
            print("  Inserire un intero valido.")
            return self._prompt_int(etichetta, default=default)

    def _prompt_float(self, etichetta, default=None, allow_empty=True):
        default_testo = None if default is None else str(default)
        testo = self._prompt(etichetta, default=default_testo, allow_empty=allow_empty)
        if testo == "":
            return None
        try:
            return float(testo)
        except ValueError:
            print("  Inserire un numero valido.")
            return self._prompt_float(etichetta, default=default, allow_empty=allow_empty)

    def _prompt_bool(self, etichetta, default=1):
        testo_default = "1" if default else "0"
        valore = self._prompt(f"{etichetta} (1/0)", default=testo_default)
        if valore not in {"0", "1"}:
            print("  Inserire 1 oppure 0.")
            return self._prompt_bool(etichetta, default=default)
        return int(valore)

    def _conferma(self, messaggio):
        return input(f"  {messaggio} (s/n): ").strip().lower() == "s"

    def _get_row(self, sql, params, label):
        row = self.db.query_one(sql, params)
        if row is None:
            print(f"  {label} non trovato.")
        return row

    def _mostra_iscritti(self):
        righe = self.db.query(
            """
            SELECT id_iscritto, nome, cognome, data_nascita, data_iscrizione
            FROM Iscritti
            ORDER BY cognome, nome
            """
        )
        stampa_tabella(righe, ["id_iscritto", "nome", "cognome", "data_nascita", "data_iscrizione"])

    def _crea_iscritto(self):
        id_iscritto = self._prompt_int("id iscritto")
        nome = self._prompt("nome")
        cognome = self._prompt("cognome")
        data_nascita = self._prompt("data nascita YYYY-MM-DD")
        data_iscrizione = self._prompt("data iscrizione YYYY-MM-DD")
        self.db.execute(
            """
            INSERT INTO Iscritti (id_iscritto, nome, cognome, data_nascita, data_iscrizione)
            VALUES (?, ?, ?, ?, ?)
            """,
            (id_iscritto, nome, cognome, data_nascita, data_iscrizione),
        )
        print("  Iscritto creato.")

    def _aggiorna_iscritto(self):
        id_iscritto = self._prompt_int("id iscritto")
        row = self._get_row("SELECT * FROM Iscritti WHERE id_iscritto = ?", (id_iscritto,), "Iscritto")
        if row is None:
            return
        nome = self._prompt("nome", row["nome"])
        cognome = self._prompt("cognome", row["cognome"])
        data_nascita = self._prompt("data nascita YYYY-MM-DD", row["data_nascita"])
        data_iscrizione = self._prompt("data iscrizione YYYY-MM-DD", row["data_iscrizione"])
        self.db.execute(
            """
            UPDATE Iscritti
            SET nome = ?, cognome = ?, data_nascita = ?, data_iscrizione = ?
            WHERE id_iscritto = ?
            """,
            (nome, cognome, data_nascita, data_iscrizione, id_iscritto),
        )
        print("  Iscritto aggiornato.")

    def _elimina_iscritto(self):
        id_iscritto = self._prompt_int("id iscritto")
        row = self._get_row("SELECT * FROM Iscritti WHERE id_iscritto = ?", (id_iscritto,), "Iscritto")
        if row is None:
            return
        if not self._conferma(f"Eliminare iscritto {row['nome']} {row['cognome']}?"):
            print("  Operazione annullata.")
            return
        self.db.execute("DELETE FROM Iscritti WHERE id_iscritto = ?", (id_iscritto,))
        print("  Iscritto eliminato.")

    def _mostra_istruttori(self):
        righe = self.db.query(
            """
            SELECT id_istruttore, nome, cognome, specializzazione
            FROM Istruttori
            ORDER BY cognome, nome
            """
        )
        stampa_tabella(righe, ["id_istruttore", "nome", "cognome", "specializzazione"])

    def _crea_istruttore(self):
        id_istruttore = self._prompt_int("id istruttore")
        nome = self._prompt("nome")
        cognome = self._prompt("cognome")
        specializzazione = self._prompt("specializzazione", allow_empty=True)
        self.db.execute(
            """
            INSERT INTO Istruttori (id_istruttore, nome, cognome, specializzazione)
            VALUES (?, ?, ?, ?)
            """,
            (id_istruttore, nome, cognome, specializzazione or None),
        )
        print("  Istruttore creato.")

    def _aggiorna_istruttore(self):
        id_istruttore = self._prompt_int("id istruttore")
        row = self._get_row("SELECT * FROM Istruttori WHERE id_istruttore = ?", (id_istruttore,), "Istruttore")
        if row is None:
            return
        nome = self._prompt("nome", row["nome"])
        cognome = self._prompt("cognome", row["cognome"])
        specializzazione = self._prompt("specializzazione", row["specializzazione"] or "", allow_empty=True)
        self.db.execute(
            """
            UPDATE Istruttori
            SET nome = ?, cognome = ?, specializzazione = ?
            WHERE id_istruttore = ?
            """,
            (nome, cognome, specializzazione or None, id_istruttore),
        )
        print("  Istruttore aggiornato.")

    def _elimina_istruttore(self):
        id_istruttore = self._prompt_int("id istruttore")
        row = self._get_row("SELECT * FROM Istruttori WHERE id_istruttore = ?", (id_istruttore,), "Istruttore")
        if row is None:
            return
        if not self._conferma(f"Eliminare istruttore {row['nome']} {row['cognome']}?"):
            print("  Operazione annullata.")
            return
        self.db.execute("DELETE FROM Istruttori WHERE id_istruttore = ?", (id_istruttore,))
        print("  Istruttore eliminato.")

    def _mostra_esercizi(self):
        righe = self.db.query(
            """
            SELECT id_esercizio, nome_esercizio, categoria, descrizione
            FROM Esercizi
            ORDER BY nome_esercizio
            """
        )
        stampa_tabella(righe, ["id_esercizio", "nome_esercizio", "categoria", "descrizione"])

    def _crea_esercizio(self):
        id_esercizio = self._prompt_int("id esercizio")
        nome = self._prompt("nome esercizio")
        categoria = self._prompt("categoria", allow_empty=True)
        descrizione = self._prompt("descrizione", allow_empty=True)
        self.db.execute(
            """
            INSERT INTO Esercizi (id_esercizio, nome_esercizio, categoria, descrizione)
            VALUES (?, ?, ?, ?)
            """,
            (id_esercizio, nome, categoria or None, descrizione or None),
        )
        print("  Esercizio creato.")

    def _aggiorna_esercizio(self):
        id_esercizio = self._prompt_int("id esercizio")
        row = self._get_row("SELECT * FROM Esercizi WHERE id_esercizio = ?", (id_esercizio,), "Esercizio")
        if row is None:
            return
        nome = self._prompt("nome esercizio", row["nome_esercizio"])
        categoria = self._prompt("categoria", row["categoria"] or "", allow_empty=True)
        descrizione = self._prompt("descrizione", row["descrizione"] or "", allow_empty=True)
        self.db.execute(
            """
            UPDATE Esercizi
            SET nome_esercizio = ?, categoria = ?, descrizione = ?
            WHERE id_esercizio = ?
            """,
            (nome, categoria or None, descrizione or None, id_esercizio),
        )
        print("  Esercizio aggiornato.")

    def _elimina_esercizio(self):
        id_esercizio = self._prompt_int("id esercizio")
        row = self._get_row("SELECT * FROM Esercizi WHERE id_esercizio = ?", (id_esercizio,), "Esercizio")
        if row is None:
            return
        if not self._conferma(f"Eliminare esercizio {row['nome_esercizio']}?"):
            print("  Operazione annullata.")
            return
        self.db.execute("DELETE FROM Esercizi WHERE id_esercizio = ?", (id_esercizio,))
        print("  Esercizio eliminato.")

    def _mostra_schede(self):
        righe = self.db.query(
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
        stampa_tabella(righe, ["id_scheda", "titolo", "iscritto", "istruttore", "data_inizio", "data_fine", "attiva"])

    def _crea_scheda(self):
        id_scheda = self._prompt_int("id scheda")
        id_iscritto = self._prompt_int("id iscritto")
        id_istruttore = self._prompt_int("id istruttore")
        titolo = self._prompt("titolo")
        data_inizio = self._prompt("data inizio YYYY-MM-DD")
        data_fine = self._prompt("data fine YYYY-MM-DD", allow_empty=True)
        attiva = self._prompt_bool("scheda attiva", default=1)
        self.db.execute(
            """
            INSERT INTO SchedeAllenamento (
                id_scheda, id_iscritto, id_istruttore, titolo, data_inizio, data_fine, attiva
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (id_scheda, id_iscritto, id_istruttore, titolo, data_inizio, data_fine or None, attiva),
        )
        print("  Scheda creata.")

    def _aggiorna_scheda(self):
        id_scheda = self._prompt_int("id scheda")
        row = self._get_row("SELECT * FROM SchedeAllenamento WHERE id_scheda = ?", (id_scheda,), "Scheda")
        if row is None:
            return
        id_iscritto = self._prompt_int("id iscritto", row["id_iscritto"])
        id_istruttore = self._prompt_int("id istruttore", row["id_istruttore"])
        titolo = self._prompt("titolo", row["titolo"])
        data_inizio = self._prompt("data inizio YYYY-MM-DD", row["data_inizio"])
        data_fine = self._prompt("data fine YYYY-MM-DD", row["data_fine"] or "", allow_empty=True)
        attiva = self._prompt_bool("scheda attiva", default=row["attiva"])
        self.db.execute(
            """
            UPDATE SchedeAllenamento
            SET id_iscritto = ?, id_istruttore = ?, titolo = ?, data_inizio = ?, data_fine = ?, attiva = ?
            WHERE id_scheda = ?
            """,
            (id_iscritto, id_istruttore, titolo, data_inizio, data_fine or None, attiva, id_scheda),
        )
        print("  Scheda aggiornata.")

    def _elimina_scheda(self):
        id_scheda = self._prompt_int("id scheda")
        row = self._get_row("SELECT * FROM SchedeAllenamento WHERE id_scheda = ?", (id_scheda,), "Scheda")
        if row is None:
            return
        if not self._conferma(f"Eliminare scheda {row['titolo']}?"):
            print("  Operazione annullata.")
            return
        self.db.execute("DELETE FROM SchedeAllenamento WHERE id_scheda = ?", (id_scheda,))
        print("  Scheda eliminata.")

    def _dettaglio_scheda(self):
        id_scheda = self._prompt_int("id scheda")
        header = self.db.query_one(
            """
            SELECT s.id_scheda, s.titolo, i.nome || ' ' || i.cognome AS iscritto
            FROM SchedeAllenamento s
            JOIN Iscritti i ON s.id_iscritto = i.id_iscritto
            WHERE s.id_scheda = ?
            """,
            (id_scheda,),
        )
        if header is None:
            print("  Scheda non trovata.")
            return
        print(f"  Scheda {header['id_scheda']} - {header['titolo']} ({header['iscritto']})")
        righe = self.db.query(
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
            (id_scheda,),
        )
        stampa_tabella(righe, ["ordine_esecuzione", "nome_esercizio", "serie", "ripetizioni", "carico_suggerito", "durata_secondi", "recupero_secondi"])

    def _aggiungi_esercizio_a_scheda(self):
        id_scheda = self._prompt_int("id scheda")
        if self._get_row("SELECT * FROM SchedeAllenamento WHERE id_scheda = ?", (id_scheda,), "Scheda") is None:
            return
        ordine = self._prompt_int("ordine esecuzione")
        id_esercizio = self._prompt_int("id esercizio")
        serie = self._prompt_int("serie")
        ripetizioni = self._prompt_int("ripetizioni", default=0)
        carico = self._prompt_float("carico suggerito", allow_empty=True)
        durata = self._prompt_int("durata secondi", default=0)
        recupero = self._prompt_int("recupero secondi", default=0)
        self.db.execute(
            """
            INSERT INTO SchedaEsercizi (
                id_scheda, ordine_esecuzione, id_esercizio, serie, ripetizioni,
                carico_suggerito, durata_secondi, recupero_secondi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                id_scheda,
                ordine,
                id_esercizio,
                serie,
                None if ripetizioni == 0 else ripetizioni,
                carico,
                None if durata == 0 else durata,
                None if recupero == 0 else recupero,
            ),
        )
        print("  Esercizio aggiunto alla scheda.")

    def _aggiorna_esercizio_di_scheda(self):
        id_scheda = self._prompt_int("id scheda")
        ordine = self._prompt_int("ordine esecuzione")
        row = self._get_row(
            "SELECT * FROM SchedaEsercizi WHERE id_scheda = ? AND ordine_esecuzione = ?",
            (id_scheda, ordine),
            "Esercizio di scheda",
        )
        if row is None:
            return
        id_esercizio = self._prompt_int("id esercizio", row["id_esercizio"])
        serie = self._prompt_int("serie", row["serie"])
        ripetizioni = self._prompt_int("ripetizioni", 0 if row["ripetizioni"] is None else row["ripetizioni"])
        carico = self._prompt_float("carico suggerito", row["carico_suggerito"], allow_empty=True)
        durata = self._prompt_int("durata secondi", 0 if row["durata_secondi"] is None else row["durata_secondi"])
        recupero = self._prompt_int("recupero secondi", 0 if row["recupero_secondi"] is None else row["recupero_secondi"])
        self.db.execute(
            """
            UPDATE SchedaEsercizi
            SET id_esercizio = ?, serie = ?, ripetizioni = ?, carico_suggerito = ?, durata_secondi = ?, recupero_secondi = ?
            WHERE id_scheda = ? AND ordine_esecuzione = ?
            """,
            (
                id_esercizio,
                serie,
                None if ripetizioni == 0 else ripetizioni,
                carico,
                None if durata == 0 else durata,
                None if recupero == 0 else recupero,
                id_scheda,
                ordine,
            ),
        )
        print("  Esercizio di scheda aggiornato.")

    def _rimuovi_esercizio_da_scheda(self):
        id_scheda = self._prompt_int("id scheda")
        ordine = self._prompt_int("ordine esecuzione")
        row = self._get_row(
            """
            SELECT se.id_scheda, se.ordine_esecuzione, e.nome_esercizio
            FROM SchedaEsercizi se
            JOIN Esercizi e ON se.id_esercizio = e.id_esercizio
            WHERE se.id_scheda = ? AND se.ordine_esecuzione = ?
            """,
            (id_scheda, ordine),
            "Esercizio di scheda",
        )
        if row is None:
            return
        if not self._conferma(f"Rimuovere {row['nome_esercizio']} dalla scheda {id_scheda}?"):
            print("  Operazione annullata.")
            return
        self.db.execute(
            "DELETE FROM SchedaEsercizi WHERE id_scheda = ? AND ordine_esecuzione = ?",
            (id_scheda, ordine),
        )
        print("  Esercizio rimosso dalla scheda.")

    def _scegli_iscritto(self):
        self._mostra_iscritti()
        id_iscritto = self._prompt_int("id iscritto per la sessione")
        return self._get_row("SELECT * FROM Iscritti WHERE id_iscritto = ?", (id_iscritto,), "Iscritto")

    def _mostra_schede_iscritto(self, id_iscritto):
        righe = self.db.query(
            """
            SELECT id_scheda, titolo, data_inizio, data_fine, attiva
            FROM SchedeAllenamento
            WHERE id_iscritto = ?
            ORDER BY data_inizio DESC, id_scheda
            """,
            (id_iscritto,),
        )
        stampa_tabella(righe, ["id_scheda", "titolo", "data_inizio", "data_fine", "attiva"])

    def _mostra_esecuzioni_iscritto(self, id_iscritto):
        righe = self.db.query(
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
            (id_iscritto,),
        )
        stampa_tabella(righe, ["id_esecuzione", "data_esecuzione", "id_scheda", "ordine_esecuzione", "nome_esercizio", "carico_effettivo", "ripetizioni_effettive", "nota"])

    def _scheda_appartiene_all_iscritto(self, id_iscritto, id_scheda):
        return self.db.query_one(
            "SELECT * FROM SchedeAllenamento WHERE id_scheda = ? AND id_iscritto = ?",
            (id_scheda, id_iscritto),
        ) is not None

    def _crea_esecuzione(self, id_iscritto):
        id_esecuzione = self._prompt_int("id esecuzione")
        id_scheda = self._prompt_int("id scheda")
        if not self._scheda_appartiene_all_iscritto(id_iscritto, id_scheda):
            print("  La scheda indicata non appartiene all'iscritto corrente.")
            return
        ordine = self._prompt_int("ordine esecuzione nella scheda")
        if self._get_row(
            "SELECT * FROM SchedaEsercizi WHERE id_scheda = ? AND ordine_esecuzione = ?",
            (id_scheda, ordine),
            "Esercizio di scheda",
        ) is None:
            return
        data_esecuzione = self._prompt("data esecuzione YYYY-MM-DD")
        carico = self._prompt_float("carico effettivo", allow_empty=True)
        ripetizioni = self._prompt_int("ripetizioni effettive", default=0)
        nota = self._prompt("nota", allow_empty=True)
        self.db.execute(
            """
            INSERT INTO Esecuzioni (
                id_esecuzione, id_iscritto, id_scheda, ordine_esecuzione,
                data_esecuzione, carico_effettivo, ripetizioni_effettive, nota
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                id_esecuzione,
                id_iscritto,
                id_scheda,
                ordine,
                data_esecuzione,
                carico,
                None if ripetizioni == 0 else ripetizioni,
                nota or None,
            ),
        )
        print("  Esecuzione registrata.")

    def _aggiorna_esecuzione(self, id_iscritto):
        id_esecuzione = self._prompt_int("id esecuzione")
        row = self._get_row(
            "SELECT * FROM Esecuzioni WHERE id_esecuzione = ? AND id_iscritto = ?",
            (id_esecuzione, id_iscritto),
            "Esecuzione",
        )
        if row is None:
            return
        data_esecuzione = self._prompt("data esecuzione YYYY-MM-DD", row["data_esecuzione"])
        carico = self._prompt_float("carico effettivo", row["carico_effettivo"], allow_empty=True)
        ripetizioni = self._prompt_int(
            "ripetizioni effettive",
            0 if row["ripetizioni_effettive"] is None else row["ripetizioni_effettive"],
        )
        nota = self._prompt("nota", row["nota"] or "", allow_empty=True)
        self.db.execute(
            """
            UPDATE Esecuzioni
            SET data_esecuzione = ?, carico_effettivo = ?, ripetizioni_effettive = ?, nota = ?
            WHERE id_esecuzione = ? AND id_iscritto = ?
            """,
            (
                data_esecuzione,
                carico,
                None if ripetizioni == 0 else ripetizioni,
                nota or None,
                id_esecuzione,
                id_iscritto,
            ),
        )
        print("  Esecuzione aggiornata.")

    def _elimina_esecuzione(self, id_iscritto):
        id_esecuzione = self._prompt_int("id esecuzione")
        row = self._get_row(
            "SELECT * FROM Esecuzioni WHERE id_esecuzione = ? AND id_iscritto = ?",
            (id_esecuzione, id_iscritto),
            "Esecuzione",
        )
        if row is None:
            return
        if not self._conferma(f"Eliminare esecuzione {id_esecuzione}?"):
            print("  Operazione annullata.")
            return
        self.db.execute(
            "DELETE FROM Esecuzioni WHERE id_esecuzione = ? AND id_iscritto = ?",
            (id_esecuzione, id_iscritto),
        )
        print("  Esecuzione eliminata.")
