"""10 · Grafici con Plotly."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="10",
        file="10_Plotly",
        titolo="Grafici con Plotly",
        blocco=3,
        giornata=2,
        intento="Il capo non legge i DataFrame, legge i grafici. Plotly Express ne fa uno per riga di codice, interattivo, e lo salva in un file HTML che si apre senza Python.",
        obiettivi=[
            "fare un grafico a linee, un istogramma e uno scatter con Plotly Express",
            "confrontare più serie e navigarle con slider e selettore di intervallo",
            "esportare un grafico in HTML da mandare a chi non ha Python",
        ],
        tempo={"base": 40, "avanzata": 30},
        dati=["prezzi_zonali_2025_settimana.csv", "TexasTurbine.csv", "load_total_north_hourly_2024.xlsx"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("I quattro pezzi di un grafico", intro="""
        Un grafico Plotly è fatto di quattro pezzi.

        - I dati: un DataFrame.
        - Il mapping: quale colonna va sulla x, quale sulla y, quale decide il colore.
        - Le tracce: le linee o i punti che ne risultano.
        - Il layout: titolo, assi, dimensioni.

        Plotly Express, `px`, costruisce i primi tre con una chiamata sola. Ripartiamo dai prezzi zonali.
    """)
    nb.code("""
        import pandas as pd
        import plotly.express as px

        prezzi = pd.read_csv("../Dati/prezzi_zonali_2025_settimana.csv")
        prezzi["timestamp"] = pd.to_datetime(prezzi["timestamp"])
        mask_nord = prezzi["zona"] == "NORD"
        nord = prezzi[mask_nord]
        nord.head(3)
    """)
    nb.md("""
        Dati, x, y: il grafico a linee più semplice che esista. `fig` è l'oggetto grafico; `fig.show()`
        lo disegna. Con il mouse sopra la linea compaiono i valori, trascinando si ingrandisce una zona,
        con un doppio clic si torna indietro.
    """)
    nb.code("""
        fig = px.line(nord, x="timestamp", y="eur_mwh")
        fig.show()
    """)
    nb.md("""
        Dentro `fig` ci sono le tracce, `fig.data`, e il layout, `fig.layout`. Una linea è una traccia
        di tipo `scatter` disegnata in modalità linee: in Plotly linee e punti sono la stessa famiglia.
    """)
    nb.code("""
        print(len(fig.data), fig.data[0].type, fig.data[0].mode)
    """)
    nb.box("nota", """
        In un notebook basta anche scrivere `fig` come ultima riga della cella. `fig.show()` funziona
        anche in uno script, quindi è l'abitudine da prendere.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Linee con `px.line`", intro="""
        Sei zone, una linea ciascuna: `color="zona"` fa una traccia per ogni valore distinto della
        colonna e aggiunge la legenda. `title` mette il titolo.
    """)
    nb.code("""
        fig = px.line(prezzi, x="timestamp", y="eur_mwh", color="zona", title="Prezzi zonali, 2-8 giugno 2025")
        fig.show()
    """)
    nb.md("""
        La legenda è viva: un clic su una zona la nasconde, un doppio clic la isola. La SICI sopra a
        tutte e il NORD con il buco del 4 giugno si vedono senza calcolare niente.
    """)
    nb.md("""
        Le etichette degli assi sono i nomi delle colonne, e `eur_mwh` sull'asse di un grafico per il
        capo non si può vedere. `labels` le traduce con un dizionario, senza rinominare il DataFrame.
    """)
    nb.code("""
        etichette = {"timestamp": "Ora", "eur_mwh": "Prezzo [€/MWh]", "zona": "Zona"}

        fig = px.line(prezzi, x="timestamp", y="eur_mwh", color="zona", labels=etichette,
                      title="Prezzi zonali, 2-8 giugno 2025")
        fig.show()
    """)
    nb.prova_tu(
        richiesta="""
            Disegna in `fig_sud` il prezzo della sola zona SUD: titolo `Zona SUD`, asse y etichettato
            `Prezzo [€/MWh]`.
        """,
        starter="""
            mask_sud = ...
            fig_sud = px.line(...)
            fig_sud.show()
        """,
        soluzione="""
            mask_sud = prezzi["zona"] == "SUD"
            fig_sud = px.line(prezzi[mask_sud], x="timestamp", y="eur_mwh", title="Zona SUD",
                              labels={"eur_mwh": "Prezzo [€/MWh]"})
            fig_sud.show()
        """,
        verifica="""
            assert len(fig_sud.data) == 1, "❌ Una zona sola: filtra il DataFrame prima di passarlo a px.line"
            assert fig_sud.layout.title.text == "Zona SUD", "❌ Il titolo va passato con title='Zona SUD'"
            assert fig_sud.layout.yaxis.title.text == "Prezzo [€/MWh]", "❌ L'etichetta dell'asse y si cambia con labels={'eur_mwh': ...}"
        """,
    )

    # ------------------------------------------------------------------ 3
    nb.sezione("Istogrammi e punti", intro="""
        Un istogramma risponde a "come sono distribuiti i valori": quante ore sotto i 90 €/MWh, quante
        sopra i 130. Serve solo la x; l'altezza delle barre la conta Plotly. `nbins` è il numero di
        barre, indicativo.
    """)
    nb.code("""
        fig = px.histogram(prezzi, x="eur_mwh", nbins=30, labels=etichette, title="Distribuzione dei prezzi orari")
        fig.show()
    """)
    nb.md("""
        Con `color` le distribuzioni si separano per zona; `barmode="overlay"` le sovrappone invece di
        impilarle e `opacity` le rende trasparenti, così si vede chi sta dove.
    """)
    nb.code("""
        fig = px.histogram(prezzi, x="eur_mwh", color="zona", nbins=30, barmode="overlay", opacity=0.6,
                           labels=etichette, title="Distribuzione dei prezzi per zona")
        fig.show()
    """)
    nb.md("""
        Lo scatter mette un punto per riga e serve a vedere la relazione tra due numeri. Il caso da
        manuale è la turbina: vento sulla x, potenza sulla y. Il timestamp lo costruiamo come nel
        notebook sulle date e rinominiamo due colonne, perché `Wind speed | (m/s)` è scomodo da scrivere.
    """)
    nb.code("""
        turbina = pd.read_csv("../Dati/TexasTurbine.csv")
        turbina["timestamp"] = pd.to_datetime("2023 " + turbina["Time stamp"], format="%Y %b %d, %I:%M %p")
        turbina = turbina.rename(columns={"System power generated | (kW)": "potenza_kw", "Wind speed | (m/s)": "vento_ms"})
        turbina.head(3)
    """)
    nb.code("""
        fig = px.scatter(turbina, x="vento_ms", y="potenza_kw", opacity=0.3,
                         labels={"vento_ms": "Vento [m/s]", "potenza_kw": "Potenza [kW]"},
                         title="Curva di potenza della turbina")
        fig.show()
    """)
    nb.md("""
        La S è la curva di potenza: sotto i 3 m/s la turbina non parte, poi sale, poi satura a 3 MW. Un
        punto con vento buono e potenza zero sarebbe un fermo o una misura da controllare: qui non ce ne
        sono, e in un grafico lo si vede in un secondo, in una tabella di 8760 righe mai. `opacity` serve
        a far vedere dove i punti si accumulano.
    """)
    nb.prova_tu(
        richiesta="""
            Com'è distribuito il vento in Texas? Costruisci in `fig_vento` l'istogramma della colonna
            `vento_ms` con 40 barre.
        """,
        starter="""
            fig_vento = px.histogram(...)
            fig_vento.show()
        """,
        soluzione="""
            fig_vento = px.histogram(turbina, x="vento_ms", nbins=40, labels={"vento_ms": "Vento [m/s]"})
            fig_vento.show()
        """,
        verifica="""
            assert fig_vento.data[0].type == "histogram", "❌ Serve px.histogram, non px.line o px.scatter"
            assert len(fig_vento.data) == 1, "❌ Una sola distribuzione: niente color"
            assert fig_vento.data[0].nbinsx == 40, "❌ Servono 40 barre: nbins=40"
            assert max(fig_vento.data[0].x) == turbina["vento_ms"].max(), "❌ Sull'asse x va la colonna vento_ms"
        """,
    )

    # ------------------------------------------------------------------ 4
    nb.sezione("Più serie e navigazione", intro="""
        I prezzi sono in formato long: una riga per ogni coppia (ora, zona), e `color` separa le serie.
        Terna è in formato wide: carico e previsione sono due colonne della stessa riga. Per il wide si
        passa a `y` una lista di colonne. Carichiamo il 2024 con la pulizia del notebook sulle date e
        teniamo febbraio.
    """)
    nb.code("""
        carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico = carico.sort_values("Date").drop_duplicates(subset="Date")

        mask_febbraio = carico["Date"].dt.month == 2
        febbraio = carico[mask_febbraio]
        len(febbraio)
    """)
    nb.code("""
        fig = px.line(febbraio, x="Date", y=["Total Load [MW]", "Forecast Total Load [MW]"],
                      title="Carico Nord, febbraio 2024")
        fig.show()
    """)
    nb.md("""
        Con la `y` a lista Plotly chiama la serie `variable` e il valore `value`: sono i nomi da mettere
        in `labels`. Il layout si ritocca dopo con `fig.update_layout`: altezza, titolo della legenda,
        etichetta dell'asse y.
    """)
    nb.code("""
        fig = px.line(febbraio, x="Date", y=["Total Load [MW]", "Forecast Total Load [MW]"],
                      labels={"Date": "Data", "value": "MW", "variable": "Serie"}, title="Carico Nord, febbraio 2024")
        fig.update_layout(height=450, legend_title_text="", yaxis_title="Carico [MW]")
        fig.show()
    """)
    nb.box("approfondimento", """
        L'altra strada è portare il DataFrame in formato long con `melt`, e poi usare `color` come con i
        prezzi. Utile quando le colonne da confrontare sono tante o cambiano:

        ```python
        lungo = febbraio.melt(id_vars="Date", value_vars=["Total Load [MW]", "Forecast Total Load [MW]"],
                              var_name="serie", value_name="mw")
        px.line(lungo, x="Date", y="mw", color="serie")
        ```
    """, titolo="Da wide a long con melt")
    nb.md("""
        Un mese di quarti d'ora sono 2784 punti: troppi per leggerli tutti insieme. Lo slider sotto il
        grafico e i bottoni del `rangeselector` servono a navigarli. I bottoni si descrivono con una
        lista di dizionari: `count` e `step` dicono quanto indietro, `label` cosa c'è scritto.
    """)
    nb.code("""
        bottoni = [
            dict(count=1, step="day", stepmode="backward", label="1 giorno"),
            dict(count=7, step="day", stepmode="backward", label="1 settimana"),
            dict(step="all", label="tutto"),
        ]
        fig.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=bottoni))
        fig.show()
    """)
    nb.box("nota", """
        Il `rangeselector` nessuno lo sa a memoria: si copia da qui o dalla documentazione. Quello che va
        ricordato è il nome, per sapere cosa cercare.
    """)
    nb.prova_tu(
        richiesta="""
            Costruisci in `fig_marzo` il grafico del solo `Total Load [MW]` di marzo 2024, con lo slider
            sotto l'asse x.
        """,
        starter="""
            mask_marzo = ...
            fig_marzo = px.line(...)
            fig_marzo.update_xaxes(...)
            fig_marzo.show()
        """,
        soluzione="""
            mask_marzo = carico["Date"].dt.month == 3
            fig_marzo = px.line(carico[mask_marzo], x="Date", y="Total Load [MW]", title="Carico Nord, marzo 2024")
            fig_marzo.update_xaxes(rangeslider_visible=True)
            fig_marzo.show()
        """,
        verifica="""
            assert len(fig_marzo.data) == 1, "❌ Una serie sola: y='Total Load [MW]' come stringa, non come lista"
            assert fig_marzo.layout.xaxis.rangeslider.visible is True, "❌ Lo slider si accende con fig.update_xaxes(rangeslider_visible=True)"
        """,
    )

    # ------------------------------------------------------------------ 5
    nb.sezione("Esportare", intro="""
        `fig.write_html` salva il grafico in un file che si apre con qualunque browser, interattività
        compresa: chi lo riceve non ha bisogno di Python. Il file finisce nella cartella del notebook.
    """)
    nb.code("""
        from pathlib import Path

        fig.write_html("carico_febbraio.html")
        print(f"{Path('carico_febbraio.html').stat().st_size / 1_000_000:.1f} MB")
    """)
    nb.md("""
        Cinque MB per un grafico: dentro c'è tutta la libreria Plotly, così il file funziona anche senza
        rete. Con `include_plotlyjs="cdn"` la libreria viene scaricata all'apertura e il file scende a
        poche centinaia di KB, ma chi lo apre deve essere connesso.
    """)
    nb.code("""
        fig.write_html("carico_febbraio_leggero.html", include_plotlyjs="cdn")
        print(f"{Path('carico_febbraio_leggero.html').stat().st_size / 1_000:.0f} KB")
    """)
    nb.box("nota", """
        Per un'immagine fissa c'è `fig.write_image("grafico.png")`, che però vuole una libreria in più
        (`kaleido`, con `uv add`). Qui basta l'HTML: nessuno deve installare niente per aprirlo.
    """)
    nb.box("ricorda", """
        - `px.line`, `px.histogram`, `px.scatter`: stessi argomenti, `(df, x=, y=, color=, labels=, title=)`, e restituiscono `fig`.
        - `fig.update_layout(...)` e `fig.update_xaxes(...)` ritoccano dopo; `fig.show()` disegna.
        - `fig.write_html("nome.html")` per chi non ha Python.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il grafico per il capo",
        scenario="""
            Il capo vuole entro stasera il grafico del carico del Nord di febbraio 2024, da aprire sul suo
            portatile in riunione, e sul suo portatile non c'è Python. Vuole una linea sola, poter
            zoomare su un giorno, e un titolo che si capisca.
        """,
        richiesta="""
            1. Da `febbraio` costruisci `fig_capo`: linea del solo `Total Load [MW]` sulla `Date`, titolo
               `Carico Nord, febbraio 2024`, asse y etichettato `Carico [MW]`.
            2. Accendi lo slider sotto l'asse x.
            3. Salvalo in `carico_febbraio_capo.html`, nella cartella del notebook.
        """,
        suggerimento="L'etichetta dell'asse si cambia con `labels={\"Total Load [MW]\": \"Carico [MW]\"}` oppure dopo, con `update_layout(yaxis_title=...)`.",
        starter="""
            fig_capo = px.line(...)
            fig_capo.update_xaxes(...)
            fig_capo.write_html(...)
            fig_capo.show()
        """,
        soluzione="""
            fig_capo = px.line(febbraio, x="Date", y="Total Load [MW]", title="Carico Nord, febbraio 2024",
                               labels={"Total Load [MW]": "Carico [MW]", "Date": "Data"})
            fig_capo.update_xaxes(rangeslider_visible=True)
            fig_capo.write_html("carico_febbraio_capo.html")
            fig_capo.show()
        """,
        verifica="""
            from pathlib import Path
            assert len(fig_capo.data) == 1, "❌ Una linea sola: y='Total Load [MW]', senza la previsione"
            assert fig_capo.layout.title.text == "Carico Nord, febbraio 2024", "❌ Il titolo deve essere esattamente 'Carico Nord, febbraio 2024'"
            assert fig_capo.layout.yaxis.title.text == "Carico [MW]", "❌ L'asse y deve dire 'Carico [MW]': labels oppure update_layout(yaxis_title=...)"
            assert fig_capo.layout.xaxis.rangeslider.visible is True, "❌ Manca lo slider: update_xaxes(rangeslider_visible=True)"
            assert Path("carico_febbraio_capo.html").exists(), "❌ Il file carico_febbraio_capo.html non c'è: write_html con quel nome esatto"
        """,
        perche="`labels` sistema le etichette nel momento in cui si crea il grafico; `update_layout` le cambia dopo. Stesso risultato, scegli quello che ti viene più naturale.",
    )
    nb.esercizio(
        titolo="Zone a confronto",
        bis=True,
        scenario="""
            Sara, del trading, vuole vedere NORD e SICI sullo stesso grafico, e solo quelle due:
            con sei linee non ci capisce niente. Il file HTML lo allega alla mail del lunedì.
        """,
        richiesta="""
            1. Filtra `prezzi` sulle zone NORD e SICI in `due_zone`.
            2. Costruisci `fig_zone`: una linea per zona, titolo `NORD e SICI a confronto`, asse y `Prezzo [€/MWh]`.
            3. Salvalo in `zone_confronto.html`.
        """,
        suggerimento="`isin([\"NORD\", \"SICI\"])` per il filtro, `color=\"zona\"` per le due linee.",
        starter="""
            mask_zone = ...
            due_zone = prezzi[mask_zone]

            fig_zone = px.line(...)
            fig_zone.write_html(...)
            fig_zone.show()
        """,
        soluzione="""
            mask_zone = prezzi["zona"].isin(["NORD", "SICI"])
            due_zone = prezzi[mask_zone]

            fig_zone = px.line(due_zone, x="timestamp", y="eur_mwh", color="zona", labels=etichette,
                               title="NORD e SICI a confronto")
            fig_zone.write_html("zone_confronto.html")
            fig_zone.show()
        """,
        verifica="""
            from pathlib import Path
            assert len(fig_zone.data) == 2, "❌ Due linee, non sei: filtra le zone prima di passare il DataFrame a px.line"
            assert {traccia.name for traccia in fig_zone.data} == {"NORD", "SICI"}, "❌ Le due tracce devono essere NORD e SICI: color='zona' sul DataFrame filtrato"
            assert fig_zone.layout.title.text == "NORD e SICI a confronto", "❌ Controlla il titolo, deve essere esatto"
            assert Path("zone_confronto.html").exists(), "❌ Manca il file zone_confronto.html"
        """,
    )
    nb.esercizio(
        titolo="Vento e potenza",
        scenario="""
            Elena, che segue l'eolico, deve presentare la turbina texana al comitato investimenti:
            vuole la curva di potenza (vento contro potenza) e la distribuzione della potenza prodotta,
            per far vedere quante ore la macchina lavora a pieno regime e quante sta ferma.
        """,
        richiesta="""
            1. `fig_curva`: scatter di `turbina` con il vento sulla x e la potenza sulla y, con `opacity=0.3`
               e titolo `Curva di potenza`.
            2. `fig_dist`: istogramma della colonna `potenza_kw`, 30 barre, titolo `Distribuzione della potenza`.
        """,
        suggerimento="Le colonne si chiamano `vento_ms` e `potenza_kw`: le abbiamo rinominate noi.",
        starter="""
            fig_curva = px.scatter(...)
            fig_curva.show()

            fig_dist = px.histogram(...)
            fig_dist.show()
        """,
        soluzione="""
            fig_curva = px.scatter(turbina, x="vento_ms", y="potenza_kw", opacity=0.3, title="Curva di potenza",
                                   labels={"vento_ms": "Vento [m/s]", "potenza_kw": "Potenza [kW]"})
            fig_curva.show()

            fig_dist = px.histogram(turbina, x="potenza_kw", nbins=30, title="Distribuzione della potenza",
                                    labels={"potenza_kw": "Potenza [kW]"})
            fig_dist.show()
        """,
        verifica="""
            assert len(fig_curva.data) == 1 and "scatter" in fig_curva.data[0].type, "❌ fig_curva: px.scatter con una sola traccia (niente color)"
            assert fig_curva.data[0].marker.opacity == 0.3, "❌ fig_curva: passa opacity=0.3 a px.scatter"
            assert fig_dist.data[0].type == "histogram", "❌ fig_dist: serve px.histogram"
            assert fig_dist.layout.title.text == "Distribuzione della potenza", "❌ fig_dist: controlla il titolo"
        """,
        perche="Lo scatter con 8760 punti è illeggibile senza `opacity`: dove i punti si sovrappongono il colore si scurisce, e la curva emerge da sola.",
        passo_in_piu=dict(
            testo="""
                Il vento cambia con le stagioni? Crea in `turbina` una colonna `mese` con il nome del
                mese (`turbina["timestamp"].dt.month_name()`, come `day_name()` dava il giorno) e rifai lo
                scatter in `fig_mesi` con `color="mese"`: una traccia per mese, e la legenda per accenderli
                uno alla volta.
            """,
            starter="""
                turbina["mese"] = ...
                fig_mesi = px.scatter(...)
                fig_mesi.show()
            """,
            soluzione="""
                turbina["mese"] = turbina["timestamp"].dt.month_name()
                fig_mesi = px.scatter(turbina, x="vento_ms", y="potenza_kw", color="mese", opacity=0.4,
                                      title="Curva di potenza per mese")
                fig_mesi.show()
            """,
            verifica="""
                assert len(fig_mesi.data) == 12, "❌ fig_mesi: una traccia per mese, dodici in tutto; il colore deve venire dal nome del mese"
                assert "January" in {traccia.name for traccia in fig_mesi.data}, "❌ fig_mesi: la colonna mese deve contenere il nome del mese (dt.month_name())"
            """,
        ),
    )
    nb.esercizio(
        titolo="Temperatura e potenza",
        bis=True,
        scenario="""
            Chi gestisce la manutenzione sospetta che col caldo la turbina renda meno. Vuole vedere la
            temperatura dell'aria contro la potenza prodotta, e come sono distribuite le temperature
            nell'anno, prima di chiedere un controllo al costruttore.
        """,
        richiesta="""
            1. Rinomina in `turbina` la colonna `Air temperature | ('C)` in `temperatura_c`.
            2. `fig_temp`: scatter con la temperatura sulla x e la potenza sulla y, con `opacity=0.3`
               e titolo `Temperatura e potenza`.
            3. `fig_temp_dist`: istogramma della colonna `temperatura_c`, 30 barre, titolo
               `Distribuzione della temperatura`.
        """,
        suggerimento="Il nome della colonna da cambiare si copia dall'intestazione del file: `rename(columns={...})` come con il vento.",
        starter="""
            turbina = turbina.rename(columns=...)

            fig_temp = px.scatter(...)
            fig_temp.show()

            fig_temp_dist = px.histogram(...)
            fig_temp_dist.show()
        """,
        soluzione="""
            turbina = turbina.rename(columns={"Air temperature | ('C)": "temperatura_c"})

            fig_temp = px.scatter(turbina, x="temperatura_c", y="potenza_kw", opacity=0.3, title="Temperatura e potenza",
                                  labels={"temperatura_c": "Temperatura [°C]", "potenza_kw": "Potenza [kW]"})
            fig_temp.show()

            fig_temp_dist = px.histogram(turbina, x="temperatura_c", nbins=30, title="Distribuzione della temperatura",
                                         labels={"temperatura_c": "Temperatura [°C]"})
            fig_temp_dist.show()
        """,
        verifica="""
            assert "temperatura_c" in turbina.columns, "❌ La colonna va rinominata in temperatura_c con rename(columns={...})"
            assert len(fig_temp.data) == 1 and "scatter" in fig_temp.data[0].type, "❌ fig_temp: px.scatter con una sola traccia (niente color)"
            assert fig_temp.data[0].marker.opacity == 0.3, "❌ fig_temp: passa opacity=0.3 a px.scatter"
            assert max(fig_temp.data[0].x) == turbina["temperatura_c"].max(), "❌ fig_temp: la temperatura va sull'asse x"
            assert fig_temp_dist.data[0].type == "histogram", "❌ fig_temp_dist: serve px.histogram"
            assert fig_temp_dist.data[0].nbinsx == 30, "❌ fig_temp_dist: servono 30 barre, nbins=30"
            assert max(fig_temp_dist.data[0].x) == turbina["temperatura_c"].max(), "❌ fig_temp_dist: sull'asse x va la colonna temperatura_c"
            assert fig_temp_dist.layout.title.text == "Distribuzione della temperatura", "❌ fig_temp_dist: controlla il titolo"
        """,
        perche="Lo scatter fa vedere subito se due numeri si muovono insieme. Qui la nuvola di punti non ha nessuna forma: la temperatura non spiega la potenza, che segue il vento.",
    )
    return nb
