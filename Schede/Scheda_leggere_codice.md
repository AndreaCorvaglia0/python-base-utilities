# Leggere il codice: cosa è cosa

Una riga di Python si legge come una frase: a sinistra del punto c'è chi fa il lavoro, tra parentesi con cosa, a sinistra dell'uguale dove finisce il risultato. Questa pagina serve quando il codice lo ha scritto qualcun altro, un collega o un agente, e bisogna sapere cosa si sta guardando prima di lanciarlo.

## La riga tipo

```python
letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",")
```

| Pezzo | Cos'è |
|---|---|
| `letture` | la variabile che riceve il risultato, qui un DataFrame |
| `=` | assegnazione; il confronto è `==` |
| `pd` | la libreria pandas, importata con `import pandas as pd` |
| `.read_csv` | una funzione della libreria |
| `"../Dati/letture_pod_2025.csv"` | il primo argomento, passato per posizione: il percorso del file |
| `sep=";"`, `decimal=","` | argomenti passati per nome: parametri facoltativi, con un default che qui cambiamo |

## Le forme, una per riga

| Forma | Nome | Cosa vuol dire | Altri esempi |
|---|---|---|---|
| `import pandas as pd` | import con alias | carica la libreria; da qui in giù si chiama `pd` | `import numpy as np` |
| `import plotly.express as px` | import di un sottomodulo | una libreria è una cartella di moduli: il punto scende di un livello | `import os.path` |
| `from pathlib import Path` | import mirato | prende una cosa sola da un modulo, qui una classe | `from math import sqrt` |
| `pd.read_csv(...)` | funzione di libreria | a sinistra del punto una libreria o un modulo | `math.sqrt(16)`, `px.line(df)` |
| `df.head()` | metodo | un'azione dell'oggetto a sinistra del punto; parentesi sempre, anche vuote | `pod.upper()`, `lista.append(3)` |
| `df.shape` | attributo | un dato dell'oggetto, senza parentesi | `df.columns`, `oggi.year` |
| `pd.DataFrame({...})`, `Path("..")` | classe chiamata | la maiuscola iniziale è la convenzione: costruisce un oggetto di quella classe | `date(2025, 3, 1)` |
| `len(df)`, `print(x)`, `round(x, 2)` | funzione di Python | sempre disponibile, senza import; l'oggetto va tra le parentesi | `type(x)`, `sorted(lista)`, `sum(lista)` |
| `df["kwh"]`, `lista[0]`, `d["F1"]` | selezione con le quadre | colonna, posizione o chiave, a seconda dell'oggetto a sinistra | `lista[-1]`, `lista[1:3]`, `df.loc[mask, "kwh"]` |
| `[1, 2]`, `{"F1": 0.28}`, `(1, 2)`, `{"a", "b"}` | letterali | una lista, un dizionario, una tupla, un set scritti a mano | `[]` lista vuota |
| `def nome(a, b=2):` ... `return` | definizione di funzione | il corpo indentato parte solo quando qualcuno la chiama; `return` è il risultato | |
| `def f(x: float) -> float:` | type hint | cosa entra e cosa esce; Python non li controlla, servono a chi legge | `path: Path`, `fasce: list[str] \| None = None` |
| `if ...:` / `elif ...:` / `else:` | condizione | un ramo solo viene eseguito | |
| `for riga in letture:` | ciclo | il corpo parte una volta per ogni elemento | `for i in range(4):` |
| `while condizione:` | ciclo a condizione | ripete finché la condizione è vera | |
| `f"Totale: {kwh:.1f} kWh"` | f-string | testo con valori dentro le graffe; dopo i due punti il formato | `{data:%d/%m/%Y}` |
| `with open(p) as f:` | context manager | apre e chiude da solo, anche se qualcosa va storto | `with pd.ExcelWriter(p) as w:` |
| `try:` / `except ValueError:` | gestione dell'errore | prova; se arriva quell'errore, fai quest'altro. Un `except:` senza tipo nasconde tutto: campanello d'allarme | |
| `raise ValueError("...")` | errore creato apposta | il contrario di `except`: ferma tutto con un messaggio chiaro | |
| `@dataclass`, `@property` | decoratore | la riga con `@` sopra un `def` o una `class` cambia come si comporta quello che sta sotto; si legge, non si scrive | `@staticmethod` |
| `class Config:` ... `self` | classe | lo stampo di un oggetto; i `def` dentro sono i suoi metodi; `self` è l'oggetto stesso | |
| `lambda x: x / 4` | funzione senza nome | una riga sola, di solito dentro `sorted(key=...)` o `.apply(...)` | |
| `[p / 4 for p in potenze]` | comprehension | un ciclo che costruisce una lista in una riga | `{k: v for k, v in ...}` |
| `*args`, `**kwargs` | argomenti raccolti | tutti quelli per posizione, tutti quelli per nome, di solito passati avanti a un'altra funzione | `pd.read_csv(path, **opzioni)` |
| `if __name__ == "__main__":` | guardia dello script | quel blocco parte solo se il file è lanciato con `uv run`, non se viene importato | |
| `yield` | generatore | una funzione che restituisce un elemento alla volta invece di una lista intera | |
| `async def` / `await` | codice asincrono | si legge come una funzione normale con una parola in più; nelle analisi dati è raro | |
| `None` | il valore "niente" | default dei parametri facoltativi; quel che restituisce una funzione senza `return` | `if fasce is not None:` |
| `__file__`, `__name__`, `__version__` | nomi speciali | li mette Python; `__file__` esiste solo negli script, in una cella dà `NameError` | |

## Come si legge uno script

1. Gli `import`, in testa: chi serve. Libreria standard (arriva con Python) o installata (ci è voluto un `uv add`)?
2. Le costanti in MAIUSCOLO: i numeri, i percorsi e le soglie che vengono da fuori.
3. Le `def`: gli attrezzi. Nome, parametri e docstring bastano per sapere cosa fanno; il corpo si legge dopo.
4. In fondo, chi li usa: `main()` oppure le righe libere. È da lì che parte l'esecuzione.
5. Le righe che fanno il lavoro vero sono poche, due o tre di pandas: il resto è cornice. Si controllano quelle, con un numero che si conosce.

## Una riga che non capisci

- All'agente: "Spiegami questa riga senza riscriverla", poi "Cosa succede se la tolgo?".
- A Python: `type(oggetto)` dice la classe, `help(funzione)` la firma e la docstring, `dir(oggetto)` tutto quello che sa fare.
- Poi si esegue e si confronta il risultato con un numero che si conosce già.
