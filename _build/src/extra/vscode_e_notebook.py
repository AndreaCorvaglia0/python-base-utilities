"""Extra X0 · VS Code e notebook (dimostrazione del docente)."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="X0",
        file="VS_Code_e_notebook",
        titolo="VS Code e notebook",
        blocco=1,
        giornata=0,
        intento="Come si apre il corso in VS Code, come si sceglie il kernel e quali comandi servono per lavorare sulle celle.",
        obiettivi=[
            "aprire un notebook in VS Code e scegliere il kernel giusto",
            "usare Run All e Restart quando i risultati non tornano",
            "lavorare sulle celle con le scorciatoie da tastiera",
        ],
        tempo=15,
        dati=[],
        extra=True,
    )

    nb.sezione("VS Code e il kernel", intro="""
        VS Code è l'editor del corso, cioè il programma in cui apriamo i file, scriviamo il codice ed
        eseguiamo i notebook. Il materiale del corso è una cartella, che in VS Code si apre con
        **File → Open Folder**. Da quel momento il pannello Explorer, a sinistra, mostra il contenuto di
        quella cartella, e da lì si apre ogni notebook con un clic.
    """)
    nb.md("""
        Per lavorare con i notebook servono due estensioni di Microsoft, **Python** e **Jupyter**. Si
        installano dal pannello delle estensioni, che si apre con l'icona dei quattro quadratini nella
        barra a sinistra, cercandole per nome. Se questo notebook compare con il codice colorato e con i
        pulsanti sopra le celle, le estensioni sono già installate.
    """)
    nb.md("""
        Il kernel è il processo Python che esegue le celle, e si sceglie con il pulsante **Select Kernel**
        in alto a destra. Se nel menu compare già una voce con `.venv` nel nome, è quella giusta;
        altrimenti si passa da **Select Another Kernel... → Python Environments...**, dove si trova la
        `.venv`. La `.venv` è l'ambiente virtuale, il virtual environment, del corso, e contiene Python e
        tutte le librerie che servono. Per controllare di aver scelto quello giusto, facciamo clic nella
        cella qui sotto e premiamo **Shift+Invio**.
    """)
    nb.code("""
        import sys

        sys.executable
    """)
    nb.md("""
        Il percorso stampato deve contenere `.venv`. Se non lo contiene, il notebook sta usando un altro
        Python, per esempio quello di sistema, nel quale le librerie del corso non sono installate; in
        questo caso si torna su **Select Kernel** e si sceglie l'ambiente del corso. La cella seguente
        completa il controllo importando pandas e mostrandone la versione.
    """)
    nb.code("""
        import pandas as pd

        pd.__version__
    """)
    nb.md("""
        Se compare un numero di versione che inizia per 3, pandas è installato nell'ambiente scelto.
        Queste due celle sono il controllo da ripetere ogni volta che una libreria sembra sparita, o che
        un notebook che il giorno prima funzionava dà errori già all'importazione.
    """)
    nb.box("attenzione", """
        Un `ModuleNotFoundError` alla prima cella della giornata indica di solito che è selezionato il
        kernel sbagliato, e solo raramente che manca una libreria. Per questo conviene controllare
        **Select Kernel** prima di provare qualsiasi altra soluzione.
    """)

    nb.sezione("Run All e Restart", intro="""
        In cima al notebook ci sono due pulsanti che si usano spesso. **Run All** esegue tutte le celle
        dall'alto in basso ed è il modo più semplice per verificare che il notebook funzioni per intero.
        **Restart** riavvia il kernel. Il codice scritto nelle celle rimane dov'è, ma le variabili create
        fino a quel momento vengono perse, perché esistevano solo nella memoria del processo appena
        chiuso. Quando un risultato non si spiega o una cella non finisce mai, conviene premere Restart e
        poi Run All, così il notebook riparte da uno stato pulito.
    """)

    nb.sezione("Le scorciatoie da tastiera", intro="""
        Una cella può trovarsi in due stati. È in modifica quando il cursore è al suo interno e stiamo
        scrivendo, ed è selezionata quando è evidenziata e i tasti funzionano come comandi. Il tasto
        **Esc** passa dalla modifica alla selezione e **Invio** torna dentro la cella. La tabella seguente
        raccoglie i comandi che bastano nel lavoro di tutti i giorni, da usare con la cella selezionata.
    """)
    nb.md("""
        | Tasto | Cosa fa |
        |---|---|
        | **Shift+Invio** | esegue la cella e passa alla successiva (funziona anche in modifica) |
        | **A** / **B** | nuova cella sopra (*above*) / sotto (*below*) |
        | **M** / **Y** | la cella diventa Markdown / codice |
        | **D D** | cancella la cella (D premuto due volte) |
        | **Ctrl+S** | salva il notebook (funziona sempre) |
    """)
    nb.md("""
        Su Mac si usa **Cmd** al posto di **Ctrl**. Tutti gli altri comandi si trovano nei menu e nei
        pulsanti che compaiono passando il mouse sopra una cella; le scorciatoie servono a lavorare senza
        staccare le mani dalla tastiera.
    """)

    return nb
