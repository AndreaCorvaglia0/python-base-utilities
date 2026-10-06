"""Extra X2 · Ruff (dimostrazione del docente)."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="X2",
        file="Ruff",
        titolo="Ruff",
        blocco=1,
        giornata=0,
        intento="Ruff controlla e rimette in forma il codice Python: lo vediamo in VS Code e dal terminale.",
        obiettivi=[
            "leggere gli avvisi di Ruff e capire cosa segnalano",
            "attivare la formattazione al salvataggio in VS Code",
            "usare `ruff check` e `ruff format` dal terminale",
        ],
        tempo=10,
        dati=[],
        extra=True,
    )

    nb.sezione("Ruff: linter e formatter", intro="""
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
    nb.sezione("Esercizi")
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
