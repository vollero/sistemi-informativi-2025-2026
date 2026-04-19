SELECT g.nome_gruppo, COUNT(a.id_contatto) AS numero_iscritti
FROM Gruppi g
LEFT JOIN Appartenenza a ON g.id_gruppo = a.id_gruppo
GROUP BY g.nome_gruppo
ORDER BY g.nome_gruppo;
