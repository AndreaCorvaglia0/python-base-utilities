"""10 · Agenti per il coding."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="10",
        file="10_Agenti_per_il_coding",
        titolo="Agenti per il coding",
        blocco=4,
        giornata=2,
        intento="Usiamo Copilot in VS Code per scrivere e spiegare codice, poi leggiamo e controlliamo uno script scritto da un agente.",
        obiettivi={
            "base": [
                "usare Copilot in VS Code per completare, chiedere e far spiegare",
                "dare al modello il contesto giusto e controllare la risposta con un numero noto",
                "leggere uno script scritto da un agente prima di lanciarlo",
            ],
            "avanzata": [
                "usare Copilot in VS Code per completare, chiedere e far spiegare",
                "leggere uno script scritto da un agente prima di lanciarlo",
                "riconoscere type hint, `@dataclass`, decoratori, generatori e `**kwargs`",
            ],
        },
        tempo={"base": 45, "avanzata": 55},
        dati=["impianti_fv.csv", "letture_pod_2025.csv"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Copilot in VS Code", intro="""
        GitHub Copilot lavora dentro VS Code in due forme. Il completamento propone codice in grigio mentre
        scriviamo: **Tab** lo accetta, **Esc** lo rifiuta. La chat risponde a domande e scrive codice su
        richiesta: si apre con **Ctrl+Alt+I** (su Mac **Ctrl+Cmd+I**), oppure dentro una cella con **Ctrl+I**.
    """)
    nb.md("""
        La chat ha tre modalità, che si scelgono dal menu in basso nel riquadro della chat.

        | Modalità | Cosa fa | Quando usarla |
        |---|---|---|
        | Ask | risponde; il codice lo copiamo noi | domande, spiegazioni, una funzione |
        | Plan | scrive i passi senza toccare i file; il piano si legge e si corregge | compiti di più passi, prima di lasciar fare |
        | Agent | legge i file, li modifica mostrando le differenze, lancia comandi chiedendo conferma | compiti che sappiamo controllare pezzo per pezzo |
    """)
    nb.md("""
        Claude Code e Codex funzionano allo stesso modo: girano nel terminale o come estensione di VS Code,
        e Codex anche dentro ChatGPT. Cambiano il modello e qualche comando; le regole che vediamo più
        avanti valgono per tutti.
    """)
    nb.md('''
        Per il completamento basta scrivere la firma di una funzione e una docstring che dice cosa deve fare:

        ```python
        def prezzo_scontato(prezzo, sconto_percento):
            """Prezzo dopo lo sconto, arrotondato ai centesimi."""
        ```

        Dopo la docstring premiamo **Invio** e Copilot propone il corpo. Lo accettiamo solo se fa quello che
        dice la docstring, e lo proviamo con un caso che conosciamo: `prezzo_scontato(80, 25)` deve dare `60.0`.
    ''')

    # ------------------------------------------------------------------ 2
    nb.sezione("Le parole", intro="""
        Sei parole che tornano ogni volta che si lavora con un agente.
    """)
    nb.md("""
        | Parola | Cos'è | Perché conta |
        |---|---|---|
        | token | il pezzo di testo che il modello legge e scrive, circa tre quarti di parola | l'uso si misura in token: un traceback costa poco, un file enorme molto |
        | finestra di contesto | quanti token il modello tiene presenti in una conversazione | se la chat dimentica una colonna nominata dieci messaggi prima, la finestra è piena: si apre una chat nuova |
        | cache | la parte iniziale della conversazione (istruzioni, file già letti) che il servizio tiene da parte per qualche minuto | rileggerla costa meno e la risposta arriva prima |
    """)
    nb.md("""
        | Parola | Cos'è | Perché conta |
        |---|---|---|
        | modelli | il completamento usa un modello piccolo e veloce; nella chat si sceglie dal menu in basso | scrive il seguito più probabile senza verificarlo; per un traceback strano si prova un modello più grande |
        | Plan e Agent | prima il piano dei passi, poi le modifiche ai file | il piano si legge e si corregge prima di lasciar fare |
        | prompt e contesto | il prompt è la domanda; il contesto è quello che il modello vede: file aperti, celle selezionate, testo incollato | conta più della domanda |
    """)
    nb.md("""
        Le istruzioni che valgono sempre si scrivono una volta in un file del progetto, che l'agente legge a
        ogni richiesta: `.github/copilot-instructions.md` per Copilot, `CLAUDE.md` per Claude Code, `AGENTS.md`
        per Codex. Per esempio: "i nomi delle colonne e delle variabili sono in italiano".
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Prova guidata", intro="""
        Due prompt, in ordine. Per ognuno: copia il testo nella chat in modalità Ask, leggi la risposta,
        incolla il codice nella cella sotto, esegui e controlla.
    """)
    nb.md("""
        Carichiamo il DataFrame su cui lavoriamo. L'output di `df.info()` è il contesto da dare al modello:
        nomi esatti delle colonne e tipi.
    """)
    nb.code("""
        import pandas as pd

        df = pd.read_csv("../Dati/impianti_fv.csv")
        df.info()
    """)
    nb.sottosezione("Una funzione", intro="""
        ```text
        Ho un DataFrame pandas `df` con queste colonne:
        id_impianto (str), comune (str), provincia (str), kwp (float), anno_allaccio (int), lat e lon (float).
        Scrivi una funzione `potenza_per_provincia(df)` che restituisce un DataFrame con due colonne,
        provincia e kwp, con la somma dei kwp per provincia, ordinato dal più alto al più basso.
        Docstring di una riga, niente commenti.
        ```

        Cosa controllare: `groupby` sulla provincia, `sum` sui kwp, `sort_values` con `ascending=False`,
        `reset_index` perché provincia torni colonna.
    """)
    nb.prova_tu(
        richiesta="""
            Incolla la funzione proposta da Copilot al posto dei puntini ed esegui la cella. Output atteso: due
            colonne, `MI` in testa con 323.5 kWp, e la somma della colonna kwp uguale a 737, come in `df`.
        """,
        starter="""
            ...


            per_provincia = potenza_per_provincia(df)
            per_provincia
        """,
        soluzione="""
            def potenza_per_provincia(df):
                \"\"\"Somma dei kwp per provincia, dalla più alta alla più bassa.\"\"\"
                somma = df.groupby("provincia")["kwp"].sum().reset_index()
                return somma.sort_values("kwp", ascending=False).reset_index(drop=True)


            per_provincia = potenza_per_provincia(df)
            per_provincia
        """,
    )
    nb.sottosezione("La spiegazione di un errore", intro="""
        Questa cella dà errore apposta: eseguila e copia il traceback intero, dalla prima riga all'ultima.
    """)
    nb.code('df["kWp"].sum()', errore=True)
    nb.md("""
        ```text
        Spiegami questo errore senza correggerlo: cosa significa, perché succede, dove devo guardare.

        <incolla qui il traceback intero>
        ```

        Cosa controllare: la risposta deve nominare `KeyError`, dire che la colonna `kWp` non esiste e che
        pandas distingue maiuscole e minuscole. La riga corretta:
    """)
    nb.code('df["kwp"].sum()')

    # ------------------------------------------------------------------ 4
    nb.sezione("Le tre regole", intro="""
        Tre regole prima di accettare codice generato, da chiunque arrivi.
    """)
    nb.md("""
        **Verifica.** Esegui subito e confronta l'output con un numero che conosci già: la somma dei kwp, il
        numero di righe. Un parametro mai visto si controlla con `help()` prima di usarlo.
    """)
    nb.md("""
        **Chiedi spiegazioni.** Prima "spiegami", poi "correggi", sempre con il traceback intero. Se la
        spiegazione non è chiara, il codice corretto non si accetta.
    """)
    nb.md("""
        **Piccoli passi.** Si chiede una cosa per volta e la si controlla prima di andare avanti. In Agent le
        modifiche arrivano come differenze, rosso quello che toglie e verde quello che aggiunge: si tengono o
        si annullano blocco per blocco (**Keep** o **Undo**).
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Leggere il codice scritto da un agente", intro="""
        In modalità Agent chiediamo: "Scrivi uno script che legge le letture, somma i kWh per POD e salva un
        CSV". Torna un file di una trentina di righe. Prima di lanciarlo lo leggiamo dall'alto, un blocco
        alla volta.
    """)
    nb.sottosezione("Lo script", aula="avanzata")
    nb.md('''
        In testa la descrizione, gli import e le costanti:

        ```python
        """Totale dei consumi per POD dal file delle letture mensili."""

        import logging
        from dataclasses import dataclass
        from pathlib import Path

        import pandas as pd

        logger = logging.getLogger(__name__)

        DATA_DIR = Path("Dati")
        OUTPUT = Path("totale_per_pod.csv")
        ```
    ''')
    nb.md('''
        | Riga | Cos'è | Cosa fa |
        |---|---|---|
        | `"""Totale..."""` | docstring di modulo | dice cosa fa lo script |
        | `import`, `from ... import` | import | caricano le librerie; `logging`, `dataclasses` e `pathlib` sono della libreria standard |
        | `logger = logging.getLogger(__name__)` | log | prepara i messaggi: `logger.info(...)` è un `print` con il livello davanti |
        | `DATA_DIR = Path("Dati")` | costante (tutto maiuscolo) | dove stanno i dati, rispetto alla cartella da cui si lancia lo script |
    ''')
    nb.md('''
        Poi la configurazione:

        ```python
        @dataclass
        class Config:
            path: Path
            sep: str = ";"
            decimal: str = ","
            encoding: str = "latin-1"
        ```
    ''')
    nb.md('''
        | Riga | Cos'è | Cosa fa |
        |---|---|---|
        | `@dataclass` | decoratore | trasforma la classe in un contenitore di campi e scrive da solo il costruttore `Config(path=...)` |
        | `sep: str = ";"` | campo con type hint e default | se non lo passiamo, vale `";"` |
    ''')
    nb.md('''
        Poi le funzioni che fanno il lavoro:

        ```python
        def leggi_letture(config: Config) -> pd.DataFrame:
            """Legge il CSV delle letture con le opzioni della configurazione."""
            if not config.path.exists():
                raise FileNotFoundError(f"File non trovato: {config.path}")
            return pd.read_csv(
                config.path, sep=config.sep, decimal=config.decimal, encoding=config.encoding
            )


        def totale_per_pod(letture: pd.DataFrame, fasce: list[str] | None = None) -> pd.DataFrame:
            """Somma dei kWh per POD, eventualmente solo per alcune fasce."""
            if fasce is not None:
                letture = letture[letture["fascia"].isin(fasce)]
            return letture.groupby("pod")["kwh"].sum().reset_index()
        ```
    ''')
    nb.md('''
        | Riga | Cos'è | Cosa fa |
        |---|---|---|
        | `-> pd.DataFrame` | type hint di ritorno | dice cosa restituisce la funzione |
        | `fasce: list[str] \\| None = None` | parametro facoltativo | lista di stringhe oppure `None`; se non lo passiamo, tiene tutte le fasce |
        | `raise FileNotFoundError(...)` | errore sollevato apposta | ferma lo script con un messaggio chiaro, prima di arrivare a pandas |
    ''')
    nb.md('''
        In fondo, chi le usa:

        ```python
        def main() -> None:
            logging.basicConfig(level=logging.INFO)
            config = Config(path=DATA_DIR / "letture_pod_2025.csv")
            totali = totale_per_pod(leggi_letture(config))
            totali.to_csv(OUTPUT, index=False)
            logger.info(f"Salvati {len(totali)} POD in {OUTPUT}")


        if __name__ == "__main__":
            main()
        ```
    ''')
    nb.md('''
        | Riga | Cos'è | Cosa fa |
        |---|---|---|
        | `def main() -> None:` | funzione principale | mette in fila i passi; `-> None` vuol dire che non restituisce niente |
        | `logging.basicConfig(level=logging.INFO)` | log | accende il log: senza, `logger.info` non stampa |
        | `if __name__ == "__main__":` | blocco main | fa partire `main()` quando il file viene lanciato, non quando viene importato |
    ''')
    nb.md("""
        Prima di accettare uno script, quattro domande, nell'ordine:

        1. La struttura è quella solita: import, costanti, `def`, `main` in fondo?
        2. Quali righe fanno il lavoro e quali sono la cornice? Qui il lavoro è `read_csv` più il `groupby`.
        3. Il percorso dei dati esiste, dalla cartella da cui lo lanciamo?
        4. Il numero torna? Qui 134507,7 kWh in tutto, su sei POD.
    """)
    nb.prova_tu(
        richiesta="""
            Per ogni riga dello script scrivi cos'è, scegliendo tra `"decoratore"`, `"type hint"`,
            `"blocco main"` e `"costante"`. Le risposte sono nelle tabelle qui sopra.
        """,
        starter="""
            cosa_e = {
                "@dataclass": ...,
                "-> pd.DataFrame": ...,
                'if __name__ == "__main__":': ...,
                "DATA_DIR": ...,
            }
            cosa_e
        """,
        soluzione="""
            cosa_e = {
                "@dataclass": "decoratore",
                "-> pd.DataFrame": "type hint",
                'if __name__ == "__main__":': "blocco main",
                "DATA_DIR": "costante",
            }
            cosa_e
        """,
    )
    nb.md("""
        Le forme che si incontrano più spesso, una per riga, stanno nella
        [scheda per leggere il codice](../Schede/Scheda_leggere_codice.md).
    """)

    with nb.solo("avanzata"):
        nb.sottosezione("Type hint", intro="""
            Le forme più frequenti: `list[str]`, `dict[str, float]`, `tuple[int, int]`, `X | None` (X oppure
            niente), `-> None`. Python non li controlla quando esegue: servono a chi legge e all'editor.
        """)
        nb.code('''
            def prezzo_medio(prezzi: dict[str, float], escludi: list[str] | None = None) -> float:
                """Prezzo medio dei prodotti, senza quelli in escludi."""
                escludi = escludi or []
                validi = [p for nome, p in prezzi.items() if nome not in escludi]
                return sum(validi) / len(validi)

            prezzo_medio({"pane": 2.5, "latte": 1.3, "caffè": 4.2}, escludi=["caffè"])
        ''')
        nb.md("""
            Con interi al posto dei `float` non succede niente di diverso: il type hint è un'indicazione, non un controllo.
        """)
        nb.code("""
            prezzo_medio({"pane": 2, "latte": 1})
        """)

        nb.sottosezione("`@dataclass`", intro="""
            `@dataclass` sopra una classe la trasforma in un contenitore di campi, ognuno con tipo e, se c'è,
            default. Il costruttore, la stampa e il confronto con `==` li scrive da solo.
        """)
        nb.code("""
            from dataclasses import dataclass

            @dataclass
            class Libro:
                titolo: str
                autore: str
                pagine: int = 0
        """)
        nb.code("""
            libro = Libro("Il nome della rosa", "Umberto Eco", pagine=503)
            libro
        """)

        nb.sottosezione("Decoratori", intro="""
            Una riga `@nome` sopra un `def` avvolge la funzione in un'altra che ne cambia il comportamento.
            Qui `@cache` ricorda i risultati già calcolati: senza, `fibonacci(80)` non finirebbe più.
        """)
        nb.code("""
            from functools import cache

            @cache
            def fibonacci(n: int) -> int:
                return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)

            fibonacci(80)
        """)
        nb.md("""
            Altri decoratori frequenti negli script degli agenti: `@property` e `@staticmethod` nelle classi,
            `@pytest.fixture` nei test.
        """)

        nb.sottosezione("Generatori", intro="""
            Una funzione con `yield` al posto di `return` è un generatore: consegna un valore alla volta, quando
            un `for` o `list()` lo chiede. Gli agenti lo usano per lavorare su dati lunghi a pezzi.
        """)
        nb.code("""
            def a_blocchi(elementi: list, n: int):
                for i in range(0, len(elementi), n):
                    yield elementi[i:i + n]

            spesa = ["pane", "latte", "uova", "mele", "pasta"]
            list(a_blocchi(spesa, 2))
        """)

        nb.sottosezione("`**kwargs`", intro="""
            `**kwargs` (il nome può cambiare, contano i due asterischi) raccoglie in un dizionario i parametri
            passati per nome che la funzione non elenca. `*args` fa lo stesso con quelli passati per posizione.
        """)
        nb.code("""
            def ordine(piatto: str, **opzioni) -> str:
                return f"{piatto}: {opzioni}"

            ordine("pizza", impasto="integrale", extra="olive")
        """)
        nb.md("""
            L'uso più comune negli script degli agenti: passare le opzioni così come sono a un'altra funzione,
            qui `read_csv`.
        """)
        nb.code("""
            def leggi_csv(path: str, **opzioni) -> pd.DataFrame:
                return pd.read_csv(path, **opzioni)

            leggi_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1").shape
        """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il parametro inventato",
        scenario="""
            `letture_pod_2025.csv` è un CSV all'italiana: punto e virgola, virgola decimale, encoding latin-1.
            Il prompt qui sotto suggerisce a Copilot nomi di parametri che `read_csv` non ha.
        """,
        richiesta="""
            1. Dai alla chat questo prompt e incolla la riga che propone al posto di quella commentata:

               ```text
               Leggi il file ../Dati/letture_pod_2025.csv con pandas: separatore punto e virgola,
               virgola come decimale, encoding latin-1. Usa i parametri separator, decimal_separator ed encoding.
               ```
            2. Eseguila e leggi l'ultima riga del traceback: quale parametro non esiste?
            3. Con `help(pd.read_csv)` trova i nomi giusti per il separatore e per il decimale.
            4. Leggi il file in `letture` con i parametri giusti. Output atteso: 216 righe, 5 colonne, `kwh` di tipo `float64`.
        """,
        starter="""
            # 1-2. incolla qui la riga proposta da Copilot ed eseguila
            # letture = pd.read_csv("../Dati/letture_pod_2025.csv", ...)

            # 3. la documentazione
            # help(pd.read_csv)

            # 4. la lettura giusta
            letture = ...
            letture.info()
        """,
        soluzione="""
            letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
            letture.info()
        """,
        verifica="""
            assert letture.shape == (216, 5), "❌ letture: 216 righe e 5 colonne; con il separatore sbagliato esce una colonna sola"
            assert str(letture["kwh"].dtype) == "float64", "❌ kwh deve essere float64: serve decimal=','"
            assert round(letture["kwh"].sum(), 1) == 134507.7, "❌ La somma dei kwh deve essere 134507.7"
        """,
        perche="I nomi dei parametri non si indovinano: `sep` e `decimal` stanno nella firma di `read_csv`.",
    )
    nb.esercizio(
        titolo="Leggere prima di lanciare",
        scenario='''
            Un collega ha fatto scrivere a un agente lo script del report settimanale. Dice che gira senza
            errori, ma il totale gli sembra strano.

            ```python
            """Report settimanale: kWh totali per POD."""

            from dataclasses import dataclass
            from pathlib import Path

            import pandas as pd


            @dataclass
            class Config:
                path: Path = Path("Dati") / "letture_pod_2025.csv"
                sep: str = ";"
                encoding: str = "latin-1"


            def leggi_letture(config: Config) -> pd.DataFrame:
                """Legge il CSV delle letture."""
                return pd.read_csv(config.path, sep=config.sep, encoding=config.encoding)


            def report_kwh(letture: pd.DataFrame) -> pd.DataFrame:
                """kWh totali per POD."""
                return letture.groupby("pod")["kwh"].sum().reset_index()


            def main() -> None:
                totale = report_kwh(leggi_letture(Config()))
                totale.to_csv("report_settimanale.csv", index=False)
                print(f"Report salvato: {len(totale)} POD")


            if __name__ == "__main__":
                main()
            ```
        ''',
        richiesta="""
            1. Compila `risposte`: in `"lavoro vero"` il nome della funzione che fa il calcolo; in
               `"lanciato in una cella"` cosa succede incollando tutto lo script in una cella del notebook,
               scegliendo tra `"FileNotFoundError"`, `"NameError"` e `"non parte niente"`.
            2. Trova il dettaglio che manca nella lettura del file e completa `leggi_letture`, che qui riceve
               direttamente il percorso. Output atteso: sei POD, 134507,7 kWh in tutto.
        """,
        suggerimento="Guarda `totale.dtypes`: se `kwh` non è un numero, il problema è in quello che `read_csv` riceve.",
        starter="""
            risposte = {
                "lavoro vero": ...,
                "lanciato in una cella": ...,
            }


            def leggi_letture(path: str) -> pd.DataFrame:
                \"\"\"Legge il CSV delle letture.\"\"\"
                ...


            def report_kwh(letture: pd.DataFrame) -> pd.DataFrame:
                \"\"\"kWh totali per POD.\"\"\"
                return letture.groupby("pod")["kwh"].sum().reset_index()


            totale = report_kwh(leggi_letture("../Dati/letture_pod_2025.csv"))
            totale
        """,
        soluzione="""
            risposte = {
                "lavoro vero": "report_kwh",
                "lanciato in una cella": "FileNotFoundError",
            }


            def leggi_letture(path: str) -> pd.DataFrame:
                \"\"\"Legge il CSV delle letture.\"\"\"
                return pd.read_csv(path, sep=";", decimal=",", encoding="latin-1")


            def report_kwh(letture: pd.DataFrame) -> pd.DataFrame:
                \"\"\"kWh totali per POD.\"\"\"
                return letture.groupby("pod")["kwh"].sum().reset_index()


            totale = report_kwh(leggi_letture("../Dati/letture_pod_2025.csv"))
            totale
        """,
        verifica="""
            assert risposte["lavoro vero"] == "report_kwh", "❌ lavoro vero: il nome della funzione con il groupby, senza parentesi"
            assert risposte["lanciato in una cella"] == "FileNotFoundError", "❌ lanciato in una cella: il blocco main parte anche nel notebook, e da qui il percorso Dati non esiste"
            assert round(totale["kwh"].sum(), 1) == 134507.7, "❌ La somma dei kwh deve essere 134507.7: controlla il tipo di kwh con .dtypes"
        """,
        perche="Senza `decimal=\",\"` la colonna `kwh` resta testo e `sum()` attacca le stringhe una all'altra: nessun traceback, solo un numero sbagliato.",
    )
    return nb
