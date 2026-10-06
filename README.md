# Python base per le utility

Corso di due giornate per chi lavora con i dati in una utility e vuole smettere di farlo a mano:
leggere file, Excel, database e API con pandas, pulire e aggregare, lavorare con le date, fare grafici
interattivi, e usare gli agenti per il coding senza fidarsi alla cieca.

Il materiale esiste in due versioni, una per aula, con lo stesso programma: **Aula Base** per chi parte
da zero, **Aula Avanzata** per chi ha già visto un po' di Python e vuole andare oltre.

## Come si parte

1. Installa [uv](https://docs.astral.sh/uv/): su Windows `winget install astral-sh.uv`, su Mac `brew install uv`.
2. Scarica questo repository (pulsante **Code → Download ZIP**, oppure `git clone`) e apri la cartella in VS Code.
3. Nel terminale di VS Code: `uv sync`. Crea la cartella `.venv` con Python e tutte le librerie del corso.
4. Apri un notebook, premi **Select Kernel** in alto a destra e scegli l'interprete dentro `.venv`.
5. Esegui la prima cella del notebook `00_Si_parte`: se stampa un percorso che contiene `.venv`, sei a posto.

Serve una libreria in più? Nel terminale `uv add nome`, poi **Restart** del kernel. Le estensioni di VS Code
da avere: **Python**, **Jupyter** e, per chi vuole, **Data Wrangler** e **Ruff**.

## La mappa del corso

| Giornata | Notebook | Aula Base | Aula Avanzata |
|---|---|---|---|
| 1 | `00_Si_parte` · VS Code, notebook e primo codice | 40 min | 30 min |
| 1 | `01_Librerie_e_ambiente` · librerie e uv (Avanzata: ambienti, script vs notebook) | 20 min | 40 min |
| 1 | `02_Sintassi_di_base` · variabili, numeri, stringhe | 60 min | 40 min |
| 1 | `03_Strutture_dati` · liste, tuple, dizionari, set | 60 min | 40 min |
| 1 | `04_Codice_leggibile` · commenti, docstring, PEP 8 (Avanzata: Ruff) | 20 min | 30 min |
| 1 | `05_Condizioni_cicli_funzioni` (Avanzata: comprehension, lambda, generatori) | 90 min | 95 min |
| 1 | `06_Oggetti_ed_errori` · leggere il codice e i traceback | 40 min | 30 min |
| 1 | `07_Pandas_import_dati` · DataFrame, CSV, Excel, SQL (Avanzata: API e wrapper) | 80 min | 120 min |
| tra le due | `Compito_a_casa` · una settimana nell'ufficio Analisi Consumi | 30-45 min | 30-45 min |
| 2 | `08_Pandas_operazioni` · selezione, pulizia, groupby, merge, Data Wrangler | 135 min | 115 min |
| 2 | `09_Pandas_date` · date, indice temporale, ora legale (Avanzata: resample, rolling) | 70 min | 90 min |
| 2 | `10_Plotly` · linee, istogrammi, scatter, slider, export HTML | 40 min | 30 min |
| 2 | `11_Agenti_per_il_coding` · Copilot in VS Code, token, contesto, tre regole | 40 min | 40 min |
| 2 | `12_Capstone` · il carico del Nord e la temperatura | 120 min | 130 min |

Ogni notebook finisce con una sezione di esercizi: due esercizi di applicazione, ciascuno con un'alternativa
("bis") e, dove ha senso, un passo in più facoltativo. Le verifiche con ✅ e ❌ dicono subito se il risultato
torna. Le soluzioni di tutto stanno in `Soluzioni_Base/` e `Soluzioni_Avanzata/`.

## Cosa c'è nelle cartelle

| Cartella | Contenuto |
|---|---|
| `Aula_Base/`, `Aula_Avanzata/` | i notebook del corso, uno per argomento, più il compito a casa |
| `Soluzioni_Base/`, `Soluzioni_Avanzata/` | gli stessi notebook con gli esercizi risolti |
| `Dati/` | i dati usati nel corso: carico Terna, turbina eolica, prezzi, più i file di esempio (vedi `Dati/README.md`) |
| `Schede/` | tre schede di una pagina: Excel → pandas, uv e script, gli errori più comuni |
| `Slides/` | la presentazione del corso |
| `_build/` | gli script che generano i notebook e i dati di esempio (non servono per seguire il corso) |

Prima del corso, con la rete disponibile, `uv run python _build/scarica_fallback.py` salva in `Dati/fallback/`
le risposte delle API usate nei notebook: se in aula la rete non collabora, i notebook leggono quelle.

## Per chi tiene il corso

- Prima del corso, con la rete disponibile: `uv run python _build/scarica_fallback.py` (salva le risposte delle API in
  `Dati/fallback/`; senza questi file le celle di fallback del notebook 07 e del capstone restano vuote).
- Estensioni di VS Code sui PC dell'aula: Python, Jupyter, Data Wrangler, GitHub Copilot (e Ruff per l'aula Avanzata).
- Ogni notebook ha nel banner il tempo previsto; se si è in ritardo si taglia a fine sezione, mai a metà. I punti
  dove tagliare senza perdere il filo: nel 06 gli esercizi "bis"; nel 07 Base la sezione di ripasso; nel 08 il
  tour di Data Wrangler (si può fare solo come dimostrazione); nel 09 i fusi orari.
- I notebook sono generati dagli script in `_build/src/`: per cambiare un testo o un esercizio in tutte e quattro
  le versioni, si modifica lo script e si lancia `uv run python _build/build.py NN`. Le Soluzioni si eseguono da
  capo a fondo con `uv run python _build/validate.py Soluzioni_Base/NN_*.ipynb` (serve la rete per le celle delle API).
  Modificare direttamente un `.ipynb` funziona, ma la modifica resta in quella sola versione.

## I riquadri nei notebook

Nei notebook incontrerai riquadri colorati: 💡 **Nota** (una precisazione utile adesso), ⚠️ **Attenzione**
(l'errore che succede davvero), 📘 **Approfondimento** (si può saltare), 📌 **Ricorda** (la regola da portare
a casa), ✏️ **Esercizio** e **Prova tu** (tocca a te), ✅ **Soluzione** (solo nelle cartelle delle soluzioni).
