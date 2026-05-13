SELECT
    i.nome,
    i.cognome,
    s.titolo,
    e.nome_esercizio,
    se.serie,
    se.ripetizioni,
    se.carico_suggerito
FROM SchedeAllenamento s
JOIN Iscritti i ON s.id_iscritto = i.id_iscritto
JOIN SchedaEsercizi se ON s.id_scheda = se.id_scheda
JOIN Esercizi e ON se.id_esercizio = e.id_esercizio
WHERE s.attiva = 1
  AND e.categoria IN (
      SELECT categoria
      FROM Esercizi
      WHERE nome_esercizio IN ('Squat', 'Affondi')
  )
ORDER BY i.cognome, i.nome, se.ordine_esecuzione;
