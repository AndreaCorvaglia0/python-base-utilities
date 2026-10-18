# Da Excel a pandas

Questa scheda raccoglie le operazioni che si fanno abitualmente in Excel, ciascuna con il nome che ha in pandas. Gli esempi presuppongono `import pandas as pd` e un DataFrame `df`, mentre per il grafico serve anche `import plotly.express as px`. Il risultato di un'operazione non modifica il DataFrame di partenza e, per conservarlo, va riassegnato, come in `df = df.sort_values("kwh")`.

## Le operazioni

| In Excel | In pandas | Nota |
|---|---|---|
| Apri un file CSV | `df = pd.read_csv("../Dati/impianti_fv.csv")` | per un CSV italiano servono `sep=";", decimal=","`; se compare `UnicodeDecodeError`, si aggiunge `encoding="latin-1"` |
| Apri un foglio Excel | `df = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Consumi")` | `sheet_name=None` legge tutti i fogli in un dizionario |
| Filtro | `mask = df["kwh"] > 1000` poi `df[mask]` | con due condizioni si scrive `(df["kwh"] > 1000) & (df["fascia"] == "F1")`, e le parentesi sono obbligatorie |
| Ordina | `df = df.sort_values("kwh", ascending=False)` | per ordinare su più colonne: `df.sort_values(["pod", "kwh"])` |
| Formato cella (tipo di colonna) | `df["kwp"] = df["kwp"].astype(float)` | per le date: `df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")`; con `df.dtypes` si controllano i tipi |
| Rimuovi duplicati | `df = df.drop_duplicates()` | per considerare solo alcune colonne: `df.drop_duplicates(subset=["pod", "data"])` |
| Colonna calcolata | `df["costo"] = df["kwh"] * 0.21` | la formula si applica a tutta la colonna, senza bisogno di trascinarla |
| SOMMA, MEDIA, CONTA.VALORI | `df["kwh"].sum()`, `df["kwh"].mean()`, `len(df)` | per contare i valori distinti: `df["pod"].nunique()` |
| SOMMA.SE (subtotali per gruppo) | `df.groupby("pod")["kwh"].sum().reset_index()` | `reset_index()` riporta `pod` a colonna normale |
| Tabella pivot | `df.pivot_table(index="pod", columns="fascia", values="kwh", aggfunc="sum")` | `aggfunc="mean"` per la media |
| CERCA.VERT | `df = pd.merge(letture, listino, on="fascia", how="left")` | conviene confrontare `len()` prima e dopo, perché il numero di righe non deve cambiare |
| Incolla un foglio sotto l'altro | `df = pd.concat([gennaio, febbraio], ignore_index=True)` | i due fogli devono avere le stesse colonne |
| Salva come CSV | `df.to_csv("consumi_puliti.csv", index=False)` | `index=False` non scrive la colonna dei numeri di riga |
| Salva un Excel a più fogli | `with pd.ExcelWriter("report.xlsx") as writer:` poi `df.to_excel(writer, sheet_name="Consumi", index=False)` | si scrive una riga `to_excel` per ogni foglio, all'interno del blocco `with` |
| Grafico a linee | `fig = px.line(df, x="data", y="kwh", color="pod")` poi `fig.show()` | `px.bar` per le barre, `px.scatter` per i punti |

## La ricetta del report mensile

Supponiamo che il CSV del fornitore arrivi via mail il primo di ogni mese e che il responsabile chieda un file Excel e un grafico. Il codice seguente, eseguito dal notebook con i percorsi del corso, produce entrambi:

```python
import pandas as pd
import plotly.express as px

# il CSV italiano: punto e virgola, virgola decimale, accenti in latin-1
letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
# via le righe doppie, e le date da testo a data
letture = letture.drop_duplicates()
letture["data"] = pd.to_datetime(letture["data"], format="%d/%m/%Y")
# kWh di ogni POD, mese per mese
mensile = letture.groupby(["pod", "data"])["kwh"].sum().reset_index()
# un Excel con il dettaglio e i totali mensili su due fogli
with pd.ExcelWriter("report_mensile.xlsx") as writer:
    letture.to_excel(writer, sheet_name="Dettaglio", index=False)
    mensile.to_excel(writer, sheet_name="Mensile", index=False)
# il grafico, salvato in HTML per chi non ha Python
fig = px.line(mensile, x="data", y="kwh", color="pod", title="Consumo mensile per POD")
fig.write_html("report_mensile.html")
```

Per un file diverso è sufficiente cambiare il percorso e i nomi delle colonne, mentre il resto del codice rimane lo stesso ogni mese.
