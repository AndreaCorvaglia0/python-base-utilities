"""07 · Pandas: operazioni sui DataFrame."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="07",
        file="07_Pandas_operazioni",
        titolo="Pandas: operazioni sui DataFrame",
        blocco=3,
        giornata=2,
        intento=(
            "Il notebook mostra come selezionare, pulire, trasformare, ordinare e raggruppare i dati di un "
            "DataFrame, e come unire tabelle diverse."
        ),
        obiettivi={
            "base": [
                "selezionare righe e colonne con `loc`, `iloc` e le condizioni",
                "gestire valori mancanti e duplicati, creare colonne nuove e ordinare",
                "raggruppare con `groupby` e unire DataFrame con `merge` e `concat`",
            ],
            "avanzata": [
                "selezionare righe e colonne con `loc`, `iloc`, le condizioni e `.query()`",
                "gestire valori mancanti e duplicati, creare colonne nuove e ordinare",
                "raggruppare con `groupby` e unire DataFrame con `merge` e `concat`",
            ],
        },
        tempo={"base": 70, "avanzata": 75},
        dati=["U.S. Electricity Prices.csv"],
    )

    nb.md("""
        Come di consueto importiamo all'inizio le librerie che ci servono, pandas e NumPy; da NumPy useremo
        soltanto `np.nan`, il valore che rappresenta un dato mancante. Ricreiamo poi il DataFrame del
        notebook precedente, con il nome, l'età e la città di tre persone e un indice fatto di etichette.
    """)
    nb.code("""
        import numpy as np
        import pandas as pd
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

    # ------------------------------------------------------------------ 1
    nb.sezione("Selezione dei dati", intro="""
        In pandas possiamo selezionare i dati di un DataFrame per nome di colonna, per etichetta dell'indice
        o per posizione. La selezione per etichetta è ciò che distingue un DataFrame da una lista di liste,
        perché permette di indicare righe e colonne con il loro nome invece che con un numero.
    """)
    nb.sottosezione("Selezione di righe e colonne", intro="""
        Possiamo selezionare una o più colonne di un DataFrame usando il nome della colonna come chiave.
        Con una lista di nomi tra doppie parentesi quadre il risultato è ancora un DataFrame, anche quando
        la colonna è una sola; con un solo nome, come in `df["Età"]`, otterremmo invece una Series.
    """)
    nb.code("""
        # selezionare una singola colonna
        df[["Età"]]
    """)
    nb.code("""
        # selezionare più colonne
        df[["Nome", "Città"]]
    """)
    nb.md("""
        Con `loc` e `iloc` selezioniamo righe specifiche in base all'indice o alla posizione. Entrambi
        ricevono tra parentesi quadre due argomenti separati da una virgola, prima le righe e poi le
        colonne. Nell'esempio `loc` usa le etichette `id_1` e `id_2`, mentre `iloc` usa le posizioni 0 e 1
        e la colonna in posizione 1, che è `Età`.
    """)
    nb.code("""
        # loc: in base all'indice
        df.loc["id_1":"id_2", ["Età"]]
    """)
    nb.code("""
        # iloc: in base alla posizione
        df.iloc[0:2, [1]]
    """)

    nb.md("""
        Le due celle restituiscono le stesse righe, ma lo slicing si comporta in modo diverso nei due casi.
        Con `loc` l'intervallo `"id_1":"id_2"` include anche l'ultima etichetta, mentre con `iloc`
        l'intervallo `0:2` esclude l'ultima posizione, come accade con le liste Python.
    """)

    nb.sottosezione("Selezione condizionale", intro="""
        Possiamo filtrare le righe di un DataFrame con condizioni booleane. Una condizione su una colonna,
        come `df["Età"] > 23`, viene valutata riga per riga e restituisce una Series di `True` e `False`
        con lo stesso indice del DataFrame. Una Series di questo tipo si chiama maschera booleana.
    """)
    nb.code("""
        df["Età"] > 23
    """)
    nb.md("""
        Se passiamo la maschera al DataFrame tra parentesi quadre, pandas tiene soltanto le righe in cui la
        maschera vale `True`. Nel nostro caso restano Alice e Bob, che hanno più di 23 anni.
    """)
    nb.code("""
        df[df["Età"] > 23]
    """)
    nb.md("""
        Più condizioni si combinano con gli operatori `&` (e), `|` (o) e `~` (non), e ciascuna va scritta
        tra parentesi tonde, perché questi operatori hanno la precedenza sui confronti. Quando la condizione
        è lunga o serve più volte, conviene salvare la maschera in una variabile, come `condiz_eta`.
    """)
    nb.code("""
        condiz_eta = (df["Età"] > 23) & (df["Età"] < 26)
        condiz_eta
    """)
    nb.md("""
        La maschera si può passare anche a `loc` come primo argomento, al posto delle etichette delle righe,
        mentre il secondo argomento sceglie le colonne. In questo modo filtro e selezione delle colonne
        stanno in un'unica espressione; con l'età compresa tra 23 e 26 anni, estremi esclusi, resta soltanto
        Alice.
    """)
    nb.code("""
        # righe con età tra 23 e 26 (esclusi), solo la colonna Nome
        df.loc[(df["Età"] > 23) & (df["Età"] < 26), ["Nome"]]
    """)

    with nb.solo("avanzata"):
        nb.sottosezione("Il metodo query", intro="""
            Il metodo `.query()` filtra le righe con una condizione scritta come testo, nella forma
            `df.query("condizione")`. Dentro la stringa i nomi delle colonne si scrivono senza virgolette e
            le condizioni si uniscono con `and` e `or`, per cui il filtro risulta più leggibile quando le
            condizioni sono più di una. L'esempio ripete il filtro precedente e poi seleziona due colonne con
            `loc`.
        """)
        nb.code("""
            colonne = ["Età", "Nome"]
            df.query("Età > 23 and Età < 26").loc[:, colonne]
        """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Manipolazione dei dati", intro="""
        La manipolazione dei dati in pandas comprende la gestione dei valori mancanti, la pulizia dei dati
        e la trasformazione. Sono operazioni che di solito si eseguono subito dopo la lettura di un file e
        prima di qualsiasi analisi, perché i dati reali arrivano spesso con valori assenti, righe ripetute
        o colonne da ricavare.
    """)
    nb.sottosezione("Valori mancanti", intro="""
        I valori mancanti possono causare problemi nelle analisi e vanno gestiti adeguatamente. In pandas un
        valore numerico mancante si rappresenta con `NaN` (*Not a Number*), e anche il `None` di Python,
        inserito in una colonna numerica, viene convertito in `NaN`. Il DataFrame qui sotto ha tre valori
        mancanti, uno in ciascuna colonna.
    """)
    nb.code("""
        # creare un DataFrame con valori mancanti
        dati_mancanti = {
            "A": [1, 2, np.nan],
            "B": [4, None, 6],
            "C": [7, 8, np.nan],
        }
        df_mancanti = pd.DataFrame(dati_mancanti)
        df_mancanti
    """)
    nb.md("""
        Il metodo `isnull()` restituisce un DataFrame di `True` e `False` che indica, cella per cella, se il
        valore manca, mentre `notnull()` fa il contrario. Poiché nella somma `True` vale 1 e `False` vale 0,
        aggiungendo `.sum()` otteniamo il numero di valori mancanti in ogni colonna.
    """)
    nb.code("""
        # identificare i valori mancanti
        df_mancanti.isnull().sum()
    """)
    nb.md("""
        Una volta individuati, i valori mancanti si possono trattare in tre modi. Il riempimento, con
        `fillna()`, sostituisce ogni valore mancante con un valore scelto da noi; la rimozione, con
        `dropna()`, elimina le righe o le colonne che contengono valori mancanti; l'interpolazione, infine,
        stima i valori mancanti a partire da quelli esistenti ed è utile soprattutto con le serie temporali.
        Nella cella qui sotto riempiamo tutti i valori mancanti con zero.
    """)
    nb.code("""
        # riempire i valori mancanti con zero
        df_riempito = df_mancanti.fillna(0)
        df_riempito
    """)
    nb.md("""
        Il metodo `fillna()` non modifica il DataFrame di partenza ma ne restituisce una copia, per cui
        `df_mancanti` contiene ancora i suoi valori mancanti. Per cambiare una colonna dobbiamo riassegnarla,
        come nella cella qui sotto, dove riempiamo la colonna `A` con la sua mediana. Applicando poi
        `dropna()` resta soltanto la prima riga, l'unica senza valori mancanti nelle colonne `B` e `C`.
    """)
    nb.code("""
        df_mancanti["A"] = df_mancanti["A"].fillna(df_mancanti["A"].median())
        df_mancanti.dropna()
    """)
    nb.md("""
        La scelta tra rimuovere e riempire dipende dai dati. Conviene rimuovere le righe quando i valori
        mancanti sono pochi e la loro eliminazione non cambia il risultato dell'analisi; conviene riempirli
        quando sono molti, purché esista un valore appropriato con cui sostituirli, come lo zero per una
        quantità non registrata o la mediana per una misura.
    """)

    nb.sottosezione("Duplicati", intro="""
        Le righe duplicate possono distorcere i risultati delle analisi, per esempio facendo contare due
        volte la stessa vendita, e vanno quindi identificate e gestite. Nel DataFrame di esempio la terza
        riga ripete esattamente la prima.
    """)
    nb.code("""
        # creare un DataFrame con duplicati
        dati_doppi = {
            "Nome": ["Alice", "Bob", "Alice"],
            "Età": [24, 27, 24],
            "Città": ["Roma", "Milano", "Roma"],
        }
        df_doppi = pd.DataFrame(dati_doppi)
        df_doppi
    """)
    nb.md("""
        Il metodo `duplicated()` restituisce una maschera booleana che vale `True` per ogni riga identica a
        una riga precedente, mentre la prima occorrenza resta `False`. Il metodo `drop_duplicates()`, nella
        cella successiva, elimina le righe segnalate e conserva la prima occorrenza di ciascuna.
    """)
    nb.code("""
        # identificare i duplicati
        df_doppi.duplicated()
    """)
    nb.code("""
        # rimuovere i duplicati
        df_senza_doppi = df_doppi.drop_duplicates()
        df_senza_doppi
    """)

    nb.sottosezione("Trasformazione", intro="""
        Possiamo aggiungere, modificare o eliminare colonne in un DataFrame per adattarlo alle nostre
        esigenze. Una colonna nuova si crea assegnando un'espressione a un nome che non esiste ancora, e
        l'espressione viene calcolata per tutte le righe insieme. Nell'esempio `70 - df["Età"]` produce gli
        anni mancanti alla pensione di ciascuna persona, senza bisogno di un ciclo.
    """)
    nb.code("""
        df["Anni alla pensione"] = 70 - df["Età"]
        df
    """)
    with nb.solo("avanzata"):
        nb.md("""
            Con `.loc` e una maschera possiamo modificare soltanto le righe che rispettano una condizione.
            Nell'esempio applichiamo una riforma ipotetica, per cui chi ha meno di 25 anni ha il 30% di anni
            in più alla pensione, mentre per gli altri il valore resta lo stesso. La prima cella salva la
            condizione nella variabile `cond_riforma`.
        """)
        nb.code("""
            cond_riforma = df["Età"] < 25
        """)
        nb.md("""
            La seconda cella scrive la nuova colonna in due passi. Per le righe in cui `cond_riforma` vale
            `True` moltiplica gli anni per 1,3, mentre per le altre, selezionate con `~cond_riforma`, copia il
            valore originale; poiché la colonna non esiste ancora, pandas la crea alla prima assegnazione.
        """)
        nb.code("""
            df.loc[cond_riforma, "Anni alla pensione riforma"] = df.loc[cond_riforma, "Anni alla pensione"] * 1.3
            df.loc[~cond_riforma, "Anni alla pensione riforma"] = df.loc[~cond_riforma, "Anni alla pensione"]
            df
        """)
        nb.box("attenzione", """
            Un'assegnazione scritta come `df[cond]["col"] = valore` non modifica `df`, perché il primo filtro
            produce una copia e il valore viene scritto su quella; pandas 3 lo segnala con l'avviso
            `ChainedAssignmentError`. Per cambiare le righe filtrate si usa sempre la forma
            `df.loc[cond, "col"] = valore`, che seleziona righe e colonna in un'unica operazione.
        """)
    nb.md("""
        Quando la colonna nuova non si ottiene con un calcolo aritmetico, sono utili due metodi. Il primo è
        `.map()`, che traduce ogni valore di una colonna attraverso un dizionario; nella cella qui sotto lo
        usiamo per ricavare la regione dalla città.
    """)
    nb.code("""
        regioni = {"Roma": "Lazio", "Milano": "Lombardia", "Torino": "Piemonte"}
        df["Regione"] = df["Città"].map(regioni)
        df
    """)
    nb.md("""
        Il secondo è `.apply()`, che applica a ogni valore una funzione scritta da noi ed è la scelta
        naturale quando la regola richiede un `if`. La funzione `fascia_eta` riceve un'età e restituisce
        l'etichetta della fascia corrispondente.
    """)
    nb.code('''
        def fascia_eta(eta):
            """Restituisce la fascia d'età di una persona."""
            if eta < 25:
                return "under 25"
            return "25 e oltre"


        df["Fascia"] = df["Età"].apply(fascia_eta)
        df
    ''')

    nb.sottosezione("Gestione degli indici", aula="base", intro="""
        Quando ordiniamo un DataFrame con `sort_values`, che vedremo tra poco, ogni riga conserva l'etichetta
        di indice che aveva prima, e l'indice risulta quindi in disordine. Il metodo `reset_index(drop=True)`
        crea un nuovo indice che parte da 0 e scarta il vecchio, invece di trasformarlo in una colonna.
    """)
    with nb.solo("avanzata"):
        nb.sottosezione("Gestione degli indici", intro="""
            Gli indici permettono di accedere ai dati per etichetta e di allineare e unire tabelle diverse.
            `set_index()` trasforma una o più colonne in indice, `reset_index()` fa il contrario. Con un
            indice formato da due colonne, una riga si seleziona con una tupla di etichette, come
            `("Alice", "Roma")`.
        """)
        nb.code("""
            # impostare due colonne come indice
            df_indicizzato = df.set_index(["Nome", "Città"])
            df_indicizzato.loc[("Alice", "Roma")]
        """)
        nb.code("""
            # resettare l'indice
            df_reset = df_indicizzato.reset_index()
            df_reset
        """)
        nb.md("""
            Quando ordiniamo un DataFrame con `sort_values`, che vedremo tra poco, ogni riga conserva
            l'etichetta di indice che aveva prima, e l'indice risulta quindi in disordine. Con
            `reset_index(drop=True)` l'indice riparte da 0 e quello vecchio viene scartato, invece di essere
            trasformato in una colonna come nella cella precedente.
        """)
    nb.code("""
        df.sort_values("Età").reset_index(drop=True)
    """)

    nb.sottosezione("Rinomina delle colonne", intro="""
        Per rinominare le colonne si usa il metodo `rename`, a cui si passa con l'argomento `columns` un
        dizionario che associa a ogni nome vecchio il nome nuovo. Le colonne che non compaiono nel
        dizionario restano come sono, e il metodo restituisce un nuovo DataFrame senza modificare quello di
        partenza.
    """)
    nb.code("""
        df_rinominato = df.rename(columns={"Città": "Residenza", "Età": "age"})
        df_rinominato
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Ordinamento dei dati", intro="""
        L'ordinamento serve sia durante l'analisi, per esempio per trovare i valori più alti, sia nella
        presentazione dei risultati. Pandas offre due metodi, che ordinano le righe in base ai valori delle
        colonne oppure in base all'indice.
    """)
    nb.sottosezione("sort_values e sort_index", intro="""
        Il metodo `sort_values()` ordina le righe in base ai valori di una colonna, indicata con `by`.
        L'ordine predefinito è crescente, e con `ascending=False` si ordina dal valore più grande al più
        piccolo, come nell'esempio, che mette in cima la persona più anziana.
    """)
    nb.code("""
        # ordinare per età
        df_ordinato = df.sort_values(by="Età", ascending=False)
        df_ordinato
    """)
    nb.md("""
        Il metodo `sort_index()` ordina invece le righe in base all'indice, ed è utile quando l'indice ha un
        significato proprio, come un codice o una data. Applicato a `df_ordinato`, per esempio, riporterebbe
        le righe nell'ordine `id_1`, `id_2`, `id_3`.
    """)
    nb.sottosezione("Ordinamento su più colonne", intro="""
        Possiamo ordinare usando più colonne come chiavi, passando a `by` una lista di nomi. Le righe vengono
        ordinate secondo la prima colonna, e la seconda decide l'ordine solo tra le righe che hanno lo stesso
        valore nella prima. Anche `ascending` accetta una lista, con un valore per ciascuna colonna, per cui
        nell'esempio l'età è in ordine decrescente e il nome in ordine crescente.
    """)
    nb.code("""
        # ordinare per età e poi per nome
        df_ordinato_2 = df.sort_values(by=["Età", "Nome"], ascending=[False, True])
        df_ordinato_2
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Groupby", intro="""
        Il metodo `groupby()` suddivide un DataFrame in gruppi in base ai valori di una o più colonne, per
        poi applicare un'aggregazione ai dati di ciascun gruppo. Questa logica prende il nome di
        **Split-Apply-Combine**: i dati vengono prima divisi in gruppi (*split*), poi a ogni gruppo si applica
        una funzione come la somma, la media o il conteggio (*apply*), e infine i risultati vengono riuniti
        in un nuovo oggetto pandas, una Series o un DataFrame (*combine*). La forma tipica è
        `df.groupby("colonna_di_raggruppamento")["colonna"].funzione()`.
    """)
    nb.code("""
        vendite = pd.DataFrame({
            "Categoria": ["A", "B", "A", "B", "A", "C"],
            "Vendite": [100, 200, 150, 250, 120, 300],
        })

        # raggruppiamo per Categoria e sommiamo le vendite
        vendite.groupby("Categoria")["Vendite"].sum()
    """)
    nb.md("""
        Il metodo `groupby()` da solo restituisce un oggetto GroupBy, che contiene i gruppi ma non calcola
        ancora nulla e aspetta una funzione per elaborarli. Con `sum()` otteniamo una Series con una riga per
        gruppo, in cui la categoria fa da indice; nel nostro esempio la somma vale 370 per la categoria A,
        450 per la B e 300 per la C.
    """)
    with nb.solo("avanzata"):
        nb.sottosezione("Aggregazione multipla", intro="""
            Con il metodo `.agg()` calcoliamo più statistiche in una volta sola, passando un dizionario che
            associa a ogni colonna la lista delle funzioni da applicare. Il risultato ha una colonna per ogni
            statistica, e la selezione finale `["Vendite"]` toglie il livello superiore dei nomi di colonna,
            che altrimenti ripeterebbe `Vendite` sopra ciascuna.
        """)
        nb.code("""
            vendite.groupby("Categoria").agg({"Vendite": ["sum", "mean", "count"]})["Vendite"]
        """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Unione e concatenazione di DataFrame", intro="""
        Pandas offre diversi modi per combinare più DataFrame. I due più usati sono `merge()`, che affianca
        le colonne di due tabelle facendo corrispondere le righe attraverso una chiave, e `concat()`, che
        mette le tabelle una sotto l'altra.
    """)
    nb.sottosezione("Merge", intro="""
        Il metodo `merge()` combina due DataFrame in base a una o più colonne chiave comuni, come un join in
        SQL, e il parametro `how` stabilisce quali righe tenere. Con l'inner join restano solo le righe la
        cui chiave è presente in entrambi i DataFrame. Il left join tiene tutte le righe del DataFrame di
        sinistra, completate con i dati di destra dove c'è una corrispondenza, e il right join fa lo stesso
        partendo da destra. L'outer join, infine, tiene tutte le righe di entrambi, che abbiano una
        corrispondenza o no.
    """)
    nb.code("""
        # DataFrame di esempio
        df_sinistra = pd.DataFrame({"ID": [1, 2, 3], "Nome": ["Alice", "Bob", "Charlie"]})
        df_destra = pd.DataFrame({"ID": [3, 4, 5], "Età": [35, 40, 45]})

        # inner join
        df_inner = pd.merge(df_sinistra, df_destra, on="ID", how="inner")
        df_inner
    """)
    nb.md("""
        L'inner join restituisce una sola riga, perché l'ID 3 è l'unico presente in entrambi i DataFrame.
        Con l'outer join, nella cella successiva, compaiono invece tutti e cinque gli ID, e i valori che una
        delle due tabelle non fornisce restano `NaN`.
    """)
    nb.code("""
        # outer join
        df_outer = pd.merge(df_sinistra, df_destra, on="ID", how="outer")
        df_outer
    """)
    nb.md("""
        Con il left join teniamo tutte le righe del DataFrame di sinistra, cioè i tre nomi. Solo Charlie,
        che ha ID 3, trova un'età corrispondente in `df_destra`, mentre per Alice e Bob la colonna `Età`
        resta `NaN`.
    """)
    nb.code("""
        # left join
        pd.merge(df_sinistra, df_destra, on="ID", how="left")
    """)
    nb.sottosezione("Concatenazione", intro="""
        La funzione `concat()` unisce DataFrame verticalmente, aggiungendo le righe del secondo sotto quelle
        del primo. Con `ignore_index=True` l'indice del risultato riparte da 0, e con `sort=False` le colonne
        restano nell'ordine in cui compaiono, senza essere riordinate alfabeticamente.
    """)
    nb.code("""
        # concatenazione verticale
        df_concatenato = pd.concat([df_sinistra, df_destra], ignore_index=True, sort=False)
        df_concatenato
    """)
    nb.md("""
        Poiché `df_sinistra` e `df_destra` hanno colonne diverse, nel risultato ogni riga ha `NaN` nelle
        colonne che appartengono all'altra tabella. Per questo `concat()` si usa di solito con DataFrame che
        hanno le stesse colonne, come i fogli Excel del notebook precedente, mentre `merge()` serve quando le
        tabelle condividono una chiave e vogliamo affiancarne le informazioni.
    """)

    nb.md("Riassunto in una pagina: [Da Excel a pandas](../Schede/Scheda_Excel_pandas.md).")

    # ------------------------------------------------------------------ 6
    nb.sezione("Esercizi", intro="""
        Negli esercizi che seguono lavori come data analyst per un'azienda che gestisce una piattaforma di
        streaming musicale. I primi tre usano il DataFrame `ascolti`, definito nella cella qui sotto, che
        registra per ogni utente la canzone, l'artista e il numero di ascolti; la cella va eseguita prima di
        cominciare.
    """)
    nb.code("""
        # DataFrame degli ascolti
        dati_ascolti = {
            "UserID": [101, 102, 103, 104, 105, 106],
            "Song": ["Song A", "Song B", "Song A", "Song C", "Song B", "Song D"],
            "Artist": ["Artist X", "Artist Y", "Artist X", "Artist Z", "Artist Y", "Artist W"],
            "Plays": [15, 2, 4, 1, 5, 2],
        }
        ascolti = pd.DataFrame(dati_ascolti)
        ascolti
    """)

    nb.esercizio(
        titolo="Gli ascolti di un utente",
        scenario="",
        richiesta="""
            Trova tutte le canzoni ascoltate dall'utente con `UserID` 103. Per farlo, filtra `ascolti` in modo
            da tenere solo le righe in cui `UserID` vale 103 e salva il risultato in `ascolti_utente_103`.

            Il risultato è una sola riga, con `Song A` di `Artist X` e 4 ascolti.
        """,
        suggerimento="costruisci una maschera booleana con il confronto `==` e usala per filtrare il DataFrame.",
        starter="""
            cond = ...
            ascolti_utente_103 = ...
            ascolti_utente_103
        """,
        soluzione="""
            cond = ascolti["UserID"] == 103
            ascolti_utente_103 = ascolti[cond]
            ascolti_utente_103
        """,
        verifica="""
            assert len(ascolti_utente_103) == 1, "❌ Deve restare una sola riga"
            assert ascolti_utente_103["Song"].tolist() == ["Song A"], "❌ La canzone dell'utente 103 è Song A"
            assert ascolti_utente_103["Plays"].tolist() == [4], "❌ Gli ascolti dell'utente 103 sono 4"
        """,
    )

    nb.esercizio(
        titolo="Totale di ascolti per canzone",
        scenario="",
        richiesta="""
            Calcola il totale degli ascolti di ogni canzone, raggruppando le righe per `Song` e sommando i
            valori di `Plays`, e salva il risultato in `ascolti_per_canzone`.

            Il risultato è una Series con quattro valori: 19 per Song A, 7 per Song B, 1 per Song C e 2 per
            Song D.
        """,
        suggerimento="serve `groupby()` seguito da `sum()`.",
        starter="""
            ascolti_per_canzone = ascolti.groupby("...")["..."].sum()
            ascolti_per_canzone
        """,
        soluzione="""
            ascolti_per_canzone = ascolti.groupby("Song")["Plays"].sum()
            ascolti_per_canzone
        """,
        verifica="""
            atteso = {"Song A": 19, "Song B": 7, "Song C": 1, "Song D": 2}
            assert ascolti_per_canzone.to_dict() == atteso, "❌ Raggruppa per Song e somma Plays"
        """,
    )

    nb.esercizio(
        titolo="L'artista più ascoltato",
        scenario="",
        richiesta="""
            Identifica l'artista più ascoltato. Raggruppa le righe per `Artist`, somma `Plays` e ordina i
            totali in modo decrescente, salvando il risultato in `ascolti_per_artista`; poi salva in
            `artista_top` il nome dell'artista con il totale più alto.

            Il risultato è una Series con un totale per artista, e il primo valore, il più alto, è 19.
        """,
        suggerimento="combina `groupby()`, `sum()` e `sort_values()`, mentre `idxmax()` restituisce l'etichetta del valore massimo.",
        starter="""
            ascolti_per_artista = ascolti.groupby(...)[...].sum().sort_values(ascending=False)
            artista_top = ascolti_per_artista.idxmax()
            artista_top
        """,
        soluzione="""
            ascolti_per_artista = ascolti.groupby("Artist")["Plays"].sum().sort_values(ascending=False)
            artista_top = ascolti_per_artista.idxmax()
            artista_top
        """,
        verifica="""
            assert ascolti_per_artista.iloc[0] == 19, "❌ Il primo totale, in ordine decrescente, è 19"
            assert artista_top == "Artist X", "❌ L'artista più ascoltato è un altro"
        """,
    )

    nb.esercizio(
        titolo="Prezzo medio dell'elettricità per stato",
        facoltativo=True,
        scenario="""
            Il file `U.S. Electricity Prices.csv` contiene il prezzo medio mensile dell'elettricità negli
            Stati Uniti, in centesimi di dollaro per kWh, per stato e per settore, dal 2001 al 2024.
        """,
        richiesta="""
            1. Partendo da `prezzi`, che la cella legge dal file, tieni in `tutti_settori` solo le righe in
               cui `sectorName` vale `"all sectors"`.
            2. Calcola il prezzo medio (`price`) di ogni stato (`stateDescription`) e salvalo in
               `prezzo_medio`, usando `reset_index()` per riavere lo stato come colonna.
            3. Unisci `stati`, già definito nella cella, e `prezzo_medio` con un inner join sulla colonna
               `stateDescription`, e salva il risultato nel DataFrame `prezzi_stati`.

            Il risultato ha quattro righe, e il prezzo medio del Texas è di circa 8,86 centesimi per kWh.
        """,
        suggerimento="conviene guardare prima le colonne e i loro valori con `prezzi.head()`.",
        starter="""
            prezzi = pd.read_csv("../Dati/U.S. Electricity Prices.csv")
            stati = pd.DataFrame({
                "stateDescription": ["California", "Texas", "New York", "Florida"],
                "sigla": ["CA", "TX", "NY", "FL"],
            })

            tutti_settori = prezzi[...]
            prezzo_medio = tutti_settori.groupby(...)[...].mean().reset_index()
            prezzi_stati = pd.merge(..., ..., on=..., how="inner")
            prezzi_stati
        """,
        soluzione="""
            prezzi = pd.read_csv("../Dati/U.S. Electricity Prices.csv")
            stati = pd.DataFrame({
                "stateDescription": ["California", "Texas", "New York", "Florida"],
                "sigla": ["CA", "TX", "NY", "FL"],
            })

            tutti_settori = prezzi[prezzi["sectorName"] == "all sectors"]
            prezzo_medio = tutti_settori.groupby("stateDescription")["price"].mean().reset_index()
            prezzi_stati = pd.merge(stati, prezzo_medio, on="stateDescription", how="inner")
            prezzi_stati
        """,
        verifica="""
            assert len(prezzi_stati) == 4, "❌ Con l'inner join restano le quattro righe di stati"
            assert {"sigla", "price"} <= set(prezzi_stati.columns), "❌ Servono le colonne sigla e price"
            prezzo_tx = prezzi_stati.loc[prezzi_stati["sigla"] == "TX", "price"].iloc[0]
            assert round(prezzo_tx, 2) == 8.86, "❌ Filtra su all sectors prima della media"
        """,
        perche="""
            Oltre ai singoli stati, il file contiene righe per le regioni e per il totale nazionale, come
            `New England` e `U.S. Total`. L'inner join con `stati` tiene soltanto i quattro stati che ci
            interessano e aggiunge a ciascuno la sua sigla. Il filtro su `all sectors` va applicato prima
            della media, altrimenti la media mescolerebbe i prezzi dei singoli settori con quello complessivo.
        """,
    )

    return nb
