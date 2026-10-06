"""02 · Sintassi di base: variabili, numeri e stringhe."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="02",
        file="02_Sintassi_di_base",
        titolo="Sintassi di base: variabili, numeri e stringhe",
        blocco=1,
        giornata=1,
        intento="Le tre cose che si fanno in quasi ogni riga di Python: dare un nome a un valore, fare un conto, scrivere un testo.",
        obiettivi=[
            "assegnare un valore a una variabile e riconoscere i tipi di base",
            "fare calcoli e confronti con gli operatori giusti",
            "costruire testi con dentro numeri e variabili usando le f-string",
        ],
        tempo={"base": 60, "avanzata": 40},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Variabili e tipi", intro="""
        Una variabile è un nome che diamo a un valore, per poterlo riusare. Si crea con `=`: a sinistra
        il nome, a destra il valore. Python non chiede di dichiarare il tipo: lo capisce dal valore.
    """)
    nb.code("""
        potenza_kw = 6            # un numero intero
        consumo_kwh = 1234.5      # un numero con la virgola (che in Python si scrive con il punto)
        pod = "IT001E12345678"    # un testo, tra virgolette: il codice del contatore (il POD)
        attivo = True             # vero o falso
    """)
    nb.md("""
        Per vedere il valore di una variabile basta scriverla come ultima riga della cella: il notebook
        la mostra. `type()` ci dice di che tipo è.
    """)
    nb.code("consumo_kwh")
    nb.code("type(consumo_kwh)")
    nb.md("""
        I quattro tipi di base: `int` per gli interi, `float` per i numeri con la virgola, `str` per il
        testo, `bool` per `True` e `False`. Il tipo decide cosa possiamo fare con il valore: due numeri
        si sommano, due testi si attaccano, un numero e un testo non si mischiano. Lo vediamo tra poco.
    """)
    nb.code("""
        print(type(potenza_kw))   # Output: <class 'int'>
        print(type(pod))          # Output: <class 'str'>
        print(type(attivo))       # Output: <class 'bool'>
    """)
    nb.md("""
        Sui nomi, tre regole che bastano: minuscolo con gli underscore (`consumo_kwh`, non `ConsumoKWh`),
        mai un numero come primo carattere, e il nome dice cosa contiene. `x` va bene per cinque secondi,
        `consumo_kwh` per sempre.
    """)
    nb.md("""
        Un'ultima cosa sulla forma. Python usa gli spazi a inizio riga per capire cosa sta dentro cosa:
        dopo un `if` o un `for`, le righe spostate di quattro spazi fanno parte di quel blocco. Lo useremo
        davvero nel notebook sulle condizioni; per ora basta sapere che gli spazi contano.
    """)
    nb.code("""
        if potenza_kw > 3:
            print("Contatore sopra i 3 kW")   # questa riga è dentro l'if: parte solo se la condizione è vera
    """)
    nb.prova_tu(
        richiesta="""
            Crea una variabile `cliente` con un nome a scelta e una variabile `numero_pod` con quanti
            contatori ha quel cliente (un numero intero). Poi mostra il tipo di entrambe.
        """,
        starter="""
            cliente = ...
            numero_pod = ...

            print(type(cliente), type(numero_pod))
        """,
        soluzione="""
            cliente = "Caffè del Corso"
            numero_pod = 2

            print(type(cliente), type(numero_pod))
        """,
        verifica="""
            assert type(cliente) is str, "❌ cliente deve essere un testo tra virgolette"
            assert type(numero_pod) is int, "❌ numero_pod deve essere un numero intero, senza virgolette"
        """,
    )

    # ------------------------------------------------------------------ 2
    nb.sezione("Numeri", intro="""
        Con i numeri Python fa quello che fa una calcolatrice, con le stesse precedenze: prima
        moltiplicazioni e divisioni, poi somme e sottrazioni, e le parentesi comandano.
    """)
    nb.code("""
        print(3 + 2)     # Output: 5
        print(3 - 2)     # Output: 1
        print(3 * 2)     # Output: 6
        print(3 / 2)     # Output: 1.5
        print(3 ** 2)    # Output: 9   (potenza)
    """)
    nb.md("""
        Due operatori meno ovvi: `//` è la divisione intera (quante volte ci sta) e `%` è il resto.
        Con i minuti si vede bene: 135 minuti sono 2 ore e 15 minuti.
    """)
    nb.code("""
        minuti = 135

        print(minuti // 60)   # Output: 2    (ore piene)
        print(minuti % 60)    # Output: 15   (minuti che avanzano)
    """)
    nb.md("""
        La divisione `/` restituisce sempre un `float`, anche quando il risultato è un numero intero.
        Per arrotondare c'è `round()`, a cui possiamo dire quanti decimali tenere.
    """)
    nb.code("""
        print(10 / 2)                # Output: 5.0
        print(round(1234.5678, 2))   # Output: 1234.57
        print(round(1234.5678))      # Output: 1235
    """)
    nb.md("""
        Le funzioni che servono più spesso sono già pronte: `abs()`, `min()`, `max()`. Per radici,
        logaritmi e π c'è la libreria `math`, che va importata prima di usarla.
    """)
    nb.code("""
        import math

        print(abs(-4.2))              # Output: 4.2
        print(max(12.3, 9.8, 15.1))   # Output: 15.1
        print(math.sqrt(16))          # Output: 4.0
        print(math.pi)                # Output: 3.141592653589793
    """)
    nb.md("""
        Un confronto è un conto che risponde `True` o `False`: `>`, `<`, `>=`, `<=`, `==` (uguale, con due
        segni) e `!=` (diverso). È lo stesso meccanismo che useremo dentro gli `if` e nei filtri sui dati.
    """)
    nb.code("""
        consumo_kwh = 1234.5
        soglia = 1000

        print(consumo_kwh > soglia)    # Output: True
        print(consumo_kwh == soglia)   # Output: False
    """)
    nb.box("attenzione", """
        `=` assegna, `==` confronta. `consumo_kwh = 1000` cambia la variabile; `consumo_kwh == 1000`
        chiede se vale 1000. Confonderli è l'errore più frequente della prima settimana.
    """)
    nb.md("""
        Una variabile si aggiorna riassegnandola. `+=` è la scorciatoia per "aggiungi a quello che c'è
        già", comoda quando accumuliamo un totale.
    """)
    nb.code("""
        totale_kwh = 0
        totale_kwh = totale_kwh + 350.0
        totale_kwh += 420.5

        totale_kwh   # Output: 770.5
    """)
    nb.prova_tu(
        richiesta="""
            Una centrale ha prodotto 1250 MWh in un giorno. Calcola la produzione media per ora,
            arrotondata a un decimale, e salvala in `media_oraria`.
        """,
        starter="""
            produzione_mwh = 1250

            media_oraria = ...
            media_oraria
        """,
        soluzione="""
            produzione_mwh = 1250

            media_oraria = round(produzione_mwh / 24, 1)
            media_oraria
        """,
        verifica="""
            assert media_oraria == 52.1, "❌ Dividi per le ore di un giorno e arrotonda a un decimale"
        """,
    )

    # ------------------------------------------------------------------ 3
    nb.sezione("Stringhe", intro="""
        Un testo in Python è una stringa: una sequenza di caratteri tra virgolette, singole o doppie
        è uguale. Sono stringhe i nomi, i codici, i messaggi e quasi tutto quello che arriva da un
        file prima di essere convertito in numero.
    """)
    nb.code("""
        cliente = "Caffè del Corso"
        pod = 'IT001E12345678'

        print(len(cliente))   # Output: 15   (caratteri, spazi compresi)
    """)
    nb.md("""
        Le stringhe si attaccano con `+`. Funziona solo tra stringhe: per attaccare un numero bisogna
        prima trasformarlo in testo con `str()`.
    """)
    nb.code("""
        etichetta = cliente + " - " + pod
        etichetta
    """)
    nb.md("""
        Questa cella dà errore apposta. Leggiamo l'ultima riga del messaggio: è quella che dice cosa
        non va.
    """)
    nb.code('"Consumo: " + 1234.5', errore=True)
    nb.md("""
        `TypeError`: Python non sa se vogliamo sommare o attaccare, e si rifiuta di indovinare.
        Con `str(1234.5)` funzionerebbe, ma c'è un modo migliore, che vediamo tra poco.
    """)
    nb.md("""
        Una stringa ha dei metodi: operazioni che si chiamano con il punto dopo il nome. Non modificano
        la stringa di partenza, ne restituiscono una nuova.
    """)
    nb.code("""
        print(cliente.upper())                 # Output: CAFFÈ DEL CORSO
        print(cliente.lower())                 # Output: caffè del corso
        print("lunedì".capitalize())           # Output: Lunedì
        print("  IT001E12345678 ".strip())     # Output: IT001E12345678   (via gli spazi ai bordi)
        print(pod.replace("IT001E", ""))       # Output: 12345678
    """)
    nb.md("""
        `.strip()` e `.replace()` sono quelli che useremo di più sui dati: codici con spazi in più,
        separatori da togliere, testi da uniformare prima di un confronto. I metodi si possono mettere
        in fila.
    """)
    nb.code("""
        pod_pulito = " it001e12345678 ".strip().upper()

        pod_pulito == pod   # Output: True
    """)

    nb.sottosezione("Le f-string", intro="""
        Per costruire un testo con dentro dei valori si usa una f-string: una `f` prima delle virgolette
        e le variabili tra graffe. Python le sostituisce con il loro valore, numeri compresi, senza `str()`.
    """)
    nb.code("""
        consumo_kwh = 1234.5678

        messaggio = f"Il cliente {cliente} ha consumato {consumo_kwh} kWh"
        messaggio
    """)
    nb.md("""
        Dentro le graffe possiamo anche dire come formattare il numero: `:.2f` vuol dire due decimali,
        `:.0f` nessuno, `:,` mette il separatore delle migliaia. Si scrive dopo il nome, separato dai
        due punti.
    """)
    nb.code("""
        prezzo_kwh = 0.215

        print(f"Consumo: {consumo_kwh:.2f} kWh")                 # Output: Consumo: 1234.57 kWh
        print(f"Totale: {consumo_kwh * prezzo_kwh:.2f} euro")    # Output: Totale: 265.43 euro
        print(f"Clienti attivi: {152000:,}")                     # Output: Clienti attivi: 152,000
    """)
    nb.box("nota", """
        Dentro le graffe ci sta un'espressione intera, come `consumo_kwh * prezzo_kwh`. Se diventa
        lunga, meglio calcolarla prima in una variabile con un nome: si legge meglio e si controlla meglio.
    """)
    nb.box("approfondimento", """
        Quando si stampano più righe una sotto l'altra, dopo i due punti si può fissare anche la
        larghezza: `{nome:<12}` allinea a sinistra su 12 caratteri, `{valore:>8.1f}` allinea a destra su
        8 caratteri con un decimale. Utile per una tabellina di testo in un messaggio o in un log.

        ```python
        print(f"{'NORD':<6}{98.456:>8.1f}")   # NORD      98.5
        print(f"{'SICI':<6}{112.3:>8.1f}")    # SICI     112.3
        ```
    """, titolo="Allineare le colonne di testo")
    nb.prova_tu(
        richiesta="""
            Con `zona = "NORD"` e `prezzo = 98.456`, costruisci la stringa `riga` in questo formato
            esatto: `Zona NORD: 98.46 €/MWh`.
        """,
        starter="""
            zona = "NORD"
            prezzo = 98.456

            riga = f"..."
            riga
        """,
        soluzione="""
            zona = "NORD"
            prezzo = 98.456

            riga = f"Zona {zona}: {prezzo:.2f} €/MWh"
            riga
        """,
        verifica="""
            assert riga == "Zona NORD: 98.46 €/MWh", "❌ Controlla spazi, due decimali e l'unità di misura"
        """,
    )
    nb.box("ricorda", """
        - `=` assegna, `==` confronta.
        - Testo e numeri non si sommano: per metterli insieme si usa una f-string.
        - `{valore:.2f}` sono due decimali, `{valore:,}` le migliaia.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="La riga di riepilogo in bolletta",
        scenario="""
            Siamo nel team fatturazione. Il collega che compilava a mano la riga di riepilogo delle
            bollette è in ferie e nessuno sa come faceva. Ci chiedono di generarla con Python: due
            decimali, niente fantasia.
        """,
        richiesta="""
            Calcola `totale` (consumo per prezzo) e costruisci `riepilogo` con una f-string a partire da
            `cliente`, `consumo_kwh` e `totale`, in questo formato esatto:
            `Cliente Rossi Mario: 1234.57 kWh, totale 265.43 euro`.
        """,
        suggerimento="`{valore:.2f}` arrotonda a due decimali.",
        starter="""
            cliente = "Rossi Mario"
            consumo_kwh = 1234.567
            prezzo_kwh = 0.215

            totale = ...
            riepilogo = f"..."
            riepilogo
        """,
        soluzione="""
            cliente = "Rossi Mario"
            consumo_kwh = 1234.567
            prezzo_kwh = 0.215

            totale = consumo_kwh * prezzo_kwh
            riepilogo = f"Cliente {cliente}: {consumo_kwh:.2f} kWh, totale {totale:.2f} euro"
            riepilogo
        """,
        verifica="""
            assert round(totale, 2) == 265.43, "❌ totale: consumo per prezzo"
            assert riepilogo == "Cliente Rossi Mario: 1234.57 kWh, totale 265.43 euro", "❌ riepilogo: controlla due decimali, spazi e virgole come nell'esempio"
        """,
        perche="Il totale calcolato in una variabile a parte: la f-string resta leggibile e il numero si può controllare da solo.",
    )
    nb.esercizio(
        titolo="Il messaggio del mattino",
        bis=True,
        scenario="""
            Ogni mattina Giulia del customer care scrive in chat il riepilogo del giorno prima, tipo
            "Lunedì: 37 nuovi contratti, 3 reclami". Vuole smettere di scriverlo a mano.
        """,
        richiesta="""
            Date le variabili `giorno`, `contratti` e `reclami`, costruisci `messaggio` con il giorno
            con l'iniziale maiuscola, in questo formato esatto: `Lunedì: 37 nuovi contratti, 3 reclami`.
        """,
        suggerimento="`.capitalize()` funziona anche dentro le graffe di una f-string.",
        starter="""
            giorno = "lunedì"
            contratti = 37
            reclami = 3

            messaggio = f"..."
            messaggio
        """,
        soluzione="""
            giorno = "lunedì"
            contratti = 37
            reclami = 3

            messaggio = f"{giorno.capitalize()}: {contratti} nuovi contratti, {reclami} reclami"
            messaggio
        """,
        verifica="""
            assert messaggio == "Lunedì: 37 nuovi contratti, 3 reclami", "❌ Iniziale maiuscola sul giorno e testo identico all'esempio"
        """,
    )
    nb.esercizio(
        titolo="Da MW a MWh",
        scenario="""
            In sala controllo arrivano le potenze medie di quattro quarti d'ora consecutivi, in MW:
            12.4, 12.9, 13.1 e 12.6. Il collega di turno vuole l'energia dell'ora in MWh e quanto pesa
            il quarto d'ora più alto sul totale, in percentuale. Oggi lo calcola con la calcolatrice del
            telefono.
        """,
        richiesta="""
            1. Calcola `energia_mwh`: un quarto d'ora a potenza P vale P/4 MWh, quindi somma i quattro
               valori e dividi per 4.
            2. Calcola `quota_max`: l'energia del quarto d'ora più alto divisa per `energia_mwh`, in
               percentuale, arrotondata a un decimale.
            3. Costruisci `frase` in questo formato esatto:
               `Energia dell'ora: 12.75 MWh (quarto d'ora di punta: 25.7%)`.
        """,
        suggerimento="`max()` accetta più numeri separati da virgola.",
        starter="""
            q1, q2, q3, q4 = 12.4, 12.9, 13.1, 12.6

            energia_mwh = ...
            quota_max = ...
            frase = f"..."
            frase
        """,
        soluzione="""
            q1, q2, q3, q4 = 12.4, 12.9, 13.1, 12.6

            energia_mwh = (q1 + q2 + q3 + q4) / 4
            quota_max = round(max(q1, q2, q3, q4) / 4 / energia_mwh * 100, 1)
            frase = f"Energia dell'ora: {energia_mwh:.2f} MWh (quarto d'ora di punta: {quota_max}%)"
            frase
        """,
        verifica="""
            assert round(energia_mwh, 2) == 12.75, "❌ energia_mwh: somma le quattro potenze e dividi per 4"
            assert quota_max == 25.7, "❌ quota_max: (massimo / 4) / energia_mwh * 100, arrotondato a un decimale"
            assert frase == "Energia dell'ora: 12.75 MWh (quarto d'ora di punta: 25.7%)", "❌ frase: controlla formato e decimali"
        """,
        perche="La percentuale si arrotonda una volta sola, alla fine: arrotondare i passaggi intermedi sposta il risultato.",
        passo_in_piu=dict(
            testo="""
                Il commerciale propone due listini per un cliente che consuma `consumo_kwh = 350` al
                mese: il listino A costa 0.21 euro/kWh e basta; il listino B costa 0.19 euro/kWh più
                8 euro fissi al mese. Calcola `costo_a` e `costo_b` e metti in `conviene_b` il risultato
                del confronto (`True` se B costa meno).
            """,
            starter="""
                consumo_kwh = 350

                costo_a = ...
                costo_b = ...
                conviene_b = ...
                print(f"A: {costo_a:.2f} euro, B: {costo_b:.2f} euro, conviene B: {conviene_b}")
            """,
            soluzione="""
                consumo_kwh = 350

                costo_a = consumo_kwh * 0.21
                costo_b = consumo_kwh * 0.19 + 8
                conviene_b = costo_b < costo_a
                print(f"A: {costo_a:.2f} euro, B: {costo_b:.2f} euro, conviene B: {conviene_b}")
            """,
            verifica="""
                assert round(costo_a, 2) == 73.5, "❌ costo_a: consumo per 0.21"
                assert round(costo_b, 2) == 74.5, "❌ costo_b: consumo per 0.19, più 8"
                assert conviene_b is False, "❌ conviene_b: confronta i due costi con <"
            """,
        ),
    )
    nb.esercizio(
        titolo="Le ore equivalenti dell'impianto",
        bis=True,
        scenario="""
            Un impianto fotovoltaico da 6 kWp ha prodotto 7380 kWh in un anno. Il commerciale vuole le
            ore equivalenti (energia prodotta divisa per la potenza installata) e una frase pronta da
            incollare nell'offerta.
        """,
        richiesta="""
            Calcola `ore_equivalenti` e costruisci `frase` in questo formato esatto:
            `Impianto da 6 kWp: 1230 ore equivalenti`.
        """,
        suggerimento="`{valore:.0f}` stampa un numero senza decimali.",
        starter="""
            potenza_kwp = 6
            produzione_kwh = 7380

            ore_equivalenti = ...
            frase = f"..."
            frase
        """,
        soluzione="""
            potenza_kwp = 6
            produzione_kwh = 7380

            ore_equivalenti = produzione_kwh / potenza_kwp
            frase = f"Impianto da {potenza_kwp} kWp: {ore_equivalenti:.0f} ore equivalenti"
            frase
        """,
        verifica="""
            assert ore_equivalenti == 1230, "❌ ore_equivalenti: produzione divisa per potenza"
            assert frase == "Impianto da 6 kWp: 1230 ore equivalenti", "❌ frase: niente decimali sulle ore"
        """,
    )
    return nb
