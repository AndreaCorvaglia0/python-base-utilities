# Dati

| File | Cos'è | Da dove viene |
|---|---|---|
| `load_total_north_hourly_2024.xlsx`, `..._2025.xlsx` | Carico elettrico della zona Nord, un valore ogni 15 minuti (MW), con la previsione di Terna | [Terna Download Center](https://dati.terna.it/en/download-center) |
| `TexasTurbine.csv` | Un anno di produzione oraria di una turbina eolica, con vento, pressione e temperatura | dataset pubblico (Kaggle) |
| `U.S. Electricity Prices.csv` | Prezzi mensili dell'elettricità negli Stati Uniti per stato e settore, 2001-2024 | EIA, via Kaggle |
| `letture_pod_2025.csv` | Consumi mensili per fascia di sei POD, formato "italiano" (`;` e virgola decimale) | dati di esempio, inventati |
| `impianti_fv.csv` | Anagrafica di 40 impianti fotovoltaici in Lombardia | dati di esempio, inventati |
| `bolletta_esempio.xlsx` | Tre fogli: `Consumi`, `Listino`, `Anagrafica` | dati di esempio, inventati |
| `utility.db` | Database SQLite con le tabelle `clienti`, `pod`, `letture` | dati di esempio, inventati |
| `prezzi_zonali_2025_settimana.csv` | Prezzi orari per zona di mercato, una settimana | dati di esempio, inventati |
| `fallback/` | Risposte salvate delle API usate nel corso, da usare se la rete non collabora | creata da `_build/scarica_fallback.py` |

I file di esempio si rigenerano con `uv run python _build/genera_dati.py`.
