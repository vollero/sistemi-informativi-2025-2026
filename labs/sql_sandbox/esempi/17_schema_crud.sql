CREATE TABLE NoteContatto (
    id_nota INTEGER PRIMARY KEY,
    id_contatto INTEGER NOT NULL,
    testo TEXT NOT NULL,
    data_nota TEXT NOT NULL,
    FOREIGN KEY (id_contatto) REFERENCES Contatti(id)
);

INSERT INTO NoteContatto (id_nota, id_contatto, testo, data_nota)
VALUES (1, 1, 'Contatto preferito per comunicazioni urgenti', '2026-05-14');

SELECT n.id_nota, c.nome, c.cognome, n.testo, n.data_nota
FROM NoteContatto n
JOIN Contatti c ON n.id_contatto = c.id;

DROP TABLE NoteContatto;
