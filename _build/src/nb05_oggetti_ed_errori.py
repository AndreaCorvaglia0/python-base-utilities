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
        intento="Come si legge una riga di codice scritta da altri e come si legge un messaggio di errore.",
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
        In Python ogni valore è un oggetto: porta con sé dei dati e le operazioni che sa fare.
        `type` dice di che oggetto si tratta.
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
        Le operazioni di un oggetto si chiamano metodi e si scrivono con il punto e le parentesi:
        `dato.metodo()`. Cosa fa il metodo lo decide l'oggetto a sinistra del punto.
    """)
    nb.code("""
        print("Roma".upper())          # Output: ROMA
        print(citta.index("Milano"))   # Output: 1
    """)
    nb.md("""
        Un DataFrame di pandas è un oggetto come gli altri. Usiamo un piccolo DataFrame di pandas:
        tre persone con nome, età e città.
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
        Un oggetto ha anche degli attributi: dati che conserva e che si leggono senza parentesi.
        `df.shape` dice quante righe e colonne ha, `df.columns` come si chiamano le colonne.
    """)
    nb.code("""
        print(df.shape)
        print(df.columns)
    """)
    nb.md("Un metodo invece è un'azione e vuole le parentesi, anche vuote: `df.head(2)` mostra le prime due righe.")
    nb.code("df.head(2)")
    nb.md("""
        Se dimentichiamo le parentesi non c'è errore: Python restituisce il metodo stesso, non il suo
        risultato. Quando nell'output compare `bound method`, mancano le parentesi.
    """)
    nb.code("df.head")
    nb.md("""
        Alcune operazioni non sono metodi ma funzioni di Python, come `len` e `print`: l'oggetto va
        tra le parentesi. Per vedere i metodi di un oggetto si scrive il punto e si preme Tab.
    """)
    nb.code("len(citta), len(df)   # Output: (3, 3)")

    # ------------------------------------------------------------------ 2
    nb.sezione("Chi è chi in una riga di codice", intro="""
        Con questi pezzi possiamo leggere una riga intera. Prendiamo la lettura di un file.

        ```python
        turbina = pd.read_csv("../Dati/TexasTurbine.csv", nrows=24)
        ```
    """)
    nb.md("""
        `pd` è la libreria pandas, importata con un nome corto, e `read_csv` è una sua funzione. Tra
        parentesi ci sono gli argomenti: il percorso del file per posizione, `nrows=24` per nome (solo
        le prime 24 righe). Il risultato finisce in `turbina`.
    """)
    nb.code("""
        turbina = pd.read_csv("../Dati/TexasTurbine.csv", nrows=24)
        type(turbina)
    """)
    nb.md("""
        `pandas.DataFrame` si legge: la classe `DataFrame` della libreria `pandas`. La classe
        definisce com'è fatto un oggetto; `turbina` è un oggetto di quella classe. Anche `str` e `list` sono classi:
        `citta` è un oggetto della classe `list`.
    """)
    nb.md("""
        Un import si legge allo stesso modo: `import plotly.express as px` prende il sottomodulo
        `express` della libreria `plotly` e lo chiama `px`.
    """)
    nb.md("""
        Le forme sono poche e si riconoscono dalla punteggiatura.

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
            Per ogni riga scrivi nel commento cos'è, con le parole della tabella.
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
            Una classe si scrive con `class`. Il metodo `__init__` parte quando chiamiamo
            `Prodotto(...)` e salva i dati dentro l'oggetto; `self` è l'oggetto stesso, quello che starà
            a sinistra del punto. Le classi si incontrano nelle librerie e nel codice scritto da un agente.
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
        I parametri di una funzione si leggono con `help(funzione)`, oppure con il nome seguito da `?`.
    """)
    nb.code("help(round)")
    nb.md("""
        La prima riga è la firma. `number` non ha `=`: è obbligatorio. `ndigits=None` ha un default e
        si può omettere; `None` è il valore "niente" di Python, qui vuol dire nessun decimale.
    """)
    nb.code("round(27.567), round(27.567, ndigits=1)   # Output: (28, 27.6)")
    nb.md("""
        Nelle firme si trovano anche i type hint: dopo i due punti il tipo atteso, dopo la freccia `->`
        il tipo restituito. Python non li controlla, servono a chi legge.
    """)
    nb.code('''
        def media(voti: list[float]) -> float:
            """Media aritmetica di una lista di voti."""
            return sum(voti) / len(voti)


        media([28, 30, 25])
    ''')
    nb.code("help(media)")
    nb.md("""
        `help` mostra firma, type hint e docstring insieme. Nelle librerie i tipi possono essere più
        lunghi, come `encoding: str | None = None` in `read_csv`: la barra verticale vuol dire "oppure".
    """)
    nb.box("nota", """
        Nelle firme delle funzioni di Python compaiono anche `/` e `*` da soli: i parametri prima di
        `/` si passano solo per posizione, quelli dopo `*` solo per nome.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Gli errori più comuni", intro="""
        Quando qualcosa va storto Python ferma la cella e stampa un traceback. Si legge dal basso:
        l'ultima riga dice il tipo di errore e il perché, la riga con la freccia `---->` dice dove. Le
        celle di questa sezione danno errore apposta.
    """)
    nb.sottosezione("SyntaxError", intro="""
        La riga non è Python valido: qui mancano i due punti dopo la condizione dell'`if`. Il `^` indica
        il punto in cui Python si è fermato.
    """)
    nb.code("""
        voto = 28
        if voto >= 18
            print("Promosso")
    """, errore=True)
    nb.sottosezione("NameError", intro="""
        Il nome non esiste: è scritto diverso, oppure è definito in una cella non ancora eseguita.
        L'ultima riga riporta il nome cercato, qui `cita` con una `t` sola.
    """)
    nb.code("""
        citta = ["Roma", "Milano", "Torino"]
        print(cita)
    """, errore=True)
    nb.sottosezione("TypeError", intro="""
        I tipi non vanno d'accordo: un testo e un numero non si sommano. Si converte prima, qui con
        `str(eta)`.
    """)
    nb.code("""
        eta = 24
        "Alice ha " + eta + " anni"
    """, errore=True)
    nb.sottosezione("KeyError", intro="""
        La chiave non c'è: l'ultima riga la riporta tale e quale, e si vede che è minuscola. Lo stesso
        errore arriva chiedendo una colonna che il DataFrame non ha.
    """)
    nb.code("""
        prezzi = {"Pane": 2.5, "Latte": 1.2, "Caffè": 3.8}
        prezzi["pane"]
    """, errore=True)
    nb.sottosezione("IndexError", intro="""
        La posizione non esiste: tre elementi occupano le posizioni 0, 1 e 2. L'ultimo si prende con
        `citta[-1]`.
    """)
    nb.code("""
        citta = ["Roma", "Milano", "Torino"]
        citta[3]
    """, errore=True)
    nb.sottosezione("ValueError", intro="""
        Il tipo è giusto ma il valore no: `float` accetta un testo, ma non riconosce la virgola
        decimale. Funziona con il punto: `float("2.50")`.
    """)
    nb.code('float("2,50")', errore=True)
    nb.sottosezione("FileNotFoundError", intro="""
        Il file non c'è dove lo cerchiamo. L'ultima riga riporta il percorso provato, da confrontare con
        il nome vero nella cartella; le righe in mezzo, dentro pandas, si saltano.
    """)
    nb.code('pd.read_csv("../Dati/texas_turbine.csv")', errore=True)
    nb.sottosezione("AttributeError", intro="""
        L'oggetto non ha quel metodo o attributo: un DataFrame non ha `sort`, ha `sort_values`. Capita
        spesso con un nome plausibile suggerito da un agente.
    """)
    nb.code('df.sort("Età")', errore=True)

    # ------------------------------------------------------------------ 5
    nb.sezione("Cosa fare davanti a un errore")
    nb.md("""
        1. Leggi l'ultima riga del traceback, poi cerca la freccia nella tua cella.
        2. Esegui le celle sopra, dall'inizio: dopo un **Restart** le variabili non esistono più.
        3. Spezza la riga: un'operazione per cella, finché l'errore resta in una sola.
        4. Cerca su internet il nome dell'errore con il messaggio, senza i tuoi nomi di variabile.
        5. Incolla il traceback intero nella chat dell'agente e chiedi di spiegarlo; poi verifica eseguendo.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Quattro celle da sistemare",
        scenario="Le quattro celle qui sotto danno ciascuna un errore diverso.",
        richiesta="""
            Leggi l'ultima riga del traceback, trova la riga con la freccia e correggi il minimo, senza
            cambiare cosa calcola la cella. Alla fine devono esistere `totale`, `anni_alla_pensione`,
            `capitale` e `citta` con quattro città.
        """,
        suggerimento="ogni cella ha un errore solo. Esegui, leggi, correggi, riesegui.",
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
        perche="Quattro ultime righe diverse: il nome, i tipi, la chiave, il metodo. In ogni caso la correzione sta nella riga indicata dalla freccia.",
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
        scenario="Per ordinare una lista Python ha la funzione `sorted`. Tutto quello che serve sta nella sua firma.",
        richiesta="""
            Esegui `help(sorted)` e compila `risposte`: in `"obbligatorio"` il nome dell'unico parametro
            obbligatorio, in `"default_reverse"` il default di `reverse`. Poi usa `reverse` per ordinare
            `voti` dal più alto al più basso in `dal_piu_alto`. Output atteso: `[30, 28, 25, 18]`.
        """,
        suggerimento="il parametro obbligatorio è quello senza `=`.",
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
        perche="`iterable` sta prima di `/` e si passa per posizione; `reverse` sta dopo `*` e si passa per nome.",
    )
    return nb
