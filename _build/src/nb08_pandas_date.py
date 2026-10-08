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
        intento="Le misure raccolte nel tempo arrivano spesso con timestamp scritti come testo, che vanno convertiti in date prima di poterli ordinare, cercarvi i buchi, aggregarli per ore o per giorni e togliere i duplicati dovuti all'ora legale.",
        obiettivi=[
            "convertire testo in date con `pd.to_datetime` ed estrarne ora, giorno e mese",
            "usare il tempo come indice per selezionare periodi, trovare i buchi e cambiare granularità con `resample`",
            "riconoscere l'ora legale nei dati e togliere i duplicati del cambio d'ora",
        ],
        tempo={"base": 55, "avanzata": 55},
        dati=["load_total_north_hourly_2024.xlsx"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Un dataset di prova", intro="""
        Per cominciare costruiamo un dataset piccolo ma realistico, con tre giorni di misure quartorarie di potenza
        (`power_kw`) e di temperatura (`temp_c`). Il timestamp è volutamente una **stringa** in formato italiano
        (`DD/MM/YYYY HH:MM`), come capita spesso con i file esportati da un gestionale o da un foglio di calcolo.
        Togliamo poi qualche riga scelta a caso per simulare le acquisizioni mancanti, che ritroveremo più avanti
        come buchi nella serie.
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
        L'attributo `dtypes` mostra il tipo di ogni colonna e conferma che `timestamp_str` è testo (`str`), mentre
        le due misure sono numeri decimali. Finché la colonna resta testo, pandas non sa che rappresenta degli
        istanti nel tempo e non può ordinarla né selezionarne un periodo.
    """)
    nb.code("""
        df.dtypes
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("`datetime` in pandas", intro=f"""
        Una colonna di testo resta testo anche quando il suo contenuto ha l'aspetto di una data. La funzione
        `pd.to_datetime` la converte in un tipo temporale (`datetime64`), che si può ordinare, filtrare per periodo
        e usare per calcolare intervalli. Con `dayfirst=True` indichiamo che nella stringa il giorno viene prima del
        mese, e la seconda cella mostra con `dtypes` che la nuova colonna `timestamp` ha il tipo temporale. La
        documentazione di riferimento è [`pd.to_datetime`]({DOC}/reference/api/pandas.to_datetime.html).
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
        Quando il formato è noto e non cambia da una riga all'altra, conviene però indicarlo per esteso con
        `format=...`, perché pandas non deve più dedurlo e la conversione diventa più affidabile.
    """)
    nb.prova_tu(
        richiesta="""
            Crea una nuova colonna `timestamp_2` convertendo di nuovo `timestamp_str`, ma questa volta con
            `format="%d/%m/%Y %H:%M"`. Poi confronta le prime cinque righe con la colonna `timestamp`: le due
            colonne devono coincidere, perché `dayfirst=True` e `format` descrivono in due modi lo stesso formato.
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
        Indicare il formato serve soprattutto quando la stringa è **ambigua** o non standard. Il caso classico è
        `01/02/2025`, che in Italia si legge 1 febbraio e negli Stati Uniti 2 gennaio, e soltanto il contesto dice
        quale delle due letture sia quella giusta. Nella cella qui sotto convertiamo due stringhe in entrambi i modi.
        Con `dayfirst=False` la seconda, `13/02/2025`, non è una data valida perché non esiste un tredicesimo mese,
        e `errors="coerce"` la trasforma in `NaT`, il valore mancante delle date.
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
        Senza `errors="coerce"` vale il comportamento predefinito, `errors="raise"`, e la conversione si interrompe
        con un errore al primo valore che non riesce a interpretare. La cella qui sotto dà errore di proposito, per
        mostrare il messaggio che si ottiene. Con un file reale questo comportamento è spesso preferibile, perché
        segnala subito le righe sbagliate invece di confonderle con i valori mancanti.
    """)
    nb.code("""
        pd.to_datetime(ambigue, dayfirst=False, errors="raise")
    """, errore=True)

    # ------------------------------------------------------------------ 4
    nb.sezione("Il tempo come indice", intro=f"""
        Quando il timestamp diventa l'indice del DataFrame, pandas permette di selezionare le righe per periodo,
        indicando un giorno o un intervallo di date senza fare calcoli. Il metodo `set_index("timestamp")` mette la
        colonna al posto dell'indice numerico, e `sort_index()` ordina le righe nel tempo. Conviene ordinare sempre,
        perché nei dati reali capita spesso di avere righe fuori ordine. La documentazione di riferimento è la
        [user guide sulle serie temporali]({DOC}/user_guide/timeseries.html).
    """)
    nb.code("""
        df_serie = (
            df[["timestamp", "power_kw", "temp_c"]]
            .set_index("timestamp")
            .sort_index()
        )

        df_serie.head()
    """)
    nb.md("""
        Con un indice temporale, `loc` accetta anche una data scritta solo in parte. La stringa `"2025-03-02"`
        seleziona tutte le righe di quel giorno, dalla mezzanotte alle 23:45, e allo stesso modo `"2025-03"`
        selezionerebbe l'intero mese.
    """)
    nb.code("""
        # slicing per periodo (anno/mese/giorno)
        df_serie.loc["2025-03-02"].head()
    """)
    nb.prova_tu(
        richiesta="""
            Seleziona in `periodo` le righe dal `2025-03-01 12:00` al `2025-03-01 18:00` usando `.loc[...]` con
            un intervallo tra due stringhe. Il risultato ha 22 righe, perché nelle sei ore considerate, che con gli
            estremi inclusi corrispondono a 25 quarti d'ora, mancano tre misure.
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
        Una volta convertito in `datetime`, il tempo si scompone facilmente nelle sue parti, come l'ora, il giorno
        della settimana o il mese, che servono per esempio a confrontare le ore del giorno o i giorni feriali con il
        weekend. Se il tempo è l'indice, queste parti si leggono direttamente da `df.index`; se invece è una colonna,
        si passa dall'accessor `.dt`, come in `df["timestamp"].dt.hour`. Nella cella qui sotto aggiungiamo tre
        colonne ricavate dall'indice. La documentazione di riferimento è quella
        dell'[accessor `.dt`]({DOC}/reference/api/pandas.Series.dt.html).
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
            Aggiungi a `df_caratteristiche_es` la colonna `date`, con la sola data senza l'ora, e la colonna
            `is_weekend`, che vale `True` il sabato e la domenica. La data si ricava da `df_caratteristiche_es.index.date`,
            mentre per il weekend basta confrontare la colonna `dayofweek` con 5, il valore del sabato (la domenica
            vale 6). Poiché il 1° marzo 2025 è un sabato, i primi due giorni del dataset cadono nel weekend e le
            righe con `is_weekend` uguale a `True` sono 182.
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
        La frequenza di una serie temporale è l'intervallo atteso tra due timestamp consecutivi, per esempio
        15 minuti, un'ora o un giorno. Quando i dati sono regolari pandas la deduce da solo, e la riporta in
        `inferred_freq`, mentre in presenza di buchi o irregolarità di solito non ci riesce. Le frequenze si
        indicano con brevi codici, detti alias, e i più comuni sono `15min` per i quarti d'ora, `h` per le ore,
        `D` per i giorni e `MS` per l'inizio del mese. La documentazione di riferimento è l'elenco degli
        [alias delle frequenze]({DOC}/user_guide/timeseries.html#dateoffset-objects).
    """)
    nb.code("""
        df_serie.index.inferred_freq
    """)
    nb.md("""
        La cella precedente non restituisce nulla, perché i buchi impediscono a pandas di riconoscere una frequenza.
        Per capire che cosa succede calcoliamo con `diff()` la distanza tra ogni timestamp e il precedente, e contiamo
        quante volte compare ciascun intervallo. La maggior parte degli intervalli vale 15 minuti, ma ne compaiono
        anche alcuni da 30 e da 45 minuti, in corrispondenza delle misure mancanti.
    """)
    nb.code("""
        df_serie.index.to_series().diff().value_counts().head()
    """)

    # ------------------------------------------------------------------ 7
    nb.sezione("I valori mancanti dopo l'allineamento", intro=f"""
        Il metodo `asfreq` impone alla serie una frequenza regolare, in questo caso un valore ogni quarto d'ora
        (`15min`). Per ogni istante previsto dalla griglia che non compare nei dati viene aggiunta una riga con `NaN`.
        In questo modo i buchi di acquisizione, che in una serie irregolare passano inosservati, diventano righe
        visibili che si possono contare e trattare. La documentazione di riferimento è
        [`DataFrame.asfreq`]({DOC}/reference/api/pandas.DataFrame.asfreq.html).
    """)
    nb.code("""
        df_15min = df_serie.asfreq("15min")
        df_15min
    """)
    nb.md("""
        Il metodo `isna()`, seguito da `sum()`, conta i valori mancanti di ogni colonna, che sono 18 come le righe
        tolte all'inizio. Usando la stessa condizione come maschera sull'indice otteniamo invece gli istanti esatti
        in cui manca la misura di `power_kw`, che ci serviranno tra poco per guardare da vicino il primo buco.
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
        I due grafici qui sotto mettono a confronto la serie prima e dopo `asfreq`. Nel primo la linea unisce i punti
        rimasti e scavalca i buchi senza che si notino, mentre nel secondo ogni `NaN` interrompe la linea e i buchi
        diventano visibili. Il codice anticipa il notebook su Plotly, quindi per ora basta guardare il risultato.
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
        Individuati i valori mancanti, bisogna decidere come trattarli. L'interpolazione lineare, con
        `df.interpolate(method="linear")`, collega con una retta il valore prima e quello dopo il buco: se alle
        10:00 abbiamo 200 kW, alle 11:00 220 kW e manca il valore delle 10:30, la stima è 210 kW. È adatta ai
        fenomeni che cambiano gradualmente, come una temperatura. Il forward fill, con `df.ffill()`, copia invece
        l'ultimo valore valido nei buchi successivi e si usa per grandezze che restano stabili per un certo tempo,
        come lo stato di un dispositivo, mentre `df.bfill()` copia all'indietro il primo valore valido che segue.
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
        Nella tabella, costruita su una finestra di 45 minuti prima e dopo il primo buco, le colonne `time` e `linear`
        stimano il valore mancante interpolando tra i due punti vicini. Il metodo `time` tiene conto della distanza
        effettiva tra i timestamp, mentre `linear` tratta le righe come equidistanti. Dopo `asfreq` le righe sono
        tutte a distanza costante, quindi i due metodi danno lo stesso risultato, in questo caso 271.25.
        Il grafico qui sotto mette a confronto le quattro imputazioni.
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
        Il resampling cambia la granularità temporale di una serie, per esempio da quartoraria a oraria, giornaliera
        o mensile. È un'aggregazione guidata dal tempo e non dalla posizione delle righe, perché `resample("h")`
        raccoglie in un gruppo tutte le misure della stessa ora, e il metodo che segue, come `mean()` o `sum()`,
        stabilisce come combinarle. Prima di aggregare riempiamo i buchi con l'interpolazione lineare, così ogni ora
        contiene i suoi quattro quarti d'ora. La documentazione di riferimento è
        [`resample`]({DOC}/reference/api/pandas.DataFrame.resample.html).
    """)
    nb.code("""
        df_15min = df_15min.interpolate(method="linear")
    """)
    nb.md("""
        Con la serie completa calcoliamo la media oraria con `resample("h").mean()` e quella giornaliera con
        `resample("D").mean()`. Il risultato orario ha 72 righe, una per ogni ora dei tre giorni, mentre quello
        giornaliero ne ha soltanto tre, e la cella successiva lo mostra per intero.
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
            Calcola in `somma_oraria` il resampling **orario** di `power_kw` usando la somma (`sum`) al posto della
            media, e confronta le prime righe con quelle di `orario`. Ogni valore della somma è quattro volte la media
            corrispondente, perché in ogni ora ci sono quattro quarti d'ora.
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
        Le date espresse in ora locale, senza indicazione del fuso orario, seguono il cambio dell'ora legale.
        L'ultima domenica di marzo gli orologi passano dalle 2:00 alle 3:00 e un'ora non esiste, mentre l'ultima
        domenica di ottobre tornano dalle 3:00 alle 2:00 e un'ora si ripete. I dati di Terna sul carico della zona
        Nord nel 2024 sono in ora locale, con un valore ogni 15 minuti nonostante il nome del file contenga `hourly`,
        e hanno le righe in ordine inverso, dalla più recente alla più vecchia. Per questo li rimettiamo in ordine
        con `sort_values` e poi contiamo i timestamp duplicati.
    """)
    nb.code("""
        carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico = carico.sort_values("Date")
        carico["Date"].duplicated().sum()
    """)
    nb.md("""
        Con `keep=False` il metodo `duplicated` segna tutte le occorrenze di un timestamp ripetuto, e non soltanto
        quelle successive alla prima, in modo da poter vedere le righe doppie una accanto all'altra.
    """)
    nb.code("""
        doppioni = carico["Date"].duplicated(keep=False)
        carico[doppioni]
    """)
    nb.md("""
        I timestamp delle 2:00, 2:15, 2:30 e 2:45 del 27 ottobre, l'ultima domenica del mese, compaiono due volte
        con carichi diversi. Una delle due ore è l'ultima dell'ora legale e l'altra la prima dell'ora solare, ma il
        file non permette di distinguerle. La soluzione più semplice è tenere una sola riga per timestamp con
        `drop_duplicates(subset="Date")`, che conserva la prima occorrenza e scarta le successive.
    """)
    nb.code("""
        carico = carico.drop_duplicates(subset="Date")
        len(carico)
    """)
    nb.md("""
        Dopo la pulizia restano 35.132 righe. Il 2024 è bisestile e ha 8784 ore, cioè 35.136 quarti d'ora, e i
        quattro valori che mancano sono quelli dell'ora che il 31 marzo non esiste.
    """)

    # ------------------------------------------------------------------ 10
    nb.sezione("Esercizi", intro="""
        Gli esercizi usano `carico`, il DataFrame di Terna già ordinato e senza duplicati. La colonna
        `Total Load [MW]` contiene la potenza media di ogni quarto d'ora, e per passare all'energia bisogna tenere
        conto della durata dell'intervallo. Un quarto d'ora a 100 MW corrisponde a 25 MWh, quindi l'energia di un
        periodo si ottiene sommando i valori e dividendo il risultato per 4.
    """)
    nb.esercizio(
        titolo="Il carico giornaliero",
        scenario="""
            A partire dal carico quartorario vogliamo calcolare l'energia consumata nella zona Nord in ciascun giorno
            del 2024 e trovare il giorno in cui il consumo è stato più alto.
        """,
        richiesta="""
            1. Metti in `serie` la colonna `Total Load [MW]` di `carico`, dopo aver impostato `Date` come indice con `set_index`.
            2. Calcola in `giornaliero` l'energia di ogni giorno in MWh, raggruppando per giorno con `resample("D")`, sommando con `sum()` e dividendo il risultato per 4.
            3. Metti in `giorno_max` il giorno con l'energia più alta, che si ottiene con `idxmax()`.

            Il risultato `giornaliero` è una Series con 366 valori, uno per ogni giorno dell'anno bisestile.
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
        suggerimento="conviene selezionare la colonna prima di chiamare `resample`, in modo che la colonna di testo `Bidding Zone` resti fuori dalla somma.",
    )
    nb.esercizio(
        titolo="Ora e giorno della settimana",
        scenario="Vogliamo sapere in quale ora del giorno il carico medio della zona Nord è più alto e in quale giorno della settimana è più basso.",
        richiesta="""
            1. Aggiungi a `carico` le colonne `ora` e `giorno_settimana`, ricavate da `Date` con `.dt.hour` e `.dt.dayofweek`, in cui il lunedì vale 0.
            2. Calcola in `per_ora` il carico medio per ora con `groupby`, e metti in `ora_di_punta` l'ora con la media più alta.
            3. Calcola in `per_giorno` il carico medio per giorno della settimana, e metti in `giorno_minimo` il giorno con la media più bassa.
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
