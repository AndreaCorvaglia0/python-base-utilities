"""09 · Plotly per serie storiche."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="09",
        file="09_Plotly",
        titolo="Plotly per serie storiche",
        blocco=3,
        giornata=2,
        intento="Plotly fa grafici interattivi: per una serie storica vuol dire zoom, intervalli e confronto tra serie senza riscrivere codice.",
        obiettivi=[
            "fare grafici a linee, istogrammi e scatter con Plotly Express",
            "confrontare più serie e navigarle con range slider e range selector",
            "esportare un grafico interattivo in HTML",
        ],
        tempo={"base": 40, "avanzata": 35},
        dati=["load_total_north_hourly_2024.xlsx", "TexasTurbine.csv"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Setup minimo", intro="""
        Restiamo sul minimo che serve nella pratica: `plotly.express` per partire, poi un salto a
        `graph_objects` per il range slider e il range selector. Documentazione ufficiale:
        [Plotly Express](https://plotly.com/python/plotly-express/),
        [Line charts](https://plotly.com/python/line-charts/),
        [Time series](https://plotly.com/python/time-series/).
    """)
    nb.code("""
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("I quattro elementi chiave", intro="""
        Plotly diventa molto più leggibile se separi sempre quattro pezzi.

        1. **Dati**: un DataFrame con una colonna tempo (`datetime`) ordinata.
        2. **Mapping**: quali colonne finiscono su `x`, `y` (e, quando serve, `color`).
        3. **Tracce**: una `Figure` è fatta di una o più tracce (`fig.data`). In una serie storica la traccia
           tipica è `go.Scatter` con `mode="lines"`.
        4. **Layout e controlli**: titolo, assi, hover, range slider… si modificano con `fig.update_layout(...)`
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
        company = "GOOG"

        fig = px.line(
            df,
            x="date",
            y=company,
            title=f"{company} (indicizzato)"
        )
        fig.show()
    """)
    nb.prova_tu(
        richiesta="""
            Cambia `company` con un'altra colonna del dataset (`AAPL`, `AMZN`, `MSFT`…). Poi limita il grafico
            agli ultimi 12 mesi filtrando `df` prima di passarlo a `px.line`: il dataset finisce a fine 2019,
            quindi bastano le date dal `2019-01-01`. Il grafico atteso parte da gennaio 2019.
        """,
        starter="""
            company = ...
            mask_12_mesi = ...
            fig_12_mesi = px.line(...)
            fig_12_mesi.show()
        """,
        soluzione="""
            company = "AAPL"
            mask_12_mesi = df["date"] >= "2019-01-01"
            fig_12_mesi = px.line(df[mask_12_mesi], x="date", y=company, title=f"{company} (indicizzato), ultimi 12 mesi")
            fig_12_mesi.show()
        """,
    )
    with nb.solo("avanzata"):
        nb.md("""
            La media mobile si calcola con `rolling` come nuova colonna e si disegna accanto alla serie
            originale, passando le due colonne a `y`. Il dataset ha un valore a settimana.
        """)
        nb.code("""
            company = "GOOG"
            rolling_window = 4

            # media mobile come nuova colonna di un nuovo DataFrame
            df_rolling = df[["date", company]].copy()
            df_rolling[f"{company}_rolling"] = df_rolling[company].rolling(rolling_window).mean()
            # attenzione ai valori mancanti all'inizio della serie: qui li togliamo
            df_rolling = df_rolling.dropna().reset_index(drop=True)
            fig = px.line(
                df_rolling,
                x="date",
                y=[company, f"{company}_rolling"],
                title=f"{company} con media mobile a {rolling_window} settimane"
            )
            fig.show()
        """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Confronto tra serie (wide-form)", intro="""
        Con i dati wide-form puoi passare direttamente una lista di colonne a `y`. È il caso che torna più
        spesso: una tabella con molte serie già allineate nel tempo.
    """)
    nb.code("""
        companies = ["AAPL", "AMZN", "MSFT"]

        fig = px.line(
            df,
            x="date",
            y=companies,
            title="Confronto tra serie (wide-form)"
        )
        fig.show()
    """)
    nb.prova_tu(
        richiesta="""
            Aggiungi o rimuovi una società dalla lista `companies`. Poi crea `df_indexed`, una copia di `df`
            con le serie riportate a base 100 alla prima data (`valore / valore.iloc[0] * 100`), e ripeti il
            grafico. Tutte le linee devono partire da 100.
        """,
        starter="""
            companies = ["AAPL", "AMZN", "MSFT", ...]
            df_indexed = df.copy()
            df_indexed[companies] = ...
            fig_100 = px.line(...)
            fig_100.show()
        """,
        soluzione="""
            companies = ["AAPL", "AMZN", "MSFT", "NFLX"]
            df_indexed = df.copy()
            df_indexed[companies] = df[companies] / df[companies].iloc[0] * 100
            fig_100 = px.line(df_indexed, x="date", y=companies, title="Confronto tra serie (base 100)")
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

    # ------------------------------------------------------------------ 7
    nb.sezione("Range slider e range selector", intro="""
        Qui si passa a `graph_objects` per usare il **range slider** e il **range selector** sull'asse x,
        utili per navigare serie storiche lunghe. Il codice segue lo schema degli
        [esempi ufficiali](https://plotly.com/python/range-slider/): si costruiscono le tracce, poi si
        aggiunge il controllo nel `layout`.
    """)
    nb.code("""
        companies = ["AAPL", "AMZN", "MSFT"]

        fig = go.Figure()
        for c in companies:
            fig.add_trace(go.Scatter(x=list(df["date"]), y=list(df[c]), name=c))
    """)
    nb.md("""
        Il range selector offre pulsanti predefiniti (1m, 6m, 1y, all) per saltare a intervalli comuni. Lo
        slider in basso permette di selezionare un intervallo qualsiasi.
    """)
    nb.code("""
        bottoni = [
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all"),
        ]
    """)
    nb.code("""
        # range slider + range selector (schema ufficiale)
        fig.update_layout(
            title_text="Stocks (indicizzato), range slider",
            height=400,
            width=700,
            xaxis=dict(
                rangeselector=dict(buttons=bottoni, bgcolor="lightgray", font=dict(size=10)),
                rangeslider=dict(visible=True),
                type="date",
            ),
            margin=dict(t=80, b=80),
        )
        fig.show()
    """)

    # ------------------------------------------------------------------ 8
    nb.sezione("Esportare in HTML", intro="""
        Per condividere il grafico interattivo senza Jupyter, l'export in HTML è la strada più semplice
        ([documentazione](https://plotly.com/python/interactive-html-export/)).
    """)
    nb.code("""
        # salva l'ultima figura (fig) in HTML, nella cartella del notebook: si apre con un browser
        # con include_plotlyjs="cdn" la libreria Plotly si scarica all'apertura: file leggero, ma serve la rete
        fig.write_html("plot_time_series.html", include_plotlyjs="cdn")
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Un mese di carico con il range slider",
        scenario="""
            Il file di Terna ha il carico del Nord del 2024, un valore ogni quarto d'ora. Vogliamo guardare
            gennaio da vicino.
        """,
        richiesta="""
            1. Da `carico` tieni il solo gennaio 2024 in `gennaio`.
            2. Costruisci `fig_carico` con `px.line`: `Total Load [MW]` sulla `Date`, titolo `Carico Nord, gennaio 2024`.
            3. Accendi il range slider sotto l'asse x.

            Output atteso: una linea sola, con lo slider sotto il grafico.
        """,
        suggerimento="su una figura di `px` lo slider si accende con `fig_carico.update_xaxes(rangeslider_visible=True)`.",
        starter="""
            carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
            carico = carico.sort_values("Date")

            mask_gennaio = ...
            gennaio = carico[mask_gennaio]

            fig_carico = px.line(...)
            fig_carico.update_xaxes(...)
            fig_carico.show()
        """,
        soluzione="""
            carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
            carico = carico.sort_values("Date")

            mask_gennaio = carico["Date"].dt.month == 1
            gennaio = carico[mask_gennaio]

            fig_carico = px.line(gennaio, x="Date", y="Total Load [MW]", title="Carico Nord, gennaio 2024")
            fig_carico.update_xaxes(rangeslider_visible=True)
            fig_carico.show()
        """,
        verifica="""
            assert len(fig_carico.data) == 1 and fig_carico.data[0].mode == "lines", "❌ Serve una linea sola: px.line con y='Total Load [MW]'"
            assert fig_carico.layout.title.text == "Carico Nord, gennaio 2024", "❌ Il titolo deve essere 'Carico Nord, gennaio 2024'"
            assert fig_carico.layout.xaxis.rangeslider.visible, "❌ Manca il range slider: update_xaxes(rangeslider_visible=True)"
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
    nb.esercizio(
        titolo="Il grafico del carico in HTML",
        facoltativo=True,
        scenario="""
            Il grafico del carico di gennaio va mandato a un collega che non ha Python.
        """,
        richiesta="""
            Salva `fig_carico` in `carico_gennaio.html` con `include_plotlyjs="cdn"`, poi aprilo con un
            doppio clic dalla cartella del notebook. Output atteso: un file di qualche centinaio di KB.
        """,
        starter="""
            fig_carico.write_html(...)
        """,
        soluzione="""
            fig_carico.write_html("carico_gennaio.html", include_plotlyjs="cdn")
        """,
        verifica="""
            from pathlib import Path
            assert Path("carico_gennaio.html").exists(), "❌ Il file carico_gennaio.html non c'è: controlla il nome in write_html"
            assert Path("carico_gennaio.html").stat().st_size < 1_000_000, "❌ Il file è troppo grande: manca include_plotlyjs=\\"cdn\\""
        """,
        perche="Senza `include_plotlyjs=\"cdn\"` il file contiene tutta la libreria Plotly (qualche MB) e si apre anche senza rete.",
    )
    return nb
