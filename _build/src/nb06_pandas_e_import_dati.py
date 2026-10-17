"""06 · Pandas: Series, DataFrame e import dei dati."""

from nbkit import Notebook

DATI_BASE = [
    "TexasTurbine.csv",
    "letture_pod_2025.csv",
    "load_total_north_hourly_2024.xlsx",
    "utility.db",
    "homework/letture_marzo.csv",
    "homework/clienti.xlsx",
    "homework/anagrafica.db",
]
EXCEL = "../Dati/homework/clienti.xlsx"
DB = "../Dati/homework/anagrafica.db"


def costruisci() -> Notebook:
    nb = Notebook(
        num="06",
        file="06_Pandas_e_import_dati",
        titolo="Pandas: Series, DataFrame e import dei dati",
        blocco=2,
        giornata=2,
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
        tempo={"base": 55, "avanzata": 70},
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
    nb.hands_on(
        aula="base",
        richiesta="""
            Salva in `prime_due` le prime due righe di `df`, con il metodo `head()` visto nel notebook 05, e in
            `forma` il suo attributo `shape`. Poiché `df` ha tre righe e tre colonne, `forma` deve valere `(3, 3)`.
        """,
        starter="""
            prime_due = ...
            forma = ...
            print(forma)
            prime_due
        """,
        soluzione="""
            prime_due = df.head(2)
            forma = df.shape
            print(forma)
            prime_due
        """,
        verifica="""
            assert list(prime_due.index) == ["id_1", "id_2"], "❌ prime_due: le prime due righe si ottengono con df.head(2)"
            assert forma == (3, 3), "❌ forma: shape è un attributo, quindi si scrive senza parentesi"
        """,
        prova_anche="con `head(1)`.",
    )

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
    nb.hands_on(
        richiesta="""
            Salva in `file_dati` l'elenco dei file contenuti nella cartella `Dati`, passando a `os.listdir()` il
            percorso relativo della cartella. Nell'elenco devono comparire, tra gli altri, `TexasTurbine.csv` e
            `utility.db`.
        """,
        starter="""
            # suggerimento: specifica il percorso della cartella in listdir()
            file_dati = ...
            for file in file_dati:
                print(file)
        """,
        soluzione="""
            file_dati = os.listdir("../Dati")
            for file in file_dati:
                print(file)
        """,
        verifica="""
            assert "TexasTurbine.csv" in file_dati and "utility.db" in file_dati, "❌ file_dati: il percorso relativo della cartella è \\"../Dati\\""
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
    nb.hands_on(
        richiesta="""
            Rileggi `letture_pod_2025.csv` con gli stessi tre parametri e aggiungi `usecols`, in modo da tenere
            soltanto le colonne `cliente`, `fascia` e `kwh`. Il DataFrame `letture_ridotte` deve avere 216 righe e
            3 colonne.
        """,
        starter="""
            letture_ridotte = pd.read_csv(
                "../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1", usecols=...
            )
            letture_ridotte.head()
        """,
        soluzione="""
            letture_ridotte = pd.read_csv(
                "../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1", usecols=["cliente", "fascia", "kwh"]
            )
            letture_ridotte.head()
        """,
        verifica="""
            assert list(letture_ridotte.columns) == ["cliente", "fascia", "kwh"], "❌ letture_ridotte: usecols riceve la lista delle tre colonne"
            assert letture_ridotte.shape == (216, 3), "❌ letture_ridotte: le righe sono 216, come nel file"
        """,
    )

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
    nb.hands_on(
        richiesta="""
            Leggi in `df_foglio2` il secondo foglio di `dati.xlsx`, indicandone il nome con `sheet_name`. La
            colonna `Nome` deve contenere David, Eva e Frank.
        """,
        starter="""
            df_foglio2 = pd.read_excel("dati.xlsx", sheet_name=...)
            df_foglio2
        """,
        soluzione="""
            df_foglio2 = pd.read_excel("dati.xlsx", sheet_name="Foglio2")
            df_foglio2
        """,
        verifica="""
            assert list(df_foglio2["Nome"]) == ["David", "Eva", "Frank"], "❌ df_foglio2: il secondo foglio si chiama \\"Foglio2\\""
        """,
    )
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
    nb.hands_on(
        richiesta="""
            Cambia la condizione del `WHERE` in modo da leggere in `pod_piccoli` i POD con una potenza inferiore a
            10 kW. Le righe sono 9, tutte con 3 o 6 kW.
        """,
        starter="""
            pod_piccoli = pd.read_sql("SELECT * FROM pod WHERE ...", con)
            pod_piccoli
        """,
        soluzione="""
            pod_piccoli = pd.read_sql("SELECT * FROM pod WHERE potenza_kw < 10", con)
            pod_piccoli
        """,
        verifica="""
            assert len(pod_piccoli) == 9, "❌ pod_piccoli: la condizione è potenza_kw < 10"
        """,
        prova_anche="con `potenza_kw = 50`, che dà 5 righe.",
    )
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
        nb.hands_on(
            rete=True,
            richiesta="""
                Ripeti la richiesta cambiando i due parametri, in modo da ricevere in `dati_bg` i sensori di
                temperatura della provincia di Bergamo, che il portale indica con `BG`. Ogni elemento della
                risposta deve avere `"BG"` alla chiave `"provincia"`.
            """,
            starter="""
                parametri_bg = {
                    "provincia": ...,
                    "tipologia": ...,
                }
                response = requests.get(url, params=parametri_bg, timeout=30)
                dati_bg = response.json()
                dati_bg[:4]
            """,
            soluzione="""
                parametri_bg = {
                    "provincia": "BG",
                    "tipologia": "Temperatura",
                }
                response = requests.get(url, params=parametri_bg, timeout=30)
                dati_bg = response.json()
                dati_bg[:4]
            """,
            verifica="""
                assert len(dati_bg) > 0 and all(d["provincia"] == "BG" for d in dati_bg), "❌ dati_bg: il parametro provincia vale \\"BG\\""
                assert all(d["tipologia"] == "Temperatura" for d in dati_bg), "❌ dati_bg: il parametro tipologia vale \\"Temperatura\\""
            """,
            prova_anche='con la tipologia `"Precipitazione"`.',
        )
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

    # ------------------------------------------------------------------ Extra
    nb.sezione("Extra", intro="""
        Questa sezione raccoglie esercizi brevi sui punti principali del notebook, cioè la lettura di un CSV
        italiano, di un foglio Excel e di una tabella SQL, da fare a casa per ripassare. Durante la lezione la
        saltiamo, e ogni esercizio ha la sua verifica, che conferma il risultato o dice che cosa controllare.
    """)
    nb.esercizio(
        titolo="Il file del distributore",
        scenario="""
            Lavoriamo nell'ufficio consumi di una piccola società di vendita di energia, e il distributore ci manda
            il CSV con le letture giornaliere di marzo degli otto POD dei nostri clienti, scritto all'italiana con
            il punto e virgola tra le colonne e la virgola nei decimali. Un'officina di Lecco segnala una bolletta
            di marzo tripla del solito, quindi leggiamo il file con pandas e controlliamo con `info()` e
            `describe()` che i consumi siano arrivati come numeri e quale sia la lettura più alta. La tabella ha 248
            righe e tre colonne, `kwh` è di tipo `float64` e il massimo è di 1530.3 kWh, molto sopra i 250 kWh di
            una giornata normale.
        """,
        richiesta="""
            1. Leggi `../Dati/homework/letture_marzo.csv` in `letture`, indicando a `read_csv` il separatore delle
               colonne e quello dei decimali.
            2. Le istruzioni già scritte sotto la lettura mostrano i tipi delle colonne con `info()`, le prime righe
               con `head()` e le statistiche con `describe()`. Controlla che `kwh` sia `float64`, perché un numero
               letto come testo non si può sommare né confrontare con altri numeri, e leggi il massimo nella riga
               `max` di `describe()`.
        """,
        suggerimenti=[
            """
                Un CSV salvato da Excel in italiano usa un separatore di colonne e un separatore decimale diversi
                da quelli standard, e `read_csv` ha un parametro per ciascuno.
            """,
            """
                Servono `sep=";"` e `decimal=","`; se `kwh` risulta letta come testo, di solito manca il
                `decimal`.
            """,
        ],
        starter="""
            letture = pd.read_csv("../Dati/homework/letture_marzo.csv", ...)
            letture.info()
            print(letture.head())
            print(letture.describe())
        """,
        soluzione="""
            letture = pd.read_csv("../Dati/homework/letture_marzo.csv", sep=";", decimal=",")
            letture.info()
            print(letture.head())
            print(letture.describe())
        """,
        verifica="""
            assert letture.shape == (248, 3), "❌ letture: 248 righe e 3 colonne, controlla sep"
            assert letture["kwh"].dtype == "float64", "❌ letture: kwh deve essere numerica, controlla decimal"
        """,
        perche="""
            `info()` mostra subito se `kwh` è stata letta come numero, perché in quel caso il suo tipo è `float64`.
            Questo file si legge senza indicare `encoding`, a differenza di `letture_pod_2025.csv`, e il massimo
            di 1530.3 kWh, lontano dalla media di circa 77 kWh, è la lettura da segnalare al distributore.
        """,
    )

    scenario_sabato = """
        Siamo di reperibilità nel fine settimana e l'Officina Meccanica Fumagalli, che contesta la bolletta, chiede
        la potenza del suo contatore e i prezzi per fascia che le applichiamo. Il gestionale è spento, ma la potenza
        sta nella tabella `pod` del database dell'anagrafica e i prezzi nel foglio Listino dell'Excel dei clienti, e
        con pandas leggiamo da lì soltanto quello che serve, in poche righe che tornano utili alla prossima
        reperibilità. Il contatore dell'officina ha 30 kW e i prezzi sono di 0.21, 0.19 e 0.17 euro/kWh nelle
        fasce F1, F2 e F3.
    """
    nb.esercizio(
        aula="base",
        titolo="La reperibilità",
        scenario=scenario_sabato,
        richiesta=f"""
            1. Leggi in `listino` il foglio `Listino` di `{EXCEL}`, indicandolo con `sheet_name`, perché senza
               questo parametro `read_excel` legge il primo foglio, che è l'anagrafica dei clienti.
            2. Apri `{DB}` con `sqlite3.connect` e leggi con `pd.read_sql` in `officina` la sola riga dell'officina
               della tabella `pod`, con un `WHERE` sulla colonna `cliente`. La riga `con.close()`, già scritta
               nella cella, chiude poi la connessione, che a quel punto non serve più.
        """,
        suggerimenti=[
            """
                Con `read_excel` il foglio si sceglie con `sheet_name`; con il database si apre la connessione, si
                legge con `read_sql` e si chiude la connessione.
            """,
            "In SQL il testo va tra apici singoli: `WHERE cliente = 'Officina Meccanica Fumagalli'`.",
        ],
        starter=f"""
            import sqlite3

            listino = pd.read_excel("{EXCEL}", sheet_name=...)

            con = sqlite3.connect("{DB}")
            officina = pd.read_sql("...", con)
            con.close()

            print(listino)
            officina
        """,
        soluzione=f"""
            import sqlite3

            listino = pd.read_excel("{EXCEL}", sheet_name="Listino")

            con = sqlite3.connect("{DB}")
            officina = pd.read_sql("SELECT * FROM pod WHERE cliente = 'Officina Meccanica Fumagalli'", con)
            con.close()

            print(listino)
            officina
        """,
        verifica="""
            assert set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ listino: è il foglio Listino? Controlla sheet_name"
            assert list(officina["potenza_kw"]) == [30.0], "❌ officina: una riga sola, presa dalla tabella pod con il WHERE"
        """,
        perche="""
            Il filtro con `WHERE` viene eseguito dal database, che restituisce a pandas soltanto la riga richiesta.
            Con una tabella di otto righe la differenza non si nota, ma su tabelle grandi evita di caricare in
            memoria dati che non servono.
        """,
    )
    nb.esercizio(
        aula="avanzata",
        titolo="La reperibilità",
        scenario=scenario_sabato,
        richiesta=f"""
            1. Leggi in `listino` il foglio `Listino` di `{EXCEL}`, scelto con `sheet_name`, perché il primo foglio
               del file è l'anagrafica dei clienti.
            2. Scrivi la funzione `leggi_tabella(nome)`, che apre `{DB}` con `sqlite3.connect`, legge tutta la
               tabella `nome` con `pd.read_sql`, chiude la connessione e restituisce il DataFrame, in modo che alla
               prossima reperibilità basti una riga per leggere una tabella senza lasciare aperta la connessione.
               Usala per mettere in `potenze` la tabella `pod`.
            3. In `officina` metti la sola riga dell'Officina Meccanica Fumagalli, filtrando `potenze` con una
               condizione sulla colonna `cliente`, come abbiamo fatto con i sensori di Milano.
        """,
        suggerimenti=[
            """
                La funzione racchiude i tre passi del database, apertura, lettura e chiusura, e il nome ricevuto
                entra nella query con una f-string: `f"SELECT * FROM {nome}"`.
            """,
        ],
        starter=f"""
            import sqlite3


            def leggi_tabella(nome):
                ...


            listino = pd.read_excel("{EXCEL}", sheet_name=...)
            potenze = leggi_tabella("pod")
            officina = ...

            print(listino)
            officina
        """,
        soluzione=f'''
            import sqlite3


            def leggi_tabella(nome):
                """Legge tutta la tabella `nome` da anagrafica.db e la restituisce come DataFrame."""
                con = sqlite3.connect("{DB}")
                df = pd.read_sql(f"SELECT * FROM {{nome}}", con)
                con.close()
                return df


            listino = pd.read_excel("{EXCEL}", sheet_name="Listino")
            potenze = leggi_tabella("pod")
            officina = potenze[potenze["cliente"] == "Officina Meccanica Fumagalli"]

            print(listino)
            officina
        ''',
        verifica="""
            assert set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ listino: è il foglio Listino? Controlla sheet_name"
            assert leggi_tabella("pod").shape == (8, 3), "❌ leggi_tabella: deve restituire tutta la tabella, 8 righe e 3 colonne"
            assert list(officina["potenza_kw"]) == [30.0], "❌ officina: una riga sola, quella dell'Officina Meccanica Fumagalli"
        """,
        perche="""
            La funzione raccoglie in un solo punto l'apertura della connessione, la lettura e la chiusura, così ogni
            chiamata chiude la connessione che ha aperto e nessuna resta aperta per dimenticanza. Il filtro
            sull'officina si applica invece in pandas, con la stessa forma usata per i sensori di Milano, perché la
            tabella è già in memoria.
        """,
    )
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="La certificazione energetica degli edifici in Lombardia",
            scenario="""
                Regione Lombardia pubblica sul portale di open data i certificati energetici degli edifici, con
                la classe energetica e le emissioni di CO2 di ciascuno. Vogliamo sapere quanta CO2 emette in
                media un edificio di ogni classe in provincia di Milano, e con `requests` e pandas prendiamo i
                dati direttamente dal portale, senza scaricare file a mano. Il risultato è una Series con una
                riga per ciascuna classe presente nei dati, dalle più efficienti, come A+, fino alla G. Per
                questo esercizio serve la rete, perché non c'è un file di riserva.
            """,
            richiesta="""
                1. Recupera i dati dall'endpoint `https://www.dati.lombardia.it/resource/rsg3-xhvk.json` e
                   salvali nel DataFrame `certificati`.
                2. Tieni solo gli edifici della provincia di Milano nel DataFrame `milano`.
                3. Calcola le emissioni medie di CO2 per ciascuna classe energetica e salvale in
                   `co2_per_classe`.
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

                milano = certificati[certificati["provincia"] == "MI"].copy()
                milano["emissioni_di_co2"] = pd.to_numeric(milano["emissioni_di_co2"], errors="coerce")
                co2_per_classe = milano.groupby("classe_energetica")["emissioni_di_co2"].mean()
                co2_per_classe
            """,
            perche="""
                Prima di scrivere il filtro conviene controllare i nomi delle colonne con `certificati.columns`
                e i valori della provincia con `unique()`, perché il portale indica la provincia con la sigla,
                `MI`, mentre il comune è scritto per esteso e in maiuscolo. Se il portale cambiasse questi
                nomi, basterebbe adattare la maschera e il `groupby`.
            """,
            verifica="""
                assert 0 < len(milano) < len(certificati), "❌ milano deve avere solo le righe della provincia di Milano"
                assert len(co2_per_classe) > 1 and co2_per_classe.index.is_unique, "❌ co2_per_classe: una riga per classe energetica, con la media"
            """,
            rete=True,
            facoltativo=True,
        )
    return nb
