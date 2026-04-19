SELECT c.nome, c.cognome, g.nome_gruppo
FROM Contatti c
LEFT JOIN Appartenenza a ON c.id = a.id_contatto
LEFT JOIN Gruppi g ON a.id_gruppo = g.id_gruppo
ORDER BY c.id, g.nome_gruppo;
