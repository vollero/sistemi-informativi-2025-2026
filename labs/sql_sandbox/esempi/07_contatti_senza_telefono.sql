SELECT nome, cognome, telefono
FROM Contatti
WHERE telefono IS NULL
ORDER BY cognome, nome;
