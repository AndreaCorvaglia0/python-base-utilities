# Gli errori più comuni

Quando Python incontra un errore, l'esecuzione della cella si interrompe e le celle successive non possono funzionare finché il problema non viene corretto. Il messaggio che compare, chiamato traceback, indica con precisione che cosa non va; occorre soltanto sapere in quale punto leggerlo.

## Leggere un traceback

1. Il traceback si legge dal basso. L'ultima riga riporta il tipo di errore e il messaggio, e quasi sempre è sufficiente per capire il problema.
2. Subito sopra, la riga indicata dalla freccia `---->` (o dal segno `^`) mostra il punto del nostro codice in cui si è verificato l'errore, mentre `Cell In[12], line 3` dice in quale cella e in quale riga si trova.
3. Le righe più in alto appartengono al codice interno di pandas o di Python e di solito si possono saltare, perché il problema sta quasi sempre nella riga che abbiamo scritto noi.
4. Se il messaggio non è chiaro, conviene copiare l'ultima riga in un motore di ricerca, oppure incollarla a Copilot chiedendo "spiegami questo errore", e poi correggere una cosa alla volta.

## Gli errori e le loro correzioni

| Ultima riga del traceback | Causa tipica | Cosa guardare | Correzione tipica |
|---|---|---|---|
| `SyntaxError: expected ':'` (o `invalid syntax`, `'(' was never closed`) | manca un due punti, una parentesi o una virgoletta | il `^` sotto la riga; spesso l'errore sta nella riga precedente | chiudi parentesi e virgolette; `:` dopo `if`, `for`, `def` |
| `NameError: name 'consumi' is not defined` | variabile mai creata, o scritta in modo diverso | maiuscole e underscore, e se la cella che la crea è stata eseguita | correggi il nome; dopo un Restart, **Run All** |
| `TypeError: can only concatenate str (not "float") to str` | testo e numero mescolati, o funzione chiamata con argomenti sbagliati | `type()` dei due valori | f-string invece di `+`; `float(testo)` se deve essere un numero |
| `KeyError: 'kWh'` | la colonna (o la chiave del dizionario) non esiste con quel nome | `df.columns`, controllando maiuscole, spazi e accenti | copia il nome esatto; `s.iloc[0]` per la posizione, non `s[0]` |
| `IndexError: list index out of range` | posizione oltre la fine della lista | `len(lista)`, ricordando che l'ultimo elemento è alla posizione `len - 1` | indice più piccolo, o `lista[-1]` per l'ultimo |
| `ValueError: could not convert string to float: '1.234,5'` | il valore c'è ma ha una forma sbagliata, per esempio la virgola decimale o una data in un altro formato | il valore citato nel messaggio | `decimal=","` nel `read_csv`; `format="%d/%m/%Y"` nel `to_datetime` |
| `FileNotFoundError: [Errno 2] No such file or directory: '../Dati/leture.csv'` | nome o percorso sbagliato, o la cartella di lavoro non è quella del notebook | `from pathlib import Path`, poi `Path.cwd()` e `list(Path("../Dati").glob("*"))` | correggi il nome; il percorso parte dalla cartella del notebook |
| `AttributeError: 'DataFrame' object has no attribute 'sort'` (o `Can only use .dt accessor with datetimelike values`) | metodo inventato o scritto male, spesso da un agente, oppure chiamato sull'oggetto sbagliato | `type(oggetto)` e `dir(oggetto)`, o il menu che compare dopo il punto in VS Code | il nome giusto (`sort_values`); `pd.to_datetime` prima di `.dt` |
| `ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment.` | con `df[mask]["kwh"] = 0` pandas mostra l'avviso ma non modifica niente | la cella non si ferma, ma il DataFrame resta uguale a prima | `df.loc[mask, "kwh"] = 0` |
| `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe8 in position 47: invalid continuation byte` | il CSV viene da Excel o da Windows, con gli accenti in un altro encoding | la lettera accentata nella riga citata (`0xe8` è una `è`) | `pd.read_csv(percorso, sep=";", decimal=",", encoding="latin-1")` |
