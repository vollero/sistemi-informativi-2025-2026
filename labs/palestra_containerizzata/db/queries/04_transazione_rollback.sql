BEGIN;

INSERT INTO Iscritti (id_iscritto, nome, cognome, data_nascita, data_iscrizione)
VALUES (99, 'Test', 'Rollback', '2002-01-01', '2026-05-13');

INSERT INTO SchedeAllenamento (
    id_scheda, id_iscritto, id_istruttore, titolo, data_inizio, data_fine, attiva
) VALUES (
    1999, 99, 10, 'Scheda temporanea', '2026-05-13', NULL, 1
);

SELECT id_iscritto, nome, cognome
FROM Iscritti
WHERE id_iscritto = 99;

ROLLBACK;

SELECT id_iscritto, nome, cognome
FROM Iscritti
WHERE id_iscritto = 99;
