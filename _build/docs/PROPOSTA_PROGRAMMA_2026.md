# Proposta di programma 2026 (v2)

Testo estratto dal documento Word del docente, `Proposta_Programma_2026_v2.docx`. Gli argomenti segnati (A) sono previsti
solo per l'aula Avanzata. È la sequenza di riferimento del corso: il piano operativo è in `PIANO_OTTOBRE_2026.md`.

Nel programma ho indicato con (A) e con l'evidenziatore giallo gli
argomenti previsti solo per l'aula Avanzata. Le due aule seguono gli
stessi blocchi e gli stessi temi: nella Base spenderemo più tempo per
introdurre e consolidare, nell'Avanzata si aggiungono gli argomenti (A)
e più tempo per applicazioni ulteriori.

# Blocco 1 · Setup, Python e sintassi di base

**Obiettivo del blocco:** chiudere e verificare il setup in modo che
tutti abbiano Python funzionante in VS Code, capire cosa sono Python e
le librerie, e saper leggere e scrivere le istruzioni di base.

1.  **Introduzione al corso e all'ambiente di lavoro**

-   Cos'è Python, cosa sono le librerie e come si usano nell'analisi
    dati; struttura del corso e perché gli agenti per il coding sono
    trattati alla fine

-   VS Code: installazione, estensioni Python e Jupyter, selezione
    dell'interprete, verifica che tutto funzioni su ogni PC

-   Notebook Jupyter in VS Code: celle di codice e celle Markdown,
    esecuzione, shortcut utili

-   (A) Ambienti virtuali per progetto: perché servono, creazione,
    installazione delle librerie e gestione delle dipendenze

-   (A) Script .py e differenza con i notebook: quando usare l'uno o
    l'altro, esecuzione da terminale

2.  **Sintassi di base**

-   Indentazione, variabili e assegnazione, import di librerie,
    differenza tra comandi base di Python e comandi di libreria

-   Tipi numerici, operatori aritmetici e di confronto, funzioni
    matematiche [esercizi]

-   Stringhe: creazione, concatenazione, formattazione; print e f-string
    per produrre testi dinamici [esercizi]

-   Strutture dati: liste (indexing, slicing, aggiunta/rimozione),
    tuple, dizionari (chiave/valore), set; quando usare ciascuna
    [esercizi]

3.  **Scrivere codice leggibile**

-   Commenti e documentazione: commentare il codice, celle Markdown per
    spiegare i passaggi di un notebook, docstring di una funzione

-   Convenzioni di stile essenziali (PEP-8: nomi, spaziatura)

-   (A) Ruff come formatter e linter in VS Code: formattazione
    automatica e segnalazione dei problemi nel codice

# Blocco 2 · Controllo del flusso, funzioni e primi dati in pandas

**Obiettivo del blocco:** saper leggere e scrivere un pezzo di codice
completo (condizioni, cicli, funzioni), capire il vocabolario degli
oggetti e degli errori per interpretare codice scritto da altri, e
portare dati reali in pandas da file, database e API.

4.  **Condizioni, cicli e funzioni**

-   if / elif / else e annidamento [esercizi]

-   Cicli for e while, range(), enumerate(), .items() sui dizionari,
    iterazione su più liste [esercizi]

-   Definire funzioni: argomenti, argomenti keyword e valori
    predefiniti, return [esercizi]

-   (A) List comprehension, funzioni lambda, map() e filter(),
    iterabili e generatori \esercizi\]

5.  **Oggetti ed errori: capire il codice**

-   In Python tutto è un oggetto: attributi e metodi, come leggere una
    riga del tipo dati.metodo() e capire cosa fa (stringhe, liste,
    DataFrame)

-   Leggere la documentazione e i type hint di una funzione per capire
    cosa si aspetta e cosa restituisce

-   Tipi di errore più comuni (SyntaxError, NameError, TypeError,
    KeyError...) e come leggere un traceback per capire dove e perché il
    codice si ferma [esercizi]

6.  **Pandas: introduzione e import dei dati da sorgenti esterne**

-   Series e DataFrame: struttura, tipi delle colonne, prime ispezioni
    (head, info, describe)

-   Gestione del filesystem: percorsi, file e directory

-   Lettura e scrittura di file: CSV (parametri utili, tipi di dato, più
    file insieme), Excel (più fogli) [esercizi]

-   Lettura da database SQL: connessione e caricamento di una tabella in
    un DataFrame [esercizi]

-   (A) Lettura da API con requests: richieste GET, codici di stato
    HTTP, query parameters, risposta JSON; esempio pratico con i dati
    meteo di Regione Lombardia (anagrafica e misure dei sensori)
    \esercizi\]

-   (A) Incapsulare la lettura da un'API in una funzione riutilizzabile
    (wrapper) \esercizi\]

-   Aula Base: esercitazioni aggiuntive su lettura e scrittura di file e
    sui database [esercizi]

# Blocco 3 · Analisi dei dati con pandas e visualizzazione

**Obiettivo del blocco:** partire da uno o più DataFrame e arrivare a
un'analisi: pulire, filtrare, aggregare, unire tabelle, lavorare con le
date e produrre grafici interattivi.

7.  **Operazioni sui DataFrame e tra DataFrame**

-   Selezione di righe e colonne: loc, iloc, filtri condizionali,
    .query() (comodo per chi conosce SQL) [esercizi]

-   Valori mancanti e duplicati, trasformazione e creazione di colonne
    (apply, map, lambda) [esercizi]

-   Indici (set_index / reset_index), ordinamento, groupby e
    aggregazioni [esercizi]

-   Operazioni tra DataFrame: merge, concat, join [esercizi]

-   Analisi esplorativa (EDA) con Data Wrangler in VS Code: esplorare,
    filtrare e pulire in modo interattivo e leggere il codice pandas che
    genera [esercizi]

8.  **Dati temporali in pandas**

-   Date in pandas: conversione e formati, tempo come indice, attributi
    temporali (anno, mese, giorno della settimana, ora)

-   Frequenza, valori mancanti da allineamento, differenze tra date,
    fuso orario e ora legale [esercizi]

-   (A) Operazioni sulle serie storiche: resampling, shift e rolling
    window \esercizi\]

9.  **Visualizzazione con Plotly**

-   Elementi chiave di un grafico Plotly, grafici con Plotly Express
    (linee, istogrammi, scatter)

-   Confronto tra più serie, slider e range selector, esportazione in
    HTML [esercizi]

# Blocco 4 · Agenti per il coding e caso d'uso end-to-end

**Obiettivo del blocco:** usare GitHub Copilot in VS Code sapendo
leggere e verificare quello che produce, e applicare tutto il percorso a
un caso reale: leggere e integrare sorgenti dati diverse e fare
un'analisi esplorativa su dati utility.

10. **Agenti per il coding: GitHub Copilot**

-   Cosa fa Copilot in VS Code (e intro generale ai coding agents claude
    code, codex e github copilot)

-   Concetti di base (token, finestra di contesto, cache, scelta dei
    modelli, plan vs agent, prompt e context engineering)

11. **Capstone project/ progetto finale (diversi livelli di richiesta
    per i due gruppi)**

-   Caricamento e unione dei dati della domanda, preparazione della
    colonna temporale

-   Integrazione di una sorgente esterna via API (temperatura da
    Open-Meteo); nell'aula Base con codice già predisposto, per
    recuperare i dati senza entrare nei dettagli tecnici

-   Aggregazioni temporali (serie giornaliera, profili medi giornalieri
    e settimanali) e analisi esplorativa

-   Visualizzazione dei risultati con Plotly

-   Lavoro in autonomia con il supporto di Copilot; soluzioni condivise
    a fine giornata

12. **(A) Modulo opzionale, da confermare insieme: introduzione al
    forecasting e primo modello semplice**

-   Introduzione a Prophet sul caso d'uso: modello base, componenti,
    regressore temperatura

-   In alternativa: introduzione al machine learning o altri temi da
    definire

-   Aula Base: eventuale breve accenno al forecasting, se avanza tempo e
    c'è interesse
