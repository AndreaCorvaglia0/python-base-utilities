# Guida per il docente

Il corso dura due giornate e si tiene in due versioni, Base e Avanzata, che seguono lo stesso programma. I notebook
contengono quello che il corsista deve leggere ed eseguire, mentre le parti che il docente mostra dal vivo, cioè VS Code,
l'ambiente del progetto, Ruff, Data Wrangler e il wrapper delle API, non compaiono nei notebook. Il materiale per
prepararle si trova nella cartella `Extra/`, e le tabelle di questa guida indicano quando svolgerle e quanto durano.

## Prima del corso

Sui PC dell'aula devono essere installati VS Code con le estensioni Python, Jupyter, Data Wrangler e GitHub Copilot,
più Ruff per la versione Avanzata, e uv. La cartella del corso va scaricata in anticipo e `uv sync` va eseguito una
volta, seguendo la sezione "Installazione" del README.

La cartella `Dati/fallback/` contiene risposte di esempio delle API usate nel corso, in modo che tutte le celle
funzionino anche senza rete. Quando la rete è disponibile, il comando `uv run python _build/scarica_fallback.py`
sostituisce i file di esempio con i dati veri, cioè la temperatura di Milano e le misure dei sensori lombardi.

I notebook si rigenerano dagli script in `_build/src/` con `uv run python _build/build.py`, e le soluzioni si possono
eseguire da capo a fondo con `uv run python _build/validate.py Soluzioni_Base/*.ipynb Soluzioni_Avanzata/*.ipynb`. I
controlli degli esercizi, richiamati nei notebook con `verifica("7.1")`, sono raccolti nel file `corso.py` presente in
ogni cartella, che il build genera dagli assert scritti nei sorgenti; il corsista vede soltanto la chiamata e una riga
con ✅ oppure ❌.

## Le dimostrazioni dal vivo

| Quando | Cosa mostrare | Materiale | Base | Avanzata |
|---|---|---|---|---|
| Giornata 1, apertura | VS Code: aprire la cartella, le estensioni, **Select Kernel** → `.venv`, eseguire una cella, Run All e Restart, le scorciatoie | `Extra/VS_Code_e_notebook.ipynb` | 15 min | 15 min |
| Giornata 1, dopo l'Esercitazione 2 | L'ambiente del progetto: `.venv`, `pyproject.toml`, `uv add`, `uv sync`; uno script `.py` lanciato con `uv run` | `Extra/Ambiente_uv_e_script.ipynb` | 5 min (solo l'idea) | 10 min |
| Giornata 1, nel 06 (A) | Il wrapper: chiudere la chiamata all'API in una funzione riutilizzabile | `Extra/API_wrapper.ipynb` | — | 10 min |
| Giornata 2, dopo il 07 | Data Wrangler: aprire un DataFrame, Editing mode, un filtro e una colonna tolta, il codice pandas che genera | `Extra/Data_Wrangler.ipynb` | 15 min | 15 min |

Il notebook `Extra/Ruff.ipynb` non è in programma e si mostra soltanto se una classe Avanzata è in anticipo.

## I tempi (minuti netti)

Giornata 1 (Blocchi 1 e 2)

| | Base | Avanzata |
|---|---|---|
| Demo VS Code | 15 | 15 |
| 00 Jupyter e i notebook | 20 | 20 |
| 01 Introduzione a Python e sintassi base | 45 | 35 |
| 02 Tipi di dato e manipolazione | 40 | 35 |
| 03 Codice leggibile | 20 | 20 |
| Esercitazione 1 | 20 | 20 |
| 04 Funzioni e controllo del flusso | 55 | 60 |
| 05 Oggetti ed errori | 40 | 35 |
| 06 Pandas: Series, DataFrame e import dei dati (+ demo wrapper in Avanzata) | 55 | 75 + 10 |
| Esercitazione 2 | 20 | 20 |
| Demo ambiente e script | 5 | 10 |
| Presentazione dell'Homework | 5 | 5 |
| **Totale** | **340** | **360** |

Giornata 2 (Blocchi 3 e 4)

| | Base | Avanzata |
|---|---|---|
| Correzione dell'Homework | 15 | 15 |
| 07 Pandas: operazioni sui DataFrame | 70 | 75 |
| Demo Data Wrangler | 15 | 15 |
| 08 Pandas: le date | 55 | 55 |
| 09 Plotly per serie storiche | 30 | 25 |
| Esercitazione 3 | 20 | 20 |
| 10 Agenti per il coding | 45 | 45 |
| 11 Capstone | 110 | 110 |
| **Totale** | **360** | **360** |

Una giornata di sette ore nette corrisponde a 420 minuti, quindi restano tra 60 e 80 minuti di margine per i
problemi di installazione, le domande e le pause che si allungano. Quando occorre tagliare, conviene farlo alla fine di
una sezione e non a metà.

## Se la classe è avanti

I notebook `Approfondimenti_1` e `Approfondimenti_2`, presenti in entrambe le cartelle Aula con le soluzioni in
`Soluzioni_*/`, raccolgono il materiale uscito dal percorso principale. Il primo contiene le operazioni con i set, il
ciclo `while` e la lettura di più file CSV con i tipi di dato; il secondo contiene le differenze tra date, il fuso
orario, il range slider e l'esportazione in HTML. Nella versione Avanzata si aggiungono `map`, `filter` e i
generatori nel primo, e `shift`, `rolling`, i type hint, le dataclass, i decoratori e `**kwargs` nel secondo. Si
aprono a fine giornata o quando un blocco termina in anticipo, una sezione alla volta, e si possono anche lasciare ai
corsisti come lettura per casa.

## Il percorso minimo

Se la giornata procede male, per problemi di installazione, di rete o per una classe lenta, le parti che non si
saltano sono queste:

- Giornata 1: 00, 01, 02 (liste e dizionari), 04 (`if`, `for`, funzioni), 06 (CSV ed Excel). Esercitazioni a voce.
- Giornata 2: 07 (selezione, valori mancanti, groupby), 08 (indice temporale e resample), 09 (un grafico a linee),
  11 (step 1-4). Il 10 si riduce alla prova guidata con un prompt solo.

## Dove tagliare se si è in ritardo

- Gli esercizi segnati **(facoltativo)**: si lasciano ai corsisti, da fare a casa.
- Esercitazioni: le domande si fanno a voce, gli esercizi si riducono a due.
- 06 Avanzata: l'esercizio facoltativo sulle API si salta; la demo del wrapper si accorcia a 5 minuti.
- 07 Avanzata: `query`, l'assegnazione condizionale con `.loc`, l'indice a due colonne e `agg` sono le parti in più rispetto a Base: si possono citare e basta.
- 10: la prova guidata si fa con un prompt solo.
- Capstone: gli step 1-4 sono il minimo; 5 e 6 si possono fare insieme sullo schermo del docente.

## Homework

L'homework occupa tra 40 e 45 minuti tra le due giornate e si trova in `Aula_*/Homework.ipynb`, con le soluzioni in
`Soluzioni_*/Homework.ipynb`. Si presenta in cinque minuti alla fine della prima giornata e si corregge insieme
all'inizio della seconda.
