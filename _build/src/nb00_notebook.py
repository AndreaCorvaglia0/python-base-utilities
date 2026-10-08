"""00 · Jupyter e i notebook."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="00",
        file="00_Notebook",
        titolo="Jupyter e i notebook",
        blocco=1,
        giornata=1,
        intento=(
            "In questo notebook vediamo come è fatto un notebook Jupyter e come si usa, perché è lo "
            "strumento in cui scriviamo ed eseguiamo il codice del corso."
        ),
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
        Una parte crescente del codice viene oggi scritta da un agente per il coding, come Copilot in
        VS Code. Anche in quel caso il codice va letto e controllato da chi lo usa, e per riuscirci
        bisogna conoscere il linguaggio in cui è scritto. Per questo nella prima parte del corso
        scriviamo il codice a mano, un'istruzione alla volta, e lo affidiamo a un agente solo
        nell'ultimo blocco.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Cos'è Jupyter Notebook", intro="""
        *Jupyter Notebook* è un ambiente di sviluppo interattivo che permette di creare e condividere
        documenti in cui il codice eseguibile convive con il testo formattato, le immagini e i grafici.
        È molto usato nell'analisi dei dati, nel *machine learning* e nella ricerca scientifica, perché
        tiene insieme in un unico file il codice, i risultati e la loro spiegazione. Il nome **Jupyter**
        richiama tre dei principali linguaggi supportati, **Julia**, **Python** e **R**. Nel corso i
        notebook si aprono e si eseguono in VS Code.

        [Documentazione ufficiale di Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html)
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Le celle di codice", intro="""
        Un notebook è composto da una serie di **celle**, che possono contenere codice oppure testo
        formattato. Per eseguire una cella di codice si clicca sulla cella e si preme **Shift + Invio**,
        oppure il triangolo che compare alla sua sinistra, e il risultato appare subito sotto la cella.
        Delle tre celle qui sotto, la prima stampa un testo con `print`, la seconda mostra che anche
        senza `print` il notebook visualizza il valore dell'ultima riga, e la terza calcola la somma di
        due numeri.
    """)
    nb.code("""
        # esegui questa cella con Shift + Invio
        print("Ciao dal notebook")
    """)
    nb.code("""
        # senza print il notebook mostra il valore dell'ultima riga
        1 + 1
    """)
    nb.code("""
        # esempio di codice Python che calcola la somma di due numeri
        a = 10
        b = 20
        c = a + b
        print(c)  # Output: 30
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Il kernel", intro="""
        Il **kernel** è il processo che esegue il codice Python del notebook e che tiene in memoria le
        variabili create durante il lavoro. Ogni kernel è legato a un interprete Python preciso, e nel
        corso usiamo quello dell'ambiente virtuale del progetto. Il percorso stampato dalla cella qui
        sotto, che indica quale interprete sta usando il kernel, deve quindi contenere `.venv`; se non
        lo contiene, si cambia kernel con **Select Kernel**, in alto a destra.
    """)
    nb.code("""
        # il Python usato dal kernel: il percorso deve contenere .venv
        # (se non c'è, cambia kernel con Select Kernel, in alto a destra)
        import sys

        sys.executable
    """)
    nb.md("""
        Le variabili create in una cella restano disponibili per tutte le altre, perché vivono nella
        memoria del kernel e non nella cella che le ha definite. Le tre celle seguenti assegnano un
        valore a `x`, lo leggono in una cella separata e poi lo incrementano. Se eseguiamo più volte
        l'ultima, `x` cresce di uno a ogni esecuzione, e cresce anche il numero a sinistra della cella,
        che conta le esecuzioni fatte dal kernel.
    """)
    nb.code("""
        x = 5
    """)
    nb.code("""
        x
    """)
    nb.code("""
        # esegui questa cella più volte: x cresce, e cresce il numero a sinistra della cella
        x = x + 1
        x
    """)
    nb.md("""
        Il pulsante **Restart**, in cima al notebook, riavvia il kernel. Il codice scritto nelle celle
        rimane dov'è, ma le variabili create fino a quel momento vengono perse, perché esistevano solo
        nella memoria del processo appena chiuso. Per vederlo, premiamo Restart e poi eseguiamo la cella
        qui sotto, che chiede il valore di `x`: Python risponde con un `NameError`, perché quel nome non
        esiste più. Il pulsante **Run All** esegue di nuovo tutte le celle dall'alto in basso e
        ricostruisce lo stato del notebook.
    """)
    nb.code("""
        x
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Le celle Markdown", intro="""
        Il testo di un notebook si scrive nelle celle *Markdown*, un linguaggio di formattazione molto
        semplice in cui, per esempio, un `#` all'inizio della riga produce un titolo e due asterischi
        intorno a una parola la rendono in grassetto. La cella qui sotto raccoglie gli elementi più
        comuni: titoli, grassetto e corsivo, elenchi e un link. Facendo doppio clic sulla cella se ne
        vede il sorgente, e dopo aver cambiato una parola si torna alla vista formattata con
        **Shift + Invio**.
    """)
    nb.md("""
        # Titolo di primo livello
        ## Titolo di secondo livello

        Un testo in **grassetto** e uno in *corsivo*.

        - Elemento 1
        - Elemento 2

        1. Primo elemento
        2. Secondo elemento

        [Guida al Markdown](https://www.markdownguide.org/basic-syntax/)
    """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Le scorciatoie da tastiera", intro="""
        Le scorciatoie da tastiera rendono più rapido il lavoro con le celle. Quasi tutte si usano in
        modalità comando, che si attiva con `Esc` e in cui i tasti agiscono sulla cella selezionata
        invece di scrivere al suo interno. Le più utili sono queste:

        - `Shift + Invio` esegue la cella e passa alla successiva;
        - `Esc` e poi `A` o `B` inseriscono una nuova cella sopra o sotto quella selezionata;
        - `Esc` e poi `M` o `Y` trasformano la cella in una cella Markdown o di codice;
        - `Esc` e poi `D` due volte eliminano la cella;
        - `Ctrl + S` (su Mac `Cmd + S`) salva il notebook.

        Le due celle che seguono servono per provarle, seguendo le istruzioni scritte nei commenti.
    """)
    nb.code("""
        # esegui, poi premi Esc e B: sotto compare una cella nuova; scrivici prezzo * 2 ed eseguila
        prezzo = 4.5
    """)
    nb.code("""
        # Premi Esc, poi M e Shift + Invio: questa riga diventa un titolo
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi", """
        Sotto gli esercizi che hanno un risultato da controllare trovi una cella con `verifica(...)`, da
        eseguire dopo aver scritto il tuo codice. Se il risultato è corretto la cella stampa ✅,
        altrimenti indica che cosa non torna.
    """)
    nb.esercizio(
        titolo="Una cella Markdown e una cella di codice",
        scenario="",
        richiesta="""
            1. Sopra la cella di codice qui sotto aggiungi una **cella Markdown** con il titolo
               "Soluzione" e, sotto il titolo, il testo "Questa è la soluzione del primo esercizio."
            2. Nella **cella di codice** scrivi `print("Primo comando Python del corso!")`.

            Infine esegui entrambe le celle. La cella Markdown mostra il titolo formattato, mentre la
            cella di codice stampa il messaggio.
        """,
        starter="""
            # scrivi qui il comando print
            ...
        """,
        soluzione="""
            print("Primo comando Python del corso!")
        """,
        perche="""
            Il sorgente della cella Markdown, cioè quello che si vede facendo doppio clic, è il seguente:

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
            Crea una variabile `citta` con il nome della tua città e una variabile `temperatura` con la
            temperatura di oggi, scritta come numero. Poi, con un solo `print`, stampa una riga come
            `Oggi a Milano ci sono 18 gradi`.
        """,
        suggerimento=(
            "`print` accetta più valori separati da virgola e li stampa uno dopo l'altro, separati da uno "
            "spazio. I testi vanno scritti tra virgolette, mentre i nomi delle variabili si scrivono senza."
        ),
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
        verifica="""
            assert isinstance(citta, str) and citta.strip(), "❌ citta deve essere un testo tra virgolette"
            assert isinstance(temperatura, (int, float)), "❌ temperatura deve essere un numero, senza virgolette"
        """,
    )
    return nb
