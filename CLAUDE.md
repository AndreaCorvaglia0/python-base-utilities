# Istruzioni per chi lavora su questo repository

Materiale di un corso Python di due giornate (versioni Base e Avanzata). I notebook in `Aula_*/`, `Soluzioni_*/` ed
`Extra/` sono GENERATI: non si modificano a mano. Si modifica il sorgente in `_build/src/` e si ricostruisce.

## Prima di scrivere o modificare testo

Leggere, in quest'ordine, `_build/docs/STILE.md` (la prosa: tono da manuale tecnico, frasi complete, nessuna frase ad
effetto, con esempi prima/dopo), `_build/docs/REGOLE.md` (struttura, volume, dominio degli esempi) e
`_build/docs/REQUISITI.md` (le richieste del docente). Lo stile vale per tutto: notebook, README, Guida, Schede. La skill generale `prosa-didattica`
(in `.claude/skills/`) descrive lo stesso tono per qualsiasi materiale didattico.
Il docente scrive in italiano; il gergo tecnico resta in inglese dove si usa in inglese.

L'edizione di ottobre 2026 (quattro giornate, 20-21 e 27-28 ottobre) segue `_build/docs/PIANO_OTTOBRE_2026.md`:
leggerlo prima di riorganizzare moduli, esercitazioni o tempi. La sequenza di riferimento è in
`_build/docs/PROPOSTA_PROGRAMMA_2026.md`.

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
- Niente box Ricorda, niente "bis", niente "passo in più". Dentro i notebook solo Hands-on inline (2-5, piccoli, con
  `verifica=`) e una sezione Extra in fondo; i compiti interi stanno nelle Esercitazioni, costruite sugli esercizi del
  docente (vedi "Dove stanno gli esercizi" in `_build/docs/REGOLE.md`).
- Niente esempi nel dominio energetico nei notebook di sintassi (00-05); dati veri o i dataset inventati da pandas in poi.
- Niente identificativi di modelli di AI nei file del repository.
