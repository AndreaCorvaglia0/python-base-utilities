# Guida per il docente

Due giornate, due aule (Base e Avanzata) con lo stesso programma. I notebook contengono quello che il corsista deve
leggere ed eseguire; le parti che si mostrano dal vivo (VS Code, ambiente, Ruff, Data Wrangler, wrapper delle API) non
stanno nei notebook: il materiale per prepararle è nella cartella `Extra/`, e qui sotto c'è quando farle e quanto durano.

## Prima del corso

- Sui PC dell'aula: VS Code con le estensioni Python, Jupyter, Data Wrangler, GitHub Copilot; Ruff per l'aula Avanzata.
- uv installato; la cartella del corso scaricata e `uv sync` già fatto (vedi il README, "Come si parte").
- `Dati/fallback/` contiene risposte di esempio delle API: il corso funziona anche senza rete. Con la rete,
  `uv run python _build/scarica_fallback.py` le sostituisce con i dati veri (temperatura di Milano, sensori lombardi).
- I notebook si rigenerano dagli script in `_build/src/` con `uv run python _build/build.py`; le soluzioni si
  eseguono da capo a fondo con `uv run python _build/validate.py Soluzioni_Base/*.ipynb Soluzioni_Avanzata/*.ipynb`.
- I controlli degli esercizi (`verifica("7.1")`) stanno in `corso.py`, un file per cartella generato dal build a
  partire dagli assert scritti nei sorgenti: nel notebook il corsista vede solo la chiamata e una riga ✅ o ❌.

## Le dimostrazioni dal vivo

| Quando | Cosa mostrare | Materiale | Base | Avanzata |
|---|---|---|---|---|
| Giornata 1, apertura | VS Code: aprire la cartella, le estensioni, **Select Kernel** → `.venv`, eseguire una cella, Run All e Restart, le scorciatoie | `Extra/VS_Code_e_notebook.ipynb` | 15 min | 15 min |
| Giornata 1, dopo l'Esercitazione 2 | L'ambiente del progetto: `.venv`, `pyproject.toml`, `uv add`, `uv sync`; uno script `.py` lanciato con `uv run` | `Extra/Ambiente_uv_e_script.ipynb` | 5 min (solo l'idea) | 10 min |
| Giornata 1, nel 06 (A) | Il wrapper: chiudere la chiamata all'API in una funzione riutilizzabile | `Extra/API_wrapper.ipynb` | — | 10 min |
| Giornata 2, dopo il 07 | Data Wrangler: aprire un DataFrame, Editing mode, un filtro e una colonna tolta, il codice pandas che genera | `Extra/Data_Wrangler.ipynb` | 15 min | 15 min |

`Extra/Ruff.ipynb` resta a disposizione: si mostra solo se una classe Avanzata è avanti.

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

Sette ore nette per giornata sono 420 minuti: restano 60-80 minuti per i problemi di installazione, le domande e le
pause che si allungano. Si taglia a fine sezione, mai a metà.

## Se la classe è avanti

`Aula_*/Approfondimenti_1.ipynb` e `Approfondimenti_2.ipynb` raccolgono quello che è uscito dal percorso principale,
con i loro esercizi e le soluzioni in `Soluzioni_*/`: le operazioni con i set, il ciclo `while`, più file CSV e i
tipi di dato (giornata 1); le differenze tra date, il fuso orario, il range slider e l'export HTML (giornata 2); in
Avanzata anche `map`, `filter` e i generatori, `shift` e `rolling`, type hint, dataclass, decoratori e `**kwargs`.
Si aprono a fine giornata o quando un blocco finisce in anticipo; una sezione alla volta. Si possono anche lasciare
ai corsisti come lettura a casa.

## Il percorso minimo

Se la giornata va male (installazioni, rete, una classe lenta), questo è quello che non si salta:

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

Tra le due giornate, 40-45 minuti: `Aula_*/Homework.ipynb`, con le soluzioni in `Soluzioni_*/Homework.ipynb`.
Si presenta in cinque minuti a fine prima giornata e si corregge insieme all'inizio della seconda.
