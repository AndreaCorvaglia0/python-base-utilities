"""02 · Tipi di dato e manipolazione: liste, tuple, dizionari, set e costruttori."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="02",
        file="02_Tipi_di_dato",
        titolo="Tipi di dato e manipolazione",
        blocco=1,
        giornata=1,
        intento="Le principali strutture dati di Python (liste, tuple, dizionari e set) e come manipolarle.",
        obiettivi=[
            "selezionare elementi di una lista con indexing e slicing",
            "aggiungere, modificare e togliere elementi da liste e dizionari",
            "riconoscere tuple e set e convertire un tipo nell'altro con i costruttori",
        ],
        tempo={"base": 50, "avanzata": 40},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Liste", intro="""
        Le **liste** sono sequenze ordinate di elementi, dove ogni elemento è identificato da un **indice**.
        In Python le liste sono **indicizzate a partire da 0**.

        Ad esempio, consideriamo la seguente lista:
    """)
    nb.code("""
        lista_numeri = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
        lista_numeri
    """)

    nb.sottosezione("Indexing", intro="""
        Possiamo accedere all'elemento in posizione `i` della lista con l'operatore di **indexing** `[]`:
    """)
    nb.code("""
        elemento = lista_numeri[2]
        elemento
    """)
    nb.md("È possibile usare **indici negativi** per accedere agli elementi dalla fine della lista:")
    nb.code("""
        elemento = lista_numeri[-2]
        elemento
    """)

    nb.sottosezione("Slicing", intro="""
        Con l'operatore di **slicing** selezioniamo una porzione della lista. La sintassi è `[start:end:step]`.

        Selezionare i primi 5 elementi della lista:
    """)
    nb.code("""
        primi_cinque = lista_numeri[:5]
        print(primi_cinque)
    """)
    nb.md("Selezionare gli elementi dalla posizione 3 alla posizione 7:")
    nb.code("lista_numeri[3:8]")
    nb.md("Selezionare gli ultimi 3 elementi della lista:")
    nb.code("""
        ultimi_tre = lista_numeri[-3:]
        print(ultimi_tre)
    """)
    nb.md("Con uno **step** negativo invertiamo l'ordine degli elementi:")
    nb.code("""
        inversi = lista_numeri[::-1]
        inversi
    """)
    nb.md("Possiamo modificare gli elementi di una lista assegnando nuovi valori a una porzione di essa:")
    nb.code("""
        # modifica i primi 3 elementi della lista
        lista_numeri[:3] = [10, 11, 12]
        print(lista_numeri)
    """)
    nb.code("lista_numeri[::2]  # un elemento ogni due")

    nb.sottosezione("Aggiunta e rimozione di elementi", intro="""
        Aggiungere un elemento alla fine della lista con `append()`:
    """)
    nb.code("""
        lista_numeri.append(11)
        lista_numeri
    """)
    nb.code("""
        lista_numeri.extend([13, 14])  # aggiunge più elementi in una volta
        print(lista_numeri)
    """)
    nb.md("Rimuovere un elemento specifico con `remove()`:")
    nb.code("""
        lista_numeri.remove(10)
        lista_numeri
    """)

    nb.sottosezione("Lunghezza della lista", intro="""
        Per ottenere la lunghezza di una lista usiamo la funzione `len()`:
    """)
    nb.code("""
        lunghezza = len(lista_numeri)
        print(f"La lista contiene {lunghezza} elementi.")  # Output: La lista contiene 12 elementi.
    """)

    nb.sottosezione("Liste di liste", intro="""
        Le **liste di liste** servono a rappresentare strutture come matrici o tabelle.
        Ad esempio, una matrice 3x3 può essere rappresentata così:
    """)
    nb.code("""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    """)
    nb.md("Per accedere all'elemento in posizione `[i][j]` (riga `i`, colonna `j`):")
    nb.code("""
        i = 2
        j = 1
        elemento = matrix[i][j]
        print(elemento)  # Output: 8
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Tuple", intro="""
        Le **tuple** sono sequenze di oggetti **immutabili**, racchiuse tra parentesi tonde `()` e separate da virgole.
    """)
    nb.sottosezione("Creazione di una tupla")
    nb.code("my_tuple = (1, 2, 3, 4, 5)")

    nb.sottosezione("Accesso agli elementi", intro="Accediamo agli elementi tramite l'indice:")
    nb.code("print(my_tuple[2])  # Output: 3")
    nb.md("Possiamo usare lo **slicing** anche sulle tuple:")
    nb.code("print(my_tuple[:3])  # Output: (1, 2, 3)")

    nb.sottosezione("Immutabilità delle tuple", intro="""
        Le tuple sono **immutabili**: una volta create non possono essere modificate, e se proviamo ad
        assegnare un elemento Python dà errore.
    """)
    nb.code("my_tuple[2] = 1", errore=True)

    # ------------------------------------------------------------------ 3
    nb.sezione("Dizionari", intro="""
        I **dizionari** sono strutture dati che memorizzano coppie **chiave-valore**.
    """)
    nb.sottosezione("Creazione di un dizionario", intro="""
        La sintassi è `{chiave1: valore1, chiave2: valore2, ...}`. Esempio:
    """)
    nb.code("dizionario = {'nome': 'Marco', 'cognome': 'Rossi', 'età': 30}")
    nb.box("nota", "Le chiavi devono essere di tipo **immutabile** (stringhe, numeri, tuple). I valori possono essere di qualsiasi tipo.")

    nb.sottosezione("Accesso ai valori", intro="Per accedere a un valore usiamo la chiave corrispondente:")
    nb.code("print(dizionario['cognome'])  # Output: Rossi")

    nb.sottosezione("Modifica di un dizionario", intro="Aggiunta di un elemento:")
    nb.code("""
        dizionario['sesso'] = 'M'
        print(dizionario)
        # Output: {'nome': 'Marco', 'cognome': 'Rossi', 'età': 30, 'sesso': 'M'}
    """)
    nb.md("Aggiornamento di un elemento:")
    nb.code("""
        dizionario['età'] = 31
        print(dizionario)
        # Output: {'nome': 'Marco', 'cognome': 'Rossi', 'età': 31, 'sesso': 'M'}
    """)
    nb.md("Rimozione di un elemento con `del`:")
    nb.code("""
        del dizionario['età']
        print(dizionario)
        # Output: {'nome': 'Marco', 'cognome': 'Rossi', 'sesso': 'M'}
    """)

    nb.sottosezione("Accesso alle chiavi e ai valori", intro="""
        Con `keys()` otteniamo tutte le chiavi, con `values()` tutti i valori:
    """)
    nb.code("""
        chiavi = list(dizionario.keys())
        print(chiavi)  # Output: ['nome', 'cognome', 'sesso']

        valori = list(dizionario.values())
        print(valori)  # Output: ['Marco', 'Rossi', 'M']
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Set", intro="""
        I **set** sono collezioni di elementi **unici**, ognuno di tipo immutabile.
        Per creare un set usiamo le parentesi graffe `{}` o il costruttore `set()`:
    """)
    nb.code("""
        colori = {"rosso", "verde", "blu"}
        # oppure
        colori = set(["rosso", "verde", "blu"])
    """)
    nb.box("attenzione", "I set sono **non ordinati**: l'ordine in cui Python stampa gli elementi può essere diverso da quello in cui li abbiamo scritti.")

    nb.sottosezione("Operazioni con i set", intro="Unione:")
    nb.code("""
        colori = {"rosso", "verde", "blu"}
        altri_colori = {"giallo", "rosso", "viola"}

        unione = colori.union(altri_colori)
        print(unione)
        # Output: {'blu', 'rosso', 'verde', 'giallo', 'viola'}
    """)
    nb.md("Intersezione:")
    nb.code("""
        intersezione = colori.intersection(altri_colori)
        print(intersezione)
        # Output: {'rosso'}
    """)
    nb.box("nota", """
        - **Elementi unici:** un set non contiene doppioni.
        - **Operazioni di insieme:** unione, intersezione, differenza.
        - **Appartenenza:** controllare se un elemento c'è è rapido.
    """, titolo="Perché usare i set")

    # ------------------------------------------------------------------ 5
    nb.sezione("Costruttori e conversioni", intro="""
        Oltre alle notazioni `[]`, `()` e `{}`, esistono i costruttori `list()`, `tuple()`, `set()` e `dict()`.
        Accettano un iterabile come input e servono soprattutto a convertire un tipo nell'altro.
    """)
    nb.md("""
        - `[]` crea una lista direttamente: `[1, 2, 3]`; `list((1, 2, 3))` trasforma una tupla in lista.
        - `()` definisce una tupla: `(1, 2, 3)`; `tuple([1, 2, 3])` converte una lista in tupla.
        - `{}` definisce un set (`{1, 2, 3}`) o un dizionario con coppie chiave-valore (`{'a': 1, 'b': 2}`); `set([1, 2, 3])` crea un set da una lista.
    """)
    nb.code("list({1, 2, 3})")
    nb.code("set([1, 2, 3, 3])")

    # ------------------------------------------------------------------ 6
    nb.sezione("Quale struttura usare")
    nb.md("""
        - **Lista** `[3, 6, 9]`: valori in ordine, anche ripetuti, che possono cambiare.
        - **Tupla** `(1, 2, 3)`: pochi valori che vanno insieme e non cambiano.
        - **Dizionario** `{'nome': 'Marco'}`: cercare un valore per chiave, non per posizione.
        - **Set** `{'rosso', 'verde'}`: valori unici, controllare se un elemento c'è.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Lista invertita",
        scenario="",
        richiesta="Inverti la lista `[1, 2, 3, 4, 5]` e metti il risultato in `lista_invertita`. Output atteso: `[5, 4, 3, 2, 1]`.",
        starter="""
            lista = [1, 2, 3, 4, 5]

            # scrivi il tuo codice qui
            lista_invertita = lista[...]
            print(lista_invertita)  # Output: [5, 4, 3, 2, 1]
        """,
        soluzione="""
            lista = [1, 2, 3, 4, 5]

            lista_invertita = lista[::-1]
            print(lista_invertita)  # Output: [5, 4, 3, 2, 1]
        """,
        verifica="""
            assert lista_invertita == [5, 4, 3, 2, 1], "❌ Lista invertita errata"
            print("✅ Lista invertita correttamente")
        """,
    )
    nb.esercizio(
        titolo="Posizioni pari",
        scenario="",
        richiesta="""
            Seleziona gli elementi in posizione pari, escludendo la posizione 0 (tutte le donne tranne Elena),
            e mettili in `elementi_pari`. Output atteso: `['Martina', 'Giulia', 'Francesca', 'Sara']`.
        """,
        suggerimento="lo slicing ha tre parti, `[start:end:step]`.",
        starter="""
            lista = ["Elena", "Luigi", "Martina", "Marco", "Giulia", "Simone", "Francesca", "Alessandro", "Sara", "Lorenzo"]

            # scrivi il tuo codice qui
            elementi_pari = lista[...]
            print(elementi_pari)  # Output: ['Martina', 'Giulia', 'Francesca', 'Sara']
        """,
        soluzione="""
            lista = ["Elena", "Luigi", "Martina", "Marco", "Giulia", "Simone", "Francesca", "Alessandro", "Sara", "Lorenzo"]

            elementi_pari = lista[2::2]
            print(elementi_pari)  # Output: ['Martina', 'Giulia', 'Francesca', 'Sara']
        """,
        verifica="""
            assert elementi_pari == ["Martina", "Giulia", "Francesca", "Sara"], "❌ Elementi pari errati"
            print("✅ Elementi pari corretti")
        """,
    )
    nb.esercizio(
        titolo="Le capitali del G8",
        scenario="""
            Il dizionario `g8` associa i paesi del G8 alla rispettiva capitale, ma è incompleto.
            La Russia è stata esclusa dal G8 nel 2014, che è diventato il G7.
        """,
        richiesta="""
            1. Aggiungi a `g8` `'Regno Unito': 'Londra'` e `'Stati Uniti': 'Washington, D.C.'`.
            2. In `g7`, una copia di `g8`, togli la Russia con `pop`.
            3. Ipotizziamo che entrino nel G7 Spagna, Paesi Bassi e Corea del Sud: in `g10`, una copia di `g7`,
               aggiungi `'Madrid'`, `'Amsterdam'` e `'Seoul'`.
            4. Supponiamo che l'Italia cambi capitale: ora è Bobbio. Aggiorna `g10`.
        """,
        starter="""
            g8 = {
                'Canada': 'Ottawa',
                'Francia': 'Parigi',
                'Germania': 'Berlino',
                'Italia': 'Roma',
                'Giappone': 'Tokyo',
                'Russia': 'Mosca'
            }

            # 1. aggiungi i paesi mancanti
            g8[...] = 'Londra'
            g8...
            print(g8)

            # 2. togli la Russia (la copia lascia intatto l'originale)
            g7 = g8.copy()
            g7.pop...
            print(g7)

            # 3. aggiungi i nuovi paesi
            g10 = g7.copy()
            g10['Spagna'] = 'Madrid'
            g10... = 'Amsterdam'
            ... = 'Seoul'

            # 4. cambia la capitale dell'Italia
            ...
            print(g10)

            lista_paesi = list(g10.keys())
            print(lista_paesi)
        """,
        soluzione="""
            g8 = {
                'Canada': 'Ottawa',
                'Francia': 'Parigi',
                'Germania': 'Berlino',
                'Italia': 'Roma',
                'Giappone': 'Tokyo',
                'Russia': 'Mosca'
            }

            # 1. aggiungi i paesi mancanti
            g8['Regno Unito'] = 'Londra'
            g8['Stati Uniti'] = 'Washington, D.C.'
            print(g8)

            # 2. togli la Russia (la copia lascia intatto l'originale)
            g7 = g8.copy()
            g7.pop('Russia')
            print(g7)

            # 3. aggiungi i nuovi paesi
            g10 = g7.copy()
            g10['Spagna'] = 'Madrid'
            g10['Paesi Bassi'] = 'Amsterdam'
            g10['Corea del Sud'] = 'Seoul'

            # 4. cambia la capitale dell'Italia
            g10['Italia'] = 'Bobbio'
            print(g10)

            lista_paesi = list(g10.keys())
            print(lista_paesi)
        """,
        verifica="""
            assert g8['Regno Unito'] == 'Londra' and g8['Stati Uniti'] == 'Washington, D.C.', "❌ g8: mancano Regno Unito o Stati Uniti"
            assert 'Russia' not in g7 and 'Russia' in g8, "❌ g7: la Russia va tolta dalla copia g7, non da g8"
            assert g10['Paesi Bassi'] == 'Amsterdam' and g10['Corea del Sud'] == 'Seoul' and g10['Italia'] == 'Bobbio', "❌ g10: controlla i paesi nuovi e la capitale dell'Italia"
            print("✅ Dizionari corretti")
        """,
    )
    return nb
