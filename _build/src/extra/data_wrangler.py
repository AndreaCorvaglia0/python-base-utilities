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
        Per provare Data Wrangler serve un DataFrame in memoria: le letture mensili di sei POD, per
        fascia. Lo leggiamo con separatore `;`, virgola decimale ed encoding latin-1.
    """)
    nb.code("""
        import pandas as pd

        letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
        letture.head()
    """)

    nb.sezione("Data Wrangler", intro="""
        Data Wrangler è un'estensione di VS Code che mostra un DataFrame come un foglio di calcolo e
        traduce i clic in codice pandas. Serve per esplorare in fretta e per imparare: ogni
        operazione fatta con il mouse mostra la riga di pandas che la fa.
    """)
    nb.md("""
        Si apre da un DataFrame già in memoria. Dopo aver eseguito una cella che lo mostra, sotto
        l'output compare il pulsante **Open 'letture' in Data Wrangler** (il nome tra apici è quello
        della variabile); in alternativa, nel pannello
        **Variables** della barra del notebook, ogni DataFrame ha l'icona di Data Wrangler accanto.
    """)
    nb.md("""
        Dentro: in alto le colonne con un riassunto (distribuzione, mancanti), a destra la lista dei
        passi fatti, in basso il codice che li produce. Le operazioni si scelgono dal pannello
        **Operations** a sinistra, che compare solo in **Editing mode**: all'apertura Data Wrangler è
        in sola lettura (Viewing mode), si cambia con il pulsante in alto a destra.
    """)
    nb.md("""
        Proviamone due: **Filter** sulla colonna `fascia` uguale a `F1`, poi **Drop columns** su
        `cliente`. Ogni passo si vede in anteprima e si può annullare.
    """)
    nb.md("""
        Il pulsante **Export to notebook** incolla nel notebook una cella come questa: una funzione
        con i passi, applicata a una copia del DataFrame.
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
        Leggiamolo: è lo stesso pandas di questo notebook, con maschera e filtro sulla stessa riga e
        `.copy()` per non toccare l'originale. Data Wrangler è un buon modo per scoprire il metodo
        che non ricordiamo; il codice che produce va letto, e se serve accorciato.
    """)
    return nb
