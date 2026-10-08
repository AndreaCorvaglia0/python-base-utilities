"""E1 · Esercitazione 1: domande ed esercizi sul blocco 1 (notebook 00-03)."""

from nbkit import Cella, Notebook, box_html


def costruisci() -> Notebook:
    nb = Notebook(
        num="E1",
        file="Esercitazione_1",
        titolo="Esercitazione 1",
        blocco=1,
        giornata=1,
        intento="Questa esercitazione raccoglie alcune domande e alcuni esercizi su variabili, numeri, stringhe, liste, tuple, dizionari e set.",
        obiettivi=[
            "prevedere il risultato di una riga di codice prima di eseguirla",
            "usare variabili, operatori e stringhe su un caso concreto",
            "modificare liste e dizionari e selezionarne una parte",
        ],
        tempo={"base": 20, "avanzata": 20},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Domande", intro="""
        Le domande che seguono riguardano i notebook 00-03. Per ciascuna prova a prevedere il risultato a mente,
        e solo dopo controllalo scrivendo la riga in una cella di codice. Se la risposta di Python è diversa da quella
        che ti aspettavi, conviene rileggere la parte del notebook che tratta quell'argomento.
    """)
    nb.md("""
        1. Cosa stampa `print(7 // 2)`?
        2. Che tipo restituisce `type(10 / 2)`?
        3. Con `numeri = [3, 6, 9, 12, 15]`, cosa restituisce `numeri[1:3]`?
        4. Con `t = (1, 2, 3)`, cosa succede se eseguiamo `t[0] = 5`?
        5. Cosa restituisce `len(set(["pane", "latte", "pane"]))`?
    """)
    nb.celle.append(Cella("md", box_html("soluzione", """
        1. Stampa `3`. L'operatore `//` calcola la divisione intera, quindi del quoziente 3.5 tiene soltanto la parte intera.
        2. Restituisce `<class 'float'>`. La divisione con `/` produce sempre un `float`, anche quando il risultato è un
           numero intero, perciò `10 / 2` vale `5.0` e non `5`.
        3. Restituisce `[6, 9]`. Lo slicing parte dall'indice 1, che contiene il 6, e si ferma prima dell'indice 3, quindi
           il 12 resta escluso.
        4. Python solleva un `TypeError`, perché le tuple sono immutabili e non permettono di sostituire un elemento dopo
           la loro creazione.
        5. Restituisce `2`. Un set non ammette duplicati, quindi dei due `"pane"` ne conserva uno solo e gli elementi
           rimasti sono `"pane"` e `"latte"`.
    """, titolo="Risposte"), solo_soluzioni=True))

    # ------------------------------------------------------------------ 2
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il budget del viaggio",
        scenario="""
            Due amici passano 4 notti a Lisbona. La camera d'albergo costa 85 euro a notte e il volo 160 euro in
            tutto. Vogliamo sapere quanto costa il viaggio e quanto spende ciascuno dei due.
        """,
        richiesta="""
            1. Calcola in `totale` il costo del viaggio, cioè il numero di notti per il prezzo a notte più il costo del volo.
            2. Calcola in `a_persona` quanto spende ciascuno dei due amici.
            3. Componi con l'operatore `+` la stringa `titolo`, che deve valere `"Viaggio a Lisbona"`, unendo un testo
               fisso alla variabile `destinazione`.
        """,
        starter="""
            destinazione = "Lisbona"
            notti = 4
            prezzo_notte = 85
            volo = 160
            persone = 2

            totale = ...
            a_persona = ...
            titolo = ...

            print(totale)     # Output: 500
            print(a_persona)  # Output: 250.0
            print(titolo)     # Output: Viaggio a Lisbona
        """,
        soluzione="""
            destinazione = "Lisbona"
            notti = 4
            prezzo_notte = 85
            volo = 160
            persone = 2

            totale = notti * prezzo_notte + volo
            a_persona = totale / persone
            titolo = "Viaggio a " + destinazione

            print(totale)     # Output: 500
            print(a_persona)  # Output: 250.0
            print(titolo)     # Output: Viaggio a Lisbona
        """,
        verifica="""
            assert totale == 500, "❌ Il totale non torna: 4 notti × 85 + 160"
            assert a_persona == 250, "❌ Dividi il totale per il numero di persone"
            assert titolo == "Viaggio a Lisbona", "❌ Controlla lo spazio dopo 'a'"
        """,
    )
    nb.esercizio(
        titolo="La lista della spesa",
        scenario="""
            Prima di uscire per la spesa della settimana sistemiamo la lista, aggiungendo un prodotto che avevamo
            dimenticato e togliendone uno che non serve più comprare.
        """,
        richiesta="""
            1. Aggiungi `"olio"` in fondo alla lista.
            2. Togli `"uova"`, che abbiamo già in casa.
            3. Salva in `primi_tre` i primi tre elementi della lista aggiornata e in `ultimi_due` gli ultimi due.
            4. Salva in `quanti` il numero di elementi della lista.
        """,
        suggerimento="servono i metodi `append()` e `remove()`, lo slicing con `[:3]` e `[-2:]` e la funzione `len()`.",
        starter="""
            spesa = ["pane", "latte", "uova", "mele", "pasta", "caffè"]

            ...
            ...
            primi_tre = ...
            ultimi_due = ...
            quanti = ...

            print(spesa)  # Output: ['pane', 'latte', 'mele', 'pasta', 'caffè', 'olio']
        """,
        soluzione="""
            spesa = ["pane", "latte", "uova", "mele", "pasta", "caffè"]

            spesa.append("olio")
            spesa.remove("uova")
            primi_tre = spesa[:3]
            ultimi_due = spesa[-2:]
            quanti = len(spesa)

            print(spesa)  # Output: ['pane', 'latte', 'mele', 'pasta', 'caffè', 'olio']
        """,
        verifica="""
            assert primi_tre == ["pane", "latte", "mele"], "❌ primi_tre: hai tolto le uova prima di selezionare?"
            assert ultimi_due == ["caffè", "olio"], "❌ ultimi_due: l'olio va aggiunto in fondo"
            assert quanti == 6, "❌ La lista finale ha 6 elementi"
        """,
    )
    nb.esercizio(
        titolo="I voti in pagella",
        scenario="""
            I voti di uno studente sono raccolti in un dizionario, in cui ogni chiave è il nome di una materia e il
            valore corrispondente è il voto.
        """,
        richiesta="""
            1. Aggiungi il voto di inglese, che è 9.
            2. Correggi il voto di storia, registrato per errore come 6, portandolo a 7.
            3. Salva in `materie` la lista delle chiavi del dizionario, cioè i nomi delle materie.
            4. Calcola in `media` la media dei quattro voti.
        """,
        suggerimento="`sum(voti.values())` restituisce la somma dei voti e `len(voti)` il numero delle materie, quindi la media è il rapporto tra i due.",
        starter="""
            voti = {"matematica": 7, "italiano": 8, "storia": 6}

            ...
            ...
            materie = ...
            media = ...

            print(voti)   # Output: {'matematica': 7, 'italiano': 8, 'storia': 7, 'inglese': 9}
            print(media)  # Output: 7.75
        """,
        soluzione="""
            voti = {"matematica": 7, "italiano": 8, "storia": 6}

            voti["inglese"] = 9
            voti["storia"] = 7
            materie = list(voti.keys())
            media = sum(voti.values()) / len(voti)

            print(voti)   # Output: {'matematica': 7, 'italiano': 8, 'storia': 7, 'inglese': 9}
            print(media)  # Output: 7.75
        """,
        verifica="""
            assert voti["storia"] == 7 and voti["inglese"] == 9, "❌ Controlla i voti di storia e inglese"
            assert materie == ["matematica", "italiano", "storia", "inglese"], "❌ materie: usa list(voti.keys())"
            assert media == 7.75, "❌ La media dei quattro voti è 7.75"
        """,
    )
    return nb
