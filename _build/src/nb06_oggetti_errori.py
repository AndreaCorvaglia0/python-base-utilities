"""06 · Oggetti ed errori."""

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
        num="06",
        file="06_Oggetti_ed_errori",
        titolo="Oggetti ed errori",
        blocco=2,
        giornata=1,
        intento="Da qui in avanti useremo quasi solo codice scritto da altri: pandas, Plotly, i suggerimenti di Copilot. Per leggerlo servono due cose: capire chi fa cosa in `dato.metodo()` e non farsi spaventare da un traceback.",
        obiettivi=[
            "leggere `dato.metodo()` e capire chi fa cosa",
            "leggere la documentazione e i type hint di una funzione",
            "leggere un traceback dal basso e riconoscere gli errori più comuni",
        ],
        tempo={"base": 40, "avanzata": 30},
        dati=["impianti_fv.csv"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Tutto è un oggetto", intro="""
        In Python ogni valore è un oggetto: porta con sé dei dati e le operazioni che sa fare. `type`
        dice di che oggetto si tratta; il punto dopo il nome apre la lista di quello che sa fare.
    """)
    nb.code("""
        pod = "it001e45678901"
        consumi = [320.5, 410.0, 275.8]

        print(type(pod))
        print(type(consumi))
    """)
    nb.md("""
        Le operazioni di un oggetto sono i metodi, e si chiamano con il punto e le parentesi.
        `pod.upper()` si legge "chiedi alla stringa `pod` di darsi in maiuscolo". La forma
        `dato.metodo()` è sempre la stessa; cosa succede lo decide l'oggetto a sinistra del punto.
    """)
    nb.code("""
        print(pod.upper())
        print(pod.count("0"))         # quante volte compare "0" nel testo
        print(consumi.count(410.0))   # quante volte compare 410.0 nella lista
    """)
    nb.md("""
        Un DataFrame di pandas è un oggetto come gli altri, solo più ricco. Lo costruiamo da un dizionario
        di liste, come avevamo anticipato parlando dei dizionari, e gli facciamo le stesse domande.
    """)
    nb.code("""
        import pandas as pd

        df = pd.DataFrame({
            "pod": ["IT001E45678901", "IT001E45678902", "IT001E45678903"],
            "kwh": [320.5, 410.0, 275.8],
            "fascia": ["F1", "F2", "F1"],
        })

        type(df)
    """)
    nb.md("""
        Un oggetto ha attributi e metodi. Un attributo è un dato che l'oggetto conserva e si legge senza
        parentesi: `df.shape` (righe e colonne), `df.columns`. Un metodo è un'azione e vuole le
        parentesi, anche vuote: `df.head()` mostra le prime righe.
    """)
    nb.code("""
        print(df.shape)
        print(df.columns)
    """)
    nb.code("df.head()")
    nb.md("""
        Lo stesso nome di metodo, `count`, su tre oggetti fa tre cose diverse: la stringa conta le
        occorrenze di un carattere, la lista quelle di un valore, il DataFrame i valori presenti per
        colonna. Per questo, prima di leggere il metodo, guardiamo cosa c'è a sinistra del punto.
    """)
    nb.code("df.count()")
    nb.md("""
        E se dimentichiamo le parentesi? Niente errore: Python ci restituisce il metodo stesso, non il
        suo risultato. Quando nell'output compare `bound method`, mancano le parentesi. Al contrario, le
        parentesi su un attributo danno un errore: una tupla come `df.shape` non si può "chiamare".
    """)
    nb.code("df.head")
    nb.md("""
        Alcune operazioni non sono metodi ma funzioni di Python che accettano oggetti di tipo diverso:
        `len` conta i caratteri di una stringa, gli elementi di una lista, le righe di un DataFrame. Si
        riconoscono perché l'oggetto va tra le parentesi, non prima del punto.
    """)
    nb.code("print(len(pod), len(consumi), len(df))")
    nb.md("""
        Per vedere tutto quello che un oggetto sa fare c'è `dir(oggetto)`: una lista lunga, con molti
        nomi tra doppi underscore da ignorare. In VS Code basta scrivere il punto e aspettare il menu dei
        suggerimenti: è la stessa lista, già filtrata.
    """)
    nb.code("dir(pod)[-8:]")
    nb.prova_tu(
        richiesta="""
            Da `df`: metti in `n_righe` il numero di righe leggendo `df.shape` (una tupla: il primo
            elemento) e in `prime_due` le prime due righe con `head`.
        """,
        starter="""
            n_righe = ...
            prime_due = ...

            print(n_righe)
            prime_due
        """,
        soluzione="""
            n_righe = df.shape[0]
            prime_due = df.head(2)

            print(n_righe)
            prime_due
        """,
        verifica="""
            assert n_righe == 3, "❌ n_righe: il primo elemento di df.shape, letto senza parentesi"
            assert len(prime_due) == 2, "❌ prime_due: head accetta il numero di righe tra parentesi"
        """,
    )
    nb.box("ricorda", """
        - Senza parentesi un dato (`df.shape`), con le parentesi un'azione (`df.head()`).
        - Chi fa cosa lo decide l'oggetto a sinistra del punto.
        - `bound method` nell'output: mancano le parentesi.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Leggere la documentazione", intro="""
        Nessuno ricorda a memoria i parametri di `read_csv`. Si legge la documentazione: `help(funzione)`
        nel notebook, oppure il nome seguito da `?`. In VS Code basta anche fermare il mouse sul nome.
        Partiamo da una funzione piccola.
    """)
    nb.code("help(round)")
    nb.md("""
        La prima riga è la firma: i parametri, nell'ordine. `number` non ha default, quindi è
        obbligatorio; `ndigits=None` ha un default, quindi si può omettere. `None` è il valore "niente" di
        Python, e qui vuol dire: nessun decimale, restituisci un intero. Sotto, il testo spiega il resto.
    """)
    nb.md("""
        Ora una firma vera, quella di `pd.read_csv`. L'output è lungo, oltre quaranta parametri: nessuno
        li legge tutti. Si guarda la firma in testa e si cerca quello che serve.
    """)
    nb.code("help(pd.read_csv)")
    nb.md("""
        Leggiamola con calma, nei pezzi che contano.

        ```python
        read_csv(filepath_or_buffer, *, sep=<no_default>, delimiter=None, header='infer', ...,
                 decimal='.', ..., encoding=None, ...)
        ```

        - `filepath_or_buffer` non ha default: è l'unico obbligatorio, il percorso del file.
        - L'asterisco `*` da solo significa che tutto quello che segue va passato per nome: `sep=";"`, non `";"` al secondo posto.
        - `decimal='.'` ed `encoding=None` hanno un default: insieme a `sep` sono le manopole che gireremo nel prossimo notebook per i CSV italiani.
    """)
    nb.md("""
        Con il solo argomento obbligatorio, `read_csv` legge un file "all'americana": virgola come
        separatore, punto decimale. Per l'anagrafica degli impianti fotovoltaici basta così.
    """)
    nb.code("""
        impianti = pd.read_csv("../Dati/impianti_fv.csv")
        impianti.head(3)
    """)
    nb.md("""
        Nelle firme moderne compaiono i type hint: dopo i due punti il tipo atteso, dopo la freccia il
        tipo restituito. Python non li controlla, servono a chi legge. `def media(valori: list[float]) -> float`
        si legge: prende una lista di numeri con la virgola e restituisce un numero con la virgola.
    """)
    nb.code('''
        def media(valori: list[float]) -> float:
            """Media aritmetica di una lista di numeri."""
            return sum(valori) / len(valori)

        media([320.5, 410.0, 275.8])
    ''')
    nb.code("help(media)")
    nb.md("""
        `help` mostra firma, type hint e docstring insieme: tutto quello che serve per usare la funzione
        senza aprirla. Nella firma di `read_csv`, `encoding: str | None = None` si legge allo stesso modo:
        una stringa oppure niente, e di default niente. La barra verticale vuol dire "oppure".
    """)
    nb.prova_tu(
        richiesta="""
            Rileggi la firma di `round` e arrotonda `1234.5678` a un decimale passando il secondo
            argomento per nome. Salva il risultato in `arrotondato`.
        """,
        starter="""
            arrotondato = round(1234.5678, ...)
            arrotondato
        """,
        soluzione="""
            arrotondato = round(1234.5678, ndigits=1)
            arrotondato
        """,
        verifica="""
            assert arrotondato == 1234.6, "❌ arrotondato: un decimale, con il parametro chiamato per nome"
        """,
    )
    nb.box("ricorda", """
        - Parametro senza `=`: obbligatorio. Con `= valore`: facoltativo, e quel valore è il default.
        - Dopo un `*` da solo, tutto si passa per nome.
        - `nome: tipo` dice cosa entra, `-> tipo` cosa esce. Python non li controlla; noi li leggiamo.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Gli errori, uno alla volta", intro="""
        Un errore in Python non è un giudizio: è un messaggio scritto per essere letto. Si chiama
        traceback e si legge dal basso. L'ultima riga dice il tipo di errore e il perché; le righe sopra,
        con la freccia, dicono dove. Li provochiamo uno alla volta, apposta, e li leggiamo.
    """)
    nb.sottosezione("SyntaxError", intro="""
        È l'unico errore che Python trova prima di eseguire: la frase non è Python. Questa cella dà errore
        apposta: mancano i due punti dopo la condizione dell'`if`.
    """)
    nb.code("""
        consumo_kwh = 1350
        if consumo_kwh > 1000
            print("Sopra soglia")
    """, errore=True)
    nb.md("""
        `SyntaxError: expected ':'`: Python dice anche cosa si aspettava, e l'accento circonflesso `^`
        indica il punto. Nei `SyntaxError` la riga segnalata è quasi sempre quella giusta; quando non lo
        è, il problema sta nella riga prima, una parentesi o una virgoletta mai chiusa.
    """)
    nb.sottosezione("NameError", intro="""
        Il nome non esiste. Una variabile mai creata, scritta diversa (`consumo` e `Consumo` sono due
        nomi), o definita in una cella che non abbiamo ancora eseguito. Qui manca una lettera.
    """)
    nb.code("""
        consumo_kwh = 1350
        print(consumo_kw * 0.25)
    """, errore=True)
    nb.md("""
        Questo traceback ha la forma tipica. In fondo, `NameError: name 'consumo_kw' is not defined`, e
        spesso anche il suggerimento `Did you mean`. Sopra, la riga con la freccia `---->` è quella della
        nostra cella che ha fallito. Dal basso: cosa, poi dove.
    """)
    nb.sottosezione("TypeError", intro="""
        I tipi non vanno d'accordo. Il caso che incontreremo di più: numeri letti da un file che sembrano
        numeri e sono testo. `sum` parte da zero, un intero, e prova a sommarci una stringa.
    """)
    nb.code("""
        letture = ["312", "298", "305"]
        sum(letture)
    """, errore=True)
    nb.md("""
        `unsupported operand type(s) for +: 'int' and 'str'`: il più non sa cosa fare tra un intero e una
        stringa. Il rimedio è convertire prima di contare, con `int()` o `float()`.
    """)
    nb.code("""
        totale = 0
        for lettura in letture:
            totale += int(lettura)

        totale
    """)
    nb.sottosezione("KeyError", intro="""
        La chiave non c'è. Su un dizionario capita con una chiave scritta diversa; su una Series di
        pandas quando usiamo un numero come se fosse una posizione, mentre l'indice ha etichette.
    """)
    nb.code("""
        listino = {"F1": 0.28, "F2": 0.25, "F3": 0.21}
        listino["f1"]
    """, errore=True)
    nb.md("""
        `KeyError: 'f1'`: l'ultima riga riporta la chiave che abbiamo chiesto, tale e quale, e si vede
        al volo che è minuscola. Stesso errore su una Series con le etichette, se chiediamo `[0]` pensando
        alla prima posizione.
    """)
    nb.code("""
        consumi_pod = pd.Series([320.5, 410.0], index=["IT001E45678901", "IT001E45678902"])
        consumi_pod[0]
    """, errore=True)
    nb.md("""
        Il traceback qui è lungo, perché attraversa il codice di pandas: le righe in mezzo non sono
        nostre e si saltano, fino all'ultima. Con le etichette si usa l'etichetta; per la posizione c'è
        `.iloc[0]`, che riprenderemo con i DataFrame.
    """)
    nb.code("""
        print(consumi_pod["IT001E45678901"])
        print(consumi_pod.iloc[0])
    """)
    nb.sottosezione("IndexError", intro="""
        La posizione non esiste. Tre elementi occupano le posizioni 0, 1 e 2: chiedere la 3 è l'errore
        "di uno" più frequente, insieme a quello su una lista vuota.
    """)
    nb.code("""
        consumi = [320.5, 410.0, 275.8]
        consumi[3]
    """, errore=True)
    nb.md("""
        `list index out of range`: fuori dall'intervallo. L'ultimo elemento è `consumi[2]`, oppure
        `consumi[-1]` se non vogliamo contare.
    """)
    nb.sottosezione("ValueError", intro="""
        Il tipo è giusto ma il valore non va: `float` accetta una stringa, purché dentro ci sia un
        numero scritto come lo vuole Python. Con la virgola decimale italiana non lo riconosce.
    """)
    nb.code('float("12,5")', errore=True)
    nb.md("""
        `could not convert string to float: '12,5'`: il messaggio mostra il valore colpevole. Qui si
        sostituisce la virgola a mano; con un CSV intero lo farà `read_csv` con `decimal=","`.
    """)
    nb.code('float("12,5".replace(",", "."))')
    nb.sottosezione("FileNotFoundError", intro="""
        Il file non c'è, o non c'è dove lo stiamo cercando. Il messaggio riporta il percorso esatto che
        Python ha provato: si confronta con quello che c'è davvero nella cartella.
    """)
    nb.code('pd.read_csv("../Dati/impianti_fotovoltaici.csv")', errore=True)
    nb.md("""
        `No such file or directory: '../Dati/impianti_fotovoltaici.csv'`. Anche qui il traceback
        attraversa pandas: righe da saltare, fino all'ultima. Nove volte su dieci il nome è scritto
        diverso, oppure manca il `../` perché il file è nella cartella accanto, non in questa.
    """)
    nb.code("""
        impianti = pd.read_csv("../Dati/impianti_fv.csv")
        impianti.shape
    """)
    nb.sottosezione("try ed except, per saperli leggere", intro="""
        Nel codice dei colleghi si incontra `try/except`: "prova questo e, se salta fuori quel tipo di
        errore, fai quest'altro". Serve saperlo leggere, non metterlo ovunque: un errore nascosto è un
        errore che scopriremo più tardi, più lontano dalla causa.
    """)
    nb.code("""
        testo = "12,5"

        try:
            valore = float(testo)
        except ValueError:
            valore = float(testo.replace(",", "."))

        valore
    """)
    nb.md("""
        Si legge: prova a convertire; se arriva un `ValueError`, riprova con il punto. Qualsiasi altro
        errore passa oltre e si vede, ed è giusto così. Un `except:` senza il tipo cattura tutto, anche
        quello che volevamo vedere: nel codice che leggiamo è un campanello d'allarme.
    """)
    nb.prova_tu(
        richiesta="""
            Questa cella dà errore. Leggi l'ultima riga del traceback, trova la riga con la freccia e
            correggi quel tanto che basta perché `prezzo_medio` venga calcolato.
        """,
        starter="""
            listino = {"F1": 0.28, "F2": 0.25, "F3": 0.21}
            prezzo_medio = (listino["F1"] + listino["F2"] + listino["f3"]) / 3
            prezzo_medio
        """,
        soluzione="""
            listino = {"F1": 0.28, "F2": 0.25, "F3": 0.21}
            prezzo_medio = (listino["F1"] + listino["F2"] + listino["F3"]) / 3
            prezzo_medio
        """,
        verifica="""
            assert round(prezzo_medio, 4) == 0.2467, "❌ prezzo_medio: la media dei tre prezzi del listino, con le chiavi scritte come nel dizionario"
        """,
    )
    nb.box("ricorda", """
        - Leggi l'ultima riga: tipo di errore e messaggio.
        - Risali fino alla freccia nel tuo codice: le righe dentro le librerie si saltano.
        - Gli errori si leggono, non si nascondono con `try/except`.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Cosa fare quando non capisco l'errore", intro="""
        Capita a tutti, ogni giorno. La differenza la fa il metodo, non l'esperienza.
    """)
    nb.md("""
        1. Leggi l'ultima riga, poi cerca la freccia nel tuo codice. Spesso basta.
        2. Esegui le celle sopra, dall'inizio: metà dei `NameError` sono celle saltate dopo un **Restart**.
        3. Spezza la riga: un'operazione per cella, finché l'errore si isola.
        4. Cerca su internet il nome dell'errore più il messaggio, tra virgolette, senza i tuoi nomi di variabile.
        5. Chiedi a Copilot "spiegami questo errore" incollando il traceback intero. Poi verifica eseguendo.
    """)
    nb.box("nota", """
        A un collega, o a Copilot, si manda tutto il traceback: la riga con la freccia è quella che
        fa risparmiare dieci minuti a chi legge.
    """)
    nb.md("""
        I sette errori di oggi, con la riga da guardare per ciascuno, stanno in una pagina sola:
        [Scheda errori](../Schede/Scheda_errori.md). Da tenere aperta nelle prossime settimane.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il traceback del collega",
        scenario="""
            Il collega del turno di notte ha lasciato un notebook con quattro celle che "ieri
            funzionavano". Oggi ognuna dà un errore diverso, e lui dorme. Le sistemiamo noi: per
            ciascuna, leggere l'ultima riga del traceback, trovare la riga con la freccia, correggere il
            minimo indispensabile.
        """,
        richiesta="""
            Fai funzionare le quattro celle qui sotto senza cambiare cosa calcolano. Alla fine devono
            esistere `totale_kwh`, `media_letture`, `costo_f3` e `potenza_kw`.
        """,
        suggerimento="Ogni cella ha un errore solo. Esegui, leggi, correggi, riesegui.",
        starter="""
            consumi_kwh = [320.5, 410.0, 275.8]
            totale_kwh = sum(consumi_kw)
            totale_kwh
        """,
        soluzione="""
            consumi_kwh = [320.5, 410.0, 275.8]
            totale_kwh = sum(consumi_kwh)
            totale_kwh
        """,
        perche="Quattro errori, quattro ultime righe diverse: il nome, i tipi, la chiave, il valore. In ogni caso la correzione sta nella riga indicata dalla freccia, non altrove.",
    )
    _altra_cella_rotta(nb, starter="""
        letture = ["312", "298", "305"]
        media_letture = sum(letture) / len(letture)
        media_letture
    """, soluzione="""
        letture = ["312", "298", "305"]
        totale = 0
        for lettura in letture:
            totale += int(lettura)
        media_letture = totale / len(letture)
        media_letture
    """)
    _altra_cella_rotta(nb, starter="""
        listino = {"F1": 0.28, "F2": 0.25, "F3": 0.21}
        costo_f3 = 150 * listino["F 3"]
        costo_f3
    """, soluzione="""
        listino = {"F1": 0.28, "F2": 0.25, "F3": 0.21}
        costo_f3 = 150 * listino["F3"]
        costo_f3
    """)
    _altra_cella_rotta(nb, starter="""
        potenza_kw = float("6,0")
        potenza_kw
    """, soluzione="""
        potenza_kw = float("6.0")
        potenza_kw
    """)
    _verifica_finale(nb, """
        assert round(totale_kwh, 1) == 1006.3, "❌ totale_kwh: la lista si chiama consumi_kwh"
        assert media_letture == 305, "❌ media_letture: converti ogni lettura in numero prima di sommare"
        assert round(costo_f3, 2) == 31.5, "❌ costo_f3: la chiave del listino è F3, senza spazio"
        assert potenza_kw == 6.0, "❌ potenza_kw: float vuole il punto decimale, non la virgola"
    """)

    nb.esercizio(
        titolo="Il notebook del tirocinante",
        bis=True,
        scenario="""
            Il tirocinante ha scritto quattro celle per il report sugli impianti fotovoltaici ed è andato
            a pranzo lasciandole rosse. Il report serve alle 14. Stesso metodo: ultima riga, freccia,
            correzione minima.
        """,
        richiesta="""
            Fai funzionare le quattro celle. Alla fine devono esistere `taglia`, `ultimo_pod`, `n_righe`
            e `impianti`, il DataFrame dell'anagrafica letto dalla cartella `../Dati`.
        """,
        suggerimento="Il primo errore compare prima ancora di eseguire. Gli altri tre li abbiamo già incontrati oggi.",
        starter="""
            potenza_kw = 10
            if potenza_kw > 6
                taglia = "trifase"
            else:
                taglia = "monofase"
            taglia
        """,
        soluzione="""
            potenza_kw = 10
            if potenza_kw > 6:
                taglia = "trifase"
            else:
                taglia = "monofase"
            taglia
        """,
        perche="`df.shape()` con le parentesi è l'errore speculare al `bound method`: un attributo si legge, non si chiama. Il nome del file si controlla nella cartella, non si indovina.",
    )
    _altra_cella_rotta(nb, starter="""
        pod = ["IT001E45678901", "IT001E45678902"]
        ultimo_pod = pod[2]
        ultimo_pod
    """, soluzione="""
        pod = ["IT001E45678901", "IT001E45678902"]
        ultimo_pod = pod[-1]
        ultimo_pod
    """)
    _altra_cella_rotta(nb, starter="""
        import pandas as pd

        df = pd.DataFrame({"pod": ["IT001E45678901", "IT001E45678902", "IT001E45678903"], "kwh": [320.5, 410.0, 275.8]})
        n_righe = df.shape()[0]
        n_righe
    """, soluzione="""
        import pandas as pd

        df = pd.DataFrame({"pod": ["IT001E45678901", "IT001E45678902", "IT001E45678903"], "kwh": [320.5, 410.0, 275.8]})
        n_righe = df.shape[0]
        n_righe
    """)
    _altra_cella_rotta(nb, starter="""
        impianti = pd.read_csv("../Dati/impianti_fotovoltaici.csv")
        impianti.head()
    """, soluzione="""
        impianti = pd.read_csv("../Dati/impianti_fv.csv")
        impianti.head()
    """)
    _verifica_finale(nb, """
        assert taglia == "trifase", "❌ taglia: dopo la condizione dell'if servono i due punti"
        assert ultimo_pod == "IT001E45678902", "❌ ultimo_pod: due elementi hanno le posizioni 0 e 1; l'ultimo è pod[-1]"
        assert n_righe == 3, "❌ n_righe: shape è un attributo, si legge senza parentesi"
        assert len(impianti) == 40, "❌ impianti: il file si chiama impianti_fv.csv, nella cartella ../Dati"
    """)

    nb.esercizio(
        titolo="Leggi la firma",
        scenario="""
            Quando chiederemo a Copilot un `read_csv` con i parametri giusti, dovremo controllare che
            non li inventi. Per allenarci, il capo ci gira tre domande a cui rispondere leggendo la
            documentazione, non a memoria.
        """,
        richiesta="""
            Esegui `help(round)`, `help(pd.read_csv)` e `help(media)` dove serve, poi compila il
            dizionario `risposte` con tre valori.

            1. `"ndigits_obbligatorio"`: `True` o `False`, a seconda che in `round` il parametro `ndigits` sia obbligatorio.
            2. `"default_decimal"`: il valore di default di `decimal` in `read_csv`, come stringa.
            3. `"tipo_restituito"`: il tipo che `media` dichiara di restituire, come stringa.
        """,
        suggerimento="Un parametro è obbligatorio se nella firma non ha `=`; il tipo restituito è quello dopo la freccia `->`.",
        starter='''
            def media(valori: list[float]) -> float:
                """Media aritmetica di una lista di numeri."""
                return sum(valori) / len(valori)


            risposte = {
                "ndigits_obbligatorio": ...,
                "default_decimal": ...,
                "tipo_restituito": ...,
            }
            risposte
        ''',
        soluzione='''
            def media(valori: list[float]) -> float:
                """Media aritmetica di una lista di numeri."""
                return sum(valori) / len(valori)


            risposte = {
                "ndigits_obbligatorio": False,
                "default_decimal": ".",
                "tipo_restituito": "float",
            }
            risposte
        ''',
        verifica="""
            assert risposte["ndigits_obbligatorio"] is False, "❌ ndigits ha un default (None): non è obbligatorio"
            assert risposte["default_decimal"] == ".", "❌ default_decimal: nella firma di read_csv cerca decimal="
            assert risposte["tipo_restituito"] == "float", "❌ tipo_restituito: il tipo dopo la freccia ->"
        """,
        perche="Tre risposte lette, non ricordate. `ndigits=None` nella firma vuol dire facoltativo; `decimal='.'` è il motivo per cui i CSV italiani si leggono con `decimal=\",\"`.",
        passo_in_piu=dict(
            testo="""
                Con `help(sorted)` trova il parametro che inverte l'ordine e scrivi il suo nome in
                `parametro`. Poi usalo per ordinare `consumi_kwh` dal più alto al più basso in
                `dal_piu_alto`.
            """,
            starter="""
                consumi_kwh = [320.5, 410.0, 275.8]

                parametro = "..."
                dal_piu_alto = sorted(consumi_kwh, ...)
                dal_piu_alto
            """,
            soluzione="""
                consumi_kwh = [320.5, 410.0, 275.8]

                parametro = "reverse"
                dal_piu_alto = sorted(consumi_kwh, reverse=True)
                dal_piu_alto
            """,
            verifica="""
                assert parametro == "reverse", "❌ parametro: il nome compare nella firma di sorted, dopo key"
                assert dal_piu_alto == [410.0, 320.5, 275.8], "❌ dal_piu_alto: passa il parametro a True"
            """,
        ),
    )
    nb.esercizio(
        titolo="Il separatore giusto",
        bis=True,
        scenario="""
            Il customer care riceve le letture come righe di testo, tipo `"IT001E45678901;320,5;F1"`,
            da un sistema che non esporta altro. Prima di arrivare a pandas vogliamo spezzare una riga nei
            suoi campi con il metodo `split` delle stringhe, leggendo la sua documentazione.
        """,
        richiesta="""
            Esegui `help(str.split)`. In `risposte` scrivi `"nome_separatore"` (il nome del parametro che
            indica il separatore) e `"default_maxsplit"` (il default di `maxsplit`, come numero). Poi
            spezza `riga` in `campi` usando il separatore giusto.
        """,
        suggerimento="La firma di un metodo delle stringhe si legge con `help(str.nome_metodo)`.",
        starter="""
            riga = "IT001E45678901;320,5;F1"

            risposte = {
                "nome_separatore": ...,
                "default_maxsplit": ...,
            }
            campi = riga.split(...)
            campi
        """,
        soluzione="""
            riga = "IT001E45678901;320,5;F1"

            risposte = {
                "nome_separatore": "sep",
                "default_maxsplit": -1,
            }
            campi = riga.split(";")
            campi
        """,
        verifica="""
            assert risposte["nome_separatore"] == "sep", "❌ nome_separatore: il primo parametro dopo self nella firma di split"
            assert risposte["default_maxsplit"] == -1, "❌ default_maxsplit: il valore dopo maxsplit= nella firma"
            assert campi == ["IT001E45678901", "320,5", "F1"], "❌ campi: il separatore è il punto e virgola"
        """,
    )
    return nb
