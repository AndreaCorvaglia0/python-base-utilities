"""05 · Condizioni, cicli e funzioni."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="05",
        file="05_Condizioni_cicli_funzioni",
        titolo="Condizioni, cicli e funzioni",
        blocco=2,
        giornata=1,
        intento="Fin qui ogni cella faceva una cosa sola, dall'alto in basso. Da qui il codice impara a scegliere una strada, a ripetersi e a farsi chiamare per nome.",
        obiettivi={
            "base": [
                "scegliere un ramo con `if`, `elif` ed `else`",
                "ripetere un'operazione su liste e dizionari con `for`",
                "chiudere il codice in una funzione con argomenti, default e `return`",
            ],
            "avanzata": [
                "scegliere un ramo con `if`/`elif`/`else` e ripetere su liste e dizionari con `for`",
                "chiudere il codice in una funzione con argomenti, default e `return`",
                "scrivere meno con list comprehension, `lambda`, `map` e `filter`, e riconoscere iterabili e generatori",
            ],
        },
        tempo={"base": 90, "avanzata": 95},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Condizioni: if, elif, else", intro="""
        Un programma che fa sempre la stessa cosa serve a poco: vogliamo un avviso solo quando il consumo
        è sopra soglia. Una condizione è una domanda con risposta `True` o `False`; `if` esegue il blocco
        rientrato solo quando la risposta è `True`.
    """)
    nb.code("""
        consumo_kwh = 1350
        soglia = 1000

        if consumo_kwh > soglia:
            print(f"Consumo sopra soglia: {consumo_kwh} kWh")
    """)
    nb.md("""
        Le righe rientrate di quattro spazi sono il blocco dell'`if`: partono solo se la condizione è vera.
        Se cambiamo `consumo_kwh` in 800 e rieseguiamo, non succede niente, ed è giusto così. Per
        fare qualcos'altro nel caso contrario c'è `else`.
    """)
    nb.code("""
        if consumo_kwh > soglia:
            print("Sopra soglia")
        else:
            print("Nella norma")
    """)
    nb.md("""
        Quando le strade sono più di due si aggiunge `elif` ("altrimenti, se"). Python prova le condizioni
        dall'alto e si ferma alla prima vera. L'esempio che ci accompagna oggi: le fasce orarie, i tre
        prezzi della bolletta che dipendono dall'ora. In un giorno lavorativo F1 dalle 8 alle 19, F2 dalle
        7 alle 8 e dalle 19 alle 23, F3 di notte.
    """)
    nb.code("""
        ora = 21

        if 8 <= ora < 19:
            fascia = "F1"
        elif 7 <= ora < 8 or 19 <= ora < 23:
            fascia = "F2"
        else:
            fascia = "F3"

        fascia
    """)
    nb.md("""
        `8 <= ora < 19` è la scrittura compatta di `ora >= 8 and ora < 19` e si legge come in matematica.
        L'`else` finale prende tutto quello che non è passato prima, cioè la notte, senza bisogno di
        descriverla.
    """)
    nb.md("""
        Le condizioni si combinano con `and` (tutte vere), `or` (almeno una vera) e `not` (il contrario).
        Il risultato è un `bool` come gli altri: possiamo guardarlo da solo, prima di metterlo in un `if`.
    """)
    nb.code("""
        ora = 10
        giorno = "sabato"

        print(8 <= ora < 19)
        print(giorno == "sabato" or giorno == "domenica")
        print(not giorno == "domenica")
    """)
    nb.md("""
        Per chiedere se un valore sta in una lista c'è `in`, che sostituisce una fila di `or`. Con i giorni
        della settimana si usa di continuo.
    """)
    nb.code("""
        if giorno in ["sabato", "domenica"]:
            print("Weekend: niente F1")
        else:
            print("Giorno lavorativo")
    """)
    nb.box("attenzione", """
        L'ordine degli `elif` decide il risultato. Con `if ora >= 7:` in testa, il ramo della F1 non verrebbe
        mai raggiunto: Python si ferma alla prima condizione vera. Dal caso più stretto al più largo, e
        l'`else` per quello che resta.
    """)
    nb.md("""
        Un `if` può stare dentro un altro `if`, rientrato di altri quattro spazi. Una volta si legge, due
        volte no: quasi sempre la stessa cosa si scrive con un `and` o con un `elif` in più.
    """)
    nb.code("""
        ora = 10
        giorno = "sabato"

        if giorno == "sabato":
            if 7 <= ora < 23:
                print("Sabato, fascia F2")
            else:
                print("Sabato, fascia F3")
        else:
            print("Valgono le fasce del giorno lavorativo")
    """)
    nb.md("""
        Senza annidare: `if giorno == "sabato" and 7 <= ora < 23:`. Negli esercizi metteremo insieme ora
        e giorno in una funzione sola, con tutte le regole delle fasce.
    """)
    nb.prova_tu(
        richiesta="""
            Dato `potenza_kw`, metti in `taglia` il testo `"domestico"` se la potenza è fino a 6 kW
            compresi, `"piccola azienda"` fino a 30 kW compresi, `"industriale"` oltre.
        """,
        starter="""
            potenza_kw = 15

            if ...:
                taglia = ...
            elif ...:
                taglia = ...
            else:
                taglia = ...

            taglia
        """,
        soluzione="""
            potenza_kw = 15

            if potenza_kw <= 6:
                taglia = "domestico"
            elif potenza_kw <= 30:
                taglia = "piccola azienda"
            else:
                taglia = "industriale"

            taglia
        """,
        verifica="""
            assert taglia == "piccola azienda", "❌ Con 15 kW la taglia è piccola azienda: controlla i confronti e l'ordine dei rami"
        """,
    )

    # ------------------------------------------------------------------ 2
    nb.sezione("Cicli: for e while", intro="""
        Abbiamo i consumi di tre POD e vogliamo stamparli uno per riga. Tre `print` quasi uguali si
        scrivono; con trecento POD no. `for` ripete un blocco per ogni elemento di una lista.
    """)
    nb.code("""
        consumi_kwh = [320.5, 410.0, 275.8]

        for consumo in consumi_kwh:
            print(f"{consumo} kWh")
    """)
    nb.md("""
        `consumo` è la variabile del ciclo: a ogni giro prende l'elemento successivo. Il nome lo scegliamo
        noi, e conviene che sia il singolare della lista. Dentro il blocco ci sta qualsiasi cosa, un `if`
        compreso.
    """)
    nb.code("""
        soglia = 300

        for consumo in consumi_kwh:
            if consumo > soglia:
                print(f"{consumo} kWh: sopra soglia")
            else:
                print(f"{consumo} kWh: nella norma")
    """)
    nb.md("""
        Due cose si fanno in quasi ogni ciclo: accumulare un totale, o raccogliere alcuni elementi in una
        lista nuova. In entrambi i casi il contenitore si crea vuoto prima del `for` e si riempie un giro
        alla volta.
    """)
    nb.code("""
        totale_kwh = 0
        for consumo in consumi_kwh:
            totale_kwh += consumo

        totale_kwh
    """)
    nb.md("""
        Per una somma secca c'è già `sum(consumi_kwh)`; la forma con `+=` serve quando il conto non è una
        somma e basta. Per raccogliere in una lista, `.append` dentro il ciclo, di solito sotto un `if`.
    """)
    nb.code("""
        sopra_soglia = []
        for consumo in consumi_kwh:
            if consumo > soglia:
                sopra_soglia.append(consumo)

        sopra_soglia
    """)
    nb.md("""
        Quando servono i numeri da 0 a `n - 1`, o ripetere `n` volte, c'è `range(n)`. Come lo slicing: parte
        da 0 e la fine è esclusa. Con due argomenti si sceglie l'inizio, con tre anche il passo.
    """)
    nb.code("""
        for ora in range(3):
            print(f"Ore {ora}:00")
    """)
    nb.md("""
        `range` non è una lista: per vederlo tutto in una volta lo convertiamo con `list`. Le ore della
        fascia F1 sono `range(8, 19)`, dalle 8 alle 18 comprese.
    """)
    nb.code("""
        print(list(range(8, 19)))
        print(list(range(0, 24, 6)))
    """)
    nb.md("""
        Se oltre al valore serve la posizione (la prima lettura, la seconda...), `enumerate` consegna
        entrambi a ogni giro: dopo il `for` si scrivono due variabili separate da virgola. La posizione
        parte da 0; con `start=1` parte da 1, se deve finire in un report.
    """)
    nb.code("""
        pod = ["IT001E45678901", "IT001E45678902", "IT001E45678903"]

        for posizione, codice in enumerate(pod, start=1):
            print(f"{posizione}. {codice}")
    """)
    nb.md("""
        Su un dizionario il `for` scorre le chiavi. Per avere chiave e valore insieme c'è `.items()`,
        con la stessa forma a due variabili.
    """)
    nb.code("""
        consumi_pod = {"IT001E45678901": 320.5, "IT001E45678902": 410.0, "IT001E45678903": 275.8}

        for codice, consumo in consumi_pod.items():
            print(f"{codice}: {consumo} kWh")
    """)
    nb.md("""
        Due liste parallele, come il consumo di quest'anno e quello dell'anno scorso per gli stessi POD,
        si scorrono insieme con `zip`: a ogni giro un elemento dalla prima e uno dalla seconda. Il `+`
        nel formato stampa il segno anche quando è positivo.
    """)
    nb.code("""
        consumi_2024 = [320.5, 410.0, 275.8]
        consumi_2025 = [335.2, 398.7, 301.4]

        for vecchio, nuovo in zip(consumi_2024, consumi_2025):
            variazione = (nuovo - vecchio) / vecchio * 100
            print(f"{vecchio} -> {nuovo} kWh ({variazione:+.1f}%)")
    """)
    nb.box("nota", """
        Il `for` di Python scorre gli elementi, non le posizioni: `for consumo in consumi_kwh`, non
        `for i in range(len(consumi_kwh))`. Se serve anche la posizione, `enumerate`; se servono due
        liste insieme, `zip`.
    """)
    nb.prova_tu(
        richiesta="""
            Dal dizionario `consumi_pod` raccogli in `pod_alti` i codici dei POD con consumo sopra
            300 kWh, con un `for` su `.items()` e un `if`.
        """,
        starter="""
            consumi_pod = {"IT001E45678901": 320.5, "IT001E45678902": 410.0, "IT001E45678903": 275.8}

            pod_alti = []
            for codice, consumo in ...:
                ...

            pod_alti
        """,
        soluzione="""
            consumi_pod = {"IT001E45678901": 320.5, "IT001E45678902": 410.0, "IT001E45678903": 275.8}

            pod_alti = []
            for codice, consumo in consumi_pod.items():
                if consumo > 300:
                    pod_alti.append(codice)

            pod_alti
        """,
        verifica="""
            assert set(pod_alti) == {"IT001E45678901", "IT001E45678902"}, "❌ pod_alti: i codici (le chiavi) dei POD con consumo sopra 300"
        """,
    )

    nb.sottosezione("while: ripetere finché", intro="""
        `for` sa in anticipo quante volte girare. Quando invece bisogna ripetere finché una condizione
        resta vera, c'è `while`. Un accumulo da 100 kWh si carica di 20 kWh l'ora: contiamo le ore che
        servono per riempirlo.
    """)
    nb.code("""
        capacita_kwh = 100
        livello_kwh = 12.5
        carica_oraria_kwh = 20
        ore = 0

        while livello_kwh < capacita_kwh:
            livello_kwh = min(livello_kwh + carica_oraria_kwh, capacita_kwh)
            ore += 1

        print(f"Pieno dopo {ore} ore")
    """)
    nb.md("""
        A ogni giro Python ricontrolla la condizione; quando diventa falsa, esce. Il rischio è una
        condizione che non diventa mai falsa: il ciclo non finisce e il kernel resta appeso (lo ferma il
        pulsante **Interrupt**). Un limite di sicurezza nella condizione costa mezza riga.
    """)
    nb.code("""
        livello_kwh = 12.5
        carica_oraria_kwh = 0      # il caricatore è guasto
        ore = 0

        while livello_kwh < capacita_kwh and ore < 24:
            livello_kwh += carica_oraria_kwh
            ore += 1

        print(f"Dopo {ore} ore il livello è ancora {livello_kwh} kWh")
    """)
    nb.prova_tu(
        aula="base",
        richiesta="""
            Un accumulo parte da `livello_kwh = 40` e si scarica di 7,5 kWh l'ora per alimentare una
            pompa. Con un `while`, conta in `ore` quante ore passano prima che il livello scenda sotto
            i 12 kWh.
        """,
        starter="""
            livello_kwh = 40
            scarica_oraria_kwh = 7.5
            ore = 0

            while livello_kwh >= ...:
                livello_kwh = ...
                ore = ...

            print(f"Dopo {ore} ore il livello è {livello_kwh} kWh")
        """,
        soluzione="""
            livello_kwh = 40
            scarica_oraria_kwh = 7.5
            ore = 0

            while livello_kwh >= 12:
                livello_kwh -= scarica_oraria_kwh
                ore += 1

            print(f"Dopo {ore} ore il livello è {livello_kwh} kWh")
        """,
        verifica="""
            assert ore == 4, "❌ ore: il ciclo continua finché il livello è almeno 12"
            assert livello_kwh == 10.0, "❌ livello_kwh: a ogni giro togli la scarica oraria"
        """,
    )
    nb.box("ricorda", """
        - `for elemento in lista` quando sappiamo su cosa girare; `while` quando sappiamo solo quando fermarci.
        - Il contenitore (totale a zero o lista vuota) si crea prima del ciclo.
        - `enumerate` per la posizione, `.items()` per chiave e valore, `zip` per due liste insieme.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Funzioni", intro="""
        Il codice della fascia oraria ci servirà in dieci posti diversi. Invece di copiarlo, lo chiudiamo
        in una funzione: un blocco con un nome, che riceve dei valori e ne restituisce uno. `def` la
        definisce; il nome con le parentesi la chiama.
    """)
    nb.code("""
        def fascia_feriale(ora):
            if 8 <= ora < 19:
                return "F1"
            elif 7 <= ora < 8 or 19 <= ora < 23:
                return "F2"
            else:
                return "F3"

        fascia_feriale(21)
    """)
    nb.md("""
        Definire una funzione non esegue niente: Python si segna la ricetta. Eseguirla è chiamarla, con un
        valore tra parentesi. `ora` è il parametro, il nome che quel valore prende dentro la funzione.
        `return` consegna il risultato a chi ha chiamato e chiude la funzione.
    """)
    nb.code("""
        print(fascia_feriale(3), fascia_feriale(7), fascia_feriale(12))
    """)
    nb.md("""
        `return` e `print` si confondono spesso, quindi li mettiamo uno accanto all'altro. Questa prima
        funzione stampa il costo: il numero si vede sullo schermo, ma non torna indietro.
    """)
    nb.code("""
        def costo_stampato(kwh, prezzo):
            print(kwh * prezzo)

        risultato = costo_stampato(300, 0.25)
        print(risultato)
    """)
    nb.md("""
        `risultato` vale `None`, il "niente" di Python: la funzione ha scritto a schermo e basta. Con
        `return` il valore torna a chi ha chiamato, e possiamo salvarlo, sommarlo, metterlo in una f-string.
    """)
    nb.code("""
        def costo(kwh, prezzo):
            return kwh * prezzo

        risultato = costo(300, 0.25)
        print(f"Costo: {risultato:.2f} euro")
    """)
    nb.md("""
        Gli argomenti si passano per posizione, nell'ordine dei parametri, oppure per nome. Per nome
        l'ordine non conta e si capisce cosa è cosa: è la forma che vedremo ovunque in pandas, come
        `pd.read_csv(path, sep=";")`.
    """)
    nb.code("""
        print(costo(300, 0.25))
        print(costo(kwh=300, prezzo=0.25))
        print(costo(prezzo=0.25, kwh=300))
    """)
    nb.md("""
        Se un parametro ha quasi sempre lo stesso valore gli diamo un default nella definizione:
        `prezzo=0.25`. Chi chiama può ometterlo, o cambiarlo quando serve. I parametri con default vanno
        dopo quelli senza.
    """)
    nb.code("""
        def costo(kwh, prezzo=0.25):
            return kwh * prezzo

        print(costo(300))
        print(costo(300, prezzo=0.18))
    """)
    nb.md("""
        La riga tra tre virgolette subito sotto `def` è la docstring: dice cosa fa la funzione, in una
        riga. La legge `help`, la mostra VS Code fermando il mouse sul nome, e la leggeremo noi tra sei
        mesi.
    """)
    nb.code('''
        def costo(kwh, prezzo=0.25):
            """Costo in euro di un consumo in kWh al prezzo unitario dato."""
            return kwh * prezzo

        help(costo)
    ''')
    nb.prova_tu(
        richiesta="""
            Scrivi `energia_mwh(potenza_mw, ore=0.25)` che restituisce l'energia in MWh, cioè potenza
            per ore. Con il default è l'energia di un quarto d'ora.
        """,
        starter="""
            def energia_mwh(potenza_mw, ore=0.25):
                ...

            print(energia_mwh(100))
            print(energia_mwh(100, ore=1))
        """,
        soluzione="""
            def energia_mwh(potenza_mw, ore=0.25):
                return potenza_mw * ore

            print(energia_mwh(100))
            print(energia_mwh(100, ore=1))
        """,
        verifica="""
            assert energia_mwh(100) == 25, "❌ Con il default: 100 MW per un quarto d'ora sono 25 MWh"
            assert energia_mwh(80, ore=2) == 160, "❌ ore passato per nome deve sostituire il default"
        """,
    )

    nb.sottosezione("Una funzione con un ciclo dentro", intro="""
        Dentro una funzione ci sta tutto quello che abbiamo visto: cicli, condizioni, liste. Qui contiamo
        quanti giorni di una settimana hanno superato una soglia di consumo, con la soglia come default
        che si può cambiare.
    """)
    nb.code('''
        def giorni_sopra_soglia(letture, soglia=400):
            """Conta quante letture superano la soglia."""
            conteggio = 0
            for lettura in letture:
                if lettura > soglia:
                    conteggio += 1
            return conteggio

        letture_settimana = [380.0, 415.5, 402.3, 390.1, 450.0, 310.2, 298.7]
        print(giorni_sopra_soglia(letture_settimana))
        print(giorni_sopra_soglia(letture_settimana, soglia=300))
    ''')
    nb.md("""
        `conteggio` e `lettura` nascono e muoiono dentro la funzione: fuori non esistono. È una
        protezione: due funzioni possono usare gli stessi nomi senza pestarsi i piedi. Il risultato esce
        solo dal `return`.
    """)
    nb.md("""
        Una funzione può restituire anche una lista o un dizionario. Lo schema è lo stesso: contenitore
        vuoto, ciclo che lo riempie, `return` alla fine con il risultato intero. I `print` di controllo si
        tolgono quando funziona.
    """)
    nb.code('''
        def pod_sopra_soglia(consumi, soglia=300):
            """Restituisce i codici dei POD con consumo sopra la soglia."""
            trovati = []
            for codice, consumo in consumi.items():
                if consumo > soglia:
                    trovati.append(codice)
            return trovati

        pod_sopra_soglia(consumi_pod)
    ''')
    nb.prova_tu(
        richiesta="""
            Scrivi `conta_in_fascia(ore, fascia)` che, usando `fascia_feriale` definita sopra, conta
            quante delle ore nella lista cadono nella fascia indicata.
        """,
        starter="""
            ore_letture = [3, 7, 9, 12, 15, 18, 21, 23]

            def conta_in_fascia(ore, fascia):
                conteggio = 0
                for ora in ore:
                    ...
                return conteggio

            conta_in_fascia(ore_letture, "F1")
        """,
        soluzione="""
            ore_letture = [3, 7, 9, 12, 15, 18, 21, 23]

            def conta_in_fascia(ore, fascia):
                conteggio = 0
                for ora in ore:
                    if fascia_feriale(ora) == fascia:
                        conteggio += 1
                return conteggio

            conta_in_fascia(ore_letture, "F1")
        """,
        verifica="""
            assert conta_in_fascia(ore_letture, "F1") == 4, "❌ In F1 cadono le ore 9, 12, 15 e 18"
            assert conta_in_fascia(ore_letture, "F3") == 2, "❌ In F3 cadono le ore 3 e 23"
        """,
    )
    nb.box("ricorda", """
        - `return` restituisce, `print` mostra: se il valore serve dopo, `return`.
        - Argomenti per nome quando sono più di due: `costo(kwh=300, prezzo=0.18)`.
        - Un default per il valore che cambia di rado; una docstring di una riga, sempre.
    """)

    # ------------------------------------------------------------------ 4 (solo Avanzata)
    with nb.solo("avanzata"):
        nb.sezione("Scrivere meno: comprehension, lambda, generatori", intro="""
            Il giro for-più-append è così frequente che Python ha una scrittura compatta, la list
            comprehension. Stesso risultato in una riga, e si legge come una frase: "il consumo, per ogni
            consumo nella lista, se supera la soglia".
        """)
        nb.code("""
            consumi_kwh = [320.5, 410.0, 275.8, 505.2]
            soglia = 300

            sopra_soglia = []
            for consumo in consumi_kwh:
                if consumo > soglia:
                    sopra_soglia.append(consumo)

            sopra_soglia_bis = [consumo for consumo in consumi_kwh if consumo > soglia]

            print(sopra_soglia)
            print(sopra_soglia_bis)
        """)
        nb.md("""
            La forma generale è `[espressione for elemento in lista if condizione]`. L'`if` è facoltativo,
            e l'espressione può trasformare l'elemento: da kWh a MWh, da numero a etichetta di testo.
        """)
        nb.code("""
            consumi_mwh = [consumo / 1000 for consumo in consumi_kwh]
            etichette = [f"{consumo:.0f} kWh" for consumo in consumi_kwh]

            print(consumi_mwh)
            print(etichette)
        """)
        nb.md("""
            Funziona anche su un dizionario, con `.items()` e due variabili. Con le graffe al posto delle
            quadre, e `chiave: valore` prima del `for`, costruisce un dizionario nuovo.
        """)
        nb.code("""
            consumi_pod = {"IT001E45678901": 320.5, "IT001E45678902": 410.0, "IT001E45678903": 275.8}

            pod_alti = [codice for codice, consumo in consumi_pod.items() if consumo > 300]
            consumi_pod_mwh = {codice: consumo / 1000 for codice, consumo in consumi_pod.items()}

            print(pod_alti)
            print(consumi_pod_mwh)
        """)
        nb.box("attenzione", """
            Una comprehension che non sta in una riga, o con due `for` dentro, si legge peggio del ciclo
            che sostituisce. In quel caso si torna al `for`: nessuno dà punti per la brevità.
        """)
        nb.prova_tu(
            richiesta="""
                Da `letture_settimana` costruisci con una comprehension `potenze_kw`: la potenza media in
                kW (lettura diviso 24, arrotondata a un decimale) delle sole letture sopra 400 kWh.
            """,
            starter="""
                letture_settimana = [380.0, 415.5, 402.3, 390.1, 450.0, 310.2, 298.7]

                potenze_kw = [... for lettura in letture_settimana if ...]
                potenze_kw
            """,
            soluzione="""
                letture_settimana = [380.0, 415.5, 402.3, 390.1, 450.0, 310.2, 298.7]

                potenze_kw = [round(lettura / 24, 1) for lettura in letture_settimana if lettura > 400]
                potenze_kw
            """,
            verifica="""
                assert potenze_kw == [17.3, 16.8, 18.8], "❌ potenze_kw: round(lettura / 24, 1) solo per le letture sopra 400"
            """,
        )

        nb.sottosezione("lambda: una funzione in una riga", intro="""
            Spesso una funzione serve solo per essere passata a un'altra funzione, come il criterio di
            ordinamento di `sorted`. Per queste c'è `lambda`: una funzione senza nome, scritta in una
            riga, con i parametri prima dei due punti e il risultato dopo.
        """)
        nb.code("""
            coppie = [("IT001E45678901", 320.5), ("IT001E45678902", 410.0), ("IT001E45678903", 275.8)]

            sorted(coppie, key=lambda coppia: coppia[1], reverse=True)
        """)
        nb.md("""
            `key` vuole una funzione che, dato un elemento, restituisce il valore su cui ordinare: qui il
            secondo pezzo di ogni coppia. Con `def` sarebbe identico, solo più lungo. La `lambda` evita di
            inventare un nome per tre parole che si usano una volta.
        """)
        nb.code("""
            def secondo_elemento(coppia):
                return coppia[1]

            sorted(coppie, key=secondo_elemento, reverse=True)
        """)
        nb.md("""
            Lo stesso trucco ordina un dizionario per valore: `sorted(consumi_pod.items(), key=lambda coppia: coppia[1])`.
            E tornerà con pandas, dove `df["kwh"].apply(lambda x: x / 1000)` applica la funzione a ogni
            valore di una colonna. Regola pratica: una `lambda` vive dentro un'altra chiamata; se le serve
            un nome, è un `def`.
        """)

        nb.sottosezione("map e filter", intro="""
            `map` applica una funzione a ogni elemento, `filter` tiene gli elementi per cui la funzione
            risponde `True`. Nessuno dei due restituisce una lista: per vedere il risultato ci vuole
            `list(...)`.
        """)
        nb.code("""
            print(list(map(lambda kwh: kwh / 1000, consumi_kwh)))
            print(list(filter(lambda kwh: kwh > 300, consumi_kwh)))
        """)
        nb.md("""
            Le stesse due righe come comprehension: `[kwh / 1000 for kwh in consumi_kwh]` e
            `[kwh for kwh in consumi_kwh if kwh > 300]`. Oggi si preferisce la comprehension; `map` e
            `filter` vanno riconosciuti perché il codice dei colleghi, e quello di Copilot, ne è pieno.
            Senza `list`, ecco cosa esce.
        """)
        nb.code("""
            map(lambda kwh: kwh / 1000, consumi_kwh)
        """)

        nb.sottosezione("Iterabili e generatori", intro="""
            Quel `<map object>` è il segno di una cosa che Python fa spesso: non calcola tutto subito,
            consegna gli elementi uno alla volta a chi li chiede. `range` fa lo stesso: non è una lista,
            è una promessa di numeri.
        """)
        nb.code("""
            ore = range(24)

            print(type(ore))
            print(ore)
            print(list(ore)[:5])
        """)
        nb.md("""
            Tutto ciò su cui un `for` può girare è un iterabile: liste, tuple, dizionari, stringhe, `range`,
            un file aperto. Un generatore è un iterabile che produce i valori al volo: si scrive come una
            comprehension, con le tonde al posto delle quadre.
        """)
        nb.code("""
            consumi_mwh = (kwh / 1000 for kwh in consumi_kwh)
            consumi_mwh
        """)
        nb.md("""
            `next` chiede il valore successivo. Quando finiscono, il generatore è esaurito: non si torna
            indietro, se serve si ricrea. Un `for` fa proprio questo: chiama `next` finché c'è qualcosa.
        """)
        nb.code("""
            print(next(consumi_mwh))
            print(next(consumi_mwh))
            print(list(consumi_mwh))   # quello che resta
        """)
        nb.md("""
            A cosa serve: passato direttamente a `sum`, calcola il totale senza costruire la lista
            intermedia. Su quattro valori non cambia niente; su quattro milioni di quartorari sì.
        """)
        nb.code("""
            sum(kwh / 1000 for kwh in consumi_kwh)
        """)
        nb.box("approfondimento", """
            Un DataFrame si può scorrere riga per riga con `df.iterrows()`, un generatore di righe.
            Si può, e non si fa: ogni giro è Python puro, lento, mentre pandas lavora su una colonna
            intera in un colpo solo, in codice compilato. Un milione di righe: minuti contro millisecondi.

            ```python
            for _, riga in df.iterrows():       # un giro di Python per riga: lento
                riga["kwh"] / 1000
            df["kwh"] / 1000                     # tutta la colonna in un colpo: veloce
            ```

            Quando ci verrà voglia di un `for` su un DataFrame, la domanda giusta sarà: quale operazione
            su colonna fa la stessa cosa.
        """, titolo="Perché non si cicla su un DataFrame")
        nb.box("ricorda", """
            - `[x for x in lista if cond]` sostituisce for-più-append; con le tonde diventa un generatore.
            - `lambda` vive dentro `sorted(key=)`, `map`, `filter` e `.apply`.
            - Se vedi `<map object>` o `<generator object>`, avvolgilo in `list(...)` o scorrilo con un `for`.
        """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="La fascia oraria",
        scenario="""
            Siamo nell'ufficio tariffe. Ogni lettura oraria va assegnata a una fascia, perché il listino
            del cliente ha tre prezzi. Il collega lo faceva con un foglio Excel di 168 righe, una per ora
            della settimana, e un CERCA.VERT; ha cambiato ufficio e il foglio ha una riga sbagliata che
            nessuno trova. Ci chiedono una funzione che dica la fascia a partire da ora e giorno.
        """,
        richiesta="""
            Scrivi `fascia(ora, giorno)` che restituisce `"F1"`, `"F2"` o `"F3"`. Le regole: la domenica
            è tutta F3; il sabato è F2 dalle 7 alle 23 (escluse) e F3 nelle altre ore; dal lunedì al
            venerdì F1 dalle 8 alle 19, F2 dalle 7 alle 8 e dalle 19 alle 23, F3 il resto. `giorno` arriva
            in minuscolo (`"lunedì"`, ..., `"domenica"`), `ora` è un intero da 0 a 23.
        """,
        suggerimento="Prima i giorni che decidono da soli (domenica, poi sabato), poi le ore: ogni `elif` può dare per scontato che i rami sopra siano falsi.",
        starter='''
            def fascia(ora, giorno):
                """Fascia oraria F1, F2 o F3 per un'ora (0-23) e un giorno della settimana."""
                if ...:
                    return "F3"
                ...


            print(fascia(12, "martedì"), fascia(21, "martedì"), fascia(12, "sabato"), fascia(12, "domenica"))
        ''',
        soluzione='''
            def fascia(ora, giorno):
                """Fascia oraria F1, F2 o F3 per un'ora (0-23) e un giorno della settimana."""
                if giorno == "domenica":
                    return "F3"
                elif giorno == "sabato" and 7 <= ora < 23:
                    return "F2"
                elif giorno == "sabato":
                    return "F3"
                elif 8 <= ora < 19:
                    return "F1"
                elif 7 <= ora < 8 or 19 <= ora < 23:
                    return "F2"
                else:
                    return "F3"


            print(fascia(12, "martedì"), fascia(21, "martedì"), fascia(12, "sabato"), fascia(12, "domenica"))
        ''',
        verifica="""
            assert fascia(12, "martedì") == "F1", "❌ Martedì alle 12 è F1"
            assert fascia(21, "martedì") == "F2", "❌ Martedì alle 21 è F2: controlla l'intervallo 19-23"
            assert fascia(3, "venerdì") == "F3", "❌ Venerdì alle 3 di notte è F3"
            assert fascia(12, "sabato") == "F2", "❌ Sabato alle 12 è F2, non F1: il sabato va controllato prima delle ore"
            assert fascia(12, "domenica") == "F3", "❌ Domenica è sempre F3"
        """,
        perche="Prima i casi che decidono da soli: domenica, poi sabato. Arrivati alle ore sappiamo già di essere in un giorno lavorativo, e le condizioni restano corte.",
    )
    nb.esercizio(
        titolo="La classe energetica",
        bis=True,
        scenario="""
            Il commerciale vende diagnosi energetiche e per la prima stima usa una scala semplificata in
            kWh per metro quadro all'anno: A fino a 30, B fino a 50, C fino a 90, D fino a 160, E oltre.
            Oggi guarda una tabella appesa al muro e ogni tanto sbaglia riga.
        """,
        richiesta="""
            Scrivi `classe_energetica(kwh_m2)` che restituisce la lettera della classe, da `"A"` a `"E"`.
            I limiti sono compresi: 30 è ancora A.
        """,
        suggerimento="Con `if`/`elif` dal limite più basso al più alto, `<=` fa già tutto il lavoro.",
        starter='''
            def classe_energetica(kwh_m2):
                """Classe energetica (A-E) dal consumo annuo in kWh per metro quadro."""
                if kwh_m2 <= 30:
                    return "A"
                ...


            print(classe_energetica(25), classe_energetica(45), classe_energetica(200))
        ''',
        soluzione='''
            def classe_energetica(kwh_m2):
                """Classe energetica (A-E) dal consumo annuo in kWh per metro quadro."""
                if kwh_m2 <= 30:
                    return "A"
                elif kwh_m2 <= 50:
                    return "B"
                elif kwh_m2 <= 90:
                    return "C"
                elif kwh_m2 <= 160:
                    return "D"
                else:
                    return "E"


            print(classe_energetica(25), classe_energetica(45), classe_energetica(200))
        ''',
        verifica="""
            assert classe_energetica(25) == "A", "❌ 25 kWh/m² è classe A"
            assert classe_energetica(30) == "A", "❌ 30 è ancora A: il limite è compreso, usa <="
            assert classe_energetica(45) == "B", "❌ 45 è classe B"
            assert classe_energetica(120) == "D", "❌ 120 è classe D"
            assert classe_energetica(200) == "E", "❌ Oltre 160 è classe E"
        """,
    )

    scenario_anomalie = """
        Il POD IT001E45678901 ha dodici letture mensili di consumo e a luglio qualcuno ha digitato uno
        zero di troppo. Il customer care riceve il reclamo, noi riceviamo la lista: dobbiamo trovare la
        lettura che non torna. Il criterio concordato con i colleghi: una lettura è anomala se supera il
        doppio della precedente.
    """
    richiesta_anomalie = """
        1. Con un `for` su `range(1, len(letture))`, confronta ogni lettura con quella prima e raccogli
           in `posizioni_anomale` le posizioni che superano il doppio della precedente. Stampa anche il
           mese, preso da `mesi` con la stessa posizione.
        2. Chiudi lo stesso ciclo in `trova_anomalie(letture, fattore=2)`, che restituisce la lista
           delle posizioni; `fattore` è il moltiplicatore rispetto alla lettura precedente.
    """
    starter_anomalie = '''
        mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
        letture = [312, 298, 305, 290, 310, 322, 3150, 318, 301, 295, 307, 315]

        posizioni_anomale = []
        for i in range(1, len(letture)):
            ...


        def trova_anomalie(letture, fattore=2):
            """Posizioni delle letture che superano la precedente moltiplicata per fattore."""
            ...


        print(posizioni_anomale, trova_anomalie(letture))
    '''
    soluzione_anomalie = '''
        mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
        letture = [312, 298, 305, 290, 310, 322, 3150, 318, 301, 295, 307, 315]

        posizioni_anomale = []
        for i in range(1, len(letture)):
            if letture[i] > 2 * letture[i - 1]:
                posizioni_anomale.append(i)
                print(f"Lettura anomala a {mesi[i]}: {letture[i]} kWh dopo {letture[i - 1]} kWh")


        def trova_anomalie(letture, fattore=2):
            """Posizioni delle letture che superano la precedente moltiplicata per fattore."""
            anomalie = []
            for i in range(1, len(letture)):
                if letture[i] > fattore * letture[i - 1]:
                    anomalie.append(i)
            return anomalie


        print(posizioni_anomale, trova_anomalie(letture))
    '''
    verifica_anomalie = """
        assert posizioni_anomale == [6], "❌ posizioni_anomale: solo luglio (posizione 6) supera il doppio del mese prima"
        assert trova_anomalie(letture) == [6], "❌ trova_anomalie con il default deve dare lo stesso risultato del ciclo: [6]"
        assert trova_anomalie([100, 120, 250, 240], fattore=1.5) == [2], "❌ fattore=1.5: solo 250 supera 120 per 1,5"
        assert trova_anomalie([100, 100, 100]) == [], "❌ Senza anomalie la funzione restituisce una lista vuota"
    """
    perche_anomalie = "Il ciclo parte da 1 perché la prima lettura non ha una precedente. La funzione è lo stesso ciclo con `fattore` al posto del 2 fisso: cambiare il criterio diventa cambiare un argomento."
    suggerimento_anomalie = "Qui il `for` gira sulle posizioni perché ci serve la lettura prima: `letture[i - 1]` è la precedente di `letture[i]`."

    nb.esercizio(
        aula="base",
        titolo="Letture anomale",
        scenario=scenario_anomalie,
        richiesta=richiesta_anomalie,
        suggerimento=suggerimento_anomalie,
        starter=starter_anomalie,
        soluzione=soluzione_anomalie,
        verifica=verifica_anomalie,
        perche=perche_anomalie,
        passo_in_piu=dict(
            testo="""
                Aggiungi a `trova_anomalie` un terzo parametro `anche_cali=False`. Quando è `True`, segnala
                anche le letture che scendono sotto la precedente divisa per `fattore` (il mese dopo lo
                zero di troppo). Con i default il risultato non deve cambiare.
            """,
            starter='''
                def trova_anomalie(letture, fattore=2, anche_cali=False):
                    """Posizioni delle letture anomale rispetto alla precedente."""
                    ...


                print(trova_anomalie(letture), trova_anomalie(letture, anche_cali=True))
            ''',
            soluzione='''
                def trova_anomalie(letture, fattore=2, anche_cali=False):
                    """Posizioni delle letture anomale rispetto alla precedente."""
                    anomalie = []
                    for i in range(1, len(letture)):
                        salto = letture[i] > fattore * letture[i - 1]
                        calo = anche_cali and letture[i] < letture[i - 1] / fattore
                        if salto or calo:
                            anomalie.append(i)
                    return anomalie


                print(trova_anomalie(letture), trova_anomalie(letture, anche_cali=True))
            ''',
            verifica="""
                assert trova_anomalie(letture) == [6], "❌ Con i default il risultato deve restare [6]"
                assert trova_anomalie(letture, anche_cali=True) == [6, 7], "❌ anche_cali=True deve segnalare anche agosto (posizione 7)"
            """,
        ),
    )
    nb.esercizio(
        aula="avanzata",
        titolo="Letture anomale",
        scenario=scenario_anomalie,
        richiesta=richiesta_anomalie,
        suggerimento=suggerimento_anomalie,
        starter=starter_anomalie,
        soluzione=soluzione_anomalie,
        verifica=verifica_anomalie,
        perche=perche_anomalie,
        passo_in_piu=dict(
            testo="""
                Riscrivi il ciclo come una comprehension in `posizioni_comp` (stesso risultato di
                `posizioni_anomale`). Poi costruisci `classifica`: le coppie (mese, lettura) ordinate dalla
                lettura più alta alla più bassa, con `sorted` e una `lambda` su `zip(mesi, letture)`.
            """,
            starter="""
                posizioni_comp = [i for i in range(1, len(letture)) if ...]
                classifica = sorted(zip(mesi, letture), key=..., reverse=True)

                print(posizioni_comp)
                print(classifica[:3])
            """,
            soluzione="""
                posizioni_comp = [i for i in range(1, len(letture)) if letture[i] > 2 * letture[i - 1]]
                classifica = sorted(zip(mesi, letture), key=lambda coppia: coppia[1], reverse=True)

                print(posizioni_comp)
                print(classifica[:3])
            """,
            verifica="""
                assert posizioni_comp == [6], "❌ posizioni_comp: la condizione dell'if va dopo il for, dentro le quadre"
                assert classifica[0] == ("lug", 3150), "❌ classifica: ordina sulla lettura (secondo elemento della coppia), decrescente"
                assert classifica[-1] == ("apr", 290), "❌ classifica: l'ultima coppia deve essere il mese con la lettura più bassa"
            """,
        ),
    )
    nb.esercizio(
        titolo="Chi fa più notti",
        bis=True,
        scenario="""
            Al pronto intervento i turni del mese sono in una lista di coppie (operatore, turno). La
            responsabile vuole sapere quante notti ha fatto ciascuno e chi ne ha fatte di più, per
            riequilibrare il mese prossimo. Oggi le conta sul foglio stampato, con la matita.
        """,
        richiesta="""
            1. Con un `for` sulle coppie, costruisci il dizionario `notti`: l'operatore come chiave, il
               numero dei suoi turni `"notte"` come valore.
            2. Trova in `chi_piu_notti` il nome con il valore più alto, scorrendo `notti.items()`.
            3. Chiudi il conteggio in `conta_turni(turni, tipo="notte")`, che restituisce il dizionario
               per il tipo di turno indicato.
        """,
        suggerimento="`notti.get(nome, 0) + 1` aggiorna il conteggio anche se il nome non c'è ancora.",
        starter='''
            turni = [
                ("Anna", "notte"), ("Luca", "mattina"), ("Anna", "notte"), ("Marco", "notte"),
                ("Luca", "notte"), ("Anna", "pomeriggio"), ("Marco", "notte"), ("Anna", "notte"),
            ]

            notti = {}
            for nome, turno in turni:
                ...

            chi_piu_notti = None
            massimo = 0
            ...


            def conta_turni(turni, tipo="notte"):
                """Dizionario operatore -> numero di turni del tipo indicato."""
                ...


            print(notti, chi_piu_notti, conta_turni(turni, tipo="mattina"))
        ''',
        soluzione='''
            turni = [
                ("Anna", "notte"), ("Luca", "mattina"), ("Anna", "notte"), ("Marco", "notte"),
                ("Luca", "notte"), ("Anna", "pomeriggio"), ("Marco", "notte"), ("Anna", "notte"),
            ]

            notti = {}
            for nome, turno in turni:
                if turno == "notte":
                    notti[nome] = notti.get(nome, 0) + 1

            chi_piu_notti = None
            massimo = 0
            for nome, numero in notti.items():
                if numero > massimo:
                    chi_piu_notti = nome
                    massimo = numero


            def conta_turni(turni, tipo="notte"):
                """Dizionario operatore -> numero di turni del tipo indicato."""
                conteggio = {}
                for nome, turno in turni:
                    if turno == tipo:
                        conteggio[nome] = conteggio.get(nome, 0) + 1
                return conteggio


            print(notti, chi_piu_notti, conta_turni(turni, tipo="mattina"))
        ''',
        verifica="""
            assert notti == {"Anna": 3, "Luca": 1, "Marco": 2}, "❌ notti: conta solo i turni 'notte', uno per coppia"
            assert chi_piu_notti == "Anna", "❌ chi_piu_notti: il nome con il valore più alto in notti"
            assert conta_turni(turni) == notti, "❌ conta_turni con il default deve dare lo stesso dizionario di notti"
            assert conta_turni(turni, tipo="mattina") == {"Luca": 1}, "❌ conta_turni: tipo deve filtrare il turno"
        """,
        perche="`.get(nome, 0)` evita l'`if nome in notti` prima di sommare. Il massimo si trova con lo stesso schema del totale: una variabile che parte da zero e si aggiorna solo quando il giro corrente la batte.",
    )
    return nb
