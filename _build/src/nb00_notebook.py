"""00 · Jupyter e i notebook."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="00",
        file="00_Notebook",
        titolo="Jupyter e i notebook",
        blocco=1,
        giornata=1,
        intento="Il codice del corso si scrive e si esegue nei notebook: qui vediamo come sono fatti e come si usano.",
        obiettivi=[
            "spiegare cos'è un notebook e come lavorano celle e kernel",
            "eseguire una cella di codice e scrivere una cella Markdown",
            "usare le scorciatoie da tastiera principali",
        ],
        tempo=20,
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("L'obiettivo del corso", intro="""
        Oggi molto codice lo scrive un agente per il coding, come Copilot in VS Code o Claude Code: gli
        si descrive a parole cosa serve e l'agente scrive il codice.
    """)
    nb.md("""
        Quel codice va letto e controllato da noi: capire quali librerie usa, cosa fa ogni riga, cosa
        dice un messaggio di errore. Per imparare a leggerlo cominciamo a scriverlo a mano, da questo
        notebook.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Cos'è Jupyter Notebook", intro="""
        *Jupyter Notebook* è un ambiente di sviluppo interattivo (*Integrated Development Environment*,
        IDE) che permette di creare e condividere documenti che contengono codice eseguibile, testo
        formattato, immagini e grafici. È molto usato nell'analisi dei dati, nel *machine learning*,
        nella ricerca scientifica e nella didattica.
    """)
    nb.md("""
        Il nome **Jupyter** richiama tre dei principali linguaggi supportati: **Julia**, **Python** e **R**.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Come funziona un notebook", intro="""
        Jupyter Notebook si basa su documenti chiamati **notebook**, che possono essere eseguiti su un
        server locale o remoto. Un notebook è composto da una serie di **celle** (*cells*), che possono
        contenere codice, testo formattato con la sintassi *Markdown* e immagini.
    """)
    nb.md("""
        Le celle di codice si eseguono in modo interattivo: il risultato delle operazioni compare subito,
        all'interno del notebook, sotto la cella, anche sotto forma di grafici e tabelle.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Come si usa un notebook", intro="""
        I notebook del corso si aprono in VS Code, con un doppio clic sul file `.ipynb`.
    """)
    nb.md("""
        Per eseguire una cella di codice, clicca sulla cella e premi il pulsante **Run** (il triangolo a
        sinistra della cella) oppure **Shift + Invio** sulla tastiera.
    """)
    nb.md("""
        Per aggiungere testo formattato con la sintassi *Markdown*, aggiungi una cella con il pulsante
        **+ Markdown** in cima al notebook. Con i comandi *Markdown* si creano titoli, elenchi, link e
        immagini.
    """)
    nb.box("nota", "Per salvare il notebook, usa la combinazione di tasti **Ctrl + S** (su Mac **Cmd + S**).")

    # ------------------------------------------------------------------ 5
    nb.sezione("Il kernel", intro="""
        Il **kernel** è il processo che esegue il codice Python all'interno del notebook. Se il kernel
        sembra bloccato o non risponde, puoi riavviarlo con il pulsante **Restart** in cima al notebook.
    """)
    nb.md("""
        Restart svuota la memoria: le variabili spariscono, il codice resta. **Run All**, accanto, esegue
        tutte le celle dall'alto in basso. Quando un risultato non torna: Restart, poi Run All.
    """)
    nb.md("Questa cella mostra quale Python sta usando il kernel:")
    nb.code("""
        import sys

        sys.executable
    """)
    nb.md("""
        Il percorso deve contenere `.venv`, la cartella con il Python e le librerie del corso. Se non la
        contiene, il kernel va cambiato con **Select Kernel**, in alto a destra.
    """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Esempio di cella di codice", intro="""
        Ecco un semplice esempio di codice Python che calcola la somma di due numeri:
    """)
    nb.code("""
        # esempio di codice Python che calcola la somma di due numeri
        a = 10
        b = 20
        c = a + b
        print(c)  # Output: 30
    """)

    # ------------------------------------------------------------------ 7
    nb.sezione("Esempio di cella Markdown", intro="""
        Qui sotto c'è una cella *Markdown* con vari elementi di formattazione. Fai doppio clic sulla
        cella per vedere il testo che la genera, poi **Shift + Invio** per tornare alla vista formattata.
    """)
    nb.md("""
        # Titolo di primo livello

        ## Titolo di secondo livello

        ### Titolo di terzo livello

        Questo è un testo in **grassetto** e questo è un testo in *corsivo*.

        Ecco una lista non ordinata:
        - Elemento 1
        - Elemento 2
        - Elemento 3

        Ecco una lista ordinata:
        1. Primo elemento
        2. Secondo elemento
        3. Terzo elemento

        Ecco un blocco di codice:

        ```python
        a = 10
        b = 20
        c = a + b
        print(c)
        ```

        Per altre opzioni di formattazione c'è la [guida al Markdown](https://www.markdownguide.org/basic-syntax/).
    """)

    # ------------------------------------------------------------------ 8
    nb.sezione("Le scorciatoie da tastiera", intro="""
        Alcune scorciatoie rendono più rapido l'uso dei notebook:
    """)
    nb.md("""
        - **Modalità comando** (premi `Esc` per attivarla):
            - `A`: inserisci una nuova cella **sopra** la cella selezionata.
            - `B`: inserisci una nuova cella **sotto** la cella selezionata.
            - `M`: cambia il tipo di cella in **Markdown**.
            - `Y`: cambia il tipo di cella in **Code**.
            - `D` `D` (premi due volte): elimina la cella selezionata.
        - **Modalità modifica** (premi `Invio` per attivarla):
            - `Ctrl + S`: salva il notebook.
            - `Shift + Invio`: esegui la cella corrente e seleziona quella successiva.
            - `Ctrl + Shift + -`: dividi la cella corrente in due nel punto del cursore.

        Su Mac, `Cmd` al posto di `Ctrl`.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Una cella Markdown e una cella di codice",
        scenario="",
        richiesta="""
            1. Sopra la cella di codice qui sotto, aggiungi una **cella Markdown** con il titolo "Soluzione"
               e sotto il testo "Questa è la soluzione del primo esercizio."
            2. Nella **cella di codice** scrivi `print("Primo comando Python del corso!")`.

            Esegui entrambe le celle per vedere il risultato.
        """,
        starter="""
            # scrivi qui il comando print
            ...
        """,
        soluzione="""
            print("Primo comando Python del corso!")
        """,
        perche="""
            La cella Markdown, vista da dentro:

            ```markdown
            # Soluzione

            Questa è la soluzione del primo esercizio.
            ```
        """,
    )
    nb.esercizio(
        titolo="Il meteo di oggi",
        scenario="",
        richiesta="""
            Crea `citta` con il nome della tua città e `temperatura` con la temperatura di oggi, un
            numero. Poi, con un solo `print`, stampa una riga come `Oggi a Milano ci sono 18 gradi`.
        """,
        suggerimento="`print` accetta più valori separati da virgola: i testi tra virgolette, le variabili senza.",
        starter="""
            citta = ...
            temperatura = ...

            print(...)
        """,
        soluzione="""
            citta = "Milano"
            temperatura = 18

            print("Oggi a", citta, "ci sono", temperatura, "gradi")
        """,
    )
    return nb
