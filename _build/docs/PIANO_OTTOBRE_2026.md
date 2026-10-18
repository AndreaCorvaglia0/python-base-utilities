# Piano dell'edizione di ottobre 2026

Questo documento raccoglie le decisioni prese con il docente per l'edizione di ottobre 2026 e prevale sui documenti
precedenti dove li contraddice. La sequenza degli argomenti è quella della proposta di programma, riportata in
`PROPOSTA_PROGRAMMA_2026.md`, che il docente considera per lo più corretta. Le regole di scrittura restano quelle di
`STILE.md` e `REGOLE.md`.

## Date e formato

Il corso si svolge in quattro giornate, una per modulo:

| Giornata | Data | Modulo |
|---|---|---|
| 1 | martedì 20 ottobre 2026 | Modulo 1 · Setup, Python e sintassi di base |
| 2 | mercoledì 21 ottobre 2026 | Modulo 2 · Controllo del flusso, funzioni e primi dati in pandas |
| 3 | martedì 27 ottobre 2026 | Modulo 3 · Analisi dei dati con pandas |
| 4 | mercoledì 28 ottobre 2026 | Modulo 4 · Agenti per il coding e capstone |

In ogni giornata l'aula Base occupa le prime quattro ore e l'aula Avanzata le quattro successive, sullo stesso modulo.
Ogni blocco di quattro ore contiene almeno due pause da 15 minuti. L'homework non è più un'attività prevista e resta
come riserva in `Riserva/`.

## La struttura di un modulo

I moduli 1, 2 e 3 si chiudono con l'esercitazione, che occupa l'ultima ora del blocco: 45 minuti di lavoro dei
corsisti e 15 minuti in cui il docente mostra le soluzioni. L'esercitazione è un momento strutturato, di durata nota a
tutti, e serve da riepilogo della giornata. Il resto del blocco, tolte le due pause e l'ora di esercitazione, lascia
circa 150 minuti di lezione, e il contenuto di ogni modulo va dimensionato su questo spazio con un margine.

Dentro i notebook restano soltanto gli Hands-on, piccoli esercizi inline subito dopo l'esempio che riprendono, che danno
una pratica immediata dopo ogni concetto e preparano le esercitazioni: da due a tre per notebook, solo dove servono e
sono rilevanti, con un massimo di cinque. In fondo a ogni notebook, tranne il capstone e `Ambiente_script_e_Ruff`, una
sezione Extra raccoglie due o tre esercizi brevi da fare a casa, che in aula si saltano; il vecchio Homework resta come
riserva fuori dalle cartelle dei corsisti. Le esercitazioni sono costruite sugli esercizi scritti dal docente nei
notebook originali: la 1 interamente, le altre con esercizi aggiunti nello stesso stile. La sezione "Dove stanno gli
esercizi" di `REGOLE.md` descrive la funzione di ciascun posto.

Il modulo 4 è dedicato interamente agli agenti per il coding e al capstone con GitHub Copilot. Si apre con il notebook
09 su Plotly, ridotto al minimo che serve per leggere un grafico scritto da un agente, prosegue con l'introduzione a
Copilot (notebook 10) e con il capstone (notebook 11), il cui ultimo step è aperto: sui dati del capstone i corsisti
chiedono a Copilot grafici e tabelle che li interessano e controllano quello che scrive. Il capstone ha livelli di
richiesta diversi per le due aule; nella Base il codice per l'API della temperatura è già predisposto.

## Base e Avanzata

Il materiale delle due aule deve restare il più simile possibile, perché il docente prepara un solo percorso. Le due
aule seguono gli stessi moduli e gli stessi temi: la Base dedica più tempo alle introduzioni e al consolidamento e fa
esercizi più semplici, più guidati o in numero minore; l'Avanzata usa il tempo che guadagna per gli argomenti (A).

Gli argomenti in più dell'Avanzata vanno collocati in modo che, alla fine di ogni giornata, le due aule siano allineate
e il modulo successivo parta dallo stesso punto per entrambe. Nel modulo 1, mentre la Base dedica più tempo alle
introduzioni, l'Avanzata affronta gli script `.py`, gli ambienti virtuali con uv e Ruff, e la sua Esercitazione 1 è
dedicata a questi temi; in questo modo il giorno dopo il modulo 2 comincia per entrambe dal notebook 04. Il materiale
è descritto nella sezione "Script, uv e Ruff nell'aula Avanzata".

## Le cartelle dei corsisti

Il corsista riceve solo la propria cartella, `Aula_Base/` o `Aula_Avanzata/`, come zip preparato da
`_build/esporta.py`. La cartella funziona da sola: contiene il progetto uv dei corsisti (il `pyproject.toml` del
progetto `corso-python`, uguale per le due aule, con `uv.lock` e `.python-version`), il README per il corsista, le
impostazioni di VS Code, i dati, le tre schede, i moduli da `Modulo_1` a `Modulo_4` e la cartella `Soluzioni/`, con le
soluzioni di tutti i notebook a disposizione dal primo giorno. Il materiale del docente, cioè le dimostrazioni di
`Extra/` e la riserva di `Riserva/`, resta nel repository; la riserva, quando serve, si consegna con uno zip a parte,
preparato con `esporta.py <aula> --riserva`. Gli zip si mandano completi prima della prima giornata. Se i moduli 3 e 4
cambiano, la settimana successiva se ne manda un aggiornamento preparato con `esporta.py --moduli 3 4`, che contiene
soltanto quei due moduli con le loro soluzioni, i dati e le schede, e quindi non sovrascrive i notebook dei moduli 1 e
2, in cui i corsisti hanno già scritto le loro risposte. La sezione "La cartella dell'aula" di `REGOLE.md` descrive
com'è fatta la cartella, come si mantiene e come si estraggono gli zip parziali.

## Le esercitazioni

Ogni esercitazione ha un minimo di narrativa: un filo conduttore semplice che lega gli esercizi, senza diventare una
storia complicata. Il dominio segue la regola già in uso: nei temi di sintassi gli esempi sono di vita quotidiana e non
riguardano le utility; i dati del settore energetico compaiono da pandas in poi. L'esercitazione 1 è quindi di vita
quotidiana, mentre la 2 può usare i dataset del corso nella parte su pandas e la 3 lavora sui dati di carico.

Le esercitazioni devono funzionare per classi eterogenee:

1. I primi esercizi sono molto semplici o molto guidati, e la difficoltà cresce gradualmente.
2. La difficoltà è sempre e soltanto in Python: nessun calcolo da impostare, nessuna nozione di matematica, nessun
   ragionamento articolato sullo scenario. Numeri e operazioni entrano di passaggio dentro gli esercizi sulle
   strutture dati; ogni esercizio applica uno a uno la teoria appena vista e tocca più punti insieme.
3. Ogni esercizio si apre dicendo che cosa vogliamo ottenere e perché conviene farlo in Python, in modo che il
   corsista sappia che cosa sta costruendo prima di leggere i passi e possa arrivarci anche da solo; i passi numerati
   sono facoltativi e si aprono con un clic, poi vengono i suggerimenti e la soluzione. Ogni richiesta ha un motivo
   nello scenario, altrimenti si toglie.
4. Dopo il nucleo comune vengono gli esercizi facoltativi, per chi finisce prima. Anche questi non sono mai difficili:
   sono sempre l'applicazione diretta di quello che si è appena visto, perché il corso resta un corso di base.
5. Ogni esercizio del nucleo ha suggerimenti facoltativi, nascosti finché il corsista non li apre: due livelli nella
   Base (prima l'idea, poi il nome della funzione o del metodo), al massimo uno nell'Avanzata. Si realizzano con un
   blocco `<details>` dentro la cella Markdown, da provare una volta in VS Code sui PC dell'aula.
6. Le soluzioni sono accessibili un esercizio alla volta, con una cella `soluzione("E1.3")` sotto ogni esercizio che
   mostra soltanto quella soluzione. Le soluzioni stanno in `corso.py` accanto alle verifiche, codificate in modo
   leggero perché aprendo il file non si leggano per caso. Il notebook completo delle soluzioni è nella cartella
   `Soluzioni/` dell'aula, a disposizione dal primo giorno (decisione del 18 ottobre).
7. Gli esercizi non dipendono l'uno dall'altro: ciascuno parte dai propri dati. Quando un passo ha bisogno di un
   risultato precedente, una cella di recupero lo ricrea, così chi si blocca può proseguire.
8. Base e Avanzata fanno lo stesso esercizio in due varianti, come già nel capstone: stessa consegna e stessa verifica,
   con più codice già scritto e più suggerimenti nella Base, una cella quasi vuota e talvolta un requisito in più
   nell'Avanzata. Nella Base alcuni esercizi possono essere più semplici o mancare del tutto.

Le domande di riepilogo che aprono l'esercitazione sono un controllo rapido di pochi concetti: dirette, con una
risposta breve e senza sottigliezze (il tipo restituito da una divisione, per esempio, non è un tema del corso). Se un
concetto è piccolo, due domande si possono fondere in una.

Il testo delle esercitazioni, come tutto il materiale, parla al corsista e non descrive l'ora dal punto di vista
del docente: le indicazioni per la correzione stanno nella `Guida_docente.md`.

Il corsista in difficoltà ha quindi una sequenza di aiuti: il messaggio della verifica, il primo suggerimento, il
secondo, la soluzione di quel passo e infine il docente. Chi è più avanti finisce senza suggerimenti e prosegue con
gli esercizi facoltativi. La correzione dei 15 minuti finali riguarda solo il nucleo comune.

Nella proposta l'aula Base ha anche esercitazioni aggiuntive su lettura e scrittura di file e sui database: trovano
posto nell'esercitazione 2. Il wrapper delle API dell'aula Avanzata è indicato nella proposta come esercizio, e può
diventare la parte Avanzata della stessa esercitazione.

L'esercitazione 1 è stata costruita per prima, come pilota del formato con suggerimenti, soluzioni per passo e le due
varianti, e la 2 e la 3 ne seguono lo stesso formato. Nell'aula Avanzata la 1 è diventata poi l'esercizio sullo
script, descritto nella sezione seguente.

## Script, uv e Ruff nell'aula Avanzata

La richiesta del docente, con le sue parole:

> alla fine del modulo 1 fatto abbastanza veloce con gli avanzati. Hanno già usato uv sync all'inizio. Ora dobbiamo
> spiegare meglio cosa è e come funziona uv, il concetto di virtual environment con vantaggi, i file principali. Poi
> la differenza tra notebook e script e i vantaggi dello script, importare una funzione da script per comprendere
> meglio gli import da libreria. parliamo di ruff introducendo cosa è un formatter e cosa significa formattare (anche
> se lo hanno visto in PEP8 etc quindi va be facciamo leva su quello. e poi parliamo del linter idem e diciamo che
> ruff fa entrambi e capiamo come fare ad usarlo. dunque serve un notebook di spiegazione di questi concetti (come la
> scheda per intenderci, più completa sugli argomenti, ma abbastanza superficiale tanto ci parlo sopra, magari metti
> nel mio materiale da docente cosa raccontare, scegli ovviamente le cose più usate in assoluto nel contesto
> dell'analisi dati e per dei principianti, astrai la complessità un po' pur rimanendo tecnico e preciso). Io
> mostrerò un esempio (output: uno script che esegue una funzione importata da un altro script, sistemato con ruff e
> con una virtual env apposito costruito aggiungendo una libreria alla volta a mano a mano che ci accorgiamo che
> manca. Il codice può essere già scritto e opzionalmente integrabile con dei print o cose basilarissime viste nel
> modulo 1, finendo col runnarlo). La loro esercitazione è rifarlo dopo di me in una cartella riservata
> all'esercitazione e in cui devono fare delle cose perfettamente equivalenti con qualche extra come dicevamo di
> aggiunta di print in punti diversi opzionale. Molto guidato da un notebook di istruzioni.

Il materiale sta nella sottocartella `Modulo_1/Script_uv_Ruff/` della sola Avanzata e ha tre parti. Il notebook di
spiegazione `Ambiente_script_e_Ruff`, che segue il 03, presenta in modo semplice ma preciso che cosa fa uv e a che
cosa serve un ambiente virtuale, i file del progetto, la differenza tra notebook e script, l'import di una funzione da
un altro file come chiave per capire gli import delle librerie, il formatter (a partire da PEP 8, già visto nel 03),
il linter e Ruff, che fa entrambe le cose. Non ha Hands-on né Extra, perché la pratica è l'esercitazione, e le note su
che cosa raccontare stanno nella `Guida_docente.md`. La cartella `demo/` è il punto di partenza della dimostrazione dal
vivo, che i corsisti ricevono per poterla seguire sul proprio PC: lo script `main.py` usa le funzioni di `calcoli.py`
sul conto della spesa, l'ambiente si costruisce una libreria alla volta, man mano che lo script si ferma perché ne
manca una (prima pandas, poi openpyxl, che pandas usa per scrivere il file Excel ma non installa), e il codice, scritto
apposta in disordine, si sistema con `ruff format`, con `ruff check --fix` e con due correzioni a mano. La cartella
`esercizio/` contiene un programma equivalente sulle temperature della settimana (`meteo.py` e `main.py`), con gli
stessi errori nello stesso ordine. Gli stati finali dei due progetti stanno in `Soluzioni/Script_uv_Ruff/`.

L'Esercitazione 1 dell'Avanzata dura sempre 60 minuti, 45 di lavoro e 15 di correzione, ed è soltanto la parte sullo
script: i corsisti rifanno la dimostrazione nella cartella `esercizio/`, guidati passo per passo dal notebook
`Modulo_1/Esercitazione_1.ipynb`, con alcuni passi facoltativi che aggiungono `print` in punti diversi (la temperatura
minima, un `print` nel file importato, il valore di `__name__`) e la ricostruzione dell'ambiente con `uv sync`. Gli
esercizi classici dell'Esercitazione 1 restano in fondo allo stesso notebook, facoltativi, da fare a casa; la Base fa
l'Esercitazione 1 di sempre. Esercizi in più su uv, script e Ruff, per una classe che va avanti, stanno in un notebook
di riserva in `Riserva/Avanzata/`, fuori dalla cartella dei corsisti, e quando servono si consegnano con uno zip a
parte, preparato con `esporta.py avanzata --riserva`. La scheda su uv e gli script non c'è più, perché il notebook la
sostituisce.

## L'homework

L'homework, la settimana nell'ufficio Analisi Consumi, era pensato per la settimana tra il modulo 2 e il modulo 3.
Con le sezioni Extra in fondo ai notebook non è più un'attività prevista: resta in `Riserva/Base/` e
`Riserva/Avanzata/`, nel formato delle esercitazioni, da distribuire con `esporta.py <aula> --riserva` solo a una
classe molto più veloce del previsto. I suoi passi migliori sono già riusati nelle sezioni Extra dei notebook 04 e 06.

## Argomenti facoltativi

Ogni modulo conserva alcuni argomenti facoltativi, da usare se il modulo procede particolarmente veloce. Restano nei
notebook `Approfondimenti_1` e `Approfondimenti_2` e non entrano nel tempo pianificato.

## Differenze tra il materiale e la proposta

Il materiale era stato costruito su due giornate; con la riorganizzazione sui quattro moduli le differenze con la
proposta sono queste, con la scelta fatta per ciascuna.

| Argomento | Proposta | Materiale di ottobre 2026 |
|---|---|---|
| Ambienti virtuali, uv, script `.py`, Ruff | (A) nel modulo 1 | sola Avanzata, modulo 1: notebook `Ambiente_script_e_Ruff`, dimostrazione dal vivo in `demo/`, Esercitazione 1 in `esercizio/` |
| `map`, `filter`, iterabili e generatori | (A) nel notebook 04 | restano facoltativi, in `Approfondimenti_1` |
| Wrapper delle API | (A) con esercizi nel notebook 06 | esercizio facoltativo dell'Avanzata nell'Esercitazione 2 |
| Più file CSV e tipi di dato | entrambe le aule, notebook 06 | in `Approfondimenti_1` |
| `.query()` | entrambe le aule, notebook 07 | solo Avanzata |
| Indici, `agg` | entrambe le aule, notebook 07 | indice a due colonne e `agg` solo Avanzata |
| Differenze tra date, fuso orario | entrambe le aule, notebook 08 | restano facoltativi, in `Approfondimenti_2` |
| Resampling | (A) nel notebook 08 | entrambe le aule, perché il capstone Base aggrega per giorno |
| `shift` e `rolling` | (A) nel notebook 08 | Avanzata, in `Approfondimenti_2` |
| Slider, range selector, export HTML | entrambe le aule, notebook 09 | nel notebook 09, modulo 4 |
| Esercitazioni | non indicate come blocco | tre da 60 minuti sugli esercizi originali del docente; nell'Avanzata la 1 è l'esercizio sullo script e gli esercizi originali restano facoltativi, a casa |
| Forecasting con Prophet | (A) modulo opzionale da confermare | da preparare, dopo la verifica dell'installazione |

## I tempi

Ogni blocco ha 240 minuti: 30 di pause, 60 di esercitazione nei moduli 1-3, e circa 150 di lezione. I tempi dei
notebook sono nei banner e nella `Guida_docente.md`; le sezioni Extra non sono comprese.

| Modulo | Lezione Base | Lezione Avanzata | Nota |
|---|---|---|---|
| 1 | 140 | 150 | l'Avanzata fa più in fretta 00, 01 e 02 e aggiunge `Ambiente_script_e_Ruff` (30); la sua Esercitazione 1 è l'esercizio sullo script |
| 2 | 140 | 150 | l'Avanzata ha la sezione sulle API nel 06, compresa la dimostrazione del wrapper delle API (10, dentro i 70 del 06) |
| 3 | 130 | 135 | compresa la dimostrazione di Data Wrangler (15) |
| 4 | 210 | 210 | 09 (25), 10 (35), capstone (150, di cui 40 per lo step 7 di richieste libere a Copilot); nessuna esercitazione |

Nel modulo 1 la lezione della Base comprende la dimostrazione di VS Code (15), il 00 (25), il 01 (40), il 02 (40) e il
03 (20). Quella dell'Avanzata comprende la dimostrazione di VS Code (15), il 00 (20), il 01 (30), il 02 (35), il 03
(20) e `Ambiente_script_e_Ruff` (30, circa 15 di notebook e 15 di dimostrazione dal vivo). Con le pause e
l'esercitazione l'Avanzata occupa tutti i 240 minuti del blocco, quindi in caso di ritardo si taglia seguendo la
`Guida_docente.md`.

## Decisioni prese

- **Modulo 3.** Il notebook 09 su Plotly passa all'inizio del modulo 4, con slider, range selector ed export HTML, e
  la finestra con gli agenti riprende Plotly subito dopo. Nel modulo 3 restano i notebook 07 e 08; le differenze tra
  date e il fuso orario restano facoltativi, negli Approfondimenti.
- **Modulo 2 dell'Avanzata.** Il wrapper delle API diventa la parte Avanzata dell'esercitazione 2. `map`, `filter` e
  i generatori restano facoltativi, in `Approfondimenti_1`.
- **Forecasting.** Si prepara un breve notebook facoltativo su Prophet per l'aula Avanzata, da usare nel modulo 4 solo
  se il capstone finisce in anticipo. Prima di scriverlo va verificato che `prophet` si installi con `uv add` sui PC
  dell'aula, perché dipende da un compilatore per i modelli statistici.
- **Cartelle dei corsisti (18 ottobre 2026).** Il corsista riceve solo la propria cartella `Aula_Base/` o
  `Aula_Avanzata/`, che funziona da sola e ha come primo livello `Modulo_1` … `Modulo_4`; le soluzioni di tutti i
  notebook sono a disposizione da subito, nella cartella `Soluzioni/`, separata dai moduli. Il progetto uv dei
  corsisti si chiama `corso-python` ed è lo stesso per le due aule.
- **Script, uv e Ruff (18 ottobre 2026).** Nell'Avanzata il modulo 1 ha la sottocartella `Script_uv_Ruff/` con il
  notebook di spiegazione, senza Hands-on né Extra, la cartella `demo/` della dimostrazione, che anche i corsisti
  ricevono per seguirla, e la cartella `esercizio/`. L'Esercitazione 1 dell'Avanzata è l'esercizio sullo script,
  guidato passo per passo e con alcuni passi facoltativi; gli esercizi classici dell'Esercitazione 1 restano nello
  stesso notebook, facoltativi, da fare a casa, e la Base non cambia. Il terminale di VS Code non attiva l'ambiente del
  corso, per evitare l'avviso `VIRTUAL_ENV` di uv nelle cartelle della dimostrazione e dell'esercizio. Ruff si lancia
  soltanto da un terminale aperto in `demo/` o in `esercizio/`, e la configurazione del progetto del corso esclude i
  notebook e i `corso.py`, così né il terminale né l'estensione di VS Code li toccano. La scheda su uv e gli script è
  sostituita dal notebook.
- **Hands-on (18 ottobre 2026).** Gli Hands-on, d'ora in poi, sono da due a tre per notebook, solo dove servono e sono
  rilevanti, con un massimo di cinque; i notebook che ne hanno di più non si riducono ora. Gli esercizi in più su uv,
  script e Ruff non diventano Hands-on.
- **Riserva e consegne (18 ottobre 2026).** Gli esercizi in più su uv, script e Ruff stanno in `Riserva/Avanzata/` e
  si consegnano, quando servono, con `esporta.py avanzata --riserva`. Gli zip completi si mandano prima della prima
  giornata, e l'eventuale aggiornamento dei moduli 3 e 4, da mandare la settimana successiva, si prepara con
  `esporta.py --moduli 3 4`.

## Ancora da fare

- Il notebook facoltativo su Prophet per l'Avanzata, dopo aver verificato che `uv add prophet` funzioni sui PC
  dell'aula.
- La prova in VS Code sui PC dell'aula dei blocchi che si aprono con un clic, della riga rossa della verifica e del
  codice colorato di `soluzione()`.
- La verifica che i PC dell'aula raggiungano PyPI, perché nella dimostrazione e nell'esercizio `uv add` risolve e
  scarica le librerie dalla rete.
- La prova, su un PC dell'aula, dell'aggiornamento dei moduli 3 e 4 preparato con `esporta.py --moduli 3 4`.
