"""02 · Tipi di dato e manipolazione: liste, tuple, dizionari, set e costruttori."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="02",
        file="02_Tipi_di_dato",
        titolo="Tipi di dato e manipolazione",
        blocco=1,
        giornata=1,
        intento=(
            "In questo notebook vediamo le principali strutture dati di Python, cioè liste, tuple, "
            "dizionari e set, e le operazioni con cui si leggono e si modificano."
        ),
        obiettivi=[
            "selezionare elementi di una lista con indexing e slicing",
            "aggiungere, modificare e togliere elementi da liste e dizionari",
            "riconoscere tuple e set e convertire un tipo nell'altro con i costruttori",
        ],
        tempo={"base": 40, "avanzata": 35},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Liste", intro="""
        Le **liste** sono sequenze ordinate di elementi, in cui ogni elemento è identificato da un
        **indice** che ne indica la posizione. In Python le liste sono **indicizzate a partire da 0**,
        quindi il primo elemento ha indice 0, il secondo indice 1 e così via. Una lista si scrive
        elencando gli elementi tra parentesi quadre, separati da virgole, come nella lista di numeri qui
        sotto, che useremo in tutta la sezione.
    """)
    nb.code("""
        lista_numeri = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
        lista_numeri
    """)

    nb.sottosezione("Indexing", intro="""
        Per leggere l'elemento in posizione `i` si scrive l'indice tra parentesi quadre dopo il nome della
        lista, con l'operatore di **indexing** `[]`. Nell'esempio `lista_numeri[2]` restituisce il terzo
        elemento, cioè `9`, perché il conteggio parte da zero.
    """)
    nb.code("""
        elemento = lista_numeri[2]
        elemento
    """)
    nb.md("""
        Gli **indici negativi** contano invece dalla fine della lista, per cui `-1` indica l'ultimo
        elemento, `-2` il penultimo e così via. Sono comodi quando ci interessano gli ultimi elementi e
        non vogliamo calcolare la lunghezza della lista. Nella cella qui sotto `lista_numeri[-2]`
        restituisce `27`.
    """)
    nb.code("""
        elemento = lista_numeri[-2]
        elemento
    """)

    nb.sottosezione("Slicing", intro="""
        Con l'operatore di **slicing** selezioniamo una porzione della lista invece di un solo elemento.
        La sintassi è `[start:end:step]`, dove `start` è l'indice da cui si parte, `end` quello a cui ci
        si ferma, che resta escluso, e `step` il passo tra un elemento e il successivo. Ognuno dei tre
        valori si può omettere: senza `start` si parte dall'inizio, senza `end` si arriva alla fine e
        senza `step` si prendono gli elementi uno dopo l'altro. Per esempio, `[:5]` seleziona i primi
        cinque elementi, quelli con indice da 0 a 4.
    """)
    nb.code("""
        primi_cinque = lista_numeri[:5]
        print(primi_cinque)
    """)
    nb.md("""
        Poiché l'indice `end` è escluso, per selezionare gli elementi dalla posizione 3 alla posizione 7
        comprese si scrive `[3:8]`. Con passo 1 il numero di elementi selezionati è la differenza tra `end` e
        `start`, in questo caso cinque.
    """)
    nb.code("lista_numeri[3:8]")
    nb.hands_on(
        richiesta="""
            Salva in `porzione` gli elementi di `lista_numeri` dal terzo al quinto compreso, cioè quelli con
            indice da 2 a 4. Il risultato è `[9, 12, 15]`.
        """,
        starter="""
            porzione = lista_numeri[...]
            porzione
        """,
        soluzione="""
            porzione = lista_numeri[2:5]
            porzione  # Output: [9, 12, 15]
        """,
        verifica="""
            assert porzione == [9, 12, 15], "❌ porzione: si parte dall'indice 2 e ci si ferma prima del 5"
        """,
        prova_anche="`lista_numeri[5:]`, che parte dal sesto elemento e arriva alla fine della lista.",
    )
    nb.md("""
        Lo slicing accetta anche gli indici negativi. Con `[-3:]` si parte dal terzultimo elemento e,
        poiché `end` non è indicato, si arriva fino alla fine della lista, quindi si ottengono gli ultimi
        tre elementi.
    """)
    nb.code("""
        ultimi_tre = lista_numeri[-3:]
        print(ultimi_tre)
    """)
    nb.md("""
        Il terzo valore dello slicing, lo **step**, indica di quanto si avanza tra un elemento e il
        successivo. Con uno step negativo la lista viene percorsa dalla fine verso l'inizio, quindi
        `[::-1]` restituisce tutti gli elementi in ordine inverso.
    """)
    nb.code("""
        inversi = lista_numeri[::-1]
        inversi
    """)
    nb.md("""
        Le liste si possono modificare dopo averle create. Assegnando una nuova lista a una porzione, come
        `lista_numeri[:3]`, si sostituiscono gli elementi selezionati con quelli nuovi. Nell'esempio i
        primi tre numeri diventano `10`, `11` e `12`, mentre il resto della lista non cambia.
    """)
    nb.code("""
        # modifica i primi 3 elementi della lista
        lista_numeri[:3] = [10, 11, 12]
        print(lista_numeri)
    """)
    nb.md("""
        Con uno step positivo maggiore di uno si saltano invece degli elementi. Nella cella qui sotto
        `[::2]` parte dal primo elemento della lista appena modificata e ne prende uno ogni due.
    """)
    nb.code("lista_numeri[::2]  # un elemento ogni due")

    nb.sottosezione("Aggiunta e rimozione di elementi", intro="""
        Il metodo `append()` aggiunge un elemento alla fine della lista. A differenza della lettura con
        lo slicing, che restituisce una lista nuova, `append()` modifica direttamente la lista su cui
        viene chiamato, quindi non serve assegnare il risultato a una variabile.
    """)
    nb.code("""
        lista_numeri.append(11)
        lista_numeri
    """)
    nb.md("""
        Per aggiungere più elementi in una sola volta si usa `extend()`, che riceve una lista e ne accoda
        tutti gli elementi, nell'ordine, alla fine della lista di partenza.
    """)
    nb.code("""
        lista_numeri.extend([13, 14])  # aggiunge più elementi in una volta
        print(lista_numeri)
    """)
    nb.md("""
        Il metodo `remove()` toglie dalla lista un elemento indicato per valore, non per posizione. Se il
        valore compare più volte viene rimosso solo il primo, e se non compare Python segnala un errore.
        Nell'esempio togliamo il `10` inserito poco fa con lo slicing.
    """)
    nb.code("""
        lista_numeri.remove(10)
        lista_numeri
    """)

    nb.sottosezione("Lunghezza della lista", intro="""
        La funzione `len()` restituisce la lunghezza di una lista, cioè il numero dei suoi elementi. È la
        stessa funzione che nel notebook precedente abbiamo usato per contare i caratteri di una stringa,
        e funziona con tutte le strutture dati che vediamo in questo notebook.
    """)
    nb.code("""
        lunghezza = len(lista_numeri)
        print(f"La lista contiene {lunghezza} elementi.")  # Output: La lista contiene 12 elementi.
    """)
    nb.hands_on(
        richiesta="""
            Aggiungi `"caffè"` in fondo alla lista `spesa` con `append()` e salva in `quanti` il numero dei
            suoi elementi con `len()`. Il risultato è 4.
        """,
        starter="""
            spesa = ["pane", "latte", "uova"]

            ...
            quanti = ...
            print(spesa, quanti)
        """,
        soluzione="""
            spesa = ["pane", "latte", "uova"]

            spesa.append("caffè")
            quanti = len(spesa)
            print(spesa, quanti)  # Output: ['pane', 'latte', 'uova', 'caffè'] 4
        """,
        verifica="""
            assert spesa == ["pane", "latte", "uova", "caffè"], "❌ spesa: il caffè va aggiunto in fondo, con append()"
            assert quanti == 4, "❌ quanti: il numero degli elementi di spesa, con len()"
        """,
        prova_anche="togli `'latte'` con `remove()` e conta di nuovo gli elementi.",
    )

    nb.sottosezione("Liste di liste", intro="""
        Una lista può contenere elementi di qualsiasi tipo, comprese altre liste. Le **liste di liste**
        servono a rappresentare strutture a due dimensioni, come matrici o tabelle, in cui ogni lista
        interna è una riga. Per esempio, una matrice 3x3 si rappresenta con una lista di tre liste,
        ciascuna con tre numeri.
    """)
    nb.code("""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    """)
    nb.md("""
        Per leggere un elemento della matrice si usano due indici di seguito, nella forma `[i][j]`. Il
        primo seleziona la riga, cioè una delle liste interne, e il secondo seleziona la colonna
        all'interno di quella riga. Con `i = 2` e `j = 1` otteniamo il secondo elemento della terza
        riga, cioè `8`.
    """)
    nb.code("""
        i = 2
        j = 1
        elemento = matrix[i][j]
        print(elemento)  # Output: 8
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Tuple", intro="""
        Le **tuple** sono sequenze di oggetti come le liste, ma sono **immutabili**, cioè una volta
        create non si possono più modificare. Si scrivono tra parentesi tonde `()`, con gli elementi
        separati da virgole. Si usano per raggruppare pochi valori che vanno insieme e che non devono
        cambiare, come le coordinate di un punto o il giorno, il mese e l'anno di una data.
    """)
    nb.sottosezione("Creazione di una tupla")
    nb.code("my_tuple = (1, 2, 3, 4, 5)")

    nb.sottosezione("Accesso agli elementi", intro="""
        Gli elementi di una tupla si leggono con l'indice tra parentesi quadre, esattamente come per le
        liste, e anche in questo caso il conteggio parte da zero.
    """)
    nb.code("print(my_tuple[2])  # Output: 3")
    nb.md("""
        Anche lo **slicing** funziona sulle tuple nello stesso modo, con la differenza che il risultato è
        a sua volta una tupla, come si vede dalle parentesi tonde nell'output.
    """)
    nb.code("print(my_tuple[:3])  # Output: (1, 2, 3)")

    nb.sottosezione("Immutabilità delle tuple", intro="""
        Poiché le tuple sono **immutabili**, l'assegnazione a un elemento, che con una lista
        funzionerebbe, con una tupla non è permessa. La cella qui sotto prova a cambiare il terzo
        elemento e Python risponde con un `TypeError`, il cui messaggio spiega che un oggetto `tuple`
        non supporta l'assegnazione degli elementi.
    """)
    nb.code("my_tuple[2] = 1", errore=True)

    # ------------------------------------------------------------------ 3
    nb.sezione("Dizionari", intro="""
        I **dizionari** sono strutture dati che memorizzano coppie **chiave-valore**. A differenza di
        liste e tuple, in cui un elemento si trova per posizione, in un dizionario ogni valore si trova
        attraverso la sua chiave, che di solito è una stringa con un nome significativo.
    """)
    nb.sottosezione("Creazione di un dizionario", intro="""
        Un dizionario si scrive tra parentesi graffe, con ogni chiave separata dal suo valore da due punti
        e le coppie separate da virgole, secondo la sintassi `{chiave1: valore1, chiave2: valore2, ...}`.
        Il dizionario qui sotto descrive una persona con tre informazioni: il nome, il cognome e l'età.
    """)
    nb.code("dizionario = {'nome': 'Marco', 'cognome': 'Rossi', 'età': 30}")
    nb.box("nota", """
        Le chiavi devono essere di tipo **immutabile**, come stringhe, numeri o tuple, quindi una lista
        non può fare da chiave. I valori, invece, possono essere di qualsiasi tipo, comprese le liste e
        altri dizionari.
    """)

    nb.sottosezione("Accesso ai valori", intro="""
        Per leggere un valore si scrive la chiave corrispondente tra parentesi quadre, con la stessa
        notazione che per le liste usa l'indice. Se la chiave non esiste, Python segnala un `KeyError`.
    """)
    nb.code("print(dizionario['cognome'])  # Output: Rossi")
    nb.hands_on(
        richiesta="""
            Leggi dal dizionario `dizionario` il valore della chiave `'nome'` e salvalo nella variabile
            `nome`. Il risultato è `'Marco'`.
        """,
        starter="""
            nome = dizionario[...]
            print(nome)
        """,
        soluzione="""
            nome = dizionario['nome']
            print(nome)  # Output: Marco
        """,
        verifica="""
            assert nome == 'Marco', "❌ nome: la chiave 'nome' va scritta tra parentesi quadre e tra apici"
        """,
        prova_anche="leggi la chiave `'indirizzo'`, che non esiste, e Python risponde con un `KeyError`.",
    )

    nb.sottosezione("Modifica di un dizionario", intro="""
        Per aggiungere un elemento basta assegnare un valore a una chiave che non esiste ancora, e Python
        crea la nuova coppia in fondo al dizionario. Nell'esempio aggiungiamo in questo modo la chiave
        `'sesso'`.
    """)
    nb.code("""
        dizionario['sesso'] = 'M'
        print(dizionario)
        # Output: {'nome': 'Marco', 'cognome': 'Rossi', 'età': 30, 'sesso': 'M'}
    """)
    nb.md("""
        La stessa assegnazione, fatta su una chiave che esiste già, sostituisce il valore precedente. In
        questo modo aggiorniamo l'età da 30 a 31, senza cambiare la posizione della chiave né gli altri
        elementi.
    """)
    nb.code("""
        dizionario['età'] = 31
        print(dizionario)
        # Output: {'nome': 'Marco', 'cognome': 'Rossi', 'età': 31, 'sesso': 'M'}
    """)
    nb.hands_on(
        richiesta="""
            Aggiungi al dizionario `viaggio` la chiave `'mezzo'` con il valore `'treno'` e porta le notti da
            4 a 5. Il risultato è `{'destinazione': 'Vienna', 'notti': 5, 'mezzo': 'treno'}`.
        """,
        starter="""
            viaggio = {'destinazione': 'Vienna', 'notti': 4}

            ...
            ...
            print(viaggio)
        """,
        soluzione="""
            viaggio = {'destinazione': 'Vienna', 'notti': 4}

            viaggio['mezzo'] = 'treno'
            viaggio['notti'] = 5
            print(viaggio)  # Output: {'destinazione': 'Vienna', 'notti': 5, 'mezzo': 'treno'}
        """,
        verifica="""
            assert viaggio.get('mezzo') == 'treno', "❌ viaggio: manca la chiave 'mezzo' con il valore 'treno'"
            assert viaggio['notti'] == 5, "❌ notti: assegna 5 alla chiave che esiste già"
        """,
    )
    nb.md("""
        Per rimuovere un elemento si usa l'istruzione `del`, seguita dal dizionario e dalla chiave tra
        parentesi quadre, e dopo questa cella la chiave `'età'` non esiste più. In alternativa si può
        usare il metodo `pop()`, che rimuove la chiave e restituisce il valore che le era associato.
    """)
    nb.code("""
        del dizionario['età']
        print(dizionario)
        # Output: {'nome': 'Marco', 'cognome': 'Rossi', 'sesso': 'M'}
    """)

    nb.sottosezione("Accesso alle chiavi e ai valori", intro="""
        I metodi `keys()` e `values()` restituiscono rispettivamente tutte le chiavi e tutti i valori del
        dizionario. Il risultato non è una lista ma un oggetto di tipo particolare, che convertiamo in
        lista con `list()` per poterlo usare come una lista qualsiasi, per esempio leggendone un elemento
        con l'indice.
    """)
    nb.code("""
        chiavi = list(dizionario.keys())
        print(chiavi)  # Output: ['nome', 'cognome', 'sesso']

        valori = list(dizionario.values())
        print(valori)  # Output: ['Marco', 'Rossi', 'M']
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Set", intro="""
        I **set** sono collezioni di elementi **unici**, nel senso che un valore inserito più volte
        compare nel set una volta sola. Come le chiavi dei dizionari, gli elementi di un set devono
        essere di tipo immutabile. Un set si crea elencando gli elementi tra parentesi graffe oppure
        passando una lista al costruttore `set()`, e le due forme della cella qui sotto producono lo
        stesso risultato. Le parentesi graffe vuote `{}` creano però un dizionario, quindi un set vuoto si
        scrive `set()`.
    """)
    nb.code("""
        colori = {"rosso", "verde", "blu"}
        # oppure
        colori = set(["rosso", "verde", "blu"])
    """)
    nb.box("attenzione", """
        I set sono **non ordinati**, quindi l'ordine in cui Python stampa gli elementi può essere diverso
        da quello in cui li abbiamo scritti. Per lo stesso motivo un set non ha indici, e un'espressione
        come `colori[0]` produce un errore.
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Costruttori e conversioni", intro="""
        Oltre alle notazioni `[]`, `()` e `{}`, Python mette a disposizione i costruttori `list()`,
        `tuple()`, `set()` e `dict()`. Ciascuno accetta come input un iterabile, cioè un oggetto di cui
        si possono scorrere gli elementi uno alla volta, come una lista, una tupla, un set o una
        stringa, e per questo i costruttori servono soprattutto a convertire un tipo nell'altro.
    """)
    nb.md("""
        Per esempio, `list((1, 2, 3))` trasforma una tupla in una lista e `tuple([1, 2, 3])` fa
        l'operazione inversa. Allo stesso modo, nella cella qui sotto, `list()` trasforma un set in una
        lista, che a differenza del set ha un ordine e si può leggere con gli indici.
    """)
    nb.code("list({1, 2, 3})")
    nb.md("""
        Con le parentesi graffe conviene fare attenzione, perché con valori semplici, come in
        `{1, 2, 3}`, definiscono un set, mentre con coppie chiave-valore, come in `{'a': 1, 'b': 2}`,
        definiscono un dizionario. Il costruttore `set()` applicato a una lista ne elimina i duplicati,
        come mostra la cella seguente, in cui il `3` ripetuto compare una volta sola.
    """)
    nb.code("set([1, 2, 3, 3])")
    nb.hands_on(
        richiesta="""
            Salva in `diversi` il set dei voti della lista `voti`, in cui ogni voto compare una volta sola, e
            in `quanti` il numero dei voti diversi. Il set contiene 6, 7, 8 e 9, quindi `quanti` vale 4.
        """,
        starter="""
            voti = [7, 8, 6, 8, 7, 9, 7]

            diversi = ...
            quanti = ...
            print(diversi, quanti)
        """,
        soluzione="""
            voti = [7, 8, 6, 8, 7, 9, 7]

            diversi = set(voti)
            quanti = len(diversi)
            print(diversi, quanti)
        """,
        verifica="""
            assert diversi == {6, 7, 8, 9}, "❌ diversi: il set costruito dalla lista voti, con set()"
            assert quanti == 4, "❌ quanti: la lunghezza del set, con len()"
        """,
        prova_anche="`len(voti)`, che conta anche le ripetizioni e restituisce 7.",
    )

    # ------------------------------------------------------------------ 6
    nb.sezione("Quale struttura usare")
    nb.md("""
        La scelta della struttura dipende da come useremo i dati. Una lista, come `[3, 6, 9]`, conviene
        quando i valori hanno un ordine, possono ripetersi e possono cambiare nel tempo. Una tupla, come
        `(1, 2, 3)`, è adatta a pochi valori che vanno insieme e che non devono cambiare. Un dizionario,
        come `{'nome': 'Marco'}`, serve quando vogliamo cercare un valore attraverso una chiave invece
        che per posizione, mentre un set, come `{'rosso', 'verde'}`, raccoglie valori senza ripetizioni e
        permette di controllare rapidamente se un elemento è presente.
    """)

    # ------------------------------------------------------------------ Extra
    nb.sezione("Extra", """
        Questa sezione raccoglie due esercizi brevi sui punti principali del notebook, pensati per il
        ripasso a casa, e durante la lezione la saltiamo. Ogni esercizio lavora sui dati scritti nella
        propria cella, quindi si può svolgere anche senza aver eseguito il resto del notebook.
    """)
    nb.esercizio(
        titolo="Il carrello con i prezzi",
        scenario="""
            Al supermercato Marta segna nel dizionario `prezzi` quanto costa ogni prodotto che mette nel
            carrello, così prima della cassa conosce già il totale. Il dizionario va completato, perché
            manca il pepe nero e il prezzo del guanciale è quello della settimana scorsa. Alla fine
            `totale` vale 20.5 e `prodotti` elenca i cinque nomi, con `'pepe nero'` per ultimo.
        """,
        richiesta="""
            1. Aggiungi il pepe nero, con la chiave `"pepe nero"` e il prezzo di 2.15 euro, e correggi il
               prezzo del guanciale, che è di 7.90 euro.
            2. Calcola in `totale` la somma dei prezzi con `sum(prezzi.values())`; la funzione `sum()`
               restituisce la somma degli elementi che riceve.
            3. Salva in `prodotti` la lista dei nomi dei prodotti, cioè delle chiavi del dizionario.
        """,
        suggerimento=(
            "una chiave nuova e una chiave esistente si assegnano con la stessa sintassi, "
            "`prezzi[chiave] = valore`; nel primo caso Python crea la coppia, nel secondo sostituisce il "
            "valore. Le chiavi si ottengono con `list(prezzi.keys())`."
        ),
        starter="""
            prezzi = {"spaghetti": 2.58, "guanciale": 8.90, "uova": 3.49, "pecorino": 4.38}

            ...
            ...
            totale = ...
            prodotti = ...

            print(totale)
            print(prodotti)
        """,
        soluzione="""
            prezzi = {"spaghetti": 2.58, "guanciale": 8.90, "uova": 3.49, "pecorino": 4.38}

            prezzi["pepe nero"] = 2.15
            prezzi["guanciale"] = 7.90
            totale = sum(prezzi.values())
            prodotti = list(prezzi.keys())

            print(totale)    # Output: 20.5
            print(prodotti)  # Output: ['spaghetti', 'guanciale', 'uova', 'pecorino', 'pepe nero']
        """,
        verifica="""
            assert prezzi.get("pepe nero") == 2.15 and prezzi["guanciale"] == 7.90, "❌ prezzi: aggiungi il pepe nero e correggi il prezzo del guanciale"
            assert round(totale, 2) == 20.5, "❌ totale: somma i valori del dizionario aggiornato con sum(prezzi.values())"
            assert prodotti == ["spaghetti", "guanciale", "uova", "pecorino", "pepe nero"], "❌ prodotti: usa list(prezzi.keys())"
        """,
    )
    nb.esercizio(
        titolo="Due liste, un carrello",
        scenario="""
            Marta e Luca hanno scritto ciascuno la propria lista della spesa, e alcuni prodotti compaiono in
            entrambe. Vogliamo un unico carrello in cui ogni prodotto compaia una volta sola, senza cercare
            i doppioni a occhio, e l'indirizzo di Marta in una tupla, perché è un gruppo di valori che non
            cambia. Alla fine `carrello` contiene sei prodotti e `civico` vale 14.
        """,
        richiesta="""
            1. Unisci le due liste in `tutti` con l'operatore `+`, che tra due liste funziona come tra due
               stringhe e produce una lista nuova con gli elementi della prima seguiti da quelli della
               seconda.
            2. Salva in `carrello` il set ottenuto da `tutti` e in `quanti` il numero dei suoi prodotti.
            3. Crea la tupla `indirizzo` con `"via Garibaldi"`, `14` e `"Bologna"` e salva in `civico` il
               suo secondo elemento, letto con l'indice.
        """,
        suggerimento=(
            "l'unione delle due liste conserva i doppioni, ed è il passaggio a set che li elimina. Il "
            "secondo elemento della tupla ha indice 1, perché gli indici partono da zero."
        ),
        starter="""
            lista_marta = ["spaghetti", "guanciale", "uova", "vino"]
            lista_luca = ["vino", "pecorino", "pane", "uova"]

            tutti = ...
            carrello = ...
            quanti = ...

            indirizzo = ...
            civico = ...

            print(quanti, civico)
        """,
        soluzione="""
            lista_marta = ["spaghetti", "guanciale", "uova", "vino"]
            lista_luca = ["vino", "pecorino", "pane", "uova"]

            tutti = lista_marta + lista_luca
            carrello = set(tutti)
            quanti = len(carrello)

            indirizzo = ("via Garibaldi", 14, "Bologna")
            civico = indirizzo[1]

            print(quanti, civico)  # Output: 6 14
        """,
        verifica="""
            assert tutti == lista_marta + lista_luca, "❌ tutti: le due liste unite con +"
            assert carrello == {"spaghetti", "guanciale", "uova", "vino", "pecorino", "pane"} and quanti == 6, "❌ carrello: set(tutti) elimina i doppioni, quanti è la sua lunghezza"
            assert isinstance(indirizzo, tuple) and civico == 14, "❌ indirizzo deve essere una tupla e civico il suo elemento di indice 1"
        """,
    )
    return nb
