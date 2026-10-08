"""11 · Capstone: il carico del Nord e la temperatura."""

from textwrap import dedent

from nbkit import Cella, Notebook, box_html


def nb_d(*parti: str) -> str:
    """Toglie l'indentazione a ogni pezzo di testo e li unisce, come fa il toolkit con le celle."""
    return "\n".join(dedent(p).strip("\n") for p in parti)


def step(nb: Notebook, titolo: str, scenario: str, richiesta: str, soluzione: str, verifica: str,
         starter_base: str, starter_avanzata: str, richiesta_avanzata: str | None = None,
         suggerimento: str | None = None, perche: str | None = None) -> None:
    """Lo stesso step per le due aule: stessa consegna e verifica, scheletro guidato in Base e quasi vuoto in Avanzata."""
    nb.esercizio(
        titolo=titolo, scenario=scenario, richiesta=richiesta, suggerimento=suggerimento,
        starter=starter_base, soluzione=soluzione, verifica=verifica, perche=perche, aula="base",
    )
    nb.esercizio(
        titolo=titolo, scenario=scenario, richiesta=richiesta_avanzata or richiesta,
        starter=starter_avanzata, soluzione=soluzione, verifica=verifica, perche=perche, aula="avanzata",
    )


def costruisci() -> Notebook:
    nb = Notebook(
        num="11",
        file="11_Capstone",
        titolo="Capstone: il carico del Nord e la temperatura",
        blocco=4,
        giornata=2,
        intento="Analizziamo due anni di carico elettrico della zona Nord insieme alla temperatura di Milano, per descrivere come il carico dipende dall'ora, dal giorno della settimana e dalla temperatura.",
        obiettivi=[
            "caricare, unire e pulire una serie temporale reale, con i salti dell'ora legale",
            "costruire la serie giornaliera e i profili medi per ora e per giorno della settimana",
            "unire il carico con la temperatura di Open-Meteo e leggere la relazione tra i due",
        ],
        tempo={"base": 110, "avanzata": 110},
        dati=["load_total_north_hourly_2024.xlsx", "load_total_north_hourly_2025.xlsx", "fallback/meteo_milano_2024_2025.json"],
        etichetta_esercizio="Step",
        prefisso_esercizi="",
    )

    # ------------------------------------------------------------------ introduzione
    nb.md("""
        I dati utilizzati provengono dal [Download Center di Terna](https://dati.terna.it/en/download-center); in
        particolare, useremo i dati di **carico elettrico della zona Nord** relativi agli anni 2024 e 2025. Nei
        dataset Terna il carico è la potenza richiesta al sistema elettrico in ciascun intervallo temporale, una
        grandezza centrale per la pianificazione e la gestione della rete di trasmissione.
    """)
    nb.md("""
        Accanto al carico integriamo la **temperatura** di Milano, ottenuta tramite API da
        [Open-Meteo](https://open-meteo.com). L'obiettivo è descrivere come il carico del Nord dipende dall'ora
        del giorno, dal giorno della settimana e dalla temperatura. Il lavoro è diviso in sei step, ciascuno con
        una consegna, una cella da completare e una verifica. Copilot si può usare per i titoli e le etichette
        dei grafici, mentre il codice degli step lo scriviamo noi, perché lo scopo del capstone è mettere in
        pratica quello che abbiamo visto nei notebook precedenti.
    """)

    # ------------------------------------------------------------------ 1
    nb.sezione("Caricamento dei dati e unione")
    step(
        nb, titolo="Caricamento dei dati e unione",
        scenario="In questo step costruiamo una singola serie storica continua a partire dai dati grezzi.",
        richiesta="""
            1. Leggi i due file Excel presenti nella cartella `../Dati/` in `df_2024` e `df_2025`:
               `load_total_north_hourly_2024.xlsx` e `load_total_north_hourly_2025.xlsx`.
            2. Unisci i due dataset **per righe** in `df`, mantenendo lo stesso schema di colonne, in modo da
               ottenere una serie unica che copra l'intero periodo 2024-2025.
            3. Controlla la dimensione del dataset, la prima e l'ultima data, il numero medio di righe per giorno
               e i valori mancanti per colonna. Il nome del file contiene `hourly`, quindi verifica con il numero
               di righe per giorno se la frequenza dei dati è effettivamente oraria.
        """,
        richiesta_avanzata="""
            1. Leggi i due file Excel presenti nella cartella `../Dati/` in `df_2024` e `df_2025`:
               `load_total_north_hourly_2024.xlsx` e `load_total_north_hourly_2025.xlsx`.
            2. Unisci i due dataset **per righe** in `df`, mantenendo lo stesso schema di colonne, in modo da
               ottenere una serie unica che copra l'intero periodo 2024-2025.
            3. Controlla la dimensione del dataset, la prima e l'ultima data, il numero medio di righe per giorno,
               da salvare in `righe_giorno`, e i valori mancanti per colonna. Il nome del file contiene `hourly`,
               quindi verifica con il numero di righe per giorno se la frequenza dei dati è effettivamente oraria.

            Il risultato è un DataFrame di 70.176 righe e 4 colonne, senza valori mancanti.
        """,
        suggerimento="`df[\"Date\"].dt.date.nunique()` conta i giorni diversi.",
        starter_base="""
            import pandas as pd

            # 1. i due file, uno per anno
            df_2024 = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
            df_2025 = ...

            # 2. uno sotto l'altro, con l'indice rifatto da 0
            df = pd.concat([...], ignore_index=True)

            # 3. dimensione, prima e ultima data, righe per giorno, valori mancanti
            print(df.shape)
            print(df["Date"].min(), ...)
            righe_giorno = len(df) / df["Date"].dt.date.nunique()
            print(f"{righe_giorno:.0f} righe al giorno")
            df.isna().sum()
        """,
        starter_avanzata="""
            import pandas as pd

            df = ...

            righe_giorno = ...
            df.isna().sum()
        """,
        soluzione="""
            import pandas as pd

            df_2024 = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
            df_2025 = pd.read_excel("../Dati/load_total_north_hourly_2025.xlsx")

            df = pd.concat([df_2024, df_2025], ignore_index=True)

            print(df.shape)
            print(df["Date"].min(), df["Date"].max())
            righe_giorno = len(df) / df["Date"].dt.date.nunique()
            print(f"{righe_giorno:.0f} righe al giorno")
            df.isna().sum()
        """,
        verifica="""
            assert df.shape == (70176, 4), "❌ df: 70.176 righe e 4 colonne, i due anni uno sotto l'altro"
            assert df.index[-1] == 70175, "❌ df: l'indice va rifatto da 0, con ignore_index=True in pd.concat"
            assert round(righe_giorno) == 96, "❌ righe_giorno: righe totali diviso il numero di giorni diversi"
        """,
    )
    nb.md("""
        Il conto dà 96 righe al giorno, quindi i dati sono quartorari, con un valore ogni 15 minuti, anche se il
        nome del file dice `hourly`. Ne terremo conto più avanti, quando dalla potenza in MW passeremo
        all'energia in MWh, perché ogni valore copre un quarto d'ora.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Colonna temporale e prima visualizzazione")
    step(
        nb, titolo="Preparazione della colonna temporale e prima visualizzazione",
        scenario="In questo step rendiamo la colonna data utilizzabile come variabile temporale e facciamo una prima ispezione visiva della serie.",
        richiesta="""
            1. Controlla con `df.dtypes` che la colonna `Date` sia già di tipo `datetime`; se fosse letta come
               testo, la si converte con `pd.to_datetime`.
            2. Ordina il dataset per data, perché ogni file comincia con l'ultimo quarto d'ora dell'anno, e
               reimposta l'indice per avere un ordinamento pulito.
            3. Importa Plotly e visualizza **entrambe** le serie nel tempo: `Total Load [MW]` e
               `Forecast Total Load [MW]`.
            4. Dopo aver verificato che le due curve siano coerenti, elimina le colonne che non useremo:
               `Forecast Total Load [MW]` e `Bidding Zone`.

            Al termine di questo step deve rimanere una serie storica con una colonna temporale in formato
            `datetime` e una sola colonna di valori, `Total Load [MW]`.
        """,
        suggerimento="`reset_index(drop=True)` rifà l'indice a partire da 0 senza conservare il vecchio come colonna, mentre `df.drop(columns=[...])` toglie le colonne indicate.",
        starter_base="""
            import plotly.express as px

            # 1. la colonna Date in formato datetime
            df["Date"] = pd.to_datetime(df["Date"])

            # 2. ordine per data e indice da 0
            df = df.sort_values(...).reset_index(drop=True)

            # 3. le due serie nel tempo
            fig = px.line(df, x="Date", y=[..., ...], title="Carico e previsione di Terna, zona Nord",
                          labels={"value": "carico [MW]", "variable": "serie"})
            fig.show()

            # 4. via le colonne che non useremo
            df = df.drop(columns=[...])
            df.head()
        """,
        starter_avanzata="""
            import plotly.express as px

            df["Date"] = ...
            df = ...

            fig = ...
            fig.show()

            df = ...
            df.head()
        """,
        soluzione="""
            import plotly.express as px

            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date").reset_index(drop=True)

            fig = px.line(df, x="Date", y=["Total Load [MW]", "Forecast Total Load [MW]"],
                          title="Carico e previsione di Terna, zona Nord",
                          labels={"value": "carico [MW]", "variable": "serie"})
            fig.show()

            df = df.drop(columns=["Forecast Total Load [MW]", "Bidding Zone"])
            df.head()
        """,
        verifica="""
            assert list(df.columns) == ["Date", "Total Load [MW]"], "❌ df: devono restare solo Date e Total Load [MW]"
            assert df["Date"].is_monotonic_increasing, "❌ df: ordina per Date"
            assert df.loc[0, "Date"] == pd.Timestamp("2024-01-01 00:00"), "❌ df: la riga 0 deve essere il primo quarto d'ora del 2024; dopo sort_values serve reset_index(drop=True)"
        """,
    )

    # ------------------------------------------------------------------ 3
    nb.sezione("Ora legale: duplicati e buchi", intro="""
        Prima di aggregare conviene controllare il passo tra un timestamp e il successivo, che in una serie
        quartoraria regolare è sempre di 15 minuti. Il passo cambia soltanto nell'ultima domenica di marzo e
        nell'ultima domenica di ottobre, i due giorni dell'anno in cui si passa dall'ora solare all'ora legale e
        viceversa.
    """)
    with nb.solo("avanzata"):
        nb.md("""
            Un primo tentativo consiste nell'assegnare alle date il fuso orario italiano con `tz_localize` e
            lasciare a pandas il compito di riconoscere l'ora ripetuta, con l'opzione `ambiguous="infer"`. La
            cella qui sotto dà errore apposta, e conviene leggerne l'ultima riga, che spiega il motivo.
        """)
        nb.code('df["Date"].dt.tz_localize("Europe/Rome", ambiguous="infer")', errore=True)
        nb.md("""
            Il messaggio `There are 4 dst switches when there should only be 1` dice che pandas ha trovato
            quattro cambi d'ora dove se ne aspettava uno. Succede perché nei file le due copie di ogni quarto
            d'ora ripetuto sono intrecciate, e dall'ordine delle righe non si capisce quale appartenga all'ora
            legale e quale all'ora solare. Per questa analisi l'ora locale senza fuso è sufficiente, quindi
            togliamo i doppioni con `drop_duplicates`.
        """)
    step(
        nb, titolo="Pulizia dei duplicati dell'ora legale",
        scenario="In questo step lasciamo una riga per timestamp e contiamo i quarti d'ora che mancano.",
        richiesta="""
            1. Calcola in `passi` la differenza tra ogni timestamp e il precedente con `diff()`, conta con
               `value_counts()` quante volte compare ogni valore e chiediti quale sia il passo normale e a che
               cosa corrispondano gli altri due valori.
            2. Metti in `duplicati` tutte le copie delle righe con un timestamp ripetuto, usando
               `duplicated(keep=False)`, e guarda in quali giorni e a quali ore cadono.
            3. Ordina per `Date`, togli i duplicati con `drop_duplicates(subset="Date")` e reimposta l'indice.
            4. Metti in `buchi` le righe che arrivano dopo un salto più lungo di 15 minuti e guarda in quali
               giorni cadono.
        """,
        suggerimento="l'ultima domenica di ottobre i quarti d'ora dalle 2:00 alle 2:45 compaiono due volte, mentre l'ultima domenica di marzo non esistono.",
        starter_base="""
            # 1. il passo tra un timestamp e il precedente, e quante volte compare ogni valore
            passi = df["Date"].diff()
            print(passi.value_counts())

            # 2. le righe con un timestamp ripetuto, tutte le copie
            duplicati = df[df["Date"].duplicated(keep=...)]
            print(duplicati)

            # 3. una riga per timestamp, indice da 0
            df = df.sort_values("Date").drop_duplicates(subset=...).reset_index(drop=True)

            # 4. le righe che arrivano dopo un salto più lungo di 15 minuti
            buchi = df[df["Date"].diff() > ...]
            buchi
        """,
        starter_avanzata="""
            passi = ...

            duplicati = ...

            df = ...

            buchi = ...
            buchi
        """,
        soluzione="""
            passi = df["Date"].diff()
            print(passi.value_counts())

            duplicati = df[df["Date"].duplicated(keep=False)]
            print(duplicati)

            df = df.sort_values("Date").drop_duplicates(subset="Date").reset_index(drop=True)

            buchi = df[df["Date"].diff() > pd.Timedelta("15min")]
            buchi
        """,
        verifica="""
            assert len(duplicati) == 16, "❌ duplicati: 16 righe, 8 timestamp ripetuti in due copie (keep=False le tiene tutte)"
            assert len(df) == 70168 and df["Date"].is_unique, "❌ df: 70.168 righe, una per timestamp"
            assert len(buchi) == 2, "❌ buchi: 2 righe, le 3:00 delle due ultime domeniche di marzo"
        """,
        perche="Dei due valori ripetuti teniamo il primo, perché le due copie differiscono di qualche centinaio di MW su circa 11.000 e la scelta incide poco sulle medie. Il buco di marzo invece resta, perché quei quarti d'ora non sono mai esistiti e non c'è nulla da ricostruire.",
    )

    # ------------------------------------------------------------------ 4
    nb.sezione("Aggregazioni temporali e profili medi", intro="""
        Useremo `Date` come colonna temporale e `Total Load [MW]` come variabile di interesse.
    """)
    step(
        nb, titolo="Aggregazioni temporali e profili medi",
        scenario="""
            In questo step analizziamo la serie quartoraria cambiando punto di vista sul tempo. Costruiamo una
            serie giornaliera e osserviamo i pattern medi legati all'ora del giorno e al giorno della settimana.
        """,
        richiesta="""
            **Serie giornaliera (somma)**

            1. Parti dal DataFrame quartorario `df`.
            2. Imposta la colonna `Date` come indice temporale in `df_indicizzato`.
            3. Aggrega per giorno usando `resample("D")` e calcola la **somma** del carico.
            4. Riporta `Date` come colonna e salva il risultato in `df_giornaliero`. Aggiungi poi la colonna
               `Energia [MWh]`, pari alla somma divisa per 4, perché un quarto d'ora a una potenza di P MW
               corrisponde a P/4 MWh.
            5. Visualizza la serie giornaliera con Plotly.

            **Profilo medio giornaliero (media per ora del giorno)**

            6. Torna alla serie quartoraria `df`, estrai l'**ora del giorno** dalla colonna `Date` e salvala in
               una nuova colonna `hour`.
            7. Raggruppa per `hour` e calcola la **media** del carico in `profilo_orario`.
            8. Visualizza il profilo medio giornaliero con Plotly.

            **Profilo medio settimanale (media per giorno della settimana)**

            9. Sempre partendo da `df`, estrai il **giorno della settimana** dalla colonna `Date` e salvalo in
               una nuova colonna `weekday`, con la convenzione `0 = lunedì, …, 6 = domenica`.
            10. Raggruppa per `weekday` e calcola la **media** del carico in `profilo_settimanale`.
            11. Visualizza il profilo medio settimanale con Plotly.

            Osserva infine i tre grafici e annota in quali periodi l'energia giornaliera scende, a che ore il
            carico è più alto e di quanto cala nel weekend, perché questi numeri serviranno nello step 6.
        """,
        suggerimento="`dt.hour` e `dt.dayofweek` estraggono ora e giorno della settimana; `reset_index()` dopo `groupby` riporta la chiave come colonna.",
        starter_base="""
            # serie giornaliera (punti 1-5)
            df_indicizzato = df.set_index("Date")
            df_giornaliero = df_indicizzato["Total Load [MW]"].resample(...).sum()
            df_giornaliero = df_giornaliero.reset_index()
            df_giornaliero["Energia [MWh]"] = ...
            fig = px.line(df_giornaliero, x="Date", y=..., title="Energia giornaliera, zona Nord")
            fig.show()

            # profilo medio giornaliero (punti 6-8)
            df["hour"] = df["Date"].dt.hour
            profilo_orario = df.groupby(...)["Total Load [MW]"].mean().reset_index()
            fig = px.line(profilo_orario, x=..., y=..., markers=True, title="Profilo medio giornaliero del carico")
            fig.update_xaxes(dtick=1)
            fig.show()

            # profilo medio settimanale (punti 9-11)
            df["weekday"] = ...
            profilo_settimanale = ...
            profilo_settimanale["giorno"] = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
            fig = px.line(profilo_settimanale, x="giorno", y="Total Load [MW]", markers=True,
                          title="Profilo medio settimanale del carico")
            fig.show()
        """,
        starter_avanzata="""
            # serie giornaliera
            df_giornaliero = ...

            # profilo medio giornaliero
            profilo_orario = ...

            # profilo medio settimanale
            profilo_settimanale = ...
        """,
        soluzione="""
            df_indicizzato = df.set_index("Date")
            df_giornaliero = df_indicizzato["Total Load [MW]"].resample("D").sum()
            df_giornaliero = df_giornaliero.reset_index()
            df_giornaliero["Energia [MWh]"] = df_giornaliero["Total Load [MW]"] / 4
            fig = px.line(df_giornaliero, x="Date", y="Energia [MWh]", title="Energia giornaliera, zona Nord")
            fig.show()

            df["hour"] = df["Date"].dt.hour
            profilo_orario = df.groupby("hour")["Total Load [MW]"].mean().reset_index()
            fig = px.line(profilo_orario, x="hour", y="Total Load [MW]", markers=True,
                          title="Profilo medio giornaliero del carico",
                          labels={"hour": "ora del giorno", "Total Load [MW]": "carico medio [MW]"})
            fig.update_xaxes(dtick=1)
            fig.show()

            df["weekday"] = df["Date"].dt.dayofweek
            profilo_settimanale = df.groupby("weekday")["Total Load [MW]"].mean().reset_index()
            profilo_settimanale["giorno"] = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
            fig = px.line(profilo_settimanale, x="giorno", y="Total Load [MW]", markers=True,
                          title="Profilo medio settimanale del carico",
                          labels={"giorno": "giorno della settimana", "Total Load [MW]": "carico medio [MW]"})
            fig.show()
        """,
        verifica="""
            assert len(df_giornaliero) == 731 and df_giornaliero["Energia [MWh]"].between(250_000, 700_000).all(), "❌ df_giornaliero: 731 giorni, con l'energia tra 250.000 e 700.000 MWh (somma dei quartorari divisa per 4)"
            assert profilo_orario.shape == (24, 2), "❌ profilo_orario: 24 righe (le ore) e 2 colonne, hour e Total Load [MW]"
            assert len(profilo_settimanale) == 7 and profilo_settimanale["Total Load [MW]"].idxmin() == 6, "❌ profilo_settimanale: 7 righe, con la domenica (6) come giorno più leggero"
        """,
        perche="L'energia giornaliera si ottiene sommando i valori quartorari e dividendo per 4, e non moltiplicando per 24 la potenza media del giorno. Nei due giorni di marzo con un'ora in meno, infatti, il prodotto per 24 conterebbe anche un'ora che non c'è stata.",
    )

    # ------------------------------------------------------------------ 5
    nb.sezione("Recupero e integrazione della temperatura", intro="""
        Al carico aggiungiamo la **temperatura a 2 metri** ricostruita per Milano. Si tratta di una
        semplificazione, perché usiamo una sola città come riferimento per tutto il Nord Italia. I dati vengono
        dall'API [Historical Weather](https://open-meteo.com/en/docs/historical-weather-api) di Open-Meteo, che
        non richiede alcuna chiave e restituisce i valori orari per l'intervallo di date indicato.
    """)
    with nb.solo("base"):
        nb.md("""
            La funzione `scarica_temperatura`, già scritta nelle celle qui sotto, chiede i dati all'API con
            `requests.get` e restituisce la parte `hourly` della risposta, cioè un dizionario con le liste `time`
            e `temperature_2m`. Se la rete non risponde, il blocco `try/except` legge al suo posto il file
            `../Dati/fallback/meteo_milano_2024_2025.json`, che contiene temperature di esempio e non misurate.
            In quel caso la funzione stampa un messaggio, e nelle frasi finali va indicato che la temperatura
            viene dai dati di esempio.
        """)
        nb.code("""
            import json
            from pathlib import Path

            import requests
        """)
        nb.code("""
            def scarica_temperatura(start, end):
                \"\"\"Temperatura oraria a Milano tra due date (Open-Meteo): dizionario con le liste time e temperature_2m.\"\"\"
                url = "https://archive-api.open-meteo.com/v1/archive"
                parametri = {"latitude": 45.4642, "longitude": 9.19, "start_date": start, "end_date": end,
                          "hourly": "temperature_2m", "timezone": "Europe/Rome"}
                try:
                    response = requests.get(url, params=parametri, timeout=30)
                    response.raise_for_status()
                    return response.json()["hourly"]
                except requests.RequestException:
                    file_meteo = Path("../Dati/fallback/meteo_milano_2024_2025.json")
                    print(f"API non raggiungibile: uso i dati di esempio di {file_meteo}")
                    with open(file_meteo, encoding="utf-8") as f:
                        return json.load(f)["hourly"]
        """)

    scenario_5 = """
        In questo step integriamo il dato di temperatura con il dato di carico. Per prima cosa va risolta la
        differente granularità, perché la temperatura è oraria mentre il carico è quartorario; la temperatura va
        quindi portata da un valore ogni ora a un valore ogni 15 minuti.
    """
    passi_comuni = """
        3. Converti `time` in datetime, rinomina le colonne in `Date` e `Temperature_C`, imposta `Date` come
           indice e ordinalo con `sort_index()`.
        4. Porta la temperatura a frequenza quartoraria con `resample("15min")` seguito da
           `interpolate(method="linear")`, così da poterla unire al carico, poi riporta `Date` come colonna e
           salva il risultato in `meteo_15`.
        5. Fai il merge con il DataFrame del carico `df`, tenendo tutte le sue righe, e salva il risultato in
           `df_completo`.
        6. Dopo il merge gli ultimi quarti d'ora del 2025 restano senza temperatura; riempili con `ffill()`,
           che ripete l'ultimo valore disponibile.
        7. Visualizza la temperatura nel tempo con `px.line()`.
    """
    soluzione_5_comune = """
        meteo = pd.DataFrame(orario)
        meteo["time"] = pd.to_datetime(meteo["time"])
        meteo = meteo.rename(columns={"time": "Date", "temperature_2m": "Temperature_C"})
        meteo = meteo.set_index("Date").sort_index()

        meteo_15 = meteo.resample("15min").interpolate(method="linear")
        meteo_15 = meteo_15.reset_index()

        df_completo = pd.merge(df, meteo_15, on="Date", how="left")
        print(df_completo["Temperature_C"].isna().sum(), "temperature mancanti dopo il merge")
        df_completo["Temperature_C"] = df_completo["Temperature_C"].ffill()

        fig = px.line(df_completo, x="Date", y="Temperature_C", title="Temperatura a Milano",
                      labels={"Temperature_C": "temperatura [°C]"})
        fig.show()
    """
    verifica_5 = """
        assert list(meteo_15.columns) == ["Date", "Temperature_C"], "❌ meteo_15: due colonne, Date e Temperature_C (dopo resample serve reset_index)"
        assert len(df_completo) == len(df), "❌ df_completo: il merge con how=\\"left\\" tiene tutte le righe di df"
        assert df_completo["Temperature_C"].notna().all(), "❌ df_completo: restano temperature mancanti, usa ffill()"
    """
    perche_5 = "L'interpolazione lineare stima i tre valori compresi tra un'ora e la successiva, quindi produce una stima e non una misura. Il merge con `how=\"left\"` tiene tutte le righe del carico; le ultime tre del 2025, dopo le 23:00, restano senza temperatura perché la serie oraria finisce a quell'ora, e `ffill` le riempie con il valore delle 23:00."
    nb.esercizio(
        titolo="Recupero e integrazione della temperatura", aula="base",
        scenario=scenario_5,
        richiesta=nb_d("""
            1. Ricava dal carico `data_inizio` e `data_fine`, cioè il primo e l'ultimo giorno, scritti come testo
               nel formato `AAAA-MM-GG` con `.min()`, `.max()` e `.strftime("%Y-%m-%d")`.
            2. Chiama `scarica_temperatura(data_inizio, data_fine)` e trasforma il risultato in `meteo` con
               `pd.DataFrame`.
        """, passi_comuni),
        suggerimento="`how=\"left\"` tiene tutte le righe del DataFrame di sinistra e aggiunge la temperatura dove c'è. `resample(\"15min\")` crea una riga ogni quarto d'ora, e `interpolate(method=\"linear\")` riempie le righe nuove con valori intermedi.",
        starter="""
            # 1. l'intervallo da chiedere, come testo AAAA-MM-GG
            data_inizio = df["Date"].min().strftime("%Y-%m-%d")
            data_fine = ...
            print("Intervallo:", data_inizio, "->", data_fine)

            # 2. la risposta dell'API: un dizionario con le liste time e temperature_2m
            orario = scarica_temperatura(data_inizio, data_fine)
            meteo = pd.DataFrame(...)

            # 3. date vere, nomi delle colonne, Date come indice
            meteo["time"] = pd.to_datetime(meteo["time"])
            meteo = meteo.rename(columns={...})
            meteo = meteo.set_index("Date").sort_index()

            # 4. da orario a 15 minuti, con interpolazione lineare
            meteo_15 = meteo.resample(...).interpolate(method="linear")
            meteo_15 = meteo_15.reset_index()

            # 5. merge con il carico, tenendo tutte le righe di df
            df_completo = pd.merge(df, meteo_15, on=..., how=...)

            # 6. l'ultima ora del 2025 senza temperatura
            df_completo["Temperature_C"] = ...

            # 7. la temperatura nel tempo
            fig = px.line(df_completo, x="Date", y="Temperature_C", title="Temperatura a Milano")
            fig.show()
        """,
        soluzione=nb_d("""
            data_inizio = df["Date"].min().strftime("%Y-%m-%d")
            data_fine = df["Date"].max().strftime("%Y-%m-%d")
            print("Intervallo:", data_inizio, "->", data_fine)

            orario = scarica_temperatura(data_inizio, data_fine)

        """, soluzione_5_comune),
        verifica=verifica_5,
        perche=perche_5,
    )

    nb.esercizio(
        titolo="Recupero e integrazione della temperatura", aula="avanzata", rete=True,
        scenario=scenario_5,
        richiesta=nb_d("""
            1. Chiedi all'archivio storico di Open-Meteo la temperatura oraria di Milano, alla latitudine
               45.4642 e longitudine 9.19, dal primo all'ultimo giorno del carico. L'indirizzo è
               `https://archive-api.open-meteo.com/v1/archive` e i parametri sono `latitude`, `longitude`,
               `start_date` ed `end_date`, con le date come testo `AAAA-MM-GG`, più `hourly="temperature_2m"` e
               `timezone="Europe/Rome"`. Salva in `orario` la chiave `hourly` della risposta.
            2. Nella cella che segue quella dei dati di riserva, trasforma `orario` in `meteo` con
               `pd.DataFrame`.
        """, passi_comuni),
        starter="""
            import requests

            data_inizio = ...
            data_fine = ...
            url = "https://archive-api.open-meteo.com/v1/archive"
            parametri = ...

            orario = ...
        """,
        soluzione="""
            import requests

            data_inizio = df["Date"].min().strftime("%Y-%m-%d")
            data_fine = df["Date"].max().strftime("%Y-%m-%d")
            url = "https://archive-api.open-meteo.com/v1/archive"
            parametri = {"latitude": 45.4642, "longitude": 9.19, "start_date": data_inizio, "end_date": data_fine,
                      "hourly": "temperature_2m", "timezone": "Europe/Rome"}
            response = requests.get(url, params=parametri, timeout=30)
            response.raise_for_status()
            orario = response.json()["hourly"]
        """,
        perche=perche_5,
    )
    with nb.solo("avanzata"):
        nb.md("""
            Se la rete non risponde, la cella qui sotto carica in `orario` le temperature di esempio della
            cartella `../Dati/fallback/`, che non sono misurate; se l'API ha risposto, la cella va saltata.
        """)
        nb.code("""
            import json

            with open("../Dati/fallback/meteo_milano_2024_2025.json", encoding="utf-8") as f:
                orario = json.load(f)["hourly"]
            len(orario["time"])
        """)
        nb.celle.append(Cella("code", nb_d("""
            # punti 2-7: da orario a df_completo
            meteo = ...

            meteo_15 = ...

            df_completo = ...
        """), aula="avanzata", solo_studente=True, ruolo="starter"))
        nb.celle.append(Cella("code", nb_d(soluzione_5_comune), aula="avanzata", solo_soluzioni=True, ruolo="soluzione"))
        nb.celle.append(Cella("code", nb_d(verifica_5), aula="avanzata", ruolo="verifica"))

    # ------------------------------------------------------------------ 6
    nb.sezione("Carico e temperatura")
    step(
        nb, titolo="Carico e temperatura",
        scenario="In questo step costruiamo uno scatter con un punto per giorno, la temperatura media sulle x, il carico medio sulle y e un colore diverso per ogni mese. Dalla forma della nuvola di punti si legge come il carico dipende dalla temperatura.",
        richiesta="""
            1. Calcola in `giornaliero` le medie giornaliere di `df_completo`, impostando `Date` come indice,
               selezionando le colonne `Total Load [MW]` e `Temperature_C`, applicando `resample("D").mean()` e
               riportando infine `Date` come colonna con `reset_index()`.
            2. Aggiungi la colonna `mese` con il nome del mese, ricavato con `dt.month_name()`, in modo che lo
               scatter abbia un colore per ogni mese invece di una scala continua.
            3. Disegna lo scatter con `px.scatter`, con la temperatura sulle x, il carico sulle y e
               `color="mese"`, e osserva che forma ha la nuvola e a quale temperatura il carico è più basso.
            4. Completa le cinque frasi della cella che segue la verifica, usando i numeri e i grafici ottenuti
               negli step precedenti.
        """,
        suggerimento="con `dt.month`, che restituisce un numero, Plotly usa una scala di colore continua, mentre con `dt.month_name()` ogni mese ha un colore distinto.",
        starter_base="""
            # 1. medie giornaliere di carico e temperatura
            df_indicizzato = df_completo.set_index("Date")
            giornaliero = df_indicizzato[["Total Load [MW]", "Temperature_C"]].resample(...).mean()
            giornaliero = giornaliero.reset_index()

            # 2. il nome del mese, per colorare i punti
            giornaliero["mese"] = ...

            # 3. lo scatter: temperatura sulle x, carico sulle y
            fig = px.scatter(giornaliero, x=..., y=..., color=..., hover_data=["Date"],
                             title="Carico medio giornaliero e temperatura media, zona Nord 2024-2025")
            fig.show()
        """,
        starter_avanzata="""
            giornaliero = ...

            fig = ...
            fig.show()
        """,
        soluzione="""
            df_indicizzato = df_completo.set_index("Date")
            giornaliero = df_indicizzato[["Total Load [MW]", "Temperature_C"]].resample("D").mean()
            giornaliero = giornaliero.reset_index()
            giornaliero["mese"] = giornaliero["Date"].dt.month_name()

            fig = px.scatter(giornaliero, x="Temperature_C", y="Total Load [MW]", color="mese", hover_data=["Date"],
                             title="Carico medio giornaliero e temperatura media, zona Nord 2024-2025",
                             labels={"Temperature_C": "temperatura media [°C]", "Total Load [MW]": "carico medio [MW]"})
            fig.show()
        """,
        verifica="""
            assert len(giornaliero) == 731, "❌ giornaliero: una riga per giorno, 731"
            assert {"Total Load [MW]", "Temperature_C", "mese"} <= set(giornaliero.columns), "❌ giornaliero: servono le colonne Total Load [MW], Temperature_C e mese"
            assert giornaliero["mese"].nunique() == 12, "❌ mese: i dodici mesi, da dt.month_name()"
        """,
        perche="Le medie giornaliere eliminano il ciclo delle ore all'interno della giornata e lasciano un solo valore per giorno, che si può confrontare direttamente con la temperatura media dello stesso giorno.",
    )
    nb.celle.append(Cella("md", nb_d("""
        **Il carico del Nord, 2024-2025**

        1. I dati sono ...: ... righe pulite, ... doppioni di ottobre tolti, ... quarti d'ora di marzo mancanti.
        2. L'energia giornaliera va da circa ... a circa ... MWh; i giorni più leggeri sono ...
        3. Nella giornata media il carico è minimo alle ... e massimo alle ...
        4. La domenica il carico medio sta intorno a ... MW, un giorno feriale intorno a ... MW.
        5. Il carico è più basso intorno a ... °C e sale con il freddo e con il caldo; pesa di più ...

        Fonte della temperatura: ... (Open-Meteo oppure i dati di esempio di `../Dati/fallback/`).
    """), solo_studente=True))
    nb.celle.append(Cella("md", box_html("soluzione", """
        1. I dati sono quartorari, non orari: 70.168 righe pulite, 8 doppioni di ottobre tolti (4 per anno),
           8 quarti d'ora di marzo mancanti, che restano un buco.
        2. L'energia giornaliera va da circa 280.000 MWh (1° gennaio 2024) a circa 645.000 MWh (luglio); i
           giorni più leggeri sono le feste, le domeniche e agosto.
        3. Nella giornata media il carico è minimo alle 3 (circa 14.300 MW) e massimo tra le 9 e le 11
           (circa 23.500 MW), con un secondo rialzo verso le 19.
        4. La domenica il carico medio sta intorno a 15.300 MW, un giorno feriale tra 20.400 e 21.900 MW.
        5. Il carico è più basso nelle giornate miti, intorno ai 15-20 °C, e sale con il freddo e con il caldo;
           al Nord pesa di più il caldo, con i massimi a luglio. I valori esatti dipendono dalla fonte della
           temperatura.
    """, titolo="Le cinque frasi"), solo_soluzioni=True))
    return nb

