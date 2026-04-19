# Esercizi Guidati 1

Tema: `SELECT`, `WHERE`, `ORDER BY`

Usa la sandbox SQL del corso.

## Preparazione

```bash
python3 labs/sql_sandbox/reset_db.py
```

Per eseguire un file SQL:

```bash
python3 labs/sql_sandbox/run_sql.py <file.sql>
```

## Esercizio 1

Mostrare tutti i contatti con:

- `nome`
- `cognome`
- `telefono`

ordinati per `cognome` e poi per `nome`.

## Esercizio 2

Mostrare i soli contatti con telefono mancante.

Domanda guida:

- quale differenza c'e' tra `telefono = NULL` e `telefono IS NULL`?

## Esercizio 3

Mostrare i contatti con prefisso `06`, ordinati per cognome.

## Esercizio 4

Mostrare per ogni contatto:

- `nome`
- `cognome`
- `nome_gruppo`

anche quando il contatto non appartiene ad alcun gruppo.

Domanda guida:

- perche' qui e' piu' adatto `LEFT JOIN` rispetto a `JOIN`?

## Esercizio 5

Scrivere una breve spiegazione in linguaggio naturale di questa query prima di eseguirla:

```sql
SELECT c.nome, c.cognome, g.nome_gruppo
FROM Contatti c
LEFT JOIN Appartenenza a ON c.id = a.id_contatto
LEFT JOIN Gruppi g ON a.id_gruppo = g.id_gruppo
ORDER BY c.cognome, c.nome, g.nome_gruppo;
```
