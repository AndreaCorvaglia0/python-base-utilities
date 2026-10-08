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
        intento="Raccoglie gli argomenti della prima giornata che restano fuori quando il tempo manca; si affronta in classe se si è in anticipo sul programma, oppure a casa.",
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
        Nel notebook 02 abbiamo visto che un set è una collezione di elementi unici, senza un ordine.
        Per i set Python mette a disposizione le operazioni della teoria degli insiemi, che confrontano
        due set e ne ricavano un terzo. Le due che si usano più spesso sono l'unione e l'intersezione.
    """)
    nb.md("""
        L'unione di due set, che si ottiene con il metodo `union()`, contiene tutti gli elementi presenti
        in almeno uno dei due, senza ripetizioni. Nell'esempio il colore `"rosso"`, che compare in entrambi
        i set, nel risultato appare una volta sola.
    """)
    nb.code("""
        colori = {"rosso", "verde", "blu"}
        altri_colori = {"giallo", "rosso", "viola"}

        unione = colori.union(altri_colori)
        print(unione)
        # Output: {'blu', 'rosso', 'verde', 'giallo', 'viola'}
    """)
    nb.md("""
        L'intersezione, che si ottiene con il metodo `intersection()`, contiene invece solo gli elementi
        che compaiono in entrambi i set. Applicata agli stessi due set di colori, restituisce l'unico
        colore che hanno in comune.
    """)
    nb.code("""
        intersezione = colori.intersection(altri_colori)
        print(intersezione)
        # Output: {'rosso'}
    """)
    nb.box("nota", """
        Un set conviene in tre situazioni. La prima è quando servono elementi unici, perché un set non
        contiene doppioni e trasformare una lista in set è il modo più semplice per eliminarli. La seconda
        è quando bisogna confrontare due collezioni con le operazioni di insieme, cioè unione, intersezione
        e differenza. La terza è quando si deve controllare spesso se un elemento è presente, perché su un
        set la verifica con `in` è molto più rapida che su una lista.
    """, titolo="Perché usare i set")

    # ------------------------------------------------------------------ 2
    nb.sezione("Il ciclo while", intro="""
        Il ciclo `while` ripete il blocco di codice indentato finché la condizione scritta dopo la parola
        chiave resta vera. Python valuta di nuovo la condizione all'inizio di ogni giro, quindi il blocco
        deve modificare qualcosa che prima o poi la renda falsa, altrimenti il ciclo non termina. Nell'esempio
        la variabile `x` parte da 0 e cresce di uno a ogni giro, e il ciclo stampa i numeri da 0 a 4.
    """)
    nb.code("""
        x = 0
        while x < 5:
            print(x)
            x += 1
    """)
    nb.md("""
        Prima di proseguire, prova a calcolare a mente quanto vale `x` al termine del ciclo seguente, e poi
        controlla la risposta copiando il codice in una cella nuova.
        ```python
        x = 10
        while x > 0:
            x = x - 3
        ```
    """)
    nb.celle.append(Cella("md", box_html("soluzione", """
        Il valore finale è `-2`. La variabile `x` passa per 10, 7, 4, 1 e infine -2, e solo a quel punto la
        condizione `x > 0` diventa falsa e il ciclo si ferma.
    """, titolo="Risposta"), solo_soluzioni=True))

    # ------------------------------------------------------------------ 3 (A)
    with nb.solo("avanzata"):
        nb.sezione("map, filter e generatori", intro="""
            Le funzioni `map` e `filter` e i generatori permettono di scrivere in forma compatta operazioni
            che altrimenti richiederebbero un ciclo. Per seguire questa sezione servono la funzione lambda e
            le list comprehension, che abbiamo visto nel notebook 04.
        """)
        nb.sottosezione("La funzione map", intro="""
            La funzione `map` applica una funzione a ciascun elemento di una lista e restituisce i risultati
            nello stesso ordine. Il risultato è un iteratore, per questo lo trasformiamo in lista con `list()`
            prima di stamparlo. Nell'esempio la funzione applicata è una lambda che eleva al quadrato.
        """)
        nb.code("""
            numeri = [1, 2, 3, 4, 5]
            numeri_al_quadrato = list(map(lambda x: x ** 2, numeri))
            print(numeri_al_quadrato)
        """)
        nb.sottosezione("La funzione filter", intro="""
            La funzione `filter` tiene soltanto gli elementi per cui la funzione passata come primo argomento
            restituisce `True`. Con una lambda che controlla il resto della divisione per 2 otteniamo i numeri
            pari della lista precedente.
        """)
        nb.code("""
            numeri_pari = list(filter(lambda x: x % 2 == 0, numeri))
            print(numeri_pari)
        """)
        nb.sottosezione("Generatori", intro="""
            Un **generatore** è una funzione che usa `yield` al posto di `return`. Invece di costruire subito
            la lista completa dei risultati, produce i valori uno alla volta, nel momento in cui vengono
            richiesti, e per questo occupa poca memoria anche quando i valori sono molti. Un generatore è un
            iteratore, quindi si percorre con un ciclo `for` oppure chiedendo il valore successivo con
            `next()`, come nell'esempio.
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
        In questa sezione riprendiamo la lettura dei file CSV del notebook 06 e la estendiamo in due
        direzioni: leggere insieme più file con la stessa struttura e indicare a pandas il tipo di ciascuna
        colonna.
    """)
    nb.code("import pandas as pd")
    nb.sottosezione("Trovare e leggere più file CSV", intro="""
        Il modulo `glob` della libreria standard trova i file il cui nome segue uno schema, per esempio
        tutti quelli che finiscono con `.csv`. Per avere qualcosa da cercare, creiamo prima due piccoli
        DataFrame con le stesse colonne e li salviamo come file CSV nella cartella del notebook. La colonna
        `Età` è scritta di proposito come testo, così nella sottosezione successiva possiamo chiedere a
        pandas di leggerla come numero intero.
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
    nb.md("""
        Nello schema `dati*.csv` l'asterisco sta per una sequenza qualsiasi di caratteri, quindi `glob`
        restituisce tutti i file il cui nome inizia con `dati` e finisce con `.csv`. L'ordine in cui `glob`
        elenca i file non è garantito, per questo lo mettiamo in ordine alfabetico con `sorted`. Nella cella
        successiva leggiamo il primo file per controllarne il contenuto.
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
        Durante la lettura pandas cerca di riconoscere da solo il tipo di ogni colonna, osservando i valori
        che contiene. Quando vogliamo essere sicuri del risultato, possiamo indicare noi i tipi con il
        parametro `dtype`, che riceve un dizionario dal nome della colonna al tipo. Nell'esempio chiediamo
        che `ID` ed `Età` siano letti come interi e `Nome` come testo, e controlliamo il risultato con
        l'attributo `dtypes`.
    """)
    nb.code("""
        # leggere il CSV specificando i tipi di dato
        tipi_colonne = {"ID": int, "Nome": str, "Età": int}
        df_csv1_tipizzato = pd.read_csv("dati1.csv", dtype=tipi_colonne)
        df_csv1_tipizzato.dtypes
    """)
    nb.md("""
        Per unire i dati di più file leggiamo ciascun file in un DataFrame, con gli stessi tipi di colonna,
        e raccogliamo i DataFrame in una lista. La funzione `pd.concat()` li mette poi uno sotto l'altro in
        un unico DataFrame; con `ignore_index=True` l'indice viene rinumerato da zero, invece di ripetere
        quello di ciascun file.
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
        scenario="""
            Anna e Luca hanno scritto ciascuno la propria lista della spesa, e alcune voci compaiono più volte
            o in tutte e due le liste. Vogliamo ricavarne un'unica lista senza doppioni e sapere quali cose
            avevano segnato entrambi.
        """,
        richiesta="""
            1. Salva in `da_comprare` il set di tutto quello che c'è nelle due liste, senza doppioni.
            2. Salva in `in_comune` il set delle cose che compaiono in entrambe.
            3. Salva in `quanti` il numero di cose da comprare.
        """,
        suggerimento="la funzione `set()` trasforma una lista in un set, sul quale si possono poi usare i metodi `union()` e `intersection()`.",
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
            messa da parte alla fine. Se il ciclo è corretto, la stampa finale mostra `7 1050`, cioè sette
            mesi e 1050 euro.
        """,
        suggerimento="il ciclo continua finché vale `risparmio < 1000`, e a ogni giro `risparmio` aumenta di 150 e `mesi` di uno.",
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
