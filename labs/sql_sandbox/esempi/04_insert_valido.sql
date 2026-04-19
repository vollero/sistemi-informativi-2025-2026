INSERT INTO Contatti (id, nome, cognome, telefono)
VALUES (6, 'Elena', 'Bruni', '06-0000000');

SELECT id, nome, cognome, telefono
FROM Contatti
WHERE id = 6;
