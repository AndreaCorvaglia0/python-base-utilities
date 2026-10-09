# Lo stile della prosa (ottobre 2026): prevale su REGOLE.md dove diverso

## La richiesta del docente (ottobre 2026, parole sue)

> Voglio uno stile umano, deve sembrare come il tono di un libro tecnico che presenta un argomento, o un blog tecnico
> che spiega come fare qualcosa. Voglio uno stile curato, fluido, senza nemmeno una frase ad effetto. Lascia perdere
> catturare l'attenzione.

E, sul testo attuale: "troppo AI like, frasi frammentate, frasi ad effetto, sembra sconclusionato".

## La diagnosi: cosa suona artificiale nel testo attuale

1. **Frasi telegrafiche in sequenza.** Tre o quattro frasi di sei parole, una dietro l'altra, senza congiunzioni.
   "Il resampling cambia granularità temporale: da quartorario a orario, giornaliero, mensile. È un'operazione di
   aggregazione guidata dal tempo."
2. **Catene di due punti.** "X: Y, Z." usato come scorciatoia al posto di una frase che spiega.
   "Restart riavvia il kernel: le variabili spariscono, il codice resta."
3. **Antitesi e chiusure a effetto.** "le variabili spariscono, il codice resta", "il caso noto torna; resta da provare".
4. **Celle etichetta.** Una cella con la sola parola "Unione:" o "Esempio:" sopra il codice.
5. **Domande retoriche e ganci.** "E se volessimo fare il ciclo solo su una parte degli elementi?"
6. **Aperture ripetute** con "Qui", "Ora", "Poi", e imperativi secchi messi in fila ("Premi Restart ed esegui...").
7. **Elenchi con grassetto in testa al posto della prosa** ("1. **Verifica.** Esegui subito...").
8. **Spiegazione annunciata e non data**: la cella dice cosa fa il codice ma non perché, né cosa aspettarsi.

## Il modello: la prosa del docente

Il riferimento è il testo originale del docente, nei notebook del branch `main`, per esempio:

> Possiamo selezionare una o più colonne di un DataFrame usando il nome della colonna come chiave. Con `loc` e
> `iloc` selezioniamo righe specifiche in base all'indice o alla posizione.

> Gli indici permettono di accedere ai dati per etichetta e di allineare e unire tabelle diverse. `set_index()`
> trasforma una o più colonne in indice, `reset_index()` fa il contrario.

Frasi complete, con soggetto e verbo, legate tra loro; si dice che cosa fa lo strumento e a cosa serve; il codice
sotto illustra la frase. È il tono di un manuale o di un articolo tecnico che spiega come si fa una cosa.

## Le regole

- **Prosa, non appunti.** Ogni cella di testo è un paragrafo di 2-5 frasi complete (circa 40-90 parole), che
  introduce il concetto, dice a cosa serve o perché conta, e prepara la cella di codice che segue. Le frasi si legano
  con "perché", "quindi", "in questo modo", "per esempio", "mentre", "invece".
- **Nessuna frase ad effetto.** Niente antitesi, slogan, massime, chiusure brillanti, metafore, triadi ritmiche,
  domande retoriche, esclamazioni. Il testo non cerca l'attenzione: la informa.
- **Nessuna cella etichetta.** "Unione:", "Esempio:", "Intersezione:" diventano frasi: "L'unione di due set, che si
  ottiene con `union()`, contiene tutti gli elementi presenti in almeno uno dei due."
- **I due punti** si usano per introdurre un elenco o un esempio di codice, non per saldare due mezze frasi.
- **Niente "Qui/Ora/Poi" come apertura** ripetuta. Niente sequenze di imperativi secchi: le istruzioni operative si
  scrivono come frasi ("Per vederlo, premiamo Restart e poi eseguiamo la cella qui sotto").
- **Le regole e le liste di principi** si scrivono in prosa, non in elenchi con grassetto in testa. Gli elenchi restano
  per i passi di una consegna, per le domande delle Esercitazioni e per enumerazioni vere (le opzioni di un parametro).
- **"Noi" quando lavoriamo** ("costruiamo", "selezioniamo"), impersonale per le regole ("si usa", "conviene"). "Tu" solo
  nelle consegne degli esercizi.
- **Esercizi.** Lo scenario e la consegna sono frasi complete; i passi numerati restano, ma ogni passo è una frase
  intera. Niente "Output atteso:" secco: "Il risultato è una Series con ...".
- **Lunghezza.** Non è un invito a gonfiare: si spiega una volta, bene, e si passa al codice. Due celle di testo
  adiacenti che parlano della stessa cella di codice si fondono in un paragrafo.
- **Italiano curato** con il gergo tecnico in inglese dove si usa in inglese (notebook, kernel, DataFrame, slicing).
  Niente virgolette di distanza ("forzi"), niente parentesi che spezzano la frase quando basta una subordinata.

## Esempi: prima → dopo

**00, il kernel**

Prima: "**Restart**, in cima al notebook, riavvia il kernel: le variabili spariscono, il codice resta. Premi Restart ed
esegui la cella qui sotto: dà `NameError`. Poi premi **Run All**, che esegue tutte le celle dall'alto in basso."

Dopo: "Il pulsante **Restart**, in cima al notebook, riavvia il kernel. Il codice scritto nelle celle rimane dov'è, ma
le variabili create fino a quel momento vengono perse, perché esistevano solo nella memoria del processo appena chiuso.
Per vederlo, premiamo Restart e poi eseguiamo la cella qui sotto, che chiede il valore di `x`: Python risponde con un
`NameError`, perché quel nome non esiste più. Il pulsante **Run All** esegue di nuovo tutte le celle dall'alto in basso
e ricostruisce lo stato del notebook."

**08, asfreq**

Prima: "Quando "forzi" una frequenza regolare, i timestamp mancanti diventano righe con `NaN`. Questo è utile: rende
visibili buchi che altrimenti restano nascosti. Qui usiamo `asfreq` per allineare a frequenza quartoraria (`15min`)."

Dopo: "Il metodo `asfreq` impone alla serie una frequenza regolare, in questo caso un valore ogni quarto d'ora. Per ogni
istante previsto dalla griglia che non compare nei dati viene aggiunta una riga con `NaN`. In questo modo i buchi di
acquisizione, che in una serie irregolare passano inosservati, diventano righe visibili che si possono contare e
trattare."

**A1, i set**

Prima: "Unione:" / codice / "Intersezione:" / codice

Dopo: "L'unione di due set, che si ottiene con il metodo `union()`, contiene tutti gli elementi presenti in almeno uno
dei due, senza ripetizioni." / codice / "L'intersezione, con `intersection()`, contiene invece solo gli elementi che
compaiono in entrambi." / codice

**10, le tre regole**

Prima: "1. **Verifica.** Esegui subito e confronta con un numero noto: la somma dei kwp, il numero di righe.
2. **Chiedi spiegazioni.** Prima "spiegami", poi "correggi", sempre con il traceback intero. 3. **Piccoli passi.** Una
richiesta per volta."

Dopo: "Nel lavoro con un agente conviene tenere tre abitudini. La prima è eseguire subito il codice ricevuto e
confrontare il risultato con un numero che conosciamo già, come la somma dei kWp o il numero di righe del file. La
seconda è chiedere una spiegazione prima della correzione: quando qualcosa non funziona, incolliamo il traceback intero
e chiediamo cosa significa, e solo dopo chiediamo di sistemarlo. La terza è procedere a piccoli passi, con una richiesta
per volta; in modalità Agent le modifiche arrivano come differenze da accettare o annullare blocco per blocco."

**04, slicing nel ciclo**

Prima: "E se volessimo fare il ciclo solo su una parte degli elementi? Basta lo slicing della lista."

Dopo: "Per iterare solo su una parte degli elementi si applica lo slicing alla lista prima del ciclo. Nell'esempio qui
sotto il ciclo considera soltanto i primi tre giorni."

**09, l'apertura**

Prima: "Restiamo sul minimo che serve nella pratica: `plotly.express`. Documentazione ufficiale: ..."

Dopo: "In questo notebook usiamo `plotly.express`, il modulo di alto livello di Plotly, che costruisce un grafico
completo a partire da un DataFrame con una sola chiamata. La documentazione di riferimento è ..."

## Cosa non si tocca

- Il codice, i dati, gli `# Output:` nei commenti, le `verifica=` e le soluzioni, la struttura delle sezioni, i tempi,
  gli obiettivi (salvo che contengano frasi ad effetto), i link alle Schede.
- Le frasi del docente che già scorrono (la maggior parte di quelle riprese dai notebook originali): si tengono così come
  sono. Si riscrive quello che è frammentato, telegrafico o a effetto, e si fondono le celle etichetta nella frase.
- Le domande delle Esercitazioni (sono quiz: restano domande numerate).

## Come si lavora

Si legge il notebook generato (Aula_Base) cella per cella come un lettore, si riscrivono nel sorgente le celle di testo
che non reggono il confronto con il modello, si ricostruisce (`uv run python _build/build.py NN`: zero errori, zero
avvisi, compresi i nuovi avvisi di stile), si validano Soluzioni e Aula, e si rilegge una seconda volta il risultato.
