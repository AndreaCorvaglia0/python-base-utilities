"""S · Ambiente, script e Ruff (solo aula Avanzata, modulo 1, dopo il notebook 03).

Notebook di spiegazione, senza esercizi, scritto per essere proiettato mentre si parla: un titolo per ogni concetto,
poche frasi e una tabella sotto ciascun titolo, gli approfondimenti in riquadri che si possono saltare. Prepara la
dimostrazione nella cartella `demo/` e l'Esercitazione 1 dell'Avanzata, che la fa rifare nella cartella `esercizio/`.
Sta in `Aula_Avanzata/Modulo_1/Script_uv_Ruff/`, quindi la radice dell'aula è `../../` e la demo è in `demo/`.
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
        indice=False,    # proiettato mentre si parla: si scorre per titoli, l'indice sarebbe lungo quanto una pagina
    )


    # ------------------------------------------------------------------ 1
    nb.sezione("uv e l'ambiente virtuale")
    nb.sottosezione("Che cosa fa uv", intro="""
        uv è il programma con cui gestiamo i progetti Python del corso. Lo abbiamo già usato all'inizio, quando
        `uv sync`, lanciato nella cartella del corso, ha preparato tutto quello che serve ai notebook. Un solo
        programma fa quattro lavori, che prima richiedevano strumenti diversi.
    """)
    nb.md("""
        | Lavoro | Esempio |
        |---|---|
        | installa la versione di Python che il progetto chiede | Python 3.13, se sul PC non c'è |
        | crea l'**ambiente virtuale** del progetto | la cartella `.venv` |
        | installa le librerie nell'ambiente | pandas, plotly, openpyxl |
        | lancia gli script con il Python giusto | `uv run main.py` |
    """)
    nb.sottosezione("Che cos'è un ambiente virtuale", intro="""
        Un ambiente virtuale è una cartella, che con uv si chiama `.venv`, con un interprete Python e le librerie
        di **un solo progetto**. Ogni progetto ha il suo, e quello che si installa in un progetto non tocca gli
        altri. La tabella riassume i vantaggi di questa separazione.
    """)
    nb.md("""
        | Vantaggio | Che cosa vuol dire in pratica |
        |---|---|
        | progetti separati | due progetti possono usare versioni diverse di pandas senza disturbarsi |
        | stesse versioni su ogni PC | chi riceve il progetto ricostruisce lo stesso ambiente con `uv sync` |
        | si cancella e si ricrea | se l'ambiente si rompe, si cancella `.venv` e si rilancia `uv sync` |
        | niente permessi di amministratore | l'ambiente sta nella cartella del progetto, non nel sistema |
    """)
    nb.sottosezione("Dove stanno Python e le librerie", intro="""
        Il kernel di questo notebook usa il Python dell'ambiente del corso, come abbiamo controllato nel notebook
        00. La cella seguente stampa il percorso dell'interprete e quello del file principale di pandas: entrambi
        passano per `.venv`, perché anche le librerie sono installate dentro l'ambiente, nella sottocartella
        `site-packages`.
    """)
    nb.code("""
        import sys

        import pandas as pd

        print(sys.executable)
        print(pd.__file__)
    """)
    nb.box("approfondimento", titolo="Una libreria è una cartella di file Python", testo="""
        Una libreria installata è una cartella di file, in gran parte file `.py` scritti in Python come i nostri.
        La cella seguente elenca i file della sottocartella `io/excel` di pandas, che legge e scrive i file
        Excel: il percorso si costruisce con `Path`, dove `parent` è la cartella che contiene il file e `/`
        aggiunge una sottocartella. Nell'elenco c'è `_openpyxl.py`, che ritroveremo nella dimostrazione.
    """)
    nb.code("""
        import os
        from pathlib import Path

        cartella_excel = Path(pd.__file__).parent / "io" / "excel"
        sorted(os.listdir(cartella_excel))
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("I file del progetto")
    nb.sottosezione("La cartella del corso", intro="""
        Un progetto gestito con uv è descritto da pochi file di testo, che stanno nella cartella del progetto
        accanto al codice. Nella cartella del corso, due livelli sopra questo notebook, sono gli ultimi quattro
        elementi dello schema seguente.
    """)
    nb.md("""
        ```
        Aula_Avanzata/
            Modulo_1/ ... Modulo_4/   i notebook, un modulo per cartella
            Soluzioni/                le soluzioni degli esercizi
            Dati/   Schede/           i dati del corso e le schede di riepilogo
            pyproject.toml            la descrizione del progetto e l'elenco delle librerie
            uv.lock                   le versioni esatte di tutte le librerie del progetto
            .python-version           la versione di Python del progetto
            .venv/                    l'ambiente virtuale, creato da uv sync
        ```
    """)
    nb.sottosezione("Che cosa contiene ciascun file", intro="""
        I quattro elementi hanno ruoli diversi. I primi tre si condividono con i colleghi insieme al codice,
        mentre `.venv` resta su ogni PC, perché pesa centinaia di megabyte e si ricrea dagli altri tre.
    """)
    nb.md("""
        | File | Che cosa contiene | Chi lo scrive | Si condivide |
        |---|---|---|---|
        | `pyproject.toml` | il nome del progetto e le librerie, con vincoli larghi come `pandas>=3.0` | uv, quando aggiungiamo o togliamo una libreria | sì |
        | `uv.lock` | la versione esatta di ogni libreria, comprese quelle da cui dipendono le altre | soltanto uv | sì |
        | `.python-version` | la versione di Python, per noi 3.13 | chi crea il progetto | sì |
        | `.venv/` | l'interprete e le librerie installate | uv, con `uv sync` e `uv run` | **no** |
    """)
    nb.sottosezione("Leggere pyproject.toml", intro="""
        Il file `pyproject.toml` è scritto nel formato TOML, fatto di sezioni tra parentesi quadre e di righe
        `chiave = valore`, e da Python si legge con il modulo `tomllib`, che lo trasforma in un dizionario. Il
        percorso `../../pyproject.toml` sale di due cartelle, perché `..` indica la cartella superiore.
    """)
    nb.code("""
        import tomllib

        testo = Path("../../pyproject.toml").read_text(encoding="utf-8")
        progetto = tomllib.loads(testo)
        print(progetto["project"]["dependencies"])
        print(progetto["dependency-groups"]["dev"])
    """)
    nb.md("""
        La prima riga sono le librerie di cui i notebook hanno bisogno. La seconda viene dal gruppo `dev`, che
        raccoglie gli **strumenti di sviluppo**, cioè quelli che servono a chi scrive il codice e non al
        programma per funzionare: nel nostro caso Ruff, che vediamo più avanti.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Aggiungere e togliere librerie")
    nb.sottosezione("I quattro comandi", intro="""
        Le librerie si gestiscono con pochi comandi di uv, che si scrivono nel **terminale** di VS Code
        (**Terminal → New Terminal**) e non in una cella. Le librerie arrivano da PyPI, il catalogo pubblico dei
        pacchetti Python, quindi questi comandi hanno bisogno di internet.
    """)
    nb.md("""
        | Comando | Che cosa fa | Quando si usa |
        |---|---|---|
        | `uv add matplotlib` | scrive la libreria in `pyproject.toml` e `uv.lock` e la installa | serve una libreria nuova |
        | `uv add --dev ruff` | come sopra, ma nel gruppo `dev` | serve uno strumento di sviluppo |
        | `uv remove matplotlib` | toglie la libreria dai file del progetto e da `.venv` | la libreria non serve più |
        | `uv sync` | rimette `.venv` esattamente come lo descrive `uv.lock` | si riceve il progetto, o l'ambiente non funziona |
    """)
    nb.sottosezione("Su quale progetto lavora un comando", intro="""
        Un comando di uv lavora sul progetto della **cartella in cui si trova il terminale**: cerca un
        `pyproject.toml` in quella cartella e, se non lo trova, risale una cartella alla volta. Nella cartella del
        corso, o in `Modulo_1`, i comandi agiscono quindi sul progetto del corso. La cartella `demo/` contiene
        soltanto due script, e diventa un progetto a sé quando `uv init --bare` vi crea un `pyproject.toml`: da quel
        momento un terminale aperto lì lavora su quel progetto, con un ambiente separato.
    """)
    nb.box("approfondimento", titolo="Perché non pip install", testo="""
        Negli esempi in rete compare spesso `pip install`, anche in una cella come `!pip install`. Il programma
        pip installa le librerie e accompagna Python da molti anni, ma un ambiente creato da uv non lo contiene,
        quindi il comando usa il pip di un altro Python e installa la libreria lì. Anche quando funziona, la
        libreria non entra in `pyproject.toml` e `uv.lock`, il collega non la riceve e il successivo `uv sync` la
        toglie.
    """)
    nb.box("approfondimento", titolo="Il kernel dopo un uv add", testo="""
        Dopo un `uv add` nell'ambiente del corso conviene riavviare il kernel con **Restart** prima di scrivere
        l'`import`. Una libreria appena installata di solito si importa anche senza riavvio, ma una libreria che
        il kernel aveva già importato, come numpy, resta in memoria nella versione di prima finché il kernel non
        riparte.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Notebook e script")
    nb.sottosezione("Quando l'uno e quando l'altro", intro="""
        Un notebook è lo strumento per esplorare, una cella alla volta, mentre uno **script** è un file `.py` che
        Python esegue dall'inizio alla fine con un solo comando. Quando un'analisi è diventata stabile e va
        ripetuta, per esempio ogni mattina o a ogni nuovo file di dati, conviene trasformarla in uno script.
    """)
    nb.md("""
        | | Notebook | Script |
        |---|---|---|
        | serve a | esplorare, provare, guardare i risultati | ripetere lo stesso lavoro |
        | si esegue | una cella alla volta, nell'ordine che scegliamo | tutto, dall'alto in basso, con `uv run nome.py` |
        | il risultato | può dipendere dall'ordine in cui abbiamo eseguito le celle | riparte da zero e non cambia |
        | si può pianificare | no | sì, anche quando nessuno è davanti al PC |
        | si riusa | copiando le celle | importando le sue funzioni da un altro file |
    """)
    nb.sottosezione("Due differenze da ricordare", intro="""
        Quando il codice passa da un notebook a uno script cambiano due dettagli, che spiegano gli errori più
        comuni delle prime volte.
    """)
    nb.md("""
        1. In uno script l'ultima espressione non viene mostrata, quindi quello che vogliamo vedere va dentro un
           `print`.
        2. I percorsi relativi partono dalla cartella in cui si trova il terminale, mentre in un notebook partono
           dalla cartella del notebook. Lo script della dimostrazione, lanciato da un terminale aperto in
           `demo/`, scrive lì il suo file Excel.
    """)
    nb.box("approfondimento", titolo="Un notebook è un file JSON", testo="""
        Un notebook è un file in formato JSON, cioè un testo fatto di parentesi graffe, chiavi e valori, che oltre
        al codice contiene il testo delle celle Markdown e gli output. Per questo nei programmi di controllo di
        versione come Git, che conservano la storia delle modifiche, la modifica di una riga di codice si confonde
        tra tutto il resto, mentre in uno script si vede subito. La cella seguente stampa l'inizio del file di
        questo notebook.
    """)
    nb.code("""
        print(Path("Ambiente_script_e_Ruff.ipynb").read_text(encoding="utf-8")[:200])
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Importare una funzione da un altro file")
    nb.sottosezione("I due file della dimostrazione", intro="""
        Il programma della dimostrazione è diviso in due file, nella cartella `demo/` accanto a questo notebook:
        `calcoli.py` definisce le funzioni che fanno i conti, e `main.py` è lo script che si lancia e le usa. Il
        file `calcoli.py` è scritto apposta in disordine, perché nella dimostrazione lo sistemiamo con Ruff.
    """)
    nb.code("""
        print(Path("demo/calcoli.py").read_text(encoding="utf-8"))
    """)
    nb.md("""
        Il file `main.py` importa le funzioni di `calcoli.py`, stampa il totale e il prezzo medio della spesa e
        salva con pandas una tabella nel file Excel `spesa.xlsx`.
    """)
    nb.code("""
        print(Path("demo/main.py").read_text(encoding="utf-8"))
    """)
    nb.sottosezione("Un file del progetto si importa come una libreria", intro="""
        La riga `from calcoli import totale, prezzo_medio` ha la stessa forma di `from math import sqrt`, che
        abbiamo usato nel notebook 01. Per Python `calcoli`, `math` e `pandas` sono tutti **moduli**, e cambia
        soltanto il posto in cui li trova.
    """)
    nb.md("""
        | Import | Che cosa importa | Dove lo trova Python |
        |---|---|---|
        | `from calcoli import totale` | un file del nostro progetto | nella cartella dello script, accanto a `main.py` |
        | `from math import sqrt` | un modulo della libreria standard | tra i file che arrivano con Python |
        | `import pandas as pd` | una libreria installata | in `.venv`, nella cartella `site-packages` |
    """)
    nb.box("approfondimento", titolo="L'elenco delle cartelle: sys.path", testo="""
        Python cerca un modulo in un elenco ordinato di cartelle, `sys.path`, e usa il primo che trova. Quando
        lanciamo uno script, la cartella che lo contiene è in testa all'elenco, ed è per questo che `main.py`
        trova `calcoli.py`. Nel notebook l'elenco contiene invece la cartella del notebook, di solito scritta come
        una stringa vuota, `''`, seguita dalla libreria standard e da `site-packages`.
    """)
    nb.code("""
        sys.path
    """)
    nb.sottosezione("Un import esegue il file", intro="""
        Un `import` esegue il file importato dall'inizio alla fine, una volta sola, e poi rende disponibili i
        nomi che ha definito. Un `print` scritto in `calcoli.py` fuori dalle funzioni comparirebbe quindi nel
        terminale prima di tutto quello che stampa `main.py`.
    """)
    nb.md("""
        Per distinguere il file lanciato da quello importato, Python dà a ogni file un nome, nella variabile
        `__name__`: vale `"__main__"` nel file lanciato con `uv run` e il nome del modulo, come `"calcoli"`, in un
        file importato. Anche il notebook è un programma principale, come mostra la cella seguente.
    """)
    nb.code("__name__")
    nb.md("""
        Per questo negli script si trova spesso, in fondo, un blocco `if __name__ == "__main__":` con le righe
        che fanno il lavoro del programma, che vengono eseguite quando lanciamo il file ma non quando un altro
        file lo importa per usarne le funzioni.
    """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Formattare il codice")
    nb.sottosezione("Che cosa vuol dire formattare", intro="""
        Nel notebook 03 abbiamo visto le regole di PEP 8 sulla forma del codice. **Formattare** significa
        sistemare la forma secondo quelle regole senza cambiare quello che il codice fa, e un **formatter** è il
        programma che lo fa al posto nostro, nello stesso modo in tutto il progetto.
    """)
    nb.md("""
        | Regola di PEP 8 | Esempio |
        |---|---|
        | quattro spazi di indentazione | il corpo di una funzione |
        | uno spazio attorno a `=` e agli operatori | `somma = a + b`, non `somma=a+b` |
        | niente spazi dentro le parentesi | `sum(prezzi)`, non `sum( prezzi )` |
        | due righe vuote prima e dopo una funzione | tra `def totale` e `def prezzo_medio` |
        | righe non troppo lunghe | nel corso al massimo 100 caratteri |
    """)
    nb.sottosezione("Il formatter su calcoli.py", intro='''
        Applicato a `calcoli.py`, il formatter aggiunge gli spazi attorno a `=` e a `/`, toglie quelli dentro
        `sum( prezzi )`, separa le funzioni con due righe vuote e mette una riga vuota dopo la docstring.

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
    nb.sottosezione("Che cosa il formatter non fa", intro="""
        Il formatter cambia **soltanto la forma**. Nel file qui sopra restano l'import di `math` e la variabile
        `numero`, che non servono a nulla, e restano tutti i problemi che non riguardano gli spazi.
    """)
    nb.md("""
        - Non rinomina le variabili, perché scegliere un nome che dica che cosa contiene resta un lavoro nostro.
        - Non toglie il codice inutile, come un import o una variabile mai usati.
        - Non divide una stringa troppo lunga: può portarla su una riga sua dentro le parentesi, ma il testo tra
          virgolette resta intero e la riga può restare oltre il limite.
    """)

    # ------------------------------------------------------------------ 7
    nb.sezione("Il linter")
    nb.sottosezione("Che cosa fa un linter", intro="""
        Un **linter** legge il codice senza eseguirlo e segnala gli errori probabili e le abitudini che portano a
        errori, come un import che non serve o una variabile mai usata. Ogni segnalazione indica il file, la riga
        e un codice, fatto da una lettera per la famiglia di regole e da un numero.
    """)
    nb.md("""
        | Famiglia | Che cosa controlla |
        |---|---|
        | `E` e `W` | lo stile di PEP 8, come la lunghezza delle righe |
        | `F` | gli errori probabili, come import e variabili inutilizzati o nomi mai definiti |
        | `I` | l'ordine degli import |
    """)
    nb.sottosezione("Le quattro segnalazioni della dimostrazione", intro="""
        Sui due file della dimostrazione il linter dà le quattro segnalazioni della tabella. Due le corregge Ruff
        da solo, con una correzione sicura che non cambia il comportamento del programma; le altre due si
        correggono a mano.
    """)
    nb.md("""
        | Codice | Messaggio | Che cosa vuol dire | Come si corregge |
        |---|---|---|---|
        | `F401` | `` `math` imported but unused `` | un modulo importato e mai usato | Ruff toglie l'import |
        | `I001` | `Import block is un-sorted or un-formatted` | gli import non sono in ordine | Ruff li riordina |
        | `F841` | `` Local variable `numero` is assigned to but never used `` | una variabile assegnata e mai letta | a mano |
        | `E501` | `Line too long (104 > 100)` | una riga oltre i 100 caratteri | a mano |
    """)
    nb.box("approfondimento", titolo="L'ordine degli import e la correzione non sicura", testo="""
        Riordinando gli import, Ruff li divide in gruppi: prima la libreria standard, poi le librerie
        installate e per ultimi i file del progetto. Per `F841` Ruff conosce anche una correzione non sicura, che
        dal terminale cita nell'ultima riga del suo output con l'opzione `--unsafe-fixes`, ma non la usiamo, perché toglierebbe
        soltanto il nome `numero` e lascerebbe la chiamata `len(prezzi)`, inutile anche lei. Una variabile mai
        usata, del resto, a volte è il segno di un errore più sotto.
    """)

    # ------------------------------------------------------------------ 8
    nb.sezione("Ruff: formatter e linter insieme")
    nb.sottosezione("Ruff in VS Code", intro="""
        **Ruff** fa da formatter e da linter, e il modo più comodo di usarlo è dall'editor, con l'estensione
        **Ruff** di Astral, che la cartella del corso propone tra le estensioni consigliate e imposta come formatter
        dei file Python. L'estensione controlla ogni file Python aperto mentre lo scriviamo: le segnalazioni
        compaiono sottolineate nel codice e nel pannello **Problems**, ciascuna con il suo codice.
    """)
    nb.md("""
        | Che cosa | In VS Code |
        |---|---|
        | vedere le segnalazioni | le sottolineature nel codice e il pannello **Problems**, con **Ctrl+Shift+M** |
        | rimettere in forma il file | **Format Document**, con **Shift+Alt+F** |
        | correggere una segnalazione | **Ctrl+.** sulla riga sottolineata, che apre il menu **Quick Fix** |
        | correggere tutto quello che Ruff sa correggere | **Ctrl+Shift+P**, poi **Ruff: Fix all auto-fixable problems** |
        | rimettere in forma a ogni salvataggio | l'impostazione **Format On Save**, per chi la attiva |
    """)
    nb.sottosezione("Lo stesso dal terminale", intro="""
        Gli stessi lavori si fanno anche dal terminale, con Ruff installato nel progetto, nel gruppo `dev`, e
        lanciato con `uv run`. I comandi vanno lanciati nel terminale aperto nella cartella `demo/` o
        `esercizio/`, perché dalla cartella del corso Ruff lavorerebbe su tutti gli script che contiene e
        metterebbe in ordine anche i file di partenza di quelle due cartelle.
    """)
    nb.md("""
        | Comando | Equivale in VS Code a |
        |---|---|
        | `uv run ruff format` | **Format Document**, ma su tutti i file della cartella |
        | `uv run ruff check` | il pannello **Problems** |
        | `uv run ruff check --fix` | **Ruff: Fix all auto-fixable problems**, su tutti i file della cartella |
    """)
    nb.sottosezione("In che ordine", intro="""
        Nella dimostrazione prima rimettiamo in forma i file, poi leggiamo le segnalazioni, lasciamo a Ruff quelle
        che sa correggere, correggiamo a mano le altre e alla fine rimettiamo in forma un'ultima volta, finché il
        pannello Problems non ha più segnalazioni di Ruff. Mettere la formattazione per prima serve a vedere
        separatamente il lavoro dei due strumenti: con le regole scelte il linter non controlla gli spazi, quindi
        anche prima della formattazione darebbe le stesse quattro segnalazioni.
    """)
    nb.sottosezione("La configurazione", intro="""
        Ruff si configura nella sezione `[tool.ruff]` di `pyproject.toml`, che la cella seguente legge dal
        dizionario `progetto`. Il `pyproject.toml` creato da `uv init --bare` in `demo/` non ha questa sezione, quindi
        Ruff, risalendo le cartelle come uv, usa quella del corso, e l'estensione di VS Code e il terminale danno
        le stesse segnalazioni.
    """)
    nb.code("""
        progetto["tool"]["ruff"]
    """)
    nb.md("""
        | Voce | Significato |
        |---|---|
        | `line-length` | il limite delle righe, 100 caratteri |
        | `target-version` | la versione di Python per cui scriviamo |
        | `extend-exclude` | i file che Ruff lascia stare: `corso.py` e i notebook del corso |
        | `src` | le cartelle in cui Ruff cerca i file dei progetti, per riconoscere `calcoli` e `meteo` |
        | `lint` → `select` | le famiglie di regole attive, `E`, `F`, `W` e `I` |
    """)
    nb.box("approfondimento", titolo="Spezzare una stringa troppo lunga", testo="""
        La riga troppo lunga di `main.py` si sistema dividendo la f-string in due pezzi scritti uno dopo l'altro
        dentro le parentesi del `print`. Python unisce due stringhe adiacenti in una sola, quindi il testo
        stampato non cambia, e ciascun pezzo ha la sua `f` perché contiene delle graffe. La cella seguente mostra
        la riga corretta, con i prezzi della dimostrazione.
    """)
    nb.code("""
        prezzi = [2.40, 1.15, 3.20, 4.50, 1.85]

        print(
            f"Prezzo medio di un prodotto: {sum(prezzi) / len(prezzi):.2f} euro, "
            f"calcolato su {len(prezzi)} prodotti"
        )
    """)

    # ------------------------------------------------------------------ 9
    nb.sezione("La dimostrazione")
    nb.sottosezione("Il punto di partenza", intro="""
        Nella dimostrazione mettiamo insieme quello che abbiamo visto: trasformiamo i due file di `demo/` in un
        progetto, gli costruiamo un ambiente apposito, **una libreria alla volta** man mano che ci accorgiamo che
        manca, sistemiamo il codice con Ruff e lo lanciamo. Chi vuole può ripetere i comandi sul proprio PC mentre
        li eseguiamo. All'inizio la cartella contiene soltanto i due script, come mostra la cella seguente, e l'opzione
        `--bare` di `uv init` aggiunge soltanto `pyproject.toml`, senza il `README.md` e il repository git che il
        comando normale prepara per un progetto da pubblicare.
    """)
    nb.code("""
        sorted(os.listdir("demo"))
    """)
    nb.md("""
        Il terminale si apre nella cartella `demo/` con il tasto destro sulla cartella, nel pannello **Explorer**,
        e la voce **Open in Integrated Terminal**, oppure con `cd Modulo_1/Script_uv_Ruff/demo` dalla cartella del
        corso. Gli script si lanciano sempre con `uv run`, perché il pulsante **Run Python File** di VS Code usa il
        Python del corso, dove pandas c'è già, e non farebbe comparire gli errori della dimostrazione.
    """)
    nb.sottosezione("Prima parte: l'ambiente, una libreria alla volta", intro="""
        Prima di creare il progetto lanciamo lo script una volta, per vedere quale ambiente usa uv quando la
        cartella non ha un progetto suo. Dopo `uv init --bare` lo rilanciamo, e sono gli errori a dirci che cosa
        aggiungere.
    """)
    nb.md("""
        | Passo | Comando | Che cosa succede |
        |---|---|---|
        | 1 | `uv run main.py` | funziona: senza un progetto suo, uv risale fino al progetto del corso e usa il suo ambiente, dove pandas c'è |
        | 2 | `uv init --bare` | uv avvisa che la cartella è esclusa dal progetto del corso, ed è quello che vogliamo; nasce il progetto `demo`, con il nome della cartella e un solo file, `pyproject.toml` con `dependencies = []` |
        | 3 | `uv run main.py` | uv crea `.venv` e `uv.lock` del progetto, poi lo script si ferma con `No module named 'pandas'` |
    """)
    nb.md("""
        Da qui in avanti ogni errore nomina la libreria che manca, e la aggiungiamo al progetto.
    """)
    nb.md("""
        | Passo | Comando | Che cosa succede |
        |---|---|---|
        | 4 | `uv add pandas` | pandas entra in `pyproject.toml` e `uv.lock` e si installa, insieme a numpy |
        | 5 | `uv run main.py` | compaiono il totale e il prezzo medio, poi il salvataggio si ferma con `No module named 'openpyxl'` |
        | 6 | `uv add openpyxl` | openpyxl entra nel progetto |
        | 7 | `uv run main.py` | lo script arriva in fondo e crea `spesa.xlsx` nella cartella `demo/` |
    """)
    nb.md("""
        Al passo 5 l'errore nasce dentro pandas: il traceback, cioè l'elenco delle righe attraversate che Python
        stampa sopra il messaggio, finisce in `pandas/io/excel/_openpyxl.py`, perché pandas usa openpyxl per
        scrivere i file Excel ma non lo installa da sé. Se VS Code propone di usare il nuovo ambiente della
        cartella, si risponde di no, perché i notebook restano sull'ambiente del corso.
    """)
    nb.sottosezione("Seconda parte: il codice in ordine con Ruff", intro="""
        Con lo script funzionante aggiungiamo Ruff al progetto della dimostrazione e lo usiamo in VS Code per
        sistemare i due file, tenendoli aperti tutti e due.
    """)
    nb.md("""
        | Passo | Comando | Che cosa succede |
        |---|---|---|
        | 8 | `uv add --dev ruff` | Ruff entra nel gruppo `dev` del progetto |
        | 9 | **Shift+Alt+F** su `calcoli.py` e su `main.py` | spazi e righe vuote al posto giusto; la riga lunga va tra parentesi ma resta lunga |
        | 10 | pannello **Problems** | le quattro segnalazioni della sezione 7, due delle quali Ruff sa correggere |
    """)
    nb.md("""
        Le segnalazioni si correggono prima con Ruff e poi a mano, e alla fine si controlla che non ne resti
        nessuna. Dal terminale gli stessi passi sono `uv run ruff format`, `uv run ruff check` e
        `uv run ruff check --fix`, e l'ultimo `uv run ruff check` risponde `All checks passed!`.
    """)
    nb.md("""
        | Passo | Comando | Che cosa succede |
        |---|---|---|
        | 11 | **Ruff: Fix all auto-fixable problems**, su ciascun file | spariscono `F401` e `I001`: l'import di `math` è tolto e gli import sono in ordine |
        | 12 | a mano | si cancella `numero = len(prezzi)` e si divide in due la f-string lunga |
        | 13 | **Shift+Alt+F** su `calcoli.py` | tolta la riga vuota rimasta, il pannello Problems non ha più segnalazioni di Ruff |
        | 14 | `uv run main.py` | le stesse tre righe di prima, con il codice in ordine |
    """)
    nb.box("nota", titolo="Dove si lanciano uv init e uv add", testo="""
        Dentro la cartella del corso `uv init` crea un progetto a sé soltanto in `demo/` ed `esercizio/`, che il
        progetto del corso esclude nella sezione `[tool.uv.workspace]` del suo `pyproject.toml`. In un'altra
        cartella del corso uv registrerebbe il nuovo progetto come parte di quello del corso, con lo stesso
        `.venv`, dove le librerie ci sono già tutte: un progetto proprio si crea quindi fuori, per esempio con
        `uv init prova` in `C:\\Corso`. Allo stesso modo `uv add`, lanciato prima di `uv init`, lavora sul
        progetto del corso.
    """)
    nb.sottosezione("Dopo la dimostrazione", intro="""
        Nell'[Esercitazione 1](../Esercitazione_1.ipynb) rifai gli stessi passi nella cartella `esercizio/`, che
        contiene un programma equivalente sulle temperature della settimana, con le funzioni in `meteo.py` e lo
        script in `main.py`. Il punto di arrivo della dimostrazione e dell'esercizio si trova nella cartella
        `Soluzioni/Script_uv_Ruff/` del corso.
    """)

    # ------------------------------------------------------------------ 10
    nb.sezione("I comandi in breve", intro="""
        I comandi di uv si scrivono nel terminale aperto sulla cartella del progetto su cui si vuole lavorare, per
        noi `demo/` o `esercizio/`. Ruff si usa dall'editor, e dal terminale con i comandi equivalenti.
    """)
    nb.md("""
        | Comando | Che cosa fa |
        |---|---|
        | `uv sync` | crea `.venv` o lo rimette esattamente come lo descrive `uv.lock`, gruppo `dev` compreso |
        | `uv add pandas` | aggiunge una libreria a `pyproject.toml` e `uv.lock` e la installa |
        | `uv add --dev ruff` | aggiunge uno strumento di sviluppo, nel gruppo `dev` |
        | `uv remove pandas` | toglie una libreria dal progetto e dall'ambiente |
        | `uv run main.py` | allinea `.venv` ai file del progetto ed esegue lo script con il suo Python |
        | `uv init --bare` | crea nella cartella del terminale un progetto con il solo `pyproject.toml` |
    """)
    nb.md("""
        | Ruff in VS Code | Dal terminale | Che cosa fa |
        |---|---|---|
        | **Shift+Alt+F** (Format Document) | `uv run ruff format` | rimette in forma il codice |
        | pannello **Problems** (**Ctrl+Shift+M**) | `uv run ruff check` | mostra le segnalazioni, con file, riga e codice |
        | **Ruff: Fix all auto-fixable problems** | `uv run ruff check --fix` | applica le correzioni sicure |
        | **Ctrl+.** su una riga sottolineata | | propone la correzione di quella riga |
    """)
    return nb
