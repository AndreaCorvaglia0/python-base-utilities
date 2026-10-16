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
| 3 | martedì 27 ottobre 2026 | Modulo 3 · Analisi dei dati con pandas e visualizzazione |
| 4 | mercoledì 28 ottobre 2026 | Modulo 4 · Agenti per il coding e capstone |

In ogni giornata l'aula Base occupa le prime quattro ore e l'aula Avanzata le quattro successive, sullo stesso modulo.
Ogni blocco di quattro ore contiene almeno due pause da 15 minuti. L'homework cade nella settimana tra il 21 e il 27,
quindi si presenta alla fine del modulo 2 e si corregge all'inizio del modulo 3.

## La struttura di un modulo

I moduli 1, 2 e 3 si chiudono con l'esercitazione, che occupa l'ultima ora del blocco: 45 minuti di lavoro dei
corsisti e 15 minuti in cui il docente mostra le soluzioni. L'esercitazione è un momento strutturato, di durata nota a
tutti, e serve da riepilogo della giornata. Il resto del blocco, tolte le due pause e l'ora di esercitazione, lascia
circa 150 minuti di lezione, e il contenuto di ogni modulo va dimensionato su questo spazio con un margine.

Gli esercizi in fondo ai notebook restano nei notebook, ma escono dal tempo d'aula: servono come pratica dopo la
lezione e come serbatoio da cui le esercitazioni attingono. I Prova tu dentro i notebook restano in aula, perché danno
una pratica immediata dopo ogni concetto.

Il modulo 4 è dedicato interamente agli agenti per il coding e al capstone con GitHub Copilot. Dopo l'introduzione a
Copilot e ai concetti di base (notebook 10) e il capstone (notebook 11), la giornata prevede una finestra in cui i
corsisti esplorano con gli agenti Plotly, selezioni ed elaborazioni avanzate sui DataFrame pandas, sempre lavorando
attraverso l'agente. Il capstone ha livelli di richiesta diversi per le due aule; nella Base il codice per l'API della
temperatura è già predisposto.

## Base e Avanzata

Il materiale delle due aule deve restare il più simile possibile, perché il docente prepara un solo percorso. Le due
aule seguono gli stessi moduli e gli stessi temi: la Base dedica più tempo alle introduzioni e al consolidamento e fa
esercizi più semplici, più guidati o in numero minore; l'Avanzata usa il tempo che guadagna per gli argomenti (A).

Gli argomenti in più dell'Avanzata vanno collocati in modo che, alla fine di ogni giornata, le due aule siano allineate
e il modulo successivo parta dallo stesso punto per entrambe. Nel modulo 1, mentre la Base dedica molto tempo alle
introduzioni, l'Avanzata affronta gli script `.py`, gli ambienti virtuali con uv e Ruff; in questo modo il giorno dopo
il modulo 2 comincia per entrambe dal notebook 04. Per questo i notebook `Extra/Ambiente_uv_e_script` ed
`Extra/Ruff`, oggi dimostrazioni del docente, diventano lezione dell'aula Avanzata nel modulo 1.

## Le esercitazioni

Ogni esercitazione ha un minimo di narrativa: un filo conduttore semplice che lega gli esercizi, senza diventare una
storia complicata. Il dominio segue la regola già in uso: nei temi di sintassi gli esempi sono di vita quotidiana e non
riguardano le utility; i dati del settore energetico compaiono da pandas in poi. L'esercitazione 1 è quindi di vita
quotidiana, mentre la 2 può usare i dataset del corso nella parte su pandas e la 3 lavora sui dati di carico.

Le esercitazioni devono funzionare per classi eterogenee:

1. I primi esercizi sono molto semplici o molto guidati, e la difficoltà cresce gradualmente.
2. Dopo il nucleo comune vengono gli esercizi facoltativi, per chi finisce prima. Anche questi non sono mai difficili:
   sono sempre l'applicazione diretta di quello che si è appena visto, perché il corso resta un corso di base.
3. Ogni esercizio del nucleo ha suggerimenti facoltativi, nascosti finché il corsista non li apre: due livelli nella
   Base (prima l'idea, poi il nome della funzione o del metodo), al massimo uno nell'Avanzata. Si realizzano con un
   blocco `<details>` dentro la cella Markdown, da provare una volta in VS Code sui PC dell'aula.
4. Le soluzioni sono accessibili un esercizio alla volta, con una cella `soluzione("E1.3")` sotto ogni esercizio che
   mostra soltanto quella soluzione. Le soluzioni stanno in `corso.py` accanto alle verifiche, codificate in modo
   leggero perché aprendo il file non si leggano per caso. Il notebook completo delle soluzioni si distribuisce dopo
   la correzione.
5. Gli esercizi non dipendono l'uno dall'altro: ciascuno parte dai propri dati. Quando un passo ha bisogno di un
   risultato precedente, una cella di recupero lo ricrea, così chi si blocca può proseguire.
6. Base e Avanzata fanno lo stesso esercizio in due varianti, come già nel capstone: stessa consegna e stessa verifica,
   con più codice già scritto e più suggerimenti nella Base, una cella quasi vuota e talvolta un requisito in più
   nell'Avanzata. Nella Base alcuni esercizi possono essere più semplici o mancare del tutto.

Il corsista in difficoltà ha quindi una sequenza di aiuti: il messaggio della verifica, il primo suggerimento, il
secondo, la soluzione di quel passo e infine il docente. Chi è più avanti finisce senza suggerimenti e prosegue con
gli esercizi facoltativi. La correzione dei 15 minuti finali riguarda solo il nucleo comune.

Nella proposta l'aula Base ha anche esercitazioni aggiuntive su lettura e scrittura di file e sui database: trovano
posto nell'esercitazione 2. Il wrapper delle API dell'aula Avanzata è indicato nella proposta come esercizio, e può
diventare la parte Avanzata della stessa esercitazione.

Il primo passo è un'esercitazione pilota, la numero 1, costruita in questo formato con suggerimenti, soluzioni per
passo e le due varianti. Il docente la prova, si sistema il formato e poi si costruiscono la 2 e la 3.

## Argomenti facoltativi

Ogni modulo conserva alcuni argomenti facoltativi, da usare se il modulo procede particolarmente veloce. Restano nei
notebook `Approfondimenti_1` e `Approfondimenti_2` e non entrano nel tempo pianificato.

## Differenze tra il materiale attuale e la proposta

Il materiale è stato costruito su due giornate e in alcuni punti si discosta dalla proposta. Queste sono le differenze
da risolvere quando si riorganizza il corso sui quattro moduli.

| Argomento | Proposta | Materiale attuale |
|---|---|---|
| Ambienti virtuali, uv, script `.py`, Ruff | (A) nel modulo 1 | dimostrazioni del docente in `Extra/` |
| `map`, `filter`, iterabili e generatori | (A) nel notebook 04 | Avanzata, in `Approfondimenti_1` |
| Wrapper delle API | (A) con esercizi nel notebook 06 | dimostrazione in `Extra/API_wrapper` |
| Più file CSV e tipi di dato | entrambe le aule, notebook 06 | in `Approfondimenti_1` |
| `.query()` | entrambe le aule, notebook 07 | solo Avanzata |
| Indici, `agg` | entrambe le aule, notebook 07 | indice a due colonne e `agg` solo Avanzata |
| Differenze tra date, fuso orario | entrambe le aule, notebook 08 | in `Approfondimenti_2` |
| Resampling | (A) nel notebook 08 | entrambe le aule, perché il capstone Base aggrega per giorno |
| `shift` e `rolling` | (A) nel notebook 08 | Avanzata, in `Approfondimenti_2` |
| Slider, range selector, export HTML | entrambe le aule, notebook 09 | in `Approfondimenti_2` |
| Esercitazioni | non indicate come blocco | tre da 20 minuti, domande ed esercizi |
| Forecasting con Prophet | (A) modulo opzionale da confermare | non presente |

## Stima del tempo

Le stime partono dai tempi dei notebook nella `Guida_docente.md`, tolti gli esercizi di fine notebook che escono dal
tempo d'aula. Sono stime proporzionali al contenuto, non misure, e vanno ricontrollate quando si riorganizza il
materiale. Ogni blocco ha 240 minuti: 30 di pause, 60 di esercitazione nei moduli 1-3, e circa 150 di lezione.

| Modulo | Lezione Base | Lezione Avanzata | Nota |
|---|---|---|---|
| 1 | circa 115 | circa 125 | l'Avanzata aggiunge uv, script e Ruff; entrambe stanno nei 150 |
| 2 | circa 125 | circa 145-155 | l'Avanzata è al limite se `map`, `filter` e generatori entrano nella lezione |
| 3 | circa 160-175 | circa 170-190 | non sta nei 150 con tutto quello che la proposta elenca |
| 4 | Copilot, capstone e finestra con gli agenti | come la Base, con richieste più ampie | giornata intera |

## Decisioni aperte

- **Modulo 3.** Con l'ora di esercitazione il modulo 3 non contiene i notebook 07, 08 e 09 con tutti gli argomenti
  della proposta. Va deciso che cosa spostare: la proposta più naturale è portare il notebook 09 all'inizio del
  modulo 4, dove la finestra con gli agenti riprende Plotly, e tenere facoltativi alcuni argomenti delle date.
- **Modulo 2 dell'Avanzata.** Va deciso se `map`, `filter` e i generatori entrano nella lezione o restano facoltativi,
  e se il wrapper delle API diventa un esercizio dell'esercitazione 2.
- **Forecasting.** Va deciso se il modulo opzionale su Prophet resta, diventa un esercizio con l'agente nel modulo 4 o
  viene tolto.
- **Documenti da aggiornare.** README, `Guida_docente.md` e slide descrivono ancora due giornate, e vanno riscritti sui
  quattro moduli quando la struttura è definitiva.
