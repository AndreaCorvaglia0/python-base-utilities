# Python base per le utility

Questo repository contiene il materiale di un corso su Python in quattro moduli di quattro ore, per chi lavora con i
dati in una società del settore energetico. Il corso parte dalle basi del linguaggio e arriva all'analisi di dati
tabellari con pandas, alla gestione delle date, ai grafici interattivi con Plotly e a un caso completo costruito sui
dati di carico elettrico pubblicati da Terna. Una parte del percorso è dedicata agli agenti per il coding, come Copilot
in VS Code: oggi molto codice viene scritto da strumenti di questo tipo, e per chiedere loro la cosa giusta e
controllare quello che restituiscono è necessario saper leggere il codice.

Il materiale esiste in due versioni con lo stesso programma. La versione **Base** è pensata per chi non ha mai
programmato, mentre la versione **Avanzata** si rivolge a chi ha già visto un po' di Python e aggiunge alcune parti in
più, come l'ambiente del progetto, gli script e Ruff nel modulo 1, le list comprehension, la lettura di dati da API e
le medie mobili. Il README è scritto per chi tiene e mantiene il corso; i corsisti non ricevono il repository, ma solo
la cartella della loro aula.

## Le cartelle dei corsisti

Ogni corsista riceve la cartella della sua aula, `Aula_Base/` o `Aula_Avanzata/`, come file zip. La cartella funziona
da sola: contiene i notebook dei quattro moduli, le soluzioni, i dati, le schede, il progetto uv `corso-python`, uguale
per le due aule, e le impostazioni di VS Code. Il suo `README.md`, generato da `_build/aula/README_base.md` e
`_build/aula/README_avanzata.md`, spiega al corsista come installare VS Code e uv, dove estrarre lo zip, come lanciare
`uv sync` e scegliere il kernel, e come risolvere i problemi più comuni. Le due cartelle sono generate dal build e non
si modificano a mano; gli zip si preparano con un comando che ricostruisce prima tutto il corso:

    uv run python _build/esporta.py                      # dist/Aula_Base.zip e dist/Aula_Avanzata.zip
    uv run python _build/esporta.py base                 # una sola aula
    uv run python _build/esporta.py --moduli 3 4         # aggiornamento dei soli moduli 3 e 4
    uv run python _build/esporta.py avanzata --riserva   # il materiale di riserva di un'aula

Nello zip entrano soltanto i file che Git conosce o non ignora, quindi restano fuori `.venv`, le cache e i file
prodotti eseguendo notebook e script; un file nuovo che Git non ignora entrerebbe invece nello zip, e `esporta.py` lo
segnala con un avviso. Lo zip di aggiornamento contiene soltanto `Modulo_3`, `Modulo_4`, le loro soluzioni con
`Soluzioni/corso.py`, `Dati/` e `Schede/`, così non tocca i notebook dei moduli 1 e 2, in cui i corsisti hanno già
scritto; la `Guida_docente.md` descrive come mandarlo.

La cartella dell'Avanzata, che è la più completa, è fatta così:

```
Aula_Avanzata/
    README.md                                  le istruzioni per il corsista
    pyproject.toml  uv.lock  .python-version   il progetto uv "corso-python"
    .vscode/                                   impostazioni ed estensioni consigliate
    Dati/  Schede/                             i dati usati dai notebook e le tre schede
    Modulo_1/ … Modulo_4/                      i notebook del percorso, con il loro corso.py
        Modulo_1/Script_uv_Ruff/               Ambiente_script_e_Ruff, demo/ ed esercizio/
    Soluzioni/                                 la versione risolta di ogni notebook, con il suo corso.py
        Soluzioni/Script_uv_Ruff/              demo/ ed esercizio/ come sono alla fine
```

I notebook sono distribuiti nei moduli come nella tabella seguente, con una numerazione da 00 a 11 unica per tutto il
corso.

| Cartella | Aula Base | Aula Avanzata |
|---|---|---|
| `Modulo_1` | 00, 01, 02, 03, Esercitazione_1 | gli stessi, più `Script_uv_Ruff/` |
| `Modulo_2` | 04, 05, 06, Esercitazione_2, Approfondimenti_1 | gli stessi |
| `Modulo_3` | 07, 08, Esercitazione_3, Approfondimenti_2 | 07, 08, Esercitazione_3 |
| `Modulo_4` | 09, 10, 11 | 09, 10, 11, Approfondimenti_2 |

## Il programma

Il corso si svolge in quattro moduli di quattro ore, il 20 e 21 ottobre e il 27 e 28 ottobre 2026. In ogni giornata
l'aula Base fa il modulo nelle prime quattro ore e l'aula Avanzata lo stesso modulo nelle quattro successive. I primi
tre moduli si chiudono con un'ora di esercitazione, il quarto è dedicato agli agenti per il coding e al progetto
finale. La tabella elenca i notebook nell'ordine in cui si svolgono, con il tempo previsto per ciascuna versione; le
sezioni Extra in fondo ai notebook non sono comprese nei tempi, e le dimostrazioni dal vivo, che non sono notebook dei
corsisti, sono nelle tabelle della `Guida_docente.md`.

| Modulo | Notebook | Aula Base | Aula Avanzata |
|---|---|---|---|
| 1 | `00_Notebook` · celle, esecuzione, variabili, Restart e Run All in VS Code | 25 min | 20 min |
| 1 | `01_Python_e_sintassi_base` · variabili, numeri, stringhe, import | 40 min | 30 min |
| 1 | `02_Tipi_di_dato` · liste, tuple, dizionari, set | 40 min | 35 min |
| 1 | `03_Codice_leggibile` · commenti, Markdown, docstring, PEP 8 | 20 min | 20 min |
| 1 | `Ambiente_script_e_Ruff` · uv e `.venv`, i file del progetto, notebook e script, import da un file, Ruff, con la dimostrazione dal vivo | no | 30 min |
| 1 | `Esercitazione_1` · Base: esercizi sui notebook 00-03; Avanzata: la dimostrazione ripetuta nella cartella `esercizio/`, con gli esercizi sui notebook 00-03 facoltativi, a casa | 60 min | 60 min |
| 2 | `04_Funzioni_e_controllo` · if, for, funzioni (Avanzata: lambda, list comprehension) | 50 min | 50 min |
| 2 | `05_Oggetti_ed_errori` · oggetti, metodi, documentazione, traceback | 35 min | 30 min |
| 2 | `06_Pandas_e_import_dati` · Series, DataFrame, CSV, Excel, SQL (Avanzata: API) | 55 min | 70 min |
| 2 | `Esercitazione_2` | 60 min | 60 min |
| 3 | `07_Pandas_operazioni` · selezione, valori mancanti, groupby, merge | 65 min | 70 min |
| 3 | `08_Pandas_date` · date, indice temporale, resample, ora legale | 50 min | 50 min |
| 3 | `Esercitazione_3` | 60 min | 60 min |
| 4 | `09_Plotly` · un grafico a linee, confronto tra serie, export HTML | 25 min | 25 min |
| 4 | `10_Agenti_per_il_coding` · Copilot in VS Code, leggere il codice scritto da un agente | 35 min | 35 min |
| 4 | `11_Capstone` · il carico del Nord e la temperatura, con lo step finale di richieste libere a Copilot | 150 min | 150 min |
| se c'è tempo | `Approfondimenti_1` · set, while, più file CSV (Avanzata: map, filter, generatori) | 40 min | 55 min |
| se c'è tempo | `Approfondimenti_2` · differenze tra date, fuso orario (Avanzata: shift, rolling, type hint, dataclass, decoratori, generatori, `**kwargs`) | 20 min | 40 min |

Nei notebook numerati da 00 a 10, subito dopo gli esempi, ci sono alcuni Hands-on: piccoli esercizi da uno a tre
minuti in cui si cambia qualcosa nel codice appena visto. In fondo agli stessi notebook una sezione Extra raccoglie due
o tre esercizi brevi da fare a casa, che in aula si saltano. Il capstone, che procede a passi guidati, e
`Ambiente_script_e_Ruff`, la cui pratica è l'Esercitazione 1 dell'Avanzata, non hanno né Hands-on né Extra. Le tre
Esercitazioni chiudono i primi tre moduli con un'ora di lavoro strutturato, con domande di riepilogo, cinque o sei
esercizi con suggerimenti nascosti e la soluzione di ogni esercizio a richiesta; nell'Avanzata l'Esercitazione 1 è
invece l'esercizio guidato sullo script nella cartella `esercizio/`. I due Approfondimenti raccolgono il materiale che
resta fuori dal percorso principale e si aprono solo quando la classe è in anticipo. Sotto ogni esercizio si trova una
cella con la chiamata `verifica("7.1")`, che controlla il risultato e stampa ✅ se è corretto, oppure una riga che
indica che cosa non torna. Le soluzioni di tutti gli esercizi sono nella cartella `Soluzioni/` di ogni aula, a
disposizione dei corsisti fin dal primo giorno.

## Il materiale del docente

Quello che serve soltanto al docente resta nel repository e non va ai corsisti. La `Guida_docente.md` riporta i tempi
dei quattro moduli, indica quando svolgere le dimostrazioni dal vivo, descrive come distribuire gli zip e gli
aggiornamenti e che cosa raccontare nella parte su uv, script e Ruff dell'Avanzata, con la dimostrazione passo per passo
e l'ora di esercitazione, e suggerisce dove tagliare se si è in ritardo.

| Cartella | Contenuto |
|---|---|
| `Aula_Base/`, `Aula_Avanzata/` | le cartelle dei corsisti, generate dal build |
| `Extra/` | i notebook delle dimostrazioni dal vivo: VS Code e notebook, Data Wrangler, wrapper delle API |
| `Riserva/` | l'Homework per le due aule e, per l'Avanzata, gli esercizi su uv, script e Ruff, per una classe molto veloce |
| `Dati/` | gli originali dei dati del corso (vedi `Dati/README.md`), copiati nelle aule a ogni build |
| `Schede/` | gli originali delle tre schede: leggere il codice, gli errori più comuni, da Excel a pandas |
| `Slides/` | la presentazione del corso |
| `_build/` | gli script che generano il materiale: in `src/` i sorgenti dei notebook e le cartelle della dimostrazione su uv e Ruff, in `aula/` il progetto uv e i README dei corsisti, in `docs/` le regole di scrittura |
| `dist/` | gli zip per i corsisti, prodotti da `_build/esporta.py` e non versionati |

## Ricostruire e controllare il materiale

Per lavorare sul repository serve uv. Il comando `uv sync` nella radice crea l'ambiente del repository, che oltre alle
librerie del corso contiene gli strumenti per eseguire e validare i notebook ed è distinto dal progetto dei corsisti
in `_build/aula/`. I notebook di `Extra/` e di `Riserva/` si aprono con questo ambiente. I comandi principali sono
questi:

    uv run python _build/controlla.py 07 E2      # build, soluzioni eseguite e Run All studente dei notebook indicati
    uv run python _build/controlla.py            # tutto il corso
    uv run python _build/leggi.py Aula_Base/Modulo_3/07_Pandas_operazioni.ipynb   # rilettura cella per cella
    uv run python _build/esporta.py              # gli zip per i corsisti

`controlla.py` deve chiudersi con zero errori e zero avvisi. A ogni giro controlla anche che le copie nelle aule
coincidano con gli originali, che il `uv.lock` dei corsisti sia aggiornato e che Ruff dia sugli script della
dimostrazione e dell'esercizio esattamente le segnalazioni previste. Le regole di scrittura del materiale stanno in
`_build/docs/`, e `CLAUDE.md` riassume il ciclo di lavoro.

## Come sono fatti i notebook

Ogni notebook si apre con il tempo previsto, i dati che utilizza e tre obiettivi di apprendimento, e si chiude con i
collegamenti al notebook precedente e al successivo. Nel testo, le note e gli approfondimenti compaiono come
citazioni rientrate, e gli approfondimenti si possono saltare senza perdere il filo. I riquadri colorati sono tre: il
riquadro verde segnala un **Esercizio** o un **Hands-on**, cioè un momento in cui si scrive codice; il riquadro
azzurro contiene la **Soluzione** e compare solo nella cartella `Soluzioni/`; il riquadro rosso, **Attenzione**,
segnala un errore che capita spesso.
