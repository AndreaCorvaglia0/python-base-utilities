"""03 · Codice leggibile."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="03",
        file="03_Codice_leggibile",
        titolo="Codice leggibile",
        blocco=1,
        giornata=1,
        intento=(
            "Il notebook presenta i commenti, le celle Markdown, le docstring e le regole principali di PEP 8, "
            "cioè gli strumenti con cui si scrive codice che resta comprensibile anche quando lo si rilegge "
            "dopo qualche mese."
        ),
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
        Un commento comincia con il carattere `#` e prosegue fino alla fine della riga. Python lo
        ignora, perché è scritto per chi legge il codice e non per l'interprete. Un buon commento non
        ripete quello che il codice dice già, ma aggiunge l'informazione che dal codice non si ricava,
        di solito il motivo di una scelta. Nella cella qui sotto c'è un esempio di commento che non aiuta.
    """)
    nb.code("""
        farina_g = 500

        # divido per 4 e moltiplico per 6
        farina_g = farina_g / 4 * 6
        farina_g   # Output: 750.0
    """)
    nb.md("""
        Questo commento descrive l'operazione che la riga successiva mostra già, quindi chi legge lo
        salta senza ricavarne nulla. Inoltre, se un giorno il calcolo cambia e il commento no, il
        commento finisce per dire una cosa falsa. Manca invece proprio quello che dal codice non si
        vede, cioè da dove vengono il 4 e il 6, ed è l'informazione che la versione seguente aggiunge.
    """)
    nb.code("""
        farina_g = 500

        # la ricetta è per 4 persone, a cena siamo in 6
        farina_g = farina_g / 4 * 6
        farina_g   # Output: 750.0
    """)
    nb.md("""
        Per convenzione il commento si scrive sulla riga sopra il codice a cui si riferisce, in
        italiano, con l'iniziale minuscola e senza punto finale. Un commento in coda alla riga si usa
        soltanto quando è molto breve, come i `# Output:` che compaiono negli esempi di questo corso.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Celle Markdown", intro="""
        Le celle Markdown contengono il testo del notebook. Servono a dire qual è la domanda a cui
        l'analisi risponde, quali dati usiamo e che cosa abbiamo trovato, in modo che chi apre il
        notebook possa seguire il ragionamento leggendo soltanto il testo, senza dover ricostruirlo
        dal codice.
    """)
    nb.md("""
        Lo schema seguente, scritto con la sintassi Markdown in chiaro, mostra una struttura semplice
        che va bene per la maggior parte delle analisi, con un titolo, la domanda, una sezione sui dati
        e una sui risultati:

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
        Tra un blocco e l'altro conviene mettere, prima di ogni cella di codice, una frase che dica che
        cosa stiamo per fare e, quando l'output non è ovvio, una frase dopo che ne commenti il
        risultato. La sintassi necessaria è poca: `# Titolo` e `## Sezione` per i titoli,
        `**grassetto**` per mettere in evidenza una parola, `- elenco` per gli elenchi puntati e i
        backtick per il codice.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Docstring", intro="""
        Una funzione si definisce con la parola chiave `def`, seguita dal nome e dai parametri tra
        parentesi tonde; il corpo è indentato e l'istruzione `return` restituisce il risultato. Le
        funzioni sono trattate per esteso nel notebook su funzioni e controllo del flusso, mentre in
        questa sezione ci interessa soltanto la riga che sta subito sotto il `def`.
    """)
    nb.code("""
        def area_rettangolo(base, altezza):
            \"\"\"Area di un rettangolo, data la base e l'altezza.\"\"\"
            return base * altezza


        area_rettangolo(4, 2.5)   # Output: 10.0
    """)
    nb.md("""
        La stringa racchiusa tra tre virgolette subito sotto il `def` si chiama docstring. Descrive che
        cosa fa la funzione e, quando non è ovvio, che cosa riceve e che cosa restituisce. A differenza
        di un commento, Python la conserva insieme alla funzione, e `help()` la mostra a richiesta.
    """)
    nb.code("help(area_rettangolo)")
    nb.md("""
        L'output di `help` riporta la firma della funzione, con i nomi dei parametri, e sotto la
        docstring. Lo stesso vale per qualunque funzione, nostra o di una libreria, per esempio
        `help(round)` o `help(sum)`. La docstring si può leggere anche direttamente, come attributo
        della funzione, con `area_rettangolo.__doc__`.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("PEP 8", intro="""
        PEP 8 è la guida di stile ufficiale di Python e stabilisce, tra le altre cose, come usare gli
        spazi, come chiamare le variabili e dove andare a capo. Seguirla rende il codice uniforme, e
        quindi più facile da leggere per chiunque conosca Python. Partiamo da una cella che funziona
        correttamente ma ignora queste regole.
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
        Le regole che si incontrano più spesso sono poche. I nomi di variabili e funzioni si scrivono in
        `snake_case`, cioè in minuscolo con le parole separate da un underscore, e dicono che cosa
        contengono: `voti_matematica` invece di `Voti`, `media` invece di `x`, `calcola_media` invece
        di `Calc`. L'indentazione è di quattro spazi. Si mette uno spazio attorno a `=` e agli
        operatori e uno dopo ogni virgola, ma nessuno subito dentro le parentesi. Le righe, infine, non
        devono essere troppo lunghe: PEP 8 indica 79 caratteri, e molti team accettano fino a 100.
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
        La cella riscritta dà lo stesso risultato della prima. La riga troppo lunga è stata divisa in
        due `print` e la funzione ha ora un nome che dice che cosa fa. Anche le due righe vuote prima e
        dopo il `def` vengono da PEP 8, che le usa per separare la definizione di una funzione dal
        codice che la utilizza.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Rinominare e documentare una funzione",
        scenario="""
            In un notebook condiviso c'è la funzione `f` qui sotto. Riceve un prezzo e una percentuale
            di sconto e restituisce il prezzo scontato, ma né il suo nome né quelli dei parametri lo
            lasciano capire.
        """,
        richiesta="""
            Lascia `f` com'è, perché serve al confronto. Sotto, riscrivila con il nome
            `prezzo_scontato`, i parametri `prezzo` e `sconto_percentuale` e una docstring di una riga.
            Il comportamento non deve cambiare: `prezzo_scontato(80, 15)` restituisce `68.0`, come
            `f(80, 15)`.
        """,
        suggerimento="la docstring va sulla prima riga sotto il `def`, racchiusa tra tre virgolette.",
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
            Questa cella calcola il totale della spesa: somma i prezzi di cinque prodotti e toglie un
            buono da 5 euro della tessera del supermercato. Il calcolo è giusto, ma la cella non segue
            PEP 8 e il suo commento ripete il codice.
        """,
        richiesta="""
            Lascia le prime due righe come sono, perché servono al confronto. Sotto, riscrivile
            seguendo PEP 8: la lista si chiama `prezzi`, il buono va nella variabile `buono` e il
            risultato in `totale`. Al posto del commento che ripete il codice, scrivine uno che spieghi
            che cosa sono i 5 euro. Alla fine `totale` vale 22.3, lo stesso valore di `t`.
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
