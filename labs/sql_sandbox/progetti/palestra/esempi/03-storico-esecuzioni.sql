SELECT
    i.nome,
    i.cognome,
    ex.data_esecuzione,
    e.nome_esercizio,
    ex.carico_effettivo,
    ex.ripetizioni_effettive,
    ex.nota
FROM Esecuzioni ex
JOIN Iscritti i ON ex.id_iscritto = i.id_iscritto
JOIN SchedaEsercizi se ON ex.id_scheda = se.id_scheda
    AND ex.ordine_esecuzione = se.ordine_esecuzione
JOIN Esercizi e ON se.id_esercizio = e.id_esercizio
WHERE ex.id_iscritto = 1
ORDER BY ex.data_esecuzione, ex.id_esecuzione;
