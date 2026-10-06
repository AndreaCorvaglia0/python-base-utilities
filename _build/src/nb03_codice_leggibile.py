"""03 · Codice leggibile."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="03",
        file="03_Codice_leggibile",
        titolo="Codice leggibile",
        blocco=1,
        giornata=1,
        intento="Commenti, celle Markdown, docstring e alcune regole di stile per scrivere codice che si capisce anche rileggendolo dopo qualche mese.",
        obiettivi=[
            "scrivere un commento dove il codice non basta",
            "raccontare un'analisi con le celle Markdown e documentare una funzione con la docstring",
            "applicare le regole essenziali di PEP 8",
        ],
        tempo={"base": 20, "avanzata": 20},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Commenti", intro="""
        Un commento comincia con `#` e Python lo ignora: è scritto per chi legge. Il codice dice già
        cosa fa; il commento serve quando manca il perché. Ecco un commento che non aiuta.
    """)
    nb.code("""
        farina_g = 500

        # divido per 4 e moltiplico per 6
        farina_g = farina_g / 4 * 6
        farina_g   # Output: 750.0
    """)
    nb.md("""
        Il commento ripete il codice: chi legge lo salta, e se il codice cambia resta lì a dire una
        cosa falsa. Manca invece quello che dal codice non si vede: da dove vengono il 4 e il 6.
    """)
    nb.code("""
        farina_g = 500

        # la ricetta è per 4 persone, a cena siamo in 6
        farina_g = farina_g / 4 * 6
        farina_g   # Output: 750.0
    """)
    nb.md("""
        Il commento va sulla riga sopra, in italiano, con la minuscola iniziale e senza punto finale.
        In coda alla riga solo se è molto breve, come i `# Output:` di questi esempi.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Celle Markdown", intro="""
        Le celle Markdown sono il testo del notebook: dicono qual è la domanda, quali dati usiamo e
        cosa abbiamo trovato. Chi apre il notebook deve capirlo leggendo solo il testo.
    """)
    nb.md("""
        Uno schema semplice, con la sintassi Markdown in chiaro:

        ```markdown
        # Voti di matematica della 3B

        **Domanda.** Com'è andato il primo quadrimestre?

        ## Dati
        `voti_3b.csv`: i voti di matematica di 24 studenti, primo quadrimestre.

        ## Risultati
        La media è 6,8; quattro studenti sono sotto il 6.
        ```
    """)
    nb.md("""
        Tra un blocco e l'altro, prima di ogni cella di codice una riga che dice cosa stiamo per fare
        e, se l'output non è ovvio, una riga dopo su cosa è venuto fuori. La sintassi che basta:
        `# Titolo` e `## Sezione`, `**grassetto**`, `- elenco`, il codice tra backtick.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Docstring", intro="""
        Una funzione si definisce con `def`, un nome e i parametri tra parentesi tonde; il corpo è
        indentato e `return` restituisce il risultato. Le funzioni le vediamo nel notebook sulle
        funzioni: qui ci interessa la riga subito sotto il `def`.
    """)
    nb.code("""
        def area_rettangolo(base, altezza):
            \"\"\"Area di un rettangolo, data la base e l'altezza.\"\"\"
            return base * altezza


        area_rettangolo(4, 2.5)   # Output: 10.0
    """)
    nb.md("""
        La stringa tra tre virgolette è la docstring: dice cosa fa la funzione e, se non è ovvio,
        cosa riceve e cosa restituisce. Python la conserva e `help()` la mostra.
    """)
    nb.code("help(area_rettangolo)")
    nb.md("""
        `help` stampa la firma, con i nomi dei parametri, e sotto la docstring. Funziona con
        qualunque funzione, nostra o di una libreria: `help(round)`, `help(sum)`. La docstring si
        legge anche con `area_rettangolo.__doc__`.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("PEP 8", intro="""
        PEP 8 è la guida di stile ufficiale di Python: come spaziare, come chiamare le variabili,
        dove andare a capo. Partiamo da una cella che funziona ma non la segue.
    """)
    nb.code("""
        Voti=[7,8 ,6,9,5]
        def Calc(v):
          m=sum(v)/len(v)
          return m
        x=Calc(Voti)
        print(f"Media: {x:.1f} su {len(Voti)} voti, dal più basso {min(Voti)} al più alto {max(Voti)}, primo quadrimestre")
    """)
    nb.md("""
        Le regole che si incontrano più spesso:

        1. Nomi in `snake_case`: minuscoli, parole separate da underscore. `voti_matematica`, non `Voti`.
        2. Quattro spazi di indentazione.
        3. Uno spazio attorno a `=` e agli operatori, uno dopo ogni virgola, nessuno subito dentro le parentesi.
        4. Righe non troppo lunghe: PEP 8 indica 79 caratteri, molti team arrivano a 100.
        5. Nomi che dicono cosa contengono: `media`, non `x`; `calcola_media`, non `Calc`.
    """)
    nb.code("""
        voti_matematica = [7, 8, 6, 9, 5]


        def calcola_media(voti):
            \"\"\"Media aritmetica di una lista di voti.\"\"\"
            return sum(voti) / len(voti)


        media = calcola_media(voti_matematica)
        print(f"Media: {media:.1f} su {len(voti_matematica)} voti")
        print(f"Voto più basso {min(voti_matematica)}, più alto {max(voti_matematica)}")
    """)
    nb.md("""
        Stesso risultato. La riga lunga è diventata due `print` e la funzione ha un nome che dice
        cosa fa. Anche le due righe vuote prima e dopo il `def` vengono da PEP 8: separano la
        definizione dal codice che la usa.
    """)
    nb.md("Qui il docente mostra Ruff, che sistema da solo spazi, rientri e righe lunghe.", aula="avanzata")

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Rinominare e documentare una funzione",
        scenario="""
            In un notebook condiviso c'è questa funzione `f`: riceve un prezzo e una percentuale di
            sconto e restituisce il prezzo scontato, ma dal nome non si capisce.
        """,
        richiesta="""
            Lascia `f` com'è: serve al confronto. Sotto, riscrivila come `prezzo_scontato`, con i
            parametri `prezzo` e `sconto_percentuale` e una docstring di una riga. Il risultato non
            cambia: `prezzo_scontato(80, 15)` restituisce `68.0`.
        """,
        suggerimento="la docstring è la prima riga sotto il `def`, tra tre virgolette.",
        starter="""
            def f(a, b):
                return a * (1 - b / 100)


            def prezzo_scontato(...):
                ...


            print(f(80, 15), prezzo_scontato(80, 15))
        """,
        soluzione="""
            def f(a, b):
                return a * (1 - b / 100)


            def prezzo_scontato(prezzo, sconto_percentuale):
                \"\"\"Prezzo dopo uno sconto espresso in percentuale.\"\"\"
                return prezzo * (1 - sconto_percentuale / 100)


            print(f(80, 15), prezzo_scontato(80, 15))
        """,
        verifica="""
            assert prezzo_scontato.__doc__, "❌ manca la docstring sotto il def"
            assert round(prezzo_scontato(80, 15), 2) == 68.0, "❌ prezzo_scontato(80, 15) deve restituire 68.0, come f"
            assert prezzo_scontato(prezzo=30, sconto_percentuale=50) == 15.0, "❌ i parametri si chiamano prezzo e sconto_percentuale"
        """,
    )
    nb.esercizio(
        titolo="Riscrivere una cella seguendo PEP 8",
        scenario="""
            Questa cella calcola il totale della spesa: i prezzi di cinque prodotti, meno un buono
            da 5 euro della tessera del supermercato.
        """,
        richiesta="""
            Lascia le prime due righe come sono: servono al confronto. Sotto, riscrivile seguendo
            PEP 8: la lista si chiama `prezzi`, il buono va nella variabile `buono` e il risultato in
            `totale`. Al posto del commento che ripete il codice, scrivine uno che dica cosa sono i
            5 euro. Output atteso: `totale` vale 22.3, come `t`.
        """,
        starter="""
            P=[3.5,2.2 ,4.8,1.9,14.9]
            t=sum( P )-5 # tolgo 5

            prezzi = ...
            buono = ...
            totale = ...
            print(t, totale)
        """,
        soluzione="""
            P=[3.5,2.2 ,4.8,1.9,14.9]
            t=sum( P )-5 # tolgo 5

            prezzi = [3.5, 2.2, 4.8, 1.9, 14.9]
            # buono della tessera del supermercato
            buono = 5
            totale = sum(prezzi) - buono
            print(t, totale)
        """,
        verifica="""
            assert prezzi == [3.5, 2.2, 4.8, 1.9, 14.9], "❌ prezzi: gli stessi cinque valori di P"
            assert buono == 5, "❌ buono: i 5 euro in una variabile"
            assert round(totale, 2) == round(t, 2), "❌ totale deve dare lo stesso risultato di t"
        """,
    )
    return nb
