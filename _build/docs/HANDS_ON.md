# Hands-on ed Extra: il piano per notebook (ottobre 2026)

Questo documento applica la sezione "Dove stanno gli esercizi" di `REGOLE.md` ai singoli notebook. Per ciascuno dice
quali concetti devono restare in mano al corsista perché tornano nei notebook seguenti, nelle esercitazioni e nel
leggere codice scritto da un'AI, e da lì ricava gli Hands-on inline e la sezione Extra.

## Che cos'è un Hands-on

Un Hands-on sta subito dopo l'esempio che riprende e chiede di rifare lo stesso gesto su un dato diverso o di cambiare
una cosa nel codice appena visto: un altro indice, un'altra chiave, un altro parametro, un'altra colonna. Dura da uno a
tre minuti, ha una cella da completare con `...`, una `verifica=` con uno o due `assert`, e può chiudersi con una riga
`prova_anche=` sempre banale ("prova con passo 3", "prova con `ascending=False`"). Non introduce niente di nuovo, non
è un compito, non ha scenario: due frasi che dicono che cosa fare e che cosa deve uscire. Nel sorgente è
`nb.hands_on(richiesta, starter, soluzione, verifica, prova_anche)`. Quando il gesto si fa nell'editor e non nel codice,
come creare una cella o premere Restart, il Hands-on ha soltanto il riquadro con le istruzioni, senza `starter` né
`verifica`; succede quasi solo nel notebook 00.

La sezione Extra chiude il notebook, si chiama "Extra", in aula si salta e chi vuole la fa a casa. Contiene due o tre
esercizi brevi (`nb.esercizio`, con il formato "prima il risultato, poi i passi"), che ripassano i punti principali
del notebook. Dove il vecchio Homework o i vecchi esercizi di fine notebook sono fatti bene, si riusano qui. Nei
notebook di sintassi (00-05) gli Extra restano nel dominio quotidiano: un passo dell'Homework che serve lì si traspone
su dati quotidiani con lo stesso codice.

Gli esercizi originali del docente che ora stanno nelle esercitazioni (01: massimo e minimo, area del cerchio; 02:
lista invertita, posizioni pari, capitali del G8; 03: stringa invertita, capitali pari, palindrome; 04 pandas: i
cinque sugli ascolti; 06 time series: formato, periodo con loc, date e weekend, resample con sum) escono dai notebook
e sono sostituiti da Hands-on nuovi.

## Notebook per notebook

### 00 · Jupyter e i notebook
Il notebook insegna lo strumento, non il Python: i corsisti non sanno ancora nulla del linguaggio, quindi il codice si
limita a variabili e `print`. Concetti che restano: celle di codice e celle Markdown; eseguire, creare ed eliminare
celle con tre scorciatoie (Shift + Invio; Esc e poi B, o A; Esc e poi M); il kernel che tiene le variabili, la vista
Variables di VS Code; l'ordine di esecuzione e il numero tra parentesi; Restart che cancella le variabili e Run All
che le ricostruisce. Hands-on, cinque, subito dopo la spiegazione di ciascun gesto: eseguire una cella con il proprio
nome; creare una cella di codice e una Markdown con le scorciatoie ed eliminarne una; trovare le variabili nella vista
e crearne una nuova; rieseguire fuori ordine una cella e guardare il risultato cambiare; Restart, `NameError` e Run
All. Tre di questi sono soltanto gesti nell'editor e non hanno codice né verifica. Extra: una cella Markdown e una di
codice con istruzioni esatte; il giro completo di variabili, Restart e Run All.

### 01 · Introduzione a Python e sintassi base
Concetti che restano: assegnazione e nomi, operatori (`/`, `//`, `%`, `**`), `import` di un modulo e `modulo.nome`,
`type()`, concatenazione e f-string con il formato `:.2f`. Sono le cose che compaiono in ogni riga di codice generato.
Hands-on, quattro: dopo "Variabili" cambiare i valori e ristampare; dopo "Operatori aritmetici" calcolare `//` e `%` su
altri due numeri; dopo "Funzioni matematiche" usare un'altra funzione di `math` (`math.sqrt(81)` dà 9.0); dopo
"Formattazione" scrivere una f-string con `:.1f`. Extra: "Ore e minuti" (attuale 1.3) e un esercizio breve sulle
stringhe (lunghezza con `len`, maiuscole con `.upper()`, concatenazione).

### 02 · Tipi di dato e manipolazione
Concetti che restano: indice e slicing (`[0]`, `[-1]`, `[1:3]`, `[::2]`), `append`/`remove`/`len`, lettura e scrittura
in un dizionario con la chiave, `.keys()`/`.values()`/`.items()`, `set()` per togliere i doppioni, la tupla come
sequenza immutabile. Hands-on, cinque: dopo "Slicing" un altro slicing sulla lista dei numeri; dopo "Aggiunta e
rimozione" aggiungere un elemento e contare; dopo "Accesso ai valori" leggere un valore con un'altra chiave; dopo
"Modifica di un dizionario" aggiungere una coppia; dopo "Set" eliminare i doppioni da una lista e contare. Extra: un
dizionario dei prezzi da completare e sommare con `sum(prezzi.values())` (riuso del vecchio E1.4, dominio spesa); due
liste unite con `+` e `set()` per il carrello (riuso del vecchio E1.5).

### 03 · Codice leggibile
Concetti che restano: commenti che spiegano il perché, docstring letta con `help()`, nomi secondo PEP 8. Hands-on, due:
dopo "Docstring" aggiungere una docstring a una funzione data e leggerla con `help()`; dopo "PEP 8" rinominare le
variabili di una riga data. Extra: i due esercizi attuali (rinominare e documentare una funzione; riscrivere una cella
seguendo PEP 8), già brevi.

### 04 · Funzioni e controllo del flusso
Concetti che restano: `if/elif/else` con una condizione, `for` su una lista con un accumulatore, `for` su `.items()`,
`range`, `def` con `return`, argomento con valore predefinito e chiamata per nome; per l'Avanzata la list
comprehension e la lambda, da saper leggere nel codice generato. Hands-on, cinque: dopo "La clausola if" cambiare la
soglia e aggiungere un `elif`; dopo "Il ciclo for" trasformare la somma in un conteggio degli elementi sopra un valore;
dopo "Dizionari, enumerate e zip" stampare `chiave: valore` con `.items()`; dopo "Argomenti predefiniti" chiamare una
funzione data con e senza l'argomento; per l'Avanzata, dopo "List comprehension", riscrivere un ciclo di due righe come
comprehension. Extra: un ciclo con `if` che costruisce la lista dei valori sopra soglia e il totale (il passo
Mercoledì dell'Homework trasposto su spese quotidiane); una funzione con valore predefinito e docstring (il passo
Giovedì dell'Homework trasposto, per esempio prezzo con sconto).

### 05 · Oggetti ed errori
Concetti che restano: `type()`, attributi e metodi letti con il punto, leggere una riga `dati.metodo()` e dire che cosa
è ogni pezzo, `help()` e la firma di una funzione, i nomi degli errori e la riga del traceback che conta. È il
notebook che prepara a leggere il codice di un agente. Hands-on, tre: l'attuale "chi è chi" (cinque espressioni da
etichettare) resta; dopo "Gli errori più comuni" una cella con un `NameError` da correggere; dopo "Leggere la
documentazione" leggere con `help()` la firma di `round` e chiamarla con il secondo argomento. Extra: "Quattro celle
da sistemare" ridotto a due celle; "Leggere una firma" attuale.

### 06 · Pandas: Series, DataFrame e import dei dati
Concetti che restano: `pd.read_csv` con `sep` e `decimal`, `head`/`info`/`shape`, `read_excel` con `sheet_name`,
`sqlite3.connect` e `pd.read_sql`, per l'Avanzata `requests.get(...).json()`. Hands-on, cinque: dopo "DataFrame"
cambiare `head(3)` in `tail(2)` e leggere `shape`; l'attuale `os.listdir` resta; dopo "Un CSV salvato da Excel in
italiano" aggiungere `usecols`; dopo "Più fogli in un file" leggere un altro foglio; dopo "Database SQL" cambiare il
`WHERE` della query; per l'Avanzata, dopo "Parametri di query", cambiare un parametro della richiesta (`rete`). Extra:
il passo Venerdì dell'Homework senza la maschera (leggere il CSV italiano e controllare `info()`); il passo Sabato
(un foglio Excel e una tabella SQL); per l'Avanzata l'attuale esercizio sulla certificazione energetica.

### 07 · Pandas: operazioni sui DataFrame
Concetti che restano: `loc`/`iloc`, maschera booleana, `fillna`/`dropna`, `groupby` con una funzione di aggregazione,
`sort_values`, `merge` con `how`. Sono le operazioni che un agente scrive in ogni analisi. Hands-on, cinque: dopo
"Selezione di righe e colonne" selezionare altre due colonne con `loc`; dopo "Selezione condizionale" cambiare la
condizione della maschera; dopo "Valori mancanti" riempire con un altro valore; dopo "Groupby" raggruppare per
un'altra colonna o con `mean` al posto di `sum`; dopo "Merge" cambiare `how` e contare le righe. Extra: l'attuale 7.4
(prezzo medio per stato) e un esercizio breve su `sort_values` con `ascending=False` e `head(3)`.

### 08 · Pandas: le date
Concetti che restano: `pd.to_datetime` con `format`, il tempo come indice e la selezione di un periodo con `loc`, gli
attributi `.hour`/`.dayofweek`/`.date`, `resample` con una funzione, `asfreq` e i `NaN` dell'allineamento. Gli Hands-on
attuali sono gli esercizi originali del docente e passano all'Esercitazione 3: qui ne servono di nuovi, quattro, con
gesti diversi: dopo "Formati" convertire una stringa con un altro formato (`"2025-03-01 12:00"` con `%Y-%m-%d %H:%M`);
dopo "Il tempo come indice" selezionare un giorno intero con `.loc["2025-03-02"]`; dopo "Attributi temporali" ricavare
l'ora dall'indice e contare le righe delle 12; dopo "Resampling" un resample a due ore (`"2h"`). Extra: i due esercizi
attuali sul carico Terna (giornaliero; ora e giorno della settimana).

### 09 · Plotly per serie storiche
Il notebook è breve, 25 minuti: Plotly serve soprattutto come terreno per leggere il codice che Copilot scrive nel
capstone. Concetti che restano: `px.line` con `x`, `y`, `title`, il grafico come oggetto `fig` con `fig.show()`, più
colonne in un grafico, `fig.write_html`; slider, istogramma e scatter si vedono una volta, in una sola sezione, senza
Hands-on. Hands-on, tre: cambiare colonna e titolo del primo grafico; aggiungere una società al confronto; esportare lo
scatter in HTML. Extra: un mese di carico con lo slider; il grafico del carico in HTML; la distribuzione della potenza.

### 10 · Agenti per il coding
Concetti che restano: formulare un prompt con il contesto, leggere il codice prima di eseguirlo, riconoscere le quattro
cose (decoratore, type hint, blocco main, costante). Hands-on: i due attuali restano come sono. Extra: i due esercizi
attuali (il parametro inventato; leggere prima di lanciare).

### 11 · Capstone e Approfondimenti
Il capstone resta a passi guidati, senza Hands-on; il suo step 7 è aperto e si fa con Copilot, con richieste a
scelta sui dati già pronti. Gli Approfondimenti tengono i loro esercizi, con la sola etichetta
nuova.
