# Corso Python, versione Base

Questa cartella contiene il materiale del corso: i notebook dei quattro moduli con le esercitazioni, le soluzioni, i
dati e le schede di riepilogo, insieme ai file che descrivono l'ambiente Python del corso. La cartella funziona da
sola, quindi dopo l'installazione descritta qui sotto non serve nient'altro, e resta utilizzabile anche dopo il corso.

## Il contenuto della cartella

| Cartella o file | Che cosa contiene |
|---|---|
| `Modulo_1/` … `Modulo_4/` | i notebook di ciascun modulo, numerati da 00 a 11 nell'ordine in cui li seguiamo, e l'esercitazione che chiude i moduli 1, 2 e 3 |
| `Soluzioni/` | gli stessi notebook con gli esercizi risolti, tutti nella stessa cartella |
| `Dati/` | i file di dati letti dai notebook, descritti in `Dati/README.md` |
| `Schede/` | tre schede di una pagina: leggere il codice, gli errori più comuni, da Excel a pandas |
| `pyproject.toml`, `uv.lock`, `.python-version` | la versione di Python e l'elenco delle librerie del corso, da cui uv costruisce l'ambiente |
| `.vscode/` | le impostazioni di VS Code per questa cartella |

I notebook `Approfondimenti_1`, nella cartella `Modulo_2`, e `Approfondimenti_2`, nella cartella `Modulo_3`,
raccolgono argomenti che non rientrano nel percorso e si leggono quando si vuole andare oltre. Il file `corso.py`
nelle cartelle dei moduli e in `Soluzioni/` contiene i controlli degli esercizi e non va modificato.

## Installazione e primo avvio

Le istruzioni sono per Windows. L'installazione si fa una volta sola e richiede la connessione a internet, perché uv
scarica Python e le librerie del corso.

1. Installa VS Code da <https://code.visualstudio.com> e, dal pannello **Extensions**, che si apre con l'icona dei
   quattro quadratini nella barra a sinistra, le estensioni **Python** e **Jupyter** di Microsoft.
2. Apri PowerShell dal menu Start, cercando *PowerShell*, e lancia `uv --version`: se compare un numero di versione,
   uv è già installato e il passo finisce qui. Altrimenti installa uv con il comando
   `winget install --id=astral-sh.uv -e`; alla prima esecuzione winget può chiedere di accettare i termini delle
   sorgenti, e in quel caso rispondi `Y`. Al termine chiudi PowerShell e, se è aperto, VS Code, perché le finestre
   aperte prima dell'installazione non vedono il comando `uv`; in una finestra nuova `uv --version` stampa la versione.
3. Estrai lo zip in una cartella con un percorso corto, per esempio `C:\Corso\`: con il tasto destro sullo zip scegli
   **Estrai tutto...** (*Extract All...* in Windows in inglese) e scrivi `C:\Corso` come destinazione. Conviene
   evitare le cartelle sincronizzate con OneDrive, come spesso sono il Desktop e i Documenti, perché l'ambiente Python
   contiene migliaia di file. Alla fine esiste la cartella `C:\Corso\Aula_Base`, con dentro il file `pyproject.toml`,
   che Esplora file mostra come `pyproject` se le estensioni dei file sono nascoste.
4. In VS Code scegli **File → Open Folder...** e apri la cartella `Aula_Base`. Alla domanda *Do you trust the authors
   of the files in this folder?* rispondi **Yes, I trust the authors**, perché in modalità ristretta i notebook non si
   possono eseguire.
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
quella del notebook, cioè `Aula_Base`. Per questo un notebook funziona soltanto se resta a quella profondità, e un
notebook nuovo creato per fare delle prove va messo in una delle cartelle `Modulo_1` … `Modulo_4`, dove gli stessi
percorsi funzionano.

Quello che scrivi in un notebook resta nel file quando lo salvi con **Ctrl+S**. Se durante il corso ricevi una
versione aggiornata di alcuni moduli, estrai lo zip nuovo nella cartella in cui hai estratto quello del corso, per
esempio `C:\Corso\`, e scegli di sostituire i file già presenti. Lo zip di aggiornamento contiene soltanto quei
moduli, con le loro soluzioni, i dati e le schede, quindi i notebook in cui hai già scritto le tue risposte restano
come sono.

## Se qualcosa non funziona

| Che cosa succede | Che cosa fare |
|---|---|
| Un notebook si ferma su un `import` con `ModuleNotFoundError: No module named 'pandas'` | Il kernel non è quello del corso. Premi **Select Kernel** e scegli la voce con `.venv`; se la voce manca, lancia `uv sync` nel terminale e riprova. |
| Il terminale risponde ``No `pyproject.toml` found in current directory or any parent directory`` | Il terminale non è nella cartella del corso. Apri `Aula_Base` con **File → Open Folder...** e poi un terminale nuovo. |
| Nel pannello Explorer c'è solo una cartella `Aula_Base` e manca `pyproject.toml` | Lo zip è stato estratto in una cartella che si chiama già `Aula_Base`, per esempio quella proposta da **Estrai tutto...**, e il materiale si trova in `Aula_Base\Aula_Base`. Apri con **File → Open Folder...** la cartella interna. |
| PowerShell risponde che `uv` non è riconosciuto | La finestra è stata aperta prima dell'installazione di uv. Chiudi tutte le finestre di VS Code e di PowerShell e riaprile; se il messaggio resta, esci dall'account di Windows e rientra, oppure riavvia il computer. |
| PowerShell risponde che `winget` non è riconosciuto, oppure l'installazione è bloccata | Su alcuni computer aziendali winget non è disponibile. Lancia in PowerShell `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"`, l'installatore ufficiale di uv, che non richiede i permessi di amministratore, e poi apri una finestra nuova; se anche questo comando è bloccato, segnalalo al docente prima del corso. |
| `uv sync` si ferma con un errore che parla di certificati (`certificate`) | La rete aziendale controlla le connessioni sicure. Lancia `uv sync --system-certs`, che usa i certificati di Windows; nelle versioni meno recenti di uv l'opzione si chiama `--native-tls`. |
| Un notebook dà `FileNotFoundError` su un percorso `../Dati/...` | Il notebook è stato aperto direttamente dallo zip, senza estrarlo, oppure è stato spostato fuori dalla sua cartella, come `Modulo_2` o `Soluzioni`. Apri il notebook dalla cartella `C:\Corso\Aula_Base` estratta al passo 3. |
