"""E1 · Esercitazione 1: un'ora di domande ed esercizi sul blocco 1 (notebook 00-03), "Una cena per otto"."""

from textwrap import dedent

from nbkit import Notebook


def unisci(*parti: str) -> str:
    """Toglie l'indentazione a ogni pezzo di codice e li unisce con una riga vuota."""
    return "\n\n".join(dedent(p).strip("\n") for p in parti)


def esercizio_due_aule(nb: Notebook, titolo: str, scenario: str, base: dict, avanzata: dict,
                       facoltativo: bool = False) -> None:
    """Lo stesso esercizio per le due aule: titolo e scenario in comune, il resto può cambiare.

    `base` e `avanzata` contengono richiesta, starter, soluzione, verifica e suggerimenti; le chiavi che mancano
    in `avanzata` si prendono da `base`.
    """
    nb.esercizio(titolo=titolo, scenario=scenario, facoltativo=facoltativo, aula="base", **base)
    nb.esercizio(titolo=titolo, scenario=scenario, facoltativo=facoltativo, aula="avanzata", **{**base, **avanzata})


def costruisci() -> Notebook:
    nb = Notebook(
        num="E1",
        file="Esercitazione_1",
        titolo="Esercitazione 1",
        blocco=1,
        giornata=1,
        intento="Un'ora di domande ed esercizi sui notebook 00-03, legati dalla preparazione di una cena per otto persone.",
        obiettivi=[
            "usare variabili, tipi e operatori e comporre un testo con le f-string",
            "modificare liste e dizionari e selezionarne una parte",
            "combinare set e tuple e riscrivere una cella seguendo PEP 8",
        ],
        tempo=60,
        dati=[],
        soluzioni_a_richiesta=True,
    )

    # ------------------------------------------------------------------ come funziona l'ora
    nb.md("""
        Questa esercitazione chiude la giornata e riprende quello che abbiamo visto nei notebook 00-03. Hai 45
        minuti per lavorare sugli esercizi, poi li guardiamo insieme. Si comincia con quattro domande di riepilogo e
        si prosegue con cinque esercizi, ciascuno con i propri dati, da fare nell'ordine perché la difficoltà cresce.
    """)
    aiuti = """
        Ogni esercizio comincia dicendo che cosa vogliamo ottenere e perché, e da lì si può arrivare al risultato da
        soli. Chi preferisce procedere per gradi apre con un clic il blocco Passo per passo, e sotto {aiuti}, da
        leggere solo dopo aver provato. Sotto la cella da completare ci sono la verifica, che conferma il risultato o
        dice che cosa controllare, e la cella `soluzione`, che mostra soltanto la soluzione di quell'esercizio. Se
        finisci prima, in fondo al notebook trovi gli esercizi facoltativi.
    """
    nb.md(aiuti.replace("{aiuti}", "due suggerimenti, anche loro nascosti"), aula="base")
    nb.md(aiuti.replace("{aiuti}", "un suggerimento, anche lui nascosto"), aula="avanzata")

    # ------------------------------------------------------------------ 1. Domande
    nb.sezione("Domande", intro="""
        Le quattro domande che seguono riguardano i notebook 00-03 e richiedono pochi minuti. Per ciascuna conviene
        prevedere la risposta a mente e solo dopo aprirla con un clic. In caso di dubbio si può provare la riga in
        una cella di codice e, se il risultato sorprende, rileggere la parte del notebook che tratta quell'argomento.
    """)
    nb.domanda(
        "Una confezione contiene 9 uova e una dose di carbonara ne richiede 4. Cosa restituisce `9 // 4`?",
        """
            Restituisce `2`. L'operatore `//` calcola la divisione intera e del quoziente, 2.25, tiene soltanto la
            parte intera, quindi con nove uova si preparano due dosi intere.
        """,
    )
    nb.domanda(
        'Con `spesa = ["spaghetti", "guanciale", "uova", "pecorino", "pepe"]`, cosa restituisce `spesa[1:3]`?',
        """
            Restituisce `['guanciale', 'uova']`. Lo slicing parte dall'indice 1, che contiene il guanciale, e si
            ferma prima dell'indice 3, quindi il pecorino resta escluso.
        """,
    )
    nb.domanda(
        'Con `cena = ("sabato", "20:30")`, cosa succede se eseguiamo `cena[1] = "21:00"`?',
        """
            Python solleva un `TypeError`, perché le tuple sono immutabili e non permettono di sostituire un
            elemento dopo la creazione. Per spostare la cena alle 21 si crea una tupla nuova,
            `cena = ("sabato", "21:00")`.
        """,
    )
    nb.domanda(
        'Cosa restituisce `len(set(["uova", "pecorino", "uova", "pepe"]))`?',
        """
            Restituisce `3`. Il costruttore `set()` elimina i duplicati, quindi delle due `"uova"` ne conserva una
            sola e il set contiene `"uova"`, `"pecorino"` e `"pepe"`.
        """,
    )

    # ------------------------------------------------------------------ 2. Esercizi
    nb.sezione("Esercizi", intro="""
        Gli esercizi seguono i preparativi di una cena. Sabato sera Marta ha otto invitati e vuole cucinare gli
        spaghetti alla carbonara, ma la sua ricetta è scritta per quattro persone. Ogni esercizio riguarda una parte
        dei preparativi e lavora sui dati scritti nella propria cella, quindi si può affrontare anche senza aver
        risolto i precedenti.
        I primi cinque sono gli esercizi che guardiamo insieme alla fine dell'ora.
    """)

    # E1.1 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Gli invitati",
        scenario="""
            La ricetta di Marta è per quattro persone e sabato saranno in otto. Vogliamo una cella che, dato il
            numero di invitati, calcoli di quanto moltiplicare la ricetta e componga l'annuncio da mettere in testa
            ai messaggi, in modo che se all'ultimo si aggiunge qualcuno basti cambiare un numero e il resto si
            aggiorni da solo. Alla fine `fattore` vale 2.0 e `annuncio` comincia con `Siamo in 8`.
        """,
        base=dict(
            richiesta="""
                1. Salva in `fattore` il risultato della divisione tra `invitati` e `persone_ricetta`, con `/`.
                2. Stampando `fattore` compare `2.0` e non `2`: salva in `tipo_fattore` il tipo della variabile, con
                   la funzione `type()`, per vedere che cosa ha prodotto la divisione.
                3. Componi `annuncio` unendo con l'operatore `+` il testo `"Siamo in "` e la variabile `invitati`,
                   che prima va convertita in stringa con `str()`.

                Alla fine `fattore` vale 2.0, `tipo_fattore` è `float` e `annuncio` vale `"Siamo in 8"`.
            """,
            suggerimenti=[
                """
                    La divisione con `/` restituisce sempre un numero con la virgola, anche quando il risultato è
                    intero. Un testo e un numero non si uniscono con `+` finché il numero non diventa un testo.
                """,
                """
                    Servono `invitati / persone_ricetta`, `type(fattore)` e `"Siamo in " + str(invitati)`.
                """,
            ],
            starter="""
                persone_ricetta = 4
                invitati = 8

                fattore = invitati / ...
                tipo_fattore = type(...)
                annuncio = "Siamo in " + ...

                print(fattore, tipo_fattore)
                print(annuncio)
            """,
            soluzione="""
                persone_ricetta = 4
                invitati = 8

                fattore = invitati / persone_ricetta
                tipo_fattore = type(fattore)
                annuncio = "Siamo in " + str(invitati)

                print(fattore, tipo_fattore)
                print(annuncio)
            """,
            verifica="""
                assert fattore == 2.0, "❌ fattore: dividi invitati per persone_ricetta con /"
                assert tipo_fattore is float, "❌ tipo_fattore: usa type(fattore)"
                assert annuncio == "Siamo in 8", "❌ annuncio: unisci il testo e str(invitati) con +"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `fattore` il risultato della divisione tra `invitati` e `persone_ricetta` e, visto che
                   stampa `2.0` e non `2`, salva in `tipo_fattore` il suo tipo con `type()`.
                2. Salva in `pasta_g` i grammi di spaghetti per otto persone, cioè 320 moltiplicato per `fattore`.
                3. Componi `annuncio` unendo con `+` il testo `"Siamo in "`, il numero di invitati, il testo
                   `", servono "`, i grammi di pasta e il testo `" g di spaghetti"`, convertendo i numeri con `str()`.

                Alla fine `fattore` vale 2.0, `tipo_fattore` è `float`, `pasta_g` vale 640.0 e `annuncio` vale
                `"Siamo in 8, servono 640.0 g di spaghetti"`.
            """,
            suggerimenti=[
                """
                    `str()` trasforma un numero nel testo che serve per unirlo a un'altra stringa con `+`; i grammi
                    restano `640.0` perché `fattore` è un numero con la virgola e il prodotto lo resta.
                """,
            ],
            starter="""
                persone_ricetta = 4
                invitati = 8

                # da creare: fattore, tipo_fattore, pasta_g, annuncio
            """,
            soluzione="""
                persone_ricetta = 4
                invitati = 8

                fattore = invitati / persone_ricetta
                tipo_fattore = type(fattore)
                pasta_g = 320 * fattore
                annuncio = "Siamo in " + str(invitati) + ", servono " + str(pasta_g) + " g di spaghetti"

                print(fattore, tipo_fattore, pasta_g)
                print(annuncio)
            """,
            verifica="""
                assert fattore == 2.0 and tipo_fattore is float, "❌ fattore è invitati / persone_ricetta e tipo_fattore è type(fattore)"
                assert pasta_g == 640.0, "❌ pasta_g: 320 moltiplicato per fattore"
                assert annuncio == "Siamo in 8, servono 640.0 g di spaghetti", "❌ annuncio: unisci i pezzi con + convertendo i numeri con str()"
            """,
        ),
    )

    # E1.2 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Il messaggio agli invitati",
        scenario="""
            Marta deve avvisare gli invitati del giorno, dell'ora e del piatto. Invece di scrivere il messaggio a
            mano vogliamo comporlo con una f-string dalle variabili già nella cella, così se la cena slitta alle 21
            si cambia `ora` e il testo si rigenera. Il piatto, scritto in minuscolo nella lista della spesa, nel
            messaggio va con l'iniziale maiuscola, e prima di inviarlo vogliamo sapere quanti caratteri è, perché
            un SMS ne contiene al massimo 160. Il messaggio comincia con `Cena da Marta sabato alle 20:30: siamo in 8`.
        """,
        base=dict(
            richiesta="""
                1. Salva in `piatto_titolo` il nome del piatto con la prima lettera maiuscola, usando il metodo
                   `.capitalize()` delle stringhe, che restituisce una nuova stringa scritta in questo modo.
                2. Completa la f-string di `messaggio`, inserendo tra le graffe le variabili dell'ora, del numero di
                   invitati e del piatto.
                3. Salva in `lunghezza` il numero di caratteri del messaggio, con la funzione `len()`.

                Il messaggio stampato è `Cena da Marta sabato alle 20:30: siamo in 8 e prepariamo Spaghetti alla carbonara.` e `lunghezza` vale 82, quindi l'SMS ci sta.
            """,
            suggerimenti=[
                """
                    In una f-string ogni coppia di graffe contiene il nome di una variabile, e nel testo compare il
                    suo valore. Il metodo `.capitalize()` non modifica `piatto`, ma restituisce una stringa nuova, che va
                    salvata in `piatto_titolo`.
                """,
                """
                    La prima riga è `piatto_titolo = piatto.capitalize()`; nella f-string servono `{ora}`, `{invitati}` e
                    `{piatto_titolo}`, e la lunghezza si ottiene con `len(messaggio)`.
                """,
            ],
            starter="""
                giorno = "sabato"
                ora = "20:30"
                padrona_di_casa = "Marta"
                invitati = 8
                piatto = "spaghetti alla carbonara"

                piatto_titolo = ...
                messaggio = f"Cena da {padrona_di_casa} {giorno} alle {...}: siamo in {...} e prepariamo {...}."
                lunghezza = ...

                print(messaggio)
                print(lunghezza)
            """,
            soluzione="""
                giorno = "sabato"
                ora = "20:30"
                padrona_di_casa = "Marta"
                invitati = 8
                piatto = "spaghetti alla carbonara"

                piatto_titolo = piatto.capitalize()
                messaggio = f"Cena da {padrona_di_casa} {giorno} alle {ora}: siamo in {invitati} e prepariamo {piatto_titolo}."
                lunghezza = len(messaggio)

                print(messaggio)
                print(lunghezza)
            """,
            verifica="""
                assert piatto_titolo == "Spaghetti alla carbonara", "❌ piatto_titolo: usa piatto.capitalize()"
                assert "Marta" in messaggio and "sabato" in messaggio and "20:30" in messaggio and "in 8" in messaggio and "Spaghetti alla carbonara" in messaggio, "❌ messaggio: controlla che contenga l'ora, il numero di invitati e piatto_titolo"
                assert lunghezza == 82, "❌ lunghezza: conta i caratteri di messaggio con len()"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `piatto_titolo` il nome del piatto con la prima lettera maiuscola, con il metodo
                   `.capitalize()` delle stringhe.
                2. Gli invitati dividono la spesa: calcola in `quota` la spesa a persona, dividendo `spesa` per il
                   numero di invitati.
                3. Componi con una f-string il `messaggio`, che riporta la padrona di casa, il giorno, l'ora, il
                   numero di invitati, il piatto e la quota a persona con due decimali. Dentro le graffe il formato
                   `{quota:.2f}` mostra il numero con due cifre dopo il punto.
                4. Salva in `lunghezza` il numero di caratteri del messaggio, con `len()`.

                Il messaggio stampato è `Cena da Marta sabato alle 20:30: siamo in 8, prepariamo Spaghetti alla carbonara e la spesa è di 2.56 euro a testa.` e `lunghezza` vale 115, quindi l'SMS ci sta.
            """,
            suggerimenti=[
                """
                    La variabile `quota` vale 2.5625 e resta così, perché il formato `:.2f` decide soltanto come il
                    numero compare nella stringa, e infatti `f"{quota:.2f}"` produce `"2.56"`.
                """,
            ],
            starter="""
                giorno = "sabato"
                ora = "20:30"
                padrona_di_casa = "Marta"
                invitati = 8
                piatto = "spaghetti alla carbonara"
                spesa = 20.50

                # da creare: piatto_titolo, quota, messaggio, lunghezza
            """,
            soluzione="""
                giorno = "sabato"
                ora = "20:30"
                padrona_di_casa = "Marta"
                invitati = 8
                piatto = "spaghetti alla carbonara"
                spesa = 20.50

                piatto_titolo = piatto.capitalize()
                quota = spesa / invitati
                messaggio = (
                    f"Cena da {padrona_di_casa} {giorno} alle {ora}: siamo in {invitati}, "
                    f"prepariamo {piatto_titolo} e la spesa è di {quota:.2f} euro a testa."
                )
                lunghezza = len(messaggio)

                print(messaggio)
                print(lunghezza)
            """,
            verifica="""
                assert piatto_titolo == "Spaghetti alla carbonara" and lunghezza == 115, "❌ Controlla piatto_titolo (piatto.capitalize()) e lunghezza (len(messaggio))"
                assert "Marta" in messaggio and "sabato" in messaggio and "20:30" in messaggio and "in 8" in messaggio and "Spaghetti alla carbonara" in messaggio, "❌ messaggio: controlla che contenga padrona di casa, giorno, ora, invitati e piatto_titolo"
                assert "2.56" in messaggio and "2.5625" not in messaggio, "❌ messaggio: la quota va scritta con due decimali, con {quota:.2f}"
            """,
        ),
    )

    # E1.3 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="La lista della spesa",
        scenario="""
            Marta ha buttato giù la lista della spesa nell'ordine in cui le venivano in mente i prodotti. Prima di
            uscire vogliamo sistemarla con qualche riga di codice invece di riscriverla: aggiungere il guanciale che
            manca, togliere il pane che ha già in casa, mettere da parte i primi tre prodotti, che compra nel negozio
            sotto casa, e mandare a Luca la lista in ordine alfabetico per il supermercato. Alla fine la lista
            ordinata comincia con `'guanciale'`.
        """,
        base=dict(
            richiesta="""
                1. Aggiungi `"guanciale"` in fondo alla lista con il metodo `append()`.
                2. Togli `"pane"`, che Marta ha già in casa, con il metodo `remove()`.
                3. Salva in `primi_tre` i primi tre prodotti della lista, quelli del negozio sotto casa, e in
                   `quanti` il numero dei prodotti della lista.
                4. Ordina la lista in ordine alfabetico con il metodo `.sort()`, che, come `append()`, modifica
                   direttamente la lista su cui viene chiamato.

                Alla fine `primi_tre` vale `['spaghetti', 'uova', 'pecorino']`, `quanti` vale 5 e la lista
                ordinata comincia con `'guanciale'`.
            """,
            suggerimenti=[
                """
                    I metodi di una lista si chiamano con il punto dopo il nome della lista e modificano la lista
                    stessa, quindi non serve assegnare il risultato a una variabile. I primi tre elementi si
                    selezionano con lo slicing, prima di ordinare la lista.
                """,
                """
                    Servono `spesa.append(...)`, `spesa.remove(...)`, lo slicing `spesa[:3]`, la funzione `len()` e,
                    per ultimo, `spesa.sort()` senza argomenti.
                """,
            ],
            starter="""
                spesa = ["spaghetti", "uova", "pecorino", "pane", "vino"]

                ...
                ...
                primi_tre = ...
                quanti = ...
                ...

                print(primi_tre)
                print(quanti)
                print(spesa)
            """,
            soluzione="""
                spesa = ["spaghetti", "uova", "pecorino", "pane", "vino"]

                spesa.append("guanciale")
                spesa.remove("pane")
                primi_tre = spesa[:3]
                quanti = len(spesa)
                spesa.sort()

                print(primi_tre)
                print(quanti)
                print(spesa)
            """,
            verifica="""
                assert spesa == ["guanciale", "pecorino", "spaghetti", "uova", "vino"], "❌ spesa: hai aggiunto il guanciale, tolto il pane e ordinato la lista con .sort()?"
                assert primi_tre == ["spaghetti", "uova", "pecorino"], "❌ primi_tre: va preso con [:3] prima di ordinare la lista"
                assert quanti == 5, "❌ quanti: la lista finale ha 5 prodotti"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Aggiungi `"guanciale"` in fondo alla lista e togli `"pane"`, che Marta ha già in casa.
                2. Inserisci `"pepe nero"` in seconda posizione, cioè con indice 1, subito dopo gli spaghetti, perché
                   anche il pepe si compra nel negozio sotto casa. Il metodo `insert(indice, elemento)` inserisce
                   l'elemento nella posizione indicata e sposta in avanti quelli che seguono.
                3. Salva in `primi_tre` i primi tre prodotti della lista e in `quanti` il numero dei prodotti.
                4. Ordina la lista in ordine alfabetico con il metodo `.sort()`.

                Alla fine `primi_tre` vale `['spaghetti', 'pepe nero', 'uova']`, `quanti` vale 6 e la lista
                ordinata comincia con `'guanciale'`.
            """,
            suggerimenti=[
                """
                    L'ordine dei passi conta, perché `.sort()` cambia la posizione degli elementi, quindi `primi_tre`
                    va calcolato prima di ordinare la lista.
                """,
            ],
            starter="""
                spesa = ["spaghetti", "uova", "pecorino", "pane", "vino"]

                # da creare: primi_tre, quanti; alla fine la lista spesa è in ordine alfabetico
            """,
            soluzione="""
                spesa = ["spaghetti", "uova", "pecorino", "pane", "vino"]

                spesa.append("guanciale")
                spesa.remove("pane")
                spesa.insert(1, "pepe nero")
                primi_tre = spesa[:3]
                quanti = len(spesa)
                spesa.sort()

                print(primi_tre)
                print(quanti)
                print(spesa)
            """,
            verifica="""
                assert spesa == ["guanciale", "pecorino", "pepe nero", "spaghetti", "uova", "vino"], "❌ spesa: controlla append, remove, insert e l'ordinamento finale con .sort()"
                assert primi_tre == ["spaghetti", "pepe nero", "uova"], "❌ primi_tre: va preso con [:3] dopo insert e prima di .sort()"
                assert quanti == 6, "❌ quanti: la lista finale ha 6 prodotti"
            """,
        ),
    )

    # E1.4 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Il carrello con i prezzi",
        scenario="""
            Al supermercato Marta segna nel dizionario `prezzi` quanto costa ogni prodotto che mette nel carrello,
            così prima della cassa sa già il totale e ha l'elenco di quello che ha preso. Il dizionario va completato:
            manca il pepe nero, e il prezzo del guanciale è quello della settimana scorsa. Alla fine `totale` vale
            20.5 e `prodotti` elenca i cinque nomi, con `'pepe nero'` per ultimo.
        """,
        base=dict(
            richiesta="""
                1. Aggiungi al dizionario il pepe nero, con la chiave `"pepe nero"` e il prezzo di 2.15 euro.
                2. Correggi il prezzo del guanciale, che è di 7.90 euro.
                3. Calcola in `totale` la somma dei prezzi con `sum(prezzi.values())`, che somma tutti i valori del
                   dizionario.
                4. Salva in `prodotti` la lista dei nomi dei prodotti, cioè delle chiavi del dizionario.

                Alla fine `totale` vale 20.5 e `prodotti` contiene cinque nomi, con `'pepe nero'` all'ultimo posto.
            """,
            suggerimenti=[
                """
                    Per aggiungere una coppia si assegna un valore a una chiave nuova, mentre per correggerla si
                    assegna un valore nuovo a una chiave che esiste già, con la stessa sintassi.
                """,
                """
                    Le due assegnazioni hanno la forma `prezzi["pepe nero"] = 2.15`, e le chiavi si ottengono con
                    `list(prezzi.keys())`.
                """,
            ],
            starter="""
                prezzi = {"spaghetti": 2.58, "guanciale": 8.90, "uova": 3.49, "pecorino": 4.38}

                ...
                ...
                totale = ...
                prodotti = ...

                print(prezzi)
                print(totale)
                print(prodotti)
            """,
            soluzione="""
                prezzi = {"spaghetti": 2.58, "guanciale": 8.90, "uova": 3.49, "pecorino": 4.38}

                prezzi["pepe nero"] = 2.15
                prezzi["guanciale"] = 7.90
                totale = sum(prezzi.values())
                prodotti = list(prezzi.keys())

                print(prezzi)
                print(totale)
                print(prodotti)
            """,
            verifica="""
                assert prezzi.get("pepe nero") == 2.15 and prezzi["guanciale"] == 7.90, "❌ prezzi: aggiungi il pepe nero e correggi il prezzo del guanciale"
                assert round(totale, 2) == 20.5, "❌ totale: somma i valori del dizionario aggiornato con sum(prezzi.values())"
                assert prodotti == ["spaghetti", "guanciale", "uova", "pecorino", "pepe nero"], "❌ prodotti: usa list(prezzi.keys())"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Aggiungi il pepe nero, che costa 2.15 euro, e correggi il prezzo del guanciale, che è di 7.90 euro.
                2. Calcola in `totale` la somma dei prezzi e salva in `prodotti` la lista dei nomi dei prodotti; la
                   funzione `sum()` accetta direttamente il risultato di `prezzi.values()`.
                3. Gli invitati dividono la spesa: calcola in `quota` la parte di ciascuno degli otto, arrotondata al
                   centesimo con `round()`.

                Alla fine `totale` vale 20.5, `prodotti` contiene cinque nomi con `'pepe nero'` all'ultimo posto e
                `quota` vale 2.56.
            """,
            suggerimenti=[
                """
                    Una chiave nuova e una chiave esistente si assegnano con la stessa sintassi,
                    `prezzi[chiave] = valore`; nel primo caso Python crea la coppia, nel secondo sostituisce il valore.
                """,
            ],
            starter="""
                prezzi = {"spaghetti": 2.58, "guanciale": 8.90, "uova": 3.49, "pecorino": 4.38}
                invitati = 8

                # da creare: totale, prodotti, quota (prima va aggiornato il dizionario prezzi)
            """,
            soluzione="""
                prezzi = {"spaghetti": 2.58, "guanciale": 8.90, "uova": 3.49, "pecorino": 4.38}
                invitati = 8

                prezzi["pepe nero"] = 2.15
                prezzi["guanciale"] = 7.90
                totale = sum(prezzi.values())
                prodotti = list(prezzi.keys())
                quota = round(totale / invitati, 2)

                print(totale, quota)
                print(prodotti)
            """,
            verifica="""
                assert prezzi.get("pepe nero") == 2.15 and prezzi["guanciale"] == 7.90, "❌ prezzi: aggiungi il pepe nero e correggi il prezzo del guanciale"
                assert round(totale, 2) == 20.5 and prodotti == ["spaghetti", "guanciale", "uova", "pecorino", "pepe nero"], "❌ Controlla totale (sum dei valori) e prodotti (list delle chiavi)"
                assert quota == 2.56, "❌ quota: dividi il totale per gli invitati e arrotonda con round(..., 2)"
            """,
        ),
    )

    # E1.5 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Due liste, un carrello",
        scenario="""
            Marta e Luca hanno scritto ciascuno la propria lista e alcuni prodotti compaiono in entrambe. Vogliamo un
            unico carrello in cui ogni prodotto compaia una volta sola, senza cercare i doppioni a occhio, e salvare
            l'indirizzo di Marta in una tupla, perché non cambia e Luca deve averlo sotto mano quando passa a portare
            la spesa. Alla fine `carrello` contiene sei prodotti e `civico` vale 14.
        """,
        base=dict(
            richiesta="""
                1. Unisci le due liste in `tutti` con l'operatore `+`, che tra due liste funziona come tra due
                   stringhe e produce una lista nuova con gli elementi della prima seguiti da quelli della seconda.
                2. Salva in `carrello` il set ottenuto da `tutti` con il costruttore `set()`, in modo che ogni prodotto
                   compaia una volta sola, e in `quanti` il numero di prodotti del carrello.
                3. Crea la tupla `indirizzo` con la via, il numero civico e la città, cioè `"via Garibaldi"`, `14` e
                   `"Bologna"`, e salva in `civico` il suo secondo elemento, leggendolo con l'indice.

                Alla fine `tutti` ha otto elementi, `carrello` contiene sei prodotti, `quanti` vale 6 e `civico`
                vale 14.
            """,
            suggerimenti=[
                """
                    L'unione delle due liste conserva i doppioni, perché una lista può contenere lo stesso valore più
                    volte; è il passaggio a set che li elimina. Una tupla si scrive come una lista, ma tra parentesi
                    tonde.
                """,
                """
                    Servono `lista_marta + lista_luca`, `set(tutti)` e `len(carrello)`; il secondo elemento della
                    tupla è `indirizzo[1]`, perché gli indici partono da zero.
                """,
            ],
            starter="""
                lista_marta = ["spaghetti", "guanciale", "uova", "vino"]
                lista_luca = ["vino", "pecorino", "pane", "uova"]

                tutti = ...
                carrello = ...
                quanti = ...

                indirizzo = ...
                civico = ...

                print(tutti)
                print(carrello)
                print(quanti, civico)
            """,
            soluzione="""
                lista_marta = ["spaghetti", "guanciale", "uova", "vino"]
                lista_luca = ["vino", "pecorino", "pane", "uova"]

                tutti = lista_marta + lista_luca
                carrello = set(tutti)
                quanti = len(carrello)

                indirizzo = ("via Garibaldi", 14, "Bologna")
                civico = indirizzo[1]

                print(tutti)
                print(carrello)
                print(quanti, civico)
            """,
            verifica="""
                assert tutti == lista_marta + lista_luca and len(tutti) == 8, "❌ tutti: le due liste unite con +, otto elementi"
                assert carrello == {"spaghetti", "guanciale", "uova", "vino", "pecorino", "pane"} and quanti == 6, "❌ carrello: set(tutti) elimina i doppioni; quanti è la sua lunghezza"
                assert isinstance(indirizzo, tuple) and civico == 14, "❌ indirizzo deve essere una tupla e civico il suo elemento di indice 1"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Trasforma le due liste nei set `marta` e `luca`, poi salva in `carrello` la loro unione, con il
                   metodo `union()`, e in `in_comune` la loro intersezione, con il metodo `intersection()`.
                2. Salva in `solo_luca` i prodotti che porta soltanto Luca, con il metodo `difference()`, che
                   restituisce gli elementi del primo set che non compaiono nel secondo.
                3. Crea la tupla `indirizzo` con `"via Garibaldi"`, `14` e `"Bologna"` e salva in `civico` il numero
                   civico, leggendolo con l'indice.

                Alla fine `carrello` contiene sei prodotti, `in_comune` contiene `'uova'` e `'vino'`, `solo_luca`
                contiene `'pane'` e `'pecorino'` e `civico` vale 14.
            """,
            suggerimenti=[
                """
                    La differenza tra due set dipende dall'ordine in cui si prendono, quindi `luca.difference(marta)`
                    e `marta.difference(luca)` danno risultati diversi.
                """,
            ],
            starter="""
                lista_marta = ["spaghetti", "guanciale", "uova", "vino"]
                lista_luca = ["vino", "pecorino", "pane", "uova"]

                # da creare: marta, luca, carrello, in_comune, solo_luca, indirizzo, civico
            """,
            soluzione="""
                lista_marta = ["spaghetti", "guanciale", "uova", "vino"]
                lista_luca = ["vino", "pecorino", "pane", "uova"]

                marta = set(lista_marta)
                luca = set(lista_luca)
                carrello = marta.union(luca)
                in_comune = marta.intersection(luca)
                solo_luca = luca.difference(marta)

                indirizzo = ("via Garibaldi", 14, "Bologna")
                civico = indirizzo[1]

                print(carrello)
                print(in_comune, solo_luca)
                print(civico)
            """,
            verifica="""
                assert carrello == {"spaghetti", "guanciale", "uova", "vino", "pecorino", "pane"} and in_comune == {"uova", "vino"}, "❌ Controlla carrello (union) e in_comune (intersection)"
                assert solo_luca == {"pecorino", "pane"}, "❌ solo_luca: parti dal set di Luca e togli quello di Marta con difference()"
                assert isinstance(indirizzo, tuple) and civico == 14, "❌ indirizzo deve essere una tupla e civico il suo elemento di indice 1"
            """,
        ),
    )

    # ------------------------------------------------------------------ facoltativi
    nb.md("""
        Gli esercizi che seguono sono facoltativi: se hai finito i primi cinque, puoi continuare con questi. I primi
        due applicano ancora i set e le regole di PEP 8 del notebook 03, mentre la sfida finale è un esercizio libero,
        senza verifica, che mette insieme le celle Markdown e le f-string. Anche sotto questi esercizi c'è la cella
        `soluzione`.
    """)

    # E1.6 ---------------------------------------------------------------
    allergie_richiesta = """
        1. Crea il set `allergie` a partire dalla lista `risposte`, in modo che ogni voce compaia una volta sola.
        2. Salva in `quante` il numero di voci diverse.
        3. Salva in `problema_lattosio` il risultato di `"lattosio" in allergie` e in `problema_uova` quello del
           controllo analogo per le uova. L'operatore `in` restituisce `True` se l'elemento è presente nel set e
           `False` se non lo è.

        Alla fine `quante` vale 3, `problema_lattosio` vale `True` e `problema_uova` vale `False`.
    """
    allergie_soluzione = """
        risposte = ["lattosio", "noci", "lattosio", "crostacei", "noci"]

        allergie = set(risposte)
        quante = len(allergie)
        problema_lattosio = "lattosio" in allergie
        problema_uova = "uova" in allergie

        print(allergie, quante)
        print(problema_lattosio, problema_uova)
    """
    allergie_verifica = """
        assert allergie == {"lattosio", "noci", "crostacei"}, "❌ allergie: trasforma la lista in un set con set()"
        assert quante == 3, "❌ quante: conta gli elementi del set con len()"
        assert problema_lattosio is True and problema_uova is False, "❌ Controlla i due booleani: ciascuno è un controllo con in sul set allergie"
    """
    esercizio_due_aule(
        nb,
        titolo="Allergie",
        facoltativo=True,
        scenario="""
            Marta ha chiesto a tutti se hanno allergie o intolleranze e ha incollato le risposte in una lista, con le
            ripetizioni di chi ha risposto la stessa cosa. Prima di confermare la carbonara, che contiene uova e
            pecorino, vogliamo l'elenco delle allergie diverse e una risposta secca, vera o falsa, a due domande:
            qualcuno è intollerante al lattosio, qualcuno è allergico alle uova. Alla fine `quante` vale 3,
            `problema_lattosio` è `True` e `problema_uova` è `False`.
        """,
        base=dict(
            richiesta=allergie_richiesta,
            suggerimenti=[
                """
                    Un set conserva ogni valore una volta sola, quindi basta trasformare la lista in un set e
                    contarne gli elementi. Il controllo con `in` produce un booleano, che si salva in una variabile
                    come qualunque altro valore.
                """,
                """
                    Servono il costruttore `set(risposte)`, la funzione `len()` e l'espressione
                    `"lattosio" in allergie`, da assegnare a `problema_lattosio`.
                """,
            ],
            starter="""
                risposte = ["lattosio", "noci", "lattosio", "crostacei", "noci"]

                allergie = ...
                quante = ...
                problema_lattosio = ...
                problema_uova = ...

                print(allergie, quante)
                print(problema_lattosio, problema_uova)
            """,
            soluzione=allergie_soluzione,
            verifica=allergie_verifica,
        ),
        avanzata=dict(
            suggerimenti=[
                """
                    Un controllo con `in` è un'espressione come le altre, e il suo valore, `True` o `False`, si
                    assegna a una variabile con `=`.
                """,
            ],
            starter="""
                risposte = ["lattosio", "noci", "lattosio", "crostacei", "noci"]

                # da creare: allergie, quante, problema_lattosio, problema_uova
            """,
        ),
    )

    # E1.7 ---------------------------------------------------------------
    cella_luca = """
        B=3
        p=7.9
        N=8
        T=B*p/N # moltiplico e divido
        print(T)
    """
    esercizio_due_aule(
        nb,
        titolo="La cella del collega",
        facoltativo=True,
        scenario="""
            Luca ha scritto in un notebook condiviso la cella che divide tra gli invitati il costo del vino. Il
            calcolo è giusto, ma tra una settimana nessuno ricorderà che cosa sono `B`, `p` e `N`. Vogliamo
            riscriverla seguendo PEP 8 in modo che si legga da sola: nomi che dicono che cosa contengono, spazi
            attorno agli operatori e un commento che spiega il perché invece di ripetere l'operazione. Alla fine
            `quota_vino` vale lo stesso di `T`, circa 2.96 euro.
        """,
        base=dict(
            richiesta="""
                1. Lascia le righe di Luca come sono, perché servono al confronto.
                2. Sotto, riscrivile seguendo PEP 8: il numero di bottiglie va in `bottiglie`, il prezzo di una
                   bottiglia in `prezzo_bottiglia`, il numero di invitati in `invitati` e il risultato in
                   `quota_vino`.
                3. Al posto del commento che ripete il codice scrivine uno che spieghi perché il costo si divide per
                   il numero di invitati.

                Alla fine `quota_vino` vale lo stesso di `T`.
            """,
            suggerimenti=[
                """
                    PEP 8 chiede nomi in minuscolo con le parole separate da un underscore e uno spazio attorno a `=`
                    e agli operatori. Un commento utile dice da dove viene un numero o perché si fa un'operazione,
                    mentre l'operazione stessa si legge già nel codice.
                """,
                """
                    La riga del calcolo diventa `quota_vino = bottiglie * prezzo_bottiglia / invitati`, e il commento
                    sopra di essa può dire che il vino si paga in parti uguali tra tutti gli invitati.
                """,
            ],
            starter=unisci(cella_luca, """
                bottiglie = ...
                prezzo_bottiglia = ...
                invitati = ...
                # ...
                quota_vino = ...
                print(T, quota_vino)
            """),
            soluzione=unisci(cella_luca, """
                bottiglie = 3
                prezzo_bottiglia = 7.9
                invitati = 8
                # il vino si paga in parti uguali tra tutti gli invitati
                quota_vino = bottiglie * prezzo_bottiglia / invitati
                print(T, quota_vino)
            """),
            verifica="""
                assert bottiglie == 3 and prezzo_bottiglia == 7.9 and invitati == 8, "❌ Controlla nomi e valori di bottiglie, prezzo_bottiglia e invitati"
                assert quota_vino == T, "❌ quota_vino deve avere lo stesso valore di T"
            """,
        ),
        avanzata=dict(
            suggerimenti=[
                """
                    Un commento utile dice da dove viene un numero o perché si fa un'operazione, mentre l'operazione
                    stessa si legge già nel codice.
                """,
            ],
            starter=unisci(cella_luca, """
                # riscrivi qui sotto la cella con i nomi bottiglie, prezzo_bottiglia, invitati e quota_vino
            """),
        ),
    )

    # E1.8 ---------------------------------------------------------------
    nb.esercizio(
        titolo="Sfida: il menu e lo scontrino",
        facoltativo=True,
        scenario="""
            Per chiudere i preparativi Marta vuole un notebook con il menu della serata in una cella Markdown e, sotto,
            lo scontrino della spesa stampato dal dizionario `prezzi`: una riga per prodotto con il prezzo a due
            decimali e il totale in fondo, così se un prezzo cambia basta correggere il dizionario. Non c'è un unico
            risultato giusto, quindi l'esercizio non ha una verifica e la cella `soluzione` mostra un esempio.
        """,
        richiesta="""
            1. Sopra la cella di codice qui sotto aggiungi una cella Markdown con un titolo, per esempio
               `# Menu della cena da Marta`, e un elenco puntato con le portate della serata.
            2. Nella cella di codice stampa lo scontrino a partire dal dizionario `prezzi`, con una riga per ogni
               prodotto che riporti il nome e il prezzo, e in fondo una riga con il totale. Con il formato `:.2f`
               dentro le graffe di una f-string tutti i prezzi compaiono con due decimali.
        """,
        suggerimenti=[
            """
                Senza un ciclo, ogni riga dello scontrino è un `print` con una f-string che legge un prezzo dal
                dizionario, come `prezzi['uova']`. Dentro una f-string scritta tra virgolette doppie conviene
                scrivere la chiave tra apici singoli.
            """,
        ],
        starter="""
            prezzi = {"spaghetti": 2.58, "guanciale": 7.90, "uova": 3.49, "pecorino": 4.38, "pepe nero": 2.15}

            # una riga dello scontrino per ogni prodotto, poi il totale
            ...
        """,
        soluzione="""
            # Nella cella Markdown sopra questa, per esempio:
            #
            # # Menu della cena da Marta
            #
            # - Bruschette al pomodoro
            # - Spaghetti alla carbonara
            # - Tiramisù

            prezzi = {"spaghetti": 2.58, "guanciale": 7.90, "uova": 3.49, "pecorino": 4.38, "pepe nero": 2.15}

            print(f"spaghetti   {prezzi['spaghetti']:.2f} euro")
            print(f"guanciale   {prezzi['guanciale']:.2f} euro")
            print(f"uova        {prezzi['uova']:.2f} euro")
            print(f"pecorino    {prezzi['pecorino']:.2f} euro")
            print(f"pepe nero   {prezzi['pepe nero']:.2f} euro")
            print(f"totale      {sum(prezzi.values()):.2f} euro")
        """,
        verifica=None,
    )
    return nb
