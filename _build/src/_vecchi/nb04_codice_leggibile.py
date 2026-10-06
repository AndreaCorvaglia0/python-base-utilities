"""04 · Codice leggibile."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="04",
        file="04_Codice_leggibile",
        titolo="Codice leggibile",
        blocco=1,
        giornata=1,
        intento="Un notebook lo rileggono il collega domani e noi tra tre mesi: commenti, docstring e qualche regola di stile bastano a farlo capire senza eseguirlo.",
        obiettivi=[
            "commentare quando serve e scrivere una docstring",
            "usare le celle Markdown per raccontare un'analisi",
            "applicare le cinque regole di stile che contano",
        ],
        tempo={"base": 30, "avanzata": 25},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Commenti", intro="""
        Un commento comincia con `#` e Python lo ignora: è scritto per chi legge. Il codice dice già
        cosa fa; il commento serve quando manca il perché. Due versioni dello stesso calcolo, prima
        quella da non scrivere.
    """)
    nb.code("""
        letture_kwh = [640, 688, 702, 715, 698, 672, 6900, 707, 719, 684, 620, 548]

        # divido la settima lettura per 10
        letture_kwh[6] = letture_kwh[6] / 10
        letture_kwh
    """)
    nb.md("""
        Il commento ripete il codice parola per parola: chi legge lo salta, e quando il codice cambia
        resta lì a dire il falso. Chi apre questo notebook tra un mese vuole sapere un'altra cosa:
        perché proprio luglio, e perché 10.
    """)
    nb.code("""
        letture_kwh = [640, 688, 702, 715, 698, 672, 6900, 707, 719, 684, 620, 548]

        # luglio è arrivato moltiplicato per 10 dal fornitore: correzione in attesa del file giusto
        letture_kwh[6] = letture_kwh[6] / 10
        letture_kwh
    """)
    nb.md("""
        Stesso codice, e adesso si sa che il 10 non fa parte del calcolo ma è una pezza, e che un giorno
        la riga andrà tolta. Forma: sulla riga sopra, in italiano con gli accenti, minuscola iniziale,
        senza punto finale. In coda alla riga solo se è cortissimo.
    """)
    nb.box("nota", """
        Il commento serve in tre casi: una scelta che dal codice non si vede, un numero che viene da
        fuori (una soglia, un'aliquota, un fattore), un rimedio temporaneo. Negli altri casi, prova
        a cancellarlo: se il codice si legge ancora, non serviva.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Markdown nei notebook", intro="""
        Le celle Markdown sono il racconto del notebook. Un collega che lo apre deve capire in
        trenta secondi qual era la domanda, su quali dati abbiamo lavorato e cosa abbiamo trovato,
        senza eseguire niente. Un notebook scritto così è già il report.
    """)
    nb.md("""
        Lo scheletro che funziona, con la sintassi Markdown in chiaro:

        ```markdown
        # Consumi anomali del POD IT001E45678901

        **Domanda.** Il customer care segnala una bolletta di luglio dieci volte più alta del solito.
        Errore di lettura o consumo reale?

        ## Dati
        `letture_pod_2025.csv`: consumi mensili per fascia di sei POD, anno 2025.

        ## Cosa abbiamo trovato
        La lettura F1 di luglio è 10 volte la media degli altri mesi; F2 e F3 sono regolari.
        È un errore di digitazione: segnalato al fornitore il 12/08.
        ```
    """)
    nb.md("""
        Tre blocchi: la domanda e chi la fa, i dati con file e periodo, il risultato con i numeri.
        In mezzo, prima di ogni cella di codice una riga che dice cosa sta per succedere, dopo una
        riga su cosa è venuto fuori. Chi legge solo il testo deve arrivare in fondo lo stesso.
    """)
    nb.box("nota", """
        Sintassi che basta: `# Titolo` e `## Sezione`, `**grassetto**`, `- elenco`, codice tra
        backtick. Il resto si cerca quando serve, ed è raro che serva.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Docstring", intro="""
        Una funzione si definisce con `def`, un nome e i parametri tra tonde; il corpo è indentato e
        `return` restituisce il risultato. Le funzioni le vediamo per bene nel notebook sulle
        condizioni, i cicli e le funzioni: qui ci interessa la riga subito sotto il `def`.
    """)
    nb.code("""
        def energia_intervallo_mwh(potenza_mw, ore):
            \"\"\"Energia in MWh di un intervallo a potenza costante.\"\"\"
            return potenza_mw * ore


        energia_intervallo_mwh(12.4, 0.25)   # Output: 3.1
    """)
    nb.md("""
        La stringa tra tre virgolette è la docstring: una riga che dice cosa fa la funzione e, se
        non è ovvio, cosa riceve e cosa restituisce. Non è un commento qualsiasi: Python la
        conserva, `help()` la mostra e VS Code la fa comparire quando passiamo il mouse sul nome
        della funzione.
    """)
    nb.code("help(energia_intervallo_mwh)")
    nb.md("""
        `help` stampa la firma, con i nomi dei parametri, e sotto la docstring. Funziona su
        qualunque funzione, nostra o di una libreria: `help(round)`, `help(sum)` e, dopo
        `import pandas as pd`, anche `help(pd.read_csv)`. La docstring vive nell'attributo
        `__doc__` della funzione, ed è lì che `help` va a leggerla.
    """)
    nb.code("energia_intervallo_mwh.__doc__   # Output: 'Energia in MWh di un intervallo a potenza costante.'")
    nb.prova_tu(
        richiesta="""
            La funzione `quarti_in_ore` funziona ma non ha docstring. Sostituisci i `...` con una
            docstring di una riga, poi controlla con `help`.
        """,
        starter="""
            def quarti_in_ore(n_quarti):
                ...
                return n_quarti / 4


            help(quarti_in_ore)
        """,
        soluzione="""
            def quarti_in_ore(n_quarti):
                \"\"\"Converte un numero di quarti d'ora in ore.\"\"\"
                return n_quarti / 4


            help(quarti_in_ore)
        """,
        verifica="""
            assert quarti_in_ore.__doc__, "❌ quarti_in_ore: la docstring è la stringa tra tre virgolette, prima riga sotto il def"
            assert quarti_in_ore(6) == 1.5, "❌ quarti_in_ore(6) deve restituire 1.5: il corpo della funzione non va cambiato"
        """,
    )

    # ------------------------------------------------------------------ 4
    nb.sezione("PEP 8 in cinque regole", intro="""
        PEP 8 è la guida di stile ufficiale di Python: come spaziare, come chiamare le cose, dove
        andare a capo. Le regole sono molte; quelle che si incontrano ogni giorno sono cinque.
        Partiamo da una cella scritta come capita spesso di trovarla.
    """)
    nb.code("""
        PrezzoKwh=0.21
        Consumi=[1250,830 ,1040]
        def Calc(c,p):
          t=sum(c)*p
          return t
        x=Calc(Consumi,PrezzoKwh)
        print(f"Totale: {x:.2f} euro, calcolato con il prezzo unico {PrezzoKwh} su {len(Consumi)} fasce e {sum(Consumi)} kWh complessivi")
    """)
    nb.md("""
        Funziona, e nessuno vorrebbe leggerlo. Le cinque regole, nell'ordine in cui le viola:

        1. Nomi in `snake_case`: minuscoli, parole separate da underscore. `prezzo_kwh`, non `PrezzoKwh`.
        2. Quattro spazi di indentazione, sempre: VS Code li mette con **Tab**.
        3. Uno spazio attorno a `=` e dopo ogni virgola, nessuno dentro le parentesi.
        4. Righe sotto i 100 caratteri: se una riga non ci sta, di solito contiene due idee.
        5. Nomi che dicono cosa contengono: `costo`, non `x`; `consumi_kwh`, non `c`.
    """)
    nb.code("""
        prezzo_kwh = 0.21
        consumi_kwh = [1250, 830, 1040]


        def costo_totale(consumi, prezzo):
            \"\"\"Costo in euro di una lista di consumi in kWh a prezzo unico.\"\"\"
            return sum(consumi) * prezzo


        costo = costo_totale(consumi_kwh, prezzo_kwh)
        print(f"Totale: {costo:.2f} euro")
        print(f"Prezzo unico {prezzo_kwh} su {len(consumi_kwh)} fasce, {sum(consumi_kwh)} kWh")
    """)
    nb.md("""
        Stesso risultato, e si legge senza decifrare. La riga lunga è diventata due `print`, la
        funzione ha un nome che dice cosa restituisce e una docstring. Le due righe vuote prima e
        dopo un `def` sono anche loro PEP 8: separano la definizione da quello che la usa.
    """)
    nb.box("nota", """
        Il limite di 100 caratteri non è sacro: PEP 8 dice 79, molti team scelgono 88 o 100. Conta
        che il team ne scelga uno e lo scriva in `pyproject.toml`, dove lo legge Ruff: nel nostro
        c'è `line-length = 100`.
    """)
    nb.prova_tu(
        richiesta="""
            Riscrivi la cella seguendo le cinque regole: stesso risultato, nomi che dicono cosa
            contengono, spazi al posto giusto. Il risultato finale si chiami `energia_mwh`.
        """,
        starter="""
            P=[12.4,12.9 ,13.1,12.6]
            E=sum( P )/4
            E
        """,
        soluzione="""
            potenze_mw = [12.4, 12.9, 13.1, 12.6]
            energia_mwh = sum(potenze_mw) / 4
            energia_mwh
        """,
        verifica="""
            assert round(energia_mwh, 2) == 12.75, "❌ energia_mwh: la somma delle quattro potenze divisa per 4, con questo nome"
        """,
    )
    nb.md("""
        A mano si fa per imparare a vederle. Spazi, rientri e righe lunghe, nel lavoro di tutti i
        giorni, li sistema uno strumento, Ruff, che vedremo quando leggeremo il codice scritto da
        un agente; i nomi che dicono cosa contengono restano compito nostro.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il notebook del collega",
        scenario="""
            Nel notebook del report mensile c'è questa funzione, scritta da un collega che ora è in
            un altro team. Funziona, e nessuno la tocca perché nessuno sa cosa sono `a`, `b` e quel
            `1.1`. Prima di riusarla dobbiamo poterla leggere, e il prossimo che la apre deve capirla
            senza chiamare nessuno.
        """,
        richiesta="""
            Lascia `f` dov'è: serve al confronto. Sotto, riscrivila come `costo_bolletta` con due
            parametri che dicono cosa sono, `consumo_kwh` e `prezzo_kwh`, e una docstring di una
            riga che spieghi anche il fattore `1.1`: è l'IVA al 10%. Dentro la funzione, prima del
            `return`, metti il `1.1` in una variabile `fattore_iva` e usala nel conto: il risultato
            deve restare lo stesso.
        """,
        suggerimento="la docstring è la prima riga sotto il `def`, tra tre virgolette.",
        starter="""
            def f(a, b):
                return a * b * 1.1


            def costo_bolletta(...):
                ...


            print(f(1250, 0.21), costo_bolletta(1250, 0.21))
        """,
        soluzione="""
            def f(a, b):
                return a * b * 1.1


            def costo_bolletta(consumo_kwh, prezzo_kwh):
                \"\"\"Costo in euro di una bolletta: consumo per prezzo, più IVA al 10%.\"\"\"
                fattore_iva = 1.1
                return consumo_kwh * prezzo_kwh * fattore_iva


            print(f(1250, 0.21), costo_bolletta(1250, 0.21))
        """,
        verifica="""
            assert costo_bolletta.__doc__, "❌ costo_bolletta: manca la docstring, la riga tra tre virgolette sotto il def"
            assert "iva" in costo_bolletta.__doc__.lower(), "❌ costo_bolletta: la docstring deve dire che il fattore 1.1 è l'IVA"
            assert round(costo_bolletta(1250, 0.21), 2) == round(f(1250, 0.21), 2), "❌ costo_bolletta deve dare lo stesso risultato di f"
            assert round(costo_bolletta(830, 0.19), 2) == 173.47, "❌ costo_bolletta(830, 0.19): consumo per prezzo per 1.1"
        """,
        perche="La docstring dice il perché del 1.1, che dal codice non si vede. Il numero ha un nome dentro la funzione: quando l'IVA cambia, si cambia una riga e si sa quale.",
        passo_in_piu=dict(
            testo="""
                Nel notebook del collega c'era anche questa riga:
                `s = f(1250, 0.21) + f(830, 0.19) + f(1040, 0.17)` (i tre consumi sono le fasce F1,
                F2 e F3 dello stesso cliente, ognuna con il suo prezzo). Riscrivila con
                `costo_bolletta`, un nome che dica cosa contiene (`totale_bolletta`) e un commento di
                una riga che spieghi perché tre chiamate.
            """,
            starter="""
                # ...
                totale_bolletta = ...
                totale_bolletta
            """,
            soluzione="""
                # una chiamata per fascia: F1, F2 e F3 hanno consumi e prezzi diversi
                costo_f1 = costo_bolletta(1250, 0.21)
                costo_f2 = costo_bolletta(830, 0.19)
                costo_f3 = costo_bolletta(1040, 0.17)
                totale_bolletta = costo_f1 + costo_f2 + costo_f3
                totale_bolletta
            """,
            verifica="""
                assert round(totale_bolletta, 2) == 656.7, "❌ totale_bolletta: la somma dei costi delle tre fasce"
            """,
        ),
    )
    nb.esercizio(
        titolo="La funzione della sala controllo",
        bis=True,
        scenario="""
            In sala controllo gira da anni una funzione `g(l, p)` che nessuno ricorda di aver scritto
            e tutti usano: riceve le quattro potenze medie quartorarie di un'ora, in MW, e un prezzo
            in euro/MWh, e restituisce il ricavo dell'ora. Quel `/ 4` è il passaggio da MW quartorari
            a MWh. Il nuovo responsabile vuole poterla leggere senza chiedere.
        """,
        richiesta="""
            Lascia `g` dov'è: serve al confronto. Sotto, riscrivila come `ricavo_ora` con due
            parametri che dicono cosa sono (`potenze_mw` e `prezzo_mwh`), una docstring di una riga
            che spieghi anche il `/ 4`, e lo stesso risultato.
        """,
        suggerimento="un passaggio intermedio con un nome, `energia_mwh = sum(potenze_mw) / 4`, si legge meglio di un conto tutto nel `return`.",
        starter="""
            def g(l, p):
                return sum(l) / 4 * p


            def ricavo_ora(...):
                ...


            print(g([12.4, 12.9, 13.1, 12.6], 98.4), ricavo_ora([12.4, 12.9, 13.1, 12.6], 98.4))
        """,
        soluzione="""
            def g(l, p):
                return sum(l) / 4 * p


            def ricavo_ora(potenze_mw, prezzo_mwh):
                \"\"\"Ricavo in euro di un'ora: i quattro MW quartorari diventano MWh dividendo per 4.\"\"\"
                energia_mwh = sum(potenze_mw) / 4
                return energia_mwh * prezzo_mwh


            print(g([12.4, 12.9, 13.1, 12.6], 98.4), ricavo_ora([12.4, 12.9, 13.1, 12.6], 98.4))
        """,
        verifica="""
            assert ricavo_ora.__doc__, "❌ ricavo_ora: manca la docstring, la riga tra tre virgolette sotto il def"
            assert round(ricavo_ora([12.4, 12.9, 13.1, 12.6], 98.4), 2) == round(g([12.4, 12.9, 13.1, 12.6], 98.4), 2), "❌ ricavo_ora deve dare lo stesso risultato di g"
            assert round(ricavo_ora([10, 10, 10, 10], 100), 2) == 1000.0, "❌ ricavo_ora([10, 10, 10, 10], 100): 10 MWh per 100 euro/MWh"
        """,
    )
    nb.esercizio(
        titolo="La cella del turno di notte",
        scenario="""
            Ogni mattina l'ufficio Misure lancia questa cella per il costo dei consumi notturni di
            una cabina: cinque letture in kWh, tutte in fascia F3. Il commento ripete il codice e
            dello `0.17` non dice niente, ma è il prezzo F3 del listino 2025 e a gennaio cambierà.
            Chi la apre a gennaio deve trovarlo al primo colpo.
        """,
        richiesta="""
            Lascia le prime due righe come sono: servono al confronto. Sotto, riscrivile seguendo
            le cinque regole: la lista si chiama `consumi_kwh`, il prezzo va in una variabile sua,
            `prezzo_f3`, e il risultato in `costo_notte`. Al posto del commento che ripete il
            codice scrivine uno che dica da dove viene lo `0.17`.
        """,
        suggerimento="il commento va sulla riga sopra `prezzo_f3` e dice quello che dal codice non si vede.",
        starter="""
            L=[310,295 ,288,402,276]
            c=sum( L )*0.17 # moltiplico la somma per 0.17


            consumi_kwh = ...
            prezzo_f3 = ...
            costo_notte = ...
            print(c, costo_notte)
        """,
        soluzione="""
            L=[310,295 ,288,402,276]
            c=sum( L )*0.17 # moltiplico la somma per 0.17


            consumi_kwh = [310, 295, 288, 402, 276]
            # prezzo F3 del listino 2025, in euro/kWh: da aggiornare a gennaio
            prezzo_f3 = 0.17
            costo_notte = sum(consumi_kwh) * prezzo_f3
            print(c, costo_notte)
        """,
        verifica="""
            assert consumi_kwh == [310, 295, 288, 402, 276], "❌ consumi_kwh: le stesse cinque letture di L, con il nome nuovo"
            assert prezzo_f3 == 0.17, "❌ prezzo_f3: lo 0.17 del listino, in una variabile sua"
            assert round(costo_notte, 2) == round(c, 2), "❌ costo_notte deve dare lo stesso risultato di c: somma delle letture per il prezzo"
        """,
        perche="Il commento nuovo dice da dove viene il numero e quando scade, cose che dal codice non si vedono. Con il prezzo in una variabile, a gennaio si cambia una riga e si sa quale.",
    )
    nb.esercizio(
        titolo="Le perdite della cabina",
        bis=True,
        scenario="""
            L'ufficio Bilancio energetico stima ogni mese le perdite della rete in bassa tensione
            con questa cella: l'energia immessa in cabina nelle tre decadi del mese, in MWh,
            moltiplicata per `0.062`. Quel numero è il 6,2% di perdita concordato con la direzione
            tecnica, ma il commento dice solo che si moltiplica. Il revisore interno vuole capirlo
            senza ripescare la mail di due anni fa.
        """,
        richiesta="""
            Lascia le prime due righe come sono: servono al confronto. Sotto, riscrivile seguendo
            le cinque regole: la lista si chiama `immessa_mwh`, il fattore va in una variabile sua,
            `quota_perdite`, e il risultato in `perdite_mwh`. Al posto del commento che ripete il
            codice scrivine uno che dica da dove viene lo `0.062`.
        """,
        suggerimento="il commento va sulla riga sopra `quota_perdite` e dice quello che dal codice non si vede.",
        starter="""
            E=[1820,1765 ,1910]
            p=sum( E )*0.062  # moltiplico per 0.062


            immessa_mwh = ...
            quota_perdite = ...
            perdite_mwh = ...
            print(p, perdite_mwh)
        """,
        soluzione="""
            E=[1820,1765 ,1910]
            p=sum( E )*0.062  # moltiplico per 0.062


            immessa_mwh = [1820, 1765, 1910]
            # perdita della rete BT concordata con la direzione tecnica: 6,2% dell'energia immessa
            quota_perdite = 0.062
            perdite_mwh = sum(immessa_mwh) * quota_perdite
            print(p, perdite_mwh)
        """,
        verifica="""
            assert immessa_mwh == [1820, 1765, 1910], "❌ immessa_mwh: gli stessi tre valori di E, con il nome nuovo"
            assert quota_perdite == 0.062, "❌ quota_perdite: lo 0.062 concordato, in una variabile sua"
            assert round(perdite_mwh, 2) == round(p, 2), "❌ perdite_mwh deve dare lo stesso risultato di p: somma dell'energia immessa per la quota"
        """,
    )
    return nb
