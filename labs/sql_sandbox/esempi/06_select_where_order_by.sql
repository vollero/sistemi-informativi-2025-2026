SELECT nome, cognome, telefono
FROM Contatti
WHERE telefono LIKE '06%'
ORDER BY cognome, nome;
