"""E3 · Esercitazione 3: un'ora di lavoro sui notebook 07 e 08, con l'anno 2023 di una turbina eolica in Texas."""

from textwrap import dedent

from nbkit import Notebook

# Il codice dell'esercizio E3.1, già scritto in testa agli esercizi successivi: chi non ha finito il primo può proseguire.
PREPARA = """
    # la turbina con i nomi brevi e l'indice di date, come nell'esercizio E3.1
    turbina = pd.read_csv("../Dati/TexasTurbine.csv")
    turbina = turbina.rename(columns={
        "System power generated | (kW)": "potenza_kw",
        "Wind speed | (m/s)": "vento_ms",
        "Wind direction | (deg)": "direzione",
        "Pressure | (atm)": "pressione",
        "Air temperature | ('C)": "temperatura",
    })
    turbina["data"] = pd.to_datetime("2023 " + turbina["Time stamp"], format="%Y %b %d, %I:%M %p")
    turbina = turbina.set_index("data").sort_index()
"""


def unisci(*parti: str | None) -> str:
    """Toglie l'indentazione a ogni pezzo di codice e li separa con una riga vuota."""
    return "\n\n".join(dedent(p).strip("\n") for p in parti if p)


def consegna(passi: list[str], esito: str | None) -> str:
    """I passi numerati della consegna, seguiti dalla frase che descrive il risultato."""
    testo = "\n".join(f"{i}. {p}" for i, p in enumerate(passi, 1))
    return testo + (f"\n\n{esito}" if esito else "")


def esercizio(nb: Notebook, titolo: str, scenario: str, passi: list[str], esito: str | None,
              starter_base: str, starter_avanzata: str, soluzione: str, verifica_base: str,
              suggerimenti_base: list[str], passo_avanzata: str, soluzione_avanzata: str,
              verifica_avanzata: str, suggerimento_avanzata: str | None = None,
              esito_avanzata: str | None = None) -> None:
    """Lo stesso esercizio per le due aule: starter guidato e due suggerimenti in Base, starter quasi vuoto e un passo in più in Avanzata."""
    nb.esercizio(
        titolo=titolo, scenario=scenario, richiesta=consegna(passi, esito),
        starter=starter_base, soluzione=soluzione, verifica=verifica_base,
        suggerimenti=suggerimenti_base, aula="base",
    )
    esito_a = " ".join(e for e in (esito, esito_avanzata) if e) or None
    nb.esercizio(
        titolo=titolo, scenario=scenario, richiesta=consegna(passi + [passo_avanzata], esito_a),
        starter=starter_avanzata, soluzione=unisci(soluzione, soluzione_avanzata), verifica=verifica_avanzata,
        suggerimenti=[suggerimento_avanzata] if suggerimento_avanzata else None, aula="avanzata",
    )


def costruisci() -> Notebook:
    nb = Notebook(
        num="E3",
        file="Esercitazione_3",
        titolo="Esercitazione 3",
        blocco=3,
        giornata=2,
        intento="Questa esercitazione riprende i notebook 07 e 08 su un anno di dati orari di una turbina eolica in Texas: date, selezioni, resampling, groupby e merge.",
        obiettivi=[
            "convertire in date un testo senza anno e usarlo come indice",
            "selezionare periodi e ore e aggregare per mese, per giorno e per ora",
            "unire due tabelle sulla data e trattare i valori mancanti che ne risultano",
        ],
        tempo=60,
        dati=["TexasTurbine.csv"],
        soluzioni_a_richiesta=True,
    )

    # ------------------------------------------------------------------ apertura
    nb.md("""
        Questa esercitazione dura un'ora. Per i primi 45 minuti si lavora da soli sugli esercizi, e negli ultimi 15
        il docente mostra e commenta le soluzioni dei cinque esercizi del nucleo comune. Tutti gli esercizi usano lo
        stesso file, che registra ora per ora la produzione di una turbina eolica in Texas durante il 2023, e
        ciascuno rilegge il file da sé, in modo che chi si blocca su un esercizio possa passare al successivo.
    """)
    aiuti = """
        Nella consegna di ogni esercizio del nucleo {aiuti} e che conviene leggere solo
        dopo aver provato da soli. Sotto la cella da completare, la cella `verifica` controlla il risultato e, se
        qualcosa non torna, dice che cosa guardare, mentre la cella `soluzione` mostra la soluzione di quel solo
        esercizio. Chi finisce prima prosegue con i due esercizi facoltativi e con la sfida finale, che non ha una
        verifica.
    """
    nb.md(aiuti.replace("{aiuti}", "ci sono due suggerimenti nascosti, che si aprono con un clic"), aula="base")
    nb.md(aiuti.replace("{aiuti}", "c'è un suggerimento nascosto, che si apre con un clic"), aula="avanzata")

    # ------------------------------------------------------------------ domande
    nb.sezione("Domande", intro="""
        Le cinque domande che seguono riguardano i notebook 07 e 08. Per ciascuna conviene formulare la risposta a
        mente o provarla in una cella di codice, e solo dopo aprire la risposta per confrontarla.
    """)
    nb.domanda(
        "Su un DataFrame con indice `0, 1, 2, 3, ...`, quante righe restituiscono `df.loc[0:2]` e `df.iloc[0:2]`?",
        """
            `df.loc[0:2]` restituisce 3 righe, mentre `df.iloc[0:2]` ne restituisce 2. `loc` seleziona per etichetta e
            include l'etichetta finale dell'intervallo, invece `iloc` seleziona per posizione ed esclude la posizione
            finale, come lo slicing delle liste.
        """,
    )
    nb.domanda(
        "Che cosa restituisce `df.groupby(\"x\")[\"y\"].sum()`?",
        """
            Restituisce una Series che ha come indice i valori distinti della colonna `x` e come valori la somma di `y`
            per ciascuno di essi. Senza la funzione finale, `df.groupby("x")` restituirebbe soltanto un oggetto
            GroupBy, che descrive i gruppi ma non calcola nulla.
        """,
    )
    nb.domanda(
        "Che cosa fa `serie.resample(\"D\").mean()` su una serie con un valore ogni ora, e che cosa serve perché funzioni?",
        """
            Raccoglie in un gruppo le 24 misure di ogni giorno e ne calcola la media, quindi la serie oraria diventa una
            serie con un valore al giorno. Perché funzioni, la serie deve avere un indice di date, che si ottiene con
            `set_index` su una colonna già convertita con `pd.to_datetime`.
        """,
    )
    nb.domanda(
        "Di che cosa ha bisogno `pd.to_datetime` quando il testo di una data è ambiguo, come `\"01/02/2025\"`?",
        """
            Ha bisogno di sapere in che ordine sono scritti giorno e mese, perché la stessa stringa può essere il 1°
            febbraio o il 2 gennaio. Si indica con `dayfirst=True` oppure, in modo più preciso, descrivendo il formato
            con `format="%d/%m/%Y"`.
        """,
    )
    nb.domanda(
        "In un `pd.merge` con `how=\"left\"`, che cosa succede alle righe di sinistra la cui chiave non compare nella tabella di destra?",
        """
            Restano nel risultato, perché il left join conserva tutte le righe della tabella di sinistra, e nelle
            colonne che arrivano dalla tabella di destra ricevono `NaN`. Con il valore predefinito `how="inner"`,
            invece, quelle righe verrebbero scartate.
        """,
    )

    # ------------------------------------------------------------------ esercizi
    nb.sezione("Esercizi", intro="""
        Il file `TexasTurbine.csv` ha 8760 righe, una per ogni ora del 2023, senza valori mancanti e senza
        duplicati. Per ogni ora riporta la potenza prodotta dalla turbina in kW, la velocità e la direzione del
        vento, la pressione dell'aria e la sua temperatura. I primi cinque esercizi sono quelli che il docente
        corregge alla fine dell'ora. La cella qui sotto importa pandas e va eseguita prima di cominciare.
    """)
    nb.code("""
        import pandas as pd
    """)

    nb.md("""
        Nel file la colonna `Time stamp` contiene le date come testo, nella forma `Jan 1, 12:00 am`, con il nome
        abbreviato del mese in inglese, l'ora da 1 a 12 seguita da am o pm, e senza l'anno. Per convertirle conviene
        descrivere il formato con il parametro `format` di `pd.to_datetime`, indicando un codice per ogni parte:
        `%b` per il mese abbreviato, `%d` per il giorno, `%I` per l'ora nel formato a 12 ore, `%M` per i minuti e
        `%p` per am o pm. Poiché senza anno pandas userebbe il 1900, aggiungiamo `"2023 "` in testa alla stringa e
        `%Y` in testa al formato.
    """)

    esercizio(
        nb,
        titolo="Leggere e datare la turbina",
        scenario="""
            Prima di analizzare la produzione della turbina diamo alle colonne nomi brevi e trasformiamo il testo di
            `Time stamp` in un indice di date, in modo da poter selezionare e aggregare per periodo.
        """,
        passi=[
            "Rinomina le colonne con `rename`, usando i nomi brevi `potenza_kw`, `vento_ms`, `direzione`, `pressione` e `temperatura`.",
            "Crea la colonna `data` convertendo con `pd.to_datetime` la stringa `\"2023 \" + turbina[\"Time stamp\"]`, con il formato che descrive il testo.",
            "Imposta `data` come indice con `set_index` e ordina le righe con `sort_index`.",
            "Salva in `primo` e in `ultimo` il primo e l'ultimo timestamp dell'indice.",
        ],
        esito="Se la conversione è corretta, il primo timestamp è la mezzanotte del 1° gennaio 2023 e l'ultimo corrisponde alle 23:00 del 31 dicembre.",
        starter_base="""
            turbina = pd.read_csv("../Dati/TexasTurbine.csv")

            nomi = {
                "System power generated | (kW)": "potenza_kw",
                "Wind speed | (m/s)": ...,
                "Wind direction | (deg)": ...,
                "Pressure | (atm)": ...,
                "Air temperature | ('C)": ...,
            }
            turbina = turbina.rename(columns=nomi)
            turbina["data"] = pd.to_datetime("2023 " + turbina["Time stamp"], format=...)
            turbina = turbina.set_index(...).sort_index()

            primo = ...
            ultimo = ...
            print(primo, ultimo)
        """,
        starter_avanzata="""
            turbina = pd.read_csv("../Dati/TexasTurbine.csv")

            turbina = ...
            primo = ...
            ultimo = ...
            ordinato = ...
            passi = ...
        """,
        soluzione="""
            turbina = pd.read_csv("../Dati/TexasTurbine.csv")

            nomi = {
                "System power generated | (kW)": "potenza_kw",
                "Wind speed | (m/s)": "vento_ms",
                "Wind direction | (deg)": "direzione",
                "Pressure | (atm)": "pressione",
                "Air temperature | ('C)": "temperatura",
            }
            turbina = turbina.rename(columns=nomi)
            turbina["data"] = pd.to_datetime("2023 " + turbina["Time stamp"], format="%Y %b %d, %I:%M %p")
            turbina = turbina.set_index("data").sort_index()

            primo = turbina.index[0]
            ultimo = turbina.index[-1]
            print(primo, ultimo)
        """,
        verifica_base="""
            assert {"potenza_kw", "vento_ms", "direzione", "pressione", "temperatura"} <= set(turbina.columns), "❌ turbina: controlla i nomi nel dizionario nomi"
            assert primo == pd.Timestamp("2023-01-01 00:00"), "❌ primo: l'indice deve partire dalla mezzanotte del 1° gennaio 2023"
            assert ultimo == pd.Timestamp("2023-12-31 23:00"), "❌ ultimo: controlla %I e %p nel formato e l'ordinamento con sort_index()"
        """,
        suggerimenti_base=[
            """
                Ogni parte della stringa `2023 Jan 1, 12:00 am` ha il suo codice, e il formato deve ripetere anche gli
                spazi, la virgola e i due punti del testo. Il primo e l'ultimo elemento dell'indice si leggono come in
                una lista.
            """,
            """
                Il formato completo è `"%Y %b %d, %I:%M %p"`, l'indice si imposta con `set_index("data")`, e il primo
                timestamp è `turbina.index[0]`.
            """,
        ],
        passo_avanzata="Controlla l'indice salvando in `ordinato` il valore di `turbina.index.is_monotonic_increasing` e in `passi` il conteggio degli intervalli tra due timestamp consecutivi, calcolati con `diff()` come nel notebook 08.",
        esito_avanzata="Il conteggio `passi` ha un solo valore, un'ora, che compare 8759 volte.",
        soluzione_avanzata="""
            ordinato = turbina.index.is_monotonic_increasing
            passi = turbina.index.to_series().diff().value_counts()
            print(ordinato)
            passi
        """,
        verifica_avanzata="""
            assert {"potenza_kw", "vento_ms", "direzione", "pressione", "temperatura"} <= set(turbina.columns), "❌ turbina: controlla i nomi passati a rename"
            assert primo == pd.Timestamp("2023-01-01 00:00") and ultimo == pd.Timestamp("2023-12-31 23:00"), "❌ primo, ultimo: controlla il formato e l'ordinamento dell'indice"
            assert ordinato and len(passi) == 1 and passi.iloc[0] == 8759, "❌ passi: tutti gli 8759 intervalli devono valere un'ora"
        """,
        suggerimento_avanzata="""
            Il formato è `"%Y %b %d, %I:%M %p"`. Gli intervalli si calcolano sull'indice trasformato in Series, con
            `turbina.index.to_series().diff()`, e si contano con `value_counts()`.
        """,
    )

    esercizio(
        nb,
        titolo="Selezionare ore e periodi",
        scenario="""
            Con l'indice di date un periodo si seleziona scrivendone solo una parte, mentre le ore che rispettano una
            condizione si selezionano con una maschera booleana. Vogliamo sapere quante ore conta luglio, in quante
            ore il vento ha superato i 12 m/s e in quante la turbina non ha prodotto nulla.
        """,
        passi=[
            "Seleziona in `luglio` le righe di luglio 2023 con `loc` e salva in `ore_luglio` il loro numero.",
            "Salva in `ventose` le ore in cui `vento_ms` è maggiore di 12, usando una maschera booleana, e in `n_ventose` il loro numero.",
            "Salva in `ore_ferme` il numero di ore in cui `potenza_kw` vale 0.",
        ],
        esito="Luglio ha 31 giorni, quindi `ore_luglio` vale 744.",
        starter_base=unisci(PREPARA, """
            luglio = turbina.loc[...]
            ore_luglio = ...

            ventose = turbina[...]
            n_ventose = ...

            ore_ferme = ...
            print(ore_luglio, n_ventose, ore_ferme)
        """),
        starter_avanzata=unisci(PREPARA, """
            luglio = ...
            ore_luglio = ...
            ventose = ...
            n_ventose = ...
            ore_ferme = ...
            ventose_query = ...
        """),
        soluzione=unisci(PREPARA, """
            luglio = turbina.loc["2023-07"]
            ore_luglio = len(luglio)

            ventose = turbina[turbina["vento_ms"] > 12]
            n_ventose = len(ventose)

            ore_ferme = (turbina["potenza_kw"] == 0).sum()
            print(ore_luglio, n_ventose, ore_ferme)
        """),
        verifica_base="""
            assert ore_luglio == 744, "❌ ore_luglio: seleziona il mese con turbina.loc[\\"2023-07\\"] e contalo con len()"
            assert n_ventose == 645, "❌ n_ventose: la condizione è vento_ms > 12, estremo escluso"
            assert ore_ferme == 822, "❌ ore_ferme: somma la maschera potenza_kw == 0"
        """,
        suggerimenti_base=[
            """
                Con un indice di date, `loc` accetta una data scritta solo in parte, come l'anno e il mese. Il numero
                di righe di un DataFrame si ottiene con `len()`, mentre la somma di una maschera conta i suoi `True`.
            """,
            """
                Il mese si seleziona con `turbina.loc["2023-07"]`; la maschera del vento è `turbina["vento_ms"] > 12`
                e va messa dentro `turbina[...]`, mentre per le ore ferme basta `(turbina["potenza_kw"] == 0).sum()`.
            """,
        ],
        passo_avanzata="Ripeti il filtro del vento con `.query()`, salvando il risultato in `ventose_query`, e controlla che abbia lo stesso numero di righe di `ventose`.",
        soluzione_avanzata="""
            ventose_query = turbina.query("vento_ms > 12")
            len(ventose_query) == n_ventose
        """,
        verifica_avanzata="""
            assert ore_luglio == 744, "❌ ore_luglio: seleziona il mese con loc e una data parziale"
            assert n_ventose == 645 and ore_ferme == 822, "❌ n_ventose, ore_ferme: controlla le due maschere"
            assert len(ventose_query) == 645, "❌ ventose_query: dentro query il nome della colonna va senza virgolette"
        """,
        suggerimento_avanzata="""
            Dentro la stringa di `query` il nome della colonna si scrive senza virgolette, come in `"vento_ms > 12"`.
        """,
    )

    nb.md("""
        Il metodo `resample` è un `groupby` guidato dal tempo, perché raccoglie in un gruppo tutte le righe dello
        stesso periodo e lascia alla funzione che segue, come `sum()` o `mean()`, il compito di combinarle. Con
        l'alias `ME` il periodo è il mese, e ogni gruppo prende come etichetta l'ultimo giorno del mese. La turbina
        registra la potenza media di ogni ora in kW, e un'ora a 1000 kW produce 1000 kWh, quindi la somma dei valori
        orari di un mese è l'energia del mese in kWh. L'etichetta del valore più alto si ottiene con `idxmax()`, e
        quella del più basso con `idxmin()`.
    """)

    esercizio(
        nb,
        titolo="L'energia per mese",
        scenario="""
            Il gestore della turbina vuole sapere quanta energia è stata prodotta in ciascun mese del 2023 e quali
            sono stati il mese migliore e il peggiore.
        """,
        passi=[
            "Calcola in `mensile` l'energia di ogni mese in kWh, sommando `potenza_kw` con `resample(\"ME\")`.",
            "Salva in `mese_migliore` l'etichetta del mese con l'energia più alta e in `mese_peggiore` quella del mese con l'energia più bassa.",
        ],
        esito="Il risultato `mensile` è una Series con 12 valori, e ogni etichetta è l'ultimo giorno di un mese.",
        starter_base=unisci(PREPARA, """
            mensile = turbina["potenza_kw"].resample(...).sum()
            mese_migliore = ...
            mese_peggiore = ...
            print(mese_migliore, mese_peggiore)
            mensile
        """),
        starter_avanzata=unisci(PREPARA, """
            mensile = ...
            mese_migliore = ...
            mese_peggiore = ...
            mensile_vento = ...
        """),
        soluzione=unisci(PREPARA, """
            mensile = turbina["potenza_kw"].resample("ME").sum()
            mese_migliore = mensile.idxmax()
            mese_peggiore = mensile.idxmin()
            print(mese_migliore, mese_peggiore)
            mensile
        """),
        verifica_base="""
            assert len(mensile) == 12, "❌ mensile: resample(\\"ME\\") produce un valore per ogni mese"
            assert mese_migliore == pd.Timestamp("2023-04-30"), "❌ mese_migliore: usa idxmax() su mensile, che restituisce l'etichetta"
            assert mese_peggiore == pd.Timestamp("2023-09-30"), "❌ mese_peggiore: usa idxmin() su mensile"
        """,
        suggerimenti_base=[
            """
                Conviene selezionare prima la colonna `potenza_kw`, poi raggruppare per mese e sommare. Il mese
                migliore è l'etichetta del valore più alto, non il valore stesso.
            """,
            """
                La prima riga è `turbina["potenza_kw"].resample("ME").sum()`, e le etichette del massimo e del minimo
                si ottengono con `mensile.idxmax()` e `mensile.idxmin()`.
            """,
        ],
        passo_avanzata="Calcola in `mensile_vento`, con un solo `resample(\"ME\")` seguito da `agg`, un DataFrame con la somma di `potenza_kw` e la media di `vento_ms` per ogni mese.",
        esito_avanzata="Con `mensile_vento` si vede se il mese più produttivo è anche il più ventoso.",
        soluzione_avanzata="""
            mensile_vento = turbina.resample("ME").agg({"potenza_kw": "sum", "vento_ms": "mean"})
            mensile_vento
        """,
        verifica_avanzata="""
            assert len(mensile) == 12, "❌ mensile: resample(\\"ME\\") produce un valore per ogni mese"
            assert mese_migliore == pd.Timestamp("2023-04-30") and mese_peggiore == pd.Timestamp("2023-09-30"), "❌ mese_migliore, mese_peggiore: usa idxmax() e idxmin()"
            assert round(mensile_vento.loc["2023-04-30", "vento_ms"], 1) == 8.5, "❌ mensile_vento: la colonna vento_ms è la media del mese"
        """,
        suggerimento_avanzata="""
            A `agg` si passa un dizionario che associa a ogni colonna la sua funzione, come
            `{"potenza_kw": "sum", "vento_ms": "mean"}`.
        """,
    )

    nb.md("""
        Nel notebook 08 abbiamo raggruppato per ora dopo aver aggiunto al DataFrame una colonna con l'ora di ogni
        riga. Con un indice di date si può fare a meno di quella colonna, perché `groupby` accetta, al posto del nome
        di una colonna, una sequenza di valori lunga quanto il DataFrame, come `turbina.index.hour`. Il risultato ha
        come indice le ore del giorno, da 0 a 23.
    """)

    esercizio(
        nb,
        titolo="Il profilo orario",
        scenario="""
            La produzione di una turbina segue il vento, che a sua volta cambia con l'ora del giorno. Vogliamo
            calcolare la potenza media della turbina in ciascuna delle 24 ore e trovare l'ora in cui rende di più.
        """,
        passi=[
            "Calcola in `profilo` la potenza media per ora del giorno, raggruppando `potenza_kw` per `turbina.index.hour`.",
            "Salva in `ora_migliore` l'ora con la potenza media più alta.",
        ],
        esito="Il risultato `profilo` è una Series con 24 valori, uno per ogni ora da 0 a 23.",
        starter_base=unisci(PREPARA, """
            profilo = turbina.groupby(...)["potenza_kw"].mean()
            ora_migliore = ...
            print(ora_migliore)
            profilo
        """),
        starter_avanzata=unisci(PREPARA, """
            profilo = ...
            ora_migliore = ...
            profilo_stat = ...
        """),
        soluzione=unisci(PREPARA, """
            profilo = turbina.groupby(turbina.index.hour)["potenza_kw"].mean()
            ora_migliore = profilo.idxmax()
            print(ora_migliore)
            profilo
        """),
        verifica_base="""
            assert len(profilo) == 24, "❌ profilo: raggruppa per turbina.index.hour, che ha 24 valori distinti"
            assert ora_migliore == 16, "❌ ora_migliore: usa idxmax() su profilo"
            assert round(profilo.max(), 1) == 1294.1, "❌ profilo: calcola la media di potenza_kw, non la somma"
        """,
        suggerimenti_base=[
            """
                Dentro le parentesi di `groupby` va l'ora di ogni riga, che si legge dall'indice; dopo il
                raggruppamento si sceglie la colonna e si calcola la media.
            """,
            """
                La forma è `turbina.groupby(turbina.index.hour)["potenza_kw"].mean()`, e l'ora migliore è l'etichetta
                del massimo, `profilo.idxmax()`.
            """,
        ],
        passo_avanzata="Calcola in `profilo_stat`, con `agg`, la media e il massimo della potenza per ogni ora, in un DataFrame con le colonne `mean` e `max`.",
        soluzione_avanzata="""
            profilo_stat = turbina.groupby(turbina.index.hour)["potenza_kw"].agg(["mean", "max"])
            profilo_stat
        """,
        verifica_avanzata="""
            assert len(profilo) == 24 and ora_migliore == 16, "❌ profilo, ora_migliore: raggruppa per turbina.index.hour e usa idxmax()"
            assert list(profilo_stat.columns) == ["mean", "max"], "❌ profilo_stat: passa ad agg la lista [\\"mean\\", \\"max\\"]"
            assert round(profilo_stat["max"].max(), 1) == 3004.0, "❌ profilo_stat: la colonna max è la potenza massima di ogni ora"
        """,
        suggerimento_avanzata="""
            Dopo aver scelto la colonna, a `agg` si può passare anche una lista di nomi di funzioni, come
            `["mean", "max"]`, e ogni funzione diventa una colonna del risultato.
        """,
    )

    nb.md("""
        Due tabelle che descrivono gli stessi giorni si uniscono con `pd.merge`, indicando con `on` la colonna che fa
        da chiave, in questo caso la data. Con `how="left"` il risultato conserva tutte le righe della tabella di
        sinistra, e le colonne che arrivano da destra valgono `NaN` nelle righe la cui data non compare nell'altra
        tabella. Questi valori mancanti si contano con `isnull().sum()` e si sostituiscono con `fillna()`. Perché le
        chiavi corrispondano, le due colonne devono avere lo stesso tipo, per cui le date della seconda tabella
        vanno create con `pd.to_datetime` e non lasciate come testo.
    """)

    manutenzioni = """
        manutenzioni = pd.DataFrame({
            "data": pd.to_datetime(["2023-03-15", "2023-06-14", "2023-11-08", "2023-12-15"]),
            "motivo": ["ispezione delle pale", "sostituzione di un sensore", "controllo del generatore", "riparazione del freno"],
        })
    """
    esercizio(
        nb,
        titolo="I giorni di manutenzione",
        scenario="""
            Il registro delle manutenzioni, inventato per questo esercizio, elenca quattro giorni del 2023 in cui un
            tecnico è intervenuto sulla turbina. Vogliamo affiancare il motivo dell'intervento alla produzione di
            ogni giorno, con la scritta `nessuna` nei giorni senza intervento.
        """,
        passi=[
            "Calcola in `giornaliera` l'energia di ogni giorno con `resample(\"D\")` e `sum()`, e applica `reset_index()` in modo che la data diventi la colonna `data`.",
            "Unisci `giornaliera` e `manutenzioni` sulla colonna `data` con un left join e salva il risultato in `unione`.",
            "Salva in `senza_intervento` il numero di valori mancanti della colonna `motivo` di `unione`.",
            "Sostituisci i valori mancanti di `motivo` con il testo `\"nessuna\"`.",
        ],
        esito="Il risultato `unione` ha una riga per ogni giorno dell'anno, 365 in tutto, e soltanto quattro righe hanno un motivo diverso da `nessuna`.",
        starter_base=unisci(PREPARA, manutenzioni, """
            giornaliera = turbina["potenza_kw"].resample(...).sum().reset_index()
            unione = pd.merge(..., ..., on=..., how=...)
            senza_intervento = ...
            unione["motivo"] = ...

            print(senza_intervento)
            unione[unione["motivo"] != "nessuna"]
        """),
        starter_avanzata=unisci(PREPARA, manutenzioni, """
            giornaliera = ...
            unione = ...
            senza_intervento = ...
            unione["motivo"] = ...
            solo_interventi = ...
        """),
        soluzione=unisci(PREPARA, manutenzioni, """
            giornaliera = turbina["potenza_kw"].resample("D").sum().reset_index()
            unione = pd.merge(giornaliera, manutenzioni, on="data", how="left")
            senza_intervento = unione["motivo"].isnull().sum()
            unione["motivo"] = unione["motivo"].fillna("nessuna")

            print(senza_intervento)
            unione[unione["motivo"] != "nessuna"]
        """),
        verifica_base="""
            assert len(unione) == 365, "❌ unione: con how=\\"left\\" e giornaliera a sinistra restano tutti i 365 giorni"
            assert senza_intervento == 361, "❌ senza_intervento: conta i NaN di motivo prima di riempirli"
            assert (unione["motivo"] == "nessuna").sum() == 361, "❌ motivo: riempi i NaN con fillna(\\"nessuna\\") e riassegna la colonna"
        """,
        suggerimenti_base=[
            """
                Il left join conserva tutte le righe della tabella che si passa per prima, quindi `giornaliera` va a
                sinistra. I valori mancanti di una colonna si contano con lo stesso metodo usato nel notebook 07.
            """,
            """
                L'unione si scrive `pd.merge(giornaliera, manutenzioni, on="data", how="left")`, il conteggio
                `unione["motivo"].isnull().sum()` e la sostituzione `unione["motivo"].fillna("nessuna")`, da
                riassegnare alla colonna.
            """,
        ],
        passo_avanzata="Ripeti l'unione con `how=\"inner\"`, salvando il risultato in `solo_interventi`, e confronta il suo numero di righe con quello di `unione`.",
        soluzione_avanzata="""
            solo_interventi = pd.merge(giornaliera, manutenzioni, on="data", how="inner")
            print(len(unione), len(solo_interventi))
            solo_interventi
        """,
        verifica_avanzata="""
            assert len(unione) == 365 and senza_intervento == 361, "❌ unione, senza_intervento: left join con giornaliera a sinistra, poi isnull().sum()"
            assert (unione["motivo"] == "nessuna").sum() == 361, "❌ motivo: riempi i NaN con fillna(\\"nessuna\\") e riassegna la colonna"
            assert len(solo_interventi) == 4, "❌ solo_interventi: con how=\\"inner\\" restano i quattro giorni presenti in entrambe le tabelle"
        """,
        suggerimento_avanzata="""
            Il conteggio dei `NaN` va fatto prima di `fillna`, perché dopo la sostituzione non ce ne sono più.
        """,
    )

    # ------------------------------------------------------------------ facoltativi
    nb.md("""
        Gli esercizi che seguono sono facoltativi e servono a chi ha finito i primi cinque prima dei 45 minuti. I
        primi due applicano ancora `groupby` e il salvataggio dei file, mentre la sfida finale è un esercizio libero,
        senza verifica, che riassume l'anno della turbina in tre righe. La correzione dell'ultimo quarto d'ora non li
        comprende, ma anche sotto questi esercizi c'è la cella `soluzione`.
    """)
    nb.esercizio(
        titolo="Il profilo settimanale",
        facoltativo=True,
        scenario="""
            Il carico elettrico cambia molto tra i giorni feriali e il fine settimana, mentre la produzione di una
            turbina dipende dal vento e non dal calendario. Vogliamo vedere come si distribuisce la potenza media sui
            sette giorni della settimana del 2023.
        """,
        richiesta=consegna([
            "Calcola in `settimanale` la potenza media per giorno della settimana, raggruppando `potenza_kw` per `turbina.index.dayofweek`, in cui il lunedì vale 0.",
            "Usando la lista `giorni`, già scritta nella cella, salva in `giorno_migliore` il nome del giorno con la media più alta.",
        ], "Il risultato `settimanale` ha sette valori, e `giorno_migliore` è una stringa come `\"martedì\"`."),
        suggerimenti=["""
            L'indice di `settimanale` va da 0 a 6, come le posizioni della lista `giorni`, quindi l'etichetta
            restituita da `settimanale.idxmax()` si può usare direttamente come posizione nella lista.
        """],
        starter=unisci(PREPARA, """
            giorni = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]

            settimanale = ...
            giorno_migliore = ...
            print(giorno_migliore)
        """),
        soluzione=unisci(PREPARA, """
            giorni = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]

            settimanale = turbina.groupby(turbina.index.dayofweek)["potenza_kw"].mean()
            giorno_migliore = giorni[settimanale.idxmax()]
            print(giorno_migliore)
        """),
        verifica="""
            assert len(settimanale) == 7, "❌ settimanale: raggruppa per turbina.index.dayofweek"
            assert giorno_migliore == "lunedì", "❌ giorno_migliore: usa settimanale.idxmax() come posizione in giorni"
        """,
    )

    nb.md("""
        Il metodo `to_csv()` scrive un DataFrame o una Series in un file CSV, nello stesso modo in cui `to_excel()`,
        visto nel notebook 06, lo scrive in un file Excel. Se si indica soltanto il nome del file, questo viene
        creato nella cartella del notebook, e l'indice viene scritto come prima colonna. Rileggendo il CSV con
        `read_csv` le date tornano testo, a meno di indicare con `parse_dates` le colonne da convertire.
    """)

    nb.esercizio(
        titolo="Le tabelle per il collega",
        facoltativo=True,
        scenario="""
            Un collega che lavora con Excel ci chiede l'energia mensile della turbina, e gliela mandiamo sia in CSV
            sia in Excel. Prima di inviare i file conviene riaprirne uno e controllare che contenga tutti i mesi.
        """,
        richiesta=consegna([
            "Salva `mensile` nel file `energia_mensile.csv` con `to_csv()` e nel file `energia_mensile.xlsx` con `to_excel()`.",
            "Rileggi il CSV con `pd.read_csv` in `riletto`, convertendo in date la colonna `data` con `parse_dates=[\"data\"]`.",
            "Salva in `stesse_righe` il risultato del confronto tra il numero di righe di `riletto` e quello di `mensile`.",
        ], "Il file CSV ha due colonne, `data` e `potenza_kw`, perché `to_csv()` scrive anche l'indice."),
        suggerimenti=["""
            Il confronto tra le lunghezze si scrive `len(riletto) == len(mensile)` e vale `True` se il file contiene
            tutti i 12 mesi.
        """],
        starter=unisci(PREPARA, """
            mensile = turbina["potenza_kw"].resample("ME").sum()

            ...
            ...
            riletto = ...
            stesse_righe = ...
            print(stesse_righe)
            riletto.head()
        """),
        soluzione=unisci(PREPARA, """
            mensile = turbina["potenza_kw"].resample("ME").sum()

            mensile.to_csv("energia_mensile.csv")
            mensile.to_excel("energia_mensile.xlsx")
            riletto = pd.read_csv("energia_mensile.csv", parse_dates=["data"])
            stesse_righe = len(riletto) == len(mensile)
            print(stesse_righe)
            riletto.head()
        """),
        verifica="""
            from pathlib import Path
            assert Path("energia_mensile.csv").exists() and Path("energia_mensile.xlsx").exists(), "❌ i due file non sono nella cartella del notebook"
            assert len(riletto) == 12 and stesse_righe, "❌ riletto: il CSV deve avere 12 righe, una per mese"
            assert str(riletto["data"].dtype).startswith("datetime64"), "❌ riletto: aggiungi parse_dates=[\\"data\\"] a read_csv"
        """,
    )

    nb.esercizio(
        titolo="Sfida: il riepilogo dell'anno",
        facoltativo=True,
        scenario="""
            Per chiudere vogliamo un riepilogo dell'anno in tre righe, da incollare in una mail. Questo esercizio non
            ha una verifica, perché il formato delle righe è libero, e la soluzione ne mostra un esempio.
        """,
        richiesta="""
            Stampa tre righe con l'energia totale prodotta nel 2023 in MWh, il mese con l'energia più alta e l'ora del
            giorno con la potenza media più alta.
        """,
        starter=unisci(PREPARA, """
            # il riepilogo dell'anno, in tre righe
            ...
        """),
        soluzione=unisci(PREPARA, """
            mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
                    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]

            energia_mwh = turbina["potenza_kw"].sum() / 1000
            mensile = turbina["potenza_kw"].resample("ME").sum()
            mese_migliore = mesi[mensile.idxmax().month - 1]
            ora_migliore = turbina.groupby(turbina.index.hour)["potenza_kw"].mean().idxmax()

            print(f"Energia prodotta nel 2023: {energia_mwh:.0f} MWh")   # Output: Energia prodotta nel 2023: 8449 MWh
            print(f"Mese con più energia: {mese_migliore}")             # Output: Mese con più energia: aprile
            print(f"Ora con la potenza media più alta: le {ora_migliore}")  # Output: Ora con la potenza media più alta: le 16
        """),
    )

    return nb
