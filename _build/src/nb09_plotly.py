"""09 · Plotly per serie storiche."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="09",
        file="09_Plotly",
        titolo="Plotly per serie storiche",
        blocco=4,
        giornata=4,
        intento="Plotly produce grafici interattivi, che per una serie storica permettono di ingrandire un periodo, scegliere un intervallo con lo slider e confrontare più serie nello stesso grafico, e che si salvano in un file HTML da aprire nel browser.",
        obiettivi=[
            "fare grafici a linee, istogrammi e scatter con Plotly Express, confrontando più serie nello stesso grafico",
            "navigare una serie lunga con range slider e range selector ed esportare un grafico in HTML",
            "riconoscere dati, mapping, tracce e layout di una figura",
        ],
        tempo={"base": 45, "avanzata": 45},
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
    nb.hands_on(
        richiesta="""
            Disegna in `fig_aapl` la linea della colonna `AAPL` con il titolo `Apple (indicizzato)`, cambiando il
            valore di `azienda` e il titolo nella chiamata a `px.line`. Il grafico ha una sola linea, che come tutte le
            serie del dataset parte da 1 alla prima data.
        """,
        starter="""
            azienda = ...

            fig_aapl = px.line(df, x="date", y=azienda, title=...)
            fig_aapl.show()
        """,
        soluzione="""
            azienda = "AAPL"

            fig_aapl = px.line(df, x="date", y=azienda, title="Apple (indicizzato)")
            fig_aapl.show()
        """,
        verifica="""
            assert fig_aapl.layout.yaxis.title.text == "AAPL", "❌ fig_aapl: azienda deve valere 'AAPL'"
            assert fig_aapl.layout.title.text == "Apple (indicizzato)", "❌ fig_aapl: il titolo è 'Apple (indicizzato)'"
        """,
        prova_anche="con `MSFT` o con `NFLX`.",
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
    nb.hands_on(
        richiesta="""
            Aggiungi `NFLX` alla lista `aziende` e disegna in `fig_4` il confronto tra le quattro società, con il
            titolo `Confronto tra quattro società`. Nel grafico compaiono quattro linee, ciascuna con la sua voce
            nella legenda.
        """,
        starter="""
            aziende = ["AAPL", "AMZN", "MSFT", ...]

            fig_4 = px.line(...)
            fig_4.show()
        """,
        soluzione="""
            aziende = ["AAPL", "AMZN", "MSFT", "NFLX"]

            fig_4 = px.line(df, x="date", y=aziende, title="Confronto tra quattro società")
            fig_4.show()
        """,
        verifica="""
            nomi = [traccia.name for traccia in fig_4.data]
            assert len(nomi) == 4 and "NFLX" in nomi, "❌ fig_4: passa a y la lista aziende con NFLX in fondo"
            assert fig_4.layout.title.text == "Confronto tra quattro società", "❌ fig_4: il titolo è 'Confronto tra quattro società'"
        """,
        prova_anche="a togliere `AMZN` dalla lista.",
    )

    # ------------------------------------------------------------------ 6
    nb.sezione("Range slider e range selector", intro="""
        Le quotazioni di `stocks` hanno un valore a settimana, ma molte serie storiche sono molto più lunghe. Il
        carico elettrico della zona Nord pubblicato da Terna, che abbiamo usato nel notebook 08, ha un valore ogni
        quarto d'ora per tutto il 2024, cioè più di 35.000 punti, e in un grafico dell'anno intero i singoli giorni
        non si distinguono. Per muoversi in una serie così Plotly offre due controlli sull'asse x: il **range
        slider**, una barra sotto il grafico con cui si sceglie l'intervallo da mostrare, e il **range selector**,
        una fila di pulsanti che saltano a intervalli predefiniti. Gli esempi ufficiali sono nella pagina sul
        [range slider](https://plotly.com/python/range-slider/).
    """)
    nb.md("""
        Leggiamo il file come nel notebook 08. Le righe arrivano dalla più recente alla più vecchia, quindi le
        ordiniamo per data, e togliamo i quattro quarti d'ora ripetuti nella notte di ottobre in cui si torna
        all'ora solare, che darebbero due valori diversi per lo stesso istante.
    """)
    nb.code("""
        carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico = carico.sort_values("Date")
        carico = carico.drop_duplicates(subset="Date")
        carico.head(3)
    """)
    nb.md("""
        I pulsanti del range selector si descrivono con una lista di dizionari, uno per pulsante. In ogni
        dizionario `count` e `step` dicono di quanto tornare indietro a partire dalla fine dell'intervallo
        visibile, per esempio sette giorni o un mese, mentre `label` è l'etichetta scritta sul pulsante. Il
        pulsante con `step="all"` riporta il grafico all'anno intero.
    """)
    nb.code("""
        bottoni = [
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(step="all"),
        ]
    """)
    nb.md("""
        Il grafico si costruisce con `px.line`, come quelli delle quotazioni, e i due controlli si aggiungono con
        `update_xaxes`, il metodo che modifica l'asse x: `rangeslider_visible=True` mostra lo slider e
        `rangeselector=dict(buttons=bottoni)` mette i pulsanti sopra il grafico. Oltre i mille punti Plotly
        Express disegna la linea con WebGL, una tecnica più veloce che però lo slider non riproduce nella sua
        anteprima, e per questo passiamo `render_mode="svg"`, che la disegna come nei grafici precedenti. Un
        clic su `1w` mostra l'ultima settimana dell'anno, e trascinando la finestra evidenziata nello slider
        l'intervallo di una settimana scorre lungo tutto il 2024.
    """)
    nb.code("""
        fig_anno = px.line(
            carico,
            x="Date",
            y="Total Load [MW]",
            title="Carico Nord, 2024",
            render_mode="svg"
        )
        fig_anno.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=bottoni))
        fig_anno.show()
    """)
    nb.hands_on(
        richiesta="""
            Prepara in `fig_pulsanti` lo stesso grafico con tre pulsanti diversi: `1d`, che mostra un giorno solo,
            `3m`, che mostra tre mesi, e `all`. Il resto della cella è già scritto, quindi basta completare `count`
            e `step` nei primi due dizionari. Con il pulsante `1d` si vede la forma del carico in una sola giornata.
        """,
        starter="""
            bottoni_nuovi = [
                dict(count=..., label="1d", step=..., stepmode="backward"),
                dict(count=..., label="3m", step=..., stepmode="backward"),
                dict(step="all"),
            ]
            fig_pulsanti = px.line(carico, x="Date", y="Total Load [MW]", title="Carico Nord, 2024", render_mode="svg")
            fig_pulsanti.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=bottoni_nuovi))
            fig_pulsanti.show()
        """,
        soluzione="""
            bottoni_nuovi = [
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(step="all"),
            ]
            fig_pulsanti = px.line(carico, x="Date", y="Total Load [MW]", title="Carico Nord, 2024", render_mode="svg")
            fig_pulsanti.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=bottoni_nuovi))
            fig_pulsanti.show()
        """,
        verifica="""
            passi = [(b.count, b.step) for b in fig_pulsanti.layout.xaxis.rangeselector.buttons]
            assert passi[:2] == [(1, "day"), (3, "month")], "❌ fig_pulsanti: i primi due pulsanti sono count=1, step='day' e count=3, step='month'"
        """,
        prova_anche="ad aggiungere un pulsante `6m` prima di `all`.",
    )

    # ------------------------------------------------------------------ 7
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
    nb.hands_on(
        richiesta="""
            Ripeti in `fig_10` l'istogramma del vento con 10 barre invece di 30, cambiando soltanto `nbins`. Le barre
            diventano più larghe e ciascuna conta le ore di un intervallo di velocità più ampio.
        """,
        starter="""
            fig_10 = px.histogram(turbina, x="vento_ms", nbins=..., title="Distribuzione del vento")
            fig_10.show()
        """,
        soluzione="""
            fig_10 = px.histogram(turbina, x="vento_ms", nbins=10, title="Distribuzione del vento")
            fig_10.show()
        """,
        verifica="""
            assert fig_10.data[0].nbinsx == 10, "❌ fig_10: passa nbins=10 a px.histogram"
        """,
        prova_anche="con `nbins=100`.",
    )
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

    # ------------------------------------------------------------------ 8
    nb.sezione("Esportare in HTML", intro="""
        Un grafico Plotly si può salvare in un file HTML, che si apre con un doppio clic in qualsiasi browser e
        conserva zoom, legenda, slider e pulsanti, quindi è il modo più semplice per mandare un grafico interattivo
        a chi non usa Python. Il metodo `write_html` scrive il file nella cartella del notebook. Con
        `include_plotlyjs="cdn"` il file contiene soltanto i dati e la descrizione del grafico, mentre la libreria
        Plotly viene scaricata da internet al momento dell'apertura; in questo modo il file del carico pesa circa
        1,4 MB invece di 6, ma per vederlo serve una connessione. I dettagli sono nella
        [documentazione](https://plotly.com/python/interactive-html-export/).
    """)
    nb.code("""
        fig_anno.write_html("carico_nord_2024.html", include_plotlyjs="cdn")
    """)
    nb.md("""
        Per controllare che il file sia stato scritto usiamo `os.path.exists`, come nel notebook 06 per i file di
        dati. Il file `carico_nord_2024.html` si trova accanto al notebook, e aprendolo nel browser ritroviamo lo
        stesso grafico, con lo slider e i pulsanti.
    """)
    nb.code("""
        import os

        os.path.exists("carico_nord_2024.html")  # Output: True
    """)
    nb.hands_on(
        richiesta="""
            Salva nel file `vento_potenza.html`, sempre con `include_plotlyjs="cdn"`, lo scatter del vento e della
            potenza, che dopo la sezione precedente è ancora nella variabile `fig`. Se apri il file nel browser e
            passi il mouse su un punto, compaiono il vento e la potenza di quell'ora.
        """,
        starter="""
            fig.write_html(...)
        """,
        soluzione="""
            fig.write_html("vento_potenza.html", include_plotlyjs="cdn")
        """,
        verifica="""
            import os
            assert os.path.exists("vento_potenza.html"), "❌ Il file vento_potenza.html non c'è: controlla il nome in fig.write_html"
        """,
    )

    # ------------------------------------------------------------------ Extra
    nb.sezione("Extra", intro="""
        Gli esercizi di questa sezione ripassano i punti principali del notebook e sono pensati per essere svolti a
        casa, con calma, e durante le ore di corso li saltiamo. I primi due usano il DataFrame `carico` della
        sezione sul range slider, mentre il terzo usa il DataFrame `turbina` della sezione sull'istogramma.
    """)
    nb.esercizio(
        titolo="Un mese di carico con lo slider",
        scenario="""
            Nel grafico del carico sull'intero 2024 i singoli giorni si distinguono solo ingrandendo, quindi
            vogliamo un grafico del solo mese di gennaio, con il titolo `Carico Nord, gennaio 2024`, il range
            slider sotto l'asse x e due pulsanti, `1w` per una settimana e `all` per il mese intero. Con una
            maschera sul mese, `px.line` e `update_xaxes` il grafico si costruisce in poche righe, e per vedere
            febbraio basta cambiare un numero. Nella linea si riconoscono i cicli giornalieri e il calo dei fine
            settimana.
        """,
        richiesta="""
            1. Tieni in `gennaio` le sole righe di `carico` relative a gennaio, usando una maschera sul mese della colonna `Date`.
            2. Costruisci `fig_carico` con `px.line`, con `Date` sull'asse x, `Total Load [MW]` sull'asse y, il titolo `Carico Nord, gennaio 2024` e `render_mode="svg"` come nel grafico dell'anno.
            3. Aggiungi con `update_xaxes` lo slider e i due pulsanti, il primo con `count=7` e `step="day"`.
        """,
        suggerimento="il mese di una colonna di date si legge con `.dt.month`, come nel notebook 08, e lo slider e i pulsanti si aggiungono con gli stessi due argomenti di `update_xaxes` usati per `fig_anno`.",
        starter="""
            mask_gennaio = ...
            gennaio = carico[mask_gennaio]

            bottoni_carico = [
                ...,
                dict(step="all"),
            ]
            fig_carico = px.line(...)
            fig_carico.update_xaxes(...)
            fig_carico.show()
        """,
        soluzione="""
            mask_gennaio = carico["Date"].dt.month == 1
            gennaio = carico[mask_gennaio]

            bottoni_carico = [
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(step="all"),
            ]
            fig_carico = px.line(gennaio, x="Date", y="Total Load [MW]", title="Carico Nord, gennaio 2024", render_mode="svg")
            fig_carico.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=bottoni_carico))
            fig_carico.show()
        """,
        verifica="""
            assert len(fig_carico.data) == 1 and len(fig_carico.data[0].x) == 2976, "❌ Serve una linea sola con le 2976 righe di gennaio: maschera su carico['Date'].dt.month"
            assert fig_carico.layout.title.text == "Carico Nord, gennaio 2024", "❌ Il titolo deve essere 'Carico Nord, gennaio 2024'"
            assert fig_carico.layout.xaxis.rangeslider.visible and len(fig_carico.layout.xaxis.rangeselector.buttons) == 2, "❌ Servono lo slider e due pulsanti: rangeslider_visible=True e rangeselector=dict(buttons=bottoni_carico)"
        """,
    )
    nb.esercizio(
        titolo="Il grafico del carico in HTML",
        scenario="""
            Un collega che non ha Python installato vuole esplorare con lo zoom e con lo slider il grafico di
            gennaio, `fig_carico`. Salvato con `write_html` nel file `carico_gennaio.html`, il grafico si apre
            con un doppio clic in qualunque browser e resta interattivo, e con l'opzione `include_plotlyjs="cdn"`
            pesa poco più di 100 kB, quindi si può mandare per email.
        """,
        richiesta="Salva `fig_carico` nel file `carico_gennaio.html` con `include_plotlyjs=\"cdn\"`, poi aprilo dalla cartella del notebook e controlla che lo zoom funzioni.",
        starter="""
            fig_carico.write_html(...)
        """,
        soluzione="""
            fig_carico.write_html("carico_gennaio.html", include_plotlyjs="cdn")
        """,
        verifica="""
            import os
            assert os.path.exists("carico_gennaio.html"), "❌ Il file carico_gennaio.html non c'è: controlla il nome in write_html"
            assert os.path.getsize("carico_gennaio.html") < 1_000_000, "❌ Il file è troppo grande: manca include_plotlyjs=\\"cdn\\""
        """,
        perche="Senza `include_plotlyjs=\"cdn\"` il file contiene al suo interno l'intera libreria Plotly, che pesa qualche megabyte, e in compenso si apre anche senza connessione. Con l'opzione `cdn` il file contiene solo i dati e la descrizione del grafico, e la libreria viene scaricata all'apertura.",
    )
    nb.esercizio(
        titolo="La distribuzione della potenza",
        scenario="""
            Vogliamo sapere per quante ore dell'anno la turbina texana produce poco e per quante lavora vicino
            alla sua potenza massima, attorno ai 3000 kW. Un istogramma della potenza risponde con un grafico
            solo, perché conta le ore che cadono in ogni intervallo, e in Plotly il numero esatto di ciascuna
            barra si legge passandoci sopra con il mouse. La barra più alta è quella vicino a 0 kW, segno che
            per molte ore la turbina produce poco o nulla.
        """,
        richiesta="Costruisci in `fig_potenza` l'istogramma della colonna `potenza_kw` di `turbina`, con 30 barre come l'istogramma del vento e il titolo `Distribuzione della potenza`.",
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
