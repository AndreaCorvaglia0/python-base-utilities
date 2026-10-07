"""Controllo degli esercizi del corso. Generato da _build/build.py: non modificare a mano.

In ogni notebook, sotto un esercizio:

    from corso import verifica
    verifica("7.1")

Se il risultato è giusto stampa ✅, altrimenti una riga che dice cosa non torna.
I controlli sono in fondo a questo file, uno per esercizio.
"""

import inspect


class VerificaFallita(Exception):
    """Il risultato dell'esercizio non è quello atteso: nel notebook compare una riga sola, senza traceback."""

    def _render_traceback_(self):
        return [f"\x1b[31m❌ {self}\x1b[0m"]


def verifica(codice: str) -> None:
    """Controlla le variabili del notebook per l'esercizio `codice`."""
    if codice not in VERIFICHE:
        raise VerificaFallita(f"Non c'è un controllo per {codice!r}")
    etichetta, controllo = VERIFICHE[codice]
    spazio = dict(inspect.currentframe().f_back.f_globals)
    try:
        exec(compile(controllo, f"<verifica {codice}>", "exec"), spazio)
    except AssertionError as e:
        msg = str(e).removeprefix("❌").strip() or "Il risultato non è quello atteso"
        raise VerificaFallita(msg) from None
    except NameError as e:
        nome = getattr(e, "name", None)
        msg = f"Non trovo la variabile `{nome}`: hai eseguito la cella dell'esercizio?" if nome else str(e)
        raise VerificaFallita(msg) from None
    except Exception as e:
        raise VerificaFallita(f"{type(e).__name__}: {e}") from None
    print(f"✅ {etichetta} completato")


VERIFICHE = {

    'X1.1': ('Esercizio X1.1', r'''
import plotly

assert versione_plotly == plotly.__version__, "❌ versione_plotly: l'attributo __version__ della libreria plotly"
assert comando_aggiungi.strip() == "uv add openpyxl", "❌ comando_aggiungi: il comando uv che aggiunge una libreria, seguito dal nome"
assert comando_collega.strip() == "uv sync", "❌ comando_collega: il comando uv che ricrea l'ambiente dal progetto"
'''),
    'X1.2': ('Esercizio X1.2', r'''
assert ".venv" in percorso_python, "❌ percorso_python: sys.executable, e deve contenere .venv (altrimenti cambia kernel tu per primo)"
assert diagnosi == "kernel", "❌ diagnosi: la libreria è installata nel progetto, quindi il problema è un altro"
assert rimedio == "Select Kernel", "❌ rimedio: non si installa niente, si cambia il Python che esegue il notebook"
'''),
    'X1.3': ('Esercizio X1.3', r'''
assert output_script.strip() == "Media delle letture: 405.5 kWh", "❌ output_script: la riga stampata dal terminale, tale e quale"
'''),
    'X2.1': ('Esercizio X2.1', r'''
assert sorted(avvisi) == ["E501", "F401", "F841"], "❌ avvisi: tre codici come stringhe: import inutilizzato, variabile mai usata, riga troppo lunga"
assert riepilogo(["IT001E45678901"], 1000) == "Trovati 1 POD sopra la soglia di 1000 kWh nel file letture_pod_2025.csv: controllare le letture di luglio", "❌ riepilogo: il testo in uscita deve restare identico"
assert riepilogo.__doc__, "❌ riepilogo: manca la docstring"
'''),
}
