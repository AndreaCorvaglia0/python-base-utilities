"""Il conto della spesa della settimana: totale, prezzo medio e una tabella in Excel."""
from calcoli import totale, prezzo_medio
import pandas as pd

spesa = {"pane": 2.40, "latte": 1.15, "mele": 3.20, "caffè": 4.50, "pasta": 1.85}
prezzi = list(spesa.values())

print(f"Totale della spesa: {totale(prezzi):.2f} euro")
print(f"Prezzo medio di un prodotto: {prezzo_medio(prezzi):.2f} euro, calcolato su {len(prezzi)} prodotti")

tabella = pd.DataFrame({"prodotto": list(spesa.keys()), "prezzo": prezzi})
tabella.to_excel("spesa.xlsx", index=False)
print("La tabella della spesa è nel file spesa.xlsx")
