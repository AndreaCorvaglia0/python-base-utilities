"""A1 · Approfondimenti 1: il materiale della prima giornata che resta fuori quando il tempo manca."""

from nbkit import Cella, Notebook, box_html


def costruisci() -> Notebook:
    nb = Notebook(
        num="A1",
        file="Approfondimenti_1",
        titolo="Approfondimenti 1",
        blocco=2,
        giornata=1,
        fuori_programma=True,
        intento="Quello che resta fuori dalla prima giornata quando il tempo manca: da fare se la classe è avanti, o a casa.",
        obiettivi={
            "base": [
                "unire e intersecare due set con `union()` e `intersection()`",
                "ripetere un'operazione finché una condizione è vera con il ciclo `while`",
                "leggere più file CSV con `glob` e indicare il tipo delle colonne con `dtype`",
            ],
            "avanzata": [
                "unire e intersecare due set con `union()` e `intersection()`",
                "ripetere un'operazione con `while` e scrivere in forma compatta con `map`, `filter` e generatori",
                "leggere più file CSV con `glob` e indicare il tipo delle colonne con `dtype`",
            ],
        },
        tempo={"base": 40, "avanzata": 55},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Operazioni con i set", intro="""
        I set sono quelli del notebook 02. Con le operazioni di insieme ne confrontiamo due.
    """)
    nb.md("Unione:")
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

    # ------------------------------------------------------------------ 2
    nb.sezione("Il ciclo while", intro="Il ciclo `while` esegue il blocco di codice finché una condizione è vera:")
    nb.code("""
        x = 0
        while x < 5:
            print(x)
            x += 1
    """)
    nb.md("""
        Rispondi a mente, poi controlla copiando il codice in una cella. Quanto vale `x` alla fine?
        ```python
        x = 10
        while x > 0:
            x = x - 3
        ```
    """)
    nb.celle.append(Cella("md", box_html("soluzione", """
        `-2`: `x` passa per 10, 7, 4, 1 e -2, e a quel punto la condizione `x > 0` è falsa.
    """, titolo="Risposta"), solo_soluzioni=True))

    # ------------------------------------------------------------------ 3 (A)
    with nb.solo("avanzata"):
        nb.sezione("map, filter e generatori", intro="""
            Servono la funzione lambda e le list comprehension del notebook 04.
        """)
        nb.sottosezione("La funzione map", intro="Applica una funzione a tutti gli elementi di una lista:")
        nb.code("""
            numeri = [1, 2, 3, 4, 5]
            numeri_al_quadrato = list(map(lambda x: x ** 2, numeri))
            print(numeri_al_quadrato)
        """)
        nb.sottosezione("La funzione filter", intro="Filtra gli elementi in base a una condizione:")
        nb.code("""
            numeri_pari = list(filter(lambda x: x % 2 == 0, numeri))
            print(numeri_pari)
        """)
        nb.sottosezione("Generatori", intro="""
            Un **generatore** è una funzione che usa `yield` al posto di `return`: produce i valori uno alla
            volta, solo quando servono, senza costruire tutta la lista. È un iteratore, quindi si percorre
            con `for` o con `next()`.
        """)
        nb.code("""
            def quadrati(n):
                for i in range(1, n + 1):
                    yield i ** 2

            generatore = quadrati(3)
            print(next(generatore), next(generatore), next(generatore))  # Output: 1 4 9
        """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Più file CSV e tipi di dato", intro="""
        Riprendiamo la lettura dei file CSV del notebook 06.
    """)
    nb.code("import pandas as pd")
    nb.sottosezione("Trovare e leggere più file CSV", intro="""
        Il modulo `glob` trova i file il cui nome segue uno schema, per esempio tutti quelli che finiscono
        con `.csv`. Prima creiamo due file CSV di esempio.
    """)
    nb.code("""
        df1 = pd.DataFrame({
            "ID": [1, 2, 3],
            "Nome": ["Alice", "Bob", "Charlie"],
            "Età": ["25", "30", "35"],  # intenzionalmente come stringhe
        })
        df2 = pd.DataFrame({
            "ID": [4, 5, 6],
            "Nome": ["David", "Eva", "Frank"],
            "Età": ["40", "45", "50"],  # intenzionalmente come stringhe
        })
    """)
    nb.code("""
        # salviamo i DataFrame come file CSV
        df1.to_csv("dati1.csv", index=False)
        df2.to_csv("dati2.csv", index=False)
        print("File 'dati1.csv' e 'dati2.csv' creati.")
    """)
    nb.code("""
        from glob import glob

        # cerchiamo i file CSV che iniziano con "dati"
        file_csv = sorted(glob("dati*.csv"))
        print("File CSV trovati:")
        for file in file_csv:
            print(file)
    """)
    nb.code("""
        # leggere il primo file CSV
        df_csv1 = pd.read_csv("dati1.csv")
        df_csv1
    """)
    nb.sottosezione("Specificare i tipi di dato", intro="""
        Durante la lettura pandas prova a riconoscere da solo il tipo di ogni colonna. A volte serve
        indicarlo noi, con il parametro `dtype`. Supponiamo di volere la colonna `Età` sicuramente come intero.
    """)
    nb.code("""
        # leggere il CSV specificando i tipi di dato
        tipi_colonne = {"ID": int, "Nome": str, "Età": int}
        df_csv1_tipizzato = pd.read_csv("dati1.csv", dtype=tipi_colonne)
        df_csv1_tipizzato.dtypes
    """)
    nb.md("""
        Per unire i dati di più file leggiamo ogni file in un DataFrame, mettiamo i DataFrame in una lista e
        li concateniamo con `pd.concat()`.
    """)
    nb.code("""
        # leggere tutti i file CSV e aggiungerli a una lista
        dfs = []
        for nome_file in file_csv:
            df = pd.read_csv(nome_file, dtype=tipi_colonne)
            dfs.append(df)
    """)
    nb.code("""
        # concatenare i DataFrame
        df_unito = pd.concat(dfs, ignore_index=True)
        df_unito
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Due liste della spesa",
        scenario="Anna e Luca hanno scritto ciascuno la sua lista, con qualche ripetizione. Vogliamo una lista unica.",
        richiesta="""
            1. Salva in `da_comprare` il set di tutto quello che c'è nelle due liste, senza doppioni.
            2. Salva in `in_comune` il set delle cose che compaiono in entrambe.
            3. Salva in `quanti` il numero di cose da comprare.
        """,
        suggerimento="`set()` trasforma una lista in set; poi `union()` e `intersection()`.",
        starter="""
            lista_anna = ["pane", "latte", "mele", "pane", "caffè"]
            lista_luca = ["latte", "pasta", "mele", "olio"]

            da_comprare = ...
            in_comune = ...
            quanti = ...

            print(in_comune)  # Output: {'latte', 'mele'} (l'ordine può cambiare)
        """,
        soluzione="""
            lista_anna = ["pane", "latte", "mele", "pane", "caffè"]
            lista_luca = ["latte", "pasta", "mele", "olio"]

            da_comprare = set(lista_anna).union(set(lista_luca))
            in_comune = set(lista_anna).intersection(set(lista_luca))
            quanti = len(da_comprare)

            print(in_comune)  # Output: {'latte', 'mele'} (l'ordine può cambiare)
        """,
        verifica="""
            assert da_comprare == {"pane", "latte", "mele", "caffè", "pasta", "olio"}, "❌ da_comprare: unisci i due set"
            assert in_comune == {"latte", "mele"}, "❌ in_comune: usa intersection()"
            assert quanti == 6, "❌ Le cose da comprare sono 6"
        """,
        facoltativo=True,
    )
    nb.esercizio(
        titolo="Risparmiare con un ciclo while",
        scenario="Mettiamo da parte 150 euro al mese e vogliamo sapere dopo quanti mesi arriviamo ad almeno 1000 euro.",
        richiesta="""
            Con un ciclo `while`, salva in `mesi` il numero di mesi necessari e in `risparmio` la somma
            messa da parte alla fine. Output atteso: `7 1050`.
        """,
        suggerimento="la condizione del `while` è `risparmio < 1000`; a ogni giro aumentano sia `risparmio` sia `mesi`.",
        starter="""
            risparmio = 0
            mesi = 0

            # scrivi il ciclo while qui

            print(mesi, risparmio)  # Output: 7 1050
        """,
        soluzione="""
            risparmio = 0
            mesi = 0

            while risparmio < 1000:
                risparmio += 150
                mesi += 1

            print(mesi, risparmio)  # Output: 7 1050
        """,
        verifica="""
            assert mesi == 7, "❌ mesi: servono 7 mesi, il settimo porta a 1050 euro"
            assert risparmio == 1050, "❌ risparmio: 150 euro per 7 mesi fanno 1050"
        """,
    )
    return nb
