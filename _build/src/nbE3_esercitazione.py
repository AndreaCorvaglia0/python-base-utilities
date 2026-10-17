"""E3 · Esercitazione 3: un'ora di domande ed esercizi sui notebook 07-08, sugli esercizi originali del docente."""

from textwrap import dedent

from nbkit import Notebook


def unisci(*parti: str) -> str:
    """Toglie l'indentazione a ogni pezzo di codice e li unisce con una riga vuota."""
    return "\n\n".join(dedent(p).strip("\n") for p in parti)


def esercizio_due_aule(nb: Notebook, titolo: str, scenario: str, base: dict, avanzata: dict,
                       facoltativo: bool = False) -> None:
    """Lo stesso esercizio per le due aule: titolo e scenario in comune, il resto può cambiare.

    `base` e `avanzata` contengono richiesta, starter, soluzione, verifica e suggerimenti; le chiavi che mancano
    in `avanzata` si prendono da `base`.
    """
    nb.esercizio(titolo=titolo, scenario=scenario, facoltativo=facoltativo, aula="base", **base)
    nb.esercizio(titolo=titolo, scenario=scenario, facoltativo=facoltativo, aula="avanzata", **{**base, **avanzata})


# Le righe che ricostruiscono la serie dell'esercizio E3.5 con i buchi riempiti, come nel notebook 08: aprono gli
# starter dell'esercizio E3.6 e della sfida, che così si possono fare anche senza aver risolto E3.5.
PREPARA_SERIE = """
    # la serie dell'esercizio E3.5, con i buchi riempiti dall'interpolazione come nel notebook 08
    df["timestamp"] = pd.to_datetime(df["timestamp_str"], format="%d/%m/%Y %H:%M")
    df_serie = df[["timestamp", "power_kw", "temp_c"]].set_index("timestamp").sort_index()
    df_15min = df_serie.asfreq("15min").interpolate(method="linear")
"""


def costruisci() -> Notebook:
    nb = Notebook(
        num="E3",
        file="Esercitazione_3",
        titolo="Esercitazione 3",
        blocco=3,
        giornata=3,
        intento="Un'ora di domande ed esercizi sui notebook 07 e 08: maschere, groupby, ordinamento e date.",
        obiettivi=[
            "selezionare righe con una maschera booleana e sommare per gruppo con `groupby`",
            "ordinare un risultato con `sort_values` e trovarne il valore più alto con `idxmax`",
            "convertire un testo in date, usarlo come indice e cambiare la frequenza con `resample`",
        ],
        tempo=60,
        dati=[],
        soluzioni_a_richiesta=True,
    )

    # ------------------------------------------------------------------ come funziona l'ora
    nb.md("""
        Questa esercitazione chiude il modulo su pandas e riprende quello che abbiamo visto nei notebook 07 e 08.
        Hai 45 minuti per lavorare sugli esercizi, poi li guardiamo insieme. Si comincia con quattro domande di
        riepilogo e si prosegue con sei esercizi, da fare nell'ordine perché la difficoltà cresce; in fondo c'è una
        sfida libera, senza verifica, per il tempo che resta.
    """)
    aiuti = """
        Ogni esercizio comincia dicendo che cosa vogliamo ottenere e perché, e da lì si può arrivare al risultato da
        soli. Chi preferisce procedere per gradi apre con un clic il blocco Passo per passo, e sotto {aiuti}, da
        leggere solo dopo aver provato. Sotto la cella da completare ci sono la verifica, che conferma il risultato o
        dice che cosa controllare, e la cella `soluzione`, che mostra soltanto la soluzione di quell'esercizio.
    """
    nb.md(aiuti.replace("{aiuti}", "due suggerimenti, anche loro nascosti"), aula="base")
    nb.md(aiuti.replace("{aiuti}", "un suggerimento, anche lui nascosto"), aula="avanzata")

    # ------------------------------------------------------------------ 1. Domande
    nb.sezione("Domande", intro="""
        Le quattro domande che seguono riguardano i notebook 07 e 08 e richiedono pochi minuti. Per ciascuna
        conviene prevedere la risposta a mente e solo dopo aprirla con un clic. In caso di dubbio si può provare la
        riga in una cella di codice e, se il risultato sorprende, rileggere la parte del notebook che tratta
        quell'argomento.
    """)
    nb.domanda(
        "Con `numeri = pd.Series([4, 9, 2, 7])`, che cosa restituisce `numeri > 5`, e che cosa restituisce `numeri[numeri > 5]`?",
        """
            `numeri > 5` restituisce una maschera booleana, cioè una Series della stessa lunghezza con `False`,
            `True`, `False`, `True`, un valore per ogni elemento. Messa tra quadre, la maschera tiene soltanto gli
            elementi in cui vale `True`, quindi `numeri[numeri > 5]` contiene 9 e 7, con le etichette 1 e 3.
        """,
    )
    nb.domanda(
        "Su un DataFrame `vendite` con le colonne `Categoria` e `Vendite`, che cosa restituisce `vendite.groupby(\"Categoria\")[\"Vendite\"].sum()`?",
        """
            Restituisce una Series con una riga per ogni categoria distinta: l'indice contiene le categorie e i valori
            sono la somma delle vendite di ciascuna. Senza la funzione finale, `groupby` restituirebbe soltanto un
            oggetto GroupBy, che descrive i gruppi ma non calcola nulla.
        """,
    )
    nb.domanda(
        "Che cosa fa `pd.to_datetime` su una colonna di testo con valori come `\"01/03/2025 08:15\"`, e perché serve?",
        """
            Converte il testo in valori di tipo `datetime64`, in questo caso il 1° marzo 2025 alle 8:15. Finché la
            colonna resta testo pandas non sa che rappresenta degli istanti, mentre dopo la conversione la può
            ordinare nel tempo, usare come indice per selezionare un periodo e scomporre in ora, giorno e mese.
        """,
    )
    nb.domanda(
        "Su una serie con un valore ogni quarto d'ora per tre giorni e un indice di date, che cosa restituisce `serie.resample(\"D\").mean()`?",
        """
            Restituisce una serie con tre valori, uno per giorno, ciascuno uguale alla media delle misure di quel
            giorno. Ogni valore ha come etichetta la mezzanotte del giorno a cui si riferisce, e senza un indice di
            date `resample` non funzionerebbe.
        """,
    )

    # ------------------------------------------------------------------ 2. Esercizi
    nb.sezione("Esercizi", intro="""
        I primi quattro esercizi ripercorrono le selezioni, i raggruppamenti e l'ordinamento del notebook 07 sul
        DataFrame `ascolti`, che una piattaforma di streaming musicale usa per registrare quante volte ogni utente
        ha ascoltato una canzone. Gli ultimi due lavorano sulle misure quartorarie del notebook 08. La cella qui
        sotto importa pandas e crea `ascolti`, e va eseguita prima di cominciare; gli esercizi partono tutti dagli
        stessi dati, quindi si possono affrontare anche senza aver risolto i precedenti.
    """)
    nb.code("""
        import pandas as pd

        # DataFrame degli ascolti
        dati_ascolti = {
            "UserID": [101, 102, 103, 104, 105, 106],
            "Song": ["Song A", "Song B", "Song A", "Song C", "Song B", "Song D"],
            "Artist": ["Artist X", "Artist Y", "Artist X", "Artist Z", "Artist Y", "Artist W"],
            "Plays": [15, 2, 4, 1, 5, 2],
        }
        ascolti = pd.DataFrame(dati_ascolti)
        ascolti
    """)

    # E3.1 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Gli ascolti di un utente",
        scenario="""
            L'utente con `UserID` 103 vuole sapere quali canzoni risultano nella sua cronologia e quante volte le ha
            ascoltate. Vogliamo quindi tutte le righe di `ascolti` che lo riguardano, e con una maschera booleana
            pandas le trova allo stesso modo in una tabella di sei righe o di sei milioni. Il risultato è una sola
            riga, con `Song A` di `Artist X` e 4 ascolti.
        """,
        base=dict(
            richiesta="""
                1. Costruisci in `cond` la maschera delle righe in cui `UserID` vale 103.
                2. Salva in `ascolti_103` le righe di `ascolti` in cui la maschera vale `True` e mostrale.
            """,
            suggerimenti=[
                """
                    Una maschera booleana nasce dal confronto tra una colonna e un valore, e messa tra quadre dopo il
                    DataFrame tiene soltanto le righe in cui vale `True`.
                """,
                """
                    Il confronto è `ascolti["UserID"] == 103`, con il doppio uguale, e la selezione è
                    `ascolti[cond]`.
                """,
            ],
            starter="""
                cond = ...
                ascolti_103 = ascolti[...]
                ascolti_103
            """,
            soluzione="""
                cond = ascolti["UserID"] == 103
                ascolti_103 = ascolti[cond]
                ascolti_103
            """,
            verifica="""
                assert len(ascolti_103) == 1, "❌ ascolti_103: deve restare una sola riga, quella con UserID 103"
                assert ascolti_103["Song"].tolist() == ["Song A"] and ascolti_103["Plays"].tolist() == [4], "❌ ascolti_103: la riga dell'utente 103 ha Song A e 4 ascolti"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Costruisci in `cond` la maschera delle righe in cui `UserID` vale 103 e salva in `ascolti_103` le
                   righe che la rispettano.
                2. Nella risposta all'utente bastano la canzone e il numero di ascolti: salva in `risposta` le sole
                   colonne `Song` e `Plays` delle stesse righe, selezionando righe e colonne insieme con `loc`.
            """,
            suggerimenti=[
                """
                    `loc` accetta la maschera come primo argomento e la lista delle colonne come secondo, come in
                    `ascolti.loc[cond, ["Song", "Plays"]]`.
                """,
            ],
            starter="""
                # da creare: cond, ascolti_103, risposta
            """,
            soluzione="""
                cond = ascolti["UserID"] == 103
                ascolti_103 = ascolti[cond]
                risposta = ascolti.loc[cond, ["Song", "Plays"]]
                risposta
            """,
            verifica="""
                assert len(ascolti_103) == 1 and ascolti_103["Plays"].tolist() == [4], "❌ ascolti_103: la maschera è ascolti[\\"UserID\\"] == 103"
                assert list(risposta.columns) == ["Song", "Plays"] and len(risposta) == 1, "❌ risposta: ascolti.loc[cond, [\\"Song\\", \\"Plays\\"]]"
            """,
        ),
    )

    # E3.2 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Totale di ascolti per canzone",
        scenario="""
            Per la classifica della settimana vogliamo il totale degli ascolti di ogni canzone, sommando quelli di
            tutti gli utenti. Con `groupby` pandas raccoglie le righe della stessa canzone e ne somma gli ascolti in
            una sola istruzione, che resta uguale quando le canzoni diventano migliaia. Il risultato è una Series con
            19 ascolti per `Song A`, 7 per `Song B`, 1 per `Song C` e 2 per `Song D`.
        """,
        base=dict(
            richiesta="""
                1. Raggruppa `ascolti` per la colonna `Song`.
                2. Somma la colonna `Plays` di ogni gruppo e salva il risultato in `ascolti_per_canzone`.
            """,
            suggerimenti=[
                """
                    La forma tipica è `df.groupby("colonna_di_raggruppamento")["colonna"].funzione()`, e la funzione
                    che somma è `sum()`.
                """,
                """
                    La riga completa è `ascolti.groupby("Song")["Plays"].sum()`.
                """,
            ],
            starter="""
                ascolti_per_canzone = ascolti.groupby("...")["..."].sum()
                ascolti_per_canzone
            """,
            soluzione="""
                ascolti_per_canzone = ascolti.groupby("Song")["Plays"].sum()
                ascolti_per_canzone
            """,
            verifica="""
                atteso = {"Song A": 19, "Song B": 7, "Song C": 1, "Song D": 2}
                assert ascolti_per_canzone.to_dict() == atteso, "❌ ascolti_per_canzone: raggruppa per Song e somma Plays"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Calcola in `ascolti_per_canzone` il totale degli ascolti di ogni canzone con `groupby`.
                2. Un totale alto può venire da molti utenti o da uno solo, e la classifica vuole distinguere i due
                   casi: salva in `riepilogo` un DataFrame con il totale e il numero di utenti di ogni canzone,
                   calcolati insieme con `agg(["sum", "count"])`.

                In `riepilogo` la riga di `Song A` ha 19 ascolti da 2 utenti.
            """,
            suggerimenti=[
                """
                    Dopo aver scelto la colonna `Plays`, `agg` accetta la lista delle funzioni da applicare, e il
                    risultato ha una colonna per ciascuna, con i nomi `sum` e `count`.
                """,
            ],
            starter="""
                # da creare: ascolti_per_canzone, riepilogo
            """,
            soluzione="""
                ascolti_per_canzone = ascolti.groupby("Song")["Plays"].sum()
                riepilogo = ascolti.groupby("Song")["Plays"].agg(["sum", "count"])
                riepilogo
            """,
            verifica="""
                assert ascolti_per_canzone.to_dict() == {"Song A": 19, "Song B": 7, "Song C": 1, "Song D": 2}, "❌ ascolti_per_canzone: raggruppa per Song e somma Plays"
                assert riepilogo.loc["Song A", "sum"] == 19 and riepilogo.loc["Song A", "count"] == 2, "❌ riepilogo: groupby(\\"Song\\")[\\"Plays\\"].agg([\\"sum\\", \\"count\\"])"
            """,
        ),
    )

    # E3.3 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="L'artista più ascoltato",
        scenario="""
            Nella newsletter del mese la piattaforma pubblica la classifica degli artisti, dal più ascoltato al meno
            ascoltato, e in apertura il nome del primo. Vogliamo ottenere entrambi da `ascolti` raggruppando per
            artista, sommando gli ascolti e ordinando i totali, in modo che il mese prossimo basti rieseguire la
            cella sui dati nuovi. In testa alla classifica c'è `Artist X`, con 19 ascolti.
        """,
        base=dict(
            richiesta="""
                1. Raggruppa le righe per `Artist`, somma `Plays` e ordina i totali in modo decrescente, come nella
                   classifica, salvando il risultato in `ascolti_per_artista`.
                2. Salva in `artista_top` il nome dell'artista con il totale più alto, quello da mettere in apertura.
            """,
            suggerimenti=[
                """
                    I tre metodi si scrivono uno dopo l'altro: `groupby` e `sum()` danno i totali, e
                    `sort_values(ascending=False)` li mette dal più grande al più piccolo. Il metodo `idxmax()`
                    restituisce l'etichetta del valore massimo, cioè il nome dell'artista.
                """,
                """
                    La prima riga è `ascolti.groupby("Artist")["Plays"].sum().sort_values(ascending=False)`, e la
                    seconda `ascolti_per_artista.idxmax()`.
                """,
            ],
            starter="""
                ascolti_per_artista = ascolti.groupby(...)[...].sum().sort_values(ascending=False)
                artista_top = ascolti_per_artista.idxmax()
                artista_top  # Output: 'Artist X'
            """,
            soluzione="""
                ascolti_per_artista = ascolti.groupby("Artist")["Plays"].sum().sort_values(ascending=False)
                artista_top = ascolti_per_artista.idxmax()
                artista_top  # Output: 'Artist X'
            """,
            verifica="""
                assert ascolti_per_artista.tolist() == [19, 7, 2, 1], "❌ ascolti_per_artista: somma Plays per Artist e ordina con ascending=False"
                assert artista_top == "Artist X", "❌ artista_top: usa idxmax() sui totali"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Calcola in `ascolti_per_artista` i totali per artista in ordine decrescente e salva in
                   `artista_top` il nome del primo.
                2. Sotto la classifica la newsletter riporta tutte le righe di `ascolti`, raggruppate per artista in
                   ordine alfabetico e, per lo stesso artista, dall'ascolto più numeroso al meno numeroso: salvale in
                   `elenco` con un solo `sort_values` su due colonne.

                La prima riga di `elenco` è quella di `Artist W`, seguita dalle due di `Artist X`, prima i 15 ascolti
                e poi i 4.
            """,
            suggerimenti=[
                """
                    `sort_values` accetta in `by` una lista di colonne e in `ascending` una lista con un valore per
                    ciascuna, come in `by=["Artist", "Plays"], ascending=[True, False]`.
                """,
            ],
            starter="""
                # da creare: ascolti_per_artista, artista_top, elenco
            """,
            soluzione="""
                ascolti_per_artista = ascolti.groupby("Artist")["Plays"].sum().sort_values(ascending=False)
                artista_top = ascolti_per_artista.idxmax()

                elenco = ascolti.sort_values(by=["Artist", "Plays"], ascending=[True, False])
                print(artista_top)  # Output: Artist X
                elenco
            """,
            verifica="""
                assert ascolti_per_artista.tolist() == [19, 7, 2, 1] and artista_top == "Artist X", "❌ ascolti_per_artista e artista_top: groupby, sum, sort_values e idxmax"
                assert elenco["UserID"].tolist() == [106, 101, 103, 105, 102, 104], "❌ elenco: by=[\\"Artist\\", \\"Plays\\"], ascending=[True, False]"
            """,
        ),
    )

    # E3.4 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Gli utenti più assidui",
        scenario="""
            La piattaforma vuole mandare un messaggio di ringraziamento agli utenti che hanno ascoltato una canzone
            più di 3 volte, e ci serve quindi l'insieme dei loro `UserID`. Lo raccogliamo in un set perché un utente che avesse superato i 3 ascolti con più canzoni comparirebbe più
            volte, mentre deve ricevere un solo messaggio. Gli utenti sono 101, 103 e 105, e Python può mostrarli in
            un ordine qualsiasi, perché un set non ha ordine.
        """,
        base=dict(
            richiesta="""
                1. Costruisci in `cond` la maschera delle righe in cui `Plays` è maggiore di 3.
                2. Seleziona con `loc` la colonna `UserID` delle sole righe della maschera e salvala in `utenti`.
                3. Salva in `utenti_assidui` il set costruito da `utenti`.
            """,
            suggerimenti=[
                """
                    `loc` accetta la maschera delle righe come primo argomento e il nome della colonna come secondo,
                    e la funzione `set()` costruisce un set da una Series.
                """,
                """
                    Le righe sono `ascolti["Plays"] > 3`, `ascolti.loc[cond, "UserID"]` e `set(utenti)`.
                """,
            ],
            starter="""
                cond = ascolti["Plays"] > ...
                utenti = ascolti.loc[cond, "..."]
                utenti_assidui = set(...)
                utenti_assidui  # Output: {105, 101, 103}
            """,
            soluzione="""
                cond = ascolti["Plays"] > 3
                utenti = ascolti.loc[cond, "UserID"]
                utenti_assidui = set(utenti)
                utenti_assidui  # Output: {105, 101, 103}
            """,
            verifica="""
                assert isinstance(utenti_assidui, set), "❌ utenti_assidui: costruiscilo con set(utenti)"
                assert utenti_assidui == {101, 103, 105}, "❌ utenti_assidui: la maschera è ascolti[\\"Plays\\"] > 3 e la colonna è UserID"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `utenti_assidui` il set degli `UserID` delle righe in cui `Plays` è maggiore di 3,
                   selezionando la colonna con `loc` e la maschera.
                2. Nel messaggio vogliamo dire anche quanti minuti hanno ascoltato in tutto. Aggiungi ad `ascolti`
                   la colonna `Length` con la durata di ogni canzone, che supponiamo di 3 minuti per tutte, e salva
                   in `minuti_assidui` la somma di `Plays` per `Length` sulle righe della maschera.

                `minuti_assidui` vale 72.
            """,
            suggerimenti=[
                """
                    Assegnando un solo valore a una colonna nuova, come in `ascolti["Length"] = 3`, pandas lo ripete
                    in tutte le righe; il prodotto di due colonne è una Series, che si filtra con la stessa maschera.
                """,
            ],
            starter="""
                # da creare: utenti_assidui, la colonna Length, minuti_assidui
            """,
            soluzione="""
                cond = ascolti["Plays"] > 3
                utenti_assidui = set(ascolti.loc[cond, "UserID"])

                ascolti["Length"] = 3
                minuti = ascolti["Plays"] * ascolti["Length"]
                minuti_assidui = minuti[cond].sum()

                print(utenti_assidui)  # Output: {105, 101, 103}
                print(minuti_assidui)  # Output: 72
            """,
            verifica="""
                assert utenti_assidui == {101, 103, 105}, "❌ utenti_assidui: set(ascolti.loc[cond, \\"UserID\\"]) con cond = Plays > 3"
                assert ascolti["Length"].tolist() == [3] * 6, "❌ Length: assegna 3 alla colonna nuova"
                assert minuti_assidui == 72, "❌ minuti_assidui: somma Plays * Length sulle righe della maschera"
            """,
        ),
    )

    # ------------------------------------------------------------------ serie temporali
    nb.md("""
        Gli ultimi due esercizi usano il dataset di prova del notebook 08: tre giorni di misure quartorarie di
        potenza (`power_kw`) e di temperatura (`temp_c`) a partire dal 1° marzo 2025, da cui sono state tolte 18
        righe per simulare le acquisizioni mancanti. La cella qui sotto lo ricostruisce con lo stesso seme casuale,
        quindi i valori sono identici a quelli del notebook, e va eseguita prima dei due esercizi. Il timestamp è
        una stringa nella forma `01/03/2025 00:15`, che `pd.to_datetime` legge con il formato `"%d/%m/%Y %H:%M"`:
        `%d` è il giorno, `%m` il mese, `%Y` l'anno a quattro cifre, `%H` l'ora e `%M` i minuti.
    """)
    nb.code("""
        import numpy as np
        np.random.seed(42)

        intervallo = pd.date_range("2025-03-01 00:00", periods=3 * 24 * 4, freq="15min")
        ore = intervallo.hour + intervallo.minute / 60
        power_kw = 220 + 60 * np.sin(2 * np.pi * (ore / 24)) + np.random.normal(0, 8, size=len(intervallo))
        temp_c = 12 + 5 * np.sin(2 * np.pi * ((ore - 6) / 24)) + np.random.normal(0, 0.7, size=len(intervallo))

        df = pd.DataFrame({
            "timestamp_str": intervallo.strftime("%d/%m/%Y %H:%M"),
            "power_kw": power_kw.round(1),
            "temp_c": temp_c.round(1),
        })

        indici_da_togliere = np.random.choice(df.index, size=18, replace=False)
        df = df.drop(indici_da_togliere).reset_index(drop=True)
        df.head()
    """)

    # E3.5 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Un pomeriggio di misure",
        scenario="""
            Vogliamo le misure del pomeriggio del 1° marzo, dalle 12:00 alle 18:00. Finché il timestamp è testo
            pandas non sa ordinarlo né selezionarne un periodo, mentre dopo averlo convertito in date e usato come
            indice basta scrivere i due estremi dentro `loc`. Il risultato ha 22 righe, perché con gli estremi
            inclusi le sei ore contengono 25 quarti d'ora, e tre misure mancano.
        """,
        base=dict(
            richiesta="""
                1. Crea in `df` la colonna `timestamp` convertendo `timestamp_str` con `pd.to_datetime` e il formato
                   `"%d/%m/%Y %H:%M"`.
                2. Costruisci `df_serie` con le colonne `power_kw` e `temp_c`, il timestamp come indice e le righe
                   in ordine di tempo, usando `set_index` e `sort_index`.
                3. Seleziona in `periodo` le righe dal `2025-03-01 12:00` al `2025-03-01 18:00` con `.loc`.
            """,
            suggerimenti=[
                """
                    Il formato si passa a `pd.to_datetime` con il parametro `format`. Con un indice di date, `loc`
                    accetta un intervallo tra due stringhe, separate dai due punti come in uno slicing, e include
                    entrambi gli estremi.
                """,
                """
                    Le righe che mancano sono `format="%d/%m/%Y %H:%M"`, `set_index("timestamp")` e
                    `df_serie.loc["2025-03-01 12:00":"2025-03-01 18:00"]`.
                """,
            ],
            starter="""
                df["timestamp"] = pd.to_datetime(df["timestamp_str"], format=...)
                df_serie = df[["timestamp", "power_kw", "temp_c"]].set_index(...).sort_index()

                periodo = df_serie.loc[...]
                len(periodo)  # Output: 22
            """,
            soluzione="""
                df["timestamp"] = pd.to_datetime(df["timestamp_str"], format="%d/%m/%Y %H:%M")
                df_serie = df[["timestamp", "power_kw", "temp_c"]].set_index("timestamp").sort_index()

                periodo = df_serie.loc["2025-03-01 12:00":"2025-03-01 18:00"]
                len(periodo)  # Output: 22
            """,
            verifica="""
                assert isinstance(df_serie.index, pd.DatetimeIndex) and df_serie.index.is_monotonic_increasing, "❌ df_serie: converti timestamp_str, usa set_index(\\"timestamp\\") e sort_index()"
                assert list(df_serie.columns) == ["power_kw", "temp_c"], "❌ df_serie: tieni le colonne power_kw e temp_c"
                assert len(periodo) == 22 and str(periodo.index[0]) == "2025-03-01 12:00:00", "❌ periodo: df_serie.loc[\\"2025-03-01 12:00\\":\\"2025-03-01 18:00\\"]"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Converti `timestamp_str` in date con il formato `"%d/%m/%Y %H:%M"` e costruisci `df_serie` con
                   `power_kw` e `temp_c`, il timestamp come indice e le righe in ordine di tempo.
                2. Seleziona in `periodo` le righe dal `2025-03-01 12:00` al `2025-03-01 18:00`.
                3. Per sapere dove la serie ha dei buchi, salva in `intervalli` il conteggio delle distanze tra due
                   timestamp consecutivi, calcolate con `diff()` sull'indice trasformato in Series.

                In `intervalli` la distanza di 15 minuti compare 252 volte, quella di 30 minuti 16 volte e quella di
                45 minuti una volta, cioè ci sono 16 buchi da una misura e uno da due, per un totale di 18 misure
                mancanti.
            """,
            suggerimenti=[
                """
                    L'indice diventa una Series con `df_serie.index.to_series()`, `diff()` calcola la distanza da
                    ogni valore al precedente e `value_counts()` conta quante volte compare ciascuna distanza.
                """,
            ],
            starter="""
                # da creare: df_serie, periodo, intervalli
            """,
            soluzione="""
                df["timestamp"] = pd.to_datetime(df["timestamp_str"], format="%d/%m/%Y %H:%M")
                df_serie = df[["timestamp", "power_kw", "temp_c"]].set_index("timestamp").sort_index()

                periodo = df_serie.loc["2025-03-01 12:00":"2025-03-01 18:00"]
                intervalli = df_serie.index.to_series().diff().value_counts()

                print(len(periodo))  # Output: 22
                intervalli
            """,
            verifica="""
                assert isinstance(df_serie.index, pd.DatetimeIndex) and df_serie.index.is_monotonic_increasing, "❌ df_serie: converti timestamp_str, usa set_index e sort_index()"
                assert len(periodo) == 22, "❌ periodo: df_serie.loc[\\"2025-03-01 12:00\\":\\"2025-03-01 18:00\\"]"
                assert intervalli[pd.Timedelta("15min")] == 252 and intervalli[pd.Timedelta("30min")] == 16, "❌ intervalli: df_serie.index.to_series().diff().value_counts()"
            """,
        ),
    )

    # E3.6 ---------------------------------------------------------------
    nb.md("""
        Con un indice di date le parti del tempo si leggono direttamente dall'indice: `df.index.date` dà la sola
        data di ogni riga e `df.index.dayofweek` il giorno della settimana, che vale 0 il lunedì e 6 la domenica.
        Il metodo `resample("h")` raccoglie invece in un gruppo tutte le misure della stessa ora, come un `groupby`
        guidato dal tempo, e lascia al metodo che segue il compito di combinarle: `mean()` ne calcola la media e
        `sum()` la somma. Ogni gruppo prende come etichetta l'inizio dell'ora.
    """)
    esercizio_due_aule(
        nb,
        titolo="Il fine settimana e le medie orarie",
        scenario="""
            Vogliamo aggiungere alla serie quartoraria due colonne, la data di ogni misura e un valore che dica se
            la misura cade nel fine settimana, e poi passare dai quarti d'ora alle ore calcolando per ogni ora la
            media e la somma di `power_kw`. Le prime righe della cella ricostruiscono la serie dell'esercizio E3.5
            con i buchi riempiti, come nel notebook 08, quindi ogni ora contiene quattro misure e la somma vale
            quattro volte la media. Poiché il 1° marzo 2025 è un sabato, 192 delle 288 righe cadono nel weekend;
            il risultato orario ha 72 valori, e per la prima ora la media è 230.925 e la somma 923.7.
        """,
        base=dict(
            richiesta="""
                1. Aggiungi a `df_15min` la colonna `date`, con la sola data letta dall'indice.
                2. Aggiungi la colonna `is_weekend`, che vale `True` il sabato e la domenica, confrontando con 5 il
                   giorno della settimana dell'indice.
                3. Calcola in `media_oraria` la media oraria di `power_kw` con `resample("h")`, e in `somma_oraria`
                   la somma oraria della stessa colonna.
            """,
            suggerimenti=[
                """
                    Le due colonne si ricavano da `df_15min.index.date` e da `df_15min.index.dayofweek`, e il
                    sabato e la domenica sono i giorni con valore maggiore o uguale a 5. Il resampling si applica
                    alla sola colonna `power_kw`.
                """,
                """
                    Le righe sono `df_15min.index.dayofweek >= 5` e `df_15min["power_kw"].resample("h").mean()`, e
                    per la somma si cambia soltanto `mean()` in `sum()`.
                """,
            ],
            starter=unisci(PREPARA_SERIE, """
                df_15min["date"] = ...
                df_15min["is_weekend"] = ...

                media_oraria = df_15min["power_kw"].resample(...).mean()
                somma_oraria = ...

                print(df_15min["is_weekend"].sum())  # Output: 192
                pd.DataFrame({"mean": media_oraria, "sum": somma_oraria}).head()
            """),
            soluzione=unisci(PREPARA_SERIE, """
                df_15min["date"] = df_15min.index.date
                df_15min["is_weekend"] = df_15min.index.dayofweek >= 5

                media_oraria = df_15min["power_kw"].resample("h").mean()
                somma_oraria = df_15min["power_kw"].resample("h").sum()

                print(df_15min["is_weekend"].sum())  # Output: 192
                pd.DataFrame({"mean": media_oraria, "sum": somma_oraria}).head()
            """),
            verifica="""
                assert df_15min["date"].nunique() == 3, "❌ date: usa df_15min.index.date"
                assert df_15min["is_weekend"].sum() == 192, "❌ is_weekend: df_15min.index.dayofweek >= 5"
                assert len(media_oraria) == 72 and round(media_oraria.iloc[0], 3) == 230.925, "❌ media_oraria: df_15min[\\"power_kw\\"].resample(\\"h\\").mean()"
                assert round(somma_oraria.iloc[0], 1) == 923.7, "❌ somma_oraria: come media_oraria, con sum() al posto di mean()"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Aggiungi a `df_15min` la colonna `date`, con la sola data di ogni misura, e la colonna
                   `is_weekend`, che vale `True` il sabato e la domenica, leggendole dall'indice.
                2. Calcola in `media_oraria` e in `somma_oraria` la media e la somma di `power_kw` per ogni ora.
                3. Le misure quartorarie oscillano per il rumore, e una media mobile su due ore le rende più
                   regolari senza cambiarne la frequenza: salva in `media_mobile` la media di `power_kw` su una
                   finestra di 8 quarti d'ora, con `rolling`.

                Le prime sette righe di `media_mobile` sono `NaN`, perché non hanno otto valori precedenti, e
                l'ottava vale circa 237.9.
            """,
            suggerimenti=[
                """
                    `df_15min.index.dayofweek >= 5` riconosce il weekend; `rolling(8)` raccoglie ogni valore con i
                    sette precedenti, e il `mean()` che segue ne calcola la media, come nel notebook 09.
                """,
            ],
            starter=unisci(PREPARA_SERIE, """
                # da creare: le colonne date e is_weekend, media_oraria, somma_oraria, media_mobile
            """),
            soluzione=unisci(PREPARA_SERIE, """
                df_15min["date"] = df_15min.index.date
                df_15min["is_weekend"] = df_15min.index.dayofweek >= 5

                media_oraria = df_15min["power_kw"].resample("h").mean()
                somma_oraria = df_15min["power_kw"].resample("h").sum()
                media_mobile = df_15min["power_kw"].rolling(8).mean()

                print(df_15min["is_weekend"].sum())  # Output: 192
                media_mobile.head(10)
            """),
            verifica="""
                assert df_15min["date"].nunique() == 3 and df_15min["is_weekend"].sum() == 192, "❌ date e is_weekend: leggile da df_15min.index"
                assert len(media_oraria) == 72 and round(somma_oraria.iloc[0], 1) == 923.7, "❌ media_oraria e somma_oraria: resample(\\"h\\") con mean() e sum()"
                assert media_mobile.isna().sum() == 7 and round(media_mobile.iloc[7], 1) == 237.9, "❌ media_mobile: df_15min[\\"power_kw\\"].rolling(8).mean()"
            """,
        ),
    )

    # Sfida ---------------------------------------------------------------
    nb.esercizio(
        titolo="Sfida: una riga per giorno",
        facoltativo=True,
        scenario="""
            Partendo dalla serie quartoraria con i buchi riempiti, vogliamo un riepilogo dei tre giorni da leggere a
            colpo d'occhio, con una riga per giorno come `01/03/2025: 218.7 kW`, in cui la potenza media del giorno
            viene calcolata e non scritta a mano. Con un `resample` giornaliero e un ciclo `for` sugli elementi del
            risultato, la stessa cella funziona anche su un mese di dati. La forma delle righe è libera, quindi
            l'esercizio non ha una verifica e la cella `soluzione` mostra un esempio, in cui le medie dei tre giorni
            sono 218.7, 220.3 e 220.1 kW.
        """,
        richiesta="""
            1. Calcola la media giornaliera di `power_kw` con `resample("D")`.
            2. Scorri il risultato con un ciclo `for` e stampa una riga per giorno con una f-string.
        """,
        suggerimenti=[
            """
                Come un dizionario, una Series ha il metodo `items()`, che nel ciclo restituisce ogni etichetta con il
                suo valore. L'etichetta è un timestamp, che `strftime("%d/%m/%Y")` scrive come testo, e nella f-string
                `{valore:.1f}` mostra un decimale.
            """,
        ],
        starter=unisci(PREPARA_SERIE, """
            # il riepilogo, una riga per giorno
            ...
        """),
        soluzione=unisci(PREPARA_SERIE, """
            giornaliera = df_15min["power_kw"].resample("D").mean()

            for giorno, valore in giornaliera.items():
                print(f"{giorno.strftime('%d/%m/%Y')}: {valore:.1f} kW")
            # Output:
            # 01/03/2025: 218.7 kW
            # 02/03/2025: 220.3 kW
            # 03/03/2025: 220.1 kW
        """),
        verifica=None,
    )
    return nb
