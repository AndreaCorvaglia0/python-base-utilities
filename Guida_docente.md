# Guida per il docente

Il corso si tiene in quattro moduli di quattro ore, il 20 e 21 ottobre e il 27 e 28 ottobre 2026, in due versioni,
Base e Avanzata, che seguono lo stesso programma. In ogni giornata l'aula Base fa il modulo nelle prime quattro ore e
l'aula Avanzata lo stesso modulo nelle quattro successive, così le due aule arrivano alla fine di ogni giornata allo
stesso punto. Ogni corsista riceve soltanto la cartella della sua aula, `Aula_Base` o `Aula_Avanzata`, con i notebook
da leggere ed eseguire, le soluzioni, i dati e le schede. Le parti che il docente mostra dal vivo, cioè VS Code, Data
Wrangler e il wrapper delle API, non compaiono nei notebook dei corsisti: il materiale per prepararle si trova nella
cartella `Extra/` del repository, quello di riserva in `Riserva/`, e le tabelle di questa guida indicano quando
svolgere ogni parte e quanto dura.

## Il materiale dei corsisti

Le cartelle `Aula_Base/` e `Aula_Avanzata/` sono generate dal build e funzionano da sole. Ciascuna contiene i moduli
da `Modulo_1` a `Modulo_4`, la cartella `Soluzioni/`, i dati, le tre schede, il progetto uv dei corsisti
(`pyproject.toml`, `uv.lock` e `.python-version` del progetto `corso-python`, uguale per le due aule), le impostazioni
di VS Code e un `README.md` scritto per il corsista, con l'installazione, il primo avvio e i problemi più comuni. Gli
zip da consegnare si preparano con un solo comando:

    uv run python _build/esporta.py                      # dist/Aula_Base.zip e dist/Aula_Avanzata.zip
    uv run python _build/esporta.py avanzata             # una sola aula
    uv run python _build/esporta.py --moduli 3 4         # aggiornamento: dist/Aula_X_moduli_3_4.zip
    uv run python _build/esporta.py avanzata --riserva   # il materiale di riserva: dist/Riserva_Avanzata.zip

Il comando ricostruisce prima tutto il corso, così le copie dei dati, delle schede e delle cartelle della dimostrazione
e dell'esercizio tornano uguali agli originali anche dopo una prova, e mette nello zip soltanto i file che Git conosce o
non ignora. Restano quindi fuori l'ambiente `.venv`, le cache e i file prodotti eseguendo notebook e script, che ogni
corsista ricrea sul proprio PC.

Le soluzioni sono a disposizione dei corsisti fin dal primo giorno. La cartella `Soluzioni/` di ogni aula contiene la
versione risolta di tutti i notebook, in una sola cartella separata dai moduli, e nelle esercitazioni la cella
`soluzione("E1.3")` sotto ogni esercizio mostra la soluzione di quell'esercizio soltanto. Nell'Avanzata
`Soluzioni/Script_uv_Ruff/` contiene i progetti della dimostrazione e dell'esercizio come sono alla fine, mentre il
notebook `Ambiente_script_e_Ruff`, che non ha esercizi, non ha una copia in `Soluzioni/`.

I due zip si mandano completi prima della prima giornata, ciascuno ai corsisti della sua aula. Se i moduli 3 e 4
cambiano dopo le prime due giornate, si prepara l'aggiornamento con `uv run python _build/esporta.py --moduli 3 4`,
che scrive `dist/Aula_Base_moduli_3_4.zip` e `dist/Aula_Avanzata_moduli_3_4.zip`, e lo si manda nella settimana tra
il 21 e il 27 ottobre. Ciascuno zip contiene, dentro la cartella `Aula_Base` o `Aula_Avanzata`, soltanto `Modulo_3` e
`Modulo_4`, le soluzioni di quei moduli con `Soluzioni/corso.py`, `Dati/` e `Schede/`. Il corsista lo estrae in
`C:\Corso\`, cioè nella cartella che contiene la sua cartella del corso, e sceglie di sostituire i file: i notebook
dei moduli 1 e 2, in cui sta il lavoro delle prime due giornate, non sono nello zip e restano come sono. Lo zip di
aggiornamento non contiene `pyproject.toml` e `uv.lock`, quindi se serve una libreria nuova si manda anche lo zip
completo e si chiede di copiarne quei due file nella cartella del corso e di lanciare di nuovo `uv sync`. Il messaggio
ai corsisti può essere di questo tipo:

> In allegato trovate la versione aggiornata dei moduli 3 e 4. Estraete lo zip in `C:\Corso\`, la cartella in cui
> avete estratto lo zip del corso, e quando Windows chiede che cosa fare dei file già presenti scegliete di
> sostituirli. Lo zip non contiene i moduli 1 e 2, quindi il lavoro delle prime due giornate resta com'è.

## Prima del corso

Sui PC dell'aula devono essere installati uv e VS Code con le estensioni Python, Jupyter e GitHub Copilot, più Ruff
per la versione Avanzata. L'estensione Data Wrangler serve sul PC del docente per la dimostrazione del modulo 3, e su
quelli dei corsisti solo se si vuole che la provino. I PC devono raggiungere PyPI (`pypi.org` e
`files.pythonhosted.org`), il catalogo da cui uv scarica le librerie, perché ogni corsista lancia `uv sync` al primo
avvio e i corsisti dell'Avanzata, nel modulo 1, lanciano `uv add` nelle cartelle `demo/` ed `esercizio/`. Devono
raggiungere anche `releases.astral.sh`, da cui uv scarica Python 3.13 quando sul PC non c'è già, mentre l'installazione
di uv con winget scarica il programma da GitHub. Conviene provarlo una volta su un PC dell'aula, estraendo lo zip
e lanciando `uv sync`. Se la rete aziendale ispeziona le connessioni HTTPS, uv si ferma con un errore di certificato e
funziona con l'opzione `--system-certs` (`--native-tls` nelle versioni meno recenti di uv); per non ripeterla a ogni
comando si imposta una volta la variabile d'ambiente `UV_SYSTEM_CERTS=true`, per esempio con
`setx UV_SYSTEM_CERTS true` in PowerShell, e si riapre VS Code.

Il docente lavora dal repository, che ha un progetto uv suo nella radice: `uv sync` lanciato lì crea l'ambiente con cui
si aprono i notebook di `Extra/` e di `Riserva/`. La cartella `Dati/fallback/` contiene risposte di esempio delle API
usate nel corso, in modo che tutte le celle funzionino anche senza rete. Quando la rete è disponibile, il comando
`uv run python _build/scarica_fallback.py` sostituisce i file di esempio con i dati veri, cioè la temperatura di
Milano e le misure dei sensori lombardi; dopo il comando si riesportano gli zip, perché le aule ne ricevono una copia.

Prima della prima giornata conviene aprire un'esercitazione in VS Code su un PC dell'aula e controllare che i blocchi
"Passo per passo" e "Suggerimento" si aprano con un clic e che la cella `soluzione(...)` mostri il codice colorato.
Nella stessa occasione conviene controllare come si chiamano, nella versione di VS Code installata, il pulsante
**Variables** e la scheda **JUPYTER** in cui compaiono le variabili, perché il notebook 00 li nomina così.

Per l'Avanzata conviene provare almeno una volta la dimostrazione di uv e Ruff descritta più avanti, su un PC
dell'aula e in una copia della cartella estratta dallo zip, come quella dei corsisti: la prova controlla la rete e dà
un'idea dei tempi. Dopo la prova la cartella `demo/` si rimette allo stato di partenza cancellandola ed estraendola di
nuovo dallo zip, perché i comandi hanno modificato `pyproject.toml` e i due script e hanno creato `.venv`, `uv.lock`,
`spesa.xlsx`, `__pycache__` e `.ruff_cache`, che un'estrazione sopra la cartella vecchia lascerebbe al loro posto.

Se la prova si fa nel repository, il build successivo rimette le cartelle `demo/` ed `esercizio/` esattamente come
all'inizio e toglie anche `.venv`, `uv.lock`, il file Excel e le cache. Una prova nel repository può però lasciare
file nuovi in altri punti delle cartelle delle aule, come uno script degli esercizi di riserva o un file Excel nella
cartella del corso. Lo zip contiene soltanto i file che Git traccia o non ignora, quindi un file nuovo che Git non
ignora finirebbe nello zip: `esporta.py` lo segnala con un avviso che elenca i file non tracciati destinati allo zip, e
prima di consegnare conviene cancellarli e lanciare di nuovo il comando.

## Il primo avvio

All'inizio del modulo 1, durante la dimostrazione di VS Code, i corsisti installano il materiale seguendo il `README.md`
della loro cartella. Estraggono lo zip in `C:\Corso\`, aprono la cartella dell'aula con **File → Open Folder...**,
rispondono **Yes, I trust the authors**, lanciano `uv sync` nel terminale di VS Code e scelgono con **Select Kernel** la
`.venv` del corso nel notebook 00; chi ha già seguito il README prima del corso trova l'ambiente pronto. I problemi più
frequenti sono quattro: lo zip estratto in una cartella che si chiama già `Aula_Base`, che produce per esempio
`C:\Corso\Aula_Base\Aula_Base` e una cartella aperta senza `pyproject.toml`; lo zip estratto dentro OneDrive; il comando
`uv` non riconosciuto, perché VS Code o PowerShell erano già aperti durante l'installazione; l'errore di certificato
della rete aziendale. Il README del corsista indica il rimedio per ciascuno, e anche la strada da seguire quando winget
non è disponibile. Con tutta l'aula che scarica Python e le librerie nello stesso momento, `uv sync` può richiedere
qualche minuto in più del solito.

Nell'aula Base ci si limita a dire che `uv sync` ha costruito la cartella `.venv` con Python e tutte le librerie del
corso, nelle versioni scritte nel progetto. Nell'Avanzata se ne riparla alla fine del modulo, con il notebook
`Ambiente_script_e_Ruff`, che parte proprio da quel comando.

## La struttura di un modulo

Ogni blocco di quattro ore, cioè 240 minuti, contiene due pause da 15 minuti. Nei moduli 1, 2 e 3 l'ultima ora è
l'esercitazione, 45 minuti di lavoro dei corsisti e 15 di correzione, quindi restano circa 150 minuti di lezione. Il
margine che resta dopo i tempi delle tabelle non è lo stesso in tutti i moduli: nella Base è di 10 minuti nei moduli 1
e 2 e di 20 minuti nel modulo 3, mentre nell'Avanzata i moduli 1 e 2 occupano tutti i 240 minuti e non hanno margine,
e il modulo 3 ne ha 15. Dove il margine manca, un ritardo si recupera con i tagli indicati in "Dove tagliare se si è in
ritardo". Il modulo 4 non ha esercitazione: la giornata è dedicata a Plotly, agli agenti per il coding e al capstone,
e il suo margine è lo step 7 del capstone.

Dentro i notebook gli Hands-on sono i momenti in cui i corsisti toccano il codice appena visto: durano da uno a tre
minuti ciascuno, si lasciano fare e non si correggono insieme. Il notebook `Ambiente_script_e_Ruff` non ne ha, perché
la sua parte pratica è l'esercitazione che lo segue, e nemmeno il capstone, che procede a passi guidati. La sezione
Extra in fondo ai notebook da 00 a 10 si salta e si indica come lavoro per casa, e non è compresa nei tempi.

## I tempi (minuti netti di lezione, pause ed esercitazione escluse)

Modulo 1 · martedì 20 ottobre · Setup, Python e sintassi di base

| | Base | Avanzata |
|---|---|---|
| Dimostrazione di VS Code e primo avvio (`Extra/VS_Code_e_notebook.ipynb`) | 15 | 15 |
| 00 Jupyter e i notebook | 25 | 20 |
| 01 Introduzione a Python e sintassi base | 40 | 30 |
| 02 Tipi di dato e manipolazione | 40 | 35 |
| 03 Codice leggibile | 20 | 20 |
| Ambiente, script e Ruff (circa 15 di notebook e 15 di dimostrazione dal vivo) | no | 30 |
| **Lezione** | **140** | **150** |
| Esercitazione 1 | 60, esercizi sui notebook 00-03 | 60, la dimostrazione ripetuta nella cartella `esercizio/` |

Con le pause la Base occupa 230 minuti e l'Avanzata tutti i 240. Nella Base conviene fare la prima pausa dopo il 01 e la
seconda dopo il 03, prima dell'esercitazione. Nell'Avanzata la prima pausa cade dopo il 01 e la seconda dopo la
dimostrazione di uv e Ruff, prima dell'esercitazione: chi ha seguito la dimostrazione sul proprio PC e si è bloccato su
un comando si può aiutare durante la pausa.

Modulo 2 · mercoledì 21 ottobre · Controllo del flusso, funzioni e primi dati in pandas

| | Base | Avanzata |
|---|---|---|
| 04 Funzioni e controllo del flusso | 50 | 50 |
| 05 Oggetti ed errori | 35 | 30 |
| 06 Pandas: Series, DataFrame e import dei dati (Avanzata: con i 10 minuti della dimostrazione del wrapper delle API) | 55 | 70 |
| **Lezione** | **140** | **150** |
| Esercitazione 2 | 60 | 60 |

Modulo 3 · martedì 27 ottobre · Analisi dei dati con pandas

| | Base | Avanzata |
|---|---|---|
| 07 Pandas: operazioni sui DataFrame | 65 | 70 |
| Dimostrazione di Data Wrangler (`Extra/Data_Wrangler.ipynb`) | 15 | 15 |
| 08 Pandas: le date | 50 | 50 |
| **Lezione** | **130** | **135** |
| Esercitazione 3 | 60 | 60 |

Modulo 4 · mercoledì 28 ottobre · Agenti per il coding e capstone

| | Base | Avanzata |
|---|---|---|
| 09 Plotly per serie storiche | 25 | 25 |
| 10 Agenti per il coding | 35 | 35 |
| 11 Capstone, step 1-6 | 110 | 110 |
| 11 Capstone, step 7 con Copilot | 40 | 40 |
| **Totale** | **210** | **210** |

Il notebook 09 dà il minimo di Plotly che serve per leggere un grafico scritto da un agente, e lo slider,
l'istogramma e lo scatter si mostrano senza fermarsi. Lo step 7 del capstone è la parte aperta della giornata: i
corsisti scelgono una richiesta tra quelle elencate e la portano a termine con Copilot, applicando le tre abitudini
del notebook 10; è anche il margine del modulo, perché si accorcia senza perdere nulla di quello che precede. Quando
occorre tagliare, conviene farlo alla fine di una sezione e non a metà.

## Le dimostrazioni dal vivo

| Quando | Cosa mostrare | Materiale | Base | Avanzata |
|---|---|---|---|---|
| Modulo 1, apertura | VS Code: aprire la cartella, le estensioni, **Select Kernel** → `.venv`, eseguire una cella, Run All e Restart, le scorciatoie | `Extra/VS_Code_e_notebook.ipynb` | 15 min | 15 min |
| Modulo 1 (A), dopo il 03 | uv e Ruff: l'ambiente della dimostrazione costruito una libreria alla volta, poi `ruff format`, `ruff check` e le correzioni a mano | `Modulo_1/Script_uv_Ruff/demo/` nella cartella dell'aula | no | 15 min, dentro i 30 del notebook |
| Modulo 2, nel 06 (A) | Il wrapper: chiudere la chiamata all'API in una funzione riutilizzabile, prima dell'esercizio facoltativo dell'Esercitazione 2 | `Extra/API_wrapper.ipynb` | no | 10 min, dentro i 70 del 06 |
| Modulo 3, dopo il 07 | Data Wrangler: aprire un DataFrame, Editing mode, un filtro e una colonna tolta, il codice pandas che genera | `Extra/Data_Wrangler.ipynb` | 15 min | 15 min |

I notebook di `Extra/` si aprono dal repository, con l'ambiente creato da `uv sync` nella sua radice, e leggono i dati
di `Dati/`. La dimostrazione di uv e Ruff si fa invece nella cartella dell'aula, la stessa che hanno i corsisti, ed è
descritta nella sezione seguente. Nella Base l'ambiente, gli script e Ruff non si mostrano: durante la dimostrazione di
VS Code basta l'idea che `uv sync` ha costruito la cartella `.venv` con tutte le librerie.

## Modulo 1 Avanzata: ambiente, script e Ruff

Alla fine del modulo 1 l'aula Avanzata riprende il `uv sync` lanciato all'inizio del modulo e lo spiega: che cosa sono
uv e un ambiente virtuale, a che cosa servono i file del progetto, che differenza c'è tra notebook e script, come si
importa una funzione da un altro file e come si usa Ruff, che fa da formatter e da linter. Il materiale sta nella
cartella `Modulo_1/Script_uv_Ruff/` dell'aula e ha tre parti. Il notebook `Ambiente_script_e_Ruff` è una spiegazione
scritta che si scorre parlandoci sopra: contiene le definizioni, i comandi e i passi della dimostrazione, e il
racconto può restare sugli esempi indicati più sotto. La cartella `demo/`, che anche i corsisti ricevono per
seguirla sul proprio PC, è il punto di partenza della dimostrazione: lo script `main.py` usa le funzioni di
`calcoli.py` sul conto della spesa. La cartella `esercizio/` contiene un programma equivalente sulle temperature della
settimana, su cui i corsisti rifanno la dimostrazione nell'Esercitazione 1. Gli stati finali dei due progetti sono in
`Soluzioni/Script_uv_Ruff/`.

### Il piano

Il notebook dura 30 minuti: circa 15 per le sezioni 1-8, che si scorrono parlandoci sopra, e circa 15 per la
dimostrazione della sezione 9. La sezione 10 riassume i comandi e non si presenta, perché serve ai corsisti durante
l'esercitazione. Dopo la seconda pausa viene l'Esercitazione 1, che nell'Avanzata è la dimostrazione ripetuta nella
cartella `esercizio/`.

| Minuti | Che cosa | Dove |
|---|---|---|
| 0-6 | uv, l'ambiente virtuale, i file del progetto, aggiungere e togliere librerie | sezioni 1-3 |
| 6-11 | notebook e script, l'import di una funzione da un altro file | sezioni 4-5 |
| 11-15 | formatter, linter e Ruff | sezioni 6-8 |
| 15-22 | dimostrazione, prima parte: l'ambiente costruito una libreria alla volta | sezione 9, passi 1-7 |
| 22-30 | dimostrazione, seconda parte: il codice sistemato con Ruff | sezione 9, passi 8-14 |
| pausa | | |
| 0-45 | Esercitazione 1: i corsisti rifanno la dimostrazione in `esercizio/` | `Modulo_1/Esercitazione_1.ipynb` |
| 45-60 | correzione | |

### Che cosa raccontare

Per ogni sezione del notebook seguono i punti che conviene toccare, scelti tra le cose che un principiante incontra
più spesso quando analizza dati in Python. Il notebook contiene già le definizioni, quindi il racconto può restare
sugli esempi.

#### uv (sezione 1)

Il punto di partenza è il `uv sync` lanciato all'inizio del modulo. Il comando ha letto `.python-version`, ha
scaricato Python 3.13 se sul PC non c'era, ha creato la cartella `.venv` e ci ha installato le librerie nelle versioni
scritte in `uv.lock`; la prima cella di codice del notebook lo conferma, perché sia `sys.executable` sia il file di
pandas stanno dentro `.venv`. uv fa da solo quello che in Python si faceva con più strumenti, cioè pip per installare
le librerie, venv per creare l'ambiente e un programma per gestire le versioni di Python, ed è prodotto da Astral, la
stessa azienda di Ruff. Nel lavoro e negli esempi in rete i corsisti incontreranno anche pip e conda, che gestiscono
ambienti e librerie con gli stessi concetti e con comandi diversi.

#### L'ambiente virtuale (sezione 1)

Il vantaggio si spiega con un caso concreto. Il report dell'anno scorso funziona con pandas 2 e il progetto nuovo usa
pandas 3: con un solo Python per tutto, aggiornare pandas per il secondo romperebbe il primo, mentre con un ambiente
per progetto ciascuno tiene le sue versioni. L'ambiente è soltanto una cartella dentro il progetto, quindi si crea
senza diritti di amministratore e si cancella e si ricrea in ogni momento; per questo lo zip ricevuto dai corsisti non
conteneva `.venv`, che hanno costruito loro, con le stesse versioni del docente, a partire da `uv.lock`. Il costo è lo
spazio, circa 100 MB per un ambiente con pandas, ma uv prende i file dalla sua cache, e un secondo ambiente con le
stesse librerie è pronto in pochi secondi.

#### I file del progetto (sezione 2)

Conviene aprire in VS Code il `pyproject.toml` della cartella del corso e leggerlo insieme alla cella che lo carica
con `tomllib`. La sezione `[project]` elenca le librerie con vincoli larghi, come `pandas>=3.0`, il gruppo `dev`
contiene Ruff, che serve a chi scrive il codice e non al programma, e `[tool.ruff]` mostra che anche la configurazione
degli strumenti sta nello stesso file. Di `uv.lock` basta dire che lo scrive soltanto uv, che registra anche le
librerie installate indirettamente, come numpy, che arriva con pandas, e che si condivide insieme al codice, mentre
`.venv` non si condivide mai, né per email né in un repository Git.

#### Aggiungere e togliere librerie (sezione 3)

Il messaggio principale è che una libreria si aggiunge con `uv add` e non con `pip install`. Gli esempi in rete, e a
volte anche Copilot nel modulo 4, propongono `pip install` o `!pip install` in una cella, ma un ambiente creato da uv
non contiene pip, e anche quando il comando trova un pip da qualche parte la libreria resta fuori da `pyproject.toml` e
il successivo `uv sync` la toglie. Il secondo punto, che serve subito nella dimostrazione, è che uv lavora sul progetto
della cartella in cui si trova il terminale, cercando `pyproject.toml` in quella cartella e poi in quelle sopra. Dopo un
`uv add` nel progetto del corso conviene riavviare il kernel dei notebook con Restart, perché una libreria che il kernel
aveva già importato resta in memoria nella versione di prima anche se il comando l'ha aggiornata.

#### Notebook e script (sezione 4)

Il notebook è adatto a esplorare i dati, mentre uno script serve quando un'analisi va ripetuta allo stesso modo.
Un'analisi che va rifatta ogni mattina diventa uno script che l'Utilità di pianificazione di Windows lancia con
`uv run report.py` all'ora stabilita, anche senza nessuno davanti al PC. Il secondo vantaggio si collega a Restart e Run
All del notebook 00: uno script riparte sempre dalla prima riga, quindi il risultato non dipende dall'ordine in cui sono
state eseguite le celle. La cella che stampa l'inizio del file `.ipynb` mostra che un notebook è un file JSON, in cui la
modifica di una riga si confonde con output e metadati quando la si guarda con Git o in una revisione del codice. Nel
passaggio da notebook a script cambiano due dettagli, cioè che il risultato si vede solo con `print` e che i percorsi
relativi partono dalla cartella del terminale.

#### Importare una funzione da un altro file (sezione 5)

L'idea da far passare è che `from calcoli import totale`, `from math import sqrt` e `import pandas as pd` sono la
stessa operazione. Python cerca un modulo con quel nome nelle cartelle di `sys.path`, nell'ordine, e usa il primo che
trova, e quando si lancia uno script la prima cartella dell'elenco è quella dello script. Ne segue un errore che i
principianti fanno spesso: un file proprio chiamato `pandas.py`, accanto allo script, nasconde la libreria vera, e la
prima riga che la usa si ferma con `AttributeError: module 'pandas' has no attribute 'DataFrame'`. Il terzo punto è
che un `import` esegue il file importato dall'inizio alla fine, una volta sola, e che la variabile `__name__` vale
`"__main__"` nel file lanciato e il nome del modulo in quello importato, ed è il motivo del blocco
`if __name__ == "__main__":`. La cartella `__pycache__`, che compare dopo il primo import, contiene una versione già
tradotta del file e si ignora.

#### Il formatter (sezione 6)

Si parte dalle regole di PEP 8 lette nel notebook 03, cioè quattro spazi di indentazione, spazi attorno agli operatori,
due righe vuote attorno alle funzioni e righe non troppo lunghe: il formatter le applica da solo, a tutto il file e
nello stesso modo per tutti. In un gruppo di lavoro questo toglie le discussioni sullo stile e fa sì che le differenze
tra due versioni di un file mostrino soltanto i cambiamenti veri. `ruff format` segue lo stile di Black, il formatter
più diffuso nei progetti Python, e ha poche opzioni, la principale delle quali è la lunghezza delle righe. Il formatter
cambia soltanto la forma, quindi non rinomina le variabili, non toglie gli import inutilizzati e non divide le
stringhe; per questo nella dimostrazione la riga del `print` resta oltre i 100 caratteri anche dopo `ruff format`.

#### Il linter (sezione 7)

Il linter legge il codice senza eseguirlo e segnala gli errori probabili, come un import che non serve, una variabile
calcolata e mai usata, che spesso è il segno di un nome sbagliato o di un passaggio dimenticato, e un nome usato ma mai
definito (`F821`), cioè un `NameError` trovato prima di lanciare lo script. Ogni segnalazione ha un codice con la
lettera della famiglia: `E` e `W` vengono da pycodestyle e controllano PEP 8, `F` viene da Pyflakes e riguarda gli
errori probabili, `I` riordina gli import come isort. Il comando `uv run ruff rule F841` stampa nel terminale la
spiegazione di una regola, ed è il modo più rapido per capire un codice nuovo. Va detta anche la differenza tra
correzioni sicure e non sicure: `--fix` applica solo quelle segnate con `[*]`, mentre per `F841` Ruff propone una
correzione non sicura che lascerebbe al suo posto `len(prezzi)`, nel dubbio che la chiamata serva a qualcosa, e la
decisione giusta, cioè cancellare la riga, resta a chi ha scritto il codice.

#### Ruff in VS Code e dal terminale (sezione 8)

La strada principale è VS Code. L'estensione Ruff, che nella cartella dell'Avanzata è il formatter dei file Python,
controlla ogni file aperto mentre lo si scrive: **Shift+Alt+F** rimette in forma il file, le segnalazioni compaiono
sottolineate e nel pannello **Problems** (**Ctrl+Shift+M**), **Ctrl+.** su una riga sottolineata propone la
correzione e **Ruff: Fix all auto-fixable problems**, dalla palette dei comandi, applica tutte le correzioni sicure del
file. La configurazione è quella della sezione `[tool.ruff]` del `pyproject.toml` del corso, con righe fino a 100
caratteri e le famiglie `E`, `F`, `W` e `I`, che vale anche per `demo/` ed `esercizio/`, perché i loro `pyproject.toml`
non hanno una sezione `[tool.ruff]`; la voce `extend-exclude` lascia fuori `corso.py` e i notebook.

Il terminale si presenta per completezza: `uv run ruff format`, `uv run ruff check` e `uv run ruff check --fix` fanno
le stesse cose su tutti i file della cartella del terminale e delle sue sottocartelle. Per questo si lanciano soltanto
nel terminale aperto in `demo/` o `esercizio/`: dalla cartella del corso metterebbero in ordine anche i file di
partenza di quelle due cartelle, che poi non darebbero più le quattro segnalazioni da cui partono la dimostrazione e
l'esercitazione. La formattazione al salvataggio non è attiva, e chi la vuole la accende con **Format On Save**. Le
impostazioni della cartella fanno invece aggiungere a VS Code l'a capo dopo l'ultima riga a ogni salvataggio (`files.insertFinalNewline`), perché in un file
scritto a mano la sua mancanza è una segnalazione di Ruff, `W292`, che negli esercizi di riserva confonderebbe il
risultato. Se su un PC è installata l'estensione Pylint o Flake8, le impostazioni della cartella la tengono spenta,
perché segnalerebbe anche regole che il corso non usa, come la docstring mancante, con codici diversi da quelli di
Ruff. Prima del passo 9 conviene non salvare `calcoli.py` con una formattazione: il passo 9 non avrebbe più nulla da
mostrare.

### La dimostrazione dal vivo

La dimostrazione si fa nella cartella `Modulo_1/Script_uv_Ruff/demo/` di una copia dell'aula estratta dallo zip, la
stessa che hanno i corsisti, che possono ripetere i comandi sul proprio PC. Prima di cominciare conviene ingrandire il
carattere del terminale e tenere aperto `calcoli.py`, per vederlo cambiare, e far notare che la cartella contiene
soltanto i due script: il progetto nasce in aula con `uv init --bare`. I numeri di versione stampati da uv possono essere più alti di
quelli riportati qui. L'ordine dei passi Ruff, con la formattazione prima della lettura delle segnalazioni, serve a mostrare separatamente il lavoro
del formatter e quello del linter, ed è lo stesso che il notebook descrive nella sezione 8. Con le regole scelte il
linter trova le stesse quattro segnalazioni prima e dopo la formattazione, con numeri di riga diversi, quindi anche
partendo da `check --fix` il risultato finale sarebbe lo stesso.

1. Si apre il terminale nella cartella `demo/`, con il tasto destro sulla cartella nel pannello Explorer e la voce
   **Open in Integrated Terminal**, oppure con `cd Modulo_1/Script_uv_Ruff/demo` dalla cartella dell'aula. Il
   percorso all'inizio della riga di comando deve finire con `Script_uv_Ruff\demo`, ed è la prima cosa da far
   controllare ai corsisti.

2. Si lancia `uv run main.py` prima di creare il progetto. Lo script arriva in fondo e stampa le tre righe, perché la
   cartella `demo/` non ha un `pyproject.toml` e uv, risalendo le cartelle, trova quello del corso e usa il suo
   ambiente, dove pandas e openpyxl ci sono già. È il momento per mostrare che un comando di uv lavora sul progetto
   che trova a partire dalla cartella del terminale.

3. Si lancia `uv init --bare`, che stampa prima ``Project `demo` is excluded by workspace ...``, cioè che la cartella
   resta fuori dal progetto del corso, poi `Initialized project` con il nome `demo`, e crea soltanto `pyproject.toml`,
   con il nome della cartella e `dependencies = []`. Senza `--bare`, `uv init` preparerebbe anche un `README.md` vuoto
   e, fuori da un repository git, `.gitignore` e la cartella nascosta `.git`, che qui non servono. Il nuovo progetto non entra in quello del corso, perché il
   `pyproject.toml` del corso esclude le cartelle di `Modulo_1/Script_uv_Ruff/` nella sezione `[tool.uv.workspace]`;
   in qualunque altra cartella del corso `uv init` lo aggiungerebbe invece come parte del progetto del corso. Il file
   `spesa.xlsx` scritto al passo precedente si può cancellare.

4. Si rilancia `uv run main.py`, che questa volta lavora sul progetto `demo`: uv crea l'ambiente del progetto e lo
   script si ferma sull'import di pandas:

   ```text
   Using CPython 3.13.x interpreter at: ...
   Creating virtual environment at: .venv
   Traceback (most recent call last):
     File "...\demo\main.py", line 3, in <module>
       import pandas as pd
   ModuleNotFoundError: No module named 'pandas'
   ```

   La cartella `.venv` compare nell'Explorer accanto a `main.py`, ed è un ambiente nuovo e vuoto, separato da quello
   del corso, dove pandas invece c'è. Nella stessa cartella compare anche `uv.lock`, che `uv run` scrive prima di
   lanciare lo script e che per ora contiene soltanto il progetto. La riga 2,
   `from calcoli import totale, prezzo_medio`, è passata, perché `calcoli.py` sta nella stessa cartella, e lo script si
   è fermato alla riga 3. VS Code non sottolinea `import pandas`, perché l'editor usa l'interprete del corso, ed è per
   lo stesso motivo che gli script di questa parte non si lanciano con **Run Python File**. Se VS Code chiede se usare
   il nuovo ambiente per la cartella, si risponde di no, perché per i notebook resta l'ambiente del corso.

5. Si lancia `uv add pandas`, che installa pandas insieme alle librerie da cui dipende:

   ```text
   Resolved 6 packages in ...
   Installed 4 packages in ...
    + numpy==2.5.4
    + pandas==3.0.6
    + python-dateutil==2.9.0.post0
    + six==1.17.0
   ```

   Su Windows compare anche `tzdata`, che pandas richiede solo su quel sistema, e i pacchetti installati sono cinque.
   Se una versione non è ancora nella cache di uv, prima di `Installed` compaiono anche righe come
   `Downloading numpy (...)` e `Prepared 1 package in ...`. In `pyproject.toml` la lista `dependencies` contiene ora
   `"pandas>=3.0.6"`, con la versione appena installata come minimo, e `uv.lock`, creato al passo precedente, ora
   elenca anche pandas e le librerie da cui dipende. Il punto da sottolineare è che abbiamo chiesto una libreria e ne
   sono arrivate altre, quelle da cui pandas dipende, tutte registrate in `uv.lock`.

6. Si rilancia `uv run main.py`. Lo script stampa le prime due righe e si ferma al salvataggio in Excel:

   ```text
   Totale della spesa: 13.10 euro
   Prezzo medio di un prodotto: 2.62 euro, calcolato su 5 prodotti
   Traceback (most recent call last):
     ...
     File "...\pandas\io\excel\_openpyxl.py", line 58, in __init__
       from openpyxl.workbook import Workbook
   ModuleNotFoundError: No module named 'openpyxl'
   ```

   Questo è l'errore che i corsisti non si aspettano, perché `main.py` non importa openpyxl. Il traceback è lungo
   perché l'errore nasce dentro pandas, e si legge dal basso, come dice la Scheda sugli errori: l'ultimo file è
   `_openpyxl.py`, lo stesso che il notebook elenca nella sezione 1. pandas usa openpyxl per scrivere e leggere i file
   `.xlsx` ma non lo installa da sé. In un progetto nuovo anche la prima `read_excel` si ferma per lo stesso motivo,
   ma con un messaggio diverso, che nomina pip e conda e che in un progetto gestito con uv si risolve comunque con
   `uv add openpyxl`:

   ```text
   ImportError: `Import openpyxl` failed.  Use pip or conda to install the openpyxl package.
   ```

7. Si lancia `uv add openpyxl`, che installa `et-xmlfile` e `openpyxl`, e poi di nuovo `uv run main.py`:

   ```text
   Totale della spesa: 13.10 euro
   Prezzo medio di un prodotto: 2.62 euro, calcolato su 5 prodotti
   La tabella della spesa è nel file spesa.xlsx
   ```

   Il file `spesa.xlsx` compare nella cartella `demo/`, che è quella del terminale, e `pyproject.toml` elenca ora
   `openpyxl` e `pandas`.

8. Si lancia `uv add --dev ruff`, che installa Ruff e aggiunge a `pyproject.toml` la sezione `[dependency-groups]`
   con `dev = ["ruff>=0.17.1"]`, lo stesso gruppo che il progetto del corso usa per Ruff.

9. Con `calcoli.py` e `main.py` aperti in VS Code, si usa **Format Document** (**Shift+Alt+F**) su ciascuno dei due
   file. In `calcoli.py` compaiono gli spazi attorno a `=` e a `/`, `sum( prezzi )` diventa `sum(prezzi)`, le due
   funzioni sono separate da due righe vuote e c'è una riga vuota dopo la docstring. In `main.py` compare la riga vuota
   dopo la docstring, e il `print` lungo viene diviso su tre righe, con la stringa da sola in quella centrale, ma resta
   oltre i 100 caratteri. L'import di `math` e la variabile `numero` sono ancora lì.

10. Si apre il pannello **Problems** (**Ctrl+Shift+M**), che con i due file aperti mostra le quattro segnalazioni di
    Ruff, ciascuna con il codice tra parentesi e la riga: `math` imported but unused `Ruff(F401)` e Local variable
    `numero` is assigned to but never used `Ruff(F841)` in `calcoli.py`, Import block is un-sorted or un-formatted
    `Ruff(I001)` e Line too long (104 > 100) `Ruff(E501)` in `main.py`. Le stesse righe sono sottolineate nel codice, e
    passandoci sopra con il mouse compare il messaggio. La riga lunga misura 104 caratteri perché il formatter ha messo
    la stringa su una riga sua, rientrata di quattro spazi; prima della formattazione ne aveva 107. Se il pannello
    mostra anche `W293` o `W292`, il file è stato modificato a mano e in fondo c'è una riga con soli spazi: il passo 9
    l'ha già tolta, oppure la toglie il passo 13.

11. Su ciascuno dei due file si apre la palette dei comandi (**Ctrl+Shift+P**) e si sceglie **Ruff: Fix all
    auto-fixable problems**; in alternativa, **Ctrl+.** sulla riga sottolineata propone la correzione di quella sola
    riga, e conviene mostrarlo almeno una volta. In `main.py` gli import diventano `import pandas as pd`, una riga
    vuota e `from calcoli import prezzo_medio, totale`: prima le librerie installate, poi i file del progetto, e i nomi
    in ordine alfabetico. In `calcoli.py` l'import di `math` non c'è più, e al suo posto resta una riga vuota di troppo
    dopo la docstring. Restano nel pannello le due segnalazioni che Ruff non corregge da solo, `F841` ed `E501`.

12. Si correggono a mano le due segnalazioni rimaste. In `calcoli.py` si cancella la riga `numero = len(prezzi)`, e in
    `main.py` si divide la f-string in due pezzi:

    ```python
    print(
        f"Prezzo medio di un prodotto: {prezzo_medio(prezzi):.2f} euro, "
        f"calcolato su {len(prezzi)} prodotti"
    )
    ```

    Python unisce due stringhe scritte una dopo l'altra in una stringa sola, quindi il testo stampato non cambia.
    Ciascun pezzo ha la sua `f` perché contiene delle graffe, e lo spazio resta alla fine del primo pezzo.

13. Si usa di nuovo **Shift+Alt+F** su `calcoli.py`, che toglie la riga vuota in più, e si salvano i due file: il
    pannello Problems non ha più segnalazioni di Ruff. La riga vuota in più non è una segnalazione del linter, con le
    regole scelte, e la sistema soltanto il formatter: per questo il lavoro si chiude sempre con una formattazione.

    Per completezza si mostra che dal terminale, nella cartella `demo/`, gli stessi passi sono `uv run ruff format`
    (`2 files reformatted`), `uv run ruff check` (le quattro segnalazioni, con `Found 4 errors.` e
    ``[*] 2 fixable with `--fix` ``), `uv run ruff check --fix`, le correzioni a mano, di nuovo `uv run ruff format` e
    `uv run ruff check`, che alla fine risponde `All checks passed!`. Nell'output di `check` Ruff ricorda anche la
    correzione non sicura di `F841`, che non usiamo perché lascerebbe la chiamata `len(prezzi)` al posto della riga.

14. Si lancia un'ultima volta `uv run main.py`, che stampa le stesse tre righe di prima. Per chiudere si mostra il
    `pyproject.toml` finale, con `openpyxl` e `pandas` tra le dipendenze e Ruff nel gruppo `dev`, e lo si confronta
    con quello di `Soluzioni/Script_uv_Ruff/demo/`.

### I print facoltativi: l'import e `__name__`

Se resta tempo, o se qualcuno chiede che cosa succede durante un import, si aggiunge sotto la docstring di
`calcoli.py` la riga `print(f"Sto leggendo calcoli.py, con il nome {__name__}")`. Con `uv run main.py` la riga compare
prima di tutto il resto, con il nome `calcoli`, perché l'import esegue il file prima che `main.py` prosegua; con
`uv run calcoli.py` compare da sola, con il nome `__main__`, perché questa volta il file è il programma principale e
per il resto contiene soltanto definizioni di funzioni. È l'occasione per scrivere in fondo a `calcoli.py` un blocco
`if __name__ == "__main__":` che stampa `totale([1.5, 2.5])`, e per far vedere che il suo contenuto si esegue con
`uv run calcoli.py` ma non con `uv run main.py`. Alla fine le righe di prova si tolgono, e i corsisti ritrovano lo
stesso esperimento nel passo facoltativo E1.7. Un'altra aggiunta che usa soltanto il modulo 1 è una riga in `main.py`
che stampa un prezzo dal dizionario, come `print(f"Il caffè costa {spesa['caffè']:.2f} euro")`.

### L'ora di esercitazione

Nell'Esercitazione 1 dell'Avanzata i corsisti rifanno la dimostrazione nella cartella `esercizio/`, che ha la stessa
struttura di `demo/`: un `pyproject.toml` con la lista `dependencies` vuota, il file `.python-version`, il file
`meteo.py` con le funzioni `massima`, `minima` e `media`, e lo script `main.py`, che ne importa due, stampa la
temperatura massima e quella media della settimana e salva la tabella in `meteo.xlsx`. Gli errori arrivano nello stesso
ordine della dimostrazione, prima pandas e poi openpyxl, e Ruff trova gli stessi quattro codici, `F401` e `F841` in
`meteo.py`, `I001` ed `E501` in `main.py`; la riga lunga, dopo la formattazione, misura 102 caratteri, e la variabile
mai usata è `giorni`, nella funzione `minima`. Nell'output di `ruff check` le segnalazioni di `main.py` vengono prima di
quelle di `meteo.py`, perché Ruff ordina i file per nome.

Il notebook `Modulo_1/Esercitazione_1.ipynb` guida i corsisti passo per passo. Si apre con il modo di aprire il
terminale nella cartella `esercizio/` e con l'avvertenza sul pulsante **Run Python File**, poi propone quattro domande
sui concetti del notebook `Ambiente_script_e_Ruff`, cinque passi da fare in sequenza, perché ognuno parte dalla
cartella come l'ha lasciata il precedente, e tre passi facoltativi. Ogni passo dice che cosa vogliamo ottenere, elenca
i comandi in un blocco *Passo per passo* e ha un suggerimento nascosto. Il corsista lavora nel terminale e nei file
della cartella e copia nella cella del passo quello che il terminale ha stampato; la verifica controlla quei valori e,
nei passi che cambiano i file del progetto, legge anche i file di `esercizio/`, per confermare che i comandi hanno
fatto il loro lavoro, e la cella `soluzione` mostra i comandi e i valori attesi.

| Passo | Il corsista scrive | La verifica controlla |
|---|---|---|
| E1.1 | `nome_progetto`, `cartella_creata`, `libreria_mancante` | `pyproject.toml` creato da `uv init --bare` con il nome `esercizio`, `uv.lock` nella cartella, `.venv` e `pandas` |
| E1.2 | `seconda_libreria` | pandas tra le `dependencies` di `esercizio/pyproject.toml`, e `openpyxl` |
| E1.3 | `riga_media` | openpyxl tra le `dependencies`, e la riga `Temperatura media della settimana: 15.0 gradi, calcolata su 5 giorni` |
| E1.4 | `avvisi` | Ruff nel gruppo `dev`, `meteo.py` già formattato, e i codici `E501`, `F401`, `F841`, `I001` letti nel pannello Problems |
| E1.5 | `segnalazioni_rimaste` | gli import di `main.py` in ordine, `meteo.py` senza `import math`, senza `giorni` e senza righe vuote di troppo, nessuna riga di `main.py` oltre i 100 caratteri, e zero segnalazioni di Ruff nel pannello Problems |
| E1.6, facoltativo | `riga_minima` | `minima` tra i nomi importati, il `print` che chiama `minima(valori)`, e la riga `Temperatura minima della settimana: 13.8 gradi` |
| E1.7, facoltativo | `nome_importato`, `nome_lanciato` | `meteo` e `__main__`, e la riga di prova tolta da `meteo.py` |
| E1.8, facoltativo | `file_versioni` | `uv.lock` |

Le verifiche leggono i file di `Script_uv_Ruff/esercizio/` con un percorso relativo al notebook, quindi un messaggio
come `pandas non è tra le dependencies di esercizio/pyproject.toml` vuol dire quasi sempre che `uv add` è stato
lanciato da un'altra cartella. Nel notebook delle soluzioni lo stesso percorso porta allo stato finale, in
`Soluzioni/Script_uv_Ruff/esercizio/`, e lì tutte le verifiche passano. Durante i 45 minuti conviene girare tra i
banchi guardando il percorso all'inizio della riga di comando, che deve finire con `Script_uv_Ruff\esercizio`, e
controllare che nessuno usi il pulsante **Run Python File**. Il passo su cui ci si ferma più spesso è il secondo
errore, quello di openpyxl, perché il traceback è lungo e il nome della libreria sta nell'ultima riga.

La correzione dei 15 minuti finali si fa su una cartella `esercizio/` completata, quella del docente o quella di un
corsista sullo schermo condiviso, in quattro passaggi.

1. Per circa cinque minuti si guardano i file del progetto. Si confronta `esercizio/pyproject.toml` con quello di
   `Soluzioni/Script_uv_Ruff/esercizio/`, selezionando i due file nell'Explorer con **Ctrl** e scegliendo **Compare
   Selected** con il tasto destro. La lista `dependencies` è passata da vuota a `openpyxl>=3.1.5` e `pandas>=3.0.6`,
   in ordine alfabetico perché la scrive uv, e il gruppo `dev` contiene Ruff. In `uv.lock` si cercano le righe
   `name =`: le librerie chieste sono pandas, openpyxl e Ruff, e le altre, cioè numpy, python-dateutil, six,
   et-xmlfile e, su Windows, tzdata, sono arrivate con loro. È il file da cui `uv sync` ricostruisce l'ambiente nel
   passo E1.8.
2. Per circa sei minuti si riprendono i quattro codici di Ruff. **Ruff: Fix all auto-fixable problems**, o `--fix` per
   chi ha usato il terminale, ha corretto `F401`, togliendo `import math`, e
   `I001`, mettendo prima `import pandas as pd` e poi, dopo una riga vuota, `from meteo import massima, media`. A mano
   si correggono `F841`, cancellando la riga `giorni = len(temperature)`, che la correzione non sicura avrebbe ridotto a
   `len(temperature)`, ed `E501`, dividendo la f-string dopo `gradi, ` come nel `main.py` delle soluzioni.
3. Per circa tre minuti si guarda lo stato finale. Il pannello Problems non ha segnalazioni di Ruff, e dal terminale
   `uv run ruff check` risponde `All checks passed!`; `uv run main.py` stampa tre righe, o quattro con la temperatura minima del passo E1.6.
4. Nell'ultimo minuto si citano i passi facoltativi. Il passo E1.7 dà `meteo` per il file importato e `__main__` per il
   file lanciato, che è il motivo del blocco `if __name__ == "__main__":`, e il passo E1.8 mostra che `.venv` si ricrea
   identico con `uv sync`, senza ripetere nessun `uv add`.

### Gli esercizi classici dell'Esercitazione 1

Nell'Avanzata gli esercizi dell'Esercitazione 1 sui notebook 00-03 restano nello stesso notebook, dopo la parte sullo
script, nella sezione "Esercizi sui notebook 00-03, da fare a casa": quattro domande di riepilogo, gli esercizi da
E1.9 a E1.13 nella variante Avanzata e la sfida E1.14, con le verifiche, le celle `soluzione` e la versione risolta in
`Soluzioni/Esercitazione_1.ipynb`. Si indicano alla fine della correzione come lavoro facoltativo per casa e non si
correggono in aula. La Base fa invece l'Esercitazione 1 sugli stessi esercizi, nella variante più guidata.

### Problemi frequenti e come rimediare

Il comando `uv init` crea un progetto a sé soltanto nelle cartelle di `Modulo_1/Script_uv_Ruff/`, che il
`pyproject.toml` dell'aula esclude nella sezione `[tool.uv.workspace]`. In qualunque altra cartella dell'aula uv vede che
la cartella sta dentro un altro progetto e registra quello nuovo come membro del progetto del corso: nella sezione
`[tool.uv.workspace]` dell'aula compare una sezione `[tool.uv.workspace]` con `members = [...]`, e il progetto nuovo usa la `.venv` e il
`uv.lock` del corso, dove le librerie ci sono già, quindi non si vede mai che cosa manca. Per rimediare si toglie la
voce aggiunta a `members`, che deve tornare `members = []`, si sposta fuori dall'aula o si cancella la cartella nuova
e si lancia `uv sync` nella cartella dell'aula, che riporta anche `uv.lock` allo stato di partenza; in alternativa si
ricopiano `pyproject.toml` e `uv.lock` dallo zip e si lancia `uv sync`. Un progetto proprio, che non sia la dimostrazione o
l'esercizio, si crea fuori dall'aula, per esempio con `uv init prova` lanciato in `C:\Corso`.

Un `uv add` lanciato dalla cartella dell'aula o da `Modulo_1`, invece che da `demo/` o da `esercizio/`, lavora sul
progetto del corso. Con pandas, openpyxl e Ruff non cambia nulla, perché il corso li ha già: uv risponde con due righe
come `Resolved 54 packages` e `Checked 47 packages`, senza nessuna riga che comincia con `+`, lo script continua a
fermarsi e la verifica di E1.2 dice che pandas non è nel `pyproject.toml` dell'esercizio. Basta aprire il terminale
nella cartella giusta e ripetere il comando. Una libreria che il corso non ha, invece, entra nel `pyproject.toml` e nel
`uv.lock` dell'aula, e si toglie con `uv remove` seguito dal suo nome, lanciato dalla cartella dell'aula. Dalla
cartella dell'aula non si lancia mai `uv remove pandas` o `uv remove openpyxl`, perché toglierebbe al corso librerie
che i notebook usano.

Il pulsante **Run Python File** di VS Code lancia lo script con l'interprete selezionato nell'editor, che è quello del
corso e ha già pandas e openpyxl. Lo script quindi funziona subito e gli errori da cui parte la dimostrazione non
compaiono. Le impostazioni della cartella dell'Avanzata fanno partire il pulsante dalla cartella dello script
(`python.terminal.executeInFileDir`), quindi il file Excel compare comunque in `demo/` o in `esercizio/`, e l'unico
segno del problema è che gli errori mancano. Si cancella il file Excel creato in questo modo e si rilancia lo script con
`uv run main.py` nel terminale della cartella giusta. Quando uv crea un `.venv` dentro la cartella del corso, VS Code
può proporre di sceglierlo come ambiente della cartella: si risponde di no, perché l'editor e i notebook devono
continuare a usare l'ambiente del corso.

Ruff lanciato nel terminale della cartella del corso lavora su tutti gli script dell'aula, cioè quelli di `demo/`, di
`esercizio/` e delle loro copie finite in `Soluzioni/Script_uv_Ruff/`, ciascuno con la configurazione del proprio
`pyproject.toml`, mentre i notebook e i file `corso.py` restano fuori per la voce `extend-exclude` del `pyproject.toml`
del corso. Su una cartella appena estratta `uv run ruff check` stampa quindi otto segnalazioni, le quattro della
dimostrazione e le quattro dell'esercizio, e `ruff format` o `ruff check --fix` mettono in ordine i file di partenza di
`demo/` ed `esercizio/`. Dopo un comando del genere la dimostrazione o i passi E1.4 ed E1.5 non trovano più le
segnalazioni attese: si cancella la cartella `demo/` o `esercizio/` e la si estrae di nuovo dallo zip del corso. Per la
stessa esclusione l'estensione Ruff non sottolinea nulla nei notebook del corso e non li rimette in forma.

Senza accesso a PyPI `uv add` non può scaricare le librerie e si ferma con un errore di rete. Con un proxy che ispeziona
le connessioni l'errore parla di certificati, e si risolve con `--system-certs` o con la variabile `UV_SYSTEM_CERTS`,
come per `uv sync`. Se la rete manca del tutto, la prima parte della dimostrazione si racconta mostrando i file finali
in `Soluzioni/Script_uv_Ruff/demo/` e quello che i comandi avrebbero stampato, riportato in questa sezione. La parte su
Ruff si fa comunque, con il Ruff del progetto del corso: dalla cartella dell'aula
`uv run ruff format Modulo_1/Script_uv_Ruff/demo` e `uv run ruff check Modulo_1/Script_uv_Ruff/demo` lavorano sulla sola
cartella `demo/`, con la sua configurazione, e danno le stesse quattro segnalazioni, con l'ultima riga scritta in modo
un po' diverso perché il corso ha una versione di Ruff meno recente.

L'avviso ``warning: `VIRTUAL_ENV=...` does not match the project environment path `.venv` and will be ignored; use
`--active` to target the active environment instead`` compare quando il terminale ha attivato l'ambiente del corso.
Le impostazioni della cartella lo evitano, perché `python.terminal.activateEnvironment` è `false`, ma succede se
qualcuno riattiva l'impostazione o lancia a mano `.venv\Scripts\activate`. L'avviso è innocuo, perché uv usa comunque
la `.venv` della cartella in cui è lanciato, e sparisce con `deactivate` o aprendo un terminale nuovo. L'opzione
`--active` suggerita dal messaggio non va usata, perché farebbe lavorare uv sull'ambiente del corso.

Una cartella dell'aula estratta dentro OneDrive o in un percorso lungo, come
`C:\Users\nome.cognome\OneDrive - Azienda\Documenti\Corso\...`, dà problemi soprattutto nell'Avanzata, che ha tre
ambienti: quello del corso, quello della dimostrazione e quello dell'esercizio. OneDrive sincronizza le migliaia di file
di ogni `.venv` e a volte li blocca, e uv si ferma con errori di accesso negato; i percorsi dentro `.venv`, inoltre,
possono superare il limite di 260 caratteri di Windows. Il rimedio è spostare la cartella dell'aula in `C:\Corso`,
cancellare le cartelle `.venv`, che dopo uno spostamento conviene sempre ricreare, e lanciare di nuovo `uv sync` nella
cartella dell'aula e nelle cartelle `demo/` ed `esercizio/`.

Dopo il primo import compare accanto a `calcoli.py` o a `meteo.py` la cartella `__pycache__`, e dopo il primo comando
di Ruff la cartella `.ruff_cache`. VS Code non le mostra, perché le impostazioni della cartella le nascondono, ma si
vedono in Esplora file e nell'elenco dei file del terminale; sono cache che si possono cancellare e che non si
condividono insieme al codice.

## Le esercitazioni

Le tre esercitazioni durano un'ora ciascuna: 45 minuti di lavoro dei corsisti e 15 di correzione, in cui si mostrano le
soluzioni degli esercizi del nucleo, cinque nelle esercitazioni 1 e 2 e sei nella 3; la sfida finale e gli eventuali
facoltativi non si correggono, ma hanno anche loro la cella `soluzione`. Gli esercizi sono quelli scritti dal docente
nei notebook delle edizioni precedenti, portati nel formato comune: ogni esercizio apre dicendo che cosa si vuole
ottenere, i passi stanno in un blocco che si apre con un clic, i suggerimenti sono nascosti e la soluzione di ogni
esercizio si mostra a richiesta. In Base ogni esercizio ha due suggerimenti e uno starter guidato, in Avanzata un
suggerimento, uno starter quasi vuoto e una richiesta in più. Il testo dei notebook non parla del docente né della
correzione: quello che serve a chi conduce l'ora sta qui. Le versioni risolte sono nella cartella `Soluzioni/` dell'aula
fin dal primo giorno, quindi chi vuole confrontare il proprio lavoro le trova lì anche durante l'ora. L'Esercitazione 1
dell'Avanzata ha un formato diverso, descritto nella sezione sul modulo 1 Avanzata.

Due controlli degli esercizi originali erano sbagliati e il materiale usa i valori corretti: le capitali con un
numero pari di lettere sono sei (Roma ne ha quattro e Washington dieci), e gli utenti con più di tre ascolti sono tre,
perché l'utente 101 ne ha quindici.

## Se la classe è avanti

I notebook `Approfondimenti_1` e `Approfondimenti_2` raccolgono il materiale uscito dal percorso principale, con le
versioni risolte in `Soluzioni/`. `Approfondimenti_1` sta in `Modulo_2` in entrambe le aule e contiene le operazioni
con i set, il ciclo `while` e la lettura di più file CSV con i tipi di dato, e nell'Avanzata anche `map`, `filter` e i
generatori. `Approfondimenti_2` contiene le differenze tra date e il fuso orario: nella Base sta in `Modulo_3` e si
ferma lì, mentre nell'Avanzata sta in `Modulo_4` e aggiunge `shift`, `rolling`, i type hint, le dataclass, i
decoratori, i generatori e `**kwargs`. Si aprono quando un modulo termina in anticipo, una sezione alla volta, e si
possono anche lasciare ai corsisti come lettura per casa. Per l'aula Avanzata è previsto anche un breve notebook
facoltativo su Prophet nel modulo 4, da preparare dopo aver verificato che `uv add prophet` funzioni sui PC dell'aula.

Il materiale di riserva sta in `Riserva/`, fuori dalle cartelle dei corsisti. L'Homework, una settimana nell'ufficio
Analisi Consumi, è in `Riserva/Base/` e `Riserva/Avanzata/` con le soluzioni accanto, da distribuire solo a una classe
molto più veloce del previsto. In `Riserva/Avanzata/` c'è anche `Esercizi_uv_script_Ruff`, circa 40 minuti, con sei
esercizi sugli argomenti del notebook `Ambiente_script_e_Ruff`: leggere `pyproject.toml` con `tomllib`, scegliere il
comando di uv adatto a una situazione, scrivere uno script con il blocco `if __name__ == "__main__":`, passare da un
notebook a uno script, correggere a mano una riga troppo lunga e ripulire un file con Ruff. Serve a un'aula Avanzata che
finisce l'esercitazione in anticipo, o a chi vuole fare pratica a casa.

Per consegnare il materiale di riserva si lancia `uv run python _build/esporta.py avanzata --riserva` (oppure `base`),
che prepara `dist/Riserva_Avanzata.zip` con la cartella `Riserva/Avanzata/`, i notebook e il `corso.py` che contiene le
verifiche, senza i file `.csv` che l'Homework scrive quando lo si esegue. I corsisti estraggono lo zip dentro la
cartella dell'aula, dove compare `Riserva/Avanzata/` allo stesso livello dei moduli: da lì i percorsi `../../Dati/`
dell'Homework arrivano ai dati del corso, come nel repository, e `from corso import verifica` trova il `corso.py`
giusto. La cartella non va copiata nelle `Aula_*` del repository, perché un build completo toglie da lì i
notebook che nessun sorgente produce.

## Il percorso minimo

Se un modulo procede male, per problemi di installazione, di rete o per una classe lenta, le parti che non si saltano
sono queste:

- Modulo 1: 00, 01, 02 (liste e dizionari). Nella Base l'esercitazione si riduce a tre esercizi; nell'Avanzata restano
  la dimostrazione di uv e Ruff, con le sezioni 1-8 del notebook raccontate in pochi minuti, e i passi E1.1-E1.5
  dell'esercitazione.
- Modulo 2: 04 (`if`, `for`, funzioni), 06 (CSV ed Excel). Esercitazione ridotta a tre esercizi.
- Modulo 3: 07 (selezione, valori mancanti, groupby), 08 (indice temporale e resample). Esercitazione ridotta a tre
  esercizi.
- Modulo 4: 09 (un grafico a linee), 10 ridotto alla prova guidata con un prompt solo, 11 (step 1-4 e una richiesta
  dello step 7).

## Dove tagliare se si è in ritardo

- Le sezioni Extra sono già fuori dal tempo d'aula; gli Hands-on si possono saltare a voce, mostrando la soluzione.
- Esercitazioni: le domande si fanno a voce, gli esercizi si riducono a tre.
- Modulo 1 Avanzata, che non ha margine: nel 03 si tengono le docstring e PEP 8, su cui si appoggia la parte sul
  formatter, e si scorrono i commenti e il Markdown; in `Ambiente_script_e_Ruff` le sezioni 1-3 si raccontano mentre
  la dimostrazione costruisce l'ambiente, invece che prima, e i print facoltativi si saltano.
- 06 Avanzata: la sezione sulle API si accorcia all'esempio dell'anagrafica dei sensori.
- 07 Avanzata: `query`, l'assegnazione condizionale con `.loc`, l'indice a due colonne e `agg` sono le parti in più
  rispetto a Base: si possono citare e basta.
- 09: la sezione sugli altri grafici si può solo mostrare.
- Capstone: gli step 1-4 sono il minimo; 5 e 6 si possono fare insieme sullo schermo del docente, e lo step 7 si
  riduce a una richiesta.

## Per chi modifica il materiale

I notebook sono generati dagli script in `_build/src/` e non si modificano a mano, e il resto delle cartelle delle aule
è una copia che `_build/statici.py` rifà a ogni build: i dati e le schede vengono da `Dati/` e `Schede/` alla radice
del repository, il progetto uv dei corsisti, i loro README e le impostazioni di VS Code da `_build/aula/`, le cartelle
`demo/` ed `esercizio/` da `_build/src/script_uv_ruff/`. Le regole di scrittura stanno in `_build/docs/`:
`STILE.md` descrive la prosa, con esempi prima e dopo, `REGOLE.md` la struttura dei notebook, i quattro posti degli
esercizi e, nella sezione "La cartella dell'aula", le cartelle dei corsisti e come si mantengono, `HANDS_ON.md` il
piano degli Hands-on per notebook, `PIANO_OTTOBRE_2026.md` le decisioni di questa edizione e `REQUISITI.md` le scelte
prese con il docente. Gli Hands-on, d'ora in poi, sono da due a tre per notebook, solo dove servono e sono rilevanti,
con un massimo di cinque.

Il file `CLAUDE.md` nella radice del repository riassume il ciclo di lavoro per chi usa un agente per il coding, e la
skill `corso-notebook` in `.claude/skills/` lo descrive passo per passo. Dopo ogni modifica si esegue
`uv run python _build/controlla.py NN`, che ricostruisce i notebook indicati, segnala le celle fuori stile ed esegue
soluzioni e versione studente, e che a ogni giro controlla anche le copie nelle aule, il `uv.lock` dei corsisti e le
segnalazioni di Ruff attese sugli script della dimostrazione e dell'esercizio; poi si rilegge il risultato con
`_build/leggi.py`. Chi cambia il codice della dimostrazione o dell'esercizio aggiorna insieme `AVVISI_INIZIALI` in
`controlla.py`, il notebook `Ambiente_script_e_Ruff`, l'Esercitazione 1 dell'Avanzata e la sezione "La dimostrazione
dal vivo" di questa guida. Gli zip per i corsisti si preparano con `uv run python _build/esporta.py`, e quelli di
aggiornamento con l'opzione `--moduli 3 4`, come descritto all'inizio di questa guida.
