# Istruzioni per chi lavora su questo repository

Materiale di un corso Python in quattro moduli (versioni Base e Avanzata). I notebook in `Aula_Base/` e
`Aula_Avanzata/` (cartelle `Modulo_1` … `Modulo_4` e `Soluzioni/`), in `Extra/` e in `Riserva/` sono GENERATI: non si
modificano a mano. Si modifica il sorgente in `_build/src/` e si ricostruisce. Anche il resto delle cartelle delle aule
è una copia rifatta a ogni build: gli originali sono `Dati/` e `Schede/` alla radice, i file del progetto dei corsisti
in `_build/aula/` e le cartelle della demo su uv e Ruff in `_build/src/script_uv_ruff/`.

## Prima di scrivere o modificare testo

Leggere, in quest'ordine, `_build/docs/STILE.md` (la prosa: tono da manuale tecnico, frasi complete, nessuna frase ad
effetto, con esempi prima/dopo), `_build/docs/REGOLE.md` (struttura, volume, dominio degli esempi, cartelle delle
aule) e `_build/docs/REQUISITI.md` (le richieste del docente); per gli esercizi anche `_build/docs/HANDS_ON.md`. Lo
stile vale per tutto: notebook, README, Guida, Schede. La skill generale `prosa-didattica` (in `.claude/skills/`)
descrive lo stesso tono per qualsiasi materiale didattico.
Il docente scrive in italiano; il gergo tecnico resta in inglese dove si usa in inglese.

L'edizione di ottobre 2026 (quattro giornate, 20-21 e 27-28 ottobre) segue `_build/docs/PIANO_OTTOBRE_2026.md`:
leggerlo prima di riorganizzare moduli, esercitazioni o tempi. La sequenza di riferimento è in
`_build/docs/PROPOSTA_PROGRAMMA_2026.md`.

## La cartella dell'aula

Il corsista riceve solo la propria cartella `Aula_X`, che deve funzionare da sola (dati, schede, `pyproject.toml`,
`uv.lock`, README). Il primo livello è `Modulo_1` … `Modulo_4`; i percorsi verso dati e schede partono dalla radice
dell'aula. Le soluzioni stanno in `Soluzioni/`, accanto ai moduli, e i corsisti le hanno da subito; il materiale del
docente (`Extra/`, `Riserva/`) resta fuori. Come si mantiene tutto questo è scritto in `_build/docs/REGOLE.md`,
sezione "La cartella dell'aula".

## Ciclo di lavoro

La skill `corso-notebook` (in `.claude/skills/`) descrive il procedimento completo: va seguita per qualsiasi modifica
al materiale. In breve:

    uv run python _build/controlla.py 07 E2    # build + soluzioni eseguite + Run All studente dei notebook indicati
    uv run python _build/controlla.py          # tutto il corso
    uv run python _build/leggi.py Aula_Base/Modulo_3/07_Pandas_operazioni.ipynb   # rilettura cella per cella
    uv run python _build/esporta.py            # build completo e zip per i corsisti in dist/

I tre passi separati restano disponibili: `_build/build.py`, `_build/validate.py` (soluzioni ed Extra) e
`_build/check_studente.py` (versione studente). `controlla.py` verifica sempre anche le cartelle delle aule: copie,
`uv.lock` dei corsisti e segnalazioni di Ruff sulla demo.

Il build deve finire con zero `[ERRORE]` e zero `[avviso]`: gli avvisi di stile (celle etichetta, frasi telegrafiche,
"Output atteso:" secco, titoli a effetto) si risolvono riscrivendo il testo, non aggirando il lint. Dopo una modifica
si rilegge il notebook generato in `Aula_Base/Modulo_N/` cella per cella, come farebbe un corsista, e la copia in
`Aula_Avanzata/` per le parti Avanzata.

## Cosa non si fa

- Niente sezioni facoltative dentro i notebook del percorso: il materiale in più va in `Approfondimenti_1/2`. Le
  sole eccezioni sono la sezione Extra in fondo ai notebook e, nell'Esercitazione 1 dell'Avanzata, la parte con gli
  esercizi classici da fare a casa.
- Niente box Ricorda, niente "bis", niente "passo in più". Dentro i notebook solo Hands-on inline (da due a tre, solo
  dove servono e sono rilevanti, cinque al massimo; piccoli, con `verifica=`) e una sezione Extra in fondo; i compiti
  interi stanno nelle Esercitazioni, costruite sugli esercizi del docente (vedi "Dove stanno gli esercizi" in
  `_build/docs/REGOLE.md`).
- Niente modifiche a mano dentro `Aula_*/`, neanche a dati, schede, README o `pyproject.toml`: si cambia l'originale e
  si ricostruisce. Niente percorsi che dai notebook delle aule escono dalla cartella dell'aula.
- Niente esempi nel dominio energetico nei notebook di sintassi (00-05), nell'Esercitazione 1 e negli script della
  demo su uv e Ruff; dati veri o i dataset inventati da pandas in poi.
- Niente identificativi di modelli di AI nei file del repository.
