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
| Giornata 1, dopo l'Esercitazione 2 | L'ambiente del progetto: `.venv`, `pyproject.toml`, `uv add`, `uv sync`; uno script `.py` lanciato con `uv run` | `Extra/Ambiente_uv_e_script.ipynb` | 5 min (solo l'idea) | 15 min |
| Giornata 1, dopo il 03 | Ruff: `uv run ruff check` e `format`, l'estensione, i tre codici che si vedono più spesso | `Extra/Ruff.ipynb` | — | 10 min |
| Giornata 1, nel 06 (A) | Il wrapper: chiudere la chiamata all'API in una funzione riutilizzabile | `Extra/API_wrapper.ipynb` | — | 10 min |
| Giornata 2, dopo il 07 | Data Wrangler: aprire un DataFrame, Editing mode, un filtro e una colonna tolta, il codice pandas che genera | `Extra/Data_Wrangler.ipynb` | 15 min | 15 min |

## I tempi (minuti netti)

Giornata 1 (Blocchi 1 e 2)

| | Base | Avanzata |
|---|---|---|
| Demo VS Code | 15 | 15 |
| 00 Jupyter e i notebook | 20 | 20 |
| 01 Introduzione a Python e sintassi base | 45 | 35 |
| 02 Tipi di dato e manipolazione | 50 | 40 |
| 03 Codice leggibile | 20 | 20 |
| Demo Ruff | — | 10 |
| Esercitazione 1 | 30 | 25 |
| 04 Funzioni e controllo del flusso | 70 | 80 |
| 05 Oggetti ed errori | 40 | 35 |
| 06 Pandas: Series, DataFrame e import dei dati (+ demo wrapper in Avanzata) | 70 | 90 + 10 |
| Esercitazione 2 | 30 | 30 |
| Demo ambiente e script | 5 | 15 |
| Presentazione dell'Homework | 5 | 5 |
| **Totale** | **400** | **430** |

Giornata 2 (Blocchi 3 e 4)

| | Base | Avanzata |
|---|---|---|
| Correzione dell'Homework | 15 | 15 |
| 07 Pandas: operazioni sui DataFrame | 90 | 80 |
| Demo Data Wrangler | 15 | 15 |
| 08 Pandas: le date | 70 | 80 |
| 09 Plotly per serie storiche | 40 | 35 |
| Esercitazione 3 | 30 | 30 |
| 10 Agenti per il coding | 45 | 55 |
| 11 Capstone | 110 | 110 |
| **Totale** | **415** | **420** |

Sette ore nette per giornata sono 420 minuti: le giornate sono piene, e la prima giornata dell'Avanzata va oltre di dieci minuti. Si taglia a fine sezione, mai a metà.

## Dove tagliare se si è in ritardo

- Gli esercizi segnati **(facoltativo)**: si lasciano ai corsisti, da fare a casa.
- Esercitazione 1 e 2: le domande si fanno a voce, gli esercizi si riducono a due.
- 04: in Base la sezione su `while` si fa come dimostrazione; in Avanzata `map` e `filter` si citano e basta.
- 06 Avanzata: l'esercizio facoltativo sulle API si salta; la demo del wrapper si accorcia a 5 minuti.
- 08: differenze tra date e fuso orario si fanno come dimostrazione, lasciando i duplicati dell'ora legale, che servono al capstone.
- 10: la prova guidata si fa con un prompt solo.
- Capstone: gli step 1-4 sono il minimo; 5 e 6 si possono fare insieme sullo schermo del docente.

## Homework

Tra le due giornate, 40-45 minuti: `Aula_*/Homework.ipynb`, con le soluzioni in `Soluzioni_*/Homework.ipynb`.
Si presenta in cinque minuti a fine prima giornata e si corregge insieme all'inizio della seconda.
