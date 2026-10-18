---
name: corso-notebook
description: Scrivere, modificare, spostare o rileggere il materiale del corso Python in questo repository (notebook in Aula_Base/ e Aula_Avanzata/, cioè Modulo_1 … Modulo_4 e Soluzioni/, in Extra/ e Riserva/; Esercitazioni, Homework, Approfondimenti, Schede, README, Guida docente; i file del progetto dei corsisti in _build/aula e le cartelle demo ed esercizio su uv e Ruff). Usare questa skill ogni volta che si tocca un notebook o un testo del corso, anche per una sola cella, un esercizio, una verifica, un titolo o una frase, e anche quando la richiesta parla solo di "stile", "tono", "esercizio", "notebook", "aula", "modulo", "soluzioni", "sorgente", "dati", "zip" o "consegna ai corsisti". Il materiale è generato da _build/src, le cartelle delle aule sono copie rifatte a ogni build, e la prosa ha uno stile preciso che va rispettato e controllato con il build.
---

# Lavorare sul materiale del corso

I notebook di questo corso non si modificano a mano: ogni notebook in `Aula_Base/` e `Aula_Avanzata/` (nelle cartelle
`Modulo_1` … `Modulo_4` e in `Soluzioni/`), in `Extra/` e in `Riserva/` è generato da uno script Python in
`_build/src/`, che produce dallo stesso sorgente la versione studente e quella con le soluzioni per le due aule. Anche
il resto delle cartelle delle aule (dati, schede, progetto uv, README, impostazioni di VS Code, cartelle della demo su
uv e Ruff) è una copia che il build rifà ogni volta. Chi tocca il materiale lavora quindi sul sorgente o
sull'originale, ricostruisce e rilegge il risultato. Lo stile della prosa è il punto a cui il docente tiene di più:
un tono da manuale tecnico, con frasi complete e nessuna frase ad effetto, e vale per tutto il testo del repository,
dalle celle dei notebook al README.

## 1. Prima di scrivere

Il tono è quello della skill generale `prosa-didattica`, che va seguita per ogni testo. In questo repository le stesse
regole, con gli esempi presi dal corso, stanno in `_build/docs/STILE.md`: leggerlo per intero, perché è il documento
che decide se una frase va bene. Se la modifica riguarda la struttura di un
notebook (sezioni, esercizi, aule, tempi, dominio degli esempi) o la posizione dei file nelle cartelle delle aule,
leggere anche `_build/docs/REGOLE.md`, in particolare la sezione "La cartella dell'aula"; per gli Hands-on e gli Extra
di un notebook preciso, `_build/docs/HANDS_ON.md`; per le decisioni di questa edizione (moduli, tempi, esercitazioni,
la parte su script, uv e Ruff dell'Avanzata), `_build/docs/PIANO_OTTOBRE_2026.md`; se riguarda una scelta didattica o
un dubbio su cosa voleva il docente, `_build/docs/REQUISITI.md`. Il modello di riferimento per la voce è il testo
originale del docente, visibile nel branch `main`.

Il testo dei notebook parla al corsista, con il "tu" nelle consegne e il "noi" quando si lavora insieme, e non
descrive mai il corso dal punto di vista di chi lo organizza: niente "il docente corregge", "nell'aula Avanzata",
"nucleo comune". Quello che serve al docente va in `Guida_docente.md`; quello che serve a chi ha commissionato il
lavoro si scrive nel rapporto finale, non nel materiale.

Le cose che il docente non vuole più vedere: celle etichetta come "Esempio:" o "Unione:", sequenze di frasi
telegrafiche, catene di due punti al posto di una frase, antitesi e chiusure brillanti, domande retoriche, aperture con
"Qui" o "Ora", elenchi con il grassetto in testa al posto della spiegazione, un "Output atteso:" secco. Al loro posto
va un paragrafo di due a cinque frasi che dice che cosa fa lo strumento, a cosa serve e che cosa mostra la cella sotto.

## 2. Trovare il sorgente

| Notebook generato | Dove viene scritto | Sorgente | Numero per il build |
|---|---|---|---|
| `00_Notebook` … `11_Capstone` | `Aula_*/Modulo_N/` e `Aula_*/Soluzioni/` | `_build/src/nbNN_*.py` | `00` … `11` |
| `Esercitazione_1/2/3` | `Aula_*/Modulo_1` … `Modulo_3/` e `Aula_*/Soluzioni/` | `_build/src/nbE1_…py` ecc. | `E1`, `E2`, `E3` |
| `Ambiente_script_e_Ruff` | `Aula_Avanzata/Modulo_1/Script_uv_Ruff/`, senza copia in `Soluzioni/` | `_build/src/nbS_ambiente_script_e_ruff.py` | `S` |
| `Approfondimenti_1/2` | A1 in `Modulo_2/`; A2 in `Aula_Base/Modulo_3/` e `Aula_Avanzata/Modulo_4/`; più `Soluzioni/` | `_build/src/nbA1_…py`, `nbA2_…py` | `A1`, `A2` |
| `Homework` | `Riserva/Base/`, `Riserva/Avanzata/` (con `Homework_Soluzioni`) | `_build/src/nbC_homework.py` | `C` |
| notebook di riserva su uv, script e Ruff | `Riserva/Avanzata/` (con `Esercizi_uv_script_Ruff_Soluzioni`) | `_build/src/nbR_…py` | `R` |
| `Extra/*.ipynb` | `Extra/` | `_build/src/extra/*.py` | `EXTRA` |

Il resto delle cartelle delle aule non è generato ma copiato da `_build/statici.py` a ogni build, quindi anche lì si
modifica l'originale:

| Copia nell'aula | Originale |
|---|---|
| `Aula_*/Dati/`, `Aula_*/Schede/` | `Dati/` e `Schede/` alla radice del repository |
| `Aula_*/pyproject.toml`, `uv.lock`, `.python-version` | `_build/aula/` (dopo un cambio di dipendenze: `uv lock` dentro `_build/aula`) |
| `Aula_*/README.md`, `Aula_*/.vscode/` | `_build/aula/README_base.md`, `README_avanzata.md`, `_build/aula/vscode/<aula>/` |
| `Aula_Avanzata/Modulo_1/Script_uv_Ruff/demo/`, `esercizio/` | `_build/src/script_uv_ruff/demo/`, `esercizio/` |
| `Aula_Avanzata/Soluzioni/Script_uv_Ruff/demo/`, `esercizio/` | `_build/src/script_uv_ruff/soluzioni/demo/`, `soluzioni/esercizio/` |

Il corsista riceve soltanto la cartella della sua aula, `Aula_Base` o `Aula_Avanzata`, che deve funzionare da sola,
perché contiene i dati, le schede, il README e i file del progetto uv (`pyproject.toml`, `uv.lock` e
`.python-version`). Al primo livello stanno le cartelle `Modulo_1` … `Modulo_4`, e i percorsi verso i dati e le schede
partono dalla radice dell'aula, quindi da `Modulo_N/` e da `Soluzioni/` si scrive `../Dati/` e da
`Modulo_1/Script_uv_Ruff/` si scrive `../../Dati/`.
La cartella in cui finisce un notebook la decide la sua voce in `nbkit.PROGRAMMA` (`modulo`, `cartella`, `soluzioni`),
e il `blocco` del sorgente, che può essere un dizionario per aula, deve coincidere; il materiale di riserva ha
`riserva=True`. I dettagli, con le cose da aggiornare quando si aggiunge un file di dati o si cambia la demo, sono nella
sezione "La cartella dell'aula" di `REGOLE.md`.

Il docstring in testa a `_build/nbkit.py` descrive l'API del sorgente: `nb.sezione`, `nb.sottosezione`, `nb.md`,
`nb.code`, `nb.box`, `nb.hands_on`, `nb.esercizio`, il blocco `with nb.solo("avanzata"):` per le parti della sola
aula Avanzata e `aula="base"` per quelle della sola Base. La `verifica=` di un esercizio non compare nel notebook:
il build la raccoglie nel modulo `corso.py` di ogni cartella e nel notebook resta la chiamata `verifica("7.1")`.

## 3. Scrivere o modificare

Lavorare nel sorgente e lasciare il codice com'è quando la richiesta riguarda il testo; quando riguarda il codice,
controllare che gli `# Output:` nei commenti restino veri. Un esercizio nuovo ha sempre titolo, scenario in una o
due frasi, consegna con passi che sono frasi complete, `starter` con i `...`, `soluzione`, una `verifica=` con uno a
tre `assert` e messaggi brevi che dicono che cosa controllare (senza `print` finale: la riga ✅ la aggiunge il
toolkit), e se serve un `suggerimento` e un `perche`. Un concetto usato nella consegna deve essere già stato
spiegato nei notebook precedenti o in quello stesso, altrimenti va introdotto nel suggerimento con un esempio. I
posti per il codice del corsista sono quattro e hanno funzioni diverse (sezione "Dove stanno gli esercizi" di
`REGOLE.md`): dentro il notebook solo Hands-on inline, piccoli, subito dopo l'esempio che modificano, da due a tre
per notebook e solo dove servono e sono rilevanti, con un massimo di cinque; una sezione Extra in fondo con due o tre
esercizi brevi da fare a casa; il compito intero nelle Esercitazioni, costruite sugli esercizi del docente del branch
`main`; il Capstone nella giornata 4. Il notebook di spiegazione `Ambiente_script_e_Ruff` non ha né Hands-on né
Extra, perché la sua pratica è l'Esercitazione 1 dell'Avanzata, e non li ha nemmeno il capstone, che procede a passi
guidati. Il materiale che non sta nel percorso principale va in `Approfondimenti_1` o `_2`, non in sezioni facoltative
dentro i notebook.

La difficoltà di un esercizio sta in Python e in nulla altro: niente calcoli da impostare, niente matematica oltre
le quattro operazioni, niente conversioni di unità o ragionamenti sullo scenario. Numeri e operazioni entrano di
passaggio dentro esercizi su strutture dati, stringhe o dati, e ogni esercizio applica uno a uno la teoria appena
vista toccando più punti insieme.

Un esercizio si apre con un paragrafo che dice che cosa vogliamo ottenere e perché conviene farlo in Python, nei
termini dello scenario, e quando possibile il risultato atteso: da quel paragrafo il corsista deve poter arrivare al
risultato da solo. I passi numerati (`richiesta=`) finiscono nel blocco "Passo per passo", che si apre con un clic,
seguito dai suggerimenti e dalla soluzione a richiesta. Ogni richiesta ha un motivo che il corsista riconosce nello
scenario; una richiesta che serve solo a "fare esercizio" si toglie. La narrativa e il tono sono quelli degli
esercizi del docente nel branch `main` (notebook 02-04): obiettivo in una frase, scenario credibile, niente di
superfluo.

Gli esempi dei notebook di sintassi (00-05), dell'Esercitazione 1 e degli script della demo e dell'esercizio su uv e
Ruff stanno in scenari comuni, come spesa, viaggi, voti o meteo; i dati del settore energetico compaiono da pandas in
poi, con i dataset veri o quelli inventati già presenti in `Dati/`. Il gergo tecnico resta in inglese dove si usa in
inglese (notebook, kernel, DataFrame, slicing, encoding, formatter, linter).

Se cambiano i tempi di un notebook, aggiornare anche la tabella in `README.md`, quelle in `Guida_docente.md` e quella
in `_build/docs/PIANO_OTTOBRE_2026.md`.

## 3b. Le esercitazioni

Le esercitazioni di fine modulo hanno un formato proprio, descritto in `_build/docs/PIANO_OTTOBRE_2026.md`: un'ora,
di cui 45 minuti di lavoro e 15 di correzione; cinque o sei esercizi del nucleo in difficoltà crescente, eventuali
esercizi facoltativi e una sfida aperta senza verifica; un filo narrativo semplice (vita quotidiana nel modulo 1, dati
del corso da pandas in poi); ogni esercizio indipendente dagli altri. Il toolkit offre `Notebook(...,
soluzioni_a_richiesta=True)` per la cella `soluzione("E1.3")` sotto ogni esercizio, `suggerimenti=[...]` per gli
aiuti nascosti (due livelli in Base, al massimo uno in Avanzata) e `nb.domanda(...)` per le domande di riepilogo
iniziali, che sono quattro o cinque, dirette e con risposta breve: un autocontrollo di concetti, non quesiti sottili.
Le due aule nascono dallo stesso sorgente con un helper che chiama `nb.esercizio` due volte, come `step()` nel
capstone: la Base ha lo starter guidato e due suggerimenti, l'Avanzata lo starter quasi vuoto e talvolta una
richiesta in più. Prima di un passo complesso o appena visto va un breve paragrafo di richiamo teorico, in prosa.

L'Esercitazione 1 dell'Avanzata fa eccezione: l'ora è l'esercizio sullo script, in cui il corsista rifà la
dimostrazione del notebook `Ambiente_script_e_Ruff` nella cartella `Script_uv_Ruff/esercizio/`, con i comandi nel
terminale e i passi guidati nel notebook, più alcuni passi facoltativi elementari (un `print` in punti diversi,
`__name__`, `uv sync`). Gli esercizi classici restano in fondo allo stesso notebook, facoltativi, da fare a casa.
Il percorso `Script_uv_Ruff/esercizio/` vale sia da `Modulo_1/` sia da `Soluzioni/`, dove porta allo stato finale;
HANDS_ON.md descrive l'esercitazione per intero.

## 4. Ricostruire e controllare

    uv run python _build/controlla.py 07 E2              # build + soluzioni eseguite + Run All studente, solo questi
    uv run python _build/controlla.py S E1               # il notebook su uv, script e Ruff e l'Esercitazione 1
    uv run python _build/controlla.py                    # tutto il corso
    uv run python _build/esporta.py                      # build completo e zip per i corsisti in dist/
    uv run python _build/esporta.py --moduli 3 4         # aggiornamento dei soli moduli 3 e 4
    uv run python _build/esporta.py avanzata --riserva   # la riserva di un'aula

Il comando deve chiudersi con `build: OK`, `cartelle delle aule: OK` e con tutti i notebook OK. Il build segnala le
celle fuori stile: una cella etichetta è un errore, le frasi telegrafiche e l'"Output atteso:" secco sono avvisi, e si
risolvono riscrivendo il testo; anche un percorso `"Dati/...` senza il prefisso verso la radice dell'aula è un errore.
Qualunque notebook si indichi, `controlla.py` verifica anche le cartelle delle aule: che le copie dei dati e dei file
del progetto coincidano con gli originali, che `_build/aula/uv.lock` sia aggiornato e che Ruff dia sugli script della
dimostrazione e dell'esercizio le segnalazioni previste all'inizio e nessuna alla fine. Un build completo, senza
numeri, toglie dalle aule i notebook che nessun sorgente produce più. Il build rimette le cartelle della dimostrazione
e dell'esercizio esattamente come gli originali e toglie anche `.venv`, `uv.lock`, le cache e i file Excel lasciati da
una prova, quindi dopo una prova basta un build per ripartire dall'inizio. Le celle che chiamano un'API hanno il tag
`rete` e durante la validazione vengono saltate, quindi vanno lette con attenzione a mano.

Per consegnare il materiale ai corsisti si lancia `_build/esporta.py`, che ricostruisce tutto e prepara
`dist/Aula_Base.zip` e `dist/Aula_Avanzata.zip` con i soli file che git traccia o non ignora: `.venv`, le cache e i
file prodotti eseguendo i notebook restano fuori. Con `--moduli 3 4` prepara l'aggiornamento dei soli moduli 3 e 4
(`dist/Aula_X_moduli_3_4.zip`, senza `Modulo_1`, `Modulo_2`, `pyproject.toml` e `uv.lock`), e con `<aula> --riserva`
lo zip della riserva di un'aula, da estrarre dentro la cartella dell'aula; come si consegnano è scritto in `REGOLE.md`,
sezione "Come si mantiene".

## 5. Rileggere

    uv run python _build/leggi.py Aula_Base/Modulo_3/07_Pandas_operazioni.ipynb
    uv run python _build/leggi.py Aula_Avanzata/Modulo_1/Script_uv_Ruff/Ambiente_script_e_Ruff.ipynb

Il comando stampa il notebook generato cella per cella, come lo vede un corsista. Leggerlo dall'inizio alla fine
una volta, con la domanda "questa cella spiega qualcosa o è un appunto?", sistemare quello che non regge e
ricostruire. Per le parti Avanzata rileggere anche la copia in `Aula_Avanzata/`, e per le soluzioni quella in
`Aula_*/Soluzioni/`. È il passaggio che distingue un testo che passa il lint da un testo che si legge bene, e non si
salta.

## 6. Riferire

Dire che cosa è cambiato e dove, con due o tre esempi prima e dopo quando si è riscritto del testo, e segnalare le
frasi su cui si è incerti, in particolare le affermazioni tecniche aggiunte che non erano nel testo di partenza.
Non fare commit se non è richiesto. Nessun identificativo di modelli di AI nei file del repository.
