"""C · Compito a casa: una settimana nell'ufficio Analisi Consumi."""

from nbkit import Notebook

EXCEL = "../Dati/compito/clienti.xlsx"
DB = "../Dati/compito/anagrafica.db"


def costruisci() -> Notebook:
    nb = Notebook(
        num="C",
        file="Compito_a_casa",
        titolo="Compito a casa: una settimana nell'ufficio Analisi Consumi",
        blocco=0,
        giornata=0,
        intento="Sei piccoli compiti, uno al giorno, come arrivano davvero in ufficio: niente di nuovo rispetto alla prima giornata, tutto da fare con le proprie mani.",
        obiettivi=[
            "rimettere in fila, su un caso di lavoro, f-string, liste, dizionari, cicli e funzioni",
            "leggere un CSV italiano, un Excel a due fogli e una tabella SQL con pandas, e controllare cosa è arrivato",
            "correggersi da soli con le celle di verifica, prima del confronto in aula",
        ],
        tempo={"base": 40, "avanzata": 45},
        dati=["compito/letture_marzo.csv", "compito/clienti.xlsx", "compito/anagrafica.db", "compito/letture_aprile.csv"],
        etichetta_esercizio="Passo",
        prefisso_esercizi="",
        prossimo="Le soluzioni le correggiamo insieme all'inizio della seconda giornata.",
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Prima di cominciare", intro="""
        Servono la cartella del corso aperta in VS Code con il kernel di `.venv`, come in aula, i quattro
        file in `../Dati/compito/` e tra i 30 e i 45 minuti di fila. I passi si parlano tra loro: meglio
        farli in ordine e in una sola seduta.
    """)
    nb.md("""
        La cella qui sotto elenca i file del compito. Se la lista è vuota, il notebook non sta leggendo
        dalla cartella giusta: controlla di aver aperto in VS Code la cartella del corso, non il singolo file.
    """)
    nb.code("""
        from pathlib import Path

        list(Path("../Dati/compito").glob("*"))
    """)
    nb.md("""
        Ogni passo ha una cella da completare, con `...` al posto del codice da scrivere, e subito sotto
        una cella di verifica da eseguire senza toccarla. Se stampa ✅ si passa al giorno dopo; se stampa ❌,
        il messaggio dice cosa controllare. I nomi delle variabili sono fissati nella richiesta: la verifica
        cerca quelli.
    """)
    nb.box("nota", """
        Se un passo non esce, il notebook da rileggere è a un clic: [02](02_Sintassi_di_base.ipynb) per le
        f-string, [03](03_Strutture_dati.ipynb) per liste e dizionari, [05](05_Condizioni_cicli_funzioni.ipynb)
        per cicli e funzioni, [07](07_Pandas_import_dati.ipynb) per CSV, Excel e SQL.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("La settimana", intro="""
        Ufficio Analisi Consumi di una piccola società di vendita: otto POD di clienti business, un capo
        che vuole le cose per ieri e un collega in ferie che faceva tutto a mano in Excel. Un POD è il
        codice del punto di prelievo (`IT001E...`): identifica il contatore, non il cliente. Sei passi, uno
        al giorno, sabato compreso.
    """)

    # Passo 1 · lunedì
    nb.esercizio(
        titolo="Lunedì: il messaggio per il capo",
        scenario="""
            Lunedì, 9:02. Il capo scrive in chat: «Mi mandi una riga con il consumo di febbraio del
            Panificio Rè e quanto gli costa al prezzo di listino? Poi la stessa riga per tutti gli altri,
            uguale uguale». La seconda parte è un problema di giovedì; oggi basta la riga.
        """,
        richiesta="""
            Calcola `costo` (consumo per prezzo) e costruisci `messaggio` con una f-string, in questo formato
            esatto: `Panificio Rè (IT001E31045201): 1654.2 kWh a febbraio, stimati 347.38 euro`. Il consumo
            con un decimale, il costo con due.
        """,
        suggerimento="`{valore:.1f}` è un decimale, `{valore:.2f}` sono due.",
        starter="""
            cliente = "Panificio Rè"
            pod = "IT001E31045201"
            kwh_febbraio = 1654.2
            prezzo = 0.21

            costo = ...
            messaggio = f"..."
            messaggio
        """,
        soluzione="""
            cliente = "Panificio Rè"
            pod = "IT001E31045201"
            kwh_febbraio = 1654.2
            prezzo = 0.21

            costo = kwh_febbraio * prezzo
            messaggio = f"{cliente} ({pod}): {kwh_febbraio:.1f} kWh a febbraio, stimati {costo:.2f} euro"
            messaggio
        """,
        verifica="""
            assert round(costo, 2) == 347.38, "❌ costo: consumo per prezzo"
            assert messaggio == "Panificio Rè (IT001E31045201): 1654.2 kWh a febbraio, stimati 347.38 euro", "❌ messaggio: controlla parentesi, decimali e spazi, deve essere identico all'esempio"
        """,
    )

    # Passo 2 · martedì
    nb.esercizio(
        titolo="Martedì: le 24 letture del panificio",
        scenario="""
            Martedì arrivano dal contatore del Panificio Rè le 24 letture orarie di ieri, in kWh, una per
            ora da mezzanotte alle 23. Il titolare sostiene che «è tutto il forno»: si accende alle 4 e
            lavora fino alle 8. Il capo vuole sapere se è vero, in percentuale.
        """,
        richiesta="""
            1. Metti in `ore_forno` le letture dalle 4 alle 8 comprese: sono cinque valori.
            2. Calcola `kwh_forno`, la loro somma, e `totale_giorno`, la somma di tutte le 24.
            3. Calcola `quota_forno`: quanto pesa il forno sul totale, in percentuale, arrotondata a un decimale.
            4. Metti in `picco` la lettura più alta della giornata.
        """,
        suggerimento="La posizione nella lista è l'ora, quindi `letture[4]` è la lettura delle 4; la fine dello slicing è esclusa.",
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
            assert ore_forno == [9.5, 11.2, 10.8, 9.9, 8.4], "❌ ore_forno: dalle 4 alle 8 comprese, la fine dello slicing è esclusa"
            assert round(kwh_forno, 1) == 49.8, "❌ kwh_forno: la somma delle letture del forno"
            assert round(totale_giorno, 1) == 87.3, "❌ totale_giorno: la somma di tutte le 24 letture"
            assert quota_forno == 57.0, "❌ quota_forno: kwh_forno diviso totale_giorno, per 100, arrotondato a un decimale"
            assert picco == 11.2, "❌ picco: la lettura più alta, con max()"
        """,
        perche="La fascia si somma sulla sottolista, non indice per indice: se domani il forno si accende alle 3 cambia un numero solo.",
    )

    # Passo 3 · mercoledì (cambia la cella: ciclo in Base, comprehension in Avanzata)
    scenario_3 = """
        Mercoledì. Il collega in ferie, prima di partire, aveva lasciato i consumi di febbraio degli
        otto POD, già sommati, in un dizionario. Il commerciale chiama chi supera i 2000 kWh al mese
        per proporre un altro contratto e vuole la lista; il capo vuole anche il totale.
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
    verifica_3 = """
        assert sorted(sopra_soglia) == ["IT001E31047092", "IT001E31048128", "IT001E31049306"], "❌ sopra_soglia: i tre POD con più di 2000 kWh, confronta il valore con >"
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
        suggerimento="Dentro il ciclo: `if kwh > soglia:` e poi `.append(pod)`. Per il totale, `sum()` sui `.values()`.",
        starter=starter_3,
        soluzione=starter_3.replace("""
        sopra_soglia = ...
        totale_kwh = ...
        """, """
        sopra_soglia = []
        for pod, kwh in consumi_febbraio.items():
            if kwh > soglia:
                sopra_soglia.append(pod)
        totale_kwh = sum(consumi_febbraio.values())
        """),
        verifica=verifica_3,
        perche="`.items()` dà chiave e valore insieme: serve il POD per la lista e il consumo per il confronto. Il totale non ha bisogno del ciclo: `sum()` sui valori basta.",
    )
    nb.esercizio(
        aula="avanzata",
        titolo="Mercoledì: chi supera la soglia",
        scenario=scenario_3,
        richiesta="""
            Costruisci la lista `sopra_soglia` con i POD che superano `soglia` usando una list comprehension
            su `consumi_febbraio.items()`. Calcola poi `totale_kwh`, la somma di tutti i consumi.
        """,
        suggerimento="`[pod for pod, kwh in ... if ...]`: la condizione va in coda. Per il totale, `sum()` sui `.values()`.",
        starter=starter_3,
        soluzione=starter_3.replace("""
        sopra_soglia = ...
        totale_kwh = ...
        """, """
        sopra_soglia = [pod for pod, kwh in consumi_febbraio.items() if kwh > soglia]
        totale_kwh = sum(consumi_febbraio.values())
        """),
        verifica=verifica_3,
        perche="La comprehension è il ciclo con `append` scritto in una riga: finché la condizione è una sola si legge d'un fiato, oltre conviene tornare al ciclo.",
    )

    # Passo 4 · giovedì (cambia la cella: un argomento keyword in più in Avanzata)
    scenario_4 = """
        Giovedì. Il conto di lunedì va rifatto per altri quattro clienti. Il collega in ferie copiava la
        riga e cambiava i numeri a mano, e una volta su tre il prezzo restava quello vecchio. Il collega
        senior, passando: «Fanne una funzione, e il prezzo mettilo come default: il listino cambia una volta
        l'anno».
    """
    suggerimento_4 = "`return` restituisce il valore a chi chiama, `print` lo mostra e basta: la verifica usa il valore."
    verifica_4 = """
        assert costo.__doc__, "❌ costo: manca la docstring, la riga tra virgolette triple sotto il def"
        assert costo(1000) == 210.0, "❌ costo(1000) deve dare 210.0: il prezzo di default è 0.21"
        assert costo(1000, prezzo=0.19) == 190.0, "❌ costo(1000, prezzo=0.19) deve dare 190.0: usa il prezzo ricevuto, non un numero fisso"
        assert costo_panificio == 347.38, "❌ costo_panificio: costo(1654.2), con il prezzo di default"
        assert costo_serra == 556.92, "❌ costo_serra: 3276.0 kWh a 0.17 euro/kWh"
    """
    verifica_4_avanzata = verifica_4 + """
        assert costo(1000, quota_fissa=8) == 218.0, "❌ costo(1000, quota_fissa=8) deve dare 218.0: la quota si somma dopo il prodotto"
        assert costo_bar == 152.92, "❌ costo_bar: 690.1 kWh al prezzo di default, più 8 euro"
    """
    nb.esercizio(
        aula="base",
        titolo="Giovedì: il conto diventa una funzione",
        scenario=scenario_4,
        richiesta="""
            1. Scrivi la funzione `costo(kwh, prezzo=0.21)` con una docstring di una riga: restituisce con `return` il costo in euro, arrotondato a due decimali.
            2. Usala per calcolare `costo_panificio` (1654.2 kWh al prezzo di default) e `costo_serra` (3276.0 kWh a 0.17 euro/kWh, passando il prezzo per nome).
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
        verifica=verifica_4,
        perche="`round` sta dentro la funzione: chi la chiama riceve sempre centesimi e non deve ricordarsi di arrotondare. Il prezzo come default si cambia in un posto solo.",
    )
    nb.esercizio(
        aula="avanzata",
        titolo="Giovedì: il conto diventa una funzione",
        scenario=scenario_4,
        richiesta="""
            1. Scrivi la funzione `costo(kwh, prezzo=0.21, quota_fissa=0.0)` con una docstring di una riga: restituisce con `return` il costo in euro, consumo per prezzo più la quota fissa, arrotondato a due decimali.
            2. Usala per calcolare `costo_panificio` (1654.2 kWh, tutto di default), `costo_serra` (3276.0 kWh a 0.17 euro/kWh) e `costo_bar` (690.1 kWh con 8 euro di quota fissa), passando gli argomenti per nome.
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
        verifica=verifica_4_avanzata,
        perche="`round` sta dentro la funzione: chi la chiama riceve sempre centesimi. Con due default, gli argomenti passati per nome dicono da soli quale stiamo cambiando.",
    )

    # Passo 5 · venerdì
    nb.esercizio(
        titolo="Venerdì: il file del distributore",
        scenario="""
            Venerdì arriva via mail il CSV del distributore: le letture giornaliere di marzo degli otto POD,
            separatore `;` e virgola decimale, come sempre. Il capo: «Dagli un'occhiata, l'officina di Lecco
            dice che la bolletta di marzo è il triplo del solito».
        """,
        richiesta="""
            1. Leggi `../Dati/compito/letture_marzo.csv` in `letture` con i parametri giusti per un CSV italiano, e guarda `info()`, `head()` e `describe()`: la colonna `kwh` deve essere numerica, e il massimo dice già qualcosa.
            2. Crea `mask`, la condizione «`kwh` sopra 500» su tutta la colonna, e `anomale = letture[mask]`: le righe in cui la condizione è vera.
            3. Salva `anomale` nel file `letture_anomale.csv`, nella cartella del notebook, senza l'indice.
        """,
        suggerimento="`sep=\";\"` e `decimal=\",\"`. Se `kwh` esce come testo, è il `decimal` che manca.",
        starter="""
            import pandas as pd

            letture = pd.read_csv("../Dati/compito/letture_marzo.csv", ...)
            letture.info()
            display(letture.head())
            display(letture.describe())

            mask = ...
            anomale = letture[mask]
            anomale.to_csv(...)
            anomale
        """,
        soluzione="""
            import pandas as pd

            letture = pd.read_csv("../Dati/compito/letture_marzo.csv", sep=";", decimal=",")
            letture.info()
            display(letture.head())
            display(letture.describe())

            mask = letture["kwh"] > 500
            anomale = letture[mask]
            anomale.to_csv("letture_anomale.csv", index=False)
            anomale
        """,
        verifica="""
            assert letture.shape == (248, 3), "❌ letture: 248 righe e 3 colonne, controlla sep=';'"
            assert letture["kwh"].dtype == "float64", "❌ letture: kwh deve essere numerica, controlla decimal=','"
            assert list(anomale["pod"]) == ["IT001E31047092"], "❌ anomale: una riga sola, quella dell'officina, con kwh > 500"
            assert list(anomale["data"]) == ["12/03/2025"], "❌ anomale: la lettura anomala è quella del 12 marzo"
            assert list(pd.read_csv("letture_anomale.csv").columns) == ["pod", "data", "kwh"], "❌ letture_anomale.csv: salva senza l'indice, con index=False"
            assert len(pd.read_csv("letture_anomale.csv")) == 1, "❌ letture_anomale.csv deve contenere solo la riga anomala"
        """,
        perche="`info()` risponde alla prima domanda prima ancora di guardare i numeri: se `kwh` compare come testo, il separatore decimale è sbagliato. Il filtro sopra 500 prende solo la lettura con lo zero di troppo: il massimo normale di marzo sta sotto i 250.",
    )

    # Passo 6 · sabato (cambia la cella: in Avanzata la lettura SQL sta in leggi_tabella)
    scenario_6 = """
        Sabato, reperibilità. Il customer care chiama: l'Officina Meccanica Fumagalli contesta la bolletta e
        chiede che potenza ha il suo contatore e a che prezzi la fatturiamo. Il gestionale è spento per
        manutenzione; tu hai l'Excel dei clienti e il database dell'anagrafica POD.
    """
    verifica_6 = """
        assert list(anagrafica.columns) == ["pod", "cliente", "comune"], "❌ anagrafica: è il foglio Anagrafica? Controlla sheet_name"
        assert set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ listino: è il foglio Listino? Controlla sheet_name"
        assert len(potenze) == 8 and "potenza_kw" in potenze.columns, "❌ potenze: tutta la tabella pod, SELECT * FROM pod"
        assert list(officina["pod"]) == ["IT001E31047092"], "❌ officina: una riga sola, quella dell'Officina Meccanica Fumagalli"
        assert list(officina["potenza_kw"]) == [30.0], "❌ officina: la potenza deve arrivare dalla tabella pod del database"
    """
    verifica_6_avanzata = verifica_6 + """
        assert leggi_tabella("pod").shape == (8, 3), "❌ leggi_tabella: deve restituire il DataFrame con tutta la tabella, 8 righe e 3 colonne"
    """
    nb.esercizio(
        aula="base",
        titolo="Sabato: la reperibilità",
        scenario=scenario_6,
        richiesta=f"""
            1. Leggi i due fogli di `{EXCEL}` in `anagrafica` e `listino`, uno per `read_excel`, scegliendo il foglio con `sheet_name`.
            2. Apri `{DB}` con `sqlite3.connect`, leggi in `potenze` tutta la tabella `pod` con `pd.read_sql` e in `officina` la sola riga dell'officina, con un `WHERE` sulla colonna `cliente`. Poi chiudi la connessione.
        """,
        suggerimento="In SQL il testo va tra apici singoli: `WHERE cliente = 'Officina Meccanica Fumagalli'`.",
        starter=f"""
            import sqlite3

            anagrafica = pd.read_excel("{EXCEL}", sheet_name=...)
            listino = pd.read_excel("{EXCEL}", sheet_name=...)

            con = sqlite3.connect("{DB}")
            potenze = pd.read_sql("...", con)
            officina = pd.read_sql("...", con)
            con.close()

            display(anagrafica)
            display(listino)
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

            display(anagrafica)
            display(listino)
            officina
        """,
        verifica=verifica_6,
        perche="Due `read_excel` con `sheet_name` sono la via più chiara per due fogli; con molti fogli conviene `sheet_name=None`, che li legge tutti in un dizionario. Il `WHERE` lo fa il database: arriva già la sola riga che serve.",
    )
    nb.esercizio(
        aula="avanzata",
        titolo="Sabato: la reperibilità",
        scenario=scenario_6,
        richiesta=f"""
            1. Leggi i due fogli di `{EXCEL}` in `anagrafica` e `listino`, uno per `read_excel`, scegliendo il foglio con `sheet_name`.
            2. Scrivi `leggi_tabella(nome)`: apre `{DB}` con `sqlite3.connect`, legge tutta la tabella `nome` con `pd.read_sql`, chiude la connessione e restituisce il DataFrame. Usala per mettere in `potenze` la tabella `pod`.
            3. In `officina` metti la sola riga dell'Officina Meccanica Fumagalli, filtrando `potenze` con una condizione sulla colonna `cliente`, come venerdì.
        """,
        suggerimento="La query con il nome ricevuto si compone con una f-string: `f\"SELECT * FROM {nome}\"`.",
        starter=f"""
            import sqlite3


            def leggi_tabella(nome):
                ...


            anagrafica = pd.read_excel("{EXCEL}", sheet_name=...)
            listino = pd.read_excel("{EXCEL}", sheet_name=...)
            potenze = leggi_tabella("pod")
            officina = ...

            display(anagrafica)
            display(listino)
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

            display(anagrafica)
            display(listino)
            officina
        ''',
        verifica=verifica_6_avanzata,
        perche="La funzione tiene insieme apri, leggi e chiudi: la connessione non resta aperta per sbaglio e il nome del file sta in un posto solo. Con un database aziendale cambia solo la riga del `connect`.",
    )

    # Passo 7 · domenica, facoltativo (+ un passo in più: glob e concat)
    nb.esercizio(
        titolo="Facoltativo: la classe di consumo",
        scenario="""
            Domenica. Nessuno ti ha chiesto niente, ma lunedì il commerciale vorrà sapere quali clienti sono
            piccoli, medi e grandi, e tu preferisci arrivare con la risposta pronta.
        """,
        richiesta="""
            1. Scrivi `classe_consumo(kwh)` che restituisce `"bassa"` sotto i 1000 kWh, `"media"` da 1000 a 3000 compresi, `"alta"` oltre i 3000, con `if`, `elif` ed `else`.
            2. Con un ciclo su `consumi_febbraio.items()` costruisci il dizionario `classi`: il POD come chiave, la classe come valore.
        """,
        suggerimento="Le condizioni si controllano in ordine: il primo `if` prende tutto quello che sta sotto 1000, l'`elif` può fermarsi a 3000.",
        starter="""
            def classe_consumo(kwh):
                ...


            classi = {}
            for pod, kwh in consumi_febbraio.items():
                ...
            classi
        """,
        soluzione='''
            def classe_consumo(kwh):
                """Classe di consumo mensile: bassa, media o alta."""
                if kwh < 1000:
                    return "bassa"
                elif kwh <= 3000:
                    return "media"
                else:
                    return "alta"


            classi = {}
            for pod, kwh in consumi_febbraio.items():
                classi[pod] = classe_consumo(kwh)
            classi
        ''',
        verifica="""
            assert classe_consumo(999.9) == "bassa", "❌ classe_consumo: sotto i 1000 è bassa"
            assert classe_consumo(1000) == "media" and classe_consumo(3000) == "media", "❌ classe_consumo: 1000 e 3000 sono compresi nella media"
            assert classe_consumo(3000.1) == "alta", "❌ classe_consumo: oltre i 3000 è alta"
            assert len(classi) == 8, "❌ classi: una voce per ogni POD del dizionario"
            assert classi["IT001E31048128"] == "alta" and classi["IT001E31045877"] == "bassa", "❌ classi: il valore è la classe restituita dalla funzione"
            assert list(classi.values()).count("media") == 2, "❌ classi: due POD sono in classe media"
        """,
        perche="L'`else` finale non ripete la condizione: se non è sotto 1000 e non è fino a 3000, è sopra. Tre rami, due confronti.",
        passo_in_piu=dict(
            testo="""
                Nella cartella c'è anche `letture_aprile.csv`, stesso formato. Con
                `Path("../Dati/compito").glob("letture_*.csv")` prendi tutti i file delle letture, leggili uno
                per uno in una lista di DataFrame e uniscili in `tutte` con `pd.concat(..., ignore_index=True)`.
                A fine anno, con dodici file, sarà lo stesso codice.
            """,
            starter="""
                from pathlib import Path

                tabelle = []
                for file in sorted(Path("../Dati/compito").glob("letture_*.csv")):
                    ...
                tutte = ...
                print(len(tutte))
            """,
            soluzione="""
                from pathlib import Path

                tabelle = []
                for file in sorted(Path("../Dati/compito").glob("letture_*.csv")):
                    tabelle.append(pd.read_csv(file, sep=";", decimal=","))
                tutte = pd.concat(tabelle, ignore_index=True)
                print(len(tutte))
            """,
            verifica="""
                assert len(tutte) == 488, "❌ tutte: 248 righe di marzo più 240 di aprile, controlla sep, decimal e che i file letti siano due"
                assert list(tutte.columns) == ["pod", "data", "kwh"], "❌ tutte: le colonne devono restare pod, data, kwh"
                assert len(set(tutte["pod"])) == 8, "❌ tutte: devono esserci tutti gli otto POD"
            """,
        ),
    )
    return nb
