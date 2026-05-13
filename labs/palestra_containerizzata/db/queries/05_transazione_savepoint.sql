BEGIN;

INSERT INTO Esecuzioni (
    id_esecuzione, id_iscritto, id_scheda, ordine_esecuzione,
    data_esecuzione, carico_effettivo, ripetizioni_effettive, nota
) VALUES (
    7000, 1, 1000, 1, '2026-05-13', 42.5, 8, 'registrazione confermata'
);

SAVEPOINT prova_seconda_registrazione;

INSERT INTO Esecuzioni (
    id_esecuzione, id_iscritto, id_scheda, ordine_esecuzione,
    data_esecuzione, carico_effettivo, ripetizioni_effettive, nota
) VALUES (
    7001, 1, 1000, 2, '2026-05-13', 32.5, 8, 'registrazione annullata'
);

ROLLBACK TO prova_seconda_registrazione;
RELEASE prova_seconda_registrazione;
COMMIT;

SELECT id_esecuzione, id_iscritto, id_scheda, ordine_esecuzione, data_esecuzione, nota
FROM Esecuzioni
WHERE id_esecuzione IN (7000, 7001)
ORDER BY id_esecuzione;
