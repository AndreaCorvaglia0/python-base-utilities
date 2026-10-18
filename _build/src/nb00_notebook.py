"""00 · Jupyter e i notebook: usare un notebook in VS Code, prima di sapere il Python."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="00",
        file="00_Notebook",
        titolo="Jupyter e i notebook",
        blocco=1,
        giornata=1,
        intento=(
            "In questo notebook impariamo a usare un notebook Jupyter in VS Code, lo strumento in cui scriviamo "
            "ed eseguiamo il codice del corso: celle, esecuzione, variabili in memoria e riavvio del kernel."
        ),
        obiettivi=[
            "riconoscere, creare, eseguire ed eliminare celle di codice e celle Markdown, con tre scorciatoie",
            "seguire le variabili in memoria nella vista Variables di VS Code",
            "capire perché conta l'ordine in cui si eseguono le celle e che cosa fanno Restart e Run All",
        ],
        tempo={"base": 25, "avanzata": 20},
        dati=[],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("L'obiettivo del corso", intro="""
        Una parte crescente del codice viene oggi scritta da un agente per il coding, come Copilot in
        VS Code. Anche in quel caso il codice va letto e controllato da chi lo usa, e per riuscirci
        bisogna conoscere il linguaggio in cui è scritto. Per questo nella prima parte del corso
        scriviamo il codice a mano, un'istruzione alla volta, e lo affidiamo a un agente solo
        nell'ultimo modulo.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Cos'è Jupyter Notebook", intro="""
        *Jupyter Notebook* è un ambiente di lavoro interattivo in cui il codice eseguibile convive con il
        testo formattato e con i risultati, come tabelle e grafici. È molto usato nell'analisi dei dati,
        perché tiene insieme in un unico file il codice, quello che produce e la sua spiegazione. Nel corso
        i notebook si aprono e si eseguono in VS Code, e questo notebook serve proprio a prendere confidenza
        con lo strumento: il Python vero e proprio comincia dal notebook 01, e qui ci bastano qualche
        variabile e qualche `print`.

        [Documentazione ufficiale di Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html)
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Celle di codice e celle Markdown", intro="""
        Un notebook è una sequenza di **celle**, di due tipi. Le celle di codice contengono istruzioni
        Python: in VS Code stanno in un riquadro, con un triangolo a sinistra per eseguirle e l'indicazione
        `Python` in basso a destra. Le celle **Markdown** contengono testo formattato, come questa che stai
        leggendo, e quando le apri con un doppio clic riportano `Markdown` in basso a destra. Per eseguire
        una cella di codice si clicca il triangolo, oppure si preme **Shift + Invio**, e il risultato
        compare subito sotto la cella.
    """)
    nb.code("""
        # una cella di codice: eseguila con il triangolo a sinistra oppure con Shift + Invio
        print("Ciao dal notebook")
    """)
    nb.md("""
        L'istruzione `print` stampa sotto la cella quello che le passiamo tra parentesi; il testo va
        scritto tra virgolette. Nella cella successiva c'è un'altra istruzione, `nome = ...`, che crea una
        **variabile**, cioè un nome a cui associamo un valore: da quel momento possiamo usare `nome` al
        posto del valore. Variabili e `print` sono tutto il Python che serve in questo notebook.
    """)
    nb.hands_on(
        richiesta="""
            Nella cella qui sotto sostituisci i puntini con il tuo nome, scritto tra virgolette, per esempio
            `"Anna"`, ed esegui la cella con il triangolo a sinistra. Sotto la cella compare `Ciao, Anna`.
        """,
        starter="""
            nome = ...
            print("Ciao,", nome)
        """,
        soluzione="""
            nome = "Anna"
            print("Ciao,", nome)  # Output: Ciao, Anna
        """,
        verifica="""
            assert isinstance(nome, str) and nome.strip(), "❌ nome deve essere un testo tra virgolette, per esempio \\"Anna\\""
        """,
    )
    nb.md("""
        La cella che segue è una cella Markdown. In questo momento ne vedi la versione formattata, con un
        titolo, una parola in grassetto e un elenco; facendo doppio clic sulla cella compare invece il testo
        di partenza, in cui il titolo comincia con `#` e il grassetto è racchiuso tra due asterischi. Dopo
        aver cambiato una parola si torna alla vista formattata con **Shift + Invio**, come per eseguire una
        cella di codice.
    """)
    nb.md("""
        ## Un titolo Markdown

        Un testo con una parola in **grassetto**.

        - primo elemento di un elenco
        - secondo elemento
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Creare ed eliminare celle", intro="""
        Le celle si creano con i pulsanti **+ Code** e **+ Markdown**, che compaiono passando con il mouse
        tra una cella e l'altra, e si eliminano con l'icona del cestino nella piccola barra in alto a destra
        della cella selezionata. Con la tastiera si lavora più in fretta, e bastano tre scorciatoie.
        **Shift + Invio** esegue la cella e passa alla successiva. **Esc** e poi **B** creano una cella di
        codice nuova sotto quella selezionata, e **A** al posto di **B** la crea sopra. **Esc** e poi **M**
        trasformano la cella selezionata in una cella Markdown. Il tasto **Esc** serve a uscire dalla scrittura dentro la cella, in modo che il
        tasto successivo agisca sulla cella intera.
    """)
    nb.code("""
        # punto di partenza per il Hands-on: clicca su questa cella
        print("Sotto questa cella creiamo le nostre")
    """)
    nb.code("""
        # questa cella va eliminata con l'icona del cestino
    """)
    nb.hands_on(
        richiesta="""
            1. Clicca sulla cella `punto di partenza` qui sopra, premi **Esc** e poi **B**: sotto compare una
               cella di codice nuova.
            2. Scrivi nella cella nuova `print("La mia prima cella")` ed eseguila con **Shift + Invio**.
            3. Premi **Esc**, poi **B** per un'altra cella nuova e **M** per trasformarla in Markdown; scrivi
               `## Le mie prove` e premi **Shift + Invio**: compare un titolo.
            4. Elimina la cella `questa cella va eliminata` con l'icona del cestino.
        """,
        prova_anche="se elimini per errore una cella, **Ctrl + Z** (su Mac **Cmd + Z**) la fa ricomparire, purché tu sia fuori dalla cella, dopo **Esc**.",
    )

    # ------------------------------------------------------------------ 5
    nb.sezione("Il kernel e le variabili", intro="""
        Il codice delle celle non viene eseguito da VS Code, ma da un programma separato, il **kernel**, che
        tiene in memoria le variabili create durante il lavoro. Per questo una variabile creata in una cella
        resta disponibile in tutte le altre: vive nella memoria del kernel e non nella cella che l'ha
        definita. Il kernel del corso deve essere quello dell'ambiente del progetto, e la cella qui sotto lo
        controlla: il percorso stampato deve contenere `.venv`, altrimenti si cambia kernel con il pulsante
        **Select Kernel**, in alto a destra. Le istruzioni della cella le capiremo più avanti, e per ora
        basta guardare il risultato.
    """)
    nb.code("""
        # il Python usato dal kernel: il percorso deve contenere .venv
        import sys

        sys.executable
    """)
    nb.md("""
        Le due celle che seguono creano due variabili, `citta` e `temperatura`, e la terza le usa. La terza
        cella funziona anche se le variabili sono state create altrove, perché il kernel le ricorda.
    """)
    nb.code("""
        citta = "Milano"
    """)
    nb.code("""
        temperatura = 18
    """)
    nb.code("""
        print("Oggi a", citta, "ci sono", temperatura, "gradi")  # Output: Oggi a Milano ci sono 18 gradi
    """)
    nb.md("""
        VS Code mostra in ogni momento le variabili che il kernel ha in memoria. Il pulsante **Variables**,
        nella barra in cima al notebook, apre in basso la scheda **JUPYTER** con una riga per variabile: il
        nome, il tipo e il valore. Se il pulsante non si vede, si trova nel menu `...` della stessa barra, e
        in alternativa si apre la palette dei comandi con **Ctrl + Shift + P** (su Mac **Cmd + Shift + P**) e
        si cerca *variables*.
    """)
    nb.hands_on(
        richiesta="""
            Apri la vista delle variabili e trova `nome`, `citta` e `temperatura`. Poi nella cella qui sotto
            scrivi `giorni = 7` ed eseguila: nella vista compare una riga nuova, con il nome `giorni`, il tipo
            `int` e il valore `7`.
        """,
        starter="""
            giorni = ...
        """,
        soluzione="""
            giorni = 7
        """,
        verifica="""
            assert giorni == 7, "❌ giorni deve valere 7"
        """,
        prova_anche="cambia `giorni = 7` in `giorni = 30`, riesegui la cella e guarda il valore cambiare nella vista.",
    )

    # ------------------------------------------------------------------ 6
    nb.sezione("L'ordine di esecuzione", intro="""
        Il kernel esegue le celle nell'ordine in cui le lanciamo, non in quello in cui compaiono sullo
        schermo, e tiene sempre l'ultimo valore assegnato a ogni variabile. Il numero tra parentesi quadre a
        sinistra di ogni cella, come `[5]`, dice in che momento è stata eseguita, e lo stesso numero cresce a
        ogni esecuzione. Di solito si eseguono le celle dall'alto in basso e il problema non si pone, ma
        rieseguire una cella più in alto dopo averne eseguite altre può dare un risultato diverso da quello
        che ci si aspetta leggendo il notebook. Le tre celle che seguono servono a vederlo.
    """)
    nb.code("""
        prezzo = 10
    """)
    nb.code("""
        print(prezzo * 2)
    """)
    nb.code("""
        prezzo = 15
    """)
    nb.hands_on(
        richiesta="""
            1. Esegui le tre celle qui sopra nell'ordine: la seconda stampa `20`.
            2. Torna alla seconda cella e rieseguila: ora stampa `30`, perché il kernel ha in memoria
               l'ultimo valore assegnato a `prezzo`, quello della terza cella, anche se sullo schermo la
               terza cella viene dopo.
            3. Guarda il numero tra parentesi a sinistra delle tre celle: la seconda ha adesso il numero più
               alto, perché è l'ultima eseguita.
        """,
    )

    # ------------------------------------------------------------------ 7
    nb.sezione("Restart e Run All", intro="""
        Il pulsante **Restart**, nella barra in cima al notebook, riavvia il kernel. Il codice scritto nelle
        celle rimane dov'è, ma le variabili create fino a quel momento vengono perse, perché esistevano solo
        nella memoria del kernel appena chiuso. Il pulsante **Run All** esegue invece tutte le celle
        dall'alto in basso, nell'ordine in cui compaiono, e ricostruisce le variabili. Restart seguito da
        Run All è quindi il modo più sicuro per controllare che il notebook funzioni da capo a fondo, senza
        dipendere da celle eseguite fuori ordine. Se una cella dà errore, Run All si ferma lì.
    """)
    nb.code("""
        print(citta)
    """)
    nb.hands_on(
        richiesta="""
            1. Premi **Restart** in cima al notebook: la vista delle variabili si svuota.
            2. Esegui la cella `print(citta)` qui sopra: compare un errore, e l'ultima riga dice
               `NameError: name 'citta' is not defined`, cioè che il nome `citta` non esiste più.
            3. Premi **Run All**: le celle vengono eseguite dall'alto, la cella stampa di nuovo `Milano` e
               nella vista ricompaiono le variabili.
        """,
    )

    # ------------------------------------------------------------------ Extra
    nb.sezione("Extra", """
        Questa sezione raccoglie due esercizi brevi per rifare a casa, da soli, i gesti di questo notebook;
        durante la lezione la saltiamo. Ogni esercizio dice esattamente che cosa scrivere, e sotto la cella da
        completare c'è la verifica, che stampa ✅ se il risultato è corretto e altrimenti dice che cosa non
        torna.
    """)
    nb.esercizio(
        titolo="Una cella Markdown e una cella di codice",
        scenario="""
            Costruiamo una coppia di celle, una Markdown con un titolo e una frase e, sotto, una di codice che
            stampa una riga, come quelle che si incontrano in ogni notebook del corso. Alla fine il titolo
            compare formattato e sotto la cella di codice si legge `Primo comando Python del corso!`.
        """,
        richiesta="""
            1. Clicca sulla cella di codice qui sotto, premi **Esc** e poi **A**: sopra compare una cella nuova.
               Trasformala in Markdown con **M**.
            2. Scrivi nella cella Markdown `# Il mio primo notebook` e, su una riga nuova, `Questa cella spiega
               quella sotto.`, poi premi **Shift + Invio**.
            3. Nella cella di codice sostituisci i puntini con `"Primo comando Python del corso!"`, tra
               virgolette, ed eseguila con **Shift + Invio**.
        """,
        starter="""
            messaggio = ...
            print(messaggio)
        """,
        soluzione="""
            messaggio = "Primo comando Python del corso!"
            print(messaggio)  # Output: Primo comando Python del corso!
        """,
        verifica="""
            assert messaggio == "Primo comando Python del corso!", "❌ messaggio: copia il testo esatto, tra virgolette"
        """,
        perche="""
            Il testo della cella Markdown, cioè quello che si vede con un doppio clic, è il seguente:

            ```markdown
            # Il mio primo notebook

            Questa cella spiega quella sotto.
            ```
        """,
    )
    nb.esercizio(
        titolo="Variabili, Restart e Run All",
        scenario="""
            Rifacciamo da capo il giro delle variabili: le creiamo, le guardiamo nella vista **Variables**, le
            perdiamo con **Restart** e le ritroviamo con **Run All**. Alla fine la cella stampa
            `Domani a Torino ci saranno 21 gradi` e la vista mostra `citta_domani` e `gradi_domani`.
        """,
        richiesta="""
            1. Nella cella qui sotto scrivi `citta_domani = "Torino"` e `gradi_domani = 21` al posto dei
               puntini, ed eseguila.
            2. Apri la vista delle variabili e trova le due righe nuove.
            3. Premi **Restart** e controlla che la vista si svuoti.
            4. Premi **Run All** e controlla che la cella stampi di nuovo la riga e che le due variabili
               ricompaiano nella vista.
        """,
        starter="""
            citta_domani = ...
            gradi_domani = ...
            print("Domani a", citta_domani, "ci saranno", gradi_domani, "gradi")
        """,
        soluzione="""
            citta_domani = "Torino"
            gradi_domani = 21
            print("Domani a", citta_domani, "ci saranno", gradi_domani, "gradi")  # Output: Domani a Torino ci saranno 21 gradi
        """,
        verifica="""
            assert citta_domani == "Torino" and gradi_domani == 21, "❌ citta_domani vale \\"Torino\\", tra virgolette, e gradi_domani vale 21, senza virgolette"
        """,
    )
    return nb
