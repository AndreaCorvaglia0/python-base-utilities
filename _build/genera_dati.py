"""
Genera i dataset di esempio usati negli esercizi del corso (cartella Dati/).

Sono dati inventati ma plausibili: pochi POD, pochi mesi, numeri in kWh.
Il generatore è deterministico (seed fisso), così i file sono sempre gli stessi.

    uv run python _build/genera_dati.py
"""

from __future__ import annotations

import sqlite3
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


if __name__ == "__main__":
    DATI.mkdir(exist_ok=True)
    letture_pod()
    impianti_fv()
    bolletta_excel()
    database()
    prezzi_zonali()
    print("Dati di esempio generati in", DATI)
