"""E1 · Esercitazione 1: un'ora di domande ed esercizi sul blocco 1 (notebook 00-03), sugli esercizi originali del docente."""

from textwrap import dedent

from nbkit import Notebook


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
        num="E1",
        file="Esercitazione_1",
        titolo="Esercitazione 1",
        blocco=1,
        giornata=1,
        intento="Un'ora di domande ed esercizi sui notebook 00-03: numeri, stringhe, liste e dizionari.",
        obiettivi=[
            "usare le funzioni di Python sui numeri e stampare i risultati con le f-string",
            "selezionare parti di una lista con lo slicing",
            "aggiungere coppie a un dizionario e leggerne i valori",
        ],
        tempo=60,
        dati=[],
        soluzioni_a_richiesta=True,
    )

    # ------------------------------------------------------------------ come funziona l'ora
    nb.md("""
        Questa esercitazione chiude la giornata e riprende quello che abbiamo visto nei notebook 00-03. Hai 45
        minuti per lavorare sugli esercizi, poi li guardiamo insieme. Si comincia con quattro domande di riepilogo e
        si prosegue con cinque esercizi brevi, ciascuno con i propri dati, da fare nell'ordine perché la difficoltà
        cresce; in fondo c'è una sfida libera, senza verifica, per il tempo che resta.
    """)
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
        Le quattro domande che seguono riguardano i notebook 00-03 e richiedono pochi minuti. Per ciascuna conviene
        prevedere la risposta a mente e solo dopo aprirla con un clic. In caso di dubbio si può provare la riga in
        una cella di codice e, se il risultato sorprende, rileggere la parte del notebook che tratta quell'argomento.
    """)
    nb.domanda(
        "Cosa restituisce `17 // 5`, e cosa restituisce `17 % 5`?",
        """
            `17 // 5` restituisce `3`, perché la divisione intera tiene soltanto la parte intera del quoziente 3.4,
            e `17 % 5` restituisce `2`, il resto della stessa divisione.
        """,
    )
    nb.domanda(
        'Con `numeri = [3, 6, 9, 12, 15]`, cosa restituisce `numeri[1:3]`?',
        """
            Restituisce `[6, 9]`. Lo slicing parte dall'indice 1 e si ferma prima dell'indice 3, quindi prende il
            secondo e il terzo elemento.
        """,
    )
    nb.domanda(
        'Con `punto = (45.46, 9.19)`, cosa succede se eseguiamo `punto[0] = 45.5`?',
        """
            Python solleva un `TypeError`, perché le tuple sono immutabili e non permettono di sostituire un
            elemento dopo la creazione. Per cambiare una coordinata si crea una tupla nuova.
        """,
    )
    nb.domanda(
        'Con `capitali = {"Italia": "Roma", "Francia": "Parigi"}`, cosa restituisce `capitali["Italia"]` e cosa fa `capitali["Spagna"] = "Madrid"`?',
        """
            `capitali["Italia"]` restituisce `"Roma"`, il valore associato a quella chiave. L'assegnazione a una
            chiave che non esiste aggiunge la coppia al dizionario, che dopo ha tre elementi.
        """,
    )

    # ------------------------------------------------------------------ 2. Esercizi
    nb.sezione("Esercizi", intro="""
        I cinque esercizi ripercorrono i numeri, le stringhe e le strutture dati dei notebook 01 e 02. Ognuno lavora
        sui dati scritti nella propria cella, quindi si può affrontare anche senza aver risolto i precedenti, e sono
        quelli che guardiamo insieme alla fine dell'ora.
    """)

    # E1.1 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Massimo, minimo e differenza",
        scenario="""
            Nella cella sono definite tre variabili numeriche. Vogliamo trovare il valore massimo, il valore minimo e
            la differenza tra i due, e stampare i tre risultati con una f-string ciascuno. Con i valori della cella
            il massimo è 25, il minimo 7 e la differenza 18.
        """,
        base=dict(
            richiesta="""
                1. Salva in `valore_massimo` il più grande dei tre numeri e in `valore_minimo` il più piccolo,
                   con le funzioni `max()` e `min()`, che abbiamo incontrato nella cella su PEP 8 del notebook 03.
                2. Salva in `differenza` la differenza tra massimo e minimo.
                3. Completa i tre `print`, in modo che stampino le righe indicate nei commenti.
            """,
            suggerimenti=[
                """
                    Le funzioni `max()` e `min()` accettano più argomenti separati da virgola e restituiscono il più
                    grande e il più piccolo.
                """,
                """
                    Servono `max(a, b, c)`, `min(a, b, c)` e `valore_massimo - valore_minimo`; nei `print` il nome
                    della variabile va tra graffe dentro la f-string.
                """,
            ],
            starter="""
                # Definizione delle variabili
                a = 10
                b = 25
                c = 7

                # Calcolo del massimo e del minimo
                valore_massimo = max(...)
                valore_minimo = ...
                differenza = ...

                # Stampa dei risultati
                print(f"Valore massimo: {valore_massimo}")   # Output: Valore massimo: 25
                print(f"Valore minimo: {...}")               # Output: Valore minimo: 7
                print(...)                                   # Output: Differenza: 18
            """,
            soluzione="""
                # Definizione delle variabili
                a = 10
                b = 25
                c = 7

                # Calcolo del massimo e del minimo
                valore_massimo = max(a, b, c)
                valore_minimo = min(a, b, c)
                differenza = valore_massimo - valore_minimo

                # Stampa dei risultati
                print(f"Valore massimo: {valore_massimo}")   # Output: Valore massimo: 25
                print(f"Valore minimo: {valore_minimo}")     # Output: Valore minimo: 7
                print(f"Differenza: {differenza}")           # Output: Differenza: 18
            """,
            verifica="""
                assert valore_massimo == 25 and valore_minimo == 7, "❌ valore_massimo e valore_minimo: usa max() e min() sui tre numeri"
                assert differenza == 18, "❌ differenza: massimo meno minimo"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `valore_massimo` e `valore_minimo` il più grande e il più piccolo dei tre numeri, con
                   `max()` e `min()`, e in
                   `differenza` la loro differenza.
                2. Salva in `media` la media dei tre numeri, arrotondata a un decimale con `round()`.
                3. Stampa i quattro risultati, uno per riga, con le f-string.

                La media vale 14.0.
            """,
            suggerimenti=[
                """
                    `max()` e `min()` accettano più argomenti separati da virgola; la media è la somma dei tre numeri
                    divisa per 3, e `round(valore, 1)` la arrotonda a un decimale.
                """,
            ],
            starter="""
                a = 10
                b = 25
                c = 7

                # da creare: valore_massimo, valore_minimo, differenza, media
            """,
            soluzione="""
                a = 10
                b = 25
                c = 7

                valore_massimo = max(a, b, c)
                valore_minimo = min(a, b, c)
                differenza = valore_massimo - valore_minimo
                media = round((a + b + c) / 3, 1)

                print(f"Valore massimo: {valore_massimo}")   # Output: Valore massimo: 25
                print(f"Valore minimo: {valore_minimo}")     # Output: Valore minimo: 7
                print(f"Differenza: {differenza}")           # Output: Differenza: 18
                print(f"Media: {media}")                     # Output: Media: 14.0
            """,
            verifica="""
                assert valore_massimo == 25 and valore_minimo == 7 and differenza == 18, "❌ Controlla max(), min() e la differenza"
                assert media == 14.0, "❌ media: (a + b + c) / 3, arrotondata con round(..., 1)"
            """,
        ),
    )

    # E1.2 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="L'area del cerchio",
        scenario="""
            Vogliamo calcolare l'area di un cerchio di raggio 5 e stampare il risultato. L'area è π moltiplicato per
            il raggio al quadrato, e il valore di π lo fornisce il modulo `math`, con `math.pi`. Il risultato è
            78.53981633974483.
        """,
        base=dict(
            richiesta="""
                1. Salva in `area` il prodotto tra `math.pi` e il raggio al quadrato.
                2. Completa il `print` con una f-string che stampi `L'area del cerchio è: 78.53981633974483`.
            """,
            suggerimenti=[
                """
                    Il quadrato si scrive con l'operatore `**`, come in `raggio ** 2`, oppure moltiplicando il
                    raggio per se stesso.
                """,
                """
                    La riga è `area = math.pi * raggio ** 2`, e nella f-string la variabile va tra graffe:
                    `f"L'area del cerchio è: {area}"`.
                """,
            ],
            starter="""
                import math

                raggio = 5
                area = ...

                print(...)  # Output: L'area del cerchio è: 78.53981633974483
            """,
            soluzione="""
                import math

                raggio = 5
                area = math.pi * raggio ** 2

                print(f"L'area del cerchio è: {area}")  # Output: L'area del cerchio è: 78.53981633974483
            """,
            verifica="""
                assert round(area, 6) == 78.539816, "❌ area: math.pi moltiplicato per raggio ** 2"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `area` il prodotto tra `math.pi` e il raggio al quadrato.
                2. Stampa l'area con una f-string che la mostri con due decimali, usando il formato `{area:.2f}`:
                   la riga stampata è `L'area del cerchio è: 78.54`.
                3. Salva in `circonferenza` il doppio di π per il raggio, cioè 31.41592653589793.
            """,
            suggerimenti=[
                """
                    Dentro le graffe di una f-string, dopo il nome della variabile, `:.2f` chiede due cifre
                    decimali; il valore di `area` non cambia, cambia soltanto come viene stampato.
                """,
            ],
            starter="""
                import math

                raggio = 5

                # da creare: area, circonferenza; stampa l'area con due decimali
            """,
            soluzione="""
                import math

                raggio = 5
                area = math.pi * raggio ** 2
                circonferenza = 2 * math.pi * raggio

                print(f"L'area del cerchio è: {area:.2f}")   # Output: L'area del cerchio è: 78.54
                print(circonferenza)                          # Output: 31.41592653589793
            """,
            verifica="""
                assert round(area, 6) == 78.539816, "❌ area: math.pi moltiplicato per raggio ** 2"
                assert round(circonferenza, 6) == 31.415927, "❌ circonferenza: 2 * math.pi * raggio"
            """,
        ),
    )

    # E1.3 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Lista invertita",
        scenario="""
            Vogliamo invertire l'ordine di una lista di numeri con lo slicing, senza riscrivere gli elementi a mano.
            La lista di partenza è `[1, 2, 3, 4, 5]` e il risultato è `[5, 4, 3, 2, 1]`.
        """,
        base=dict(
            richiesta="""
                1. Salva in `lista_invertita` la lista letta al contrario, con uno slicing a passo negativo.
                2. Stampa `lista_invertita`.
            """,
            suggerimenti=[
                """
                    Lo slicing ha tre parti, `[inizio:fine:passo]`, e il passo può essere negativo: in quel caso la
                    lista viene letta dall'ultimo elemento al primo.
                """,
                """
                    Con inizio e fine vuoti e passo `-1`, cioè `lista[::-1]`, si ottiene tutta la lista al contrario.
                """,
            ],
            starter="""
                lista = [1, 2, 3, 4, 5]

                # Scrivi il tuo codice qui
                lista_invertita = lista[...]
                print(lista_invertita)  # Output: [5, 4, 3, 2, 1]
            """,
            soluzione="""
                lista = [1, 2, 3, 4, 5]

                lista_invertita = lista[::-1]
                print(lista_invertita)  # Output: [5, 4, 3, 2, 1]
            """,
            verifica="""
                assert lista_invertita == [5, 4, 3, 2, 1], "❌ lista_invertita: slicing con passo -1, cioè lista[::-1]"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `lista_invertita` la lista letta al contrario, con uno slicing a passo negativo.
                2. Salva in `ultimi_due` gli ultimi due elementi della lista di partenza, con uno slicing che usa un
                   indice negativo, e in `ogni_due` gli elementi di posizione pari, cioè `[1, 3, 5]`.

                `ultimi_due` vale `[4, 5]`.
            """,
            suggerimenti=[
                """
                    Un indice negativo conta dalla fine, quindi `lista[-2:]` parte dal penultimo elemento; il passo
                    `2` prende un elemento ogni due.
                """,
            ],
            starter="""
                lista = [1, 2, 3, 4, 5]

                # da creare: lista_invertita, ultimi_due, ogni_due
            """,
            soluzione="""
                lista = [1, 2, 3, 4, 5]

                lista_invertita = lista[::-1]
                ultimi_due = lista[-2:]
                ogni_due = lista[::2]

                print(lista_invertita)  # Output: [5, 4, 3, 2, 1]
                print(ultimi_due, ogni_due)  # Output: [4, 5] [1, 3, 5]
            """,
            verifica="""
                assert lista_invertita == [5, 4, 3, 2, 1], "❌ lista_invertita: slicing con passo -1"
                assert ultimi_due == [4, 5] and ogni_due == [1, 3, 5], "❌ ultimi_due è lista[-2:] e ogni_due è lista[::2]"
            """,
        ),
    )

    # E1.4 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Posizioni pari",
        scenario="""
            La lista della cella alterna nomi di donne e di uomini, a partire da Elena. Vogliamo selezionare con un
            solo slicing gli elementi in posizione pari escludendo la posizione 0, cioè tutte le donne tranne Elena.
            Il risultato è `['Martina', 'Giulia', 'Francesca', 'Sara']`.
        """,
        base=dict(
            richiesta="""
                1. Salva in `elementi_pari` gli elementi dalla posizione 2 in avanti, uno ogni due.
                2. Stampa `elementi_pari`.
            """,
            suggerimenti=[
                """
                    Lo slicing `[inizio::passo]` parte dall'indice indicato e salta `passo` elementi alla volta fino
                    alla fine della lista.
                """,
                """
                    Serve `lista[2::2]`: inizio 2 per saltare Elena e Luigi, passo 2 per prendere un nome ogni due.
                """,
            ],
            starter="""
                lista = ["Elena", "Luigi", "Martina", "Marco", "Giulia", "Simone", "Francesca", "Alessandro", "Sara", "Lorenzo"]

                # Scrivi il tuo codice qui
                elementi_pari = lista[...]
                print(elementi_pari)  # Output: ['Martina', 'Giulia', 'Francesca', 'Sara']
            """,
            soluzione="""
                lista = ["Elena", "Luigi", "Martina", "Marco", "Giulia", "Simone", "Francesca", "Alessandro", "Sara", "Lorenzo"]

                elementi_pari = lista[2::2]
                print(elementi_pari)  # Output: ['Martina', 'Giulia', 'Francesca', 'Sara']
            """,
            verifica="""
                assert elementi_pari == ["Martina", "Giulia", "Francesca", "Sara"], "❌ elementi_pari: slicing dalla posizione 2 con passo 2, cioè lista[2::2]"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `elementi_pari` gli elementi in posizione pari escludendo la posizione 0.
                2. Salva in `uomini` gli elementi in posizione impari, cioè `['Luigi', 'Marco', 'Simone',
                   'Alessandro', 'Lorenzo']`, e in `quanti_uomini` quanti sono.
            """,
            suggerimenti=[
                """
                    Le posizioni impari si prendono partendo dall'indice 1 con passo 2, e `len()` conta gli
                    elementi di una lista.
                """,
            ],
            starter="""
                lista = ["Elena", "Luigi", "Martina", "Marco", "Giulia", "Simone", "Francesca", "Alessandro", "Sara", "Lorenzo"]

                # da creare: elementi_pari, uomini, quanti_uomini
            """,
            soluzione="""
                lista = ["Elena", "Luigi", "Martina", "Marco", "Giulia", "Simone", "Francesca", "Alessandro", "Sara", "Lorenzo"]

                elementi_pari = lista[2::2]
                uomini = lista[1::2]
                quanti_uomini = len(uomini)

                print(elementi_pari)  # Output: ['Martina', 'Giulia', 'Francesca', 'Sara']
                print(uomini, quanti_uomini)  # Output: ['Luigi', 'Marco', 'Simone', 'Alessandro', 'Lorenzo'] 5
            """,
            verifica="""
                assert elementi_pari == ["Martina", "Giulia", "Francesca", "Sara"], "❌ elementi_pari: lista[2::2]"
                assert uomini == ["Luigi", "Marco", "Simone", "Alessandro", "Lorenzo"] and quanti_uomini == 5, "❌ uomini è lista[1::2] e quanti_uomini è len(uomini)"
            """,
        ),
    )

    # E1.5 ---------------------------------------------------------------
    g8_cella = """
        g8 = {
            'Canada': 'Ottawa',
            'Francia': 'Parigi',
            'Germania': 'Berlino',
            'Italia': 'Roma',
            'Giappone': 'Tokyo',
            'Russia': 'Mosca'
        }
    """
    esercizio_due_aule(
        nb,
        titolo="Le capitali del G8",
        scenario="""
            Il dizionario `g8` associa ai paesi del G8 la loro capitale, ma è incompleto: mancano `'Regno Unito'`
            con `'Londra'` e `'Stati Uniti'` con `'Washington, D.C.'`. Vogliamo aggiungere le due coppie e, alla
            fine, avere un dizionario con otto paesi.
        """,
        base=dict(
            richiesta="""
                1. Aggiungi la coppia `'Regno Unito': 'Londra'`, assegnando il valore alla chiave nuova.
                2. Aggiungi nello stesso modo `'Stati Uniti': 'Washington, D.C.'`.
                3. Stampa il dizionario.
            """,
            suggerimenti=[
                """
                    Per aggiungere una coppia a un dizionario si assegna un valore a una chiave che ancora non
                    esiste, con la stessa sintassi con cui si legge un valore.
                """,
                """
                    Le due righe hanno la forma `g8['Regno Unito'] = 'Londra'`.
                """,
            ],
            starter=unisci(g8_cella, """
                # Aggiungi i paesi mancanti
                g8[...] = 'Londra'
                g8...

                print(g8)
            """),
            soluzione=unisci(g8_cella, """
                # Aggiungi i paesi mancanti
                g8['Regno Unito'] = 'Londra'
                g8['Stati Uniti'] = 'Washington, D.C.'

                print(g8)
            """),
            verifica="""
                assert g8.get('Regno Unito') == 'Londra' and g8.get('Stati Uniti') == 'Washington, D.C.', "❌ Aggiungi le due coppie con g8[chiave] = valore"
                assert len(g8) == 8, "❌ Alla fine il dizionario ha otto paesi"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Aggiungi le coppie `'Regno Unito': 'Londra'` e `'Stati Uniti': 'Washington, D.C.'`.
                2. Salva in `quanti` il numero di paesi e in `capitale_italia` la capitale dell'Italia, letta dal
                   dizionario con la sua chiave.
                3. Salva in `paesi` la lista dei paesi in ordine alfabetico, usando `sorted()` sulle chiavi.

                `quanti` vale 8 e `paesi` comincia con `'Canada'` e finisce con `'Stati Uniti'`.
            """,
            suggerimenti=[
                """
                    `len()` conta le coppie di un dizionario, `g8['Italia']` legge un valore dalla sua chiave e
                    `sorted(g8.keys())` restituisce le chiavi in ordine alfabetico come lista.
                """,
            ],
            starter=unisci(g8_cella, """
                # da creare: quanti, capitale_italia, paesi (prima completa il dizionario)
            """),
            soluzione=unisci(g8_cella, """
                g8['Regno Unito'] = 'Londra'
                g8['Stati Uniti'] = 'Washington, D.C.'

                quanti = len(g8)
                capitale_italia = g8['Italia']
                paesi = sorted(g8.keys())

                print(quanti, capitale_italia)  # Output: 8 Roma
                print(paesi)
            """),
            verifica="""
                assert g8.get('Regno Unito') == 'Londra' and g8.get('Stati Uniti') == 'Washington, D.C.', "❌ Aggiungi le due coppie con g8[chiave] = valore"
                assert quanti == 8 and capitale_italia == 'Roma', "❌ quanti è len(g8) e capitale_italia è g8['Italia']"
                assert paesi[0] == 'Canada' and paesi[-1] == 'Stati Uniti', "❌ paesi: sorted(g8.keys())"
            """,
        ),
    )

    # Sfida ---------------------------------------------------------------
    nb.esercizio(
        titolo="Sfida: una riga sul G8",
        facoltativo=True,
        scenario="""
            Partendo dal dizionario `g8` completo, vogliamo stampare una frase come `Il G8 ha 8 paesi e la capitale
            del Giappone è Tokyo`, in cui il numero di paesi e la capitale vengono letti dal dizionario e non scritti
            a mano, così la frase resta giusta se il dizionario cambia. La forma della frase è libera, quindi
            l'esercizio non ha una verifica e la cella `soluzione` mostra un esempio.
        """,
        richiesta="""
            1. Componi la frase con una f-string, mettendo tra graffe `len(g8)` e il valore letto con la chiave del
               paese che preferisci.
            2. Cambia il paese e riesegui la cella.
        """,
        suggerimenti=[
            """
                Dentro le graffe di una f-string può stare un'espressione qualunque, oltre al nome di una
                variabile: `{len(g8)}` e `{g8['Giappone']}` funzionano.
            """,
        ],
        starter=unisci(g8_cella, """
            g8['Regno Unito'] = 'Londra'
            g8['Stati Uniti'] = 'Washington, D.C.'

            print(f"...")
        """),
        soluzione=unisci(g8_cella, """
            g8['Regno Unito'] = 'Londra'
            g8['Stati Uniti'] = 'Washington, D.C.'

            print(f"Il G8 ha {len(g8)} paesi e la capitale del Giappone è {g8['Giappone']}")
        """),
        verifica=None,
    )
    return nb
