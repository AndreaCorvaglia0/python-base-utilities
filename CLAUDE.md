# Istruzioni per chi lavora su questo repository

Materiale di un corso Python di due giornate (versioni Base e Avanzata). I notebook in `Aula_*/`, `Soluzioni_*/` ed
`Extra/` sono GENERATI: non si modificano a mano. Si modifica il sorgente in `_build/src/` e si ricostruisce.

## Prima di scrivere o modificare testo

Leggere, in quest'ordine, `_build/docs/STILE.md` (la prosa: tono da manuale tecnico, frasi complete, nessuna frase ad
effetto, con esempi prima/dopo), `_build/docs/REGOLE.md` (struttura, volume, dominio degli esempi) e
`_build/docs/REQUISITI.md` (le richieste del docente). Lo stile vale per tutto: notebook, README, Guida, Schede.
Il docente scrive in italiano; il gergo tecnico resta in inglese dove si usa in inglese.

## Ciclo di lavoro

La skill `corso-notebook` (in `.claude/skills/`) descrive il procedimento completo: va seguita per qualsiasi modifica
al materiale. In breve:

    uv run python _build/controlla.py 07 E2    # build + soluzioni eseguite + Run All studente dei notebook indicati
    uv run python _build/controlla.py          # tutto il corso
    uv run python _build/leggi.py Aula_Base/07_Pandas_operazioni.ipynb   # rilettura cella per cella

I tre passi separati restano disponibili: `_build/build.py`, `_build/validate.py` (Soluzioni ed Extra) e
`_build/check_studente.py` (Aula).

Il build deve finire con zero `[ERRORE]` e zero `[avviso]`: gli avvisi di stile (celle etichetta, frasi telegrafiche,
"Output atteso:" secco, titoli a effetto) si risolvono riscrivendo il testo, non aggirando il lint. Dopo una modifica
si rilegge il notebook generato in `Aula_Base/` cella per cella, come farebbe un corsista.

## Cosa non si fa

- Niente sezioni facoltative dentro i notebook del percorso: il materiale in più va in `Approfondimenti_1/2`.
- Niente box Ricorda, niente "bis", niente "passo in più"; al massimo due Prova tu per notebook, 2-3 esercizi più uno
  facoltativo, ogni esercizio con la sua `verifica=` (1-3 assert).
- Niente esempi nel dominio energetico nei notebook di sintassi (00-05); dati veri o i dataset inventati da pandas in poi.
- Niente identificativi di modelli di AI nei file del repository.
