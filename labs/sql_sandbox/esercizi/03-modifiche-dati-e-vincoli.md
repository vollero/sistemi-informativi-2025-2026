# Esercizi Guidati 3

Tema: `INSERT`, `UPDATE`, `DELETE`

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

Inserire un nuovo contatto:

- `id = 6`
- `nome = Elena`
- `cognome = Bruni`
- `telefono = NULL`

Poi mostrare tutti i contatti ordinati per `id`.

## Esercizio 2

Inserire una nuova riga in `Appartenenza` che colleghi:

- il contatto `3`
- il gruppo `20`

Poi mostrare il contenuto di `Appartenenza`.

Domanda guida:

- perche' questa operazione e' lecita?

## Esercizio 3

Provare a inserire in `Appartenenza` una riga con:

- `id_contatto = 99`
- `id_gruppo = 20`

Domanda guida:

- quale vincolo deve bloccare l'operazione?

## Esercizio 4

Aggiornare il telefono del contatto con `id = 3` impostandolo a `06-2222222`.

Poi verificare il risultato con una `SELECT`.

Domanda guida:

- che cosa succederebbe se mancasse la clausola `WHERE`?

## Esercizio 5

Provare a cancellare:

1. il contatto con `id = 5`
2. il contatto con `id = 1`

Domanda guida:

- perche' i due casi hanno esito diverso?
