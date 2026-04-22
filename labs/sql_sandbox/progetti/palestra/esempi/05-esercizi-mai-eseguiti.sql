SELECT
    e.nome_esercizio
FROM Esercizi e
LEFT JOIN SchedaEsercizi se ON e.id_esercizio = se.id_esercizio
LEFT JOIN Esecuzioni ex ON se.id_scheda = ex.id_scheda
    AND se.ordine_esecuzione = ex.ordine_esecuzione
WHERE ex.id_esecuzione IS NULL
ORDER BY e.nome_esercizio;
