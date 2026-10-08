"""Extra X3 · Data Wrangler (dimostrazione del docente)."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="X3",
        file="Data_Wrangler",
        titolo="Data Wrangler",
        blocco=1,
        giornata=0,
        intento="Data Wrangler mostra un DataFrame come un foglio di calcolo e scrive il codice pandas dei passi fatti con il mouse.",
        obiettivi=[
            "aprire un DataFrame in Data Wrangler",
            "filtrare righe e togliere colonne con i comandi dell'estensione",
            "esportare i passi in una cella di codice e leggerla",
        ],
        tempo=15,
        dati=["letture_pod_2025.csv"],
        extra=True,
    )

    nb.sezione("Il file delle letture", intro="""
        Data Wrangler lavora su un DataFrame già presente in memoria, quindi per provarlo leggiamo prima
        un file. Usiamo le letture mensili di sei POD, divise per fascia, che il file salva con il punto e
        virgola come separatore, la virgola come separatore decimale e l'encoding latin-1; per questo
        passiamo a `read_csv` i parametri `sep`, `decimal` ed `encoding`.
    """)
    nb.code("""
        import pandas as pd

        letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
        letture.head()
    """)

    nb.sezione("Data Wrangler", intro="""
        Data Wrangler è un'estensione di VS Code che mostra un DataFrame come un foglio di calcolo e
        traduce in codice pandas le operazioni fatte con il mouse. È utile per esplorare un dataset in
        fretta, e anche per imparare, perché per ogni operazione mostra la riga di pandas che la esegue.
    """)
    nb.md("""
        L'estensione si apre a partire da un DataFrame già in memoria. Dopo aver eseguito una cella che
        mostra il DataFrame, sotto l'output compare il pulsante **Open 'letture' in Data Wrangler**, dove
        il nome tra apici è quello della variabile. In alternativa si può aprire il pannello
        **Variables** dalla barra del notebook, dove accanto a ogni DataFrame c'è l'icona di Data Wrangler.
    """)
    nb.md("""
        La finestra di Data Wrangler mostra in alto le colonne, ciascuna con un riassunto della
        distribuzione dei valori e del numero di valori mancanti; a destra c'è l'elenco dei passi eseguiti
        e in basso il codice che li produce. All'apertura l'estensione è in sola lettura, in
        **Viewing mode**, e per modificare i dati si passa in **Editing mode** con il pulsante in alto a
        destra. Solo allora compare a sinistra il pannello **Operations**, da cui si scelgono le operazioni.
    """)
    nb.md("""
        Proviamo due operazioni. Con **Filter** teniamo solo le righe in cui la colonna `fascia` vale
        `F1`, e con **Drop columns** togliamo la colonna `cliente`. Ogni passo si vede in anteprima nella
        tabella e si può annullare dall'elenco dei passi. Quando i passi sono quelli voluti, il pulsante
        **Export to notebook** incolla nel notebook una cella come quella qui sotto, che raccoglie i passi
        in una funzione e la applica a una copia del DataFrame.
    """)
    nb.code("""
        # codice incollato da Data Wrangler: i commenti in inglese sono suoi
        def clean_data(letture):
            # Filter rows based on column: 'fascia'
            letture = letture[letture["fascia"] == "F1"]
            # Drop column: 'cliente'
            letture = letture.drop(columns=["cliente"])
            return letture


        letture_clean = clean_data(letture.copy())
        letture_clean.head()
    """)
    nb.md("""
        Il codice generato è lo stesso pandas che scriviamo a mano. Il filtro usa una maschera booleana,
        scritta sulla stessa riga della selezione, e la funzione riceve una copia del DataFrame, così
        l'originale resta intatto. Data Wrangler è quindi un buon modo per ritrovare un metodo che non
        ricordiamo, a patto di leggere il codice che produce e, se serve, di accorciarlo.
    """)
    return nb
