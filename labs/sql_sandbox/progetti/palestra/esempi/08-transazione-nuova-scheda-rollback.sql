BEGIN;

INSERT INTO SchedeAllenamento (
    id_scheda, id_iscritto, id_istruttore, titolo, data_inizio, data_fine, attiva
) VALUES (
    2000, 3, 10, 'Scheda prova transazione', '2026-05-14', NULL, 1
);

INSERT INTO SchedaEsercizi (
    id_scheda, ordine_esecuzione, id_esercizio, serie, ripetizioni,
    carico_suggerito, durata_secondi, recupero_secondi
) VALUES
    (2000, 1, 100, 3, 8, 30.0, NULL, 90),
    (2000, 2, 130, 3, NULL, NULL, 45, 30);

SELECT s.id_scheda, s.titolo, e.nome_esercizio
FROM SchedeAllenamento s
JOIN SchedaEsercizi se ON s.id_scheda = se.id_scheda
JOIN Esercizi e ON se.id_esercizio = e.id_esercizio
WHERE s.id_scheda = 2000
ORDER BY se.ordine_esecuzione;

ROLLBACK;

SELECT id_scheda, titolo
FROM SchedeAllenamento
WHERE id_scheda = 2000;
