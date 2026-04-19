PRAGMA foreign_keys = ON;

CREATE TABLE Contatti (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cognome TEXT NOT NULL,
    telefono TEXT
);

CREATE TABLE Gruppi (
    id_gruppo INTEGER PRIMARY KEY,
    nome_gruppo TEXT NOT NULL UNIQUE
);

CREATE TABLE Appartenenza (
    id_contatto INTEGER,
    id_gruppo INTEGER,
    PRIMARY KEY (id_contatto, id_gruppo),
    FOREIGN KEY (id_contatto) REFERENCES Contatti(id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY (id_gruppo) REFERENCES Gruppi(id_gruppo) ON DELETE RESTRICT ON UPDATE RESTRICT
);
