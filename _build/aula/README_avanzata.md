# Corso Python, versione Avanzata

Questa cartella contiene il materiale del corso: i notebook dei quattro moduli con le esercitazioni, le soluzioni, i
dati e le schede di riepilogo, insieme ai file che descrivono l'ambiente Python del corso. La cartella funziona da
sola, quindi dopo l'installazione descritta qui sotto non serve nient'altro, e resta utilizzabile anche dopo il corso.

## Il contenuto della cartella

| Cartella o file | Che cosa contiene |
|---|---|
| `Modulo_1/` … `Modulo_4/` | i notebook di ciascun modulo, numerati da 00 a 11 nell'ordine in cui li seguiamo, e l'esercitazione che chiude i moduli 1, 2 e 3 |
| `Modulo_1/Script_uv_Ruff/` | il notebook *Ambiente, script e Ruff*, la cartella `demo/` con il progetto della dimostrazione, che puoi seguire sul tuo PC, e la cartella `esercizio/`, in cui si svolge l'Esercitazione 1 |
| `Soluzioni/` | gli stessi notebook con gli esercizi risolti, tutti nella stessa cartella; in `Soluzioni/Script_uv_Ruff/` ci sono i progetti della dimostrazione e dell'esercizio come sono alla fine |
| `Dati/` | i file di dati letti dai notebook, descritti in `Dati/README.md` |
| `Schede/` | tre schede di una pagina: leggere il codice, gli errori più comuni, da Excel a pandas |
| `pyproject.toml`, `uv.lock`, `.python-version` | la versione di Python e l'elenco delle librerie del corso, da cui uv costruisce l'ambiente |
| `.vscode/` | le impostazioni di VS Code per questa cartella |

L'Esercitazione 1 riguarda lo script della cartella `esercizio/`, e in fondo allo stesso notebook ci sono gli esercizi
sui notebook 00-03, da fare a casa. I notebook `Approfondimenti_1`, nella cartella `Modulo_2`, e `Approfondimenti_2`,
nella cartella `Modulo_4`, raccolgono argomenti che non rientrano nel percorso e si leggono quando si vuole andare
oltre. Il file `corso.py` nelle cartelle dei moduli e in `Soluzioni/` contiene i controlli degli esercizi e non va
modificato.

## Installazione e primo avvio

Le istruzioni sono per Windows. L'installazione si fa una volta sola e richiede la connessione a internet, perché uv
scarica Python e le librerie del corso.

1. Installa VS Code da <https://code.visualstudio.com> e, dal pannello **Extensions** (l'icona dei quattro
   quadratini nella barra a sinistra), le estensioni **Python** e **Jupyter** di Microsoft e l'estensione **Ruff** di
   Astral. Quando apri la cartella del corso, VS Code le propone comunque tra le estensioni consigliate.
2. Installa uv con il comando `winget install --id=astral-sh.uv -e` in un terminale PowerShell, poi chiudi e riapri
   VS Code, in modo che il comando `uv` venga riconosciuto. Se uv è già installato, `uv --version` ne stampa la
   versione e il passo si può saltare.
3. Estrai lo zip in una cartella con un percorso corto, per esempio `C:\Corso\`: con il tasto destro sullo zip scegli
   **Extract All...** e scrivi `C:\Corso` come destinazione. Conviene evitare le cartelle sincronizzate con OneDrive,
   come spesso sono il Desktop e i Documenti, perché ogni ambiente Python contiene migliaia di file. Alla fine esiste
   la cartella `C:\Corso\Aula_Avanzata`, che contiene il file `pyproject.toml`.
4. In VS Code scegli **File → Open Folder...** e apri la cartella `Aula_Avanzata`. Alla domanda *Do you trust the
   authors of the files in this folder?* rispondi **Yes, I trust the authors**, perché in modalità ristretta i
   notebook non si possono eseguire.
5. Apri il terminale con **Terminal → New Terminal**, che parte dalla cartella aperta, e lancia `uv sync`. Il comando
   crea la cartella `.venv`, cioè l'ambiente virtuale del corso, con Python e tutte le librerie nelle versioni indicate
   in `uv.lock`; la prima volta richiede qualche minuto.
6. Apri `Modulo_1/00_Notebook.ipynb`, premi **Select Kernel** in alto a destra e scegli la voce che contiene `.venv`;
   se non compare, la trovi in **Select Another Kernel... → Python Environments...**. La cella della sezione 5 del
   notebook stampa il percorso del Python in uso, che deve contenere `.venv`.

Nel modulo 4 si usa anche Copilot, l'assistente per il codice di VS Code, che richiede l'accesso con un account
abilitato.

## Come si usano i notebook

Ogni notebook si apre con il tempo previsto, i dati che utilizza e gli obiettivi. Negli Hands-on e negli esercizi il
codice da scrivere prende il posto dei `...`, e la cella sotto, con la chiamata `verifica("4.2")`, controlla il
risultato e stampa ✅ se è corretto, oppure una riga rossa che dice che cosa non torna. Nelle esercitazioni i blocchi
*Passo per passo* e *Suggerimento* si aprono con un clic, e la cella `soluzione("E1.3")` sotto ogni esercizio mostra
la soluzione di quell'esercizio e di nessun altro. La cartella `Soluzioni/` contiene fin dal primo giorno la versione
risolta di ogni notebook: conviene provare prima da soli e aprirla dopo, per confrontare.

I notebook leggono i dati con percorsi relativi come `../Dati/impianti_fv.csv`, in cui `..` indica la cartella sopra
quella del notebook, cioè `Aula_Avanzata`. Per questo un notebook funziona soltanto dalla cartella in cui si trova, e
un notebook nuovo creato per fare delle prove va messo in una delle cartelle `Modulo_1` … `Modulo_4`, dove gli stessi
percorsi funzionano. Quello che scrivi in un notebook resta nel file quando lo salvi con **Ctrl+S**. Se durante il
corso ricevi una versione aggiornata di alcuni moduli, copia dallo zip nuovo soltanto le cartelle indicate nel
messaggio che lo accompagna, perché le altre contengono il tuo lavoro.

Le cartelle `demo/` ed `esercizio/` sono progetti separati da quello del corso, ciascuno con il suo `pyproject.toml`
e, dopo il primo comando, il suo ambiente `.venv`. Gli script che contengono si lanciano sempre con `uv run main.py`
in un terminale aperto in quella cartella, che si ottiene con il tasto destro sulla cartella nel pannello Explorer e
la voce **Open in Integrated Terminal**.

## Se qualcosa non funziona

| Che cosa succede | Che cosa fare |
|---|---|
| Un notebook si ferma su un `import` con `ModuleNotFoundError: No module named 'pandas'` | Il kernel non è quello del corso. Premi **Select Kernel** e scegli la voce con `.venv`; se la voce manca, lancia `uv sync` nel terminale e riprova. |
| Il terminale risponde ``No `pyproject.toml` found in current directory or any parent directory`` | Il terminale non è nella cartella del corso. Apri `Aula_Avanzata` con **File → Open Folder...** e poi un terminale nuovo. |
| Nel pannello Explorer c'è solo una cartella `Aula_Avanzata` e manca `pyproject.toml` | Lo zip è stato estratto due volte, in `Aula_Avanzata\Aula_Avanzata`. Apri con **File → Open Folder...** la cartella interna. |
| PowerShell risponde che `uv` non è riconosciuto | VS Code era aperto durante l'installazione di uv. Chiudilo e riaprilo; se il messaggio resta, ripeti l'installazione. |
| `uv sync` si ferma con un errore che parla di certificati (`certificate`) | La rete aziendale controlla le connessioni sicure. Lancia `uv sync --system-certs`, che usa i certificati di Windows; nelle versioni meno recenti di uv l'opzione si chiama `--native-tls`. |
| Un notebook dà `FileNotFoundError` su un percorso `../Dati/...` | Il notebook è stato spostato fuori dalla sua cartella, oppure in VS Code è aperta una cartella diversa da `Aula_Avanzata`. |
| Nella cartella `demo` o `esercizio` lo script non si ferma sulle librerie mancanti, oppure il file Excel compare nella cartella principale | Lo script è stato lanciato con il pulsante **Run Python File**, che usa l'ambiente del corso. Lancialo con `uv run main.py` in un terminale aperto nella cartella dello script. |
| `uv run main.py` risponde con `error: Failed to spawn` | Il terminale non è nella cartella dello script. Aprilo con **Open in Integrated Terminal**, oppure, da un terminale aperto nella cartella del corso, entra nella cartella con `cd Modulo_1/Script_uv_Ruff/esercizio`. |
| `uv add` risponde senza elencare librerie installate, e lo script continua a fermarsi | Il comando ha lavorato sul progetto del corso, perché il terminale non era nella cartella dello script. Apri il terminale nella cartella giusta e ripeti il comando. |
| uv stampa un avviso che comincia con `warning:` e nomina `VIRTUAL_ENV` | L'avviso è innocuo, perché uv usa comunque l'ambiente della cartella. Per non vederlo più, lancia `deactivate` oppure apri un terminale nuovo. |
