"""09 · Plotly per serie storiche."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="09",
        file="09_Plotly",
        titolo="Plotly per serie storiche",
        blocco=3,
        giornata=2,
        intento="Plotly produce grafici interattivi: per una serie storica permette zoom, selezione di intervalli e confronto tra serie.",
        obiettivi=[
            "fare grafici a linee, istogrammi e scatter con Plotly Express",
            "confrontare più serie nello stesso grafico, partendo da dati wide-form",
            "riconoscere dati, mapping, tracce e layout di una figura",
        ],
        tempo={"base": 30, "avanzata": 25},
        dati=["load_total_north_hourly_2024.xlsx", "TexasTurbine.csv"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Setup minimo", intro="""
        Restiamo sul minimo che serve nella pratica: `plotly.express`. Documentazione ufficiale:
        [Plotly Express](https://plotly.com/python/plotly-express/),
        [Line charts](https://plotly.com/python/line-charts/),
        [Time series](https://plotly.com/python/time-series/).
    """)
    nb.code("""
        import pandas as pd
        import plotly.express as px
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("I quattro elementi chiave", intro="""
        Plotly diventa molto più leggibile se separi sempre quattro pezzi.

        1. **Dati**: un DataFrame con una colonna tempo (`datetime`) ordinata.
        2. **Mapping**: quali colonne finiscono su `x`, `y` (e, quando serve, `color`).
        3. **Tracce**: una `Figure` è fatta di una o più tracce (`fig.data`). In una serie storica la traccia
           tipica è uno `Scatter` con `mode="lines"`.
        4. **Layout e controlli**: titolo, assi, hover… si modificano con `fig.update_layout(...)`
           e `fig.update_xaxes(...)`.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Il dataset stocks", intro="""
        `px.data.stocks()`, già incluso in Plotly, è un dataset
        [wide-form](https://plotly.com/python/wide-form/): una colonna tempo (`date`) e una colonna per
        ciascuna serie. I valori sono **indicizzati** (partono da 1): è comodo per confrontare andamenti relativi.
    """)
    nb.code("""
        df = px.data.stocks().copy()
        df["date"] = pd.to_datetime(df["date"])
        df.head()
    """)
    nb.box("nota", """
        Se `date` non è `datetime` o non è ordinata, la linea può produrre risultati confusi (salti avanti
        e indietro).
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Primo grafico con Plotly Express", intro="""
        Il primo obiettivo è avere una linea leggibile con un mapping esplicito (`x` e `y`).
    """)
    nb.code("""
        azienda = "GOOG"

        fig = px.line(
            df,
            x="date",
            y=azienda,
            title=f"{azienda} (indicizzato)"
        )
        fig.show()
    """)
    nb.prova_tu(
        richiesta="""
            Cambia `azienda` con un'altra colonna del dataset (`AAPL`, `AMZN`, `MSFT`…). Poi limita il grafico
            agli ultimi 12 mesi filtrando `df` prima di passarlo a `px.line`: il dataset finisce a fine 2019,
            quindi bastano le date dal `2019-01-01`. Il grafico atteso parte da gennaio 2019.
        """,
        starter="""
            azienda = ...
            mask_12_mesi = ...
            fig_12_mesi = px.line(...)
            fig_12_mesi.show()
        """,
        soluzione="""
            azienda = "AAPL"
            mask_12_mesi = df["date"] >= "2019-01-01"
            fig_12_mesi = px.line(df[mask_12_mesi], x="date", y=azienda, title=f"{azienda} (indicizzato), ultimi 12 mesi")
            fig_12_mesi.show()
        """,
    )
    with nb.solo("avanzata"):
        nb.md("""
            La media mobile si calcola con `rolling` come nuova colonna e si disegna accanto alla serie
            originale, passando le due colonne a `y`. Il dataset ha un valore a settimana.
        """)
        nb.code("""
            azienda = "GOOG"
            finestra_mobile = 4

            # media mobile come nuova colonna di un nuovo DataFrame
            df_mobile = df[["date", azienda]].copy()
            df_mobile[f"{azienda}_rolling"] = df_mobile[azienda].rolling(finestra_mobile).mean()
            # attenzione ai valori mancanti all'inizio della serie: qui li togliamo
            df_mobile = df_mobile.dropna().reset_index(drop=True)
            fig = px.line(
                df_mobile,
                x="date",
                y=[azienda, f"{azienda}_rolling"],
                title=f"{azienda} con media mobile a {finestra_mobile} settimane"
            )
            fig.show()
        """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Confronto tra serie (wide-form)", intro="""
        Con i dati wide-form puoi passare direttamente una lista di colonne a `y`. È il caso che torna più
        spesso: una tabella con molte serie già allineate nel tempo.
    """)
    nb.code("""
        aziende = ["AAPL", "AMZN", "MSFT"]

        fig = px.line(
            df,
            x="date",
            y=aziende,
            title="Confronto tra serie (wide-form)"
        )
        fig.show()
    """)
    nb.prova_tu(
        richiesta="""
            Aggiungi o rimuovi una società dalla lista `aziende`. Poi crea `df_indicizzato`, una copia di `df`
            con le serie riportate a base 100 alla prima data (`valore / valore.iloc[0] * 100`), e ripeti il
            grafico. Tutte le linee devono partire da 100.
        """,
        starter="""
            aziende = ["AAPL", "AMZN", "MSFT", ...]
            df_indicizzato = df.copy()
            df_indicizzato[aziende] = ...
            fig_100 = px.line(...)
            fig_100.show()
        """,
        soluzione="""
            aziende = ["AAPL", "AMZN", "MSFT", "NFLX"]
            df_indicizzato = df.copy()
            df_indicizzato[aziende] = df[aziende] / df[aziende].iloc[0] * 100
            fig_100 = px.line(df_indicizzato, x="date", y=aziende, title="Confronto tra serie (base 100)")
            fig_100.show()
        """,
    )

    # ------------------------------------------------------------------ 6
    nb.sezione("Istogramma e scatter", intro="""
        Plotly Express ha una funzione per ogni tipo di grafico, con gli stessi argomenti di `px.line`. Le
        proviamo sui dati orari della turbina eolica texana, con due colonne rinominate per comodità.
    """)
    nb.code("""
        turbina = pd.read_csv("../Dati/TexasTurbine.csv")
        # il timestamp non ha l'anno: lo aggiungiamo noi
        turbina["timestamp"] = pd.to_datetime("2023 " + turbina["Time stamp"], format="%Y %b %d, %I:%M %p")
        turbina = turbina.rename(columns={"System power generated | (kW)": "potenza_kw", "Wind speed | (m/s)": "vento_ms"})
        turbina.head(3)
    """)
    nb.md("""
        L'istogramma conta quante ore cadono in ogni intervallo di velocità del vento: basta la `x`, e
        `nbins` è il numero di barre.
    """)
    nb.code("""
        fig = px.histogram(turbina, x="vento_ms", nbins=30, title="Distribuzione del vento")
        fig.show()
    """)
    nb.md("""
        Lo scatter disegna un punto per riga e mostra la relazione tra due colonne: vento sulla x, potenza
        sulla y. Ne esce la curva di potenza della turbina; `opacity` fa vedere dove i punti si accumulano.
    """)
    nb.code("""
        fig = px.scatter(turbina, x="vento_ms", y="potenza_kw", opacity=0.3, title="Vento e potenza")
        fig.show()
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Un mese di carico",
        scenario="""
            Il file di Terna ha il carico del Nord del 2024, un valore ogni quarto d'ora. Vogliamo guardare
            gennaio da vicino.
        """,
        richiesta="""
            1. Da `carico` tieni il solo gennaio 2024 in `gennaio`.
            2. Costruisci `fig_carico` con `px.line`: `Total Load [MW]` sulla `Date`, titolo `Carico Nord, gennaio 2024`.

            Output atteso: una linea sola.
        """,
        starter="""
            carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
            carico = carico.sort_values("Date")

            mask_gennaio = ...
            gennaio = carico[mask_gennaio]

            fig_carico = px.line(...)
            fig_carico.show()
        """,
        soluzione="""
            carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
            carico = carico.sort_values("Date")

            mask_gennaio = carico["Date"].dt.month == 1
            gennaio = carico[mask_gennaio]

            fig_carico = px.line(gennaio, x="Date", y="Total Load [MW]", title="Carico Nord, gennaio 2024")
            fig_carico.show()
        """,
        verifica="""
            assert len(fig_carico.data) == 1 and fig_carico.data[0].mode == "lines", "❌ Serve una linea sola: px.line con y='Total Load [MW]'"
            assert fig_carico.layout.title.text == "Carico Nord, gennaio 2024", "❌ Il titolo deve essere 'Carico Nord, gennaio 2024'"
        """,
    )
    nb.esercizio(
        titolo="La distribuzione della potenza",
        scenario="""
            Quante ore la turbina texana produce poco, e quante lavora vicino ai 3000 kW?
        """,
        richiesta="""
            Costruisci in `fig_potenza` l'istogramma della colonna `potenza_kw` di `turbina`, con 30 barre e
            titolo `Distribuzione della potenza`. Output atteso: la barra più alta è quella vicino a 0 kW.
        """,
        starter="""
            fig_potenza = px.histogram(...)
            fig_potenza.show()
        """,
        soluzione="""
            fig_potenza = px.histogram(turbina, x="potenza_kw", nbins=30, title="Distribuzione della potenza")
            fig_potenza.show()
        """,
        verifica="""
            assert len(fig_potenza.data) == 1 and fig_potenza.data[0].type == "histogram", "❌ Serve un solo istogramma: px.histogram, senza color"
            assert fig_potenza.layout.title.text == "Distribuzione della potenza", "❌ Il titolo deve essere 'Distribuzione della potenza'"
        """,
    )
    return nb
