"""04 · Codice leggibile."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="04",
        file="04_Codice_leggibile",
        titolo="Codice leggibile",
        blocco=1,
        giornata=1,
        intento="Il codice si scrive una volta e si legge venti: dal collega domani, da noi tra tre mesi. Le poche abitudini che fanno la differenza tra un notebook e un rebus.",
        obiettivi={
            "base": [
                "commentare quando serve e scrivere una docstring",
                "usare le celle Markdown per raccontare un'analisi",
                "applicare le cinque regole di stile che contano",
            ],
            "avanzata": [
                "commentare quando serve e scrivere una docstring",
                "usare le celle Markdown per raccontare un'analisi",
                "applicare le cinque regole di stile che contano e lasciare il resto a Ruff",
            ],
        },
        tempo={"base": 20, "avanzata": 30},
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
        Stesso codice, e adesso si sa che il 10 non è un parametro ma un rimedio, e che un giorno la
        riga andrà tolta. Forma: sulla riga sopra, in italiano con gli accenti, minuscola iniziale,
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
        def energia_mwh(potenza_mw, ore):
            \"\"\"Energia in MWh di un intervallo a potenza costante.\"\"\"
            return potenza_mw * ore


        energia_mwh(12.4, 0.25)   # Output: 3.1
    """)
    nb.md("""
        La stringa tra tre virgolette è la docstring: una riga che dice cosa fa la funzione e, se
        non è ovvio, cosa riceve e cosa restituisce. Non è un commento qualsiasi: Python la
        conserva, `help()` la mostra e VS Code la fa comparire quando passiamo il mouse sul nome
        della funzione.
    """)
    nb.code("help(energia_mwh)")
    nb.md("""
        `help` stampa la firma, con i nomi dei parametri, e sotto la docstring. Funziona su
        qualunque funzione, nostra o di una libreria: `help(round)`, `help(pd.read_csv)`. La
        docstring vive nell'attributo `__doc__` della funzione, ed è lì che `help` va a leggerla.
    """)
    nb.code("energia_mwh.__doc__   # Output: 'Energia in MWh di un intervallo a potenza costante.'")
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
        andare a capo. Sono decine di pagine e ne contano cinque. Prima la versione che si vede
        troppo spesso.
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
        che il team ne scelga uno e lo scriva in `pyproject.toml`; nel progetto del corso c'è
        `line-length = 100`.
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
    nb.box("nota", """
        Esistono strumenti che applicano queste regole al posto nostro: si chiamano formattatori, e
        Ruff è quello che oggi si usa di più. Quando lavorerai su script veri, cercalo: in VS Code è
        un'estensione, si installa in un minuto.
    """, aula="base")
    nb.md("""
        Queste regole non si applicano a mano, a meno di volerci passare le serate: le applica Ruff,
        qui sotto.
    """, aula="avanzata")

    # ------------------------------------------------------------------ 5 (solo Avanzata)
    with nb.solo("avanzata"):
        nb.sezione("Ruff in VS Code", intro="""
            Ruff è il linter e formattatore di Python: segnala quello che non va (`check`) e rimette
            in forma il codice da solo (`format`). È già tra le dipendenze di sviluppo del progetto e
            si lancia dal terminale con `uvx ruff`.
        """)
        nb.md("""
            In VS Code si installa l'estensione **Ruff** dal pannello delle estensioni. Poi si attiva
            la formattazione al salvataggio: ogni **Ctrl+S** su un file `.py` rimette a posto spazi,
            virgole e righe vuote. In `settings.json` sono queste righe:

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
            I tre avvisi che vedremo più spesso. La lettera del codice è la famiglia (`F` errori veri,
            `E` stile), il numero la regola.

            | Codice | Avviso | Cosa vuol dire |
            |---|---|---|
            | `F401` | `` `math` imported but unused `` | una libreria importata e mai usata: via la riga |
            | `F841` | `` Local variable `totale` is assigned to but never used `` | una variabile calcolata e mai letta: un avanzo o un refuso |
            | `E501` | `Line too long (129 > 100)` | la riga supera il limite scritto in `pyproject.toml`: si spezza |
        """)
        nb.md("""
            Dal terminale, nella cartella del progetto, su un file `.py`:

            ```bash
            uvx ruff check report_pod.py                            # elenca gli avvisi
            uvx ruff check --output-format concise report_pod.py    # una riga per avviso
            uvx ruff format report_pod.py                           # riscrive il file nella forma giusta
            uvx ruff check --fix report_pod.py                      # corregge quello che sa correggere
            ```

            Il primo comando, in forma concisa, su un file con i tre problemi della tabella:

            ```text
            report_pod.py:1:8: F401 [*] `math` imported but unused
            report_pod.py:9:5: F841 Local variable `totale` is assigned to but never used
            report_pod.py:10:101: E501 Line too long (129 > 100)
            Found 3 errors.
            [*] 1 fixable with the `--fix` option.
            ```
        """)
        nb.md("""
            Ogni riga dice file, riga, colonna, codice e messaggio. `format` tocca solo la forma e
            non cambia mai cosa fa il codice; `check --fix` toglie gli import inutilizzati e poco
            altro. Righe lunghe e variabili inutili restano a noi: decidere cosa farne è un giudizio,
            non una regola. Per una stringa lunga, la ricetta è questa.
        """)
        nb.code("""
            soglia_kwh = 1000

            messaggio = (
                f"Trovati 3 POD sopra la soglia di {soglia_kwh} kWh: "
                "controllare le letture di luglio prima di fatturare"
            )
            messaggio
        """)
        nb.md("""
            Due pezzi tra parentesi, uno per riga, e Python li attacca in una stringa sola. La `f`
            serve solo sui pezzi che hanno le graffe.
        """)
        nb.box("nota", """
            Ruff legge anche i notebook: `uvx ruff check nome.ipynb` controlla le celle una per una,
            con la stessa configurazione del progetto.
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
            parametri che dicono cosa sono (`consumo_kwh` e `prezzo_kwh`), una docstring di una riga
            che spieghi anche cos'è il fattore `1.1` (è l'IVA al 10%) e lo stesso risultato. Dentro
            la funzione, dai un nome anche a quel numero.
        """,
        suggerimento="La docstring è la prima riga sotto il `def`, tra tre virgolette.",
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
                iva = 1.1
                return consumo_kwh * prezzo_kwh * iva


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
                `s = f(1250, 0.21) + f(830, 0.19) + f(1040, 0.17)`. Riscrivila con `costo_bolletta`,
                un nome che dica cosa contiene (`totale_bolletta`) e un commento di una riga che
                spieghi perché tre chiamate.
            """,
            starter="""
                # ...
                totale_bolletta = ...
                totale_bolletta
            """,
            soluzione="""
                # una chiamata per fascia: F1, F2 e F3 hanno consumi e prezzi diversi
                totale_bolletta = costo_bolletta(1250, 0.21) + costo_bolletta(830, 0.19) + costo_bolletta(1040, 0.17)
                totale_bolletta
            """,
            verifica="""
                assert round(totale_bolletta, 2) == 656.7, "❌ totale_bolletta: la somma delle tre bollette per fascia"
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
        suggerimento="Dare un nome al passaggio intermedio (`energia_mwh`) rende inutile il commento.",
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
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="Pulizia con Ruff",
            scenario="""
                Un collega ha lasciato lo script `report_pod.py` qui sotto e vuole metterlo nel
                repository del team, dove Ruff gira a ogni salvataggio e non lascia passare niente.
                Prima di lanciarlo facciamo noi il lavoro di Ruff: leggiamo il file e scriviamo quali
                avvisi darebbe.

                ```python
                import math

                soglia_kwh = 1000
                pod_anomali = ["IT001E45678901"]


                def riepilogo(pod_anomali, soglia_kwh):
                    n = len(pod_anomali)
                    totale = 0
                    return f"Trovati {n} POD sopra la soglia di {soglia_kwh} kWh nel file letture_pod_2025.csv: controllare le letture di luglio"


                print(riepilogo(pod_anomali, soglia_kwh))
                ```
            """,
            richiesta="""
                Tre passi, il terzo facoltativo.

                1. Metti in `avvisi` la lista dei codici Ruff che questo file farebbe scattare, come stringhe, uno per problema.
                2. Riscrivi il codice corretto nella cella: niente avvisi, stesso testo in uscita, una docstring per `riepilogo`.
                3. Salva l'originale in un file `report_pod.py` e lancia `uvx ruff check report_pod.py` nel terminale per confrontare.
            """,
            suggerimento="I codici sono nella tabella della sezione su Ruff; la stringa lunga si spezza tra parentesi.",
            starter="""
                avvisi = [...]

                # qui sotto il codice corretto
                soglia_kwh = 1000
                pod_anomali = ["IT001E45678901"]


                def riepilogo(pod_anomali, soglia_kwh):
                    ...


                print(riepilogo(pod_anomali, soglia_kwh))
            """,
            soluzione="""
                avvisi = ["F401", "F841", "E501"]  # import mai usato, variabile mai usata, riga da 129 caratteri

                soglia_kwh = 1000
                pod_anomali = ["IT001E45678901"]


                def riepilogo(pod_anomali, soglia_kwh):
                    \"\"\"Una riga di testo con quanti POD superano la soglia.\"\"\"
                    n = len(pod_anomali)
                    return (
                        f"Trovati {n} POD sopra la soglia di {soglia_kwh} kWh nel file letture_pod_2025.csv: "
                        "controllare le letture di luglio"
                    )


                print(riepilogo(pod_anomali, soglia_kwh))
            """,
            verifica="""
                assert sorted(avvisi) == ["E501", "F401", "F841"], "❌ avvisi: tre codici come stringhe: import inutilizzato, variabile mai usata, riga troppo lunga"
                assert riepilogo(["IT001E45678901"], 1000) == "Trovati 1 POD sopra la soglia di 1000 kWh nel file letture_pod_2025.csv: controllare le letture di luglio", "❌ riepilogo: il testo in uscita deve restare identico"
                assert riepilogo.__doc__, "❌ riepilogo: manca la docstring"
            """,
            perche="`import math` e `totale` si tolgono e basta. La riga lunga si spezza in due pezzi tra parentesi: il testo in uscita non cambia, e Ruff tace.",
        )
    return nb
