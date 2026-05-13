BEGIN;

INSERT INTO Contatti (id, nome, cognome, telefono)
VALUES (6, 'Elena', 'Bruni', '06-0000000');

UPDATE Contatti
SET telefono = '06-1111111'
WHERE id = 1;

SELECT id, nome, cognome, telefono
FROM Contatti
ORDER BY id;

ROLLBACK;

SELECT id, nome, cognome, telefono
FROM Contatti
ORDER BY id;
