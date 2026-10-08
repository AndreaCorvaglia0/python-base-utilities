"""C · Homework: una settimana nell'ufficio Analisi Consumi."""

from nbkit import Notebook

EXCEL = "../Dati/homework/clienti.xlsx"
DB = "../Dati/homework/anagrafica.db"


def costruisci() -> Notebook:
    nb = Notebook(
        num="C",
        file="Homework",
        titolo="Homework: una settimana nell'ufficio Analisi Consumi",
        blocco=0,
        giornata=0,
        intento="L'homework è diviso in sei passi, uno per ogni giorno della settimana, sugli argomenti della prima giornata; i primi cinque sono da svolgere e il sesto è facoltativo.",
        obiettivi=[
            "usare liste, dizionari, cicli e funzioni su un caso di lavoro",
            "leggere un CSV italiano con pandas e trovare le righe anomale",
            "leggere un Excel a due fogli e una tabella di un database SQL",
        ],
        tempo={"base": 40, "avanzata": 45},
        dati=["homework/letture_marzo.csv", "homework/clienti.xlsx", "homework/anagrafica.db"],
        etichetta_esercizio="Passo",
        prefisso_esercizi="",
        prossimo="Correggiamo insieme le soluzioni all'inizio della seconda giornata.",
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Prima di cominciare", intro="""
        I file dell'homework si trovano nella cartella `../Dati/homework/`, e la cella qui sotto ne mostra l'elenco.
        Se la lista risulta vuota, il percorso relativo non porta alla cartella giusta, di solito perché il notebook
        è stato spostato fuori da Aula_Base o Aula_Avanzata.
    """)
    nb.code("""
        from pathlib import Path

        list(Path("../Dati/homework").glob("*"))
    """)
    nb.md("""
        Ogni passo ha una cella da completare, in cui i `...` prendono il posto del codice da scrivere, seguita da
        una cella di verifica da eseguire senza modificarla. La verifica stampa ✅ quando il risultato è giusto e ❌,
        insieme a un'indicazione su cosa controllare, quando non lo è. Conviene svolgere i passi in ordine, perché
        alcuni riprendono il lavoro dei giorni precedenti. Per ripassare si possono riaprire il notebook
        [02](02_Tipi_di_dato.ipynb) per liste e dizionari, il [04](04_Funzioni_e_controllo.ipynb) per cicli e
        funzioni e il [06](06_Pandas_e_import_dati.ipynb) per CSV, Excel e SQL.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("La settimana", intro="""
        L'homework segue una settimana di lavoro nell'ufficio Analisi Consumi di una piccola società di vendita di
        energia, che gestisce otto POD di clienti business. Il collega che se ne occupava, facendo tutto a mano in
        Excel, è in ferie, e in sua assenza sbrighiamo con Python le richieste che arrivano ogni giorno. Un POD è il codice del punto
        di prelievo, nella forma `IT001E...`, e identifica un contatore; per questo un cliente con più sedi ha più POD.
    """)

    # Passo 1 · lunedì
    nb.esercizio(
        titolo="Lunedì: il consumo del panificio",
        scenario="""
            Lunedì mattina il capo chiede il consumo di febbraio del Panificio Rè e quanto gli costa al prezzo di
            listino, che è di 0.21 euro/kWh. I dati del cliente sono raccolti in un dizionario.
        """,
        richiesta="""
            Prendi dal dizionario `panificio` il nome del cliente, da salvare in `cliente`, e il consumo di febbraio,
            da salvare in `kwh`; poi calcola `costo`, cioè il consumo moltiplicato per `prezzo`. Se tutto è corretto,
            la cella stampa la riga `Panificio Rè 1654.2 kWh a febbraio, costo 347.38 euro`.
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
        scenario="""
            Martedì arrivano le 24 letture orarie del giorno prima del Panificio Rè, in kWh, una per ogni ora da
            mezzanotte alle 23. Il titolare sostiene che quasi tutto il consumo dipende dal forno, che resta acceso
            dalle 4 alle 8, e per verificarlo misuriamo quale quota del consumo giornaliero cade in quelle ore.
        """,
        richiesta="""
            1. Metti in `ore_forno` le cinque letture dalle 4 alle 8 comprese.
            2. Calcola `kwh_forno`, la loro somma, e `totale_giorno`, la somma di tutte le 24.
            3. Calcola `quota_forno`, il peso del forno sul totale in percentuale, arrotondato a un decimale.
            4. Metti in `picco` la lettura più alta della giornata.
        """,
        suggerimento="la posizione nella lista coincide con l'ora, quindi `letture[4]` è la lettura delle 4; ricorda che nello slicing l'indice finale è escluso.",
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
        Mercoledì si riparte dai consumi di febbraio degli otto POD, che il collega in ferie aveva lasciato in un
        dizionario. Il commerciale vuole la lista dei POD che superano i 2000 kWh al mese, e il capo vuole conoscere
        anche il consumo totale.
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
            Con un ciclo `for` su `consumi_febbraio.items()` e un `if`, costruisci la lista `sopra_soglia`
            con i POD che superano `soglia`. Calcola poi `totale_kwh`, la somma di tutti i consumi.
        """,
        suggerimento="dentro il ciclo servono `if kwh > soglia:` e poi `.append(pod)`, mentre per il totale basta applicare `sum()` ai `.values()` del dizionario.",
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
            Costruisci la lista `sopra_soglia` con i POD che superano `soglia` usando una list comprehension
            su `consumi_febbraio.items()`. Calcola poi `totale_kwh`, la somma di tutti i consumi.
        """,
        suggerimento="la forma è `[pod for pod, kwh in ... if ...]`, con la condizione in coda, mentre per il totale basta applicare `sum()` ai `.values()` del dizionario.",
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
        Giovedì il conto fatto lunedì va ripetuto per altri clienti. Il collega in ferie copiava la riga e cambiava
        i numeri a mano, mentre il collega senior suggerisce di scrivere una funzione che abbia il prezzo di listino
        come valore di default.
    """
    suggerimento_4 = "`return` restituisce il valore a chi chiama la funzione, mentre `print` si limita a mostrarlo; la verifica ha bisogno del valore restituito."
    nb.esercizio(
        aula="base",
        titolo="Giovedì: il conto diventa una funzione",
        scenario=scenario_4,
        richiesta="""
            1. Scrivi la funzione `costo(kwh, prezzo=0.21)`, con una docstring di una riga, che restituisce con `return` il costo in euro arrotondato a due decimali.
            2. Usala per calcolare `costo_panificio`, il costo di 1654.2 kWh al prezzo di default, e `costo_serra`, il costo di 3276.0 kWh a 0.17 euro/kWh, passando il prezzo per nome.
        """,
        suggerimento=suggerimento_4,
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
            1. Scrivi la funzione `costo(kwh, prezzo=0.21, quota_fissa=0.0)`, con una docstring di una riga, che restituisce con `return` il costo in euro, calcolato come consumo per prezzo più la quota fissa e arrotondato a due decimali.
            2. Usala per calcolare tre costi, passando per nome gli argomenti diversi dal consumo: `costo_panificio` per 1654.2 kWh con tutti i valori di default, `costo_serra` per 3276.0 kWh a 0.17 euro/kWh e `costo_bar` per 690.1 kWh con 8 euro di quota fissa.
        """,
        suggerimento=suggerimento_4,
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
            Venerdì arriva dal distributore il CSV con le letture giornaliere di marzo degli otto POD, che usa il punto
            e virgola come separatore e la virgola per i decimali. Nel frattempo l'officina di Lecco segnala che la sua
            bolletta di marzo è il triplo del solito.
        """,
        richiesta="""
            1. Leggi `../Dati/homework/letture_marzo.csv` in `letture` con i parametri adatti a un CSV italiano e guarda `info()`, `head()` e `describe()`, controllando che la colonna `kwh` sia numerica.
            2. Crea `mask`, la condizione che confronta tutta la colonna `kwh` con il valore 500, e poi `anomale = letture[mask]`, che contiene solo le righe in cui la condizione è vera.
            3. Salva `anomale` nel file `letture_anomale.csv`, nella cartella del notebook, senza l'indice.

            Lo stesso filtro si può scrivere anche in una sola espressione, `letture[letture["kwh"] > 500]`, che tiene solo le righe con `kwh` sopra 500.
        """,
        suggerimento="servono `sep=\";\"` e `decimal=\",\"`; se `kwh` risulta letta come testo, di solito manca il `decimal`.",
        starter="""
            import pandas as pd

            letture = pd.read_csv("../Dati/homework/letture_marzo.csv", ...)
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

            letture = pd.read_csv("../Dati/homework/letture_marzo.csv", sep=";", decimal=",")
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
            `info()` mostra subito se `kwh` è stata letta come numero, perché in quel caso il suo tipo è `float64`. Le
            letture normali di marzo restano sotto i 250 kWh al giorno, quindi la soglia di 500 lascia passare soltanto
            la lettura anomala dell'officina.
        """,
    )

    # Passo 6 · sabato, facoltativo (in Avanzata la lettura SQL sta in leggi_tabella)
    scenario_6 = """
        Sabato siamo di reperibilità. L'Officina Meccanica Fumagalli contesta la bolletta e chiede la potenza del suo
        contatore e i prezzi applicati, ma il gestionale è spento e restano a disposizione soltanto l'Excel dei clienti
        e il database con l'anagrafica dei POD.
    """
    nb.esercizio(
        aula="base",
        facoltativo=True,
        titolo="Sabato: la reperibilità",
        scenario=scenario_6,
        richiesta=f"""
            1. Leggi i due fogli di `{EXCEL}` in `anagrafica` e `listino`, con una chiamata a `read_excel` per ciascuno e il foglio scelto con `sheet_name`.
            2. Apri `{DB}` con `sqlite3.connect` e leggi con `pd.read_sql` tutta la tabella `pod` in `potenze` e la sola riga dell'officina in `officina`, usando un `WHERE` sulla colonna `cliente`; alla fine chiudi la connessione.
        """,
        suggerimento="in SQL il testo va tra apici singoli: `WHERE cliente = 'Officina Meccanica Fumagalli'`.",
        starter=f"""
            import sqlite3

            anagrafica = pd.read_excel("{EXCEL}", sheet_name=...)
            listino = pd.read_excel("{EXCEL}", sheet_name=...)

            con = sqlite3.connect("{DB}")
            potenze = pd.read_sql("...", con)
            officina = pd.read_sql("...", con)
            con.close()

            print(anagrafica)
            print(listino)
            officina
        """,
        soluzione=f"""
            import sqlite3

            anagrafica = pd.read_excel("{EXCEL}", sheet_name="Anagrafica")
            listino = pd.read_excel("{EXCEL}", sheet_name="Listino")

            con = sqlite3.connect("{DB}")
            potenze = pd.read_sql("SELECT * FROM pod", con)
            officina = pd.read_sql("SELECT * FROM pod WHERE cliente = 'Officina Meccanica Fumagalli'", con)
            con.close()

            print(anagrafica)
            print(listino)
            officina
        """,
        verifica="""
            assert list(anagrafica.columns) == ["pod", "cliente", "comune"], "❌ anagrafica: è il foglio Anagrafica? Controlla sheet_name"
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
            1. Leggi i due fogli di `{EXCEL}` in `anagrafica` e `listino`, con una chiamata a `read_excel` per ciascuno e il foglio scelto con `sheet_name`.
            2. Scrivi la funzione `leggi_tabella(nome)`, che apre `{DB}` con `sqlite3.connect`, legge tutta la tabella `nome` con `pd.read_sql`, chiude la connessione e restituisce il DataFrame; poi usala per mettere in `potenze` la tabella `pod`.
            3. In `officina` metti la sola riga dell'Officina Meccanica Fumagalli, filtrando `potenze` con una condizione sulla colonna `cliente`, come venerdì.
        """,
        suggerimento="la query con il nome ricevuto si compone con una f-string: `f\"SELECT * FROM {nome}\"`.",
        starter=f"""
            import sqlite3


            def leggi_tabella(nome):
                ...


            anagrafica = pd.read_excel("{EXCEL}", sheet_name=...)
            listino = pd.read_excel("{EXCEL}", sheet_name=...)
            potenze = leggi_tabella("pod")
            officina = ...

            print(anagrafica)
            print(listino)
            officina
        """,
        soluzione=f'''
            import sqlite3


            def leggi_tabella(nome):
                """Legge tutta la tabella `nome` da anagrafica.db e la restituisce come DataFrame."""
                con = sqlite3.connect("{DB}")
                df = pd.read_sql(f"SELECT * FROM {{nome}}", con)
                con.close()
                return df


            anagrafica = pd.read_excel("{EXCEL}", sheet_name="Anagrafica")
            listino = pd.read_excel("{EXCEL}", sheet_name="Listino")
            potenze = leggi_tabella("pod")
            officina = potenze[potenze["cliente"] == "Officina Meccanica Fumagalli"]

            print(anagrafica)
            print(listino)
            officina
        ''',
        verifica="""
            assert list(anagrafica.columns) == ["pod", "cliente", "comune"] and set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ anagrafica e listino: controlla sheet_name"
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
