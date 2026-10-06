"""
Scarica una volta le risposte delle API usate nel corso e le salva in Dati/fallback/.

Serve come rete di sicurezza in aula: se il wifi non collabora, i notebook possono
leggere i file locali al posto dell'API, e il codice a valle resta identico.

    uv run python _build/scarica_fallback.py
"""

from __future__ import annotations

import json
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Dati" / "fallback"
OUT.mkdir(parents=True, exist_ok=True)


def get_json(url: str, params: dict) -> dict | list:
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def salva(nome: str, dati) -> None:
    (OUT / nome).write_text(json.dumps(dati, ensure_ascii=False), encoding="utf-8")
    print("salvato", OUT / nome)


# Open-Meteo: temperatura oraria a Milano, 2024-2025 (per il capstone)
salva("meteo_milano_2024_2025.json", get_json(
    "https://archive-api.open-meteo.com/v1/archive",
    {"latitude": 45.4642, "longitude": 9.19, "start_date": "2024-01-01", "end_date": "2025-12-31",
     "hourly": "temperature_2m", "timezone": "Europe/Rome"},
))

# Open-Meteo: previsione dei prossimi 7 giorni a Milano (per gli esercizi sulle API)
salva("meteo_milano_previsione.json", get_json(
    "https://api.open-meteo.com/v1/forecast",
    {"latitude": 45.4642, "longitude": 9.19, "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
     "timezone": "Europe/Rome", "forecast_days": 7},
))

# Regione Lombardia: anagrafica dei sensori meteo (tutti) e misure di un sensore di temperatura
salva("lombardia_sensori.json", get_json(
    "https://www.dati.lombardia.it/resource/nf78-nj6b.json", {"$limit": 5000},
))
salva("lombardia_misure_2001.json", get_json(
    "https://www.dati.lombardia.it/resource/647i-nhxk.json",
    {"idsensore": "2001", "$order": "data", "$limit": 50000},
))
