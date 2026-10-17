# Guida per il docente

Il corso si tiene in quattro moduli di quattro ore, il 20 e 21 ottobre e il 27 e 28 ottobre 2026, in due versioni,
Base e Avanzata, che seguono lo stesso programma. In ogni giornata l'aula Base fa il modulo nelle prime quattro ore e
l'aula Avanzata lo stesso modulo nelle quattro successive, così le due aule arrivano alla fine di ogni giornata allo
stesso punto. I notebook contengono quello che il corsista deve leggere ed eseguire, mentre le parti che il docente
mostra dal vivo, cioè VS Code, Data Wrangler e il wrapper delle API, non compaiono nei notebook: il materiale per
prepararle si trova nella cartella `Extra/`, e le tabelle di questa guida indicano quando svolgerle e quanto durano.

## Prima del corso

Sui PC dell'aula devono essere installati VS Code con le estensioni Python, Jupyter, Data Wrangler e GitHub Copilot,
più Ruff per la versione Avanzata, e uv. La cartella del corso va scaricata in anticipo e `uv sync` va eseguito una
volta, seguendo la sezione "Installazione" del README.

La cartella `Dati/fallback/` contiene risposte di esempio delle API usate nel corso, in modo che tutte le celle
funzionino anche senza rete. Quando la rete è disponibile, il comando `uv run python _build/scarica_fallback.py`
sostituisce i file di esempio con i dati veri, cioè la temperatura di Milano e le misure dei sensori lombardi.

I notebook si rigenerano dagli script in `_build/src/` con `uv run python _build/build.py`, e `uv run python
_build/controlla.py` ricostruisce tutto, esegue le soluzioni e la versione studente e segnala le celle fuori stile. I
controlli degli esercizi, richiamati nei notebook con `verifica("7.1")`, sono raccolti nel file `corso.py` presente in
ogni cartella, che il build genera dagli assert scritti nei sorgenti; il corsista vede soltanto la chiamata e una riga
con ✅ oppure ❌. Prima della prima giornata conviene aprire un'esercitazione in VS Code su un PC dell'aula e controllare
che i blocchi "Passo per passo" e "Suggerimento" si aprano con un clic e che la cella `soluzione(...)` mostri il codice
colorato.

## La struttura di un modulo

Ogni blocco di quattro ore, cioè 240 minuti, contiene due pause da 15 minuti. Nei moduli 1, 2 e 3 l'ultima ora è
l'esercitazione, 45 minuti di lavoro dei corsisti e 15 di correzione, quindi restano circa 150 minuti di lezione, e i
tempi qui sotto stanno dentro questo spazio con un margine di 10-20 minuti. Il modulo 4 non ha esercitazione: la
giornata è dedicata a Plotly, agli agenti per il coding e al capstone.

Dentro i notebook gli Hands-on sono i momenti in cui i corsisti toccano il codice appena visto: uno o due minuti
ciascuno, si lasciano fare e non si correggono insieme. La sezione Extra in fondo a ogni notebook si salta e si indica
come lavoro per casa; non è compresa nei tempi.

## I tempi (minuti netti di lezione, pause ed esercitazione escluse)

Modulo 1 · martedì 20 ottobre · Setup, Python e sintassi di base

| | Base | Avanzata |
|---|---|---|
| Demo VS Code (`Extra/VS_Code_e_notebook.ipynb`) | 15 | 15 |
| 00 Jupyter e i notebook | 20 | 20 |
| 01 Introduzione a Python e sintassi base | 40 | 30 |
| 02 Tipi di dato e manipolazione | 40 | 35 |
| 03 Codice leggibile | 20 | 20 |
| Ambiente, script e Ruff (solo Avanzata) | — | 30 |
| **Lezione** | **135** | **150** |
| Esercitazione 1 | 60 | 60 |

Modulo 2 · mercoledì 21 ottobre · Controllo del flusso, funzioni e primi dati in pandas

| | Base | Avanzata |
|---|---|---|
| 04 Funzioni e controllo del flusso | 50 | 50 |
| 05 Oggetti ed errori | 35 | 30 |
| 06 Pandas: Series, DataFrame e import dei dati | 55 | 70 |
| **Lezione** | **140** | **150** |
| Esercitazione 2 | 60 | 60 |

Modulo 3 · martedì 27 ottobre · Analisi dei dati con pandas

| | Base | Avanzata |
|---|---|---|
| 07 Pandas: operazioni sui DataFrame | 65 | 70 |
| Demo Data Wrangler (`Extra/Data_Wrangler.ipynb`) | 15 | 15 |
| 08 Pandas: le date | 50 | 50 |
| **Lezione** | **130** | **135** |
| Esercitazione 3 | 60 | 60 |

Modulo 4 · mercoledì 28 ottobre · Agenti per il coding e capstone

| | Base | Avanzata |
|---|---|---|
| 09 Plotly per serie storiche | 25 | 25 |
| 10 Agenti per il coding | 35 | 35 |
| 11 Capstone, step 1-6 | 110 | 110 |
| 11 Capstone, step 7 con Copilot | 40 | 40 |
| **Totale** | **210** | **210** |

Il notebook 09 dà il minimo di Plotly che serve per leggere un grafico scritto da un agente, e lo slider,
l'istogramma e lo scatter si mostrano senza fermarsi. Lo step 7 del capstone è la parte aperta della giornata: i
corsisti scelgono una richiesta tra quelle elencate e la portano a termine con Copilot, applicando le tre abitudini
del notebook 10; è anche il margine del modulo, perché si accorcia senza perdere nulla di quello che precede. Quando
occorre tagliare, conviene farlo alla fine di una sezione e non a metà.

## Le dimostrazioni dal vivo

| Quando | Cosa mostrare | Materiale | Base | Avanzata |
|---|---|---|---|---|
| Modulo 1, apertura | VS Code: aprire la cartella, le estensioni, **Select Kernel** → `.venv`, eseguire una cella, Run All e Restart, le scorciatoie | `Extra/VS_Code_e_notebook.ipynb` | 15 min | 15 min |
| Modulo 2, nel 06 (A) | Il wrapper: chiudere la chiamata all'API in una funzione riutilizzabile, prima dell'esercizio facoltativo dell'Esercitazione 2 | `Extra/API_wrapper.ipynb` | — | 5 min |
| Modulo 3, dopo il 07 | Data Wrangler: aprire un DataFrame, Editing mode, un filtro e una colonna tolta, il codice pandas che genera | `Extra/Data_Wrangler.ipynb` | 15 min | 15 min |

L'ambiente del progetto, gli script e Ruff non sono più dimostrazioni: nell'aula Avanzata sono il notebook
`Ambiente_script_e_Ruff` del modulo 1, mentre nella Base si citano in apertura, durante la demo di VS Code, con la sola
idea che `uv sync` ha costruito la cartella `.venv` con tutte le librerie.

## Le esercitazioni

Le tre esercitazioni durano un'ora ciascuna: 45 minuti di lavoro dei corsisti e 15 di correzione, in cui si mostrano
le soluzioni dei cinque esercizi; la sfida finale e gli eventuali facoltativi non si correggono, ma hanno anche loro la
cella `soluzione`. Gli esercizi sono quelli scritti dal docente nei notebook delle edizioni precedenti, portati nel
formato comune: ogni esercizio apre dicendo che cosa si vuole ottenere, i passi stanno in un blocco che si apre con un
clic, i suggerimenti sono nascosti e la soluzione di ogni esercizio si mostra a richiesta. In Base ogni esercizio ha
due suggerimenti e uno starter guidato, in Avanzata un suggerimento, uno starter quasi vuoto e una richiesta in più. Il
testo dei notebook non parla del docente né della correzione: quello che serve a chi conduce l'ora sta qui. I
notebook delle soluzioni si distribuiscono dopo la correzione.

Due controlli degli esercizi originali erano sbagliati e il materiale usa i valori corretti: le capitali con un
numero pari di lettere sono sei (Roma ne ha quattro e Washington dieci), e gli utenti con più di tre ascolti sono tre,
perché l'utente 101 ne ha quindici.

## Se la classe è avanti

I notebook `Approfondimenti_1` e `Approfondimenti_2`, presenti in entrambe le cartelle Aula con le soluzioni in
`Soluzioni_*/`, raccolgono il materiale uscito dal percorso principale. Il primo contiene le operazioni con i set, il
ciclo `while` e la lettura di più file CSV con i tipi di dato; il secondo contiene le differenze tra date e il fuso
orario. Nella versione Avanzata si aggiungono `map`, `filter` e i generatori nel primo, e `shift`, `rolling`, i type
hint, le dataclass, i decoratori e `**kwargs` nel secondo. Si aprono quando un modulo termina in anticipo, una sezione
alla volta, e si possono anche lasciare ai corsisti come lettura per casa. L'Homework, una settimana nell'ufficio
Analisi Consumi, resta in `Riserva/Base/` e `Riserva/Avanzata/` con le soluzioni, da distribuire solo a una classe
molto più veloce del previsto. Per l'aula Avanzata è previsto un breve notebook facoltativo su Prophet nel modulo 4,
da preparare dopo aver verificato che `uv add prophet` funzioni sui PC dell'aula.

## Il percorso minimo

Se un modulo procede male, per problemi di installazione, di rete o per una classe lenta, le parti che non si saltano
sono queste:

- Modulo 1: 00, 01, 02 (liste e dizionari). Esercitazione ridotta a tre esercizi.
- Modulo 2: 04 (`if`, `for`, funzioni), 06 (CSV ed Excel). Esercitazione ridotta a tre esercizi.
- Modulo 3: 07 (selezione, valori mancanti, groupby), 08 (indice temporale e resample). Esercitazione ridotta a tre
  esercizi.
- Modulo 4: 09 (un grafico a linee), 10 ridotto alla prova guidata con un prompt solo, 11 (step 1-4 e una richiesta
  dello step 7).

## Dove tagliare se si è in ritardo

- Le sezioni Extra sono già fuori dal tempo d'aula; gli Hands-on si possono saltare a voce, mostrando la soluzione.
- Esercitazioni: le domande si fanno a voce, gli esercizi si riducono a tre.
- 06 Avanzata: la sezione sulle API si accorcia all'esempio dell'anagrafica dei sensori.
- 07 Avanzata: `query`, l'assegnazione condizionale con `.loc`, l'indice a due colonne e `agg` sono le parti in più
  rispetto a Base: si possono citare e basta.
- 09: la sezione sugli altri grafici si può solo mostrare.
- Capstone: gli step 1-4 sono il minimo; 5 e 6 si possono fare insieme sullo schermo del docente, e lo step 7 si
  riduce a una richiesta.

## Per chi modifica il materiale

I notebook sono generati dagli script in `_build/src/` e non si modificano a mano. Le regole di scrittura stanno in
`_build/docs/`: `STILE.md` descrive la prosa, con esempi prima e dopo, `REGOLE.md` la struttura dei notebook e i
quattro posti degli esercizi, `HANDS_ON.md` il piano degli Hands-on per notebook, `PIANO_OTTOBRE_2026.md` le decisioni
di questa edizione e `REQUISITI.md` le scelte prese con il docente. Il file `CLAUDE.md` nella radice del repository
riassume il ciclo di lavoro per chi usa un agente per il coding, e la skill `corso-notebook` in `.claude/skills/` lo
descrive passo per passo: dopo ogni modifica si esegue `uv run python _build/controlla.py NN`, che ricostruisce i
notebook indicati, segnala le celle fuori stile ed esegue soluzioni e versione studente, e si rilegge il risultato con
`_build/leggi.py`.
