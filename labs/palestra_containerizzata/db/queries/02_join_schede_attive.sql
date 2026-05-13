SELECT
    i.nome || ' ' || i.cognome AS iscritto,
    s.titolo AS scheda,
    it.nome || ' ' || it.cognome AS istruttore,
    se.ordine_esecuzione,
    e.nome_esercizio,
    se.serie,
    se.ripetizioni,
    se.carico_suggerito,
    se.durata_secondi,
    se.recupero_secondi
FROM SchedeAllenamento s
JOIN Iscritti i ON s.id_iscritto = i.id_iscritto
JOIN Istruttori it ON s.id_istruttore = it.id_istruttore
JOIN SchedaEsercizi se ON s.id_scheda = se.id_scheda
JOIN Esercizi e ON se.id_esercizio = e.id_esercizio
WHERE s.attiva = 1
ORDER BY i.cognome, i.nome, s.id_scheda, se.ordine_esecuzione;
