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
        intento="Le due strutture dati di pandas, Series e DataFrame, e la lettura dei dati da file e da database.",
        obiettivi={
            "base": [
                "creare Series e DataFrame e accedere ai loro elementi",
                "leggere file CSV ed Excel con i parametri di lettura, anche più file o più fogli insieme",
                "caricare una tabella da un database SQL con una query",
            ],
            "avanzata": [
                "creare Series e DataFrame e leggere file CSV ed Excel con i parametri di lettura",
                "caricare una tabella da un database SQL con una query",
                "chiedere dati a un'API con `requests` e trasformare la risposta JSON in un DataFrame",
            ],
        },
        tempo={"base": 70, "avanzata": 90},
        dati={
            "base": DATI_BASE,
            "avanzata": DATI_BASE + ["fallback/lombardia_sensori.json", "fallback/lombardia_misure_2001.json"],
        },
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Importare le librerie", intro="""
        Pandas è una libreria open-source per l'analisi e la manipolazione dei dati: offre strutture dati e
        funzioni per lavorare con dati strutturati, come tabelle e serie temporali.

        Per usare una libreria la importiamo con la parola chiave `import`. È buona pratica importare le
        librerie all'inizio del notebook.
    """)
    nb.code("import pandas as pd")

    # ------------------------------------------------------------------ 2
    nb.sezione("Le strutture dati di pandas", intro="""
        Pandas fornisce due strutture dati principali:

        - **Series**: array unidimensionali etichettati;
        - **DataFrame**: strutture bidimensionali con righe e colonne etichettate.
    """)
    nb.sottosezione("Series", intro="""
        Una **Series** è un array unidimensionale che può contenere qualsiasi tipo di dato (interi, stringhe,
        numeri decimali, oggetti Python). Ogni elemento è associato a un'etichetta, chiamata **indice**.
    """)
    nb.code("""
        # creare una Series da una lista
        dati = [10, 20, 30, 40]
        s = pd.Series(dati, name="valori")
        s
    """)
    nb.md("Possiamo specificare un indice personalizzato:")
    nb.code("""
        s_custom = pd.Series(dati, index=["a", "b", "c", "d"])
        s_custom
    """)
    nb.md("""
        Agli elementi di una Series si accede con l'indice, come per gli elementi di una lista.
    """)
    nb.code("""
        # accesso tramite indice numerico
        s[0]
    """)
    nb.code("""
        # accesso tramite indice personalizzato
        s_custom["b"]
    """)
    nb.md("Possiamo fare slicing, come con le liste Python:")
    nb.code("""
        # slicing della Series
        s[1:3]
    """)
    nb.sottosezione("DataFrame", intro="""
        Un **DataFrame** è una struttura bidimensionale con dati allineati in righe e colonne, simile a un
        foglio di calcolo o a una tabella SQL. Lo creiamo da un dizionario: ogni chiave diventa una colonna.
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
        Il modulo `os` di Python serve a interagire con il sistema operativo: navigare tra le cartelle,
        gestire file, ottenere informazioni sul sistema. `os.listdir()` elenca file e cartelle.
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
        La cartella di lavoro di un notebook è quella in cui si trova il file. I dati stanno nella cartella
        `Dati`, un livello più su: `..` indica la cartella superiore, quindi il percorso è `../Dati/`.
    """)
    nb.code("os.getcwd()")
    nb.code('os.path.exists("../Dati/TexasTurbine.csv")')
    nb.prova_tu(
        richiesta="""
            Stampa la lista dei file nella cartella `Dati`. Il risultato atteso è un elenco che comprende,
            tra gli altri, `TexasTurbine.csv` e `utility.db`.
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
        tabulari. Pandas li legge con `read_csv()`.
    """)
    nb.code("""
        # leggere un file CSV
        df_turbina = pd.read_csv("../Dati/TexasTurbine.csv")
        df_turbina.head()
    """)
    nb.md("""
        `head()` mostra le prime righe. `info()` riassume righe, colonne, tipi e quanti valori non mancano;
        `describe()` calcola le statistiche principali delle colonne numeriche.
    """)
    nb.code("df_turbina.info()")
    nb.code("df_turbina.describe()")
    nb.sottosezione("Trovare e leggere più file CSV", intro="""
        Il modulo `glob` trova i file il cui nome segue uno schema, per esempio tutti quelli che finiscono
        con `.csv`. Prima creiamo due file CSV di esempio.
    """)
    nb.code("""
        df1 = pd.DataFrame({
            "ID": [1, 2, 3],
            "Nome": ["Alice", "Bob", "Charlie"],
            "Età": ["25", "30", "35"],  # intenzionalmente come stringhe
        })
        df2 = pd.DataFrame({
            "ID": [4, 5, 6],
            "Nome": ["David", "Eva", "Frank"],
            "Età": ["40", "45", "50"],  # intenzionalmente come stringhe
        })
    """)
    nb.code("""
        # salviamo i DataFrame come file CSV
        df1.to_csv("dati1.csv", index=False)
        df2.to_csv("dati2.csv", index=False)
        print("File 'dati1.csv' e 'dati2.csv' creati.")
    """)
    nb.code("""
        from glob import glob

        # cerchiamo i file CSV che iniziano con "dati"
        file_csv = sorted(glob("dati*.csv"))
        print("File CSV trovati:")
        for file in file_csv:
            print(file)
    """)
    nb.code("""
        # leggere il primo file CSV
        df_csv1 = pd.read_csv("dati1.csv")
        df_csv1
    """)
    nb.sottosezione("Specificare i tipi di dato", intro="""
        Durante la lettura pandas prova a riconoscere da solo il tipo di ogni colonna. A volte serve
        indicarlo noi, con il parametro `dtype`. Supponiamo di volere la colonna `Età` sicuramente come intero.
    """)
    nb.code("""
        # leggere il CSV specificando i tipi di dato
        tipi_colonne = {"ID": int, "Nome": str, "Età": int}
        df_csv1_tipizzato = pd.read_csv("dati1.csv", dtype=tipi_colonne)
        df_csv1_tipizzato.dtypes
    """)
    nb.md("""
        Altri parametri utili di `read_csv()`:

        - **`usecols`**: quali colonne leggere dal file;
        - **`sep`**: il delimitatore (`,`, `;`, `\\t`);
        - **`decimal`**: il separatore dei decimali (per esempio `,` invece di `.`).
    """)
    nb.md("""
        Per unire i dati di più file leggiamo ogni file in un DataFrame, mettiamo i DataFrame in una lista e
        li concateniamo con `pd.concat()`.
    """)
    nb.code("""
        # leggere tutti i file CSV e aggiungerli a una lista
        dfs = []
        for nome_file in file_csv:
            df = pd.read_csv(nome_file, dtype=tipi_colonne)
            dfs.append(df)
    """)
    nb.code("""
        # concatenare i DataFrame
        df_unito = pd.concat(dfs, ignore_index=True)
        df_unito
    """)
    nb.sottosezione("Un CSV salvato da Excel in italiano", intro="""
        `letture_pod_2025.csv` contiene i consumi mensili per fascia di sei POD, esportati da un Excel
        italiano. Questa cella dà errore apposta: leggiamo l'ultima riga del messaggio.
    """)
    nb.code('pd.read_csv("../Dati/letture_pod_2025.csv")', errore=True)
    nb.md("""
        `UnicodeDecodeError`: pandas legge il file come UTF-8 e trova un byte che non lo è (la `è` di
        "Caffè"). I file salvati da Excel su Windows usano spesso l'encoding `latin-1`. In più i CSV italiani
        separano le colonne con `;` e scrivono i decimali con la virgola: servono tre parametri.
    """)
    nb.code("""
        letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
        letture.head()
    """)
    nb.code("letture.dtypes")
    nb.md("""
        `kwh` è `float64`: senza `decimal=","` sarebbe rimasta testo, e una colonna di testo non si somma.
        `encoding="latin-1"` si aggiunge solo dopo aver visto l'errore: su un file UTF-8 con lettere
        accentate produrrebbe caratteri strani senza segnalarlo.
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("File Excel", intro="""
        I file Excel sono molto usati per i dati strutturati e possono contenere più fogli. Il carico
        elettrico della zona Nord pubblicato da Terna è in un file Excel.
    """)
    nb.code("""
        carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico.head()
    """)
    nb.sottosezione("Più fogli in un file", intro="""
        `pd.ExcelWriter` scrive più DataFrame nello stesso file, ognuno in un foglio. Con `read_excel()`
        scegliamo il foglio da leggere con `sheet_name`.
    """)
    nb.code("""
        # creare un file Excel con più fogli
        with pd.ExcelWriter("dati.xlsx") as writer:
            df1.to_excel(writer, sheet_name="Foglio1", index=False)
            df2.to_excel(writer, sheet_name="Foglio2", index=False)
        print("File 'dati.xlsx' creato.")
    """)
    nb.code("""
        # leggere un foglio specifico
        df_foglio1 = pd.read_excel("dati.xlsx", sheet_name="Foglio1", dtype=tipi_colonne)
        df_foglio1.dtypes
    """)
    nb.md("""
        Con `sheet_name=None` pandas legge tutti i fogli e restituisce un dizionario: la chiave è il nome del
        foglio, il valore il suo DataFrame. Poi li uniamo con `pd.concat()`.
    """)
    nb.code("""
        # leggere tutti i fogli dal file Excel
        fogli = pd.read_excel("dati.xlsx", sheet_name=None, dtype=tipi_colonne)
        fogli.keys()
    """)
    nb.code("""
        # concatenare i DataFrame
        df_excel_unito = pd.concat(fogli.values(), ignore_index=True)
        df_excel_unito
    """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Database SQL", intro="""
        Spesso i dati stanno in un database: tabelle interrogate con SQL. Python ci parla attraverso una
        connessione, e `pd.read_sql` restituisce il risultato di una query come DataFrame. Qui usiamo SQLite,
        un database contenuto in un singolo file, `utility.db`.
    """)
    nb.code("""
        import sqlite3

        con = sqlite3.connect("../Dati/utility.db")
        pd.read_sql("SELECT name FROM sqlite_master WHERE type = 'table'", con)
    """)
    nb.md("""
        `sqlite_master` è la tabella in cui SQLite tiene l'elenco del suo contenuto: le tabelle sono
        `clienti`, `pod` e `letture`. `SELECT * FROM letture` vuol dire: tutte le colonne e tutte le righe.
    """)
    nb.code("""
        letture_db = pd.read_sql("SELECT * FROM letture", con)
        letture_db.head()
    """)
    nb.md("""
        Con `WHERE` il filtro lo fa il database, e arrivano solo le righe che servono.
    """)
    nb.code('pd.read_sql("SELECT * FROM pod WHERE potenza_kw >= 30", con)')
    nb.md("Alla fine si chiude la connessione.")
    nb.code("con.close()")

    # ------------------------------------------------------------------ 7 (A)
    with nb.solo("avanzata"):
        nb.sezione("Lettura di dati da API", intro="""
            Le API (*Application Programming Interface*) permettono a programmi diversi di comunicare tra
            loro. Molti servizi web offrono API pubbliche per accedere ai loro dati: si invia una richiesta
            HTTP (per esempio una GET) a un indirizzo, l'endpoint, e si riceve una risposta, spesso in JSON.
        """)
        nb.sottosezione("JSON e requests", intro="""
            JSON (*JavaScript Object Notation*) è un formato di testo per lo scambio di dati, fatto di coppie
            chiave-valore simili ai dizionari Python.

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
            La libreria `requests` invia le richieste HTTP. I passi sono sempre gli stessi: definire
            l'endpoint e i parametri, inviare la richiesta, convertire il JSON ricevuto in un DataFrame.
        """)
        nb.md("""
            Usiamo gli open data di Regione Lombardia sulle stazioni meteo:

            - anagrafica dei sensori: `https://www.dati.lombardia.it/resource/nf78-nj6b.json`;
            - misure dei sensori: `https://www.dati.lombardia.it/resource/647i-nhxk.json`.
        """)
        nb.code("""
            import requests

            url = "https://www.dati.lombardia.it/resource/nf78-nj6b.json"
            response = requests.get(url, timeout=30)
            response
        """, rete=True)
        nb.md("""
            Ogni risposta ha un *codice di stato* che dice com'è andata la richiesta:

            - **200**: la richiesta è stata completata correttamente;
            - **404**: risorsa non trovata, l'URL potrebbe essere sbagliato;
            - **500**: errore del server.
        """)
        nb.code("""
            risposta_json = response.json()
            len(risposta_json)
        """, rete=True)
        nb.code("risposta_json[0]", rete=True)
        nb.sottosezione("Parametri di query", intro="""
            Spesso non vogliamo tutti i dati, ma solo una parte. I **parametri di query** si aggiungono alla
            fine dell'URL: iniziano dopo il simbolo `?`, sono coppie `chiave=valore` e si separano con `&`.
        """)
        nb.code("""
            # URL con i parametri di query per la provincia di Milano
            url = "https://www.dati.lombardia.it/resource/nf78-nj6b.json?provincia=MI&tipologia=Precipitazione"
            response = requests.get(url, timeout=30)
            dati = response.json()
            dati[:4]
        """, rete=True)
        nb.md("""
            Con `requests` i parametri si passano in un dizionario con l'argomento `params`: il codice è più
            leggibile e `requests` costruisce l'URL per noi.
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
            Recuperiamo le informazioni su tutti i sensori. I parametri speciali iniziano con `$`: `$limit`
            dice quante righe vogliamo (senza, il portale ne restituisce mille). `raise_for_status()` ferma la
            cella se il codice di stato è un errore.
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
            Se l'API non risponde, esegui la cella qui sotto: legge dati di esempio da un file di riserva.
        """)
        nb.code("""
            import json

            with open("../Dati/fallback/lombardia_sensori.json", encoding="utf-8") as f:
                sensori_df = pd.DataFrame(json.load(f))
            sensori_df.head()
        """)
        nb.md("Quali tipi di sensori ci sono, e in quali province?")
        nb.code('sensori_df["tipologia"].unique()')
        nb.code('sensori_df["provincia"].unique()')
        nb.md("Il filtro con due condizioni lo vediamo nel notebook sulle operazioni: qui basta leggerlo.")
        nb.md("""
            Teniamo i sensori di temperatura della provincia di Milano: tra parentesi quadre mettiamo le due
            condizioni, unite da `&`.
        """)
        nb.code("""
            sensori_milano = sensori_df[(sensori_df["tipologia"] == "Temperatura") & (sensori_df["provincia"] == "MI")]
            sensori_milano.head()
        """)
        nb.sottosezione("Le misure di un sensore", intro="""
            Con l'ID di un sensore recuperiamo le sue misure dall'altra risorsa. Scegliamo il sensore 2001, il
            termometro di Milano via Brera.
        """)
        nb.code('idsensore = "2001"')
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
            Se l'API non risponde, esegui la cella qui sotto: legge dati di esempio da un file di riserva.
        """)
        nb.code("""
            with open("../Dati/fallback/lombardia_misure_2001.json", encoding="utf-8") as f:
                misure_df = pd.DataFrame(json.load(f))
            misure_df
        """)
        nb.md("Le conversioni e il grafico qui sotto anticipano i notebook sulle date e su Plotly.")
        nb.md("""
            Il portale manda tutto come testo: convertiamo la data in datetime e il valore in numero, poi
            ordiniamo per data. Il valore `-9999` indica una misura mancante: togliamo quelle righe.
        """)
        nb.code("""
            misure_df["data"] = pd.to_datetime(misure_df["data"])
            misure_df["valore"] = pd.to_numeric(misure_df["valore"], errors="coerce")
            misure_df = misure_df.sort_values("data")
            misure_df = misure_df[misure_df["valore"] != -9999]
        """)
        nb.md("Visualizziamo l'andamento della temperatura nelle ultime 100 misure.")
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
        scenario="Delle letture dei POD ci servono solo tre colonne e il consumo complessivo.",
        richiesta="""
            1. Leggi `../Dati/letture_pod_2025.csv` nel DataFrame `letture_kwh`, tenendo solo le colonne
               `pod`, `fascia` e `kwh`.
            2. Metti in `totale_kwh` la somma della colonna `kwh`.

            *Output atteso:* 216 righe, 3 colonne, un totale di circa 134507.7 kWh.
        """,
        suggerimento="i parametri sono `sep`, `decimal`, `encoding` e `usecols`; la somma di una colonna è `.sum()`.",
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
        perche="Senza `decimal=\",\"` la colonna `kwh` resterebbe testo e la somma non darebbe un numero.",
    )
    nb.esercizio(
        titolo="Due fogli Excel in una tabella",
        scenario="Un negozio tiene le vendite di gennaio e di febbraio in due fogli dello stesso file Excel.",
        richiesta="""
            1. Scrivi `gennaio` e `febbraio` nel file `vendite.xlsx`, nei fogli `Gennaio` e `Febbraio`.
            2. Leggi tutti i fogli del file nel dizionario `fogli`.
            3. Concatenali nel DataFrame `vendite`, con un indice da 0 a 5.

            *Output atteso:* 6 righe con le colonne `prodotto` e `pezzi`.
        """,
        suggerimento="`pd.ExcelWriter`, poi `sheet_name=None` e `pd.concat(..., ignore_index=True)`.",
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
        scenario="Un POD è il codice che identifica un punto di prelievo. Dal database `utility.db` ci servono le letture di marzo di un solo POD.",
        richiesta="""
            1. Apri la connessione a `../Dati/utility.db`.
            2. Con una query, leggi dalla tabella `letture` solo le righe del POD `IT001E10000000` nel
               DataFrame `letture_pod`.
            3. Metti in `totale_marzo` la somma della colonna `kwh`, poi chiudi la connessione.

            *Output atteso:* 31 righe, una per giorno, e un totale di 7785.6 kWh.
        """,
        suggerimento="dentro la query il testo va tra apici singoli: `WHERE pod = '...'`.",
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
                Regione Lombardia pubblica i dati sulla certificazione energetica degli edifici. Questo
                esercizio richiede la rete: non c'è un file di riserva.
            """,
            richiesta="""
                1. Recupera i dati dall'endpoint `https://www.dati.lombardia.it/resource/rsg3-xhvk.json` nel
                   DataFrame `certificati`.
                2. Tieni solo gli edifici della provincia di Milano nel DataFrame `milano`.
                3. Calcola le emissioni medie di CO2 per ciascuna classe energetica in `co2_per_classe`.

                *Output atteso:* una Series con una riga per classe energetica (A4, A3, ..., G) e le emissioni
                medie di CO2.
            """,
            suggerimento="""
                guarda prima `certificati.columns` e i valori con `unique()`; i numeri arrivano come testo
                (`pd.to_numeric`); la media per gruppo si scrive `df.groupby("colonna")["altra"].mean()`.
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
                I nomi delle colonne e i valori della provincia vanno controllati con `certificati.columns` e
                `unique()`: se il portale li cambia, si adattano la maschera e il `groupby`.
            """,
            verifica="""
                assert 0 < len(milano) < len(certificati), "❌ milano deve avere solo le righe della provincia di Milano"
                assert len(co2_per_classe) > 1 and co2_per_classe.index.is_unique, "❌ co2_per_classe: una riga per classe energetica, con la media"
            """,
            rete=True,
            facoltativo=True,
        )
    return nb
