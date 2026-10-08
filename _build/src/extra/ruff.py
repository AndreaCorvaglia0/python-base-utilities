"""Extra X2 · Ruff (dimostrazione del docente)."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="X2",
        file="Ruff",
        titolo="Ruff",
        blocco=1,
        giornata=0,
        intento="Ruff controlla e rimette in forma il codice Python; vediamo come si usa in VS Code e dal terminale.",
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
        Ruff è uno strumento che svolge due compiti. Come linter, con il comando `check`, segnala i
        problemi del codice, per esempio un import inutilizzato o una variabile mai letta; come formatter,
        con il comando `format`, rimette in forma il codice secondo le regole di PEP 8 viste nel notebook
        sul codice leggibile. Nel progetto del corso Ruff è già tra le dipendenze di sviluppo e si lancia
        dal terminale con `uv run ruff`.
    """)
    nb.md("""
        In VS Code si installa l'estensione **Ruff** dal pannello delle estensioni e si attiva la
        formattazione al salvataggio, in modo che ogni **Ctrl+S** su un file `.py` sistemi spazi, virgole
        e righe vuote. Per farlo si aggiungono al file `settings.json` le righe seguenti:

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
        La tabella riporta i tre avvisi che si incontrano più spesso. Ogni avviso ha un codice formato da
        una lettera, che indica la famiglia di regole, e da un numero, che indica la regola: la famiglia
        `F` segnala codice inutile o sospetto, mentre la famiglia `E` segnala le violazioni dello stile
        PEP 8.
    """)
    nb.md("""
        | Codice | Avviso | Cosa vuol dire |
        |---|---|---|
        | `F401` | `` `math` imported but unused `` | una libreria importata e mai usata: via la riga |
        | `F841` | `` Local variable `totale` is assigned to but never used `` | una variabile calcolata e mai letta: un avanzo o un refuso |
        | `E501` | `Line too long (129 > 100)` | la riga supera il limite scritto in `pyproject.toml`: si spezza |
    """)
    nb.md("""
        Dal terminale, nella cartella del progetto, Ruff si usa con i quattro comandi qui sotto, applicati
        a un file `.py`. I primi due elencano gli avvisi, in forma estesa oppure con una riga per avviso,
        mentre gli ultimi due modificano il file:

        ```bash
        uv run ruff check report_pod.py                            # elenca gli avvisi
        uv run ruff check --output-format concise report_pod.py    # una riga per avviso
        uv run ruff format report_pod.py                           # riscrive il file nella forma giusta
        uv run ruff check --fix report_pod.py                      # corregge quello che sa correggere
        ```
    """)
    nb.md("""
        Su un file che contiene i tre problemi della tabella, il secondo comando produce questo output:

        ```text
        report_pod.py:1:8: F401 [*] `math` imported but unused
        report_pod.py:9:5: F841 Local variable `totale` is assigned to but never used
        report_pod.py:10:101: E501 Line too long (129 > 100)
        Found 3 errors.
        [*] 1 fixable with the `--fix` option (1 hidden fix can be enabled with the `--unsafe-fixes` option).
        ```
    """)
    nb.md("""
        Ogni riga dell'output indica il file, la riga, la colonna, il codice dell'avviso e il messaggio.
        Il comando `format` interviene solo sulla forma e non cambia mai il comportamento del codice,
        mentre `check --fix` toglie gli import inutilizzati e poche altre cose sicure. `format` spezza le
        righe di codice troppo lunghe, ma non spezza una stringa, e nessuno dei due comandi elimina una
        variabile inutile: queste correzioni restano a noi. Per una stringa lunga si usa la tecnica
        mostrata nella cella seguente.
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
        Quando due stringhe scritte una dopo l'altra stanno dentro le stesse parentesi, Python le unisce
        in una stringa sola, e in questo modo un testo lungo si può distribuire su più righe. Il prefisso
        `f` serve soltanto sui pezzi che contengono delle graffe da sostituire.
    """)
    nb.box("nota", """
        Ruff legge anche i notebook. Il comando `uv run ruff check nome.ipynb` controlla le celle una per
        una, con la stessa configurazione usata per i file del progetto.
    """)
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Pulizia con Ruff",
        scenario="""
            Un collega ha lasciato lo script `report_pod.py` qui sotto e vuole metterlo nel
            repository del team, dove ogni file deve passare `uv run ruff check` senza avvisi.
            Prima di lanciare Ruff proviamo a fare il suo lavoro, leggendo il file e individuando gli
            avvisi che darebbe.

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
            La consegna ha tre passi, e il terzo è facoltativo.

            1. Metti in `avvisi` la lista dei codici Ruff che questo file farebbe scattare, scritti come stringhe, uno per ogni problema.
            2. Riscrivi nella cella il codice corretto, in modo che non dia avvisi, stampi lo stesso testo e abbia una docstring per `riepilogo`.
            3. Salva l'originale in un file `report_pod.py` nella cartella principale del progetto, accanto a `pyproject.toml`, e lancia dal terminale `uv run ruff check report_pod.py` per confrontare gli avvisi di Ruff con i tuoi.
        """,
        suggerimento="I codici sono nella tabella della sezione su Ruff, e la stringa lunga si spezza in due pezzi tra parentesi, come nell'esempio del messaggio.",
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
        perche="L'import di `math` e la variabile `totale` non servono a nulla e si possono semplicemente togliere. La riga lunga si spezza in due pezzi tra parentesi; il testo in uscita resta identico e Ruff non segnala più alcun avviso.",
    )
    return nb
