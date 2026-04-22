PRAGMA foreign_keys = ON;

INSERT INTO Iscritti (id_iscritto, nome, cognome, data_nascita, data_iscrizione) VALUES
    (1, 'Alice', 'Conti', '2000-05-14', '2026-01-10'),
    (2, 'Marco', 'De Santis', '1998-11-02', '2026-02-03'),
    (3, 'Sara', 'Leoni', '2001-07-21', '2026-02-20');

INSERT INTO Istruttori (id_istruttore, nome, cognome, specializzazione) VALUES
    (10, 'Paolo', 'Rinaldi', 'Forza'),
    (20, 'Elena', 'Marini', 'Funzionale');

INSERT INTO Esercizi (id_esercizio, nome_esercizio, categoria, descrizione) VALUES
    (100, 'Squat', 'Gambe', 'Piegamenti con bilanciere'),
    (110, 'Panca piana', 'Petto', 'Spinta su panca con bilanciere'),
    (120, 'Lat machine', 'Schiena', 'Trazione al cavo alto'),
    (130, 'Plank', 'Core', 'Tenuta isometrica'),
    (140, 'Affondi', 'Gambe', 'Affondi alternati con manubri');

INSERT INTO SchedeAllenamento (id_scheda, id_iscritto, id_istruttore, titolo, data_inizio, data_fine, attiva) VALUES
    (1000, 1, 10, 'Scheda forza base', '2026-03-01', NULL, 1),
    (1001, 2, 20, 'Scheda ricondizionamento', '2026-03-10', NULL, 1),
    (1002, 1, 20, 'Scheda febbraio introduttiva', '2026-02-01', '2026-02-28', 0);

INSERT INTO SchedaEsercizi (
    id_scheda, ordine_esecuzione, id_esercizio, serie, ripetizioni,
    carico_suggerito, durata_secondi, recupero_secondi
) VALUES
    (1000, 1, 100, 4, 8, 40.0, NULL, 90),
    (1000, 2, 110, 4, 8, 30.0, NULL, 90),
    (1000, 3, 130, 3, NULL, NULL, 45, 30),
    (1001, 1, 140, 3, 10, 12.0, NULL, 60),
    (1001, 2, 120, 3, 12, 25.0, NULL, 75),
    (1001, 3, 130, 3, NULL, NULL, 30, 30),
    (1002, 1, 120, 3, 10, 20.0, NULL, 60),
    (1002, 2, 130, 2, NULL, NULL, 30, 30);

INSERT INTO Esecuzioni (
    id_esecuzione, id_iscritto, id_scheda, ordine_esecuzione,
    data_esecuzione, carico_effettivo, ripetizioni_effettive, nota
) VALUES
    (5000, 1, 1000, 1, '2026-03-04', 40.0, 8, 'esecuzione regolare'),
    (5001, 1, 1000, 2, '2026-03-04', 30.0, 8, 'ultima serie faticosa'),
    (5002, 1, 1000, 3, '2026-03-04', NULL, NULL, 'tenuta completa'),
    (5003, 2, 1001, 1, '2026-03-12', 10.0, 10, 'buon controllo'),
    (5004, 2, 1001, 2, '2026-03-12', 25.0, 12, 'completo'),
    (5005, 2, 1001, 3, '2026-03-12', NULL, NULL, '30 secondi mantenuti');
