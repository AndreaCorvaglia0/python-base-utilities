"""A2 · Approfondimenti 2: il materiale della seconda giornata da fare se la classe è avanti."""

from nbkit import Notebook

DOC = "https://pandas.pydata.org/pandas-docs/stable"


def costruisci() -> Notebook:
    nb = Notebook(
        num="A2",
        file="Approfondimenti_2",
        titolo="Approfondimenti 2",
        blocco=4,
        giornata=2,
        fuori_programma=True,
        intento="Quello che resta fuori dalla seconda giornata quando il tempo manca: da fare se la classe è avanti, o a casa.",
        obiettivi={
            "base": [
                "misurare durate con `Timedelta` e dare un fuso orario alle date con `tz_localize` e `tz_convert`",
                "navigare una serie lunga con range slider e range selector",
                "esportare un grafico interattivo in HTML",
            ],
            "avanzata": [
                "misurare durate con `Timedelta`, gestire il fuso orario e costruire lag e medie mobili con `shift` e `rolling`",
                "navigare una serie con range slider e range selector ed esportare il grafico in HTML",
                "riconoscere type hint, `@dataclass`, decoratori, generatori e `**kwargs`",
            ],
        },
        tempo={"base": 40, "avanzata": 60},
        dati={
            "base": ["load_total_north_hourly_2024.xlsx"],
            "avanzata": ["load_total_north_hourly_2024.xlsx", "impianti_fv.csv"],
        },
    )

    # ------------------------------------------------------------------ setup
    nb.md("""
        Le sezioni sulle date usano `df_15min`, la serie del notebook 08: potenza e temperatura inventate,
        un valore ogni 15 minuti per tre giorni, con i buchi riempiti dall'interpolazione lineare. La ricostruiamo qui.
    """)
    nb.code("""
        import numpy as np
        np.random.seed(42)
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
    """)
    nb.code("""
        intervallo = pd.date_range("2025-03-01 00:00", periods=3 * 24 * 4, freq="15min")
        ore = intervallo.hour + intervallo.minute / 60
        power_kw = 220 + 60 * np.sin(2 * np.pi * (ore / 24)) + np.random.normal(0, 8, size=len(intervallo))
        temp_c = 12 + 5 * np.sin(2 * np.pi * ((ore - 6) / 24)) + np.random.normal(0, 0.7, size=len(intervallo))

        misure = pd.DataFrame({"timestamp": intervallo, "power_kw": power_kw.round(1), "temp_c": temp_c.round(1)})
        misure = misure.drop(np.random.choice(misure.index, size=18, replace=False))  # i buchi

        df_15min = misure.set_index("timestamp").asfreq("15min").interpolate(method="linear")
        df_15min.head()
    """)

    # ------------------------------------------------------------------ 1
    nb.sezione("Differenze tra date", intro="""
        Le differenze tra timestamp producono `Timedelta` (durate).
        Servono sia per capire la regolarità della serie sia per misurare intervalli (es. "quante ore copre il dataset?").
    """)
    nb.code("""
        # differenze tra timestamp consecutivi
        delta_consecutivi = df_15min.index.to_series().diff()

        delta_consecutivi.head(10)
    """)
    nb.code("""
        # intervallo totale coperto
        delta_totale = df_15min.index.max() - df_15min.index.min()
        delta_totale
    """)
    nb.code("""
        # durata in ore (float)
        delta_totale.total_seconds() / 3600
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Fuso orario", intro=f"""
        Un timestamp può essere **naive**, senza fuso orario (solo data e ora), oppure **timezone-aware**,
        con fuso orario (es. `Europe/Rome`). Spesso si ricevono orari locali naive da interpretare correttamente.
        L'ora legale è la trappola tipica: alcune ore non esistono (primavera) o si ripetono (autunno).

        Documentazione: [fusi orari]({DOC}/user_guide/timeseries.html#time-zone-handling)
    """)
    nb.box("attenzione", """
        Localizzare un indice che attraversa un cambio ora legale può generare timestamp ambigui o inesistenti:
        in quei casi servono i parametri `ambiguous=` e `nonexistent=`.
        Se i dati arrivano già in UTC, spesso è meglio mantenerli in UTC e convertire solo in visualizzazione.
    """)
    nb.code("""
        df_fuso = df_15min.copy()

        # interpretiamo i timestamp come orari locali italiani
        df_fuso.index = df_fuso.index.tz_localize("Europe/Rome")

        # conversione a UTC (utile per sistemi e confronti)
        df_utc = df_fuso.tz_convert("UTC")

        df_fuso.index[:3], df_utc.index[:3]
    """)
    nb.code("""
        df_fuso.loc["2025-03-01 06:00":"2025-03-01 12:00"].head()
    """)

    # ------------------------------------------------------------------ 3 (A)
    with nb.solo("avanzata"):
        nb.sezione("Shift e rolling", intro=f"""
            Due operazioni semplici e molto usate nella gestione di time series:

            - `shift(k)`: sposta i valori di `k` step nel tempo (crea "lag").
            - `rolling(w)`: calcola statistiche su una finestra mobile di ampiezza `w`.

            Entrambe possono introdurre `NaN` in testa (perché mancano i valori "precedenti").
            Documentazione: [`rolling`]({DOC}/reference/api/pandas.DataFrame.rolling.html)
        """)
        nb.code("""
            df_scorrimento = df_15min.copy()

            # lag di 1 ora: con frequenza 15min corrisponde a 4 step
            df_scorrimento["power_lag_4"] = df_scorrimento["power_kw"].shift(4)

            # media mobile su 2 ore: 8 step
            df_scorrimento["power_ma_8"] = df_scorrimento["power_kw"].rolling(8).mean()

            df_scorrimento[["power_kw", "power_lag_4", "power_ma_8"]].head(12)
        """)
        nb.code("""
            # shift di 1 ora (4 step) contro power_kw
            fig = px.line(df_scorrimento, x=df_scorrimento.index, y=["power_kw", "power_lag_4"], title="Shift di 1 ora (4 step)")
            fig.show()
        """)
        nb.code("""
            # media mobile su una finestra di 2 ore (8 step) contro power_kw
            fig = px.line(df_scorrimento, x=df_scorrimento.index, y=["power_kw", "power_ma_8"], title="Media mobile su finestra di 2 ore (8 step)")
            fig.show()
        """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Range slider e range selector", intro="""
        Qui si passa a `graph_objects` per usare il **range slider** e il **range selector** sull'asse x,
        utili per navigare serie storiche lunghe. Il codice segue lo schema degli
        [esempi ufficiali](https://plotly.com/python/range-slider/): si costruiscono le tracce, poi si
        aggiunge il controllo nel `layout`.
    """)
    nb.md("""
        Usiamo il dataset `px.data.stocks()` del notebook 09: una colonna tempo (`date`) e una colonna per
        azienda, con i valori indicizzati (partono da 1).
    """)
    nb.code("""
        df = px.data.stocks().copy()
        df["date"] = pd.to_datetime(df["date"])
        df.head()
    """)
    nb.code("""
        aziende = ["AAPL", "AMZN", "MSFT"]

        fig = go.Figure()
        for c in aziende:
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

    # ------------------------------------------------------------------ 5
    nb.sezione("Esportare in HTML", intro="""
        Per condividere il grafico interattivo senza Jupyter, l'export in HTML è la strada più semplice
        ([documentazione](https://plotly.com/python/interactive-html-export/)).
    """)
    nb.code("""
        # salva l'ultima figura (fig) in HTML, nella cartella del notebook: si apre con un browser
        # con include_plotlyjs="cdn" la libreria Plotly si scarica all'apertura: file leggero, ma serve la rete
        fig.write_html("plot_time_series.html", include_plotlyjs="cdn")
    """)

    # ------------------------------------------------------------------ 6 (A)
    with nb.solo("avanzata"):
        nb.sezione("Leggere il codice di un agente: type hint, dataclass, decoratori, generatori, kwargs", intro="""
            Cinque costrutti che compaiono spesso negli script scritti da un agente, come quello letto nel
            notebook 10, ognuno con un esempio piccolo.
        """)
        nb.sottosezione("Type hint", intro="""
            Le forme più frequenti sono `list[str]`, `dict[str, float]`, `X | None` e `-> None`; Python non le
            controlla quando esegue.
        """)
        nb.code('''
            def prezzo_medio(prezzi: dict[str, float], escludi: list[str] | None = None) -> float:
                """Prezzo medio dei prodotti, senza quelli in escludi."""
                escludi = escludi or []
                validi = [p for nome, p in prezzi.items() if nome not in escludi]
                return sum(validi) / len(validi)


            print(prezzo_medio({"pane": 2.5, "latte": 1.3, "caffè": 4.2}, escludi=["caffè"]))  # Output: 1.9
            print(prezzo_medio({"pane": 2, "latte": 1}))  # int al posto di float, nessun errore. Output: 1.5
        ''')

        nb.sottosezione("`@dataclass`", intro="""
            Su una classe fatta di campi, `@dataclass` scrive da solo il costruttore, la stampa e il confronto con `==`.
        """)
        nb.code("""
            from dataclasses import dataclass


            @dataclass
            class Libro:
                titolo: str
                autore: str
                pagine: int = 0


            libro = Libro("Il nome della rosa", "Umberto Eco", pagine=503)
            print(libro)
            print(libro == Libro("Il nome della rosa", "Umberto Eco", 503))  # Output: True
        """)

        nb.sottosezione("Decoratori", intro="""
            Una riga `@nome` sopra un `def` avvolge la funzione in un'altra: `@cache` ricorda i risultati già calcolati.
        """)
        nb.code("""
            from functools import cache


            @cache  # senza, fibonacci(80) richiederebbe miliardi di chiamate
            def fibonacci(n: int) -> int:
                return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)


            fibonacci(80)  # altri decoratori frequenti: @property, @staticmethod, @pytest.fixture
        """)

        nb.sottosezione("Generatori", intro="""
            Una funzione con `yield` al posto di `return` consegna un valore alla volta, quando un `for` o `list()` lo chiede.
        """)
        nb.code("""
            def a_blocchi(elementi: list, n: int):
                for i in range(0, len(elementi), n):
                    yield elementi[i:i + n]


            spesa = ["pane", "latte", "uova", "mele", "pasta"]
            list(a_blocchi(spesa, 2))
        """)

        nb.sottosezione("`**kwargs`", intro="""
            `**kwargs` raccoglie in un dizionario i parametri passati per nome che la funzione non elenca
            (`*args` in una tupla quelli per posizione); negli script degli agenti li passa così come sono a
            un'altra funzione.
        """)
        nb.code("""
            def ordine(piatto: str, **opzioni) -> str:
                return f"{piatto}: {opzioni}"


            def leggi_csv(path: str, **opzioni) -> pd.DataFrame:
                return pd.read_csv(path, **opzioni)


            print(ordine("pizza", impasto="integrale", extra="olive"))
            leggi_csv("../Dati/impianti_fv.csv", usecols=["comune", "kwp"], nrows=3)
        """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi", intro="""
        Gli esercizi usano `carico`, il carico Terna della zona Nord 2024 ordinato e senza i duplicati
        dell'ora legale, come nel notebook 08, e `fig_carico`, il grafico di gennaio dell'esercizio 9.1.
        La cella qui sotto li ricostruisce.
    """)
    nb.code("""
        carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico = carico.sort_values("Date")
        carico = carico.drop_duplicates(subset="Date")

        gennaio = carico[carico["Date"].dt.month == 1]
        fig_carico = px.line(gennaio, x="Date", y="Total Load [MW]", title="Carico Nord, gennaio 2024")
        fig_carico.show()
    """)
    nb.esercizio(
        titolo="Il range slider sul carico di gennaio",
        aula="base",
        scenario="""
            Gennaio ha quasi 3000 quarti d'ora: con lo slider e due pulsanti si passa da una settimana al mese intero.
        """,
        richiesta="""
            1. Attiva il range slider sotto l'asse x di `fig_carico`.
            2. Aggiungi un range selector con due pulsanti: `1w`, una settimana indietro (`count=7`, `step="day"`), e `all`.

            Output atteso: lo slider sotto il grafico e i due pulsanti sopra.
        """,
        suggerimento="su una figura di `px` lo slider si accende con `fig_carico.update_xaxes(rangeslider_visible=True)`; il range selector va nella stessa chiamata, con `rangeselector=dict(buttons=...)`.",
        starter="""
            bottoni_carico = [
                ...,
                dict(step="all"),
            ]
            fig_carico.update_xaxes(...)
            fig_carico.show()
        """,
        soluzione="""
            bottoni_carico = [
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(step="all"),
            ]
            fig_carico.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=bottoni_carico))
            fig_carico.show()
        """,
        verifica="""
            assert fig_carico.layout.xaxis.rangeslider.visible, "❌ Manca il range slider: update_xaxes(rangeslider_visible=True)"
            assert len(fig_carico.layout.xaxis.rangeselector.buttons) == 2, "❌ Il range selector deve avere due pulsanti, 1w e all"
            assert fig_carico.layout.xaxis.rangeselector.buttons[0].count == 7, "❌ Il primo pulsante va indietro di 7 giorni: count=7, step='day'"
        """,
    )
    nb.esercizio(
        titolo="Il grafico del carico in HTML",
        scenario="""
            Il grafico del carico di gennaio, `fig_carico`, va mandato a un collega che non ha Python.
        """,
        richiesta="""
            Salva `fig_carico` in `carico_gennaio.html` con `include_plotlyjs="cdn"`, poi aprilo con un
            doppio clic dalla cartella del notebook. Output atteso: un file leggero, sotto 1 MB.
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
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="La media mobile su 24 ore",
            scenario="Il carico quartorario oscilla molto tra giorno e notte: una media mobile su 24 ore mostra l'andamento di fondo.",
            richiesta="""
                1. Calcola in `media_24h` la media mobile su 24 ore di `Total Load [MW]`, con `Date` come indice.
                2. Metti in `picco_24h` il timestamp in cui la media mobile è più alta.
            """,
            starter="""
                serie = carico.set_index("Date")["Total Load [MW]"]
                media_24h = ...
                picco_24h = ...

                picco_24h
            """,
            soluzione="""
                serie = carico.set_index("Date")["Total Load [MW]"]
                media_24h = serie.rolling(96).mean()
                picco_24h = media_24h.idxmax()

                picco_24h
            """,
            verifica="""
                assert round(media_24h.max()) == 27189, "❌ media_24h: rolling su 96 quarti d'ora, poi mean()"
                assert picco_24h == pd.Timestamp("2024-07-19 15:30"), "❌ picco_24h: usa media_24h.idxmax()"
            """,
            suggerimento="24 ore sono 96 quarti d'ora.",
            facoltativo=True,
        )

    return nb
