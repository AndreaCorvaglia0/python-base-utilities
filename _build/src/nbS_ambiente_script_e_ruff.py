"""S · Ambiente, script e Ruff (solo aula Avanzata, modulo 1, dopo il notebook 03).

Notebook di spiegazione, senza esercizi: prepara la dimostrazione nella cartella `demo/` e l'Esercitazione 1
dell'Avanzata, che la fa rifare nella cartella `esercizio/`. Sta in `Aula_Avanzata/Modulo_1/Script_uv_Ruff/`, quindi
la radice dell'aula è `../../` e la demo è in `demo/`.
"""

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
            "Il notebook spiega che cosa fa uv e che cos'è un ambiente virtuale, quali file descrivono un "
            "progetto, quando conviene uno script al posto di un notebook e come si importa una funzione da un "
            "altro file; presenta poi Ruff come formatter e come linter e raccoglie i passi della dimostrazione "
            "che l'Esercitazione 1 fa rifare."
        ),
        obiettivi=[
            "spiegare che cosa fa uv, a che cosa serve un ambiente virtuale e quali file descrivono un progetto",
            "scrivere uno script che importa una funzione da un altro file e lanciarlo con `uv run`",
            "usare Ruff come formatter e come linter, dal terminale e in VS Code",
        ],
        tempo=30,
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("uv e l'ambiente virtuale", intro="""
        uv è il programma con cui gestiamo i progetti Python del corso. Sa installare la versione di
        Python richiesta da un progetto, creare l'ambiente virtuale del progetto, installare al suo interno
        le librerie e lanciare i programmi con il Python giusto. Lo abbiamo già usato all'inizio del corso, quando il
        comando `uv sync`, lanciato nella cartella del corso, ha preparato tutto quello che serve ai
        notebook. In questo notebook vediamo che cosa ha fatto quel comando e come si usa uv per un
        progetto nuovo.
    """)
    nb.md("""
        Un ambiente virtuale è una cartella, che nei progetti gestiti con uv si chiama `.venv`, con un
        interprete Python e le librerie di un solo progetto. Avere un ambiente per progetto porta alcuni
        vantaggi concreti. Due progetti possono usare versioni diverse della stessa libreria senza
        disturbarsi, e aggiornare una libreria in uno non cambia nulla negli altri. L'ambiente sta nella
        cartella del progetto, quindi si crea senza diritti di amministratore, e si può cancellare e
        ricostruire in ogni momento, perché quello che serve a ricrearlo è scritto nei file del progetto.
    """)
    nb.md("""
        Il kernel di questo notebook usa il Python dell'ambiente del corso, come abbiamo controllato nel
        primo notebook con `sys.executable`. La cella seguente lo ripete e chiede anche a pandas dove si
        trova il suo file principale, che si legge nell'attributo `__file__` del modulo. Entrambi i
        percorsi passano per `.venv`, perché anche le librerie sono installate dentro l'ambiente, nella
        sottocartella `site-packages`.
    """)
    nb.code("""
        import sys

        import pandas as pd

        print(sys.executable)
        print(pd.__file__)
    """)
    nb.md("""
        Una libreria installata, quindi, è una cartella di file, in gran parte file `.py` scritti in
        Python come i nostri. La cella seguente elenca i file della sottocartella `io/excel` di pandas, che
        contiene il codice per leggere e scrivere i file Excel. Tra questi c'è `_openpyxl.py`, che
        ritroveremo nella dimostrazione, quando un messaggio di errore indicherà proprio quel file.
    """)
    nb.code("""
        from pathlib import Path

        cartella_pandas = Path(pd.__file__).parent
        sorted(f.name for f in (cartella_pandas / "io" / "excel").glob("*.py"))
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("I file del progetto", intro="""
        Un progetto gestito con uv è descritto da pochi file di testo, che stanno nella cartella
        principale accanto al codice. Nella cartella del corso, due livelli sopra questo notebook, sono
        gli ultimi quattro elementi dello schema seguente.
    """)
    nb.md("""
        ```
        Aula_Avanzata/
            Modulo_1/ ... Modulo_4/   i notebook, un modulo per cartella
            Soluzioni/                le soluzioni degli esercizi
            Dati/   Schede/           i dati del corso e le schede di riepilogo
            pyproject.toml            la descrizione del progetto e l'elenco delle librerie
            uv.lock                   le versioni esatte di tutto quello che è installato
            .python-version           la versione di Python del progetto
            .venv/                    l'ambiente virtuale, creato da uv sync
        ```
    """)
    nb.md("""
        Il file `pyproject.toml` è scritto nel formato TOML, fatto di sezioni tra parentesi quadre e di
        righe `chiave = valore`, e si apre in VS Code come qualunque file di testo. La sezione `[project]`
        contiene il nome del progetto, la versione minima di Python e, alla voce `dependencies`, le
        librerie di cui il programma ha bisogno. Lo stesso contenuto si legge anche da Python con il modulo
        `tomllib` della libreria standard, che trasforma il testo in un dizionario con una chiave per
        sezione.
    """)
    nb.code("""
        import tomllib

        testo = Path("../../pyproject.toml").read_text(encoding="utf-8")
        progetto = tomllib.loads(testo)
        print(progetto["project"]["dependencies"])
        print(progetto["dependency-groups"]["dev"])
    """)
    nb.md("""
        Ogni libreria compare con un vincolo di versione largo, come `pandas>=3.0`, che accetta pandas
        dalla versione 3.0 in su. La seconda riga viene dalla sezione `[dependency-groups]`, che alla voce
        `dev` raccoglie gli strumenti di sviluppo, cioè quelli che servono a chi scrive il codice ma non al
        programma per funzionare: nel nostro caso Ruff, che vediamo più avanti. Le due liste non si
        modificano a mano, perché le aggiorna uv ogni volta che aggiungiamo o togliamo una libreria.
    """)
    nb.md("""
        Gli altri file completano la descrizione. Il file `uv.lock` elenca la versione esatta di ogni
        libreria installata, comprese quelle da cui dipendono le librerie di `pyproject.toml`, e permette a
        chi riceve il progetto di ricostruire lo stesso identico ambiente su un altro PC. Il file
        `.python-version` indica la versione di Python che uv usa per creare l'ambiente, mentre `.venv` è
        l'ambiente stesso, che uv crea e aggiorna a partire dagli altri file. La tabella seguente dice chi
        scrive ciascun file e se si condivide con i colleghi insieme al codice.
    """)
    nb.md("""
        | File | Chi lo scrive | Si condivide |
        |---|---|---|
        | `pyproject.toml` | uv, per le librerie; a mano, per la configurazione degli strumenti | sì |
        | `uv.lock` | soltanto uv | sì |
        | `.python-version` | chi crea il progetto, oppure `uv init` | sì |
        | `.venv/` | uv, con `uv sync` e `uv run` | no, perché pesa centinaia di megabyte e si ricrea con `uv sync` |
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Aggiungere e togliere librerie", intro="""
        Le librerie di un progetto si gestiscono con pochi comandi di uv, che si scrivono nel terminale e
        non in una cella del notebook. In VS Code il terminale si apre con **Terminal → New Terminal** e
        parte dalla cartella aperta nell'editor, che per noi è la cartella del corso. Le librerie
        arrivano da PyPI, il catalogo pubblico dei pacchetti Python, quindi i comandi che le installano
        hanno bisogno della connessione a internet. Quelli che si usano di più sono quattro.
    """)
    nb.md("""
        ```bash
        uv add matplotlib       # aggiunge la libreria a pyproject.toml e uv.lock e la installa
        uv add --dev ruff       # aggiunge uno strumento di sviluppo, nel gruppo dev
        uv remove matplotlib    # toglie la libreria dai file del progetto e da .venv
        uv sync                 # rimette .venv esattamente come lo descrive uv.lock
        ```

        Il comando `uv add` è quello di chi aggiunge una libreria, mentre `uv sync` è quello di chi riceve
        il progetto aggiornato da un collega o vuole ricostruire un ambiente che non funziona più.
    """)
    nb.md("""
        Dopo un `uv add` nell'ambiente del corso il kernel già avviato non vede la nuova libreria, quindi
        prima di scrivere l'`import` lo si riavvia con **Restart**. Negli esempi in rete compare spesso
        `pip install`, anche dentro una cella come `!pip install`, ma nei progetti gestiti con uv non si
        usa. Un ambiente creato da uv non contiene pip, quindi il comando, se trova un pip sul PC, usa
        quello di un altro Python e installa la libreria lì invece che in `.venv`. Anche quando funziona,
        la libreria non entra in `pyproject.toml` e `uv.lock`, quindi il collega non la riceve e il
        successivo `uv sync` la toglie.
    """)
    nb.md("""
        Tutti i comandi di uv lavorano sul progetto della cartella in cui si trova il terminale. uv cerca
        un file `pyproject.toml` in quella cartella e, se non lo trova, risale una cartella alla volta fino
        a trovarne uno. In un terminale aperto sulla cartella del corso, o su una sua sottocartella senza
        `pyproject.toml` come `Modulo_1`, i comandi agiscono quindi sul progetto del corso e sul suo
        `.venv`. La cartella `demo/` della dimostrazione ha invece un `pyproject.toml` suo, e un terminale
        aperto lì lavora su quel progetto, con un ambiente separato.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Notebook e script", intro="""
        Un notebook è lo strumento adatto all'esplorazione, perché permette di eseguire una cella alla
        volta, guardare il risultato e cambiare strada. Uno script è invece un file di testo con
        estensione `.py`, che Python esegue dall'inizio alla fine con un solo comando, sempre nello stesso
        ordine e senza che nessuno debba intervenire. Quando un'analisi è diventata stabile e va ripetuta,
        per esempio ogni mattina o a ogni nuovo file di dati, conviene trasformarla in uno script.
    """)
    nb.md("""
        Lo script ha alcuni vantaggi pratici. Si lancia dal terminale con `uv run nome.py`, quindi si può
        affidare a un'attività pianificata che lo esegue a un'ora stabilita, anche quando nessuno è
        davanti al PC. Ogni esecuzione riparte da zero, quindi il risultato non dipende da quello che è
        stato eseguito prima, mentre in un notebook può dipendere dall'ordine in cui abbiamo eseguito le
        celle. Le funzioni definite in uno script, infine, si riusano da altri file con un `import`, come
        vediamo nella prossima sezione.
    """)
    nb.md("""
        Uno script è anche più semplice da leggere fuori da VS Code. Un notebook, infatti, è un file JSON
        che contiene, oltre al codice, il testo delle celle Markdown, gli output e alcune informazioni per
        Jupyter, e nel controllo di versione, come Git, una modifica di una riga si confonde tra tutto il
        resto. La cella seguente stampa l'inizio del file di questo notebook, cioè quello che si vede
        aprendolo con un editor di testo.
    """)
    nb.code("""
        print(Path("Ambiente_script_e_Ruff.ipynb").read_text(encoding="utf-8")[:200])
    """)
    nb.md("""
        Quando il codice passa da un notebook a uno script cambiano due dettagli. In uno script l'ultima
        espressione non viene mostrata, quindi un nome lasciato da solo sull'ultima riga non stampa nulla,
        e quello che vogliamo vedere va messo dentro un `print`. I percorsi relativi, inoltre, partono
        dalla cartella in cui si trova il terminale e non da quella del file: lo script della
        dimostrazione, lanciato dalla cartella `demo/`, scrive lì il suo file Excel.
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Importare una funzione da un altro file", intro="""
        Il programma della dimostrazione è diviso in due file, che stanno nella cartella `demo/` accanto a
        questo notebook. Il file `calcoli.py` definisce le funzioni che fanno i conti, mentre `main.py` è lo
        script che si lancia e che le usa. La cella seguente stampa `calcoli.py`, scritto apposta in
        disordine, con spazi mancanti, un import che non serve e una variabile mai usata, perché nella
        dimostrazione lo sistemiamo con Ruff.
    """)
    nb.code("""
        print(Path("demo/calcoli.py").read_text(encoding="utf-8"))
    """)
    nb.md("""
        Il file `main.py` comincia con due `import` e poi usa le funzioni di `calcoli.py` per stampare il
        totale e il prezzo medio della spesa della settimana. Le ultime righe costruiscono con pandas una
        tabella con i prodotti e i prezzi e la salvano nel file Excel `spesa.xlsx`.
    """)
    nb.code("""
        print(Path("demo/main.py").read_text(encoding="utf-8"))
    """)
    nb.md("""
        La riga `from calcoli import totale, prezzo_medio` ha la stessa forma di `from math import sqrt`,
        che abbiamo usato nel notebook 01, e `import pandas as pd` è l'import di sempre. Per Python,
        infatti, `calcoli`, `math` e `pandas` sono tutti moduli, e cambia soltanto il posto in cui si
        trovano. Python cerca un modulo in un elenco ordinato di cartelle, `sys.path`, e usa il primo che
        trova. La cella seguente stampa il percorso del modulo `json` della libreria standard e poi
        l'elenco delle cartelle.
    """)
    nb.code("""
        import json

        print(json.__file__)
        for cartella in sys.path:
            print(cartella)
    """)
    nb.md("""
        L'elenco contiene le cartelle della libreria standard, che arriva con il Python installato da uv e
        contiene `json`, e la cartella `site-packages` dentro `.venv`, dove uv installa pandas e le altre
        librerie del progetto. Nel notebook compare anche la cartella corrente, cioè quella del notebook,
        di solito scritta come una riga vuota. Quando lanciamo uno script, invece, Python mette in testa
        all'elenco la cartella che contiene il file, ed è per questo che `main.py` trova `calcoli.py`, che
        gli sta accanto.
    """)
    nb.md("""
        Un `import` esegue il file importato dall'inizio alla fine, una volta sola, e poi rende disponibili
        i nomi che ha definito. Per `calcoli.py` significa definire le due funzioni, ma un `print` scritto
        fuori dalle funzioni comparirebbe nel terminale prima di tutto quello che stampa `main.py`. Per
        distinguere i due casi Python dà a ogni file eseguito un nome, che si legge nella variabile `__name__`: vale
        `"__main__"` nel file lanciato con `uv run` e il nome del modulo, qui `"calcoli"`, in un file
        importato. Anche il notebook è il programma principale, come mostra la cella seguente.
    """)
    nb.code("__name__")
    nb.md("""
        Per questo negli script si trova spesso, in fondo al file, un blocco `if __name__ == "__main__":`
        con le righe che fanno il lavoro, che vengono eseguite quando lanciamo il file ma non quando un
        altro file lo importa per usarne le funzioni. Dopo il primo import, inoltre, accanto a
        `calcoli.py` compare la cartella `__pycache__`, dove Python conserva una versione già tradotta del
        file per partire più in fretta la volta successiva. Si può ignorare, e VS Code, nella cartella del
        corso, non la mostra.
    """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Formattare il codice", intro="""
        Nel notebook 03 abbiamo visto le regole di PEP 8 sulla forma del codice: l'indentazione di quattro
        spazi, uno spazio attorno a `=` e agli operatori e dopo le virgole, due righe vuote prima e dopo
        una funzione e righe non troppo lunghe. Formattare il codice significa sistemarne la forma secondo
        queste regole senza cambiare quello che fa. Un formatter è il programma che lo fa al posto nostro,
        riscrivendo il file con gli spazi, le righe vuote e gli a capo al posto giusto, nello stesso modo
        in tutto il progetto.
    """)
    nb.md('''
        Applicato a `calcoli.py`, il formatter aggiunge gli spazi attorno a `=` e a `/`, toglie quelli
        dentro `sum( prezzi )`, separa le funzioni con due righe vuote e mette una riga vuota dopo la
        docstring del modulo:

        ```python
        """Le funzioni che servono per fare i conti della spesa."""

        import math


        def totale(prezzi):
            """La somma dei prezzi."""
            numero = len(prezzi)
            return sum(prezzi)


        def prezzo_medio(prezzi):
            """Il prezzo medio, cioè il totale diviso per il numero dei prodotti."""
            return sum(prezzi) / len(prezzi)
        ```
    ''')
    nb.md("""
        Il formatter cambia soltanto la forma. Non rinomina le variabili, perché scegliere un nome che dica
        che cosa contiene resta un lavoro nostro, e non toglie l'import di `math` né la variabile `numero`,
        anche se non servono a nulla. Non divide nemmeno una stringa troppo lunga: può spezzare
        un'istruzione su più righe dentro le parentesi, ma il testo tra virgolette resta intero, e la riga
        che lo contiene può restare oltre il limite.
    """)

    # ------------------------------------------------------------------ 7
    nb.sezione("Il linter", intro="""
        Un linter legge il codice senza eseguirlo e segnala gli errori probabili e le abitudini che
        portano a errori, come un import che non serve, una variabile calcolata e mai usata o un nome mai
        definito. Ogni segnalazione indica il file, la riga e un codice formato da una lettera, che indica
        la famiglia di regole, e da un numero. Le famiglie che usiamo sono quattro: `E` e `W` per lo stile
        di PEP 8, `F` per gli errori probabili e `I` per l'ordine degli import. Sui due file della
        dimostrazione, dopo la formattazione, il linter dà le quattro segnalazioni della tabella seguente.
    """)
    nb.md("""
        | Codice | Messaggio | Che cosa vuol dire | Come si corregge |
        |---|---|---|---|
        | `F401` | `` `math` imported but unused `` | un modulo importato e mai usato | `--fix` toglie l'import |
        | `F841` | `` Local variable `numero` is assigned to but never used `` | una variabile assegnata e mai letta | a mano |
        | `I001` | `Import block is un-sorted or un-formatted` | gli import non sono in ordine | `--fix` li riordina |
        | `E501` | `Line too long (104 > 100)` | una riga oltre i 100 caratteri | a mano |
    """)
    nb.md("""
        L'opzione `--fix` applica soltanto le correzioni sicure, che Ruff segna con `[*]` nell'elenco e
        che non cambiano il comportamento del programma. Per gli import la correzione è sicura: Ruff toglie
        quelli inutilizzati e riordina gli altri in gruppi, prima la libreria standard, poi le librerie
        installate e per ultimi i file del progetto. La riga di `F841` la lascia invece a noi, e conviene
        guardarla con attenzione, perché una variabile calcolata e mai usata a volte è il segno di un
        errore più sotto.
        Per `E501` non c'è una correzione automatica, perché dividere un testo è una scelta di chi scrive.
    """)

    # ------------------------------------------------------------------ 8
    nb.sezione("Ruff: formatter e linter insieme", intro="""
        Ruff è un unico programma che fa da formatter e da linter, con due comandi distinti: `ruff format`
        rimette in forma il codice e `ruff check` lo controlla. Nel progetto del corso è già installato,
        nel gruppo `dev` che abbiamo letto in `pyproject.toml`, e si configura nella sezione `[tool.ruff]`
        dello stesso file, che la cella seguente legge dal dizionario `progetto`.
    """)
    nb.code("""
        progetto["tool"]["ruff"]
    """)
    nb.md("""
        La voce `line-length` fissa a 100 caratteri il limite delle righe, `target-version` indica la
        versione di Python per cui scriviamo ed `extend-exclude` toglie dal controllo il file `corso.py`,
        che contiene le verifiche degli esercizi. La sottosezione `lint`, alla voce `select`, sceglie le
        famiglie di regole `E`, `F`, `W` e `I` viste sopra. Il terminale e l'estensione di VS Code leggono
        la stessa configurazione, e quindi danno le stesse segnalazioni.
    """)
    nb.md("""
        Dal terminale Ruff si lancia con `uv run`, che usa la versione installata nel progetto. Senza il
        nome di un file, i comandi lavorano su tutti i file Python, notebook compresi, della cartella del
        terminale e delle sue sottocartelle:

        ```bash
        uv run ruff format          # rimette in forma i file
        uv run ruff check           # elenca le segnalazioni
        uv run ruff check --fix     # applica le correzioni sicure
        ```

        Conviene seguire un ordine preciso: prima `check --fix`, poi le correzioni a mano di quello che
        resta, poi `format` e alla fine un ultimo `check`, che risponde `All checks passed!` quando non
        c'è più nulla da segnalare.
    """)
    nb.md("""
        In VS Code Ruff funziona attraverso l'estensione **Ruff**, pubblicata da Astral, che la cartella
        del corso propone tra le estensioni consigliate e imposta come formatter dei file Python. Il
        comando **Format Document**, con la scorciatoia **Shift+Alt+F**, rimette in forma il file aperto.
        Le segnalazioni del linter compaiono come sottolineature nel codice e nel pannello **Problems**, e
        su una riga sottolineata la scorciatoia **Ctrl+.** apre il menu **Quick Fix** con le correzioni
        disponibili. Chi vuole la formattazione a ogni salvataggio può attivare l'impostazione
        **Format On Save**.
    """)
    nb.md("""
        La riga troppo lunga di `main.py` si sistema a mano, dividendo la f-string in due pezzi scritti uno
        dopo l'altro dentro le parentesi del `print`. Python unisce due stringhe adiacenti in una stringa
        sola, quindi il testo stampato non cambia, e ciascun pezzo ha la sua `f` perché contiene delle
        graffe da sostituire. La cella seguente mostra la riga corretta, con i prezzi della dimostrazione.
    """)
    nb.code("""
        prezzi = [2.40, 1.15, 3.20, 4.50, 1.85]

        print(
            f"Prezzo medio di un prodotto: {sum(prezzi) / len(prezzi):.2f} euro, "
            f"calcolato su {len(prezzi)} prodotti"
        )
    """)

    # ------------------------------------------------------------------ 9
    nb.sezione("La dimostrazione", intro="""
        Nella dimostrazione mettiamo insieme quello che abbiamo visto. Partiamo dai due file della cartella
        `demo/`, costruiamo per loro un ambiente apposito, aggiungendo una libreria alla volta man mano che
        ci accorgiamo che manca, sistemiamo il codice con Ruff e lo lanciamo. La cartella `demo/` contiene
        il punto di partenza, quindi chi vuole può ripetere i comandi sul proprio PC mentre li eseguiamo
        insieme. Il progetto della demo parte senza librerie, come mostra la cella seguente.
    """)
    nb.code("""
        demo = tomllib.loads(Path("demo/pyproject.toml").read_text(encoding="utf-8"))
        demo["project"]
    """)
    nb.md("""
        La prima parte costruisce l'ambiente, con i passi seguenti.

        1. Apriamo un terminale nella cartella `demo/`, con il tasto destro sulla cartella nel pannello
           **Explorer** e la voce **Open in Integrated Terminal**, oppure con
           `cd Modulo_1/Script_uv_Ruff/demo` dalla cartella del corso.
        2. Lanciamo `uv run main.py`. uv crea `.venv` per il progetto della demo, e lo script si ferma
           alla riga dell'import con `ModuleNotFoundError: No module named 'pandas'`.
        3. Aggiungiamo la libreria con `uv add pandas`, che la scrive in `pyproject.toml`, aggiorna
           `uv.lock` e la installa insieme a numpy e alle altre librerie da cui dipende.
    """)
    nb.md("""
        4. Rilanciamo `uv run main.py`. Le due righe con il totale e il prezzo medio compaiono, ma il
           salvataggio in Excel si ferma con `No module named 'openpyxl'`. Il traceback finisce dentro
           `pandas/io/excel/_openpyxl.py`, il file che abbiamo visto nella prima sezione, perché pandas
           usa openpyxl per scrivere i file Excel ma non lo installa da sé.
        5. Aggiungiamo `uv add openpyxl` e rilanciamo lo script, che questa volta stampa anche
           `La tabella della spesa è nel file spesa.xlsx`. Il file Excel compare nella cartella `demo/`.
    """)
    nb.md("""
        La seconda parte sistema il codice con Ruff.

        6. Aggiungiamo Ruff come strumento di sviluppo con `uv add --dev ruff`.
        7. Lanciamo `uv run ruff format`, che risponde `2 files reformatted`. La riga lunga di `main.py`
           finisce tra parentesi, ma resta oltre i 100 caratteri.
        8. Lanciamo `uv run ruff check`, che trova le quattro segnalazioni della tabella e indica che due
           si correggono con `--fix`.
        9. Lanciamo `uv run ruff check --fix`, che toglie l'import di `math` e riordina gli import di
           `main.py`, con `import pandas as pd` prima e l'import da `calcoli` dopo, separati da una riga
           vuota.
    """)
    nb.md("""
        10. Correggiamo a mano le due segnalazioni rimaste: cancelliamo la riga `numero = len(prezzi)` e
            dividiamo la f-string lunga in due pezzi, come nell'ultima cella della sezione 8.
        11. Rilanciamo `uv run ruff format`, perché l'import tolto ha lasciato righe vuote di troppo in
            `calcoli.py`, e poi `uv run ruff check`, che risponde `All checks passed!`.
        12. Lanciamo un'ultima volta `uv run main.py`, che stampa le stesse tre righe di prima con il
            codice ormai in ordine.
    """)
    nb.box("attenzione", """
        Alcuni errori sono frequenti la prima volta. Il comando `uv init` non va lanciato dentro la
        cartella del corso, perché uv registra il nuovo progetto come parte di quello del corso e gli fa
        usare lo stesso `.venv`, dove le librerie ci sono già tutte e non si vede mai che cosa manca. Per
        lo stesso motivo `uv add`, in una cartella senza `pyproject.toml`, modifica il progetto del corso.
        Il pulsante **Run Python File** di VS Code usa l'interprete selezionato nell'editor, cioè il
        Python del corso, che ha già pandas, quindi in questa parte gli script si lanciano sempre con
        `uv run` nel terminale. Se uv stampa l'avviso
        `VIRTUAL_ENV=... does not match the project environment path`, l'avviso è innocuo: uv usa
        comunque l'ambiente della cartella.
    """)
    nb.md("""
        Nell'[Esercitazione 1](../Esercitazione_1.ipynb) rifai gli stessi passi nella cartella
        `esercizio/`, che contiene un programma equivalente sulle temperature della settimana, con le
        funzioni in `meteo.py` e lo script in `main.py`. Il punto di arrivo della dimostrazione e
        dell'esercizio, con i file sistemati e i `pyproject.toml` completi, si trova nella cartella
        `Soluzioni/Script_uv_Ruff/` del corso.
    """)

    # ------------------------------------------------------------------ 10
    nb.sezione("I comandi in breve", intro="""
        Le due tabelle seguenti raccolgono i comandi del notebook, da scrivere nel terminale aperto sulla
        cartella del progetto su cui si vuole lavorare. La prima riguarda uv e l'ambiente, la seconda Ruff.
    """)
    nb.md("""
        | Comando | Che cosa fa |
        |---|---|
        | `uv sync` | crea `.venv` o lo rimette esattamente come lo descrive `uv.lock`, gruppo `dev` compreso |
        | `uv add pandas` | aggiunge una libreria a `pyproject.toml` e `uv.lock` e la installa |
        | `uv add --dev ruff` | aggiunge uno strumento di sviluppo, nel gruppo `dev` |
        | `uv remove pandas` | toglie una libreria dal progetto e dall'ambiente |
        | `uv run main.py` | esegue uno script con il Python di `.venv`, dopo averlo allineato ai file del progetto |
        | `uv init nome` | crea un progetto nuovo nella cartella `nome`, fuori dalla cartella del corso |
    """)
    nb.md("""
        | Comando | Che cosa fa |
        |---|---|
        | `uv run ruff format` | rimette in forma i file della cartella e delle sottocartelle |
        | `uv run ruff check` | elenca le segnalazioni, con file, riga e codice |
        | `uv run ruff check --fix` | applica le correzioni sicure, come togliere e riordinare gli import |
        | **Shift+Alt+F** in VS Code | rimette in forma il file aperto |
        | **Ctrl+.** su una riga sottolineata | apre le correzioni proposte da Ruff |
    """)
    return nb
