"""
Genera i dataset di esempio usati negli esercizi del corso (cartella Dati/).

Sono dati inventati ma plausibili: pochi POD, pochi mesi, numeri in kWh.
Il generatore è deterministico (seed fisso), così i file sono sempre gli stessi.
Dati/fallback/ contiene dati di esempio con lo stesso schema delle API reali (Open-Meteo e
Regione Lombardia): servono quando la rete non c'è; `scarica_fallback.py` li sostituisce con i veri.

    uv run python _build/genera_dati.py             # tutti i dati di esempio
    uv run python _build/genera_dati.py fallback    # solo Dati/fallback/
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATI = ROOT / "Dati"
rng = np.random.default_rng(42)

FASCE = ["F1", "F2", "F3"]
ZONE = ["NORD", "CNOR", "CSUD", "SUD", "SICI", "SARD"]

CLIENTI = [
    ("IT001E12345678", "Caffè del Corso", "Monza"),
    ("IT001E23456789", "Lavanderia Più", "Lodi"),
    ("IT001E34567890", "Società Agricola Verdi", "Cremona"),
    ("IT001E45678901", "Panificio Rè", "Cantù"),
    ("IT001E56789012", "Officina Meccanica Fumagalli", "Lecco"),
    ("IT001E67890123", "Studio Dentistico Colombo", "Varese"),
]

COMUNI = [
    ("Milano", "MI", 45.4642, 9.1900), ("Bergamo", "BG", 45.6983, 9.6773), ("Brescia", "BS", 45.5416, 10.2118),
    ("Como", "CO", 45.8081, 9.0852), ("Cremona", "CR", 45.1333, 10.0227), ("Lecco", "LC", 45.8566, 9.3977),
    ("Lodi", "LO", 45.3139, 9.5034), ("Mantova", "MN", 45.1564, 10.7914), ("Monza", "MB", 45.5845, 9.2744),
    ("Pavia", "PV", 45.1847, 9.1582), ("Sondrio", "SO", 46.1699, 9.8713), ("Varese", "VA", 45.8206, 8.8251),
    ("Busto Arsizio", "VA", 45.6120, 8.8498), ("Legnano", "MI", 45.5977, 8.9152), ("Vigevano", "PV", 45.3149, 8.8544),
    ("Crema", "CR", 45.3617, 9.6868), ("Treviglio", "BG", 45.5222, 9.5927), ("Desenzano del Garda", "BS", 45.4698, 10.5359),
    ("Rho", "MI", 45.5317, 9.0405), ("Gallarate", "VA", 45.6606, 8.7918), ("Saronno", "VA", 45.6260, 9.0362),
    ("Voghera", "PV", 44.9925, 9.0097), ("Abbiategrasso", "MI", 45.3989, 8.9183), ("Cantù", "CO", 45.7375, 9.1308),
    ("Lissone", "MB", 45.6116, 9.2420), ("Cernusco sul Naviglio", "MI", 45.5236, 9.3350), ("Rozzano", "MI", 45.3828, 9.1565),
    ("Segrate", "MI", 45.4913, 9.2978), ("Chiari", "BS", 45.5361, 9.9306), ("Suzzara", "MN", 44.9917, 10.7450),
]


def letture_pod() -> None:
    """CSV 'all'italiana': separatore ';', virgola decimale, date gg/mm/aaaa, codifica latin-1."""
    righe = []
    quote = {"F1": 0.45, "F2": 0.30, "F3": 0.25}
    base = {pod: rng.uniform(600, 2500) for pod, _, _ in CLIENTI}
    for pod, cliente, _ in CLIENTI:
        for mese in range(1, 13):
            stagione = 1 + 0.25 * np.cos(2 * np.pi * (mese - 1) / 12)  # più consumo d'inverno
            tot = base[pod] * stagione * rng.uniform(0.9, 1.1)
            for fascia in FASCE:
                kwh = tot * quote[fascia] * rng.uniform(0.95, 1.05)
                if pod == "IT001E45678901" and mese == 7 and fascia == "F1":
                    kwh *= 10  # una lettura digitata male: l'anomalia da trovare
                righe.append({"pod": pod, "cliente": cliente, "data": f"01/{mese:02d}/2025", "fascia": fascia, "kwh": round(kwh, 1)})
    df = pd.DataFrame(righe)
    df.to_csv(DATI / "letture_pod_2025.csv", sep=";", decimal=",", index=False, encoding="latin-1")


def impianti_fv() -> None:
    """Anagrafica di 40 impianti fotovoltaici (coordinate approssimative del comune)."""
    righe = []
    for i in range(40):
        comune, prov, lat, lon = COMUNI[i % len(COMUNI)]
        righe.append({
            "id_impianto": f"FV{i + 1:03d}",
            "comune": comune,
            "provincia": prov,
            "kwp": float(rng.choice([3.0, 4.5, 6.0, 10.0, 20.0, 50.0, 99.0, 200.0], p=[.2, .2, .2, .15, .1, .08, .05, .02])),
            "anno_allaccio": int(rng.integers(2011, 2026)),
            "lat": round(lat + rng.normal(0, 0.01), 4),
            "lon": round(lon + rng.normal(0, 0.01), 4),
        })
    pd.DataFrame(righe).to_csv(DATI / "impianti_fv.csv", index=False)


def bolletta_excel() -> None:
    """Excel a tre fogli: consumi mensili per fascia, listino, anagrafica."""
    consumi = []
    for pod, _, _ in CLIENTI:
        base = rng.uniform(500, 2000)
        for mese in range(1, 13):
            stag = 1 + 0.25 * np.cos(2 * np.pi * (mese - 1) / 12)
            tot = base * stag
            consumi.append({"pod": pod, "mese": f"2025-{mese:02d}",
                            "F1": round(tot * 0.45 * rng.uniform(.9, 1.1), 1),
                            "F2": round(tot * 0.30 * rng.uniform(.9, 1.1), 1),
                            "F3": round(tot * 0.25 * rng.uniform(.9, 1.1), 1)})
    listino = pd.DataFrame({"fascia": FASCE, "eur_kwh": [0.21, 0.19, 0.17]})
    anagrafica = pd.DataFrame([{"pod": p, "cliente": c, "comune": m} for p, c, m in CLIENTI])
    with pd.ExcelWriter(DATI / "bolletta_esempio.xlsx") as w:
        pd.DataFrame(consumi).to_excel(w, sheet_name="Consumi", index=False)
        listino.to_excel(w, sheet_name="Listino", index=False)
        anagrafica.to_excel(w, sheet_name="Anagrafica", index=False)


def database() -> None:
    """SQLite con tre tabelle collegate: clienti -> pod -> letture (giornaliere, marzo 2025)."""
    path = DATI / "utility.db"
    if path.exists():
        path.unlink()
    clienti = pd.DataFrame({
        "id_cliente": range(1, 21),
        "ragione_sociale": [f"{n} {c}" for n, c in zip(
            ["Panificio", "Bar", "Officina", "Studio", "Azienda Agricola", "Lavanderia", "Ristorante", "Falegnameria",
             "Farmacia", "Palestra", "Supermercato", "Cartoleria", "Hotel", "Tipografia", "Caseificio", "Autofficina",
             "Pasticceria", "Libreria", "Serra", "Carrozzeria"],
            ["Rossi", "Centrale", "Bianchi", "Verdi", "Brambilla", "Splendor", "Da Gino", "Colombo", "San Marco",
             "Energy", "Il Mercato", "Ferrari", "Belvedere", "Moderna", "Lombardo", "Fumagalli", "Dolce Vita",
             "Il Segnalibro", "Fiorita", "Galli"])],
        "comune": [COMUNI[i % 12][0] for i in range(20)],
    })
    pods = []
    for i in range(30):
        pods.append({"pod": f"IT001E{10000000 + i * 7919:08d}", "id_cliente": int(rng.integers(1, 21)),
                     "potenza_kw": float(rng.choice([3.0, 6.0, 10.0, 15.0, 30.0, 50.0]))})
    pods = pd.DataFrame(pods)
    giorni = pd.date_range("2025-03-01", "2025-03-31", freq="D")
    letture = []
    for _, r in pods.iterrows():
        media = r["potenza_kw"] * rng.uniform(3, 6)  # kWh al giorno
        for g in giorni:
            fattore = 0.6 if g.dayofweek >= 5 else 1.0
            letture.append({"pod": r["pod"], "data": g.strftime("%Y-%m-%d"), "kwh": round(media * fattore * rng.uniform(.85, 1.15), 1)})
    letture = pd.DataFrame(letture)
    con = sqlite3.connect(path)
    clienti.to_sql("clienti", con, index=False)
    pods.to_sql("pod", con, index=False)
    letture.to_sql("letture", con, index=False)
    con.close()


def prezzi_zonali() -> None:
    """Prezzi orari dell'energia per zona di mercato, una settimana (valori inventati), con due ore mancanti."""
    ore = pd.date_range("2025-06-02 00:00", "2025-06-08 23:00", freq="h")
    offset = {"NORD": 0, "CNOR": 2, "CSUD": 3, "SUD": -4, "SICI": 12, "SARD": 6}
    righe = []
    for z in ZONE:
        for t in ore:
            giornaliero = 25 * np.sin(2 * np.pi * (t.hour - 6) / 24) + (8 if 17 <= t.hour <= 21 else 0)
            weekend = -15 if t.dayofweek >= 5 else 0
            prezzo = 105 + giornaliero + weekend + offset[z] + rng.normal(0, 4)
            righe.append({"timestamp": t.strftime("%Y-%m-%d %H:%M"), "zona": z, "eur_mwh": round(prezzo, 2)})
    df = pd.DataFrame(righe)
    df = df[~((df["zona"] == "NORD") & df["timestamp"].isin(["2025-06-04 14:00", "2025-06-04 15:00"]))]
    df.to_csv(DATI / "prezzi_zonali_2025_settimana.csv", index=False)


POD_COMPITO = [
    ("IT001E31045201", "Panificio Rè", "Cantù", 15.0),
    ("IT001E31045877", "Lavanderia Più", "Lodi", 10.0),
    ("IT001E31046310", "Bar Centrale", "Monza", 6.0),
    ("IT001E31047092", "Officina Meccanica Fumagalli", "Lecco", 30.0),
    ("IT001E31047555", "Studio Dentistico Colombo", "Varese", 6.0),
    ("IT001E31048128", "Supermercato Il Mercato", "Crema", 50.0),
    ("IT001E31048743", "Palestra Energy", "Rho", 15.0),
    ("IT001E31049306", "Serra Fiorita", "Mantova", 30.0),
]
POD_ANOMALO, GIORNO_ANOMALO = "IT001E31047092", "12/03/2025"


def compito() -> None:
    """Cartella Dati/homework/: letture giornaliere di marzo (e aprile) di 8 POD, un Excel a due fogli, un SQLite."""
    cartella = DATI / "homework"
    cartella.mkdir(exist_ok=True)
    media = {pod: potenza * rng.uniform(2.5, 5.0) for pod, _, _, potenza in POD_COMPITO}  # kWh al giorno

    def letture(inizio: str, fine: str) -> pd.DataFrame:
        righe = []
        for pod, _, _, _ in POD_COMPITO:
            for g in pd.date_range(inizio, fine, freq="D"):
                fattore = 0.6 if g.dayofweek >= 5 else 1.0
                kwh = media[pod] * fattore * rng.uniform(0.85, 1.15)
                data = g.strftime("%d/%m/%Y")
                if pod == POD_ANOMALO and data == GIORNO_ANOMALO:
                    kwh *= 10  # uno zero di troppo: la lettura da trovare
                righe.append({"pod": pod, "data": data, "kwh": round(kwh, 1)})
        return pd.DataFrame(righe)

    letture("2025-03-01", "2025-03-31").to_csv(cartella / "letture_marzo.csv", sep=";", decimal=",", index=False)
    letture("2025-04-01", "2025-04-30").to_csv(cartella / "letture_aprile.csv", sep=";", decimal=",", index=False)

    anagrafica = pd.DataFrame([{"pod": p, "cliente": c, "comune": m} for p, c, m, _ in POD_COMPITO])
    listino = pd.DataFrame({"fascia": FASCE, "eur_kwh": [0.21, 0.19, 0.17]})
    with pd.ExcelWriter(cartella / "clienti.xlsx") as w:
        anagrafica.to_excel(w, sheet_name="Anagrafica", index=False)
        listino.to_excel(w, sheet_name="Listino", index=False)

    path = cartella / "anagrafica.db"
    if path.exists():
        path.unlink()
    pods = pd.DataFrame([{"pod": p, "cliente": c, "potenza_kw": k} for p, c, _, k in POD_COMPITO])
    con = sqlite3.connect(path)
    pods.to_sql("pod", con, index=False)
    con.close()


SENSORI = [
    # (idsensore, tipologia, stazione, provincia, quota m, lat, lng): sensori meteo ARPA della Lombardia
    ("2001", "Temperatura", "Milano via Brera", "MI", 122, 45.4719, 9.1881),
    ("2002", "Temperatura", "Legnano", "MI", 199, 45.5977, 8.9152),
    ("2003", "Temperatura", "Rho", "MI", 158, 45.5317, 9.0405),
    ("2004", "Temperatura", "Bergamo via Goisis", "BG", 249, 45.6983, 9.6773),
    ("2005", "Temperatura", "Treviglio", "BG", 126, 45.5222, 9.5927),
    ("2006", "Temperatura", "Brescia Broletto", "BS", 149, 45.5416, 10.2118),
    ("2007", "Temperatura", "Como Muggiò", "CO", 201, 45.8081, 9.0852),
    ("2008", "Temperatura", "Cremona", "CR", 45, 45.1333, 10.0227),
    ("2009", "Temperatura", "Lecco", "LC", 214, 45.8566, 9.3977),
    ("2010", "Temperatura", "Varese Vidoletti", "VA", 382, 45.8206, 8.8251),
    ("2011", "Temperatura", "Pavia Folperti", "PV", 77, 45.1847, 9.1582),
    ("2012", "Temperatura", "Sondrio", "SO", 307, 46.1699, 9.8713),
    ("2101", "Precipitazione", "Milano via Brera", "MI", 122, 45.4719, 9.1881),
    ("2102", "Precipitazione", "Bergamo via Goisis", "BG", 249, 45.6983, 9.6773),
    ("2103", "Precipitazione", "Lodi", "LO", 80, 45.3139, 9.5034),
    ("2104", "Precipitazione", "Mantova Lunetta", "MN", 19, 45.1564, 10.7914),
    ("2105", "Precipitazione", "Monza", "MB", 162, 45.5845, 9.2744),
    ("2106", "Precipitazione", "Sondrio", "SO", 307, 46.1699, 9.8713),
    ("2201", "Umidità Relativa", "Milano via Brera", "MI", 122, 45.4719, 9.1881),
    ("2202", "Umidità Relativa", "Brescia Broletto", "BS", 149, 45.5416, 10.2118),
    ("2203", "Umidità Relativa", "Cremona", "CR", 45, 45.1333, 10.0227),
    ("2204", "Umidità Relativa", "Varese Vidoletti", "VA", 382, 45.8206, 8.8251),
    ("2301", "Velocità Vento", "Milano Linate", "MI", 103, 45.4451, 9.2767),
    ("2302", "Velocità Vento", "Brescia Broletto", "BS", 149, 45.5416, 10.2118),
    ("2303", "Velocità Vento", "Mantova Lunetta", "MN", 19, 45.1564, 10.7914),
    ("2304", "Velocità Vento", "Lecco", "LC", 214, 45.8566, 9.3977),
    ("2401", "Radiazione Globale", "Milano via Brera", "MI", 122, 45.4719, 9.1881),
    ("2402", "Radiazione Globale", "Pavia Folperti", "PV", 77, 45.1847, 9.1582),
    ("2403", "Radiazione Globale", "Lodi", "LO", 80, 45.3139, 9.5034),
    ("2404", "Radiazione Globale", "Bergamo via Goisis", "BG", 249, 45.6983, 9.6773),
]
UNITA = {"Temperatura": "°C", "Precipitazione": "mm", "Umidità Relativa": "%",
         "Velocità Vento": "m/s", "Radiazione Globale": "W/m²"}


def temperatura_milano(tempi: pd.DatetimeIndex, r: np.random.Generator) -> np.ndarray:
    """Temperatura plausibile per Milano: stagione, ciclo del giorno, meteo del giorno, rumore."""
    giorno_anno = tempi.dayofyear.to_numpy() + tempi.hour.to_numpy() / 24
    stagione = -np.cos(2 * np.pi * (giorno_anno - 15) / 365.25)  # -1 a metà gennaio, +1 a metà luglio
    base = 14.5 + 11.5 * stagione  # circa 3 °C a gennaio, 26 °C a luglio
    # ciclo del giorno: minimo alle 6, massimo alle 15 (la salita dura 9 ore, la discesa 15)
    ora = (tempi.hour.to_numpy() + tempi.minute.to_numpy() / 60 - 6) % 24
    ciclo = np.where(ora <= 9, -np.cos(np.pi * ora / 9), np.cos(np.pi * (ora - 9) / 15))
    ampiezza = 5 + 1 * stagione  # escursione maggiore d'estate (4-6 °C)
    # il meteo del giorno (sereno, nuvoloso, fronte) sposta tutta la giornata
    giorni = tempi.normalize()
    anomalia = pd.Series(np.clip(r.normal(0, 1.8, giorni.nunique()), -3, 3), index=giorni.unique()).reindex(giorni).to_numpy()
    return base + ampiezza * ciclo + anomalia + r.normal(0, 0.3, len(tempi))


def meteo_open_meteo(r, tempi: pd.DatetimeIndex, variabili: dict, quale: str) -> dict:
    """Risposta nello stesso formato di Open-Meteo: metadati e `hourly` come dizionario di liste."""
    temp = temperatura_milano(tempi, r)
    hourly = {"time": [t.strftime("%Y-%m-%dT%H:%M") for t in tempi], "temperature_2m": [round(float(x), 1) for x in temp]}
    if quale == "previsione":
        umidita = np.clip(95 - 2.2 * (temp - temp.min()) + r.normal(0, 4, len(temp)), 25, 100)
        vento = np.clip(8 + 5 * np.sin(2 * np.pi * np.arange(len(temp)) / 61) + r.normal(0, 2, len(temp)), 0.5, None)
        hourly["relative_humidity_2m"] = [int(round(x)) for x in umidita]
        hourly["wind_speed_10m"] = [round(float(x), 1) for x in vento]
    return {
        "latitude": 45.47, "longitude": 9.19,
        "generationtime_ms": 0.5 if quale == "previsione" else 31.2,
        "utc_offset_seconds": 3600, "timezone": "Europe/Rome", "timezone_abbreviation": "GMT+1",
        "elevation": 122.0,
        "hourly_units": variabili,
        "hourly": hourly,
    }


def fallback() -> None:
    """Dati/fallback/: le risposte delle API del corso, inventate ma con lo stesso schema di quelle vere."""
    r = np.random.default_rng(7)
    cartella = DATI / "fallback"
    cartella.mkdir(parents=True, exist_ok=True)

    def salva(nome: str, dati) -> None:
        (cartella / nome).write_text(json.dumps(dati, ensure_ascii=False), encoding="utf-8")

    # Open-Meteo archivio: temperatura oraria a Milano, 2024-2025 (17544 ore, ora locale)
    ore = pd.date_range("2024-01-01 00:00", "2025-12-31 23:00", freq="h")
    salva("meteo_milano_2024_2025.json",
          meteo_open_meteo(r, ore, {"time": "iso8601", "temperature_2m": "°C"}, "archivio"))

    # Open-Meteo previsione: 7 giorni a partire da oggi alle 00:00 (168 ore)
    inizio = pd.Timestamp(date.today())
    ore = pd.date_range(inizio, periods=7 * 24, freq="h")
    unita = {"time": "iso8601", "temperature_2m": "°C", "relative_humidity_2m": "%", "wind_speed_10m": "km/h"}
    salva("meteo_milano_previsione.json", meteo_open_meteo(r, ore, unita, "previsione"))

    # Regione Lombardia: Socrata restituisce ogni campo come testo, anche numeri e date
    sensori = []
    for i, (idsensore, tipologia, stazione, provincia, quota, lat, lng) in enumerate(SENSORI):
        sensori.append({
            "idsensore": idsensore, "tipologia": tipologia, "unit_dimisura": UNITA[tipologia],
            "idstazione": str(500 + i), "nomestazione": stazione, "quota": str(quota), "provincia": provincia,
            "storico": "N", "datastart": f"{1995 + i % 20}-0{1 + i % 9}-1{i % 10}T00:00:00.000",
            "cgb_nord": str(round(lat * 111_000)), "cgb_est": str(round(lng * 78_000)),
            "lng": str(lng), "lat": str(lat),
            "location": {"type": "Point", "coordinates": [lng, lat]},
        })
    salva("lombardia_sensori.json", sensori)

    # Misure del sensore 2001 (Milano, temperatura): giugno 2025, una ogni 10 minuti, già in ordine di `data`
    tempi = pd.date_range("2025-06-01 00:00", "2025-06-30 23:50", freq="10min")
    valori = np.round(temperatura_milano(tempi, r) - 1.5, 1)  # giugno è più fresco di luglio
    mancanti = {"2025-06-03T14:20:00", "2025-06-03T14:30:00", "2025-06-05T09:10:00"}  # -9999: misura mancante
    misure = []
    for t, v in zip(tempi, valori):
        data = t.strftime("%Y-%m-%dT%H:%M:%S.000")
        buona = data[:19] not in mancanti
        misure.append({"idsensore": "2001", "data": data, "valore": str(float(v)) if buona else "-9999",
                       "stato": "VA" if buona else "NA", "idoperatore": "1"})
    salva("lombardia_misure_2001.json", misure)


if __name__ == "__main__":
    DATI.mkdir(exist_ok=True)
    if sys.argv[1:] == ["fallback"]:
        fallback()
        sys.exit()
    letture_pod()
    impianti_fv()
    bolletta_excel()
    database()
    prezzi_zonali()
    compito()
    fallback()
    print("Dati di esempio generati in", DATI)
