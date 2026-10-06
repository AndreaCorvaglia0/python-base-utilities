"""E2 · Esercitazione 2: domande ed esercizi sul blocco 2 (notebook 04-06)."""

from nbkit import Cella, Notebook, box_html


def costruisci() -> Notebook:
    nb = Notebook(
        num="E2",
        file="Esercitazione_2",
        titolo="Esercitazione 2",
        blocco=2,
        giornata=1,
        intento="Qualche domanda e qualche esercizio su cicli, funzioni, errori e lettura dei dati con pandas.",
        obiettivi=[
            "prevedere cosa fanno un ciclo e una funzione prima di eseguirli",
            "leggere un traceback e correggere l'errore che segnala",
            "leggere un file o una tabella di dati e descriverli con head, info e describe",
        ],
        tempo=30,
        dati=["letture_pod_2025.csv", "utility.db"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Domande", intro="""
        Rispondi a mente, poi controlla copiando il codice in una cella (per la domanda 5 serve `import pandas as pd`).
    """)
    nb.md("""
        **1.** Cosa stampa questo ciclo?
        ```python
        for n in [3, 8, 5, 12]:
            if n > 4:
                print(n)
        ```
        **2.** Cosa restituisce `prezzo_finale(50)`?
        ```python
        def prezzo_finale(prezzo, sconto=10):
            return prezzo - prezzo * sconto / 100
        ```
        **3.** Quale errore dà questa cella?
        ```python
        def saluta(nome):
            print(f"Ciao {nome}")

        saluta()
        ```
        **4.** Quanto vale `x` alla fine?
        ```python
        x = 10
        while x > 0:
            x = x - 3
        ```
        **5.** Con `df = pd.DataFrame({"Nome": ["Alice", "Bob"], "Età": [24, 27]})`, che tipo è `df["Età"]`?
    """)
    nb.celle.append(Cella("md", box_html("soluzione", """
        1. `8`, `5` e `12`, uno per riga: il `print` scatta solo per i numeri maggiori di 4.
        2. `45.0`: `sconto` vale 10 per default e la divisione con `/` dà un `float`.
        3. `TypeError: saluta() missing 1 required positional argument: 'nome'`: il parametro `nome` non ha un default.
        4. `-2`: `x` passa per 10, 7, 4, 1 e -2, e a quel punto la condizione `x > 0` è falsa.
        5. Una `Series` (`<class 'pandas.Series'>`): una colonna di un DataFrame.
    """, titolo="Risposte"), solo_soluzioni=True))

    # ------------------------------------------------------------------ 2
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="I giorni caldi",
        scenario="Abbiamo segnato la temperatura massima di ogni giorno della settimana sul balcone di casa.",
        richiesta="""
            1. Scrivi la funzione `giorni_caldi(temperature, soglia=25)` che restituisce quanti giorni hanno
               una temperatura di almeno `soglia` gradi.
            2. Usala sulla lista `settimana`, prima con la soglia di default e poi con `soglia=30`.
        """,
        suggerimento="parti da un contatore a 0 e aumentalo di 1 dentro un `if`, nel ciclo `for`.",
        starter="""
            def giorni_caldi(temperature, soglia=25):
                \"\"\"Restituisce quanti giorni hanno una temperatura di almeno soglia gradi.\"\"\"
                ...

            settimana = [22.5, 26.0, 31.2, 24.8, 25.0, 19.5, 27.3]

            print(giorni_caldi(settimana))             # Output: 4
            print(giorni_caldi(settimana, soglia=30))  # Output: 1
        """,
        soluzione="""
            def giorni_caldi(temperature, soglia=25):
                \"\"\"Restituisce quanti giorni hanno una temperatura di almeno soglia gradi.\"\"\"
                conta = 0
                for t in temperature:
                    if t >= soglia:
                        conta += 1
                return conta

            settimana = [22.5, 26.0, 31.2, 24.8, 25.0, 19.5, 27.3]

            print(giorni_caldi(settimana))             # Output: 4
            print(giorni_caldi(settimana, soglia=30))  # Output: 1
        """,
        verifica="""
            assert giorni_caldi(settimana) == 4, "❌ Con la soglia di default i giorni sono 4: 25.0 conta (almeno 25)"
            assert giorni_caldi(settimana, soglia=30) == 1, "❌ Sopra i 30 gradi c'è un solo giorno"
            assert giorni_caldi([]) == 0, "❌ Con una lista vuota la funzione deve restituire 0"
        """,
    )

    nb.esercizio(
        titolo="Due celle da sistemare",
        scenario="Le due celle qui sotto si fermano con un errore. Ognuna ne contiene uno solo.",
        richiesta="""
            1. Esegui la prima cella e leggi l'ultima riga del traceback: dice il tipo di errore e cosa non va.
            2. Correggi la riga indicata e riesegui; poi fai lo stesso con la seconda cella.
        """,
        suggerimento="nel traceback, la freccia `---->` indica la riga in cui Python si è fermato.",
        starter="""
            biglietto = 12
            persone = 3
            messaggio = "Totale: " + biglietto * persone + " euro"
            print(messaggio)  # Output: Totale: 36 euro
        """,
        soluzione="""
            biglietto = 12
            persone = 3
            messaggio = f"Totale: {biglietto * persone} euro"
            print(messaggio)  # Output: Totale: 36 euro
        """,
        verifica="""
            assert messaggio == "Totale: 36 euro", "❌ messaggio: controlla spazi e testo, deve essere 'Totale: 36 euro'"
            assert durata == 16, "❌ La playlist dura 16 minuti"
        """,
        perche="""
            Nella prima cella il `TypeError` dice che non si può sommare una stringa e un numero: la f-string
            (oppure `str(...)`) risolve. Nella seconda il `NameError` segnala un nome scritto male: `totle` invece di `totale`.
        """,
    )
    # la seconda cella rotta: va subito dopo la prima, sia nella versione studente sia nelle soluzioni
    seconda_starter = Cella("code", """
def durata_totale(minuti):
    \"\"\"Restituisce la durata totale di una playlist, in minuti.\"\"\"
    totale = 0
    for m in minuti:
        totale = totle + m
    return totale

playlist = [3, 4, 5, 4]
durata = durata_totale(playlist)
print(durata)  # Output: 16""".strip("\n"), solo_studente=True, ruolo="starter")
    seconda_soluzione = Cella("code", """
def durata_totale(minuti):
    \"\"\"Restituisce la durata totale di una playlist, in minuti.\"\"\"
    totale = 0
    for m in minuti:
        totale = totale + m
    return totale

playlist = [3, 4, 5, 4]
durata = durata_totale(playlist)
print(durata)  # Output: 16""".strip("\n"), solo_soluzioni=True, ruolo="soluzione")
    i_starter = max(i for i, c in enumerate(nb.celle) if c.ruolo == "starter")
    nb.celle.insert(i_starter + 1, seconda_starter)
    i_soluzione = max(i for i, c in enumerate(nb.celle) if c.ruolo == "soluzione")
    nb.celle.insert(i_soluzione + 1, seconda_soluzione)

    nb.esercizio(
        titolo="Un primo sguardo ai consumi",
        scenario="""
            Il file `letture_pod_2025.csv` contiene i consumi mensili per fascia di sei POD (punti di prelievo) nel 2025.
            È un CSV in formato italiano: separatore `;`, virgola decimale, encoding `latin-1`.
        """,
        richiesta="""
            1. Leggi il file in `letture` con i parametri giusti e guarda `head()`, `info()` e `describe()`.
            2. Salva in `righe` il numero di righe del DataFrame.
            3. Salva in `kwh_max` il valore più alto della colonna `kwh`.
            4. Confronta il massimo con la media e con la riga `75%`: in un commento, scrivi se ti sembra un valore plausibile.
        """,
        suggerimento="il numero di righe è nella seconda riga di `info()`, il massimo nella riga `max` di `describe()`.",
        starter="""
            import pandas as pd

            letture = ...

            righe = ...
            kwh_max = ...
        """,
        soluzione="""
            import pandas as pd

            letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
            letture.info()

            righe = len(letture)
            kwh_max = letture["kwh"].max()
            # 5785.2 è quasi dieci volte la media (623) e più di sette volte il 75% (755): è sospetto
            letture.describe()
        """,
        verifica="""
            assert letture["kwh"].dtype == "float64", "❌ kwh non è numerica: manca decimal=','"
            assert righe == 216, "❌ Il file ha 216 righe"
            assert round(kwh_max, 1) == 5785.2, "❌ Il massimo di kwh è nella riga max di describe()"
        """,
        perche="""
            È la lettura di luglio (fascia F1) del POD IT001E45678901, registrata dieci volte più alta del dovuto.
            `describe()` è spesso il modo più rapido per accorgersi di un valore fuori scala.
        """,
    )

    nb.esercizio(
        titolo="Le letture nel database",
        scenario="Il database `utility.db` contiene tre tabelle: `clienti`, `pod` e `letture`.",
        richiesta="""
            1. Apri la connessione con `sqlite3.connect`, leggi tutta la tabella `letture` in `letture_db`
               con `pd.read_sql` e chiudi la connessione.
            2. Salva in `n_letture` il numero di righe della tabella.
        """,
        suggerimento='la query per leggere tutta la tabella è `"SELECT * FROM letture"`.',
        starter="""
            import sqlite3

            import pandas as pd

            con = ...
            letture_db = ...
            con.close()

            n_letture = ...
            letture_db.head()
        """,
        soluzione="""
            import sqlite3

            import pandas as pd

            con = sqlite3.connect("../Dati/utility.db")
            letture_db = pd.read_sql("SELECT * FROM letture", con)
            con.close()

            n_letture = len(letture_db)
            letture_db.head()
        """,
        verifica="""
            assert list(letture_db.columns) == ["pod", "data", "kwh"], "❌ Leggi tutta la tabella letture con SELECT *"
            assert n_letture == 930, "❌ La tabella letture ha 930 righe"
        """,
        facoltativo=True,
    )
    return nb
