SELECT i.nome, i.cognome, s.titolo, s.data_inizio, it.nome AS nome_istruttore, it.cognome AS cognome_istruttore
FROM SchedeAllenamento s
JOIN Iscritti i ON s.id_iscritto = i.id_iscritto
JOIN Istruttori it ON s.id_istruttore = it.id_istruttore
WHERE s.attiva = 1
ORDER BY i.cognome, i.nome;
