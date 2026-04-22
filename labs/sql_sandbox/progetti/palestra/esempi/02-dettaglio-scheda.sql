SELECT
    s.id_scheda,
    s.titolo,
    se.ordine_esecuzione,
    e.nome_esercizio,
    se.serie,
    se.ripetizioni,
    se.carico_suggerito,
    se.durata_secondi,
    se.recupero_secondi
FROM SchedeAllenamento s
JOIN SchedaEsercizi se ON s.id_scheda = se.id_scheda
JOIN Esercizi e ON se.id_esercizio = e.id_esercizio
WHERE s.id_scheda = 1000
ORDER BY se.ordine_esecuzione;
