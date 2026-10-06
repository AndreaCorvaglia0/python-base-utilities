"""E3 · Esercitazione 3: domande ed esercizi del blocco 3 (pandas, date, Plotly) su dati veri."""

from nbkit import Cella, Notebook, box_html


def costruisci() -> Notebook:
    nb = Notebook(
        num="E3",
        file="Esercitazione_3",
        titolo="Esercitazione 3",
        blocco=3,
        giornata=2,
        intento="Domande ed esercizi su filtri, groupby, date e grafici, con i dati veri della cartella Dati.",
        obiettivi=[
            "filtrare e raggruppare i prezzi dell'elettricità per stato",
            "portare il carico Terna da quartorario a giornaliero con `resample`",
            "disegnare un istogramma con Plotly Express",
        ],
        tempo=30,
        dati=["U.S. Electricity Prices.csv", "load_total_north_hourly_2024.xlsx", "TexasTurbine.csv"],
    )

    # ------------------------------------------------------------------ domande
    nb.sezione("Domande", intro="Cinque domande brevi: rispondi in una riga, a parole o provando in una cella di codice.")
    nb.md("""
        1. Su un DataFrame con indice `0, 1, 2, 3, ...`, quante righe restituiscono `df.loc[0:2]` e `df.iloc[0:2]`? Perché?
        2. Cosa restituisce `df.groupby("Categoria")["Vendite"].sum()`? E `df.groupby("Categoria")` da solo?
        3. Cosa fa `serie.resample("D").mean()` su una serie con un valore ogni 15 minuti? Che cosa serve perché funzioni?
        4. A cosa serve `dayfirst=True` in `pd.to_datetime`? Fai l'esempio di `"01/02/2025"`.
        5. Quando serve `how="left"` in `pd.merge`, invece del valore predefinito?
    """)
    nb.celle.append(Cella("md", box_html("soluzione", """
        1. `loc` usa le etichette e include l'ultima: 3 righe. `iloc` usa le posizioni e la esclude, come le liste: 2 righe.
        2. Una Series: indice le categorie, valori le somme. `groupby` da solo dà un oggetto GroupBy, che aspetta una funzione.
        3. Raggruppa per giorno e fa la media: 96 valori quartorari diventano uno. Serve un indice di date (`set_index`).
        4. Nelle date ambigue il primo numero è il giorno: `"01/02/2025"` diventa il 1° febbraio invece del 2 gennaio.
        5. Quando vogliamo tenere tutte le righe di sinistra, anche senza corrispondenza: le colonne mancanti diventano
           `NaN`. Con il predefinito `how="inner"` quelle righe spariscono.
    """, titolo="Risposte"), solo_soluzioni=True))

    # ------------------------------------------------------------------ esercizi
    nb.sezione("Esercizi", intro="""
        Leggiamo i prezzi mensili dell'elettricità negli Stati Uniti, che serve al primo esercizio.
        Il prezzo `price` è in centesimi di dollaro per kWh; la colonna `stateDescription` contiene anche
        regioni e il totale nazionale (`U.S. Total`).
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
            1. Metti in `residenziale_2023` le righe di `prezzi` con `sectorName` uguale a `"residential"` e anno 2023.
            2. Calcola `prezzo_medio`: il prezzo medio per `stateDescription`, ordinato dal più alto al più basso.
        """,
        suggerimento="due condizioni tra parentesi unite con `&`; l'anno si legge con `.dt.year`.",
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
            Il file Terna ha un valore di carico ogni 15 minuti (MW), dal più recente al più vecchio, con quattro orari
            ripetuti il 27 ottobre per il ritorno all'ora solare.
        """,
        richiesta="""
            1. Ordina `carico` per `Date`, togli i duplicati di `Date` e metti `Date` come indice.
            2. Calcola `giornaliero`: la media giornaliera di `Total Load [MW]` per ottobre 2024.
            3. Metti in `giorno_max` il giorno con il carico medio più alto.
        """,
        suggerimento="`drop_duplicates(subset=\"Date\")`; poi `.loc[\"2024-10\", \"Total Load [MW]\"]` e `resample(\"D\")`.",
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
        scenario="Il file della turbina texana ha un valore di potenza per ogni ora dell'anno.",
        richiesta="""
            1. Disegna in `fig` l'istogramma della colonna `System power generated | (kW)` con `px.histogram`.
            2. Metti in `ore_ferme` il numero di ore in cui la potenza è 0.
        """,
        suggerimento="una maschera booleana con `== 0` e `.sum()` conta i `True`.",
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
