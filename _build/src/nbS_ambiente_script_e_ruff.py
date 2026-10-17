"""S · Ambiente, script e Ruff (solo aula Avanzata, modulo 1, dopo il notebook 03)."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="S",
        file="Ambiente_script_e_Ruff",
        titolo="Ambiente, script e Ruff",
        blocco=1,
        giornata=1,
        aule=("avanzata",),
        intento=(
            "Il notebook mostra come è fatto l'ambiente del progetto e come lo gestisce uv, quando conviene "
            "uno script al posto di un notebook e come Ruff controlla e rimette in forma il codice."
        ),
        obiettivi=[
            "riconoscere i file che descrivono il progetto e gestire le librerie con `uv add` e `uv sync`",
            "trasformare il codice di un notebook in uno script `.py` e lanciarlo con `uv run`",
            "usare Ruff in VS Code per rimettere in forma il codice e leggere i suoi avvisi",
        ],
        tempo=30,
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Il progetto del corso", intro="""
        Il progetto del corso è stato preparato con il comando `uv sync`, lanciato nella cartella
        principale. Il comando ha letto i file che descrivono il progetto, ha scaricato la versione di
        Python richiesta, se sul PC mancava, e ha creato la cartella `.venv` con quel Python e tutte le
        librerie del corso. In questa sezione vediamo che cosa contengono quei file, che sono gli stessi
        in qualunque progetto Python gestito con uv.
    """)
    nb.md("""
        Accanto alle cartelle dei notebook e dei dati, la cartella principale contiene tre elementi che
        riguardano l'ambiente, cioè gli ultimi tre dello schema seguente:

        ```
        python-base-utilities/
            Aula_.../           i notebook del corso
            Dati/               i file che leggeremo: CSV, Excel, un database SQLite
            Schede/             una pagina di riepilogo per argomento
            pyproject.toml      la descrizione del progetto e l'elenco delle librerie
            uv.lock             le versioni esatte di ogni libreria installata
            .venv/              l'ambiente virtuale: Python e le librerie del progetto
        ```
    """)
    nb.md("""
        Il file `pyproject.toml` è un file di testo nel formato TOML, che si può aprire in VS Code e
        leggere liberamente. La sezione `[project]` contiene il nome del progetto, la versione minima di
        Python e, sotto la voce `dependencies`, le librerie di cui il progetto ha bisogno. Lo stesso
        contenuto si legge anche da Python: `Path` del modulo `pathlib` legge il file come testo, e la
        funzione `tomllib.loads` lo trasforma in un dizionario in cui ogni sezione del file è una chiave.
    """)
    nb.code("""
        import tomllib
        from pathlib import Path

        testo = Path("../pyproject.toml").read_text(encoding="utf-8")
        progetto = tomllib.loads(testo)
        progetto["project"]["dependencies"]
    """)
    nb.md("""
        Il risultato è la lista delle librerie, ciascuna con un vincolo di versione largo: `pandas>=3.0`,
        per esempio, indica pandas dalla versione 3.0 in su. Il file si legge per capire di che cosa ha
        bisogno il progetto, ma non serve modificarlo a mano, perché lo aggiorna uv quando aggiungiamo o
        togliamo una libreria.
    """)
    nb.hands_on(
        richiesta="""
            La sezione `[dependency-groups]` del file elenca, sotto la voce `dev`, gli strumenti che servono
            a chi scrive il codice ma non al programma. Metti in `strumenti` quella lista, leggendola da
            `progetto` con due chiavi come nell'esempio: tra gli strumenti compare anche Ruff, che useremo
            alla fine del notebook.
        """,
        starter="""
            strumenti = ...
            strumenti
        """,
        soluzione="""
            strumenti = progetto["dependency-groups"]["dev"]
            strumenti
        """,
        verifica="""
            assert strumenti == progetto["dependency-groups"]["dev"], "❌ strumenti: prima la chiave \\"dependency-groups\\", poi \\"dev\\""
            assert any(voce.startswith("ruff") for voce in strumenti), "❌ tra gli strumenti di sviluppo dovrebbe esserci ruff"
        """,
        prova_anche='`progetto["project"]["requires-python"]`, che dice quale versione di Python serve al progetto.',
    )
    nb.md("""
        Il file `uv.lock` completa `pyproject.toml` con l'elenco esatto di quello che è stato installato,
        versione per versione, comprese le librerie da cui dipendono quelle elencate. Lo scrive uv e non si
        modifica a mano. Si condivide insieme a `pyproject.toml`, in modo che chi riceve il progetto e
        lancia `uv sync` ottenga esattamente lo stesso ambiente. La cartella `.venv`, invece, non si
        condivide, perché pesa centinaia di megabyte e si ricrea a partire da `uv.lock` in circa un minuto.
    """)
    nb.md("""
        Negli esempi che si trovano in rete compare spesso il comando `!pip install nome`, scritto dentro
        una cella di un notebook. Nel progetto non lo usiamo, perché installa la libreria nell'ambiente
        senza registrarla nei file del progetto. Di conseguenza `pyproject.toml` e `uv.lock` restano come
        prima, il collega che lancia `uv sync` non riceve la libreria, e al successivo `uv sync` la
        libreria sparisce anche dal nostro ambiente, che il comando rimette esattamente come lo descrive
        `uv.lock`. Le librerie si aggiungono invece con `uv add`, che vediamo nella prossima sezione.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Un ambiente per progetto", intro="""
        Un notebook può funzionare sul nostro PC e non partire su quello di un collega, perché lui ha
        installato tempo fa, per un altro progetto, una versione di pandas con cui il nostro codice dà
        errore. Il problema nasce dal fatto che un solo Python condiviso tra più progetti ha una sola
        versione di ogni libreria, che può andare bene per un progetto e non per un altro. Per questo ogni
        progetto ha il suo ambiente virtuale, cioè una cartella con un Python e le versioni delle librerie
        che servono a quel progetto.
    """)
    nb.md("""
        Nel nostro progetto l'ambiente è la cartella `.venv`, e il kernel del notebook usa il Python che
        sta lì dentro. Lo abbiamo controllato nel primo notebook con `sys.executable`, e la cella seguente
        lo ripete chiedendo anche a pandas dove si trova il suo file principale, che si legge
        nell'attributo `__file__` del modulo. Entrambi i percorsi passano per `.venv`, perché anche le
        librerie sono installate dentro l'ambiente.
    """)
    nb.code("""
        import sys

        import pandas as pd

        print(sys.executable)
        print(pd.__file__)
    """)
    nb.md("""
        Le librerie dell'ambiente si gestiscono con uv dal terminale di VS Code, che si apre con
        **Terminal → New Terminal** e parte già nella cartella del progetto. I comandi che servono nella
        pratica sono quattro, e si scrivono nel terminale, non in una cella del notebook:

        ```bash
        uv add matplotlib       # aggiunge la libreria a pyproject.toml, aggiorna uv.lock e la installa
        uv remove matplotlib    # toglie la libreria dal progetto
        uv sync                 # rimette .venv esattamente come la descrive uv.lock
        uv run spesa.py         # esegue un file Python con il Python di .venv
        ```
    """)
    nb.md("""
        Il comando `uv add` è quello che usa chi aggiunge una libreria al progetto, mentre `uv sync` è
        quello che usa chi riceve il progetto aggiornato o vuole ricreare un ambiente che non funziona più.
        Dopo un `uv add` il kernel già in esecuzione non vede la nuova libreria, quindi prima di scrivere
        l'`import` lo si riavvia con **Restart**. Il comando `uv run`, infine, esegue un programma dentro
        l'ambiente senza bisogno di attivarlo prima, e nella prossima sezione lo usiamo per gli script.
    """)
    nb.md("""
        Quando un `import` fallisce con un `ModuleNotFoundError`, conviene controllare due cose
        nell'ordine. Se la libreria non compare in `pyproject.toml`, manca dal progetto e si aggiunge con
        `uv add`. Se invece compare e `uv sync` risponde che è tutto a posto, la libreria è installata, ma
        il notebook la cerca in un altro Python, perché il kernel scelto non è quello di `.venv`. In questo
        caso si cambia kernel con **Select Kernel**, senza installare nulla una seconda volta.
    """)
    nb.box("nota", """
        uv non è l'unico strumento per gestire gli ambienti. La coppia `venv` e `pip`, inclusa in Python,
        segue la stessa idea ma richiede più passaggi a mano e non produce un file come `uv.lock`; conda è
        diffuso in ambito scientifico, e Poetry svolge un lavoro simile a quello di uv. Chi eredita un
        progetto usa lo strumento che vi trova, riconoscibile da file come `environment.yml` per conda o
        `poetry.lock` per Poetry.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Script e notebook", intro="""
        Il notebook è lo strumento adatto all'esplorazione, perché permette di provare una cella, guardare
        il risultato e cambiare strada. Uno script è invece un file `.py` che esegue sempre le stesse
        istruzioni dall'inizio alla fine, senza che nessuno debba intervenire, ed è la forma giusta per
        un'operazione da ripetere, come un report che parte ogni mattina o un controllo da lanciare ogni
        lunedì. Quando il codice di un notebook è diventato stabile, conviene quindi trasformarlo in uno
        script.
    """)
    nb.md('''
        Per creare uno script usiamo **File → New File** in VS Code e salviamo il file con il nome
        `spesa.py` nella cartella principale del progetto, accanto a `pyproject.toml`. Il file contiene
        una docstring che dice a che cosa serve, una funzione e le righe che la usano:

        ```python
        """Totale della spesa della settimana."""


        def totale(prezzi):
            """Somma dei prezzi di una lista di prodotti."""
            return sum(prezzi)


        scontrino = [3.5, 2.2, 4.8, 1.9, 14.9]
        print(f"Totale della spesa: {totale(scontrino):.2f} euro")
        ```
    ''')
    nb.md("""
        Lo script si lancia dal terminale, nella cartella del progetto, con `uv run`, che avvia il Python
        di `.venv` sul file, esegue il codice e termina:

        ```bash
        uv run spesa.py
        ```

        Il terminale stampa la riga `Totale della spesa: 27.30 euro`. Non servono celle né un kernel, e per
        questo lo stesso comando si può affidare a un'attività pianificata, che lo lancia a un'ora
        stabilita anche quando nessuno è davanti al PC.
    """)
    nb.md("""
        Lo stesso codice, incollato in una cella, stampa la stessa riga, perché una cella e uno script
        eseguono le istruzioni Python nello stesso modo. Le differenze stanno nel contorno. In uno script
        l'ultima espressione non viene mostrata, quindi un nome lasciato da solo sull'ultima riga non
        stampa nulla e va messo dentro un `print`. I percorsi relativi, inoltre, partono dalla cartella da
        cui si lancia lo script e non da quella del notebook: dalla cartella principale del progetto i dati
        si trovano in `Dati/`, senza il `../` che usiamo nei notebook.
    """)
    nb.code('''
        def totale(prezzi):
            """Somma dei prezzi di una lista di prodotti."""
            return sum(prezzi)


        scontrino = [3.5, 2.2, 4.8, 1.9, 14.9]
        print(f"Totale della spesa: {totale(scontrino):.2f} euro")
    ''')
    nb.md("""
        Quando lanciamo `uv run spesa.py`, Python assegna al file il nome speciale `__main__`, che si legge
        nella variabile `__name__`; se invece un altro file importa il nostro con `import spesa`, il nome è
        `spesa`. Per questo negli script si trova spesso il controllo `if __name__ == "__main__":`, che
        esegue il blocco sottostante solo quando il file è il programma lanciato. Lì si mettono le righe
        che fanno il lavoro, mentre le funzioni definite sopra restano utilizzabili da altri file con un
        `import`. Anche il notebook, per Python, è il programma principale, e infatti nella cella seguente
        `__name__` vale `'__main__'`.
    """)
    nb.code("__name__")
    nb.hands_on(
        richiesta="""
            Nella cella le righe che fanno il lavoro stanno dentro il blocco `if`, ma la condizione è
            incompleta. Al posto dei `...` scrivi il nome che Python dà al programma lanciato, in modo che
            il blocco venga eseguito e la cella stampi `Totale della spesa: 27.30 euro`.
        """,
        starter='''
            def totale(prezzi):
                """Somma dei prezzi di una lista di prodotti."""
                return sum(prezzi)


            if __name__ == "...":
                scontrino = [3.5, 2.2, 4.8, 1.9, 14.9]
                riga = f"Totale della spesa: {totale(scontrino):.2f} euro"
                print(riga)
        ''',
        soluzione='''
            def totale(prezzi):
                """Somma dei prezzi di una lista di prodotti."""
                return sum(prezzi)


            if __name__ == "__main__":
                scontrino = [3.5, 2.2, 4.8, 1.9, 14.9]
                riga = f"Totale della spesa: {totale(scontrino):.2f} euro"
                print(riga)  # Output: Totale della spesa: 27.30 euro
        ''',
        verifica="""
            assert riga == "Totale della spesa: 27.30 euro", "❌ il blocco if non è stato eseguito: la condizione confronta __name__ con \\"__main__\\""
        """,
        prova_anche='scrivi `"spesa"` al posto di `"__main__"` ed esegui di nuovo: la cella non stampa nulla, perché nel notebook il nome è `__main__`.',
    )

    # ------------------------------------------------------------------ 4
    nb.sezione("Ruff", intro="""
        Ruff è uno strumento che svolge due compiti. Come formatter, con il comando `ruff format`, rimette
        in forma il codice secondo le regole di PEP 8 viste nel notebook sul codice leggibile, sistemando
        spazi, indentazione e righe vuote senza cambiare il comportamento del programma. Come linter, con
        il comando `ruff check`, segnala i problemi che non riguardano la forma, per esempio un import che
        non serve o una variabile calcolata e mai usata. Nel progetto Ruff è già installato, tra gli
        strumenti di sviluppo che abbiamo letto in `pyproject.toml`.
    """)
    nb.md("""
        In VS Code si installa l'estensione **Ruff**, pubblicata da Astral, dal pannello delle estensioni.
        Da quel momento gli avvisi del linter compaiono nell'editor come sottolineature, con il codice e il
        messaggio che si leggono passando sopra con il mouse. Per rimettere in forma il file a ogni
        **Ctrl+S** si aggiungono le righe seguenti al file `settings.json`, che si apre dalla palette dei
        comandi (**Ctrl+Shift+P**) con **Preferences: Open User Settings (JSON)**:

        ```json
        {
            "[python]": {
                "editor.defaultFormatter": "charliermarsh.ruff",
                "editor.formatOnSave": true
            }
        }
        ```
    """)
    nb.md("""
        Il formatter, applicato alla cella scritta senza regole del notebook sul codice leggibile, aggiunge
        gli spazi attorno a `=` e agli operatori e dopo le virgole, porta l'indentazione a quattro spazi e
        mette due righe vuote prima e dopo il `def`. I nomi `Voti`, `Calc` e `x` restano invece com'erano,
        perché scegliere un nome che dica che cosa contiene la variabile è un lavoro che Ruff lascia a noi.

        ```python
        # prima
        Voti=[7,8 ,6,9,5]
        def Calc(v):
          m=sum(v)/len(v)
          return m

        # dopo ruff format
        Voti = [7, 8, 6, 9, 5]


        def Calc(v):
            m = sum(v) / len(v)
            return m
        ```
    """)
    nb.md("""
        Gli avvisi del linter hanno un codice formato da una lettera, che indica la famiglia di regole, e
        da un numero, che indica la regola. La tabella riporta i tre avvisi che si incontrano più spesso.

        | Codice | Avviso | Che cosa vuol dire |
        |---|---|---|
        | `F401` | `` `math` imported but unused `` | una libreria importata e mai usata |
        | `F841` | `` Local variable `totale` is assigned to but never used `` | una variabile calcolata e mai letta |
        | `E501` | `Line too long (117 > 100)` | una riga oltre il limite fissato in `pyproject.toml` |
    """)
    nb.md("""
        Il comportamento di Ruff si configura nella sezione `[tool.ruff]` di `pyproject.toml`, che la cella
        seguente legge dal dizionario `progetto` costruito all'inizio del notebook. La voce `line-length`
        fissa a 100 caratteri il limite delle righe, `target-version` indica la versione di Python per cui
        scriviamo e `select` sceglie le famiglie di regole: `E` e `W` per lo stile di PEP 8, `F` per gli
        import inutilizzati e i nomi non definiti, `I` per l'ordine degli import. L'estensione di VS Code e
        il terminale leggono la stessa configurazione, quindi danno gli stessi avvisi.
    """)
    nb.code("""
        progetto["tool"]["ruff"]
    """)
    nb.md("""
        Dal terminale, nella cartella del progetto, Ruff si lancia con `uv run`, che usa la versione
        installata nel progetto. Il primo comando elenca gli avvisi, il secondo corregge quelli che sa
        correggere e il terzo rimette in forma il file:

        ```bash
        uv run ruff check spesa.py
        uv run ruff check --fix spesa.py
        uv run ruff format spesa.py
        ```
    """)
    nb.md("""
        Le correzioni automatiche hanno un limite preciso. Il comando `check --fix` toglie gli import
        inutilizzati e riordina quelli rimasti, che sono modifiche sicure, ma non elimina una variabile mai
        usata, perché quella riga potrebbe essere un errore da capire e non un avanzo da cancellare. Il
        comando `format` spezza su più righe un'istruzione troppo lunga, ma non divide una stringa, e in
        quel caso l'avviso `E501` resta finché non dividiamo la stringa noi, come nella cella seguente.
    """)
    nb.code("""
        soglia = 30

        messaggio = (
            f"Trovati 2 giorni sopra i {soglia} gradi nel file meteo_luglio.csv: "
            "controllare il sensore sul balcone"
        )
        messaggio
    """)
    nb.md("""
        Quando due stringhe scritte una dopo l'altra stanno dentro le stesse parentesi, Python le unisce in
        una stringa sola, e in questo modo un testo lungo si distribuisce su più righe senza cambiare. Il
        prefisso `f` serve soltanto sui pezzi che contengono delle graffe da sostituire.
    """)
    nb.hands_on(
        richiesta="""
            La riga di `avviso` è lunga 122 caratteri e Ruff la segnalerebbe con `E501`. Scrivi in
            `avviso_diviso` lo stesso testo diviso in due pezzi tra parentesi, come nell'esempio, con la
            `f` solo sul pezzo che contiene `{citta}`. La cella stampa `True` quando i due testi coincidono.
        """,
        starter="""
            citta = "Bologna"
            avviso = f"Domani a {citta} è prevista pioggia dalle 14 alle 18: conviene rimandare la partita di calcetto a giovedì sera"

            avviso_diviso = (
                ...
            )
            print(avviso_diviso == avviso)
        """,
        soluzione="""
            citta = "Bologna"
            avviso = f"Domani a {citta} è prevista pioggia dalle 14 alle 18: conviene rimandare la partita di calcetto a giovedì sera"

            avviso_diviso = (
                f"Domani a {citta} è prevista pioggia dalle 14 alle 18: "
                "conviene rimandare la partita di calcetto a giovedì sera"
            )
            print(avviso_diviso == avviso)  # Output: True
        """,
        verifica="""
            assert isinstance(avviso_diviso, str), "❌ avviso_diviso: due stringhe tra parentesi, una dopo l'altra"
            assert avviso_diviso == avviso, "❌ avviso_diviso: il testo deve essere identico a quello di avviso, spazi compresi"
        """,
    )
    nb.box("nota", """
        Ruff controlla anche i notebook. Il comando `uv run ruff check nome.ipynb` esamina le celle una per
        una con la stessa configurazione dei file `.py`, e in VS Code l'estensione mostra gli avvisi
        direttamente nelle celle.
    """)

    nb.md("Riassunto in una pagina: [uv, il progetto e gli script](../Schede/Scheda_uv_e_script.md).")

    # ------------------------------------------------------------------ Extra
    nb.sezione("Extra", """
        Questa sezione raccoglie tre esercizi brevi sui punti principali del notebook, pensati per il
        ripasso a casa, e durante la lezione la saltiamo. Il secondo chiede di creare un file nella
        cartella del progetto e di lanciarlo dal terminale di VS Code, e lo stesso vale, se vuoi
        controllare la tua risposta, per il terzo.
    """)
    nb.esercizio(
        titolo="La libreria che manca",
        scenario="""
            Un collega, prima di andare in ferie, ti ha lasciato un notebook che disegna alcuni grafici con
            Plotly e altri con matplotlib, una libreria che nel progetto non c'è. Vogliamo controllare che
            Plotly sia installato, sapere con quale comando si aggiunge matplotlib e lasciare scritto al
            collega il comando con cui, al rientro, riceverà la libreria. Alla fine `versione_plotly`
            contiene la versione installata di Plotly, una stringa di numeri separati da punti, e
            `comando_aggiungi` e `comando_collega` contengono i due comandi di uv, scritti come nel
            terminale.
        """,
        richiesta="""
            1. Importa `plotly` e metti in `versione_plotly` il valore del suo attributo `__version__`.
            2. Metti in `comando_aggiungi` il comando del terminale che aggiunge `matplotlib` al progetto.
            3. Metti in `comando_collega` il comando che il collega lancia per ricevere la libreria aggiunta.
        """,
        suggerimento="i due comandi sono nella sezione sull'ambiente per progetto, e si scrivono tutti in minuscolo.",
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
            comando_aggiungi = "uv add matplotlib"
            comando_collega = "uv sync"

            print(versione_plotly, comando_aggiungi, comando_collega)
        """,
        verifica="""
            import plotly

            assert versione_plotly == plotly.__version__, "❌ versione_plotly: l'attributo __version__ della libreria plotly"
            assert comando_aggiungi.strip() == "uv add matplotlib", "❌ comando_aggiungi: il comando uv che aggiunge una libreria, seguito dal nome"
            assert comando_collega.strip() == "uv sync", "❌ comando_collega: il comando uv che ricrea l'ambiente dai file del progetto"
        """,
        perche=(
            "Chi aggiunge una libreria usa `uv add`, che aggiorna `pyproject.toml` e `uv.lock`; chi riceve il "
            "progetto aggiornato usa `uv sync`, che legge quei due file e installa quello che manca."
        ),
    )
    nb.esercizio(
        titolo="Da notebook a script",
        scenario="""
            Sul balcone hai una piccola stazione meteo, e ogni domenica vuoi conoscere la temperatura media
            della settimana con un solo comando nel terminale, senza aprire un notebook. Le temperature di
            questa settimana sono `14.5, 16.0, 15.2, 13.8, 15.5`, e lo script `media_temperature.py`,
            lanciato con `uv run`, stampa la riga `Temperatura media: 15.0 gradi`. Per controllare che lo
            script sia stato eseguito, copiamo nel notebook la riga che compare nel terminale.
        """,
        richiesta="""
            1. Crea in VS Code il file `media_temperature.py` nella cartella principale del progetto,
               accanto a `pyproject.toml`.
            2. Scrivi nel file una funzione `media(valori)` che restituisce `sum(valori) / len(valori)`.
            3. Sotto la funzione, dentro un blocco `if __name__ == "__main__":`, scrivi la lista
               `temperature` e un `print` con una f-string che stampa la media con una cifra decimale.
            4. Lancia lo script dal terminale con `uv run media_temperature.py`.
            5. Copia la riga stampata dal terminale nella variabile `output_script` della cella qui sotto.
        """,
        suggerimento="parti dal file `spesa.py` della sezione sugli script e cambia nomi, calcolo e testo; il formato `:.1f` dentro le graffe dà una cifra decimale.",
        starter="""
            # il codice sta nel file media_temperature.py; qui solo la riga copiata dal terminale
            output_script = "..."
            output_script
        """,
        soluzione='''
            # contenuto di media_temperature.py, nella cartella principale del progetto
            def media(valori):
                """Media aritmetica di una lista di numeri."""
                return sum(valori) / len(valori)


            if __name__ == "__main__":
                temperature = [14.5, 16.0, 15.2, 13.8, 15.5]
                print(f"Temperatura media: {media(temperature):.1f} gradi")

            # la riga stampata dal terminale dopo uv run media_temperature.py
            output_script = "Temperatura media: 15.0 gradi"
        ''',
        verifica="""
            assert output_script.strip() == "Temperatura media: 15.0 gradi", "❌ output_script: la riga stampata dal terminale, tale e quale"
        """,
        perche=(
            "Il file sta nella cartella principale, che è anche quella in cui si apre il terminale, quindi "
            "`uv run media_temperature.py` funziona senza indicare percorsi. La riga va copiata dal terminale "
            "e non ricalcolata nel notebook, perché è la prova che lo script è stato eseguito."
        ),
    )
    nb.esercizio(
        titolo="Pulizia con Ruff",
        scenario="""
            Un amico ha scritto lo script `meteo_report.py` qui sotto e vuole metterlo in un repository
            condiviso, dove ogni file deve passare `uv run ruff check` senza avvisi. Prima di lanciare Ruff
            proviamo a fare il suo lavoro, leggendo il file e scrivendo i codici degli avvisi che darebbe,
            e poi riscriviamo il codice in modo che non ne dia nessuno e stampi lo stesso testo.

            ```python
            import math

            soglia = 30
            giorni_caldi = ["12 luglio", "13 luglio"]


            def riepilogo(giorni_caldi, soglia):
                n = len(giorni_caldi)
                totale = 0
                return f"Trovati {n} giorni sopra i {soglia} gradi nel file meteo_luglio.csv: controllare il sensore sul balcone"


            print(riepilogo(giorni_caldi, soglia))
            ```
        """,
        richiesta="""
            1. Metti in `avvisi` la lista dei codici Ruff che il file farebbe scattare, come stringhe, uno per problema.
            2. Riscrivi nella cella il codice corretto, con una docstring per `riepilogo`, in modo che non dia
               avvisi e stampi lo stesso testo.
            3. Se vuoi controllare la tua risposta, salva l'originale in `meteo_report.py` nella cartella
               principale del progetto e lancia `uv run ruff check meteo_report.py`.
        """,
        suggerimento="i codici sono nella tabella della sezione su Ruff, e la stringa lunga si divide in due pezzi tra parentesi.",
        starter="""
            avvisi = [...]

            # qui sotto il codice corretto
            soglia = 30
            giorni_caldi = ["12 luglio", "13 luglio"]


            def riepilogo(giorni_caldi, soglia):
                ...


            print(riepilogo(giorni_caldi, soglia))
        """,
        soluzione='''
            # un import mai usato, una variabile mai letta, una riga da 117 caratteri
            avvisi = ["F401", "F841", "E501"]

            soglia = 30
            giorni_caldi = ["12 luglio", "13 luglio"]


            def riepilogo(giorni_caldi, soglia):
                """Una riga di testo con il numero di giorni sopra la soglia."""
                n = len(giorni_caldi)
                return (
                    f"Trovati {n} giorni sopra i {soglia} gradi nel file meteo_luglio.csv: "
                    "controllare il sensore sul balcone"
                )


            print(riepilogo(giorni_caldi, soglia))
        ''',
        verifica="""
            assert sorted(avvisi) == ["E501", "F401", "F841"], "❌ avvisi: tre codici come stringhe, per l'import inutilizzato, la variabile mai letta e la riga troppo lunga"
            assert riepilogo(["12 luglio", "13 luglio"], 30) == "Trovati 2 giorni sopra i 30 gradi nel file meteo_luglio.csv: controllare il sensore sul balcone", "❌ riepilogo: il testo in uscita deve restare identico"
            assert riepilogo.__doc__, "❌ riepilogo: manca la docstring"
        """,
        perche=(
            "L'import di `math` e la variabile `totale` non servono a nulla e si tolgono. La riga lunga si "
            "divide in due pezzi tra parentesi, il testo in uscita resta identico e Ruff non segnala più "
            "alcun avviso."
        ),
    )
    return nb
