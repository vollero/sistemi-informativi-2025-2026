PRAGMA foreign_keys = ON;

CREATE TABLE Iscritti (
    id_iscritto INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cognome TEXT NOT NULL,
    data_nascita TEXT NOT NULL,
    data_iscrizione TEXT NOT NULL
);

CREATE TABLE Istruttori (
    id_istruttore INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cognome TEXT NOT NULL,
    specializzazione TEXT
);

CREATE TABLE Esercizi (
    id_esercizio INTEGER PRIMARY KEY,
    nome_esercizio TEXT NOT NULL,
    categoria TEXT,
    descrizione TEXT
);

CREATE TABLE SchedeAllenamento (
    id_scheda INTEGER PRIMARY KEY,
    id_iscritto INTEGER NOT NULL,
    id_istruttore INTEGER NOT NULL,
    titolo TEXT NOT NULL,
    data_inizio TEXT NOT NULL,
    data_fine TEXT,
    attiva INTEGER NOT NULL DEFAULT 1 CHECK (attiva IN (0, 1)),
    FOREIGN KEY (id_iscritto) REFERENCES Iscritti(id_iscritto) ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY (id_istruttore) REFERENCES Istruttori(id_istruttore) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE TABLE SchedaEsercizi (
    id_scheda INTEGER NOT NULL,
    ordine_esecuzione INTEGER NOT NULL,
    id_esercizio INTEGER NOT NULL,
    serie INTEGER NOT NULL,
    ripetizioni INTEGER,
    carico_suggerito REAL,
    durata_secondi INTEGER,
    recupero_secondi INTEGER,
    PRIMARY KEY (id_scheda, ordine_esecuzione),
    FOREIGN KEY (id_scheda) REFERENCES SchedeAllenamento(id_scheda) ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY (id_esercizio) REFERENCES Esercizi(id_esercizio) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE TABLE Esecuzioni (
    id_esecuzione INTEGER PRIMARY KEY,
    id_iscritto INTEGER NOT NULL,
    id_scheda INTEGER NOT NULL,
    ordine_esecuzione INTEGER NOT NULL,
    data_esecuzione TEXT NOT NULL,
    carico_effettivo REAL,
    ripetizioni_effettive INTEGER,
    nota TEXT,
    FOREIGN KEY (id_iscritto) REFERENCES Iscritti(id_iscritto) ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY (id_scheda, ordine_esecuzione) REFERENCES SchedaEsercizi(id_scheda, ordine_esecuzione)
        ON DELETE RESTRICT ON UPDATE RESTRICT
);
