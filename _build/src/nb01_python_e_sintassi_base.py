"""01 · Introduzione a Python e sintassi base."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="01",
        file="01_Python_e_sintassi_base",
        titolo="Introduzione a Python e sintassi base",
        blocco=1,
        giornata=1,
        intento="Le basi di Python: come si scrive il codice, come si lavora con i numeri e con le stringhe.",
        obiettivi=[
            "riconoscere l'indentazione, le variabili e l'`import` di una libreria",
            "fare calcoli con gli operatori aritmetici e il modulo `math`",
            "costruire stringhe con la concatenazione, `.format()` e le f-string",
        ],
        tempo={"base": 45, "avanzata": 35},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Cos'è Python", intro="""
        Python è un linguaggio di programmazione molto diffuso, usato nello sviluppo web, nella scienza
        dei dati, nell'Intelligenza Artificiale e nel Machine Learning, e per lo scripting.
    """)
    nb.md("""
        Si dice che Python arrivi **"con le batterie incluse"**: ha una libreria di base completa. Ed
        essendo molto usato, ci sono moltissime librerie e framework di qualità per svolgere compiti in
        modo rapido.

        [Sito ufficiale di Python](https://www.python.org/)
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Caratteristiche principali", intro="""
        - **Leggibilità del codice**
        - **Sintassi semplice e pulita**
        - **Interpretato**, non compilato
        - **Gestione automatica della memoria**
        - Linguaggio **multi-paradigma** (procedurale, ad oggetti e funzionale)
        - Ampia **libreria standard**
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Sintassi di base")
    nb.sottosezione("Indentazione", intro="""
        In Python l'indentazione definisce i blocchi di codice: non ci sono parentesi graffe o altri
        segni per separare le istruzioni.
    """)
    nb.code("""
        if 3 == 3:
            print("Questo è un output")
    """)

    nb.sottosezione("Variabili", intro="""
        In Python non serve specificare il tipo di una variabile quando la dichiariamo: il tipo viene
        dal valore assegnato.
    """)
    nb.code("""
        x = 42        # x è un intero (int)
        y = 3.14      # y è un numero con la virgola mobile (float)
        z = "Hello"   # z è una stringa (str)

        print(type(x))  # Output: <class 'int'>
        print(type(y))  # Output: <class 'float'>
        print(type(z))  # Output: <class 'str'>
    """)
    nb.code("x")

    nb.sottosezione("Importare librerie", intro="""
        Python ha un vasto ecosistema di librerie e framework. Per usare una libreria bisogna
        **importarla** nel proprio codice. Un esempio con la libreria `numpy`:
    """)
    nb.code("""
        import numpy as np

        print(np.__version__)
    """)
    nb.md("""
        Non tutto ha bisogno di un `import`. `print`, `len` e `type` sono comandi di Python, sempre
        disponibili. `pd.read_csv`, invece, è di pandas: esiste solo dopo `import pandas as pd`, e il
        prefisso `pd.` dice da dove arriva.
    """)
    nb.code("""
        # comando di Python: nessun import
        len("Python")
    """)
    nb.md("""
        Le librerie che incontreremo stanno da una parte o dall'altra:

        | Libreria standard: arriva con Python | Da installare nel progetto |
        |---|---|
        | `math`, `datetime`, `os` | `pandas`, `numpy` |
        | `pathlib`, `json`, `sqlite3` | `plotly`, `requests`, `openpyxl` |
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Tipi di dato numerici", intro="""
        Python gestisce vari tipi di dati numerici:

        - **Integers (`int`)**: numeri interi positivi o negativi
        - **Floats (`float`)**: numeri decimali positivi o negativi
        - **Booleans (`bool`)**: valori binari `True` (vero) o `False` (falso)
    """)
    nb.sottosezione("Operatori aritmetici", intro="""
        Python supporta gli operatori aritmetici standard:

        - **Somma (`+`)**
        - **Sottrazione (`-`)**
        - **Moltiplicazione (`*`)**
        - **Divisione (`/`)**
        - **Divisione intera (`//`)**: restituisce la parte intera della divisione
        - **Modulo (`%`)**: resto della divisione
        - **Potenza (`**`)**
    """)
    nb.code("""
        a = 5    # int
        b = 2    # int
        c = 3.5  # float

        # Somma
        print(a + b)   # Output: 7
        print(c + b)   # Output: 5.5

        # Moltiplicazione
        print(a * b)   # Output: 10
        print(c * b)   # Output: 7.0

        # Divisione
        print(a / b)   # Output: 2.5
        print(c / b)   # Output: 1.75
    """)
    nb.code("""
        # Divisione intera
        print(a // b)  # Output: 2
        print(c // b)  # Output: 1.0

        # Modulo
        print(a % b)   # Output: 1
        print(c % b)   # Output: 1.5

        # Potenza
        print(a ** b)  # Output: 25
        print(c ** b)  # Output: 12.25
    """)

    nb.sottosezione("Funzioni matematiche", intro="""
        Con il modulo `math` possiamo usare funzioni matematiche avanzate.
    """)
    nb.code("""
        from math import sqrt

        help(sqrt)
    """)
    nb.code("""
        import math

        # Radice quadrata
        print(math.sqrt(25))  # Output: 5.0

        # Valore assoluto
        print(abs(-10))       # Output: 10

        # Seno di un angolo (in radianti)
        print(math.sin(math.pi / 2))  # Output: 1.0
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Manipolazione di stringhe", intro="""
        Le **stringhe** sono sequenze di caratteri usate per rappresentare testi.
    """)
    nb.sottosezione("Creazione e tipo di stringhe", intro="""
        Le stringhe possono essere delimitate da apici singoli (`'`) o doppi (`"`).
    """)
    nb.code("""
        nome = 'Mario'
        cognome = "Rossi"

        print(type(nome))    # Output: <class 'str'>
        print(type(cognome)) # Output: <class 'str'>
    """)

    nb.sottosezione("Concatenazione", intro="""
        Possiamo concatenare stringhe con l'operatore `+`:
    """)
    nb.code("""
        nome_completo = nome + ' ' + cognome
        print(nome_completo)  # Output: Mario Rossi
    """)

    nb.sottosezione("Formattazione", intro="""
        Per inserire valori dentro una stringa possiamo usare il metodo `.format()` oppure le
        **f-string**. Un esempio con `.format()`:
    """)
    nb.code("""
        nome = 'Mario'
        anni = 30

        saluto = 'Ciao, mi chiamo {} e ho {} anni'.format(nome, anni)
        print(saluto)  # Output: Ciao, mi chiamo Mario e ho 30 anni
    """)
    nb.md("Lo stesso con una f-string: i valori si scrivono direttamente tra le graffe.")
    nb.code("""
        saluto = f'Ciao, mi chiamo {nome} e ho {anni} anni'
        print(saluto)  # Output: Ciao, mi chiamo Mario e ho 30 anni
    """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Massimo, minimo e differenza",
        scenario="",
        richiesta=(
            "Definisci tre variabili numeriche, trova il valore massimo, il valore minimo e la "
            "differenza tra massimo e minimo. Stampa i risultati con le f-string."
        ),
        suggerimento="usa le funzioni `max()` e `min()`.",
        starter="""
            # Definizione delle variabili
            a = 10
            b = 25
            c = 7

            # Calcolo del massimo e minimo
            valore_massimo = max(...)
            valore_minimo = ...
            differenza = ...

            # Stampa dei risultati
            print(f"Valore massimo: {valore_massimo}")  # Output: Valore massimo: 25
            print(f"Valore minimo: {...}")              # Output: Valore minimo: 7
            print(...)                                  # Output: Differenza: 18
        """,
        soluzione="""
            # Definizione delle variabili
            a = 10
            b = 25
            c = 7

            # Calcolo del massimo e minimo
            valore_massimo = max(a, b, c)
            valore_minimo = min(a, b, c)
            differenza = valore_massimo - valore_minimo

            # Stampa dei risultati
            print(f"Valore massimo: {valore_massimo}")  # Output: Valore massimo: 25
            print(f"Valore minimo: {valore_minimo}")    # Output: Valore minimo: 7
            print(f"Differenza: {differenza}")          # Output: Differenza: 18
        """,
        verifica="""
            assert valore_massimo == 25, "❌ Valore massimo errato"
            assert valore_minimo == 7, "❌ Valore minimo errato"
            assert differenza == 18, "❌ Differenza errata"
            print("✅ Esercizio corretto")
        """,
    )
    nb.esercizio(
        titolo="Area del cerchio",
        scenario="",
        richiesta="""
            Scrivi un programma che calcoli l'area di un cerchio di raggio 5 e stampi il risultato.

            Formula: $\\text{Area} = \\pi \\times r^2$
        """,
        suggerimento="usa `math.pi` per il valore di π.",
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
            assert math.isclose(area, 78.54, rel_tol=1e-3), "❌ Area errata"
            print("✅ Calcolo corretto")
        """,
    )
    nb.esercizio(
        titolo="Ore e minuti",
        scenario="Un film dura 137 minuti e vogliamo scrivere la durata in ore e minuti.",
        richiesta="Calcola `ore` con la divisione intera `//` e `minuti` con il modulo `%`.",
        suggerimento="un'ora ha 60 minuti.",
        starter="""
            durata_minuti = 137

            ore = ...
            minuti = ...

            print(ore, minuti)  # Output: 2 17
        """,
        soluzione="""
            durata_minuti = 137

            ore = durata_minuti // 60
            minuti = durata_minuti % 60

            print(ore, minuti)  # Output: 2 17
        """,
        verifica="""
            assert ore == 2, "❌ ore: quante volte 60 sta in 137"
            assert minuti == 17, "❌ minuti: il resto della divisione per 60"
        """,
        facoltativo=True,
    )
    return nb
