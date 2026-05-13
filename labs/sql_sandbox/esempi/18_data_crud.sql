INSERT INTO Contatti (id, nome, cognome, telefono)
VALUES (6, 'Elena', 'Bruni', '06-0000000');

SELECT id, nome, cognome, telefono
FROM Contatti
WHERE id = 6;

UPDATE Contatti
SET telefono = '06-1111111'
WHERE id = 6;

SELECT id, nome, cognome, telefono
FROM Contatti
WHERE id = 6;

DELETE FROM Contatti
WHERE id = 6;

SELECT id, nome, cognome, telefono
FROM Contatti
WHERE id = 6;
