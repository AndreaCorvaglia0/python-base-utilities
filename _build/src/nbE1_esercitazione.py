"""E1 · Esercitazione 1: un'ora di domande ed esercizi sul blocco 1 (notebook 00-03), sugli esercizi originali del docente.

Nell'aula Avanzata l'ora è dedicata allo script: i corsisti rifanno la demo del docente nella cartella
`Modulo_1/Script_uv_Ruff/esercizio/`, guidati passo per passo, e gli esercizi sui notebook 00-03 restano in fondo al
notebook, facoltativi, da fare a casa. La versione Base non cambia.
"""

from textwrap import dedent

from nbkit import Notebook

# Il progetto dell'esercizio visto dalla cartella dell'esercitazione: Modulo_1/ per i corsisti (lo stato di partenza),
# Soluzioni/ per le soluzioni (lo stato finale), con lo stesso percorso relativo.
ESERCIZIO = "Script_uv_Ruff/esercizio"


def unisci(*parti: str) -> str:
    """Toglie l'indentazione a ogni pezzo di codice e li unisce con una riga vuota."""
    return "\n\n".join(dedent(p).strip("\n") for p in parti)


def esercizio_due_aule(nb: Notebook, titolo: str, scenario: str, base: dict, avanzata: dict,
                       facoltativo: bool = False) -> None:
    """Lo stesso esercizio per le due aule: titolo e scenario in comune, il resto può cambiare.

    `base` e `avanzata` contengono richiesta, starter, soluzione, verifica e suggerimenti; le chiavi che mancano
    in `avanzata` si prendono da `base`.
    """
    nb.esercizio(titolo=titolo, scenario=scenario, facoltativo=facoltativo, aula="base", **base)
    nb.esercizio(titolo=titolo, scenario=scenario, facoltativo=facoltativo, aula="avanzata", **{**base, **avanzata})


# Le verifiche dei passi leggono i file del progetto: dalla cartella del notebook, ESERCIZIO porta allo stato di
# partenza in Modulo_1/ e allo stato finale in Soluzioni/.
LEGGI_PROGETTO = f"""
    import tomllib
    from pathlib import Path

    progetto = tomllib.loads(Path("{ESERCIZIO}/pyproject.toml").read_text(encoding="utf-8"))
"""


def parte_script(nb: Notebook) -> None:
    """Avanzata: l'apertura dell'ora, le domande sul notebook Ambiente_script_e_Ruff e i passi dello script."""
    nb.md("""
        In questa esercitazione rifai, passo per passo, la demo che abbiamo appena seguito sul conto della spesa,
        lavorando nella cartella `Script_uv_Ruff/esercizio`. La cartella contiene un piccolo progetto già scritto,
        con lo script `main.py` che usa le funzioni del file `meteo.py`, e il lavoro consiste nel costruirgli un
        ambiente, una libreria alla volta, e nel mettere in ordine il codice con Ruff. Hai 45 minuti, poi guardiamo
        insieme il risultato. La seconda parte del notebook raccoglie gli esercizi sui notebook 00-03 ed è
        facoltativa, da fare a casa.
    """)
    nb.md("""
        Questa è la copia con le soluzioni: la cartella `Script_uv_Ruff/esercizio` che le sta accanto contiene già
        il progetto finito, con le librerie aggiunte e il codice in ordine, e le celle dei passi riportano i valori
        che il terminale stampa. Per rifare l'esercizio da capo si lavora nella cartella `esercizio` del modulo 1.
    """, solo_soluzioni=True)
    nb.md("""
        Tutti i comandi si scrivono nel terminale di VS Code, aperto nella cartella `esercizio`. Il modo più
        semplice per aprirlo è un clic con il tasto destro sulla cartella, nel pannello Explorer, e poi la voce
        **Open in Integrated Terminal**; in alternativa, da un terminale aperto nella cartella principale
        dell'aula, si entra nella cartella con `cd Modulo_1/Script_uv_Ruff/esercizio`. Gli script si lanciano
        sempre con `uv run`, e non con il pulsante **Run Python File** di VS Code, che usa il Python del corso,
        dove pandas è già installato, e quindi non farebbe comparire gli errori da cui parte l'esercizio.
    """)

    # ------------------------------------------------------------------ 1. Domande sul notebook della lezione
    nb.sezione("Domande", intro="""
        Le quattro domande che seguono riprendono i concetti del notebook *Ambiente, script e Ruff* che servono
        nei passi dell'esercizio, e richiedono pochi minuti. Per ciascuna conviene prevedere la risposta a mente e
        solo dopo aprirla con un clic.
    """)
    nb.domanda(
        "In quale file sono elencate le librerie di cui ha bisogno un progetto gestito con uv?",
        """
            In `pyproject.toml`, nella lista `dependencies` della sezione `[project]`. Il file `uv.lock`, che uv
            scrive da solo, registra invece le versioni esatte di tutto quello che è installato, comprese le
            librerie da cui dipendono quelle della lista.
        """,
    )
    nb.domanda(
        "Con quale comando si aggiunge una libreria al progetto, e che cosa fa quel comando?",
        """
            Con `uv add` seguito dal nome della libreria, per esempio `uv add pandas`. Il comando aggiunge la
            libreria a `pyproject.toml`, aggiorna `uv.lock` e la installa nella cartella `.venv` del progetto.
        """,
    )
    nb.domanda(
        "Che differenza c'è tra un formatter e un linter, e con quali comandi Ruff svolge i due compiti?",
        """
            Il formatter rimette in forma il codice, sistemando spazi, righe vuote e a capo senza cambiare quello
            che il programma fa, mentre il linter segnala i problemi che non riguardano la forma, come un import
            inutilizzato o una variabile mai usata. Ruff svolge entrambi i compiti: `ruff format` rimette in
            forma il codice e `ruff check` lo controlla.
        """,
    )
    nb.domanda(
        "Lo script `main.py` dell'esercizio contiene la riga `from meteo import media`, anche se `meteo` non è "
        "una libreria installata. Perché la riga funziona?",
        """
            Perché il file `meteo.py` sta nella stessa cartella di `main.py`, e Python cerca i moduli da importare
            prima nella cartella dello script lanciato e solo dopo tra i moduli di Python e le librerie installate
            in `.venv`. Un file `.py` del progetto si importa quindi come una libreria, con il nome del file senza
            l'estensione.
        """,
    )

    # ------------------------------------------------------------------ 2. I passi dello script
    nb.sezione("Lo script delle temperature", intro="""
        La cartella `esercizio` ha la stessa struttura della demo: un `pyproject.toml` con la lista delle librerie
        ancora vuota, il file `.python-version` con la versione di Python, il file `meteo.py` con tre funzioni
        sulle temperature e lo script `main.py`, che le importa, stampa la temperatura massima e quella media
        della settimana e salva una tabella in Excel. I cinque passi seguono l'ordine della demo e vanno fatti in
        sequenza, perché ognuno parte dalla cartella come l'ha lasciata il precedente.
    """)
    nb.md("""
        Ogni passo comincia dicendo che cosa vogliamo ottenere e perché, e il blocco Passo per passo, che si apre
        con un clic, elenca i comandi da lanciare; sotto c'è un suggerimento, anche lui nascosto. Il lavoro si fa
        nel terminale e nei file della cartella, mentre nella cella del passo si copia quello che il terminale ha
        stampato. La verifica controlla quei valori e legge i file del progetto, per confermare che i comandi
        hanno fatto il loro lavoro, e la cella `soluzione` mostra i comandi e i valori attesi di quel passo.
    """)
    nb.md("""
        Prima di ogni `uv add` conviene controllare che il terminale sia nella cartella `esercizio`, il cui
        percorso compare all'inizio della riga di comando. Lanciato dalla cartella principale dell'aula, il
        comando modificherebbe il `pyproject.toml` del corso invece di quello dell'esercizio. Un avviso che nomina
        `VIRTUAL_ENV` indica invece soltanto che il terminale ha attivato l'ambiente del corso, e si può ignorare,
        perché uv usa comunque l'ambiente della cartella in cui viene lanciato.
    """)

    # E1.1 ---------------------------------------------------------------
    nb.esercizio(
        titolo="Il primo lancio dello script",
        scenario="""
            Come nella demo, partiamo da un progetto che non dichiara nessuna libreria e lanciamo lo script per
            farci dire da Python che cosa manca, in modo che l'ambiente contenga soltanto le librerie che servono.
            Al primo `uv run main.py` uv crea l'ambiente del progetto in una cartella nuova, e lo script si ferma
            subito con un `ModuleNotFoundError`, il cui messaggio nomina la libreria mancante.
        """,
        richiesta="""
            1. Apri `esercizio/pyproject.toml` in VS Code e controlla che la voce `dependencies` sia una lista vuota.
            2. Nel terminale aperto nella cartella `esercizio` lancia `uv run main.py`.
            3. Scrivi in `cartella_creata` il nome della cartella che uv dice di aver creato e in
               `libreria_mancante` il nome della libreria che compare nell'ultima riga dell'errore.
        """,
        suggerimenti=[
            """
                Tra le prime righe stampate da uv c'è `Creating virtual environment at: ...`, e l'ultima riga
                dell'errore ha la forma `No module named '...'`: i due nomi da copiare stanno al posto dei puntini.
            """,
        ],
        starter="""
            # i comandi si lanciano nel terminale, nella cartella Script_uv_Ruff/esercizio
            cartella_creata = "..."
            libreria_mancante = "..."
        """,
        soluzione="""
            # nel terminale, nella cartella esercizio
            #   uv run main.py
            # Creating virtual environment at: .venv
            # ...
            # ModuleNotFoundError: No module named 'pandas'
            cartella_creata = ".venv"
            libreria_mancante = "pandas"
        """,
        verifica="""
            assert cartella_creata.strip().rstrip("/") == ".venv", "❌ cartella_creata: il nome nella riga Creating virtual environment at"
            assert libreria_mancante.strip() == "pandas", "❌ libreria_mancante: il nome tra apici nell'ultima riga dell'errore"
        """,
    )

    # E1.2 ---------------------------------------------------------------
    nb.esercizio(
        titolo="Aggiungere pandas",
        scenario="""
            Lo script ha bisogno di pandas, e una libreria si aggiunge al progetto con `uv add`, che la scrive in
            `pyproject.toml`, registra in `uv.lock` le versioni esatte e la installa in `.venv`. Vogliamo
            aggiungerla, guardare che cosa è cambiato nei due file e lanciare di nuovo lo script. Questa volta lo
            script stampa le prime due righe e si ferma più avanti, quando prova a salvare la tabella in Excel,
            perché manca una seconda libreria.
        """,
        richiesta="""
            1. Lancia `uv add pandas` e guarda l'elenco delle librerie installate, dove oltre a pandas compaiono
               quelle da cui pandas dipende, come numpy.
            2. Apri `pyproject.toml` e controlla la voce `dependencies`, poi apri il file `uv.lock`, comparso
               accanto, e cerca la riga `name = "pandas"`.
            3. Lancia di nuovo `uv run main.py` e scrivi in `seconda_libreria` il nome della libreria che manca
               adesso.
        """,
        suggerimenti=[
            """
                Il traceback è più lungo del primo, perché l'errore nasce dentro pandas, nel metodo `to_excel` che
                scrive il file Excel. Il nome della libreria che manca si legge, come prima, nell'ultima riga.
            """,
        ],
        starter="""
            seconda_libreria = "..."
        """,
        soluzione="""
            # nel terminale, nella cartella esercizio
            #   uv add pandas        installa pandas e le librerie da cui dipende
            #   uv run main.py
            # Temperatura massima della settimana: 16.0 gradi
            # Temperatura media della settimana: 15.0 gradi, calcolata su 5 giorni
            # ...
            # ModuleNotFoundError: No module named 'openpyxl'
            seconda_libreria = "openpyxl"
        """,
        verifica=unisci(LEGGI_PROGETTO, """
            librerie = progetto["project"]["dependencies"]
            assert any(voce.startswith("pandas") for voce in librerie), "❌ pandas non è tra le dependencies di esercizio/pyproject.toml: lancia uv add pandas nella cartella esercizio"
            assert seconda_libreria.strip() == "openpyxl", "❌ seconda_libreria: il nome tra apici nell'ultima riga del nuovo errore"
        """),
    )

    # E1.3 ---------------------------------------------------------------
    nb.esercizio(
        titolo="Lo script completo",
        scenario="""
            Con la seconda libreria lo script arriva fino in fondo: stampa la temperatura massima e quella media
            della settimana, salva la tabella nel file `meteo.xlsx` e lo conferma con una terza riga. Vogliamo
            arrivare a questo punto e conservare nel notebook la riga della media, copiata dal terminale, come
            prova che lo script è stato eseguito.
        """,
        richiesta="""
            1. Lancia `uv add openpyxl` e poi di nuovo `uv run main.py`.
            2. Controlla che nella cartella `esercizio` sia comparso il file `meteo.xlsx`.
            3. Copia dal terminale la riga che comincia con `Temperatura media` e incollala tra le virgolette di
               `riga_media`.
        """,
        suggerimenti=[
            """
                Nel terminale di VS Code il testo si copia come in un editor, selezionandolo con il mouse e
                premendo **Ctrl+C**.
            """,
        ],
        starter="""
            riga_media = "..."
        """,
        soluzione="""
            # nel terminale, nella cartella esercizio
            #   uv add openpyxl
            #   uv run main.py
            # Temperatura massima della settimana: 16.0 gradi
            # Temperatura media della settimana: 15.0 gradi, calcolata su 5 giorni
            # La tabella delle temperature è nel file meteo.xlsx
            riga_media = "Temperatura media della settimana: 15.0 gradi, calcolata su 5 giorni"
        """,
        verifica=unisci(LEGGI_PROGETTO, """
            librerie = progetto["project"]["dependencies"]
            assert any(voce.startswith("openpyxl") for voce in librerie), "❌ openpyxl non è tra le dependencies di esercizio/pyproject.toml: lancia uv add openpyxl"
            assert riga_media.strip() == "Temperatura media della settimana: 15.0 gradi, calcolata su 5 giorni", "❌ riga_media: la riga copiata dal terminale, tale e quale"
        """),
    )

    # E1.4 ---------------------------------------------------------------
    nb.esercizio(
        titolo="Ruff trova i problemi",
        scenario="""
            Lo script funziona, ma il codice di `meteo.py` e di `main.py` è scritto in modo disordinato e contiene
            qualche avanzo. Vogliamo aggiungere Ruff al progetto come strumento di sviluppo, lasciare che il
            formatter sistemi la forma e poi leggere che cosa segnala il linter. Dopo `ruff format` il comando
            `ruff check` trova quattro problemi, due in ciascun file.
        """,
        richiesta="""
            1. Lancia `uv add --dev ruff`, che mette Ruff nel gruppo `dev` di `pyproject.toml`, tra gli strumenti
               di chi scrive il codice, e non tra le librerie che servono allo script.
            2. Lancia `uv run ruff format` e apri i due file per vedere che cosa è cambiato, per esempio gli spazi
               attorno agli operatori e le righe vuote tra le funzioni.
            3. Lancia `uv run ruff check` e scrivi in `avvisi` i codici dei quattro problemi, come stringhe.
        """,
        suggerimenti=[
            """
                Ogni avviso si apre con il suo codice, una lettera seguita da tre cifre come `F401`, e sotto
                riporta il file e la riga a cui si riferisce. La riga lunga che `ruff format` ha messo tra
                parentesi resta segnalata, perché il formatter non divide le stringhe.
            """,
        ],
        starter="""
            avvisi = [...]
        """,
        soluzione="""
            # nel terminale, nella cartella esercizio
            #   uv add --dev ruff
            #   uv run ruff format       2 files reformatted
            #   uv run ruff check
            # I001 [*] Import block is un-sorted or un-formatted         --> main.py
            # E501 Line too long (102 > 100)                             --> main.py
            # F401 [*] `math` imported but unused                        --> meteo.py
            # F841 Local variable `giorni` is assigned to but never used --> meteo.py
            avvisi = ["I001", "E501", "F401", "F841"]
        """,
        verifica=unisci(LEGGI_PROGETTO, """
            sviluppo = progetto.get("dependency-groups", {}).get("dev", [])
            assert any(voce.startswith("ruff") for voce in sviluppo), "❌ ruff non è nel gruppo dev di esercizio/pyproject.toml: lancia uv add --dev ruff"
            assert sorted(avvisi) == ["E501", "F401", "F841", "I001"], "❌ avvisi: i quattro codici stampati da uv run ruff check, come stringhe"
        """),
    )

    # E1.5 ---------------------------------------------------------------
    nb.esercizio(
        titolo="Il codice in ordine",
        scenario="""
            Dei quattro avvisi, due si correggono da soli con `ruff check --fix`, che toglie l'import inutilizzato
            e riordina gli import, mentre gli altri due richiedono una decisione nostra. Ruff non cancella la
            variabile mai usata, perché potrebbe essere il segno di un errore da capire, e non divide la stringa
            troppo lunga. Vogliamo arrivare al punto in cui `uv run ruff check` risponde `All checks passed!` e lo
            script stampa le stesse righe di prima.
        """,
        richiesta="""
            1. Lancia `uv run ruff check --fix` e guarda come sono diventati gli import di `main.py`, con prima le
               librerie installate e poi i file del progetto, separati da una riga vuota.
            2. In `meteo.py` cancella la riga `giorni = len(temperature)`.
            3. In `main.py` dividi il testo del `print` della media in due f-string scritte una dopo l'altra dentro
               le parentesi, in modo che nessuna riga superi i 100 caratteri.
            4. Lancia di nuovo `uv run ruff format`, che toglie la riga vuota rimasta al posto dell'import, e poi
               `uv run ruff check`.
            5. Scrivi in `esito_finale` la riga stampata da `ruff check`, poi lancia `uv run main.py` e controlla
               che lo script stampi le stesse righe di prima.
        """,
        suggerimenti=[
            """
                Due stringhe scritte una dopo l'altra dentro le stesse parentesi diventano una stringa sola. Il
                testo si può dividere dopo `gradi, `, lasciando lo spazio alla fine del primo pezzo, e ogni pezzo
                che contiene delle graffe ha bisogno della sua `f`.
            """,
        ],
        starter="""
            esito_finale = "..."
        """,
        soluzione="""
            # nel terminale, nella cartella esercizio
            #   uv run ruff check --fix      corregge F401 e I001
            # a mano, in meteo.py, si cancella la riga giorni = len(temperature)
            # a mano, in main.py, il print della media diventa
            #     print(
            #         f"Temperatura media della settimana: {media(valori):.1f} gradi, "
            #         f"calcolata su {len(valori)} giorni"
            #     )
            #   uv run ruff format
            #   uv run ruff check            All checks passed!
            #   uv run main.py
            esito_finale = "All checks passed!"
        """,
        verifica=f"""
            from pathlib import Path

            cartella = Path("{ESERCIZIO}")
            meteo = (cartella / "meteo.py").read_text(encoding="utf-8")
            righe_lunghe = [r for r in (cartella / "main.py").read_text(encoding="utf-8").splitlines() if len(r) > 100]
            assert esito_finale.strip() == "All checks passed!", "❌ esito_finale: la riga stampata da uv run ruff check quando non trova problemi"
            assert "import math" not in meteo and "giorni =" not in meteo and "giorni=" not in meteo, "❌ meteo.py contiene ancora import math o la variabile giorni"
            assert not righe_lunghe, "❌ main.py ha ancora una riga di più di 100 caratteri"
        """,
    )

    # Passi facoltativi ---------------------------------------------------
    nb.md("""
        I tre passi che seguono sono facoltativi e lavorano sulla stessa cartella. Il primo aggiunge una riga allo
        script, il secondo mostra che cosa fa Python quando importa un file e il terzo ricostruisce l'ambiente da
        zero, per vedere che `pyproject.toml` e `uv.lock` bastano a ricrearlo identico.
    """)

    # E1.6 ---------------------------------------------------------------
    nb.esercizio(
        titolo="La temperatura minima",
        facoltativo=True,
        scenario="""
            Il file `meteo.py` contiene anche la funzione `minima`, che `main.py` non usa. Vogliamo importarla e
            aggiungere allo script una riga con la temperatura minima della settimana, scritta come le altre con
            una cifra decimale: la riga stampata è `Temperatura minima della settimana: 13.8 gradi`.
        """,
        richiesta="""
            1. Aggiungi `minima` ai nomi importati nella riga `from meteo import` di `main.py`.
            2. Sotto il `print` della massima scrivi un `print` con una f-string che chiama `minima(valori)` con il
               formato `:.1f`.
            3. Lancia `uv run main.py` e copia la nuova riga in `riga_minima`.
            4. Lancia `uv run ruff check`; se segnala di nuovo `I001`, `uv run ruff check --fix` rimette in ordine
               alfabetico i nomi importati.
        """,
        suggerimenti=[
            """
                La riga nuova ha la stessa forma di quella della massima, con `minima` al posto di `massima`.
            """,
        ],
        starter="""
            riga_minima = "..."
        """,
        soluzione="""
            # in main.py
            #   from meteo import massima, media, minima
            #   print(f"Temperatura minima della settimana: {minima(valori):.1f} gradi")
            # nel terminale, nella cartella esercizio
            #   uv run main.py
            #   uv run ruff check            All checks passed!
            riga_minima = "Temperatura minima della settimana: 13.8 gradi"
        """,
        verifica=f"""
            from pathlib import Path

            righe = Path("{ESERCIZIO}/main.py").read_text(encoding="utf-8").splitlines()
            riga_import = next((r for r in righe if r.startswith("from meteo import")), "")
            assert "minima" in riga_import, "❌ main.py: aggiungi minima alla riga from meteo import"
            assert riga_minima.strip() == "Temperatura minima della settimana: 13.8 gradi", "❌ riga_minima: la riga stampata dal terminale, tale e quale"
        """,
    )

    # E1.7 ---------------------------------------------------------------
    nb.esercizio(
        titolo="Che cosa succede durante un import",
        facoltativo=True,
        scenario="""
            Quando `main.py` importa le funzioni di `meteo.py`, Python esegue tutto il file importato, dall'inizio
            alla fine, prima di proseguire con le righe di `main.py`. La variabile speciale `__name__`, inoltre,
            ha un valore diverso a seconda che il file venga importato o lanciato direttamente con
            `uv run meteo.py`. Vogliamo vedere entrambe le cose con una riga di prova, perché spiegano come mai
            negli script le istruzioni da eseguire si mettono sotto `if __name__ == "__main__":`.
        """,
        richiesta="""
            1. In `meteo.py`, sotto la docstring, aggiungi la riga
               `print(f"Sto leggendo meteo.py, con il nome {__name__}")`.
            2. Lancia `uv run main.py`, controlla che la nuova riga compaia prima di quelle di `main.py` e scrivi
               in `nome_importato` il nome che stampa.
            3. Lancia `uv run meteo.py` e scrivi in `nome_lanciato` il nome che stampa questa volta.
            4. Togli la riga di prova da `meteo.py`.
        """,
        starter="""
            nome_importato = "..."
            nome_lanciato = "..."
        """,
        soluzione="""
            # in meteo.py, sotto la docstring
            #   print(f"Sto leggendo meteo.py, con il nome {__name__}")
            # nel terminale, nella cartella esercizio
            #   uv run main.py     la prima riga è: Sto leggendo meteo.py, con il nome meteo
            #   uv run meteo.py    stampa: Sto leggendo meteo.py, con il nome __main__
            nome_importato = "meteo"
            nome_lanciato = "__main__"
        """,
        verifica="""
            assert nome_importato.strip() == "meteo", "❌ nome_importato: il nome stampato con uv run main.py"
            assert nome_lanciato.strip() == "__main__", "❌ nome_lanciato: il nome stampato con uv run meteo.py"
        """,
        perche="""
            Quando `main.py` lo importa, `meteo.py` ha come nome `meteo`, cioè il nome del file senza
            l'estensione, mentre lanciato con `uv run meteo.py` è il programma principale e Python lo chiama
            `__main__`. Le righe scritte sotto `if __name__ == "__main__":` vengono quindi eseguite solo quando
            il file è lanciato direttamente, e chi lo importa riceve le funzioni senza eseguire altro.
        """,
    )

    # E1.8 ---------------------------------------------------------------
    nb.esercizio(
        titolo="L'ambiente ricostruito",
        facoltativo=True,
        scenario="""
            La cartella `.venv` non si conserva e non si condivide, perché si ricrea in qualunque momento a
            partire da `pyproject.toml` e `uv.lock`, con le stesse versioni di prima. Vogliamo provarlo
            cancellando l'ambiente dell'esercizio e ricostruendolo con un solo comando, senza ripetere nessun
            `uv add`.
        """,
        richiesta="""
            1. Nel pannello Explorer di VS Code cancella la cartella `.venv` dentro `esercizio`, con il tasto destro
               e la voce **Delete**.
            2. Lancia `uv sync`, che crea di nuovo `.venv` e installa le stesse librerie, Ruff compreso, di solito
               in pochi secondi, perché uv tiene una copia delle librerie già scaricate.
            3. Lancia `uv run main.py` e controlla che lo script funzioni come prima.
            4. Scrivi in `file_versioni` il nome del file da cui `uv sync` legge le versioni esatte da installare.
        """,
        starter="""
            file_versioni = "..."
        """,
        soluzione="""
            # nel pannello Explorer: tasto destro su esercizio/.venv, Delete
            # nel terminale, nella cartella esercizio
            #   uv sync           Creating virtual environment at: .venv, poi installa le stesse librerie
            #   uv run main.py
            file_versioni = "uv.lock"
        """,
        verifica="""
            assert file_versioni.strip() == "uv.lock", "❌ file_versioni: il file in cui uv registra le versioni esatte di ogni libreria"
        """,
    )


def costruisci() -> Notebook:
    nb = Notebook(
        num="E1",
        file="Esercitazione_1",
        titolo="Esercitazione 1",
        blocco=1,
        giornata=1,
        intento=(
            "Un'ora di domande ed esercizi sui notebook 00-03: numeri, stringhe, liste e dizionari. Nell'Avanzata "
            "l'ora serve a rifare la demo dello script con uv e Ruff, e gli esercizi sui notebook 00-03 restano "
            "facoltativi, da fare a casa."
        ),
        obiettivi={
            "base": [
                "usare le funzioni di Python sui numeri e stampare i risultati con le f-string",
                "selezionare parti di una lista con lo slicing",
                "aggiungere coppie a un dizionario e leggerne i valori",
            ],
            "avanzata": [
                "costruire l'ambiente di un progetto con `uv add`, aggiungendo una libreria alla volta quando manca",
                "lanciare con `uv run` uno script che importa le sue funzioni da un altro file",
                "rimettere in forma il codice con `ruff format` e correggere gli avvisi di `ruff check`",
            ],
        },
        tempo=60,
        dati=[],
        soluzioni_a_richiesta=True,
    )

    # ------------------------------------------------------------------ come funziona l'ora
    nb.md("""
        Questa esercitazione chiude la giornata e riprende quello che abbiamo visto nei notebook 00-03. Hai 45
        minuti per lavorare sugli esercizi, poi li guardiamo insieme. Si comincia con quattro domande di riepilogo e
        si prosegue con cinque esercizi brevi, ciascuno con i propri dati, da fare nell'ordine perché la difficoltà
        cresce; in fondo c'è una sfida libera, senza verifica, per il tempo che resta.
    """, aula="base")
    aiuti = """
        Ogni esercizio comincia dicendo che cosa vogliamo ottenere e perché, e da lì si può arrivare al risultato da
        soli. Chi preferisce procedere per gradi apre con un clic il blocco Passo per passo, e sotto {aiuti}, da
        leggere solo dopo aver provato. Sotto la cella da completare ci sono la verifica, che conferma il risultato o
        dice che cosa controllare, e la cella `soluzione`, che mostra soltanto la soluzione di quell'esercizio.
    """
    nb.md(aiuti.replace("{aiuti}", "due suggerimenti, anche loro nascosti"), aula="base")

    # ------------------------------------------------------------------ Avanzata: lo script, poi il ripasso a casa
    with nb.solo("avanzata"):
        parte_script(nb)

    # ------------------------------------------------------------------ 1. Domande (Avanzata: 3.1, a casa)
    nb.sezione("Domande", aula="base", intro="""
        Le quattro domande che seguono riguardano i notebook 00-03 e richiedono pochi minuti. Per ciascuna conviene
        prevedere la risposta a mente e solo dopo aprirla con un clic. In caso di dubbio si può provare la riga in
        una cella di codice e, se il risultato sorprende, rileggere la parte del notebook che tratta quell'argomento.
    """)
    with nb.solo("avanzata"):
        nb.sezione("Esercizi sui notebook 00-03, da fare a casa", intro="""
            Questa seconda parte è facoltativa e si fa a casa, per ripassare i numeri, le stringhe, le liste e i
            dizionari dei notebook 00-03. Comincia con quattro domande di riepilogo e prosegue con cinque esercizi
            brevi, in difficoltà crescente, e con una sfida libera senza verifica. Gli esercizi funzionano come i
            passi della prima parte, con il blocco Passo per passo e il suggerimento che si aprono con un clic, la
            verifica e la cella `soluzione`, ma il codice si scrive direttamente nella cella del notebook.
        """)
        nb.sottosezione("Domande", intro="""
            Per ciascuna delle quattro domande conviene prevedere la risposta a mente e solo dopo aprirla con un
            clic. In caso di dubbio si può provare la riga in una cella di codice e, se il risultato sorprende,
            rileggere la parte del notebook che tratta quell'argomento.
        """)
    nb.domanda(
        "Cosa restituisce `17 // 5`, e cosa restituisce `17 % 5`?",
        """
            `17 // 5` restituisce `3`, perché la divisione intera tiene soltanto la parte intera del quoziente 3.4,
            e `17 % 5` restituisce `2`, il resto della stessa divisione.
        """,
    )
    nb.domanda(
        'Con `numeri = [3, 6, 9, 12, 15]`, cosa restituisce `numeri[1:3]`?',
        """
            Restituisce `[6, 9]`. Lo slicing parte dall'indice 1 e si ferma prima dell'indice 3, quindi prende il
            secondo e il terzo elemento.
        """,
    )
    nb.domanda(
        'Con `punto = (45.46, 9.19)`, cosa succede se eseguiamo `punto[0] = 45.5`?',
        """
            Python solleva un `TypeError`, perché le tuple sono immutabili e non permettono di sostituire un
            elemento dopo la creazione. Per cambiare una coordinata si crea una tupla nuova.
        """,
    )
    nb.domanda(
        'Con `capitali = {"Italia": "Roma", "Francia": "Parigi"}`, cosa restituisce `capitali["Italia"]` e cosa fa `capitali["Spagna"] = "Madrid"`?',
        """
            `capitali["Italia"]` restituisce `"Roma"`, il valore associato a quella chiave. L'assegnazione a una
            chiave che non esiste aggiunge la coppia al dizionario, che dopo ha tre elementi.
        """,
    )

    # ------------------------------------------------------------------ 2. Esercizi (Avanzata: 3.2, a casa)
    nb.sezione("Esercizi", aula="base", intro="""
        I cinque esercizi ripercorrono i numeri, le stringhe e le strutture dati dei notebook 01 e 02. Ognuno lavora
        sui dati scritti nella propria cella, quindi si può affrontare anche senza aver risolto i precedenti, e sono
        quelli che guardiamo insieme alla fine dell'ora.
    """)
    nb.sottosezione("Esercizi", aula="avanzata", intro="""
        I cinque esercizi ripercorrono i numeri, le stringhe e le strutture dati dei notebook 01 e 02. Ognuno lavora
        sui dati scritti nella propria cella, quindi si può affrontare anche senza aver risolto i precedenti. La
        sfida in fondo non ha una verifica, perché la forma della frase da stampare è libera.
    """)

    # E1.1 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Massimo, minimo e differenza",
        scenario="""
            Nella cella sono definite tre variabili numeriche. Vogliamo trovare il valore massimo, il valore minimo e
            la differenza tra i due, e stampare i tre risultati con una f-string ciascuno. Con i valori della cella
            il massimo è 25, il minimo 7 e la differenza 18.
        """,
        base=dict(
            richiesta="""
                1. Salva in `valore_massimo` il più grande dei tre numeri e in `valore_minimo` il più piccolo,
                   con le funzioni `max()` e `min()`, che abbiamo incontrato nella cella su PEP 8 del notebook 03.
                2. Salva in `differenza` la differenza tra massimo e minimo.
                3. Completa i tre `print`, in modo che stampino le righe indicate nei commenti.
            """,
            suggerimenti=[
                """
                    Le funzioni `max()` e `min()` accettano più argomenti separati da virgola e restituiscono il più
                    grande e il più piccolo.
                """,
                """
                    Servono `max(a, b, c)`, `min(a, b, c)` e `valore_massimo - valore_minimo`; nei `print` il nome
                    della variabile va tra graffe dentro la f-string.
                """,
            ],
            starter="""
                # Definizione delle variabili
                a = 10
                b = 25
                c = 7

                # Calcolo del massimo e del minimo
                valore_massimo = max(...)
                valore_minimo = ...
                differenza = ...

                # Stampa dei risultati
                print(f"Valore massimo: {valore_massimo}")   # Output: Valore massimo: 25
                print(f"Valore minimo: {...}")               # Output: Valore minimo: 7
                print(...)                                   # Output: Differenza: 18
            """,
            soluzione="""
                # Definizione delle variabili
                a = 10
                b = 25
                c = 7

                # Calcolo del massimo e del minimo
                valore_massimo = max(a, b, c)
                valore_minimo = min(a, b, c)
                differenza = valore_massimo - valore_minimo

                # Stampa dei risultati
                print(f"Valore massimo: {valore_massimo}")   # Output: Valore massimo: 25
                print(f"Valore minimo: {valore_minimo}")     # Output: Valore minimo: 7
                print(f"Differenza: {differenza}")           # Output: Differenza: 18
            """,
            verifica="""
                assert valore_massimo == 25 and valore_minimo == 7, "❌ valore_massimo e valore_minimo: usa max() e min() sui tre numeri"
                assert differenza == 18, "❌ differenza: massimo meno minimo"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `valore_massimo` e `valore_minimo` il più grande e il più piccolo dei tre numeri, con
                   `max()` e `min()`, e in
                   `differenza` la loro differenza.
                2. Salva in `media` la media dei tre numeri, arrotondata a un decimale con `round()`.
                3. Stampa i quattro risultati, uno per riga, con le f-string.

                La media vale 14.0.
            """,
            suggerimenti=[
                """
                    `max()` e `min()` accettano più argomenti separati da virgola; la media è la somma dei tre numeri
                    divisa per 3, e `round(valore, 1)` la arrotonda a un decimale.
                """,
            ],
            starter="""
                a = 10
                b = 25
                c = 7

                # da creare: valore_massimo, valore_minimo, differenza, media
            """,
            soluzione="""
                a = 10
                b = 25
                c = 7

                valore_massimo = max(a, b, c)
                valore_minimo = min(a, b, c)
                differenza = valore_massimo - valore_minimo
                media = round((a + b + c) / 3, 1)

                print(f"Valore massimo: {valore_massimo}")   # Output: Valore massimo: 25
                print(f"Valore minimo: {valore_minimo}")     # Output: Valore minimo: 7
                print(f"Differenza: {differenza}")           # Output: Differenza: 18
                print(f"Media: {media}")                     # Output: Media: 14.0
            """,
            verifica="""
                assert valore_massimo == 25 and valore_minimo == 7 and differenza == 18, "❌ Controlla max(), min() e la differenza"
                assert media == 14.0, "❌ media: (a + b + c) / 3, arrotondata con round(..., 1)"
            """,
        ),
    )

    # E1.2 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="L'area del cerchio",
        scenario="""
            Vogliamo calcolare l'area di un cerchio di raggio 5 e stampare il risultato. L'area è π moltiplicato per
            il raggio al quadrato, e il valore di π lo fornisce il modulo `math`, con `math.pi`. Il risultato è
            78.53981633974483.
        """,
        base=dict(
            richiesta="""
                1. Salva in `area` il prodotto tra `math.pi` e il raggio al quadrato.
                2. Completa il `print` con una f-string che stampi `L'area del cerchio è: 78.53981633974483`.
            """,
            suggerimenti=[
                """
                    Il quadrato si scrive con l'operatore `**`, come in `raggio ** 2`, oppure moltiplicando il
                    raggio per se stesso.
                """,
                """
                    La riga è `area = math.pi * raggio ** 2`, e nella f-string la variabile va tra graffe:
                    `f"L'area del cerchio è: {area}"`.
                """,
            ],
            starter="""
                import math

                raggio = 5
                area = ...

                print(...)  # Output: L'area del cerchio è: 78.53981633974483
            """,
            soluzione="""
                import math

                raggio = 5
                area = math.pi * raggio ** 2

                print(f"L'area del cerchio è: {area}")  # Output: L'area del cerchio è: 78.53981633974483
            """,
            verifica="""
                assert round(area, 6) == 78.539816, "❌ area: math.pi moltiplicato per raggio ** 2"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `area` il prodotto tra `math.pi` e il raggio al quadrato.
                2. Stampa l'area con una f-string che la mostri con due decimali, usando il formato `{area:.2f}`:
                   la riga stampata è `L'area del cerchio è: 78.54`.
                3. Salva in `circonferenza` il doppio di π per il raggio, cioè 31.41592653589793.
            """,
            suggerimenti=[
                """
                    Dentro le graffe di una f-string, dopo il nome della variabile, `:.2f` chiede due cifre
                    decimali; il valore di `area` non cambia, cambia soltanto come viene stampato.
                """,
            ],
            starter="""
                import math

                raggio = 5

                # da creare: area, circonferenza; stampa l'area con due decimali
            """,
            soluzione="""
                import math

                raggio = 5
                area = math.pi * raggio ** 2
                circonferenza = 2 * math.pi * raggio

                print(f"L'area del cerchio è: {area:.2f}")   # Output: L'area del cerchio è: 78.54
                print(circonferenza)                          # Output: 31.41592653589793
            """,
            verifica="""
                assert round(area, 6) == 78.539816, "❌ area: math.pi moltiplicato per raggio ** 2"
                assert round(circonferenza, 6) == 31.415927, "❌ circonferenza: 2 * math.pi * raggio"
            """,
        ),
    )

    # E1.3 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Lista invertita",
        scenario="""
            Vogliamo invertire l'ordine di una lista di numeri con lo slicing, senza riscrivere gli elementi a mano.
            La lista di partenza è `[1, 2, 3, 4, 5]` e il risultato è `[5, 4, 3, 2, 1]`.
        """,
        base=dict(
            richiesta="""
                1. Salva in `lista_invertita` la lista letta al contrario, con uno slicing a passo negativo.
                2. Stampa `lista_invertita`.
            """,
            suggerimenti=[
                """
                    Lo slicing ha tre parti, `[inizio:fine:passo]`, e il passo può essere negativo: in quel caso la
                    lista viene letta dall'ultimo elemento al primo.
                """,
                """
                    Con inizio e fine vuoti e passo `-1`, cioè `lista[::-1]`, si ottiene tutta la lista al contrario.
                """,
            ],
            starter="""
                lista = [1, 2, 3, 4, 5]

                # Scrivi il tuo codice qui
                lista_invertita = lista[...]
                print(lista_invertita)  # Output: [5, 4, 3, 2, 1]
            """,
            soluzione="""
                lista = [1, 2, 3, 4, 5]

                lista_invertita = lista[::-1]
                print(lista_invertita)  # Output: [5, 4, 3, 2, 1]
            """,
            verifica="""
                assert lista_invertita == [5, 4, 3, 2, 1], "❌ lista_invertita: slicing con passo -1, cioè lista[::-1]"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `lista_invertita` la lista letta al contrario, con uno slicing a passo negativo.
                2. Salva in `ultimi_due` gli ultimi due elementi della lista di partenza, con uno slicing che usa un
                   indice negativo, e in `ogni_due` gli elementi di posizione pari, cioè `[1, 3, 5]`.

                `ultimi_due` vale `[4, 5]`.
            """,
            suggerimenti=[
                """
                    Un indice negativo conta dalla fine, quindi `lista[-2:]` parte dal penultimo elemento; il passo
                    `2` prende un elemento ogni due.
                """,
            ],
            starter="""
                lista = [1, 2, 3, 4, 5]

                # da creare: lista_invertita, ultimi_due, ogni_due
            """,
            soluzione="""
                lista = [1, 2, 3, 4, 5]

                lista_invertita = lista[::-1]
                ultimi_due = lista[-2:]
                ogni_due = lista[::2]

                print(lista_invertita)  # Output: [5, 4, 3, 2, 1]
                print(ultimi_due, ogni_due)  # Output: [4, 5] [1, 3, 5]
            """,
            verifica="""
                assert lista_invertita == [5, 4, 3, 2, 1], "❌ lista_invertita: slicing con passo -1"
                assert ultimi_due == [4, 5] and ogni_due == [1, 3, 5], "❌ ultimi_due è lista[-2:] e ogni_due è lista[::2]"
            """,
        ),
    )

    # E1.4 ---------------------------------------------------------------
    esercizio_due_aule(
        nb,
        titolo="Posizioni pari",
        scenario="""
            La lista della cella alterna nomi di donne e di uomini, a partire da Elena. Vogliamo selezionare con un
            solo slicing gli elementi in posizione pari escludendo la posizione 0, cioè tutte le donne tranne Elena.
            Il risultato è `['Martina', 'Giulia', 'Francesca', 'Sara']`.
        """,
        base=dict(
            richiesta="""
                1. Salva in `elementi_pari` gli elementi dalla posizione 2 in avanti, uno ogni due.
                2. Stampa `elementi_pari`.
            """,
            suggerimenti=[
                """
                    Lo slicing `[inizio::passo]` parte dall'indice indicato e salta `passo` elementi alla volta fino
                    alla fine della lista.
                """,
                """
                    Serve `lista[2::2]`: inizio 2 per saltare Elena e Luigi, passo 2 per prendere un nome ogni due.
                """,
            ],
            starter="""
                lista = ["Elena", "Luigi", "Martina", "Marco", "Giulia", "Simone", "Francesca", "Alessandro", "Sara", "Lorenzo"]

                # Scrivi il tuo codice qui
                elementi_pari = lista[...]
                print(elementi_pari)  # Output: ['Martina', 'Giulia', 'Francesca', 'Sara']
            """,
            soluzione="""
                lista = ["Elena", "Luigi", "Martina", "Marco", "Giulia", "Simone", "Francesca", "Alessandro", "Sara", "Lorenzo"]

                elementi_pari = lista[2::2]
                print(elementi_pari)  # Output: ['Martina', 'Giulia', 'Francesca', 'Sara']
            """,
            verifica="""
                assert elementi_pari == ["Martina", "Giulia", "Francesca", "Sara"], "❌ elementi_pari: slicing dalla posizione 2 con passo 2, cioè lista[2::2]"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Salva in `elementi_pari` gli elementi in posizione pari escludendo la posizione 0.
                2. Salva in `uomini` gli elementi in posizione impari, cioè `['Luigi', 'Marco', 'Simone',
                   'Alessandro', 'Lorenzo']`, e in `quanti_uomini` quanti sono.
            """,
            suggerimenti=[
                """
                    Le posizioni impari si prendono partendo dall'indice 1 con passo 2, e `len()` conta gli
                    elementi di una lista.
                """,
            ],
            starter="""
                lista = ["Elena", "Luigi", "Martina", "Marco", "Giulia", "Simone", "Francesca", "Alessandro", "Sara", "Lorenzo"]

                # da creare: elementi_pari, uomini, quanti_uomini
            """,
            soluzione="""
                lista = ["Elena", "Luigi", "Martina", "Marco", "Giulia", "Simone", "Francesca", "Alessandro", "Sara", "Lorenzo"]

                elementi_pari = lista[2::2]
                uomini = lista[1::2]
                quanti_uomini = len(uomini)

                print(elementi_pari)  # Output: ['Martina', 'Giulia', 'Francesca', 'Sara']
                print(uomini, quanti_uomini)  # Output: ['Luigi', 'Marco', 'Simone', 'Alessandro', 'Lorenzo'] 5
            """,
            verifica="""
                assert elementi_pari == ["Martina", "Giulia", "Francesca", "Sara"], "❌ elementi_pari: lista[2::2]"
                assert uomini == ["Luigi", "Marco", "Simone", "Alessandro", "Lorenzo"] and quanti_uomini == 5, "❌ uomini è lista[1::2] e quanti_uomini è len(uomini)"
            """,
        ),
    )

    # E1.5 ---------------------------------------------------------------
    g8_cella = """
        g8 = {
            'Canada': 'Ottawa',
            'Francia': 'Parigi',
            'Germania': 'Berlino',
            'Italia': 'Roma',
            'Giappone': 'Tokyo',
            'Russia': 'Mosca'
        }
    """
    esercizio_due_aule(
        nb,
        titolo="Le capitali del G8",
        scenario="""
            Il dizionario `g8` associa ai paesi del G8 la loro capitale, ma è incompleto: mancano `'Regno Unito'`
            con `'Londra'` e `'Stati Uniti'` con `'Washington, D.C.'`. Vogliamo aggiungere le due coppie e, alla
            fine, avere un dizionario con otto paesi.
        """,
        base=dict(
            richiesta="""
                1. Aggiungi la coppia `'Regno Unito': 'Londra'`, assegnando il valore alla chiave nuova.
                2. Aggiungi nello stesso modo `'Stati Uniti': 'Washington, D.C.'`.
                3. Stampa il dizionario.
            """,
            suggerimenti=[
                """
                    Per aggiungere una coppia a un dizionario si assegna un valore a una chiave che ancora non
                    esiste, con la stessa sintassi con cui si legge un valore.
                """,
                """
                    Le due righe hanno la forma `g8['Regno Unito'] = 'Londra'`.
                """,
            ],
            starter=unisci(g8_cella, """
                # Aggiungi i paesi mancanti
                g8[...] = 'Londra'
                g8...

                print(g8)
            """),
            soluzione=unisci(g8_cella, """
                # Aggiungi i paesi mancanti
                g8['Regno Unito'] = 'Londra'
                g8['Stati Uniti'] = 'Washington, D.C.'

                print(g8)
            """),
            verifica="""
                assert g8.get('Regno Unito') == 'Londra' and g8.get('Stati Uniti') == 'Washington, D.C.', "❌ Aggiungi le due coppie con g8[chiave] = valore"
                assert len(g8) == 8, "❌ Alla fine il dizionario ha otto paesi"
            """,
        ),
        avanzata=dict(
            richiesta="""
                1. Aggiungi le coppie `'Regno Unito': 'Londra'` e `'Stati Uniti': 'Washington, D.C.'`.
                2. Salva in `quanti` il numero di paesi e in `capitale_italia` la capitale dell'Italia, letta dal
                   dizionario con la sua chiave.
                3. Salva in `paesi` la lista dei paesi in ordine alfabetico, usando `sorted()` sulle chiavi.

                `quanti` vale 8 e `paesi` comincia con `'Canada'` e finisce con `'Stati Uniti'`.
            """,
            suggerimenti=[
                """
                    `len()` conta le coppie di un dizionario, `g8['Italia']` legge un valore dalla sua chiave e
                    `sorted(g8.keys())` restituisce le chiavi in ordine alfabetico come lista.
                """,
            ],
            starter=unisci(g8_cella, """
                # da creare: quanti, capitale_italia, paesi (prima completa il dizionario)
            """),
            soluzione=unisci(g8_cella, """
                g8['Regno Unito'] = 'Londra'
                g8['Stati Uniti'] = 'Washington, D.C.'

                quanti = len(g8)
                capitale_italia = g8['Italia']
                paesi = sorted(g8.keys())

                print(quanti, capitale_italia)  # Output: 8 Roma
                print(paesi)
            """),
            verifica="""
                assert g8.get('Regno Unito') == 'Londra' and g8.get('Stati Uniti') == 'Washington, D.C.', "❌ Aggiungi le due coppie con g8[chiave] = valore"
                assert quanti == 8 and capitale_italia == 'Roma', "❌ quanti è len(g8) e capitale_italia è g8['Italia']"
                assert paesi[0] == 'Canada' and paesi[-1] == 'Stati Uniti', "❌ paesi: sorted(g8.keys())"
            """,
        ),
    )

    # Sfida ---------------------------------------------------------------
    nb.esercizio(
        titolo="Sfida: una riga sul G8",
        facoltativo=True,
        scenario="""
            Partendo dal dizionario `g8` completo, vogliamo stampare una frase come `Il G8 ha 8 paesi e la capitale
            del Giappone è Tokyo`, in cui il numero di paesi e la capitale vengono letti dal dizionario e non scritti
            a mano, così la frase resta giusta se il dizionario cambia. La forma della frase è libera, quindi
            l'esercizio non ha una verifica e la cella `soluzione` mostra un esempio.
        """,
        richiesta="""
            1. Componi la frase con una f-string, mettendo tra graffe `len(g8)` e il valore letto con la chiave del
               paese che preferisci.
            2. Cambia il paese e riesegui la cella.
        """,
        suggerimenti=[
            """
                Dentro le graffe di una f-string può stare un'espressione qualunque, oltre al nome di una
                variabile: `{len(g8)}` e `{g8['Giappone']}` funzionano.
            """,
        ],
        starter=unisci(g8_cella, """
            g8['Regno Unito'] = 'Londra'
            g8['Stati Uniti'] = 'Washington, D.C.'

            print(f"...")
        """),
        soluzione=unisci(g8_cella, """
            g8['Regno Unito'] = 'Londra'
            g8['Stati Uniti'] = 'Washington, D.C.'

            print(f"Il G8 ha {len(g8)} paesi e la capitale del Giappone è {g8['Giappone']}")
        """),
        verifica=None,
    )
    return nb
