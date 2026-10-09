# Leggere il codice: cosa è cosa

Una riga di Python si può leggere come una frase. A sinistra del punto c'è chi svolge il lavoro, tra le parentesi ciò su cui lavora e a sinistra dell'uguale la variabile in cui finisce il risultato. Questa pagina serve quando il codice è stato scritto da qualcun altro, un collega o un agente, e prima di eseguirlo bisogna capire che cosa si sta guardando.

## Una riga tipica

```python
letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
```

| Pezzo | Cos'è |
|---|---|
| `letture` | la variabile che riceve il risultato, qui un DataFrame |
| `=` | l'assegnazione; il confronto si scrive `==` |
| `pd` | la libreria pandas, importata con `import pandas as pd` |
| `.read_csv` | una funzione della libreria |
| `"../Dati/letture_pod_2025.csv"` | il primo argomento, passato per posizione, cioè il percorso del file |
| `sep=";"`, `decimal=","` | argomenti passati per nome, cioè parametri facoltativi che hanno un default e che qui cambiamo |
| `encoding="latin-1"` | argomento per nome che indica come sono scritti i caratteri accentati nel file |

## Le forme più comuni

| Forma | Nome | Cosa vuol dire | Altri esempi |
|---|---|---|---|
| `import pandas as pd` | import con alias | carica la libreria, che da quel punto in poi si chiama `pd` | `import numpy as np` |
| `import plotly.express as px` | import di un sottomodulo | una libreria è una cartella di moduli, e il punto scende di un livello | `import os.path` |
| `from pathlib import Path` | import mirato | prende una cosa sola da un modulo, qui una classe | `from math import sqrt` |
| `pd.read_csv(...)` | funzione di libreria | a sinistra del punto c'è una libreria o un modulo | `math.sqrt(16)`, `px.line(df)` |
| `df.head()` | metodo | un'azione dell'oggetto a sinistra del punto; le parentesi ci sono sempre, anche vuote | `pod.upper()`, `lista.append(3)` |
| `df.shape` | attributo | un dato dell'oggetto, senza parentesi | `df.columns`, `oggi.year` |
| `pd.DataFrame({...})`, `Path("..")` | classe chiamata | costruisce un oggetto di quella classe; per convenzione il nome ha l'iniziale maiuscola | `date(2025, 3, 1)` |
| `len(df)`, `print(x)`, `round(x, 2)` | funzione di Python | sempre disponibile, senza import, e l'oggetto va tra le parentesi; se il nome viene da un `from … import`, è della libreria indicata in testa | `type(x)`, `sorted(lista)`, `sum(lista)` |
| `df["kwh"]`, `lista[0]`, `d["F1"]` | selezione con le quadre | colonna, posizione o chiave, a seconda dell'oggetto a sinistra | `lista[-1]`, `lista[1:3]`, `df.loc[mask, "kwh"]` |
| `[1, 2]`, `{"F1": 0.28}`, `(1, 2)`, `{"a", "b"}` | letterali | una lista, un dizionario, una tupla e un set scritti a mano | `[]` lista vuota |
| `def nome(a, b=2):` ... `return` | definizione di funzione | il corpo indentato viene eseguito solo quando la funzione è chiamata; `return` restituisce il risultato | |
| `def f(x: float) -> float:` | type hint | indicano che cosa entra e che cosa esce; Python non li controlla, servono a chi legge; `list[str] \| None` si legge "lista di stringhe oppure `None`" | `path: Path`, `fasce: list[str] \| None = None` |
| `if ...:` / `elif ...:` / `else:` | condizione | viene eseguito un solo ramo | |
| `for pod in lista_pod:` | ciclo | il corpo viene eseguito una volta per ogni elemento | `for i in range(4):` |
| `while condizione:` | ciclo a condizione | ripete il corpo finché la condizione è vera | |
| `f"Totale: {kwh:.1f} kWh"` | f-string | testo con valori inseriti tra le graffe; dopo i due punti si indica il formato | `{data:%d/%m/%Y}` |
| `with open(p) as f:` | context manager | apre la risorsa e la chiude da solo, anche se nel blocco qualcosa va storto | `with pd.ExcelWriter(p) as w:` |
| `try:` / `except ValueError:` | gestione dell'errore | esegue il blocco `try` e, se si verifica quell'errore, passa al blocco `except`. Un `except:` senza tipo nasconde qualunque errore e va considerato un segnale di allarme | |
| `raise ValueError("...")` | errore creato apposta | ferma l'esecuzione con un messaggio chiaro, mentre `except` intercetta l'errore | |
| `@dataclass`, `@property` | decoratore | la riga con `@` sopra un `def` o una `class` cambia il comportamento di ciò che sta sotto; nel corso basta saperla leggere | `@staticmethod` |
| `class Config:` ... `self` | classe | il modello da cui si costruiscono gli oggetti; i `def` al suo interno sono i suoi metodi e `self` è l'oggetto stesso | |
| `lambda x: x / 4` | funzione senza nome | una funzione di una riga sola, di solito dentro `sorted(key=...)` o `.apply(...)` | |
| `[p / 4 for p in potenze]` | comprehension | un ciclo che costruisce una lista in una riga | `{k: v for k, v in ...}` |
| `*args`, `**kwargs` | argomenti raccolti | raccolgono tutti gli argomenti per posizione e tutti quelli per nome, di solito per passarli a un'altra funzione | `pd.read_csv(path, **opzioni)` |
| `logger.info("...")` | log | come un `print`, ma con il livello davanti (`INFO:__main__:...`); il messaggio va nel terminale e si attiva con `logging.basicConfig` | |
| `if __name__ == "__main__":` | blocco main (guardia dello script) | il blocco viene eseguito quando il file è il programma lanciato, con `uv run` o incollato in una cella, ma non quando viene importato | |
| `yield` | generatore | una funzione che restituisce un elemento alla volta invece di una lista intera | |
| `async def` / `await` | codice asincrono | si legge come una funzione normale con una parola in più; nell'analisi dei dati si incontra di rado | |
| `None` | il valore "niente" | è il default dei parametri facoltativi e ciò che restituisce una funzione senza `return` | `if fasce is not None:` |
| `x is None`, `x is not None` | controllo del niente | per `None` si usa `is`, non `==`; nel codice degli agenti è il modo di dire "se il parametro è stato passato" | `if fasce is not None:` |
| `assert condizione, "❌ messaggio"` | verifica | se la condizione è falsa si ferma con `AssertionError` e mostra il messaggio; è così che sono scritti i test, anche quelli generati da un agente | le celle di verifica del corso |
| `__file__`, `__name__`, `__version__` | nomi speciali | li definisce Python; `__file__` esiste solo negli script, in una cella dà `NameError` | |

## Leggere uno script

1. Gli `import` in testa al file dicono quali librerie servono, e conviene distinguere quelle della libreria standard, che arrivano con Python, da quelle installate, che hanno richiesto un `uv add`.
2. Le costanti scritte in MAIUSCOLO raccolgono i numeri, i percorsi e le soglie che vengono dall'esterno.
3. Le `def` sono gli strumenti dello script. Il nome, i parametri e la docstring bastano per capire che cosa fanno, e il corpo si può leggere in un secondo momento.
4. In fondo al file si trova il codice che usa queste funzioni, dentro `main()` oppure in righe libere, ed è da lì che parte l'esecuzione.
5. Le righe che svolgono il lavoro vero sono poche, di solito due o tre istruzioni di pandas, mentre il resto fa da cornice. Sono quelle che vanno controllate, confrontando il risultato con un numero che si conosce.

## Quando una riga non è chiara

- All'agente si può chiedere "Spiegami questa riga senza riscriverla" e poi "Cosa succede se la tolgo?".
- A Python si chiedono informazioni sull'oggetto: `type(oggetto)` restituisce la classe, `help(funzione)` mostra la firma e la docstring, `dir(oggetto)` elenca tutto quello che l'oggetto sa fare.
- Infine si esegue la riga e si confronta il risultato con un numero che si conosce già.
