SELECT
    e.id_esercizio,
    e.nome_esercizio,
    e.categoria
FROM Esercizi e
WHERE e.categoria IN (
    SELECT categoria
    FROM Esercizi
    WHERE nome_esercizio IN ('Squat', 'Panca piana')
)
ORDER BY e.categoria, e.nome_esercizio;

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
    ) conteggi_per_iscritto
)
ORDER BY numero_esecuzioni DESC, i.cognome;
