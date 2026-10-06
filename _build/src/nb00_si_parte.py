"""00 · Si parte: VS Code, notebook e primo codice."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="00",
        file="00_Si_parte",
        titolo="Si parte: VS Code, notebook e primo codice",
        blocco=1,
        giornata=1,
        intento="Prima di scrivere Python bisogna sapere dove si scrive e come si fa partire. Dal doppio clic sul file alla prima riga stampata.",
        obiettivi=[
            "aprire un notebook in VS Code e scegliere il kernel giusto",
            "eseguire celle di codice e celle Markdown, e leggere quello che restituiscono",
            "dire in due frasi cosa sono Python e le librerie",
        ],
        tempo={"base": 40, "avanzata": 30},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Python e le librerie", intro="""
        Python è un linguaggio di programmazione: un modo di scrivere istruzioni che il computer esegue
        una riga dopo l'altra. Per noi vuol dire tre cose: legge i file Excel e i CSV senza aprirli,
        parla con le API da cui arrivano prezzi e misure, e disegna i grafici che il capo vuole per ieri.
    """)
    nb.md("""
        Da solo, però, Python sa fare poco più di una calcolatrice. Il resto lo fanno le librerie:
        codice scritto da altri, già provato e corretto, che portiamo dentro al nostro con una riga di
        `import`. Nel corso ne useremo tre su tutte: pandas per le tabelle, Plotly per i grafici,
        requests per le API.
    """)
    nb.md("""
        Un notebook come questo è il posto dove si scrive e si prova il codice un pezzo alla volta, con
        il risultato subito sotto. È lo strumento di chi analizza dati: si prova, si guarda, si
        corregge. Prima però serve il programma che lo apre: VS Code.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("VS Code e il kernel", intro="""
        VS Code è l'editor: il programma in cui si aprono i file, si scrive il codice e si eseguono i
        notebook. Il corso è una cartella: in VS Code si apre con **File → Open Folder**, e da quel
        momento tutto quello che compare a sinistra, nell'Explorer, è il contenuto di quella cartella.
    """)
    nb.md("""
        Servono due estensioni, **Python** e **Jupyter**, entrambe di Microsoft: si installano
        dall'icona dei quattro quadratini nella barra a sinistra, cercando il nome. Se stai leggendo
        questo notebook con il codice colorato e i pulsanti sopra le celle, ci sono già.
    """)
    nb.md("""
        Il kernel è il Python che esegue le celle. In alto a destra c'è **Select Kernel**: scegli
        **Python Environments** e poi la voce con `.venv` nel nome. Quello è l'ambiente del corso, con
        dentro Python e tutte le librerie che servono. Controlliamo subito di aver preso quello giusto:
        clicca nella cella qui sotto e premi **Shift+Invio**.
    """)
    nb.code("""
        import sys

        sys.executable
    """)
    nb.md("""
        Il percorso che compare deve contenere `.venv`. Se non c'è, il notebook sta usando un altro
        Python, magari quello di sistema, senza le librerie: torna su **Select Kernel** e cambia.
    """)
    nb.code("""
        import pandas as pd

        pd.__version__
    """)
    nb.md("""
        Un numero di versione che inizia per 3: pandas c'è. Queste due celle sono il controllo da fare
        ogni volta che qualcosa sembra sparito.
    """)
    nb.box("attenzione", """
        `ModuleNotFoundError: No module named 'pandas'` alla prima cella del giorno quasi mai vuol dire
        che pandas manca: vuol dire che il kernel selezionato è un altro Python. Prima **Select Kernel**,
        poi tutto il resto.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Le celle", intro="""
        Un notebook è una sequenza di celle, di due tipi: le celle di codice, che il kernel esegue, e le
        celle Markdown, che contengono testo formattato come questo. Si eseguono una alla volta,
        nell'ordine che vogliamo, e il risultato compare sotto.
    """)
    nb.md("""
        Per eseguire una cella: clicca dentro e premi **Shift+Invio**. Il kernel la esegue e il cursore
        passa alla cella successiva. Proviamo con un conto.
    """)
    nb.code("3 + 4")
    nb.md("""
        L'ultima riga di una cella, se è un'espressione, viene mostrata sotto: è l'output, e non serve
        chiedere niente. Diamo un nome al risultato, così possiamo riusarlo.
    """)
    nb.code("consumo_kwh = 1480")
    nb.md("""
        Nessun output: l'assegnazione con `=` non è un'espressione, mette solo il valore dentro la
        variabile. Il kernel però se lo è ricordato, e la cella qui sotto lo trova.
    """)
    nb.code("consumo_kwh")
    nb.md("""
        Un testo si scrive tra virgolette. Per mostrare più cose insieme, o una frase intera, c'è
        `print`: accetta più valori separati da virgola e li stampa con uno spazio in mezzo.
    """)
    nb.code("""
        cliente = "Panificio Bianchi"

        print("Cliente:", cliente)
        print("Consumo di settembre:", consumo_kwh, "kWh")
    """)
    nb.md("""
        Il numero tra parentesi quadre a sinistra di ogni cella dice in che ordine è stata eseguita. Il
        kernel ricorda tutto quello che ha eseguito e niente di quello che non ha eseguito. Questa cella
        dà errore apposta: leggiamo l'ultima riga del messaggio.
    """)
    nb.code('print("Consumo di agosto:", consumo_agosto, "kWh")', errore=True)
    nb.md("""
        `NameError: name 'consumo_agosto' is not defined`: nessuna cella ha creato quel nome, oppure la
        cella che lo crea non è stata ancora eseguita. È l'errore tipico di chi salta una cella o le
        esegue in ordine sparso, e il rimedio è quasi sempre lo stesso: eseguire le celle dall'alto.
    """)
    nb.md("""
        Due pulsanti in cima al notebook fanno il grosso del lavoro. **Run All** esegue tutte le celle
        dall'alto in basso: è la prova che il notebook funziona per intero. **Restart** riavvia il
        kernel: la memoria si svuota, le variabili spariscono, il codice resta. Si usa quando "non torna
        niente": una variabile ha un valore che non ci spieghiamo, una cella non finisce mai, l'output
        non cambia. Restart, poi Run All.
    """)
    nb.prova_tu(
        richiesta="""
            Un contatore registra una lettura ogni quarto d'ora. Nella cella qui sotto calcola quante
            letture fa in un giorno (24 ore, 4 letture l'ora), salvale in `letture_giorno` e mostrale
            come ultima riga. Poi esegui la verifica.
        """,
        starter="""
            letture_giorno = ...
            letture_giorno
        """,
        soluzione="""
            letture_giorno = 24 * 4
            letture_giorno
        """,
        verifica="""
            assert letture_giorno == 96, "❌ letture_giorno: le ore di un giorno per le letture in un'ora"
        """,
    )
    nb.box("ricorda", """
        - **Shift+Invio** esegue la cella; l'ultima espressione è l'output.
        - Il kernel ricorda solo quello che ha eseguito, nell'ordine in cui lo ha eseguito.
        - Se non torna niente: **Restart**, poi Run All.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Le scorciatoie che servono davvero", intro="""
        Una cella ha due stati: in modifica, quando il cursore è dentro e scriviamo, e selezionata,
        quando è evidenziata e i tasti diventano comandi. **Esc** passa da modifica a selezionata,
        **Invio** torna dentro. Con la cella selezionata bastano questi.
    """)
    nb.md("""
        | Tasto | Cosa fa |
        |---|---|
        | **Shift+Invio** | esegue la cella e passa alla successiva (funziona anche in modifica) |
        | **A** / **B** | nuova cella sopra (*above*) / sotto (*below*) |
        | **M** / **Y** | la cella diventa Markdown / codice |
        | **D D** | cancella la cella (D premuto due volte) |
        | **Ctrl+S** | salva il notebook (funziona sempre) |
    """)
    nb.md("""
        Su Mac, **Cmd** al posto di **Ctrl**. Tutto il resto si trova nei menu e nei pulsanti che
        compaiono passando il mouse sopra una cella: le scorciatoie servono a non staccare le mani dalla
        tastiera, niente di più.
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Markdown e i riquadri", intro="""
        Le celle di testo si scrivono in Markdown: testo semplice con qualche segno per la
        formattazione. Le regole che servono stanno in sei righe, e il modo migliore per vederle è
        guardare una cella da dentro.
    """)
    nb.md("""
        Fai doppio clic su questa cella: compare il Markdown che la genera. Poi **Shift+Invio** per
        tornare al testo formattato. Qui dentro ci sono un **grassetto**, del `codice` e un elenco:

        - un titolo si fa con `#`, `##` o `###` a inizio riga: meno cancelletti, titolo più grande
        - il grassetto con due asterischi prima e due dopo, `**così**`
        - un elenco con un trattino e uno spazio a inizio riga
        - il codice dentro al testo tra due apici inversi, `` `così` ``
        - una riga vuota separa i paragrafi
    """)
    nb.md("""
        Nei notebook incontrerai questi riquadri, sempre con gli stessi colori: grigio per una nota a
        margine, rosso quando qualcosa può andare storto, viola per un approfondimento che si può
        saltare, verde per gli esercizi, ambra per le cose da ricordare a fine sezione. Uno per tipo,
        qui sotto.
    """)
    nb.box("nota", """
        Una precisazione a margine, come questa: il file di un notebook finisce in `.ipynb` (IPython
        Notebook, il vecchio nome di Jupyter) e contiene celle e output insieme. Se hai fretta, le note
        si saltano e ci si torna dopo.
    """)
    nb.box("attenzione", """
        Una cella modificata non è una cella eseguita: finché non premi **Shift+Invio**, il kernel usa
        ancora la versione vecchia e l'output sotto non c'entra più con il codice sopra. Quando un
        risultato non ha senso, è la prima cosa da controllare.
    """)
    nb.box("approfondimento", """
        Un pezzo in più per chi vuole il perché: non serve per gli esercizi, e la coda nel titolo è seria.

        Quando esegui una cella, VS Code manda il testo al kernel, un processo Python che gira in
        sottofondo. Il kernel esegue, tiene in memoria le variabili e rimanda l'output, che VS Code
        mostra sotto la cella e salva nel file `.ipynb` insieme al codice. Per questo un notebook
        riaperto il giorno dopo mostra ancora i vecchi output, ma le variabili non ci sono più: il
        processo è morto con la chiusura. Restart kernel fa la stessa cosa a comando: chiude quel
        processo e ne apre uno nuovo, vuoto.
    """, titolo="Cosa succede quando premi Shift+Invio")
    nb.md("""
        Il verde è l'esercizio: un Prova tu in mezzo a una sezione, da due o tre minuti, o un Esercizio
        alla fine del notebook. Sotto al riquadro c'è una cella da completare al posto dei `...` e una
        cella di verifica, da eseguire senza modificare: ✅ se va bene, ❌ e cosa controllare se no.
    """)
    nb.prova_tu(
        richiesta="""
            Clicca nella cella di codice qui sotto, premi **Esc**, poi **A** e **M**: hai una cella
            Markdown nuova sopra. Entra con Invio, scrivi un titolo di terzo livello e un elenco di due
            voci, poi Shift+Invio. Infine completa la cella di codice: in `titolo` il Markdown che
            produce un titolo di secondo livello con il testo `Report consumi`, in `grassetto` quello
            che produce la parola `urgente` in grassetto.
        """,
        starter="""
            titolo = "..."
            grassetto = "..."

            print(titolo)
            print(grassetto)
        """,
        soluzione="""
            titolo = "## Report consumi"
            grassetto = "**urgente**"

            print(titolo)
            print(grassetto)
        """,
        verifica="""
            assert titolo == "## Report consumi", "❌ titolo: due cancelletti, uno spazio, poi il testo"
            assert grassetto == "**urgente**", "❌ grassetto: due asterischi prima e due dopo la parola"
        """,
    )
    nb.box("ricorda", """
        - `#` per i titoli, `**` per il grassetto, `-` per gli elenchi, `` ` `` per il codice.
        - Nel riquadro verde si completa la cella con i `...`; la cella di verifica non si tocca.
        - Il viola si può saltare, il rosso no.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il primo report",
        scenario="""
            Ufficio Analisi Consumi, ore 9. Il capo passa e chiede quanto ha consumato il Panificio
            Bianchi a settembre. Lo sappiamo: 1480 kWh. Vorremmo che la risposta la desse Python, così
            la prossima volta cambiamo due numeri e non riscriviamo la frase.
        """,
        richiesta="""
            Crea `cliente` con il testo `Panificio Bianchi` e `consumo_kwh` con il numero 1480. Poi, con
            un solo `print`, stampa una riga con il nome e il consumo, tipo:
            `Consumo di Panificio Bianchi a settembre: 1480 kWh`.
        """,
        suggerimento="`print` accetta più valori separati da virgola: testi tra virgolette, variabili senza.",
        starter="""
            cliente = ...
            consumo_kwh = ...

            print(...)
        """,
        soluzione="""
            cliente = "Panificio Bianchi"
            consumo_kwh = 1480

            print("Consumo di", cliente, "a settembre:", consumo_kwh, "kWh")
        """,
        verifica="""
            assert cliente == "Panificio Bianchi", "❌ cliente: il nome esatto, tra virgolette"
            assert consumo_kwh == 1480, "❌ consumo_kwh: un numero, senza virgolette"
        """,
        perche="Il nome tra virgolette, il numero senza: `print` accetta entrambi e mette gli spazi da solo.",
    )
    nb.esercizio(
        titolo="Il badge",
        bis=True,
        scenario="""
            Primo giorno in sala controllo: all'ingresso chiedono nome e ruolo per il badge. Lo
            compiliamo con Python, tanto per cominciare a scrivere qualcosa di nostro.
        """,
        richiesta="""
            Crea `nome` con il tuo nome e `ruolo` con il tuo ruolo in azienda, entrambi testi tra
            virgolette. Poi stampa una riga con tutti e due, tipo `Giulia Ferri · Analista consumi`.
        """,
        starter="""
            nome = ...
            ruolo = ...

            print(...)
        """,
        soluzione="""
            nome = "Giulia Ferri"
            ruolo = "Analista consumi"

            print(nome, "·", ruolo)
        """,
        verifica="""
            assert type(nome) is str and len(nome) > 0, "❌ nome: un testo tra virgolette, non vuoto"
            assert type(ruolo) is str and len(ruolo) > 0, "❌ ruolo: un testo tra virgolette, non vuoto"
        """,
    )
    return nb
