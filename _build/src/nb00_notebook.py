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
        Oggi molto codice lo scrive un agente per il coding, come Copilot in VS Code. Quel codice va
        letto e controllato da noi: per imparare a leggerlo, cominciamo a scriverlo a mano.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Cos'è Jupyter Notebook", intro="""
        *Jupyter Notebook* è un ambiente interattivo per creare documenti con codice eseguibile, testo
        formattato, immagini e grafici. Il nome richiama tre linguaggi supportati: **Julia**, **Python**
        e **R**. Nel corso i notebook si aprono in VS Code.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Le celle di codice", intro="""
        Un notebook è una serie di **celle**, di codice o di testo. Per eseguire una cella di codice,
        clicca sulla cella e premi **Shift + Invio**, oppure il triangolo a sinistra.
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
        Il **kernel** è il processo che esegue il codice Python del notebook e tiene in memoria le
        variabili, condivise da tutte le celle.
    """)
    nb.code("""
        # il Python usato dal kernel: il percorso deve contenere .venv
        # (se non c'è, cambia kernel con Select Kernel, in alto a destra)
        import sys

        sys.executable
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
        **Restart**, in cima al notebook, riavvia il kernel: le variabili spariscono, il codice resta.
        Premi Restart ed esegui la cella qui sotto: dà `NameError`. Poi premi **Run All**, che esegue
        tutte le celle dall'alto in basso.
    """)
    nb.code("""
        x
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Le celle Markdown", intro="""
        Il testo si scrive in celle *Markdown*. Fai doppio clic sulla cella qui sotto, cambia una parola
        e premi **Shift + Invio** per tornare alla vista formattata.
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
        - `Shift + Invio`: esegui la cella e passa alla successiva
        - `Esc` poi `A` o `B`: nuova cella sopra o sotto
        - `Esc` poi `M` o `Y`: cella Markdown o di codice
        - `Esc` poi `D` `D`: elimina la cella
        - `Ctrl + S` (su Mac `Cmd + S`): salva il notebook
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
        Sotto gli esercizi trovi una cella con `verifica(...)`: eseguila dopo il tuo codice. Se stampa ✅ il
        risultato è giusto, altrimenti dice cosa non torna.
    """)
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
        verifica="""
            assert isinstance(citta, str) and citta.strip(), "❌ citta deve essere un testo tra virgolette"
            assert isinstance(temperatura, (int, float)), "❌ temperatura deve essere un numero, senza virgolette"
        """,
    )
    return nb
