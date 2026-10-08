"""Extra X1 · Ambiente uv e script (dimostrazione del docente)."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="X1",
        file="Ambiente_uv_e_script",
        titolo="Ambiente uv e script",
        blocco=1,
        giornata=0,
        intento="Dove vivono Python e le librerie di un progetto, come le gestisce uv e come si passa da un notebook a uno script.",
        obiettivi=[
            "aggiungere una libreria al progetto con uv e ricreare l'ambiente con `uv sync`",
            "leggere `pyproject.toml` e sapere a cosa serve `.venv`",
            "trasformare un notebook in uno script e lanciarlo con `uv run`",
        ],
        tempo=15,
        dati=["letture_pod_2025.csv"],
        extra=True,
    )

    nb.sezione("Il progetto del corso", intro="""
        Tutto il materiale del corso sta in una cartella, quella che abbiamo aperto in VS Code. Al suo
        interno i notebook, i dati e le schede stanno in sottocartelle separate, e accanto a queste ci
        sono i file che descrivono il progetto:

        ```
        python-base-utilities/
            Aula_.../           i notebook, da compilare
            Soluzioni_.../      gli stessi notebook, risolti
            Dati/               i file che leggeremo: CSV, Excel, un database SQLite
            Schede/             una pagina per argomento, da tenere a portata di mano
            pyproject.toml      l'elenco delle librerie del progetto
            uv.lock             le versioni esatte di ogni libreria
            .venv/              l'ambiente virtuale (il virtual environment): Python e le librerie, non si tocca
        ```
    """)
    nb.md("""
        Un notebook cerca i file a partire dalla cartella in cui è salvato. I dati stanno in una cartella
        accanto, quindi per raggiungerli si sale di un livello con `..` e si scende in `Dati`, scrivendo
        `../Dati`; in tutto il corso i percorsi dei dati hanno questa forma. Per vedere che cosa contiene
        la cartella usiamo la funzione `listdir` del modulo `os`, che fa parte della libreria standard.
    """)
    nb.code("""
        import os

        os.listdir("../Dati")
    """)
    nb.md("""
        Il risultato è una lista con i nomi dei file, che apriremo uno per uno a partire dal notebook
        sull'import dei dati. Nella cartella principale c'è anche `pyproject.toml`, un file di testo con
        l'elenco delle librerie del progetto. Si può aprire e leggere liberamente, ma non serve modificarlo
        a mano, perché lo aggiorna uv.
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
        Le librerie del progetto sono gestite da uv, un programma che si usa dal terminale di VS Code. Il
        terminale si apre con **Terminal → New Terminal** e parte già nella cartella del progetto. Nella
        pratica servono due comandi, che si scrivono nel terminale e non in una cella del notebook:

        ```bash
        uv sync          # ricrea l'ambiente: installa tutte le librerie elencate nel progetto
        uv add nome      # aggiunge una libreria al progetto e la installa
        ```

        Tutti i comandi sono raccolti anche nella [scheda uv e script](../Schede/Scheda_uv_e_script.md).
    """)
    nb.md("""
        Il comando `uv sync` si lancia la prima volta, e poi ogni volta che l'ambiente sembra danneggiato
        o che qualcuno ha aggiunto librerie al progetto. Dopo un `uv add`, invece, il kernel già in
        esecuzione non vede la nuova libreria, quindi prima di eseguire l'`import` si riavvia il kernel
        con **Restart**.
    """)
    nb.box("attenzione", """
        Negli esempi in rete si trova spesso `!pip install nome` scritto dentro una cella, ma nel corso
        non si usa. Il comando installa la libreria in un modo che il progetto non registra: `pyproject.toml`
        non viene aggiornato, e il collega che lancia `uv sync` non la riceve. La strada corretta è
        `uv add nome` nel terminale, seguito da un Restart del kernel.
    """)
    nb.sezione("Un ambiente per progetto", intro="""
        Capita che un notebook funzioni sul nostro PC e non parta su quello di un collega, perché lui ha
        una versione di pandas di qualche anno fa, installata per un altro progetto, con cui il nostro
        codice dà errori. Il problema nasce dal fatto che un solo Python condiviso tra più progetti ha una
        sola versione di ogni libreria, che può andare bene per un progetto e non per un altro. Per questo
        si crea un ambiente separato per ciascun progetto, con le versioni delle librerie che gli servono.
    """)
    nb.md("""
        Nel nostro progetto l'ambiente è la cartella `.venv`, che contiene un Python e le librerie
        dedicate a questo progetto. La crea `uv sync`, la usa il kernel che abbiamo scelto, e si può
        cancellare e ricreare in un minuto; è per questo che il percorso restituito da `sys.executable`
        doveva contenere `.venv`. Anche le librerie si trovano lì dentro, come si vede chiedendo a pandas
        il percorso del suo file principale.
    """)
    nb.code("""
        import pandas as pd

        pd.__file__
    """)
    nb.md("""
        Il percorso porta dentro `.venv`, nella cartella che contiene i moduli di pandas, che sono file
        Python come i nostri, scritti da altri. Quali librerie finiscono in questa cartella lo stabilisce
        `pyproject.toml`, di cui riportiamo la parte principale:

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
        La voce `dependencies` elenca le librerie che il progetto dichiara di usare, ciascuna con un
        vincolo di versione largo: `pandas>=3.0`, per esempio, indica pandas dalla versione 3.0 in su. Il
        file si legge per capire di che cosa ha bisogno il progetto, mentre ad aggiornarlo pensa `uv add`.
        Più sotto c'è la sezione `[dependency-groups]`, che elenca gli strumenti utili a chi scrive il
        codice ma non al programma, come il linter Ruff che useremo più avanti.
    """)
    nb.md("""
        Il file `uv.lock` completa `pyproject.toml` con l'elenco esatto di quanto è stato installato,
        versione per versione, comprese le dipendenze delle dipendenze. Questo è un estratto della voce
        dedicata a pandas:

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
        Il file `uv.lock` lo scrive uv e non si modifica a mano. Si condivide insieme a `pyproject.toml`,
        così il collega che lancia `uv sync` ottiene esattamente lo stesso ambiente, oggi come tra un anno.
        La cartella `.venv`, invece, non si condivide, perché pesa centinaia di megabyte e si ricrea da
        `uv.lock` in un minuto.
    """)
    nb.md("""
        I comandi di uv che useremo nel corso si lanciano sempre dal terminale, nella cartella del
        progetto. Accanto a ciascuno, un commento ne riassume l'effetto:

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
        Il comando `uv run` esegue un programma dentro `.venv` senza che l'ambiente debba essere attivato
        prima. Lo useremo per lanciare gli script e anche Ruff, che nel progetto è già installato nella
        versione scritta in `uv.lock`. Il comando `uvx`, invece, scarica uno strumento e lo esegue senza
        aggiungerlo ad alcun progetto, ed è utile in una cartella in cui `pyproject.toml` non c'è.
    """)
    nb.md("""
        uv non è l'unico strumento per gestire gli ambienti. Lo strumento di base di Python è `pip`
        insieme a `venv`, che segue la stessa idea ma richiede più passaggi a mano e non produce un file
        come `uv.lock`. In ambito scientifico è diffuso conda, mentre Poetry svolge un lavoro simile a
        quello di uv. Nei progetti che li usano, il ruolo di `pyproject.toml` e `uv.lock` è svolto da
        `environment.yml` per conda o da `poetry.lock` per Poetry; chi eredita un progetto usa lo strumento
        che trova, mentre per un progetto nuovo nel corso si usa uv.
    """)
    nb.prova_tu(
        richiesta="""
            Un collega ti passa la cartella del suo progetto, che contiene `pyproject.toml` e `uv.lock`
            ma, come è giusto, non la cartella `.venv`. Scrivi in `comando` il comando del terminale che
            ricrea sul tuo PC un ambiente identico al suo.
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
        Se su un PC uv non è installato, lo si installa una volta sola seguendo le istruzioni su
        docs.astral.sh/uv, e da quel momento vale per tutti i progetti. uv non compare in
        `pyproject.toml`, perché è lo strumento che gestisce le librerie e non una libreria del progetto.
    """)
    nb.sezione("Script e notebook", intro="""
        Il notebook è lo strumento adatto all'esplorazione, perché permette di provare una cella,
        guardare il risultato e cambiare strada. Uno script è invece un file `.py` che esegue sempre le
        stesse operazioni dall'inizio alla fine, senza che nessuno debba intervenire, come un report che
        parte alle sei di mattina o un controllo da ripetere ogni lunedì. Quando il codice di un notebook è
        diventato stabile, si può trasformare in uno script.
    """)
    nb.md("""
        Per creare lo script usiamo **File → New File** in VS Code e salviamo il file con il nome
        `profilo_carico.py` nella cartella principale del progetto, accanto a `pyproject.toml`. Il file
        contiene una funzione che riceve una lista di potenze e restituisce l'energia, seguita da un
        `print` che la chiama. Incolliamo nel file il codice seguente, che leggeremo riga per riga nei
        prossimi notebook:

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
        Lo script si lancia dal terminale, nella cartella del progetto, e stampa una sola riga:

        ```bash
        uv run profilo_carico.py
        ```

        ```
        Energia dell'ora: 12.75 MWh
        ```

        Il comando `uv run` avvia il Python di `.venv` sul file, esegue il codice e termina. Non servono
        celle né un kernel, e per questo lo stesso comando può essere lanciato da un'attività pianificata,
        anche prima che qualcuno arrivi in ufficio.
    """)
    nb.md("""
        Lo stesso codice, incollato in una cella del notebook, stampa esattamente la stessa riga, perché
        una cella e uno script eseguono le istruzioni Python nello stesso modo e differiscono solo per il
        modo in cui vengono avviati.
    """)
    nb.code('''
        def energia_mwh(potenze_mw):
            """Un quarto d'ora a potenza P vale P/4 MWh: somma e dividi per 4."""
            return sum(potenze_mw) / 4


        quartorari = [12.4, 12.9, 13.1, 12.6]
        print(f"Energia dell'ora: {energia_mwh(quartorari)} MWh")
    ''')
    nb.box("nota", """
        Il notebook cerca i file a partire dalla propria cartella, ed è per questo che i dati sono in
        `../Dati`. Uno script, invece, li cerca a partire dalla cartella da cui viene lanciato, che non è
        necessariamente quella in cui è salvato: lanciato dalla cartella principale, trova i dati in
        `Dati/...`, senza `..`. È il primo errore che si incontra passando dal notebook allo script.
    """)
    nb.box("approfondimento", """
        Quando si lancia `uv run profilo_carico.py`, Python assegna al file il nome speciale
        `__main__`, mentre se un altro file lo importa con `import profilo_carico` il nome è
        `profilo_carico`. Il controllo `if __name__ == "__main__":` esegue quindi il blocco sottostante
        solo quando il file è il programma lanciato. Lì si mettono le righe che fanno il lavoro, mentre
        le funzioni definite sopra restano importabili.

        ```python
        def energia_mwh(potenze_mw):
            return sum(potenze_mw) / 4


        if __name__ == "__main__":
            print(energia_mwh([12.4, 12.9, 13.1, 12.6]))
        ```
    """, titolo="Il blocco `if __name__ == \"__main__\"`")
    nb.md("""
        Lo stesso vale nel notebook, che per Python è il programma principale, e infatti nella cella
        seguente `__name__` vale `'__main__'`.
    """)
    nb.code("__name__")

    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="La libreria che manca",
        scenario="""
            Prima di andare in ferie, Marco del reporting ha lasciato un notebook che disegna i grafici
            con Plotly e scrive i file Excel con openpyxl. Prima di lanciarlo vogliamo controllare che le
            librerie siano installate e lasciare scritto cosa fare se ne manca una, perché lui torna tra
            due settimane.
        """,
        richiesta="""
            1. Importa `plotly` e metti in `versione_plotly` la sua versione, che si legge dall'attributo `__version__`.
            2. Metti in `comando_aggiungi` il comando del terminale che aggiunge `openpyxl` al progetto.
            3. Metti in `comando_collega` il comando che il collega, tornato dalle ferie, lancia per
               ricevere la libreria che hai aggiunto.

            Scrivi i comandi come li scriveresti nel terminale, tutto in minuscolo. Infine, in una nuova
            cella Markdown sotto la verifica, riportali come promemoria per Marco.
        """,
        suggerimento="I due comandi sono nella sezione sul progetto del corso.",
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
        perche="Chi aggiunge una libreria usa `uv add`, che aggiorna `pyproject.toml` e `uv.lock`; chi riceve il progetto aggiornato usa `uv sync`, che legge quei due file e installa quello che manca.",
    )
    nb.esercizio(
        titolo="Il kernel sbagliato",
        scenario="""
            Lunedì mattina Marco apre il notebook del reporting e `import pandas` fallisce con un
            `ModuleNotFoundError`. Nel terminale `uv sync` risponde che è tutto a posto e in
            `pyproject.toml` pandas compare tra le dipendenze, eppure sul suo PC il notebook non parte,
            mentre sul nostro funziona.
        """,
        richiesta="""
            1. Metti in `percorso_python` il percorso del Python che sta eseguendo questo notebook
               (`sys.executable`).
            2. In `diagnosi` scrivi `"kernel"` se il problema di Marco è il kernel selezionato,
               `"libreria"` se gli manca la libreria.
            3. In `rimedio` scrivi cosa deve fare Marco, scegliendo tra `"Select Kernel"`,
               `"uv add pandas"` e `"!pip install pandas"`.
        """,
        suggerimento="Se `uv sync` non segnala problemi e `pyproject.toml` elenca pandas, la libreria è installata nell'ambiente del progetto.",
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
        perche="La libreria è installata, come conferma `uv sync`, ma il notebook la cerca in un Python diverso da quello del progetto. La soluzione è quindi scegliere il kernel giusto, senza installare nulla una seconda volta.",
    )
    nb.esercizio(
        titolo="Da notebook a script",
        scenario="""
            Il collega della reperibilità vuole trovare ogni mattina, appena arriva, la media delle
            letture della notte, calcolata da un'attività pianificata senza aprire alcun notebook. Le
            cinque letture di stanotte, in kWh, sono `412.5, 398.0, 405.2, 410.8, 401.0`.
        """,
        richiesta="""
            1. Crea in VS Code il file `media_letture.py` nella cartella principale del progetto,
               accanto a `pyproject.toml`. Il file deve contenere una lista `letture` con i cinque valori, una
               funzione `media(valori)` che restituisce `sum(valori) / len(valori)` e un `print`
               con f-string, come in `profilo_carico.py`, che stampa
               `Media delle letture: <media> kWh`.
            2. Lancia lo script dal terminale con `uv run media_letture.py`.
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
        perche="Il file sta nella cartella principale, che è anche quella in cui si apre il terminale, quindi `uv run media_letture.py` funziona senza indicare percorsi. La riga finale va copiata dal terminale e non ricalcolata nel notebook, perché è la prova che lo script è stato eseguito.",
    )
    return nb
