"""10 · Agenti per il coding."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="10",
        file="10_Agenti_per_il_coding",
        titolo="Agenti per il coding",
        blocco=4,
        giornata=2,
        intento="Usiamo Copilot in VS Code per scrivere codice e farcelo spiegare, e impariamo a leggere e controllare uno script scritto da un agente prima di eseguirlo.",
        obiettivi=[
            "usare Copilot in VS Code per completare, chiedere e far spiegare",
            "dare al modello il contesto giusto e controllare la risposta con un numero noto",
            "leggere uno script scritto da un agente prima di lanciarlo",
        ],
        tempo={"base": 45, "avanzata": 45},
        dati=["impianti_fv.csv", "letture_pod_2025.csv"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Copilot in VS Code", intro="""
        Copilot si usa in VS Code in due modi. Il completamento propone il codice in grigio mentre scriviamo, e
        il suggerimento si accetta con **Tab** o si scarta con **Esc**. La chat, invece, scrive codice su
        richiesta e si apre con **Ctrl+Alt+I** (su Mac **Ctrl+Cmd+I**); per lavorare su una sola cella si può
        aprire la chat inline con **Ctrl+I**, che mostra la proposta direttamente nella cella.
    """)
    nb.md("""
        La chat ha tre modalità, che si scelgono dal menu in basso e si distinguono per quanto l'agente può fare
        da solo.

        | Modalità | Cosa fa |
        |---|---|
        | Ask | risponde nella chat, e il codice lo copiamo noi |
        | Plan | descrive i passi da seguire senza modificare i file |
        | Agent | modifica i file mostrando le differenze e lancia comandi dopo averci chiesto conferma |

        Claude Code e Codex funzionano allo stesso modo, dal terminale o dentro VS Code. Nella cella qui sotto
        abbiamo scritto la firma e la docstring di `prezzo_scontato`, e il completamento ha proposto il corpo.
    """)
    nb.code('''
        # Completamento: scriviamo firma e docstring, Invio, e Copilot propone il corpo in grigio
        def prezzo_scontato(prezzo, sconto_percento):
            """Prezzo dopo lo sconto, arrotondato ai centesimi."""
            return round(prezzo * (1 - sconto_percento / 100), 2)


        prezzo_scontato(80, 25)  # Output: 60.0
    ''')
    nb.md("""
        Un suggerimento si accetta solo se fa quello che dice la docstring, e per saperlo bisogna provarlo. Il
        caso semplice, 80 euro scontati del 25%, dà 60 come previsto, ma non dice nulla sull'arrotondamento ai
        centesimi. Per controllarlo serve un prezzo con i decimali, come quello della cella seguente, dove il
        risultato corretto è 17.99 e non 17.991.
    """)
    nb.code("""
        prezzo_scontato(19.99, 10)  # Output: 17.99, non 17.991
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Glossario", intro="""
        Lavorando con un agente si incontrano spesso alcuni termini, che la tabella raccoglie con una breve
        spiegazione.

        | Parola | Cos'è |
        |---|---|
        | modello | È il programma che genera il testo: scrive il seguito più probabile della richiesta, senza verificarlo. Nella chat si sceglie dal menu in basso. |
        | token | È il pezzo di testo che il modello legge e scrive, in media circa tre quarti di una parola. L'uso di un servizio si misura in token. |
        | finestra di contesto | È il numero di token che il modello riesce a tenere presenti. Quando la finestra è piena la chat perde l'inizio della conversazione, e conviene aprirne una nuova. |
        | cache | È la parte iniziale della conversazione che il servizio conserva per qualche minuto, in modo che rileggerla costi meno. |
        | file di istruzioni | È un file di regole che l'agente legge a ogni richiesta: `.github/copilot-instructions.md` per Copilot, `CLAUDE.md` per Claude Code, `AGENTS.md` per Codex. |
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Prompt e contesto", intro="""
        Il prompt è la richiesta che scriviamo, mentre il contesto è tutto ciò che il modello vede insieme alla
        richiesta, cioè i file aperti, le celle selezionate e il testo che incolliamo. Il modello non conosce i
        nostri dati se non glieli descriviamo, quindi la qualità della risposta dipende in gran parte dal
        contesto. Nelle celle che seguono il commento in testa riporta il prompt dato alla chat in modalità Ask,
        e il codice sotto è la risposta. La prima cella carica il file degli impianti e stampa con `df.info()` i
        nomi esatti e i tipi delle colonne, che sono proprio le informazioni da passare al modello.
    """)
    nb.code("""
        import pandas as pd

        df = pd.read_csv("../Dati/impianti_fv.csv")
        df.info()  # nomi esatti e tipi delle colonne: il contesto da incollare nel prompt
    """)
    nb.code("""
        # Prompt: "Conta gli impianti per anno"
        df["anno"].value_counts()
    """, errore=True)
    nb.code("""
        # Prompt: "Ho un DataFrame df con le colonne id_impianto, comune, provincia, kwp,
        #          anno_allaccio, lat, lon. Conta gli impianti per anno_allaccio, in ordine di anno."
        per_anno = df["anno_allaccio"].value_counts().sort_index()
        per_anno
    """)
    nb.md("""
        Il primo prompt non nomina le colonne, e il modello ne ha usata una che non esiste, `anno`, con il
        risultato di un `KeyError`. Il secondo prompt riporta i nomi esatti e la risposta usa la colonna giusta,
        ma va comunque controllata. Gli anni devono comparire in ordine crescente e la somma dei conteggi deve
        essere uguale al numero di righe di `df`, cioè 40, perché ogni impianto ha un solo anno di allaccio.
    """)
    nb.code("""
        print(per_anno.sum(), len(df))  # Output: 40 40
    """)
    nb.prova_tu(
        richiesta="""
            Dai alla chat, in modalità Ask, il prompt seguente, che descrive le colonne del DataFrame e il
            risultato che vogliamo:

            ```text
            Ho un DataFrame pandas `df` con queste colonne:
            id_impianto (str), comune (str), provincia (str), kwp (float), anno_allaccio (int), lat e lon (float).
            Scrivi una funzione `potenza_per_provincia(df)` che restituisce un DataFrame con due colonne,
            provincia e kwp, con la somma dei kwp per provincia, ordinato dal più alto al più basso.
            Docstring di una riga, niente commenti.
            ```

            Incolla poi la funzione proposta al posto dei puntini ed esegui la cella. Il risultato è un DataFrame
            con due colonne, `provincia` e `kwp`, con `MI` in testa e 323,5 kWp; la somma della colonna `kwp` è
            737, la stessa che si ottiene da `df`.
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
    nb.md("""
        La chat serve anche a farsi spiegare un errore. La cella qui sotto dà errore apposta, perché chiede la
        colonna `kWp` con la maiuscola. In casi come questo conviene copiare nella chat il traceback intero e
        chiedere per cominciare soltanto una spiegazione, in modo da capire da dove viene il problema prima di modificare
        il codice.
    """)
    nb.code("""
        # Questa cella dà errore apposta: il traceback si copia intero nella chat
        df["kWp"].sum()
    """, errore=True)
    nb.code("""
        # Prompt: "Spiegami questo errore senza correggerlo: cosa significa, perché succede,
        #          dove devo guardare. <traceback intero>"
        # Risposta: KeyError, la colonna 'kWp' non esiste. pandas distingue maiuscole e
        # minuscole: guarda i nomi esatti delle colonne.
        df.columns.tolist()
    """)
    nb.md("""
        Una buona spiegazione nomina l'eccezione, in questo caso `KeyError`, e la colonna che non esiste. La
        lista delle colonne conferma la diagnosi, perché contiene il nome giusto, `kwp`, scritto in minuscolo.
        Solo a questo punto chiediamo alla chat di correggere la riga, e la correzione si controlla subito
        eseguendola.
    """)
    nb.code("""
        # Prompt: "Ora correggi la riga"
        df["kwp"].sum()
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Le tre regole", intro="""
        Nel lavoro con un agente conviene tenere tre abitudini. La prima è eseguire subito il codice ricevuto e
        confrontare il risultato con un numero che conosciamo già, come la somma dei kWp o il numero di righe
        del file. La seconda è chiedere una spiegazione prima della correzione: quando qualcosa non funziona,
        incolliamo il traceback intero e chiediamo che cosa significa, e solo dopo chiediamo di sistemarlo. La
        terza è procedere a piccoli passi, con una richiesta per volta; in modalità Agent le modifiche arrivano
        come differenze da tenere o annullare blocco per blocco, con i pulsanti **Keep** e **Undo**.
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Leggere il codice scritto da un agente", intro="""
        Uno script scritto da un agente si legge prima di lanciarlo, un blocco alla volta, tenendo presenti
        quattro domande. La prima riguarda la struttura, che dovrebbe essere quella consueta: gli import, le
        costanti, le funzioni definite con `def` e la funzione `main` in fondo. La seconda chiede quali righe
        fanno il lavoro e quali fanno solo da cornice, come la configurazione e il log. La terza domanda è se il
        percorso dei dati esiste rispetto alla cartella da cui lanciamo lo script, e la quarta è se il numero
        prodotto torna con uno che conosciamo. Le celle che seguono riportano lo script di esempio diviso in
        blocchi.
    """)
    nb.sottosezione("Lo script", aula="avanzata")
    nb.code('''
        # Prompt (modalità Agent): "Scrivi uno script che legge le letture, somma i kWh per POD e salva un CSV"
        """Totale dei consumi per POD dal file delle letture mensili."""

        import logging
        from dataclasses import dataclass
        from pathlib import Path

        import pandas as pd

        logger = logging.getLogger(__name__)

        DATA_DIR = Path("../Dati")
        OUTPUT = Path("totale_per_pod.csv")
    ''')
    nb.md("""
        Il primo blocco si apre con la docstring di modulo, che dice in una riga che cosa fa lo script, ed è
        seguito dagli import e dalle costanti, scritte in maiuscolo per convenzione. I moduli `logging`,
        `dataclasses` e `pathlib` fanno parte della libreria standard e quindi non vanno installati. L'oggetto
        `logger` serve a scrivere messaggi durante l'esecuzione, e `logger.info(...)` si comporta come un
        `print` che premette al testo il livello del messaggio.
    """)
    nb.code("""
        @dataclass
        class Config:
            path: Path
            sep: str = ";"
            decimal: str = ","
            encoding: str = "latin-1"


        config = Config(path=DATA_DIR / "letture_pod_2025.csv")  # la riga che sta in main()
        config
    """)
    nb.md("""
        Il secondo blocco raccoglie le opzioni di lettura in una classe. La riga `@dataclass` è un decoratore,
        cioè un'istruzione che modifica la definizione scritta subito sotto; in questo caso genera da sola il
        costruttore `Config(path=...)` e la rappresentazione leggibile dell'oggetto che vediamo stampata. Ogni
        campo ha un type hint e può avere un valore predefinito: per esempio `sep: str = ";"` dichiara che `sep`
        è una stringa e che, se non lo passiamo, vale `";"`.
    """)
    nb.code('''
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
    ''')
    nb.md("""
        Nelle due funzioni il lavoro lo fanno `read_csv` e il `groupby`, mentre il controllo sul file, le
        docstring e i type hint fanno da cornice. L'annotazione `-> pd.DataFrame` indica il tipo del valore
        restituito. Il parametro `fasce: list[str] | None = None` è facoltativo: se non lo passiamo vale `None` e
        la funzione somma tutte le fasce, altrimenti tiene solo quelle indicate, come nella cella qui sotto.
    """)
    nb.code("""
        totale_per_pod(leggi_letture(config), fasce=["F1"])  # solo la fascia F1
    """)
    nb.md("""
        La cella seguente risponde alla terza e alla quarta domanda. Controlla che il file indicato nella
        configurazione esista dalla cartella del notebook, e poi confronta il totale dei kWh e il numero di POD
        con i valori che conosciamo dal notebook 06, cioè 134507,7 kWh su sei POD.
    """)
    nb.code("""
        print(config.path.exists())  # domanda 3. Output: True
        totali = totale_per_pod(leggi_letture(config))
        print(round(totali["kwh"].sum(), 1), len(totali))  # domanda 4. Output: 134507.7 6
    """)
    nb.code("""
        def main() -> None:
            logging.basicConfig(level=logging.INFO)
            config = Config(path=DATA_DIR / "letture_pod_2025.csv")
            totali = totale_per_pod(leggi_letture(config))
            totali.to_csv(OUTPUT, index=False)
            logger.info(f"Salvati {len(totali)} POD in {OUTPUT}")


        # Le ultime due righe dello script:
        # if __name__ == "__main__":
        #     main()
    """)
    nb.md("""
        La funzione `main` mette insieme i pezzi: legge il file, calcola i totali, li salva in un CSV e scrive
        un messaggio nel log. La chiamata `logging.basicConfig(level=logging.INFO)` attiva il log, e senza di
        essa `logger.info` non stamperebbe nulla. Il blocco `if __name__ == "__main__":` fa partire `main()`
        quando il file viene lanciato come script, e non la esegue quando il file viene importato da un altro
        modulo.
    """)
    nb.prova_tu(
        richiesta="""
            Le chiavi del dizionario `cosa_e` sono quattro righe dello script. Per ciascuna scrivi che cosa è,
            scegliendo tra `"decoratore"`, `"type hint"`, `"blocco main"` e `"costante"`; le spiegazioni delle
            celle precedenti contengono tutte le risposte.
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
    nb.md("Riassunto in una pagina: [Leggere il codice: cosa è cosa](../Schede/Scheda_leggere_codice.md).")

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il parametro inventato",
        scenario="""
            Il file `letture_pod_2025.csv` è un CSV all'italiana, con il punto e virgola come separatore, la
            virgola come separatore decimale e l'encoding latin-1. Il prompt che userai suggerisce a Copilot nomi
            di parametri che `read_csv` non ha, e il modello tende a seguire le indicazioni della richiesta anche
            quando sono sbagliate.
        """,
        richiesta="""
            1. Dai alla chat il prompt seguente e incolla la riga che propone al posto di quella commentata
               nella cella:

               ```text
               Leggi il file ../Dati/letture_pod_2025.csv con pandas: separatore punto e virgola,
               virgola come decimale, encoding latin-1. Usa i parametri separator, decimal_separator ed encoding.
               ```
            2. Esegui la riga proposta e leggi la fine del traceback, che indica quale parametro non esiste.
            3. Cerca con `help(pd.read_csv)` i nomi giusti dei parametri per il separatore e per il decimale.
            4. Leggi il file in `letture` usando i parametri giusti. Il risultato è un DataFrame di 216 righe e 5
               colonne, con la colonna `kwh` di tipo `float64`.
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
        perche="I nomi dei parametri vanno controllati nella documentazione, perché il modello può inventarli quando la richiesta lo suggerisce. Quelli giusti, `sep` e `decimal`, compaiono nella firma di `read_csv` che `help` mostra.",
    )
    nb.esercizio(
        titolo="Leggere prima di lanciare",
        scenario='''
            Un collega ha fatto scrivere a un agente lo script del report settimanale. Dice che gira senza
            errori, ma il totale gli sembra strano. Lo script è riportato qui sotto, e prima di lanciarlo
            conviene leggerlo con le quattro domande della sezione precedente.

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
            1. Compila il dizionario `risposte`. Alla chiave `"lavoro vero"` scrivi il nome della funzione che fa
               il calcolo; alla chiave `"lanciato in una cella"` scrivi che cosa succede se si incolla tutto lo
               script in una cella del notebook, scegliendo tra `"FileNotFoundError"`, `"NameError"` e
               `"non parte niente"`.
            2. Trova il dettaglio che manca nella lettura del file e completa `leggi_letture`, che qui riceve
               direttamente il percorso. Il risultato è una tabella con sei POD e un totale di 134507,7 kWh.
        """,
        suggerimento="controlla il tipo delle colonne con `totale.dtypes`; se `kwh` non è numerica, il problema sta nei parametri passati a `read_csv`.",
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
        perche="Senza `decimal=\",\"` pandas non riconosce i numeri scritti con la virgola, e la colonna `kwh` resta di testo. Il `groupby` con `sum()` allora concatena le stringhe invece di sommarle, e lo script termina senza traceback ma con un risultato sbagliato, che si scopre solo controllando il totale.",
    )
    return nb
