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
| `homework/letture_marzo.csv` | Letture giornaliere di marzo 2025 di otto POD, formato "italiano" (`;` e virgola decimale), con una lettura ×10 il 12 marzo per il POD IT001E31047092 | dati di esempio, inventati (homework) |
| `homework/clienti.xlsx` | Due fogli: `Anagrafica` (pod, cliente, comune) e `Listino` (fascia, eur_kwh) | dati di esempio, inventati (homework) |
| `homework/anagrafica.db` | Database SQLite con la tabella `pod` (pod, cliente, potenza_kw) | dati di esempio, inventati (homework) |
| `fallback/meteo_milano_2024_2025.json` | Risposta di Open-Meteo (archivio): temperatura oraria a Milano, 2024-2025, 17544 ore | copia della risposta dell'API, usata quando la rete non è disponibile |
