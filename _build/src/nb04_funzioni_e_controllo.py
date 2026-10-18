"""04 · Funzioni e controllo del flusso (dal notebook 03 del docente)."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="04",
        file="04_Funzioni_e_controllo",
        titolo="Funzioni e controllo del flusso",
        blocco=2,
        giornata=2,
        intento=(
            "Il notebook mostra come eseguire un blocco di codice solo quando una condizione è vera, come "
            "ripetere un'operazione con i cicli e come raccogliere il codice in funzioni riutilizzabili."
        ),
        obiettivi={
            "base": [
                "eseguire codice solo a certe condizioni con `if`, `else`, `and` e `or`",
                "ripetere un'operazione con `for`, anche con `.items()`, `enumerate`, `zip` e `range`",
                "definire funzioni con argomenti keyword e valori predefiniti",
            ],
            "avanzata": [
                "eseguire codice solo a certe condizioni e ripetere un'operazione con `for`",
                "definire funzioni con argomenti keyword e valori predefiniti",
                "scrivere in forma compatta con `lambda` e list comprehension",
            ],
        },
        tempo={"base": 50, "avanzata": 50},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("La clausola if", intro="""
        La clausola `if` permette di eseguire un blocco di codice solo se una certa condizione è vera.
        La condizione si scrive dopo la parola chiave `if` ed è seguita dai due punti, mentre il blocco
        da eseguire va sulle righe successive, indentato di quattro spazi:

        ```python
        if condizione:
            # codice da eseguire se la condizione è vera
        ```
    """)
    nb.md("""
        Una condizione è un'espressione che ha come risultato `True` oppure `False`. Nella prima cella qui
        sotto controlliamo se `x` è pari, cioè se il resto della divisione per 2, calcolato con
        l'operatore `%`, è uguale a zero. Nella seconda usiamo lo stesso confronto come condizione di un
        `if`, che stampa il messaggio solo quando il numero è pari.
    """)
    nb.code("""
        x = 4
        x % 2 == 0
    """)
    nb.code("""
        condizione_pari = x % 2 == 0

        if condizione_pari:
            print('numero pari!')
    """)
    nb.md("""
        Con `else` specifichiamo un blocco di codice alternativo, eseguito quando la condizione è falsa:

        ```python
        if condizione:
            # codice se la condizione è vera
        else:
            # codice se la condizione è falsa
        ```

        Nell'esempio che segue `x` vale 1, quindi la condizione `x > 5` è falsa e Python esegue il
        blocco sotto `else`.
    """)
    nb.code("""
        # esempio 1: clausola if semplice
        x = 1
        if x > 5:
            print("x è maggiore di 5")
        else:
            print("x è minore o uguale a 5")
    """)
    nb.md("""
        È possibile annidare più clausole `if` per gestire condizioni più complesse:

        ```python
        if condizione1:
            if condizione2:
                # codice se entrambe le condizioni sono vere
            else:
                # codice se condizione1 è vera ma condizione2 è falsa
        else:
            # codice se condizione1 è falsa
        ```

        Nell'esempio seguente il secondo `if` viene valutato solo perché il primo è vero: con `x` uguale
        a 9 sono vere entrambe le condizioni e il messaggio viene stampato.
    """)
    nb.code("""
        # esempio 2: clausola if annidata
        x = 9
        if x > 5:
            if x > 8:
                print("x è maggiore di 5 e anche maggiore di 8")
        else:
            print("x è minore o uguale a 5")
    """)
    nb.md("""
        Più condizioni si combinano con gli operatori `and` e `or`. Un'espressione costruita con `and` è
        vera solo se sono vere tutte le condizioni, mentre con `or` basta che ne sia vera una, ed è per
        questo che `True or False` vale `True`. Nella seconda cella le due condizioni su `x` e su `y` sono
        entrambe vere, quindi viene eseguito il primo blocco.
    """)
    nb.code("""
        True or False
    """)
    nb.code("""
        # esempio 3: clausola if con più condizioni
        x = 10
        y = 12
        if x > 5 and y > 10:
            print("x è maggiore di 5 e y è maggiore di 10")
        else:
            print("Almeno una delle due condizioni non è soddisfatta")
    """)
    nb.hands_on(
        richiesta="""
            Il biglietto del museo è ridotto per chi ha meno di 26 anni oppure almeno 65: completa la condizione
            con `or` e il ramo `else`, che assegna `"intero"`. Con `eta = 40` la variabile `biglietto` deve valere
            `"intero"`.
        """,
        starter="""
            eta = 40
            if eta < 26 or ...:
                biglietto = "ridotto"
            else:
                biglietto = ...
            print(biglietto)
        """,
        soluzione="""
            eta = 40
            if eta < 26 or eta >= 65:
                biglietto = "ridotto"
            else:
                biglietto = "intero"
            print(biglietto)
        """,
        verifica="""
            assert biglietto == "intero", "❌ con 40 anni il biglietto è intero: la seconda condizione è eta >= 65 e il ramo else assegna 'intero'"
        """,
        prova_anche='con `eta = 70`, che deve dare `"ridotto"`.',
    )

    # ------------------------------------------------------------------ 2
    nb.sezione("Cicli su serie di dati", intro="""
        I cicli permettono di eseguire un blocco di codice ripetutamente sugli elementi di una sequenza,
        come liste o tuple.
    """)
    nb.sottosezione("Il ciclo for", intro="""
        Il ciclo `for` prende uno dopo l'altro gli elementi di una sequenza e, per ciascuno, esegue il
        blocco indentato che segue. A ogni passo la variabile scritta dopo `for`, in questo caso
        `elemento`, contiene l'elemento corrente. Nell'esempio iteriamo su una lista di cinque numeri e
        li stampiamo.
    """)
    nb.code("""
        lista = [1, 2, 3, 4, 5]
        for elemento in lista:
            print(elemento)
    """)
    nb.md("""
        All'interno del ciclo possiamo usare una clausola `if`, che viene valutata di nuovo a ogni
        iterazione. Nella cella seguente, per ogni numero della lista, stampiamo se è pari o dispari.
    """)
    nb.code("""
        for num in lista:
            if num % 2 == 0:
                print(f"Il numero {num} è pari.")
            else:
                print(f"Il numero {num} è dispari.")
    """)
    nb.hands_on(
        richiesta="""
            Il ciclo qui sotto conta i voti maggiori di 25, aumentando di uno la variabile `sopra_25` ogni volta
            che la condizione dell'`if` è vera. Completa la condizione: i voti sopra il 25 sono tre.
        """,
        starter="""
            voti = [18, 24, 30, 27, 21, 28]
            sopra_25 = 0

            for voto in voti:
                if ...:
                    sopra_25 = sopra_25 + 1

            print(sopra_25)
        """,
        soluzione="""
            voti = [18, 24, 30, 27, 21, 28]
            sopra_25 = 0

            for voto in voti:
                if voto > 25:
                    sopra_25 = sopra_25 + 1

            print(sopra_25)
        """,
        verifica="""
            assert sopra_25 == 3, "❌ sopra_25: i voti maggiori di 25 sono 30, 27 e 28"
        """,
        prova_anche="con i voti maggiori o uguali a 24, che sono quattro.",
    )
    nb.md("""
        Per iterare solo su una parte degli elementi si applica lo slicing alla lista prima del ciclo.
        Nell'esempio qui sotto `lista[1::2]` prende un elemento ogni due a partire dal secondo, quindi il
        ciclo considera soltanto i numeri 2 e 4.
    """)
    nb.code("""
        # ciclo su un sottoinsieme: un elemento sì e uno no, partendo dal secondo
        for num in lista[1::2]:
            if num % 2 == 0:
                print(f"Il numero {num} è pari.")
            else:
                print(f"Il numero {num} è dispari.")
    """)

    nb.sottosezione("Dizionari, enumerate e zip", intro="""
        Il metodo `.items()` restituisce tutte le coppie chiave-valore di un dizionario, ciascuna sotto
        forma di tupla. È il modo abituale di percorrere un dizionario con un ciclo, perché fornisce a ogni
        passo la chiave e il valore insieme.
    """)
    nb.code("""
        dizionario = {'nome': 'Marco', 'cognome': 'Rossi', 'età': 30}

        dizionario.items()
    """)
    nb.md("""
        Usando `.items()` in un ciclo `for` iteriamo su tutte le coppie chiave-valore del dizionario.
        Poiché ogni coppia è una tupla di due elementi, dopo `for` possiamo scrivere due variabili, qui
        `k` per la chiave e `v` per il valore, che Python assegna a ogni passo.
    """)
    nb.code("""
        for k, v in dizionario.items():
            print(k, ' : ', v)
    """)
    nb.hands_on(
        richiesta="""
            Completa il ciclo `for` sulle coppie del dizionario `prezzi`, con le variabili `prodotto` e `prezzo`,
            in modo che a ogni passo aggiunga a `righe` una stringa come `"pane: 2.5 euro"`. Alla fine `righe`
            contiene tre stringhe, una per prodotto.
        """,
        starter="""
            prezzi = {"pane": 2.5, "latte": 1.2, "caffè": 3.8}
            righe = []

            for ... in ...:
                righe.append(f"{prodotto}: {prezzo} euro")

            print(righe)
        """,
        soluzione="""
            prezzi = {"pane": 2.5, "latte": 1.2, "caffè": 3.8}
            righe = []

            for prodotto, prezzo in prezzi.items():
                righe.append(f"{prodotto}: {prezzo} euro")

            print(righe)
        """,
        verifica="""
            assert righe == ["pane: 2.5 euro", "latte: 1.2 euro", "caffè: 3.8 euro"], "❌ righe: il ciclo va su prezzi.items(), con prodotto e prezzo"
        """,
    )
    nb.md("""
        La funzione `enumerate()` permette di iterare su una lista mantenendo il conteggio degli elementi.
        A ogni passo il ciclo riceve una coppia formata dal numero d'ordine e dall'elemento, e con
        `start=1` il conteggio parte da 1 invece che da 0.
    """)
    nb.code("""
        giorni = ['lunedì', 'martedì', 'mercoledì']

        for idx, giorno in enumerate(giorni, start=1):
            print(idx, giorno)
    """)
    nb.md("""
        La funzione `zip()` permette di iterare su due liste in parallelo, combinando i loro elementi in coppie.
        In questo esempio controlliamo il meteo per trovare i giorni di sole: a ogni passo `giorno` e
        `meteo` contengono gli elementi che stanno nella stessa posizione delle due liste, e i giorni di
        sole vengono aggiunti con `append()` alla lista `giorni_di_sole`.
    """)
    nb.code("""
        giorni = ['lunedì', 'martedì', 'mercoledì']
        lista_meteo = ['sole', 'pioggia', 'sole']
        giorni_di_sole = []

        for giorno, meteo in zip(giorni, lista_meteo):
            if meteo == 'sole':
                giorni_di_sole.append(giorno)

        print(f'I giorni di sole sono stati: {giorni_di_sole}')
    """)

    nb.sottosezione("Ripetere un'azione con range()", intro="""
        La funzione `range(n)` produce i numeri interi da 0 a `n - 1`, quindi un ciclo `for` su
        `range(n_iter)` esegue il suo blocco esattamente `n_iter` volte. In questo esempio stampiamo
        "ciao" 10 volte; la variabile `i` contiene il numero del passo, anche se qui non la usiamo.
    """)
    nb.code("""
        n_iter = 10

        for i in range(n_iter):
            print('ciao')
    """)

    nb.sottosezione("Iterabili e iteratori", intro="""
        Un **iterabile** è qualsiasi oggetto che contiene una sequenza di elementi e che può essere
        percorso, come le liste, le stringhe e i dizionari; si chiama così perché permette di attraversare
        i suoi elementi uno alla volta in un ciclo `for`. Un **iteratore** è invece l'oggetto che produce
        quegli elementi uno alla volta, e Python ne crea uno ogni volta che si usa un ciclo `for`. Con
        `next()` l'iteratore restituisce l'elemento successivo; se non ci sono più elementi, solleva
        l'eccezione `StopIteration`, che il ciclo `for` interpreta come il segnale di fermarsi.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Creare funzioni personalizzate", intro="""
        Le funzioni consentono di incapsulare codice riutilizzabile, che si scrive una volta e si
        richiama ogni volta che serve, anche con argomenti diversi. Una funzione si definisce con `def`,
        seguito dal nome e dai parametri tra parentesi; il corpo è indentato e l'istruzione `return`
        restituisce il risultato a chi ha chiamato la funzione:

        ```python
        def nome_funzione(parametri):
            # corpo della funzione
            return risultato
        ```

        Nell'esempio la funzione `somma` riceve due numeri e restituisce la loro somma, che salviamo
        nella variabile `risultato`.
    """)
    nb.code("""
        def somma(a, b):
            return a + b

        risultato = somma(2, 3)
        print(risultato)  # Output: 5
    """)
    nb.sottosezione("Argomenti keyword", intro="""
        Quando chiamiamo una funzione possiamo passare gli argomenti indicando il nome dei parametri, e in
        questo caso l'ordine in cui li scriviamo non conta. Gli argomenti passati per nome, detti
        argomenti keyword, rendono anche la chiamata più leggibile, perché chi legge vede subito a quale
        parametro va ciascun valore.
    """)
    nb.code("""
        def messaggio(nome, testo):
            print(f"Ciao {nome}, {testo}")

        messaggio(testo="come stai?", nome="Paolo")
        # Output: Ciao Paolo, come stai?
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Argomenti predefiniti", intro="""
        Possiamo definire valori predefiniti per i parametri, scrivendo il valore dopo il nome del
        parametro nella definizione della funzione. Se nella chiamata l'argomento manca, Python usa il
        valore predefinito; se invece lo passiamo, il valore passato prende il suo posto.
    """)
    nb.code("""
        def saluta(nome="Marco"):
            print(f"Ciao {nome}")

        saluta()           # Output: Ciao Marco
        saluta("Paolo")    # Output: Ciao Paolo
    """)
    nb.md("""
        Riprendiamo il ciclo dei giorni di sole della sezione precedente e lo raccogliamo in una funzione.
        Il parametro `annuncio` vale `False` se non lo indichiamo, mentre con `annuncio=True` la funzione
        stampa anche un messaggio per ogni giorno di sole. Nella seconda cella chiamiamo la funzione con
        le stesse liste di prima.
    """)
    nb.code('''
        def conta_giorni_di_sole(giorni, lista_meteo, annuncio=False):
            """Restituisce i giorni di sole."""
            giorni_di_sole = []
            for giorno, meteo in zip(giorni, lista_meteo):
                if meteo == 'sole':
                    if annuncio:
                        print(f'Oggi è {giorno} ed è soleggiato!')
                    giorni_di_sole.append(giorno)

            return giorni_di_sole
    ''')
    nb.code("""
        giorni = ['lunedì', 'martedì', 'mercoledì']
        lista_meteo = ['sole', 'pioggia', 'sole']

        conta_giorni_di_sole(giorni, lista_meteo=lista_meteo, annuncio=True)
    """)
    nb.hands_on(
        richiesta="""
            Chiama `conta_giorni_di_sole` sulle due liste della cella qui sotto, la prima volta senza indicare
            `annuncio` e la seconda con `annuncio=True`, e salva i risultati in `senza_annuncio` e `con_annuncio`.
            Solo la seconda chiamata stampa i messaggi, e tutte e due restituiscono `['venerdì', 'sabato']`.
        """,
        starter="""
            giorni = ['giovedì', 'venerdì', 'sabato', 'domenica']
            lista_meteo = ['pioggia', 'sole', 'sole', 'nuvole']

            senza_annuncio = ...
            con_annuncio = ...
        """,
        soluzione="""
            giorni = ['giovedì', 'venerdì', 'sabato', 'domenica']
            lista_meteo = ['pioggia', 'sole', 'sole', 'nuvole']

            senza_annuncio = conta_giorni_di_sole(giorni, lista_meteo)
            con_annuncio = conta_giorni_di_sole(giorni, lista_meteo, annuncio=True)
        """,
        verifica="""
            assert senza_annuncio == ['venerdì', 'sabato'], "❌ senza_annuncio: chiama la funzione con le due liste, senza annuncio"
            assert con_annuncio == ['venerdì', 'sabato'], "❌ con_annuncio: la stessa chiamata con annuncio=True"
        """,
    )

    # ------------------------------------------------------------------ 5 (A)
    with nb.solo("avanzata"):
        nb.sezione("Lambda e list comprehension")
        nb.sottosezione("Funzioni lambda", intro="""
            Le funzioni lambda sono funzioni anonime e compatte, che si scrivono su una sola riga con la
            parola chiave `lambda`, seguita dai parametri, dai due punti e dall'espressione da restituire.
            Si usano per funzioni molto brevi, quando definirne una con `def` sarebbe eccessivo;
            nell'esempio la assegniamo a una variabile solo per poterla chiamare.
        """)
        nb.code("""
            quadrato = lambda x: x ** 2
            print(quadrato(4))  # Output: 16
        """)
        nb.sottosezione("List comprehension", intro="""
            La list comprehension è una sintassi compatta per creare una lista a partire da un'altra
            sequenza. Tra parentesi quadre si scrive l'espressione che calcola ogni elemento, seguita da un
            `for` che indica su che cosa iterare. L'esempio costruisce la lista dei quadrati dei numeri da
            1 a 10, che con un ciclo `for` e `append()` richiederebbe tre righe.
        """)
        nb.code("""
            lista_quadrati = [x ** 2 for x in range(1, 11)]
            print(lista_quadrati)
        """)
        nb.hands_on(
            richiesta="""
                Il ciclo nella cella qui sotto costruisce con `append()` la lista delle lunghezze delle parole.
                Riscrivilo come list comprehension in una riga sola, assegnata a `lunghezze_compatte`, che deve
                valere `[4, 7, 4]` come la lista del ciclo.
            """,
            starter="""
                parole = ["sole", "pioggia", "neve"]

                lunghezze = []
                for parola in parole:
                    lunghezze.append(len(parola))

                lunghezze_compatte = [...]
                print(lunghezze, lunghezze_compatte)
            """,
            soluzione="""
                parole = ["sole", "pioggia", "neve"]

                lunghezze = []
                for parola in parole:
                    lunghezze.append(len(parola))

                lunghezze_compatte = [len(parola) for parola in parole]
                print(lunghezze, lunghezze_compatte)
            """,
            verifica="""
                assert lunghezze_compatte == [4, 7, 4], "❌ lunghezze_compatte: [len(parola) for parola in parole]"
            """,
            prova_anche='con la parola `"grandine"` aggiunta alla lista `parole`.',
        )
        nb.md("""
            Una list comprehension può contenere anche una condizione, scritta in fondo con `if`, per
            tenere solo alcuni elementi: `[x for x in lista if x % 2 == 0]`, per esempio, contiene soltanto
            i numeri pari. Lambda e list comprehension permettono di scrivere codice più conciso, ma
            conviene usarle solo finché l'espressione resta breve; quando servono più condizioni, un ciclo
            `for` esplicito è di solito più chiaro.
        """)

    # ------------------------------------------------------------------ Extra
    nb.sezione("Extra", intro="""
        Questa sezione raccoglie due esercizi brevi sui punti principali del notebook, i cicli con una condizione
        e le funzioni con un valore predefinito, da fare a casa per ripassare. Durante la lezione la saltiamo, e
        ogni esercizio ha la sua verifica, che conferma il risultato o dice che cosa controllare.
    """)

    # 4.1 · ciclo con if su .items() (comprehension in Avanzata)
    scenario_1 = """
        A fine febbraio vogliamo sapere in quali categorie abbiamo speso più di 100 euro e quanto abbiamo speso in
        tutto il mese. Le spese stanno in un dizionario con la categoria come chiave, e conviene scorrerlo con il
        codice invece di cercare a occhio, perché la stessa cella funziona con otto categorie come con ottanta e,
        se cambiamo il limite, basta modificare un numero. Le categorie sopra i 100 euro sono tre, alimentari,
        ristoranti e regali, su 805.8 euro di spese totali.
    """
    starter_1 = """
        spese_febbraio = {
            "alimentari": 312.4,
            "trasporti": 86.5,
            "ristoranti": 145.0,
            "abbigliamento": 59.9,
            "sport": 40.0,
            "libri": 23.7,
            "farmacia": 18.3,
            "regali": 120.0,
        }
        soglia = 100

        sopra_soglia = ...
        totale = ...
        print(f"{len(sopra_soglia)} categorie sopra i {soglia} euro, su {totale:.1f} euro di spese")
    """
    starter_1_base = starter_1.replace("""
        sopra_soglia = ...
        totale = ...
        """, """
        sopra_soglia = []
        for categoria, spesa in ...:
            ...
        totale = ...
        """)
    verifica_1 = """
        assert sopra_soglia == ["alimentari", "ristoranti", "regali"], "❌ sopra_soglia: le tre categorie con più di 100 euro"
        assert round(totale, 1) == 805.8, "❌ totale: la somma di tutti i valori del dizionario"
    """
    nb.esercizio(
        aula="base",
        titolo="Le categorie sopra soglia",
        scenario=scenario_1,
        richiesta="""
            1. Con un ciclo `for` su `spese_febbraio.items()`, che a ogni passo fornisce una categoria e la sua
               spesa, e un `if` che confronta la spesa con `soglia`, aggiungi alla lista `sopra_soglia` le
               categorie che la superano.
            2. Calcola in `totale` la somma di tutte le spese del dizionario.
        """,
        suggerimenti=[
            """
                Il ciclo passa su ogni coppia di categoria e spesa, e dentro il ciclo una condizione decide se
                aggiungere la categoria alla lista; il totale non ha bisogno del ciclo.
            """,
            """
                Dentro il ciclo servono `if spesa > soglia:` e poi `sopra_soglia.append(categoria)`, mentre per il
                totale basta applicare `sum()` ai `.values()` del dizionario.
            """,
        ],
        starter=starter_1_base,
        soluzione=starter_1_base.replace("""
        for categoria, spesa in ...:
            ...
        totale = ...
        """, """
        for categoria, spesa in spese_febbraio.items():
            if spesa > soglia:
                sopra_soglia.append(categoria)
        totale = sum(spese_febbraio.values())
        """),
        verifica=verifica_1,
        perche="""
            Il ciclo scorre `.items()` perché a ogni passo servono sia la chiave sia il valore, cioè la categoria
            da aggiungere alla lista e la spesa da confrontare con la soglia. Il totale non richiede un ciclo, dato
            che `sum()` lavora direttamente sui valori del dizionario.
        """,
    )
    nb.esercizio(
        aula="avanzata",
        titolo="Le categorie sopra soglia",
        scenario=scenario_1,
        richiesta="""
            1. Costruisci la lista `sopra_soglia` con una list comprehension su `spese_febbraio.items()`, che tiene
               le categorie con una spesa maggiore di `soglia`.
            2. Calcola in `totale` la somma di tutte le spese del dizionario.
        """,
        suggerimenti=[
            """
                La forma è `[categoria for categoria, spesa in ... if ...]`, con la condizione in fondo, mentre per
                il totale basta applicare `sum()` ai `.values()` del dizionario.
            """,
        ],
        starter=starter_1,
        soluzione=starter_1.replace("""
        sopra_soglia = ...
        totale = ...
        """, """
        sopra_soglia = [categoria for categoria, spesa in spese_febbraio.items() if spesa > soglia]
        totale = sum(spese_febbraio.values())
        """),
        verifica=verifica_1,
        perche="""
            La list comprehension esprime in una riga lo stesso ciclo con `append()` della versione estesa. Con una
            sola condizione resta facile da leggere, mentre con più condizioni o con calcoli intermedi conviene
            tornare al ciclo `for`.
        """,
    )

    # 4.2 · funzione con valore predefinito e docstring (un parametro in più in Avanzata)
    scenario_2 = """
        Il bike sharing della città costa 0.25 euro al minuto, mentre con l'abbonamento mensile la tariffa scende
        a 0.19 euro. Invece di rifare il conto a ogni corsa, scriviamo una funzione `costo` che riceve i minuti e
        la tariffa, con 0.25 come valore predefinito, e restituisce l'importo arrotondato al centesimo. In questo
        modo per una corsa normale basta passare i minuti, mentre con l'abbonamento si aggiunge la tariffa nella
        chiamata: una corsa di 18 minuti costa 4.5 euro, una di 42 minuti in abbonamento 7.98 euro.
    """
    suggerimenti_2 = [
        """
            La funzione riceve i minuti e una tariffa con valore predefinito, calcola il prodotto, lo arrotonda e
            lo restituisce.
        """,
        """
            `return` restituisce il valore a chi chiama la funzione, mentre `print` si limita a mostrarlo; la
            verifica ha bisogno del valore restituito.
        """,
    ]
    nb.esercizio(
        aula="base",
        titolo="Il costo di una corsa come funzione",
        scenario=scenario_2,
        richiesta="""
            1. Scrivi la funzione `costo(minuti, tariffa=0.25)`, che restituisce con `return` i minuti moltiplicati
               per la tariffa, arrotondati a due decimali con `round()` perché l'importo è in euro e centesimi.
            2. Sotto il `def` aggiungi una docstring di una riga, che chi riprende la funzione potrà leggere con
               `help(costo)` per sapere che cosa calcola.
            3. Usala per calcolare `costo_breve`, il costo di una corsa di 18 minuti alla tariffa normale, e
               `costo_abbonato`, il costo di una corsa di 42 minuti con l'abbonamento. Nella seconda chiamata
               scrivi `tariffa=0.19`, in modo che chi la rilegge capisca subito che quel numero è una tariffa.

            Alla fine `costo_breve` vale 4.5 e `costo_abbonato` vale 7.98.
        """,
        suggerimenti=suggerimenti_2,
        starter="""
            def costo(minuti, tariffa=0.25):
                ...


            costo_breve = ...
            costo_abbonato = ...
            print(f"Corsa breve: {costo_breve} euro, corsa in abbonamento: {costo_abbonato} euro")
        """,
        soluzione='''
            def costo(minuti, tariffa=0.25):
                """Costo in euro di una corsa in bike sharing, arrotondato ai centesimi."""
                return round(minuti * tariffa, 2)


            costo_breve = costo(18)
            costo_abbonato = costo(42, tariffa=0.19)
            print(f"Corsa breve: {costo_breve} euro, corsa in abbonamento: {costo_abbonato} euro")
        ''',
        verifica="""
            assert costo(100) == 25.0, "❌ costo(100) deve dare 25.0: la tariffa predefinita è 0.25"
            assert costo(100, tariffa=0.19) == 19.0, "❌ costo(100, tariffa=0.19) deve dare 19.0: usa la tariffa ricevuta"
            assert costo_abbonato == 7.98, "❌ costo_abbonato: 42 minuti a 0.19 euro al minuto"
        """,
        perche="""
            Con la tariffa normale come valore predefinito, la maggior parte delle chiamate passa soltanto i
            minuti, e se la tariffa cambia basta modificare la definizione della funzione. Anche l'arrotondamento
            sta dentro la funzione, così non occorre ripeterlo a ogni chiamata.
        """,
    )
    nb.esercizio(
        aula="avanzata",
        titolo="Il costo di una corsa come funzione",
        scenario=scenario_2,
        richiesta="""
            1. Le bici elettriche hanno anche un costo di sblocco a ogni corsa, quindi scrivi la funzione
               `costo(minuti, tariffa=0.25, sblocco=0.0)`, che restituisce con `return` i minuti per la tariffa
               più lo sblocco, arrotondati al centesimo.
            2. Aggiungi una docstring di una riga, che chi riprende la funzione potrà leggere con `help(costo)`.
            3. Usala per tre corse, passando per nome gli argomenti diversi dai minuti, in modo che in ogni
               chiamata si legga quale valore cambia: `costo_breve` per 18 minuti con i valori predefiniti,
               `costo_abbonato` per 42 minuti a 0.19 euro al minuto e `costo_elettrica` per 35 minuti su una bici
               elettrica, con 1 euro di sblocco.

            Alla fine `costo_breve` vale 4.5, `costo_abbonato` 7.98 e `costo_elettrica` 9.75.
        """,
        suggerimenti=suggerimenti_2[1:],
        starter="""
            def costo(minuti, tariffa=0.25, sblocco=0.0):
                ...


            costo_breve = ...
            costo_abbonato = ...
            costo_elettrica = ...
            print(f"Breve: {costo_breve} euro, abbonato: {costo_abbonato} euro, elettrica: {costo_elettrica} euro")
        """,
        soluzione='''
            def costo(minuti, tariffa=0.25, sblocco=0.0):
                """Costo in euro di una corsa in bike sharing, più lo sblocco, arrotondato ai centesimi."""
                return round(minuti * tariffa + sblocco, 2)


            costo_breve = costo(18)
            costo_abbonato = costo(42, tariffa=0.19)
            costo_elettrica = costo(35, sblocco=1)
            print(f"Breve: {costo_breve} euro, abbonato: {costo_abbonato} euro, elettrica: {costo_elettrica} euro")
        ''',
        verifica="""
            assert costo(100) == 25.0, "❌ costo(100) deve dare 25.0: la tariffa predefinita è 0.25 e lo sblocco 0"
            assert costo(100, tariffa=0.19, sblocco=1) == 20.0, "❌ costo(100, tariffa=0.19, sblocco=1) deve dare 20.0"
            assert costo_elettrica == 9.75, "❌ costo_elettrica: 35 minuti alla tariffa predefinita, più 1 euro"
        """,
        perche="""
            Quando una funzione ha due parametri con un valore predefinito, passare gli argomenti per nome rende
            esplicito quale dei due stiamo cambiando. Nella chiamata `costo(35, sblocco=1)`, per esempio, la
            tariffa resta quella normale e cambia solo lo sblocco, mentre scrivendo `costo(35, 1)` l'1 finirebbe
            nel parametro `tariffa`.
        """,
    )
    return nb
