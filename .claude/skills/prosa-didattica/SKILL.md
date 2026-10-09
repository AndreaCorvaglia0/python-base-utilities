---
name: prosa-didattica
description: Scrivere o riscrivere materiale didattico (lezioni, notebook Jupyter, dispense, tutorial, esercizi, schede, README di un corso, note per il docente) con il tono di un manuale tecnico o di un buon blog tecnico che spiega come si fa una cosa, frasi complete e legate, nessuna frase ad effetto. Usare questa skill ogni volta che si produce o si corregge testo destinato a chi impara, in italiano o in un'altra lingua, e in particolare quando qualcuno dice che un testo "sembra scritto da un'AI", è "frammentato", "telegrafico", "sconclusionato", pieno di "frasi ad effetto" o "sembra tradotto male dall'inglese", anche se non nomina la parola "stile".
---

# Prosa didattica: il tono di un manuale tecnico

Questa skill serve a scrivere testo per chi impara una materia tecnica in un registro preciso: quello di un libro
tecnico che presenta un argomento, o di un articolo tecnico ben scritto che spiega come si fa una cosa. Il testo è
curato e scorrevole, informa e non cerca l'attenzione. Il lettore deve poterlo rileggere da solo mesi dopo il corso e
capire, senza il docente accanto, che cosa fa uno strumento, perché si usa e che cosa mostra l'esempio che segue.

La skill riguarda solo il tono e la forma della prosa. Non decide la struttura del corso, il numero di esercizi o il
formato dei file: quelle scelte vengono dal progetto in cui si lavora, e la skill si applica sopra di esse.

## Perché serve

Il testo generato in fretta, da un modello o da una persona che prende appunti, tende a una forma riconoscibile:
frasi brevissime messe in fila, due punti al posto dei verbi, chiusure brillanti, domande retoriche per tenere desta
l'attenzione. Chi legge la percepisce come artificiale o come una traduzione approssimativa dall'inglese, e soprattutto
non riceve la spiegazione: riceve un elenco di affermazioni da ricollegare da solo. Il registro del manuale risolve
entrambi i problemi, perché lega le affermazioni con il loro perché.

## I difetti da riconoscere

Prima di scrivere, e soprattutto prima di correggere un testo esistente, conviene saper riconoscere questi schemi.

1. **Frasi telegrafiche in sequenza.** Tre o quattro frasi di sei parole una dietro l'altra, senza congiunzioni.
   "Il resampling cambia granularità. È un'aggregazione. Si basa sul tempo."
2. **Catene di due punti.** "X: Y, Z." usato al posto di una frase con soggetto e verbo.
   "Restart riavvia il kernel: le variabili spariscono, il codice resta."
3. **Antitesi e chiusure a effetto.** Frasi costruite per suonare bene: "le variabili spariscono, il codice resta",
   "non è magia, è metodo", "il caso noto torna; resta da provare".
4. **Celle o righe etichetta.** Una riga che contiene solo "Unione:", "Esempio:" o "Vediamo:" sopra un blocco di codice.
5. **Domande retoriche e ganci.** "E se volessimo farlo solo su una parte?", "Sembra facile, vero?"
6. **Aperture ripetute** con "Qui", "Ora", "Poi", e imperativi secchi in fila ("Premi Restart. Esegui. Guarda.").
7. **Elenchi con il grassetto in testa al posto della spiegazione.** "1. **Verifica.** Esegui subito." quando il
   contenuto è un ragionamento e non una lista di passi.
8. **Spiegazione annunciata e non data.** Il testo dice che cosa fa il codice ma non perché, né che cosa aspettarsi.
9. **Calchi dall'inglese.** Titoli come "Come si legge un traceback" usati come etichette, "è importante notare che",
   costruzioni nominali ("Gestione degli errori: fondamentale"), virgolette di distanza ("quando 'forzi' una frequenza").

## Le regole

- **Paragrafi, non appunti.** Ogni blocco di testo è un paragrafo di due a cinque frasi complete, di solito tra 40 e
  90 parole, che introduce il concetto, dice a cosa serve o perché conta, e prepara l'esempio che segue. Le frasi si
  legano con "perché", "quindi", "in questo modo", "per esempio", "mentre", "invece".
- **Nessuna frase ad effetto.** Niente antitesi, slogan, massime, metafore, triadi ritmiche, domande retoriche,
  esclamazioni, aggettivi di entusiasmo ("potente", "fondamentale", "incredibile"). Il testo non cerca l'attenzione:
  la dà per scontata e la ripaga con informazioni.
- **Nessuna riga etichetta.** "Unione:" diventa una frase: "L'unione di due set, che si ottiene con `union()`,
  contiene tutti gli elementi presenti in almeno uno dei due, senza ripetizioni."
- **I due punti** introducono un elenco o un esempio, e non saldano due mezze frasi.
- **Istruzioni operative come frasi.** "Per vederlo, premiamo Restart e poi eseguiamo la cella qui sotto" invece di
  una fila di imperativi.
- **Principi e regole in prosa.** Gli elenchi numerati restano per i passi di una procedura, le consegne degli
  esercizi, le domande di un quiz e le enumerazioni vere, come le opzioni di un parametro. Ogni voce di un elenco è
  comunque una frase intera.
- **Le persone.** "Noi" quando si lavora insieme ("costruiamo", "selezioniamo"), la forma impersonale per le regole
  ("si usa", "conviene"), il "tu" solo nelle consegne degli esercizi. Una volta scelto, il registro non cambia a metà.
- **Il risultato atteso è una frase.** Non "Output atteso: 42" ma "Il risultato è 42, cioè ...".
- **Lunghezza giusta.** La regola non è un invito a gonfiare: si spiega una volta, bene, e si passa all'esempio.
  Due blocchi di testo che parlano dello stesso esempio si fondono in uno.
- **Lingua.** Italiano curato, con il gergo tecnico in inglese dove nella pratica si usa in inglese (notebook,
  kernel, DataFrame, slicing, encoding, commit). Niente parentesi che spezzano la frase quando basta una subordinata.
  Le stesse regole valgono per un testo in un'altra lingua: cambiano i connettivi, non il registro.
- **Titoli piatti e descrittivi.** "Selezione dei dati", "Valori mancanti", "Esercizi". Mai titoli con promesse o
  aggettivi ("Le scorciatoie che servono davvero", "In cinque regole").

## Esempi: prima e dopo

**Un concetto con il suo effetto**

Prima: "**Restart**, in cima al notebook, riavvia il kernel: le variabili spariscono, il codice resta. Premi Restart
ed esegui la cella qui sotto: dà `NameError`."

Dopo: "Il pulsante **Restart**, in cima al notebook, riavvia il kernel. Il codice scritto nelle celle rimane dov'è,
ma le variabili create fino a quel momento vengono perse, perché esistevano solo nella memoria del processo appena
chiuso. Per vederlo, premiamo Restart e poi eseguiamo la cella qui sotto, che chiede il valore di `x`: Python
risponde con un `NameError`, perché quel nome non esiste più."

**Appunti tecnici da trasformare in spiegazione**

Prima: "Quando "forzi" una frequenza regolare, i timestamp mancanti diventano righe con `NaN`. Questo è utile: rende
visibili buchi che altrimenti restano nascosti. Qui usiamo `asfreq` per allineare a frequenza quartoraria."

Dopo: "Il metodo `asfreq` impone alla serie una frequenza regolare, in questo caso un valore ogni quarto d'ora. Per
ogni istante previsto dalla griglia che non compare nei dati viene aggiunta una riga con `NaN`. In questo modo i
buchi di acquisizione, che in una serie irregolare passano inosservati, diventano righe visibili che si possono
contare e trattare."

**Righe etichetta**

Prima: "Unione:" / codice / "Intersezione:" / codice

Dopo: "L'unione di due set, che si ottiene con il metodo `union()`, contiene tutti gli elementi presenti in almeno
uno dei due, senza ripetizioni." / codice / "L'intersezione, con `intersection()`, contiene invece solo gli
elementi che compaiono in entrambi." / codice

**Un elenco di principi**

Prima: "1. **Verifica.** Esegui subito e confronta con un numero noto. 2. **Chiedi spiegazioni.** Prima
"spiegami", poi "correggi". 3. **Piccoli passi.** Una richiesta per volta."

Dopo: "Nel lavoro con un assistente di programmazione conviene tenere tre abitudini. La prima è eseguire subito il
codice ricevuto e confrontare il risultato con un numero che conosciamo già, come il numero di righe del file. La
seconda è chiedere una spiegazione prima della correzione: quando qualcosa non funziona, incolliamo l'errore intero e
chiediamo che cosa significa, e solo dopo chiediamo di sistemarlo. La terza è procedere a piccoli passi, con una
richiesta per volta."

**Una domanda retorica**

Prima: "E se volessimo fare il ciclo solo su una parte degli elementi? Basta lo slicing della lista."

Dopo: "Per iterare solo su una parte degli elementi si applica lo slicing alla lista prima del ciclo. Nell'esempio
qui sotto il ciclo considera soltanto i primi tre giorni."

**Un'apertura da brochure**

Prima: "Restiamo sul minimo che serve nella pratica: `plotly.express`."

Dopo: "In questo capitolo usiamo `plotly.express`, il modulo di alto livello di Plotly, che costruisce un grafico
completo a partire da una tabella con una sola chiamata."

## Come si lavora su un testo esistente

1. **Leggere tutto come un lettore**, dall'inizio alla fine, nella forma in cui lo vedrà chi impara (il notebook
   generato, la pagina renderizzata), e segnare i blocchi che sono appunti e non spiegazioni.
2. **Tenere quello che già scorre.** Le frasi dell'autore che sono già complete e legate restano come sono, anche se
   sono semplici: la riscrittura serve a correggere, non a imporre una voce diversa.
3. **Riscrivere i blocchi segnati** secondo le regole, fondendo le righe etichetta nella frase che spiega l'esempio e
   i blocchi adiacenti che parlano della stessa cosa.
4. **Non toccare il resto.** Codice, comandi, numeri, risultati attesi, link e struttura delle sezioni restano
   invariati, salvo che la richiesta riguardi proprio quelli. Se un numero citato nel testo va controllato, si
   controlla eseguendo il codice o leggendo i dati, non a memoria.
5. **Rileggere una seconda volta** il risultato, sempre come lettore, e sistemare quello che suona ancora come un
   appunto o come una frase costruita per fare effetto.
6. **Riferire** che cosa è cambiato, con due o tre coppie prima e dopo, e segnalare le affermazioni tecniche
   aggiunte durante la riscrittura che non erano nel testo di partenza, perché sono quelle da verificare.

Quando si scrive da zero vale lo stesso procedimento a partire dal punto 3: si scrive il paragrafo, si rilegge come
lettore e si corregge.

## Controllo automatico

Lo script `scripts/controlla_stile.py` segnala nei file Markdown e nei notebook Jupyter i difetti che si possono
riconoscere a macchina: righe etichetta, sequenze di frasi telegrafiche, "Output atteso:" secco, domande retoriche
fuori dalle consegne, aperture con "Qui/Ora/Poi", parole da brochure.

    python scripts/controlla_stile.py percorso/al/file.ipynb percorso/alla/cartella

Lo script trova i casi evidenti e lascia passare il resto: la fluidità di un paragrafo si giudica rileggendolo, e
nessun controllo automatico sostituisce la seconda lettura.
