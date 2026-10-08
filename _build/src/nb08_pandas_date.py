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
        intento="Le misure nel tempo arrivano spesso con timestamp di testo: li convertiamo in date per ordinarle, trovare i buchi, aggregarle per ore o giorni e togliere i duplicati dell'ora legale.",
        obiettivi=[
            "convertire testo in date con `pd.to_datetime` ed estrarne ora, giorno e mese",
            "usare il tempo come indice per selezionare periodi, trovare i buchi e cambiare granularità con `resample`",
            "riconoscere l'ora legale nei dati e togliere i duplicati del cambio d'ora",
        ],
        tempo={"base": 55, "avanzata": 55},
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
    """)
    nb.code("""
        intervallo = pd.date_range("2025-03-01 00:00", periods=3 * 24 * 4, freq="15min")

        # pattern giornaliero semplice + rumore: giusto per avere una serie "viva"
        ore = intervallo.hour + intervallo.minute / 60
        power_kw = 220 + 60 * np.sin(2 * np.pi * (ore / 24)) + np.random.normal(0, 8, size=len(intervallo))
        temp_c = 12 + 5 * np.sin(2 * np.pi * ((ore - 6) / 24)) + np.random.normal(0, 0.7, size=len(intervallo))

        df = pd.DataFrame({
            "timestamp_str": intervallo.strftime("%d/%m/%Y %H:%M"),  # formato tipico in Italia
            "power_kw": power_kw.round(1),
            "temp_c": temp_c.round(1),
        })

        # rimuoviamo alcune righe per simulare missing (buchi nella serie)
        indici_da_togliere = np.random.choice(df.index, size=18, replace=False)  # ~2.5% su 288 punti
        df = df.drop(indici_da_togliere).reset_index(drop=True)

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

        date_giorno_prima = pd.to_datetime(ambigue, dayfirst=True)
        date_mese_prima = pd.to_datetime(ambigue, dayfirst=False, errors="coerce")  # qui un valore diventa NaT

        pd.DataFrame({
            "stringa": ambigue,
            "dayfirst=True": date_giorno_prima,
            "dayfirst=False (coerce)": date_mese_prima,
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
        `set_index("timestamp")` mette la colonna al posto dell'indice numerico. Poi si ordina l'indice:
        con dati reali capita spesso di avere righe fuori ordine.

        Documentazione: [serie temporali, user guide]({DOC}/user_guide/timeseries.html)
    """)
    nb.code("""
        df_serie = (
            df[["timestamp", "power_kw", "temp_c"]]
            .set_index("timestamp")
            .sort_index()
        )

        df_serie.head()
    """)
    nb.code("""
        # slicing per periodo (anno/mese/giorno)
        df_serie.loc["2025-03-02"].head()
    """)
    nb.prova_tu(
        richiesta="""
            Seleziona in `periodo` le righe dal `2025-03-01 12:00` al `2025-03-01 18:00` usando `.loc[...]`.
            Sono 22 righe: in quelle sei ore ci sono tre buchi.
        """,
        starter="""
            periodo = df_serie.loc[...]
            len(periodo)  # Output: 22
        """,
        soluzione="""
            periodo = df_serie.loc["2025-03-01 12:00":"2025-03-01 18:00"]
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
        df_caratteristiche = df_serie.copy()
        df_caratteristiche["hour"] = df_caratteristiche.index.hour
        df_caratteristiche["dayofweek"] = df_caratteristiche.index.dayofweek  # 0=lunedì
        df_caratteristiche["month"] = df_caratteristiche.index.month

        df_caratteristiche.head()
    """)
    nb.prova_tu(
        richiesta="""
            Aggiungi a `df_caratteristiche_es` le colonne `date` (solo data) e `is_weekend` (`True` per sabato e domenica).
            Il 1° marzo 2025 è un sabato: le righe del weekend sono 182.

            Suggerimento: `df_caratteristiche_es.index.date` e `dayofweek` (sabato=5, domenica=6).
        """,
        starter="""
            df_caratteristiche_es = df_caratteristiche.copy()
            df_caratteristiche_es["date"] = ...
            df_caratteristiche_es["is_weekend"] = ...

            df_caratteristiche_es["is_weekend"].sum()  # Output: 182
        """,
        soluzione="""
            df_caratteristiche_es = df_caratteristiche.copy()
            df_caratteristiche_es["date"] = df_caratteristiche_es.index.date
            df_caratteristiche_es["is_weekend"] = df_caratteristiche_es["dayofweek"] >= 5

            df_caratteristiche_es["is_weekend"].sum()  # Output: 182
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
        df_serie.index.inferred_freq
    """)
    nb.md("""
        Non restituisce niente: con i buchi pandas non riesce a inferire una frequenza.
        La differenza tra timestamp consecutivi mostra cosa succede.
    """)
    nb.code("""
        df_serie.index.to_series().diff().value_counts().head()
    """)

    # ------------------------------------------------------------------ 7
    nb.sezione("Missing che emergono con l'allineamento", intro=f"""
        Quando "forzi" una frequenza regolare, i timestamp mancanti diventano righe con `NaN`.
        Questo è utile: rende visibili buchi che altrimenti restano nascosti.
        Qui usiamo `asfreq` per allineare a frequenza quartoraria (`15min`).

        Documentazione: [`DataFrame.asfreq`]({DOC}/reference/api/pandas.DataFrame.asfreq.html)
    """)
    nb.code("""
        df_15min = df_serie.asfreq("15min")
        df_15min
    """)
    nb.code("""
        conteggio_mancanti = df_15min.isna().sum()
        conteggio_mancanti
    """)
    nb.code("""
        # dove mancano i valori di power_kw?
        timestamp_mancanti = df_15min.index[df_15min["power_kw"].isna()]
        timestamp_mancanti[:10]
    """)
    nb.md("""
        I grafici qui sotto anticipano il notebook su Plotly: per ora si leggono e basta.
    """)
    nb.code("""
        # i dati prima e dopo asfreq: nel secondo grafico i buchi interrompono la linea
        import plotly.express as px

        fig = px.line(df_serie, x=df_serie.index, y="power_kw", title="Dati originali (con buchi)")
        fig.show()
        fig = px.line(df_15min, x=df_15min.index, y="power_kw", title="Dati con asfreq (buchi evidenziati)")
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
    nb.md("""
        **Backward fill**: `df.bfill()` fa il contrario, copia all'indietro il prossimo valore valido.
    """)
    nb.code("""
        # lavoriamo SOLO su power_kw
        s = df_15min["power_kw"]

        t0 = timestamp_mancanti[0]
        # finestra: da t0-45min a t0+45min
        idx = slice(t0 - pd.Timedelta(minutes=45), t0 + pd.Timedelta(minutes=45))

        # imputazioni (una colonna ciascuna)
        confronto = pd.DataFrame({
            "original": s.loc[idx],
            "time": s.interpolate(method="time").loc[idx],
            "linear": s.interpolate(method="linear").loc[idx],
            "ffill": s.ffill().loc[idx],
            "bfill": s.bfill().loc[idx],
        })

        confronto
    """)
    nb.md("""
        I metodi `time` e `linear` stimano il valore mancante interpolando tra i due punti vicini.
        Con frequenza regolare, i due metodi danno lo stesso risultato (qui 271.25).
    """)
    nb.code("""
        # visualizzazione con Plotly delle imputazioni
        import plotly.graph_objects as go

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=confronto.index, y=confronto["time"], mode="markers+lines", name="interpolate time"))
        fig.add_trace(go.Scatter(x=confronto.index, y=confronto["linear"], mode="markers+lines", name="interpolate linear"))
        fig.add_trace(go.Scatter(x=confronto.index, y=confronto["ffill"], mode="markers+lines", name="ffill"))
        fig.add_trace(go.Scatter(x=confronto.index, y=confronto["bfill"], mode="markers+lines", name="bfill"))
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
        df_15min = df_15min.interpolate(method="linear")
    """)
    nb.code("""
        orario = df_15min.resample("h").mean()
        giornaliero = df_15min.resample("D").mean()

        orario.head()
    """)
    nb.code("""
        giornaliero
    """)
    nb.prova_tu(
        richiesta="""
            Crea un resampling **orario** di `power_kw` con la somma (`sum`) invece della media, e confronta
            le prime righe con `orario`. La somma è 4 volte la media: in ogni ora ci sono 4 quarti d'ora.
        """,
        starter="""
            somma_oraria = df_15min...
            pd.DataFrame({"mean": orario["power_kw"], "sum": somma_oraria}).head()
        """,
        soluzione="""
            somma_oraria = df_15min["power_kw"].resample("h").sum()
            pd.DataFrame({"mean": orario["power_kw"], "sum": somma_oraria}).head()
        """,
    )

    # ------------------------------------------------------------------ 9
    nb.sezione("I duplicati dell'ora legale nei dati Terna", intro="""
        Le date in ora locale, senza fuso orario, seguono il cambio dell'ora legale: a fine marzo un'ora non
        esiste, a fine ottobre un'ora si ripete.
    """)
    nb.md("""
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
        Restano 35.132 righe invece di 35.136 (8784 ore per 4): i quattro quarti d'ora mancanti sono quelli
        dell'ora che a marzo non esiste.
    """)

    # ------------------------------------------------------------------ 10
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

    return nb
