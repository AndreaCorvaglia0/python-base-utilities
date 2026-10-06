# uv, il progetto e gli script

uv è il package manager del corso: crea l'ambiente virtuale `.venv`, installa le librerie scritte in `pyproject.toml` e lancia gli script. Si usa dal terminale (in VS Code: **Terminal → New Terminal**), dentro la cartella del progetto.

## Mettere in piedi il progetto

1. Installa uv. Windows: `winget install astral-sh.uv`. Mac: `brew install uv`. Poi chiudi e riapri il terminale.
2. Scarica il repository: `git clone https://github.com/AndreaCorvaglia0/python-base-utilities` oppure, da GitHub, **Code → Download ZIP** e scompatta la cartella.
3. Entra nella cartella (`cd python-base-utilities`) e lancia `uv sync`: crea `.venv` con la versione giusta di Python e tutte le librerie. La prima volta ci vuole un minuto.
4. Apri la cartella in VS Code: **File → Open Folder**. Servono le estensioni Python e Jupyter.
5. Apri un notebook e scegli il kernel: in alto a destra **Select Kernel → Python Environments → .venv**.
6. Verifica in una cella: `import sys` e poi `sys.executable`. Il percorso deve contenere `.venv`; se no, il kernel è sbagliato.

Una libreria in più: nel terminale `uv add nome`, poi **Restart** del kernel, poi `import nome`. Mai `!pip install` dentro il notebook: la libreria non finisce in `pyproject.toml` e al prossimo `uv sync` sparisce.

Uno script si lancia con `uv run script.py` dalla cartella in cui sta: usa `.venv` senza attivare niente.

## Da notebook a script in 6 passi

1. Crea `nome.py` nella stessa cartella del notebook: i percorsi `../Dati/...` restano validi.
2. Copia solo le celle che portano al risultato: via le prove, gli `head()`, i "prova tu" e le celle di esplorazione.
3. Gli `import` tutti in testa, una volta sola.
4. In uno script l'ultima espressione di una cella non mostra niente: togli le righe tipo `df` da solo, oppure mettile in un `print()`.
5. Metti il lavoro in una funzione con 2-3 parametri, un default e un `return`; in fondo al file la chiamata e un `print` del risultato.
6. Lancia `uv run nome.py` dal terminale. Se fallisce, leggi l'ultima riga del traceback (vedi `Scheda_errori.md`).

```python
import pandas as pd


def consumo_per_pod(percorso, fascia="F1"):
    """Somma i kWh di una fascia per ogni POD."""
    letture = pd.read_csv(percorso, sep=";", decimal=",", encoding="latin-1")
    mask = letture["fascia"] == fascia
    totali = letture[mask].groupby("pod")["kwh"].sum()
    return totali.reset_index()


risultato = consumo_per_pod("../Dati/letture_pod_2025.csv")
print(risultato)
```

## Ruff in VS Code

Ruff è linter e formatter insieme: `check` segnala quello che non va, `format` rimette in forma spazi, virgole e righe vuote senza cambiare cosa fa il codice. In VS Code si installa l'estensione **Ruff** (di Astral) e si attiva la formattazione al salvataggio, in `settings.json`:

```json
{
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true
    }
}
```

Dal terminale, nella cartella del progetto:

| Comando | Cosa fa |
|---|---|
| `uvx ruff check script.py` | elenca gli avvisi: file, riga, colonna, codice, messaggio |
| `uvx ruff format script.py` | riscrive il file nella forma giusta |
| `uvx ruff check --fix script.py` | corregge quello che sa correggere (gli import inutilizzati, per esempio) |

I tre codici che si vedono più spesso: `F401` import mai usato, `F841` variabile assegnata e mai letta, `E501` riga oltre il limite scritto in `pyproject.toml` (`line-length = 100`). La `F` sono errori veri, la `E` è stile.

## I comandi uv

| Comando | Cosa fa | Quando |
|---|---|---|
| `uv init nome` | crea un progetto nuovo con il suo `pyproject.toml` | un lavoro nuovo, fuori dal corso |
| `uv add pandas` | aggiunge una libreria a `pyproject.toml` e la installa | prima dell'`import` che fallisce |
| `uv remove pandas` | toglie una libreria dal progetto | quando non serve più |
| `uv sync` | ricrea `.venv` esattamente come dice `uv.lock` | subito dopo il clone, o se l'ambiente si rompe |
| `uv run script.py` | esegue uno script dentro `.venv` | lanciare uno script dal terminale |
| `uv python install 3.13` | scarica una versione di Python | se `uv sync` dice che manca |
| `uvx ruff check .` | controlla il codice con Ruff senza installarlo nel progetto | prima di passare lo script a un collega |
