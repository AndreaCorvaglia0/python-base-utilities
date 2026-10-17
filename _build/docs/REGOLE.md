# Regole del materiale 2026 (struttura, volume, dominio)

Si legge insieme a REQUISITI.md (le richieste del docente) e al REGOLE.md (formato e API del toolkit).

## Voce (sostituita da STILE.md, ottobre 2026: leggere quello)
- Prosa da libro tecnico o blog tecnico che spiega come si fa una cosa: paragrafi di 2-5 frasi complete e legate,
  che dicono che cosa fa lo strumento, a cosa serve e cosa mostra la cella sotto. Curata, fluida, senza nessuna frase
  ad effetto: niente antitesi, slogan, metafore, domande retoriche, triadi, "davvero", "che contano".
- Il modello è la prosa del docente nei notebook originali. Niente celle etichetta ("Esempio:"), niente catene di due
  punti, niente frasi telegrafiche in sequenza, niente elenchi con grassetto in testa al posto della spiegazione.
- Il testo parla al corsista, mai del corso visto da chi lo organizza: niente "il docente", "l'aula", "la
  correzione" nei notebook; le note per il docente stanno nella Guida (vedi STILE.md, "A chi parla il testo").
- Titoli descrittivi e piatti. Commenti di codice brevi; `# Output: ...` ammesso. "Noi" quando lavoriamo, impersonale
  per le regole, "tu" nelle consegne. Italiano con il gergo in inglese dove si usa in inglese.

## Volume
- Una cella di testo: un paragrafo di 2-5 frasi (40-90 parole), uno per cella di codice che introduce. Due celle di
  testo adiacenti sullo stesso codice si fondono. Niente box Ricorda. Box ammessi con parsimonia: Attenzione (rosso,
  raro), Esercizio/Hands-on (verde), Soluzione (azzurro); Nota e Approfondimento sono citazioni.
- Hands-on inline: da due a cinque per notebook, con verifica. Sezione Extra in fondo: 2-3 esercizi brevi, uno può essere
  facoltativo; ogni esercizio ha una `verifica=` con 1-3 assert (nel notebook: `verifica("7.1")`).
- Un esercizio per concetto nel corso: le f-string hanno un solo esercizio (01).

## Dove stanno gli esercizi e a cosa servono (decisioni di ottobre 2026)

Il corso ha quattro posti per il codice scritto dal corsista, e ciascuno ha una funzione diversa. Un esercizio scritto
nel posto sbagliato è sbagliato anche se è buono.

- **Hands-on dentro il notebook.** Sono il primo contatto con un concetto appena mostrato: piccoli, inline, subito dopo
  l'esempio che riprendono, e consistono nel cambiare qualcosa nel codice appena visto o nel ripetere lo stesso gesto su
  un dato diverso (un altro indice, un'altra chiave, un altro parametro), con una verifica. Non sono un compito
  completo e non introducono niente di nuovo: servono a mettere le mani sul codice e a fissare la memoria dei concetti
  che torneranno nei notebook seguenti e nel leggere codice scritto da un'AI. Da due a cinque per notebook, in
  proporzione alla lunghezza e al peso del notebook, ciascuno da uno a tre minuti. Possono chiudersi con una riga
  facoltativa "prova anche", sempre banale. Il nome è Hands-on; "Prova tu" non si usa più.
- **Extra in fondo al notebook.** Una sezione finale, che in aula si salta e che chi vuole fa a casa, con due o tre
  esercizi brevi che ripassano i punti principali del notebook. Il materiale del vecchio Homework, dove è fatto bene, si
  riusa qui. Non si contano nei tempi del notebook.
- **Esercitazioni di fine modulo.** L'ora strutturata (45 minuti di lavoro, 15 di correzione) in cui si fa un compito
  intero: cinque esercizi del nucleo, varianti Base e Avanzata, suggerimenti nascosti, soluzione per esercizio,
  domande di riepilogo in apertura. Il nucleo è fatto dagli esercizi scritti dal docente nel branch `main`, adattati al
  formato: la 1 usa i cinque esercizi dei notebook 01 e 02 originali (massimo, minimo e differenza; area del cerchio;
  lista invertita; posizioni pari; capitali del G8) e non ha facoltativi; la 2 usa i tre esercizi sulle funzioni del
  notebook 03 originale più esercizi di import (CSV, Excel, SQL, API per l'Avanzata) scritti nello stesso stile; la 3
  usa i cinque esercizi pandas del notebook 04 originale (dataset degli ascolti) più quelli sulle serie temporali del
  notebook 06 originale. Gli esercizi che il docente aveva messo dentro i notebook e che ora stanno nelle esercitazioni
  vanno sostituiti nei notebook da Hands-on nuovi.
- **Homework.** Non è più un'attività prevista: resta un notebook di riserva fuori dalle cartelle `Aula_*`, da usare
  solo se una classe è molto più veloce del previsto.
- **Capstone.** La giornata 4: passi guidati su un caso reale, con livelli diversi per le due aule e il supporto di
  Copilot. Lì il corsista costruisce un'analisi intera e i passi sono più lunghi.

Le regole di questo documento sulla difficoltà (tutta in Python), sull'apertura con il risultato e sulle richieste
motivate valgono in tutti e quattro i posti; cambiano la lunghezza e lo scopo.

## Esercizi: la difficoltà sta in Python
- Un esercizio allena quello che si è appena visto, uno a uno con la teoria, a livello basilare. La difficoltà è tutta
  in Python: nessun calcolo da impostare, nessuna nozione di matematica oltre le quattro operazioni, nessuna
  conversione di unità, nessun ragionamento articolato sullo scenario. Se il corsista deve pensare al problema prima
  che al codice, l'esercizio è sbagliato.
- I numeri e le operazioni entrano di passaggio dentro esercizi sulle strutture dati, sulle stringhe o sui dati:
  una somma, una divisione, un arrotondamento, non un conto da impostare.
- Ogni esercizio, pur semplice, è pensato per toccare più punti della teoria (per esempio un dizionario, un suo
  metodo e una funzione di Python), in modo che rifare l'esercizio significhi ripassare la lezione.

## Esercizi: prima il risultato, poi i passi
- Un esercizio si apre con un paragrafo che dice che cosa vogliamo ottenere e perché conviene farlo in Python, nei
  termini dello scenario: il messaggio che si rigenera quando cambia il numero degli invitati, la lista che si sistema
  senza riscriverla, il file che un collega apre in Excel. Chi legge deve capire che cosa sta costruendo, e trovarlo
  sensato anche in un caso gioco, prima di leggere qualunque passo; da quel paragrafo deve poter arrivare al risultato
  da solo. Quando il risultato è breve, il paragrafo lo dice (il testo del messaggio, il valore del totale).
- I passi numerati sono un aiuto facoltativo: stanno nel blocco "Passo per passo", che si apre con un clic, e dopo di
  loro vengono i suggerimenti e la soluzione a richiesta. L'ordine di lettura è obiettivo, passi, suggerimenti,
  soluzione, e ogni livello aggiunge dettagli senza ripetere il precedente.
- Ogni richiesta ha un motivo nello scenario. Non si chiede un `int()`, un `len()` o un `type()` perché "fa
  esercizio": se non c'è una ragione che il corsista riconosce (un SMS ha 160 caratteri, il negozio vende confezioni
  intere), la richiesta si toglie o si cambia.
- Il modello per la narrativa e il tono sono gli esercizi scritti dal docente nel branch `main`, per esempio quelli dei
  notebook 02-04: un obiettivo detto in una frase, uno scenario credibile, niente di superfluo. Se ne prende lo
  spirito, non la forma.

## Dominio
- Esempi e esercizi semplici in scenari comuni (spesa, viaggi, voti, ricette, sport, meteo, biblioteca, negozio, musica).
- Energia/utility solo con dati veri (Terna, TexasTurbine, U.S. Electricity Prices, Open-Meteo, sensori Lombardia) e nei
  dataset inventati già esistenti usati da pandas in poi (letture POD, impianti FV, bolletta, utility.db, prezzi zonali,
  Homework). Negli esercizi di sintassi (00-05) niente POD, kWh, bollette, fasce.

## Struttura
- Testata piana (ottobre 2026): H1, una riga con tempo e dati, "In questo notebook impariamo a" con 3 obiettivi. Niente box,
  niente intento. Indice solo se il notebook ha almeno 50 celle. Sezioni numerate. Ultima sezione "Esercizi". Chiusura con
  link precedente/prossimo e, in piccolo, blocco · giornata · aula.
- Colore solo per Esercizio/Hands-on (verde), Soluzione (azzurro), Attenzione (rosso, tre in tutto il corso). Nota e
  Approfondimento sono citazioni (`>`). Ogni notebook punta alla sua Scheda con "Riassunto in una pagina: [...]".
- Dimostrazioni del docente (VS Code, kernel, ambiente/uv, script, Ruff, Data Wrangler, wrapper API): NIENTE nel
  notebook. Stanno in `Extra/` e nella `Guida_docente.md`.
- Due aule dallo stesso sorgente: Avanzata aggiunge le parti (A); Base non vede buchi.
- Il materiale deve reggere da solo dopo il corso: quello che si rilegge a settembre è scritto, in breve.

## Margine (ottobre 2026)
- Il percorso principale sta in 340-360 minuti per giornata su 420: il resto è margine per installazioni, domande, pause.
- Il materiale secondario sta in `Approfondimenti_1/2` (num A1/A2, `fuori_programma=True`): fuori dalla catena
  precedente/prossimo, con esercizi e soluzioni, da aprire se la classe è avanti. Non si aggiungono sezioni facoltative
  dentro i notebook del percorso: quello che è facoltativo sta negli Approfondimenti o è un esercizio (facoltativo).
