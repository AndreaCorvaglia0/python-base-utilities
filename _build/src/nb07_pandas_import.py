"""07 · pandas: DataFrame e import dei dati."""

from nbkit import Notebook

DATI_COMUNI = [
    "impianti_fv.csv",
    "letture_pod_2025.csv",
    "bolletta_esempio.xlsx",
    "load_total_north_hourly_2024.xlsx",
    "utility.db",
]


def costruisci() -> Notebook:
    nb = Notebook(
        num="07",
        file="07_Pandas_import_dati",
        titolo="pandas: DataFrame e import dei dati",
        blocco=2,
        giornata=1,
        intento="Fin qui i dati li abbiamo scritti a mano nelle celle. Da qui in avanti arrivano da fuori: file CSV, cartelle Excel, un database. pandas li porta tutti nella stessa forma, il DataFrame, e da lì si lavora sempre allo stesso modo.",
        obiettivi={
            "base": [
                "creare e ispezionare Series e DataFrame con `head`, `info`, `describe` e `dtypes`",
                "leggere e scrivere CSV ed Excel con i parametri giusti, anche quando il file arriva da un Excel italiano",
                "caricare una tabella da un database SQL con una query",
            ],
            "avanzata": [
                "creare e ispezionare Series e DataFrame; leggere e scrivere CSV, Excel e tabelle SQL con i parametri giusti",
                "chiamare un'API con requests e trasformare la risposta JSON in un DataFrame",
                "incapsulare la chiamata in una funzione da riusare",
            ],
        },
        tempo={"base": 80, "avanzata": 120},
        dati={
            "base": DATI_COMUNI,
            "avanzata": DATI_COMUNI + [
                "fallback/meteo_milano_previsione.json",
                "fallback/lombardia_sensori.json",
                "fallback/lombardia_misure_2001.json",
            ],
        },
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Series e DataFrame", intro="""
        Un DataFrame è una tabella: righe, colonne con un nome, un tipo per colonna. È il foglio Excel di
        pandas, e quasi tutto quello che faremo da qui alla fine del corso passa di lì. Lo costruiamo prima
        a mano, da un dizionario di liste, per capirne la forma; poi lo riempiremo da file.
    """)
    nb.code("""
        import pandas as pd

        consumi = pd.DataFrame({
            "pod": ["IT001E12345678", "IT001E23456789", "IT001E34567890",
                    "IT001E45678901", "IT001E56789012", "IT001E67890123"],
            "cliente": ["Caffè del Corso", "Lavanderia Più", "Società Agricola Verdi",
                        "Panificio Rè", "Officina Fumagalli", "Studio Colombo"],
            "kwh_marzo": [2724.7, 1130.2, 4210.5, 2362.0, 5880.3, 950.8],
        })
        consumi
    """)
    nb.md("""
        Ogni chiave del dizionario è diventata una colonna, ogni lista i suoi valori. La colonna di numeri
        a sinistra, senza nome, è l'**indice**: il numero di riga, da 0, come i numeri di riga di Excel.
        Non è un dato nostro, lo mette pandas.
    """)
    nb.md("""
        Una colonna sola si prende con le parentesi quadre e il nome, come il valore di un dizionario.
        Quello che torna è una **Series**: una colonna con il suo indice.
    """)
    nb.code('consumi["kwh_marzo"]')
    nb.md("""
        Con due parentesi quadre passiamo una lista di nomi, e torna un DataFrame, anche se la lista ha un
        nome solo. È la domanda che prima o poi fa qualcuno: perché le doppie quadre? Perché dentro c'è
        una lista.
    """)
    nb.code('consumi[["cliente", "kwh_marzo"]]')
    nb.code("""
        print(type(consumi["kwh_marzo"]))
        print(type(consumi[["kwh_marzo"]]))
    """)
    nb.md("""
        Prima di fare qualsiasi cosa con una tabella, la guardiamo. `shape` dice quante righe e quante
        colonne (è una tupla), `columns` i nomi, `dtypes` il tipo di ogni colonna.
    """)
    nb.code("consumi.shape")
    nb.code("consumi.columns")
    nb.code("consumi.dtypes")
    nb.md("""
        `str` per il testo, `float64` per i numeri con la virgola, `int64` per gli interi. Il tipo decide
        cosa si può fare: una colonna `str` piena di numeri scritti male non si somma, e lo scopriremo tra
        poco su un file vero.
    """)
    nb.md("""
        `head()` mostra le prime righe, `tail()` le ultime. Con tabelle da migliaia di righe sono l'unico
        modo sensato di dare un'occhiata.
    """)
    nb.code("consumi.head(3)")
    nb.md("""
        Una cella mostra da sola solo il valore dell'ultima espressione. Per vedere due tabelle nella stessa
        cella si usa `display(tabella)`: è come `print`, ma la tabella resta formattata.
    """)
    nb.code("""
        display(consumi.head(2))
        consumi.tail(2)
    """)
    nb.md("""
        `info()` mette insieme tutto: righe, colonne, tipi e quanti valori non mancano. `describe()` fa le
        statistiche di base delle colonne numeriche. Sono le prime due cose da chiamare su un file appena
        aperto.
    """)
    nb.code("consumi.info()")
    nb.code("consumi.describe()")
    nb.md("""
        Le righe da guardare sono `count` (quanti valori), `mean` (la media), `50%` (la mediana: metà dei
        valori sta sotto, metà sopra), `min` e `max`. Se la media e la mediana sono molto lontane, di
        solito c'è qualche valore anomalo.
    """)
    nb.md("""
        Su una Series si calcolano direttamente somma, media, massimo: tutta la colonna in un colpo,
        senza ciclo.
    """)
    nb.code("""
        print(consumi["kwh_marzo"].sum())
        print(consumi["kwh_marzo"].mean())
        print(consumi["kwh_marzo"].max())
    """)
    nb.md("""
        Una colonna nuova si crea assegnando, come una chiave nuova in un dizionario. Il conto a destra
        vale per tutte le righe insieme.
    """)
    nb.code("""
        consumi["mwh_marzo"] = consumi["kwh_marzo"] / 1000
        consumi
    """)
    nb.md("""
        Per tenere solo alcune righe serve una condizione scritta sulla colonna intera: è la condizione
        dell'`if`, su tutta la colonna. Il risultato è una Series di `True` e `False`, uno per riga.
    """)
    nb.code("""
        mask = consumi["kwh_marzo"] > 2000
        mask
    """)
    nb.md("""
        Passata al DataFrame tra parentesi quadre, la maschera tiene le righe con `True`. L'indice resta
        quello di partenza: le righe scartate si portano via i loro numeri.
    """)
    nb.code("consumi[mask]")
    nb.box("nota", """
        Il risultato non si salva da solo: `consumi[mask]` mostra le righe filtrate, ma `consumi` è ancora
        intero. Per tenerle si assegna a un nome, `grandi = consumi[mask]`.
    """)
    nb.prova_tu(
        richiesta="""
            Crea il DataFrame `prezzi` da un dizionario con due colonne: `zona` con le sei zone di mercato
            (NORD, CNOR, CSUD, SUD, SICI, SARD) e `eur_mwh` con i prezzi 98.5, 101.2, 103.7, 95.0, 118.4,
            104.9. Poi metti in `prezzo_medio` la media dei prezzi arrotondata a un decimale.
        """,
        starter="""
            prezzi = pd.DataFrame({
                "zona": [...],
                "eur_mwh": [...],
            })

            prezzo_medio = ...
            prezzo_medio
        """,
        soluzione="""
            prezzi = pd.DataFrame({
                "zona": ["NORD", "CNOR", "CSUD", "SUD", "SICI", "SARD"],
                "eur_mwh": [98.5, 101.2, 103.7, 95.0, 118.4, 104.9],
            })

            prezzo_medio = round(prezzi["eur_mwh"].mean(), 1)
            prezzo_medio
        """,
        verifica="""
            assert prezzi.shape == (6, 2), "❌ prezzi deve avere 6 righe e 2 colonne"
            assert prezzo_medio == 103.6, "❌ prezzo_medio: media della colonna eur_mwh, arrotondata a un decimale"
        """,
    )
    nb.box("ricorda", """
        - `df["col"]` è una Series, `df[["col"]]` è un DataFrame.
        - Su una tabella appena aperta: `head()`, `info()`, `describe()`.
        - Una condizione sulla colonna dà una maschera; `df[mask]` tiene le righe vere.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Dove sono i file", intro="""
        Prima di leggere un file bisogna sapere dove siamo. Quando VS Code esegue un notebook, la cartella
        di lavoro è quella del notebook, e i percorsi relativi partono da lì. La libreria `pathlib` ci fa
        fare domande al disco invece di tirare a indovinare.
    """)
    nb.code("""
        from pathlib import Path

        Path.cwd()
    """)
    nb.md("""
        Siamo nella cartella del notebook. I dati stanno in `Dati`, una cartella sorella: `..` sale di un
        livello, poi si scende. `Path(...)` costruisce il percorso, `.exists()` dice se c'è davvero.
    """)
    nb.code("""
        cartella_dati = Path("../Dati")
        cartella_dati.exists()
    """)
    nb.md("""
        `glob` elenca i file che corrispondono a un modello: `*.csv` sono tutti i CSV. Li restituisce uno
        alla volta, quindi li raccogliamo con `sorted`, che li mette anche in ordine.
    """)
    nb.code('sorted(cartella_dati.glob("*.csv"))')
    nb.md("""
        Il percorso di un singolo file si compone con `/`, su Windows come su Mac. Controllare che esista,
        prima di leggerlo, risparmia un errore.
    """)
    nb.code("""
        file_impianti = cartella_dati / "impianti_fv.csv"
        file_impianti.exists()
    """)
    nb.md("""
        Questa cella dà errore apposta: il nome del file è sbagliato. Leggiamo l'ultima riga del traceback.
    """)
    nb.code('pd.read_csv("../Dati/impianti.csv")', errore=True)
    nb.md("""
        `FileNotFoundError`, già incontrato nel notebook sugli errori: il percorso non porta a nessun
        file. Prima di cercare altrove facciamo due controlli: `Path.cwd()` dice da quale cartella stiamo
        lavorando, `.exists()` dice se il file c'è.
    """)
    nb.box("nota", """
        Nel resto del corso i percorsi sono stringhe come `"../Dati/impianti_fv.csv"`. `pathlib` serve
        quando un percorso va costruito o controllato; per leggere un file che sappiamo dov'è, la stringa
        basta.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("CSV", intro="""
        Il CSV è il formato di scambio più comune: testo, una riga per record, un separatore tra i campi.
        `pd.read_csv` lo legge in un DataFrame. Quando il file è pulito basta il nome; quando viene da un
        gestionale italiano, no.
    """)
    nb.code("""
        with open("../Dati/impianti_fv.csv", encoding="utf-8") as f:
            print(f.readline().strip())
            print(f.readline().strip())
    """)
    nb.md("""
        Ecco il CSV com'è davvero: righe di testo. La prima contiene i nomi delle colonne, le altre i
        valori, separati dalla virgola. `open` apre il file e `with ... as f` lo richiude da solo alla fine
        del blocco: è una forma che troviamo spesso nel codice scritto da un agente. `pd.read_csv` fa
        questo per tutte le righe e ne fa una tabella.
    """)
    nb.code("""
        impianti = pd.read_csv("../Dati/impianti_fv.csv")
        impianti.head()
    """)
    nb.md("""
        Quaranta impianti fotovoltaici con comune, provincia, potenza in kWp e anno di allaccio. Prima di
        tutto `info()`: righe, colonne, tipi, e nessun valore mancante.
    """)
    nb.code("impianti.info()")
    nb.code("impianti.describe()")
    nb.md("""
        Potenze da 3 a 200 kWp, anni dal 2011 al 2025. Le colonne di testo non compaiono: `describe()`
        fa statistiche sui numeri.
    """)
    nb.md("""
        Capita spesso: chiediamo all'agente una tabella da incollare in chat, e lui scrive
        `.to_markdown()`. Questa cella dà errore apposta: leggiamo l'ultima riga.
    """)
    nb.code("impianti.head().to_markdown()", errore=True)
    nb.md("""
        L'errore dice il nome della libreria che manca: `tabulate`. Il consiglio su pip non vale per noi:
        le librerie le gestisce uv. Nel terminale, nella cartella del corso, scriviamo `uv add tabulate`,
        poi Restart kernel e infine la cella qui sotto. Il Restart svuota la memoria: per questo la cella
        reimporta pandas e `Path` e rilegge il file.
    """)
    nb.code("""
        import pandas as pd
        from pathlib import Path

        impianti = pd.read_csv("../Dati/impianti_fv.csv")
        print(impianti.head().to_markdown())
    """, rete=True)
    nb.md("""
        Apri `pyproject.toml`: tra le `dependencies` adesso c'è anche `tabulate`.
    """)

    nb.sottosezione("Il CSV del fornitore", intro="""
        Il fornitore ci manda i consumi mensili per fascia (F1, F2, F3) di sei POD. Il file è un'esportazione
        da Excel italiano, e si vede subito. Questa cella dà errore apposta: leggiamo l'ultima riga.
    """)
    nb.code('pd.read_csv("../Dati/letture_pod_2025.csv")', errore=True)
    nb.md("""
        `UnicodeDecodeError`: pandas prova a leggere il file come UTF-8 e inciampa su un byte che non lo è
        (la `è` di "Caffè"). I file salvati da Excel su Windows usano un altro encoding, `latin-1`:
        glielo diciamo con `encoding`.
    """)
    nb.code("""
        letture = pd.read_csv("../Dati/letture_pod_2025.csv", encoding="latin-1")
        letture.head()
    """)
    nb.md("""
        Si legge, ma è una colonna sola con un nome lunghissimo: il separatore non è la virgola ma il
        punto e virgola. È lo standard dei CSV italiani, perché la virgola la usiamo per i decimali.
        Quindi `sep=";"`.
    """)
    nb.code("""
        letture = pd.read_csv("../Dati/letture_pod_2025.csv", encoding="latin-1", sep=";")
        letture.head()
    """)
    nb.md("""
        Adesso le colonne ci sono. Ma `kwh` è scritto `1260,6`: controlliamo i tipi.
    """)
    nb.code("letture.dtypes")
    nb.md("""
        `kwh` è `str`: con la virgola pandas non riconosce il numero, e una colonna di testo non si somma.
        `decimal=","` chiude il cerchio. Questi tre parametri insieme sono la ricetta per quasi ogni CSV
        italiano.
    """)
    nb.code("""
        letture = pd.read_csv("../Dati/letture_pod_2025.csv", encoding="latin-1", sep=";", decimal=",")
        letture.dtypes
    """)
    nb.code("letture.describe()")
    nb.md("""
        216 righe: 6 POD per 12 mesi per 3 fasce. Il massimo è 5785 kWh contro una mediana di 571:
        qualcuno ha battuto uno zero di troppo. Lo troveremo nel prossimo notebook. Qui intanto isoliamo
        un POD con una maschera, come prima: `mask.sum()` conta le righe vere.
    """)
    nb.code("""
        mask = letture["pod"] == "IT001E12345678"
        mask.sum()
    """)
    nb.code("""
        caffe = letture[mask]
        caffe.head()
    """)
    nb.box("attenzione", """
        `encoding="latin-1"` non si mette "per sicurezza" su ogni file: su un UTF-8 con lettere accentate
        produce caratteri strani senza dare nessun errore. Si aggiunge solo dopo aver visto
        l'`UnicodeDecodeError`.
    """)
    nb.md("""
        Spesso non servono tutte le colonne: `usecols` prende solo quelle che ci interessano, e il file si
        legge più in fretta.
    """)
    nb.code("""
        letture_kwh = pd.read_csv("../Dati/letture_pod_2025.csv", encoding="latin-1", sep=";", decimal=",",
                                  usecols=["pod", "fascia", "kwh"])
        letture_kwh.head()
    """)
    nb.box("nota", """
        Se un codice è fatto solo di cifre (un CAP come `00100`, un codice cliente `000123`) pandas lo
        legge come numero e perde gli zeri iniziali. `dtype={"cap": str}` lo tiene testo fin dalla lettura.
    """)
    nb.prova_tu(
        richiesta="""
            Leggi `letture_pod_2025.csv` tenendo solo le colonne `pod`, `data` e `kwh` nel DataFrame
            `letture_ridotte`, e metti in `totale_kwh` la somma di tutti i consumi, arrotondata a un
            decimale.
        """,
        starter="""
            letture_ridotte = pd.read_csv("../Dati/letture_pod_2025.csv", ...)

            totale_kwh = ...
            totale_kwh
        """,
        soluzione="""
            letture_ridotte = pd.read_csv("../Dati/letture_pod_2025.csv", encoding="latin-1", sep=";",
                                          decimal=",", usecols=["pod", "data", "kwh"])

            totale_kwh = round(letture_ridotte["kwh"].sum(), 1)
            totale_kwh
        """,
        verifica="""
            assert letture_ridotte.shape == (216, 3), "❌ letture_ridotte: 216 righe e solo le tre colonne pod, data, kwh"
            assert totale_kwh == 134507.7, "❌ totale_kwh: somma della colonna kwh (serve decimal=',' perché sia un numero)"
        """,
    )

    nb.sottosezione("Scrivere un CSV, e leggerne tanti", intro="""
        Il percorso inverso è `to_csv`. Lo proviamo in una situazione da ufficio: il fornitore manda un file
        al mese, e noi dobbiamo rimetterli insieme. Prima costruiamo i due file di gennaio e febbraio a
        partire da `letture`, con una maschera sulla data.
    """)
    nb.code("""
        mask_gennaio = letture["data"] == "01/01/2025"
        mask_febbraio = letture["data"] == "01/02/2025"

        gennaio = letture[mask_gennaio]
        febbraio = letture[mask_febbraio]
        print(len(gennaio), len(febbraio))
    """)
    nb.code("""
        gennaio.to_csv("letture_2025_01.csv", index=False)
        febbraio.to_csv("letture_2025_02.csv", index=False)

        sorted(Path(".").glob("letture_2025_*.csv"))
    """)
    nb.md("""
        I due file sono nella cartella del notebook. `index=False` evita di salvare la colonna
        dell'indice, che rileggendo diventerebbe una colonna in più senza nome. In uscita il formato è
        quello standard, virgola e punto: per un collega con Excel italiano si aggiungono `sep=";"` e
        `decimal=","` anche qui.
    """)
    nb.md("""
        Per rimetterli insieme: un ciclo legge ogni file e lo aggiunge a una lista di DataFrame,
        `pd.concat` li impila. `ignore_index=True` rinumera le righe da 0, altrimenti avremmo due volte
        le righe da 0 a 17.
    """)
    nb.code("""
        tabelle = []
        for file in sorted(Path(".").glob("letture_2025_*.csv")):
            tabelle.append(pd.read_csv(file))

        due_mesi = pd.concat(tabelle, ignore_index=True)
        due_mesi.shape
    """)
    nb.md("""
        36 righe, 18 per file. Con dodici file al posto di due il codice è identico: è il motivo per cui
        si scrive il ciclo invece di dodici `read_csv`.
    """)
    nb.box("ricorda", """
        - CSV italiano: `sep=";"`, `decimal=","`, e `encoding="latin-1"` solo dopo l'errore.
        - Appena letto: `dtypes`. Un numero letto come `str` non si somma.
        - Un file si guarda come testo con `with open(p, encoding="utf-8") as f:` e `f.readline()`; si
          salva con `to_csv("nome.csv", index=False)`.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Excel", intro="""
        Mezza azienda vive dentro Excel, e i file che riceviamo sono spesso cartelle con più fogli.
        `pd.read_excel` legge un foglio in un DataFrame: senza altri parametri, il primo.
    """)
    nb.code("""
        consumi_mensili = pd.read_excel("../Dati/bolletta_esempio.xlsx")
        consumi_mensili.head()
    """)
    nb.md("""
        È il foglio `Consumi`: un POD e un mese per riga, i kWh per fascia nelle colonne. Per un altro
        foglio si passa `sheet_name` con il nome (o la posizione, da 0).
    """)
    nb.code("""
        listino = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Listino")
        listino
    """)
    nb.md("""
        Con `sheet_name=None` arrivano tutti i fogli in un dizionario: le chiavi sono i nomi dei fogli, i
        valori i DataFrame. Comodo quando non sappiamo cosa c'è dentro.
    """)
    nb.code("""
        fogli = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name=None)
        fogli.keys()
    """)
    nb.code('fogli["Anagrafica"]')
    nb.prova_tu(
        richiesta="""
            Dal dizionario `fogli` prendi il foglio `Consumi` nel DataFrame `consumi_mensili`, poi metti in
            `n_righe` il suo numero di righe e in `totale_f1` la somma della colonna `F1`, arrotondata a
            un decimale.
        """,
        starter="""
            consumi_mensili = fogli[...]

            n_righe = ...
            totale_f1 = ...
            print(n_righe, totale_f1)
        """,
        soluzione="""
            consumi_mensili = fogli["Consumi"]

            n_righe = len(consumi_mensili)
            totale_f1 = round(consumi_mensili["F1"].sum(), 1)
            print(n_righe, totale_f1)
        """,
        verifica="""
            assert n_righe == 72, "❌ n_righe: il foglio Consumi ha 6 POD per 12 mesi"
            assert totale_f1 == 41383.1, "❌ totale_f1: somma della colonna F1 del foglio Consumi, a un decimale"
        """,
    )

    nb.sottosezione("Scrivere un Excel", intro="""
        `to_excel` scrive un DataFrame in un foglio. Per più fogli nello stesso file si apre un
        `ExcelWriter` con `with` e si scrive un foglio alla volta: alla fine del blocco il file si chiude
        da solo. Prepariamo per il commerciale l'anagrafica degli impianti con, a parte, quelli da 50 kWp
        in su.
    """)
    nb.code("""
        mask = impianti["kwp"] >= 50
        grandi = impianti[mask]
        len(grandi)
    """)
    nb.code("""
        with pd.ExcelWriter("impianti_fv_report.xlsx") as writer:
            impianti.to_excel(writer, sheet_name="Tutti", index=False)
            grandi.to_excel(writer, sheet_name="Sopra_50_kWp", index=False)
    """)
    nb.md("""
        Nessun output: il file è stato scritto. Controlliamo rileggendolo: due fogli, con i nomi che
        abbiamo dato.
    """)
    nb.code('pd.read_excel("impianti_fv_report.xlsx", sheet_name=None).keys()')

    nb.sottosezione("Un Excel vero: il carico di Terna", intro="""
        Il file di Terna con il carico della zona Nord nel 2024 è un Excel da 35 mila righe: un valore
        ogni quarto d'ora. Si legge come gli altri, e ci mette un paio di secondi.
    """)
    nb.code("""
        carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico.head()
    """)
    nb.code("carico.dtypes")
    nb.md("""
        La colonna `Date` ha un tipo nuovo, `datetime64`: una data vera, non un testo. Excel salva le
        date come numeri con un formato, e pandas le riconosce da solo. Da un CSV sarebbero arrivate come
        stringhe, e la conversione sarebbe toccata a noi: la facciamo nel notebook sulle date.
    """)
    nb.code("carico.tail(3)")
    nb.md("""
        Tre cose che ci serviranno più avanti: il passo è di un quarto d'ora anche se il nome del file dice
        `hourly` (vale quello che vediamo nei dati, non il nome); il file è in ordine inverso (parte dal 31
        dicembre e finisce il 1° gennaio); i valori sono in MW, cioè la potenza media del quarto d'ora. Per
        l'energia in MWh si divide per 4: un quarto d'ora a 100 MW sono 25 MWh.
    """)
    nb.box("nota", """
        Per leggere e scrivere `.xlsx` pandas si appoggia alla libreria `openpyxl`, già nel progetto. Se in
        un altro progetto manca, nel terminale `uv add openpyxl`, poi Restart kernel.
    """)
    nb.box("ricorda", """
        - `pd.read_excel(file)` legge il primo foglio; `sheet_name="Nome"` uno preciso; `sheet_name=None`
          tutti, in un dizionario.
        - Più fogli in uscita: `with pd.ExcelWriter("file.xlsx") as writer:` e un `to_excel` per foglio.
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("SQL", intro="""
        I dati che contano stanno in un database: tabelle collegate tra loro, interrogate con SQL. Python
        ci parla attraverso una connessione, e pandas riceve il risultato di una query come DataFrame.
        Qui usiamo SQLite, un database che vive in un singolo file, `utility.db`.
    """)
    nb.code("""
        import sqlite3

        con = sqlite3.connect("../Dati/utility.db")
        pd.read_sql("SELECT name FROM sqlite_master WHERE type = 'table'", con)
    """)
    nb.md("""
        `sqlite_master` è la tabella in cui SQLite tiene l'elenco di quello che contiene: con questa query
        scopriamo le tabelle di un database che non conosciamo. Sono tre: `clienti`, `pod` e `letture`.
        `pd.read_sql` prende una query e la connessione, e restituisce un DataFrame. `SELECT * FROM
        letture` vuol dire: tutte le colonne, tutte le righe della tabella.
    """)
    nb.code("""
        letture_db = pd.read_sql("SELECT * FROM letture", con)
        letture_db.head()
    """)
    nb.code("letture_db.shape")
    nb.md("""
        930 righe: 30 POD per i 31 giorni di marzo. Con `WHERE` il filtro lo fa il database, e a noi
        arrivano solo le righe che servono: su tabelle da milioni di righe è la differenza tra un secondo
        e una pausa caffè. Il testo tra apici singoli dentro la query è SQL, non Python.
    """)
    nb.code('pd.read_sql("SELECT * FROM pod WHERE potenza_kw >= 30", con)')
    nb.md("""
        Il database sa anche unire le tabelle: `JOIN` affianca a ogni POD il suo cliente, usando la
        colonna che hanno in comune, `id_cliente`. Gli alias `p` e `c` servono solo a scrivere meno. La
        query è una stringa normale tra tre virgolette, come la docstring: così può andare su più righe e
        si legge meglio.
    """)
    nb.code('''
        query = """
        SELECT p.pod, p.potenza_kw, c.ragione_sociale, c.comune
        FROM pod AS p
        JOIN clienti AS c ON p.id_cliente = c.id_cliente
        """
        pod_clienti = pd.read_sql(query, con)
        pod_clienti.head()
    ''')
    nb.md("""
        Finito, si chiude la connessione: il file resta libero per chi viene dopo.
    """)
    nb.code("con.close()")
    nb.md("""
        Con un database aziendale cambia solo la connessione: al posto di `sqlite3.connect` c'è la stringa
        di connessione a SQL Server, Postgres o Oracle. La riga con `pd.read_sql` resta identica, e con
        lei tutto quello che viene dopo.
    """)
    nb.box("approfondimento", """
        Per i database di rete si usa la libreria `sqlalchemy` (`uv add sqlalchemy`, più il driver del
        database, poi Restart kernel). La connessione diventa un `engine`, il resto non cambia:

        ```python
        from sqlalchemy import create_engine

        engine = create_engine("postgresql://utente:password@server:5432/utility")
        pod = pd.read_sql("SELECT * FROM pod", engine)
        ```

        Utente e password non si scrivono nel notebook: si leggono da una variabile d'ambiente con
        `os.environ["DB_PASSWORD"]`, così il file si può condividere.
    """, titolo="La connessione a un database aziendale")
    nb.box("ricorda", """
        - `con = sqlite3.connect(...)`, poi `pd.read_sql(query, con)`, poi `con.close()`.
        - Se la tabella è grande, il filtro va nella query con `WHERE`, non dopo in pandas.
    """)

    # ------------------------------------------------------------------ 6-7 (A)
    with nb.solo("avanzata"):
        nb.sezione("API", intro="""
            Un'API web è un sito fatto per i programmi: si chiede un indirizzo e, invece di una pagina,
            torna un dato, quasi sempre in formato JSON. La richiesta più comune è una **GET**: un URL più
            dei parametri, come quando una ricerca finisce nell'indirizzo dopo il `?`. La libreria
            `requests` fa la chiamata; pandas trasforma la risposta in tabella.
        """)
        nb.md("""
            Partiamo da Open-Meteo, un servizio meteo gratuito e senza registrazione. I parametri vanno
            in un dizionario: coordinate, variabili orarie, fuso orario, quanti giorni.
        """)
        nb.code("""
            import requests

            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": 45.4642,
                "longitude": 9.19,
                "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                "timezone": "Europe/Rome",
                "forecast_days": 7,
            }
            response = requests.get(url, params=params, timeout=30)
            response.status_code
        """, rete=True)
        nb.md("""
            200 vuol dire che è andata. I codici che iniziano per 4 sono errori nostri (parametro
            sbagliato, 404 indirizzo inesistente), quelli per 5 sono problemi del server. `timeout=30`
            evita che la cella resti appesa per sempre se il server non risponde. L'URL completo, con i
            parametri messi dopo il `?`, è in `response.url`.
        """)
        nb.code("response.url", rete=True)
        nb.md("""
            Questa cella dà errore apposta: chiediamo una previsione senza longitudine. Il server risponde
            400 e spiega perché; `raise_for_status()` trasforma il codice di errore in un'eccezione, così il
            notebook si ferma lì invece di proseguire con dati vuoti.
        """)
        nb.code("""
            sbagliata = requests.get(url, params={"latitude": 45.4642}, timeout=30)
            print(sbagliata.status_code, sbagliata.json()["reason"])
            sbagliata.raise_for_status()
        """, rete=True, errore=True)
        nb.md("""
            Torniamo alla risposta buona. `.json()` la trasforma da testo nelle strutture che conosciamo,
            dizionari e liste. Guardiamo le chiavi.
        """)
        nb.code("""
            response.raise_for_status()
            dati = response.json()
            dati.keys()
        """, rete=True)
        nb.md("""
            Se l'API non risponde, esegui la cella qui sotto al posto di quella sopra: legge una risposta
            di esempio, salvata in un file di riserva. `with open(...) as f` apre il file e lo chiude alla
            fine del blocco; `json.load` lo trasforma come farebbe `.json()`.
        """)
        nb.code("""
            import json

            file_previsione = Path("../Dati/fallback/meteo_milano_previsione.json")
            if file_previsione.exists():
                with open(file_previsione, encoding="utf-8") as f:
                    dati = json.load(f)
                print(dati.keys())
            else:
                print(f"File di riserva non trovato: {file_previsione}")
        """)
        nb.md("""
            `hourly_units` dice le unità di misura. `hourly` è un dizionario di liste, una per variabile,
            tutte lunghe uguale: 7 giorni per 24 ore. È esattamente la forma da cui abbiamo costruito il
            primo DataFrame.
        """)
        nb.code('dati["hourly_units"]', rete=True)
        nb.code("""
            previsione = pd.DataFrame(dati["hourly"])
            previsione.head()
        """, rete=True)
        nb.code("previsione.dtypes", rete=True)
        nb.md("""
            `time` è `str`: una stringa che sembra una data è ancora una stringa. `pd.to_datetime` la
            trasforma in una data vera, e `.dt.date` ne ricava il giorno. Nel notebook sulle date ci
            torniamo con calma; qui ci basta sapere di che giorno è ogni ora.
        """)
        nb.code("""
            previsione["time"] = pd.to_datetime(previsione["time"])
            previsione["giorno"] = previsione["time"].dt.date
            previsione.head(3)
        """, rete=True)
        nb.prova_tu(
            richiesta="""
                Chiedi a Open-Meteo la previsione per Bergamo (latitudine 45.6983, longitudine 9.6773), solo
                `temperature_2m`, per 3 giorni. Metti la risposta convertita in `dati_bergamo` e il
                DataFrame orario in `bergamo`.
            """,
            starter="""
                params_bergamo = {
                    "latitude": ...,
                    "longitude": ...,
                    "hourly": "temperature_2m",
                    "timezone": "Europe/Rome",
                    "forecast_days": ...,
                }
                response_bergamo = requests.get(url, params=params_bergamo, timeout=30)
                response_bergamo.raise_for_status()

                dati_bergamo = ...
                bergamo = ...
                bergamo.shape
            """,
            soluzione="""
                params_bergamo = {
                    "latitude": 45.6983,
                    "longitude": 9.6773,
                    "hourly": "temperature_2m",
                    "timezone": "Europe/Rome",
                    "forecast_days": 3,
                }
                response_bergamo = requests.get(url, params=params_bergamo, timeout=30)
                response_bergamo.raise_for_status()

                dati_bergamo = response_bergamo.json()
                bergamo = pd.DataFrame(dati_bergamo["hourly"])
                bergamo.shape
            """,
            verifica="""
                assert len(bergamo) == 72, "❌ bergamo: 3 giorni per 24 ore fanno 72 righe (controlla forecast_days)"
                assert "temperature_2m" in bergamo.columns, "❌ bergamo: deve avere la colonna temperature_2m"
            """,
            rete=True,
        )

        nb.sottosezione("Open data: i sensori di Regione Lombardia", intro="""
            I portali open data funzionano allo stesso modo. Regione Lombardia pubblica l'anagrafica dei
            sensori meteo di ARPA e le loro misure: la rete che si guarda per sapere che tempo fa vicino a
            un impianto. Qui i parametri speciali iniziano con `$`: `$limit` dice quante righe vogliamo
            (senza, mille).
        """)
        nb.code("""
            url_sensori = "https://www.dati.lombardia.it/resource/nf78-nj6b.json"
            response = requests.get(url_sensori, params={"$limit": 5000}, timeout=30)
            response.raise_for_status()

            sensori = pd.DataFrame(response.json())
            sensori.head()
        """, rete=True)
        nb.md("""
            Se l'API non risponde, esegui la cella qui sotto al posto di quella sopra: il file di riserva
            contiene dati di esempio.
        """)
        nb.code("""
            file_sensori = Path("../Dati/fallback/lombardia_sensori.json")
            if file_sensori.exists():
                with open(file_sensori, encoding="utf-8") as f:
                    sensori = pd.DataFrame(json.load(f))
                print(sensori.shape)
            else:
                print(f"File di riserva non trovato: {file_sensori}")
        """)
        nb.md("""
            La risposta è una lista di dizionari, uno per sensore, e `pd.DataFrame` la trasforma così
            com'è. Per vedere cosa misurano, `value_counts()` conta quante righe ci sono per ogni valore di
            una colonna.
        """)
        nb.code('sensori["tipologia"].value_counts()', rete=True)
        nb.md("""
            Con una maschera teniamo i soli termometri. Lo stesso filtro si può chiedere al server,
            `params={"tipologia": "Temperatura"}`: stesso risultato, meno dati in viaggio.
        """)
        nb.code("""
            mask = sensori["tipologia"] == "Temperatura"
            termometri = sensori[mask]
            termometri[["idsensore", "nomestazione", "provincia", "quota"]].head()
        """, rete=True)
        nb.md("""
            Le misure stanno in un'altra risorsa. `$where` filtra sul server (le date in formato ISO),
            `$order` ordina. Chiediamo il sensore 2001, un termometro, per la prima settimana di giugno
            2025.
        """)
        nb.code("""
            url_misure = "https://www.dati.lombardia.it/resource/647i-nhxk.json"
            params = {
                "idsensore": "2001",
                "$where": "data between '2025-06-01T00:00:00' and '2025-06-07T23:59:59'",
                "$order": "data",
                "$limit": 5000,
            }
            response = requests.get(url_misure, params=params, timeout=30)
            response.raise_for_status()

            misure = pd.DataFrame(response.json())
            misure.head()
        """, rete=True)
        nb.md("""
            Se l'API non risponde, esegui la cella qui sotto al posto di quella sopra: il file di riserva
            contiene dati di esempio, con tutto lo storico del sensore, settimana compresa.
        """)
        nb.code("""
            file_misure = Path("../Dati/fallback/lombardia_misure_2001.json")
            if file_misure.exists():
                with open(file_misure, encoding="utf-8") as f:
                    misure = pd.DataFrame(json.load(f))
                print(misure.shape)
            else:
                print(f"File di riserva non trovato: {file_misure}")
        """)
        nb.code("misure.dtypes", rete=True)
        nb.md("""
            Tutto `str`, anche `valore`: il portale manda testo. `pd.to_numeric` converte la colonna in
            numeri. E `-9999` non è una temperatura: è il modo del portale di dire "misura mancante".
            Contiamo quante sono.
        """)
        nb.code("""
            misure["valore"] = pd.to_numeric(misure["valore"])
            mask = misure["valore"] == -9999
            mask.sum()
        """, rete=True)
        nb.code("""
            mask = misure["valore"] != -9999
            misure = misure[mask]
            misure["valore"].describe()
        """, rete=True)
        nb.box("attenzione", """
            Un valore sentinella come `-9999` passa inosservato in una media e la distrugge: una settimana
            a 20 gradi con tre `-9999` dentro fa una media sotto zero. Prima di qualunque statistica, via
            i mancanti.
        """)

        nb.sezione("Il wrapper", intro="""
            Abbiamo scritto quattro volte le stesse tre righe: `requests.get`, `raise_for_status()`, `.json()`.
            Quando un pezzo di codice si ripete uguale lo chiudiamo in una funzione, un **wrapper**: si riusa
            con una riga e, se c'è da correggere qualcosa (il timeout, una chiave di accesso), si corregge in
            un posto solo.
        """)
        nb.code('''
            def get_json(url: str, params: dict) -> dict | list:
                """Fa una GET con i parametri dati e restituisce la risposta JSON già convertita."""
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response.json()
        ''')
        nb.md("""
            La usiamo subito per l'anagrafica: una riga al posto di tre, e il resto non cambia.
        """)
        nb.code("""
            sensori = pd.DataFrame(get_json(url_sensori, {"$limit": 5000}))
            sensori.shape
        """, rete=True)
        nb.md("""
            Il secondo passo è una funzione di dominio: dato un sensore e due date, restituisce le misure
            pulite, numeriche e senza `-9999`. Dentro c'è tutto il lavoro della sezione precedente; fuori
            resta una chiamata che si legge come una frase.
        """)
        nb.code('''
            def misure_sensore(idsensore: str, inizio: str, fine: str) -> pd.DataFrame:
                """Misure ARPA di un sensore tra due date (aaaa-mm-gg), numeriche e senza i -9999."""
                url = "https://www.dati.lombardia.it/resource/647i-nhxk.json"
                periodo = f"data between '{inizio}T00:00:00' and '{fine}T23:59:59'"
                params = {"idsensore": idsensore, "$where": periodo, "$order": "data", "$limit": 50000}
                misure = pd.DataFrame(get_json(url, params))
                misure["valore"] = pd.to_numeric(misure["valore"])
                mask = misure["valore"] != -9999
                return misure[mask]
        ''')
        nb.code("""
            giugno = misure_sensore("2001", "2025-06-01", "2025-06-30")
            giugno["valore"].describe()
        """, rete=True)
        nb.md("""
            Se l'API non risponde, esegui la cella qui sotto al posto di quella sopra: fa gli stessi passi
            della funzione sui dati di esempio del file di riserva.
        """)
        nb.code("""
            if file_misure.exists():
                with open(file_misure, encoding="utf-8") as f:
                    giugno = pd.DataFrame(json.load(f))
                giugno["valore"] = pd.to_numeric(giugno["valore"])
                mask = giugno["valore"] != -9999
                giugno = giugno[mask]
                display(giugno["valore"].describe())
            else:
                print(f"File di riserva non trovato: {file_misure}")
        """)
        nb.md("""
            Il type hint `-> pd.DataFrame` e la docstring dicono a chi legge (e a Copilot) cosa aspettarsi.
            Da qui in avanti, quando una fonte dati va letta più di una volta, la strada è questa: una
            funzione piccola, con un nome che dice cosa restituisce.
        """)
        nb.box("ricorda", """
            - `requests.get(url, params=params, timeout=30)`, poi `raise_for_status()`, poi `.json()`.
            - Un dizionario di liste o una lista di dizionari diventano tabella con `pd.DataFrame(...)`.
            - Tre righe che si ripetono sono una funzione.
        """)

    # ------------------------------------------------------------------ 6 (Base)
    with nb.solo("base"):
        nb.sezione("Ripasso: CSV, Excel e SQL", intro="""
            Un esercizio breve per ogni formato, con i passi scritti uno per uno. L'obiettivo è arrivare in
            fondo senza tornare a guardare sopra.
        """)
        nb.prova_tu(
            richiesta="""
                Il commerciale di Varese vuole l'elenco dei suoi impianti in un file a parte.

                1. Leggi `../Dati/impianti_fv.csv` in `impianti`.
                2. Crea la maschera `mask` per la `provincia` uguale a `"VA"`.
                3. Metti le righe filtrate in `impianti_va`.
                4. Salva `impianti_va` in `impianti_va.csv`, senza indice.
            """,
            starter="""
                impianti = ...
                mask = ...
                impianti_va = ...
                ...
                impianti_va
            """,
            soluzione="""
                impianti = pd.read_csv("../Dati/impianti_fv.csv")
                mask = impianti["provincia"] == "VA"
                impianti_va = impianti[mask]
                impianti_va.to_csv("impianti_va.csv", index=False)
                impianti_va
            """,
            verifica="""
                assert Path("impianti_va.csv").exists(), "❌ Il file impianti_va.csv non c'è nella cartella del notebook"
                controllo = pd.read_csv("impianti_va.csv")
                assert len(controllo) == 4, "❌ Gli impianti in provincia di Varese sono 4: controlla la maschera"
                assert set(controllo["provincia"]) == {"VA"}, "❌ Nel file ci sono impianti di altre province"
                assert "Unnamed: 0" not in controllo.columns, "❌ Salva con index=False: c'è una colonna in più"
            """,
        )
        nb.prova_tu(
            richiesta="""
                Il customer care vuole un Excel con i consumi e l'anagrafica, senza il foglio del listino.

                1. Leggi i fogli `Consumi` e `Anagrafica` di `../Dati/bolletta_esempio.xlsx` in
                   `consumi_mensili` e `anagrafica`.
                2. Con `pd.ExcelWriter` scrivi `consumi_anagrafica.xlsx` con due fogli, `Consumi` e
                   `Anagrafica`, senza indice.
            """,
            starter="""
                consumi_mensili = pd.read_excel(...)
                anagrafica = pd.read_excel(...)

                with pd.ExcelWriter(...) as writer:
                    ...
                    ...
            """,
            soluzione="""
                consumi_mensili = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Consumi")
                anagrafica = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Anagrafica")

                with pd.ExcelWriter("consumi_anagrafica.xlsx") as writer:
                    consumi_mensili.to_excel(writer, sheet_name="Consumi", index=False)
                    anagrafica.to_excel(writer, sheet_name="Anagrafica", index=False)
            """,
            verifica="""
                assert Path("consumi_anagrafica.xlsx").exists(), "❌ Il file consumi_anagrafica.xlsx non c'è nella cartella del notebook"
                controllo = pd.read_excel("consumi_anagrafica.xlsx", sheet_name=None)
                assert set(controllo.keys()) == {"Consumi", "Anagrafica"}, "❌ I fogli devono chiamarsi Consumi e Anagrafica, e basta"
                assert controllo["Consumi"].shape == (72, 5), "❌ Il foglio Consumi deve avere 72 righe e 5 colonne: salva con index=False"
                assert controllo["Anagrafica"].shape == (6, 3), "❌ Il foglio Anagrafica deve avere 6 righe e 3 colonne"
            """,
        )
        nb.prova_tu(
            richiesta="""
                Quanti clienti abbiamo a Milano?

                1. Apri la connessione a `../Dati/utility.db` in `con`.
                2. Con `pd.read_sql` e un `WHERE` sul `comune` prendi i clienti di Milano in `clienti_milano`.
                3. Chiudi la connessione.
                4. Metti in `n_milano` il numero di righe.
            """,
            starter="""
                con = sqlite3.connect(...)
                clienti_milano = pd.read_sql(..., con)
                ...

                n_milano = ...
                clienti_milano
            """,
            soluzione="""
                con = sqlite3.connect("../Dati/utility.db")
                clienti_milano = pd.read_sql("SELECT * FROM clienti WHERE comune = 'Milano'", con)
                con.close()

                n_milano = len(clienti_milano)
                clienti_milano
            """,
            verifica="""
                assert n_milano == 2, "❌ I clienti con comune Milano sono 2: controlla il WHERE (il nome va tra apici singoli)"
                assert set(clienti_milano["ragione_sociale"]) == {"Panificio Rossi", "Hotel Belvedere"}, "❌ clienti_milano: devono esserci solo i due clienti di Milano"
            """,
        )

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il CSV del fornitore",
        scenario="""
            Siamo nell'ufficio Analisi Consumi. Il Panificio Rè (POD `IT001E45678901`) contesta la bolletta
            di luglio, e il collega che segue il fornitore vuole le righe di quel POD in un file a parte da
            girargli oggi. Il CSV è quello di prima, con tutti i suoi vizi.
        """,
        richiesta="""
            1. Leggi `../Dati/letture_pod_2025.csv` in `letture` con i tre parametri giusti, e controlla con
               `info()` che `kwh` sia un numero.
            2. Crea `mask` per il POD `IT001E45678901` e metti le sue righe in `anomalo`.
            3. Salva `anomalo` in `pod_anomalo.csv`, senza indice.
            4. Metti in `kwh_max` il valore massimo di `kwh` in `anomalo`: è la lettura da contestare.
        """,
        suggerimento="Se `info()` dice che `kwh` è `str`, manca `decimal=\",\"`.",
        starter="""
            letture = pd.read_csv("../Dati/letture_pod_2025.csv", ...)
            letture.info()

            mask = ...
            anomalo = ...
            ...

            kwh_max = ...
            kwh_max
        """,
        soluzione="""
            letture = pd.read_csv("../Dati/letture_pod_2025.csv", encoding="latin-1", sep=";", decimal=",")
            letture.info()

            mask = letture["pod"] == "IT001E45678901"
            anomalo = letture[mask]
            anomalo.to_csv("pod_anomalo.csv", index=False)

            kwh_max = anomalo["kwh"].max()
            kwh_max
        """,
        verifica="""
            assert letture.shape == (216, 5), "❌ letture: 216 righe e 5 colonne (serve sep=';')"
            assert str(letture["kwh"].dtype) == "float64", "❌ kwh deve essere un numero: serve decimal=','"
            assert len(anomalo) == 36, "❌ anomalo: il POD ha 12 mesi per 3 fasce, 36 righe"
            assert set(anomalo["pod"]) == {"IT001E45678901"}, "❌ anomalo: dentro c'è un POD diverso"
            assert Path("pod_anomalo.csv").exists(), "❌ Il file pod_anomalo.csv non c'è nella cartella del notebook"
            assert pd.read_csv("pod_anomalo.csv").shape == (36, 5), "❌ pod_anomalo.csv: 36 righe e 5 colonne, salva con index=False"
            assert kwh_max == 5785.2, "❌ kwh_max: il massimo della colonna kwh di anomalo"
        """,
        perche="""
            La maschera in una variabile con un nome si guarda da sola prima di usarla. E `index=False`
            evita la colonna in più senza nome che il fornitore avrebbe chiamato per chiedere cos'è.
        """,
    )
    nb.esercizio(
        titolo="I file dei turni",
        bis=True,
        scenario="""
            La sala controllo salva le potenze medie orarie della cabina in un CSV per turno, tre al
            giorno. Il responsabile vuole la giornata intera in una tabella sola, e l'energia totale: oggi
            incolla i tre file uno sotto l'altro a mano.
        """,
        richiesta="""
            Le prime righe della cella, già scritte, creano i tre file dei turni. Poi:

            1. Elenca i file `cabina_turno_*.csv` della cartella del notebook, in ordine, in `file_turni`.
            2. Con un ciclo leggi ogni file e aggiungilo alla lista `tabelle`.
            3. Impila le tabelle in `giornata` con `pd.concat`, rinumerando le righe da 0.
            4. Metti in `energia_mwh` la somma della colonna `mw`: con un valore all'ora, i MW sommati sono
               già MWh.
        """,
        suggerimento="`sorted(Path(\".\").glob(...))` per i file; `ignore_index=True` per rinumerare.",
        starter="""
            turno_1 = pd.DataFrame({"ora": [0, 1, 2, 3, 4, 5, 6, 7],
                                    "mw": [8.1, 7.9, 7.8, 7.7, 7.9, 8.4, 9.2, 10.1]})
            turno_2 = pd.DataFrame({"ora": [8, 9, 10, 11, 12, 13, 14, 15],
                                    "mw": [10.8, 11.2, 11.5, 11.4, 11.0, 10.9, 11.1, 11.3]})
            turno_3 = pd.DataFrame({"ora": [16, 17, 18, 19, 20, 21, 22, 23],
                                    "mw": [11.0, 10.7, 10.9, 10.4, 9.8, 9.1, 8.6, 8.2]})
            turno_1.to_csv("cabina_turno_1.csv", index=False)
            turno_2.to_csv("cabina_turno_2.csv", index=False)
            turno_3.to_csv("cabina_turno_3.csv", index=False)

            file_turni = ...
            tabelle = []
            for file in file_turni:
                ...

            giornata = ...
            energia_mwh = ...
            print(giornata.shape, energia_mwh)
        """,
        soluzione="""
            turno_1 = pd.DataFrame({"ora": [0, 1, 2, 3, 4, 5, 6, 7],
                                    "mw": [8.1, 7.9, 7.8, 7.7, 7.9, 8.4, 9.2, 10.1]})
            turno_2 = pd.DataFrame({"ora": [8, 9, 10, 11, 12, 13, 14, 15],
                                    "mw": [10.8, 11.2, 11.5, 11.4, 11.0, 10.9, 11.1, 11.3]})
            turno_3 = pd.DataFrame({"ora": [16, 17, 18, 19, 20, 21, 22, 23],
                                    "mw": [11.0, 10.7, 10.9, 10.4, 9.8, 9.1, 8.6, 8.2]})
            turno_1.to_csv("cabina_turno_1.csv", index=False)
            turno_2.to_csv("cabina_turno_2.csv", index=False)
            turno_3.to_csv("cabina_turno_3.csv", index=False)

            file_turni = sorted(Path(".").glob("cabina_turno_*.csv"))
            tabelle = []
            for file in file_turni:
                tabelle.append(pd.read_csv(file))

            giornata = pd.concat(tabelle, ignore_index=True)
            energia_mwh = giornata["mw"].sum()
            print(giornata.shape, energia_mwh)
        """,
        verifica="""
            assert len(file_turni) == 3, "❌ file_turni: devono essere i tre file cabina_turno_*.csv"
            assert giornata.shape == (24, 2), "❌ giornata: 24 righe (8 per turno) e 2 colonne"
            assert set(giornata["ora"]) == set(range(24)), "❌ giornata: devono esserci tutte le ore da 0 a 23"
            assert list(giornata.index) == list(range(24)), "❌ Le righe vanno rinumerate da 0 a 23: ignore_index=True"
            assert round(energia_mwh, 1) == 235.0, "❌ energia_mwh: somma della colonna mw"
        """,
        perche="""
            Il ciclo non sa quanti file ci sono, e non gli importa: domani con quattro turni funziona
            uguale.
        """,
    )
    nb.esercizio(
        titolo="Chi è il cliente",
        scenario="""
            Al customer care arriva una telefonata: "sono il titolare del POD IT001E10031676, la bolletta
            di marzo è troppo alta". L'operatrice ha il database ma non il gestionale, e Python aperto.
            Vuole sapere chi è il cliente e quanto ha consumato davvero.
        """,
        richiesta="""
            1. Apri la connessione a `../Dati/utility.db` in `con`.
            2. Con `pd.read_sql` e `WHERE`, prendi la riga di quel POD dalla tabella `pod` in `scheda_pod` e
               guarda nella tabella stampata il suo `id_cliente`.
            3. Con un'altra query prendi il cliente dalla tabella `clienti` in `scheda_cliente`, scrivendo
               nel `WHERE` il numero che hai letto (è un numero: senza apici).
            4. Prendi tutte le letture di quel POD in `letture_pod`, poi metti in `n_letture` quante sono e
               in `kwh_marzo` la somma dei kWh, arrotondata a un decimale.
            5. Chiudi la connessione.
        """,
        suggerimento="Il POD in una variabile e la query con una f-string: `f\"SELECT * FROM letture WHERE pod = '{pod_cercato}'\"`. Gli apici singoli restano, sono SQL.",
        starter="""
            pod_cercato = "IT001E10031676"

            con = sqlite3.connect("../Dati/utility.db")
            scheda_pod = pd.read_sql(..., con)
            display(scheda_pod)

            scheda_cliente = pd.read_sql(..., con)
            display(scheda_cliente)

            letture_pod = pd.read_sql(..., con)
            ...

            n_letture = ...
            kwh_marzo = ...
            print(n_letture, kwh_marzo)
        """,
        soluzione="""
            pod_cercato = "IT001E10031676"

            con = sqlite3.connect("../Dati/utility.db")
            scheda_pod = pd.read_sql(f"SELECT * FROM pod WHERE pod = '{pod_cercato}'", con)
            display(scheda_pod)

            scheda_cliente = pd.read_sql("SELECT * FROM clienti WHERE id_cliente = 9", con)
            display(scheda_cliente)

            letture_pod = pd.read_sql(f"SELECT * FROM letture WHERE pod = '{pod_cercato}'", con)
            con.close()

            n_letture = len(letture_pod)
            kwh_marzo = round(letture_pod["kwh"].sum(), 1)
            print(n_letture, kwh_marzo)
        """,
        verifica="""
            assert list(scheda_pod["id_cliente"]) == [9], "❌ scheda_pod: una sola riga, quella del POD cercato, con id_cliente 9"
            assert set(scheda_cliente["ragione_sociale"]) == {"Farmacia San Marco"}, "❌ scheda_cliente: nel WHERE scrivi l'id_cliente che vedi in scheda_pod, senza apici"
            assert n_letture == 31, "❌ n_letture: marzo ha 31 giorni, una lettura al giorno"
            assert kwh_marzo == 3094.4, "❌ kwh_marzo: somma della colonna kwh di letture_pod, a un decimale"
        """,
        perche="""
            L'`id_cliente` l'abbiamo letto a occhio dalla prima query e scritto nella seconda: con due
            query va bene così. Con una sola, con il `JOIN`, lo fa il database (è il passo in più).
        """,
        passo_in_piu=dict(
            testo="""
                Il database può fare tutto in un colpo. Con una query sola e due `JOIN` in fila (da
                `letture` a `pod` su `pod`, da `pod` a `clienti` su `id_cliente`), prendi per il POD
                cercato le colonne `data`, `kwh` e `ragione_sociale` in `letture_cliente`. Riapri la
                connessione prima e richiudila dopo.
            """,
            starter="""
                con = sqlite3.connect("../Dati/utility.db")
                query = f\"\"\"
                SELECT ...
                FROM letture AS l
                JOIN ...
                JOIN ...
                WHERE l.pod = '{pod_cercato}'
                \"\"\"
                letture_cliente = pd.read_sql(query, con)
                con.close()
                letture_cliente.head()
            """,
            soluzione="""
                con = sqlite3.connect("../Dati/utility.db")
                query = f\"\"\"
                SELECT l.data, l.kwh, c.ragione_sociale
                FROM letture AS l
                JOIN pod AS p ON l.pod = p.pod
                JOIN clienti AS c ON p.id_cliente = c.id_cliente
                WHERE l.pod = '{pod_cercato}'
                \"\"\"
                letture_cliente = pd.read_sql(query, con)
                con.close()
                letture_cliente.head()
            """,
            verifica="""
                assert letture_cliente.shape == (31, 3), "❌ letture_cliente: 31 righe e le tre colonne data, kwh, ragione_sociale"
                assert set(letture_cliente["ragione_sociale"]) == {"Farmacia San Marco"}, "❌ letture_cliente: il secondo JOIN deve portare la ragione sociale del cliente"
            """,
        ),
    )
    nb.esercizio(
        titolo="Il listino nel foglio giusto",
        bis=True,
        scenario="""
            Il collega della fatturazione vuole un Excel con il listino e l'anagrafica dei clienti, ma
            senza il foglio `Consumi`, che è riservato. E il foglio del listino lo vuole chiamato `Prezzi`,
            perché così si chiama nel suo gestionale.
        """,
        richiesta="""
            1. Leggi tutti i fogli di `../Dati/bolletta_esempio.xlsx` nel dizionario `fogli`.
            2. Scrivi `listino_clienti.xlsx` con due fogli: `Prezzi` (il listino) e `Clienti` (l'anagrafica),
               senza indice.
            3. Rileggi il file con `sheet_name=None` in `controllo` e metti in `nomi_fogli` la lista dei
               nomi dei suoi fogli.
        """,
        suggerimento="Le chiavi di un dizionario diventano lista con `list(controllo.keys())`.",
        starter="""
            fogli = pd.read_excel("../Dati/bolletta_esempio.xlsx", ...)

            with pd.ExcelWriter("listino_clienti.xlsx") as writer:
                ...
                ...

            controllo = ...
            nomi_fogli = ...
            nomi_fogli
        """,
        soluzione="""
            fogli = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name=None)

            with pd.ExcelWriter("listino_clienti.xlsx") as writer:
                fogli["Listino"].to_excel(writer, sheet_name="Prezzi", index=False)
                fogli["Anagrafica"].to_excel(writer, sheet_name="Clienti", index=False)

            controllo = pd.read_excel("listino_clienti.xlsx", sheet_name=None)
            nomi_fogli = list(controllo.keys())
            nomi_fogli
        """,
        verifica="""
            assert Path("listino_clienti.xlsx").exists(), "❌ Il file listino_clienti.xlsx non c'è nella cartella del notebook"
            assert set(nomi_fogli) == {"Prezzi", "Clienti"}, "❌ nomi_fogli: i fogli devono chiamarsi Prezzi e Clienti, e basta"
            assert controllo["Prezzi"].shape == (3, 2), "❌ Il foglio Prezzi deve avere le 3 fasce e 2 colonne: salva con index=False"
            assert controllo["Clienti"].shape == (6, 3), "❌ Il foglio Clienti deve avere 6 clienti e 3 colonne"
        """,
        perche="""
            Rileggere il file appena scritto è il controllo più semplice che esista, e il collega che lo
            apre non trova sorprese.
        """,
    )
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="Quanto fa caldo a Milano",
            scenario="""
                Il responsabile della sala controllo vuole, ogni mattina, la temperatura media prevista a
                Milano per i prossimi sette giorni, un numero per giorno: d'estate il carico del Nord segue
                il condizionamento. Abbiamo `get_json` e Open-Meteo.
            """,
            richiesta="""
                1. Con `get_json`, chiedi a `https://api.open-meteo.com/v1/forecast` la previsione oraria di
                   `temperature_2m` per Milano (45.4642, 9.19), fuso `Europe/Rome`, 7 giorni, in `dati`.
                2. Costruisci `previsione` da `dati["hourly"]`, trasforma `time` in data e aggiungi la
                   colonna `giorno`.
                3. Con un ciclo sui giorni, calcola per ognuno la media di `temperature_2m` con una maschera
                   e salvala nel dizionario `media_per_giorno` (chiave il giorno, valore la media
                   arrotondata a un decimale).
                4. Metti in `temperatura_max` il massimo orario dei sette giorni.
            """,
            suggerimento="I giorni distinti, in ordine: `sorted(set(previsione[\"giorno\"]))`. Senza rete, le due righe commentate nella cella leggono la risposta salvata.",
            starter="""
                import json

                url = "https://api.open-meteo.com/v1/forecast"
                params = {...}
                dati = get_json(url, params)
                # se l'API non risponde: commenta la riga sopra e togli il # alle due righe sotto
                # with open("../Dati/fallback/meteo_milano_previsione.json", encoding="utf-8") as f:
                #     dati = json.load(f)

                previsione = ...
                previsione["time"] = ...
                previsione["giorno"] = ...

                media_per_giorno = {}
                for giorno in sorted(set(previsione["giorno"])):
                    mask = ...
                    media_per_giorno[giorno] = ...

                temperatura_max = ...
                print(media_per_giorno)
                print(temperatura_max)
            """,
            soluzione="""
                import json

                url = "https://api.open-meteo.com/v1/forecast"
                params = {
                    "latitude": 45.4642,
                    "longitude": 9.19,
                    "hourly": "temperature_2m",
                    "timezone": "Europe/Rome",
                    "forecast_days": 7,
                }
                dati = get_json(url, params)
                # se l'API non risponde: commenta la riga sopra e togli il # alle due righe sotto
                # with open("../Dati/fallback/meteo_milano_previsione.json", encoding="utf-8") as f:
                #     dati = json.load(f)

                previsione = pd.DataFrame(dati["hourly"])
                previsione["time"] = pd.to_datetime(previsione["time"])
                previsione["giorno"] = previsione["time"].dt.date

                media_per_giorno = {}
                for giorno in sorted(set(previsione["giorno"])):
                    mask = previsione["giorno"] == giorno
                    media_per_giorno[giorno] = round(previsione[mask]["temperature_2m"].mean(), 1)

                temperatura_max = previsione["temperature_2m"].max()
                print(media_per_giorno)
                print(temperatura_max)
            """,
            verifica="""
                assert len(previsione) == 168, "❌ previsione: 7 giorni per 24 ore fanno 168 righe (controlla forecast_days)"
                assert str(previsione["time"].dtype).startswith("datetime64"), "❌ previsione['time'] deve essere una data: pd.to_datetime"
                assert len(media_per_giorno) == 7, "❌ media_per_giorno: una chiave per ciascuno dei 7 giorni"
                assert abs(sum(media_per_giorno.values()) / 7 - previsione["temperature_2m"].mean()) < 0.1, "❌ media_per_giorno: la media di ogni giorno va calcolata sulle sole righe di quel giorno (maschera)"
                assert temperatura_max == previsione["temperature_2m"].max(), "❌ temperatura_max: il massimo della colonna temperature_2m"
            """,
            perche="""
                Il ciclo con una maschera per giorno è il modo onesto di raggruppare con quello che sappiamo
                oggi. Nel prossimo notebook `groupby` fa le stesse sette medie in una riga.
            """,
            rete=True,
            passo_in_piu=dict(
                testo="""
                    Dall'anagrafica dei sensori (riusa `sensori`, oppure richiamala con `get_json`), tieni
                    solo quelli di tipologia `Temperatura` e conta quanti sono per provincia con
                    `value_counts()` in `termometri_per_provincia`. Metti in `provincia_top` la provincia
                    con più termometri: `value_counts()` ordina dal più frequente, quindi è il primo nome
                    dell'indice, `termometri_per_provincia.index[0]`.
                """,
                starter="""
                    mask = ...
                    termometri = ...
                    termometri_per_provincia = ...
                    provincia_top = ...
                    print(provincia_top)
                    termometri_per_provincia
                """,
                soluzione="""
                    mask = sensori["tipologia"] == "Temperatura"
                    termometri = sensori[mask]
                    termometri_per_provincia = termometri["provincia"].value_counts()
                    provincia_top = termometri_per_provincia.index[0]
                    print(provincia_top)
                    termometri_per_provincia
                """,
                verifica="""
                    assert termometri_per_provincia.sum() == len(termometri), "❌ termometri_per_provincia: value_counts della colonna provincia dei soli termometri"
                    assert len(termometri_per_provincia) <= 12, "❌ termometri_per_provincia: la Lombardia ha 12 province, qui ce ne sono di più"
                    assert termometri_per_provincia[provincia_top] == termometri_per_provincia.max(), "❌ provincia_top: la provincia con il conteggio più alto"
                """,
            ),
        )
    return nb
