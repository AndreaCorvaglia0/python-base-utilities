"""09 · Plotly per serie storiche."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="09",
        file="09_Plotly",
        titolo="Plotly per serie storiche",
        blocco=3,
        giornata=2,
        intento="Plotly produce grafici interattivi, che per una serie storica permettono di ingrandire un periodo, selezionare un intervallo e confrontare più serie nello stesso grafico.",
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
        In questo notebook usiamo `plotly.express`, il modulo di alto livello di Plotly, che costruisce un grafico
        completo a partire da un DataFrame con una sola chiamata. A differenza di un'immagine statica, una figura
        Plotly si può ingrandire, scorrere e interrogare passando il mouse sui punti, e per una serie storica questo
        permette di muoversi nel tempo senza riscrivere il codice. La documentazione di riferimento è quella di
        [Plotly Express](https://plotly.com/python/plotly-express/), con le pagine dedicate ai
        [grafici a linee](https://plotly.com/python/line-charts/) e alle
        [serie temporali](https://plotly.com/python/time-series/).
    """)
    nb.code("""
        import pandas as pd
        import plotly.express as px
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("I quattro elementi chiave", intro="""
        Il codice di un grafico Plotly diventa molto più facile da leggere se si tengono distinti quattro elementi.
        Il primo sono i dati, cioè un DataFrame con una colonna tempo di tipo `datetime`, ordinata. Il secondo è il
        mapping, che stabilisce quali colonne finiscono sull'asse `x`, sull'asse `y` e, quando serve, nel colore
        (`color`). Il terzo sono le tracce: una `Figure` è composta da una o più tracce, elencate in `fig.data`, e in
        una serie storica la traccia tipica è uno `Scatter` con `mode="lines"`. Il quarto è il layout, cioè titolo,
        assi e testo al passaggio del mouse, che si modifica con `fig.update_layout(...)` e `fig.update_xaxes(...)`.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Il dataset stocks", intro="""
        Come primo esempio usiamo `px.data.stocks()`, un dataset già incluso in Plotly con le quotazioni settimanali
        di sei società tecnologiche nel 2018 e nel 2019. È in formato [wide-form](https://plotly.com/python/wide-form/),
        cioè ha una colonna tempo (`date`) e una colonna per ciascuna serie. I valori sono **indicizzati**, nel senso
        che ogni serie vale 1 alla prima data, e questo rende immediato il confronto tra andamenti relativi. Nella
        cella qui sotto convertiamo `date` in `datetime`, perché nel dataset è una stringa.
    """)
    nb.code("""
        df = px.data.stocks().copy()
        df["date"] = pd.to_datetime(df["date"])
        df.head()
    """)
    nb.box("nota", """
        Se la colonna `date` non è di tipo `datetime` o non è ordinata, la linea collega i punti nell'ordine delle
        righe e il grafico diventa confuso, con salti avanti e indietro nel tempo.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Primo grafico con Plotly Express", intro="""
        Il primo grafico è una linea sola, costruita con `px.line` e con un mapping esplicito, che mette la colonna
        `date` sull'asse `x` e la colonna della società scelta sull'asse `y`. Il nome della società sta in una
        variabile, così per cambiare serie basta modificare una riga, e il titolo si compone con una f-string. Il
        grafico è interattivo: trascinando il mouse su un tratto si ingrandisce quel periodo, e un doppio clic
        riporta alla vista completa.
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
            Assegna ad `azienda` un'altra colonna del dataset, per esempio `AAPL`, `AMZN` o `MSFT`. Poi limita il
            grafico agli ultimi 12 mesi, filtrando `df` con una maschera sulla colonna `date` prima di passarlo a
            `px.line`. Poiché il dataset finisce alla fine del 2019, basta tenere le date a partire dal `2019-01-01`,
            e il grafico che ottieni comincia a gennaio 2019.
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
            La media mobile attenua le oscillazioni di breve periodo e rende più visibile la tendenza della serie. La
            calcoliamo con `rolling` in una nuova colonna e la disegniamo accanto alla serie originale, passando a `y`
            la lista delle due colonne. Poiché il dataset ha un valore a settimana, una finestra di 4 osservazioni
            copre circa un mese; le prime tre righe non hanno abbastanza valori precedenti e restano `NaN`, quindi
            le togliamo con `dropna`.
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
        Con i dati wide-form si può passare direttamente a `y` una lista di colonne, e `px.line` disegna una linea per
        ciascuna, con un colore diverso e una voce nella legenda. È il caso che si incontra più spesso nella pratica,
        quando si lavora con una tabella che contiene molte serie già allineate sulla stessa colonna tempo. Un clic
        su una voce della legenda nasconde la linea corrispondente, mentre un doppio clic lascia visibile solo quella.
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
            Aggiungi o togli una società dalla lista `aziende`. Poi crea `df_indicizzato`, una copia di `df` in cui le
            serie sono riportate a base 100 alla prima data, dividendo ogni colonna per il suo primo valore e
            moltiplicando per 100 (`valore / valore.iloc[0] * 100`), e ripeti il grafico. Se il calcolo è corretto,
            tutte le linee partono da 100.
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
        Plotly Express ha una funzione per ogni tipo di grafico, e tutte accettano gli stessi argomenti di `px.line`,
        a partire dal DataFrame e dal mapping delle colonne. Le proviamo sui dati orari di una turbina eolica in Texas,
        che contengono tra l'altro la velocità del vento e la potenza prodotta. Il timestamp del file non riporta
        l'anno, quindi lo aggiungiamo prima della conversione, e diamo alle due colonne che ci interessano nomi più brevi.
    """)
    nb.code("""
        turbina = pd.read_csv("../Dati/TexasTurbine.csv")
        # il timestamp non ha l'anno: lo aggiungiamo noi
        turbina["timestamp"] = pd.to_datetime("2023 " + turbina["Time stamp"], format="%Y %b %d, %I:%M %p")
        turbina = turbina.rename(columns={"System power generated | (kW)": "potenza_kw", "Wind speed | (m/s)": "vento_ms"})
        turbina.head(3)
    """)
    nb.md("""
        L'istogramma divide la velocità del vento in intervalli e conta quante ore cadono in ciascuno. Per questo
        basta indicare la colonna da mettere sull'asse `x`, perché l'altezza delle barre è il conteggio, mentre il
        parametro `nbins` stabilisce il numero di barre.
    """)
    nb.code("""
        fig = px.histogram(turbina, x="vento_ms", nbins=30, title="Distribuzione del vento")
        fig.show()
    """)
    nb.md("""
        Lo scatter disegna un punto per ogni riga e mostra la relazione tra due colonne, in questo caso il vento
        sull'asse x e la potenza sull'asse y. L'insieme dei punti descrive la curva di potenza della turbina, che sale
        rapidamente con il vento e poi si appiattisce quando la turbina raggiunge la sua potenza massima. Con
        `opacity` i punti diventano semitrasparenti, e le zone in cui si accumulano risultano più scure.
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
            Il file di Terna contiene il carico della zona Nord nel 2024, con un valore ogni quarto d'ora. Su un anno
            intero le oscillazioni dei singoli giorni si confondono, quindi vogliamo guardare da vicino il solo mese
            di gennaio.
        """,
        richiesta="""
            1. Tieni in `gennaio` le sole righe di `carico` relative a gennaio 2024, usando una maschera sul mese della colonna `Date`.
            2. Costruisci `fig_carico` con `px.line`, mettendo `Date` sull'asse x e `Total Load [MW]` sull'asse y, con il titolo `Carico Nord, gennaio 2024`.

            Il grafico che ottieni contiene una sola linea, in cui si riconoscono i cicli giornalieri e il calo dei fine settimana.
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
            Vogliamo sapere per quante ore la turbina texana produce poco e per quante lavora vicino alla sua potenza
            massima, attorno ai 3000 kW.
        """,
        richiesta="""
            Costruisci in `fig_potenza` l'istogramma della colonna `potenza_kw` di `turbina`, con 30 barre e il
            titolo `Distribuzione della potenza`. Nel grafico la barra più alta è quella vicino a 0 kW, segno che per
            molte ore la turbina produce poco o nulla.
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
