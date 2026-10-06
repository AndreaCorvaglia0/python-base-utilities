# Python base per le utility

Corso di due giornate per chi lavora con i dati in una utility. Oggi il codice lo scrive spesso un agente:
Copilot in VS Code, Claude Code, Codex. Scrive in fretta e sbaglia con grande sicurezza, e il lavoro che resta
a noi è dire cosa vogliamo, leggere quello che torna, capire se è giusto e correggere la rotta. Per farlo bisogna
sapere come è fatto Python: in due giornate si scrive molto codice a mano, perché è il modo più rapido per
imparare a leggerlo.

Alla fine delle due giornate chi ha seguito il corso sa:

- aprire VS Code, un notebook e uno script e farli girare nell'ambiente giusto (uv, kernel, estensioni), aggiungere
  una libreria, importarla e usarne una funzione;
- dire cosa è cosa in una riga di codice: libreria, modulo, funzione, classe, oggetto, metodo, attributo, type hint, decoratore;
- distinguere la libreria standard dalle librerie installate, e sapere dove vivono (`.venv`, `pyproject.toml`);
- usare liste, dizionari, condizioni, cicli e funzioni, e leggere un traceback dal basso;
- leggere file, Excel, database e API con pandas, pulire e aggregare, lavorare con le date, fare grafici
  interattivi, controllare il codice con Ruff ed esplorare i dati con Data Wrangler;
- chiedere a un agente la cosa giusta con il contesto giusto, leggere quello che scrive e verificarlo con un
  numero che conosce.

Il materiale esiste in due versioni, una per aula, con lo stesso programma: **Aula Base** per chi parte
da zero, **Aula Avanzata** per chi ha già visto un po' di Python e vuole andare oltre.

## Come si parte

1. Installa [uv](https://docs.astral.sh/uv/): su Windows `winget install --id=astral-sh.uv -e`, su Mac `brew install uv`.
2. Scarica questo repository (pulsante **Code → Download ZIP**, oppure `git clone`) e apri la cartella in VS Code.
3. Nel terminale di VS Code: `uv sync`. Crea la cartella `.venv` con Python e tutte le librerie del corso.
4. Apri un notebook e premi **Select Kernel** in alto a destra: se c'è già una voce con `.venv` nel nome scegli quella, altrimenti **Select Another Kernel... → Python Environments...** e poi la `.venv`.
5. Esegui la prima cella del notebook `00_Si_parte`: se stampa un percorso che contiene `.venv`, sei a posto.

Serve una libreria in più? Nel terminale `uv add nome`, poi **Restart** del kernel. Le estensioni di VS Code
da avere: **Python**, **Jupyter**, **Data Wrangler**, **Ruff** e **GitHub Copilot**.

## La mappa del corso

| Giornata | Notebook | Aula Base | Aula Avanzata |
|---|---|---|---|
| 1 | `00_Si_parte` · perché Python nel 2026, VS Code, notebook e primo codice | 40 min | 30 min |
| 1 | `01_Librerie_e_ambiente` · librerie, uv, l'ambiente del progetto, script e notebook (Avanzata: `uv.lock`, `__main__`) | 35 min | 40 min |
| 1 | `02_Sintassi_di_base` · variabili, numeri, stringhe | 60 min | 40 min |
| 1 | `03_Strutture_dati` · liste, tuple, dizionari, set | 60 min | 40 min |
| 1 | `04_Codice_leggibile` · commenti, docstring, Markdown, PEP 8 | 30 min | 25 min |
| 1 | `05_Condizioni_cicli_funzioni` (Avanzata: comprehension, lambda, generatori) | 90 min | 95 min |
| 1 | `06_Oggetti_ed_errori` · chi è chi in una riga di codice, documentazione, traceback | 55 min | 40 min |
| 1 | `07_Pandas_import_dati` · DataFrame, CSV, Excel, SQL (Avanzata: API e wrapper) | 80 min | 120 min |
| tra le due | `Homework` · una settimana nell'ufficio Analisi Consumi | 40 min | 45 min |
| 2 | `08_Pandas_operazioni` · selezione, pulizia, groupby, merge, Data Wrangler | 135 min | 115 min |
| 2 | `09_Pandas_date` · date, indice temporale, resample, ora legale (Avanzata: shift, rolling) | 80 min | 90 min |
| 2 | `10_Plotly` · linee, istogrammi, scatter, slider, export HTML | 40 min | 30 min |
| 2 | `11_Agenti_per_il_coding` · Copilot in VS Code, contesto, Ruff, leggere il codice scritto da un agente, tre regole | 70 min | 70 min |
| 2 | `12_Capstone` · il carico del Nord e la temperatura | 120 min | 130 min |

Ogni notebook finisce con una sezione di esercizi di applicazione, quasi sempre due, con un'alternativa ("bis")
tra cui scegliere e, dove ha senso, un passo in più facoltativo. Le verifiche con ✅ e ❌ dicono subito se il risultato
torna. Le soluzioni di tutto stanno in `Soluzioni_Base/` e `Soluzioni_Avanzata/`.

## Cosa c'è nelle cartelle

| Cartella | Contenuto |
|---|---|
| `Aula_Base/`, `Aula_Avanzata/` | i notebook del corso, uno per argomento, più l'homework |
| `Soluzioni_Base/`, `Soluzioni_Avanzata/` | gli stessi notebook con gli esercizi risolti |
| `Dati/` | i dati usati nel corso: carico Terna, turbina eolica, prezzi, più i file di esempio (vedi `Dati/README.md`) |
| `Schede/` | quattro schede di una pagina: leggere il codice (cosa è cosa), Excel → pandas, uv e script, gli errori più comuni |
| `Slides/` | la presentazione del corso |
| `_build/` | gli script che generano i notebook e i dati di esempio (non servono per seguire il corso) |

Se in aula la rete non collabora, i notebook leggono le risposte delle API salvate in `Dati/fallback/`.

## Per chi tiene il corso

- `Dati/fallback/` contiene risposte di esempio delle API, con lo stesso schema di quelle vere: il corso funziona
  anche senza rete. Prima del corso, con la rete disponibile, `uv run python _build/scarica_fallback.py` le
  sostituisce con i dati veri (temperatura di Milano, sensori della Regione Lombardia).
- Estensioni di VS Code sui PC dell'aula, per tutte e due le aule: Python, Jupyter, Data Wrangler, Ruff, GitHub Copilot.
- Ogni notebook ha nel banner il tempo previsto; se si è in ritardo si taglia a fine sezione, mai a metà. La prima
  giornata dell'Aula Base è piena: si può tagliare, nel 01, la sezione "Script e notebook", fatta come dimostrazione
  dal docente (l'esercizio che la segue resta ai corsisti); nel 06 gli esercizi "bis"; nel 07 Base la sezione di ripasso. Nella seconda giornata: nel 08 il tour di
  Data Wrangler si può fare solo come dimostrazione; nel 09 Avanzata i fusi orari; nell'11 l'esercizio su Ruff, come dimostrazione.
- I notebook sono generati dagli script in `_build/src/`: per cambiare un testo o un esercizio in tutte e quattro
  le versioni, si modifica lo script e si lancia `uv run python _build/build.py NN`. Le Soluzioni si eseguono da
  capo a fondo con `uv run python _build/validate.py Soluzioni_Base/NN_*.ipynb` (serve la rete per le celle delle API).
  Modificare direttamente un `.ipynb` funziona, ma la modifica resta in quella sola versione.

## I riquadri nei notebook

Nei notebook incontrerai riquadri colorati: 💡 **Nota** (una precisazione utile adesso), ⚠️ **Attenzione**
(l'errore che succede davvero), 📘 **Approfondimento** (si può saltare), 📌 **Ricorda** (la regola da portare
a casa), ✏️ **Esercizio** e **Prova tu** (tocca a te), ✅ **Soluzione** (solo nelle cartelle delle soluzioni).
