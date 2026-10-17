"""E2 · Esercitazione 2: un'ora di domande ed esercizi sul blocco 2 (notebook 04-06), sugli esercizi originali del docente."""

from textwrap import dedent

from nbkit import Cella, Notebook

FILE_CSV = "../Dati/letture_pod_2025.csv"


def unisci(*parti: str) -> str:
    """Toglie l'indentazione a ogni pezzo di codice e li unisce con una riga vuota."""
    return "\n\n".join(dedent(p).strip("\n") for p in parti)


def esercizio_due_aule(nb: Notebook, titolo: str, scenario: str, base: dict, avanzata: dict,
                       facoltativo: bool = False) -> None:
    """Lo stesso esercizio per le due aule: titolo e scenario in comune, il resto può cambiare.

    `base` e `avanzata` contengono richiesta, starter, soluzione, verifica e suggerimenti; le chiavi che mancano
    in `avanzata` si prendono da `base`.
    """
    nb.esercizio(titolo=titolo, scenario=scenario, facoltativo=facoltativo, aula="base", **base)
    nb.esercizio(titolo=titolo, scenario=scenario, facoltativo=facoltativo, aula="avanzata", **{**base, **avanzata})


def costruisci() -> Notebook:
    nb = Notebook(
        num="E2",
        file="Esercitazione_2",
        titolo="Esercitazione 2",
        blocco=2,
        giornata=1,
        intento="Un'ora di domande ed esercizi sui notebook 04-06: funzioni, cicli, condizioni e lettura dei dati con pandas.",
        obiettivi={
            "base": [
                "scrivere funzioni che usano lo slicing, un ciclo `for` e una condizione `if`",
                "leggere un CSV in formato italiano con i parametri giusti di `read_csv`",
                "leggere un foglio di un file Excel e una tabella di un database SQLite",
            ],
            "avanzata": [
                "scrivere funzioni con lo slicing, un ciclo `for`, una condizione `if` e una list comprehension",
                "leggere un CSV in formato italiano, un foglio di un file Excel e una tabella di un database",
                "raccogliere in una funzione la chiamata a un'API, con un file di riserva quando manca la rete",
            ],
        },
        tempo=60,
        dati={
            "base": ["letture_pod_2025.csv", "bolletta_esempio.xlsx", "utility.db"],
            "avanzata": ["letture_pod_2025.csv", "bolletta_esempio.xlsx", "utility.db", "fallback/lombardia_sensori.json"],
        },
        soluzioni_a_richiesta=True,
    )

    # ------------------------------------------------------------------ come funziona l'ora
    intro = """
        Questa esercitazione chiude la giornata e riprende quello che abbiamo visto nei notebook 04-06. Hai 45
        minuti per lavorare sugli esercizi, poi li guardiamo insieme. Si comincia con quattro domande di riepilogo e
        si prosegue con cinque esercizi, ciascuno con i propri dati, da fare nell'ordine perché la difficoltà
        cresce; in fondo {fondo}, per il tempo che resta.
    """
    nb.md(intro.replace("{fondo}", "c'è una sfida libera, senza verifica"), aula="base")
    nb.md(intro.replace("{fondo}", "ci sono un esercizio facoltativo sulle API e una sfida libera, senza verifica"),
          aula="avanzata")
    aiuti = """
        Ogni esercizio comincia dicendo che cosa vogliamo ottenere e perché, e da lì si può arrivare al risultato da
        soli. Chi preferisce procedere per gradi apre con un clic il blocco Passo per passo, e sotto {aiuti}, da
        leggere solo dopo aver provato. Sotto la cella da completare ci sono la verifica, che conferma il risultato o
        dice che cosa controllare, e la cella `soluzione`, che mostra soltanto la soluzione di quell'esercizio.
    """
    nb.md(aiuti.replace("{aiuti}", "due suggerimenti, anche loro nascosti"), aula="base")
    nb.md(aiuti.replace("{aiuti}", "un suggerimento, anche lui nascosto"), aula="avanzata")

    # ------------------------------------------------------------------ 1. Domande
    nb.sezione("Domande", intro="""
        Le quattro domande che seguono riguardano i notebook 04-06 e richiedono pochi minuti. Per ciascuna conviene
        prevedere la risposta a mente e solo dopo aprirla con un clic. In caso di dubbio si può provare la riga in
        una cella di codice e, se il risultato sorprende, rileggere la parte del notebook che tratta quell'argomento.
    """)
    nb.domanda(
        "Quali valori assume `i` nel ciclo `for i in range(3):`?",
        """
            Assume i valori `0`, `1` e `2`, in quest'ordine. La funzione `range(3)` produce i numeri interi da 0 a
            3 escluso, quindi il blocco del ciclo viene eseguito tre volte.
        """,
    )
    nb.domanda(
        """
            Che cosa contiene `risultato` dopo queste righe?

            ```python
            def saluta(nome):
                print(f"Ciao {nome}")

            risultato = saluta("Anna")
            ```
        """,
        """
            Contiene `None`. La funzione stampa `Ciao Anna`, ma non ha un `return`, e una funzione senza `return`
            restituisce `None`. Per avere il testo in `risultato` la funzione dovrebbe terminare con
            `return f"Ciao {nome}"`.
        """,
    )
    nb.domanda(
        "Quale errore dà la riga `int(\"12,5\")`, e come si ottiene il numero 12.5?",
        """
            Dà `ValueError: invalid literal for int() with base 10: '12,5'`. Il tipo dell'argomento è giusto, perché
            `int` accetta un testo, ma il valore non rappresenta un numero intero, e per di più contiene la virgola,
            che Python non riconosce come separatore decimale. Per ottenere 12.5 si scrive il punto al posto della
            virgola e si usa `float("12.5")`.
        """,
    )
    nb.domanda(
        "Che tipo di oggetto restituisce `pd.read_csv`, e come si conta il numero di righe del risultato?",
        """
            Restituisce un DataFrame, la tabella di pandas con le colonne del file. Il numero di righe si ottiene
            con `len()`, come per una lista, oppure dal riepilogo di `info()`.
        """,
    )

    # ------------------------------------------------------------------ 2. Esercizi
    nb.sezione("Esercizi", intro="""
        I primi tre esercizi riprendono le funzioni, i cicli e le condizioni del notebook 04, mentre gli ultimi due
        leggono con pandas i file del notebook 06. Ognuno lavora sui dati scritti nella propria cella o letti dal
        proprio file, quindi si può affrontare anche senza aver risolto i precedenti, e sono quelli che guardiamo
        insieme alla fine dell'ora.
    """)

    # E2.1 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Stringa invertita",
        scenario="""
            Vogliamo una funzione `inverti_stringa` che riceva una stringa e la restituisca letta al contrario,
            dall'ultimo carattere al primo. Una stringa si può pensare come una lista di caratteri, quindi lo stesso
            slicing che nell'Esercitazione 1 ha invertito una lista funziona anche qui. Con `'Python'` la funzione
            restituisce `'nohtyP'`.
        """,
        base=dict(
            richiesta="""
                1. Completa la funzione in modo che restituisca, con `return`, la stringa letta al contrario.
                2. Esegui la cella, che chiama la funzione su `'Python'` e stampa il risultato.
            """,
            suggerimenti=[
                """
                    Lo slicing con passo negativo legge una sequenza dall'ultimo elemento al primo, e sulle stringhe
                    funziona come sulle liste.
                """,
                """
                    La riga della funzione è `return stringa[::-1]`, con inizio e fine vuoti e passo `-1`.
                """,
            ],
            starter="""
                def inverti_stringa(stringa):
                    return ...

                print(inverti_stringa("Python"))  # Output: nohtyP
            """,
            soluzione="""
                def inverti_stringa(stringa):
                    return stringa[::-1]

                print(inverti_stringa("Python"))  # Output: nohtyP
            """,
            verifica="""
                assert inverti_stringa("Python") == "nohtyP", "❌ inverti_stringa('Python') deve restituire 'nohtyP': usa stringa[::-1]"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Scrivi la funzione `inverti_stringa(stringa)`, che restituisce la stringa letta al contrario.
                2. Aggiungi sotto il `def` una docstring di una riga, in modo che `help(inverti_stringa)` dica a chi
                   la riprende che cosa fa la funzione.
                3. Chiama la funzione anche su `'radar'` e salva in `uguale` il confronto tra il risultato e la
                   parola di partenza: vale `True`, perché `'radar'` è una delle parole palindrome che cerchiamo
                   nell'esercizio 3.
            """,
            suggerimenti=[
                """
                    La docstring è una stringa tra tripli apici scritta come prima riga del corpo della funzione, e
                    il confronto tra due stringhe si scrive con `==`.
                """,
            ],
            starter="""
                # da creare: inverti_stringa (con docstring), uguale
            """,
            soluzione="""
                def inverti_stringa(stringa):
                    \"\"\"Restituisce la stringa letta dall'ultimo carattere al primo.\"\"\"
                    return stringa[::-1]

                uguale = inverti_stringa("radar") == "radar"

                print(inverti_stringa("Python"))  # Output: nohtyP
                print(uguale)                     # Output: True
            """,
            verifica="""
                assert inverti_stringa("Python") == "nohtyP", "❌ inverti_stringa('Python') deve restituire 'nohtyP'"
                assert inverti_stringa.__doc__, "❌ Manca la docstring sotto il def"
                assert uguale is True, "❌ uguale: confronta inverti_stringa('radar') con 'radar' usando =="
            """,
        ),
    )

    # E2.2 ---------------------------------------------------------------
    g10_cella = """
        g10 = {
            'Canada': 'Ottawa',
            'Francia': 'Parigi',
            'Germania': 'Berlino',
            'Italia': 'Roma',
            'Giappone': 'Tokyo',
            'Regno Unito': 'Londra',
            'Stati Uniti': 'Washington',
            'Spagna': 'Madrid',
            'Paesi Bassi': 'Amsterdam',
            'Corea del Sud': 'Seoul'
        }
    """
    paesi_pari = "['Canada', 'Francia', 'Italia', 'Regno Unito', 'Stati Uniti', 'Spagna']"
    funzione_pari = """
        def paesi_capitale_pari(dizionario):
            risultato = []
            for paese, capitale in dizionario.items():
                if len(capitale) % 2 == 0:
                    risultato.append(paese)
            return risultato
    """
    esercizio_due_aule(
        nb,
        titolo="Paesi con capitale pari",
        scenario=f"""
            Il dizionario `g10` associa a dieci paesi la loro capitale. Vogliamo una funzione `paesi_capitale_pari`
            che riceva un dizionario di paesi e capitali e restituisca la lista dei paesi la cui capitale ha un
            numero pari di lettere, così la stessa regola vale per qualunque dizionario senza contare le lettere a
            mano. Con `g10` la funzione restituisce `{paesi_pari}`.
        """,
        base=dict(
            richiesta="""
                1. Dentro la funzione crea la lista vuota `risultato`, che raccoglierà i paesi trovati.
                2. Percorri il dizionario con un ciclo `for` su `.items()`, che a ogni passo fornisce il paese e la
                   sua capitale.
                3. Se il numero di lettere della capitale è pari, aggiungi il paese a `risultato`.
                4. Alla fine del ciclo restituisci `risultato`, poi esegui la cella, che chiama la funzione su `g10`.
            """,
            suggerimenti=[
                """
                    Il numero di lettere di una stringa si ottiene con `len()`, e un numero è pari quando il resto
                    della sua divisione per 2 è zero.
                """,
                """
                    La condizione è `if len(capitale) % 2 == 0:` e il paese si aggiunge con
                    `risultato.append(paese)`; il `return` va fuori dal ciclo, allineato al `for`.
                """,
            ],
            starter=unisci("""
                def paesi_capitale_pari(dizionario):
                    # inizializza una lista vuota chiamata risultato
                    ...

                    for paese, capitale ...  # loop su chiave, valore (usa .items())
                        if ...:  # condizione lunghezza pari del nome della capitale
                            risultato...  # aggiungi a risultato il paese visto che la condizione è rispettata
                    return risultato
            """, g10_cella, f"""
                print(paesi_capitale_pari(g10))  # Output: {paesi_pari}
            """),
            soluzione=unisci(funzione_pari, g10_cella, f"""
                print(paesi_capitale_pari(g10))  # Output: {paesi_pari}
            """),
            verifica=f"""
                assert paesi_capitale_pari(g10) == {paesi_pari}, "❌ Controlla la condizione: len(capitale) % 2 == 0"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Scrivi la funzione `paesi_capitale_pari(dizionario)`, che percorre il dizionario con un ciclo
                   `for` su `.items()` e raccoglie in una lista i paesi la cui capitale ha un numero pari di lettere.
                2. Salva in `paesi_pari` il risultato della funzione su `g10`.
                3. Salva in `quanti` il numero di paesi trovati, così il conteggio si legge senza scorrere la lista:
                   con `g10` vale 6.
            """,
            suggerimenti=[
                """
                    Un numero è pari quando `numero % 2 == 0`; la lista si costruisce con `append()` dentro l'`if`,
                    e `len()` conta i suoi elementi.
                """,
            ],
            starter=unisci(g10_cella, """
                # da creare: paesi_capitale_pari, paesi_pari, quanti
            """),
            soluzione=unisci(funzione_pari, g10_cella, f"""
                paesi_pari = paesi_capitale_pari(g10)
                quanti = len(paesi_pari)

                print(paesi_pari)  # Output: {paesi_pari}
                print(quanti)      # Output: 6
            """),
            verifica=f"""
                assert paesi_capitale_pari(g10) == {paesi_pari}, "❌ Controlla la condizione: len(capitale) % 2 == 0"
                assert paesi_pari == paesi_capitale_pari(g10) and quanti == 6, "❌ paesi_pari è il risultato su g10 e quanti è len(paesi_pari)"
            """,
        ),
    )

    # E2.3 ---------------------------------------------------------------
    test_palindrome = """
        lista_parole = ['ciao', 'anna', 'radar', 'gatto', 'osso', 'madam']
        print(trova_palindrome(lista_parole))  # Output: ['anna', 'radar', 'osso', 'madam']
    """
    esercizio_due_aule(
        nb,
        titolo="Parole palindrome",
        scenario="""
            Una parola palindroma si legge allo stesso modo nei due sensi, come `anna` o `radar`, cioè è uguale a sé
            stessa letta al contrario. Vogliamo una funzione `trova_palindrome` che riceva una lista di parole e
            restituisca una nuova lista con le sole palindrome, così possiamo controllare elenchi lunghi quanto
            vogliamo invece di esaminare le parole una per una. Con la lista `['ciao', 'anna', 'radar', 'gatto',
            'osso', 'madam']` il risultato è `['anna', 'radar', 'osso', 'madam']`.
        """,
        base=dict(
            richiesta="""
                1. Nel ciclo, completa la condizione dell'`if`, che è vera quando la parola è uguale a sé stessa
                   letta al contrario.
                2. Quando la condizione è vera, aggiungi la parola alla lista `palindrome`.
                3. Esegui la cella, che chiama la funzione sulla lista di prova.
            """,
            suggerimenti=[
                """
                    Per leggere una parola al contrario si usa lo stesso slicing dell'esercizio sulla stringa
                    invertita, e il confronto tra due stringhe si scrive con `==`.
                """,
                """
                    La condizione è `if parola == parola[::-1]:` e sotto, indentata, va la riga
                    `palindrome.append(parola)`.
                """,
            ],
            starter=unisci("""
                def trova_palindrome(lista_parole):
                    palindrome = []
                    for parola in lista_parole:
                        if ...:  # completa la condizione parola == parola invertita
                            ...
                    return palindrome
            """, test_palindrome),
            soluzione=unisci("""
                def trova_palindrome(lista_parole):
                    palindrome = []
                    for parola in lista_parole:
                        if parola == parola[::-1]:
                            palindrome.append(parola)
                    return palindrome
            """, test_palindrome),
            verifica="""
                assert trova_palindrome(['ciao', 'anna', 'radar', 'gatto', 'osso', 'madam']) == ['anna', 'radar', 'osso', 'madam'], "❌ Le palindrome della lista sono anna, radar, osso e madam"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Scrivi il corpo della funzione in una riga sola, con una list comprehension che ha un `if` in
                   fondo, perché la funzione tiene soltanto alcuni elementi della lista.
                2. Una parola con l'iniziale maiuscola, come `'Anna'`, letta al contrario diventa `'annA'` e il
                   confronto la scarta. Fai in modo che la condizione confronti le parole in minuscolo, con il
                   metodo `lower()`, ma che la lista restituita contenga le parole come sono scritte.
                3. Salva in `con_maiuscole` il risultato della funzione sulla lista `['Anna', 'Roma', 'Otto',
                   'pane']`, che è `['Anna', 'Otto']`.
            """,
            suggerimenti=[
                """
                    Il metodo `lower()` restituisce la stringa in minuscolo, per esempio `'Anna'.lower()` vale
                    `'anna'`, e si può applicare prima dello slicing: `parola.lower()[::-1]`.
                """,
            ],
            starter=unisci("""
                def trova_palindrome(lista_parole):
                    return [... for ... if ...]  # completa la condizione parola == parola invertita
            """, test_palindrome, """
                # da creare: con_maiuscole
            """),
            soluzione=unisci("""
                def trova_palindrome(lista_parole):
                    return [parola for parola in lista_parole if parola.lower() == parola.lower()[::-1]]
            """, test_palindrome, """
                con_maiuscole = trova_palindrome(['Anna', 'Roma', 'Otto', 'pane'])
                print(con_maiuscole)  # Output: ['Anna', 'Otto']
            """),
            verifica="""
                assert trova_palindrome(['ciao', 'anna', 'radar', 'gatto', 'osso', 'madam']) == ['anna', 'radar', 'osso', 'madam'], "❌ Le palindrome della lista sono anna, radar, osso e madam"
                assert con_maiuscole == ['Anna', 'Otto'], "❌ con_maiuscole: confronta parola.lower() con parola.lower()[::-1] e restituisci la parola originale"
            """,
        ),
    )

    nb.md("""
        Gli ultimi due esercizi lavorano sui dati di esempio di una piccola società di vendita di energia, gli
        stessi del notebook 06, che arrivano in tre forme diverse: un CSV, un file Excel e un database SQLite. Un
        POD è il codice che identifica un punto di prelievo dell'energia elettrica, cioè il contatore di un cliente.
    """)

    # E2.4 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Lettura di un CSV italiano",
        scenario="""
            Il file `letture_pod_2025.csv` contiene i consumi mensili del 2025 di sei POD, divisi per fascia oraria,
            ed è stato esportato da un Excel in italiano, come quello del notebook 06. Vogliamo leggerlo con pandas e
            ricavare il numero di righe e il consumo totale, i due numeri con cui si controlla che un file sia
            arrivato intero prima di usarlo. Il file ha 216 righe e il consumo totale è di 134507.7 kWh.
        """,
        base=dict(
            richiesta="""
                1. Leggi `../Dati/letture_pod_2025.csv` nel DataFrame `letture`, con i parametri adatti al formato
                   italiano.
                2. Controlla con `info()` che la colonna `kwh` sia di tipo `float64`, perché soltanto una colonna
                   numerica si può sommare.
                3. Salva in `righe` il numero di righe del DataFrame e in `totale_kwh` la somma della colonna `kwh`.
            """,
            suggerimenti=[
                """
                    Un CSV salvato da Excel in italiano differisce da quello standard per tre aspetti, cioè il
                    carattere che separa le colonne, quello che separa i decimali e l'encoding, e a ciascuno
                    corrisponde un parametro di `read_csv`. Il numero di righe di un DataFrame si ottiene come la
                    lunghezza di una lista.
                """,
                """
                    I tre parametri sono `sep=";"`, `decimal=","` ed `encoding="latin-1"`. Le righe si contano con
                    `len(letture)` e la somma di una colonna si calcola con `letture["kwh"].sum()`.
                """,
            ],
            starter=f"""
                import pandas as pd

                letture = pd.read_csv("{FILE_CSV}", sep=..., decimal=..., encoding=...)
                letture.info()

                righe = ...
                totale_kwh = ...

                print(righe, round(totale_kwh, 1))  # Output: 216 134507.7
            """,
            soluzione=f"""
                import pandas as pd

                letture = pd.read_csv("{FILE_CSV}", sep=";", decimal=",", encoding="latin-1")
                letture.info()

                righe = len(letture)
                totale_kwh = letture["kwh"].sum()

                print(righe, round(totale_kwh, 1))  # Output: 216 134507.7
            """,
            verifica="""
                assert letture["kwh"].dtype == "float64", "❌ kwh non è numerica: manca decimal=','"
                assert righe == 216, "❌ Il file ha 216 righe: contale con len(letture)"
                assert round(totale_kwh, 1) == 134507.7, "❌ totale_kwh: somma la colonna kwh"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Leggi `../Dati/letture_pod_2025.csv` nel DataFrame `letture`, con i parametri adatti al formato
                   italiano, e tieni soltanto le colonne `pod`, `fascia` e `kwh`, perché il nome del cliente e la
                   data non servono a questo controllo e senza di loro `info()` mostra solo quello che interessa.
                2. Controlla con `info()` che la colonna `kwh` sia di tipo `float64`.
                3. Salva in `righe` il numero di righe del DataFrame e in `totale_kwh` la somma della colonna `kwh`.

                Il DataFrame ha 216 righe e 3 colonne.
            """,
            suggerimenti=[
                """
                    Il parametro `usecols` di `read_csv` riceve la lista dei nomi delle colonne da leggere, come in
                    `usecols=["pod", "fascia", "kwh"]`.
                """,
            ],
            starter="""
                import pandas as pd

                # da creare: letture (solo pod, fascia e kwh), righe, totale_kwh
            """,
            soluzione=f"""
                import pandas as pd

                letture = pd.read_csv(
                    "{FILE_CSV}",
                    sep=";", decimal=",", encoding="latin-1",
                    usecols=["pod", "fascia", "kwh"],
                )
                letture.info()

                righe = len(letture)
                totale_kwh = letture["kwh"].sum()

                print(righe, round(totale_kwh, 1))  # Output: 216 134507.7
            """,
            verifica="""
                assert list(letture.columns) == ["pod", "fascia", "kwh"], "❌ Con usecols leggi solo pod, fascia e kwh"
                assert letture["kwh"].dtype == "float64" and righe == 216, "❌ kwh deve essere numerica e le righe 216"
                assert round(totale_kwh, 1) == 134507.7, "❌ totale_kwh: somma la colonna kwh"
            """,
        ),
    )

    # E2.5 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Excel e database",
        scenario="""
            Il listino prezzi sta nel foglio `Listino` del file `bolletta_esempio.xlsx`, che non è il primo dei suoi
            tre fogli, e le letture giornaliere di marzo 2025 di trenta POD stanno nella tabella `letture` del
            database `utility.db`. Vogliamo portare il listino e la tabella in due DataFrame e ricavarne il prezzo
            della fascia F1, il numero di letture e il consumo complessivo del mese. Il prezzo della fascia F1 è di
            0.21 euro al kWh, la tabella ha 930 righe, una per giorno e per POD, e il consumo di marzo è di 69880.1
            kWh.
        """,
        base=dict(
            richiesta="""
                1. Leggi il foglio `Listino` nel DataFrame `listino`, indicando a `read_excel` il nome del foglio,
                   perché senza questa indicazione la funzione legge soltanto il primo.
                2. Salva in `prezzo_f1` il prezzo della fascia F1, che si trova nella prima riga del listino, nella
                   colonna `eur_kwh`.
                3. Apri la connessione a `../Dati/utility.db` con `sqlite3.connect`, leggi tutta la tabella
                   `letture` nel DataFrame `letture_db` con `pd.read_sql` e chiudi la connessione, che non serve più.
                4. Salva in `n_letture` il numero di righe di `letture_db` e in `kwh_marzo` la somma della sua
                   colonna `kwh`.
            """,
            suggerimenti=[
                """
                    Il parametro `sheet_name` di `read_excel` sceglie il foglio da leggere, e il primo elemento di
                    una colonna si legge con le parentesi quadre, come in una Series. La query che legge una tabella
                    intera usa l'asterisco al posto dell'elenco delle colonne.
                """,
                """
                    Servono `sheet_name="Listino"` e `listino["eur_kwh"][0]`. La connessione si apre con
                    `sqlite3.connect("../Dati/utility.db")` e la query è `"SELECT * FROM letture"`.
                """,
            ],
            starter="""
                import sqlite3

                import pandas as pd

                listino = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name=...)
                prezzo_f1 = ...

                con = ...
                letture_db = pd.read_sql(..., con)
                con.close()

                n_letture = ...
                kwh_marzo = ...

                print(prezzo_f1)                        # Output: 0.21
                print(n_letture, round(kwh_marzo, 1))   # Output: 930 69880.1
            """,
            soluzione="""
                import sqlite3

                import pandas as pd

                listino = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Listino")
                prezzo_f1 = listino["eur_kwh"][0]

                con = sqlite3.connect("../Dati/utility.db")
                letture_db = pd.read_sql("SELECT * FROM letture", con)
                con.close()

                n_letture = len(letture_db)
                kwh_marzo = letture_db["kwh"].sum()

                print(prezzo_f1)                        # Output: 0.21
                print(n_letture, round(kwh_marzo, 1))   # Output: 930 69880.1
            """,
            verifica="""
                assert len(listino) == 3 and prezzo_f1 == 0.21, "❌ listino: leggi il foglio Listino; prezzo_f1 è il primo valore di eur_kwh"
                assert n_letture == 930 and list(letture_db.columns) == ["pod", "data", "kwh"], "❌ letture_db: leggi tutta la tabella letture con SELECT *"
                assert round(kwh_marzo, 1) == 69880.1, "❌ kwh_marzo: somma la colonna kwh di letture_db"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Leggi il foglio `Listino` nel DataFrame `listino` e salva in `prezzo_f1` il prezzo della fascia
                   F1, preso dalla colonna `eur_kwh`.
                2. Apri la connessione a `../Dati/utility.db` e leggi tutta la tabella `letture` nel DataFrame
                   `letture_db`; salva in `n_letture` il numero di righe e in `kwh_marzo` la somma della colonna
                   `kwh`.
                3. Il cliente del POD `IT001E10087109` ha chiesto le sue letture di marzo, quindi con una seconda
                   query, che usa la clausola `WHERE`, leggi nel DataFrame `letture_pod` soltanto le sue righe, e
                   poi chiudi la connessione.

                Il POD `IT001E10087109` ha 31 letture, una per ogni giorno di marzo.
            """,
            suggerimenti=[
                """
                    Nella query il codice del POD va tra apici singoli, come in `WHERE pod = 'IT001E10087109'`,
                    mentre la query intera sta tra apici doppi.
                """,
            ],
            starter="""
                import sqlite3

                import pandas as pd

                # da creare: listino, prezzo_f1, letture_db, n_letture, kwh_marzo, letture_pod
            """,
            soluzione="""
                import sqlite3

                import pandas as pd

                listino = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Listino")
                prezzo_f1 = listino["eur_kwh"][0]

                con = sqlite3.connect("../Dati/utility.db")
                letture_db = pd.read_sql("SELECT * FROM letture", con)
                letture_pod = pd.read_sql("SELECT * FROM letture WHERE pod = 'IT001E10087109'", con)
                con.close()

                n_letture = len(letture_db)
                kwh_marzo = letture_db["kwh"].sum()

                print(prezzo_f1)                                          # Output: 0.21
                print(n_letture, round(kwh_marzo, 1), len(letture_pod))   # Output: 930 69880.1 31
            """,
            verifica="""
                assert len(listino) == 3 and prezzo_f1 == 0.21, "❌ listino: leggi il foglio Listino; prezzo_f1 è il primo valore di eur_kwh"
                assert n_letture == 930 and round(kwh_marzo, 1) == 69880.1, "❌ letture_db: leggi tutta la tabella letture e somma la colonna kwh"
                assert len(letture_pod) == 31 and set(letture_pod["pod"]) == {"IT001E10087109"}, "❌ letture_pod: filtra con WHERE pod = '...'"
            """,
        ),
    )

    # E2.6 (solo Avanzata) ------------------------------------------------
    chiamata = """
        import pandas as pd
        import requests


        def sensori(provincia):
            \"\"\"Anagrafica dei sensori meteo di Regione Lombardia in una provincia, come DataFrame.\"\"\"
            url = "https://www.dati.lombardia.it/resource/nf78-nj6b.json"
            response = requests.get(url, params={"provincia": provincia}, timeout=30)
            response.raise_for_status()
            return pd.DataFrame(response.json())


        sensori_mi = sensori("MI")
        sensori_mi.head()
    """
    riserva = """
        import json

        import pandas as pd

        with open("../Dati/fallback/lombardia_sensori.json", encoding="utf-8") as f:
            tutti = pd.DataFrame(json.load(f))
        sensori_mi = tutti[tutti["provincia"] == "MI"]
        sensori_mi.head()
    """
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="Il wrapper dell'API",
            scenario="""
                Nel notebook 06 abbiamo chiesto al portale di Regione Lombardia l'anagrafica dei sensori meteo
                ripetendo ogni volta l'indirizzo, i parametri e il controllo della risposta. Vogliamo raccogliere
                questi passi in una funzione, detta wrapper, che riceve la sigla di una provincia e restituisce i
                suoi sensori in un DataFrame, così per passare da Milano a Bergamo basta cambiare l'argomento. Alla
                fine `sensori_mi` contiene soltanto i sensori della provincia di Milano; se il portale non risponde,
                la seconda cella li legge da un file di riserva.
            """,
            richiesta="""
                1. Scrivi la funzione `sensori(provincia)`, con una docstring, che chiama l'endpoint
                   `https://www.dati.lombardia.it/resource/nf78-nj6b.json` con il parametro di query `provincia`,
                   un `timeout` di 30 secondi e `raise_for_status()`, e restituisce la risposta come DataFrame.
                2. Salva in `sensori_mi` il risultato di `sensori("MI")`.
                3. Se il portale non risponde, completa ed esegui la seconda cella, che legge
                   `../Dati/fallback/lombardia_sensori.json` e deve tenere in `sensori_mi` le sole righe con
                   provincia `MI`.
            """,
            suggerimenti=["""
                La funzione ripete i passi del notebook 06, con il dizionario `params={"provincia": provincia}`.
                Nel file di riserva la provincia si seleziona con una condizione sulla colonna `provincia`.
            """],
            starter="""
                import pandas as pd
                import requests

                # da creare: sensori(provincia), sensori_mi
            """,
            soluzione=chiamata,
            verifica=None,
            rete=True,
            facoltativo=True,
        )
        # la cella di riserva, la verifica e la soluzione a richiesta: senza tag rete, così la verifica gira sempre
        rivela = nb.celle.pop()
        assert rivela.ruolo == "rivela"
        nb.celle.append(Cella("code", _dedent(riserva).replace(
            'sensori_mi = tutti[tutti["provincia"] == "MI"]', "sensori_mi = ..."), aula="avanzata",
            solo_studente=True, ruolo="starter"))
        nb.celle.append(Cella("code", _dedent(riserva), aula="avanzata", solo_soluzioni=True, ruolo="soluzione"))
        nb.celle.append(Cella("code", _dedent("""
            assert len(sensori_mi) > 0, "❌ sensori_mi è vuoto: hai chiamato sensori(\\"MI\\") o letto il file di riserva?"
            assert {"idsensore", "tipologia", "provincia"} <= set(sensori_mi.columns), "❌ Mancano le colonne dell'anagrafica"
            assert set(sensori_mi["provincia"]) == {"MI"}, "❌ sensori_mi deve contenere solo la provincia MI"
        """), aula="avanzata", ruolo="verifica"))
        rivela.src = _dedent(chiamata) + "\n\n\n# se il portale non risponde, nella seconda cella\n" + _dedent(riserva)
        nb.celle.append(rivela)

    # Sfida ---------------------------------------------------------------
    nb.esercizio(
        titolo="Sfida: una funzione per i CSV italiani",
        facoltativo=True,
        scenario="""
            Ogni volta che leggiamo un CSV salvato da Excel in italiano ripetiamo gli stessi tre parametri. Vogliamo
            una funzione `leggi_csv_italiano` che riceva il percorso del file e restituisca il DataFrame già letto
            con il separatore, i decimali e l'encoding giusti, in modo che la volta successiva basti il percorso.
            Chiamata su `letture_pod_2025.csv`, la funzione restituisce un DataFrame di 216 righe. La forma è
            libera, quindi l'esercizio non ha una verifica e la cella `soluzione` mostra un esempio.
        """,
        richiesta="""
            1. Scrivi la funzione con un parametro, il percorso, e fai restituire con `return` il risultato di
               `pd.read_csv` con i tre parametri del formato italiano.
            2. Chiamala su `../Dati/letture_pod_2025.csv` e controlla il risultato con `info()`.
        """,
        suggerimenti=[
            """
                Il percorso è il primo argomento di `pd.read_csv`, quindi dentro la funzione si scrive il nome del
                parametro al posto della stringa con il nome del file.
            """,
        ],
        starter="""
            import pandas as pd

            def leggi_csv_italiano(percorso):
                ...
        """,
        soluzione=f"""
            import pandas as pd

            def leggi_csv_italiano(percorso):
                \"\"\"Legge un CSV salvato da Excel in italiano e lo restituisce come DataFrame.\"\"\"
                return pd.read_csv(percorso, sep=";", decimal=",", encoding="latin-1")

            letture = leggi_csv_italiano("{FILE_CSV}")
            letture.info()
        """,
        verifica=None,
    )
    return nb


def _dedent(testo: str) -> str:
    return dedent(testo).strip("\n")
