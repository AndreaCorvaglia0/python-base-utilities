"""01 · Librerie e ambiente."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="01",
        file="01_Librerie_e_ambiente",
        titolo="Librerie e ambiente",
        blocco=1,
        giornata=1,
        intento="Python da solo fa poco: il lavoro vero lo fanno le librerie, e il posto dove vivono è l'ambiente del progetto. Impariamo a chiamarle senza romperlo.",
        obiettivi={
            "base": [
                "capire cos'è una libreria e cosa fa `import`",
                "aggiungere una libreria al progetto con uv, nel modo giusto",
                "orientarci nella cartella del corso: notebook, dati e `pyproject.toml`",
            ],
            "avanzata": [
                "usare `import` nelle sue tre forme e capire perché serve un ambiente per progetto",
                "leggere `pyproject.toml` e `uv.lock` e gestire le librerie con uv",
                "trasformare un notebook in uno script e lanciarlo con `uv run`",
            ],
        },
        tempo={"base": 20, "avanzata": 40},
        dati=[],
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
        sempre disponibili: poche decine, e le incontreremo quasi tutte. `pd.read_csv`, invece, è di
        pandas: esiste solo dopo l'import, e il prefisso `pd.` ci dice da dove arriva.
    """)
    nb.code("""
        # funzione di Python: nessun import
        len("IT001E12345678")
    """)
    nb.md("""
        Questa cella dà errore apposta: importiamo una libreria che non esiste.
    """)
    nb.code("import grafici_bollette", errore=True)
    nb.md("""
        `ModuleNotFoundError: No module named 'grafici_bollette'`. Lo stesso messaggio compare in due
        casi diversi: la libreria non è installata nel progetto, oppure il kernel non è `.venv` e sta
        guardando nel posto sbagliato. Prima si controlla il kernel, poi si aggiunge la libreria: come,
        lo vediamo nella prossima sezione.
    """)
    nb.md("""
        Per sapere cosa fa una funzione senza uscire dal notebook c'è `help(nome)`: stampa la
        documentazione scritta da chi l'ha creata.
    """)
    nb.code("help(sqrt)")
    nb.box("nota", """
        In VS Code basta anche passare il mouse sul nome della funzione, oppure scrivere `sqrt?` in una
        cella ed eseguirla: compare la stessa documentazione, in un pannello a lato.
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
            .venv/              l'ambiente: Python e le librerie installate (non si tocca a mano)
        ```
    """)
    nb.md("""
        Il notebook vede i file a partire dalla sua cartella. I dati stanno nella cartella accanto: per
        arrivarci si sale di un livello con `..` e si scende in `Dati`, quindi `../Dati`. Lo scriveremo
        così in tutto il corso. La libreria standard `os` ci fa dare un'occhiata.
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

    # ------------------------------------------------------------------ 3 (A)
    with nb.solo("avanzata"):
        nb.sezione("Un ambiente per progetto", intro="""
            Il notebook funziona sul nostro PC, lo mandiamo al collega e da lui non parte: ha una
            versione di pandas di tre anni fa, installata per un altro progetto, e il nostro codice gli
            dà errori che da noi non esistono. Due progetti, un solo Python condiviso: prima o poi uno
            dei due si rompe. La soluzione è un ambiente per progetto.
        """)
        nb.md("""
            L'ambiente è la cartella `.venv`: un Python e le sue librerie, dedicati a questo progetto.
            Lo crea `uv sync`, lo usa il kernel che abbiamo scelto, e si può cancellare e ricreare in un
            minuto. È il motivo per cui `sys.executable` doveva contenere `.venv`. Dove vive pandas, per
            dire:
        """)
        nb.code("""
            import pandas as pd

            pd.__file__
        """)
        nb.md("""
            Un file dentro `.venv`: una libreria è una cartella di file Python come i nostri, solo
            scritti da altri. Chi decide cosa finisce lì dentro è `pyproject.toml`:

            ```toml
            [project]
            name = "python-base-utilities"
            requires-python = ">=3.12"
            dependencies = [
                "pandas>=2.2",
                "plotly>=6.0",
                "openpyxl>=3.1",
                "requests>=2.32",
            ]
            ```
        """)
        nb.md("""
            `dependencies` è la lista delle librerie che il progetto dichiara di usare, con un vincolo
            largo: "pandas, dalla 2.2 in su". È il file che si legge per capire di cosa ha bisogno un
            progetto, e che `uv add` aggiorna da solo.
        """)
        nb.md("""
            `uv.lock` è l'altra metà: la fotografia esatta di cosa è stato installato, versione per
            versione, dipendenze delle dipendenze comprese.

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
            uv add "pandas>=2.2"        # con un vincolo di versione
            uv remove requests          # toglie la libreria dal progetto
            uv run profilo_carico.py    # esegue un file Python dentro l'ambiente del progetto
            uvx ruff check .            # esegue uno strumento una volta, senza aggiungerlo al progetto
            ```
        """)
        nb.md("""
            `uv run` usa `.venv` senza bisogno di "attivarlo": è il comando con cui lanceremo gli
            script. `uvx` serve per gli strumenti che non fanno parte del progetto ma ci lavorano sopra,
            come Ruff, che controlla e formatta il codice.
        """)
        nb.md("""
            uv non è l'unico modo. `pip` con `venv` è lo strumento di base di Python: stessa idea, più
            passaggi a mano, niente `uv.lock`. conda è diffuso in ambito scientifico, Poetry fa quello che
            fa uv ma più lentamente. Chi entra in un progetto esistente usa quello che trova; chi ne apre
            uno nuovo, oggi, usa uv.
        """)
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
            - `pyproject.toml` dice cosa serve, `uv.lock` dice esattamente cosa è installato: viaggiano
              insieme al progetto.
            - `.venv` si ricrea con `uv sync`: non si passa a nessuno, non si ripara a mano.
            - `uv add`, `uv remove`, `uv run`: dal terminale, nella cartella del progetto.
        """)

        # -------------------------------------------------------------- 4 (A)
        nb.sezione("Script e notebook", intro="""
            Il notebook è il posto per esplorare: si prova una cella, si guarda il risultato, si cambia
            idea. Uno script è un file `.py` che fa sempre la stessa cosa, dall'inizio alla fine, senza
            nessuno davanti: il report che parte alle sei di mattina, la funzione che tre notebook si
            passano. Regola pratica: quando il notebook ha smesso di cambiare, diventa uno script.
        """)
        nb.md("""
            Si crea in VS Code con **File → New File**, nome `profilo_carico.py`, salvato nella cartella
            principale del progetto, accanto a `pyproject.toml`. Dentro, una funzione (`def`) che riceve
            una lista di potenze e restituisce l'energia, e un `print` che la chiama. Funzioni e liste
            le vediamo per bene nei prossimi notebook: qui ci interessa il file.

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
            può farlo anche un'attività pianificata alle sei di mattina, con tutti a casa.
        """)
        nb.md("""
            Lo stesso codice, incollato in una cella, fa la stessa cosa. La differenza non è il codice:
            è chi lo lancia, e quando.
        """)
        nb.code('''
            def energia_mwh(potenze_mw):
                """Un quarto d'ora a potenza P vale P/4 MWh: somma e dividi per 4."""
                return sum(potenze_mw) / 4


            quartorari = [12.4, 12.9, 13.1, 12.6]
            print(f"Energia dell'ora: {energia_mwh(quartorari)} MWh")
        ''')
        nb.box("nota", """
            Il notebook parte dalla sua cartella, per questo i dati sono in `../Dati`. Uno script salvato
            nella cartella principale parte da lì: per lui i dati stanno in `Dati/...`, senza `..`. È il
            primo errore che si incontra passando dall'uno all'altro.
        """)
        nb.box("approfondimento", """
            Quando lanci `uv run profilo_carico.py`, Python dà al file il nome speciale `__main__`;
            quando invece un altro file lo importa con `import profilo_carico`, il nome è
            `profilo_carico`. Il controllo `if __name__ == "__main__":` dice: "questo pezzo parte solo
            se sono io il programma lanciato, non quando mi importano". Ci si mettono sotto le righe di
            prova e i `print`, lasciando le funzioni libere di essere importate da un notebook o da un
            altro script.

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
            - Le funzioni in alto, le righe che le usano in basso: così lo script si può anche importare.
        """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="La libreria che manca",
        scenario="""
            Il collega del reporting, prima di andare in ferie, ha lasciato un notebook che fa i grafici
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
                valore, virgolette escluse, nella stringa `requisito`. Poi, con la libreria standard
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
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="Da notebook a script",
            scenario="""
                Il collega della reperibilità vuole la media delle letture della notte ogni mattina alle
                sei, lanciata da un'attività pianificata: niente notebook, niente clic. Le cinque letture
                di stanotte, in kWh: 412.5, 398.0, 405.2, 410.8, 401.0.
            """,
            richiesta="""
                1. Crea in VS Code il file `media_letture.py` nella cartella principale del progetto,
                   accanto a `pyproject.toml`. Dentro: una lista `letture` con i cinque valori, una
                   funzione `media(valori)` che restituisce `sum(valori) / len(valori)` e un `print`
                   che stampa esattamente `Media delle letture: 405.5 kWh`.
                2. Nel terminale, `uv run media_letture.py`.
                3. Copia la riga stampata dal terminale nella variabile `output_script` qui sotto.
            """,
            suggerimento="Parti dal file `profilo_carico.py` e cambia nomi, numeri e divisione.",
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
