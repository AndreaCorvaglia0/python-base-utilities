"""01 · Librerie e ambiente."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="01",
        file="01_Librerie_e_ambiente",
        titolo="Librerie e ambiente",
        blocco=1,
        giornata=1,
        intento="Python da solo fa poco: il lavoro vero lo fanno le librerie, codice già scritto che entra in gioco con `import`. Vivono nell'ambiente del progetto, e uv lo tiene in ordine.",
        obiettivi={
            "base": [
                "capire cos'è una libreria, cosa fa `import` e cosa distingue la libreria standard da quelle installate",
                "aggiungere una libreria con uv e sapere cosa sono `.venv` e `pyproject.toml`",
                "trasformare un notebook in uno script e lanciarlo con `uv run`",
            ],
            "avanzata": [
                "usare `import` nelle sue tre forme e distinguere la libreria standard da quelle installate",
                "leggere `pyproject.toml` e `uv.lock` e gestire le librerie con uv",
                "trasformare un notebook in uno script e lanciarlo con `uv run`",
            ],
        },
        tempo={"base": 35, "avanzata": 40},
        dati=["letture_pod_2025.csv"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Librerie e import", intro="""
        Una libreria è codice scritto da altri, pronto da usare: funzioni già provate e corrette.
        Alcune arrivano insieme a Python (`math`, `os`, `datetime`: la libreria
        standard), altre vanno installate nel progetto (pandas, Plotly, requests). In entrambi i casi
        entrano in gioco con `import`.
    """)
    nb.md("""
        La forma base è `import nome`. Da quel momento tutto quello che la libreria contiene si
        raggiunge con il punto: `libreria.funzione`.
    """)
    nb.code("""
        import math

        math.sqrt(1600)
    """)
    nb.md("""
        Se di una libreria ci serve una cosa sola, possiamo importare solo quella con
        `from libreria import nome`. Poi si usa senza prefisso.
    """)
    nb.code("""
        from math import sqrt

        sqrt(1600)
    """)
    nb.md("""
        La terza forma è `import nome as alias`: un nome corto per una libreria che scriveremo cento
        volte. `pd` per pandas è una convenzione così diffusa che negli esempi in rete non la spiegano
        neanche più.
    """)
    nb.code("""
        import pandas as pd

        pd.__version__
    """)
    nb.md("""
        Non tutto ha bisogno di un `import`. `print`, `len`, `round`, `type` sono funzioni di Python,
        sempre disponibili: sono una settantina, e quelle che servono le incontreremo strada facendo.
        `pd.read_csv`, invece, è di pandas: esiste solo dopo l'import, e il prefisso `pd.` ci dice da
        dove arriva.
    """)
    nb.code("""
        # funzione di Python: nessun import
        len("IT001E12345678")
    """)
    nb.md("""
        Le librerie che incontreremo stanno da una parte o dall'altra:

        | Libreria standard: arriva con Python | Installata nel progetto |
        |---|---|
        | `math`, `datetime`, `os` | `pandas`, `numpy` |
        | `pathlib`, `json`, `sqlite3` | `plotly`, `requests`, `openpyxl` |

        Regola pratica: se prima di importarla serve `uv add`, è una libreria installata.
    """)
    nb.md("""
        Una libreria è una cartella di moduli, cioè di file Python, e le più grandi hanno cartelle
        dentro cartelle. Il punto serve anche a scendere di un livello: `import plotly.express as px`
        entra in `plotly` e prende il sottomodulo `express`, quello dei grafici veloci.
        `from datetime import date`, invece, prende una cosa sola da un modulo.
    """)
    nb.code("""
        import plotly.express as px

        px.__name__
    """)
    nb.md("""
        `plotly.express` è il percorso dentro la libreria. Dopo il punto può esserci una funzione, che
        fa qualcosa e si chiama con le parentesi: `math.sqrt(1600)`. Oppure un dato che la libreria o
        l'oggetto porta con sé, che si legge senza parentesi: `pd.__version__`, `px.__name__`. Il
        secondo si chiama **attributo**; lo riprendiamo nel notebook sugli oggetti.
    """)
    nb.md("""
        Questa cella dà errore apposta: importiamo una libreria che non esiste.
    """)
    nb.code("import grafici_bollette", errore=True)
    nb.md("""
        `ModuleNotFoundError: No module named 'grafici_bollette'`. Lo stesso messaggio compare in due
        casi diversi: la libreria non è installata nel progetto, oppure il kernel non usa il Python di
        `.venv` e sta guardando nel posto sbagliato. Prima si controlla il kernel, poi si aggiunge la libreria: come,
        lo vediamo nella prossima sezione.
    """)
    nb.md("""
        Per sapere cosa fa una funzione senza uscire dal notebook c'è `help(nome)`: stampa la
        documentazione scritta da chi l'ha creata.
    """)
    nb.code("help(sqrt)")
    nb.box("nota", """
        In VS Code basta anche passare il mouse sul nome della funzione: la documentazione compare in
        un riquadro. Oppure si scrive `sqrt?` in una cella e la si esegue: la stessa documentazione
        compare sotto la cella, come output.
    """)
    nb.prova_tu(
        richiesta="""
            Un campo fotovoltaico quadrato occupa 2500 m². Importa `sqrt` dalla libreria `math` e
            calcola in `lato` la lunghezza del lato, in metri.
        """,
        starter="""
            from math import ...

            area_m2 = 2500
            lato = ...
            lato
        """,
        soluzione="""
            from math import sqrt

            area_m2 = 2500
            lato = sqrt(area_m2)
            lato
        """,
        verifica="""
            assert lato == 50.0, "❌ lato: la radice quadrata dell'area, con sqrt"
        """,
    )
    nb.prova_tu(
        richiesta="""
            Il nome del report mensile deve contenere l'anno in corso. Importa `date` dalla libreria
            `datetime`, chiama `date.today()` e salva il risultato in `oggi`; poi metti in `anno` il suo
            attributo `.year`.
        """,
        starter="""
            from datetime import ...

            oggi = ...
            anno = ...
            anno
        """,
        soluzione="""
            from datetime import date

            oggi = date.today()
            anno = oggi.year
            anno
        """,
        verifica="""
            from datetime import date

            assert anno == date.today().year, "❌ anno: l'attributo .year della data di oggi"
        """,
    )

    # ------------------------------------------------------------------ 2
    nb.sezione("Il progetto del corso", intro="""
        Tutto il corso sta in una cartella, quella aperta in VS Code. Dentro, ogni cosa ha il suo posto:

        ```
        python-base-utilities/
            Aula_.../           i notebook, da compilare: questo file è qui
            Soluzioni_.../      gli stessi notebook, risolti
            Dati/               i file che leggeremo: CSV, Excel, un database SQLite
            Schede/             una pagina per argomento, da tenere a portata di mano
            pyproject.toml      l'elenco delle librerie del progetto
            uv.lock             le versioni esatte di ogni libreria
            .venv/              l'ambiente virtuale, il virtual environment: Python e le librerie installate (non si tocca a mano)
        ```
    """)
    nb.md("""
        Il notebook vede i file a partire dalla sua cartella. I dati stanno nella cartella accanto: per
        arrivarci si sale di un livello con `..` e si scende in `Dati`, quindi `../Dati`. Lo scriveremo
        così in tutto il corso. Diamo un'occhiata dentro con `os`, della libreria standard.
    """)
    nb.code("""
        import os

        os.listdir("../Dati")
    """)
    nb.md("""
        Una lista con i nomi dei file: li apriremo uno per uno dal notebook sull'import dei dati in
        avanti. `pyproject.toml` è un file di testo con l'elenco delle librerie del progetto: si può
        aprire e leggere, lo aggiorna uv da solo.
    """)
    nb.prova_tu(
        richiesta="""
            Metti in `cartella_dati` il percorso della cartella dei dati visto da questo notebook, come
            testo tra virgolette, e in `file_letture` il percorso del file `letture_pod_2025.csv` che
            sta lì dentro.
        """,
        starter="""
            cartella_dati = "..."
            file_letture = "..."

            print(cartella_dati, file_letture)
        """,
        soluzione="""
            cartella_dati = "../Dati"
            file_letture = "../Dati/letture_pod_2025.csv"

            print(cartella_dati, file_letture)
        """,
        verifica="""
            import os

            assert cartella_dati.rstrip("/") == "../Dati", "❌ cartella_dati: due punti per salire, poi il nome della cartella"
            assert os.path.exists(file_letture), "❌ file_letture: la cartella dei dati, una barra, il nome del file"
        """,
    )
    nb.md("""
        Le librerie del progetto le gestisce uv, un programma che si usa dal terminale di VS Code
        (**Terminal → New Terminal**: si apre già nella cartella del progetto). I comandi che servono
        sono due, e si scrivono lì, non in una cella.

        ```bash
        uv sync          # ricrea l'ambiente: installa tutte le librerie elencate nel progetto
        uv add nome      # aggiunge una libreria al progetto e la installa
        ```

        Tutti i comandi sono anche nella [scheda uv e script](../Schede/Scheda_uv_e_script.md).
    """)
    nb.md("""
        `uv sync` si lancia la prima volta e ogni volta che l'ambiente sembra rotto o qualcuno ha
        aggiunto librerie al progetto. Dopo un `uv add`, il kernel che è già in esecuzione non vede la
        novità: **Restart** del kernel, poi `import`.
    """)
    nb.box("attenzione", """
        In rete si trova `!pip install nome` scritto dentro una cella: qui non si fa. Installa in un
        posto che il progetto non conosce, `pyproject.toml` non se ne accorge e il collega che fa
        `uv sync` non la riceve. Nel terminale `uv add nome`, poi Restart del kernel.
    """)
    nb.box("ricorda", """
        - I dati sono in `../Dati/...`, visti dal notebook.
        - Una libreria nuova: nel terminale `uv add nome`, poi Restart del kernel.
        - Ambiente rotto o mancante: `uv sync`.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Un ambiente per progetto", intro="""
        Il notebook funziona sul nostro PC, lo mandiamo al collega e da lui non parte: ha una
        versione di pandas di tre anni fa, installata per un altro progetto, e il nostro codice gli
        dà errori che da noi non esistono. Due progetti, un solo Python condiviso: prima o poi uno
        dei due si rompe. La soluzione è un ambiente per progetto.
    """)
    nb.md("""
        `.venv` è una cartella: un Python e le sue librerie, dedicati a questo progetto. Lo crea `uv sync`, lo usa il kernel che abbiamo scelto, e
        si può cancellare e ricreare in un minuto. È il motivo per cui `sys.executable` doveva
        contenere `.venv`. Dove vive pandas, per dire:
    """)
    nb.code("""
        import pandas as pd

        pd.__file__
    """)
    nb.md("""
        Un file dentro `.venv`: la cartella di moduli di pandas, file Python come i nostri, solo
        scritti da altri. Chi decide cosa finisce lì dentro è `pyproject.toml`; eccone la parte che conta:

        ```toml
        [project]
        name = "python-base-utilities"
        requires-python = ">=3.12"
        dependencies = [
            "pandas>=3.0",
            "numpy>=2.0",
            "plotly>=6.0",
            "openpyxl>=3.1",
            "requests>=2.32",
            "ipykernel>=6.29",
            "nbformat>=5.10",
        ]
        ```
    """)
    nb.md("""
        `dependencies` è la lista delle librerie che il progetto dichiara di usare, con un vincolo
        largo: "pandas, dalla 3.0 in su". Il file si legge per capire di cosa ha bisogno il progetto,
        e `uv add` lo aggiorna da solo. Più sotto c'è `[dependency-groups]`: gli strumenti che servono a
        chi scrive il codice ma non al programma, come Ruff, il linter che useremo più avanti.
    """)
    with nb.solo("avanzata"):
        nb.md("""
            `uv.lock` è l'altra metà: la fotografia esatta di cosa è stato installato, versione per
            versione, dipendenze delle dipendenze comprese (un estratto):

            ```toml
            [[package]]
            name = "pandas"
            version = "3.0.6"
            source = { registry = "https://pypi.org/simple" }
            dependencies = [
                { name = "numpy" },
                { name = "python-dateutil" },
            ]
            ```
        """)
        nb.md("""
            Lo scrive uv, non si tocca a mano, e viaggia insieme a `pyproject.toml`: così il collega
            che fa `uv sync` ottiene lo stesso identico ambiente, oggi e tra un anno. `.venv`, invece,
            non si passa a nessuno: pesa centinaia di megabyte e si ricrea da `uv.lock` in un minuto.
        """)
        nb.md("""
            I comandi di uv che useremo, sempre dal terminale, nella cartella del progetto:

            ```bash
            uv add requests             # aggiunge a pyproject.toml, aggiorna uv.lock, installa
            uv add "pandas>=3.0"        # con un vincolo di versione
            uv remove requests          # toglie la libreria dal progetto
            uv run profilo_carico.py    # esegue un file Python dentro l'ambiente del progetto
            uv run ruff check .         # Ruff del progetto, alla versione di uv.lock
            uvx ruff check .            # lo stesso Ruff al volo, su una cartella senza progetto
            ```
        """)
        nb.md("""
            `uv run` usa `.venv` senza bisogno di "attivarlo": è il comando con cui lanceremo gli
            script, e anche Ruff, che nel progetto è già installato alla versione scritta in `uv.lock`.
            `uvx` scarica uno strumento e lo lancia al volo, senza aggiungerlo a nessun progetto: serve
            su una cartella senza progetto, dove `pyproject.toml` non c'è.
        """)
    nb.md("""
        uv non è l'unico modo. `pip` con `venv` è lo strumento di base di Python: stessa idea, più
        passaggi a mano, niente `uv.lock`. conda è diffuso in ambito scientifico, Poetry fa un lavoro
        simile a uv. In un progetto che li usa, `environment.yml` (conda) o `poetry.lock` (Poetry) fanno
        la parte di `pyproject.toml` e `uv.lock`: chi lo eredita usa quello che trova; chi ne apre uno
        nuovo, oggi, usa uv.
    """, aula="avanzata")
    nb.prova_tu(
        richiesta="""
            Il collega ti passa la cartella del suo progetto: dentro ci sono `pyproject.toml` e
            `uv.lock`, ma niente `.venv`, giustamente. Scrivi in `comando` il comando del terminale
            che ricrea il suo ambiente, identico al suo.
        """,
        starter="""
            comando = "..."
            comando
        """,
        soluzione="""
            comando = "uv sync"
            comando
        """,
        verifica="""
            assert comando.strip() == "uv sync", "❌ comando: quello che legge pyproject.toml e uv.lock e installa tutto"
        """,
    )
    nb.box("nota", """
        Se su un PC uv non c'è, si installa una volta sola seguendo le istruzioni su
        docs.astral.sh/uv; poi vale per tutti i progetti. Non va nel `pyproject.toml`: è lo
        strumento, non una libreria.
    """)
    nb.box("ricorda", """
        - Un progetto, un ambiente: `.venv`, creato da `uv sync`.
        - `pyproject.toml` elenca le librerie che servono: lo aggiorna `uv add`, viaggia insieme al progetto.
        - `.venv` si ricrea con `uv sync`: non si passa a nessuno, non si ripara a mano.
    """, aula="base")
    nb.box("ricorda", """
        - `pyproject.toml` dice cosa serve, `uv.lock` dice esattamente cosa è installato: viaggiano
          insieme al progetto.
        - `.venv` si ricrea con `uv sync`: non si passa a nessuno, non si ripara a mano.
        - `uv add`, `uv remove`, `uv run`: dal terminale, nella cartella del progetto.
    """, aula="avanzata")

    # ------------------------------------------------------------------ 4
    nb.sezione("Script e notebook", intro="""
        Il notebook è il posto per esplorare: si prova una cella, si guarda il risultato, si cambia
        idea. Uno script è un file `.py` che fa sempre la stessa cosa, dall'inizio alla fine, senza
        nessuno davanti: il report che parte alle sei di mattina, il controllo che lanciamo uguale
        ogni lunedì. Regola pratica: quando il notebook ha smesso di cambiare, diventa uno script.
    """)
    nb.md("""
        Si crea in VS Code con **File → New File**, nome `profilo_carico.py`, salvato nella cartella
        principale del progetto, accanto a `pyproject.toml`. Dentro ci vanno una funzione (`def`) che
        riceve una lista di potenze e restituisce l'energia, e un `print` che la chiama; incollaci
        questo codice (lo leggeremo riga per riga nei prossimi notebook):

        ```python
        \"\"\"Dai MW medi di quattro quarti d'ora all'energia dell'ora.\"\"\"


        def energia_mwh(potenze_mw):
            \"\"\"Un quarto d'ora a potenza P vale P/4 MWh: somma e dividi per 4.\"\"\"
            return sum(potenze_mw) / 4


        quartorari = [12.4, 12.9, 13.1, 12.6]
        print(f"Energia dell'ora: {energia_mwh(quartorari)} MWh")
        ```
    """)
    nb.md("""
        Nel terminale, dalla cartella del progetto:

        ```bash
        uv run profilo_carico.py
        ```

        ```
        Energia dell'ora: 12.75 MWh
        ```

        `uv run` apre `.venv`, lancia Python sul file, stampa e chiude. Nessuna cella, nessun kernel:
        può farlo anche un'attività pianificata, prima che arrivi qualcuno in ufficio.
    """)
    nb.md("""
        Incollato in una cella, lo stesso codice stampa la stessa riga: cambia solo chi lo lancia.
    """)
    nb.code('''
        def energia_mwh(potenze_mw):
            """Un quarto d'ora a potenza P vale P/4 MWh: somma e dividi per 4."""
            return sum(potenze_mw) / 4


        quartorari = [12.4, 12.9, 13.1, 12.6]
        print(f"Energia dell'ora: {energia_mwh(quartorari)} MWh")
    ''')
    nb.box("nota", """
        Il notebook parte dalla sua cartella, per questo i dati sono in `../Dati`. Lo script parte dalla
        cartella da cui lo lanci, non da quella in cui è salvato: dalla cartella principale i dati sono
        in `Dati/...`, senza `..`. È il primo errore che si incontra passando dall'uno all'altro.
    """)
    with nb.solo("avanzata"):
        nb.box("approfondimento", """
            Quando lanci `uv run profilo_carico.py`, Python dà al file il nome speciale `__main__`;
            quando invece un altro file lo importa con `import profilo_carico`, il nome è
            `profilo_carico`. Il controllo `if __name__ == "__main__":` dice: "questo pezzo parte solo
            se sono io il programma lanciato, non quando mi importano". Sotto ci vanno le righe che
            fanno il lavoro; le funzioni sopra restano importabili.

            ```python
            def energia_mwh(potenze_mw):
                return sum(potenze_mw) / 4


            if __name__ == "__main__":
                print(energia_mwh([12.4, 12.9, 13.1, 12.6]))
            ```
        """, titolo="Il blocco `if __name__ == \"__main__\"`")
        nb.md("""
            Vale anche qui: per Python, il notebook è il programma principale.
        """)
        nb.code("__name__")
    nb.box("ricorda", """
        - Si esplora nel notebook, si automatizza nello script.
        - `uv run nome.py` dal terminale: stesso ambiente, stesso codice, nessun kernel.
        - Lo script si lancia dalla cartella principale: se legge dei file, li trova in `Dati/...`; il notebook in `../Dati/...`.
    """, aula="base")
    nb.box("ricorda", """
        - Si esplora nel notebook, si automatizza nello script.
        - `uv run nome.py` dal terminale: stesso ambiente, stesso codice, nessun kernel.
        - Lo script si lancia dalla cartella principale: se legge dei file, li trova in `Dati/...`; il notebook in `../Dati/...`.
    """, aula="avanzata")

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="La libreria che manca",
        scenario="""
            Marco, del reporting, prima di andare in ferie ha lasciato un notebook che fa i grafici
            con Plotly e scrive gli Excel con openpyxl. Prima di lanciarlo vogliamo sapere se le librerie
            ci sono, e lasciare scritto cosa fare se mancano: lui torna tra due settimane.
        """,
        richiesta="""
            1. Importa `plotly` e metti in `versione_plotly` la sua versione (l'attributo `__version__`).
            2. Metti in `comando_aggiungi` il comando del terminale che aggiunge `openpyxl` al progetto.
            3. Metti in `comando_collega` il comando che il collega, tornato dalle ferie, lancia per
               ricevere la libreria che hai aggiunto.

            Scrivi i comandi come li scriveresti nel terminale, tutto minuscolo. Poi, in una cella
            Markdown nuova sotto la verifica, lasciali scritti come promemoria per lui.
        """,
        suggerimento="I due comandi sono nel riquadro Ricorda della sezione sul progetto del corso.",
        starter="""
            import ...

            versione_plotly = ...
            comando_aggiungi = "..."
            comando_collega = "..."

            print(versione_plotly, comando_aggiungi, comando_collega)
        """,
        soluzione="""
            import plotly

            versione_plotly = plotly.__version__
            comando_aggiungi = "uv add openpyxl"
            comando_collega = "uv sync"

            print(versione_plotly, comando_aggiungi, comando_collega)
        """,
        verifica="""
            import plotly

            assert versione_plotly == plotly.__version__, "❌ versione_plotly: l'attributo __version__ della libreria plotly"
            assert comando_aggiungi.strip() == "uv add openpyxl", "❌ comando_aggiungi: il comando uv che aggiunge una libreria, seguito dal nome"
            assert comando_collega.strip() == "uv sync", "❌ comando_collega: il comando uv che ricrea l'ambiente dal progetto"
        """,
        perche="Chi aggiunge fa `uv add`; chi riceve il progetto aggiornato fa `uv sync`. Sono i due lati dello stesso `pyproject.toml`.",
        passo_in_piu=dict(
            testo="""
                Il notebook del collega richiede una versione minima di Python: è scritta in
                `pyproject.toml`, alla voce `requires-python`. Apri il file da VS Code e copia quel
                valore, virgolette escluse, nel testo `requisito`. Poi, con la libreria standard
                `platform`, metti in `versione_python` il risultato di `platform.python_version()`:
                siamo a posto?
            """,
            starter="""
                import platform

                requisito = "..."
                versione_python = ...

                print(requisito, versione_python)
            """,
            soluzione="""
                import platform

                requisito = ">=3.12"
                versione_python = platform.python_version()

                print(requisito, versione_python)
            """,
            verifica="""
                import platform

                assert requisito.replace(" ", "") == ">=3.12", "❌ requisito: il valore di requires-python in pyproject.toml, senza virgolette"
                assert versione_python == platform.python_version(), "❌ versione_python: il risultato di platform.python_version()"
            """,
        ),
    )
    nb.esercizio(
        titolo="Il kernel sbagliato",
        bis=True,
        scenario="""
            Lunedì mattina Marco apre il notebook del reporting e `import pandas` fallisce con
            `ModuleNotFoundError`. Nel terminale `uv sync` risponde che è tutto a posto, e in
            `pyproject.toml` pandas c'è. Ci chiama: "sul tuo funziona, sul mio no".
        """,
        richiesta="""
            1. Metti in `percorso_python` il percorso del Python che sta eseguendo questo notebook
               (`sys.executable`, visto nel notebook precedente).
            2. In `diagnosi` scrivi `"kernel"` se il problema di Marco è il kernel selezionato,
               `"libreria"` se gli manca la libreria.
            3. In `rimedio` scrivi cosa deve fare Marco, scegliendo tra `"Select Kernel"`,
               `"uv add pandas"` e `"!pip install pandas"`.
        """,
        suggerimento="Se `uv sync` è contento e `pyproject.toml` elenca pandas, la libreria nell'ambiente c'è.",
        starter="""
            import sys

            percorso_python = ...
            diagnosi = "..."
            rimedio = "..."

            print(percorso_python, diagnosi, rimedio)
        """,
        soluzione="""
            import sys

            percorso_python = sys.executable
            diagnosi = "kernel"
            rimedio = "Select Kernel"

            print(percorso_python, diagnosi, rimedio)
        """,
        verifica="""
            assert ".venv" in percorso_python, "❌ percorso_python: sys.executable, e deve contenere .venv (altrimenti cambia kernel tu per primo)"
            assert diagnosi == "kernel", "❌ diagnosi: la libreria è installata nel progetto, quindi il problema è un altro"
            assert rimedio == "Select Kernel", "❌ rimedio: non si installa niente, si cambia il Python che esegue il notebook"
        """,
        perche="La libreria c'è, lo dice `uv sync`: il notebook la cerca nel Python sbagliato. Si cambia kernel, non si installa due volte.",
    )
    nb.esercizio(
        titolo="Da notebook a script",
        aula="base",
        scenario="""
            Il collega della reperibilità vuole trovare ogni mattina, appena arriva, la media delle
            letture della notte, calcolata da un'attività pianificata: niente notebook, niente clic.
            Le cinque letture di stanotte sono già nel codice qui sotto.
        """,
        richiesta='''
            1. Crea in VS Code il file `media_letture.py` nella cartella principale del progetto,
               accanto a `pyproject.toml`, e incollaci questo codice:

               ```python
               letture = [412.5, 398.0, 405.2, 410.8, 401.0]


               def media(valori):
                   """Media aritmetica di una lista di numeri."""
                   return sum(valori) / len(valori)


               print(f"Media delle letture: {media(letture)} kWh")
               ```

            2. Nel terminale, `uv run media_letture.py`.
            3. Copia la riga stampata dal terminale nella variabile `output_script` qui sotto.
        ''',
        suggerimento="Salva il file prima di lanciarlo: finché non salvi, VS Code mette un pallino accanto al nome.",
        starter="""
            # il contenuto del file sta in media_letture.py; qui solo la riga copiata dal terminale
            output_script = "..."
            output_script
        """,
        soluzione="""
            # la riga stampata dal terminale dopo: uv run media_letture.py
            output_script = "Media delle letture: 405.5 kWh"
        """,
        verifica="""
            assert output_script.strip() == "Media delle letture: 405.5 kWh", "❌ output_script: la riga stampata dal terminale, tale e quale"
        """,
        perche="Il file sta nella cartella principale, dove si apre il terminale: così `uv run media_letture.py` funziona senza percorsi. La riga finale è copiata dal terminale, non ricalcolata: è la prova che lo script è partito davvero.",
        passo_in_piu=dict(
            testo="""
                Cambia l'ultima lettura da `401.0` a `421.0`, salva, rilancia `uv run media_letture.py` e
                copia la nuova riga in `output_script_bis`. Il codice è lo stesso: è cambiato solo il dato.
            """,
            starter="""
                output_script_bis = "..."
                output_script_bis
            """,
            soluzione="""
                output_script_bis = "Media delle letture: 409.5 kWh"
            """,
            verifica="""
                assert output_script_bis.strip() == "Media delle letture: 409.5 kWh", "❌ output_script_bis: la riga stampata dopo aver cambiato 401.0 in 421.0"
            """,
        ),
    )
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="Da notebook a script",
            scenario="""
                Il collega della reperibilità vuole trovare ogni mattina, appena arriva, la media delle
                letture della notte, calcolata da un'attività pianificata: niente notebook, niente clic.
                Le cinque letture di stanotte, in kWh: `412.5, 398.0, 405.2, 410.8, 401.0`.
            """,
            richiesta="""
                1. Crea in VS Code il file `media_letture.py` nella cartella principale del progetto,
                   accanto a `pyproject.toml`. Dentro: una lista `letture` con i cinque valori, una
                   funzione `media(valori)` che restituisce `sum(valori) / len(valori)` e un `print`
                   con f-string, come in `profilo_carico.py`, che stampa
                   `Media delle letture: <media> kWh`.
                2. Nel terminale, `uv run media_letture.py`.
                3. Copia la riga stampata dal terminale nella variabile `output_script` qui sotto.
            """,
            suggerimento="Parti da `profilo_carico.py` e adatta nomi e calcolo.",
            starter="""
                # il contenuto del file sta in media_letture.py; qui solo la riga copiata dal terminale
                output_script = "..."
                output_script
            """,
            soluzione='''
                # contenuto di media_letture.py, salvato nella cartella principale del progetto
                letture = [412.5, 398.0, 405.2, 410.8, 401.0]


                def media(valori):
                    """Media aritmetica di una lista di numeri."""
                    return sum(valori) / len(valori)


                print(f"Media delle letture: {media(letture)} kWh")

                # la riga stampata dal terminale dopo: uv run media_letture.py
                output_script = "Media delle letture: 405.5 kWh"
            ''',
            verifica="""
                assert output_script.strip() == "Media delle letture: 405.5 kWh", "❌ output_script: la riga stampata dal terminale, tale e quale"
            """,
            perche="Il file sta nella cartella principale, dove si apre il terminale: così `uv run media_letture.py` funziona senza percorsi. La riga finale è copiata dal terminale, non ricalcolata: è la prova che lo script è partito davvero.",
        )
    return nb
