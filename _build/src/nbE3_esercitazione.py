"""E3 · Esercitazione 3: domande ed esercizi del blocco 3 (pandas, date, Plotly) su dati veri."""

from nbkit import Cella, Notebook, box_html


def costruisci() -> Notebook:
    nb = Notebook(
        num="E3",
        file="Esercitazione_3",
        titolo="Esercitazione 3",
        blocco=3,
        giornata=2,
        intento="Questa esercitazione propone domande ed esercizi su filtri, groupby, date e grafici, lavorando sui dati veri della cartella Dati.",
        obiettivi=[
            "filtrare e raggruppare i prezzi dell'elettricità per stato",
            "portare il carico Terna da quartorario a giornaliero con `resample`",
            "disegnare un istogramma con Plotly Express",
        ],
        tempo=20,
        dati=["U.S. Electricity Prices.csv", "load_total_north_hourly_2024.xlsx", "TexasTurbine.csv"],
    )

    # ------------------------------------------------------------------ domande
    nb.sezione("Domande", intro="""
        Le cinque domande che seguono riguardano i notebook 07-09. A ciascuna si risponde in una riga, a parole
        oppure provando il codice in una cella.
    """)
    nb.md("""
        1. Su un DataFrame con indice `0, 1, 2, 3, ...`, quante righe restituiscono `df.loc[0:2]` e `df.iloc[0:2]`? Perché?
        2. Cosa restituisce `df.groupby("Categoria")["Vendite"].sum()`? E `df.groupby("Categoria")` da solo?
        3. Cosa fa `serie.resample("D").mean()` su una serie con un valore ogni 15 minuti? Che cosa serve perché funzioni?
        4. A cosa serve `dayfirst=True` in `pd.to_datetime`? Fai l'esempio di `"01/02/2025"`.
        5. Quando serve `how="left"` in `pd.merge`, invece del valore predefinito?
    """)
    nb.celle.append(Cella("md", box_html("soluzione", """
        1. `df.loc[0:2]` restituisce 3 righe, mentre `df.iloc[0:2]` ne restituisce 2. `loc` seleziona per etichetta e
           include l'etichetta finale dell'intervallo, invece `iloc` seleziona per posizione ed esclude la posizione
           finale, come lo slicing delle liste.
        2. La prima espressione restituisce una Series che ha come indice le categorie e come valori la somma delle
           vendite di ciascuna. `df.groupby("Categoria")` da solo restituisce invece un oggetto GroupBy, che descrive i
           gruppi ma non calcola nulla finché non gli si applica una funzione di aggregazione come `sum()` o `mean()`.
        3. Raggruppa i valori per giorno e ne calcola la media, quindi i 96 valori quartorari di ogni giornata diventano
           un valore solo. Perché funzioni, la serie deve avere un indice di date, che si ottiene per esempio con
           `set_index` su una colonna già convertita con `pd.to_datetime`.
        4. Indica a pandas che nelle date ambigue il primo numero è il giorno, come si usa in Italia. Con
           `dayfirst=True` la stringa `"01/02/2025"` diventa il 1° febbraio 2025, mentre senza il parametro viene letta
           come 2 gennaio.
        5. Serve quando vogliamo conservare tutte le righe della tabella di sinistra, comprese quelle che non hanno una
           corrispondenza nell'altra tabella; per queste righe le colonne che arrivano da destra valgono `NaN`. Con il
           valore predefinito `how="inner"`, invece, le righe senza corrispondenza vengono scartate.
    """, titolo="Risposte"), solo_soluzioni=True))

    # ------------------------------------------------------------------ esercizi
    nb.sezione("Esercizi", intro="""
        La cella qui sotto importa pandas e Plotly Express e legge i prezzi mensili dell'elettricità negli Stati
        Uniti, che servono al primo esercizio. La colonna `price` è espressa in centesimi di dollaro per kWh, mentre
        `stateDescription` contiene, oltre ai singoli stati, anche alcune regioni e il totale nazionale `U.S. Total`.
    """)
    nb.code("""
        import pandas as pd
        import plotly.express as px

        prezzi = pd.read_csv("../Dati/U.S. Electricity Prices.csv")
        prezzi["date"] = pd.to_datetime(prezzi["date"])
        prezzi.head()
    """)

    nb.esercizio(
        titolo="Il prezzo residenziale per stato",
        scenario="Vogliamo sapere in quali stati l'elettricità per le famiglie è costata di più nel 2023.",
        richiesta="""
            1. Metti in `residenziale_2023` le righe di `prezzi` che hanno `sectorName` uguale a `"residential"` e una
               data del 2023.
            2. Calcola in `prezzo_medio` il prezzo medio per ogni valore di `stateDescription` e ordina il risultato
               dal prezzo più alto al più basso.
        """,
        suggerimento="le due condizioni vanno scritte ciascuna tra parentesi e unite con `&`, mentre l'anno di una colonna di date si legge con `.dt.year`.",
        starter="""
            residenziale_2023 = ...
            prezzo_medio = ...
            prezzo_medio.head()
        """,
        soluzione="""
            residenziale = prezzi["sectorName"] == "residential"
            anno_2023 = prezzi["date"].dt.year == 2023
            residenziale_2023 = prezzi[residenziale & anno_2023]

            prezzo_medio = residenziale_2023.groupby("stateDescription")["price"].mean().sort_values(ascending=False)
            prezzo_medio.head()
        """,
        verifica="""
            assert len(residenziale_2023) == 744, "❌ residenziale_2023: 62 voci per 12 mesi, 744 righe"
            assert prezzo_medio.index[0] == "Hawaii", "❌ prezzo_medio: ordina dal prezzo più alto (ascending=False)"
            assert round(prezzo_medio.iloc[0], 2) == 42.41, "❌ prezzo_medio: media di price per stato"
        """,
    )

    nb.esercizio(
        titolo="Il carico giornaliero di ottobre",
        scenario="""
            Il file Terna riporta il carico elettrico del Nord in MW, con un valore ogni 15 minuti e le righe
            ordinate dalla più recente alla più vecchia. Il 27 ottobre quattro orari compaiono due volte, perché con il ritorno all'ora
            solare l'ora dalle 2 alle 3 si ripete.
        """,
        richiesta="""
            1. Ordina `carico` per `Date`, elimina le righe con un valore di `Date` ripetuto e imposta `Date` come indice.
            2. Calcola in `giornaliero` la media giornaliera della colonna `Total Load [MW]` per il mese di ottobre 2024.
            3. Metti in `giorno_max` il giorno con il carico medio più alto.
        """,
        suggerimento="per i duplicati si usa `drop_duplicates(subset=\"Date\")`, mentre per la media si seleziona il mese con `.loc[\"2024-10\", \"Total Load [MW]\"]` e si applica `resample(\"D\")`.",
        starter="""
            carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
            carico = ...

            giornaliero = ...
            giorno_max = ...
            giorno_max
        """,
        soluzione="""
            carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
            carico = carico.sort_values("Date").drop_duplicates(subset="Date").set_index("Date")

            giornaliero = carico.loc["2024-10", "Total Load [MW]"].resample("D").mean()
            giorno_max = giornaliero.idxmax()
            giorno_max
        """,
        verifica="""
            assert len(carico) == 35132, "❌ carico: dopo drop_duplicates restano 35132 righe"
            assert len(giornaliero) == 31, "❌ giornaliero: un valore per ogni giorno di ottobre"
            assert giorno_max == pd.Timestamp("2024-10-16"), "❌ giorno_max: usa idxmax() sulla serie giornaliera"
        """,
    )

    nb.esercizio(
        titolo="L'istogramma della potenza della turbina",
        scenario="""
            Il file `TexasTurbine.csv` contiene la potenza prodotta da una turbina eolica in Texas, con un valore per
            ogni ora dell'anno. Un istogramma mostra come si distribuiscono questi valori, comprese le ore in cui la
            turbina è ferma.
        """,
        richiesta="""
            1. Disegna in `fig` l'istogramma della colonna `System power generated | (kW)` con `px.histogram`.
            2. Metti in `ore_ferme` il numero di ore in cui la potenza è 0.
        """,
        suggerimento="il confronto `== 0` sulla colonna produce una maschera booleana, e `.sum()` applicato alla maschera conta i valori `True`.",
        starter="""
            turbina = pd.read_csv("../Dati/TexasTurbine.csv")

            fig = ...
            fig.show()

            ore_ferme = ...
            ore_ferme
        """,
        soluzione="""
            turbina = pd.read_csv("../Dati/TexasTurbine.csv")

            fig = px.histogram(turbina, x="System power generated | (kW)", nbins=30,
                               title="Potenza oraria della turbina")
            fig.show()

            ore_ferme = (turbina["System power generated | (kW)"] == 0).sum()
            ore_ferme
        """,
        verifica="""
            assert fig.data[0].type == "histogram", "❌ fig: usa px.histogram"
            assert ore_ferme == 822, "❌ ore_ferme: conta le righe con potenza uguale a 0"
        """,
    )

    return nb
