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
        VS Code è l'editor: il programma in cui si aprono i file, si scrive il codice e si eseguono i
        notebook. Il corso è una cartella: in VS Code si apre con **File → Open Folder**, e da quel
        momento tutto quello che compare a sinistra, nell'Explorer, è il contenuto di quella cartella.
    """)
    nb.md("""
        Servono due estensioni, **Python** e **Jupyter**, entrambe di Microsoft: si installano
        dall'icona dei quattro quadratini nella barra a sinistra, cercando il nome. Se questo notebook
        si vede con il codice colorato e i pulsanti sopra le celle, ci sono già.
    """)
    nb.md("""
        Il kernel è il Python che esegue le celle. In alto a destra c'è **Select Kernel**. Se nel menu
        compare già una voce con `.venv` nel nome, è quella. Se no, **Select Another Kernel... → Python
        Environments...** e lì trovi la `.venv`. È l'ambiente virtuale, il virtual environment,
        del corso: dentro ci sono Python e tutte le librerie che servono. Controlliamo subito di aver preso quello giusto: un clic nella
        cella qui sotto e **Shift+Invio**.
    """)
    nb.code("""
        import sys

        sys.executable
    """)
    nb.md("""
        Il percorso che compare deve contenere `.venv`. Se non c'è, il notebook sta usando un altro
        Python, magari quello di sistema, senza le librerie: torna su **Select Kernel** e cambia.
    """)
    nb.code("""
        import pandas as pd

        pd.__version__
    """)
    nb.md("""
        Un numero di versione che inizia per 3: pandas c'è. Queste due celle sono il controllo da fare
        ogni volta che qualcosa sembra sparito.
    """)
    nb.box("attenzione", """
        `ModuleNotFoundError: No module named 'pandas'` alla prima cella del giorno quasi mai vuol dire
        che pandas manca: vuol dire che il kernel selezionato è un altro Python. Prima **Select Kernel**,
        poi tutto il resto.
    """)

    nb.sezione("Run All e Restart", intro="""
        Due pulsanti in cima al notebook fanno il grosso del lavoro. **Run All** esegue tutte le celle
        dall'alto in basso: è la prova che il notebook funziona per intero. **Restart** riavvia il
        kernel: la memoria si svuota, le variabili spariscono, il codice resta. Si usa quando "non torna
        niente": un valore che non ci spieghiamo, una cella che non finisce mai. Restart, poi Run All.
    """)

    nb.sezione("Le scorciatoie da tastiera", intro="""
        Una cella ha due stati: in modifica, quando il cursore è dentro e scriviamo, e selezionata,
        quando è evidenziata e i tasti diventano comandi. **Esc** passa da modifica a selezionata,
        **Invio** torna dentro. Con la cella selezionata bastano questi.
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
        Su Mac, **Cmd** al posto di **Ctrl**. Tutto il resto si trova nei menu e nei pulsanti che
        compaiono passando il mouse sopra una cella: le scorciatoie servono a non staccare le mani dalla
        tastiera, niente di più.
    """)

    return nb
