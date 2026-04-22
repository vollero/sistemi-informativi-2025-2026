SELECT
    e.nome_esercizio,
    COUNT(ex.id_esecuzione) AS numero_esecuzioni
FROM Esercizi e
LEFT JOIN SchedaEsercizi se ON e.id_esercizio = se.id_esercizio
LEFT JOIN Esecuzioni ex ON se.id_scheda = ex.id_scheda
    AND se.ordine_esecuzione = ex.ordine_esecuzione
GROUP BY e.id_esercizio, e.nome_esercizio
ORDER BY numero_esecuzioni DESC, e.nome_esercizio;
