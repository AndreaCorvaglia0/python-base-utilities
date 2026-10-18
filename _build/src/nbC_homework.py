"""C · Homework: una settimana nell'ufficio Analisi Consumi."""

from nbkit import Notebook

EXCEL = "../../Dati/homework/clienti.xlsx"
DB = "../../Dati/homework/anagrafica.db"


def costruisci() -> Notebook:
    nb = Notebook(
        num="C",
        riserva=True,
        file="Homework",
        titolo="Homework: una settimana nell'ufficio Analisi Consumi",
        blocco=0,
        giornata=0,
        intento="L'homework ripercorre in mezz'ora i temi principali dei primi due moduli, in sei passi, uno per giorno della settimana, di cui due facoltativi.",
        obiettivi=[
            "usare liste, dizionari, cicli e funzioni su un caso di lavoro",
            "leggere un CSV italiano con pandas e trovare le righe anomale",
            "scegliere il foglio di un Excel e leggere una tabella di un database SQL",
        ],
        tempo=30,
        soluzioni_a_richiesta=True,
        dati=["homework/letture_marzo.csv", "homework/clienti.xlsx", "homework/anagrafica.db"],
        etichetta_esercizio="Passo",
        prefisso_esercizi="",
        prossimo="Le soluzioni le guardiamo insieme all'inizio del modulo 3.",
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Prima di cominciare", intro="""
        I file dell'homework si trovano nella cartella `../../Dati/homework/`, e la cella qui sotto ne mostra l'elenco.
        Se la lista risulta vuota, il percorso relativo non porta alla cartella giusta, di solito perché la cartella
        `Riserva` non è stata estratta dentro la cartella del corso, accanto a `Dati` e ai moduli.
    """)
    nb.code("""
        from pathlib import Path

        list(Path("../../Dati/homework").glob("*"))
    """)
    nb.md("""
        L'homework richiede circa mezz'ora e lo riprendiamo insieme all'inizio del modulo 3. Ogni passo comincia
        dicendo che cosa vogliamo ottenere e perché, e da lì si può arrivare al risultato da soli; chi preferisce
        procedere per gradi apre con un clic il blocco Passo per passo, e sotto i suggerimenti, anche loro nascosti,
        da leggere solo dopo aver provato. Nella cella da completare i `...` prendono il posto del codice da
        scrivere, e sotto ci sono la verifica, che stampa ✅ quando il risultato è giusto e altrimenti dice che cosa
        controllare, e la cella `soluzione`, che mostra la soluzione di quel passo e di nessun altro.
    """)
    nb.md("""
        I passi sono indipendenti, quindi chi si blocca su uno può passare al successivo, e i due segnati come
        facoltativi si fanno se resta tempo. Per ripassare si possono riaprire il notebook 02, nella cartella
        `Modulo_1`, per liste e dizionari, e i notebook 04 e 06, nella cartella `Modulo_2`, per cicli e funzioni e
        per CSV, Excel e SQL.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("La settimana", intro="""
        L'homework segue una settimana di lavoro nell'ufficio Analisi Consumi di una piccola società di vendita di
        energia, che gestisce otto POD di clienti business. Il collega che se ne occupava, facendo tutto a mano in
        Excel, è in ferie, e in sua assenza sbrighiamo con Python le richieste che arrivano ogni giorno. Un POD è il
        codice del punto di prelievo, nella forma `IT001E...`, e identifica un contatore; per questo un cliente con
        più sedi ha più POD.
    """)

    # Passo 1 · lunedì
    nb.esercizio(
        titolo="Lunedì: il consumo del panificio",
        suggerimenti=[
            "Il valore di un dizionario si legge scrivendo la chiave tra parentesi quadre dopo il nome del dizionario, e il costo è il prodotto tra il consumo e il prezzo.",
            "Il nome del cliente è `panificio[\"cliente\"]`, il consumo di febbraio sta sotto la chiave del mese, e `costo = kwh * prezzo`.",
        ],
        scenario="""
            Lunedì mattina il capo chiede quanto ha consumato a febbraio il Panificio Rè e quanto gli costa quel
            consumo al prezzo di listino di 0.21 euro/kWh. I dati del cliente sono già raccolti in un dizionario,
            quindi invece di ricopiarli a mano li leggiamo dalle sue chiavi e calcoliamo il costo con una
            moltiplicazione, in modo che la stessa cella funzioni anche con il dizionario di un altro cliente. La
            riga da mandare al capo è `Panificio Rè 1654.2 kWh a febbraio, costo 347.38 euro`.
        """,
        richiesta="""
            1. Salva in `cliente` il nome del cliente, con cui comincia la riga per il capo, e in `kwh` il consumo di
               febbraio, leggendoli dal dizionario `panificio` con le loro chiavi.
            2. Calcola in `costo` il consumo moltiplicato per `prezzo`.

            Il `print` già scritto nella cella compone la riga e arrotonda il costo al centesimo, quindi `costo` può
            restare con tutti i suoi decimali.
        """,
        starter="""
            panificio = {"cliente": "Panificio Rè", "pod": "IT001E31045201", "kwh_febbraio": 1654.2}
            prezzo = 0.21

            cliente = ...
            kwh = ...
            costo = ...
            print(cliente, kwh, "kWh a febbraio, costo", round(costo, 2), "euro")
        """,
        soluzione="""
            panificio = {"cliente": "Panificio Rè", "pod": "IT001E31045201", "kwh_febbraio": 1654.2}
            prezzo = 0.21

            cliente = panificio["cliente"]
            kwh = panificio["kwh_febbraio"]
            costo = kwh * prezzo
            print(cliente, kwh, "kWh a febbraio, costo", round(costo, 2), "euro")
        """,
        verifica="""
            assert cliente == "Panificio Rè", "❌ cliente: il valore della chiave 'cliente'"
            assert kwh == 1654.2, "❌ kwh: il valore della chiave 'kwh_febbraio'"
            assert round(costo, 2) == 347.38, "❌ costo: consumo per prezzo"
        """,
    )

    # Passo 2 · martedì
    nb.esercizio(
        titolo="Martedì: le 24 letture del panificio",
        facoltativo=True,
        scenario="""
            Martedì arrivano le 24 letture orarie del Panificio Rè del giorno prima, una per ogni ora da mezzanotte
            alle 23. Il titolare sostiene che quasi tutto il consumo dipenda dal forno, acceso dalle 4 alle 8, e per
            rispondergli calcoliamo la percentuale del consumo del giorno che cade in quelle ore e cerchiamo la
            lettura più alta, per vedere se il picco è del forno. Le letture sono già in una lista, quindi bastano
            uno slicing e due funzioni di Python, senza sommare a mano. Il forno pesa per il 57.0% e il picco è di
            11.2 kWh.
        """,
        richiesta="""
            1. Metti in `ore_forno` le cinque letture dalle 4 alle 8 comprese.
            2. Calcola `kwh_forno`, la loro somma, e `totale_giorno`, la somma di tutte le 24.
            3. Calcola `quota_forno`, cioè `kwh_forno / totale_giorno * 100`, arrotondata a un decimale con
               `round()`, perché nella risposta al titolare la percentuale si scrive con un solo decimale.
            4. Metti in `picco` la lettura più alta della giornata e controlla nella lista che cada in una delle ore
               del forno.
        """,
        suggerimenti=[
            "Le ore sono posizioni della lista, quindi un intervallo di ore è uno slicing; la somma e il massimo di una lista si ottengono con due funzioni di Python.",
            "La posizione nella lista coincide con l'ora, quindi `letture[4]` è la lettura delle 4; nello slicing l'indice finale è escluso, e servono `sum()` e `max()`.",
        ],
        starter="""
            letture = [0.8, 0.7, 0.9, 1.1, 9.5, 11.2, 10.8, 9.9, 8.4, 4.2, 3.9, 3.5,
                       3.1, 2.4, 2.0, 1.8, 2.2, 2.6, 2.9, 1.5, 1.2, 1.0, 0.9, 0.8]

            ore_forno = ...
            kwh_forno = ...
            totale_giorno = ...
            quota_forno = ...
            picco = ...
            print(f"Forno: {kwh_forno:.1f} kWh su {totale_giorno:.1f}, il {quota_forno}% (picco {picco} kWh)")
        """,
        soluzione="""
            letture = [0.8, 0.7, 0.9, 1.1, 9.5, 11.2, 10.8, 9.9, 8.4, 4.2, 3.9, 3.5,
                       3.1, 2.4, 2.0, 1.8, 2.2, 2.6, 2.9, 1.5, 1.2, 1.0, 0.9, 0.8]

            ore_forno = letture[4:9]
            kwh_forno = sum(ore_forno)
            totale_giorno = sum(letture)
            quota_forno = round(kwh_forno / totale_giorno * 100, 1)
            picco = max(letture)
            print(f"Forno: {kwh_forno:.1f} kWh su {totale_giorno:.1f}, il {quota_forno}% (picco {picco} kWh)")
        """,
        verifica="""
            assert ore_forno == [9.5, 11.2, 10.8, 9.9, 8.4], "❌ ore_forno: dalle 4 alle 8 comprese"
            assert quota_forno == 57.0, "❌ quota_forno: kwh_forno diviso totale_giorno, per 100, arrotondato a un decimale"
            assert picco == 11.2, "❌ picco: la lettura più alta, con max()"
        """,
    )

    # Passo 3 · mercoledì (ciclo in Base, comprehension in Avanzata)
    scenario_3 = """
        Mercoledì il commerciale chiede l'elenco dei POD che a febbraio hanno superato i 2000 kWh, e il capo vuole
        anche il consumo totale di tutti i POD. I consumi stanno nel dizionario lasciato dal collega in ferie, con il
        POD come chiave, e conviene scorrerlo con il codice invece di cercare a occhio, perché la stessa cella
        funziona con 8 POD come con 800 e, se il commerciale cambia la soglia, basta modificare un numero. I POD
        sopra la soglia sono tre, su 16244.1 kWh totali.
    """
    starter_3 = """
        consumi_febbraio = {
            "IT001E31045201": 1654.2,
            "IT001E31045877": 812.6,
            "IT001E31046310": 690.1,
            "IT001E31047092": 3310.4,
            "IT001E31047555": 431.8,
            "IT001E31048128": 4890.7,
            "IT001E31048743": 1178.3,
            "IT001E31049306": 3276.0,
        }
        soglia = 2000

        sopra_soglia = ...
        totale_kwh = ...
        print(f"{len(sopra_soglia)} POD sopra i {soglia} kWh, su {totale_kwh:.1f} kWh totali")
    """
    starter_3_base = starter_3.replace("""
        sopra_soglia = ...
        totale_kwh = ...
        """, """
        sopra_soglia = []
        for pod, kwh in ...:
            ...
        totale_kwh = ...
        """)
    verifica_3 = """
        assert sorted(sopra_soglia) == ["IT001E31047092", "IT001E31048128", "IT001E31049306"], "❌ sopra_soglia: i tre POD con più di 2000 kWh"
        assert round(totale_kwh, 1) == 16244.1, "❌ totale_kwh: la somma di tutti i valori del dizionario"
    """
    nb.esercizio(
        aula="base",
        titolo="Mercoledì: chi supera la soglia",
        scenario=scenario_3,
        richiesta="""
            1. Con un ciclo `for` su `consumi_febbraio.items()`, che a ogni giro dà un POD e il suo consumo, e un
               `if` che confronta il consumo con `soglia`, aggiungi alla lista `sopra_soglia` i POD che la superano.
            2. Calcola in `totale_kwh` la somma di tutti i consumi del dizionario.
        """,
        suggerimenti=[
            "Il ciclo passa su ogni coppia POD e consumo del dizionario, e dentro il ciclo una condizione decide se aggiungere il POD alla lista; il totale non ha bisogno del ciclo.",
            "Dentro il ciclo servono `if kwh > soglia:` e poi `.append(pod)`, mentre per il totale basta applicare `sum()` ai `.values()` del dizionario.",
        ],
        starter=starter_3_base,
        soluzione=starter_3_base.replace("""
        for pod, kwh in ...:
            ...
        totale_kwh = ...
        """, """
        for pod, kwh in consumi_febbraio.items():
            if kwh > soglia:
                sopra_soglia.append(pod)
        totale_kwh = sum(consumi_febbraio.values())
        """),
        verifica=verifica_3,
        perche="""
            Il ciclo scorre `.items()` perché a ogni giro servono sia la chiave sia il valore, cioè il POD da
            aggiungere alla lista e il consumo da confrontare con la soglia. Il totale non richiede un ciclo, dato che
            `sum()` lavora direttamente sui valori del dizionario.
        """,
    )
    nb.esercizio(
        aula="avanzata",
        titolo="Mercoledì: chi supera la soglia",
        scenario=scenario_3,
        richiesta="""
            1. Costruisci la lista `sopra_soglia` con una list comprehension su `consumi_febbraio.items()`, che tiene
               i POD con un consumo maggiore di `soglia`.
            2. Calcola in `totale_kwh` la somma di tutti i consumi del dizionario.
        """,
        suggerimenti=[
            "La forma è `[pod for pod, kwh in ... if ...]`, con la condizione in coda, mentre per il totale basta applicare `sum()` ai `.values()` del dizionario.",
        ],
        starter=starter_3,
        soluzione=starter_3.replace("""
        sopra_soglia = ...
        totale_kwh = ...
        """, """
        sopra_soglia = [pod for pod, kwh in consumi_febbraio.items() if kwh > soglia]
        totale_kwh = sum(consumi_febbraio.values())
        """),
        verifica=verifica_3,
        perche="""
            La list comprehension esprime in una riga lo stesso ciclo con `append` della versione estesa. Con una sola
            condizione resta facile da leggere, mentre con più condizioni o con calcoli intermedi conviene tornare al
            ciclo `for`.
        """,
    )

    # Passo 4 · giovedì (un argomento con default in più in Avanzata)
    scenario_4 = """
        Giovedì il capo chiede il costo di febbraio anche per altri clienti. Invece di copiare la riga di lunedì e
        cambiare i numeri a mano, come faceva il collega in ferie, scriviamo una funzione `costo` che riceve il
        consumo e il prezzo, con il listino di 0.21 euro/kWh come valore di default, e restituisce l'importo
        arrotondato al centesimo. In questo modo per i clienti a listino basta passare il consumo, mentre per chi ha
        un prezzo concordato, come la Serra Fiorita a 0.17 euro/kWh, si aggiunge il prezzo nella chiamata.
    """
    suggerimenti_4 = [
        "La funzione riceve i kWh e un prezzo con valore predefinito, calcola il prodotto, lo arrotonda e lo restituisce.",
        "`return` restituisce il valore a chi chiama la funzione, mentre `print` si limita a mostrarlo; la verifica ha bisogno del valore restituito.",
    ]
    nb.esercizio(
        aula="base",
        titolo="Giovedì: il conto diventa una funzione",
        scenario=scenario_4,
        richiesta="""
            1. Scrivi la funzione `costo(kwh, prezzo=0.21)`, che restituisce con `return` il consumo moltiplicato per
               il prezzo, arrotondato a due decimali con `round()` perché l'importo è in euro e centesimi.
            2. Sotto il `def` aggiungi una docstring di una riga, che il collega, al rientro dalle ferie, potrà
               leggere con `help(costo)` per sapere che cosa calcola la funzione.
            3. Usala per calcolare `costo_panificio`, il costo dei 1654.2 kWh del panificio al prezzo di listino, e
               `costo_serra`, il costo dei 3276.0 kWh della serra a 0.17 euro/kWh. Nella seconda chiamata scrivi
               `prezzo=0.17`, in modo che chi la rilegge capisca subito che quel numero è un prezzo.

            Alla fine `costo_panificio` vale 347.38 e `costo_serra` vale 556.92.
        """,
        suggerimenti=suggerimenti_4,
        starter="""
            def costo(kwh, prezzo=0.21):
                ...


            costo_panificio = ...
            costo_serra = ...
            print(f"Panificio: {costo_panificio} euro, Serra: {costo_serra} euro")
        """,
        soluzione='''
            def costo(kwh, prezzo=0.21):
                """Costo in euro di un consumo in kWh, arrotondato ai centesimi."""
                return round(kwh * prezzo, 2)


            costo_panificio = costo(1654.2)
            costo_serra = costo(3276.0, prezzo=0.17)
            print(f"Panificio: {costo_panificio} euro, Serra: {costo_serra} euro")
        ''',
        verifica="""
            assert costo(1000) == 210.0, "❌ costo(1000) deve dare 210.0: il prezzo di default è 0.21"
            assert costo(1000, prezzo=0.19) == 190.0, "❌ costo(1000, prezzo=0.19) deve dare 190.0: usa il prezzo ricevuto"
            assert costo_serra == 556.92, "❌ costo_serra: 3276.0 kWh a 0.17 euro/kWh"
        """,
        perche="""
            Con il prezzo di listino come default, la maggior parte delle chiamate passa soltanto il consumo, e se il
            listino cambia basta modificare la definizione della funzione. Anche l'arrotondamento sta dentro la
            funzione, così non occorre ripeterlo a ogni chiamata.
        """,
    )
    nb.esercizio(
        aula="avanzata",
        titolo="Giovedì: il conto diventa una funzione",
        scenario=scenario_4,
        richiesta="""
            1. Alcuni clienti, come il Bar Centrale, pagano anche una quota fissa mensile, quindi scrivi la funzione
               `costo(kwh, prezzo=0.21, quota_fissa=0.0)`, che restituisce con `return` il consumo per il prezzo più
               la quota fissa, arrotondato al centesimo.
            2. Aggiungi una docstring di una riga, che il collega, al rientro dalle ferie, potrà leggere con
               `help(costo)`.
            3. Usala per tre clienti, passando per nome gli argomenti diversi dal consumo, in modo che in ogni
               chiamata si legga quale valore cambia: `costo_panificio` per 1654.2 kWh con i valori di default,
               `costo_serra` per 3276.0 kWh a 0.17 euro/kWh e `costo_bar` per i 690.1 kWh del bar con 8 euro di
               quota fissa.

            Alla fine `costo_panificio` vale 347.38, `costo_serra` 556.92 e `costo_bar` 152.92.
        """,
        suggerimenti=suggerimenti_4[1:],
        starter="""
            def costo(kwh, prezzo=0.21, quota_fissa=0.0):
                ...


            costo_panificio = ...
            costo_serra = ...
            costo_bar = ...
            print(f"Panificio: {costo_panificio} euro, Serra: {costo_serra} euro, Bar: {costo_bar} euro")
        """,
        soluzione='''
            def costo(kwh, prezzo=0.21, quota_fissa=0.0):
                """Costo in euro di un consumo in kWh, più la quota fissa, arrotondato ai centesimi."""
                return round(kwh * prezzo + quota_fissa, 2)


            costo_panificio = costo(1654.2)
            costo_serra = costo(3276.0, prezzo=0.17)
            costo_bar = costo(690.1, quota_fissa=8)
            print(f"Panificio: {costo_panificio} euro, Serra: {costo_serra} euro, Bar: {costo_bar} euro")
        ''',
        verifica="""
            assert costo(1000) == 210.0, "❌ costo(1000) deve dare 210.0: il prezzo di default è 0.21 e la quota fissa 0"
            assert costo(1000, prezzo=0.19, quota_fissa=8) == 198.0, "❌ costo(1000, prezzo=0.19, quota_fissa=8) deve dare 198.0"
            assert costo_bar == 152.92, "❌ costo_bar: 690.1 kWh al prezzo di default, più 8 euro"
        """,
        perche="""
            Quando una funzione ha due parametri con un default, passare gli argomenti per nome rende esplicito quale
            dei due stiamo cambiando. Nella chiamata `costo(690.1, quota_fissa=8)`, per esempio, il prezzo resta quello
            di listino e cambia solo la quota fissa, mentre scrivendo `costo(690.1, 8)` l'8 finirebbe nel parametro
            `prezzo`.
        """,
    )

    # Passo 5 · venerdì
    nb.esercizio(
        titolo="Venerdì: il file del distributore",
        scenario="""
            Venerdì il distributore manda il CSV con le letture giornaliere di marzo degli otto POD, scritto
            all'italiana con il punto e virgola tra le colonne e la virgola nei decimali, e l'officina di Lecco
            segnala una bolletta di marzo tripla del solito. Una giornata normale resta sotto i 250 kWh, quindi con
            pandas cerchiamo tra le 248 righe quelle sopra i 500 e le salviamo in un CSV da girare al distributore per
            un controllo. L'unica riga anomala è dell'officina, POD `IT001E31047092`, con 1530.3 kWh il 12 marzo.
        """,
        richiesta="""
            1. Leggi `../../Dati/homework/letture_marzo.csv` in `letture`, indicando a `read_csv` il separatore delle
               colonne e quello dei decimali.
            2. Le istruzioni già scritte sotto la lettura mostrano le prime righe con `head()`, i tipi delle colonne con
               `info()` e le statistiche con `describe()`. Controlla che `kwh` sia `float64`, perché un numero letto
               come testo non si può confrontare con 500, e che il suo massimo sia molto sopra i 250 kWh.
            3. Scrivi in `mask` la condizione che confronta tutta la colonna `kwh` con 500. Il risultato ha un
               `True` o un `False` per ogni riga, e `letture[mask]`, già scritto nella cella, tiene in `anomale`
               soltanto le righe con `True`.
            4. Salva `anomale` nel file `letture_anomale.csv`, nella cartella del notebook, senza l'indice, perché
               il distributore lo apre in Excel e l'indice comparirebbe come una colonna in più senza nome.
        """,
        suggerimenti=[
            "Un CSV salvato da Excel in italiano usa un separatore di colonne e un separatore decimale diversi da quelli standard, e `read_csv` ha un parametro per ciascuno; la maschera confronta tutta la colonna con la soglia.",
            "Servono `sep=\";\"` e `decimal=\",\"`; se `kwh` risulta letta come testo, di solito manca il `decimal`. La maschera è `letture[\"kwh\"] > 500`.",
        ],
        starter="""
            import pandas as pd

            letture = pd.read_csv("../../Dati/homework/letture_marzo.csv", ...)
            letture.info()
            print(letture.head())
            print(letture.describe())

            mask = ...
            anomale = letture[mask]
            anomale.to_csv(...)
            anomale
        """,
        soluzione="""
            import pandas as pd

            letture = pd.read_csv("../../Dati/homework/letture_marzo.csv", sep=";", decimal=",")
            letture.info()
            print(letture.head())
            print(letture.describe())

            mask = letture["kwh"] > 500
            anomale = letture[mask]
            anomale.to_csv("letture_anomale.csv", index=False)
            anomale
        """,
        verifica="""
            assert letture["kwh"].dtype == "float64", "❌ letture: kwh deve essere numerica, controlla sep e decimal"
            assert list(anomale["pod"]) == ["IT001E31047092"], "❌ anomale: una riga sola, quella dell'officina, con kwh > 500"
            assert list(pd.read_csv("letture_anomale.csv").columns) == ["pod", "data", "kwh"], "❌ letture_anomale.csv: salva senza l'indice, con index=False"
        """,
        perche="""
            `info()` mostra subito se `kwh` è stata letta come numero, perché in quel caso il suo tipo è `float64`. La
            maschera e la selezione si scrivono spesso in una sola espressione, `letture[letture["kwh"] > 500]`, che
            tiene le stesse righe; tenerle separate, come qui, permette di guardare la maschera prima di usarla.
        """,
    )

    # Passo 6 · sabato, facoltativo (in Avanzata la lettura SQL sta in leggi_tabella)
    scenario_6 = """
        Sabato siamo di reperibilità e l'Officina Meccanica Fumagalli, che contesta la bolletta, chiede la potenza
        del suo contatore e i prezzi per fascia che le applichiamo. Il gestionale è spento, ma la potenza sta nella
        tabella `pod` del database dell'anagrafica e i prezzi nel foglio Listino dell'Excel dei clienti, e con pandas
        leggiamo da lì soltanto quello che serve, in poche righe che tornano utili alla prossima reperibilità. Il
        contatore dell'officina ha 30 kW e i prezzi sono di 0.21, 0.19 e 0.17 euro/kWh nelle fasce F1, F2 e F3.
    """
    nb.esercizio(
        aula="base",
        facoltativo=True,
        titolo="Sabato: la reperibilità",
        scenario=scenario_6,
        richiesta=f"""
            1. Leggi in `listino` il foglio `Listino` di `{EXCEL}`, indicandolo con `sheet_name`, perché senza
               questo parametro `read_excel` legge il primo foglio, che è l'anagrafica dei clienti.
            2. Apri `{DB}` con `sqlite3.connect` e leggi con `pd.read_sql` in `officina` la sola riga dell'officina
               della tabella `pod`, con un `WHERE` sulla colonna `cliente`. La riga `con.close()`, già scritta
               nella cella, chiude poi la connessione, che a quel punto non serve più.
        """,
        suggerimenti=[
            "Con `read_excel` il foglio si sceglie con `sheet_name`; con il database si apre la connessione, si legge con `read_sql` e si chiude la connessione.",
            "In SQL il testo va tra apici singoli: `WHERE cliente = 'Officina Meccanica Fumagalli'`.",
        ],
        starter=f"""
            import pandas as pd
            import sqlite3

            listino = pd.read_excel("{EXCEL}", sheet_name=...)

            con = sqlite3.connect("{DB}")
            officina = pd.read_sql("...", con)
            con.close()

            print(listino)
            officina
        """,
        soluzione=f"""
            import pandas as pd
            import sqlite3

            listino = pd.read_excel("{EXCEL}", sheet_name="Listino")

            con = sqlite3.connect("{DB}")
            officina = pd.read_sql("SELECT * FROM pod WHERE cliente = 'Officina Meccanica Fumagalli'", con)
            con.close()

            print(listino)
            officina
        """,
        verifica="""
            assert set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ listino: è il foglio Listino? Controlla sheet_name"
            assert list(officina["potenza_kw"]) == [30.0], "❌ officina: una riga sola, presa dalla tabella pod con il WHERE"
        """,
        perche="""
            Il filtro con `WHERE` viene eseguito dal database, che restituisce a pandas soltanto la riga richiesta. Con
            una tabella di otto righe la differenza non si nota, ma su tabelle grandi evita di caricare in memoria dati
            che non servono.
        """,
    )
    nb.esercizio(
        aula="avanzata",
        facoltativo=True,
        titolo="Sabato: la reperibilità",
        scenario=scenario_6,
        richiesta=f"""
            1. Leggi in `listino` il foglio `Listino` di `{EXCEL}`, scelto con `sheet_name`, perché il primo foglio
               del file è l'anagrafica dei clienti.
            2. Scrivi la funzione `leggi_tabella(nome)`, che apre `{DB}` con `sqlite3.connect`, legge tutta la
               tabella `nome` con `pd.read_sql`, chiude la connessione e restituisce il DataFrame, in modo che alla
               prossima reperibilità basti una riga per leggere una tabella senza lasciare aperta la connessione.
               Usala per mettere in `potenze` la tabella `pod`.
            3. In `officina` metti la sola riga dell'Officina Meccanica Fumagalli, filtrando `potenze` con una
               condizione sulla colonna `cliente`, come venerdì.
        """,
        suggerimenti=[
            "La funzione racchiude i tre passi del database, apertura, lettura e chiusura, e il nome ricevuto entra nella query con una f-string: `f\"SELECT * FROM {nome}\"`.",
        ],
        starter=f"""
            import pandas as pd
            import sqlite3


            def leggi_tabella(nome):
                ...


            listino = pd.read_excel("{EXCEL}", sheet_name=...)
            potenze = leggi_tabella("pod")
            officina = ...

            print(listino)
            officina
        """,
        soluzione=f'''
            import pandas as pd
            import sqlite3


            def leggi_tabella(nome):
                """Legge tutta la tabella `nome` da anagrafica.db e la restituisce come DataFrame."""
                con = sqlite3.connect("{DB}")
                df = pd.read_sql(f"SELECT * FROM {{nome}}", con)
                con.close()
                return df


            listino = pd.read_excel("{EXCEL}", sheet_name="Listino")
            potenze = leggi_tabella("pod")
            officina = potenze[potenze["cliente"] == "Officina Meccanica Fumagalli"]

            print(listino)
            officina
        ''',
        verifica="""
            assert set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ listino: è il foglio Listino? Controlla sheet_name"
            assert leggi_tabella("pod").shape == (8, 3), "❌ leggi_tabella: deve restituire tutta la tabella, 8 righe e 3 colonne"
            assert list(officina["potenza_kw"]) == [30.0], "❌ officina: una riga sola, quella dell'Officina Meccanica Fumagalli"
        """,
        perche="""
            La funzione raccoglie in un solo punto l'apertura della connessione, la lettura e la chiusura, così ogni
            chiamata chiude la connessione che ha aperto e nessuna resta aperta per dimenticanza. Il filtro
            sull'officina si applica invece in pandas, come venerdì, perché la tabella è già in memoria.
        """,
    )
    return nb
