BEGIN;

INSERT INTO Esecuzioni (
    id_esecuzione, id_iscritto, id_scheda, ordine_esecuzione,
    data_esecuzione, carico_effettivo, ripetizioni_effettive, nota
) VALUES (
    6000, 1, 1000, 1, '2026-05-14', 42.5, 8, 'prima registrazione della sessione'
);

SAVEPOINT seconda_esecuzione;

INSERT INTO Esecuzioni (
    id_esecuzione, id_iscritto, id_scheda, ordine_esecuzione,
    data_esecuzione, carico_effettivo, ripetizioni_effettive, nota
) VALUES (
    6001, 1, 1000, 2, '2026-05-14', 35.0, 8, 'registrazione da annullare'
);

ROLLBACK TO seconda_esecuzione;
RELEASE seconda_esecuzione;

COMMIT;

SELECT id_esecuzione, id_iscritto, id_scheda, ordine_esecuzione, data_esecuzione, nota
FROM Esecuzioni
WHERE id_esecuzione IN (6000, 6001)
ORDER BY id_esecuzione;
