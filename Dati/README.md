# Dati

| File | Cos'è | Da dove viene |
|---|---|---|
| `load_total_north_hourly_2024.xlsx`, `load_total_north_hourly_2025.xlsx` | Carico elettrico della zona Nord, un valore ogni 15 minuti (MW), con la previsione di Terna | [Terna Download Center](https://dati.terna.it/en/download-center) |
| `TexasTurbine.csv` | Un anno di produzione oraria di una turbina eolica, con vento, pressione e temperatura | dataset pubblico (Kaggle) |
| `U.S. Electricity Prices.csv` | Prezzi mensili dell'elettricità negli Stati Uniti per stato e settore, 2001-2024 | EIA, via Kaggle |
| `letture_pod_2025.csv` | Consumi mensili per fascia di sei POD, formato "italiano" (`;`, virgola decimale, encoding latin-1), con una lettura ×10 a luglio (F1) per il POD IT001E45678901 | dati di esempio, inventati |
| `impianti_fv.csv` | Anagrafica di 40 impianti fotovoltaici in Lombardia | dati di esempio, inventati |
| `bolletta_esempio.xlsx` | Tre fogli: `Consumi`, `Listino`, `Anagrafica` | dati di esempio, inventati |
| `utility.db` | Database SQLite con le tabelle `clienti`, `pod`, `letture` | dati di esempio, inventati |
| `prezzi_zonali_2025_settimana.csv` | Prezzi orari per zona di mercato, una settimana | dati di esempio, inventati |
| `homework/letture_marzo.csv` | Letture giornaliere di marzo 2025 di otto POD, formato "italiano" (`;` e virgola decimale), con una lettura ×10 il 12 marzo per il POD IT001E31047092 | dati di esempio, inventati (homework) |
| `homework/clienti.xlsx` | Due fogli: `Anagrafica` (pod, cliente, comune) e `Listino` (fascia, eur_kwh) | dati di esempio, inventati (homework) |
| `homework/anagrafica.db` | Database SQLite con la tabella `pod` (pod, cliente, potenza_kw) | dati di esempio, inventati (homework) |
| `fallback/meteo_milano_2024_2025.json` | Risposta di Open-Meteo (archivio): temperatura oraria a Milano, 2024-2025, 17544 ore | dati di esempio, generati da `_build/genera_dati.py` con lo stesso schema dell'API; `uv run python _build/scarica_fallback.py` li sostituisce con i dati veri |
| `fallback/meteo_milano_previsione.json` | Risposta di Open-Meteo (previsione): temperatura, umidità e vento orari a Milano per 7 giorni dalla data di generazione | dati di esempio, generati da `_build/genera_dati.py` con lo stesso schema dell'API; `uv run python _build/scarica_fallback.py` li sostituisce con i dati veri |
| `fallback/lombardia_sensori.json` | Anagrafica dei sensori meteo di Regione Lombardia (dataset `nf78-nj6b`), 30 sensori, tutti i campi come testo | dati di esempio, generati da `_build/genera_dati.py` con lo stesso schema dell'API; `uv run python _build/scarica_fallback.py` li sostituisce con i dati veri |
| `fallback/lombardia_misure_2001.json` | Misure del sensore di temperatura 2001 (dataset `647i-nhxk`), giugno 2025 ogni 10 minuti, con qualche `-9999` | dati di esempio, generati da `_build/genera_dati.py` con lo stesso schema dell'API; `uv run python _build/scarica_fallback.py` li sostituisce con i dati veri |

I file di esempio si rigenerano con `uv run python _build/genera_dati.py`.
