# Python base per le utility

Corso di due giornate per chi lavora con i dati in una utility. Oggi molto codice lo scrive un agente, come Copilot in
VS Code: per chiedergli la cosa giusta e controllare quello che torna bisogna saper leggere il codice. Il corso parte dalle
basi di Python e arriva a pandas, alle date, ai grafici con Plotly e a un caso completo sui dati di carico di Terna.

Il materiale esiste in due versioni, una per aula, con lo stesso programma: **Aula Base** per chi parte da zero,
**Aula Avanzata** per chi ha già visto un po' di Python e vuole andare oltre.

## Come si parte

1. Installa [uv](https://docs.astral.sh/uv/): su Windows `winget install --id=astral-sh.uv -e`, su Mac `brew install uv`.
2. Scarica questo repository (pulsante **Code → Download ZIP**, oppure `git clone`) e apri la cartella in VS Code.
3. Nel terminale di VS Code: `uv sync`. Crea la cartella `.venv` con Python e tutte le librerie del corso.
4. Apri un notebook e premi **Select Kernel** in alto a destra: se c'è già una voce con `.venv` nel nome scegli quella,
   altrimenti **Select Another Kernel... → Python Environments...** e poi la `.venv`.
5. Esegui la prima cella di codice del notebook `00_Notebook`: se stampa un percorso che contiene `.venv`, sei a posto.

Serve una libreria in più? Nel terminale `uv add nome`, poi **Restart** del kernel. Le estensioni di VS Code da avere:
**Python** e **Jupyter**; in aula si usano anche **Data Wrangler**, **GitHub Copilot** e, per l'aula Avanzata, **Ruff**.

## La mappa del corso

| Giornata | Notebook | Aula Base | Aula Avanzata |
|---|---|---|---|
| 1 | `00_Notebook` · Jupyter e i notebook | 20 min | 20 min |
| 1 | `01_Python_e_sintassi_base` · variabili, numeri, stringhe, import | 45 min | 35 min |
| 1 | `02_Tipi_di_dato` · liste, tuple, dizionari, set | 50 min | 40 min |
| 1 | `03_Codice_leggibile` · commenti, Markdown, docstring, PEP 8 | 20 min | 20 min |
| 1 | `Esercitazione_1` | 30 min | 25 min |
| 1 | `04_Funzioni_e_controllo` · if, for, while, funzioni (Avanzata: lambda, comprehension, generatori) | 70 min | 80 min |
| 1 | `05_Oggetti_ed_errori` · oggetti, metodi, documentazione, traceback | 40 min | 35 min |
| 1 | `06_Pandas_e_import_dati` · Series, DataFrame, CSV, Excel, SQL (Avanzata: API) | 70 min | 90 min |
| 1 | `Esercitazione_2` | 30 min | 30 min |
| tra le due | `Homework` · una settimana nell'ufficio Analisi Consumi | 40 min | 45 min |
| 2 | `07_Pandas_operazioni` · selezione, valori mancanti, groupby, merge | 90 min | 80 min |
| 2 | `08_Pandas_date` · date, indice temporale, resample, ora legale (Avanzata: shift, rolling) | 70 min | 80 min |
| 2 | `09_Plotly` · linee, confronto tra serie, slider, istogrammi, export HTML | 40 min | 35 min |
| 2 | `Esercitazione_3` | 30 min | 30 min |
| 2 | `10_Agenti_per_il_coding` · Copilot in VS Code, leggere il codice scritto da un agente | 45 min | 55 min |
| 2 | `11_Capstone` · il carico del Nord e la temperatura | 110 min | 110 min |

Ogni notebook finisce con due o tre esercizi, a volte un quarto facoltativo; quelli segnati **(facoltativo)** si fanno se c'è tempo o a casa. Le tre
Esercitazioni chiudono i blocchi con qualche domanda e un po' di esercizi in più. Sotto ogni esercizio c'è una cella
`verifica("7.1")` che controlla il risultato: stampa ✅ se è giusto, altrimenti una riga che dice cosa non torna. Le
soluzioni stanno in `Soluzioni_Base/` e `Soluzioni_Avanzata/`.

## Cosa c'è nelle cartelle

| Cartella | Contenuto |
|---|---|
| `Aula_Base/`, `Aula_Avanzata/` | i notebook del corso, le tre Esercitazioni e l'Homework; `corso.py` è il modulo con i controlli degli esercizi |
| `Soluzioni_Base/`, `Soluzioni_Avanzata/` | gli stessi notebook con gli esercizi risolti |
| `Extra/` | le parti che il docente mostra dal vivo: VS Code, ambiente e script, Ruff, Data Wrangler, wrapper delle API |
| `Dati/` | i dati usati nel corso: carico Terna, turbina eolica, prezzi, più i file di esempio (vedi `Dati/README.md`) |
| `Schede/` | quattro schede di una pagina: leggere il codice, Excel → pandas, uv e script, gli errori più comuni |
| `Slides/` | la presentazione del corso |
| `_build/` | gli script che generano i notebook e i dati di esempio (non servono per seguire il corso) |

`Guida_docente.md` dice quando fare le dimostrazioni dal vivo, i tempi delle due giornate e dove tagliare.

## I riquadri nei notebook

Nei notebook incontrerai riquadri colorati: 💡 **Nota** (una precisazione), ⚠️ **Attenzione** (un errore che capita),
📘 **Approfondimento** (si può saltare), ✏️ **Esercizio** e **Prova tu** (tocca a te), ✅ **Soluzione** (solo nelle
cartelle delle soluzioni).
