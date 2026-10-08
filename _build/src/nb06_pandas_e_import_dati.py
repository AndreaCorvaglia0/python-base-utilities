"""06 · Pandas: Series, DataFrame e import dei dati."""

from nbkit import Notebook

DATI_BASE = [
    "TexasTurbine.csv",
    "letture_pod_2025.csv",
    "load_total_north_hourly_2024.xlsx",
    "utility.db",
]


def costruisci() -> Notebook:
    nb = Notebook(
        num="06",
        file="06_Pandas_e_import_dati",
        titolo="Pandas: Series, DataFrame e import dei dati",
        blocco=2,
        giornata=1,
        intento=(
            "Il notebook presenta le due strutture dati di pandas, Series e DataFrame, e mostra come leggere "
            "i dati da file CSV ed Excel, da un database SQL e da un'API web."
        ),
        obiettivi={
            "base": [
                "creare Series e DataFrame e accedere ai loro elementi",
                "leggere file CSV ed Excel con i parametri di lettura, anche più fogli insieme",
                "caricare una tabella da un database SQL con una query",
            ],
            "avanzata": [
                "creare Series e DataFrame e leggere file CSV ed Excel con i parametri di lettura",
                "caricare una tabella da un database SQL con una query",
                "chiedere dati a un'API con `requests` e trasformare la risposta JSON in un DataFrame",
            ],
        },
        tempo={"base": 55, "avanzata": 75},
        dati={
            "base": DATI_BASE,
            "avanzata": DATI_BASE + ["fallback/lombardia_sensori.json", "fallback/lombardia_misure_2001.json"],
        },
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Importare le librerie", intro="""
        Pandas è una libreria open-source per l'analisi e la manipolazione dei dati in Python. Offre
        strutture dati e funzioni pensate per lavorare con dati strutturati, come tabelle e serie temporali.

        Per usare una libreria la importiamo con la parola chiave `import`, di solito con un nome abbreviato;
        per pandas il nome convenzionale è `pd`. È buona pratica importare tutte le librerie necessarie
        all'inizio del notebook, in modo che chi lo legge veda subito di che cosa ha bisogno.
    """)
    nb.code("import pandas as pd")

    # ------------------------------------------------------------------ 2
    nb.sezione("Le strutture dati di pandas", intro="""
        Pandas si basa su due strutture dati principali. La **Series** è un array unidimensionale in cui
        ogni elemento ha un'etichetta, mentre il **DataFrame** è una struttura bidimensionale, con righe e
        colonne etichettate. Un DataFrame si può vedere come un insieme di Series, una per colonna, che
        condividono le stesse etichette di riga.
    """)
    nb.sottosezione("Series", intro="""
        Una **Series** è un array unidimensionale che può contenere qualsiasi tipo di dato, come interi,
        stringhe, numeri decimali o oggetti Python. Ogni elemento è associato a un'etichetta, chiamata
        **indice**. Nella cella qui sotto creiamo una Series a partire da una lista e le diamo un nome con
        `name`; poiché non indichiamo un indice, pandas usa le posizioni 0, 1, 2 e 3.
    """)
    nb.code("""
        # creare una Series da una lista
        dati = [10, 20, 30, 40]
        s = pd.Series(dati, name="valori")
        s
    """)
    nb.md("""
        Con il parametro `index` possiamo assegnare agli elementi etichette scelte da noi al posto delle
        posizioni numeriche. La lista delle etichette deve avere la stessa lunghezza della lista dei dati.
    """)
    nb.code("""
        s_custom = pd.Series(dati, index=["a", "b", "c", "d"])
        s_custom
    """)
    nb.md("""
        Agli elementi di una Series si accede con le parentesi quadre, come per gli elementi di una lista.
        Nella prima cella qui sotto usiamo l'indice numerico di `s`, nella seconda l'etichetta `"b"` di
        `s_custom`, che restituisce il secondo valore.
    """)
    nb.code("""
        # accesso tramite indice numerico
        s[0]
    """)
    nb.code("""
        # accesso tramite indice personalizzato
        s_custom["b"]
    """)
    nb.md("""
        Anche lo slicing funziona come con le liste Python. L'espressione `s[1:3]` restituisce una nuova
        Series con gli elementi nelle posizioni 1 e 2, perché l'estremo finale è escluso, e ogni elemento
        conserva la sua etichetta originale.
    """)
    nb.code("""
        # slicing della Series
        s[1:3]
    """)
    nb.sottosezione("DataFrame", intro="""
        Un **DataFrame** è una struttura bidimensionale con dati allineati in righe e colonne, simile a un
        foglio di calcolo o a una tabella SQL. Un modo semplice per crearlo è partire da un dizionario, in
        cui ogni chiave diventa il nome di una colonna e la lista associata ne contiene i valori. Con
        `index` diamo un'etichetta anche alle righe, e nel prossimo notebook la useremo per selezionarle.
    """)
    nb.code("""
        # creare un DataFrame da un dizionario
        dati = {
            "Nome": ["Alice", "Bob", "Charlie"],
            "Età": [24, 27, 22],
            "Città": ["Roma", "Milano", "Torino"],
        }
        df = pd.DataFrame(dati, index=["id_1", "id_2", "id_3"])
        df
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("File e cartelle con os", intro="""
        Il modulo `os` di Python serve a interagire con il sistema operativo, per esempio per navigare tra
        le cartelle, gestire i file e ottenere informazioni sul sistema. La funzione `os.listdir()`
        restituisce l'elenco dei file e delle cartelle contenuti in una cartella e, se non riceve argomenti,
        considera la cartella di lavoro. Nella cella qui sotto stampiamo questo elenco una voce per riga.
    """)
    nb.code("""
        import os

        # elencare i file nella cartella di lavoro
        elenco_file = os.listdir()
        print("Contenuto della cartella:")
        for file in elenco_file:
            print(file)
    """)
    nb.md("""
        La cartella di lavoro di un notebook è quella in cui si trova il file, e `os.getcwd()` ne
        restituisce il percorso completo. I dati del corso stanno nella cartella `Dati`, che si trova un
        livello più in alto; poiché `..` indica la cartella superiore, il percorso relativo dei file è
        `../Dati/`. Con `os.path.exists()` controlliamo che un file esista prima di leggerlo; la funzione
        restituisce `True` se il percorso è corretto e `False` altrimenti.
    """)
    nb.code("os.getcwd()")
    nb.code('os.path.exists("../Dati/TexasTurbine.csv")')
    nb.prova_tu(
        richiesta="""
            Stampa l'elenco dei file contenuti nella cartella `Dati`, passando a `os.listdir()` il percorso
            relativo della cartella. Nell'elenco devono comparire, tra gli altri, `TexasTurbine.csv` e
            `utility.db`.
        """,
        starter="""
            # suggerimento: specifica il percorso della cartella in listdir()
            ...
        """,
        soluzione="""
            for file in os.listdir("../Dati"):
                print(file)
        """,
    )

    # ------------------------------------------------------------------ 4
    nb.sezione("File CSV", intro="""
        I file CSV (*Comma-Separated Values*) sono uno dei formati più comuni per archiviare e scambiare dati
        tabulari. Ogni riga del file corrisponde a una riga della tabella, e i valori sono separati da un
        carattere, di solito la virgola. Pandas li legge con la funzione `read_csv()`, che restituisce un
        DataFrame, e con il metodo `head()` ne vediamo le prime cinque righe.
    """)
    nb.code("""
        # leggere un file CSV
        df_turbina = pd.read_csv("../Dati/TexasTurbine.csv")
        df_turbina.head()
    """)
    nb.md("""
        Dopo la lettura conviene controllare che cosa è arrivato. Il metodo `info()` riassume il numero di
        righe e di colonne, il tipo di ogni colonna e quanti valori non mancano, mentre `describe()` calcola
        le statistiche principali delle colonne numeriche, come media, minimo, massimo e quartili.
    """)
    nb.code("df_turbina.info()")
    nb.code("df_turbina.describe()")
    nb.md("""
        Quando un file non segue il formato standard, `read_csv()` si adatta attraverso alcuni parametri.
        Quelli che useremo più spesso sono i seguenti:

        - `usecols` indica quali colonne leggere dal file;
        - `sep` indica il delimitatore tra le colonne, per esempio `,`, `;` oppure `\\t`;
        - `decimal` indica il separatore dei decimali, per esempio `,` invece di `.`.
    """)
    nb.sottosezione("Un CSV salvato da Excel in italiano", intro="""
        Il file `letture_pod_2025.csv` contiene i consumi mensili per fascia di sei POD ed è stato esportato
        da un Excel configurato in italiano. Se proviamo a leggerlo con i parametri predefiniti, la cella qui
        sotto si ferma con un errore, che in questo caso è voluto. L'informazione che serve per capirlo si
        trova nell'ultima riga del messaggio.
    """)
    nb.code('pd.read_csv("../Dati/letture_pod_2025.csv")', errore=True)
    nb.md("""
        L'errore è un `UnicodeDecodeError`, e nasce dal fatto che pandas legge il file come UTF-8 e incontra
        un byte che in UTF-8 non è valido, cioè la `è` di "Caffè". I file salvati da Excel su Windows usano spesso l'encoding
        `latin-1`, che va quindi indicato con il parametro `encoding`. I CSV italiani, inoltre, separano le
        colonne con `;` e scrivono i decimali con la virgola, per cui alla lettura servono tre parametri.
        Nella seconda cella controlliamo con `dtypes` il tipo di ogni colonna.
    """)
    nb.code("""
        letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
        letture.head()
    """)
    nb.code("letture.dtypes")
    nb.md("""
        La colonna `kwh` risulta di tipo `float64`, cioè numerica. Senza `decimal=","` pandas l'avrebbe
        letta come testo, e su una colonna di testo non si possono calcolare somme o medie. Il parametro
        `encoding="latin-1"`, invece, conviene aggiungerlo solo quando l'errore lo richiede, perché su un
        file UTF-8 che contiene lettere accentate non darebbe alcun errore, ma produrrebbe caratteri
        sbagliati senza segnalarlo.
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("File Excel", intro="""
        I file Excel sono molto usati per i dati strutturati e, a differenza dei CSV, possono contenere più
        fogli. Pandas li legge con la funzione `read_excel()`, che senza altre indicazioni carica il primo
        foglio. Come esempio leggiamo il carico elettrico della zona Nord nel 2024, che Terna pubblica con
        un valore ogni quarto d'ora.
    """)
    nb.code("""
        carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico.head()
    """)
    nb.sottosezione("Più fogli in un file", intro="""
        Con `pd.ExcelWriter` possiamo scrivere più DataFrame nello stesso file Excel, ciascuno nel proprio
        foglio. Per vederlo creiamo prima due piccoli DataFrame di esempio, con le stesse colonne.
    """)
    nb.code("""
        df1 = pd.DataFrame({
            "ID": [1, 2, 3],
            "Nome": ["Alice", "Bob", "Charlie"],
            "Età": [25, 30, 35],
        })
        df2 = pd.DataFrame({
            "ID": [4, 5, 6],
            "Nome": ["David", "Eva", "Frank"],
            "Età": [40, 45, 50],
        })
    """)
    nb.md("""
        L'istruzione `with pd.ExcelWriter("dati.xlsx") as writer` apre il file in scrittura e lo chiude alla
        fine del blocco. Dentro il blocco il metodo `to_excel()` scrive ogni DataFrame nel foglio indicato
        da `sheet_name`, e `index=False` evita di salvare l'indice come colonna aggiuntiva.
    """)
    nb.code("""
        # creare un file Excel con più fogli
        with pd.ExcelWriter("dati.xlsx") as writer:
            df1.to_excel(writer, sheet_name="Foglio1", index=False)
            df2.to_excel(writer, sheet_name="Foglio2", index=False)
        print("File 'dati.xlsx' creato.")
    """)
    nb.md("""
        Per leggere un foglio specifico si passa il suo nome al parametro `sheet_name` di `read_excel()`.
        Con `dtypes` controlliamo poi che le colonne siano arrivate con il tipo giusto, per esempio `Età`
        come numero intero.
    """)
    nb.code("""
        # leggere un foglio specifico
        df_foglio1 = pd.read_excel("dati.xlsx", sheet_name="Foglio1")
        df_foglio1.dtypes
    """)
    nb.md("""
        Con `sheet_name=None` pandas legge tutti i fogli in una volta e restituisce un dizionario, in cui la
        chiave è il nome del foglio e il valore è il DataFrame corrispondente. Le chiavi del dizionario ci
        mostrano quali fogli sono stati letti.
    """)
    nb.code("""
        # leggere tutti i fogli dal file Excel
        fogli = pd.read_excel("dati.xlsx", sheet_name=None)
        fogli.keys()
    """)
    nb.md("""
        Poiché i due fogli hanno le stesse colonne, possiamo metterli uno sotto l'altro con `pd.concat()`,
        a cui passiamo i DataFrame contenuti nel dizionario. Con `ignore_index=True` l'indice del risultato
        riparte da 0, invece di ripetere gli indici dei singoli fogli.
    """)
    nb.code("""
        # concatenare i DataFrame
        df_excel_unito = pd.concat(fogli.values(), ignore_index=True)
        df_excel_unito
    """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Database SQL", intro="""
        Spesso i dati stanno in un database, organizzati in tabelle che si interrogano con il linguaggio
        SQL. Python comunica con il database attraverso una connessione, e la funzione `pd.read_sql` esegue
        una query e ne restituisce il risultato come DataFrame. In questo notebook usiamo SQLite, un database
        contenuto in un singolo file, `utility.db`, che si apre con il modulo `sqlite3` della libreria
        standard. La prima query chiede al database l'elenco delle sue tabelle.
    """)
    nb.code("""
        import sqlite3

        con = sqlite3.connect("../Dati/utility.db")
        pd.read_sql("SELECT name FROM sqlite_master WHERE type = 'table'", con)
    """)
    nb.md("""
        La tabella `sqlite_master` è quella in cui SQLite tiene l'elenco del proprio contenuto, e dal
        risultato vediamo che il database contiene le tabelle `clienti`, `pod` e `letture`. Per leggere una
        tabella intera si usa una query come `SELECT * FROM letture`, in cui l'asterisco indica tutte le
        colonne; poiché la query non pone condizioni, arrivano anche tutte le righe.
    """)
    nb.code("""
        letture_db = pd.read_sql("SELECT * FROM letture", con)
        letture_db.head()
    """)
    nb.md("""
        Quando ci serve solo una parte dei dati, la clausola `WHERE` aggiunge una condizione alla query. In
        questo modo il filtro lo esegue il database, e in Python arrivano soltanto le righe che servono;
        nell'esempio teniamo i POD con una potenza di almeno 30 kW.
    """)
    nb.code('pd.read_sql("SELECT * FROM pod WHERE potenza_kw >= 30", con)')
    nb.md("""
        Al termine del lavoro la connessione si chiude con il metodo `close()`, che libera il file del
        database. Dopo la chiusura, per eseguire altre query occorre aprire una nuova connessione con
        `sqlite3.connect()`.
    """)
    nb.code("con.close()")

    # ------------------------------------------------------------------ 7 (A)
    with nb.solo("avanzata"):
        nb.sezione("Lettura di dati da API", intro="""
            Le API (*Application Programming Interface*) sono insiemi di regole che permettono a programmi
            diversi di comunicare tra loro, e molti servizi web ne offrono di pubbliche per accedere ai
            propri dati. Per interagire con un'API si invia una richiesta HTTP, di solito di tipo GET, a un
            indirizzo specifico chiamato endpoint, e si riceve una risposta, spesso in formato JSON.
        """)
        nb.sottosezione("JSON e requests", intro="""
            JSON (*JavaScript Object Notation*) è un formato di testo per lo scambio di dati, strutturato in
            coppie chiave-valore simili ai dizionari Python. È molto usato per inviare dati tra server e
            applicazioni web, perché è leggibile e non dipende dal linguaggio di programmazione. Un oggetto
            JSON ha questo aspetto:

            ```json
            {
              "name": "Alice",
              "age": 30,
              "city": "Rome",
              "interests": ["reading", "hiking", "coding"]
            }
            ```
        """)
        nb.md("""
            In Python le richieste HTTP si inviano con la libreria `requests`, e il procedimento è sempre lo
            stesso. Si definiscono l'endpoint e i parametri, si invia la richiesta e si converte il JSON
            ricevuto in un DataFrame. Come esempio usiamo gli open data di Regione Lombardia sulle stazioni
            meteo, divisi in due risorse:

            - l'anagrafica dei sensori, `https://www.dati.lombardia.it/resource/nf78-nj6b.json`;
            - le misure dei sensori, `https://www.dati.lombardia.it/resource/647i-nhxk.json`.

            La prima richiesta chiede l'anagrafica con `requests.get()`; il parametro `timeout` evita che la
            cella resti in attesa indefinitamente se il server non risponde.
        """)
        nb.code("""
            import requests

            url = "https://www.dati.lombardia.it/resource/nf78-nj6b.json"
            response = requests.get(url, timeout=30)
            response
        """, rete=True)
        nb.md("""
            Il risultato della cella, `<Response [200]>`, riporta il *codice di stato* della risposta, un
            numero che indica com'è andata la richiesta. I codici che si incontrano più spesso sono questi:

            - `200` indica che la richiesta è stata completata correttamente;
            - `404` indica che la risorsa non è stata trovata, di solito perché l'URL è sbagliato;
            - `500` indica un errore del server.

            Con `response.json()` trasformiamo il testo della risposta in una lista di dizionari Python e ne
            contiamo gli elementi; nella cella successiva guardiamo il primo, che descrive un sensore.
        """)
        nb.code("""
            risposta_json = response.json()
            len(risposta_json)
        """, rete=True)
        nb.code("risposta_json[0]", rete=True)
        nb.sottosezione("Parametri di query", intro="""
            Spesso non vogliamo tutti i dati disponibili, ma solo una parte. Per questo molte API accettano
            dei **parametri di query**, che si aggiungono alla fine dell'URL dopo il simbolo `?` e si
            scrivono come coppie `chiave=valore`, separate da `&` quando sono più di una. Nell'esempio
            chiediamo soltanto i sensori di precipitazione della provincia di Milano.
        """)
        nb.code("""
            # URL con i parametri di query per la provincia di Milano
            url = "https://www.dati.lombardia.it/resource/nf78-nj6b.json?provincia=MI&tipologia=Precipitazione"
            response = requests.get(url, timeout=30)
            dati = response.json()
            dati[:4]
        """, rete=True)
        nb.md("""
            Con `requests` gli stessi parametri si possono scrivere in un dizionario, passato con l'argomento
            `params`, e la libreria costruisce da sola l'URL completo. Il risultato è identico a quello della
            cella precedente, ma il codice è più leggibile e i parametri sono più facili da modificare.
        """)
        nb.code("""
            parametri = {
                "provincia": "MI",
                "tipologia": "Precipitazione",
            }
            url = "https://www.dati.lombardia.it/resource/nf78-nj6b.json"
            response = requests.get(url, params=parametri, timeout=30)
            dati = response.json()
            dati[:4]
        """, rete=True)
        nb.sottosezione("L'anagrafica dei sensori", intro="""
            Recuperiamo adesso l'anagrafica completa dei sensori. Il portale riconosce alcuni parametri
            speciali, che iniziano con `$`; tra questi `$limit` indica quante righe vogliamo ricevere, e senza
            di esso il portale ne restituisce soltanto mille. Il metodo `raise_for_status()` interrompe la
            cella con un errore se il codice di stato segnala un problema, in modo da non proseguire con dati
            incompleti. La lista di dizionari ricevuta diventa infine un DataFrame con `pd.DataFrame()`.
        """)
        nb.code("""
            url_sensori = "https://www.dati.lombardia.it/resource/nf78-nj6b.json"
            parametri = {"$limit": 5000}
            response = requests.get(url_sensori, params=parametri, timeout=30)
            response.raise_for_status()

            sensori_df = pd.DataFrame(response.json())
            sensori_df.head()
        """, rete=True)
        nb.md("""
            Se l'API non risponde, la cella qui sotto permette di proseguire comunque, perché legge dati di
            esempio nello stesso formato da un file di riserva. Il modulo `json` della libreria standard
            trasforma il contenuto del file nella stessa lista di dizionari che avremmo ricevuto dal portale.
        """)
        nb.code("""
            import json

            with open("../Dati/fallback/lombardia_sensori.json", encoding="utf-8") as f:
                sensori_df = pd.DataFrame(json.load(f))
            sensori_df.head()
        """)
        nb.md("""
            Per farci un'idea del contenuto guardiamo i valori distinti di due colonne. Il metodo `unique()`
            restituisce i valori diversi presenti in una colonna, e lo applichiamo prima alla tipologia del
            sensore e poi alla provincia.
        """)
        nb.code('sensori_df["tipologia"].unique()')
        nb.code('sensori_df["provincia"].unique()')
        nb.md("""
            Teniamo soltanto i sensori di temperatura della provincia di Milano. Il filtro mette tra parentesi
            quadre due condizioni unite da `&`, ciascuna tra parentesi tonde, e conserva le righe che le
            rispettano entrambe. La selezione condizionale è uno degli argomenti del notebook sulle
            operazioni, dove la vedremo in dettaglio; per ora basta saperla leggere.
        """)
        nb.code("""
            sensori_milano = sensori_df[(sensori_df["tipologia"] == "Temperatura") & (sensori_df["provincia"] == "MI")]
            sensori_milano.head()
        """)
        nb.sottosezione("Le misure di un sensore", intro="""
            Con l'identificativo di un sensore possiamo recuperarne le misure dalla seconda risorsa del
            portale. Scegliamo il sensore 2001, il termometro di Milano in via Brera, e salviamo il suo
            identificativo in una variabile, come testo, perché il portale riporta tutti i valori in questa
            forma.
        """)
        nb.code('idsensore = "2001"')
        nb.md("""
            La richiesta segue lo stesso schema di prima. Nel dizionario dei parametri indichiamo il sensore
            con `idsensore` e alziamo `$limit` a 100000, in modo da ricevere molte più misure delle mille
            previste in assenza di indicazioni.
        """)
        nb.code("""
            url_misure = "https://www.dati.lombardia.it/resource/647i-nhxk.json"
            parametri_misure = {
                "idsensore": idsensore,
                "$limit": 100000,
            }
            response = requests.get(url_misure, params=parametri_misure, timeout=30)
            response.raise_for_status()

            misure_df = pd.DataFrame(response.json())
            misure_df
        """, rete=True)
        nb.md("""
            Anche per le misure è disponibile un file di riserva, che la cella qui sotto legge nel caso in cui
            il portale non risponda.
        """)
        nb.code("""
            with open("../Dati/fallback/lombardia_misure_2001.json", encoding="utf-8") as f:
                misure_df = pd.DataFrame(json.load(f))
            misure_df
        """)
        nb.md("""
            Il portale restituisce tutti i valori come testo, quindi prima di usarli convertiamo la colonna
            `data` in datetime con `pd.to_datetime()` e la colonna `valore` in numero con `pd.to_numeric()`, e
            ordiniamo le righe per data. Il valore `-9999` indica una misura mancante, e per questo togliamo
            le righe che lo contengono. Queste conversioni anticipano il notebook sulle date, dove le
            riprenderemo con calma.
        """)
        nb.code("""
            misure_df["data"] = pd.to_datetime(misure_df["data"])
            misure_df["valore"] = pd.to_numeric(misure_df["valore"], errors="coerce")
            misure_df = misure_df.sort_values("data")
            misure_df = misure_df[misure_df["valore"] != -9999]
        """)
        nb.md("""
            Infine visualizziamo l'andamento della temperatura nelle ultime 100 misure, selezionate con
            `iloc[-100:]`. La funzione `px.line()` di Plotly disegna una linea a partire dalle colonne
            indicate in `x` e `y`; Plotly è l'argomento di un notebook successivo, dove vedremo le sue opzioni.
        """)
        nb.code("""
            import plotly.express as px

            df_grafico = misure_df.iloc[-100:]

            fig = px.line(
                df_grafico,
                x="data",
                y="valore",
                markers=True,
                title=f"Andamento della temperatura per IDsensore {idsensore}",
                labels={"data": "Data e ora", "valore": "Temperatura (°C)"},
            )
            fig.show()
        """)

    nb.md("Riassunto in una pagina: [Da Excel a pandas](../Schede/Scheda_Excel_pandas.md).")

    # ------------------------------------------------------------------ 8
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Lettura di un CSV italiano",
        scenario="""
            Per un primo controllo delle letture dei POD ci servono soltanto tre colonne del file, cioè il
            codice del POD, la fascia e i kWh, e il consumo complessivo di tutte le righe.
        """,
        richiesta="""
            1. Leggi `../Dati/letture_pod_2025.csv` nel DataFrame `letture_kwh`, tenendo solo le colonne
               `pod`, `fascia` e `kwh`.
            2. Calcola la somma della colonna `kwh` e salvala in `totale_kwh`.

            Il DataFrame risultante ha 216 righe e 3 colonne, e il totale è di circa 134507.7 kWh.
        """,
        suggerimento="i parametri che servono sono `sep`, `decimal`, `encoding` e `usecols`, e la somma di una colonna si calcola con `.sum()`.",
        starter="""
            letture_kwh = pd.read_csv("../Dati/letture_pod_2025.csv", ...)
            totale_kwh = ...
            totale_kwh
        """,
        soluzione="""
            letture_kwh = pd.read_csv(
                "../Dati/letture_pod_2025.csv",
                sep=";",
                decimal=",",
                encoding="latin-1",
                usecols=["pod", "fascia", "kwh"],
            )
            totale_kwh = letture_kwh["kwh"].sum()
            totale_kwh
        """,
        verifica="""
            assert list(letture_kwh.columns) == ["pod", "fascia", "kwh"], "❌ letture_kwh: servono solo pod, fascia e kwh (usecols)"
            assert round(totale_kwh, 1) == 134507.7, "❌ totale_kwh: controlla decimal=\\",\\""
        """,
        perche="""
            Il parametro `usecols` limita la lettura alle tre colonne richieste. Senza `decimal=","` la
            colonna `kwh` resterebbe testo, e la somma non darebbe un numero.
        """,
    )
    nb.esercizio(
        titolo="Due fogli Excel in una tabella",
        scenario="""
            Un negozio tiene le vendite di gennaio e di febbraio in due fogli dello stesso file Excel e vuole
            analizzarle in un'unica tabella.
        """,
        richiesta="""
            1. Scrivi i DataFrame `gennaio` e `febbraio` nel file `vendite.xlsx`, rispettivamente nei fogli
               `Gennaio` e `Febbraio`.
            2. Leggi tutti i fogli del file nel dizionario `fogli`.
            3. Concatena i fogli nel DataFrame `vendite`, con un indice che va da 0 a 5.

            Il risultato è un DataFrame di 6 righe con le colonne `prodotto` e `pezzi`.
        """,
        suggerimento="il file si scrive con `pd.ExcelWriter`, tutti i fogli si leggono con `sheet_name=None` e con `pd.concat(..., ignore_index=True)` l'indice riparte da 0.",
        starter="""
            gennaio = pd.DataFrame({"prodotto": ["pane", "latte", "caffè"], "pezzi": [120, 80, 45]})
            febbraio = pd.DataFrame({"prodotto": ["pane", "latte", "caffè"], "pezzi": [110, 95, 50]})

            with pd.ExcelWriter("vendite.xlsx") as writer:
                ...

            fogli = ...
            vendite = ...
            vendite
        """,
        soluzione="""
            gennaio = pd.DataFrame({"prodotto": ["pane", "latte", "caffè"], "pezzi": [120, 80, 45]})
            febbraio = pd.DataFrame({"prodotto": ["pane", "latte", "caffè"], "pezzi": [110, 95, 50]})

            with pd.ExcelWriter("vendite.xlsx") as writer:
                gennaio.to_excel(writer, sheet_name="Gennaio", index=False)
                febbraio.to_excel(writer, sheet_name="Febbraio", index=False)

            fogli = pd.read_excel("vendite.xlsx", sheet_name=None)
            vendite = pd.concat(fogli.values(), ignore_index=True)
            vendite
        """,
        verifica="""
            assert list(fogli.keys()) == ["Gennaio", "Febbraio"], "❌ fogli: il file deve avere i fogli Gennaio e Febbraio"
            assert len(vendite) == 6 and list(vendite.index) == list(range(6)), "❌ vendite: 6 righe con indice da 0 a 5 (ignore_index=True)"
            assert vendite["pezzi"].sum() == 500, "❌ vendite: il totale dei pezzi è 500"
        """,
    )
    nb.esercizio(
        titolo="Le letture di un POD dal database",
        scenario="""
            Un POD è il codice che identifica un punto di prelievo dell'energia elettrica. Dal database
            `utility.db` ci servono le letture giornaliere di marzo di un solo POD.
        """,
        richiesta="""
            1. Apri la connessione a `../Dati/utility.db`.
            2. Con una query, leggi dalla tabella `letture` solo le righe del POD `IT001E10000000` e salvale
               nel DataFrame `letture_pod`.
            3. Salva in `totale_marzo` la somma della colonna `kwh`, poi chiudi la connessione.

            Il DataFrame ha 31 righe, una per giorno, e il totale è di 7785.6 kWh.
        """,
        suggerimento="dentro la query i valori di testo vanno tra apici singoli, come in `WHERE pod = '...'`.",
        starter="""
            con = ...
            letture_pod = pd.read_sql(..., con)
            totale_marzo = ...
            con.close()
            totale_marzo
        """,
        soluzione="""
            con = sqlite3.connect("../Dati/utility.db")
            letture_pod = pd.read_sql("SELECT * FROM letture WHERE pod = 'IT001E10000000'", con)
            totale_marzo = letture_pod["kwh"].sum()
            con.close()
            totale_marzo
        """,
        verifica="""
            assert len(letture_pod) == 31, "❌ letture_pod: servono le 31 righe del solo POD IT001E10000000"
            assert round(totale_marzo, 1) == 7785.6, "❌ totale_marzo: somma la colonna kwh"
        """,
        facoltativo=True,
    )
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="La certificazione energetica degli edifici in Lombardia",
            scenario="""
                Regione Lombardia pubblica sul proprio portale di open data i certificati energetici degli
                edifici. Per questo esercizio serve la connessione alla rete, perché non c'è un file di
                riserva.
            """,
            richiesta="""
                1. Recupera i dati dall'endpoint `https://www.dati.lombardia.it/resource/rsg3-xhvk.json` e
                   salvali nel DataFrame `certificati`.
                2. Tieni solo gli edifici della provincia di Milano nel DataFrame `milano`.
                3. Calcola le emissioni medie di CO2 per ciascuna classe energetica e salvale in
                   `co2_per_classe`.

                Il risultato è una Series con una riga per classe energetica (A4, A3, ..., G) e le emissioni
                medie di CO2 di ciascuna.
            """,
            suggerimento="""
                conviene guardare prima `certificati.columns` e i valori di una colonna con `unique()`. I numeri
                arrivano come testo e vanno convertiti con `pd.to_numeric`, mentre la media per gruppo si
                scrive `df.groupby("colonna")["altra"].mean()`.
            """,
            starter="""
                url = "https://www.dati.lombardia.it/resource/rsg3-xhvk.json"
                response = ...
                certificati = ...

                milano = ...
                co2_per_classe = ...
                co2_per_classe
            """,
            soluzione="""
                url = "https://www.dati.lombardia.it/resource/rsg3-xhvk.json"
                response = requests.get(url, params={"$limit": 50000}, timeout=30)
                response.raise_for_status()
                certificati = pd.DataFrame(response.json())

                milano = certificati[certificati["provincia"] == "MILANO"].copy()
                milano["emissioni_di_co2"] = pd.to_numeric(milano["emissioni_di_co2"], errors="coerce")
                co2_per_classe = milano.groupby("classe_energetica")["emissioni_di_co2"].mean()
                co2_per_classe
            """,
            perche="""
                Prima di scrivere il filtro conviene controllare i nomi delle colonne con `certificati.columns`
                e i valori della provincia con `unique()`, perché il portale scrive la provincia per esteso e
                in maiuscolo. Se il portale cambiasse questi nomi, basterebbe adattare la maschera e il
                `groupby`.
            """,
            verifica="""
                assert 0 < len(milano) < len(certificati), "❌ milano deve avere solo le righe della provincia di Milano"
                assert len(co2_per_classe) > 1 and co2_per_classe.index.is_unique, "❌ co2_per_classe: una riga per classe energetica, con la media"
            """,
            rete=True,
            facoltativo=True,
        )
    return nb
