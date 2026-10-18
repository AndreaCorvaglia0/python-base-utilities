"""Il riepilogo delle temperature della settimana: massima, media e una tabella in Excel."""
from meteo import media, massima
import pandas as pd

temperature = {"lunedì": 14.5, "martedì": 16.0, "mercoledì": 15.2, "giovedì": 13.8, "venerdì": 15.5}
valori = list(temperature.values())

print(f"Temperatura massima della settimana: {massima(valori):.1f} gradi")
print(f"Temperatura media della settimana: {media(valori):.1f} gradi, calcolata su {len(valori)} giorni")

tabella = pd.DataFrame({"giorno": list(temperature.keys()), "temperatura": valori})
tabella.to_excel("meteo.xlsx", index=False)
print("La tabella delle temperature è nel file meteo.xlsx")
