"""03 · Strutture dati: liste, tuple, dizionari e set."""

from nbkit import Notebook

# Schema delle posizioni: etichetta su 11 caratteri, celle da 9. Costruito in codice
# così le colonne restano allineate anche se qualcuno cambia un valore.
_LARGHEZZA_ETICHETTA = 11
_LARGHEZZA_CELLA = 9
_ZONE = ['"NORD"', '"CNOR"', '"CSUD"', '"SUD"', '"SICI"', '"SARD"']


def _riga(etichetta: str, celle: list[str]) -> str:
    return (f"{etichetta:<{_LARGHEZZA_ETICHETTA}}" + "".join(f"{c:^{_LARGHEZZA_CELLA}}" for c in celle)).rstrip()


def _fetta(etichetta: str, a: int, b: int, testo: str) -> str:
    """Parentesi quadre sotto le celle da a (compreso) a b (escluso), poi il testo a destra."""
    inizio = _LARGHEZZA_ETICHETTA + _LARGHEZZA_CELLA * a
    fine = _LARGHEZZA_ETICHETTA + _LARGHEZZA_CELLA * b - 1
    colonna_testo = _LARGHEZZA_ETICHETTA + _LARGHEZZA_CELLA * len(_ZONE) + 2
    riga = f"{etichetta:<{_LARGHEZZA_ETICHETTA}}" + " " * (inizio - _LARGHEZZA_ETICHETTA)
    riga += "[" + "-" * (fine - inizio - 1) + "]"
    return riga + " " * (colonna_testo - len(riga)) + testo


SCHEMA_INDICI = "\n".join([
    _riga("indice", ["0", "1", "2", "3", "4", "5"]),
    _riga("zone", _ZONE),
    _riga("da destra", ["-6", "-5", "-4", "-3", "-2", "-1"]),
])

SCHEMA_FETTE = "\n".join([
    _riga("indice", ["0", "1", "2", "3", "4", "5"]),
    _riga("zone", _ZONE),
    _fetta("zone[1:3]", 1, 3, "parte da 1, si ferma prima di 3"),
    _fetta("zone[:2]", 0, 2, "dall'inizio, si ferma prima di 2"),
    _fetta("zone[4:]", 4, 6, "da 4 fino alla fine"),
])


def costruisci() -> Notebook:
    nb = Notebook(
        num="03",
        file="03_Strutture_dati",
        titolo="Strutture dati: liste, tuple, dizionari e set",
        blocco=1,
        giornata=1,
        intento="Una variabile tiene un valore. Per tenerne ventiquattro, o un listino intero, servono i contenitori: Python ne ha quattro, ognuno con il suo mestiere.",
        obiettivi=[
            "usare le liste con indici e slicing",
            "scegliere tra lista, tupla, dizionario e set",
            "leggere e modificare un dizionario",
        ],
        tempo={"base": 60, "avanzata": 40},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Liste", intro="""
        Una lista è una sequenza di valori in ordine, tra parentesi quadre e separati da virgola.
        Le letture orarie di una cabina, i POD di un cliente, le zone di mercato: quando i valori
        sono più di uno e l'ordine conta, è una lista.
    """)
    nb.code("""
        zone = ["NORD", "CNOR", "CSUD", "SUD", "SICI", "SARD"]
        letture_kwh = [12.4, 15.1, 14.8, 13.0, 11.7, 12.9]

        print(len(zone))           # Output: 6
        print(type(letture_kwh))   # Output: <class 'list'>
    """)
    nb.md("""
        `len()` conta gli elementi, come contava i caratteri di una stringa. Una lista accetta valori
        di tipo diverso, ma in pratica si tiene a un tipo solo: numeri con numeri, testi con testi.
        Due parole sui dati: le zone di mercato sono le sei aree in cui si forma il prezzo
        dell'energia in Italia; il POD è il codice del punto di prelievo, comincia con IT001E e
        identifica il contatore, non il cliente.
    """)

    nb.sottosezione("Indici e slicing", intro="""
        Per prendere un elemento si scrive la sua posizione tra quadre. Python conta da zero: il
        primo elemento è in posizione 0, l'ultimo in posizione `len - 1`. I numeri negativi contano
        da destra, e `-1` è sempre l'ultimo. Questo schema vale per tutto il corso, dalle liste alle
        righe di una tabella.
    """)
    nb.md("```text\n" + SCHEMA_INDICI + "\n```")
    nb.code("""
        print(zone[0])    # Output: NORD
        print(zone[2])    # Output: CSUD
        print(zone[-1])   # Output: SARD   (l'ultimo, senza sapere quanti sono)
        print(zone[-2])   # Output: SICI
    """)
    nb.md("""
        Chiedere `zone[6]` dà `IndexError`: con sei elementi l'ultimo indice è 5. È l'errore di chi
        conta da 1 per abitudine, e capita a tutti per un mese. Con due indici separati dai due punti
        prendiamo una fetta della lista: `[a:b]` parte da `a` e si ferma prima di `b`. L'inizio è
        compreso, la fine è esclusa.
    """)
    nb.md("```text\n" + SCHEMA_FETTE + "\n```")
    nb.code("""
        print(zone[1:3])   # Output: ['CNOR', 'CSUD']
        print(zone[:2])    # Output: ['NORD', 'CNOR']
        print(zone[4:])    # Output: ['SICI', 'SARD']
        print(zone[-2:])   # Output: ['SICI', 'SARD']   (gli ultimi due)
        print(zone[::2])   # Output: ['NORD', 'CSUD', 'SICI']   (uno sì e uno no)
    """)
    nb.md("""
        Il controllo rapido: `b - a` è quanti elementi prendiamo. `[1:3]` sono 2 elementi, `[8:19]`
        sono 11. Un terzo numero, dopo un altro due punti, è il passo: `[::2]` prende un elemento ogni
        due e, su dati quartorari, `[::4]` prende un valore per ora.
    """)
    nb.prova_tu(
        richiesta="""
            In `settimana_kwh` ci sono le letture giornaliere di una settimana, da lunedì a domenica.
            Con lo slicing metti in `feriali` le cinque letture da lunedì a venerdì e in `weekend`
            le due di sabato e domenica.
        """,
        starter="""
            settimana_kwh = [418.0, 432.5, 425.1, 440.2, 398.7, 215.3, 180.9]

            feriali = ...
            weekend = ...
            print(feriali, weekend)
        """,
        soluzione="""
            settimana_kwh = [418.0, 432.5, 425.1, 440.2, 398.7, 215.3, 180.9]

            feriali = settimana_kwh[:5]
            weekend = settimana_kwh[5:]
            print(feriali, weekend)
        """,
        verifica="""
            assert feriali == [418.0, 432.5, 425.1, 440.2, 398.7], "❌ feriali: dall'inizio alla posizione 5 esclusa"
            assert weekend == [215.3, 180.9], "❌ weekend: dalla posizione 5 alla fine"
        """,
    )

    nb.sottosezione("Modificare una lista", intro="""
        Una lista si può cambiare dopo averla creata: sovrascrivere una posizione, aggiungere in
        coda, togliere un valore. I metodi lavorano sul posto, sulla lista stessa.
    """)
    nb.code("""
        letture_kwh = [12.4, 15.1, 14.8, 13.0, 11.7, 12.9]

        letture_kwh[2] = 14.9               # la posizione 2 cambia valore: una lettura corretta
        letture_kwh.append(13.2)            # aggiunge un elemento in coda
        letture_kwh.extend([12.0, 11.4])    # aggiunge tutti gli elementi di un'altra lista

        letture_kwh   # Output: [12.4, 15.1, 14.9, 13.0, 11.7, 12.9, 13.2, 12.0, 11.4]
    """)
    nb.md("""
        `.append()` aggiunge un elemento, `.extend()` aggiunge tutti gli elementi di un'altra lista.
        Non sono intercambiabili: `.append([12.0, 11.4])` avrebbe aggiunto un elemento solo, una
        lista dentro la lista. Per togliere ci sono `.remove()`, che cerca un valore, e `.pop()`,
        che toglie l'ultimo e ce lo restituisce.
    """)
    nb.code("""
        letture_kwh.remove(11.4)     # toglie la prima occorrenza di quel valore
        ultima = letture_kwh.pop()   # toglie l'ultimo elemento e lo restituisce

        print(ultima)        # Output: 12.0
        print(letture_kwh)   # Output: [12.4, 15.1, 14.9, 13.0, 11.7, 12.9, 13.2]
    """)
    nb.box("attenzione", """
        `letture_kwh = letture_kwh.append(13.2)` è il modo più rapido per perdere una lista:
        `append` modifica sul posto e restituisce `None`, che finisce in `letture_kwh`. I metodi
        delle liste si chiamano senza `=`; con pandas sarà il contrario, lì si riassegna sempre.
    """)
    nb.box("nota", """
        Eseguire due volte una cella con `append` aggiunge due volte. Quando una cella modifica una
        lista, conviene che la crei anche: così ogni esecuzione parte pulita.
    """)
    nb.prova_tu(
        richiesta="""
            In `letture_kwh` manca l'ultima lettura della giornata, 13.2. Aggiungila in coda, poi
            calcola `media` (arrotondata a due decimali) e `massimo`.
        """,
        starter="""
            letture_kwh = [12.4, 15.1, 14.9, 13.0, 11.7, 12.9]

            ...
            media = ...
            massimo = ...
            print(media, massimo)
        """,
        soluzione="""
            letture_kwh = [12.4, 15.1, 14.9, 13.0, 11.7, 12.9]

            letture_kwh.append(13.2)
            media = round(sum(letture_kwh) / len(letture_kwh), 2)
            massimo = max(letture_kwh)
            print(media, massimo)
        """,
        verifica="""
            assert len(letture_kwh) == 7 and letture_kwh[-1] == 13.2, "❌ letture_kwh: aggiungi 13.2 in coda con append"
            assert media == 13.31, "❌ media: somma diviso numero di letture, due decimali"
            assert massimo == 15.1, "❌ massimo: la lettura più alta"
        """,
    )

    nb.sottosezione("Conti su una lista", intro="""
        Somma, minimo, massimo e ordinamento sono funzioni di Python già pronte: si passa la lista
        e si legge il risultato. La media non c'è e si fa a mano, somma diviso lunghezza.
    """)
    nb.code("""
        letture_kwh = [12.4, 15.1, 14.9, 13.0, 11.7, 12.9, 13.2]

        print(sum(letture_kwh))                                 # Output: 93.2
        print(min(letture_kwh), max(letture_kwh))               # Output: 11.7 15.1
        print(round(sum(letture_kwh) / len(letture_kwh), 2))    # Output: 13.31
        print(sorted(letture_kwh))                              # Output: [11.7, 12.4, 12.9, 13.0, 13.2, 14.9, 15.1]
    """)
    nb.md("""
        `sorted()` restituisce una lista nuova e lascia l'originale com'è; con `reverse=True` ordina
        dal più alto. Una lista può contenere altre liste, una per riga: è una tabella, e si legge
        con due indici, riga e colonna.
    """)
    nb.code("""
        tabella = [
            ["IT001E12345678", "Monza", 6.0],
            ["IT001E23456789", "Lodi", 10.0],
        ]

        tabella[1][2]   # Output: 10.0   (seconda riga, terza colonna)
    """)
    nb.md("""
        Funziona, ma `[1][2]` non dice niente a chi legge. Per le tabelle useremo i DataFrame di
        pandas, dove le colonne hanno un nome: ci arriviamo nel notebook sui DataFrame.
    """)
    nb.box("ricorda", """
        - Si conta da 0: il primo elemento è `[0]`, l'ultimo è `[-1]`.
        - In `[a:b]` l'inizio è compreso e la fine esclusa: `b - a` elementi.
        - I metodi delle liste modificano sul posto: niente `=` davanti.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Tuple", intro="""
        Una tupla è una lista che non si può più cambiare: parentesi tonde invece di quadre e, una
        volta creata, resta così. Serve per i valori che vanno insieme e non devono muoversi: le
        coordinate di una cabina, le dimensioni di una tabella.
    """)
    nb.code("""
        coordinate = (45.4642, 9.1900)   # latitudine e longitudine di Milano

        print(coordinate[0])      # Output: 45.4642
        print(len(coordinate))    # Output: 2
        print(type(coordinate))   # Output: <class 'tuple'>
    """)
    nb.md("""
        Indici e slicing funzionano come sulle liste. Quello che non funziona è la modifica. Questa
        cella dà errore apposta: leggiamo l'ultima riga.
    """)
    nb.code("coordinate[0] = 46.0", errore=True)
    nb.md("""
        `TypeError: 'tuple' object does not support item assignment`: la tupla non accetta
        assegnazioni. È una garanzia, non un limite: nessuno sposta Milano per sbaglio a metà di
        un'analisi. Quando un valore deve poter cambiare, si usa una lista.
    """)
    nb.md("""
        Una tupla si spacchetta: a sinistra dell'uguale tanti nomi quanti sono gli elementi, e ognuno
        prende il suo. Lo abbiamo già fatto nel notebook sulla sintassi, con
        `q1, q2, q3, q4 = 12.4, 12.9, 13.1, 12.6`: quella a destra era una tupla senza parentesi.
    """)
    nb.code("""
        lat, lon = coordinate

        print(f"Latitudine {lat}, longitudine {lon}")   # Output: Latitudine 45.4642, longitudine 9.19
    """)
    nb.md("""
        Le incontreremo più spesso di quanto sembri: `df.shape` restituisce una tupla
        `(righe, colonne)`, e molte funzioni restituiscono una coppia di valori. Quando un risultato
        ha le parentesi tonde, si legge con l'indice o si spacchetta.
    """)
    nb.prova_tu(
        richiesta="""
            La posizione della cabina primaria di Monza è nella tupla `posizione`. Spacchettala in
            `lat` e `lon` e costruisci `etichetta` in questo formato esatto:
            `CP Monza: lat 45.5845, lon 9.2744`.
        """,
        starter="""
            posizione = (45.5845, 9.2744)

            lat, lon = ...
            etichetta = f"..."
            etichetta
        """,
        soluzione="""
            posizione = (45.5845, 9.2744)

            lat, lon = posizione
            etichetta = f"CP Monza: lat {lat}, lon {lon}"
            etichetta
        """,
        verifica="""
            assert lat == 45.5845 and lon == 9.2744, "❌ lat, lon: spacchetta la tupla con due nomi a sinistra dell'uguale"
            assert etichetta == "CP Monza: lat 45.5845, lon 9.2744", "❌ etichetta: controlla spazi e virgole come nell'esempio"
        """,
    )

    # ------------------------------------------------------------------ 3
    nb.sezione("Dizionari", intro="""
        In una lista si cerca per posizione, in un dizionario si cerca per nome. Ogni elemento è una
        coppia chiave e valore tra graffe: la chiave è l'etichetta con cui ritroviamo il valore.
        L'anagrafica di un cliente, un listino, i parametri di una chiamata API: sono tutti dizionari.
    """)
    nb.code("""
        cliente = {
            "pod": "IT001E12345678",
            "cliente": "Caffè del Corso",
            "comune": "Monza",
            "potenza_kw": 6.0,
        }

        cliente["comune"]   # Output: 'Monza'
    """)
    nb.md("""
        La chiave va tra quadre come un indice, ma è un nome, non una posizione. Chiedere una
        chiave che non esiste dà `KeyError`; quando non siamo sicuri che ci sia, `.get()`
        restituisce un valore di riserva al posto dell'errore.
    """)
    nb.code("""
        print(cliente.get("comune"))           # Output: Monza
        print(cliente.get("tensione"))         # Output: None   (la chiave non c'è: nessun errore)
        print(cliente.get("tensione", "BT"))   # Output: BT     (il valore di riserva)
    """)
    nb.md("""
        Stessa sintassi per aggiungere e per modificare: se la chiave esiste il valore viene
        sostituito, altrimenti la coppia viene creata. `del` toglie chiave e valore insieme.
    """)
    nb.code("""
        cliente["tensione"] = "BT"      # chiave nuova: la aggiunge
        cliente["potenza_kw"] = 10.0    # chiave esistente: sostituisce il valore
        del cliente["comune"]           # toglie la coppia

        cliente
    """)
    nb.code("""
        print(list(cliente.keys()))     # Output: ['pod', 'cliente', 'potenza_kw', 'tensione']
        print(list(cliente.values()))   # Output: ['IT001E12345678', 'Caffè del Corso', 10.0, 'BT']
        print(list(cliente.items()))    # Output: [('pod', 'IT001E12345678'), ('cliente', 'Caffè del Corso'), ...]
    """)
    nb.md("""
        `.keys()`, `.values()` e `.items()` danno le chiavi, i valori e le coppie, ognuna una tupla.
        Li useremo soprattutto nei cicli `for`. `len()` conta le coppie e `in` cerca tra le chiavi,
        non tra i valori: `"pod" in cliente` è `True`, `"BT" in cliente` è `False`.
    """)
    nb.prova_tu(
        richiesta="""
            `contatori` dice quanti contatori ha in carico ogni cabina. Aggiungi `"CP Lecco"` con 64
            contatori, porta `"CP Monza"` a 125 e leggi in `n_cremona` il valore di `"CP Cremona"` con
            `.get()`, usando 0 come riserva.
        """,
        starter="""
            contatori = {"CP Monza": 120, "CP Lodi": 85}

            ...
            ...
            n_cremona = ...
            print(contatori, n_cremona)
        """,
        soluzione="""
            contatori = {"CP Monza": 120, "CP Lodi": 85}

            contatori["CP Lecco"] = 64
            contatori["CP Monza"] = 125
            n_cremona = contatori.get("CP Cremona", 0)
            print(contatori, n_cremona)
        """,
        verifica="""
            assert contatori.get("CP Lecco") == 64, "❌ contatori: aggiungi la chiave CP Lecco con 64"
            assert contatori["CP Monza"] == 125, "❌ contatori: aggiorna CP Monza a 125"
            assert len(contatori) == 3, "❌ contatori: devono esserci tre cabine, niente di più"
            assert n_cremona == 0, "❌ n_cremona: usa .get con 0 come riserva, la chiave non esiste"
        """,
    )

    nb.sottosezione("Un dizionario di liste", intro="""
        Un dizionario può avere liste come valori: una chiave per colonna, una lista con i valori di
        quella colonna. È una tabella scritta per colonne, ed è quello che pandas si aspetta per
        costruire un DataFrame.
    """)
    nb.code("""
        consumi = {
            "pod": ["IT001E12345678", "IT001E23456789", "IT001E34567890"],
            "comune": ["Monza", "Lodi", "Cremona"],
            "kwh": [1250.5, 980.0, 2210.3],
        }

        sum(consumi["kwh"])   # Output: 4440.8
    """)
    nb.md("""
        `consumi["kwh"]` è la colonna dei consumi, e `sum` la somma. Dalla stessa struttura pandas
        costruisce la tabella con una riga: un'anteprima di quello che faremo nel notebook sui
        DataFrame.
    """)
    nb.code("""
        import pandas as pd

        tabella = pd.DataFrame(consumi)
        tabella
    """)
    nb.code("tabella.shape   # Output: (3, 3)   una tupla: righe e colonne")

    # ------------------------------------------------------------------ 4
    nb.sezione("Set", intro="""
        Un set è un insieme: niente ordine, niente doppioni. Si scrive tra graffe come un dizionario,
        ma senza i due punti. Serve quando la domanda è quali valori ci sono, non quante volte o in
        che ordine.
    """)
    nb.code("""
        zone_letture = ["NORD", "NORD", "CSUD", "NORD", "SICI", "CSUD"]

        zone_distinte = set(zone_letture)
        zone_distinte   # Output: {'CSUD', 'NORD', 'SICI'}   (in un ordine qualsiasi)
    """)
    nb.md("""
        `set(lista)` toglie i doppioni in un colpo. L'ordine che vediamo non è quello di partenza e
        può cambiare da un'esecuzione all'altra: a un set non si chiede `[0]`. Per riavere una lista
        in ordine, `sorted()`.
    """)
    nb.code("""
        print(len(zone_distinte))        # Output: 3
        print("NORD" in zone_distinte)   # Output: True
        print("SARD" in zone_distinte)   # Output: False
        print(sorted(zone_distinte))     # Output: ['CSUD', 'NORD', 'SICI']
    """)
    nb.md("""
        `in` risponde se un valore c'è, e sui set è immediato anche con milioni di elementi. Vale
        allo stesso modo per liste, tuple e stringhe: `"NORD" in zone`, `"IT" in "IT001E12345678"`.
        Tra due set si fanno le operazioni degli insiemi: `|` unisce, `&` tiene quello che hanno in
        comune, `-` toglie.
    """)
    nb.code("""
        pod_gennaio = {"IT001E12345678", "IT001E23456789", "IT001E34567890"}
        pod_febbraio = {"IT001E23456789", "IT001E34567890", "IT001E45678901"}

        print(pod_gennaio | pod_febbraio)   # Output: i quattro POD visti almeno una volta (unione)
        print(pod_gennaio & pod_febbraio)   # Output: i due POD presenti in entrambi i mesi (intersezione)
        print(pod_gennaio - pod_febbraio)   # Output: {'IT001E12345678'}   (c'era a gennaio, non più a febbraio)
    """)
    nb.md("""
        Chi c'era a gennaio e non a febbraio, chi c'è in entrambi i mesi: con due set sono due righe.
        Per aggiungere un valore a un set c'è `.add()`, per toglierlo `.remove()`.
    """)
    nb.prova_tu(
        richiesta="""
            `comuni_letture` elenca il comune di ogni lettura arrivata oggi, con molte ripetizioni.
            Metti in `comuni_distinti` l'insieme dei comuni e in `n_comuni` quanti sono.
        """,
        starter="""
            comuni_letture = ["Monza", "Lodi", "Monza", "Cremona", "Lodi", "Monza", "Lecco", "Cremona"]

            comuni_distinti = ...
            n_comuni = ...
            print(sorted(comuni_distinti), n_comuni)
        """,
        soluzione="""
            comuni_letture = ["Monza", "Lodi", "Monza", "Cremona", "Lodi", "Monza", "Lecco", "Cremona"]

            comuni_distinti = set(comuni_letture)
            n_comuni = len(comuni_distinti)
            print(sorted(comuni_distinti), n_comuni)
        """,
        verifica="""
            assert comuni_distinti == {"Monza", "Lodi", "Cremona", "Lecco"}, "❌ comuni_distinti: set(lista) toglie i doppioni"
            assert n_comuni == 4, "❌ n_comuni: len del set, non della lista"
        """,
    )

    # ------------------------------------------------------------------ 5
    nb.sezione("Quale struttura quando", intro="""
        Quattro contenitori, quattro domande diverse. La scelta si fa guardando come useremo i dati,
        non come arrivano.
    """)
    nb.md("""
        | Struttura | Quando | Dove la incontreremo |
        |---|---|---|
        | Lista `[12.4, 15.1]` | valori in ordine, anche ripetuti, che possono cambiare | le letture di un giorno, i file di una cartella |
        | Tupla `(45.46, 9.19)` | pochi valori che vanno insieme e non cambiano | `df.shape`, le coordinate |
        | Dizionario `{"F1": 0.21}` | cercare per nome, non per posizione | anagrafiche, listini, i parametri di un'API |
        | Set `{"NORD", "SUD"}` | valori unici: c'è o non c'è, quanti distinti | togliere i doppioni, confrontare due elenchi |
    """)
    nb.md("""
        Nel dubbio: lista. Se poi ci accorgiamo che cerchiamo sempre per nome, era un dizionario; se
        contiamo solo i distinti, era un set. Con pandas la lista diventa una colonna e il dizionario
        di liste un DataFrame: le quattro strutture restano le stesse.
    """)
    nb.box("ricorda", """
        - Lista per l'ordine, dizionario per il nome, set per gli unici, tupla per quello che non cambia.
        - `.get(chiave, riserva)` legge un dizionario senza errori.
        - `set(lista)` toglie i doppioni; `|` unisce, `&` interseca.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Le 24 letture della cabina",
        scenario="""
            Siamo nell'ufficio misure. Ogni mattina arrivano le 24 letture orarie, in kWh, della
            cabina del polo logistico di Lodi: la lettura delle 0 in posizione 0, quella delle 23 in
            posizione 23. Il collega vuole totale, media e picco della fascia F1, e oggi conta le
            celle in Excel con il dito. Le fasce orarie sono i tre prezzi della bolletta secondo
            l'ora: F1 lunedì-venerdì 8-19, F2 lunedì-venerdì 7-8 e 19-23 più il sabato 7-23, F3
            notte, domenica e festivi.
        """,
        richiesta="""
            È un giorno feriale.

            1. Metti in `letture_f1` le 11 letture delle ore da 8 a 18 comprese, con lo slicing.
            2. Calcola `totale_f1` (la somma) e `media_f1` (la media, un decimale).
            3. Metti in `picco_f1` la lettura più alta della fascia.
        """,
        suggerimento="L'ora è l'indice: la lettura delle 8 è `letture_kwh[8]`. La fine dello slicing è esclusa.",
        starter="""
            letture_kwh = [
                310, 295, 288, 284, 290, 318, 402, 515,   # ore 0-7
                640, 688, 702, 715, 698, 672, 690, 707,   # ore 8-15
                719, 684, 620, 548, 470, 410, 365, 330,   # ore 16-23
            ]

            letture_f1 = ...
            totale_f1 = ...
            media_f1 = ...
            picco_f1 = ...
            print(f"F1: {totale_f1} kWh in {len(letture_f1)} ore, media {media_f1}, picco {picco_f1}")
        """,
        soluzione="""
            letture_kwh = [
                310, 295, 288, 284, 290, 318, 402, 515,   # ore 0-7
                640, 688, 702, 715, 698, 672, 690, 707,   # ore 8-15
                719, 684, 620, 548, 470, 410, 365, 330,   # ore 16-23
            ]

            letture_f1 = letture_kwh[8:19]
            totale_f1 = sum(letture_f1)
            media_f1 = round(totale_f1 / len(letture_f1), 1)
            picco_f1 = max(letture_f1)
            print(f"F1: {totale_f1} kWh in {len(letture_f1)} ore, media {media_f1}, picco {picco_f1}")
        """,
        verifica="""
            assert len(letture_f1) == 11, "❌ letture_f1: dalle 8 alle 18 comprese sono 11 letture, controlla gli estremi dello slicing"
            assert letture_f1[0] == 640 and letture_f1[-1] == 620, "❌ letture_f1: deve partire dalla lettura delle 8 e finire con quella delle 18"
            assert totale_f1 == 7535, "❌ totale_f1: la somma delle letture in F1"
            assert media_f1 == 685.0, "❌ media_f1: totale diviso numero di letture, un decimale"
            assert picco_f1 == 719, "❌ picco_f1: la lettura più alta tra quelle in F1"
        """,
        perche="`[8:19]` e non `[8:18]`: la fine è esclusa, quindi per arrivare alla lettura delle 18 si scrive 19. Controllo: 19 - 8 = 11 letture.",
    )
    nb.esercizio(
        titolo="I POD del turno",
        bis=True,
        scenario="""
            Il customer care lavora su una coda di POD da richiamare, in ordine di arrivo. Il turno
            del mattino prende i primi quattro, quello del pomeriggio i quattro successivi, il resto
            slitta a domani. Stamattina è arrivata una richiesta nuova e un cliente ha richiamato da
            solo: la coda va aggiornata prima di dividerla.
        """,
        richiesta="""
            Prima si aggiorna la coda, poi si divide.

            1. Aggiungi in coda a `coda_pod` il POD `"IT001E99887766"` e togli `"IT001E23456789"`.
            2. Metti in `turno_mattina` i primi quattro POD della coda aggiornata e in
               `turno_pomeriggio` i quattro successivi.
            3. Metti in `domani` quanti POD restano dopo gli otto assegnati.
        """,
        suggerimento="`.append()` e `.remove()` modificano la lista sul posto; poi due slicing e un `len()`.",
        starter="""
            coda_pod = [
                "IT001E12345678", "IT001E23456789", "IT001E34567890", "IT001E45678901", "IT001E56789012",
                "IT001E67890123", "IT001E78901234", "IT001E89012345", "IT001E90123456", "IT001E01234567",
            ]

            ...
            ...
            turno_mattina = ...
            turno_pomeriggio = ...
            domani = ...
            print(turno_mattina, turno_pomeriggio, domani)
        """,
        soluzione="""
            coda_pod = [
                "IT001E12345678", "IT001E23456789", "IT001E34567890", "IT001E45678901", "IT001E56789012",
                "IT001E67890123", "IT001E78901234", "IT001E89012345", "IT001E90123456", "IT001E01234567",
            ]

            coda_pod.append("IT001E99887766")
            coda_pod.remove("IT001E23456789")
            turno_mattina = coda_pod[:4]
            turno_pomeriggio = coda_pod[4:8]
            domani = len(coda_pod[8:])
            print(turno_mattina, turno_pomeriggio, domani)
        """,
        verifica="""
            assert "IT001E99887766" in coda_pod and "IT001E23456789" not in coda_pod, "❌ coda_pod: aggiungi il POD nuovo e togli quello annullato"
            assert turno_mattina == ["IT001E12345678", "IT001E34567890", "IT001E45678901", "IT001E56789012"], "❌ turno_mattina: i primi quattro della coda aggiornata"
            assert turno_pomeriggio == ["IT001E67890123", "IT001E78901234", "IT001E89012345", "IT001E90123456"], "❌ turno_pomeriggio: dal quinto all'ottavo, cioè [4:8]"
            assert domani == 2, "❌ domani: quanti POD restano dopo i primi otto"
        """,
        perche="Prima si aggiorna la coda, poi si taglia: se tagliassimo prima, il POD tolto finirebbe in un turno.",
    )
    nb.esercizio(
        titolo="Il listino per fascia",
        scenario="""
            Il commerciale applica a mano, preventivo dopo preventivo, un listino per fascia oraria:
            F1 a 0.21, F2 a 0.19 e F3 a 0.17 euro/kWh. Un cliente ha consumato 1250 kWh in F1, 830 in
            F2 e 1040 in F3. Da lunedì il prezzo F1 scende a 0.20 e il commerciale vuole rifare il
            conto senza riscrivere tutto.
        """,
        richiesta="""
            Tutto parte dal dizionario `listino`.

            1. Costruisci il dizionario `listino`: fascia come chiave, prezzo come valore.
            2. Calcola `costo` della bolletta: per ogni fascia il consumo per il prezzo, sommati.
            3. Aggiorna nel dizionario il prezzo di F1 a 0.20 e ricalcola in `costo_nuovo`.
            4. Metti in `fasce` la lista delle chiavi del listino.
        """,
        suggerimento="`consumi_kwh[\"F1\"] * listino[\"F1\"]` è il costo della fascia F1; le chiavi si elencano con `list(listino.keys())`.",
        starter="""
            consumi_kwh = {"F1": 1250, "F2": 830, "F3": 1040}

            listino = {...}
            costo = ...
            ...
            costo_nuovo = ...
            fasce = ...
            print(f"Prima: {costo:.2f} euro, dopo: {costo_nuovo:.2f} euro, fasce: {fasce}")
        """,
        soluzione="""
            consumi_kwh = {"F1": 1250, "F2": 830, "F3": 1040}

            listino = {"F1": 0.21, "F2": 0.19, "F3": 0.17}
            costo = (consumi_kwh["F1"] * listino["F1"]
                     + consumi_kwh["F2"] * listino["F2"]
                     + consumi_kwh["F3"] * listino["F3"])
            listino["F1"] = 0.20
            costo_nuovo = (consumi_kwh["F1"] * listino["F1"]
                           + consumi_kwh["F2"] * listino["F2"]
                           + consumi_kwh["F3"] * listino["F3"])
            fasce = list(listino.keys())
            print(f"Prima: {costo:.2f} euro, dopo: {costo_nuovo:.2f} euro, fasce: {fasce}")
        """,
        verifica="""
            assert len(listino) == 3 and listino["F2"] == 0.19, "❌ listino: tre chiavi F1, F2, F3 con i prezzi del commerciale"
            assert round(costo, 2) == 597.0, "❌ costo: somma di consumo per prezzo per le tre fasce, con i prezzi di partenza"
            assert listino["F1"] == 0.20, "❌ listino: aggiorna il prezzo di F1 nel dizionario, non in una variabile a parte"
            assert round(costo_nuovo, 2) == 584.5, "❌ costo_nuovo: rifai il conto dopo l'aggiornamento"
            assert fasce == ["F1", "F2", "F3"], "❌ fasce: le chiavi del listino, come lista"
        """,
        perche="La formula compare due volte: nel notebook sulle funzioni la chiuderemo in una `def` e la richiameremo. Il punto, qui, è che il prezzo si aggiorna in un posto solo e tutto il resto segue.",
        passo_in_piu=dict(
            testo="""
                Due liste con il comune di ogni POD attivato a gennaio e a febbraio, con ripetizioni.
                Metti in `comuni_entrambi` il set dei comuni serviti in tutti e due i mesi e in
                `comuni_totali` quanti comuni distinti abbiamo servito nel bimestre.
            """,
            starter="""
                comuni_gennaio = ["Monza", "Lodi", "Monza", "Cremona", "Lecco", "Lodi"]
                comuni_febbraio = ["Lodi", "Varese", "Lecco", "Lecco", "Cantù"]

                comuni_entrambi = ...
                comuni_totali = ...
                print(sorted(comuni_entrambi), comuni_totali)
            """,
            soluzione="""
                comuni_gennaio = ["Monza", "Lodi", "Monza", "Cremona", "Lecco", "Lodi"]
                comuni_febbraio = ["Lodi", "Varese", "Lecco", "Lecco", "Cantù"]

                comuni_entrambi = set(comuni_gennaio) & set(comuni_febbraio)
                comuni_totali = len(set(comuni_gennaio) | set(comuni_febbraio))
                print(sorted(comuni_entrambi), comuni_totali)
            """,
            verifica="""
                assert comuni_entrambi == {"Lodi", "Lecco"}, "❌ comuni_entrambi: trasforma le liste in set e usa & per l'intersezione"
                assert comuni_totali == 6, "❌ comuni_totali: quanti elementi ha l'unione dei due set, con |"
            """,
        ),
    )
    nb.esercizio(
        titolo="Anagrafica impianti",
        bis=True,
        scenario="""
            L'ufficio tecnico tiene l'anagrafica di ogni impianto fotovoltaico in un dizionario:
            identificativo, comune, potenza in kWp, anno di allaccio. Per l'impianto FV017 è arrivato
            un potenziamento: la potenza sale a 9.0 kWp, va registrata la data del collaudo e la
            vecchia chiave `note` va tolta. Il collega vuole anche sapere se c'è il campo `tensione`,
            senza che la cella esploda se non c'è.
        """,
        richiesta="""
            Tutto sul dizionario `impianto`, già creato nella cella.

            1. Porta `kwp` a 9.0 e aggiungi la chiave `collaudo` con il valore `"2025-09-15"`.
            2. Togli la chiave `note`.
            3. Leggi in `tensione` il valore della chiave `tensione` con `.get()`, usando `"BT"` come riserva.
            4. Metti in `campi` la lista delle chiavi, in ordine alfabetico.
        """,
        suggerimento="`sorted()` funziona anche sulle chiavi di un dizionario.",
        starter="""
            impianto = {
                "id_impianto": "FV017",
                "comune": "Treviglio",
                "kwp": 6.0,
                "anno_allaccio": 2019,
                "note": "da verificare",
            }

            ...
            ...
            ...
            tensione = ...
            campi = ...
            print(impianto, tensione, campi)
        """,
        soluzione="""
            impianto = {
                "id_impianto": "FV017",
                "comune": "Treviglio",
                "kwp": 6.0,
                "anno_allaccio": 2019,
                "note": "da verificare",
            }

            impianto["kwp"] = 9.0
            impianto["collaudo"] = "2025-09-15"
            del impianto["note"]
            tensione = impianto.get("tensione", "BT")
            campi = sorted(impianto.keys())
            print(impianto, tensione, campi)
        """,
        verifica="""
            assert impianto["kwp"] == 9.0, "❌ impianto: aggiorna kwp a 9.0"
            assert impianto.get("collaudo") == "2025-09-15", "❌ impianto: aggiungi la chiave collaudo"
            assert "note" not in impianto, "❌ impianto: togli la chiave note con del"
            assert tensione == "BT", "❌ tensione: la chiave non esiste, .get deve restituire la riserva"
            assert campi == ["anno_allaccio", "collaudo", "comune", "id_impianto", "kwp"], "❌ campi: le chiavi del dizionario ordinate con sorted"
        """,
    )
    return nb
