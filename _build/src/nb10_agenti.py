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
        Copilot lavora in VS Code in due forme. Il completamento propone codice in grigio mentre scriviamo:
        **Tab** lo accetta, **Esc** lo rifiuta. La chat scrive codice su richiesta: si apre con **Ctrl+Alt+I**
        (su Mac **Ctrl+Cmd+I**), oppure inline in una cella con **Ctrl+I**.
    """)
    nb.md("""
        La chat ha tre modalità, dal menu in basso.

        | Modalità | Cosa fa |
        |---|---|
        | Ask | risponde; il codice lo copiamo noi |
        | Plan | scrive i passi senza toccare i file |
        | Agent | modifica i file mostrando le differenze, lancia comandi chiedendo conferma |

        Claude Code e Codex funzionano allo stesso modo, nel terminale o in VS Code.
    """)
    nb.code('''
        # Completamento: scriviamo firma e docstring, Invio, e Copilot propone il corpo in grigio
        def prezzo_scontato(prezzo, sconto_percento):
            """Prezzo dopo lo sconto, arrotondato ai centesimi."""
            return round(prezzo * (1 - sconto_percento / 100), 2)


        prezzo_scontato(80, 25)  # Output: 60.0
    ''')
    nb.md("""
        Il corpo si accetta se fa quello che dice la docstring. Il caso noto torna; resta da provare
        l'arrotondamento ai centesimi.
    """)
    nb.code("""
        prezzo_scontato(19.99, 10)  # Output: 17.99, non 17.991
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Glossario", intro="""
        | Parola | Cos'è |
        |---|---|
        | token | il pezzo di testo che il modello legge e scrive, circa tre quarti di parola; l'uso si misura in token |
        | finestra di contesto | quanti token il modello tiene presenti; quando è piena la chat dimentica l'inizio: si apre una chat nuova |
        | cache | l'inizio della conversazione tenuto da parte per qualche minuto: rileggerlo costa meno |
    """)
    nb.md("""
        | Parola | Cos'è |
        |---|---|
        | modello | scrive il seguito più probabile, senza verificarlo; nella chat si sceglie dal menu in basso |
        | file di istruzioni | regole che l'agente legge a ogni richiesta: `.github/copilot-instructions.md` per Copilot, `CLAUDE.md` per Claude Code, `AGENTS.md` per Codex |
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Prompt e contesto", intro="""
        Il prompt è la richiesta; il contesto è quello che il modello vede: file aperti, celle selezionate,
        testo incollato. Nelle celle qui sotto il commento in testa è il prompt dato alla chat in modalità Ask,
        il codice è la risposta.
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
        Il primo prompt non nomina le colonne e la risposta ne usa una che non esiste, `anno`. Per il
        secondo controlliamo due cose: gli anni sono in ordine, e i conteggi sommano a 40, le righe di `df`.
    """)
    nb.code("""
        print(per_anno.sum(), len(df))  # Output: 40 40
    """)
    nb.prova_tu(
        richiesta="""
            Dai alla chat, in modalità Ask, questo prompt:

            ```text
            Ho un DataFrame pandas `df` con queste colonne:
            id_impianto (str), comune (str), provincia (str), kwp (float), anno_allaccio (int), lat e lon (float).
            Scrivi una funzione `potenza_per_provincia(df)` che restituisce un DataFrame con due colonne,
            provincia e kwp, con la somma dei kwp per provincia, ordinato dal più alto al più basso.
            Docstring di una riga, niente commenti.
            ```

            Incolla la funzione al posto dei puntini ed esegui. Output atteso: due colonne, `MI` in testa con
            323,5 kWp, e la somma della colonna kwp uguale a 737, come in `df`.
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
        La spiegazione nomina `KeyError` e la colonna sbagliata, e nella lista c'è il nome giusto, `kwp`.
        Solo dopo chiediamo la correzione.
    """)
    nb.code("""
        # Prompt: "Ora correggi la riga"
        df["kwp"].sum()
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Le tre regole", intro="""
        1. **Verifica.** Esegui subito e confronta con un numero noto: la somma dei kwp, il numero di righe.
        2. **Chiedi spiegazioni.** Prima "spiegami", poi "correggi", sempre con il traceback intero.
        3. **Piccoli passi.** Una richiesta per volta. In Agent le modifiche arrivano come differenze, da
           tenere o annullare blocco per blocco (**Keep** o **Undo**).
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Leggere il codice scritto da un agente", intro="""
        Uno script scritto da un agente si legge prima di lanciarlo, un blocco alla volta, con quattro domande:

        1. La struttura è quella solita: import, costanti, `def`, `main` in fondo?
        2. Quali righe fanno il lavoro e quali sono la cornice?
        3. Il percorso dei dati esiste, dalla cartella da cui lo lanciamo?
        4. Il numero torna?
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
        In testa la docstring di modulo, gli import e le costanti, in maiuscolo. `logging`, `dataclasses` e
        `pathlib` sono della libreria standard; `logger.info(...)` è un `print` con il livello davanti.
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
        `@dataclass` è un decoratore: scrive da solo il costruttore `Config(path=...)` e la stampa.
        `sep: str = ";"` è un campo con type hint e default: se non lo passiamo, vale `";"`.
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
        Il lavoro lo fanno `read_csv` e il `groupby`; il resto è cornice. `-> pd.DataFrame` è il type hint
        di ritorno; `fasce: list[str] | None = None` è un parametro facoltativo.
    """)
    nb.code("""
        totale_per_pod(leggi_letture(config), fasce=["F1"])  # solo la fascia F1
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
        `logging.basicConfig` accende il log: senza, `logger.info` non stampa. Il blocco
        `if __name__ == "__main__":` fa partire `main()` quando il file viene lanciato, non quando viene importato.
    """)
    nb.prova_tu(
        richiesta="""
            Per ogni riga dello script scrivi cos'è, scegliendo tra `"decoratore"`, `"type hint"`,
            `"blocco main"` e `"costante"`. Le risposte sono nelle celle qui sopra.
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
        suggerimento="guarda `totale.dtypes`: se `kwh` non è un numero, il problema è in quello che `read_csv` riceve.",
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
