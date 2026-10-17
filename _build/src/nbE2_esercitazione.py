"""E2 · Esercitazione 2: un'ora di domande ed esercizi sul blocco 2 (notebook 04-06), nel formato di ottobre 2026."""

from nbkit import Cella, Notebook

FILE_CSV = "../Dati/letture_pod_2025.csv"
LEGGI_CSV = f'letture = pd.read_csv("{FILE_CSV}", sep=";", decimal=",", encoding="latin-1")'


def esercizio_due_aule(nb: Notebook, titolo: str, scenario: str, *, richiesta: str, soluzione: str, verifica: str | None,
                       starter_base: str, starter_avanzata: str, suggerimenti_base: list[str] | None = None,
                       suggerimento_avanzata: str | None = None, richiesta_avanzata: str | None = None,
                       soluzione_avanzata: str | None = None, verifica_avanzata: str | None = None,
                       facoltativo: bool = False) -> None:
    """Lo stesso esercizio per le due aule, come gli step del capstone: stesso titolo e scenario.

    Nella Base lo starter è guidato e i suggerimenti sono due (prima l'idea, poi il nome del metodo); nell'Avanzata
    lo starter è quasi vuoto, c'è al massimo un suggerimento e la consegna può avere un passo in più, con la sua
    soluzione e la sua verifica.
    """
    nb.esercizio(
        titolo=titolo, scenario=scenario, richiesta=richiesta, starter=starter_base, soluzione=soluzione,
        verifica=verifica, suggerimenti=suggerimenti_base, facoltativo=facoltativo, aula="base",
    )
    nb.esercizio(
        titolo=titolo, scenario=scenario, richiesta=richiesta_avanzata or richiesta, starter=starter_avanzata,
        soluzione=soluzione_avanzata or soluzione, verifica=verifica_avanzata or verifica,
        suggerimenti=[suggerimento_avanzata] if suggerimento_avanzata else None, facoltativo=facoltativo,
        aula="avanzata",
    )


def costruisci() -> Notebook:
    nb = Notebook(
        num="E2",
        file="Esercitazione_2",
        titolo="Esercitazione 2",
        blocco=2,
        giornata=1,
        intento="Questa esercitazione chiude il blocco 2 con alcune domande e una serie di esercizi su cicli, funzioni e lettura dei dati da CSV, Excel e database.",
        obiettivi={
            "base": [
                "usare cicli, condizioni e funzioni con valori predefiniti su un caso di tutti i giorni",
                "leggere un CSV in formato italiano e i fogli di un file Excel con i parametri giusti",
                "caricare una tabella da un database SQLite e controllarne righe e totali",
            ],
            "avanzata": [
                "usare cicli, condizioni e funzioni con valori predefiniti su un caso di tutti i giorni",
                "leggere un CSV in formato italiano, i fogli di un file Excel e una tabella da un database",
                "raccogliere in una funzione la chiamata a un'API, con un file di riserva quando manca la rete",
            ],
        },
        tempo=60,
        dati={
            "base": ["letture_pod_2025.csv", "bolletta_esempio.xlsx", "utility.db"],
            "avanzata": ["letture_pod_2025.csv", "bolletta_esempio.xlsx", "utility.db", "fallback/lombardia_sensori.json"],
        },
        soluzioni_a_richiesta=True,
    )

    # ------------------------------------------------------------------ come funziona l'ora
    nb.md("""
        Questa esercitazione chiude la giornata e riprende quello che abbiamo visto nei notebook 04-06. Hai 45
        minuti per lavorare sugli esercizi, poi li guardiamo insieme. Si comincia con cinque domande di riepilogo e si
        prosegue con cinque esercizi: i primi due riguardano le spese di un mese, i tre successivi i dati dei POD che
        usiamo da pandas in poi. Ogni esercizio legge i propri dati, quindi se ti blocchi su uno puoi passare al
        successivo.
    """)
    nb.md("""
        Gli esercizi che seguono sono facoltativi: se hai finito i primi cinque, puoi continuare con questi, che
        applicano in modo diretto quello che abbiamo appena visto. La sfida finale è un esercizio libero, senza
        verifica. Anche sotto questi esercizi c'è la cella `soluzione`.
    """)

    # ------------------------------------------------------------------ 1
    nb.sezione("Domande", intro="""
        Le domande che seguono riguardano i notebook 04-06. Conviene rispondere a mente, o scrivendo la risposta su
        un foglio, e solo dopo aprire la risposta; quando la spiegazione non basta, si può copiare il codice in una
        cella ed eseguirlo.
    """)
    nb.domanda(
        """
        Cosa stampa questa cella?

        ```python
        totale = 0
        for n in [4, 7, 2, 9]:
            if n % 2 == 1:
                totale = totale + n
        print(totale)
        ```
        """,
        """
        Stampa `16`. Il ciclo aggiunge al totale soltanto i numeri dispari, cioè quelli per cui il resto della
        divisione per 2 vale 1, quindi 7 e 9. Il `print` sta fuori dal ciclo, perché non è indentato sotto il `for`,
        e viene eseguito una volta sola, alla fine.
        """,
    )
    nb.domanda(
        """
        Con la funzione qui sotto, che cosa restituiscono `biglietto(8)` e `biglietto(30, prezzo=15)`?

        ```python
        def biglietto(eta, prezzo=12):
            if eta < 12:
                return prezzo / 2
            return prezzo
        ```
        """,
        """
        `biglietto(8)` restituisce `6.0`. L'argomento `prezzo` non è indicato, quindi vale 12, e poiché l'età è
        minore di 12 la funzione restituisce metà del prezzo, un `float` perché viene da una divisione con `/`.
        `biglietto(30, prezzo=15)` restituisce invece `15`, perché il valore passato prende il posto di quello
        predefinito e la condizione sull'età è falsa.
        """,
    )
    nb.domanda(
        "Quale errore dà la riga `int(\"12,5\")`, e come si ottiene il numero 12.5?",
        """
        Dà `ValueError: invalid literal for int() with base 10: '12,5'`. Il tipo dell'argomento è giusto, perché
        `int` accetta un testo, ma il valore non rappresenta un numero intero, e per di più contiene la virgola, che
        Python non riconosce come separatore decimale. Per ottenere 12.5 si scrive il punto al posto della virgola
        e si usa `float("12.5")`.
        """,
    )
    nb.domanda(
        """
        Con `df = pd.DataFrame({"prodotto": ["pane", "latte"], "prezzo": [2.5, 1.2]})`, che cosa restituisce
        `type(df["prezzo"])`?
        """,
        """
        Restituisce `<class 'pandas.Series'>`. Selezionando una sola colonna di un DataFrame con il suo nome tra
        parentesi quadre si ottiene una Series, che contiene i valori della colonna e conserva l'indice del
        DataFrame.
        """,
    )
    nb.domanda(
        """
        A che cosa serve `sep=";"` in `pd.read_csv`, e che cosa otteniamo se leggiamo `letture_pod_2025.csv`
        senza indicarlo?
        """,
        """
        Il parametro `sep` indica il carattere che separa le colonne nel file. Senza `sep=";"` pandas cerca la
        virgola, che in questo file compare soltanto come separatore dei decimali, quindi le colonne non vengono
        separate. La riga di intestazione diventa il nome di un'unica colonna, `pod;cliente;data;fascia;kwh`, e
        il DataFrame che si ottiene non ha le colonne `pod`, `fascia` e `kwh` su cui lavorare.
        """,
    )

    # ------------------------------------------------------------------ 2
    nb.sezione("Esercizi")
    nb.md("""
        I primi due esercizi riprendono i cicli, le condizioni e le funzioni del notebook 04 su un caso di tutti i
        giorni, le spese personali del mese di ottobre. Le spese sono in euro e sono scritte con il punto decimale,
        come vuole Python.
    """)

    # E2.1 ------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Le spese sopra soglia",
        scenario="""
            Nella lista `spese` abbiamo annotato quanto abbiamo speso in dodici giornate di ottobre. Vogliamo sapere
            in quanti giorni abbiamo superato i 50 euro e quanto abbiamo speso in tutto.
        """,
        richiesta="""
            1. Con un ciclo `for` sulla lista e un `if` al suo interno, aggiungi alla lista `sopra_soglia` le spese
               maggiori di 50 euro.
            2. Salva in `quante` il numero di spese sopra la soglia.
            3. Salva in `totale` la somma di tutte le spese, calcolata con la funzione `sum`.

            Le spese sopra i 50 euro sono cinque, perché la spesa di 50.0 euro non supera la soglia, e il totale
            del mese è di 578.8 euro.
        """,
        richiesta_avanzata="""
            1. Con un ciclo `for` sulla lista e un `if` al suo interno, aggiungi alla lista `sopra_soglia` le spese
               maggiori di 50 euro.
            2. Nello stesso ciclo, senza scriverne un secondo, accumula in `totale_sopra` la somma delle sole spese
               sopra la soglia.
            3. Salva in `quante` il numero di spese sopra la soglia e in `totale` la somma di tutte le spese.

            Le spese sopra i 50 euro sono cinque, perché la spesa di 50.0 euro non supera la soglia, e sommano
            397.7 euro; il totale del mese è di 578.8 euro.
        """,
        suggerimenti_base=[
            """
            Prima del ciclo la lista `sopra_soglia` è vuota. A ogni passo il ciclo guarda una spesa e, se supera la
            soglia, la aggiunge alla lista; il numero delle spese sopra la soglia è quindi la lunghezza della lista
            alla fine del ciclo.
            """,
            """
            Dentro il ciclo servono la condizione `if spesa > soglia:` e il metodo `append()`, come nell'esempio dei
            giorni di sole del notebook 04. La lunghezza della lista si ottiene con `len(sopra_soglia)`.
            """,
        ],
        suggerimento_avanzata="""
            Il totale delle spese sopra la soglia parte da 0 prima del ciclo e cresce nello stesso blocco dell'`if`
            in cui si chiama `append()`, perché va aggiornato soltanto quando la condizione è vera.
        """,
        starter_base="""
            spese = [12.5, 64.0, 8.9, 51.2, 23.0, 120.0, 45.5, 7.8, 89.9, 50.0, 33.4, 72.6]
            soglia = 50

            sopra_soglia = []
            for spesa in spese:
                if ...:
                    ...

            quante = ...
            totale = ...

            print(sopra_soglia)  # Output: [64.0, 51.2, 120.0, 89.9, 72.6]
            print(quante)        # Output: 5
            print(totale)        # Output: 578.8
        """,
        starter_avanzata="""
            spese = [12.5, 64.0, 8.9, 51.2, 23.0, 120.0, 45.5, 7.8, 89.9, 50.0, 33.4, 72.6]
            soglia = 50

            # sopra_soglia, totale_sopra, quante, totale
        """,
        soluzione="""
            spese = [12.5, 64.0, 8.9, 51.2, 23.0, 120.0, 45.5, 7.8, 89.9, 50.0, 33.4, 72.6]
            soglia = 50

            sopra_soglia = []
            for spesa in spese:
                if spesa > soglia:
                    sopra_soglia.append(spesa)

            quante = len(sopra_soglia)
            totale = sum(spese)

            print(sopra_soglia)  # Output: [64.0, 51.2, 120.0, 89.9, 72.6]
            print(quante)        # Output: 5
            print(totale)        # Output: 578.8
        """,
        soluzione_avanzata="""
            spese = [12.5, 64.0, 8.9, 51.2, 23.0, 120.0, 45.5, 7.8, 89.9, 50.0, 33.4, 72.6]
            soglia = 50

            sopra_soglia = []
            totale_sopra = 0
            for spesa in spese:
                if spesa > soglia:
                    sopra_soglia.append(spesa)
                    totale_sopra = totale_sopra + spesa

            quante = len(sopra_soglia)
            totale = sum(spese)

            print(sopra_soglia)              # Output: [64.0, 51.2, 120.0, 89.9, 72.6]
            print(quante, round(totale_sopra, 2), totale)  # Output: 5 397.7 578.8
        """,
        verifica="""
            assert sopra_soglia == [64.0, 51.2, 120.0, 89.9, 72.6], "❌ sopra_soglia: tieni le spese maggiori di 50, nell'ordine della lista"
            assert quante == 5, "❌ Le spese sopra i 50 euro sono 5: la spesa di 50.0 non conta"
            assert round(totale, 2) == 578.8, "❌ totale: somma tutta la lista con sum(spese)"
        """,
        verifica_avanzata="""
            assert sopra_soglia == [64.0, 51.2, 120.0, 89.9, 72.6] and quante == 5, "❌ sopra_soglia: tieni le 5 spese maggiori di 50"
            assert round(totale_sopra, 2) == 397.7, "❌ totale_sopra: somma solo le spese sopra la soglia, dentro l'if"
            assert round(totale, 2) == 578.8, "❌ totale: somma tutta la lista con sum(spese)"
        """,
    )

    # E2.2 ------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Lo sconto come funzione",
        scenario="""
            Il negozio sotto casa applica di solito uno sconto del 10%, ma in alcune giornate lo alza. Una funzione
            con un valore predefinito per lo sconto calcola il prezzo finale in entrambi i casi.
        """,
        richiesta="""
            1. Completa la funzione `prezzo_scontato(prezzo, sconto=10)`, che restituisce il prezzo dopo lo sconto,
               espresso in percentuale, arrotondato a due decimali.
            2. Scrivi sotto il `def` una docstring di una riga che dica che cosa fa la funzione.
            3. Chiama la funzione su un prezzo di 49.90 euro, prima senza indicare lo sconto, salvando il risultato
               in `normale`, e poi con uno sconto del 30%, salvandolo in `promozione`.

            Con lo sconto predefinito il prezzo diventa 44.91 euro, con lo sconto del 30% diventa 34.93 euro.
        """,
        richiesta_avanzata="""
            1. Scrivi la funzione `prezzo_scontato(prezzo, sconto=10, arrotonda=2)`, con una docstring di una riga,
               che restituisce il prezzo dopo lo sconto, espresso in percentuale, arrotondato al numero di decimali
               indicato da `arrotonda`.
            2. Chiama la funzione su un prezzo di 49.90 euro, prima senza indicare lo sconto, salvando il risultato
               in `normale`, e poi con uno sconto del 30%, salvandolo in `promozione`.
            3. Salva in `intero` il prezzo con lo sconto del 30% arrotondato all'euro, cioè con `arrotonda=0`.

            Con lo sconto predefinito il prezzo diventa 44.91 euro, con lo sconto del 30% diventa 34.93 euro, che
            arrotondati all'euro sono 35.0.
        """,
        suggerimenti_base=[
            """
            Il prezzo scontato è il prezzo meno la sua parte di sconto, cioè `prezzo * (1 - sconto / 100)`. La
            funzione calcola questo valore, lo arrotonda e lo restituisce con `return`.
            """,
            """
            L'arrotondamento si fa con `round(valore, 2)`, la funzione di cui abbiamo letto la firma nel notebook 05.
            Nella seconda chiamata lo sconto si passa per nome, come in `prezzo_scontato(49.90, sconto=30)`.
            """,
        ],
        suggerimento_avanzata="""
            Il secondo argomento di `round` può essere il parametro stesso, come in `round(valore, arrotonda)`.
        """,
        starter_base="""
            def prezzo_scontato(prezzo, sconto=10):
                ...
                return ...


            normale = ...
            promozione = ...

            print(normale)     # Output: 44.91
            print(promozione)  # Output: 34.93
        """,
        starter_avanzata="""
            # prezzo_scontato(prezzo, sconto=10, arrotonda=2), normale, promozione, intero
        """,
        soluzione="""
            def prezzo_scontato(prezzo, sconto=10):
                \"\"\"Prezzo dopo uno sconto in percentuale, arrotondato a due decimali.\"\"\"
                return round(prezzo * (1 - sconto / 100), 2)


            normale = prezzo_scontato(49.90)
            promozione = prezzo_scontato(49.90, sconto=30)

            print(normale)     # Output: 44.91
            print(promozione)  # Output: 34.93
        """,
        soluzione_avanzata="""
            def prezzo_scontato(prezzo, sconto=10, arrotonda=2):
                \"\"\"Prezzo dopo uno sconto in percentuale, arrotondato a `arrotonda` decimali.\"\"\"
                return round(prezzo * (1 - sconto / 100), arrotonda)


            normale = prezzo_scontato(49.90)
            promozione = prezzo_scontato(49.90, sconto=30)
            intero = prezzo_scontato(49.90, sconto=30, arrotonda=0)

            print(normale, promozione, intero)  # Output: 44.91 34.93 35.0
        """,
        verifica="""
            assert prezzo_scontato.__doc__, "❌ Manca la docstring sotto il def"
            assert normale == 44.91 and prezzo_scontato(80) == 72.0, "❌ Con lo sconto predefinito 49.90 diventa 44.91"
            assert promozione == 34.93, "❌ promozione: con sconto=30 il prezzo è 34.93"
        """,
        verifica_avanzata="""
            assert prezzo_scontato.__doc__, "❌ Manca la docstring sotto il def"
            assert normale == 44.91 and promozione == 34.93, "❌ normale vale 44.91 e promozione 34.93"
            assert intero == 35 and prezzo_scontato(80) == 72.0, "❌ intero: con arrotonda=0 il prezzo è 35.0"
        """,
    )

    nb.md("""
        I tre esercizi successivi lavorano sui dati di esempio di una piccola società di vendita di energia, che
        riceve i consumi dei clienti in tre forme diverse: un CSV dal distributore, un file Excel con i dati delle
        bollette e un database SQLite. Un POD è il codice che identifica un punto di prelievo dell'energia
        elettrica, cioè il contatore di un cliente.
    """)

    # E2.3 ------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Il CSV del distributore",
        scenario="""
            Il distributore ci manda i consumi mensili del 2025 di sei POD, divisi per fascia oraria, nel file
            `letture_pod_2025.csv`, esportato da un Excel configurato in italiano come quello letto nel notebook 06.
        """,
        richiesta="""
            1. Leggi `../Dati/letture_pod_2025.csv` nel DataFrame `letture`, con i parametri adatti al formato
               italiano.
            2. Controlla con `info()` che la colonna `kwh` sia di tipo `float64`, cioè numerica.
            3. Salva in `righe` il numero di righe del DataFrame e in `totale_kwh` la somma della colonna `kwh`.

            Il file ha 216 righe e il consumo totale è di circa 134507.7 kWh.
        """,
        richiesta_avanzata="""
            1. Leggi `../Dati/letture_pod_2025.csv` nel DataFrame `letture`, con i parametri adatti al formato
               italiano e tenendo soltanto le colonne `pod`, `fascia` e `kwh`.
            2. Controlla con `info()` che la colonna `kwh` sia di tipo `float64`, cioè numerica.
            3. Salva in `righe` il numero di righe del DataFrame e in `totale_kwh` la somma della colonna `kwh`.

            Il DataFrame ha 216 righe e 3 colonne, e il consumo totale è di circa 134507.7 kWh.
        """,
        suggerimenti_base=[
            """
            Un CSV salvato da Excel in italiano differisce da quello standard per tre aspetti, cioè il carattere che
            separa le colonne, quello che separa i decimali e l'encoding, e a ciascuno corrisponde un parametro di
            `read_csv`. Il numero di righe di un DataFrame si ottiene come la lunghezza di una lista.
            """,
            """
            I tre parametri sono `sep=";"`, `decimal=","` ed `encoding="latin-1"`. Le righe si contano con
            `len(letture)` e la somma di una colonna si calcola con `letture["kwh"].sum()`.
            """,
        ],
        suggerimento_avanzata="""
            Il parametro `usecols` riceve la lista dei nomi delle colonne da leggere, come in
            `usecols=["pod", "fascia", "kwh"]`.
        """,
        starter_base=f"""
            import pandas as pd

            letture = pd.read_csv("{FILE_CSV}", sep=..., decimal=..., encoding=...)
            letture.info()

            righe = ...
            totale_kwh = ...

            print(righe, round(totale_kwh, 1))  # Output: 216 134507.7
        """,
        starter_avanzata="""
            import pandas as pd

            # letture (solo pod, fascia e kwh), righe, totale_kwh
        """,
        soluzione=f"""
            import pandas as pd

            {LEGGI_CSV}
            letture.info()

            righe = len(letture)
            totale_kwh = letture["kwh"].sum()

            print(righe, round(totale_kwh, 1))  # Output: 216 134507.7
        """,
        soluzione_avanzata=f"""
            import pandas as pd

            letture = pd.read_csv(
                "{FILE_CSV}",
                sep=";", decimal=",", encoding="latin-1",
                usecols=["pod", "fascia", "kwh"],
            )
            letture.info()

            righe = len(letture)
            totale_kwh = letture["kwh"].sum()

            print(righe, round(totale_kwh, 1))  # Output: 216 134507.7
        """,
        verifica="""
            assert letture["kwh"].dtype == "float64", "❌ kwh non è numerica: manca decimal=','"
            assert righe == 216, "❌ Il file ha 216 righe: contale con len(letture)"
            assert round(totale_kwh, 1) == 134507.7, "❌ totale_kwh: somma la colonna kwh"
        """,
        verifica_avanzata="""
            assert list(letture.columns) == ["pod", "fascia", "kwh"], "❌ Con usecols leggi solo pod, fascia e kwh"
            assert letture["kwh"].dtype == "float64" and righe == 216, "❌ kwh deve essere numerica e le righe 216"
            assert round(totale_kwh, 1) == 134507.7, "❌ totale_kwh: somma la colonna kwh"
        """,
    )

    # E2.4 ------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="I fogli della bolletta",
        scenario="""
            Il file `bolletta_esempio.xlsx` raccoglie in tre fogli i dati delle bollette degli stessi sei POD: i
            consumi mensili per fascia nel foglio `Consumi`, i prezzi nel foglio `Listino` e i clienti nel foglio
            `Anagrafica`. Per calcolare una bolletta ci servono i consumi e il listino.
        """,
        richiesta="""
            1. Leggi il foglio `Consumi` nel DataFrame `consumi` e il foglio `Listino` nel DataFrame `listino`,
               indicando a `read_excel` il nome del foglio.
            2. Salva in `righe_consumi` e `righe_listino` il numero di righe dei due DataFrame.
            3. Salva in `prezzo_f1` il prezzo in euro al kWh della fascia F1, che si trova nella prima riga del
               listino, nella colonna `eur_kwh`.

            Il foglio dei consumi ha 72 righe, una per POD e per mese, il listino ne ha 3, una per fascia, e il
            prezzo della fascia F1 è di 0.21 euro al kWh.
        """,
        richiesta_avanzata="""
            1. Leggi il foglio `Consumi` nel DataFrame `consumi` e il foglio `Listino` nel DataFrame `listino`.
            2. Salva in `righe_consumi` e `righe_listino` il numero di righe dei due DataFrame e in `prezzo_f1` il
               prezzo in euro al kWh della fascia F1, preso dalla colonna `eur_kwh` del listino.
            3. Leggi poi tutti i fogli del file con una sola chiamata nel dizionario `fogli`, e salva in
               `nomi_fogli` la lista dei nomi dei fogli.

            Il foglio dei consumi ha 72 righe, il listino ne ha 3, il prezzo della fascia F1 è di 0.21 euro al kWh
            e i fogli sono `Consumi`, `Listino` e `Anagrafica`, in quest'ordine.
        """,
        suggerimenti_base=[
            """
            Il parametro `sheet_name` di `read_excel` sceglie il foglio da leggere, quindi servono due letture dello
            stesso file, una per foglio. Il prezzo si ottiene in due passi: prima si seleziona la colonna, che è una
            Series, e poi il suo primo elemento.
            """,
            """
            La prima lettura è `pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Consumi")` e la seconda
            è uguale, con `"Listino"`. Il primo elemento della colonna si legge con le parentesi quadre, come
            nella Series del notebook 06: `listino["eur_kwh"][0]`.
            """,
        ],
        suggerimento_avanzata="""
            Con `sheet_name=None` la funzione `read_excel` restituisce un dizionario che ha come chiavi i nomi dei
            fogli, e `list(fogli.keys())` li raccoglie in una lista.
        """,
        starter_base="""
            import pandas as pd

            consumi = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name=...)
            listino = ...

            righe_consumi = ...
            righe_listino = ...
            prezzo_f1 = ...

            print(righe_consumi, righe_listino, prezzo_f1)  # Output: 72 3 0.21
        """,
        starter_avanzata="""
            import pandas as pd

            # consumi, listino, righe_consumi, righe_listino, prezzo_f1, fogli, nomi_fogli
        """,
        soluzione="""
            import pandas as pd

            consumi = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Consumi")
            listino = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Listino")

            righe_consumi = len(consumi)
            righe_listino = len(listino)
            prezzo_f1 = listino["eur_kwh"][0]

            print(righe_consumi, righe_listino, prezzo_f1)  # Output: 72 3 0.21
        """,
        soluzione_avanzata="""
            import pandas as pd

            consumi = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Consumi")
            listino = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Listino")

            righe_consumi = len(consumi)
            righe_listino = len(listino)
            prezzo_f1 = listino["eur_kwh"][0]

            fogli = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name=None)
            nomi_fogli = list(fogli.keys())

            print(righe_consumi, righe_listino, prezzo_f1)  # Output: 72 3 0.21
            print(nomi_fogli)                               # Output: ['Consumi', 'Listino', 'Anagrafica']
        """,
        verifica="""
            assert righe_consumi == 72 and list(consumi.columns) == ["pod", "mese", "F1", "F2", "F3"], "❌ consumi: leggi il foglio Consumi"
            assert righe_listino == 3, "❌ Il listino ha 3 righe, una per fascia"
            assert prezzo_f1 == 0.21, "❌ prezzo_f1: è il primo valore della colonna eur_kwh del listino"
        """,
        verifica_avanzata="""
            assert righe_consumi == 72 and righe_listino == 3, "❌ Il foglio Consumi ha 72 righe e il Listino 3"
            assert prezzo_f1 == 0.21, "❌ prezzo_f1: il prezzo della fascia F1 è 0.21"
            assert nomi_fogli == ["Consumi", "Listino", "Anagrafica"], "❌ nomi_fogli: leggi tutti i fogli con sheet_name=None"
        """,
    )

    # E2.5 ------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="La tabella dal database",
        scenario="""
            Le letture giornaliere di marzo 2025 di trenta POD stanno nella tabella `letture` del database SQLite
            `utility.db`, che ha le colonne `pod`, `data` e `kwh`.
        """,
        richiesta="""
            1. Apri la connessione a `../Dati/utility.db` con `sqlite3.connect` e salvala in `con`.
            2. Leggi tutta la tabella `letture` nel DataFrame `letture_db` con `pd.read_sql`, poi chiudi la
               connessione.
            3. Salva in `n_letture` il numero di righe e in `kwh_marzo` la somma della colonna `kwh`.

            La tabella ha 930 righe, cioè 31 giorni per 30 POD, e il consumo complessivo di marzo è di 69880.1 kWh.
        """,
        richiesta_avanzata="""
            1. Apri la connessione a `../Dati/utility.db` e leggi tutta la tabella `letture` nel DataFrame
               `letture_db`.
            2. Con una seconda query, che usa la clausola `WHERE`, leggi nel DataFrame `letture_pod` soltanto le
               righe del POD `IT001E10087109`, e poi chiudi la connessione.
            3. Salva in `n_letture` il numero di righe di `letture_db` e in `kwh_marzo` la somma della sua colonna
               `kwh`.

            La tabella ha 930 righe, cioè 31 giorni per 30 POD, e il consumo complessivo di marzo è di 69880.1 kWh;
            il POD `IT001E10087109` ha 31 letture.
        """,
        suggerimenti_base=[
            """
            Il lavoro con un database segue sempre tre passi: si apre la connessione, si eseguono le query e alla
            fine si chiude la connessione. La query che legge una tabella intera usa l'asterisco al posto
            dell'elenco delle colonne.
            """,
            """
            La connessione si apre con `sqlite3.connect("../Dati/utility.db")` e la query è
            `"SELECT * FROM letture"`. La somma della colonna si calcola con `letture_db["kwh"].sum()`.
            """,
        ],
        suggerimento_avanzata="""
            Nella query il codice del POD va tra apici singoli, come in `WHERE pod = 'IT001E10087109'`.
        """,
        starter_base="""
            import sqlite3

            import pandas as pd

            con = ...
            letture_db = pd.read_sql(..., con)
            con.close()

            n_letture = ...
            kwh_marzo = ...

            print(n_letture, round(kwh_marzo, 1))  # Output: 930 69880.1
        """,
        starter_avanzata="""
            import sqlite3

            import pandas as pd

            # con, letture_db, letture_pod, n_letture, kwh_marzo
        """,
        soluzione="""
            import sqlite3

            import pandas as pd

            con = sqlite3.connect("../Dati/utility.db")
            letture_db = pd.read_sql("SELECT * FROM letture", con)
            con.close()

            n_letture = len(letture_db)
            kwh_marzo = letture_db["kwh"].sum()

            print(n_letture, round(kwh_marzo, 1))  # Output: 930 69880.1
        """,
        soluzione_avanzata="""
            import sqlite3

            import pandas as pd

            con = sqlite3.connect("../Dati/utility.db")
            letture_db = pd.read_sql("SELECT * FROM letture", con)
            letture_pod = pd.read_sql("SELECT * FROM letture WHERE pod = 'IT001E10087109'", con)
            con.close()

            n_letture = len(letture_db)
            kwh_marzo = letture_db["kwh"].sum()

            print(n_letture, round(kwh_marzo, 1), len(letture_pod))  # Output: 930 69880.1 31
        """,
        verifica="""
            assert list(letture_db.columns) == ["pod", "data", "kwh"], "❌ Leggi tutta la tabella letture con SELECT *"
            assert n_letture == 930, "❌ La tabella letture ha 930 righe"
            assert round(kwh_marzo, 1) == 69880.1, "❌ kwh_marzo: somma la colonna kwh di letture_db"
        """,
        verifica_avanzata="""
            assert n_letture == 930 and list(letture_db.columns) == ["pod", "data", "kwh"], "❌ letture_db: leggi tutta la tabella letture"
            assert round(kwh_marzo, 1) == 69880.1, "❌ kwh_marzo: somma la colonna kwh di letture_db"
            assert len(letture_pod) == 31 and set(letture_pod["pod"]) == {"IT001E10087109"}, "❌ letture_pod: filtra con WHERE pod = '...'"
        """,
    )

    # ------------------------------------------------------------------ facoltativi
    nb.md("""
        Gli esercizi che seguono sono facoltativi: se hai finito i primi cinque, puoi continuare con questi, che
        applicano in modo diretto quello che abbiamo appena visto. La sfida finale è un esercizio libero, senza
        verifica. Anche sotto questi esercizi c'è la cella `soluzione`.
    """, aula="base")
    nb.md("""
        Gli esercizi che seguono sono facoltativi: se hai finito i primi cinque, puoi continuare con questi, che
        applicano in modo diretto quello che abbiamo appena visto. La sfida finale è un esercizio libero, senza
        verifica. Anche sotto questi esercizi c'è la cella `soluzione`.
    """, aula="avanzata")

    # E2.6 ------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Il riepilogo per mese",
        scenario="""
            Le spese del primo trimestre sono raccolte in un dizionario che associa a ogni mese la lista delle spese
            di quel mese. Vogliamo un secondo dizionario con il totale di ciascun mese.
        """,
        richiesta="""
            1. Con un ciclo `for` su `spese_mesi.items()`, assegna a `totali[mese]` la somma delle spese del mese,
               arrotondata a due decimali.
            2. Salva in `totale_trimestre` la somma dei tre totali.

            Il dizionario `totali` è `{'gennaio': 161.7, 'febbraio': 108.7, 'marzo': 187.1}` e il totale del
            trimestre è di 457.5 euro.
        """,
        suggerimenti_base=[
            """
            A ogni passo il ciclo su `.items()` fornisce il nome del mese e la sua lista di spese, e la riga dentro
            il ciclo assegna alla chiave `mese` di `totali` la somma della lista, ottenuta con `sum` e arrotondata
            con `round`. I tre totali sono i valori del dizionario, cioè `totali.values()`.
            """,
        ],
        starter_base="""
            spese_mesi = {
                "gennaio": [45.0, 12.3, 80.5, 23.9],
                "febbraio": [60.0, 15.5, 33.2],
                "marzo": [22.4, 95.0, 41.1, 18.7, 9.9],
            }

            totali = {}
            for mese, lista in ...:
                totali[mese] = ...

            totale_trimestre = ...

            print(totali)            # Output: {'gennaio': 161.7, 'febbraio': 108.7, 'marzo': 187.1}
            print(totale_trimestre)  # Output: 457.5
        """,
        starter_avanzata="""
            spese_mesi = {
                "gennaio": [45.0, 12.3, 80.5, 23.9],
                "febbraio": [60.0, 15.5, 33.2],
                "marzo": [22.4, 95.0, 41.1, 18.7, 9.9],
            }

            # totali, totale_trimestre
        """,
        soluzione="""
            spese_mesi = {
                "gennaio": [45.0, 12.3, 80.5, 23.9],
                "febbraio": [60.0, 15.5, 33.2],
                "marzo": [22.4, 95.0, 41.1, 18.7, 9.9],
            }

            totali = {}
            for mese, lista in spese_mesi.items():
                totali[mese] = round(sum(lista), 2)

            totale_trimestre = sum(totali.values())

            print(totali)            # Output: {'gennaio': 161.7, 'febbraio': 108.7, 'marzo': 187.1}
            print(totale_trimestre)  # Output: 457.5
        """,
        verifica="""
            assert totali == {"gennaio": 161.7, "febbraio": 108.7, "marzo": 187.1}, "❌ totali: una chiave per mese, con la somma arrotondata"
            assert round(totale_trimestre, 2) == 457.5, "❌ totale_trimestre: somma i valori di totali"
        """,
        facoltativo=True,
    )

    # E2.7 ------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Il file per il collega",
        scenario="""
            Un collega ci chiede le letture della fascia F3 del CSV del distributore in un file Excel, da aprire
            per conto suo. La cella qui sotto rilegge il CSV, quindi l'esercizio non dipende dall'E2.3.
        """,
        richiesta="""
            1. Salva in `f3` le sole righe della fascia F3, con la selezione `letture[letture["fascia"] == "F3"]`,
               che tiene le righe in cui la condizione tra parentesi quadre è vera e che il notebook 07 tratta per
               esteso.
            2. Scrivi `f3` nel file `riepilogo_fascia.xlsx`, nella cartella del notebook, con il metodo `to_excel()`
               e `index=False`.
            3. Rileggi il file con `read_excel` nel DataFrame `riletto` e confronta il suo numero di righe con
               quello di `f3`.

            Il file contiene 72 righe, cioè 12 mesi per 6 POD, e le stesse colonne del CSV, senza la colonna
            dell'indice.
        """,
        richiesta_avanzata="""
            1. Salva in `f3` le sole righe della fascia F3, con una selezione condizionale sulla colonna `fascia`.
            2. Scrivi `f3` nel file `riepilogo_fascia.xlsx`, nella cartella del notebook, senza la colonna
               dell'indice.
            3. Rileggi il file nel DataFrame `riletto` e confronta il suo numero di righe con quello di `f3`.

            Il file contiene 72 righe, cioè 12 mesi per 6 POD, e le stesse colonne del CSV.
        """,
        suggerimenti_base=[
            """
            Quando il file ha un solo foglio, `to_excel()` riceve direttamente il nome del file, senza
            `pd.ExcelWriter`, come in `f3.to_excel("riepilogo_fascia.xlsx", index=False)`. Il file si rilegge con
            `pd.read_excel("riepilogo_fascia.xlsx")` e le righe si contano con `len`.
            """,
        ],
        starter_base=f"""
            import pandas as pd

            {LEGGI_CSV}

            f3 = letture[letture["fascia"] == ...]
            f3.to_excel(..., index=False)

            riletto = ...

            print(len(f3), len(riletto))  # Output: 72 72
        """,
        starter_avanzata=f"""
            import pandas as pd

            {LEGGI_CSV}

            # f3, il file riepilogo_fascia.xlsx, riletto
        """,
        soluzione=f"""
            import pandas as pd

            {LEGGI_CSV}

            f3 = letture[letture["fascia"] == "F3"]
            f3.to_excel("riepilogo_fascia.xlsx", index=False)

            riletto = pd.read_excel("riepilogo_fascia.xlsx")

            print(len(f3), len(riletto))  # Output: 72 72
        """,
        verifica="""
            import os
            assert os.path.exists("riepilogo_fascia.xlsx"), "❌ Non trovo riepilogo_fascia.xlsx nella cartella del notebook"
            assert len(f3) == 72 and len(riletto) == len(f3), "❌ Il file deve avere le 72 righe della fascia F3"
            assert list(riletto.columns) == ["pod", "cliente", "data", "fascia", "kwh"], "❌ Colonne diverse dal CSV: hai usato index=False?"
        """,
        facoltativo=True,
    )

    # E2.8 (solo Avanzata) ---------------------------------------------
    chiamata = """
        import pandas as pd
        import requests


        def sensori(provincia):
            \"\"\"Anagrafica dei sensori meteo di Regione Lombardia in una provincia, come DataFrame.\"\"\"
            url = "https://www.dati.lombardia.it/resource/nf78-nj6b.json"
            response = requests.get(url, params={"provincia": provincia}, timeout=30)
            response.raise_for_status()
            return pd.DataFrame(response.json())


        sensori_mi = sensori("MI")
        sensori_mi.head()
    """
    riserva = """
        import json

        import pandas as pd

        with open("../Dati/fallback/lombardia_sensori.json", encoding="utf-8") as f:
            tutti = pd.DataFrame(json.load(f))
        sensori_mi = tutti[tutti["provincia"] == "MI"]
        sensori_mi.head()
    """
    with nb.solo("avanzata"):
        nb.esercizio(
            titolo="Il wrapper dell'API",
            scenario="""
                Nel notebook 06 abbiamo chiesto al portale di Regione Lombardia l'anagrafica dei sensori meteo,
                ripetendo ogni volta gli stessi passi. Una funzione che li raccoglie, detta wrapper, permette di
                chiedere i sensori di una provincia con una sola chiamata.
            """,
            richiesta="""
                1. Scrivi la funzione `sensori(provincia)`, con una docstring, che chiama l'endpoint
                   `https://www.dati.lombardia.it/resource/nf78-nj6b.json` con il parametro di query `provincia`,
                   un `timeout` di 30 secondi e `raise_for_status()`, e restituisce la risposta come DataFrame.
                2. Salva in `sensori_mi` i sensori della provincia di Milano, con la chiamata `sensori("MI")`.
                3. Se il portale non risponde, completa ed esegui la seconda cella, che legge il file di riserva
                   `../Dati/fallback/lombardia_sensori.json` e deve tenere in `sensori_mi` le sole righe con
                   provincia `MI`.

                La verifica controlla `sensori_mi` e funziona con entrambe le strade: il DataFrame non è vuoto, ha
                le colonne `idsensore`, `tipologia` e `provincia` e contiene soltanto sensori della provincia di
                Milano.
            """,
            suggerimenti=["""
                La funzione ripete i passi della sezione 7.3 del notebook 06, con il dizionario
                `params={"provincia": provincia}` al posto di `$limit`. Nel file di riserva la provincia si
                seleziona con una condizione sulla colonna `provincia`, come per i sensori di Milano nello stesso
                notebook.
            """],
            starter="""
                import pandas as pd
                import requests

                # def sensori(provincia): ...
                # sensori_mi = sensori("MI")
            """,
            soluzione=chiamata,
            verifica=None,
            rete=True,
            facoltativo=True,
        )
        # la cella di riserva, la verifica e la soluzione a richiesta: senza tag rete, così la verifica gira sempre
        rivela = nb.celle.pop()
        assert rivela.ruolo == "rivela"
        nb.celle.append(Cella("code", _dedent(riserva).replace(
            'sensori_mi = tutti[tutti["provincia"] == "MI"]', "sensori_mi = ..."), aula="avanzata",
            solo_studente=True, ruolo="starter"))
        nb.celle.append(Cella("code", _dedent(riserva), aula="avanzata", solo_soluzioni=True, ruolo="soluzione"))
        nb.celle.append(Cella("code", _dedent("""
            assert len(sensori_mi) > 0, "❌ sensori_mi è vuoto: hai chiamato sensori(\\"MI\\") o letto il file di riserva?"
            assert {"idsensore", "tipologia", "provincia"} <= set(sensori_mi.columns), "❌ Mancano le colonne dell'anagrafica"
            assert set(sensori_mi["provincia"]) == {"MI"}, "❌ sensori_mi deve contenere solo la provincia MI"
        """), aula="avanzata", ruolo="verifica"))
        rivela.src = _dedent(chiamata) + "\n\n\n# se il portale non risponde, nella seconda cella\n" + _dedent(riserva)
        nb.celle.append(rivela)

    # Sfida -----------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Sfida: il riepilogo per l'ufficio",
        scenario="""
            Per chiudere, l'ufficio vuole un riepilogo di tre righe sui consumi del CSV del distributore, da
            incollare in una mail. L'esercizio è aperto e non ha una verifica, perché il risultato si controlla
            confrontandolo con i numeri trovati negli esercizi precedenti.
        """,
        richiesta="""
            1. Partendo dal DataFrame `letture`, che la cella rilegge, calcola il consumo totale in kWh, il numero
               di POD diversi e la fascia con il consumo più alto.
            2. Stampa le tre informazioni con tre `print` e tre f-string, una per riga.

            Un riepilogo corretto riporta circa 134507.7 kWh, 6 POD e la fascia F1.
        """,
        suggerimenti_base=[
            """
            Il numero di POD diversi è la lunghezza del set dei valori della colonna `pod`, perché un set non
            ammette duplicati. Il consumo di una fascia è la somma di `kwh` sulle sole righe di quella fascia, con
            la selezione dell'esercizio sul file per il collega, e un ciclo sulle tre fasce che tiene da parte la
            più alta trova quella cercata.
            """,
        ],
        starter_base=f"""
            import pandas as pd

            {LEGGI_CSV}

            # il consumo totale, il numero di POD diversi e la fascia con il consumo più alto
            ...

            print(...)
            print(...)
            print(...)
        """,
        starter_avanzata=f"""
            import pandas as pd

            {LEGGI_CSV}
        """,
        soluzione=f"""
            import pandas as pd

            {LEGGI_CSV}

            totale = letture["kwh"].sum()
            n_pod = len(set(letture["pod"]))

            fascia_max = ""
            kwh_max = 0
            for fascia in ["F1", "F2", "F3"]:
                kwh_fascia = letture[letture["fascia"] == fascia]["kwh"].sum()
                if kwh_fascia > kwh_max:
                    fascia_max = fascia
                    kwh_max = kwh_fascia

            print(f"Consumo totale 2025: {{totale:.1f}} kWh")
            print(f"POD nel file: {{n_pod}}")
            print(f"Fascia con il consumo più alto: {{fascia_max}} ({{kwh_max:.1f}} kWh)")
        """,
        verifica=None,
        facoltativo=True,
    )
    return nb


def _dedent(testo: str) -> str:
    from textwrap import dedent

    return dedent(testo).strip("\n")
