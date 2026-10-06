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
        intento="Eseguiamo codice solo a certe condizioni, ripetiamo operazioni con i cicli e raccogliamo il codice in funzioni.",
        obiettivi={
            "base": [
                "eseguire codice solo a certe condizioni con `if`, `else`, `and` e `or`",
                "ripetere un'operazione con `for` e `while`, anche con `.items()`, `enumerate`, `zip` e `range`",
                "definire funzioni con argomenti keyword e valori predefiniti",
            ],
            "avanzata": [
                "eseguire codice solo a certe condizioni e ripetere un'operazione con `for` e `while`",
                "definire funzioni con argomenti keyword e valori predefiniti",
                "scrivere in forma compatta con `lambda`, list comprehension, `map`, `filter` e generatori",
            ],
        },
        tempo={"base": 70, "avanzata": 80},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("La clausola if", intro="""
        La clausola `if` permette di eseguire un blocco di codice solo se una certa condizione è vera.

        ```python
        if condizione:
            # codice da eseguire se la condizione è vera
        ```
    """)
    nb.md("Una condizione è un'espressione che vale `True` o `False`: per esempio, se `x` è pari.")
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
    nb.md("Più condizioni si combinano con `and` (devono essere vere tutte) e `or` (basta che ne sia vera una).")
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
    nb.sottosezione("Il ciclo for", intro="Iterazione su una lista:")
    nb.code("""
        lista = [1, 2, 3, 4, 5]
        for elemento in lista:
            print(elemento)
    """)
    nb.md("Il ciclo `for` con una condizione `if`:")
    nb.code("""
        for num in lista:
            if num % 2 == 0:
                print(f"Il numero {num} è pari.")
            else:
                print(f"Il numero {num} è dispari.")
    """)
    nb.md("E se volessimo fare il ciclo solo su una parte degli elementi? Basta lo slicing della lista.")
    nb.code("""
        # ciclo su un sottoinsieme: un elemento sì e uno no, partendo dal secondo
        for num in lista[1::2]:
            if num % 2 == 0:
                print(f"Il numero {num} è pari.")
            else:
                print(f"Il numero {num} è dispari.")
    """)

    nb.sottosezione("Dizionari, enumerate e zip", intro="""
        Il metodo `.items()` restituisce tutte le coppie chiave-valore di un dizionario, come tuple.
    """)
    nb.code("""
        dizionario = {'nome': 'Marco', 'cognome': 'Rossi', 'età': 30}

        dizionario.items()
    """)
    nb.md("Usando `.items()` in un ciclo `for` iteriamo su tutte le coppie chiave-valore del dizionario:")
    nb.code("""
        for k, v in dizionario.items():
            print(k, ' : ', v)
    """)
    nb.md("""
        La funzione `enumerate()` permette di iterare su una lista mantenendo il conteggio degli elementi.
        Con `start=1` il conteggio parte da 1 invece che da 0.
    """)
    nb.code("""
        days = ['lunedì', 'martedì', 'mercoledì']

        for idx, day in enumerate(days, start=1):
            print(idx, day)
    """)
    nb.md("""
        La funzione `zip()` permette di iterare su due liste in parallelo, combinando i loro elementi in coppie.
        In questo esempio controlliamo il meteo per trovare i giorni di sole.
    """)
    nb.code("""
        days = ['lunedì', 'martedì', 'mercoledì']
        weather_list = ['sole', 'pioggia', 'sole']
        sunny_days = []

        for day, weather in zip(days, weather_list):
            if weather == 'sole':
                sunny_days.append(day)

        print(f'I giorni di sole sono stati: {sunny_days}')
    """)

    nb.sottosezione("Ripetere un'azione con range()", intro="""
        Con `range(n_iter)` eseguiamo un'azione un numero fissato di volte. In questo esempio stampiamo
        "ciao" 10 volte.
    """)
    nb.code("""
        n_iter = 10

        for i in range(n_iter):
            print('ciao')
    """)

    nb.sottosezione("Iterabili e iteratori", intro="""
        Un **iterabile** è qualsiasi oggetto che contiene una sequenza di elementi e che può essere percorso,
        come liste, stringhe e dizionari: ci permette di attraversare i suoi elementi uno alla volta in un
        ciclo `for`.
    """)
    nb.md("""
        Un **iteratore** è un oggetto che produce gli elementi di un iterabile uno alla volta. Python crea un
        iteratore ogni volta che si usa un ciclo `for`. Con `next()` l'iteratore restituisce l'elemento
        successivo; se non ci sono più elementi, solleva l'eccezione `StopIteration`.
    """)
    with nb.solo("avanzata"):
        nb.md("""
            Un **generatore** è una funzione che usa `yield` al posto di `return` (le funzioni le vediamo tra
            poco): produce i valori uno alla volta, solo quando servono, senza costruire tutta la lista. È un
            iteratore, quindi si percorre con `for` o con `next()`.
        """)
        nb.code("""
            def quadrati(n):
                for i in range(1, n + 1):
                    yield i ** 2

            gen = quadrati(3)
            print(next(gen), next(gen), next(gen))  # Output: 1 4 9
        """)

    nb.sottosezione("Il ciclo while", intro="Il ciclo `while` esegue il blocco di codice finché una condizione è vera:")
    nb.code("""
        x = 0
        while x < 5:
            print(x)
            x += 1
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Creare funzioni personalizzate", intro="""
        Le funzioni consentono di incapsulare codice riutilizzabile.

        ```python
        def nome_funzione(parametri):
            # corpo della funzione
            return risultato
        ```
    """)
    nb.code("""
        def somma(a, b):
            return a + b

        risultato = somma(2, 3)
        print(risultato)  # Output: 5
    """)
    nb.sottosezione("Argomenti keyword", intro="Possiamo passare gli argomenti indicando il nome dei parametri, in qualsiasi ordine:")
    nb.code("""
        def messaggio(nome, testo):
            print(f"Ciao {nome}, {testo}")

        messaggio(testo="come stai?", nome="Paolo")
        # Output: Ciao Paolo, come stai?
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Argomenti predefiniti", intro="Possiamo definire valori predefiniti per i parametri:")
    nb.code("""
        def saluta(nome="Marco"):
            print(f"Ciao {nome}")

        saluta()           # Output: Ciao Marco
        saluta("Paolo")    # Output: Ciao Paolo
    """)
    nb.md("""
        Riprendiamo il ciclo dei giorni di sole e lo raccogliamo in una funzione. Il parametro `annuncio`
        vale `False` se non lo indichiamo; con `annuncio=True` la funzione stampa anche un messaggio per
        ogni giorno di sole.
    """)
    nb.code('''
        def sunny_fun(days, weather_list, annuncio=False):
            """Restituisce i giorni di sole."""
            sunny_days = []
            for day, weather in zip(days, weather_list):
                if weather == 'sole':
                    if annuncio:
                        print(f'Oggi è {day} ed è soleggiato!')
                    sunny_days.append(day)

            return sunny_days
    ''')
    nb.code("""
        days = ['lunedì', 'martedì', 'mercoledì']
        weather_list = ['sole', 'pioggia', 'sole']

        sunny_fun(days, weather_list=weather_list, annuncio=True)
    """)

    # ------------------------------------------------------------------ 5 (A)
    with nb.solo("avanzata"):
        nb.sezione("Lambda, list comprehension, map e filter")
        nb.sottosezione("Funzioni lambda", intro="Le funzioni lambda sono funzioni anonime e compatte:")
        nb.code("""
            quadrato = lambda x: x ** 2
            print(quadrato(4))  # Output: 16
        """)
        nb.sottosezione("List comprehension", intro="Sintassi compatta per creare liste:")
        nb.code("""
            squares = [x ** 2 for x in range(1, 11)]
            print(squares)
        """)
        nb.sottosezione("La funzione map", intro="Applica una funzione a tutti gli elementi di una lista:")
        nb.code("""
            numbers = [1, 2, 3, 4, 5]
            squared_numbers = list(map(lambda x: x ** 2, numbers))
            print(squared_numbers)
        """)
        nb.sottosezione("La funzione filter", intro="Filtra gli elementi in base a una condizione:")
        nb.code("""
            even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
            print(even_numbers)
        """)
        nb.md("Questi strumenti permettono di scrivere codice più conciso.")

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Stringa invertita",
        scenario="",
        richiesta="""
            Scrivi una funzione `reverse_string` che prenda in input una stringa e restituisca la stringa
            invertita. Esempio: input `'Python'`, output `'nohtyP'`.
        """,
        suggerimento="puoi pensare alla stringa come a una **lista** di caratteri.",
        starter="""
            def reverse_string(stringa):
                return ...
        """,
        soluzione="""
            def reverse_string(stringa):
                return stringa[::-1]
        """,
        verifica="""
            assert reverse_string("Python") == "nohtyP", "❌ Stringa invertita errata"
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
            Scrivi una funzione `paesi_capitale_pari` che prenda in input un dizionario di paesi e capitali e
            restituisca la lista dei paesi la cui capitale ha un numero pari di lettere. Il dizionario
            `g10` è nella cella qui sotto.
        """,
        starter=unisci("""
            def paesi_capitale_pari(dizionario):
                result = ...  # inizializza una lista vuota
                for paese, capitale in ...:  # ciclo su chiave e valore (usa .items())
                    if ...:  # condizione: lunghezza pari del nome della capitale
                        ...  # aggiungi a result il paese, visto che la condizione è rispettata
                return result
        """, g10),
        soluzione=unisci("""
            def paesi_capitale_pari(dizionario):
                result = []
                for paese, capitale in dizionario.items():
                    if len(capitale) % 2 == 0:
                        result.append(paese)
                return result
        """, g10),
        verifica="""
            atteso = ['Canada', 'Francia', 'Italia', 'Regno Unito', 'Stati Uniti', 'Spagna']
            assert paesi_capitale_pari(g10) == atteso, "❌ Lista dei paesi errata"
        """,
    )

    richiesta_palindrome = """
        Scrivi una funzione `trova_palindrome` che prenda in input una lista di parole e restituisca una
        nuova lista contenente solo le parole palindrome. Esempio: input
        `['ciao', 'anna', 'radar', 'gatto', 'osso', 'madam']`, output `['anna', 'radar', 'osso', 'madam']`.
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
        suggerimento="una parola è palindroma se è uguale alla parola invertita, come nell'esercizio sulla stringa invertita.",
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
        richiesta=richiesta_palindrome,
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
