"""11 · Agenti per il coding."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="11",
        file="11_Agenti_per_il_coding",
        titolo="Agenti per il coding",
        blocco=4,
        giornata=2,
        intento="Copilot scrive codice in fretta e sbaglia con grande sicurezza. Qui gli chiediamo le cose giuste, poi leggiamo quello che scrive e lo controlliamo con un numero che conosciamo.",
        obiettivi=[
            "usare Copilot in VS Code per completare, chiedere e far spiegare",
            "sapere cosa sono token, finestra di contesto e modelli quanto basta per non fidarsi alla cieca",
            "leggere uno script scritto da un agente, passarlo a Ruff e farsi le quattro domande prima di accettarlo",
        ],
        tempo={"base": 70, "avanzata": 70},
        dati=["impianti_fv.csv", "letture_pod_2025.csv"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Cosa fa Copilot in VS Code", intro="""
        GitHub Copilot vive dentro VS Code in due forme. Il completamento propone codice in grigio mentre
        scriviamo: **Tab** lo accetta, **Esc** lo rifiuta. La chat risponde a domande e scrive codice su
        richiesta: si apre con **Ctrl+Alt+I** (su Mac **Ctrl+Cmd+I**), oppure dentro una cella con
        **Ctrl+I** (su Mac **Cmd+I**).
    """)
    nb.md("""
        La chat ha tre modalità (Ask, Plan, Agent), che si scelgono dal menu in basso nel riquadro della chat.
    """)
    nb.md("""
        | Modalità | Cosa fa | Quando usarla |
        |---|---|---|
        | Ask | risponde; il codice lo copiamo noi | domande, spiegazioni, una funzione alla volta |
        | Plan | scrive il piano dei passi senza toccare i file; il piano si legge e si corregge, poi si passa ad Agent | compiti di più passi, prima di lasciar fare |
        | Agent | legge i file, modifica il codice mostrando le differenze da accettare, lancia comandi nel terminale chiedendo conferma, crea celle, finché non pensa di aver finito | compiti che sappiamo controllare pezzo per pezzo |
    """)
    nb.md("""
        Claude Code e Codex fanno la stessa cosa con un vestito diverso: tutti e due girano nel terminale
        o come estensione di VS Code, e Codex anche dentro ChatGPT. Cambia il modello sotto e qualche
        comando. Le tre regole che vediamo più avanti valgono per tutti e tre.
    """)
    nb.md("""
        Partiamo dal completamento. Il modo più affidabile di ottenerlo è scrivere la firma di una funzione
        e una docstring che dice cosa deve fare: Copilot legge la docstring e propone il corpo.
    """)
    nb.prova_tu(
        richiesta="""
            Nella cella qui sotto cancella i tre puntini, premi **Invio** dopo la docstring e aspetta un
            secondo: Copilot propone il corpo della funzione. Accettalo con **Tab** solo se fa quel che dice
            la docstring: somma delle potenze quartorarie divisa per 4. Poi esegui la verifica.
        """,
        starter="""
            def mw_a_mwh(potenze_mw):
                \"\"\"Energia in MWh di una lista di potenze medie quartorarie in MW.\"\"\"
                ...


            mw_a_mwh([100, 100, 100, 100])
        """,
        soluzione="""
            def mw_a_mwh(potenze_mw):
                \"\"\"Energia in MWh di una lista di potenze medie quartorarie in MW.\"\"\"
                return sum(potenze_mw) / 4


            mw_a_mwh([100, 100, 100, 100])
        """,
        verifica="""
            assert mw_a_mwh([100, 100, 100, 100]) == 100, "❌ Quattro quartorari a 100 MW sono 100 MWh"
            assert mw_a_mwh([12.4, 12.9, 13.1, 12.6]) == 12.75, "❌ Somma delle potenze diviso 4, senza arrotondare"
            assert mw_a_mwh([100] * 8) == 200, "❌ Otto quartorari a 100 MW sono due ore: 200 MWh, non la media"
        """,
    )
    nb.md("""
        Se il corpo proposto era diverso (un ciclo, `* 0.25`), può essere giusto lo stesso: la verifica
        decide, non l'aspetto del codice. È il primo controllo che faremo sempre.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Le parole che servono", intro="""
        Sei parole spiegano perché Copilot a volte ha ragione e a volte inventa. Stanno nelle tabelle
        qui sotto, da rileggere quando una risposta non torna.
    """)
    nb.md("""
        | Parola | Cos'è | Perché conta |
        |---|---|---|
        | token | il pezzo di testo che il modello legge e scrive: circa tre quarti di parola in inglese, un po' meno in italiano | si paga e si conta in token: incollare un traceback intero costa poco |
        | finestra di contesto | quanti token il modello tiene in mente in una conversazione | se la chat "dimentica" la colonna di cui parlavamo dieci messaggi fa, la finestra è piena: chat nuova |
    """)
    nb.md("""
        | Parola | Cos'è | Perché conta |
        |---|---|---|
        | allucinazione | il modello scrive il seguito più probabile e non verifica che sia vero | un parametro dal nome sensato può non esistere; in Ask nessuno esegue il codice: lo scopriamo solo eseguendolo noi |
        | modello piccolo o grande | il completamento usa un modello piccolo e veloce; nella chat il modello lo scegli tu dal menu in basso, accanto alla modalità | per un `groupby` basta il piccolo; se la risposta su un traceback strano non convince, si prova un modello più grande dal menu |
    """)
    nb.md("""
        | Parola | Cos'è | Perché conta |
        |---|---|---|
        | Plan e Agent | prima il piano dei passi, poi le modifiche | il piano si legge; solo dopo si lascia eseguire |
        | prompt e contesto | il prompt è la domanda; il contesto è tutto il resto che il modello vede: file aperti, celle, quello che incolli | la qualità della risposta dipende più dal contesto che dalla domanda |
    """)
    nb.md("""
        Il contesto è la parte che decidiamo noi. Tre cose fanno la differenza: `df.info()` incollato nella
        chat (nomi, tipi e righe), i nomi esatti delle colonne, il traceback intero dalla prima riga all'ultima.
        Carichiamo il DataFrame su cui lavoreremo e guardiamo cosa gli daremo da leggere.
    """)
    nb.code("""
        import pandas as pd

        df = pd.read_csv("../Dati/impianti_fv.csv")
        df.info()
    """)
    nb.md("""
        Questo output è il contesto da incollare. "Ho un DataFrame con degli impianti" fa indovinare i nomi
        delle colonne; `df.info()` li dà, con i tipi. Un prompt completo somiglia a questo:
    """)
    nb.md("""
        ```text
        Ho un DataFrame pandas `df` con queste colonne:
        id_impianto (str), comune (str), provincia (str), kwp (float), anno_allaccio (int), lat e lon (float).
        Scrivi una funzione `potenza_per_provincia(df)` che restituisce un DataFrame con due colonne,
        provincia e kwp, con la somma dei kwp per provincia, ordinato dal più alto al più basso.
        Niente commenti, docstring di una riga.
        ```
    """)
    nb.md("""
        Incollare va bene per una domanda sola. Per un file intero basta scriverne il nome nel prompt con
        `#file:` (per esempio `#file:Dati/README.md`), e Copilot lo legge da sé. Selezionare righe o una
        cella prima di aprire la chat le mette nel contesto.
    """)
    nb.md("""
        Le regole che valgono sempre si scrivono una volta sola, in un file di istruzioni del progetto:
        `.github/copilot-instructions.md` per Copilot, `CLAUDE.md` per Claude Code, `AGENTS.md` per Codex.
        L'agente lo legge a ogni richiesta. Per un progetto come il nostro bastano tre righe:

        ```text
        Le librerie si aggiungono con `uv add`, mai con `pip install`.
        I dati stanno in `Dati/` (dai notebook, `../Dati/`).
        pandas 3: riassegna sempre il risultato, niente `inplace=True`.
        ```

        Se l'agente propone `pip install` o un percorso inventato, di solito questo file manca.
    """)
    nb.box("ricorda", """
        Incolla `df.info()` e i nomi esatti delle colonne: senza, il modello inventa quelli che gli
        sembrano plausibili.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Prova guidata", intro="""
        Tre prompt, in ordine. Per ognuno: copia il testo nella chat in modalità Ask, leggi la
        risposta, incolla il codice nella cella sotto, esegui, controlla. La verifica guarda il risultato
        finale, non da dove viene.
    """)
    nb.sottosezione("Una funzione", intro="""
        Il primo prompt è quello della sezione precedente. Copialo com'è.
    """)
    nb.md("""
        ```text
        Ho un DataFrame pandas `df` con queste colonne:
        id_impianto (str), comune (str), provincia (str), kwp (float), anno_allaccio (int), lat e lon (float).
        Scrivi una funzione `potenza_per_provincia(df)` che restituisce un DataFrame con due colonne,
        provincia e kwp, con la somma dei kwp per provincia, ordinato dal più alto al più basso.
        Niente commenti, docstring di una riga.
        ```

        Cosa controllare: `groupby` sulla provincia e `sum` sui kwp; `sort_values` con `ascending=False`;
        `reset_index`, così provincia torna colonna. E un numero che conosci: la somma della colonna kwp
        deve restare la stessa, 737.
    """)
    nb.prova_tu(
        richiesta="""
            Incolla la funzione proposta da Copilot al posto dei puntini, eseguila su `df` e salva il
            risultato in `per_provincia`.
        """,
        starter="""
            ...


            per_provincia = potenza_per_provincia(df)
            per_provincia
        """,
        soluzione="""
            def potenza_per_provincia(df):
                \"\"\"Somma dei kWp per provincia, dalla più alta alla più bassa.\"\"\"
                somma = df.groupby("provincia")["kwp"].sum().reset_index()
                return somma.sort_values("kwp", ascending=False).reset_index(drop=True)


            per_provincia = potenza_per_provincia(df)
            per_provincia
        """,
        verifica="""
            assert set(per_provincia.columns) == {"provincia", "kwp"}, "❌ Due colonne: provincia e kwp (serve un reset_index dopo il groupby)"
            assert round(per_provincia["kwp"].sum(), 1) == 737.0, "❌ La somma dei kwp deve restare 737: controlla che sommi e non faccia la media"
            assert per_provincia["kwp"].is_monotonic_decreasing, "❌ Ordina dal più alto al più basso: ascending=False"
            assert per_provincia.iloc[0]["provincia"] == "MI", "❌ In testa deve esserci MI, la provincia con più kWp: controlla l'ordinamento"
        """,
    )

    nb.sottosezione("La spiegazione di un errore", intro="""
        Questa cella dà errore apposta: eseguila e copia il traceback intero, dalla prima riga all'ultima.
    """)
    nb.code('totale_kwp = df["kWp"].sum()', errore=True)
    nb.md("""
        ```text
        Spiegami questo errore senza correggerlo: cosa significa, perché succede, dove devo guardare.

        <incolla qui il traceback intero>
        ```

        Cosa controllare: la risposta deve nominare `KeyError`, dire che la colonna `kWp` non esiste e
        che pandas distingue maiuscole e minuscole. Se propone anche il codice corretto va bene, ma prima
        leggi la spiegazione: è quella che ti serve la prossima volta.
    """)
    nb.prova_tu(
        richiesta="""
            Correggi la riga e salva il totale in `totale_kwp`.
        """,
        starter="""
            totale_kwp = ...
            totale_kwp
        """,
        soluzione="""
            totale_kwp = df["kwp"].sum()
            totale_kwp
        """,
        verifica="""
            assert totale_kwp == 737.0, "❌ La colonna si chiama kwp, tutta minuscola"
        """,
    )

    nb.sottosezione("Un errore che non fa rumore", intro="""
        Il terzo prompt è innocuo: nessun parametro strano, nessuna trappola nel testo. Il codice gira e
        non dà errori; se è sbagliato, nessuno ce lo dice.
    """)
    nb.md("""
        ```text
        Ho un DataFrame pandas `letture` letto da letture_pod_2025.csv, con le colonne pod, cliente, data (testo, es. 01/03/2025), fascia, kwh.
        Converti la colonna data in datetime e calcola in `per_mese` la somma dei kwh per mese (una Series con il mese come indice).
        ```

        Cosa controllare: un numero che conosci. Le letture coprono un anno, quindi i mesi devono essere
        dodici e la somma 134507,7. Se `per_mese` ha una riga sola, `pd.to_datetime` ha letto 01/03/2025
        all'americana (3 gennaio): servono `format="%d/%m/%Y"` o `dayfirst=True`.
    """)
    nb.prova_tu(
        richiesta="""
            La lettura del file è già pronta. Incolla al posto dei puntini il codice proposto da Copilot e
            lascia il risultato in `per_mese`.
        """,
        starter="""
            letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")

            ...
            per_mese
        """,
        soluzione="""
            letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")

            letture["data"] = pd.to_datetime(letture["data"], format="%d/%m/%Y")
            per_mese = letture.groupby(letture["data"].dt.month)["kwh"].sum()
            per_mese
        """,
        verifica="""
            assert len(per_mese) == 12, "❌ I mesi devono essere 12: la data è gg/mm/aaaa, serve format=\\"%d/%m/%Y\\""
            assert round(per_mese.sum(), 1) == 134507.7, "❌ La somma dei kwh deve restare 134507.7"
        """,
    )
    nb.md("""
        Nessun traceback, nessun avviso: il codice sbagliato gira come quello giusto. Nell'esercizio sul
        parametro inventato, alla fine, Copilot segue invece un nome che non esiste. In tutti e due i casi
        se ne accorge solo chi controlla il risultato.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Le tre regole", intro="""
        Tre regole prima di accettare codice generato, da chiunque arrivi. Sono le stesse che useremo nel
        capstone.
    """)
    nb.md("""
        **Verifica.** Esegui subito, guarda l'output, confrontalo con un numero che conosci già: la somma
        dei kwp, il numero di righe, il valore di un POD che hai sotto mano. Un parametro mai visto si
        controlla con `help()` prima di usarlo, non dopo l'errore.
    """)
    nb.md("""
        **Chiedi spiegazioni.** "Spiegami" prima di "correggi", e sempre con il traceback intero. Se la
        spiegazione non la capisci, il codice corretto non lo accetti: la prossima volta lo stesso errore
        lo dovrai riconoscere da solo.
    """)
    nb.md("""
        **Piccoli passi.** Un prompt, una cella, un controllo. "Fai tutta l'analisi" produce un notebook
        lungo con tre errori nascosti in mezzo; "calcola il profilo medio orario" produce una cella che
        puoi leggere. La modalità Agent va bene solo su cose che sai controllare pezzo per pezzo.
    """)
    nb.md("""
        In Agent le modifiche arrivano come differenze: rosso è quello che toglie, verde quello che
        aggiunge. Leggi prima il rosso, poi tieni o annulla blocco per blocco (**Keep** o **Undo**). Se
        propone un comando nel terminale, leggilo prima di approvarlo: un `pip install` al posto di
        `uv add` installa nell'ambiente sbagliato.
    """)
    nb.box("ricorda", """
        - Verifica con un numero che conosci, non con l'aspetto del codice.
        - "Spiegami l'errore" con il traceback intero, mai solo "risolvilo".
        - Un prompt, una cella, un controllo.
    """)

    # ------------------------------------------------------------------ 5
    nb.sezione("Ruff in VS Code", intro="""
        Il primo controllo su codice che non abbiamo scritto noi lo fa una macchina. Ruff è linter e
        formatter in uno: segnala quello che non va (`check`) e rimette in forma il codice da solo
        (`format`), con le regole di PEP 8 viste nel notebook sul codice leggibile. È già tra le
        dipendenze di sviluppo del progetto e si lancia dal terminale con `uv run ruff`.
    """)
    nb.md("""
        In VS Code si installa l'estensione **Ruff** dal pannello delle estensioni. Poi si attiva
        la formattazione al salvataggio: ogni **Ctrl+S** su un file `.py` rimette a posto spazi,
        virgole e righe vuote. In `settings.json` servono queste righe:

        ```json
        {
            "[python]": {
                "editor.defaultFormatter": "charliermarsh.ruff",
                "editor.formatOnSave": true
            }
        }
        ```
    """)
    nb.md("""
        I tre avvisi che vedremo più spesso. La lettera del codice è la famiglia (`F` codice inutile
        o sospetto, `E` stile, PEP 8), il numero la regola.

        | Codice | Avviso | Cosa vuol dire |
        |---|---|---|
        | `F401` | `` `math` imported but unused `` | una libreria importata e mai usata: via la riga |
        | `F841` | `` Local variable `totale` is assigned to but never used `` | una variabile calcolata e mai letta: un avanzo o un refuso |
        | `E501` | `Line too long (129 > 100)` | la riga supera il limite scritto in `pyproject.toml`: si spezza |
    """)
    nb.md("""
        Dal terminale, nella cartella del progetto, su un file `.py`:

        ```bash
        uv run ruff check report_pod.py                            # elenca gli avvisi
        uv run ruff check --output-format concise report_pod.py    # una riga per avviso
        uv run ruff format report_pod.py                           # riscrive il file nella forma giusta
        uv run ruff check --fix report_pod.py                      # corregge quello che sa correggere
        ```
    """)
    nb.md("""
        Il secondo comando, su un file con i tre problemi della tabella:

        ```text
        report_pod.py:1:8: F401 [*] `math` imported but unused
        report_pod.py:9:5: F841 Local variable `totale` is assigned to but never used
        report_pod.py:10:101: E501 Line too long (129 > 100)
        Found 3 errors.
        [*] 1 fixable with the `--fix` option (1 hidden fix can be enabled with the `--unsafe-fixes` option).
        ```
    """)
    nb.md("""
        Ogni riga dice file, riga, colonna, codice e messaggio. `format` tocca solo la forma e
        non cambia mai cosa fa il codice; `check --fix` toglie gli import inutilizzati e poco
        altro. `format` spezza le righe lunghe di codice ma non una stringa: quella, come le
        variabili inutili, resta a noi. Per una stringa lunga, la ricetta è questa.
    """)
    nb.code("""
        soglia_kwh = 1000

        messaggio = (
            f"Trovati 3 POD sopra la soglia di {soglia_kwh} kWh: "
            "controllare le letture di luglio prima di fatturare"
        )
        messaggio
    """)
    nb.md("""
        Due pezzi tra parentesi, uno per riga, e Python li attacca in una stringa sola. La `f`
        serve solo sui pezzi che hanno le graffe.
    """)
    nb.box("nota", """
        Ruff legge anche i notebook: `uv run ruff check nome.ipynb` controlla le celle una per una,
        con la stessa configurazione del progetto.
    """)

    # ------------------------------------------------------------------ 6
    nb.sezione("Leggere il codice scritto da un agente", intro="""
        In modalità Agent chiediamo: "Scrivi uno script che legge le letture, somma i kWh per POD e salva
        un CSV". In pochi secondi torna un file di una quarantina di righe. Prima di lanciarlo lo leggiamo
        dall'alto, un pezzo alla volta. In testa ci sono la descrizione, gli import e le costanti:
    """)
    nb.md('''
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
        | Riga | Come si riconosce | Cosa fa | Va toccata? |
        |---|---|---|---|
        | `"""Totale..."""` | prima riga, tra tre virgolette | docstring di modulo: cosa fa lo script | no |
        | `import`, `from ... import` | in testa | caricano le librerie: `logging`, `dataclasses`, `pathlib` sono standard, pandas è installata | no |
        | `logger = logging.getLogger(...)` | dopo gli import | prepara il log: `logger.info(...)` è un `print` con il livello davanti (`INFO:__main__:...`), nel terminale | no |
        | `DATA_DIR = Path("Dati")` | tutto maiuscolo | costante: dove sono i dati, dalla cartella da cui si lancia lo script | se i dati stanno altrove |
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
        | Riga | Come si riconosce | Cosa fa | Va toccata? |
        |---|---|---|---|
        | `@dataclass` | riga che inizia con `@`, sopra un `class` o un `def` | decoratore: cambia come si comporta quello che sta sotto; qui trasforma `Config` in un contenitore di campi, ognuno con tipo e, se c'è, default; scrive da solo il costruttore (`Config(path=...)`) e la stampa | no |
        | `sep: str = ";"` | nome, due punti, tipo, uguale | campo con type hint e default | no |
    ''')
    nb.md("Poi le funzioni che fanno il lavoro:")
    nb.md('''
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
    ''', aula="base")
    nb.md('''
        ```python
        def leggi_letture(path: Path, **opzioni) -> pd.DataFrame:
            """Legge il CSV delle letture; le opzioni vanno dritte a read_csv."""
            if not path.exists():
                raise FileNotFoundError(f"File non trovato: {path}")
            return pd.read_csv(path, **opzioni)


        def totale_per_pod(letture: pd.DataFrame, fasce: list[str] | None = None) -> pd.DataFrame:
            """Somma dei kWh per POD, eventualmente solo per alcune fasce."""
            mancanti = [col for col in ("pod", "fascia", "kwh") if col not in letture.columns]
            if mancanti:
                raise ValueError(f"Colonne mancanti: {mancanti}")
            if fasce is not None:
                letture = letture[letture["fascia"].isin(fasce)]
            return letture.groupby("pod")["kwh"].sum().reset_index()
        ```
    ''', aula="avanzata")
    nb.md('''
        | Riga | Come si riconosce | Cosa fa | Va toccata? |
        |---|---|---|---|
        | `-> pd.DataFrame` | dopo la parentesi del `def` | type hint di ritorno: cosa restituisce la funzione | no |
        | `fasce: list[str] \\| None = None` | parametro con default `None` | lista di stringhe oppure `None` (`\\|` si legge «oppure»); facoltativo: se non lo passiamo, la funzione tiene tutte le fasce | no |
        | `raise FileNotFoundError(...)` | dentro un `if` | crea un errore apposta, con un messaggio chiaro: il contrario di `except` | no |

        Quello che tocchiamo noi sono le due o tre righe di pandas: `read_csv` e il `groupby`.
    ''')
    with nb.solo("avanzata"):
        nb.md("""
            Nella firma di `leggi_letture` c'è anche `**opzioni`: raccoglie tutti i parametri passati per
            nome (`sep=`, `decimal=`, `encoding=`) e li passa avanti a `read_csv` così come sono. In
            `totale_per_pod` c'è una comprehension: `mancanti` è la lista delle colonne richieste che non
            ci sono, vuota se ci sono tutte.
        """)
    nb.md("In fondo, chi le usa:")
    nb.md('''
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
    ''', aula="base")
    nb.md('''
        ```python
        def main() -> None:
            logging.basicConfig(level=logging.INFO)
            config = Config(path=DATA_DIR / "letture_pod_2025.csv")
            letture = leggi_letture(
                config.path, sep=config.sep, decimal=config.decimal, encoding=config.encoding
            )
            totali = totale_per_pod(letture)
            totali.to_csv(OUTPUT, index=False)
            logger.info(f"Salvati {len(totali)} POD in {OUTPUT}")


        if __name__ == "__main__":
            main()
        ```
    ''', aula="avanzata")
    nb.md('''
        | Riga | Come si riconosce | Cosa fa | Va toccata? |
        |---|---|---|---|
        | `-> None` | dopo la parentesi del `def` | la funzione non restituisce niente: `main` esegue i passi | no |
        | `logging.basicConfig(level=logging.INFO)` | prima riga di `main` | accende il log: senza, `logger.info` non stampa | no |
        | `if __name__ == "__main__":` (blocco main) | in fondo al file | parte solo se il file è il programma lanciato, con `uv run` o in una cella; non se viene importato | no |
        | `main()` | l'ultima riga | chiama la funzione che mette in fila i passi | no |
    ''')
    nb.md("""
        Portiamo nel notebook la configurazione e le due funzioni; cambia solo `DATA_DIR`, perché il
        notebook gira nella sua cartella e i dati stanno un livello sopra, in `../Dati`.
    """)
    nb.code("""
        from dataclasses import dataclass
        from pathlib import Path

        import pandas as pd

        DATA_DIR = Path("../Dati")


        @dataclass
        class Config:
            path: Path
            sep: str = ";"
            decimal: str = ","
            encoding: str = "latin-1"


        config = Config(path=DATA_DIR / "letture_pod_2025.csv")
        config
    """)
    nb.md("""
        La stampa ordinata di `config` non l'abbiamo scritta noi: l'ha aggiunta `@dataclass`. Poi le due
        funzioni, identiche.
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
    ''', aula="base")
    nb.code('''
        def leggi_letture(path: Path, **opzioni) -> pd.DataFrame:
            """Legge il CSV delle letture; le opzioni vanno dritte a read_csv."""
            if not path.exists():
                raise FileNotFoundError(f"File non trovato: {path}")
            return pd.read_csv(path, **opzioni)
    ''', aula="avanzata")
    nb.code('''
        def totale_per_pod(letture: pd.DataFrame, fasce: list[str] | None = None) -> pd.DataFrame:
            """Somma dei kWh per POD, eventualmente solo per alcune fasce."""
            mancanti = [col for col in ("pod", "fascia", "kwh") if col not in letture.columns]
            if mancanti:
                raise ValueError(f"Colonne mancanti: {mancanti}")
            if fasce is not None:
                letture = letture[letture["fascia"].isin(fasce)]
            return letture.groupby("pod")["kwh"].sum().reset_index()
    ''', aula="avanzata")
    nb.md("Le chiamiamo come fa `main`, senza salvare il CSV:")
    nb.code("""
        totali = totale_per_pod(leggi_letture(config))
        totali
    """, aula="base")
    nb.code("""
        letture = leggi_letture(
            config.path, sep=config.sep, decimal=config.decimal, encoding=config.encoding
        )
        totali = totale_per_pod(letture)
        totali
    """, aula="avanzata")
    nb.md("""
        Sei POD, una riga ciascuno. Il numero che conosciamo è la somma di tutte le letture,
        134507,7 kWh:
    """)
    nb.code("""
        round(totali["kwh"].sum(), 1)
    """)
    nb.md("""
        Con il percorso dello script, `Dati`, la stessa lettura dal notebook non trova il file. Questa
        cella dà errore apposta: leggiamo l'ultima riga.
    """)
    nb.code("""
        leggi_letture(Config(path=Path("Dati") / "letture_pod_2025.csv"))
    """, aula="base", errore=True)
    nb.code("""
        leggi_letture(Path("Dati") / "letture_pod_2025.csv", sep=";")
    """, aula="avanzata", errore=True)
    nb.md("""
        L'ultima riga è il messaggio del `raise`: lo script si ferma con una frase chiara, prima di arrivare
        dentro pandas.
    """)
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
            `"blocco main"`, `"log"` e `"costante"`. Le tabelle qui sopra hanno tutte le risposte.
        """,
        starter="""
            cosa_e = {
                "@dataclass": ...,
                "-> pd.DataFrame": ...,
                'if __name__ == "__main__":': ...,
                "logger.info(...)": ...,
                "DATA_DIR": ...,
            }
            cosa_e
        """,
        soluzione="""
            cosa_e = {
                "@dataclass": "decoratore",
                "-> pd.DataFrame": "type hint",
                'if __name__ == "__main__":': "blocco main",
                "logger.info(...)": "log",
                "DATA_DIR": "costante",
            }
            cosa_e
        """,
        verifica="""
            assert str(cosa_e["@dataclass"]).strip().lower() == "decoratore", "❌ @dataclass: una riga con @ sopra una class è un decoratore"
            assert str(cosa_e["-> pd.DataFrame"]).strip().lower() == "type hint", "❌ -> pd.DataFrame: dice cosa restituisce la funzione, è un type hint"
            assert str(cosa_e['if __name__ == "__main__":']).strip().lower() == "blocco main", "❌ if __name__ == \\"__main__\\": è il blocco main, in fondo al file"
            assert str(cosa_e["logger.info(...)"]).strip().lower() == "log", "❌ logger.info(...): un print con il livello davanti, cioè il log"
            assert str(cosa_e["DATA_DIR"]).strip().lower() == "costante", "❌ DATA_DIR: tutto maiuscolo, è una costante"
        """,
    )
    nb.md("""
        Tutte le forme che si incontrano, una per riga, stanno nella
        [scheda per leggere il codice](../Schede/Scheda_leggere_codice.md).
    """)
    nb.box("ricorda", """
        - Leggi dall'alto: import, costanti, `def`; in fondo, chi li usa.
        - Una riga che non capisci: "spiegami questa riga", poi verifica eseguendo.
        - Il lavoro vero sono poche righe: controlla quelle, con un numero che conosci.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il parametro inventato",
        scenario="""
            L'ufficio misure ci manda `letture_pod_2025.csv`, il solito CSV all'italiana: punto e virgola,
            virgola decimale, encoding latin-1. Giulia ha chiesto a Copilot di leggerlo con i nomi dei
            parametri che ricordava lei, ha incollato quel che le ha dato, e adesso la cella dà `TypeError`.
            Ha un treno tra venti minuti.
        """,
        richiesta="""
            1. Dai alla chat questo prompt e incolla la riga che propone al posto di quella commentata:

               ```text
               Leggi il file ../Dati/letture_pod_2025.csv con pandas: separatore punto e virgola,
               virgola come decimale, encoding latin-1. Usa i parametri separator, decimal_separator ed encoding.
               ```
            2. Eseguila. Se dà `TypeError`, leggi l'ultima riga del traceback: quale parametro non esiste?
            3. Apri la documentazione con `help(pd.read_csv)` e trova i nomi giusti per il separatore dei
               campi e per il decimale.
            4. Leggi il file in `letture` con i parametri giusti e controlla con `letture.info()`: la
               colonna `kwh` deve essere `float64`.
        """,
        suggerimento="Nella firma di `read_csv` i parametri sono in ordine: quello del separatore è tra i primi, quello del decimale più in basso.",
        starter="""
            # 1-2. incolla qui la riga proposta da Copilot ed eseguila: leggi l'ultima riga del traceback
            # letture = pd.read_csv("../Dati/letture_pod_2025.csv", ...)

            # 3. la documentazione: cerca i parametri per il separatore e per il decimale
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
            assert set(letture.columns) == {"pod", "cliente", "data", "fascia", "kwh"}, "❌ Le colonne devono essere pod, cliente, data, fascia, kwh"
            assert str(letture["kwh"].dtype) == "float64", "❌ kwh deve essere float64: serve decimal=','"
            assert round(letture["kwh"].sum(), 1) == 134507.7, "❌ La somma dei kwh non torna: controlla decimal e sep"
        """,
        perche="I nomi dei parametri non si indovinano: `sep` e `decimal` stanno nella firma di `read_csv`. Copilot li conosce benissimo, finché il prompt non gliene suggerisce altri.",
        passo_in_piu=dict(
            testo="""
                Chiedi a Copilot, in modalità Ask, di chiudere la lettura giusta in una funzione
                `leggi_csv_letture(path)` con docstring di una riga e type hint. Incollala, poi controlla con
                `help(leggi_csv_letture)` che la docstring ci sia e che il risultato sia lo stesso di prima.
            """,
            starter="""
                ...


                help(leggi_csv_letture)
                letture_bis = leggi_csv_letture("../Dati/letture_pod_2025.csv")
            """,
            soluzione="""
                def leggi_csv_letture(path: str) -> pd.DataFrame:
                    \"\"\"Legge un CSV di letture all'italiana: punto e virgola, virgola decimale, latin-1.\"\"\"
                    return pd.read_csv(path, sep=";", decimal=",", encoding="latin-1")


                help(leggi_csv_letture)
                letture_bis = leggi_csv_letture("../Dati/letture_pod_2025.csv")
            """,
            verifica="""
                assert leggi_csv_letture.__doc__, "❌ La funzione deve avere una docstring"
                assert letture_bis.shape == (216, 5), "❌ leggi_csv_letture deve restituire le stesse 216 righe e 5 colonne"
            """,
        ),
    )
    nb.esercizio(
        titolo="Spiegami l'errore",
        bis=True,
        scenario="""
            Marco, di reperibilità nel weekend, deve mandare al commerciale la lista degli impianti sopra
            i 10 kWp in provincia di Milano. Ha scritto il filtro di corsa e la cella esplode con un
            `TypeError` lungo tre schermate. Ci chiede un occhio prima di chiamare qualcuno.
        """,
        richiesta="""
            1. La cella qui sotto dà errore apposta: eseguila e copia il traceback intero.
            2. Dai alla chat questo prompt:

               ```text
               Spiegami questo errore senza correggerlo. Perché Python prova a fare 10 & una colonna di testo?

               <incolla qui il traceback intero>
               ```
            3. La spiegazione deve parlare di precedenza: `&` viene valutato prima di `>` e `==`. Se non lo
               dice, chiediglielo.
            4. Correggi la riga nella stessa cella, con le parentesi attorno a ogni condizione, e lascia il
               risultato in `grandi_milano`.
        """,
        suggerimento="Il traceback è lungo perché passa per pandas; l'ultima riga dice chi non sa fare `&` con chi.",
        starter="""
            impianti = pd.read_csv("../Dati/impianti_fv.csv")

            grandi_milano = impianti[impianti["kwp"] > 10 & impianti["provincia"] == "MI"]
            grandi_milano
        """,
        soluzione="""
            impianti = pd.read_csv("../Dati/impianti_fv.csv")

            grandi_milano = impianti[(impianti["kwp"] > 10) & (impianti["provincia"] == "MI")]
            grandi_milano
        """,
        verifica="""
            assert len(grandi_milano) == 5, "❌ grandi_milano: 5 impianti sopra i 10 kWp in provincia di Milano"
            assert set(grandi_milano["provincia"]) == {"MI"}, "❌ Solo la provincia MI"
            assert (grandi_milano["kwp"] > 10).all(), "❌ Solo gli impianti sopra i 10 kWp"
        """,
        perche="Le parentesi attorno a ogni condizione non sono stile: senza, `10 & impianti[\"provincia\"]` viene calcolato per primo e non ha senso.",
    )
    nb.esercizio(
        titolo="Leggere prima di lanciare",
        scenario='''
            Paolo, in fatturazione, ha fatto scrivere all'agente lo script del report settimanale e vuole
            metterlo nel giro del lunedì mattina. Prima ce lo fa leggere. Dice che gira senza errori, ma il
            totale gli sembra strano.

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
            1. Compila `risposte` con quattro voci: in `"file letto"` il nome del file che lo script legge;
               in `"lavoro vero"` il nome della funzione che fa il calcolo; in `"riga con @"` cos'è quella
               riga, scegliendo tra `"decoratore"`, `"commento"` e `"type hint"`; in
               `"lanciato in una cella"` cosa succede incollando tutto lo script in una cella del notebook,
               scegliendo tra `"FileNotFoundError"`, `"NameError"` e `"non parte niente"`.
            2. Trova il dettaglio sbagliato nella `leggi_letture` dello script e scrivi nella cella la
               versione giusta, che qui riceve direttamente il percorso.
        """,
        suggerimento="Guarda `totale.dtypes`: se `kwh` non è un numero, il problema è in quello che `read_csv` riceve.",
        starter="""
            risposte = {
                "file letto": ...,
                "lavoro vero": ...,
                "riga con @": ...,
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
                "file letto": "letture_pod_2025.csv",
                "lavoro vero": "report_kwh",
                "riga con @": "decoratore",
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
            assert str(risposte["file letto"]).endswith("letture_pod_2025.csv"), "❌ file letto: il nome del file sta nel default di path, dentro Config"
            assert str(risposte["lavoro vero"]).strip().rstrip("()") == "report_kwh", "❌ lavoro vero: il nome della funzione con il groupby, come stringa; solo il nome, senza parentesi"
            assert risposte["riga con @"] == "decoratore", "❌ riga con @: una riga che inizia con @ sopra una class è un decoratore"
            assert risposte["lanciato in una cella"] == "FileNotFoundError", "❌ lanciato in una cella: il blocco main parte anche nel notebook, e da qui il percorso Dati non esiste"
            assert str(totale["kwh"].dtype) == "float64", "❌ kwh è ancora testo: controlla totale.dtypes e i parametri di read_csv"
            assert round(totale["kwh"].sum(), 1) == 134507.7, "❌ La somma dei kwh deve essere 134507.7: controlla il tipo di kwh con .dtypes"
        """,
        perche="Nessun traceback, solo un numero sbagliato: senza `decimal=\",\"` la colonna `kwh` era rimasta testo e `sum()` ha incollato le stringhe. È il caso in cui l'errore lo trovi solo controllando con un numero che conosci.",
    )
    nb.esercizio(
        titolo="Pulizia con Ruff",
        scenario="""
            Un collega ha lasciato lo script `report_pod.py` qui sotto e vuole metterlo nel
            repository del team, dove ogni file deve passare `uv run ruff check` senza avvisi.
            Prima di lanciarlo facciamo noi il lavoro di Ruff: leggiamo il file e scriviamo quali
            avvisi darebbe.

            ```python
            import math

            soglia_kwh = 1000
            pod_anomali = ["IT001E45678901"]


            def riepilogo(pod_anomali, soglia_kwh):
                n = len(pod_anomali)
                totale = 0
                return f"Trovati {n} POD sopra la soglia di {soglia_kwh} kWh nel file letture_pod_2025.csv: controllare le letture di luglio"


            print(riepilogo(pod_anomali, soglia_kwh))
            ```
        """,
        richiesta="""
            Tre passi, il terzo facoltativo.

            1. Metti in `avvisi` la lista dei codici Ruff che questo file farebbe scattare, come stringhe, uno per problema.
            2. Riscrivi il codice corretto nella cella: niente avvisi, stesso testo in uscita, una docstring per `riepilogo`.
            3. Salva l'originale in un file `report_pod.py` nella cartella principale del progetto, accanto a `pyproject.toml`, e da lì lancia `uv run ruff check report_pod.py` nel terminale per confrontare.
        """,
        suggerimento="I codici sono nella tabella della sezione su Ruff; la stringa lunga si spezza tra parentesi.",
        starter="""
            avvisi = [...]

            # qui sotto il codice corretto
            soglia_kwh = 1000
            pod_anomali = ["IT001E45678901"]


            def riepilogo(pod_anomali, soglia_kwh):
                ...


            print(riepilogo(pod_anomali, soglia_kwh))
        """,
        soluzione="""
            # un import mai usato, una variabile mai letta, una riga da 129 caratteri
            avvisi = ["F401", "F841", "E501"]

            soglia_kwh = 1000
            pod_anomali = ["IT001E45678901"]


            def riepilogo(pod_anomali, soglia_kwh):
                \"\"\"Una riga di testo con quanti POD superano la soglia.\"\"\"
                n = len(pod_anomali)
                return (
                    f"Trovati {n} POD sopra la soglia di {soglia_kwh} kWh nel file letture_pod_2025.csv: "
                    "controllare le letture di luglio"
                )


            print(riepilogo(pod_anomali, soglia_kwh))
        """,
        verifica="""
            assert sorted(avvisi) == ["E501", "F401", "F841"], "❌ avvisi: tre codici come stringhe: import inutilizzato, variabile mai usata, riga troppo lunga"
            assert riepilogo(["IT001E45678901"], 1000) == "Trovati 1 POD sopra la soglia di 1000 kWh nel file letture_pod_2025.csv: controllare le letture di luglio", "❌ riepilogo: il testo in uscita deve restare identico"
            assert riepilogo.__doc__, "❌ riepilogo: manca la docstring"
        """,
        perche="`import math` e `totale` si tolgono e basta. La riga lunga si spezza in due pezzi tra parentesi: il testo in uscita non cambia, e Ruff tace.",
    )
    return nb
