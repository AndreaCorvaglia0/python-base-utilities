"""07 · Pandas: operazioni sui DataFrame."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="07",
        file="07_Pandas_operazioni",
        titolo="Pandas: operazioni sui DataFrame",
        blocco=3,
        giornata=2,
        intento="Le operazioni di tutti i giorni su un DataFrame: selezionare, pulire, trasformare, ordinare, raggruppare e unire tabelle.",
        obiettivi=[
            "selezionare righe e colonne con `loc`, `iloc`, le condizioni e `.query()`",
            "gestire valori mancanti e duplicati, creare colonne nuove e ordinare",
            "raggruppare con `groupby` e unire DataFrame con `merge` e `concat`",
        ],
        tempo={"base": 90, "avanzata": 80},
        dati=["U.S. Electricity Prices.csv"],
    )

    nb.md("""
        Importiamo le librerie e ricreiamo il DataFrame del notebook precedente: tre persone con nome,
        età e città, e un indice con etichette.
    """)
    nb.code("""
        import numpy as np
        import pandas as pd
    """)
    nb.code("""
        # creare un DataFrame da un dizionario
        data = {
            "Nome": ["Alice", "Bob", "Charlie"],
            "Età": [24, 27, 22],
            "Città": ["Roma", "Milano", "Torino"],
        }
        df = pd.DataFrame(data, index=["id_1", "id_2", "id_3"])
        df
    """)

    # ------------------------------------------------------------------ 1
    nb.sezione("Selezione dei dati", intro="""
        In pandas possiamo selezionare i dati per nome di colonna, per etichetta dell'indice o per
        posizione.
    """)
    nb.sottosezione("Selezione di righe e colonne", intro="""
        Possiamo selezionare una o più colonne di un DataFrame usando il nome della colonna come chiave.
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
        Con `loc` e `iloc` selezioniamo righe specifiche in base all'indice o alla posizione.
    """)
    nb.code("""
        # loc: in base all'indice
        df.loc["id_1":"id_2", ["Età"]]
    """)
    nb.code("""
        # iloc: in base alla posizione
        df.iloc[0:2, [1]]
    """)

    nb.sottosezione("Differenze tra loc e iloc", intro="""
        - `loc`: seleziona i dati in base alle etichette (indice).
        - `iloc`: seleziona i dati in base alla posizione intera (indice numerico).

        Esempio con `loc`:
    """)
    nb.code("""
        df.loc["id_2":, ["Nome", "Età"]]
    """)
    nb.md("""
        Esempio con `iloc`:
    """)
    nb.code("""
        df.iloc[1:3, :2]
    """)
    nb.md("""
        `loc` permette una selezione più intuitiva quando si conoscono le etichette; con `loc` lo
        slicing include anche l'ultima etichetta, con `iloc` l'ultima posizione resta esclusa.
    """)

    nb.sottosezione("Selezione condizionale", intro="""
        Possiamo filtrare i dati con condizioni booleane. La condizione da sola restituisce una Series
        di `True` e `False`, una per riga.
    """)
    nb.code("""
        df["Età"] > 23
    """)
    nb.md("""
        Messa tra parentesi quadre, la condizione tiene solo le righe con `True`.
    """)
    nb.code("""
        df[df["Età"] > 23]
    """)
    nb.md("""
        Più condizioni si combinano con `&` (e), `|` (o) e `~` (non), ognuna tra parentesi tonde.
    """)
    nb.code("""
        condiz_eta = (df["Età"] > 23) & (df["Età"] < 26)
        condiz_eta
    """)
    nb.code("""
        # righe con età tra 23 e 26 (esclusi), solo la colonna Nome
        df.loc[(df["Età"] > 23) & (df["Età"] < 26), ["Nome"]]
    """)
    nb.md("""
        Queste Series di `True` e `False` si chiamano maschere booleane: sono il modo standard per
        filtrare i dati in pandas.
    """)

    nb.sottosezione("Il metodo query", intro="""
        Il metodo `.query()` filtra le righe con una condizione scritta come testo, ed è comodo da
        leggere quando le condizioni sono più di una. La sintassi di base è `df.query("condizione")`.
    """)
    nb.code("""
        cols = ["Età", "Nome"]
        df.query("Età > 23 and Età < 26").loc[:, cols]
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Manipolazione dei dati", intro="""
        La manipolazione dei dati in pandas comprende la gestione dei valori mancanti, la pulizia dei
        dati e la trasformazione.
    """)
    nb.sottosezione("Valori mancanti", intro="""
        I valori mancanti possono causare problemi nelle analisi e vanno gestiti. Ne esistono di tre tipi:

        - `NaN` (Not a Number): usato per i valori mancanti numerici (`np.nan` di NumPy).
        - `None`: l'oggetto Python che rappresenta l'assenza di valore.
        - `pd.NA`: rappresenta i valori mancanti in pandas per i tipi estesi.
    """)
    nb.code("""
        # creare un DataFrame con valori mancanti
        data_nan = {
            "A": [1, 2, np.nan],
            "B": [4, None, 6],
            "C": [7, 8, np.nan],
        }
        df_nan = pd.DataFrame(data_nan)
        df_nan
    """)
    nb.md("""
        `isnull()` (e il suo opposto `notnull()`) dice per ogni cella se il valore manca. Con `.sum()`
        contiamo i mancanti per colonna.
    """)
    nb.code("""
        # identificare i valori mancanti
        df_nan.isnull().sum()
    """)
    nb.md("""
        Una colonna di interi con un `NaN` diventa di tipo `float64`. Anche `info()` mostra quanti
        valori non mancanti ha ogni colonna.
    """)
    nb.code("""
        df_nan["A"].dtype  # Output: dtype('float64')
    """)
    nb.code("""
        df_nan.info()
    """)
    nb.md("""
        Per risolvere i valori mancanti abbiamo tre strade:

        - **Riempimento**: `fillna()` sostituisce i valori mancanti con un valore specificato.
        - **Rimozione**: `dropna()` elimina le righe o le colonne con valori mancanti.
        - **Interpolazione**: stima i valori mancanti basandosi sui dati esistenti.
    """)
    nb.code("""
        df_nan["A"].fillna(df_nan["A"].median())
    """)
    nb.code("""
        # riempire i valori mancanti con zero
        df_nan_filled = df_nan.fillna(0)
        df_nan_filled
    """)
    nb.md("""
        `fillna` restituisce una copia: per modificare la colonna la riassegniamo.
    """)
    nb.code("""
        df_nan["A"] = df_nan["A"].fillna(df_nan["A"].median())
        df_nan.dropna()
    """)
    nb.md("""
        - **Quando rimuovere**: se i dati mancanti sono pochi e la rimozione non influisce sull'analisi.
        - **Quando riempire**: se i dati mancanti sono molti e c'è un valore appropriato per sostituirli.
    """)

    nb.sottosezione("Duplicati", intro="""
        I duplicati possono distorcere i risultati delle analisi e vanno identificati e gestiti.
    """)
    nb.code("""
        # creare un DataFrame con duplicati
        data_dup = {
            "Nome": ["Alice", "Bob", "Alice"],
            "Età": [24, 27, 24],
            "Città": ["Roma", "Milano", "Roma"],
        }
        df_dup = pd.DataFrame(data_dup)
        df_dup
    """)
    nb.code("""
        # identificare i duplicati
        df_dup.duplicated()
    """)
    nb.code("""
        # rimuovere i duplicati
        df_dup_clean = df_dup.drop_duplicates()
        df_dup_clean
    """)

    nb.sottosezione("Trasformazione", intro="""
        Possiamo aggiungere, modificare o eliminare colonne in un DataFrame per adattarlo alle nostre
        esigenze. Una colonna nuova si crea assegnando un'espressione a un nome che non esiste ancora.
    """)
    nb.code("""
        df["Anni alla pensione"] = 70 - df["Età"]
        df
    """)
    nb.md("""
        Con `.loc` e una condizione modifichiamo solo le righe che la rispettano: qui chi ha meno di 25
        anni ha il 30% di anni in più alla pensione, gli altri restano uguali.
    """)
    nb.code("""
        cond_riforma = df["Età"] < 25
    """)
    nb.code("""
        df.loc[cond_riforma, "Anni alla pensione riforma"] = df.loc[cond_riforma, "Anni alla pensione"] * 1.3
        df.loc[~cond_riforma, "Anni alla pensione riforma"] = df.loc[~cond_riforma, "Anni alla pensione"]
        df
    """)
    nb.box("attenzione", """
        `df[cond]["col"] = valore` non modifica `df`: scrive su una copia, e pandas 3 avvisa con
        `ChainedAssignmentError`. Per cambiare le righe filtrate si usa sempre `df.loc[cond, "col"] = valore`.
    """)
    nb.md("""
        Quando la colonna nuova non viene da un conto, `.map` traduce ogni valore con un dizionario e
        `.apply` applica una funzione a ogni valore.
    """)
    nb.code("""
        regioni = {"Roma": "Lazio", "Milano": "Lombardia", "Torino": "Piemonte"}
        df["Regione"] = df["Città"].map(regioni)
        df
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

    nb.sottosezione("Gestione degli indici", intro="""
        Gli indici permettono di accedere ai dati per etichetta e di allineare e unire tabelle diverse.
        `set_index()` trasforma una o più colonne in indice, `reset_index()` fa il contrario.
    """)
    nb.code("""
        # impostare due colonne come indice
        df_indexed = df.set_index(["Nome", "Città"])
        df_indexed.loc[("Alice", "Roma")]
    """)
    nb.code("""
        # resettare l'indice
        df_reset = df_indexed.reset_index()
        df_reset
    """)
    nb.md("""
        Dopo un ordinamento con `sort_values` (lo vediamo tra poco) le righe tengono l'indice di prima,
        in disordine. `reset_index(drop=True)` lo fa ripartire da 0 e scarta il vecchio invece di
        trasformarlo in una colonna.
    """)
    nb.code("""
        df.sort_values("Età").reset_index(drop=True)
    """)

    nb.sottosezione("Rinomina delle colonne", intro="""
        Possiamo rinominare le colonne con `rename` e un dizionario da nome vecchio a nome nuovo.
    """)
    nb.code("""
        df_renamed = df.rename(columns={"Città": "Residenza", "Età": "age"})
        df_renamed
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Ordinamento dei dati", intro="""
        L'ordinamento serve sia nell'analisi sia nella presentazione dei risultati.
    """)
    nb.sottosezione("sort_values e sort_index", intro="""
        `sort_values()` ordina i dati in base ai valori di una o più colonne; `ascending=False` ordina
        dal più grande.
    """)
    nb.code("""
        # ordinare per età
        df_sorted = df.sort_values(by="Età", ascending=False)
        df_sorted
    """)
    nb.md("""
        `sort_index()` ordina in base all'indice: è utile quando l'indice ha un significato. Qui
        prendiamo metà delle righe in ordine casuale con `sample` e le rimettiamo in ordine.
    """)
    nb.code("""
        df_shuffled = df.sample(frac=0.5)
        df_shuffled.sort_index()
    """)
    nb.sottosezione("Ordinamento su più colonne", intro="""
        Possiamo ordinare usando più colonne come chiavi: a pari valore della prima decide la seconda.
        `ascending` accetta una lista, un valore per colonna.
    """)
    nb.code("""
        # ordinare per età e poi per nome
        df_multi_sorted = df.sort_values(by=["Età", "Nome"], ascending=[False, True])
        df_multi_sorted
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Groupby", intro="""
        Il metodo `groupby()` **suddivide** un DataFrame in gruppi in base a una o più colonne, per poi
        applicare un'**aggregazione** ai dati di ciascun gruppo. È la logica **Split-Apply-Combine**:

        1. **Split**: dividere i dati in gruppi in base a una o più colonne.
        2. **Apply**: applicare una funzione (somma, media, conteggio) a ogni gruppo.
        3. **Combine**: unire i risultati in un nuovo oggetto pandas (Series o DataFrame).

        La forma è `df.groupby("colonna_di_raggruppamento")["colonna"].funzione()`.
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
        `groupby()` da solo restituisce un oggetto GroupBy, che aspetta una funzione per elaborare i
        gruppi. Con `sum()` otteniamo una riga per gruppo, con la categoria nell'indice.
    """)
    nb.sottosezione("Aggregazione multipla", intro="""
        Con `.agg()` calcoliamo più statistiche in una volta sola.
    """)
    nb.code("""
        vendite.groupby("Categoria").agg({"Vendite": ["sum", "mean", "count"]})["Vendite"]
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Unione e concatenazione di DataFrame", intro="""
        Pandas offre diversi modi per combinare più DataFrame.
    """)
    nb.sottosezione("Merge", intro="""
        `merge()` combina DataFrame in base a chiavi comuni, come un join in SQL. Tipi di join:

        - **Inner join**: le righe con chiavi presenti in entrambi i DataFrame.
        - **Left join**: tutte le righe del DataFrame di sinistra e quelle corrispondenti di destra.
        - **Right join**: tutte le righe del DataFrame di destra e quelle corrispondenti di sinistra.
        - **Outer join**: tutte le righe, che abbiano una corrispondenza o no.
    """)
    nb.code("""
        # DataFrame di esempio
        df_left = pd.DataFrame({"ID": [1, 2, 3], "Nome": ["Alice", "Bob", "Charlie"]})
        df_right = pd.DataFrame({"ID": [3, 4, 5], "Età": [35, 40, 45]})

        # inner join
        df_inner = pd.merge(df_left, df_right, on="ID", how="inner")
        df_inner
    """)
    nb.code("""
        # outer join
        df_outer = pd.merge(df_left, df_right, on="ID", how="outer")
        df_outer
    """)
    nb.md("""
        Il left join è il più usato per aggiungere informazioni a una tabella senza perdere righe:
        dove manca la corrispondenza resta `NaN`.
    """)
    nb.code("""
        # left join
        pd.merge(df_left, df_right, on="ID", how="left")
    """)
    nb.sottosezione("Concatenazione", intro="""
        `concat()` unisce DataFrame verticalmente (aggiunge righe) o orizzontalmente (aggiunge colonne).
    """)
    nb.code("""
        # concatenazione verticale
        df_concat_vertical = pd.concat([df_left, df_right], ignore_index=True, sort=False)
        df_concat_vertical
    """)
    nb.code("""
        # concatenazione orizzontale
        df_concat_horizontal = pd.concat([df_left, df_right], axis=1)
        df_concat_horizontal
    """)
    nb.sottosezione("Differenze tra merge e concat", intro="""
        - **Merge**: quando vogliamo combinare DataFrame su una o più chiavi comuni.
        - **Concat**: quando vogliamo unire DataFrame che hanno le stesse colonne o lo stesso indice.
    """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Esercizi", intro="""
        Lavori come data analyst per un'azienda che gestisce una piattaforma di streaming musicale.
        Il dataset con gli ascolti degli utenti è questo: eseguilo prima dei primi tre esercizi.
    """)
    nb.code("""
        # DataFrame degli ascolti
        listens_data = {
            "UserID": [101, 102, 103, 104, 105, 106],
            "Song": ["Song A", "Song B", "Song A", "Song C", "Song B", "Song D"],
            "Artist": ["Artist X", "Artist Y", "Artist X", "Artist Z", "Artist Y", "Artist W"],
            "Plays": [15, 2, 4, 1, 5, 2],
        }
        listens = pd.DataFrame(listens_data)
        listens
    """)

    nb.esercizio(
        titolo="Gli ascolti di un utente",
        scenario="",
        richiesta="""
            Trova tutte le canzoni ascoltate dall'utente con `UserID` 103: filtra `listens` per tenere
            solo le righe dove `UserID` è 103 e salva il risultato in `user_103_listens`.

            Output atteso: una riga, `Song A` di `Artist X` con 4 ascolti.
        """,
        suggerimento="usa il filtraggio condizionale con una maschera booleana.",
        starter="""
            cond = ...
            user_103_listens = ...
            user_103_listens
        """,
        soluzione="""
            cond = listens["UserID"] == 103
            user_103_listens = listens[cond]
            user_103_listens
        """,
        verifica="""
            assert len(user_103_listens) == 1, "❌ Deve restare una sola riga"
            assert user_103_listens["Song"].tolist() == ["Song A"], "❌ La canzone dell'utente 103 è Song A"
            assert user_103_listens["Plays"].tolist() == [4], "❌ Gli ascolti dell'utente 103 sono 4"
        """,
    )

    nb.esercizio(
        titolo="Totale di ascolti per canzone",
        scenario="",
        richiesta="""
            Calcola il totale di ascolti per ogni canzone: raggruppa per `Song` e somma i valori di
            `Plays`. Salva il risultato in `total_plays_per_song`.

            Output atteso: Song A 19, Song B 7, Song C 1, Song D 2.
        """,
        suggerimento="usa `groupby()` seguito da `sum()`.",
        starter="""
            total_plays_per_song = listens.groupby("...")["..."].sum()
            total_plays_per_song
        """,
        soluzione="""
            total_plays_per_song = listens.groupby("Song")["Plays"].sum()
            total_plays_per_song
        """,
        verifica="""
            expected = {"Song A": 19, "Song B": 7, "Song C": 1, "Song D": 2}
            assert total_plays_per_song.to_dict() == expected, "❌ Raggruppa per Song e somma Plays"
        """,
    )

    nb.esercizio(
        titolo="L'artista più ascoltato",
        scenario="",
        richiesta="""
            Identifica l'artista più popolare: raggruppa per `Artist`, somma `Plays` e ordina in modo
            decrescente (`artist_popularity`). Poi salva in `top_artist` il nome dell'artista con il
            totale di ascolti più alto.
        """,
        suggerimento="combina `groupby()`, `sum()` e `sort_values()`; `idxmax()` restituisce l'etichetta del valore massimo.",
        starter="""
            artist_popularity = listens.groupby(...)[...].sum().sort_values(ascending=False)
            top_artist = artist_popularity.idxmax()
            top_artist
        """,
        soluzione="""
            artist_popularity = listens.groupby("Artist")["Plays"].sum().sort_values(ascending=False)
            top_artist = artist_popularity.idxmax()
            top_artist
        """,
        verifica="""
            assert artist_popularity.iloc[0] == 19, "❌ Il primo totale, in ordine decrescente, è 19"
            assert top_artist == "Artist X", "❌ L'artista più ascoltato è un altro"
        """,
    )

    nb.esercizio(
        titolo="Prezzo medio dell'elettricità per stato",
        facoltativo=True,
        scenario="""
            Il file `U.S. Electricity Prices.csv` contiene il prezzo medio mensile dell'elettricità negli
            Stati Uniti (in centesimi di dollaro per kWh), per stato e per settore, dal 2001 al 2024.
        """,
        richiesta="""
            1. Leggi il file in `prezzi` e tieni solo le righe con `sectorName` uguale a `"all sectors"`.
            2. Calcola il prezzo medio (`price`) per stato (`stateDescription`) in `prezzo_medio`,
               con `reset_index()` per riavere lo stato come colonna.
            3. Unisci `stati` (già definito nella cella) e `prezzo_medio` con un inner join sulla
               colonna `stateDescription`, nel DataFrame `prezzi_stati`.

            Output atteso: quattro righe; il Texas ha un prezzo medio di circa 8,86.
        """,
        suggerimento="guarda prima le colonne con `prezzi.head()`.",
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
            assert len(prezzi_stati) == 4, "❌ Con l'inner join restano i quattro stati di stati"
            assert {"sigla", "price"} <= set(prezzi_stati.columns), "❌ Servono le colonne sigla e price"
            prezzo_tx = prezzi_stati.loc[prezzi_stati["sigla"] == "TX", "price"].iloc[0]
            assert round(prezzo_tx, 2) == 8.86, "❌ Filtra su all sectors prima della media"
        """,
        perche="""
            Il file contiene anche regioni e il totale nazionale (`New England`, `U.S. Total`): l'inner
            join con `stati` tiene solo gli stati che ci interessano, con la loro sigla.
        """,
    )

    return nb
