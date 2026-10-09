# uv, il progetto e gli script

uv è il package manager usato nel corso. Crea l'ambiente virtuale `.venv`, installa le librerie elencate in `pyproject.toml` e lancia gli script. Si usa dal terminale, aperto dentro la cartella del progetto; in VS Code il terminale si apre con **Terminal → New Terminal**.

## Preparare il progetto

1. Si installa uv con `winget install --id=astral-sh.uv -e` su Windows oppure con `brew install uv` su Mac, e poi si chiude e si riapre il terminale.
2. Si scarica il repository con `git clone https://github.com/AndreaCorvaglia0/python-base-utilities` oppure, dalla pagina GitHub, con **Code → Download ZIP**, e in questo caso si scompatta la cartella.
3. Si entra nella cartella con `cd python-base-utilities` e si lancia `uv sync`, che crea `.venv` con la versione giusta di Python e tutte le librerie. La prima volta l'operazione richiede circa un minuto.
4. Si apre la cartella in VS Code con **File → Open Folder**; servono le estensioni Python e Jupyter.
5. Si apre un notebook e si sceglie il kernel con **Select Kernel**, in alto a destra. Se nel menu c'è già una voce con `.venv` nel nome si sceglie quella, altrimenti si passa da **Select Another Kernel... → Python Environments...** e si seleziona la `.venv`.
6. Per verificare la scelta si eseguono in una cella `import sys` e poi `sys.executable`. Il percorso stampato deve contenere `.venv`; in caso contrario il kernel selezionato è sbagliato.

Per aggiungere una libreria si esegue `uv add nome` nel terminale, si riavvia il kernel con **Restart** e solo allora si scrive `import nome`. Non si usa invece `!pip install` dentro il notebook, perché la libreria non viene registrata in `pyproject.toml` e scompare al successivo `uv sync`.

Uno script si salva nella cartella principale del progetto e si lancia da lì con `uv run script.py`, che usa `.venv` senza bisogno di attivare l'ambiente.

## Da notebook a script in sei passi

1. Si crea `nome.py` nella cartella principale del progetto, accanto a `pyproject.toml`; da lì i dati si trovano in `Dati/...`, senza `../`.
2. Si copiano solo le celle che portano al risultato, lasciando fuori le prove, gli `head()`, i "prova tu" e le celle di esplorazione.
3. Gli `import` si raccolgono tutti in testa al file, una volta sola.
4. In uno script l'ultima espressione di una cella non mostra niente, quindi le righe come `df` da solo vanno tolte oppure messe dentro un `print()`.
5. Il lavoro si raccoglie in una funzione con 2-3 parametri, un default e un `return`, e in fondo al file si scrivono la chiamata e un `print` del risultato.
6. Infine si lancia `uv run nome.py` dal terminale. Se lo script fallisce, si legge l'ultima riga del traceback, come spiegato in `Scheda_errori.md`.

```python
import pandas as pd


def consumo_per_pod(percorso, fascia="F1"):
    """Somma i kWh di una fascia per ogni POD."""
    letture = pd.read_csv(percorso, sep=";", decimal=",", encoding="latin-1")
    mask = letture["fascia"] == fascia
    totali = letture[mask].groupby("pod")["kwh"].sum()
    return totali.reset_index()


risultato = consumo_per_pod("Dati/letture_pod_2025.csv")
print(risultato)
```

## Ruff in VS Code

Ruff svolge insieme il ruolo di linter e di formatter. Il comando `check` segnala quello che non va nel codice, mentre `format` sistema spazi, virgole e righe vuote senza cambiare il comportamento del programma. In VS Code si installa l'estensione **Ruff**, pubblicata da Astral, e si attiva la formattazione al salvataggio aggiungendo a `settings.json` queste righe:

```json
{
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true
    }
}
```

Dal terminale, nella cartella del progetto, si usano i comandi seguenti:

| Comando | Cosa fa |
|---|---|
| `uv run ruff check script.py` | elenca gli avvisi, ciascuno con file, riga, colonna, codice e messaggio |
| `uv run ruff format script.py` | riscrive il file nella forma giusta |
| `uv run ruff check --fix script.py` | corregge da solo gli avvisi che sa correggere, per esempio gli import inutilizzati |

I codici che si incontrano più spesso sono tre: `F401` indica un import mai usato, `F841` una variabile assegnata e mai letta, `E501` una riga più lunga del limite fissato in `pyproject.toml` (`line-length = 100`). I codici `F` segnalano problemi reali, che possono impedire al codice di funzionare, mentre i codici `E` riguardano lo stile.

## I comandi uv

| Comando | Cosa fa | Quando |
|---|---|---|
| `uv init nome` | crea un progetto nuovo con il suo `pyproject.toml` | per un lavoro nuovo, fuori dal corso |
| `uv add pandas` | aggiunge una libreria a `pyproject.toml` e la installa | prima di un `import` che altrimenti fallirebbe |
| `uv remove pandas` | toglie una libreria dal progetto | quando non serve più |
| `uv sync` | ricrea `.venv` esattamente come dice `uv.lock` | subito dopo il clone, o quando l'ambiente non funziona più |
| `uv run script.py` | esegue uno script dentro `.venv` | per lanciare uno script dal terminale |
| `uv python install 3.13` | scarica una versione di Python | quando `uv sync` segnala che quella versione manca |
| `uv run ruff check .` | controlla il codice con Ruff, che nel progetto del corso è già installato | prima di passare lo script a un collega |
| `uvx ruff check .` | lancia Ruff al volo, senza aggiungerlo al progetto | su una cartella che non è un progetto uv |
