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

1. Installa VS Code da <https://code.visualstudio.com> e, dal pannello **Extensions**, che si apre con l'icona dei
   quattro quadratini nella barra a sinistra, le estensioni **Python** e **Jupyter** di Microsoft e l'estensione
   **Ruff** di Astral. Quando apri la cartella del corso, VS Code le propone comunque tra le estensioni consigliate.
2. Apri PowerShell dal menu Start, cercando *PowerShell*, e lancia `uv --version`: se compare un numero di versione,
   uv è già installato e il passo finisce qui. Altrimenti installa uv con il comando
   `winget install --id=astral-sh.uv -e`; alla prima esecuzione winget può chiedere di accettare i termini delle
   sorgenti, e in quel caso rispondi `Y`. Al termine chiudi PowerShell e, se è aperto, VS Code, perché le finestre
   aperte prima dell'installazione non vedono il comando `uv`; in una finestra nuova `uv --version` stampa la versione.
3. Estrai lo zip in una cartella con un percorso corto, per esempio `C:\Corso\`: con il tasto destro sullo zip scegli
   **Estrai tutto...** (*Extract All...* in Windows in inglese) e scrivi `C:\Corso` come destinazione. Conviene
   evitare le cartelle sincronizzate con OneDrive, come spesso sono il Desktop e i Documenti, perché ogni ambiente
   Python contiene migliaia di file. Alla fine esiste la cartella `C:\Corso\Aula_Avanzata`, con dentro il file
   `pyproject.toml`, che Esplora file mostra come `pyproject` se le estensioni dei file sono nascoste.
4. In VS Code scegli **File → Open Folder...** e apri la cartella `Aula_Avanzata`. Alla domanda *Do you trust the
   authors of the files in this folder?* rispondi **Yes, I trust the authors**, perché in modalità ristretta i
   notebook non si possono eseguire.
5. Apri il terminale con **Terminal → New Terminal**, che parte dalla cartella aperta, e lancia `uv sync`. Il comando
   crea la cartella `.venv`, cioè l'ambiente virtuale del corso, con Python e tutte le librerie nelle versioni indicate
   in `uv.lock`; la prima volta richiede qualche minuto.
6. Apri `Modulo_1/00_Notebook.ipynb`, premi **Select Kernel** in alto a destra e scegli la voce che contiene `.venv`;
   se non compare, la trovi in **Select Another Kernel... → Python Environments...**. La cella della sezione 5 del
   notebook stampa il percorso del Python in uso, che deve contenere `.venv`.

Nel modulo 4 si usa anche Copilot, l'assistente per il codice integrato in VS Code, che funziona dopo l'accesso con
l'account abilitato dall'azienda. Conviene provarlo prima di quella giornata: **Ctrl+Alt+I** apre la chat, che propone
l'accesso se non è ancora stato fatto, e una domanda qualsiasi deve ricevere una risposta.

## Come si usano i notebook

Ogni notebook si apre con il tempo previsto, i dati che utilizza e gli obiettivi. Negli Hands-on, i piccoli esercizi
che seguono gli esempi, e negli esercizi il codice da scrivere prende il posto dei `...`, e la cella sotto controlla il
risultato e stampa ✅ se è corretto. Se qualcosa non torna, negli esercizi la chiamata `verifica("4.2")` stampa una
sola riga rossa che dice che cosa correggere, mentre negli Hands-on il messaggio da leggere è l'ultima riga
dell'errore, dopo `AssertionError`.

Nelle esercitazioni i blocchi *Passo per passo* e *Suggerimento* si aprono con un clic, e la cella `soluzione("E1.3")`
sotto ogni esercizio mostra soltanto la soluzione di quell'esercizio. La cartella `Soluzioni/` contiene fin dal primo
giorno la versione risolta di ogni notebook, che conviene aprire dopo aver provato da solo, per confrontare.

I notebook leggono i dati con percorsi relativi come `../Dati/impianti_fv.csv`, in cui `..` indica la cartella sopra
quella del notebook, cioè `Aula_Avanzata`. Per questo un notebook funziona soltanto se resta a quella profondità, e un
notebook nuovo creato per fare delle prove va messo in una delle cartelle `Modulo_1` … `Modulo_4`, dove gli stessi
percorsi funzionano.

Quello che scrivi in un notebook resta nel file quando lo salvi con **Ctrl+S**. Se durante il corso ricevi una
versione aggiornata di alcuni moduli, estrai lo zip nuovo nella cartella in cui hai estratto quello del corso, per
esempio `C:\Corso\`, e scegli di sostituire i file già presenti. Lo zip di aggiornamento contiene soltanto quei
moduli, con le loro soluzioni, i dati e le schede, quindi i notebook in cui hai già scritto le tue risposte restano
come sono.

## Le cartelle demo ed esercizio

Le cartelle `demo/` ed `esercizio/`, in `Modulo_1/Script_uv_Ruff/`, all'inizio contengono soltanto due script. Con
`uv init`, lanciato in un terminale aperto nella cartella, ciascuna diventa un progetto separato da quello del corso,
con il suo `pyproject.toml` e, dopo il primo `uv run`, con il suo ambiente `.venv` e il suo `uv.lock`. Gli
script che contengono si lanciano sempre con `uv run main.py` in un terminale aperto in quella cartella, che si ottiene
con il tasto destro sulla cartella nel pannello Explorer e la voce **Open in Integrated Terminal**. Anche Ruff si
lancia soltanto da quel terminale, perché dalla cartella del corso metterebbe in ordine anche i file di partenza delle
due cartelle, che poi non darebbero più i problemi da cui partono la dimostrazione e l'esercitazione.

Per ricominciare da capo una delle due cartelle, cancellala ed estraila di nuovo dallo zip del corso. Con un doppio
clic sullo zip, Esplora file ne mostra il contenuto: la cartella sta in `Aula_Avanzata\Modulo_1\Script_uv_Ruff\`, e
da lì la trascini in `Modulo_1\Script_uv_Ruff\` della tua cartella del corso. Estraendola sopra quella vecchia,
invece, resterebbero al loro posto `.venv`, `uv.lock` e gli altri file creati dai comandi.

## Se qualcosa non funziona

| Che cosa succede | Che cosa fare |
|---|---|
| Un notebook si ferma su un `import` con `ModuleNotFoundError: No module named 'pandas'` | Il kernel non è quello del corso. Premi **Select Kernel** e scegli la voce con `.venv`; se la voce manca, lancia `uv sync` nel terminale e riprova. |
| Il terminale risponde ``No `pyproject.toml` found in current directory or any parent directory`` | Il terminale non è nella cartella del corso. Apri `Aula_Avanzata` con **File → Open Folder...** e poi un terminale nuovo. |
| Nel pannello Explorer c'è solo una cartella `Aula_Avanzata` e manca `pyproject.toml` | Lo zip è stato estratto in una cartella che si chiama già `Aula_Avanzata`, per esempio quella proposta da **Estrai tutto...**, e il materiale si trova in `Aula_Avanzata\Aula_Avanzata`. Apri con **File → Open Folder...** la cartella interna. |
| PowerShell risponde che `uv` non è riconosciuto | La finestra è stata aperta prima dell'installazione di uv. Chiudi tutte le finestre di VS Code e di PowerShell e riaprile; se il messaggio resta, esci dall'account di Windows e rientra, oppure riavvia il computer. |
| PowerShell risponde che `winget` non è riconosciuto, oppure l'installazione è bloccata | Su alcuni computer aziendali winget non è disponibile. Lancia in PowerShell `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"`, l'installatore ufficiale di uv, che non richiede i permessi di amministratore, e poi apri una finestra nuova; se anche questo comando è bloccato, segnalalo al docente prima del corso. |
| `uv sync` o `uv add` si fermano con un errore che parla di certificati (`certificate`) | La rete aziendale controlla le connessioni sicure. Lancia una volta `setx UV_SYSTEM_CERTS true` in PowerShell, chiudi e riapri VS Code e ripeti il comando: da quel momento uv usa i certificati di Windows in tutti i comandi. Per un solo comando basta l'opzione `--system-certs`, che nelle versioni meno recenti di uv si chiama `--native-tls`. |
| Un notebook dà `FileNotFoundError` su un percorso `../Dati/...` | Il notebook è stato aperto direttamente dallo zip, senza estrarlo, oppure è stato spostato fuori dalla sua cartella, come `Modulo_2` o `Soluzioni`. Apri il notebook dalla cartella `C:\Corso\Aula_Avanzata` estratta al passo 3. |
| Nella cartella `demo` o `esercizio` lo script funziona subito, senza fermarsi sulle librerie mancanti | Lo script è stato lanciato con il pulsante **Run Python File**, che usa l'ambiente del corso, dove le librerie ci sono già. Lancialo con `uv run main.py` in un terminale aperto nella cartella dello script. |
| `uv run main.py` risponde con `error: Failed to spawn` | Il terminale non è nella cartella dello script. Aprilo con **Open in Integrated Terminal**, oppure, da un terminale aperto nella cartella del corso, entra nella cartella con `cd Modulo_1/Script_uv_Ruff/demo` o `cd Modulo_1/Script_uv_Ruff/esercizio`. |
| `uv add` risponde senza elencare librerie installate, e lo script continua a fermarsi | Il comando ha lavorato sul progetto del corso, perché il terminale non era nella cartella dello script. Apri il terminale nella cartella giusta e ripeti il comando. |
| Prima della dimostrazione o dell'esercitazione i file di `demo` o `esercizio` sono già in ordine, e `uv run ruff check` trova meno di quattro problemi | Ruff è stato lanciato dal terminale della cartella del corso e ha sistemato anche quei file. Cancella la cartella `demo` o `esercizio` ed estrai di nuovo soltanto quella dallo zip del corso, come descritto in [Le cartelle demo ed esercizio](#le-cartelle-demo-ed-esercizio). |
| uv stampa un avviso che comincia con `warning:` e nomina `VIRTUAL_ENV` | L'avviso è innocuo, perché uv usa comunque l'ambiente della cartella. Per non vederlo più, lancia `deactivate` oppure apri un terminale nuovo. |
