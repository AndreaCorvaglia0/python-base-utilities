# Gli errori più comuni

Un errore ferma la cella, e le celle sotto non girano finché non lo sistemiamo. Il messaggio dice esattamente cosa non torna: basta sapere dove leggerlo.

## Come si legge un traceback

1. Dal basso: l'ultima riga è il tipo di errore e il messaggio, e quasi sempre basta quella.
2. Subito sopra, la riga con la freccia `---->` (o con il `^`) è il punto del nostro codice che si è rotto; `Cell In[12], line 3` dice quale cella e quale riga.
3. Le righe più in alto sono dentro pandas o dentro Python: si saltano, il problema sta quasi sempre nella nostra riga.
4. Se il messaggio non si capisce, si copia l'ultima riga in un motore di ricerca o la si incolla a Copilot con "spiegami questo errore", e si corregge una cosa alla volta.

## Gli errori, uno per uno

| Ultima riga del traceback | Causa tipica | Cosa guardare | Correzione tipica |
|---|---|---|---|
| `SyntaxError: expected ':'` (o `invalid syntax`, `'(' was never closed`) | manca un due punti, una parentesi o una virgoletta | il `^` sotto la riga; spesso il guasto è nella riga prima | chiudi parentesi e virgolette; `:` dopo `if`, `for`, `def` |
| `NameError: name 'consumi' is not defined` | variabile mai creata, o scritta in modo diverso | maiuscole e underscore; la cella che la crea è stata eseguita? | correggi il nome; dopo un Restart, **Run All** |
| `TypeError: can only concatenate str (not "float") to str` | testo e numero mescolati, o funzione chiamata con argomenti sbagliati | `type()` dei due valori | f-string invece di `+`; `float(testo)` se deve essere un numero |
| `KeyError: 'kWh'` | la colonna (o la chiave del dizionario) non esiste con quel nome | `df.columns`: maiuscole, spazi, accenti | copia il nome esatto; `s.iloc[0]` per la posizione, non `s[0]` |
| `IndexError: list index out of range` | posizione oltre la fine della lista | `len(lista)`: l'ultimo elemento è alla posizione `len - 1` | indice più piccolo, o `lista[-1]` per l'ultimo |
| `ValueError: could not convert string to float: '1.234,5'` | il valore c'è ma ha la forma sbagliata: virgola decimale, data in un altro formato | il valore citato nel messaggio | `decimal=","` nel `read_csv`; `format="%d/%m/%Y"` nel `to_datetime` |
| `FileNotFoundError: [Errno 2] No such file or directory: '../Dati/leture.csv'` | nome o percorso sbagliato, o la cartella di lavoro non è quella del notebook | `from pathlib import Path`, poi `Path.cwd()` e `list(Path("../Dati").glob("*"))` | correggi il nome; il percorso parte dalla cartella del notebook |
| `ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment.` | `df[mask]["kwh"] = 0`: pandas avvisa e non cambia niente | la cella non si ferma, ma il DataFrame è uguale a prima | `df.loc[mask, "kwh"] = 0` |
| `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe8 in position 47: invalid continuation byte` | il CSV viene da Excel o da Windows, con gli accenti in un altro encoding | la lettera accentata nella riga citata (`0xe8` è una `è`) | `pd.read_csv(percorso, sep=";", decimal=",", encoding="latin-1")` |
