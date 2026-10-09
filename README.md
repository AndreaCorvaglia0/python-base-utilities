# Python base per le utility

Questo repository contiene il materiale di un corso di due giornate su Python per chi lavora con i dati in una
società del settore energetico. Il corso parte dalle basi del linguaggio e arriva all'analisi di dati tabellari con
pandas, alla gestione delle date, ai grafici interattivi con Plotly e a un caso completo costruito sui dati di carico
elettrico pubblicati da Terna. Una parte del percorso è dedicata agli agenti per il coding, come Copilot in VS Code:
oggi molto codice viene scritto da strumenti di questo tipo, e per chiedere loro la cosa giusta e controllare quello
che restituiscono è necessario saper leggere il codice.

Il materiale esiste in due versioni con lo stesso programma. La versione **Base** è pensata per chi non ha mai
programmato, mentre la versione **Avanzata** si rivolge a chi ha già visto un po' di Python e aggiunge alcune sezioni
in più, come le list comprehension, la lettura di dati da API e le medie mobili.

## Installazione

Per seguire il corso servono VS Code, il gestore di ambienti uv e una copia di questa cartella. L'installazione
richiede pochi minuti.

1. Installare [uv](https://docs.astral.sh/uv/). Su Windows il comando è `winget install --id=astral-sh.uv -e`, su
   Mac `brew install uv`.
2. Scaricare il repository, con il pulsante **Code → Download ZIP** oppure con `git clone`, e aprire la cartella in
   VS Code.
3. Eseguire `uv sync` nel terminale di VS Code. Il comando crea la cartella `.venv` con l'interprete Python e tutte le
   librerie usate nel corso, nelle versioni indicate dal progetto.
4. Aprire un notebook e scegliere il kernel con il pulsante **Select Kernel**, in alto a destra. Se nell'elenco compare
   già una voce con `.venv` nel nome è quella giusta; altrimenti si passa da **Select Another Kernel... → Python
   Environments...** e si sceglie la `.venv` appena creata.
5. Eseguire la prima cella di codice del notebook `00_Notebook`. Se stampa un percorso che contiene `.venv`,
   l'ambiente è configurato correttamente.

Se durante il corso serve una libreria che non è nel progetto, si aggiunge con `uv add nome` dal terminale e poi si
riavvia il kernel con **Restart**. Le estensioni di VS Code necessarie sono **Python** e **Jupyter**; in aula si usano
anche **Data Wrangler** e **GitHub Copilot**, e nella versione Avanzata **Ruff**.

## Il programma

La tabella elenca i notebook nell'ordine in cui si svolgono, con il tempo previsto per ciascuna versione.

| Giornata | Notebook | Aula Base | Aula Avanzata |
|---|---|---|---|
| 1 | `00_Notebook` · Jupyter e i notebook | 20 min | 20 min |
| 1 | `01_Python_e_sintassi_base` · variabili, numeri, stringhe, import | 45 min | 35 min |
| 1 | `02_Tipi_di_dato` · liste, tuple, dizionari, set | 40 min | 35 min |
| 1 | `03_Codice_leggibile` · commenti, Markdown, docstring, PEP 8 | 20 min | 20 min |
| 1 | `Esercitazione_1` | 20 min | 20 min |
| 1 | `04_Funzioni_e_controllo` · if, for, funzioni (Avanzata: lambda, list comprehension) | 55 min | 60 min |
| 1 | `05_Oggetti_ed_errori` · oggetti, metodi, documentazione, traceback | 40 min | 35 min |
| 1 | `06_Pandas_e_import_dati` · Series, DataFrame, CSV, Excel, SQL (Avanzata: API) | 55 min | 75 min |
| 1 | `Esercitazione_2` | 20 min | 20 min |
| tra le due | `Homework` · una settimana nell'ufficio Analisi Consumi | 40 min | 45 min |
| 2 | `07_Pandas_operazioni` · selezione, valori mancanti, groupby, merge | 70 min | 75 min |
| 2 | `08_Pandas_date` · date, indice temporale, resample, ora legale | 55 min | 55 min |
| 2 | `09_Plotly` · linee, confronto tra serie, istogrammi | 30 min | 25 min |
| 2 | `Esercitazione_3` | 20 min | 20 min |
| 2 | `10_Agenti_per_il_coding` · Copilot in VS Code, leggere il codice scritto da un agente | 45 min | 45 min |
| 2 | `11_Capstone` · il carico del Nord e la temperatura | 110 min | 110 min |
| se c'è tempo | `Approfondimenti_1` · set, while, più file CSV (Avanzata: map, filter, generatori) | 40 min | 55 min |
| se c'è tempo | `Approfondimenti_2` · differenze tra date, fuso orario, slider, export HTML (Avanzata: shift, rolling, type hint, dataclass, decoratori) | 40 min | 60 min |

Ogni notebook si chiude con due o tre esercizi, a volte con un quarto segnato come facoltativo, che si svolge se resta
tempo oppure a casa. Le tre Esercitazioni chiudono i blocchi del programma con alcune domande e qualche esercizio in
più, mentre i due Approfondimenti raccolgono il materiale che resta fuori dal percorso principale e si aprono solo
quando la classe è in anticipo. Sotto ogni esercizio si trova una cella con la chiamata `verifica("7.1")`, che
controlla il risultato e stampa ✅ se è corretto, oppure una riga che indica che cosa non torna. Le soluzioni di tutti
gli esercizi sono nelle cartelle `Soluzioni_Base/` e `Soluzioni_Avanzata/`.

## Il contenuto delle cartelle

| Cartella | Contenuto |
|---|---|
| `Aula_Base/`, `Aula_Avanzata/` | i notebook del corso, le tre Esercitazioni, l'Homework e i due Approfondimenti; `corso.py` è il modulo con i controlli degli esercizi |
| `Soluzioni_Base/`, `Soluzioni_Avanzata/` | gli stessi notebook con gli esercizi risolti |
| `Extra/` | le parti che il docente mostra dal vivo: VS Code, ambiente e script, Ruff, Data Wrangler, wrapper delle API |
| `Dati/` | i dati usati nel corso: carico Terna, turbina eolica, prezzi, più i file di esempio (vedi `Dati/README.md`) |
| `Schede/` | quattro schede di una pagina: leggere il codice, Excel → pandas, uv e script, gli errori più comuni; i notebook 01, 05, 06 e 07 rimandano alla loro |
| `Slides/` | la presentazione del corso |
| `_build/` | gli script che generano i notebook e i dati di esempio (non servono per seguire il corso) |

Il file `Guida_docente.md` indica quando svolgere le dimostrazioni dal vivo, riporta i tempi delle due giornate e
suggerisce dove tagliare se si è in ritardo.

## Come sono fatti i notebook

Ogni notebook si apre con il tempo previsto, i dati che utilizza e tre obiettivi di apprendimento, e si chiude con i
collegamenti al notebook precedente e al successivo. Nel testo, le note e gli approfondimenti compaiono come
citazioni rientrate, e gli approfondimenti si possono saltare senza perdere il filo. I riquadri colorati sono tre: il
riquadro verde segnala un **Esercizio** o un **Prova tu**, cioè un momento in cui si scrive codice; il riquadro
azzurro contiene la **Soluzione** e compare solo nelle cartelle delle soluzioni; il riquadro rosso, **Attenzione**,
segnala un errore che capita spesso.
