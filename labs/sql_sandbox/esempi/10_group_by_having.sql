SELECT g.nome_gruppo, COUNT(a.id_contatto) AS numero_iscritti
FROM Gruppi g
LEFT JOIN Appartenenza a ON g.id_gruppo = a.id_gruppo
GROUP BY g.nome_gruppo
HAVING COUNT(a.id_contatto) >= 1
ORDER BY numero_iscritti DESC, g.nome_gruppo;
