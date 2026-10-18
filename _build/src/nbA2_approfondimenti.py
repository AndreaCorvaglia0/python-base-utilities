"""A2 · Approfondimenti 2: date (differenze e fuso orario) e, per l'Avanzata, shift, rolling e il codice degli agenti."""

from nbkit import Notebook

DOC = "https://pandas.pydata.org/pandas-docs/stable"


def costruisci() -> Notebook:
    nb = Notebook(
        num="A2",
        file="Approfondimenti_2",
        titolo="Approfondimenti 2",
        blocco={"base": 3, "avanzata": 4},     # Base: solo le date (modulo 3); Avanzata: anche il codice degli agenti (modulo 4)
        giornata=4,
        fuori_programma=True,
        intento="Raccoglie gli argomenti sulle date che restano fuori dal notebook 08 e, nella versione Avanzata, `shift`, `rolling` e i costrutti che si incontrano nel codice scritto da un agente; si affronta in classe se si è in anticipo sul programma, oppure a casa.",
        obiettivi={
            "base": [
                "misurare la distanza tra due date e la durata di una serie con `Timedelta`",
                "dare un fuso orario a date che non ne hanno con `tz_localize`",
                "convertire le date in un altro fuso con `tz_convert` e selezionare un intervallo su un indice con fuso",
            ],
            "avanzata": [
                "misurare durate con `Timedelta` e gestire il fuso orario con `tz_localize` e `tz_convert`",
                "costruire lag e medie mobili con `shift` e `rolling`",
                "riconoscere type hint, `@dataclass`, decoratori, generatori e `**kwargs`",
            ],
        },
        tempo={"base": 20, "avanzata": 40},
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

    # ------------------------------------------------------------------ 4 (A)
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
        Questa sezione usa `carico`, il carico Terna della zona Nord nel 2024, ordinato per data e senza i
        duplicati dovuti al ritorno all'ora solare, come nel notebook 08. La cella seguente lo ricostruisce.
    """)
    nb.code("""
        carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico = carico.sort_values("Date")
        carico = carico.drop_duplicates(subset="Date")
        carico.head(3)
    """)
    nb.esercizio(
        titolo="L'ora che manca a marzo",
        scenario="""
            Nel notebook 08 abbiamo visto che a ottobre, quando si torna all'ora solare, nel carico compaiono
            quattro quarti d'ora ripetuti. A marzo succede il contrario, perché con il passaggio all'ora legale
            un'ora non esiste e nei dati mancano quattro quarti d'ora. Vogliamo trovare
            il punto della serie in cui due righe consecutive distano più di 15 minuti: con `diff()` sulla colonna
            `Date` e una maschera il risultato è una riga sola, quella delle 3:00 del 31 marzo 2024, che arriva
            un'ora e un quarto dopo la precedente.
        """,
        richiesta="""
            1. Calcola in `distanze` la differenza tra ogni valore di `carico["Date"]` e il precedente, con `diff()`.
            2. Tieni in `salti` le righe di `carico` in cui `distanze` è maggiore di 15 minuti.
        """,
        suggerimento="una durata fissa si scrive con `pd.Timedelta(\"15min\")` e si confronta con `>` come un numero, quindi `distanze > pd.Timedelta(\"15min\")` è una maschera che si usa tra parentesi quadre su `carico`.",
        starter="""
            distanze = ...
            salti = ...

            salti
        """,
        soluzione="""
            distanze = carico["Date"].diff()
            salti = carico[distanze > pd.Timedelta("15min")]

            salti
        """,
        verifica="""
            assert len(salti) == 1, "❌ salti: deve restare una riga sola, quella con distanze > pd.Timedelta('15min')"
            assert salti["Date"].iloc[0] == pd.Timestamp("2024-03-31 03:00"), "❌ salti: la riga attesa è quella delle 3:00 del 31 marzo"
        """,
    )
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="La media mobile su 24 ore",
            scenario="""
                Il carico quartorario oscilla molto tra il giorno e la notte, e queste oscillazioni nascondono
                l'andamento nel corso dell'anno. Vogliamo una media mobile su 24 ore, cioè su 96 quarti d'ora
                consecutivi, che copre sempre un giorno intero e quindi elimina il ciclo giornaliero, e il momento
                in cui raggiunge il valore più alto. Con `rolling` pandas la calcola su tutto l'anno in una riga,
                e il massimo, circa 27.189 MW, cade il 19 luglio 2024 alle 15:30.
            """,
            richiesta="""
                1. Calcola in `media_24h` la media mobile su 96 valori di `Total Load [MW]`, con `Date` come indice.
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
            suggerimento="come `power_ma_8` nella sezione su `rolling`, la media mobile si ottiene con `rolling` seguito da `mean()`, e `idxmax()` restituisce l'etichetta del valore più alto, che qui è un timestamp.",
            facoltativo=True,
        )

    return nb
