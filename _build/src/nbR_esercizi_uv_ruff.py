"""R · Esercizi su uv, script e Ruff (riserva, solo aula Avanzata).

Gli Hands-on e gli esercizi Extra che stavano nel notebook `Ambiente_script_e_Ruff`, tolti da lì per decisione del
docente e raccolti come riserva in `Riserva/Avanzata/`. Il notebook non legge file con percorsi relativi, perché
nel repository sta in `Riserva/Avanzata/` e, se usato, verrebbe copiato nella cartella del corsista: i due esercizi
con un file da creare lo fanno nella cartella del corso, accanto a `pyproject.toml`, dove si apre il terminale.
"""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="R",
        file="Esercizi_uv_script_Ruff",
        titolo="Esercizi su uv, script e Ruff",
        blocco=0,
        giornata=0,
        riserva=True,
        aule=("avanzata",),
        intento=(
            "Il notebook raccoglie sei esercizi brevi sui temi del notebook Ambiente, script e Ruff: i file che "
            "descrivono un progetto, i comandi di uv, gli script lanciati con `uv run` e le segnalazioni di Ruff."
        ),
        obiettivi=[
            "leggere `pyproject.toml` da Python e scegliere il comando di uv adatto a ogni situazione",
            "scrivere uno script con il blocco `if __name__ == \"__main__\":` e lanciarlo con `uv run`",
            "riconoscere le segnalazioni di Ruff e correggere a mano quelle che `--fix` non sistema",
        ],
        tempo=40,
        dati=[],
        soluzioni_a_richiesta=True,
    )

    nb.sezione("Esercizi", intro="""
        Questo notebook raccoglie sei esercizi brevi sui temi del notebook *Ambiente, script e Ruff*, che si
        trova nella cartella `Modulo_1/Script_uv_Ruff` del corso. Gli esercizi sono indipendenti e si possono
        fare in qualunque ordine. L'esercizio R.4 chiede di creare un file nella cartella del corso, cioè
        quella che contiene `pyproject.toml` e che apriamo in VS Code, e di lanciarlo dal terminale, che si
        apre proprio in quella cartella. L'esercizio R.6 propone lo stesso passaggio, facoltativo, per
        controllare la risposta con Ruff.
    """)
    nb.md("""
        Ogni esercizio comincia dicendo che cosa vogliamo ottenere, e da lì puoi arrivare al risultato da
        solo; se preferisci procedere per gradi, apri con un clic il blocco Passo per passo. Nella cella da
        completare i `...` prendono il posto del codice da scrivere. Sotto ci sono la verifica, che stampa ✅
        quando il risultato è giusto e altrimenti dice che cosa controllare, e la cella `soluzione`, che mostra
        soltanto la soluzione di quell'esercizio.
    """)

    # ------------------------------------------------------------------ uv e il progetto
    nb.sottosezione("uv e i file del progetto", intro="""
        I primi due esercizi riguardano il file `pyproject.toml` e i comandi con cui uv aggiunge una libreria a
        un progetto e con cui un collega la riceve sul suo PC.
    """)
    nb.esercizio(
        titolo="Le librerie di un progetto",
        scenario="""
            Un collega ti ha incollato in un messaggio il contenuto del file `pyproject.toml` del progetto con
            cui prepara ogni mese il riepilogo e il grafico delle spese di casa. Prima di scaricare il progetto
            e lanciare `uv sync` vuoi sapere quali librerie installerà e quali strumenti di sviluppo usa.
            Invece di cercarle a occhio, conviene trasformare il testo in un dizionario con `tomllib.loads`,
            come nel notebook *Ambiente, script e Ruff*, in modo che la stessa cella funzioni con il
            `pyproject.toml` di qualunque altro progetto. Alla fine `librerie` contiene la lista delle tre
            librerie del programma e `strumenti` la lista con la sola voce di Ruff.
        """,
        richiesta="""
            1. Trasforma la stringa `testo` nel dizionario `progetto` con la funzione `tomllib.loads`.
            2. Metti in `librerie` la lista che sta alla voce `dependencies` della sezione `[project]`.
            3. Metti in `strumenti` la lista che sta alla voce `dev` della sezione `[dependency-groups]`.
        """,
        suggerimento=(
            'ogni sezione del file diventa una chiave del dizionario, quindi ogni lista si legge con due chiavi '
            'di fila, come `progetto["project"]["name"]` per il nome del progetto.'
        ),
        starter='''
            import tomllib

            testo = """
            [project]
            name = "spese-di-casa"
            version = "0.1.0"
            requires-python = ">=3.12"
            dependencies = ["openpyxl>=3.1.5", "pandas>=3.0.6", "plotly>=6.0"]

            [dependency-groups]
            dev = ["ruff>=0.17.1"]
            """

            progetto = ...
            librerie = ...
            strumenti = ...
            print(librerie)
            print(strumenti)
        ''',
        soluzione='''
            import tomllib

            testo = """
            [project]
            name = "spese-di-casa"
            version = "0.1.0"
            requires-python = ">=3.12"
            dependencies = ["openpyxl>=3.1.5", "pandas>=3.0.6", "plotly>=6.0"]

            [dependency-groups]
            dev = ["ruff>=0.17.1"]
            """

            progetto = tomllib.loads(testo)
            librerie = progetto["project"]["dependencies"]
            strumenti = progetto["dependency-groups"]["dev"]
            print(librerie)  # Output: ['openpyxl>=3.1.5', 'pandas>=3.0.6', 'plotly>=6.0']
            print(strumenti)  # Output: ['ruff>=0.17.1']
        ''',
        verifica="""
            assert isinstance(progetto, dict), "❌ progetto: il dizionario restituito da tomllib.loads(testo)"
            assert librerie == ["openpyxl>=3.1.5", "pandas>=3.0.6", "plotly>=6.0"], "❌ librerie: prima la chiave 'project', poi 'dependencies'"
            assert strumenti == ["ruff>=0.17.1"], "❌ strumenti: prima la chiave 'dependency-groups', poi 'dev'"
        """,
        perche=(
            "La funzione `tomllib.loads` trasforma il testo in un dizionario con una chiave per sezione, e le voci "
            "di ogni sezione diventano le chiavi del dizionario interno. Per leggere un file `pyproject.toml` dal "
            "disco si passa a `tomllib.loads` il testo restituito da `read_text`, come nel notebook "
            "*Ambiente, script e Ruff*."
        ),
    )
    nb.esercizio(
        titolo="La libreria che manca",
        scenario="""
            Un collega, prima di andare in ferie, ti ha lasciato un notebook che disegna alcuni grafici con
            Plotly e altri con matplotlib, una libreria che aveva installato con `pip install` e che per questo
            nel progetto del corso non c'è. Vogliamo controllare che Plotly sia installato, sapere con quale
            comando si aggiunge matplotlib e lasciare scritto al collega il comando con cui, al rientro,
            riceverà la libreria. Alla fine `versione_plotly` contiene
            la versione installata di Plotly, una stringa di numeri separati da punti, e `comando_aggiungi` e
            `comando_collega` contengono i due comandi di uv, scritti come nel terminale.
        """,
        richiesta="""
            1. Importa `plotly` e metti in `versione_plotly` il valore del suo attributo `__version__`, come
               abbiamo fatto con `np.__version__` nel notebook 01.
            2. Metti in `comando_aggiungi` il comando del terminale che aggiunge `matplotlib` al progetto. Non
               serve lanciarlo, perché l'esercizio chiede soltanto di scriverlo.
            3. Metti in `comando_collega` il comando che il collega lancia per ricevere la libreria aggiunta.
        """,
        suggerimento=(
            "i due comandi sono nella sezione *Aggiungere e togliere librerie* del notebook "
            "*Ambiente, script e Ruff*, e si scrivono tutti in minuscolo."
        ),
        starter="""
            import ...

            versione_plotly = ...
            comando_aggiungi = "..."
            comando_collega = "..."

            print(versione_plotly, comando_aggiungi, comando_collega)
        """,
        soluzione="""
            import plotly

            versione_plotly = plotly.__version__
            comando_aggiungi = "uv add matplotlib"
            comando_collega = "uv sync"

            print(versione_plotly, comando_aggiungi, comando_collega)
        """,
        verifica="""
            import plotly

            assert versione_plotly == plotly.__version__, "❌ versione_plotly: l'attributo __version__ della libreria plotly"
            assert comando_aggiungi.strip() == "uv add matplotlib", "❌ comando_aggiungi: il comando uv che aggiunge una libreria, seguito dal nome"
            assert comando_collega.strip() == "uv sync", "❌ comando_collega: il comando uv che ricrea l'ambiente dai file del progetto"
        """,
        perche=(
            "Chi aggiunge una libreria usa `uv add`, che aggiorna `pyproject.toml` e `uv.lock`; chi riceve il "
            "progetto aggiornato usa `uv sync`, che legge quei due file e installa quello che manca."
        ),
    )

    # ------------------------------------------------------------------ script
    nb.sottosezione("Gli script", intro="""
        Gli esercizi seguenti riguardano il blocco `if __name__ == "__main__":` e il passaggio da una cella a
        uno script lanciato dal terminale con `uv run`.
    """)
    nb.esercizio(
        titolo="Il programma principale",
        scenario="""
            La cella contiene il codice del file `spesa.py`, cioè la funzione `totale` e le righe che stampano
            il totale di uno scontrino. Vogliamo che quelle righe vengano eseguite quando lanciamo il file con
            `uv run spesa.py`, ma non quando un altro file lo importa con `import spesa` per usare soltanto la
            funzione. Il blocco `if` che separa i due casi c'è già, con la condizione da completare. Quando la
            condizione è giusta la cella stampa `Totale della spesa: 27.30 euro`, perché per Python anche il
            notebook è il programma principale.
        """,
        richiesta="""
            1. Al posto dei `...` nella condizione scrivi il nome che Python dà al programma lanciato.
            2. Metti in `nome_importato` il valore che `__name__` avrebbe dentro `spesa.py` se il file venisse
               importato da `main.py` con `import spesa`.
        """,
        suggerimento=(
            "i due nomi sono nella sezione *Importare una funzione da un altro file* del notebook "
            "*Ambiente, script e Ruff*: il primo è lo stesso per ogni programma lanciato, il secondo è il nome "
            "del modulo."
        ),
        starter='''
            def totale(prezzi):
                """Somma dei prezzi di una lista di prodotti."""
                return sum(prezzi)


            if __name__ == "...":
                scontrino = [3.5, 2.2, 4.8, 1.9, 14.9]
                riga = f"Totale della spesa: {totale(scontrino):.2f} euro"
                print(riga)

            nome_importato = "..."
        ''',
        soluzione='''
            def totale(prezzi):
                """Somma dei prezzi di una lista di prodotti."""
                return sum(prezzi)


            if __name__ == "__main__":
                scontrino = [3.5, 2.2, 4.8, 1.9, 14.9]
                riga = f"Totale della spesa: {totale(scontrino):.2f} euro"
                print(riga)  # Output: Totale della spesa: 27.30 euro

            nome_importato = "spesa"
        ''',
        verifica="""
            assert "riga" in globals(), "❌ il blocco if non è stato eseguito: la condizione confronta __name__ con il nome del programma lanciato"
            assert riga == "Totale della spesa: 27.30 euro", "❌ riga: il testo stampato dal blocco if"
            assert nome_importato == "spesa", "❌ nome_importato: in un file importato __name__ è il nome del modulo, cioè il nome del file senza .py"
        """,
        perche=(
            "Nel file lanciato, e anche nel notebook, `__name__` vale `\"__main__\"`, quindi il blocco viene "
            "eseguito. Nel file importato con `import spesa` vale invece `\"spesa\"`, il blocco viene saltato e "
            "chi importa riceve soltanto la funzione `totale`."
        ),
    )
    nb.esercizio(
        titolo="Da notebook a script",
        scenario="""
            Vai al lavoro in bicicletta e ogni sera annoti i chilometri percorsi. Il venerdì vuoi conoscere la
            media della settimana con un solo comando nel terminale, senza aprire un notebook. I chilometri di
            questa settimana sono `12.5, 8.0, 15.2, 9.8, 11.5`, e lo script `bici.py`, lanciato con `uv run`,
            stampa la riga `Media della settimana: 11.4 km`. Per controllare che lo script sia stato eseguito,
            copia nel notebook la riga che compare nel terminale.
        """,
        richiesta="""
            1. Crea in VS Code il file `bici.py` nella cartella del corso, accanto a `pyproject.toml`, che è anche
               la cartella in cui si apre il terminale.
            2. Scrivi nel file una funzione `media(valori)`, con una docstring, che restituisce
               `sum(valori) / len(valori)`.
            3. Sotto la funzione, dentro un blocco `if __name__ == "__main__":`, scrivi la lista `chilometri` e
               un `print` con una f-string che stampa la media con una cifra decimale.
            4. Lancia lo script dal terminale con `uv run bici.py`, e controlla il file con
               `uv run ruff check bici.py`, che risponde `All checks passed!` quando non c'è nulla da segnalare.
               Se Ruff segnala `W292`, al file manca l'a capo dopo l'ultima riga, e basta aggiungerlo e
               salvare. Con le impostazioni di VS Code della cartella del corso l'a capo si aggiunge da solo a
               ogni salvataggio, ma un file creato con un altro programma può non averlo.
            5. Copia la riga stampata dal terminale nella variabile `output_script` della cella qui sotto.
        """,
        suggerimento=(
            "puoi partire dal codice dell'esercizio precedente, con la funzione e il blocco "
            "`if __name__ == \"__main__\":`, e cambiare nomi, calcolo e testo; il formato `:.1f` dentro le "
            "graffe dà una cifra decimale."
        ),
        starter="""
            # il codice sta nel file bici.py; qui solo la riga copiata dal terminale
            output_script = "..."
            output_script
        """,
        soluzione='''
            # contenuto di bici.py, nella cartella del corso
            def media(valori):
                """Media aritmetica di una lista di numeri."""
                return sum(valori) / len(valori)


            if __name__ == "__main__":
                chilometri = [12.5, 8.0, 15.2, 9.8, 11.5]
                print(f"Media della settimana: {media(chilometri):.1f} km")

            # la riga stampata dal terminale dopo uv run bici.py
            output_script = "Media della settimana: 11.4 km"
        ''',
        verifica="""
            assert output_script.strip() == "Media della settimana: 11.4 km", "❌ output_script: la riga stampata dal terminale, tale e quale"
        """,
        perche=(
            "Il file sta nella cartella del corso, che è anche quella in cui si apre il terminale, quindi "
            "`uv run bici.py` funziona senza indicare percorsi e usa l'ambiente del corso. La riga va copiata dal "
            "terminale e non ricalcolata nel notebook, perché è la prova che lo script è stato eseguito."
        ),
    )

    # ------------------------------------------------------------------ Ruff
    nb.sottosezione("Ruff", intro="""
        Gli ultimi due esercizi riguardano le segnalazioni di Ruff, e in particolare quelle che le correzioni
        automatiche non sistemano, come la riga troppo lunga e la variabile assegnata e mai usata.
    """)
    nb.esercizio(
        titolo="Una riga troppo lunga",
        scenario="""
            Uno script che ogni mattina controlla le previsioni prepara un avviso per gli amici della partita di
            calcetto, ma la riga che lo compone è lunga 122 caratteri e Ruff la segnala con `E501`, perché il
            limite del progetto è di 100. Il comando `ruff format` non la sistema, dato che non divide mai una
            stringa, quindi la dividiamo noi in due pezzi scritti uno dopo l'altro tra parentesi, che Python
            unisce in una stringa sola. La cella stampa `True` quando il nuovo testo coincide con quello di
            partenza.
        """,
        richiesta="""
            1. Scrivi in `avviso_diviso`, dentro le parentesi, lo stesso testo di `avviso` diviso in due pezzi,
               uno per riga.
            2. Metti la `f` soltanto sul pezzo che contiene `{citta}`, e controlla che lo spazio tra i due pezzi
               non vada perso.
        """,
        suggerimento=(
            "l'ultima cella della sezione *Ruff: formatter e linter insieme* del notebook "
            "*Ambiente, script e Ruff* divide nello stesso modo la riga lunga della dimostrazione."
        ),
        starter="""
            citta = "Bologna"
            avviso = f"Domani a {citta} è prevista pioggia dalle 14 alle 18: conviene rimandare la partita di calcetto a giovedì sera"

            avviso_diviso = (
                ...
            )
            print(avviso_diviso == avviso)
        """,
        soluzione="""
            citta = "Bologna"
            avviso = f"Domani a {citta} è prevista pioggia dalle 14 alle 18: conviene rimandare la partita di calcetto a giovedì sera"

            avviso_diviso = (
                f"Domani a {citta} è prevista pioggia dalle 14 alle 18: "
                "conviene rimandare la partita di calcetto a giovedì sera"
            )
            print(avviso_diviso == avviso)  # Output: True
        """,
        verifica="""
            assert isinstance(avviso_diviso, str), "❌ avviso_diviso: due stringhe tra parentesi, una dopo l'altra"
            assert avviso_diviso == avviso, "❌ avviso_diviso: il testo deve essere identico a quello di avviso, spazi compresi"
        """,
        perche=(
            "Due stringhe scritte una dopo l'altra dentro le stesse parentesi diventano una stringa sola, quindi "
            "il testo non cambia e ogni riga resta sotto i 100 caratteri. Il secondo pezzo non contiene graffe "
            "da sostituire, e per questo non ha bisogno della `f`."
        ),
    )
    nb.esercizio(
        titolo="Pulizia con Ruff",
        scenario="""
            Un amico ha scritto lo script `meteo_report.py` qui sotto e vuole metterlo in un repository
            condiviso, dove ogni file deve passare `uv run ruff check` senza segnalazioni. Prima di lanciare Ruff
            proviamo a fare a mano il lavoro del linter, leggendo il file e scrivendo i codici delle
            segnalazioni che darebbe, e poi riscriviamo il codice in modo che non ne dia nessuna e stampi lo
            stesso testo.

            ```python
            import math

            soglia = 30
            giorni_caldi = ["12 luglio", "13 luglio"]


            def riepilogo(giorni_caldi, soglia):
                n = len(giorni_caldi)
                totale = 0
                return f"Trovati {n} giorni sopra i {soglia} gradi nel file meteo_luglio.csv: controllare il sensore sul balcone"


            print(riepilogo(giorni_caldi, soglia))
            ```
        """,
        richiesta="""
            1. Metti in `avvisi` la lista dei codici Ruff che il file farebbe scattare, come stringhe, uno per
               problema.
            2. Riscrivi nella cella il codice corretto, con una docstring per `riepilogo`, in modo che non dia
               segnalazioni e stampi lo stesso testo.
            3. Se vuoi controllare la tua risposta, salva il codice originale nel file `meteo_report.py` nella
               cartella del corso, accanto a `pyproject.toml`, e lancia nel terminale
               `uv run ruff check meteo_report.py`. Un eventuale `W292` non è uno dei codici da trovare,
               perché indica soltanto che al file manca l'a capo dopo l'ultima riga: VS Code, con le
               impostazioni della cartella del corso, lo aggiunge a ogni salvataggio, ma un file creato con
               un altro programma può non averlo.
        """,
        suggerimento=(
            "i codici sono nella tabella della sezione *Il linter* del notebook *Ambiente, script e Ruff*, e la "
            "stringa lunga si divide in due pezzi tra parentesi."
        ),
        starter="""
            avvisi = [...]

            # qui sotto il codice corretto
            soglia = 30
            giorni_caldi = ["12 luglio", "13 luglio"]


            def riepilogo(giorni_caldi, soglia):
                ...


            print(riepilogo(giorni_caldi, soglia))
        """,
        soluzione='''
            # un import mai usato, una variabile mai letta, una riga da 117 caratteri
            avvisi = ["F401", "F841", "E501"]

            soglia = 30
            giorni_caldi = ["12 luglio", "13 luglio"]


            def riepilogo(giorni_caldi, soglia):
                """Una riga di testo con il numero di giorni sopra la soglia."""
                n = len(giorni_caldi)
                return (
                    f"Trovati {n} giorni sopra i {soglia} gradi nel file meteo_luglio.csv: "
                    "controllare il sensore sul balcone"
                )


            print(riepilogo(giorni_caldi, soglia))
        ''',
        verifica="""
            assert sorted(avvisi) == ["E501", "F401", "F841"], "❌ avvisi: tre codici come stringhe, per l'import inutilizzato, la variabile mai letta e la riga troppo lunga"
            assert riepilogo(["12 luglio", "13 luglio"], 30) == "Trovati 2 giorni sopra i 30 gradi nel file meteo_luglio.csv: controllare il sensore sul balcone", "❌ riepilogo: il testo in uscita deve restare identico"
            assert riepilogo.__doc__, "❌ riepilogo: manca la docstring"
        """,
        perche=(
            "L'import di `math` e la variabile `totale` non servono a nulla e si tolgono: il primo lo toglierebbe "
            "anche `uv run ruff check --fix`, la seconda va cancellata a mano. La riga lunga si divide in due "
            "pezzi tra parentesi, il testo in uscita resta identico e Ruff non segnala più nulla."
        ),
    )
    return nb
