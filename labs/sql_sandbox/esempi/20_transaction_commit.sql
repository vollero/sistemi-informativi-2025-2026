BEGIN;

INSERT INTO Contatti (id, nome, cognome, telefono)
VALUES (6, 'Elena', 'Bruni', '06-0000000');

COMMIT;

SELECT id, nome, cognome, telefono
FROM Contatti
ORDER BY id;
