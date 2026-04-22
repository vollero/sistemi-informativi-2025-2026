# Esercizio Guidato 4

Tema: modellazione di una base dati per schede di allenamento

Questa esercitazione chiede di passare da uno scenario reale a un primo schema relazionale.

## Scenario

Una palestra vuole gestire:

- iscritti
- istruttori
- esercizi
- schede di allenamento
- esecuzioni reali degli esercizi

Ogni scheda:

- appartiene a un iscritto
- viene preparata da un istruttore
- contiene piu' esercizi ordinati
- per ogni esercizio indica serie, ripetizioni e altri parametri

L'applicazione deve anche registrare alcune esecuzioni svolte in palestra.

## Attivita'

1. Elenca le entita' principali del dominio.
2. Proponi un insieme di tabelle relazionali.
3. Indica le chiavi primarie.
4. Indica le chiavi esterne.
5. Spiega perche' serve una tabella separata per gli esercizi contenuti nella scheda.
6. Distingui tra dati della scheda e dati delle esecuzioni reali.
7. Scrivi uno schema relazionale sintetico.

## Domande guida

- una scheda contiene direttamente un solo esercizio o una lista ordinata di esercizi?
- lo stesso esercizio puo' comparire in schede diverse?
- le esecuzioni reali coincidono con la definizione della scheda oppure rappresentano eventi distinti?
- quali cancellazioni potrebbero rompere la coerenza dei dati?

## Output atteso

Un documento breve con:

- entita'
- relazioni
- tabelle proposte
- schema relazionale finale

Se vuoi, puoi anche provare a tradurre lo schema in primi `CREATE TABLE`.
