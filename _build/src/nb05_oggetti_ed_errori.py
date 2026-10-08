"""05 · Oggetti ed errori."""

import textwrap

from nbkit import Cella, Notebook


def _d(testo: str) -> str:
    return textwrap.dedent(testo).strip("\n")


def _altra_cella_rotta(nb: Notebook, starter: str, soluzione: str) -> None:
    """Aggiunge all'esercizio in corso un'altra coppia cella rotta (studente) / cella sistemata (soluzioni)."""
    nb.celle.append(Cella("code", _d(starter), solo_studente=True, ruolo="starter"))
    nb.celle.append(Cella("code", _d(soluzione), solo_soluzioni=True, ruolo="soluzione"))


def _verifica_finale(nb: Notebook, src: str) -> None:
    """Cella di verifica dell'esercizio in corso, dopo tutte le celle rotte."""
    nb.celle.append(Cella("code", _d(src), ruolo="verifica"))


def costruisci() -> Notebook:
    nb = Notebook(
        num="05",
        file="05_Oggetti_ed_errori",
        titolo="Oggetti ed errori",
        blocco=2,
        giornata=1,
        intento=(
            "Il notebook insegna a leggere una riga di codice scritta da altri, riconoscendo librerie, classi, "
            "oggetti, metodi e attributi, e a leggere un messaggio di errore per capire che cosa è andato storto e dove."
        ),
        obiettivi=[
            "riconoscere in una riga di codice libreria, funzione, classe, oggetto, metodo e attributo",
            "leggere la documentazione e i type hint di una funzione",
            "leggere un traceback dal basso e riconoscere gli errori più comuni",
        ],
        tempo={"base": 40, "avanzata": 35},
        dati=["TexasTurbine.csv"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Tutto è un oggetto", intro="""
        In Python ogni valore è un oggetto, cioè porta con sé dei dati e le operazioni che si possono
        fare su di essi. Una lista, un numero intero e un numero decimale sono oggetti di tipo diverso,
        e la funzione `type` dice di quale tipo è un oggetto. Nella cella seguente la applichiamo a tre
        variabili.
    """)
    nb.code("""
        citta = ["Roma", "Milano", "Torino"]
        voto = 28
        prezzo = 2.5

        print(type(citta))
        print(type(voto))
        print(type(prezzo))
    """)
    nb.md("""
        Le operazioni di un oggetto si chiamano metodi e si scrivono con il punto e le parentesi, nella
        forma `dato.metodo()`. Quali metodi esistono e che cosa fanno dipende dall'oggetto che sta a
        sinistra del punto: una stringa ha `upper()`, che la trasforma in maiuscolo, mentre una lista ha
        `index()`, che restituisce la posizione di un elemento.
    """)
    nb.code("""
        print("Roma".upper())          # Output: ROMA
        print(citta.index("Milano"))   # Output: 1
    """)
    nb.md("""
        Anche un DataFrame di pandas è un oggetto come gli altri, con molti più dati e metodi. Per
        vederlo costruiamo un piccolo DataFrame con tre persone, ciascuna con nome, età e città, e
        chiediamo a `type` di che oggetto si tratta.
    """)
    nb.code("""
        import pandas as pd

        data = {
            "Nome": ["Alice", "Bob", "Charlie"],
            "Età": [24, 27, 22],
            "Città": ["Roma", "Milano", "Torino"],
        }
        df = pd.DataFrame(data, index=["id_1", "id_2", "id_3"])
        type(df)
    """)
    nb.md("""
        Oltre ai metodi, un oggetto ha degli attributi, cioè dati che conserva al suo interno e che si
        leggono senza parentesi. Per esempio, `df.shape` dice quante righe e quante colonne ha il
        DataFrame, mentre `df.columns` contiene i nomi delle colonne.
    """)
    nb.code("""
        print(df.shape)
        print(df.columns)
    """)
    nb.md("""
        Un metodo è invece un'azione che l'oggetto compie, e per eseguirlo servono le parentesi, anche
        quando sono vuote. Tra le parentesi si passano gli eventuali argomenti: `df.head(2)`, per
        esempio, mostra le prime due righe del DataFrame.
    """)
    nb.code("df.head(2)")
    nb.md("""
        Se dimentichiamo le parentesi, Python non segnala un errore ma restituisce il metodo stesso
        invece del suo risultato. La scritta `bound method` che compare nell'output della cella qui
        sotto è il modo in cui Python mostra un metodo che non è stato eseguito, ed è quindi il segno
        che mancano le parentesi.
    """)
    nb.code("df.head")
    nb.md("""
        Alcune operazioni non sono metodi ma funzioni di Python, come `len` e `print`, e in questo caso
        l'oggetto si passa tra le parentesi invece di stare davanti al punto. La funzione `len`, per
        esempio, restituisce il numero di elementi di una lista e il numero di righe di un DataFrame.
        Per vedere l'elenco dei metodi di un oggetto basta scrivere il suo nome seguito dal punto e
        premere Tab.
    """)
    nb.code("len(citta), len(df)   # Output: (3, 3)")

    # ------------------------------------------------------------------ 2
    nb.sezione("Chi è chi in una riga di codice", intro="""
        Con questi elementi possiamo leggere una riga di codice intera e dire che cosa rappresenta
        ciascuna delle sue parti. Come esempio prendiamo la riga che legge un file CSV con pandas:

        ```python
        turbina = pd.read_csv("../Dati/TexasTurbine.csv", nrows=24)
        ```
    """)
    nb.md("""
        `pd` è la libreria pandas, importata con un nome corto, e `read_csv` è una sua funzione. Tra
        le parentesi ci sono gli argomenti: il percorso del file è passato per posizione, mentre
        `nrows=24` è passato per nome e chiede di leggere soltanto le prime 24 righe. Il valore
        restituito dalla funzione viene assegnato alla variabile `turbina`, di cui la cella seguente
        mostra il tipo.
    """)
    nb.code("""
        turbina = pd.read_csv("../Dati/TexasTurbine.csv", nrows=24)
        type(turbina)
    """)
    nb.md("""
        Il risultato, `pandas.DataFrame`, si legge come la classe `DataFrame` della libreria `pandas`.
        Una classe definisce com'è fatto un certo tipo di oggetto, cioè quali dati contiene e quali
        metodi offre, e `turbina` è un oggetto di quella classe. Anche `str` e `list` sono classi, e la
        variabile `citta` è un oggetto della classe `list`. Un import si legge allo stesso modo:
        `import plotly.express as px` prende il sottomodulo `express` della libreria `plotly` e gli dà
        il nome `px`.
    """)
    nb.md("""
        Le forme che si incontrano sono poche e si riconoscono dalla punteggiatura, come riassume la
        tabella seguente.

        | Forma | Cos'è | Esempio |
        |---|---|---|
        | `libreria.funzione(...)` | funzione di una libreria | `pd.read_csv(...)` |
        | `Nome(...)`, con la maiuscola | classe: costruisce un oggetto | `pd.DataFrame(data)` |
        | `oggetto.metodo(...)` | metodo: un'azione dell'oggetto | `df.head(2)` |
        | `oggetto.attributo`, senza parentesi | attributo: un dato dell'oggetto | `df.shape` |
        | `funzione(...)`, senza punto davanti | funzione di Python | `len(df)` |
        | `oggetto[...]` | selezione con le quadre | `df["Età"]` |
    """)
    nb.prova_tu(
        richiesta="""
            Nella cella qui sotto ci sono cinque espressioni, una per riga. Per ciascuna scrivi nel
            commento, dopo la freccia, che cosa rappresenta, usando i nomi della seconda colonna della
            tabella.
        """,
        starter="""
            # turbina.head(3)        -> ...
            # turbina.shape          -> ...
            # pd.Series([1, 2, 3])   -> ...
            # round(27.6)            -> ...
            # len(turbina)           -> ...
        """,
        soluzione="""
            # turbina.head(3)        -> metodo
            # turbina.shape          -> attributo
            # pd.Series([1, 2, 3])   -> classe
            # round(27.6)            -> funzione di Python
            # len(turbina)           -> funzione di Python
        """,
    )
    with nb.solo("avanzata"):
        nb.box("approfondimento", """
            Una classe si definisce con la parola chiave `class`, seguita dal nome e dai metodi
            indentati. Il metodo speciale `__init__` viene eseguito quando chiamiamo `Prodotto(...)` e
            salva i dati dentro il nuovo oggetto, mentre il parametro `self` indica l'oggetto stesso,
            cioè quello che nelle chiamate starà a sinistra del punto. Nel corso non scriveremo classi
            nostre, ma saperle leggere è utile, perché compaiono spesso nelle librerie e nel codice
            scritto da un agente.
        """, titolo="Una classe minima")
        nb.code("""
            class Prodotto:
                def __init__(self, nome, prezzo):
                    self.nome = nome
                    self.prezzo = prezzo

                def scontato(self, sconto):
                    return self.prezzo * (1 - sconto)


            pane = Prodotto("pane", 2.5)
            pane.nome, pane.scontato(0.2)   # Output: ('pane', 2.0)
        """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Leggere la documentazione e i type hint", intro="""
        Per usare una funzione bisogna sapere quali parametri accetta, quali sono obbligatori e che cosa
        restituisce. Queste informazioni si leggono con `help(funzione)` oppure, in un notebook,
        scrivendo il nome della funzione seguito da `?`. Come esempio guardiamo la documentazione di
        `round`.
    """)
    nb.code("help(round)")
    nb.md("""
        La prima riga dell'output è la firma della funzione. Il parametro `number` non è seguito da `=`,
        quindi è obbligatorio, mentre `ndigits=None` ha un valore predefinito e si può omettere. `None` è
        il valore con cui Python rappresenta l'assenza di un valore, e qui significa che il numero viene
        arrotondato all'intero, senza decimali.
    """)
    nb.code("round(27.567), round(27.567, ndigits=1)   # Output: (28, 27.6)")
    nb.md("""
        Nelle firme si trovano spesso anche i type hint, che indicano il tipo dei parametri e del
        risultato. Il tipo atteso di un parametro si scrive dopo i due punti che seguono il suo nome,
        mentre il tipo restituito si scrive dopo la freccia `->`. Python non li controlla durante
        l'esecuzione, perché servono a chi legge il codice e agli strumenti dell'editor.
    """)
    nb.code('''
        def media(voti: list[float]) -> float:
            """Media aritmetica di una lista di voti."""
            return sum(voti) / len(voti)


        media([28, 30, 25])
    ''')
    nb.code("help(media)")
    nb.md("""
        L'output di `help` mostra insieme la firma, i type hint e la docstring. Nelle librerie i tipi
        possono essere più articolati, come `encoding: str | None = None` nella firma di `read_csv`.
        La barra verticale significa "oppure", quindi il parametro accetta una stringa oppure `None`,
        che è anche il suo valore predefinito.
    """)
    nb.box("nota", """
        Nelle firme delle funzioni di Python compaiono a volte anche i simboli `/` e `*` isolati, che
        non sono parametri. I parametri che stanno prima di `/` si possono passare solo per posizione,
        mentre quelli che stanno dopo `*` si possono passare solo per nome.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Gli errori più comuni", intro="""
        Quando qualcosa va storto, Python interrompe l'esecuzione della cella e stampa un traceback,
        cioè il resoconto delle istruzioni che hanno portato all'errore. Il traceback si legge dal
        basso: l'ultima riga riporta il tipo di errore e la sua causa, mentre la riga indicata dalla
        freccia `---->` mostra dove si è verificato. Le celle di questa sezione producono un errore di
        proposito, e per ciascuna vediamo come si legge il messaggio e come si corregge il codice.
    """)
    nb.sottosezione("SyntaxError", intro="""
        Un `SyntaxError` indica che il codice non rispetta la grammatica di Python, e per questo la
        cella non viene eseguita affatto. Nell'esempio mancano i due punti dopo la condizione dell'`if`,
        e il simbolo `^` sotto la riga indica il punto in cui Python si è fermato.
    """)
    nb.code("""
        voto = 28
        if voto >= 18
            print("Promosso")
    """, errore=True)
    nb.sottosezione("NameError", intro="""
        Un `NameError` compare quando usiamo un nome che Python non conosce, perché è scritto in modo
        diverso da come è stato definito oppure perché la cella che lo definisce non è ancora stata
        eseguita. L'ultima riga del traceback riporta il nome cercato, in questo caso `cita` con una
        `t` sola.
    """)
    nb.code("""
        citta = ["Roma", "Milano", "Torino"]
        print(cita)
    """, errore=True)
    nb.sottosezione("TypeError", intro="""
        Un `TypeError` segnala un'operazione tra valori di tipo incompatibile. Nell'esempio proviamo a
        unire con `+` un testo e un numero, che Python non sa sommare; per correggere la riga si
        converte prima il numero in testo, scrivendo `str(eta)` al posto di `eta`.
    """)
    nb.code("""
        eta = 24
        "Alice ha " + eta + " anni"
    """, errore=True)
    nb.sottosezione("KeyError", intro="""
        Un `KeyError` indica che la chiave richiesta non esiste nel dizionario. L'ultima riga del
        traceback riporta la chiave tale e quale, e si vede che è scritta in minuscolo, mentre nel
        dizionario compare con l'iniziale maiuscola. Lo stesso errore si ottiene chiedendo a un
        DataFrame una colonna che non ha.
    """)
    nb.code("""
        prezzi = {"Pane": 2.5, "Latte": 1.2, "Caffè": 3.8}
        prezzi["pane"]
    """, errore=True)
    nb.sottosezione("IndexError", intro="""
        Un `IndexError` compare quando chiediamo una posizione che la lista non ha. Una lista di tre
        elementi occupa le posizioni 0, 1 e 2, quindi `citta[3]` va oltre la fine; per prendere l'ultimo
        elemento, qualunque sia la lunghezza della lista, si scrive `citta[-1]`.
    """)
    nb.code("""
        citta = ["Roma", "Milano", "Torino"]
        citta[3]
    """, errore=True)
    nb.sottosezione("ValueError", intro="""
        Un `ValueError` indica che l'argomento ha il tipo giusto ma un valore che la funzione non sa
        trattare. La funzione `float` accetta un testo, ma si aspetta il punto come separatore decimale
        e non riconosce la virgola, quindi `float("2,50")` dà errore, mentre `float("2.50")` restituisce
        2.5.
    """)
    nb.code('float("2,50")', errore=True)
    nb.sottosezione("FileNotFoundError", intro="""
        Un `FileNotFoundError` significa che nel percorso indicato non c'è nessun file. L'ultima riga
        riporta il percorso che pandas ha provato ad aprire, e conviene confrontarlo con il nome vero del
        file nella cartella, che qui è `TexasTurbine.csv`. Le righe intermedie del traceback riguardano
        il codice interno di pandas e in questo caso si possono saltare.
    """)
    nb.code('pd.read_csv("../Dati/texas_turbine.csv")', errore=True)
    nb.sottosezione("AttributeError", intro="""
        Un `AttributeError` indica che l'oggetto non ha il metodo o l'attributo richiesto. Un DataFrame,
        per esempio, non ha un metodo `sort`, perché quello che ordina le righe si chiama `sort_values`.
        L'errore capita spesso con nomi plausibili ma inesistenti, come quelli che a volte suggerisce un
        agente.
    """)
    nb.code('df.sort("Età")', errore=True)

    # ------------------------------------------------------------------ 5
    nb.sezione("Cosa fare davanti a un errore", intro="""
        Davanti a un errore conviene seguire sempre lo stesso procedimento. Si comincia leggendo l'ultima
        riga del traceback, che dice che cosa è successo, e poi si cerca la freccia che nella nostra
        cella indica dove. Se un nome risulta inesistente, conviene eseguire di nuovo le celle sopra,
        dall'inizio, perché dopo un **Restart** le variabili non esistono più. Quando la riga che dà
        errore contiene più operazioni, la si spezza mettendo un'operazione per cella, finché l'errore
        resta in una sola.
    """)
    nb.md("""
        Se il messaggio non basta a capire il problema, si può cercare su internet il nome dell'errore
        insieme al messaggio, togliendo i nomi delle nostre variabili, che non dicono nulla a chi non
        conosce il nostro codice. Un'altra strada è incollare il traceback intero nella chat di un
        agente e chiedere di spiegarlo; anche in questo caso la correzione proposta va verificata
        eseguendo di nuovo la cella.
    """)

    nb.md("Riassunto in una pagina: [Gli errori più comuni](../Schede/Scheda_errori.md).")

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Quattro celle da sistemare",
        scenario="""
            Le quattro celle qui sotto contengono ciascuna un errore diverso, tra quelli visti nella
            sezione sugli errori più comuni.
        """,
        richiesta="""
            Esegui le celle una dopo l'altra. Per ciascuna leggi l'ultima riga del traceback, trova la
            riga indicata dalla freccia e correggi il minimo indispensabile, senza cambiare quello che la
            cella calcola. Alla fine devono esistere le variabili `totale`, `anni_alla_pensione` e
            `capitale`, e la lista `citta` deve contenere quattro città.
        """,
        suggerimento="ogni cella contiene un solo errore, quindi dopo averla corretta conviene rieseguirla e controllare l'output prima di passare alla successiva.",
        starter="""
            prezzi = [2.5, 1.2, 3.8]
            totale = sum(prezzo)
            totale
        """,
        soluzione="""
            prezzi = [2.5, 1.2, 3.8]
            totale = sum(prezzi)
            totale
        """,
        perche="""
            Le quattro celle danno quattro errori diversi: un `NameError` per il nome sbagliato della
            lista, un `TypeError` per la sottrazione tra un numero e un testo, un `KeyError` per la
            chiave scritta in minuscolo e un `AttributeError` per il metodo `add`, che le liste non
            hanno. In tutti i casi la correzione sta nella riga indicata dalla freccia.
        """,
    )
    _altra_cella_rotta(nb, starter="""
        eta = "24"
        anni_alla_pensione = 70 - eta
        anni_alla_pensione
    """, soluzione="""
        eta = "24"
        anni_alla_pensione = 70 - int(eta)
        anni_alla_pensione
    """)
    _altra_cella_rotta(nb, starter="""
        capitali = {"Italia": "Roma", "Francia": "Parigi", "Spagna": "Madrid"}
        capitale = capitali["italia"]
        capitale
    """, soluzione="""
        capitali = {"Italia": "Roma", "Francia": "Parigi", "Spagna": "Madrid"}
        capitale = capitali["Italia"]
        capitale
    """)
    _altra_cella_rotta(nb, starter="""
        citta = ["Roma", "Milano", "Torino"]
        citta.add("Napoli")
        citta
    """, soluzione="""
        citta = ["Roma", "Milano", "Torino"]
        citta.append("Napoli")
        citta
    """)
    _verifica_finale(nb, """
        assert round(totale, 2) == 7.5, "❌ totale: la lista si chiama prezzi"
        assert anni_alla_pensione == 46, "❌ anni_alla_pensione: eta è un testo, convertilo con int()"
        assert capitale == "Roma" and citta[-1] == "Napoli", "❌ capitale o citta: la chiave è Italia con la maiuscola; una lista si allunga con append"
    """)

    nb.esercizio(
        titolo="Leggere una firma",
        scenario="""
            Per ordinare una lista Python mette a disposizione la funzione `sorted`. Quello che serve
            per usarla, cioè quali parametri accetta e quali valori predefiniti hanno, si legge nella
            sua firma.
        """,
        richiesta="""
            Esegui `help(sorted)` e compila il dizionario `risposte`: alla chiave `"obbligatorio"`
            assegna il nome dell'unico parametro obbligatorio e alla chiave `"default_reverse"` il valore
            predefinito di `reverse`. Poi usa il parametro `reverse` per ordinare `voti` dal più alto al
            più basso e salva il risultato in `dal_piu_alto`, che alla fine deve essere la lista
            `[30, 28, 25, 18]`.
        """,
        suggerimento="nella firma il parametro obbligatorio è quello che non è seguito da `=`.",
        starter="""
            voti = [28, 18, 30, 25]

            risposte = {
                "obbligatorio": ...,
                "default_reverse": ...,
            }
            dal_piu_alto = sorted(voti, ...)
            dal_piu_alto
        """,
        soluzione="""
            voti = [28, 18, 30, 25]

            risposte = {
                "obbligatorio": "iterable",
                "default_reverse": False,
            }
            dal_piu_alto = sorted(voti, reverse=True)
            dal_piu_alto
        """,
        verifica="""
            assert risposte["obbligatorio"] == "iterable", "❌ obbligatorio: il nome del parametro che nella firma non ha ="
            assert risposte["default_reverse"] is False, "❌ default_reverse: il valore dopo reverse=, senza virgolette"
            assert dal_piu_alto == [30, 28, 25, 18], "❌ dal_piu_alto: passa reverse=True per nome"
        """,
        perche="""
            Nella firma `sorted(iterable, /, *, key=None, reverse=False)` il parametro `iterable` è
            l'unico senza valore predefinito, e poiché sta prima di `/` si passa per posizione. Il
            parametro `reverse` vale `False` se non lo indichiamo e, poiché sta dopo `*`, si può passare
            solo per nome, scrivendo `reverse=True`.
        """,
    )
    return nb
