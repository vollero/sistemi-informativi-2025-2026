# Esercizi Guidati 2

Tema: `COUNT`, `GROUP BY`, `HAVING`

## Preparazione

```bash
python3 labs/sql_sandbox/reset_db.py
```

## Esercizio 1

Contare il numero totale di contatti.

Domanda guida:

- quante righe produce una query con `COUNT(*)`?

## Esercizio 2

Contare quanti contatti appartengono a ciascun gruppo.

Vincolo:

- il risultato deve mostrare il nome del gruppo, non solo il suo identificatore.

## Esercizio 3

Ripetere l'esercizio precedente mostrando anche i gruppi senza iscritti.

Domanda guida:

- quale differenza produce qui `LEFT JOIN`?

## Esercizio 4

Mostrare solo i gruppi con almeno un iscritto.

Vincolo:

- usare `HAVING`.

## Esercizio 5

Ordinare il risultato finale:

- prima per numero di iscritti decrescente
- poi per nome del gruppo

## Esercizio 6

Spiegare a parole la differenza tra:

- `WHERE`
- `HAVING`
