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
        intento="Raccoglie gli argomenti della seconda giornata che restano fuori quando il tempo manca; si affronta in classe se si è in anticipo sul programma, oppure a casa.",
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
        Le sezioni sulle date usano `df_15min`, la serie costruita nel notebook 08. Contiene una potenza e
        una temperatura inventate, con un valore ogni 15 minuti per tre giorni, e i buchi di acquisizione
        sono già riempiti con l'interpolazione lineare. Le due celle seguenti importano le librerie e
        ricostruiscono la serie, in modo che questo notebook si possa eseguire da solo.
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
        Sottraendo due timestamp si ottiene un `Timedelta`, cioè una durata. Le durate servono a due scopi:
        controllare la regolarità di una serie, guardando la distanza tra ogni istante e il successivo, e
        misurare l'intervallo complessivo coperto dai dati. Nella prima cella calcoliamo con `diff()` la
        differenza tra ogni timestamp e il precedente; il primo valore è `NaT`, perché prima della prima
        riga non c'è nulla da sottrarre.
    """)
    nb.code("""
        # differenze tra timestamp consecutivi
        delta_consecutivi = df_15min.index.to_series().diff()

        delta_consecutivi.head(10)
    """)
    nb.md("""
        La durata totale della serie è la differenza tra l'ultimo e il primo timestamp dell'indice. Un
        `Timedelta` si converte in un numero con `total_seconds()`, e dividendo i secondi per 3600 otteniamo
        le ore coperte dal dataset.
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
        Un timestamp può essere **naive**, cioè composto solo da data e ora senza indicazione del fuso,
        oppure **timezone-aware**, quando porta con sé un fuso orario come `Europe/Rome`. Capita spesso di
        ricevere orari locali naive, che vanno interpretati nel fuso giusto prima di confrontarli con dati di
        altre fonti. La difficoltà principale è l'ora legale: nel giorno del cambio di primavera un'ora non
        esiste, mentre in quello d'autunno un'ora si ripete due volte.

        La documentazione di pandas dedica una sezione alla [gestione dei fusi orari]({DOC}/user_guide/timeseries.html#time-zone-handling).
    """)
    nb.box("attenzione", """
        Quando si localizza un indice che attraversa un cambio dell'ora legale, alcuni timestamp risultano
        ambigui o inesistenti e `tz_localize` solleva un errore. In questi casi si indica come trattarli con
        i parametri `ambiguous=` e `nonexistent=`. Se i dati arrivano già in UTC, conviene in genere
        mantenerli in UTC e convertirli all'ora locale solo al momento di mostrarli.
    """)
    nb.md("""
        Con `tz_localize` dichiariamo in quale fuso vanno letti i timestamp naive dell'indice, senza
        cambiare l'ora scritta. Con `tz_convert` riscriviamo poi gli stessi istanti nell'ora di un altro
        fuso: il 1° marzo l'Italia è un'ora avanti rispetto a UTC, quindi la mezzanotte italiana diventa le
        23 del giorno prima. Su un indice con fuso orario la selezione per intervallo con `loc` funziona come
        prima, e le stringhe vengono interpretate nel fuso dell'indice.
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
            Due operazioni molto usate sulle serie storiche sono `shift` e `rolling`. Il metodo `shift(k)`
            sposta i valori di `k` passi in avanti nel tempo e crea così una colonna ritardata, detta *lag*,
            che affianca a ogni istante il valore di qualche passo prima. Il metodo `rolling(w)` calcola
            invece una statistica, per esempio la media, su una finestra mobile di `w` valori consecutivi.
            Entrambe lasciano dei `NaN` all'inizio della serie, perché per le prime righe mancano i valori
            precedenti; la documentazione di riferimento è quella di [`rolling`]({DOC}/reference/api/pandas.DataFrame.rolling.html).
        """)
        nb.code("""
            df_scorrimento = df_15min.copy()

            # lag di 1 ora: con frequenza 15min corrisponde a 4 step
            df_scorrimento["power_lag_4"] = df_scorrimento["power_kw"].shift(4)

            # media mobile su 2 ore: 8 step
            df_scorrimento["power_ma_8"] = df_scorrimento["power_kw"].rolling(8).mean()

            df_scorrimento[["power_kw", "power_lag_4", "power_ma_8"]].head(12)
        """)
        nb.md("""
            Per vedere l'effetto delle due operazioni disegniamo ciascuna colonna nuova accanto alla potenza
            originale. La curva ritardata è la stessa curva spostata a destra di un'ora, mentre la media
            mobile è più liscia, perché attenua le oscillazioni casuali tra un quarto d'ora e l'altro.
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
        Per navigare una serie storica lunga Plotly offre due controlli sull'asse x: il **range slider**,
        una barra sotto il grafico con cui si sceglie l'intervallo da mostrare, e il **range selector**, una
        fila di pulsanti che saltano a intervalli predefiniti. Per usarli passiamo a `graph_objects` e
        seguiamo lo schema degli [esempi ufficiali](https://plotly.com/python/range-slider/), nel quale
        prima si costruiscono le tracce e poi si aggiunge il controllo nel `layout`.
    """)
    nb.md("""
        Come dati usiamo `px.data.stocks()`, lo stesso dataset del notebook 09. Contiene una colonna con la
        data, `date`, e una colonna per ciascuna azienda con il prezzo dell'azione indicizzato, cioè diviso
        per il valore iniziale, in modo che tutte le serie partano da 1. La colonna `date` è memorizzata come
        testo, quindi la convertiamo subito in datetime.
    """)
    nb.code("""
        df = px.data.stocks().copy()
        df["date"] = pd.to_datetime(df["date"])
        df.head()
    """)
    nb.md("""
        Con `go.Figure()` creiamo una figura vuota e con `add_trace` aggiungiamo una linea per ciascuna
        delle tre aziende scelte. Il nome della colonna diventa il nome della traccia, che compare nella
        legenda.
    """)
    nb.code("""
        aziende = ["AAPL", "AMZN", "MSFT"]

        fig = go.Figure()
        for c in aziende:
            fig.add_trace(go.Scatter(x=list(df["date"]), y=list(df[c]), name=c))
    """)
    nb.md("""
        I pulsanti del range selector si descrivono con una lista di dizionari. Ogni pulsante indica, con
        `count` e `step`, di quanto tornare indietro rispetto all'ultima data, e con `label` l'etichetta da
        mostrare; il pulsante con `step="all"` riporta il grafico all'intervallo completo. Nell'esempio
        definiamo quattro pulsanti: un mese, sei mesi, un anno e l'intero periodo.
    """)
    nb.code("""
        bottoni = [
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all"),
        ]
    """)
    nb.md("""
        Infine passiamo i pulsanti a `update_layout`, dentro la configurazione dell'asse x, e rendiamo
        visibile lo slider con `rangeslider=dict(visible=True)`. Nel grafico i pulsanti compaiono sopra
        l'area del disegno e lo slider sotto l'asse; trascinando i bordi dello slider si sceglie un
        intervallo qualsiasi.
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
        Per condividere un grafico interattivo con chi non usa Jupyter, la strada più semplice è salvarlo
        come file HTML, che si apre con qualsiasi browser e conserva zoom, legenda e controlli. Il metodo
        `write_html` scrive il file nella cartella del notebook; con `include_plotlyjs="cdn"` il file resta
        leggero, perché la libreria Plotly viene scaricata da internet al momento dell'apertura. I dettagli
        sono nella [documentazione](https://plotly.com/python/interactive-html-export/).
    """)
    nb.code("""
        # salva l'ultima figura (fig) in HTML, nella cartella del notebook: si apre con un browser
        # con include_plotlyjs="cdn" la libreria Plotly si scarica all'apertura: file leggero, ma serve la rete
        fig.write_html("plot_time_series.html", include_plotlyjs="cdn")
    """)

    # ------------------------------------------------------------------ 6 (A)
    with nb.solo("avanzata"):
        nb.sezione("Leggere il codice di un agente: type hint, dataclass, decoratori, generatori, kwargs", intro="""
            Gli script scritti da un agente, come quello che abbiamo letto nel notebook 10, usano spesso
            alcuni costrutti di Python che nel corso non abbiamo trattato. In questa sezione ne vediamo
            cinque, ciascuno con un esempio breve, con l'obiettivo di riconoscerli e di capire che cosa fanno
            quando li incontriamo nel codice di qualcun altro.
        """)
        nb.sottosezione("Type hint", intro="""
            I type hint sono annotazioni che indicano il tipo atteso dei parametri e del valore restituito da
            una funzione. Le forme più frequenti sono `list[str]`, `dict[str, float]`, `X | None` per un valore
            che può mancare e `-> None` per una funzione che non restituisce nulla. Python non le controlla
            durante l'esecuzione, perché servono a chi legge e agli strumenti dell'editor; infatti la seconda
            chiamata dell'esempio passa degli interi senza dare alcun errore.
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
            Il decoratore `@dataclass`, applicato a una classe che contiene solo dei campi con il loro tipo,
            scrive da solo il costruttore, una rappresentazione leggibile per la stampa e il confronto con
            `==`. Nell'esempio la classe `Libro` ha tre campi, l'ultimo con un valore predefinito, e due oggetti
            con gli stessi valori risultano uguali.
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
            Una riga che inizia con `@` sopra un `def` è un decoratore, che avvolge la funzione in un'altra e
            ne modifica il comportamento senza cambiarne il codice. Il decoratore `@cache` del modulo
            `functools` memorizza i risultati già calcolati, così una chiamata ripetuta con lo stesso argomento
            restituisce subito il valore salvato. Nell'esempio il calcolo ricorsivo di `fibonacci(80)`, che
            senza cache richiederebbe miliardi di chiamate, termina all'istante, perché ogni valore di `n`
            viene calcolato una volta sola.
        """)
        nb.code("""
            from functools import cache


            @cache  # senza, fibonacci(80) richiederebbe miliardi di chiamate
            def fibonacci(n: int) -> int:
                return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)


            fibonacci(80)  # altri decoratori frequenti: @property, @staticmethod, @pytest.fixture
        """)

        nb.sottosezione("Generatori", intro="""
            Una funzione che usa `yield` al posto di `return` è un generatore, e consegna un valore alla volta,
            quando un ciclo `for` o una chiamata a `list()` lo richiede. Negli script si trova spesso per
            dividere una sequenza in blocchi, come nell'esempio, che restituisce la lista della spesa a gruppi
            di due elementi.
        """)
        nb.code("""
            def a_blocchi(elementi: list, n: int):
                for i in range(0, len(elementi), n):
                    yield elementi[i:i + n]


            spesa = ["pane", "latte", "uova", "mele", "pasta"]
            list(a_blocchi(spesa, 2))
        """)

        nb.sottosezione("`**kwargs`", intro="""
            Un parametro preceduto da due asterischi, scritto di solito `**kwargs`, raccoglie in un dizionario
            tutti gli argomenti passati per nome che la funzione non elenca esplicitamente; allo stesso modo
            `*args` raccoglie in una tupla quelli passati per posizione. Il nome è libero, e nell'esempio è
            `opzioni`. Negli script degli agenti si usa soprattutto per inoltrare le opzioni a un'altra
            funzione così come sono, come fa `leggi_csv` con `usecols` e `nrows`.
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
        Gli esercizi usano due oggetti dei notebook precedenti. Il primo è `carico`, il carico Terna della
        zona Nord nel 2024, ordinato per data e senza i duplicati dovuti all'ora legale come nel notebook 08;
        il secondo è `fig_carico`, il grafico di gennaio costruito nell'esercizio 9.1. La cella seguente li
        ricostruisce entrambi.
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
            Il grafico di gennaio contiene quasi 3000 quarti d'ora, troppi per distinguere i singoli giorni
            a colpo d'occhio. Con un range slider e due pulsanti possiamo passare rapidamente dalla vista di
            una settimana a quella del mese intero.
        """,
        richiesta="""
            1. Attiva il range slider sotto l'asse x di `fig_carico`.
            2. Aggiungi un range selector con due pulsanti: il primo, con etichetta `1w`, torna indietro di una settimana (`count=7`, `step="day"`), mentre il secondo, `all`, mostra tutto il mese.

            Se il codice è corretto, sotto il grafico compare lo slider e sopra compaiono i due pulsanti.
        """,
        suggerimento="su una figura creata con `px` lo slider si attiva con `fig_carico.update_xaxes(rangeslider_visible=True)`, e il range selector si aggiunge nella stessa chiamata con `rangeselector=dict(buttons=...)`.",
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
            Dobbiamo mandare il grafico del carico di gennaio, `fig_carico`, a un collega che non ha Python
            installato ma vuole comunque poterlo esplorare con lo zoom.
        """,
        richiesta="""
            Salva `fig_carico` nel file `carico_gennaio.html` con `include_plotlyjs="cdn"`, poi aprilo con un
            doppio clic dalla cartella del notebook. Il file che ottieni è leggero, sotto 1 MB, e nel browser
            il grafico resta interattivo.
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
        perche="Senza `include_plotlyjs=\"cdn\"` il file contiene al suo interno l'intera libreria Plotly, che pesa qualche megabyte, e in compenso si apre anche senza connessione. Con l'opzione `cdn` il file contiene solo i dati e la descrizione del grafico, e la libreria viene scaricata all'apertura.",
    )
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="La media mobile su 24 ore",
            scenario="""
                Il carico quartorario oscilla molto tra il giorno e la notte, e queste oscillazioni nascondono
                l'andamento nel corso dell'anno. Una media mobile su 24 ore copre sempre un giorno intero, quindi
                elimina il ciclo giornaliero e lascia vedere l'andamento di fondo.
            """,
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
            suggerimento="su dati quartorari una finestra di 24 ore comprende 96 valori.",
            facoltativo=True,
        )

    return nb
