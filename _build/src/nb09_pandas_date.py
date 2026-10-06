"""09 · pandas: le date."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="09",
        file="09_Pandas_date",
        titolo="pandas: le date",
        blocco=3,
        giornata=2,
        intento="Una stringa che sembra una data è testo. Oggi la trasformiamo in una data vera e le facciamo le domande che si fanno alle date: che ora è, che giorno della settimana, cosa manca.",
        obiettivi={
            "base": [
                "trasformare testo in date e interrogarle con `.dt`",
                "usare il tempo come indice per selezionare periodi",
                "riconoscere buchi, duplicati e ora legale in una serie temporale",
            ],
            "avanzata": [
                "trasformare testo in date e interrogarle con `.dt`",
                "usare il tempo come indice e riconoscere buchi, duplicati e ora legale",
                "cambiare granularità con `resample` e costruire lag e medie mobili con `shift` e `rolling`",
            ],
        },
        tempo={"base": 70, "avanzata": 90},
        dati=["prezzi_zonali_2025_settimana.csv", "load_total_north_hourly_2024.xlsx", "TexasTurbine.csv"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Da testo a data", intro="""
        Un file CSV non sa cosa sia una data: `2025-06-02 00:00` arriva come testo, e con il testo non
        si fanno conti, non si ordinano i mesi, non si chiede "che ora è". Partiamo dai prezzi zonali
        di una settimana di giugno.
    """)
    nb.code("""
        import pandas as pd

        prezzi = pd.read_csv("../Dati/prezzi_zonali_2025_settimana.csv")
        prezzi.dtypes
    """)
    nb.md("""
        `timestamp` è `str`. `pd.to_datetime` lo trasforma in una colonna di date vere (`datetime64`).
        Come sempre, il risultato si riassegna.
    """)
    nb.code("""
        prezzi["timestamp"] = pd.to_datetime(prezzi["timestamp"])
        prezzi.dtypes
    """)
    nb.md("""
        Qui pandas ha indovinato il formato perché è quello ISO: anno-mese-giorno, nessuna ambiguità.
        Con le date scritte all'italiana conviene dirglielo noi con `format`: `%d` giorno, `%m` mese,
        `%Y` anno a quattro cifre, `%H:%M` ore e minuti.
    """)
    nb.code("""
        pd.to_datetime("04/06/2025 14:30", format="%d/%m/%Y %H:%M")
    """)
    nb.md("""
        Perché insistere sul formato: `01/02/2025` è il primo febbraio o il 2 gennaio? Se non glielo
        diciamo, pandas ragiona all'americana. `dayfirst=True` gli dice che il giorno viene prima.
    """)
    nb.code("""
        print(pd.to_datetime("01/02/2025"))                  # mese/giorno: 2 gennaio
        print(pd.to_datetime("01/02/2025", dayfirst=True))   # giorno/mese: 1 febbraio
    """)
    nb.md("""
        Su una colonna intera il problema peggiora: pandas sceglie il formato guardando la prima riga e
        poi lo pretende da tutte le altre. Questa cella dà errore apposta: leggiamolo.
    """)
    nb.code("""
        date_it = pd.Series(["01/02/2025", "15/02/2025", "28/02/2025"])
        pd.to_datetime(date_it)
    """, errore=True)
    nb.md("""
        Dal basso: `time data "15/02/2025" doesn't match format "%m/%d/%Y"`. Dalla prima riga ha dedotto
        mese/giorno, e 15 non è un mese. Il rimedio è dichiarare il formato (o almeno `dayfirst=True`).
    """)
    nb.code("""
        pd.to_datetime(date_it, format="%d/%m/%Y")
    """)
    nb.md("""
        Quando in mezzo alle date c'è un valore che data non è (un "n.d.", una cella vuota scritta a
        mano), `errors="coerce"` lo trasforma in `NaT`, il valore mancante delle date, invece di fermare
        tutto.
    """)
    nb.code("""
        date_sporche = pd.Series(["01/02/2025", "n.d.", "15/02/2025"])
        pd.to_datetime(date_sporche, format="%d/%m/%Y", errors="coerce")
    """)
    nb.box("attenzione", """
        `errors="coerce"` nasconde i problemi dentro ai `NaT`. Subito dopo contiamoli con
        `.isna().sum()`: se sono 2 su 8760 è una svista del fornitore, se sono 4000 è il formato sbagliato.
    """)

    nb.sottosezione("Il caso della turbina", intro="""
        I dati della turbina texana hanno un timestamp senza anno: `Jan 1, 12:00 am`. Vediamo cosa
        succede se lo diamo a `to_datetime` così com'è.
    """)
    nb.code("""
        turbina = pd.read_csv("../Dati/TexasTurbine.csv")
        turbina["Time stamp"].head(3)
    """)
    nb.code("""
        pd.to_datetime(turbina["Time stamp"]).head(3)
    """)
    nb.md("""
        pandas avvisa che non riconosce il formato, poi fa del suo meglio: anno 1. Nessun errore, un dato
        sbagliato. Il rimedio è aggiungere noi l'anno davanti al testo (il `+` tra una stringa e una
        colonna funziona riga per riga) e dichiarare il formato: `%b` è il mese abbreviato in inglese,
        `%I` l'ora su 12 e `%p` am/pm.
    """)
    nb.code("""
        turbina["timestamp"] = pd.to_datetime("2023 " + turbina["Time stamp"], format="%Y %b %d, %I:%M %p")
        turbina[["Time stamp", "timestamp"]].head(3)
    """)
    nb.prova_tu(
        richiesta="""
            Le letture di un contatore arrivano con la data all'italiana e un valore che data non è.
            Convertile in `date_lette` dichiarando il formato e trasformando il valore sbagliato in `NaT`.
        """,
        starter="""
            letture = pd.Series(["03/06/2025 08:15", "03/06/2025 08:30", "lettura mancante", "03/06/2025 09:00"])

            date_lette = ...
            date_lette
        """,
        soluzione="""
            letture = pd.Series(["03/06/2025 08:15", "03/06/2025 08:30", "lettura mancante", "03/06/2025 09:00"])

            date_lette = pd.to_datetime(letture, format="%d/%m/%Y %H:%M", errors="coerce")
            date_lette
        """,
        verifica="""
            assert date_lette.isna().sum() == 1, "❌ Il valore che non è una data deve diventare NaT: serve errors='coerce'"
            assert date_lette.iloc[0].month == 6, "❌ Il 03/06 è il 3 giugno: il giorno viene prima del mese"
        """,
    )

    # ------------------------------------------------------------------ 2
    nb.sezione("Gli attributi `.dt`", intro="""
        Una colonna di date risponde alle domande attraverso `.dt`: `.dt.hour` l'ora, `.dt.dayofweek`
        il giorno della settimana (0 lunedì, 6 domenica), `.dt.month` il mese, `.dt.date` la data senza
        l'ora. Il risultato è una colonna nuova, lunga quanto la tabella.
    """)
    nb.code("""
        prezzi["ora"] = prezzi["timestamp"].dt.hour
        prezzi["giorno_settimana"] = prezzi["timestamp"].dt.dayofweek
        prezzi.head()
    """)
    nb.md("""
        `day_name()` dà il nome del giorno, in inglese. È un metodo, quindi con le parentesi.
    """)
    nb.code("""
        prezzi["timestamp"].dt.day_name().unique()
    """)
    nb.md("""
        Il weekend è "giorno della settimana 5 o 6": una condizione sulla colonna, cioè una maschera.
        Prima la maschera, poi la usiamo per confrontare il prezzo medio di sabato e domenica con quello
        dei giorni lavorativi.
    """)
    nb.code("""
        weekend = prezzi["giorno_settimana"] >= 5
        weekend.head()
    """)
    nb.code("""
        print(f"Weekend:   {prezzi.loc[weekend, 'eur_mwh'].mean():.2f} €/MWh")
        print(f"Lun-ven:   {prezzi.loc[~weekend, 'eur_mwh'].mean():.2f} €/MWh")
    """)
    nb.md("""
        Con l'ora in una colonna, il profilo orario è un `groupby` come quelli appena visti: prezzo medio
        per ora del giorno, su tutte le zone e tutti i giorni. L'ora finisce nell'indice; `reset_index()`
        la riporta colonna.
    """)
    nb.code("""
        profilo = prezzi.groupby("ora")["eur_mwh"].mean().reset_index()
        profilo.round(1)
    """)
    nb.md("""
        `.dt.date` toglie l'ora e lascia il giorno. Serve soprattutto per contare: quante righe ha ogni
        giorno? Con 6 zone e 24 ore ne aspettiamo 144.
    """)
    nb.code("""
        prezzi["timestamp"].dt.date.value_counts().sort_index()
    """)
    nb.md("""
        Il 4 giugno ne ha 142. Due righe mancano da qualche parte: ce lo segniamo, tra poco le troviamo.
    """)
    nb.prova_tu(
        richiesta="""
            Il prezzo di notte: calcola in `prezzo_notte` il prezzo medio delle ore da 0 a 5 comprese,
            su tutte le zone. Costruisci prima la maschera `notte` sulla colonna `ora`.
        """,
        starter="""
            notte = ...
            prezzo_notte = ...
            round(prezzo_notte, 2)
        """,
        soluzione="""
            notte = prezzi["ora"] <= 5
            prezzo_notte = prezzi.loc[notte, "eur_mwh"].mean()
            round(prezzo_notte, 2)
        """,
        verifica="""
            assert round(prezzo_notte, 2) == 86.3, "❌ Ore da 0 a 5 comprese: la condizione è ora <= 5 (o ora < 6)"
        """,
    )
    nb.box("ricorda", """
        Una stringa che sembra una data è testo: prima `pd.to_datetime`, poi `.dt`. Se il formato è
        noto, dichiaralo con `format`; se è all'italiana e non vuoi scriverlo, `dayfirst=True`.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Il tempo come indice", intro="""
        Per selezionare un periodo è comodo mettere il timestamp nell'indice: pandas capisce
        `"2025-06-04"` come "tutto il 4 giugno". Lo facciamo su una zona sola, il NORD, e ordiniamo
        l'indice: le selezioni per intervallo lo vogliono in ordine.
    """)
    nb.code("""
        mask_nord = prezzi["zona"] == "NORD"
        nord = prezzi[mask_nord]
        nord = nord.set_index("timestamp").sort_index()
        nord.head(3)
    """)
    nb.md("""
        Adesso `loc` accetta una data scritta come testo. Un giorno intero:
    """)
    nb.code("""
        nord.loc["2025-06-04"]
    """)
    nb.md("""
        22 righe, non 24: sono le due che mancavano. Un intervallo si scrive con i due punti, e qui la
        fine è compresa (sono etichette, non posizioni).
    """)
    nb.code("""
        nord.loc["2025-06-04 12:00":"2025-06-04 17:00"]
    """)
    nb.md("""
        Dal 7 giugno in avanti, solo la colonna del prezzo, e la media: il weekend del NORD in una riga.
    """)
    nb.code("""
        nord.loc["2025-06-07":, "eur_mwh"].mean()
    """)
    nb.prova_tu(
        richiesta="""
            Seleziona dal DataFrame `nord` il 6 giugno e metti in `max_6_giugno` il prezzo più alto di
            quel giorno.
        """,
        starter="""
            max_6_giugno = ...
            max_6_giugno
        """,
        soluzione="""
            max_6_giugno = nord.loc["2025-06-06", "eur_mwh"].max()
            max_6_giugno
        """,
        verifica="""
            assert max_6_giugno == 133.34, "❌ Seleziona il giorno con loc e prendi il massimo della colonna eur_mwh"
        """,
    )

    nb.sottosezione("Terna arriva al contrario", intro="""
        Il carico della zona Nord del 2024, pubblicato da Terna, arriva in Excel. `read_excel` ci dà le
        date già convertite, ma la tabella è ordinata dall'ultimo quarto d'ora al primo.
    """)
    nb.code("""
        carico_grezzo = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
        carico_grezzo.head(3)
    """)
    nb.md("""
        Il nome del file dice `hourly`, le righe dicono un valore ogni 15 minuti: con i dati conta quello
        che c'è dentro. Rimettiamo le righe in ordine di tempo con `sort_values`.
    """)
    nb.code("""
        carico = carico_grezzo.sort_values("Date")
        carico.head(3)
    """)
    nb.code("""
        len(carico)
    """)
    nb.md("""
        35 136 righe: 366 giorni per 96 quarti d'ora, il conto torna alla perfezione. Teniamolo a mente,
        perché tra poco scopriremo che torna per caso.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Frequenza e buchi", intro="""
        La prima domanda da fare a una serie temporale è: ogni quanto arriva un dato? `diff()` calcola
        la distanza tra una riga e la successiva; `value_counts()` conta quante volte compare ogni
        distanza. Se la serie è regolare, c'è un valore solo.
    """)
    nb.code("""
        nord.index.diff().value_counts()
    """)
    nb.md("""
        164 passi di un'ora e un salto di tre: in mezzo mancano due ore. `asfreq("h")` ricostruisce la
        griglia oraria completa e mette `NaN` dove non c'era niente, così i buchi diventano righe che si
        possono contare e guardare.
    """)
    nb.code("""
        nord_completo = nord.asfreq("h")
        nord_completo["eur_mwh"].isna().sum()
    """)
    nb.code("""
        buchi = nord_completo["eur_mwh"].isna()
        nord_completo[buchi]
    """)
    nb.md("""
        Le 14:00 e le 15:00 del 4 giugno. Per riempirle ci sono due strade: `interpolate()` tira una
        retta tra il valore prima e quello dopo, `ffill()` ripete l'ultimo valore noto. Le vediamo sulle
        stesse sei ore.
    """)
    nb.code("""
        finestra = nord_completo.loc["2025-06-04 12:00":"2025-06-04 17:00", "eur_mwh"]
        finestra.interpolate()
    """)
    nb.code("""
        finestra.ffill()
    """)
    nb.md("""
        Prezzi, carichi e temperature variano con continuità: `interpolate`. Uno stato che resta finché
        qualcuno non lo cambia (un livello, un setpoint, una lettura di contatore): `ffill`. In entrambi i
        casi, prima si contano i buchi e si scrive nel report quanti valori sono stimati.
    """)
    nb.prova_tu(
        richiesta="""
            Riempi i buchi del NORD per interpolazione: metti in `nord_riempito` la colonna `eur_mwh`
            di `nord_completo` senza più `NaN`.
        """,
        starter="""
            nord_riempito = ...
            nord_riempito.isna().sum()
        """,
        soluzione="""
            nord_riempito = nord_completo["eur_mwh"].interpolate()
            nord_riempito.isna().sum()
        """,
        verifica="""
            assert nord_riempito.isna().sum() == 0, "❌ Dopo interpolate() non devono restare NaN"
            assert round(nord_riempito.loc["2025-06-04 14:00"], 2) == 123.47, "❌ Alle 14:00 ci aspettiamo un valore a metà strada tra le 13:00 e le 16:00: usa interpolate, non ffill"
        """,
    )
    nb.box("ricorda", """
        Tre righe prima di qualunque analisi su una serie temporale: `sort_values` sul tempo,
        `duplicated().sum()`, `diff().value_counts()`. Dopo, sai con cosa hai a che fare.
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("L'ora legale", intro="""
        Due volte l'anno l'orologio salta: l'ultima domenica di marzo le 2:00 non esistono, l'ultima
        domenica di ottobre esistono due volte. Terna scrive l'ora locale, quindi nel file c'è un buco
        e ci sono dei doppioni. Partiamo dai doppioni.
    """)
    nb.code("""
        carico["Date"].duplicated().sum()
    """)
    nb.code("""
        doppioni = carico["Date"].duplicated(keep=False)
        carico[doppioni]
    """)
    nb.md("""
        Le 2:00, 2:15, 2:30 e 2:45 del 27 ottobre compaiono due volte, con carichi diversi: una serie è
        l'ultima ora legale, l'altra la prima ora solare, e il file non dice quale sia quale.
        `drop_duplicates(subset="Date")` tiene la prima occorrenza di ogni timestamp.
    """)
    nb.code("""
        carico = carico.drop_duplicates(subset="Date")
        len(carico)
    """)
    nb.md("""
        35 132 righe: un'ora di dati persa su 8784, e lo si scrive nel report. Ora il buco di marzo. La
        distanza tra righe consecutive dovrebbe essere sempre un quarto d'ora.
    """)
    nb.code("""
        carico["Date"].diff().value_counts()
    """)
    nb.md("""
        Un salto di un'ora e un quarto. Per guardarlo da vicino mettiamo il tempo nell'indice, come
        abbiamo fatto con i prezzi, e selezioniamo la notte del 31 marzo.
    """)
    nb.code("""
        carico = carico.set_index("Date")
        carico.loc["2024-03-31 01:30":"2024-03-31 03:15"]
    """)
    nb.md("""
        Dalle 1:45 si passa alle 3:00: le 2:00 di quella notte non sono mai esistite. Ecco perché il
        conto delle righe tornava: quattro quarti d'ora in più a ottobre, quattro in meno a marzo. Il
        buco non va riempito, è il calendario che è fatto così.
    """)

    with nb.solo("avanzata"):
        nb.sottosezione("Fusi orari", intro="""
            pandas sa attaccare un fuso orario alle date con `tz_localize`. Di fronte a un'ora che
            esiste due volte dovrebbe capire da solo quale è quale, con `ambiguous="infer"`: funziona se
            i doppioni sono in blocco (2:00, 2:15, 2:30, 2:45, poi di nuovo 2:00...). Nel file originale
            sono intrecciati. Questa cella dà errore apposta.
        """)
        nb.code("""
            ordinato = carico_grezzo.sort_values("Date")
            ordinato["Date"].dt.tz_localize("Europe/Rome", ambiguous="infer")
        """, errore=True)
        nb.md("""
            `There are 4 dst switches when there should only be 1`: pandas vede quattro passaggi
            dall'ora legale alla solare dove ne aspetta uno. Sull'indice pulito l'ambiguità resta, ma la
            decidiamo noi: `ambiguous="NaT"` marca come mancanti le quattro ore incerte.
        """)
        nb.code("""
            indice_locale = carico.index.tz_localize("Europe/Rome", ambiguous="NaT")
            indice_locale.isna().sum()
        """)
        nb.md("""
            Su un periodo senza cambio d'ora non c'è niente da decidere. Febbraio si localizza senza
            discussioni, e `tz_convert("UTC")` lo porta nel fuso che usano la maggior parte dei sistemi
            di misura e delle API.
        """)
        nb.code("""
            febbraio = carico.loc["2024-02"]
            febbraio = febbraio.tz_localize("Europe/Rome")
            febbraio.head(3)
        """)
        nb.code("""
            febbraio.tz_convert("UTC").head(3)
        """)
        nb.box("nota", """
            Quando un dato "sembra spostato di un'ora" rispetto a un altro, il fuso è il primo sospettato:
            Terna pubblica l'ora locale, molti SCADA e molte API lavorano in UTC.
        """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Differenze tra date", intro="""
        La differenza tra due date è un `Timedelta`, cioè una durata. Quanto copre il dataset Terna?
    """)
    nb.code("""
        durata = carico.index.max() - carico.index.min()
        durata
    """)
    nb.md("""
        Da un `Timedelta` si estraggono i giorni con `.days`, oppure si divide per un'altra durata per
        avere il numero che ci serve: le ore, per esempio.
    """)
    nb.code("""
        print(durata.days)
        print(durata / pd.Timedelta("1h"))
    """)
    nb.md("""
        Una durata si somma a una data. Comodo per "una settimana dopo", e istruttivo sulla notte del
        31 marzo: pandas non sa che quelle 2:00 non sono mai esistite, per lui è un orologio e basta.
    """)
    nb.code("""
        print(pd.Timestamp("2025-06-02") + pd.Timedelta(days=7))
        print(pd.Timestamp("2024-03-31 01:45") + pd.Timedelta("15min"))
    """)
    nb.prova_tu(
        richiesta="""
            Quante ore copre il dataset dei prezzi? Calcola `durata_prezzi` come differenza tra l'ultimo
            e il primo `timestamp` di `prezzi`, poi `ore_prezzi` dividendo per un'ora.
        """,
        starter="""
            durata_prezzi = ...
            ore_prezzi = ...
            ore_prezzi
        """,
        soluzione="""
            durata_prezzi = prezzi["timestamp"].max() - prezzi["timestamp"].min()
            ore_prezzi = durata_prezzi / pd.Timedelta("1h")
            ore_prezzi
        """,
        verifica="""
            assert ore_prezzi == 167, "❌ Dal lunedì alle 0:00 alla domenica alle 23:00 passano 167 ore: max meno min, diviso pd.Timedelta('1h')"
        """,
    )

    # ------------------------------------------------------------------ 7 (A)
    with nb.solo("avanzata"):
        nb.sezione("Cambiare passo: resample", intro="""
            `resample` cambia il passo di una serie: da quarti d'ora a ore, a giorni, a settimane. È un
            `groupby` sul tempo, e vuole il tempo nell'indice. Dopo il `resample` si dice cosa fare dei
            valori raggruppati: `mean()`, `sum()`, `max()`.
        """)
        nb.code("""
            mw = carico["Total Load [MW]"]
            orario = mw.resample("h").mean()
            orario.head()
        """)
        nb.md("""
            Attenzione a non confonderlo con il profilo orario. `resample("h")` risponde a "quanto valeva
            il carico in ogni singola ora dell'anno" (8784 valori); `groupby` sull'ora risponde a "quanto
            vale in media alle 8, alle 9, alle 10" (24 valori). Sull'indice l'ora si legge con `.hour`,
            senza `.dt`, che è per le colonne.
        """)
        nb.code("""
            profilo_carico = carico.groupby(carico.index.hour)["Total Load [MW]"].mean()
            profilo_carico.round(0)
        """)
        nb.md("""
            Da MW a MWh. Ogni riga è una potenza media su un quarto d'ora, quindi vale un quarto di MWh
            per MW: l'energia di un giorno è la somma dei 96 valori divisa per 4.
        """)
        nb.code("""
            energia_giorno = mw.resample("D").sum() / 4
            energia_giorno.head()
        """)
        nb.code("""
            print(f"Giorno di massimo consumo: {energia_giorno.idxmax():%d/%m/%Y}, {energia_giorno.max():,.0f} MWh")
            print(f"Giorno di minimo consumo:  {energia_giorno.idxmin():%d/%m/%Y}, {energia_giorno.min():,.0f} MWh")
        """)
        nb.md("""
            Il 17 luglio contro il primo gennaio: l'aria condizionata contro il giorno in cui il paese
            dorme. Il 31 marzo ha 92 quarti d'ora e il 27 ottobre ne avrebbe 100: la somma di quei due
            giorni è sbagliata di un'ora. Su un report annuale è rumore, su un bilancio orario no.
        """)
        nb.box("nota", """
            I passi si scrivono con sigle: `"15min"`, `"h"`, `"D"`, `"W"` (settimane che chiudono la
            domenica), `"ME"` (fine mese), `"YE"` (fine anno). Minuscole e maiuscole contano.
        """)

        # -------------------------------------------------------------- 8 (A)
        nb.sezione("Spostare e lisciare: shift e rolling", intro="""
            `shift(n)` sposta la serie di `n` righe, non di `n` ore: con il quartorario un'ora sono 4
            righe, un giorno 96, una settimana 672. Serve per mettere accanto "adesso" e "un'ora fa".
        """)
        nb.code("""
            confronto = pd.DataFrame({"mw": mw, "un_ora_prima": mw.shift(4)})
            confronto.head(6)
        """)
        nb.md("""
            I primi quattro valori spostati sono `NaN`: non esiste un'ora prima della prima. La
            variazione oraria è la differenza tra le due colonne, e `idxmax()` ci dice quando il carico è
            salito di più in un'ora.
        """)
        nb.code("""
            confronto["variazione"] = confronto["mw"] - confronto["un_ora_prima"]
            print(confronto["variazione"].idxmax(), round(confronto["variazione"].max()))
        """)
        nb.md("""
            Un giovedì di dicembre alle 6:45: si sveglia il Nord e accende tutto. Con 672 righe il
            confronto è con la settimana prima, stesso giorno e stessa ora.
        """)
        nb.code("""
            confronto["settimana_prima"] = mw.shift(4 * 24 * 7)
            confronto.loc["2024-01-08"].head(3)
        """)
        nb.md("""
            `rolling(96).mean()` è la media mobile sulle ultime 24 ore: per ogni riga, la media sua e
            delle 95 precedenti. La curva che ne esce segue il carico senza il su e giù della giornata.
            Anche qui, i primi 95 valori sono `NaN`.
        """)
        nb.code("""
            media_24h = mw.rolling(96).mean()
            media_24h.isna().sum()
        """)
        nb.code("""
            pd.DataFrame({"mw": mw, "media_24h": media_24h}).loc["2024-01-02"].head(4)
        """)
        nb.box("ricorda", """
            `shift` sposta, `rolling` liscia, e tutti e due contano righe: con un quartorario 1 ora = 4,
            1 giorno = 96, 1 settimana = 672. I `NaN` in testa sono normali: non c'è un prima del primo.
        """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="La settimana dei prezzi",
        scenario="""
            Il collega del trading ha ricevuto i prezzi zonali della settimana e vuole due cose: a che
            ora del giorno l'energia costa di più, in media, e perché "nel NORD mancano due righe". Finora
            apriva il CSV in Excel e contava a mano.
        """,
        richiesta="""
            1. Leggi `../Dati/prezzi_zonali_2025_settimana.csv` in `prezzi` e trasforma `timestamp` in data.
            2. Calcola il prezzo medio per ora del giorno su tutte le zone; metti in `ora_piu_cara` l'ora
               (un intero da 0 a 23) con la media più alta e in `prezzo_ora_piu_cara` quella media.
            3. Trova i due timestamp che mancano nella zona NORD e mettili nella lista `ore_mancanti`.
        """,
        suggerimento="Per il punto 3: NORD nell'indice ordinato, `asfreq(\"h\")`, poi le righe dove il prezzo è `NaN`.",
        starter="""
            prezzi = pd.read_csv("../Dati/prezzi_zonali_2025_settimana.csv")
            prezzi["timestamp"] = ...

            ora_piu_cara = ...
            prezzo_ora_piu_cara = ...

            ore_mancanti = ...
            print(ora_piu_cara, round(prezzo_ora_piu_cara, 2), ore_mancanti)
        """,
        soluzione="""
            prezzi = pd.read_csv("../Dati/prezzi_zonali_2025_settimana.csv")
            prezzi["timestamp"] = pd.to_datetime(prezzi["timestamp"])

            prezzi["ora"] = prezzi["timestamp"].dt.hour
            media_ora = prezzi.groupby("ora")["eur_mwh"].mean()
            ora_piu_cara = media_ora.idxmax()
            prezzo_ora_piu_cara = media_ora.max()

            mask_nord = prezzi["zona"] == "NORD"
            nord = prezzi[mask_nord].set_index("timestamp").sort_index()
            nord_completo = nord.asfreq("h")
            buchi = nord_completo["eur_mwh"].isna()
            ore_mancanti = list(nord_completo[buchi].index)
            print(ora_piu_cara, round(prezzo_ora_piu_cara, 2), ore_mancanti)
        """,
        verifica="""
            assert ora_piu_cara == 12, "❌ ora_piu_cara: raggruppa per ora del giorno (dt.hour), fai la media e prendi idxmax()"
            assert round(prezzo_ora_piu_cara, 2) == 129.09, "❌ prezzo_ora_piu_cara: è la media della fascia oraria più cara, su tutte le zone"
            assert len(ore_mancanti) == 2, "❌ ore_mancanti: devono essere esattamente due timestamp"
            assert sorted(ore_mancanti) == [pd.Timestamp("2025-06-04 14:00"), pd.Timestamp("2025-06-04 15:00")], "❌ ore_mancanti: sono le due ore del 4 giugno in cui il NORD non ha prezzo"
        """,
        perche="La media per ora del giorno è un `groupby` su una colonna creata con `.dt.hour`; i buchi si fanno emergere con `asfreq`, perché una riga che non c'è non si può filtrare.",
    )
    nb.esercizio(
        titolo="Il mese della turbina",
        bis=True,
        scenario="""
            La collega che segue l'eolico vuole la produzione mensile della turbina texana per la
            relazione annuale. Il file ha il timestamp senza anno e la potenza oraria in kW: su un passo
            orario, un kW medio per un'ora è un kWh.
        """,
        richiesta="""
            1. Leggi `../Dati/TexasTurbine.csv` in `turbina` e costruisci la colonna `timestamp` aggiungendo
               l'anno 2023 e dichiarando il formato.
            2. Calcola `produzione_mensile`: la somma della colonna `System power generated | (kW)` per mese.
            3. Metti in `mese_top` e `mese_min` il numero (1-12) del mese con la produzione più alta e più bassa.
        """,
        suggerimento="Una colonna `mese` con `.dt.month`, poi `groupby`. `idxmax()` e `idxmin()` danno l'etichetta, non il valore.",
        starter="""
            turbina = pd.read_csv("../Dati/TexasTurbine.csv")
            turbina["timestamp"] = ...

            produzione_mensile = ...
            mese_top = ...
            mese_min = ...
            print(mese_top, mese_min)
        """,
        soluzione="""
            turbina = pd.read_csv("../Dati/TexasTurbine.csv")
            turbina["timestamp"] = pd.to_datetime("2023 " + turbina["Time stamp"], format="%Y %b %d, %I:%M %p")

            turbina["mese"] = turbina["timestamp"].dt.month
            produzione_mensile = turbina.groupby("mese")["System power generated | (kW)"].sum()
            mese_top = produzione_mensile.idxmax()
            mese_min = produzione_mensile.idxmin()
            print(mese_top, mese_min)
        """,
        verifica="""
            assert len(produzione_mensile) == 12, "❌ produzione_mensile: un valore per mese, dodici in tutto"
            assert round(produzione_mensile.max()) == 932618, "❌ produzione_mensile: somma (non media) della potenza per mese"
            assert mese_top == 4, "❌ mese_top: il mese più ventoso è aprile; usa idxmax() sulla produzione mensile"
            assert mese_min == 9, "❌ mese_min: usa idxmin()"
        """,
    )
    nb.esercizio(
        titolo="Terna, ma pulita",
        scenario="""
            Il carico 2024 di Terna sta per entrare nel report mensile. Prima di aggregare qualunque cosa
            il responsabile vuole la risposta a una domanda sola: ogni giorno ha davvero 96 quarti d'ora?
            Il collega che controllava a occhio in Excel è in ferie.
        """,
        richiesta="""
            1. Leggi `../Dati/load_total_north_hourly_2024.xlsx` in `carico` e ordina le righe per `Date`.
            2. Conta i quarti d'ora di ogni giorno in `per_giorno` (una Series: giorno → numero di righe).
            3. Metti in `giorno_corto` il giorno con 92 righe e in `giorno_lungo` quello con 100.
            4. Togli i timestamp duplicati con `drop_duplicates(subset="Date")`, riassegna `carico` e
               metti in `n_righe_pulite` il numero di righe che restano.
        """,
        suggerimento="`.dt.date` toglie l'ora; `value_counts()` conta; `idxmin()` e `idxmax()` danno il giorno, non il conteggio.",
        starter="""
            carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
            carico = ...

            per_giorno = ...
            giorno_corto = ...
            giorno_lungo = ...

            carico = ...
            n_righe_pulite = ...
            print(giorno_corto, giorno_lungo, n_righe_pulite)
        """,
        soluzione="""
            carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
            carico = carico.sort_values("Date")

            per_giorno = carico["Date"].dt.date.value_counts()
            giorno_corto = per_giorno.idxmin()
            giorno_lungo = per_giorno.idxmax()

            carico = carico.drop_duplicates(subset="Date")
            n_righe_pulite = len(carico)
            print(giorno_corto, giorno_lungo, n_righe_pulite)
        """,
        verifica="""
            assert per_giorno.min() == 92 and per_giorno.max() == 100, "❌ per_giorno: conta le righe per giorno (dt.date + value_counts) prima di togliere i duplicati"
            assert str(giorno_corto)[:10] == "2024-03-31", "❌ giorno_corto: è l'ultima domenica di marzo, quella con 92 quarti d'ora"
            assert str(giorno_lungo)[:10] == "2024-10-27", "❌ giorno_lungo: è l'ultima domenica di ottobre, quella con 100"
            assert n_righe_pulite == 35132, "❌ n_righe_pulite: dopo drop_duplicates(subset='Date') restano 35136 - 4 righe"
        """,
        perche="Il conteggio per giorno va fatto prima di `drop_duplicates`, altrimenti il 27 ottobre torna a 96 e il problema sparisce dalla vista. Pulire e verificare sono due passi, in quest'ordine: verifica, poi pulisci.",
    )
    nb.esercizio(
        titolo="Il 2025, stessa storia",
        bis=True,
        scenario="""
            Arriva il file del 2025 e il responsabile chiede se ha gli stessi difetti di quello del 2024:
            l'ora legale non è cambiata, ma il file lo ha fatto un altro ufficio.
        """,
        richiesta="""
            1. Leggi `../Dati/load_total_north_hourly_2025.xlsx` in `carico_2025` e ordina per `Date`.
            2. Metti in `n_duplicati` quanti timestamp sono duplicati.
            3. Conta le righe per giorno in `per_giorno_2025` e metti in `giorni_anomali` la lista dei giorni che
               non hanno 96 righe.
            4. Togli i duplicati, riassegna `carico_2025` e metti in `n_righe_2025` le righe rimaste.
        """,
        suggerimento="Una maschera su `per_giorno_2025 != 96`, poi `.index` e `list(...)`.",
        starter="""
            carico_2025 = pd.read_excel("../Dati/load_total_north_hourly_2025.xlsx")
            carico_2025 = ...

            n_duplicati = ...
            per_giorno_2025 = ...
            giorni_anomali = ...

            carico_2025 = ...
            n_righe_2025 = ...
            print(n_duplicati, giorni_anomali, n_righe_2025)
        """,
        soluzione="""
            carico_2025 = pd.read_excel("../Dati/load_total_north_hourly_2025.xlsx")
            carico_2025 = carico_2025.sort_values("Date")

            n_duplicati = carico_2025["Date"].duplicated().sum()
            per_giorno_2025 = carico_2025["Date"].dt.date.value_counts()
            anomali = per_giorno_2025 != 96
            giorni_anomali = list(per_giorno_2025[anomali].index)

            carico_2025 = carico_2025.drop_duplicates(subset="Date")
            n_righe_2025 = len(carico_2025)
            print(n_duplicati, giorni_anomali, n_righe_2025)
        """,
        verifica="""
            assert n_duplicati == 4, "❌ n_duplicati: duplicated().sum() sulla colonna Date, prima di toglierli"
            assert sorted(str(g)[:10] for g in giorni_anomali) == ["2025-03-30", "2025-10-26"], "❌ giorni_anomali: sono le due domeniche del cambio d'ora del 2025"
            assert n_righe_2025 == 35036, "❌ n_righe_2025: 35040 righe meno i 4 duplicati"
        """,
    )
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="Profilo orario vs giornaliero",
            scenario="""
                Il report mensile vuole tre viste del carico 2024: la serie giornaliera, il profilo medio
                per ora del giorno e una curva liscia che faccia vedere la stagionalità senza il rumore
                dei singoli giorni. Tre domande diverse, tre strumenti diversi.
            """,
            richiesta="""
                Le prime righe rileggono e puliscono il carico 2024 e mettono il tempo nell'indice: sono già scritte.
                1. `giornaliero`: il carico medio di ogni giorno, in MW (`resample`).
                2. `profilo`: il carico medio per ora del giorno, 24 valori; metti in `ora_picco` l'ora con la media più alta.
                3. `media_mobile_sett`: la media mobile a una settimana (672 quarti d'ora) del carico quartorario;
                   metti in `n_nan` quanti `NaN` ha in testa.
            """,
            suggerimento="Sull'indice l'ora è `carico.index.hour`. Una settimana di quartorari sono 4 × 24 × 7 righe.",
            starter="""
                carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
                carico = carico.sort_values("Date").drop_duplicates(subset="Date")
                carico = carico.set_index("Date")
                mw = carico["Total Load [MW]"]

                giornaliero = ...
                profilo = ...
                ora_picco = ...
                media_mobile_sett = ...
                n_nan = ...
                print(len(giornaliero), ora_picco, n_nan)
            """,
            soluzione="""
                carico = pd.read_excel("../Dati/load_total_north_hourly_2024.xlsx")
                carico = carico.sort_values("Date").drop_duplicates(subset="Date")
                carico = carico.set_index("Date")
                mw = carico["Total Load [MW]"]

                giornaliero = mw.resample("D").mean()
                profilo = mw.groupby(carico.index.hour).mean()
                ora_picco = profilo.idxmax()
                media_mobile_sett = mw.rolling(4 * 24 * 7).mean()
                n_nan = media_mobile_sett.isna().sum()
                print(len(giornaliero), ora_picco, n_nan)
            """,
            verifica="""
                assert len(giornaliero) == 366, "❌ giornaliero: resample('D') su un anno bisestile dà 366 valori"
                assert round(giornaliero.max()) == 26869, "❌ giornaliero: media (non somma) per giorno"
                assert len(profilo) == 24 and ora_picco == 11, "❌ profilo: groupby sull'ora dell'indice, 24 valori; il picco medio è alle 11"
                assert n_nan == 671, "❌ media_mobile_sett: con rolling(672) i primi 671 valori sono NaN"
            """,
            perche="`resample` e `groupby` sull'ora rispondono a due domande diverse, e si chiamano quasi allo stesso modo: la differenza è se il tempo scorre (resample) o si piega su se stesso (groupby).",
            passo_in_piu=dict(
                testo="""
                    Qual è stata la settimana con il carico medio più alto del 2024? Usa `resample("W")`
                    (le settimane chiudono la domenica) sulla serie `mw`, metti in `settimana_top` l'etichetta
                    della settimana e in `carico_top` il suo carico medio.
                """,
                starter="""
                    settimanale = ...
                    settimana_top = ...
                    carico_top = ...
                    print(settimana_top, round(carico_top))
                """,
                soluzione="""
                    settimanale = mw.resample("W").mean()
                    settimana_top = settimanale.idxmax()
                    carico_top = settimanale.max()
                    print(settimana_top, round(carico_top))
                """,
                verifica="""
                    assert str(settimana_top)[:10] == "2024-07-21", "❌ settimana_top: la settimana che chiude domenica 21 luglio; usa idxmax() sulla media settimanale"
                    assert round(carico_top) == 24421, "❌ carico_top: la media (non la somma) di quella settimana, in MW"
                """,
            ),
        )
    return nb
