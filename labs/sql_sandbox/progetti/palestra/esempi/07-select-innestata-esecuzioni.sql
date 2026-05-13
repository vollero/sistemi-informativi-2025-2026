SELECT
    i.nome,
    i.cognome,
    COUNT(ex.id_esecuzione) AS numero_esecuzioni
FROM Iscritti i
LEFT JOIN Esecuzioni ex ON i.id_iscritto = ex.id_iscritto
GROUP BY i.id_iscritto, i.nome, i.cognome
HAVING COUNT(ex.id_esecuzione) >= (
    SELECT AVG(conteggio)
    FROM (
        SELECT COUNT(*) AS conteggio
        FROM Esecuzioni
        GROUP BY id_iscritto
    )
)
ORDER BY numero_esecuzioni DESC, i.cognome;
