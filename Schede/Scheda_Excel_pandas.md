# Da Excel a pandas

Le operazioni di sempre, con il nome che hanno in pandas. Le righe assumono `import pandas as pd` e un DataFrame `df`; per il grafico serve anche `import plotly.express as px`. Il risultato non si salva da solo: si riassegna (`df = df.sort_values("kwh")`).

## Le operazioni

| In Excel | In pandas | Nota |
|---|---|---|
| Apri un file CSV | `df = pd.read_csv("../Dati/impianti_fv.csv")` | CSV italiano: `sep=";", decimal=","`; se dà `UnicodeDecodeError`, aggiungi `encoding="latin-1"` |
| Apri un foglio Excel | `df = pd.read_excel("../Dati/bolletta_esempio.xlsx", sheet_name="Consumi")` | `sheet_name=None` legge tutti i fogli in un dizionario |
| Filtro | `mask = df["kwh"] > 1000` poi `df[mask]` | due condizioni: `(df["kwh"] > 1000) & (df["fascia"] == "F1")`, parentesi obbligatorie |
| Ordina | `df = df.sort_values("kwh", ascending=False)` | più colonne: `df.sort_values(["pod", "kwh"])` |
| Formato cella (tipo di colonna) | `df["kwp"] = df["kwp"].astype(float)` | date: `df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")`; `df.dtypes` per controllare |
| Rimuovi duplicati | `df = df.drop_duplicates()` | solo su alcune colonne: `df.drop_duplicates(subset=["pod", "data"])` |
| Colonna calcolata | `df["costo"] = df["kwh"] * 0.21` | la formula vale per tutta la colonna, senza trascinare |
| SOMMA, MEDIA, CONTA.VALORI | `df["kwh"].sum()`, `df["kwh"].mean()`, `len(df)` | valori distinti: `df["pod"].nunique()` |
| SOMMA.SE (subtotali per gruppo) | `df.groupby("pod")["kwh"].sum().reset_index()` | `reset_index()` riporta `pod` a colonna normale |
| Tabella pivot | `df.pivot_table(index="pod", columns="fascia", values="kwh", aggfunc="sum")` | `aggfunc="mean"` per la media |
| CERCA.VERT | `df = pd.merge(letture, listino, on="fascia", how="left")` | `len()` prima e dopo: le righe non devono cambiare |
| Incolla un foglio sotto l'altro | `df = pd.concat([gennaio, febbraio], ignore_index=True)` | i due fogli devono avere le stesse colonne |
| Salva come CSV | `df.to_csv("consumi_puliti.csv", index=False)` | `index=False` non scrive la colonna dei numeri di riga |
| Salva un Excel a più fogli | `with pd.ExcelWriter("report.xlsx") as writer:` poi `df.to_excel(writer, sheet_name="Consumi", index=False)` | una riga `to_excel` per ogni foglio, dentro il `with` |
| Grafico a linee | `fig = px.line(df, x="data", y="kwh", color="pod")` poi `fig.show()` | `px.bar` per le barre, `px.scatter` per i punti |

## La ricetta del report mensile

Il CSV del fornitore arriva via mail il primo del mese e il capo vuole un Excel e un grafico. Dal notebook, con i percorsi del corso:

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

Per un altro file cambiano il percorso e i nomi delle colonne; il resto è uguale ogni mese.
