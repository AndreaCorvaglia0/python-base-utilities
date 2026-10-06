"""08 · pandas: operazioni sui DataFrame."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="08",
        file="08_Pandas_operazioni",
        titolo="pandas: operazioni sui DataFrame",
        blocco=3,
        giornata=2,
        intento="Il grosso del lavoro di tutti i giorni: prendere le righe giuste, togliere quello che non serve, aggiungere quello che manca, raggruppare e incrociare con un'altra tabella.",
        obiettivi=[
            "selezionare righe e colonne con `loc`, `iloc` e i filtri",
            "pulire valori mancanti e duplicati e creare colonne nuove",
            "aggregare con `groupby` e unire tabelle con `merge` e `concat`",
        ],
        tempo={"base": 135, "avanzata": 115},
        dati=["letture_pod_2025.csv", "bolletta_esempio.xlsx", "utility.db", "U.S. Electricity Prices.csv"],
    )

    nb.code("""
        # librerie usate in questo notebook
        import sqlite3

        import pandas as pd
    """)

    # ------------------------------------------------------------------ 1
    nb.sezione("Selezionare", intro="""
        Ripartiamo dal file del fornitore del notebook precedente: le letture mensili di sei POD, per
        fascia. Lo leggiamo con i parametri che ci erano costati un errore a testa: separatore `;`,
        virgola decimale, encoding latin-1.
    """)
    nb.code("""
        letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
        letture.head()
    """)
    nb.md("""
        Prima domanda di ogni analisi: quali colonne ci servono. Una colonna tra parentesi quadre è
        una Series; una lista di colonne (doppie quadre) è un DataFrame più stretto.
    """)
    nb.code("""
        letture["kwh"].head()
    """)
    nb.code("""
        letture[["pod", "kwh"]].head()
    """)

    nb.sottosezione("Righe per etichetta: loc", intro="""
        Per prendere una riga per nome serve un indice parlante. L'anagrafica dei clienti, nel file
        Excel della bolletta, ha un POD per riga: con `set_index` lo mettiamo come indice.
    """)
    nb.code("""
        anagrafica = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Anagrafica")
        anagrafica_pod = anagrafica.set_index("pod")
        anagrafica_pod
    """)
    nb.md("""
        `pod` non è più una colonna: è l'indice, in grassetto a sinistra. Adesso `loc` prende una
        riga per etichetta, come CERCA.VERT prende una riga per chiave.
    """)
    nb.code("""
        anagrafica_pod.loc["IT001E45678901"]
    """)
    nb.md("""
        Con due argomenti, riga e colonna, `loc` restituisce il singolo valore. Con due liste, un
        pezzo di tabella.
    """)
    nb.code("""
        anagrafica_pod.loc["IT001E45678901", "cliente"]
    """)
    nb.code("""
        anagrafica_pod.loc[["IT001E12345678", "IT001E45678901"], ["cliente", "comune"]]
    """)
    nb.prova_tu(
        richiesta="""
            Da `anagrafica_pod`, leggi con `loc` il comune del POD `IT001E23456789` e salvalo in
            `comune_lavanderia`.
        """,
        starter="""
            comune_lavanderia = ...
            comune_lavanderia
        """,
        soluzione="""
            comune_lavanderia = anagrafica_pod.loc["IT001E23456789", "comune"]
            comune_lavanderia
        """,
        verifica="""
            assert comune_lavanderia == "Lodi", "❌ loc[etichetta della riga, nome della colonna]"
        """,
    )

    nb.sottosezione("Righe per posizione: iloc", intro="""
        `iloc` conta le righe da 0, come una lista, e ignora le etichette. Serve per sbirciare:
        la prima riga, le prime tre, l'ultima.
    """)
    nb.code("""
        letture.iloc[0]
    """)
    nb.code("""
        letture.iloc[0:3]
    """)
    nb.md("""
        Lo slicing è quello delle liste: fine esclusa, `-1` è l'ultima. La regola per scegliere:
        nome → `loc`, posizione → `iloc`. Quasi sempre vorremo `loc`, o un filtro.
    """)

    nb.sottosezione("Filtrare con una condizione", intro="""
        Un filtro è la condizione dell'`if`, applicata a tutta la colonna in un colpo. Il risultato è
        una Series di `True` e `False`, una per riga: la chiamiamo maschera.
    """)
    nb.code("""
        mask = letture["kwh"] > 1300
        mask.head()
    """)
    nb.md("""
        `sum()` su una maschera conta i `True`. E la maschera tra parentesi quadre tiene solo le
        righe `True`.
    """)
    nb.code("""
        mask.sum()
    """)
    nb.code("""
        letture[mask]
    """)
    nb.md("""
        Quattro letture sopra i 1300 kWh: tre dello Studio Dentistico, nei mesi freddi, e una del
        Panificio a luglio da 5785 kWh. Un panificio che a luglio consuma quattro volte un dentista
        in gennaio: teniamola d'occhio.
    """)
    nb.md("""
        Due condizioni si combinano con `&` (e) e `|` (oppure); `~` nega. Ogni condizione va tra
        parentesi.
    """)
    nb.code("""
        mask_f1_alte = (letture["fascia"] == "F1") & (letture["kwh"] > 1300)
        letture[mask_f1_alte]
    """)
    nb.box("attenzione", """
        Senza parentesi, `letture["fascia"] == "F1" & letture["kwh"] > 1300` dà un errore o un
        risultato sbagliato in silenzio: `&` ha la precedenza sui confronti. E in pandas si usano
        `&`, `|`, `~`, mai `and`, `or`, `not`: quelli funzionano su un `True` solo, non su una colonna.
    """)
    nb.code("""
        mask_f1 = letture["fascia"] == "F1"
        letture[~mask_f1].head(4)
    """)
    nb.md("""
        Quando i valori ammessi sono più di due, `.isin` con una lista evita una catena di `|`.
    """)
    nb.code("""
        mask_due_pod = letture["pod"].isin(["IT001E12345678", "IT001E45678901"])
        letture[mask_due_pod].head()
    """)
    nb.md("""
        La maschera va anche dentro `loc`, con il nome di una colonna: `loc[maschera, colonna]`
        legge solo quella colonna delle righe filtrate. Qui la media delle letture in F1.
    """)
    nb.code("""
        round(letture.loc[mask_f1, "kwh"].mean(), 1)
    """)
    nb.md("""
        Chi viene da SQL può scrivere la condizione come testo con `query`. Stesso risultato della
        maschera: lo mostriamo perché capita di trovarlo nel codice dei colleghi.
    """)
    nb.code("""
        letture.query("fascia == 'F1' and kwh > 1300")
    """)
    nb.prova_tu(
        richiesta="""
            Costruisci la maschera `mask_notte` per le letture in fascia F3 sopra i 700 kWh (due
            condizioni) e metti le righe filtrate in `notturne`. Quante sono?
        """,
        starter="""
            mask_notte = ...
            notturne = letture[mask_notte]
            notturne
        """,
        soluzione="""
            mask_notte = (letture["fascia"] == "F3") & (letture["kwh"] > 700)
            notturne = letture[mask_notte]
            notturne
        """,
        verifica="""
            assert len(notturne) == 3, "❌ Due condizioni tra parentesi, unite da &"
            assert set(notturne["fascia"]) == {"F3"}, "❌ Devono restare solo righe in fascia F3"
        """,
    )
    nb.box("ricorda", """
        - Nome → `loc`, posizione → `iloc`.
        - Filtro in due passi: prima la maschera, poi `df[mask]`.
        - Più condizioni: parentesi, `&`, `|`, `~`.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Pulire", intro="""
        I dati veri arrivano con buchi e doppioni. Partiamo da un contatore che per due giorni non ha
        trasmesso e che un giorno ha trasmesso due volte.
    """)
    nb.code("""
        contatore = pd.DataFrame({
            "giorno": ["2025-03-01", "2025-03-02", "2025-03-02", "2025-03-03", "2025-03-04", "2025-03-05", "2025-03-06"],
            "kwh": [12.3, 11.8, 11.8, None, 12.9, None, 13.4],
        })
        contatore
    """)
    nb.md("""
        `isna()` segna i valori mancanti (pandas li mostra come `NaN`); `.sum()` li conta per colonna.
        È la prima cosa da guardare dopo `info()`.
    """)
    nb.code("""
        contatore.isna().sum()
    """)
    nb.md("""
        Due strade: buttare le righe incomplete con `dropna`, o riempire i buchi con `fillna`.
        Dipende dalla domanda: per un totale mensile, un giorno a zero è un errore e un giorno alla
        mediana è una stima onesta.
    """)
    nb.code("""
        contatore.dropna()
    """)
    nb.code("""
        contatore["kwh"].fillna(0)
    """)
    nb.code("""
        mediana = contatore["kwh"].median()
        contatore["kwh"].fillna(mediana)
    """)
    nb.md("""
        Il risultato non si salva da solo. `dropna`, `fillna` e quasi tutti i metodi di pandas
        restituiscono una tabella nuova e lasciano l'originale com'è: `contatore` ha ancora i suoi
        due `NaN`.
    """)
    nb.code("""
        contatore.dropna()
        contatore
    """)
    nb.md("""
        Per tenere il risultato lo riassegniamo, alla stessa variabile o a una nuova.
    """)
    nb.code("""
        contatore["kwh"] = contatore["kwh"].fillna(mediana)
        contatore
    """)
    nb.md("""
        Doppioni: `duplicated()` segna con `True` la seconda copia di una riga identica,
        `drop_duplicates()` la toglie. Con `subset=["giorno"]` basta lo stesso giorno per dire
        "identica", anche se il resto della riga cambia.
    """)
    nb.code("""
        contatore.duplicated()
    """)
    nb.code("""
        contatore = contatore.drop_duplicates()
        contatore
    """)
    nb.md("""
        Su un file grande il metodo è lo stesso. I prezzi dell'elettricità negli Stati Uniti, 85 mila
        righe mensili per stato e settore, hanno la colonna `customers` vuota nei primi anni.
    """)
    nb.code("""
        prezzi = pd.read_csv("../Dati/U.S. Electricity Prices.csv")
        prezzi.isna().sum()
    """)
    nb.md("""
        `dropna(subset=[...])` butta una riga solo se manca quella colonna. Prima e dopo, `len`.
    """)
    nb.code("""
        prezzi_completi = prezzi.dropna(subset=["customers"])
        print(f"prima: {len(prezzi)} righe, dopo: {len(prezzi_completi)} righe")
    """)
    nb.prova_tu(
        richiesta="""
            Nel file dei prezzi la colonna `customers` (clienti serviti) manca nei primi anni. Crea
            `customers_pieni`: la colonna con i mancanti sostituiti da 0. Poi conta in `n_mancanti`
            quanti `NaN` restano.
        """,
        starter="""
            customers_pieni = ...
            n_mancanti = ...
            n_mancanti
        """,
        soluzione="""
            customers_pieni = prezzi["customers"].fillna(0)
            n_mancanti = customers_pieni.isna().sum()
            n_mancanti
        """,
        verifica="""
            assert n_mancanti == 0, "❌ Dopo fillna(0) non devono restare NaN"
            assert len(customers_pieni) == len(prezzi), "❌ fillna non toglie righe: la lunghezza resta quella"
            assert (customers_pieni == 0).sum() >= 26040, "❌ I 26040 mancanti devono essere diventati 0"
        """,
    )

    nb.sottosezione("Correggere un valore", intro="""
        Torniamo alle letture. Il customer care conferma: la lettura F1 di luglio del Panificio è
        stata digitata con uno zero in più. Va divisa per 10. Prima la maschera, poi la correzione.
    """)
    nb.code("""
        mask_errata = letture["kwh"] > 5000
        letture[mask_errata]
    """)
    nb.md("""
        Questa cella non dà errore ma avvisa, e non cambia nulla: `letture[mask_errata]` è una copia,
        e stiamo scrivendo sulla copia. Leggiamo l'avviso.
    """)
    nb.code("""
        letture[mask_errata]["kwh"] = letture[mask_errata]["kwh"] / 10
        letture["kwh"].max()
    """, errore=True)
    nb.md("""
        `ChainedAssignmentError`: due operazioni in catena (prima filtra, poi assegna) non arrivano
        mai all'originale. La forma giusta è una sola operazione, `loc[maschera, colonna] = valore`.
    """)
    nb.code("""
        letture.loc[mask_errata, "kwh"] = letture.loc[mask_errata, "kwh"] / 10
        letture["kwh"].max()
    """)
    nb.md("""
        Ora il massimo è 1434,9 kWh, lo Studio Dentistico a febbraio, e il Panificio a luglio è
        tornato a 578,5. Da qui in avanti lavoriamo sulle letture corrette.
    """)
    nb.box("ricorda", """
        - `isna().sum()` prima di tutto.
        - Il risultato non si salva da solo: `df = df.dropna()`.
        - Si scrive con `df.loc[mask, "col"] = valore`, mai con `df[mask]["col"]`.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Trasformare", intro="""
        Una colonna nuova si crea assegnando a un nome che non esiste ancora. Con l'aritmetica tra
        colonne pandas lavora riga per riga da solo, senza cicli.
    """)
    nb.code("""
        letture["mwh"] = letture["kwh"] / 1000
        letture.head(3)
    """)
    nb.md("""
        Per il costo serve il prezzo della fascia. `.map` con un dizionario traduce ogni fascia nel
        suo prezzo in €/kWh. Poi il prodotto, con `round` a due decimali.
    """)
    nb.code("""
        listino = {"F1": 0.21, "F2": 0.19, "F3": 0.17}

        letture["eur_kwh"] = letture["fascia"].map(listino)
        letture["costo"] = (letture["kwh"] * letture["eur_kwh"]).round(2)
        letture.head(3)
    """)
    nb.md("""
        Quando la regola è più di un conto, la scriviamo in una funzione e la applichiamo a ogni
        valore con `.apply`. Qui una classe di consumo con due soglie.
    """)
    nb.code('''
        def classe_consumo(kwh):
            """Classifica una lettura mensile in basso, medio o alto."""
            if kwh < 300:
                return "basso"
            elif kwh < 1000:
                return "medio"
            return "alto"


        letture["classe"] = letture["kwh"].apply(classe_consumo)
        letture[["pod", "kwh", "classe"]].head()
    ''')
    with nb.solo("avanzata"):
        nb.md("""
            Per una regola di una riga si può passare ad `apply` una `lambda`, senza dare un nome alla
            funzione. Qui il numero della fascia, letto dal secondo carattere di `F1`, `F2`, `F3`. Se la
            stessa cosa si fa con l'aritmetica tra colonne, meglio l'aritmetica: più veloce e più chiara.
        """)
        nb.code("""
            letture["fascia_num"] = letture["fascia"].apply(lambda f: int(f[1]))
            letture[["fascia", "fascia_num"]].head(3)
        """)
    nb.md("""
        Togliere una colonna: `drop(columns=[...])`. I MWh erano un esempio, non ci servono:
        via, riassegnando.
    """)
    nb.code("""
        letture = letture.drop(columns=["mwh"])
        letture.columns
    """)
    nb.md("""
        Il file dei prezzi americani ha i nomi delle colonne in inglese e in camelCase. `rename` con
        un dizionario da nome vecchio a nome nuovo li sistema; le colonne non nominate restano come sono.
    """)
    nb.code("""
        prezzi = prezzi.rename(columns={"stateDescription": "stato", "sectorName": "settore", "price": "prezzo"})
        prezzi.head(3)
    """)
    nb.md("""
        `date` è testo, `2001-01-01` (le date vere arrivano nel prossimo notebook). I primi quattro
        caratteri sono l'anno: `.str` applica a tutta la colonna le operazioni delle stringhe, e
        `astype(int)` cambia il tipo da testo a numero intero.
    """)
    nb.code("""
        prezzi["anno"] = prezzi["date"].str[:4].astype(int)
        prezzi[["date", "anno"]].dtypes
    """)
    with nb.solo("avanzata"):
        nb.md("""
            Con `.str` anche la `fascia_num` di prima si fa senza `lambda`:
            `letture["fascia"].str[1].astype(int)`. Quando nel codice di un agente troviamo
            `.apply(lambda ...)`, controlliamo se esiste già l'operazione su colonna.
        """)
    nb.md("""
        `sort_values` ordina per una colonna, `ascending=False` dal più grande. Con una lista di
        colonne ordina per la prima e, a pari merito, per la seconda.
    """)
    nb.code("""
        letture.sort_values("kwh", ascending=False).head()
    """)
    nb.md("""
        `set_index` e `reset_index` sono l'andata e il ritorno: una colonna diventa indice, l'indice
        torna colonna. Lo rivedremo subito con `groupby`, che mette la chiave nell'indice.
    """)
    nb.code("""
        anagrafica_pod.reset_index().head(3)
    """)
    nb.md("""
        Dopo un ordinamento l'indice resta in disordine (183, 180, 213...). `reset_index(drop=True)` lo
        riparte da 0 e scarta il vecchio; senza `drop=True` il vecchio indice diventerebbe una colonna
        `index`.
    """)
    nb.code("""
        ordinate = letture.sort_values("kwh", ascending=False).reset_index(drop=True)
        ordinate.head(3)
    """)
    nb.prova_tu(
        richiesta="""
            Aggiungi ad `anagrafica` la colonna `provincia` con `.map` e il dizionario `sigle`
            (da comune a sigla).
        """,
        starter="""
            sigle = {"Monza": "MB", "Lodi": "LO", "Cremona": "CR", "Cantù": "CO", "Lecco": "LC", "Varese": "VA"}

            anagrafica["provincia"] = ...
            anagrafica
        """,
        soluzione="""
            sigle = {"Monza": "MB", "Lodi": "LO", "Cremona": "CR", "Cantù": "CO", "Lecco": "LC", "Varese": "VA"}

            anagrafica["provincia"] = anagrafica["comune"].map(sigle)
            anagrafica
        """,
        verifica="""
            assert list(anagrafica["provincia"]) == ["MB", "LO", "CR", "CO", "LC", "VA"], "❌ map va chiamato sulla colonna comune, con il dizionario sigle"
        """,
    )
    nb.box("ricorda", """
        - Colonna nuova: `df["nuova"] = espressione sulle colonne`.
        - Dizionario → `.map`; funzione → `.apply`.
        - `rename`, `drop`, `sort_values` restituiscono una tabella nuova: riassegna.
        - `reset_index(drop=True)` dopo `sort_values`: indice da 0, senza colonna `index`.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Aggregare", intro="""
        La domanda tipica è un totale per qualcosa: per POD, per fascia, per mese. In Excel è una
        tabella pivot; in pandas è `groupby`: dividi per chiave, calcola, rimetti insieme.
    """)
    nb.code("""
        totale_pod = letture.groupby("pod")["kwh"].sum()
        totale_pod
    """)
    nb.md("""
        Il risultato è una Series: i POD sono finiti nell'indice e la colonna `pod` è sparita. Per
        riavere una tabella normale, con `pod` come colonna, `reset_index()`. Lo faremo quasi sempre.
    """)
    nb.code("""
        tabella_pod = totale_pod.reset_index()
        tabella_pod
    """)
    nb.md("""
        Più statistiche in un colpo: `.agg` con la lista dei nomi.
    """)
    nb.code("""
        statistiche_pod = letture.groupby("pod")["kwh"].agg(["mean", "max"])
        statistiche_pod.round(1)
    """)
    nb.md("""
        Due chiavi: la lista dentro `groupby`. Il totale per POD e fascia.
    """)
    nb.code("""
        per_fascia = letture.groupby(["pod", "fascia"])["kwh"].sum()
        per_fascia.reset_index().head(6)
    """)
    nb.md("""
        Chi consuma di più? `idxmax` restituisce l'etichetta dell'indice dove sta il massimo: per
        questo lo chiamiamo sulla Series, prima di `reset_index`.
    """)
    nb.code("""
        totale_pod.idxmax()
    """)
    nb.md("""
        Sulla colonna di un DataFrame, `idxmax` dà l'etichetta della riga, che poi leggiamo con `loc`.
    """)
    nb.code("""
        posizione = letture["kwh"].idxmax()
        letture.loc[posizione, ["pod", "data", "fascia", "kwh"]]
    """)
    nb.md("""
        La pivot di Excel esiste anche qui: `pivot_table` con righe, colonne, valore e funzione.
        Stessi numeri del `groupby` a due chiavi, disposti in griglia.
    """)
    nb.code("""
        letture.pivot_table(index="pod", columns="fascia", values="kwh", aggfunc="sum").round(1)
    """)
    nb.md("""
        Per contare quante volte compare ogni valore c'è `value_counts`: la risposta a "quanti ne ho
        per tipo". Sulle classi di consumo e, nel file grande, sui settori.
    """)
    nb.code("""
        letture["classe"].value_counts()
    """)
    nb.code("""
        prezzi["settore"].value_counts()
    """)
    nb.md("""
        Con 85 mila righe `groupby` fa lo stesso lavoro senza battere ciglio: il prezzo medio
        (centesimi di dollaro al kWh) per settore e anno.
    """)
    nb.code("""
        prezzo_settore_anno = prezzi.groupby(["settore", "anno"])["prezzo"].mean()
        prezzo_settore_anno.reset_index().head()
    """)
    nb.prova_tu(
        richiesta="""
            Calcola la Series `costo_cliente`: il totale della colonna `costo` di `letture` per
            `cliente` (senza `reset_index`, ci serve l'indice). Poi metti in `cliente_top` il cliente
            che spende di più.
        """,
        starter="""
            costo_cliente = ...
            cliente_top = ...
            print(cliente_top)
            costo_cliente.round(2)
        """,
        soluzione="""
            costo_cliente = letture.groupby("cliente")["costo"].sum()
            cliente_top = costo_cliente.idxmax()
            print(cliente_top)
            costo_cliente.round(2)
        """,
        verifica="""
            assert len(costo_cliente) == 6, "❌ Un totale per ciascuno dei sei clienti"
            assert round(costo_cliente.sum(), 2) == 25083.22, "❌ Somma la colonna costo, non kwh"
            assert cliente_top == "Studio Dentistico Colombo", "❌ cliente_top: idxmax sulla Series"
        """,
    )
    with nb.solo("avanzata"):
        nb.md("""
            `groupby(...).transform("median")` calcola la statistica per gruppo ma la restituisce lunga
            quanto la tabella di partenza, un valore per riga: così ogni lettura si confronta con la
            mediana del suo POD, senza merge.
        """)
        nb.code("""
            mediana_pod = letture.groupby("pod")["kwh"].transform("median")
            letture["rapporto"] = (letture["kwh"] / mediana_pod).round(2)
            letture.sort_values("rapporto", ascending=False).head(3)
        """)
        nb.md("""
            Il massimo è 2: il Panificio a gennaio in F1, un inverno normale. Prima della correzione di
            luglio la lettura sballata dava 9,3: un rapporto così alto salta subito all'occhio.
        """)
        nb.md("""
            `.agg` accetta anche la forma con nome: `nome_nuovo=(colonna, funzione)`. È quella che
            scrive di solito Copilot, e si legge così: il nome della colonna di arrivo, poi la colonna
            di partenza e la funzione da applicare. Qui una riga per POD con massimo e mediana, già
            etichettati.
        """)
        nb.code("""
            letture.groupby("pod").agg(massimo=("kwh", "max"), mediana=("kwh", "median"))
        """)
    nb.box("ricorda", """
        - `groupby(chiave)[colonna].funzione()`, poi `reset_index()`.
        - `idxmax` prima di `reset_index`: vuole l'etichetta.
        - `value_counts` per contare, `pivot_table` per la griglia.
    """, aula="base")
    with nb.solo("avanzata"):
        nb.box("ricorda", """
            - `groupby(chiave)[colonna].funzione()`, poi `reset_index()`.
            - `idxmax` prima di `reset_index`: vuole l'etichetta.
            - `value_counts` per contare, `pivot_table` per la griglia.
            - `transform` restituisce un valore per riga; `.agg(nome=(col, fn))` dà il nome alla colonna.
        """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Unire", intro="""
        Le informazioni stanno quasi sempre in due tabelle: i consumi da una parte, l'anagrafica
        dall'altra. `merge` le incrocia su una colonna in comune: un CERCA.VERT che porta tutte le
        colonne in una volta.
    """)
    nb.md("""
        Il foglio Consumi ha i kWh per POD e mese ma non dice chi è il cliente; l'Anagrafica sì.
        Prima del merge contiamo le righe di entrambi.
    """)
    nb.code("""
        consumi = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Consumi")
        print(f"consumi: {len(consumi)} righe, anagrafica: {len(anagrafica)} righe")
        consumi.head(3)
    """)
    nb.code("""
        consumi_clienti = pd.merge(consumi, anagrafica, on="pod", how="left")
        print(f"dopo il merge: {len(consumi_clienti)} righe")
        consumi_clienti.head(3)
    """)
    nb.md("""
        `on` è la colonna in comune. `how="left"` dice: tieni tutte le righe della tabella di
        sinistra e cerca la corrispondenza a destra; chi non la trova resta, con `NaN` nelle colonne
        nuove. È il comportamento di CERCA.VERT, e il più usato.
    """)
    nb.md("""
        Vediamolo su una tabella piccola: tre offerte commerciali, una delle quali per un POD che
        non è nostro. `how="inner"` tiene solo le corrispondenze, `how="outer"` tiene tutto da
        entrambe le parti. Con `indicator=True` la colonna `_merge` dice da dove viene ogni riga: è
        il modo più rapido per trovare chi è rimasto senza corrispondenza.
    """)
    nb.code("""
        offerte = pd.DataFrame({
            "pod": ["IT001E12345678", "IT001E45678901", "IT001E99999999"],
            "sconto_pct": [5, 10, 7],
        })
        tutto = pd.merge(anagrafica, offerte, on="pod", how="outer", indicator=True)
        tutto[["pod", "cliente", "sconto_pct", "_merge"]]
    """)
    nb.code("""
        mask_senza_offerta = tutto["_merge"] == "left_only"
        tutto[mask_senza_offerta]
    """)
    nb.md("""
        Dal database: 20 clienti e 30 POD, legati da `id_cliente`. Un cliente può avere più POD, e
        dopo il merge le righe saranno più di 20. Non è un errore, è la risposta giusta; ma va
        previsto, perciò si conta prima e dopo.
    """)
    nb.code("""
        con = sqlite3.connect("../Dati/utility.db")
        clienti_db = pd.read_sql("SELECT * FROM clienti", con)
        pod_db = pd.read_sql("SELECT * FROM pod", con)
        con.close()
        print(f"clienti: {len(clienti_db)} righe, pod: {len(pod_db)} righe")
    """)
    nb.code("""
        clienti_pod = pd.merge(clienti_db, pod_db, on="id_cliente", how="left")
        print(f"dopo il merge: {len(clienti_pod)} righe")
        clienti_pod.head()
    """)
    nb.box("attenzione", """
        Se la chiave non è unica nella tabella di destra, le righe si moltiplicano: 20 clienti
        diventano 34 righe perché alcuni hanno più POD. Se dopo un merge le righe aumentano senza un
        motivo, la chiave va controllata con `duplicated()` prima di andare avanti.
    """)
    nb.prova_tu(
        richiesta="""
            Fai il merge al contrario: `pod_db` a sinistra, `clienti_db` a destra, su `id_cliente`,
            `how="left"`, in `pod_clienti`. Quante righe ti aspetti?
        """,
        starter="""
            pod_clienti = ...
            print(len(pod_clienti))
            pod_clienti.head()
        """,
        soluzione="""
            pod_clienti = pd.merge(pod_db, clienti_db, on="id_cliente", how="left")
            print(len(pod_clienti))
            pod_clienti.head()
        """,
        verifica="""
            assert len(pod_clienti) == 30, "❌ Ogni POD ha un solo cliente: le righe restano 30"
            assert "ragione_sociale" in pod_clienti.columns, "❌ Dopo il merge devono esserci le colonne di clienti_db"
            assert pod_clienti["ragione_sociale"].isna().sum() == 0, "❌ Tutti i POD devono aver trovato il loro cliente"
        """,
    )

    nb.sottosezione("Impilare tabelle: concat", intro="""
        `concat` mette una tabella sotto l'altra: stesse colonne, più righe. È il caso dei file
        mensili dello stesso fornitore, o dei clienti nuovi che arrivano dal commerciale.
        `ignore_index=True` rinumera le righe da 0.
    """)
    nb.code("""
        nuovi_clienti = pd.DataFrame({
            "pod": ["IT001E78901234", "IT001E89012345"],
            "cliente": ["Gelateria Polo Nord", "Palestra Olimpo"],
            "comune": ["Como", "Bergamo"],
        })
        anagrafica_completa = pd.concat([anagrafica, nuovi_clienti], ignore_index=True)
        anagrafica_completa
    """)
    nb.md("""
        Se una delle due tabelle ha una colonna in più, le righe dell'altra la ricevono vuota
        (`NaN`): `concat` allinea per nome di colonna, non per posizione.
    """)
    nb.box("nota", """
        `merge` e `concat` lavorano sulle colonne. Esiste anche `df.join(altro)`, che unisce
        sull'indice: capita di incontrarlo nel codice degli altri, ma `merge` fa lo stesso lavoro e si
        legge meglio.
    """)
    nb.box("ricorda", """
        - Prima e dopo il merge: `len()`.
        - `how="left"` è il CERCA.VERT; `indicator=True` per vedere chi resta senza corrispondenza.
        - `concat` per impilare, `merge` per incrociare.
        - Le operazioni di Excel con il loro nome in pandas, in una pagina: [scheda Excel → pandas](../Schede/Scheda_Excel_pandas.md).
    """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Data Wrangler", intro="""
        Data Wrangler è un'estensione di VS Code che mostra un DataFrame come un foglio di calcolo e
        traduce i clic in codice pandas. Serve per esplorare in fretta e per imparare: ogni
        operazione fatta con il mouse mostra la riga di pandas che la fa.
    """)
    nb.md("""
        Si apre da un DataFrame già in memoria. Dopo aver eseguito una cella che lo mostra, sotto
        l'output compare il pulsante **Open 'letture' in Data Wrangler** (il nome tra apici è quello
        della variabile); in alternativa, nel pannello
        **Variables** della barra del notebook, ogni DataFrame ha l'icona di Data Wrangler accanto.
    """)
    nb.md("""
        Dentro: in alto le colonne con un riassunto (distribuzione, mancanti), a destra la lista dei
        passi fatti, in basso il codice che li produce. Le operazioni si scelgono dal pannello
        **Operations** a sinistra, che compare solo in **Editing mode**: all'apertura Data Wrangler è
        in sola lettura (Viewing mode), si cambia con il pulsante in alto a destra.
    """)
    nb.md("""
        Proviamone due: **Filter** sulla colonna `fascia` uguale a `F1`, poi **Drop columns** su
        `cliente`. Ogni passo si vede in anteprima e si può annullare.
    """)
    nb.md("""
        Il pulsante **Export to notebook** incolla nel notebook una cella come questa: una funzione
        con i passi, applicata a una copia del DataFrame.
    """)
    nb.code("""
        # codice incollato da Data Wrangler: i commenti in inglese sono suoi
        def clean_data(letture):
            # Filter rows based on column: 'fascia'
            letture = letture[letture["fascia"] == "F1"]
            # Drop column: 'cliente'
            letture = letture.drop(columns=["cliente"])
            return letture


        letture_clean = clean_data(letture.copy())
        letture_clean.head()
    """)
    nb.md("""
        Leggiamolo: è lo stesso pandas di questo notebook, con maschera e filtro sulla stessa riga e
        `.copy()` per non toccare l'originale. Data Wrangler è un buon modo per scoprire il metodo
        che non ricordiamo; il codice che produce va letto, e se serve accorciato.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il POD con la lettura sballata",
        scenario="""
            Il fornitore ha rimandato il file delle letture, quello grezzo. Il controllo qualità è stanco
            di cercare a occhio la lettura digitata male e vuole una procedura che la trovi da sola:
            quella che, in fascia F1, è fuori scala rispetto alle altre letture dello stesso POD.
        """,
        richiesta="""
            1. Rileggi `../Dati/letture_pod_2025.csv` in `letture` (separatore, encoding e decimale
               giusti) e tieni in `f1` solo le righe della fascia F1.
            2. Calcola `statistiche`: per ogni POD il massimo e la mediana di `kwh`, con `groupby` e
               `.agg(["max", "median"])`.
            3. Aggiungi a `statistiche` la colonna `rapporto`: massimo diviso mediana.
            4. Metti in `pod_anomalo` il POD con il rapporto più alto e in `mese_anomalo` la `data`
               della riga di `f1` con il `kwh` più alto.
        """,
        suggerimento="`idxmax` su una colonna di `f1` dà l'etichetta della riga; con `loc` leggi la sua `data`.",
        starter="""
            letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=..., decimal=..., encoding=...)
            mask_f1 = ...
            f1 = letture[mask_f1]

            statistiche = ...
            statistiche["rapporto"] = ...

            pod_anomalo = ...
            mese_anomalo = ...
            print(f"POD {pod_anomalo}, lettura del {mese_anomalo}")
            statistiche.round(2)
        """,
        soluzione="""
            letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
            mask_f1 = letture["fascia"] == "F1"
            f1 = letture[mask_f1]

            statistiche = f1.groupby("pod")["kwh"].agg(["max", "median"])
            statistiche["rapporto"] = statistiche["max"] / statistiche["median"]

            pod_anomalo = statistiche["rapporto"].idxmax()
            mese_anomalo = f1.loc[f1["kwh"].idxmax(), "data"]
            print(f"POD {pod_anomalo}, lettura del {mese_anomalo}")
            statistiche.round(2)
        """,
        verifica="""
            assert len(f1) == 72, "❌ f1 deve contenere solo le 72 righe della fascia F1"
            assert round(statistiche["rapporto"].max(), 1) == 6.5, "❌ rapporto: massimo diviso mediana, per POD"
            assert pod_anomalo == "IT001E45678901", "❌ pod_anomalo: idxmax sulla colonna rapporto"
            assert mese_anomalo == "01/07/2025", "❌ mese_anomalo: la data della riga di f1 con il kwh massimo"
        """,
        perche="La mediana non si lascia trascinare dal valore sbagliato, la media sì: il rapporto con la mediana isola l'anomalia (6,5 contro 1,2-1,4 degli altri POD).",
    )
    nb.esercizio(
        titolo="I prezzi del Texas",
        bis=True,
        scenario="""
            Il commerciale prepara un confronto internazionale e vuole sapere come è cambiato il
            prezzo residenziale in Texas, anno per anno. Il file è quello dei prezzi americani: 85 mila
            righe, prezzi in centesimi di dollaro al kWh.
        """,
        richiesta="""
            1. Leggi `../Dati/U.S. Electricity Prices.csv` in `prezzi` e crea la colonna `anno`
               (numero intero) dai primi quattro caratteri di `date`.
            2. Tieni in `texas` le righe con `stateDescription` uguale a `Texas` e `sectorName`
               uguale a `residential`.
            3. Calcola la Series `prezzo_anno`: media di `price` per `anno`, senza `reset_index`.
            4. Metti in `anno_max` l'anno con il prezzo medio più alto e in `prezzo_max` quel prezzo,
               arrotondato a due decimali.
        """,
        suggerimento="Due condizioni, tra parentesi, unite da `&`. Il massimo di una Series è `.max()`, la sua etichetta `.idxmax()`.",
        starter="""
            prezzi = pd.read_csv("../Dati/U.S. Electricity Prices.csv")
            prezzi["anno"] = ...

            mask_texas = ...
            texas = prezzi[mask_texas]

            prezzo_anno = ...
            anno_max = ...
            prezzo_max = ...
            print(f"Anno più caro: {anno_max} ({prezzo_max} cent/kWh)")
            prezzo_anno.round(2)
        """,
        soluzione="""
            prezzi = pd.read_csv("../Dati/U.S. Electricity Prices.csv")
            prezzi["anno"] = prezzi["date"].str[:4].astype(int)

            mask_texas = (prezzi["stateDescription"] == "Texas") & (prezzi["sectorName"] == "residential")
            texas = prezzi[mask_texas]

            prezzo_anno = texas.groupby("anno")["price"].mean()
            anno_max = prezzo_anno.idxmax()
            prezzo_max = round(prezzo_anno.max(), 2)
            print(f"Anno più caro: {anno_max} ({prezzo_max} cent/kWh)")
            prezzo_anno.round(2)
        """,
        verifica="""
            assert len(texas) == 277, "❌ texas: stato Texas e settore residential, due condizioni con &"
            assert len(prezzo_anno) == 24, "❌ prezzo_anno: una media per ciascuno dei 24 anni"
            assert anno_max == 2023, "❌ anno_max: idxmax sulla Series prezzo_anno"
            assert prezzo_max == 14.37, "❌ prezzo_max: il massimo di prezzo_anno, con due decimali"
        """,
        perche="L'anno estratto con `.str[:4]` e convertito in intero basta per raggruppare; le date vere arrivano nel prossimo notebook.",
        passo_in_piu=dict(
            testo="""
                Il commerciale ora vuole tutti gli stati: una griglia stato × anno con il prezzo medio
                residenziale. Riparti da `prezzi` con la colonna `anno`: tieni in `residenziale` il
                settore `residential`, poi costruisci `tabella` con `pivot_table` (`index="stateDescription"`,
                `columns="anno"`, `values="price"`, `aggfunc="mean"`), arrotondata a due decimali.
                Infine `stato_piu_caro_2024`: lo stato con il prezzo più alto nella colonna `2024`.
            """,
            starter="""
                mask_res = ...
                residenziale = prezzi[mask_res]

                tabella = ...
                stato_piu_caro_2024 = ...
                print(stato_piu_caro_2024)
                tabella.head()
            """,
            soluzione="""
                mask_res = prezzi["sectorName"] == "residential"
                residenziale = prezzi[mask_res]

                tabella = residenziale.pivot_table(index="stateDescription", columns="anno", values="price", aggfunc="mean").round(2)
                stato_piu_caro_2024 = tabella[2024].idxmax()
                print(stato_piu_caro_2024)
                tabella.head()
            """,
            verifica="""
                assert tabella.shape == (62, 24), "❌ tabella: 62 stati in riga, 24 anni in colonna"
                assert round(tabella.loc["Hawaii", 2024], 2) == 44.28, "❌ tabella: media di price, con anno intero in colonna"
                assert stato_piu_caro_2024 == "Hawaii", "❌ stato_piu_caro_2024: idxmax sulla colonna 2024 della tabella"
            """,
        ),
    )
    nb.esercizio(
        titolo="Bolletta per cliente",
        scenario="""
            Fine anno: la fatturazione vuole, per ogni cliente, il costo dell'energia 2025 a partire
            dai tre fogli di `bolletta_esempio.xlsx`. Consumi ha i kWh per POD e mese, una colonna per
            fascia; Listino i prezzi per fascia; Anagrafica chi è il cliente. Oggi lo fa un collega
            con tre CERCA.VERT e una pivot, e il risultato deve finire in un Excel.
        """,
        richiesta="""
            1. Leggi i tre fogli in `consumi`, `listino`, `anagrafica`.
            2. Metti `fascia` come indice del listino e leggi con `loc` i tre prezzi `p_f1`, `p_f2`,
               `p_f3`.
            3. Aggiungi a `consumi` la colonna `costo`: `F1` per `p_f1`, più `F2` per `p_f2`, più `F3`
               per `p_f3`.
            4. Calcola `costo_pod`: il totale di `costo` per POD, arrotondato a due decimali, con
               `reset_index`.
            5. Unisci `costo_pod` con `anagrafica` in `bolletta` (merge su `pod`, `how="left"`),
               stampando `len` prima e dopo.
            6. Salva `bolletta` in `bolletta_2025.xlsx` nella cartella del notebook, senza indice.
        """,
        suggerimento="`sheet_name=None` legge tutti i fogli in un dizionario; `to_excel(nome, index=False)` scrive il file.",
        starter="""
            fogli = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name=None)
            consumi = fogli["Consumi"]
            listino = fogli["Listino"]
            anagrafica = fogli["Anagrafica"]

            listino_fascia = ...
            p_f1 = ...
            p_f2 = ...
            p_f3 = ...

            consumi["costo"] = ...
            costo_pod = ...

            print(f"prima: {len(costo_pod)} righe")
            bolletta = ...
            print(f"dopo: {len(bolletta)} righe")
            bolletta.to_excel(...)
            bolletta
        """,
        soluzione="""
            fogli = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name=None)
            consumi = fogli["Consumi"]
            listino = fogli["Listino"]
            anagrafica = fogli["Anagrafica"]

            listino_fascia = listino.set_index("fascia")
            p_f1 = listino_fascia.loc["F1", "eur_kwh"]
            p_f2 = listino_fascia.loc["F2", "eur_kwh"]
            p_f3 = listino_fascia.loc["F3", "eur_kwh"]

            consumi["costo"] = consumi["F1"] * p_f1 + consumi["F2"] * p_f2 + consumi["F3"] * p_f3
            costo_pod = consumi.groupby("pod")["costo"].sum()
            costo_pod = costo_pod.round(2).reset_index()

            print(f"prima: {len(costo_pod)} righe")
            bolletta = pd.merge(costo_pod, anagrafica, on="pod", how="left")
            print(f"dopo: {len(bolletta)} righe")
            bolletta.to_excel("bolletta_2025.xlsx", index=False)
            bolletta
        """,
        verifica="""
            assert len(bolletta) == 6, "❌ bolletta: una riga per POD, sei POD"
            assert abs(bolletta["costo"].sum() - 17874.13) < 0.05, "❌ costo: F1*p_f1 + F2*p_f2 + F3*p_f3, totale per POD arrotondato a due decimali"
            assert "cliente" in bolletta.columns, "❌ bolletta: dopo il merge deve avere la colonna cliente dell'anagrafica"
            assert len(pd.read_excel("bolletta_2025.xlsx")) == 6, "❌ Il file bolletta_2025.xlsx deve avere sei righe"
        """,
        perche="Il listino ha tre righe: metterle nell'indice e leggerle con `loc` è più chiaro di un merge su una tabella larga. Il merge serve dove serve, per attaccare l'anagrafica.",
    )
    nb.esercizio(
        titolo="Clienti senza letture",
        bis=True,
        scenario="""
            Il customer care ha venti clienti nel database e il sospetto che per alcuni non arrivi
            nessuna lettura. Nel database le letture sono per POD, e i POD sono legati al cliente da
            `id_cliente`: due salti. Serve l'elenco dei clienti senza nemmeno una lettura a marzo.
        """,
        richiesta="""
            1. Leggi dal database `../Dati/utility.db` le tre tabelle in `clienti_db`, `pod_db`,
               `letture_db` e chiudi la connessione.
            2. Unisci `letture_db` con `pod_db` su `pod` (`how="left"`) in `letture_pod`: ogni lettura
               acquista il suo `id_cliente`. Controlla `len` prima e dopo.
            3. Calcola `kwh_cliente`: totale di `kwh` per `id_cliente`, con `reset_index`.
            4. Unisci `clienti_db` con `kwh_cliente` su `id_cliente`, `how="left"` e `indicator=True`,
               in `clienti_kwh`; tieni in `senza_letture` le righe con `_merge` uguale a `left_only`.
        """,
        suggerimento="Il merge con `indicator=True` aggiunge la colonna `_merge`: filtrala con una maschera come qualunque altra colonna.",
        starter="""
            con = sqlite3.connect("../Dati/utility.db")
            clienti_db = pd.read_sql("SELECT * FROM clienti", con)
            pod_db = ...
            letture_db = ...
            con.close()

            letture_pod = ...
            print(f"letture: {len(letture_db)} righe, dopo il merge: {len(letture_pod)} righe")

            kwh_cliente = ...
            clienti_kwh = ...
            mask_senza = ...
            senza_letture = clienti_kwh[mask_senza]
            senza_letture
        """,
        soluzione="""
            con = sqlite3.connect("../Dati/utility.db")
            clienti_db = pd.read_sql("SELECT * FROM clienti", con)
            pod_db = pd.read_sql("SELECT * FROM pod", con)
            letture_db = pd.read_sql("SELECT * FROM letture", con)
            con.close()

            letture_pod = pd.merge(letture_db, pod_db, on="pod", how="left")
            print(f"letture: {len(letture_db)} righe, dopo il merge: {len(letture_pod)} righe")

            kwh_cliente = letture_pod.groupby("id_cliente")["kwh"].sum()
            kwh_cliente = kwh_cliente.reset_index()
            clienti_kwh = pd.merge(clienti_db, kwh_cliente, on="id_cliente", how="left", indicator=True)
            mask_senza = clienti_kwh["_merge"] == "left_only"
            senza_letture = clienti_kwh[mask_senza]
            senza_letture
        """,
        verifica="""
            assert len(letture_pod) == 930, "❌ letture_pod: ogni POD ha un solo cliente, le 930 letture restano 930"
            assert len(clienti_kwh) == 20, "❌ clienti_kwh: how='left' da clienti_db tiene tutti i 20 clienti"
            assert len(senza_letture) == 4, "❌ senza_letture: le righe con _merge uguale a left_only"
            assert set(senza_letture["ragione_sociale"]) == {"Panificio Rossi", "Lavanderia Splendor", "Pasticceria Dolce Vita", "Serra Fiorita"}, "❌ Controlla la direzione del merge: clienti_db a sinistra"
        """,
        perche="Il totale per cliente si calcola prima del merge con l'anagrafica: così la tabella finale ha una riga per cliente e `left_only` significa davvero \"nessuna lettura\".",
    )
    return nb
