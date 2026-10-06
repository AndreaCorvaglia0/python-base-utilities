"""12 · Capstone: il carico del Nord e la temperatura."""

from nbkit import Notebook

DA_SOLI = "*Senza Copilot: qui conta capire il meccanismo.*"
DETTAGLIO = "*Copilot solo per il dettaglio, titoli, etichette e colori: la logica la scriviamo noi.*"
CHAT = "*Copilot in chat, per capire: davanti a un errore \"spiegami\", mai \"risolvilo\".*"


def step(nb: Notebook, titolo: str, scenario: str, soluzione: str, verifica: str,
         base: dict, avanzata: dict, perche: str | None = None, rete: bool = False) -> None:
    """Lo stesso step per le due aule: stessa soluzione e verifica, richiesta e scheletro diversi."""
    nb.esercizio(
        titolo=titolo, scenario=scenario, richiesta=base["richiesta"], suggerimento=base.get("suggerimento"),
        starter=base["starter"], soluzione=soluzione, verifica=verifica, perche=perche, aula="base", rete=rete,
    )
    nb.esercizio(
        titolo=titolo, scenario=scenario, richiesta=avanzata["richiesta"], starter=avanzata["starter"],
        soluzione=soluzione, verifica=verifica, perche=perche, aula="avanzata", rete=rete,
    )
    if avanzata.get("bloccato"):
        nb.box("nota", avanzata["bloccato"], titolo="Se sei bloccato", aula="avanzata")


def costruisci() -> Notebook:
    nb = Notebook(
        num="12",
        file="12_Capstone",
        titolo="Capstone: il carico del Nord e la temperatura",
        blocco=4,
        giornata=2,
        intento="Due anni di carico elettrico della zona Nord e la temperatura di Milano: dalla domanda del capo al grafico che risponde, passando per tutto quello che abbiamo imparato.",
        obiettivi=[
            "caricare, pulire e aggregare una serie temporale reale, con i suoi difetti",
            "unire due fonti diverse e leggere la relazione tra carico e temperatura",
            "chiudere un'analisi con numeri, frasi e un grafico da mandare a chi non ha Python",
        ],
        tempo={"base": 120, "avanzata": 130},
        dati=["load_total_north_hourly_2024.xlsx", "load_total_north_hourly_2025.xlsx", "fallback/meteo_milano_2024_2025.json"],
        etichetta_esercizio="Step",
        prefisso_esercizi="",
    )

    # ------------------------------------------------------------------ scenario
    nb.md("""
        Lunedì mattina, riunione di pianificazione. Il capo: "Il carico del Nord dipende dalla temperatura?
        Quanto cala nel weekend? E l'estate pesa più dell'inverno, da noi?". Abbiamo i file di Terna con due
        anni di carico della zona Nord e un'API meteo. Niente previsioni: prima bisogna capire i dati.
    """)
    nb.md("""
        Otto step, uno per sezione. Ogni sezione si apre con una riga su Copilot: senza, dove conta capire
        il meccanismo; per il dettaglio, dove può sistemare titoli ed etichette; in chat, quando qualcosa
        non torna. Le verifiche controllano forma e intervalli: il resto lo controlli tu, guardando l'output.
    """)
    nb.md("""
        Lungo la strada scopriremo la frequenza vera dei dati, quanti picchi ha una giornata, di quanto
        cala il weekend, se al Nord pesa più il caldo o il freddo, che forma ha la relazione tra carico e
        temperatura e cosa combina l'ora legale due volte l'anno.
    """)

    # ------------------------------------------------------------------ 1
    nb.sezione("I dati di Terna", intro=f"""
        {DA_SOLI}

        Due file Excel, uno per anno, con la stessa struttura: `Date`, `Total Load [MW]`,
        `Forecast Total Load [MW]`, `Bidding Zone`. Ci serve una tabella sola, con due colonne dai nomi
        corti e le righe in ordine di tempo. Il forecast di Terna lo lasciamo a Terna.
    """)
    soluzione_1 = """
        import pandas as pd
        import plotly.express as px

        carico_2024 = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico_2025 = pd.read_excel("../Dati/load_total_north_hourly_2025.xlsx")
        carico = pd.concat([carico_2024, carico_2025], ignore_index=True)

        carico = carico.drop(columns=["Forecast Total Load [MW]", "Bidding Zone"])
        carico = carico.rename(columns={"Date": "data", "Total Load [MW]": "mw"})
        carico["data"] = pd.to_datetime(carico["data"])
        carico = carico.sort_values("data").reset_index(drop=True)
        carico.info()
    """
    verifica_1 = """
        assert set(carico.columns) == {"data", "mw"}, "❌ carico: due colonne sole, data e mw"
        assert len(carico) == 70176, "❌ carico: 70176 righe, i due anni uno sotto l'altro senza togliere nulla per ora"
        assert str(carico["data"].dtype).startswith("datetime64"), "❌ La colonna data deve essere datetime"
        assert carico["data"].is_monotonic_increasing, "❌ Ordina per data: i file arrivano al contrario"
    """
    step(
        nb, titolo="Caricare e mettere in ordine",
        scenario="I file sono nella cartella `../Dati/`. Guarda le prime righe di uno dei due prima di partire: c'è una sorpresa sull'ordine.",
        soluzione=soluzione_1, verifica=verifica_1,
        base=dict(
            richiesta="""
                1. Leggi i due file in `carico_2024` e `carico_2025` con `pd.read_excel`.
                2. Mettili uno sotto l'altro in `carico` con `pd.concat`, indice rifatto da 0.
                3. Togli le colonne `Forecast Total Load [MW]` e `Bidding Zone`; rinomina `Date` in `data` e
                   `Total Load [MW]` in `mw`.
                4. Assicurati che `data` sia datetime, ordina per `data` e rifai l'indice. Chiudi con
                   `carico.info()`.
            """,
            suggerimento="`read_excel` legge le date già come datetime; `to_datetime` qui è una cintura di sicurezza.",
            starter="""
                import pandas as pd
                import plotly.express as px

                # 1. i due file, uno per anno
                carico_2024 = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
                carico_2025 = ...
                # 2. uno sotto l'altro
                carico = pd.concat([...], ignore_index=True)

                # 3. solo data e carico, con nomi corti
                carico = carico.drop(columns=[...])
                carico = carico.rename(columns={...})
                # 4. date vere, ordine cronologico, indice da 0
                carico["data"] = pd.to_datetime(carico["data"])
                carico = ...
                carico.info()
            """,
        ),
        avanzata=dict(
            richiesta="""
                Costruisci `carico`: i due anni in una tabella sola, due colonne `data` (datetime) e `mw`,
                righe in ordine cronologico con indice da 0, senza il forecast e la zona.
                Risultato atteso: `carico.info()` con 70176 righe e due colonne.
            """,
            starter="""
                import pandas as pd
                import plotly.express as px

                carico = ...
                carico.info()
            """,
            bloccato="""
                `pd.concat([a, b], ignore_index=True)` mette le righe una sotto l'altra; `drop(columns=...)`
                e `rename(columns={...})` sistemano le colonne; `sort_values` e `reset_index(drop=True)`
                l'ordine. Un metodo per riga: si legge meglio e si sbaglia meno.
            """,
        ),
    )

    # ------------------------------------------------------------------ 2
    nb.sezione("L'ora legale", intro=f"""
        {DA_SOLI}

        Il file si chiama `hourly`. Prima di fidarci del nome, misuriamo il passo tra un timestamp e il
        successivo: lo abbiamo già fatto sui prezzi zonali.
    """)
    nb.prova_tu(
        richiesta="""
            In `passi` metti la differenza tra ogni timestamp e il precedente, in `frequenza` quante volte
            compare ogni valore. Qual è il passo vero? E cosa sono gli altri due valori?
        """,
        starter="""
            passi = carico["data"].diff()
            frequenza = ...
            frequenza
        """,
        soluzione="""
            passi = carico["data"].diff()
            frequenza = passi.value_counts()
            frequenza
        """,
        verifica="""
            assert frequenza.idxmax() == pd.Timedelta("15min"), "❌ Il passo più frequente deve essere di 15 minuti: value_counts su diff"
            assert frequenza[pd.Timedelta(0)] == 8, "❌ Dovrebbero esserci 8 passi di zero minuti: timestamp ripetuti"
            assert frequenza[pd.Timedelta("1h15min")] == 2, "❌ Dovrebbero esserci 2 passi di un'ora e un quarto: buchi"
        """,
    )
    nb.md("""
        Quartorario, non orario: 96 valori al giorno. Otto passi di zero minuti sono timestamp ripetuti;
        due passi di un'ora e un quarto sono buchi di quattro quartorari. Vediamo dove stanno.
    """)
    soluzione_2 = """
        mask_doppi = carico["data"].duplicated(keep=False)
        duplicati = carico[mask_doppi]
        display(duplicati)

        quartorari_giorno = carico.groupby(carico["data"].dt.date).size()
        giorni_strani = quartorari_giorno[quartorari_giorno != 96]
        display(giorni_strani)

        carico = carico.drop_duplicates(subset="data")
        carico = carico.reset_index(drop=True)
        carico.isna().sum()
    """
    verifica_2 = """
        assert len(duplicati) == 16, "❌ duplicati: 16 righe, cioè 4 timestamp doppi per anno in 2 copie (keep=False le tiene tutte)"
        assert set(pd.to_datetime(list(giorni_strani.index)).strftime("%Y-%m-%d")) == {"2024-03-31", "2024-10-27", "2025-03-30", "2025-10-26"}, "❌ giorni_strani: le ultime domeniche di marzo e di ottobre dei due anni"
        assert len(carico) == 70168, "❌ carico: 70176 righe meno gli 8 duplicati"
        assert carico["data"].duplicated().sum() == 0, "❌ Ci sono ancora timestamp ripetuti"
        assert carico["mw"].isna().sum() == 0, "❌ Non dovrebbero esserci valori mancanti"
    """
    step(
        nb, titolo="Pulizia temporale",
        scenario="Due anni, otto doppioni e otto quartorari che mancano: sempre negli stessi due giorni dell'anno. Prima di togliere qualcosa, guardiamo che giorni sono.",
        soluzione=soluzione_2, verifica=verifica_2,
        perche="Tenere la prima occorrenza basta: le due copie di ogni quartorario d'ottobre hanno valori quasi uguali. Il buco di marzo resta: quell'ora non è mai esistita.",
        base=dict(
            richiesta="""
                1. In `duplicati` metti le righe con un timestamp ripetuto, tutte le copie
                   (`duplicated(keep=False)`). Che giorno è? Che ora?
                2. Conta i quartorari di ogni giorno in `quartorari_giorno` e in `giorni_strani` tieni i
                   giorni che non ne hanno 96. Riconosci le date?
                3. Togli i duplicati con `drop_duplicates(subset="data")`, poi rifai l'indice.
                4. Chiudi con il conteggio dei valori mancanti per colonna: devono essere zero. Il buco di
                   marzo resta: perché va bene così?
            """,
            suggerimento="Nell'ultima domenica di ottobre le 2:00 esistono due volte; nell'ultima di marzo non esistono.",
            starter="""
                # 1. le righe con timestamp ripetuto, tutte le copie
                mask_doppi = carico["data"].duplicated(keep=False)
                duplicati = carico[...]
                display(duplicati)

                # 2. quanti quartorari ha ogni giorno? uno normale ne ha 96
                quartorari_giorno = carico.groupby(carico["data"].dt.date).size()
                giorni_strani = quartorari_giorno[...]
                display(giorni_strani)

                # 3. via i duplicati, tenendo la prima occorrenza, poi indice da 0
                carico = carico.drop_duplicates(subset=...)
                carico = carico.reset_index(drop=True)
                # 4. valori mancanti per colonna
                carico.isna().sum()
            """,
        ),
        avanzata=dict(
            richiesta="""
                Trova i timestamp ripetuti in `duplicati` (tutte le copie) e, in `giorni_strani`, i giorni
                che non hanno 96 quartorari (`quartorari_giorno` è il conteggio per giorno). Poi lascia in
                `carico` una riga per timestamp, indice da 0, e conta i valori mancanti.
                Risultato atteso: 16 righe in `duplicati` (8 timestamp, due copie ciascuno), 4 giorni
                strani, 70168 righe pulite, zero valori mancanti.
                Domanda: perché proprio quei quattro giorni, e perché il buco di marzo non va riempito?
            """,
            starter="""
                duplicati = ...
                quartorari_giorno = ...
                giorni_strani = ...

                carico = ...
                carico.isna().sum()
            """,
            bloccato="""
                `duplicated(keep=False)` segna tutte le copie, `drop_duplicates(subset="data")` tiene la
                prima. Per contare per giorno: `groupby(carico["data"].dt.date).size()`.
            """,
        ),
    )
    with nb.solo("avanzata"):
        nb.md("""
            Perché proprio quelle date? Chiediamolo a pandas. Questa cella dà errore apposta: leggiamolo
            dal basso.
        """)
        nb.code('carico["data"].dt.tz_localize("Europe/Rome", ambiguous="infer")', errore=True)
        nb.md("""
            `AmbiguousTimeError`: nel fuso italiano le 2:00 dell'ultima domenica di ottobre esistono due
            volte, e dalla copia rimasta pandas non capisce quale delle due sia. Per questa analisi basta
            l'ora locale, senza fuso: i doppioni li abbiamo già tolti e il resto lo lasciamo stare.
        """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Un anno in un grafico", intro=f"""
        {DA_SOLI}

        Settantamila punti non si guardano: li raggruppiamo per giorno. `resample("D")` lavora su un
        indice temporale e raggruppa per giorno di calendario, come un `groupby` che sa che i giorni sono
        consecutivi; il risultato ha la data come indice e `reset_index()` la riporta colonna.
    """)
    soluzione_3 = """
        indice_tempo = carico.set_index("data")
        giornaliero = indice_tempo["mw"].resample("D").sum().reset_index()
        giornaliero["mwh"] = giornaliero["mw"] / 4
        giornaliero = giornaliero.drop(columns="mw")

        fig = px.line(giornaliero, x="data", y="mwh", title="Energia giornaliera, zona Nord",
                      labels={"mwh": "MWh", "data": ""})
        fig.update_xaxes(rangeslider_visible=True)
        fig.show()

        estremi = giornaliero.loc[[giornaliero["mwh"].idxmin(), giornaliero["mwh"].idxmax()]]
        estremi
    """
    verifica_3 = """
        assert set(giornaliero.columns) == {"data", "mwh"}, "❌ giornaliero: due colonne, data e mwh"
        assert len(giornaliero) == 731, "❌ giornaliero: 366 + 365 giorni"
        assert giornaliero["mwh"].between(250_000, 700_000).all(), "❌ mwh fuori scala: hai diviso per 4 i MW quartorari?"
        assert len(estremi) == 2, "❌ estremi: due righe, il giorno più leggero e quello più pesante"
        assert estremi["mwh"].min() < 300_000 and estremi["mwh"].max() > 640_000, "❌ estremi: il minimo sta sotto i 300.000 MWh, il massimo sopra i 640.000"
    """
    step(
        nb, titolo="La serie giornaliera",
        scenario="Il capo vuole \"vedere i due anni\". Un grafico con lo slider sotto, e due numeri: il giorno più leggero e quello più pesante.",
        soluzione=soluzione_3, verifica=verifica_3,
        perche="Somma dei quartorari e poi diviso 4: un quarto d'ora a P MW vale P/4 MWh. La media moltiplicata per 24 darebbe quasi lo stesso, ma nel giorno del buco di marzo conterebbe un'ora che non c'è stata.",
        base=dict(
            richiesta="""
                1. Metti `data` come indice in `indice_tempo`.
                2. Costruisci `giornaliero`: somma dei quartorari di ogni giorno con `resample("D").sum()`,
                   poi `reset_index()`. Aggiungi la colonna `mwh` dividendo per 4 e togli la colonna `mw`.
                3. Disegna `mwh` nel tempo con `px.line` e lo slider sotto. Con lo slider guarda agosto e
                   la settimana di Natale: cosa succede?
                4. In `estremi` metti le due righe del giorno più leggero e di quello più pesante.
            """,
            suggerimento="`idxmin()` e `idxmax()` danno l'etichetta della riga; `.loc[[a, b]]` ne prende due insieme.",
            starter="""
                # 1. il tempo come indice: serve a resample
                indice_tempo = carico.set_index("data")
                # 2. energia di ogni giorno: somma dei quartorari, poi da MW a MWh
                giornaliero = indice_tempo["mw"].resample("D").sum().reset_index()
                giornaliero["mwh"] = ...
                giornaliero = giornaliero.drop(columns="mw")

                # 3. la linea con lo slider sotto
                fig = px.line(giornaliero, x=..., y=..., title="Energia giornaliera, zona Nord")
                fig.update_xaxes(rangeslider_visible=True)
                fig.show()

                # 4. il giorno più leggero e quello più pesante, in una tabella di due righe
                estremi = giornaliero.loc[[..., ...]]
                estremi
            """,
        ),
        avanzata=dict(
            richiesta="""
                Costruisci `giornaliero`: una riga per giorno, colonne `data` e `mwh` (energia del giorno:
                un quartorario a P MW vale P/4 MWh). Disegnala con lo slider sotto e metti in `estremi` le
                due righe del giorno più leggero e di quello più pesante.
                Risultato atteso: una tabella 731×2, un grafico a una linea, una tabella 2×2.
                Domanda: cosa succede ad agosto e nella settimana di Natale?
            """,
            starter="""
                giornaliero = ...

                estremi = ...
                estremi
            """,
            bloccato="""
                `set_index("data")`, poi `["mw"].resample("D").sum()`: il risultato ha la data come indice,
                `reset_index()` la riporta colonna. Lo slider: `fig.update_xaxes(rangeslider_visible=True)`.
            """,
        ),
    )

    # ------------------------------------------------------------------ 4
    nb.sezione("La giornata tipo", intro=f"""
        {DETTAGLIO}

        Un'altra domanda sugli stessi dati: com'è fatta una giornata media? Non serve il tempo come
        indice, basta l'ora del giorno in una colonna e un `groupby`.
    """)
    soluzione_4 = """
        carico["ora"] = carico["data"].dt.hour
        carico["weekend"] = carico["data"].dt.dayofweek >= 5

        profilo = carico.groupby("ora")["mw"].mean()
        profilo = profilo.reset_index()
        profilo_tipo = carico.groupby(["weekend", "ora"])["mw"].mean()
        profilo_tipo = profilo_tipo.reset_index()

        fig = px.line(profilo_tipo, x="ora", y="mw", color="weekend", markers=True,
                      title="Profilo orario medio: feriale e weekend", labels={"mw": "MW medi", "ora": "ora del giorno"})
        fig.show()

        medie = carico.groupby("weekend")["mw"].mean()
        calo_weekend = round((1 - medie.loc[True] / medie.loc[False]) * 100, 1)
        print(f"Calo del weekend: {calo_weekend}%")
        profilo
    """
    verifica_4 = """
        assert profilo.shape == (24, 2), "❌ profilo: 24 righe (le ore) e 2 colonne (ora e mw): serve reset_index"
        assert profilo["ora"].nunique() == 24, "❌ profilo: manca qualche ora"
        assert 3 <= profilo.loc[profilo["mw"].idxmin(), "ora"] <= 6, "❌ Il minimo del profilo dovrebbe cadere di notte, tra le 3 e le 6"
        assert len(profilo_tipo) == 48, "❌ profilo_tipo: 24 ore per 2 tipi di giorno = 48 righe"
        assert 20 <= calo_weekend <= 30, "❌ calo_weekend: tra 20 e 30 per cento, con un decimale"
    """
    step(
        nb, titolo="I profili",
        scenario="Il collega della sala controllo giura che i picchi sono due. Il commerciale vuole sapere quanto cala il weekend, in percentuale, per un'offerta.",
        soluzione=soluzione_4, verifica=verifica_4,
        perche="Il calo del weekend si calcola sulle medie dei due gruppi, non sulle due linee: il profilo medio è già una media, e la media di medie inganna.",
        base=dict(
            richiesta="""
                1. Aggiungi a `carico` la colonna `ora` (`dt.hour`) e la colonna `weekend`: `True` se il
                   giorno della settimana è sabato o domenica (`dt.dayofweek` conta da lunedì = 0).
                2. Costruisci `profilo`: carico medio per `ora`, 24 righe e 2 colonne.
                3. Costruisci `profilo_tipo`: carico medio per `weekend` e `ora` insieme, 48 righe.
                4. Disegna `profilo_tipo` con `px.line`, una linea per tipo di giorno. Quanti picchi vedi, e
                   a che ore? A che ora il minimo?
                5. Calcola `calo_weekend`: di quanto il carico medio del weekend sta sotto quello feriale,
                   in percentuale con un decimale.
            """,
            suggerimento="`groupby` con due chiavi vuole una lista; `color=\"weekend\"` separa le linee.",
            starter="""
                # 1. ora del giorno e weekend (sabato = 5, domenica = 6)
                carico["ora"] = carico["data"].dt.hour
                carico["weekend"] = carico["data"].dt.dayofweek >= ...

                # 2. profilo medio orario: una riga per ora, poi l'ora torna colonna
                profilo = carico.groupby(...)["mw"].mean()
                profilo = profilo.reset_index()
                # 3. lo stesso, separato tra feriale e weekend
                profilo_tipo = carico.groupby([..., ...])["mw"].mean()
                profilo_tipo = profilo_tipo.reset_index()

                # 4. due linee
                fig = px.line(profilo_tipo, x="ora", y="mw", color=..., markers=True, title="Profilo orario medio")
                fig.show()

                # 5. di quanto cala il weekend, in percentuale sul feriale
                medie = carico.groupby("weekend")["mw"].mean()
                calo_weekend = round((1 - ... / ...) * 100, 1)
                print(f"Calo del weekend: {calo_weekend}%")
                profilo
            """,
        ),
        avanzata=dict(
            richiesta="""
                Aggiungi a `carico` le colonne `ora` e `weekend` (True il sabato e la domenica). Costruisci
                `profilo` (carico medio per ora: tabella 24×2) e `profilo_tipo` (lo stesso, separato per
                `weekend`: 48 righe) e disegna `profilo_tipo` a due linee. Calcola `calo_weekend`: di quanto
                il carico medio del weekend sta sotto quello feriale, in percentuale con un decimale.
                Domande: quanti picchi, a che ore? A che ora il minimo?
            """,
            starter="""
                carico["ora"] = ...
                carico["weekend"] = ...

                profilo = ...
                profilo_tipo = ...
                calo_weekend = ...
                print(f"Calo del weekend: {calo_weekend}%")
                profilo
            """,
            bloccato="""
                `dt.hour` e `dt.dayofweek >= 5` fanno le due colonne; `groupby(["weekend", "ora"])` dà una
                riga per combinazione. Per il calo: medie per `weekend`, poi `1 - weekend / feriale`.
            """,
        ),
    )
    with nb.solo("avanzata"):
        nb.prova_tu(
            richiesta="""
                Le due linee dicono poco sul sabato rispetto alla domenica. Costruisci `mappa`: una griglia
                con i giorni della settimana sulle righe (0 = lunedì) e le ore sulle colonne, carico medio
                dentro; poi colorala con `px.imshow(mappa, aspect="auto")`. Dove sta il carico più alto?
                E il sabato somiglia più al venerdì o alla domenica?
            """,
            starter="""
                carico["giorno_settimana"] = carico["data"].dt.dayofweek
                mappa = carico.pivot_table(index=..., columns=..., values=..., aggfunc="mean")

                fig = px.imshow(mappa, aspect="auto", labels={"x": "ora", "y": "giorno (0 = lunedì)", "color": "MW"},
                                title="Carico medio per giorno della settimana e ora")
                fig.show()
            """,
            soluzione="""
                carico["giorno_settimana"] = carico["data"].dt.dayofweek
                mappa = carico.pivot_table(index="giorno_settimana", columns="ora", values="mw", aggfunc="mean")

                fig = px.imshow(mappa, aspect="auto", labels={"x": "ora", "y": "giorno (0 = lunedì)", "color": "MW"},
                                title="Carico medio per giorno della settimana e ora")
                fig.show()
            """,
            verifica="""
                assert mappa.shape == (7, 24), "❌ mappa: 7 giorni sulle righe, 24 ore sulle colonne"
                assert mappa.loc[6].mean() < mappa.loc[2].mean(), "❌ La domenica (6) dovrebbe stare sotto il mercoledì (2)"
            """,
        )

    # ------------------------------------------------------------------ 5
    nb.sezione("La temperatura di Milano", intro=f"""
        {DETTAGLIO}

        La temperatura arriva dall'archivio storico di Open-Meteo: oraria, per un punto. Prendiamo Milano
        come rappresentante del Nord: non lo è del tutto, ma per capire la forma della relazione basta.
    """)
    with nb.solo("base"):
        nb.md("""
            La funzione qui sotto è già scritta: leggiamola prima di usarla. Dentro c'è la chiamata all'API
            con `requests` e un `try/except` come quello del notebook sugli errori: se la rete non risponde,
            legge la copia salvata in `../Dati/fallback/`. Restituisce la parte `hourly` della risposta: un
            dizionario con due liste, pronto per `pd.DataFrame`.
        """)
        nb.code("""
            import json

            import requests
        """)
        nb.code("""
            def scarica_temperatura(start, end):
                \"\"\"Temperatura oraria a Milano tra due date (Open-Meteo): dizionario con le liste time e temperature_2m.\"\"\"
                url = "https://archive-api.open-meteo.com/v1/archive"
                params = {"latitude": 45.4642, "longitude": 9.19, "start_date": start, "end_date": end,
                          "hourly": "temperature_2m", "timezone": "Europe/Rome"}
                try:
                    response = requests.get(url, params=params, timeout=30)
                    response.raise_for_status()
                    risposta = response.json()
                except requests.RequestException:
                    print("API non raggiungibile: uso la copia in ../Dati/fallback/")
                    with open("../Dati/fallback/meteo_milano_2024_2025.json", encoding="utf-8") as f:
                        risposta = json.load(f)
                return risposta["hourly"]
        """)
    soluzione_5_base = """
        inizio = carico["data"].min().strftime("%Y-%m-%d")
        fine = carico["data"].max().strftime("%Y-%m-%d")
        orario = scarica_temperatura(inizio, fine)

        meteo = pd.DataFrame(orario)
        meteo["time"] = pd.to_datetime(meteo["time"])
        meteo = meteo.rename(columns={"time": "data", "temperature_2m": "temperatura"})
        display(meteo.head())

        fig = px.line(meteo, x="data", y="temperatura", title="Temperatura oraria a Milano", labels={"temperatura": "°C", "data": ""})
        fig.show()
        meteo.describe()
    """
    soluzione_5_avanzata = """
        import requests

        inizio = carico["data"].min().strftime("%Y-%m-%d")
        fine = carico["data"].max().strftime("%Y-%m-%d")
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {"latitude": 45.4642, "longitude": 9.19, "start_date": inizio, "end_date": fine,
                  "hourly": "temperature_2m", "timezone": "Europe/Rome"}
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        risposta = response.json()

        meteo = pd.DataFrame(risposta["hourly"])
        meteo["time"] = pd.to_datetime(meteo["time"])
        meteo = meteo.rename(columns={"time": "data", "temperature_2m": "temperatura"})

        fig = px.line(meteo, x="data", y="temperatura", title="Temperatura oraria a Milano", labels={"temperatura": "°C", "data": ""})
        fig.show()
        meteo.describe()
    """
    verifica_5 = """
        assert set(meteo.columns) == {"data", "temperatura"}, "❌ meteo: due colonne, data e temperatura"
        assert str(meteo["data"].dtype).startswith("datetime64"), "❌ meteo: la colonna data deve essere datetime"
        assert len(meteo) == 17544, "❌ meteo: un valore per ogni ora dei due anni, 17544"
        assert meteo["temperatura"].between(-15, 45).all(), "❌ meteo: temperature fuori da ogni plausibilità per Milano"
    """
    nb.esercizio(
        titolo="Scaricare la temperatura", aula="base", rete=True,
        scenario="Due anni di temperatura oraria: 17544 valori. Prima di unirli al carico, guardiamoli.",
        richiesta="""
            1. Ricava `inizio` e `fine` dal carico: primo e ultimo giorno, come testo `AAAA-MM-GG`
               (`.min()`, `.max()` e `.strftime("%Y-%m-%d")`).
            2. Chiama `scarica_temperatura(inizio, fine)`: restituisce un dizionario con due liste, `time` e
               `temperature_2m`. Trasformalo in `meteo` con `pd.DataFrame`.
            3. Converti `time` in datetime e rinomina le colonne in `data` e `temperatura`. Guarda le prime
               righe.
            4. Disegna la temperatura nel tempo con `px.line` e chiudi con `meteo.describe()`: il massimo e
               il minimo sono plausibili per Milano?
        """,
        suggerimento="`strftime` trasforma una data in testo nel formato che vuoi; l'API vuole `2024-01-01`.",
        starter="""
            # 1. l'intervallo da chiedere: dal primo all'ultimo giorno del carico, come testo
            inizio = carico["data"].min().strftime("%Y-%m-%d")
            fine = ...
            # 2. la risposta dell'API: un dizionario con due liste, time e temperature_2m
            orario = scarica_temperatura(inizio, fine)
            meteo = pd.DataFrame(...)

            # 3. date vere e nomi corti
            meteo["time"] = pd.to_datetime(meteo["time"])
            meteo = meteo.rename(columns={...})
            display(meteo.head())

            # 4. un grafico per vedere se è plausibile, e i numeri
            fig = px.line(meteo, x=..., y=..., title="Temperatura oraria a Milano")
            fig.show()
            meteo.describe()
        """,
        soluzione=soluzione_5_base,
        verifica=verifica_5,
    )
    nb.esercizio(
        titolo="Scaricare la temperatura", aula="avanzata", rete=True,
        scenario="Due anni di temperatura oraria, dall'archivio storico di Open-Meteo. La chiamata la scriviamo noi, con lo schema già usato per la previsione.",
        richiesta="""
            Chiedi all'archivio storico di Open-Meteo la temperatura oraria di Milano (latitudine
            45.4642, longitudine 9.19) dal primo all'ultimo giorno del carico. URL
            `https://archive-api.open-meteo.com/v1/archive`; parametri `latitude`, `longitude`,
            `start_date` ed `end_date` come testo `AAAA-MM-GG`, `hourly="temperature_2m"`,
            `timezone="Europe/Rome"`. Trasforma la risposta in `meteo` con due colonne: `data` (datetime)
            e `temperatura`. Disegnala e chiudi con `describe()`.
            Risultato atteso: 17544 righe, temperature plausibili per Milano.
        """,
        starter="""
            import requests

            meteo = ...
            meteo.describe()
        """,
        soluzione=soluzione_5_avanzata,
        verifica=verifica_5,
        perche="Stesso schema della previsione: `requests.get` con `params`, `raise_for_status`, `.json()`. La chiave `hourly` è un dizionario di liste, pronto per `pd.DataFrame`.",
    )
    with nb.solo("avanzata"):
        nb.box("nota", """
            `requests.get(url, params=params, timeout=30)`, poi `raise_for_status()` e `.json()`. Nella
            risposta, `["hourly"]` è un dizionario con due liste, `time` e `temperature_2m`:
            `pd.DataFrame(...)` lo trasforma in tabella, poi `to_datetime` su `time` e `rename`.
        """, titolo="Se sei bloccato")
        nb.md("""
            Se l'API non risponde, esegui la cella qui sotto al posto di quella sopra: produce lo stesso
            `meteo` dalla copia salvata. Poi rilancia la verifica.
        """)
        nb.code("""
            import json

            with open("../Dati/fallback/meteo_milano_2024_2025.json", encoding="utf-8") as f:
                risposta = json.load(f)

            meteo = pd.DataFrame(risposta["hourly"])
            meteo["time"] = pd.to_datetime(meteo["time"])
            meteo = meteo.rename(columns={"time": "data", "temperature_2m": "temperatura"})
            meteo.describe()
        """, rete=True)

    # ------------------------------------------------------------------ 6
    nb.sezione("Due tabelle, una sola", intro=f"""
        {DETTAGLIO}

        La temperatura è oraria, il carico quartorario: prima di unirli, portiamo il carico all'ora.
        Per questo passaggio basta il carico; la temperatura entra subito dopo.
    """)
    verifica_6a = """
        assert set(carico_orario.columns) == {"data", "mw"}, "❌ carico_orario: due colonne, data e mw"
        assert len(carico_orario) == 17544, "❌ carico_orario: 17544 ore; con resample compare anche l'ora di marzo che manca, vuota"
    """
    soluzione_6a = """
        indice_tempo = carico.set_index("data")
        carico_orario = indice_tempo["mw"].resample("h").mean().reset_index()

        print(len(carico_orario), "ore")
        carico_orario[carico_orario["mw"].isna()]
    """
    nb.prova_tu(
        aula="base",
        richiesta="""
            Costruisci `carico_orario`: media dei quattro quartorari di ogni ora, con `data` e `mw` come
            colonne. Quante righe sono, e da dove vengono i valori mancanti?
        """,
        starter="""
            indice_tempo = carico.set_index("data")
            carico_orario = indice_tempo["mw"].resample(...).mean().reset_index()

            print(len(carico_orario), "ore")
            carico_orario[carico_orario["mw"].isna()]
        """,
        soluzione=soluzione_6a,
        verifica=verifica_6a,
    )
    nb.prova_tu(
        aula="avanzata",
        richiesta="""
            Costruisci `carico_orario`: media dei quattro quartorari di ogni ora, con `data` e `mw` come
            colonne, e mostra le righe con valori mancanti. Risultato atteso: 17544 righe. Domanda: da dove
            vengono i valori mancanti?
        """,
        starter="""
            carico_orario = ...

            print(len(carico_orario), "ore")
            carico_orario[carico_orario["mw"].isna()]
        """,
        soluzione=soluzione_6a,
        verifica=verifica_6a,
    )
    nb.md("""
        Le due ore vuote sono le 2:00 dell'ultima domenica di marzo: `resample` costruisce tutte le ore
        del calendario, anche quella che nei dati non c'è. Ora il `merge`: a ogni ora del carico la sua
        temperatura, come un CERCA.VERT.
    """)
    soluzione_6 = """
        print(len(carico_orario), len(meteo))
        unione = pd.merge(carico_orario, meteo, on="data", how="left")
        print(len(unione))
        display(unione.isna().sum())

        unione = unione.dropna()
        unione.head()
    """
    verifica_6 = """
        assert set(unione.columns) == {"data", "mw", "temperatura"}, "❌ unione: tre colonne, data, mw e temperatura"
        assert unione.isna().sum().sum() == 0, "❌ unione: dopo dropna non devono restare valori mancanti"
        assert 17000 <= len(unione) <= 17548, "❌ unione: circa 17500 righe, una per ora"
    """
    step(
        nb, titolo="L'unione", rete=True,
        scenario="Due tabelle con la stessa colonna `data`. Prima e dopo il merge contiamo le righe: è il controllo che smaschera una chiave non unica.",
        soluzione=soluzione_6, verifica=verifica_6,
        perche="`how=\"left\"` tiene tutte le ore del carico: se alla temperatura manca un'ora, lo vediamo come NaN invece di perdere la riga in silenzio.",
        base=dict(
            richiesta="""
                1. Stampa quante righe hanno `carico_orario` e `meteo`.
                2. Unisci in `unione` con `pd.merge`, chiave `data`, tenendo tutte le righe del carico.
                3. Stampa quante righe ha `unione` e conta i valori mancanti per colonna. Da dove vengono?
                4. Togli le righe incomplete con `dropna()` e riassegna.
            """,
            suggerimento="`how=\"left\"` è il CERCA.VERT: tutte le righe di sinistra, la temperatura dove c'è.",
            starter="""
                # 1. quante righe prima
                print(len(carico_orario), len(meteo))
                # 2. il CERCA.VERT: a ogni ora del carico la sua temperatura
                unione = pd.merge(carico_orario, meteo, on=..., how=...)
                # 3. quante righe dopo, e quanti valori mancanti per colonna
                print(len(unione))
                display(unione.isna().sum())

                # 4. via le righe incomplete
                unione = ...
                unione.head()
            """,
        ),
        avanzata=dict(
            richiesta="""
                Unisci `carico_orario` e `meteo` in `unione` (colonne `data`, `mw`, `temperatura`) tenendo
                tutte le ore del carico. Stampa le righe prima e dopo, conta i valori mancanti per colonna,
                poi togli le righe incomplete.
                Risultato atteso: circa 17540 righe, zero valori mancanti. Domanda: da dove venivano?
            """,
            starter="""
                unione = ...
                unione.head()
            """,
            bloccato="""
                `pd.merge(carico_orario, meteo, on="data", how="left")`; `len()` prima e dopo dice se la
                chiave era unica; `isna().sum()` conta i buchi per colonna; `dropna()` li toglie, riassegnando.
            """,
        ),
    )

    # ------------------------------------------------------------------ 7
    nb.sezione("La relazione", intro=f"""
        {DETTAGLIO}

        Ora la domanda del capo. Un punto per giorno: temperatura media sulle x, carico medio sulle y, un
        colore per mese. La forma che esce è la risposta.
    """)
    soluzione_7 = """
        indice_tempo = unione.set_index("data")
        giornaliero_tc = indice_tempo.resample("D").mean().reset_index()
        giornaliero_tc["mese"] = giornaliero_tc["data"].dt.month

        fig = px.scatter(giornaliero_tc, x="temperatura", y="mw", color="mese", hover_data=["data"],
                         title="Carico medio giornaliero e temperatura media, zona Nord 2024-2025",
                         labels={"temperatura": "temperatura media (°C)", "mw": "carico medio (MW)"})
        fig.show()

        giornaliero_tc["fascia_t"] = (giornaliero_tc["temperatura"] // 3) * 3
        per_fascia = giornaliero_tc.groupby("fascia_t")["mw"].mean()
        temperatura_minimo = per_fascia.idxmin()
        print(f"Carico minimo nella fascia {temperatura_minimo:.0f}-{temperatura_minimo + 3:.0f} °C")
    """
    verifica_7 = """
        assert len(giornaliero_tc) == 731, "❌ giornaliero_tc: una riga per giorno, 731"
        assert giornaliero_tc["mese"].nunique() == 12, "❌ mese: i dodici mesi, da dt.month"
        assert 10 <= temperatura_minimo <= 21, "❌ temperatura_minimo: la fascia con il carico più basso sta tra 10 e 21 °C; serve il bordo inferiore della fascia, da idxmin"
    """
    step(
        nb, titolo="Carico e temperatura", rete=True,
        scenario="Il capo si aspetta una retta. Vediamo cosa dicono 731 giorni.",
        soluzione=soluzione_7, verifica=verifica_7,
        perche="Le medie giornaliere tolgono il ciclo orario, che qui è rumore: la relazione con la temperatura si vede giorno per giorno, non ora per ora.",
        base=dict(
            richiesta="""
                1. Porta `unione` a medie giornaliere in `giornaliero_tc` (indice temporale, `resample("D")`,
                   `mean()`, `reset_index()`).
                2. Aggiungi la colonna `mese` (`dt.month`).
                3. Disegna lo scatter: temperatura sulle x, carico sulle y, `color="mese"`,
                   `hover_data=["data"]`. Che forma ha? Dove stanno i punti bassi di ogni colore?
                4. A che temperatura il carico è minimo? Raggruppa per fasce di 3 °C (la colonna `fascia_t`
                   è già scritta), fai la media per fascia in `per_fascia` e metti in `temperatura_minimo`
                   la fascia con il carico più basso.
            """,
            suggerimento="`idxmin()` su una Series dà l'etichetta del minimo: qui, la fascia.",
            starter="""
                # 1. medie giornaliere di carico e temperatura
                indice_tempo = unione.set_index("data")
                giornaliero_tc = indice_tempo.resample("D").mean().reset_index()
                # 2. il mese, per colorare i punti
                giornaliero_tc["mese"] = ...

                # 3. lo scatter: temperatura sulle x, carico sulle y, un colore per mese
                fig = px.scatter(giornaliero_tc, x=..., y=..., color=..., hover_data=["data"],
                                 title="Carico medio giornaliero e temperatura media, zona Nord 2024-2025")
                fig.show()

                # 4. in che fascia di 3 °C il carico medio è più basso?
                giornaliero_tc["fascia_t"] = (giornaliero_tc["temperatura"] // 3) * 3
                per_fascia = ...
                temperatura_minimo = ...
                print(f"Carico minimo nella fascia {temperatura_minimo:.0f}-{temperatura_minimo + 3:.0f} °C")
            """,
        ),
        avanzata=dict(
            richiesta="""
                Porta `unione` a medie giornaliere in `giornaliero_tc` (colonne `data`, `mw`,
                `temperatura`, più `mese`) e disegna lo scatter temperatura contro carico, un colore per
                mese. Poi trova `temperatura_minimo`: il bordo inferiore della fascia di 3 °C in cui il
                carico medio è più basso.
                Risultato atteso: 731 punti con una forma riconoscibile, e una fascia.
                Domande: pesa di più il freddo o il caldo? Dove stanno i punti bassi di ogni colore?
            """,
            starter="""
                giornaliero_tc = ...

                temperatura_minimo = ...
                print(f"Carico minimo nella fascia {temperatura_minimo:.0f}-{temperatura_minimo + 3:.0f} °C")
            """,
            bloccato="""
                `(temperatura // 3) * 3` arrotonda al multiplo di 3 inferiore: è la fascia.
                `groupby("fascia_t")["mw"].mean().idxmin()` dice quale fascia ha il carico medio più basso.
            """,
        ),
    )

    # ------------------------------------------------------------------ 8
    nb.sezione("Il report", intro=f"""
        {CHAT}

        Il capo non apre notebook. Gli servono cinque frasi con i numeri e un grafico che si apre con un
        doppio clic. Il grafico lo esportiamo in HTML; le frasi le scriviamo noi, con i numeri trovati
        negli step precedenti.
    """)
    soluzione_8 = """
        from pathlib import Path

        fig = px.scatter(giornaliero_tc, x="temperatura", y="mw", color="mese", hover_data=["data"],
                         title=f"Carico del Nord e temperatura: minimo intorno a {temperatura_minimo:.0f}-{temperatura_minimo + 3:.0f} °C",
                         labels={"temperatura": "temperatura media (°C)", "mw": "carico medio (MW)"})
        fig.write_html("carico_nord_temperatura.html")
        print(Path("carico_nord_temperatura.html").exists())

        print(f"Quartorari puliti: {len(carico)}, doppioni tolti: {len(duplicati) // 2}")
        print(f"Giorno più leggero e più pesante:\\n{estremi.to_string(index=False)}")
        print(f"Minimo alle {profilo.loc[profilo['mw'].idxmin(), 'ora']}, massimo alle {profilo.loc[profilo['mw'].idxmax(), 'ora']}")
        print(f"Calo del weekend: {calo_weekend}%")
        print(f"Fondo della U: {temperatura_minimo:.0f}-{temperatura_minimo + 3:.0f} °C")
    """
    verifica_8 = """
        assert Path("carico_nord_temperatura.html").exists(), "❌ Il file HTML non c'è: write_html con il nome carico_nord_temperatura.html, nella cartella del notebook"
    """
    step(
        nb, titolo="La sintesi", rete=True,
        scenario="Un file HTML e cinque frasi. Il grafico finale è lo scatter, con un titolo che dice la scoperta.",
        soluzione=soluzione_8, verifica=verifica_8,
        base=dict(
            richiesta="""
                1. Costruisci di nuovo lo scatter in `fig`, con un titolo che dica dove sta il minimo.
                2. Esportalo con `fig.write_html("carico_nord_temperatura.html")`, nella cartella del notebook.
                3. Esegui le `print` già scritte: sono i numeri per le cinque frasi della cella Markdown
                   dopo la verifica. Completala al posto dei puntini.
            """,
            suggerimento="Il titolo è una f-string: dentro le graffe ci sta `temperatura_minimo`.",
            starter="""
                from pathlib import Path

                # 1. il grafico finale, con la scoperta nel titolo
                fig = px.scatter(giornaliero_tc, x="temperatura", y="mw", color="mese", hover_data=["data"],
                                 title=f"Carico del Nord e temperatura: minimo intorno a {...} °C",
                                 labels={"temperatura": "temperatura media (°C)", "mw": "carico medio (MW)"})
                # 2. il file da mandare
                fig.write_html(...)
                print(Path("carico_nord_temperatura.html").exists())

                # 3. i numeri per le cinque frasi
                print(f"Quartorari puliti: {len(carico)}, doppioni tolti: {len(duplicati) // 2}")
                print(f"Giorno più leggero e più pesante:\\n{estremi.to_string(index=False)}")
                print(f"Minimo alle {profilo.loc[profilo['mw'].idxmin(), 'ora']}, massimo alle {profilo.loc[profilo['mw'].idxmax(), 'ora']}")
                print(f"Calo del weekend: {calo_weekend}%")
                print(f"Fondo della U: {temperatura_minimo:.0f}-{temperatura_minimo + 3:.0f} °C")
            """,
        ),
        avanzata=dict(
            richiesta="""
                Ricostruisci lo scatter in `fig` con un titolo che dica dove sta il minimo ed esportalo in
                `carico_nord_temperatura.html`, nella cartella del notebook. Poi stampa i numeri che
                servono alle cinque frasi della cella Markdown dopo la verifica, e completala.
                Risultato atteso: un file HTML che si apre nel browser, cinque frasi con i numeri.
            """,
            starter="""
                from pathlib import Path

                fig = ...
                fig.write_html(...)
                print(Path("carico_nord_temperatura.html").exists())
            """,
            bloccato="""
                I numeri stanno già nelle variabili: `estremi`, `profilo`, `calo_weekend`,
                `temperatura_minimo`. Una `print` con f-string per ciascuna, poi i numeri si copiano
                nella cella Markdown.
            """,
        ),
    )
    nb.md("""
        **Cosa abbiamo scoperto sul carico del Nord, 2024-2025**

        1. I dati di Terna sono ... (non orari): ... righe pulite, tolti ... doppioni dell'ora legale di
           ottobre; le ... ore mancanti di marzo restano un buco.
        2. Il giorno più pesante è stato il ... con ... MWh; il più leggero il ... con ... MWh.
        3. La giornata media ha ... picchi, alle ... e alle ...; il minimo è alle ...
        4. Nel weekend il carico medio cala del ...% rispetto al feriale.
        5. Il carico è minimo tra ... e ... °C e sale con il freddo e con il caldo; al Nord pesa di più ...
    """)
    with nb.solo("avanzata"):
        nb.box("nota", """
            Prova la modalità Agent su questa cella: chiedile di compilare le cinque frasi leggendo le
            variabili del notebook. Poi controlla ogni numero con le `print` dello step: se uno non torna,
            vince la `print`.
        """)
    nb.md("""
        **Cosa ho chiesto a Copilot e cosa ho dovuto correggere**

        - Ho chiesto: ...
        - Ha sbagliato su: ...
        - Ho verificato con: ...
    """)
    nb.box("ricorda", """
        - Prima la frequenza vera e i duplicati, poi tutto il resto: un `resample` su dati sporchi mente con precisione.
        - `len()` prima e dopo ogni `merge`.
        - Il grafico risponde alla domanda solo se il titolo dice la risposta.
    """)
    return nb
