"""04 · Funzioni e controllo del flusso (dal notebook 03 del docente)."""

import textwrap

from nbkit import Notebook


def unisci(*pezzi: str) -> str:
    """Unisce più blocchi di codice in una cella, con una riga vuota tra l'uno e l'altro."""
    return "\n\n".join(textwrap.dedent(p).strip() for p in pezzi)


def costruisci() -> Notebook:
    nb = Notebook(
        num="04",
        file="04_Funzioni_e_controllo",
        titolo="Funzioni e controllo del flusso",
        blocco=2,
        giornata=1,
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
        tempo={"base": 55, "avanzata": 60},
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
        nb.md("""
            Una list comprehension può contenere anche una condizione, scritta in fondo con `if`, per
            tenere solo alcuni elementi: `[x for x in lista if x % 2 == 0]`, per esempio, contiene soltanto
            i numeri pari. Lambda e list comprehension permettono di scrivere codice più conciso, ma
            conviene usarle solo finché l'espressione resta breve; quando servono più condizioni, un ciclo
            `for` esplicito è di solito più chiaro.
        """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Stringa invertita",
        scenario="",
        richiesta="""
            Scrivi una funzione `inverti_stringa` che riceva una stringa e restituisca la stessa stringa
            con i caratteri in ordine inverso. Per esempio, `inverti_stringa('Python')` deve restituire
            `'nohtyP'`.
        """,
        suggerimento="puoi pensare alla stringa come a una **lista** di caratteri.",
        starter="""
            def inverti_stringa(stringa):
                return ...
        """,
        soluzione="""
            def inverti_stringa(stringa):
                return stringa[::-1]
        """,
        verifica="""
            assert inverti_stringa("Python") == "nohtyP", "❌ Stringa invertita errata"
        """,
    )

    g10 = """
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
    nb.esercizio(
        titolo="Paesi con capitale di lunghezza pari",
        scenario="",
        richiesta="""
            Scrivi una funzione `paesi_capitale_pari` che riceva un dizionario di paesi e capitali e
            restituisca la lista dei paesi la cui capitale ha un numero pari di lettere. Il dizionario
            `g10`, che associa dieci paesi alle loro capitali, è già definito nella cella qui sotto, dopo
            la funzione da completare. Per esempio, `'Roma'` ha quattro lettere, quindi `'Italia'` fa parte
            del risultato.
        """,
        starter=unisci("""
            def paesi_capitale_pari(dizionario):
                risultato = ...  # inizializza una lista vuota
                for paese, capitale in ...:  # ciclo su chiave e valore (usa .items())
                    if ...:  # condizione: lunghezza pari del nome della capitale
                        ...  # aggiungi a risultato il paese, visto che la condizione è rispettata
                return risultato
        """, g10),
        soluzione=unisci("""
            def paesi_capitale_pari(dizionario):
                risultato = []
                for paese, capitale in dizionario.items():
                    if len(capitale) % 2 == 0:
                        risultato.append(paese)
                return risultato
        """, g10),
        verifica="""
            atteso = ['Canada', 'Francia', 'Italia', 'Regno Unito', 'Stati Uniti', 'Spagna']
            assert paesi_capitale_pari(g10) == atteso, "❌ Lista dei paesi errata"
        """,
    )

    richiesta_palindrome = """
        Scrivi una funzione `trova_palindrome` che riceva una lista di parole e restituisca una nuova
        lista con le sole parole palindrome, cioè quelle che si leggono allo stesso modo nei due sensi.
        Per esempio, con la lista `['ciao', 'anna', 'radar', 'gatto', 'osso', 'madam']` la funzione deve
        restituire `['anna', 'radar', 'osso', 'madam']`.
    """
    test_palindrome = """
        # test
        lista_parole = ['ciao', 'anna', 'radar', 'gatto', 'osso', 'madam']
        print(trova_palindrome(lista_parole))
    """
    verifica_palindrome = """
        assert trova_palindrome(lista_parole) == ['anna', 'radar', 'osso', 'madam'], "❌ Lista delle parole palindrome errata"
    """
    nb.esercizio(
        aula="base",
        titolo="Parole palindrome",
        scenario="",
        richiesta=richiesta_palindrome,
        suggerimento="una parola è palindroma se è uguale a sé stessa invertita, e per invertirla puoi usare lo stesso procedimento dell'esercizio sulla stringa invertita.",
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
        verifica=verifica_palindrome,
    )
    nb.esercizio(
        aula="avanzata",
        titolo="Parole palindrome",
        scenario="",
        richiesta=richiesta_palindrome.rstrip() + """
        Il corpo della funzione è una sola list comprehension con una condizione, come nella cella di
        partenza.
    """,
        starter=unisci("""
            def trova_palindrome(lista_parole):
                return [... for ... if ...]  # completa la condizione parola == parola invertita
        """, test_palindrome),
        soluzione=unisci("""
            def trova_palindrome(lista_parole):
                return [parola for parola in lista_parole if parola == parola[::-1]]
        """, test_palindrome),
        verifica=verifica_palindrome,
    )
    return nb
