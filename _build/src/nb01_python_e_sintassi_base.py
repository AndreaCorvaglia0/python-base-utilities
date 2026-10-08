"""01 · Introduzione a Python e sintassi base."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="01",
        file="01_Python_e_sintassi_base",
        titolo="Introduzione a Python e sintassi base",
        blocco=1,
        giornata=1,
        intento=(
            "In questo notebook vediamo le regole di base con cui si scrive il codice Python e i primi "
            "due tipi di dato con cui si lavora, i numeri e le stringhe."
        ),
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
        Python è uno dei linguaggi di programmazione più diffusi al mondo, apprezzato per la sua
        flessibilità e perché si impara con relativa facilità. Si usa nello sviluppo web, nella scienza
        dei dati, nell'Intelligenza Artificiale e nel Machine Learning, oltre che per scrivere piccoli
        script che automatizzano attività ripetitive. Si dice spesso che Python arrivi **"con le batterie
        incluse"**, perché la sua libreria di base copre già molte esigenze comuni. Inoltre, essendo
        molto usato, dispone di un gran numero di librerie e framework di qualità, che permettono di
        svolgere compiti complessi con poco codice.

        [Sito ufficiale di Python](https://www.python.org/)
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Caratteristiche principali", intro="""
        Il codice Python è pensato per essere **leggibile**, con una sintassi semplice e pulita. Python è
        un linguaggio **interpretato** e non compilato, il che significa che un programma chiamato
        interprete legge ed esegue le istruzioni una alla volta, senza una traduzione preliminare in
        codice macchina; per questo un notebook può eseguire una cella per volta. La **memoria** è
        gestita in modo automatico, quindi non dobbiamo occuparci di riservarla e di liberarla. Python è
        inoltre **multi-paradigma**, perché permette di scrivere codice procedurale, a oggetti o
        funzionale, e offre un'ampia **libreria standard**.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Sintassi di base")
    nb.sottosezione("Indentazione", intro="""
        In Python l'indentazione, cioè lo spazio all'inizio della riga, definisce i blocchi di codice.
        Non ci sono parentesi graffe o altri segni che indichino dove un blocco inizia e dove finisce,
        quindi le istruzioni che appartengono allo stesso blocco si scrivono tutte rientrate dello
        stesso numero di spazi, di solito quattro. Nell'esempio qui sotto la riga con `print` è
        rientrata perché fa parte del blocco dell'`if`, e viene eseguita solo se la condizione è vera.
    """)
    nb.code("""
        if 3 == 3:
            print("Questo è un output")
    """)

    nb.sottosezione("Variabili", intro="""
        In Python non serve dichiarare il tipo di una variabile quando la creiamo, perché il tipo viene
        ricavato dal valore che le assegniamo. La funzione `type()` restituisce il tipo di un valore, e
        nella prima cella qui sotto la usiamo per vedere che `x`, `y` e `z` sono rispettivamente un
        intero, un numero con la virgola e una stringa. La seconda cella contiene soltanto il nome `x`,
        e il notebook mostra il suo valore perché è l'ultima riga della cella.
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
        Python ha un vasto ecosistema di librerie e framework, e per usare una libreria bisogna prima
        **importarla** nel proprio codice con l'istruzione `import`. Nell'esempio qui sotto importiamo
        `numpy`, una libreria per il calcolo numerico, con il nome abbreviato `np`, che è la convenzione
        più diffusa. Da quel momento il contenuto della libreria si raggiunge con il prefisso `np.`, come
        `np.__version__`, che contiene la versione installata.
    """)
    nb.code("""
        import numpy as np

        print(np.__version__)
    """)
    nb.md("""
        Non tutto ha bisogno di un `import`. Funzioni come `print`, `len` e `type` fanno parte del
        linguaggio e sono sempre disponibili, come mostra la cella qui sotto, che conta i caratteri di
        una parola. Una funzione come `pd.read_csv`, invece, appartiene alla libreria pandas e si può
        usare solo dopo `import pandas as pd`; il prefisso `pd.` indica proprio da quale libreria
        proviene.
    """)
    nb.code("""
        # comando di Python: nessun import
        len("Python")
    """)
    nb.md("""
        Le librerie che incontreremo nel corso appartengono a due gruppi. Quelle della libreria standard
        sono installate insieme a Python e basta importarle, mentre le altre vanno prima aggiunte
        all'ambiente del progetto. La tabella seguente riporta le principali di ciascun gruppo.

        | Libreria standard: arriva con Python | Da installare nel progetto |
        |---|---|
        | `math`, `datetime`, `os` | `pandas`, `numpy` |
        | `pathlib`, `json`, `sqlite3` | `plotly`, `requests`, `openpyxl` |
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Tipi di dato numerici", intro="""
        Python distingue diversi tipi di dati numerici. Gli interi (`int`) sono numeri senza parte
        decimale, positivi o negativi, mentre i numeri in virgola mobile (`float`) hanno una parte
        decimale, che in Python si separa con il punto e non con la virgola. I booleani (`bool`) possono
        assumere soltanto due valori, `True` (vero) e `False` (falso), e sono il risultato dei confronti
        come `3 == 3`, che abbiamo usato nell'esempio sull'indentazione.
    """)
    nb.sottosezione("Operatori aritmetici", intro="""
        Python supporta gli operatori aritmetici standard, cioè la somma (`+`), la sottrazione (`-`), la
        moltiplicazione (`*`) e la divisione (`/`), a cui si aggiungono la divisione intera (`//`), il
        modulo (`%`) e la potenza (`**`). La cella qui sotto prova somma, moltiplicazione e divisione su
        due interi e su un numero decimale. Conviene notare che la divisione `/` restituisce sempre un
        `float`, anche quando divide due interi, e che basta un `float` tra gli operandi perché anche il
        risultato sia un `float`.
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
    nb.md("""
        La cella successiva mostra gli altri tre operatori. La divisione intera `//` restituisce la parte
        intera del quoziente, il modulo `%` restituisce il resto della divisione e `**` eleva il primo
        numero alla potenza indicata dal secondo. Anche in questo caso, quando uno degli operandi è un
        `float` il risultato è un `float`, come in `c // b`, che vale `1.0`.
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
        Le funzioni matematiche più avanzate, come la radice quadrata, i logaritmi e le funzioni
        trigonometriche, si trovano nel modulo `math` della libreria standard. Con `from math import sqrt`
        importiamo una sola funzione del modulo, che da quel momento si usa senza prefisso. La funzione
        `help()` ne mostra la documentazione, cioè che cosa fa e quali argomenti accetta.
    """)
    nb.code("""
        from math import sqrt

        help(sqrt)
    """)
    nb.md("""
        In alternativa si importa l'intero modulo con `import math` e si richiamano le sue funzioni con il
        prefisso `math.`, come nella cella seguente; nello stesso modulo `math.pi` contiene il valore di
        π. La funzione `abs()`, che restituisce il valore assoluto, non fa parte di `math` ma è sempre
        disponibile, come `print` e `len`.
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
        Le **stringhe** sono sequenze di caratteri e sono il tipo che Python usa per rappresentare i
        testi, dai nomi ai messaggi da stampare. In questa sezione vediamo come si creano, come si
        uniscono e come si inseriscono al loro interno i valori calcolati dal programma.
    """)
    nb.sottosezione("Creazione e tipo di stringhe", intro="""
        Una stringa si scrive tra apici singoli (`'`) o doppi (`"`), e le due forme sono equivalenti.
        Conviene scegliere quella che non compare nel testo, per cui una frase con un apostrofo, come
        `"L'area del cerchio"`, si scrive tra virgolette doppie. In entrambi i casi `type()` restituisce
        `str`.
    """)
    nb.code("""
        nome = 'Mario'
        cognome = "Rossi"

        print(type(nome))    # Output: <class 'str'>
        print(type(cognome)) # Output: <class 'str'>
    """)

    nb.sottosezione("Concatenazione", intro="""
        L'operatore `+`, applicato a due stringhe, le concatena, cioè le unisce una dopo l'altra in una
        stringa nuova. Lo spazio tra nome e cognome non viene aggiunto in automatico, quindi
        nell'esempio lo inseriamo come stringa a sé, `' '`, tra le due variabili.
    """)
    nb.code("""
        nome_completo = nome + ' ' + cognome
        print(nome_completo)  # Output: Mario Rossi
    """)

    nb.sottosezione("Formattazione", intro="""
        Quando una stringa deve contenere valori calcolati dal programma, come un numero, la
        concatenazione diventa scomoda, perché obbliga a convertire ogni valore in stringa. Python offre
        due strumenti più comodi, il metodo `.format()` e le **f-string**. Con `.format()` si scrivono
        nella stringa delle parentesi graffe vuote, che vengono sostituite, nell'ordine, dagli argomenti
        passati al metodo.
    """)
    nb.code("""
        nome = 'Mario'
        anni = 30

        saluto = 'Ciao, mi chiamo {} e ho {} anni'.format(nome, anni)
        print(saluto)  # Output: Ciao, mi chiamo Mario e ho 30 anni
    """)
    nb.md("""
        Una f-string si riconosce dalla lettera `f` prima delle virgolette e permette di scrivere i nomi
        delle variabili direttamente tra le graffe, nel punto in cui il valore deve comparire. Il
        risultato è identico a quello di `.format()`, ma il codice si legge più facilmente, ed è per
        questo che nel corso useremo quasi sempre le f-string.
    """)
    nb.code("""
        saluto = f'Ciao, mi chiamo {nome} e ho {anni} anni'
        print(saluto)  # Output: Ciao, mi chiamo Mario e ho 30 anni
    """)

    nb.md("Riassunto in una pagina: [Leggere il codice: cosa è cosa](../Schede/Scheda_leggere_codice.md).")

    # ------------------------------------------------------------------ 6
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Massimo, minimo e differenza",
        scenario="",
        richiesta=(
            "Nella cella qui sotto sono già definite tre variabili numeriche, `a`, `b` e `c`. Calcola il "
            "valore massimo, il valore minimo e la differenza tra i due, assegnandoli a `valore_massimo`, "
            "`valore_minimo` e `differenza`, e stampa i tre risultati con le f-string."
        ),
        suggerimento=(
            "usa le funzioni `max()` e `min()`, che accettano più numeri separati da virgola e "
            "restituiscono rispettivamente il più grande e il più piccolo."
        ),
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
            L'area si ottiene moltiplicando π per il quadrato del raggio, secondo la formula
            $\\text{Area} = \\pi \\times r^2$.
        """,
        suggerimento="il valore di π si trova in `math.pi`, e il quadrato del raggio si calcola con l'operatore `**`.",
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
        richiesta=(
            "Calcola con la divisione intera `//` il numero di ore intere e assegnalo a `ore`, poi "
            "calcola con il modulo `%` i minuti che restano e assegnali a `minuti`."
        ),
        suggerimento="un'ora ha 60 minuti, quindi entrambe le operazioni dividono la durata per 60.",
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
