"""08 · Pandas: le date."""

from nbkit import Notebook

DOC = "https://pandas.pydata.org/pandas-docs/stable"


def costruisci() -> Notebook:
    nb = Notebook(
        num="08",
        file="08_Pandas_date",
        titolo="Pandas: le date",
        blocco=3,
        giornata=2,
        intento="Le misure nel tempo arrivano spesso con timestamp di testo: li convertiamo in date per ordinarle, trovare i buchi, aggregarle per ore o giorni e gestire il fuso orario.",
        obiettivi={
            "base": [
                "convertire testo in date con `pd.to_datetime` ed estrarne ora, giorno e mese",
                "usare il tempo come indice per selezionare periodi, trovare i buchi e cambiare granularità con `resample`",
                "riconoscere fuso orario e ora legale e togliere i duplicati del cambio d'ora",
            ],
            "avanzata": [
                "convertire testo in date con `pd.to_datetime` ed estrarne ora, giorno e mese",
                "usare il tempo come indice per trovare i buchi e cambiare granularità con `resample`",
                "costruire lag e medie mobili con `shift` e `rolling` e gestire l'ora legale",
            ],
        },
        tempo={"base": 70, "avanzata": 80},
        dati=["load_total_north_hourly_2024.xlsx"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Dataset toy", intro="""
        Costruiamo un dataset piccolo ma realistico: misure quartorarie di potenza (`power_kw`) e temperatura (`temp_c`).
        Il timestamp è intenzionalmente una **stringa** in formato italiano (`DD/MM/YYYY HH:MM`).
        Poi inseriamo qualche buco per simulare acquisizioni mancanti.
    """)
    nb.code("""
        import numpy as np
        np.random.seed(42)
        import pandas as pd

        pd.set_option("display.max_rows", 10)
        pd.set_option("display.max_columns", 20)

        rng = pd.date_range("2025-03-01 00:00", periods=3 * 24 * 4, freq="15min")

        # pattern giornaliero semplice + rumore: giusto per avere una serie "viva"
        hours = rng.hour + rng.minute / 60
        power_kw = 220 + 60 * np.sin(2 * np.pi * (hours / 24)) + np.random.normal(0, 8, size=len(rng))
        temp_c = 12 + 5 * np.sin(2 * np.pi * ((hours - 6) / 24)) + np.random.normal(0, 0.7, size=len(rng))

        df = pd.DataFrame({
            "timestamp_str": rng.strftime("%d/%m/%Y %H:%M"),  # formato tipico in Italia
            "power_kw": power_kw.round(1),
            "temp_c": temp_c.round(1),
        })

        # rimuoviamo alcune righe per simulare missing (buchi nella serie)
        drop_idx = np.random.choice(df.index, size=18, replace=False)  # ~2.5% su 288 punti
        df = df.drop(drop_idx).reset_index(drop=True)

        df.head()
    """)
    nb.md("""
        `df.dtypes` conferma che `timestamp_str` è testo (`str`).
    """)
    nb.code("""
        df.dtypes
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("`datetime` in pandas", intro=f"""
        Una colonna di testo che "sembra una data" resta testo. `pd.to_datetime` la trasforma in un tipo
        temporale (`datetime64`) che si può ordinare, filtrare per periodo e usare per calcolare intervalli.

        Documentazione: [`pd.to_datetime`]({DOC}/reference/api/pandas.to_datetime.html)
    """)
    nb.code("""
        df["timestamp"] = pd.to_datetime(df["timestamp_str"], dayfirst=True)
        df[["timestamp_str", "timestamp"]].head()
    """)
    nb.code("""
        df.dtypes
    """)
    nb.box("nota", """
        In Italia il caso più comune è `giorno/mese/anno`, quindi `dayfirst=True` è spesso la scelta corretta.
        Quando il formato è noto e stabile, `format=...` rende la conversione più affidabile.
    """)
    nb.prova_tu(
        richiesta="""
            Crea una nuova colonna `timestamp_2` convertendo di nuovo `timestamp_str`, ma questa volta con
            `format="%d/%m/%Y %H:%M"`. Confronta le prime 5 righe con `timestamp`: devono coincidere.
        """,
        starter="""
            df["timestamp_2"] = pd.to_datetime(df["timestamp_str"], format=...)
            df[["timestamp", "timestamp_2"]].head()
        """,
        soluzione="""
            df["timestamp_2"] = pd.to_datetime(df["timestamp_str"], format="%d/%m/%Y %H:%M")
            df[["timestamp", "timestamp_2"]].head()
        """,
    )

    # ------------------------------------------------------------------ 3
    nb.sezione("Formati", intro="""
        Il formato serve soprattutto quando la stringa è **ambigua** o non standard.
        Esempio classico: `01/02/2025` può essere 1 febbraio oppure 2 gennaio (dipende dal contesto).
    """)
    nb.code("""
        # esempio di ambiguità giorno/mese + gestione errori
        ambigue = pd.Series(["01/02/2025 08:00", "13/02/2025 08:00"])

        parsed_dayfirst = pd.to_datetime(ambigue, dayfirst=True)
        parsed_monthfirst = pd.to_datetime(ambigue, dayfirst=False, errors="coerce")  # qui un valore diventa NaT

        pd.DataFrame({
            "stringa": ambigue,
            "dayfirst=True": parsed_dayfirst,
            "dayfirst=False (coerce)": parsed_monthfirst,
        })
    """)
    nb.md("""
        Senza `errors="coerce"` vale il default, `errors="raise"`: la conversione si ferma con un errore
        sul primo valore che non torna. Questa cella dà errore apposta.
    """)
    nb.code("""
        pd.to_datetime(ambigue, dayfirst=False, errors="raise")
    """, errore=True)

    # ------------------------------------------------------------------ 4
    nb.sezione("Il tempo come indice", intro=f"""
        Quando il timestamp è l'indice, pandas abilita selezioni "per periodo" senza calcoli manuali.
        Prima di tutto: ordinare l'indice. Con dati reali capita spesso di avere righe fuori ordine.

        Documentazione: [serie temporali, user guide]({DOC}/user_guide/timeseries.html)
    """)
    nb.code("""
        df_ts = (
            df[["timestamp", "power_kw", "temp_c"]]
            .set_index("timestamp")
            .sort_index()
        )

        df_ts.head()
    """)
    nb.code("""
        # slicing per periodo (anno/mese/giorno)
        df_ts.loc["2025-03-02"].head()
    """)
    nb.prova_tu(
        richiesta="""
            Seleziona in `periodo` le righe dal `2025-03-01 12:00` al `2025-03-01 18:00` usando `.loc[...]`.
            Sono 22 righe: in quelle sei ore ci sono tre buchi.
        """,
        starter="""
            periodo = df_ts.loc[...]
            len(periodo)  # Output: 22
        """,
        soluzione="""
            periodo = df_ts.loc["2025-03-01 12:00":"2025-03-01 18:00"]
            len(periodo)  # Output: 22
        """,
    )

    # ------------------------------------------------------------------ 5
    nb.sezione("Attributi temporali", intro=f"""
        Una volta che il tempo è `datetime`, estrarre componenti temporali diventa semplice (mese, ora, giorno della settimana).
        Se il tempo è indice, si lavora via `df.index`; se è una colonna, si usa `.dt`.

        Documentazione: [accessor `.dt`]({DOC}/reference/api/pandas.Series.dt.html)
    """)
    nb.code("""
        df_feat = df_ts.copy()
        df_feat["hour"] = df_feat.index.hour
        df_feat["dayofweek"] = df_feat.index.dayofweek  # 0=lunedì
        df_feat["month"] = df_feat.index.month

        df_feat.head()
    """)
    nb.prova_tu(
        richiesta="""
            Aggiungi a `df_feat_ex` le colonne `date` (solo data) e `is_weekend` (`True` per sabato e domenica).
            Il 1° marzo 2025 è un sabato: le righe del weekend sono 182.

            Suggerimento: `df_feat_ex.index.date` e `dayofweek` (sabato=5, domenica=6).
        """,
        starter="""
            df_feat_ex = df_feat.copy()
            df_feat_ex["date"] = ...
            df_feat_ex["is_weekend"] = ...

            df_feat_ex["is_weekend"].sum()  # Output: 182
        """,
        soluzione="""
            df_feat_ex = df_feat.copy()
            df_feat_ex["date"] = df_feat_ex.index.date
            df_feat_ex["is_weekend"] = df_feat_ex["dayofweek"] >= 5

            df_feat_ex["is_weekend"].sum()  # Output: 182
        """,
    )

    # ------------------------------------------------------------------ 6
    nb.sezione("Frequenza", intro=f"""
        "Frequenza" significa intervallo atteso tra due timestamp consecutivi (15 minuti, 1 ora, 1 giorno).
        Con dati puliti e regolari, pandas può inferirla; con buchi o irregolarità spesso no.
        Frequenze comuni: `15min` (quartorario), `h` (orario), `D` (giornaliero), `MS` (inizio mese).

        Documentazione: [alias delle frequenze]({DOC}/user_guide/timeseries.html#dateoffset-objects)
    """)
    nb.code("""
        df_ts.index.inferred_freq
    """)
    nb.md("""
        Non restituisce niente: con i buchi pandas non riesce a inferire una frequenza.
        La differenza tra timestamp consecutivi mostra cosa succede.
    """)
    nb.code("""
        df_ts.index.to_series().diff().value_counts().head()
    """)

    # ------------------------------------------------------------------ 7
    nb.sezione("Missing che emergono con l'allineamento", intro=f"""
        Quando "forzi" una frequenza regolare, i timestamp mancanti diventano righe con `NaN`.
        Questo è utile: rende visibili buchi che altrimenti restano nascosti.
        Qui usiamo `asfreq` per allineare a frequenza quartoraria (`15min`).

        Documentazione: [`DataFrame.asfreq`]({DOC}/reference/api/pandas.DataFrame.asfreq.html)
    """)
    nb.code("""
        df_qh = df_ts.asfreq("15min")
        df_qh
    """)
    nb.code("""
        missing_counts = df_qh.isna().sum()
        missing_counts
    """)
    nb.code("""
        # dove mancano i valori di power_kw?
        missing_timestamps = df_qh.index[df_qh["power_kw"].isna()]
        missing_timestamps[:10]
    """)
    nb.code("""
        # i dati prima e dopo asfreq: nel secondo grafico i buchi interrompono la linea
        import plotly.express as px

        fig = px.line(df_ts, x=df_ts.index, y="power_kw", title="Dati originali (con buchi)")
        fig.show()
        fig = px.line(df_qh, x=df_qh.index, y="power_kw", title="Dati con asfreq (buchi evidenziati)")
        fig.show()
    """)
    nb.md("""
        Ora che abbiamo individuato i valori mancanti, dobbiamo decidere come gestirli. Due approcci semplici e comuni.

        **Interpolazione lineare**: pandas collega il valore prima e dopo il buco con una retta. Se alle 10:00
        abbiamo 200 kW, alle 11:00 220 kW e manca il valore delle 10:30, stima 210 kW. Utile quando il fenomeno
        cambia gradualmente (una temperatura). Comando: `df.interpolate(method="linear")`.
    """)
    nb.md("""
        **Forward fill** (riempimento in avanti): copia l'ultimo valore valido nei buchi successivi. Utile
        quando il valore resta stabile per un po' (lo stato di un dispositivo). Comando: `df.ffill()`.
    """)
    nb.code("""
        # lavoriamo SOLO su power_kw
        s = df_qh["power_kw"]

        t0 = missing_timestamps[0]
        # finestra: da t0-45min a t0+45min
        idx = slice(
            t0 - pd.Timedelta(minutes=45),
            t0 + pd.Timedelta(minutes=45),
        )

        # imputazioni (una colonna ciascuna)
        out = pd.DataFrame({
            "original": s.loc[idx],
            "time": s.interpolate(method="time").loc[idx],
            "linear": s.interpolate(method="linear").loc[idx],
            "ffill": s.ffill().loc[idx],
            "bfill": s.bfill().loc[idx],
        })

        out
    """)
    nb.md("""
        I metodi `time` e `linear` stimano il valore mancante interpolando tra i due punti vicini.
        Con frequenza regolare, i due metodi danno lo stesso risultato (qui 271.25).
    """)
    nb.code("""
        # visualizzazione con Plotly delle imputazioni
        import plotly.graph_objects as go

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=out.index, y=out["time"], mode="markers+lines", name="interpolate time"))
        fig.add_trace(go.Scatter(x=out.index, y=out["linear"], mode="markers+lines", name="interpolate linear"))
        fig.add_trace(go.Scatter(x=out.index, y=out["ffill"], mode="markers+lines", name="ffill"))
        fig.add_trace(go.Scatter(x=out.index, y=out["bfill"], mode="markers+lines", name="bfill"))
        fig.update_layout(title="Imputazioni per missing value", height=400, width=700)
        fig.show()
    """)

    # ------------------------------------------------------------------ 8
    nb.sezione("Resampling", intro=f"""
        Il resampling cambia granularità temporale: da quartorario a orario, giornaliero, mensile.
        È un'operazione di aggregazione guidata dal tempo (non dalla posizione delle righe).

        Documentazione: [`resample`]({DOC}/reference/api/pandas.DataFrame.resample.html)
    """)
    nb.md("""
        Prima riempiamo i buchi con l'interpolazione lineare.
    """)
    nb.code("""
        df_qh = df_qh.interpolate(method="linear")
    """)
    nb.code("""
        hourly = df_qh.resample("h").mean()
        daily = df_qh.resample("D").mean()

        hourly.head()
    """)
    nb.code("""
        daily
    """)
    nb.prova_tu(
        richiesta="""
            Crea un resampling **orario** di `power_kw` con la somma (`sum`) invece della media, e confronta
            le prime righe con `hourly`. La somma è 4 volte la media: in ogni ora ci sono 4 quarti d'ora.
        """,
        starter="""
            hourly_sum = df_qh...
            pd.DataFrame({"mean": hourly["power_kw"], "sum": hourly_sum}).head()
        """,
        soluzione="""
            hourly_sum = df_qh["power_kw"].resample("h").sum()
            pd.DataFrame({"mean": hourly["power_kw"], "sum": hourly_sum}).head()
        """,
    )

    # ------------------------------------------------------------------ 9 (A)
    with nb.solo("avanzata"):
        nb.sezione("Shift e rolling", intro=f"""
            Due operazioni semplici e molto usate nella gestione di time series:

            - `shift(k)`: sposta i valori di `k` step nel tempo (crea "lag").
            - `rolling(w)`: calcola statistiche su una finestra mobile di ampiezza `w`.

            Entrambe possono introdurre `NaN` in testa (perché mancano i valori "precedenti").
            Documentazione: [`rolling`]({DOC}/reference/api/pandas.DataFrame.rolling.html)
        """)
        nb.code("""
            df_sr = df_qh.copy()

            # lag di 1 ora: con frequenza 15min corrisponde a 4 step
            df_sr["power_lag_4"] = df_sr["power_kw"].shift(4)

            # media mobile su 2 ore: 8 step
            df_sr["power_ma_8"] = df_sr["power_kw"].rolling(8).mean()

            df_sr[["power_kw", "power_lag_4", "power_ma_8"]].head(12)
        """)
        nb.code("""
            # shift di 1 ora (4 step) contro power_kw
            fig = px.line(df_sr, x=df_sr.index, y=["power_kw", "power_lag_4"], title="Shift di 1 ora (4 step)")
            fig.show()
        """)
        nb.code("""
            # media mobile su una finestra di 2 ore (8 step) contro power_kw
            fig = px.line(df_sr, x=df_sr.index, y=["power_kw", "power_ma_8"], title="Media mobile su finestra di 2 ore (8 step)")
            fig.show()
        """)

    # ------------------------------------------------------------------ 10
    nb.sezione("Differenze tra date", intro="""
        Le differenze tra timestamp producono `Timedelta` (durate).
        Servono sia per capire la regolarità della serie sia per misurare intervalli (es. "quante ore copre il dataset?").
    """)
    nb.code("""
        # differenze tra timestamp consecutivi
        delta_consecutivi = df_qh.index.to_series().diff()

        delta_consecutivi.head(10)
    """)
    nb.code("""
        # intervallo totale coperto
        delta_totale = df_qh.index.max() - df_qh.index.min()
        delta_totale
    """)
    nb.code("""
        # durata in ore (float)
        delta_totale.total_seconds() / 3600
    """)

    # ------------------------------------------------------------------ 11
    nb.sezione("Fuso orario e ora legale", intro=f"""
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
        df_tz = df_qh.copy()

        # interpretiamo i timestamp come orari locali italiani
        df_tz.index = df_tz.index.tz_localize("Europe/Rome")

        # conversione a UTC (utile per sistemi e confronti)
        df_utc = df_tz.tz_convert("UTC")

        df_tz.index[:3], df_utc.index[:3]
    """)
    nb.code("""
        df_tz.loc["2025-03-01 06:00":"2025-03-01 12:00"].head()
    """)
    nb.sottosezione("I duplicati dell'ora legale nei dati Terna", intro="""
        Nei dati veri il cambio d'ora si vede. Il carico della zona Nord 2024 di Terna è in ora locale, un valore
        ogni 15 minuti (il nome del file dice `hourly`), con le righe dall'ultima alla prima. Le rimettiamo in
        ordine con `sort_values` e contiamo i timestamp duplicati.
    """)
    nb.code("""
        carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico = carico.sort_values("Date")
        carico["Date"].duplicated().sum()
    """)
    nb.code("""
        doppioni = carico["Date"].duplicated(keep=False)
        carico[doppioni]
    """)
    nb.md("""
        Le 2:00, 2:15, 2:30 e 2:45 del 27 ottobre, l'ultima domenica del mese, compaiono due volte con carichi
        diversi: una è l'ultima ora legale, l'altra la prima ora solare, e il file non dice quale sia quale.
        `drop_duplicates(subset="Date")` tiene la prima occorrenza di ogni timestamp.
    """)
    nb.code("""
        carico = carico.drop_duplicates(subset="Date")
        len(carico)
    """)
    nb.md("""
        35.132 righe: un'ora persa su 8784. A marzo succede il contrario: l'ultima domenica le 2:00 non
        esistono, e nel file mancano quattro quarti d'ora.
    """)

    # ------------------------------------------------------------------ 12
    nb.sezione("Esercizi", intro="""
        Gli esercizi usano `carico`, il file Terna già ordinato e senza duplicati. La colonna
        `Total Load [MW]` è una potenza media su ogni quarto d'ora: un quarto d'ora a 100 MW sono 25 MWh,
        quindi l'energia si ottiene sommando i valori e dividendo per 4.
    """)
    nb.esercizio(
        titolo="Il carico giornaliero",
        scenario="Dal carico quartorario vogliamo l'energia consumata ogni giorno del 2024 nella zona Nord.",
        richiesta="""
            1. Metti in `serie` la colonna `Total Load [MW]` di `carico`, con `Date` come indice (`set_index`).
            2. Calcola in `giornaliero` l'energia di ogni giorno in MWh: `resample("D")`, `sum()`, poi diviso 4.
            3. Metti in `giorno_max` il giorno con l'energia più alta (`idxmax()`).
        """,
        starter="""
            serie = ...
            giornaliero = ...
            giorno_max = ...

            print(len(giornaliero))  # Output: 366
            giorno_max
        """,
        soluzione="""
            serie = carico.set_index("Date")["Total Load [MW]"]
            giornaliero = serie.resample("D").sum() / 4
            giorno_max = giornaliero.idxmax()

            print(len(giornaliero))  # Output: 366
            giorno_max
        """,
        verifica="""
            assert len(giornaliero) == 366, "❌ giornaliero: un valore per ogni giorno del 2024, con resample('D')"
            assert round(giornaliero.max()) == 644863, "❌ giornaliero: somma dei quarti d'ora del giorno, divisa per 4"
            assert giorno_max == pd.Timestamp("2024-07-17"), "❌ giorno_max: usa giornaliero.idxmax()"
        """,
        suggerimento="si seleziona la colonna prima di `resample`, così la colonna di testo `Bidding Zone` resta fuori.",
    )
    nb.esercizio(
        titolo="Ora e giorno della settimana",
        scenario="Vogliamo sapere a che ora del giorno e in quale giorno della settimana il carico medio è più alto e più basso.",
        richiesta="""
            1. Aggiungi a `carico` le colonne `ora` (`.dt.hour`) e `giorno_settimana` (`.dt.dayofweek`, 0=lunedì) a partire da `Date`.
            2. Calcola in `per_ora` il carico medio per ora con `groupby`, e in `ora_di_punta` l'ora con la media più alta.
            3. Calcola in `per_giorno` il carico medio per giorno della settimana, e in `giorno_minimo` il giorno con la media più bassa.
        """,
        starter="""
            carico["ora"] = ...
            carico["giorno_settimana"] = ...

            per_ora = ...
            ora_di_punta = ...

            per_giorno = ...
            giorno_minimo = ...

            print(ora_di_punta, giorno_minimo)
        """,
        soluzione="""
            carico["ora"] = carico["Date"].dt.hour
            carico["giorno_settimana"] = carico["Date"].dt.dayofweek

            per_ora = carico.groupby("ora")["Total Load [MW]"].mean()
            ora_di_punta = per_ora.idxmax()

            per_giorno = carico.groupby("giorno_settimana")["Total Load [MW]"].mean()
            giorno_minimo = per_giorno.idxmin()

            print(ora_di_punta, giorno_minimo)
        """,
        verifica="""
            assert len(per_ora) == 24 and len(per_giorno) == 7, "❌ per_ora e per_giorno: groupby su ora e su giorno_settimana"
            assert ora_di_punta == 11, "❌ ora_di_punta: idxmax() della media per ora"
            assert giorno_minimo == 6, "❌ giorno_minimo: idxmin() della media per giorno della settimana (6 = domenica)"
        """,
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
