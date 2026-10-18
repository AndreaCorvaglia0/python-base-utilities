"""Controllo degli esercizi del corso. Il file è generato insieme ai notebook: non va modificato a mano.

In ogni notebook, sotto un esercizio:

    from corso import verifica
    verifica("7.1")

Se il risultato è giusto stampa ✅, altrimenti una riga che dice cosa non torna.
I controlli sono in fondo a questo file, uno per esercizio.
"""

import inspect


class VerificaFallita(Exception):
    """Il risultato dell'esercizio non è quello atteso: nel notebook compare una riga sola, senza traceback."""

    def _render_traceback_(self):
        return [f"\x1b[31m❌ {self}\x1b[0m"]


def verifica(codice: str) -> None:
    """Controlla le variabili del notebook per l'esercizio `codice`."""
    if codice not in VERIFICHE:
        raise VerificaFallita(f"Non c'è un controllo per {codice!r}")
    etichetta, controllo = VERIFICHE[codice]
    spazio = dict(inspect.currentframe().f_back.f_globals)
    try:
        exec(compile(controllo, f"<verifica {codice}>", "exec"), spazio)
    except AssertionError as e:
        msg = str(e).removeprefix("❌").strip() or "Il risultato non è quello atteso"
        raise VerificaFallita(msg) from None
    except NameError as e:
        nome = getattr(e, "name", None)
        msg = f"Non trovo la variabile `{nome}`: hai eseguito la cella dell'esercizio?" if nome else str(e)
        raise VerificaFallita(msg) from None
    except Exception as e:
        raise VerificaFallita(f"{type(e).__name__}: {e}") from None
    print(f"✅ {etichetta} completato")


def soluzione(codice: str) -> None:
    """Mostra la soluzione dell'esercizio `codice`, e soltanto quella."""
    import base64

    if codice not in SOLUZIONI:
        raise VerificaFallita(f"Non c'è una soluzione registrata per {codice!r}")
    etichetta, testo = SOLUZIONI[codice]
    sorgente = base64.b64decode(testo).decode("utf-8")
    try:
        from IPython.display import Code, display

        print(f"Soluzione · {etichetta}")
        display(Code(sorgente, language="python"))
    except ImportError:
        print(f"Soluzione · {etichetta}\n\n{sorgente}")


VERIFICHE = {

    '0.1': ('Esercizio 0.1', r'''
assert messaggio == "Primo comando Python del corso!", "❌ messaggio: copia il testo esatto, tra virgolette"
'''),
    '0.2': ('Esercizio 0.2', r'''
assert citta_domani == "Torino" and gradi_domani == 21, "❌ citta_domani vale \"Torino\", tra virgolette, e gradi_domani vale 21, senza virgolette"
'''),
    '1.1': ('Esercizio 1.1', r'''
assert ore == 2, "❌ ore: quante volte 60 sta in 137"
assert minuti == 17, "❌ minuti: il resto della divisione per 60"
'''),
    '1.2': ('Esercizio 1.2', r'''
assert cartellino == "MARIO ROSSI - LISBONA", "❌ cartellino: nome, cognome e città uniti con +, poi .upper()"
assert lunghezza == 21, "❌ lunghezza: i caratteri di cartellino, con len()"
'''),
    '2.1': ('Esercizio 2.1', r'''
assert prezzi.get("pepe nero") == 2.15 and prezzi["guanciale"] == 7.90, "❌ prezzi: aggiungi il pepe nero e correggi il prezzo del guanciale"
assert round(totale, 2) == 20.5, "❌ totale: somma i valori del dizionario aggiornato con sum(prezzi.values())"
assert prodotti == ["spaghetti", "guanciale", "uova", "pecorino", "pepe nero"], "❌ prodotti: usa list(prezzi.keys())"
'''),
    '2.2': ('Esercizio 2.2', r'''
assert tutti == lista_marta + lista_luca, "❌ tutti: le due liste unite con +"
assert carrello == {"spaghetti", "guanciale", "uova", "vino", "pecorino", "pane"} and quanti == 6, "❌ carrello: set(tutti) elimina i doppioni, quanti è la sua lunghezza"
assert isinstance(indirizzo, tuple) and civico == 14, "❌ indirizzo deve essere una tupla e civico il suo elemento di indice 1"
'''),
    '3.1': ('Esercizio 3.1', r'''
assert prezzo_scontato.__doc__, "❌ manca la docstring sotto il def"
assert round(prezzo_scontato(80, 15), 2) == 68.0, "❌ prezzo_scontato(80, 15) deve restituire 68.0, come f"
assert prezzo_scontato(prezzo=30, sconto_percentuale=50) == 15.0, "❌ i parametri si chiamano prezzo e sconto_percentuale"
'''),
    '3.2': ('Esercizio 3.2', r'''
assert prezzi == [3.5, 2.2, 4.8, 1.9, 14.9], "❌ prezzi: gli stessi cinque valori di P"
assert buono == 5, "❌ buono: i 5 euro in una variabile"
assert round(totale, 2) == round(t, 2), "❌ totale deve dare lo stesso risultato di t"
'''),
    'E1.1': ('Esercizio E1.1', r'''
import tomllib
from pathlib import Path

pyproject = Path("Script_uv_Ruff/esercizio/pyproject.toml")
assert pyproject.exists(), "❌ nella cartella esercizio non c'è ancora pyproject.toml: lancia uv init --bare nel terminale aperto in quella cartella"
assert nome_progetto.strip() == tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]["name"] == "esercizio", "❌ nome_progetto: la voce name di esercizio/pyproject.toml"
assert Path("Script_uv_Ruff/esercizio/uv.lock").exists(), "❌ nella cartella esercizio non c'è ancora uv.lock: dopo uv init --bare lancia di nuovo uv run main.py"
assert cartella_creata.strip().rstrip("/") == ".venv", "❌ cartella_creata: il nome nella riga Creating virtual environment at"
assert libreria_mancante.strip() == "pandas", "❌ libreria_mancante: il nome tra apici nell'ultima riga dell'errore"
'''),
    'E1.2': ('Esercizio E1.2', r'''
import tomllib
from pathlib import Path

progetto = tomllib.loads(Path("Script_uv_Ruff/esercizio/pyproject.toml").read_text(encoding="utf-8"))

librerie = progetto["project"]["dependencies"]
assert any(voce.startswith("pandas") for voce in librerie), "❌ pandas non è tra le dependencies di esercizio/pyproject.toml: lancia uv add pandas nella cartella esercizio"
assert seconda_libreria.strip() == "openpyxl", "❌ seconda_libreria: il nome tra apici nell'ultima riga del nuovo errore"
'''),
    'E1.3': ('Esercizio E1.3', r'''
import tomllib
from pathlib import Path

progetto = tomllib.loads(Path("Script_uv_Ruff/esercizio/pyproject.toml").read_text(encoding="utf-8"))

librerie = progetto["project"]["dependencies"]
assert any(voce.startswith("openpyxl") for voce in librerie), "❌ openpyxl non è tra le dependencies di esercizio/pyproject.toml: lancia uv add openpyxl"
assert riga_media.strip() == "Temperatura media della settimana: 15.0 gradi, calcolata su 5 giorni", "❌ riga_media: la riga copiata dal terminale, tale e quale"
'''),
    'E1.4': ('Esercizio E1.4', r'''
import tomllib
from pathlib import Path

progetto = tomllib.loads(Path("Script_uv_Ruff/esercizio/pyproject.toml").read_text(encoding="utf-8"))

sviluppo = progetto.get("dependency-groups", {}).get("dev", [])
meteo = Path("Script_uv_Ruff/esercizio/meteo.py").read_text(encoding="utf-8")
assert any(voce.startswith("ruff") for voce in sviluppo), "❌ ruff non è nel gruppo dev di esercizio/pyproject.toml: lancia uv add --dev ruff"
assert "sum(temperature) / len(temperature)" in meteo, "❌ meteo.py non è ancora in forma: lancia uv run ruff format nella cartella esercizio"
assert sorted(avvisi) == ["E501", "F401", "F841", "I001"], "❌ avvisi: i quattro codici stampati da uv run ruff check, come stringhe"
'''),
    'E1.5': ('Esercizio E1.5', r'''
from pathlib import Path

cartella = Path("Script_uv_Ruff/esercizio")
meteo = (cartella / "meteo.py").read_text(encoding="utf-8")
main = (cartella / "main.py").read_text(encoding="utf-8")
assert "import pandas as pd\n\nfrom meteo import" in main, "❌ main.py: gli import non sono ancora in ordine, lancia uv run ruff check --fix"
assert "import math" not in meteo and "giorni =" not in meteo and "giorni=" not in meteo, "❌ meteo.py contiene ancora import math o la variabile giorni"
assert all(len(r) <= 100 for r in main.splitlines()), "❌ main.py ha ancora una riga di più di 100 caratteri"
assert "\n\n\n\n" not in meteo, "❌ meteo.py ha ancora una riga vuota di troppo: lancia di nuovo uv run ruff format"
assert esito_finale.strip() == "All checks passed!", "❌ esito_finale: la riga stampata da uv run ruff check quando non trova problemi"
'''),
    'E1.6': ('Esercizio E1.6', r'''
from pathlib import Path

main = Path("Script_uv_Ruff/esercizio/main.py").read_text(encoding="utf-8")
riga_import = next((r for r in main.splitlines() if r.startswith("from meteo import")), "")
assert "minima" in riga_import, "❌ main.py: aggiungi minima alla riga from meteo import"
assert "minima(valori)" in main, "❌ main.py: manca il print che chiama minima(valori)"
assert riga_minima.strip() == "Temperatura minima della settimana: 13.8 gradi", "❌ riga_minima: la riga stampata dal terminale, tale e quale"
'''),
    'E1.7': ('Esercizio E1.7', r'''
from pathlib import Path

assert nome_importato.strip() == "meteo", "❌ nome_importato: il nome stampato con uv run main.py"
assert nome_lanciato.strip() == "__main__", "❌ nome_lanciato: il nome stampato con uv run meteo.py"
assert "Sto leggendo" not in Path("Script_uv_Ruff/esercizio/meteo.py").read_text(encoding="utf-8"), "❌ meteo.py: togli la riga di prova con il print, come dice l'ultimo passo"
'''),
    'E1.8': ('Esercizio E1.8', r'''
assert file_versioni.strip() == "uv.lock", "❌ file_versioni: il file in cui uv registra le versioni esatte di ogni libreria"
'''),
    'E1.9': ('Esercizio E1.9', r'''
assert valore_massimo == 25 and valore_minimo == 7 and differenza == 18, "❌ Controlla max(), min() e la differenza"
assert media == 14.0, "❌ media: (a + b + c) / 3, arrotondata con round(..., 1)"
'''),
    'E1.10': ('Esercizio E1.10', r'''
assert round(area, 6) == 78.539816, "❌ area: math.pi moltiplicato per raggio ** 2"
assert round(circonferenza, 6) == 31.415927, "❌ circonferenza: 2 * math.pi * raggio"
'''),
    'E1.11': ('Esercizio E1.11', r'''
assert lista_invertita == [5, 4, 3, 2, 1], "❌ lista_invertita: slicing con passo -1"
assert ultimi_due == [4, 5] and ogni_due == [1, 3, 5], "❌ ultimi_due è lista[-2:] e ogni_due è lista[::2]"
'''),
    'E1.12': ('Esercizio E1.12', r'''
assert elementi_pari == ["Martina", "Giulia", "Francesca", "Sara"], "❌ elementi_pari: lista[2::2]"
assert uomini == ["Luigi", "Marco", "Simone", "Alessandro", "Lorenzo"] and quanti_uomini == 5, "❌ uomini è lista[1::2] e quanti_uomini è len(uomini)"
'''),
    'E1.13': ('Esercizio E1.13', r'''
assert g8.get('Regno Unito') == 'Londra' and g8.get('Stati Uniti') == 'Washington, D.C.', "❌ Aggiungi le due coppie con g8[chiave] = valore"
assert quanti == 8 and capitale_italia == 'Roma', "❌ quanti è len(g8) e capitale_italia è g8['Italia']"
assert paesi[0] == 'Canada' and paesi[-1] == 'Stati Uniti', "❌ paesi: sorted(g8.keys())"
'''),
}

# Le soluzioni degli esercizi che le mostrano a richiesta, codificate perché non si leggano per caso.
SOLUZIONI = {
    'E1.1': ('Esercizio E1.1', 'IyBuZWwgdGVybWluYWxlLCBuZWxsYSBjYXJ0ZWxsYSBlc2VyY2l6aW8KIyAgIHV2IHJ1biBtYWluLnB5ICAgICAgICBmdW56aW9uYSwgY29uIGwnYW1iaWVudGUgZGVsIGNvcnNvCiMgICB1diBpbml0IC0tYmFyZSAgICAgICAgSW5pdGlhbGl6ZWQgcHJvamVjdCBgZXNlcmNpemlvYAojICAgdXYgcnVuIG1haW4ucHkKIyBDcmVhdGluZyB2aXJ0dWFsIGVudmlyb25tZW50IGF0OiAudmVudgojIC4uLgojIE1vZHVsZU5vdEZvdW5kRXJyb3I6IE5vIG1vZHVsZSBuYW1lZCAncGFuZGFzJwpub21lX3Byb2dldHRvID0gImVzZXJjaXppbyIKY2FydGVsbGFfY3JlYXRhID0gIi52ZW52IgpsaWJyZXJpYV9tYW5jYW50ZSA9ICJwYW5kYXMi'),
    'E1.2': ('Esercizio E1.2', 'IyBuZWwgdGVybWluYWxlLCBuZWxsYSBjYXJ0ZWxsYSBlc2VyY2l6aW8KIyAgIHV2IGFkZCBwYW5kYXMgICAgICAgIGluc3RhbGxhIHBhbmRhcyBlIGxlIGxpYnJlcmllIGRhIGN1aSBkaXBlbmRlCiMgICB1diBydW4gbWFpbi5weQojIFRlbXBlcmF0dXJhIG1hc3NpbWEgZGVsbGEgc2V0dGltYW5hOiAxNi4wIGdyYWRpCiMgVGVtcGVyYXR1cmEgbWVkaWEgZGVsbGEgc2V0dGltYW5hOiAxNS4wIGdyYWRpLCBjYWxjb2xhdGEgc3UgNSBnaW9ybmkKIyAuLi4KIyBNb2R1bGVOb3RGb3VuZEVycm9yOiBObyBtb2R1bGUgbmFtZWQgJ29wZW5weXhsJwpzZWNvbmRhX2xpYnJlcmlhID0gIm9wZW5weXhsIg=='),
    'E1.3': ('Esercizio E1.3', 'IyBuZWwgdGVybWluYWxlLCBuZWxsYSBjYXJ0ZWxsYSBlc2VyY2l6aW8KIyAgIHV2IGFkZCBvcGVucHl4bAojICAgdXYgcnVuIG1haW4ucHkKIyBUZW1wZXJhdHVyYSBtYXNzaW1hIGRlbGxhIHNldHRpbWFuYTogMTYuMCBncmFkaQojIFRlbXBlcmF0dXJhIG1lZGlhIGRlbGxhIHNldHRpbWFuYTogMTUuMCBncmFkaSwgY2FsY29sYXRhIHN1IDUgZ2lvcm5pCiMgTGEgdGFiZWxsYSBkZWxsZSB0ZW1wZXJhdHVyZSDDqCBuZWwgZmlsZSBtZXRlby54bHN4CnJpZ2FfbWVkaWEgPSAiVGVtcGVyYXR1cmEgbWVkaWEgZGVsbGEgc2V0dGltYW5hOiAxNS4wIGdyYWRpLCBjYWxjb2xhdGEgc3UgNSBnaW9ybmki'),
    'E1.4': ('Esercizio E1.4', 'IyBuZWwgdGVybWluYWxlLCBuZWxsYSBjYXJ0ZWxsYSBlc2VyY2l6aW8KIyAgIHV2IGFkZCAtLWRldiBydWZmCiMgICB1diBydW4gcnVmZiBmb3JtYXQgICAgICAgMiBmaWxlcyByZWZvcm1hdHRlZAojICAgdXYgcnVuIHJ1ZmYgY2hlY2sKIyBJMDAxIFsqXSBJbXBvcnQgYmxvY2sgaXMgdW4tc29ydGVkIG9yIHVuLWZvcm1hdHRlZCAgICAgICAgIC0tPiBtYWluLnB5CiMgRTUwMSBMaW5lIHRvbyBsb25nICgxMDIgPiAxMDApICAgICAgICAgICAgICAgICAgICAgICAgICAgICAtLT4gbWFpbi5weQojIEY0MDEgWypdIGBtYXRoYCBpbXBvcnRlZCBidXQgdW51c2VkICAgICAgICAgICAgICAgICAgICAgICAgLS0+IG1ldGVvLnB5CiMgRjg0MSBMb2NhbCB2YXJpYWJsZSBgZ2lvcm5pYCBpcyBhc3NpZ25lZCB0byBidXQgbmV2ZXIgdXNlZCAtLT4gbWV0ZW8ucHkKYXZ2aXNpID0gWyJJMDAxIiwgIkU1MDEiLCAiRjQwMSIsICJGODQxIl0='),
    'E1.5': ('Esercizio E1.5', 'IyBuZWwgdGVybWluYWxlLCBuZWxsYSBjYXJ0ZWxsYSBlc2VyY2l6aW8KIyAgIHV2IHJ1biBydWZmIGNoZWNrIC0tZml4ICAgICAgY29ycmVnZ2UgRjQwMSBlIEkwMDEKIyBhIG1hbm8sIGluIG1ldGVvLnB5LCBzaSBjYW5jZWxsYSBsYSByaWdhIGdpb3JuaSA9IGxlbih0ZW1wZXJhdHVyZSkKIyBhIG1hbm8sIGluIG1haW4ucHksIGlsIHByaW50IGRlbGxhIG1lZGlhIGRpdmVudGEKIyAgICAgcHJpbnQoCiMgICAgICAgICBmIlRlbXBlcmF0dXJhIG1lZGlhIGRlbGxhIHNldHRpbWFuYToge21lZGlhKHZhbG9yaSk6LjFmfSBncmFkaSwgIgojICAgICAgICAgZiJjYWxjb2xhdGEgc3Uge2xlbih2YWxvcmkpfSBnaW9ybmkiCiMgICAgICkKIyAgIHV2IHJ1biBydWZmIGZvcm1hdAojICAgdXYgcnVuIHJ1ZmYgY2hlY2sgICAgICAgICAgICBBbGwgY2hlY2tzIHBhc3NlZCEKIyAgIHV2IHJ1biBtYWluLnB5CmVzaXRvX2ZpbmFsZSA9ICJBbGwgY2hlY2tzIHBhc3NlZCEi'),
    'E1.6': ('Esercizio E1.6', 'IyBpbiBtYWluLnB5CiMgICBmcm9tIG1ldGVvIGltcG9ydCBtYXNzaW1hLCBtZWRpYSwgbWluaW1hCiMgICBwcmludChmIlRlbXBlcmF0dXJhIG1pbmltYSBkZWxsYSBzZXR0aW1hbmE6IHttaW5pbWEodmFsb3JpKTouMWZ9IGdyYWRpIikKIyBuZWwgdGVybWluYWxlLCBuZWxsYSBjYXJ0ZWxsYSBlc2VyY2l6aW8KIyAgIHV2IHJ1biBtYWluLnB5CiMgICB1diBydW4gcnVmZiBjaGVjayAgICAgICAgICAgIEFsbCBjaGVja3MgcGFzc2VkIQpyaWdhX21pbmltYSA9ICJUZW1wZXJhdHVyYSBtaW5pbWEgZGVsbGEgc2V0dGltYW5hOiAxMy44IGdyYWRpIg=='),
    'E1.7': ('Esercizio E1.7', 'IyBpbiBtZXRlby5weSwgc290dG8gbGEgZG9jc3RyaW5nCiMgICBwcmludChmIlN0byBsZWdnZW5kbyBtZXRlby5weSwgY29uIGlsIG5vbWUge19fbmFtZV9ffSIpCiMgbmVsIHRlcm1pbmFsZSwgbmVsbGEgY2FydGVsbGEgZXNlcmNpemlvCiMgICB1diBydW4gbWFpbi5weSAgICAgbGEgcHJpbWEgcmlnYSDDqDogU3RvIGxlZ2dlbmRvIG1ldGVvLnB5LCBjb24gaWwgbm9tZSBtZXRlbwojICAgdXYgcnVuIG1ldGVvLnB5ICAgIHN0YW1wYTogU3RvIGxlZ2dlbmRvIG1ldGVvLnB5LCBjb24gaWwgbm9tZSBfX21haW5fXwpub21lX2ltcG9ydGF0byA9ICJtZXRlbyIKbm9tZV9sYW5jaWF0byA9ICJfX21haW5fXyI='),
    'E1.8': ('Esercizio E1.8', 'IyBuZWwgcGFubmVsbG8gRXhwbG9yZXI6IHRhc3RvIGRlc3RybyBzdSBlc2VyY2l6aW8vLnZlbnYsIERlbGV0ZQojIG5lbCB0ZXJtaW5hbGUsIG5lbGxhIGNhcnRlbGxhIGVzZXJjaXppbwojICAgdXYgc3luYyAgICAgICAgICAgQ3JlYXRpbmcgdmlydHVhbCBlbnZpcm9ubWVudCBhdDogLnZlbnYsIHBvaSBpbnN0YWxsYSBsZSBzdGVzc2UgbGlicmVyaWUKIyAgIHV2IHJ1biBtYWluLnB5CmZpbGVfdmVyc2lvbmkgPSAidXYubG9jayI='),
    'E1.9': ('Esercizio E1.9', 'YSA9IDEwCmIgPSAyNQpjID0gNwoKdmFsb3JlX21hc3NpbW8gPSBtYXgoYSwgYiwgYykKdmFsb3JlX21pbmltbyA9IG1pbihhLCBiLCBjKQpkaWZmZXJlbnphID0gdmFsb3JlX21hc3NpbW8gLSB2YWxvcmVfbWluaW1vCm1lZGlhID0gcm91bmQoKGEgKyBiICsgYykgLyAzLCAxKQoKcHJpbnQoZiJWYWxvcmUgbWFzc2ltbzoge3ZhbG9yZV9tYXNzaW1vfSIpICAgIyBPdXRwdXQ6IFZhbG9yZSBtYXNzaW1vOiAyNQpwcmludChmIlZhbG9yZSBtaW5pbW86IHt2YWxvcmVfbWluaW1vfSIpICAgICAjIE91dHB1dDogVmFsb3JlIG1pbmltbzogNwpwcmludChmIkRpZmZlcmVuemE6IHtkaWZmZXJlbnphfSIpICAgICAgICAgICAjIE91dHB1dDogRGlmZmVyZW56YTogMTgKcHJpbnQoZiJNZWRpYToge21lZGlhfSIpICAgICAgICAgICAgICAgICAgICAgIyBPdXRwdXQ6IE1lZGlhOiAxNC4w'),
    'E1.10': ('Esercizio E1.10', 'aW1wb3J0IG1hdGgKCnJhZ2dpbyA9IDUKYXJlYSA9IG1hdGgucGkgKiByYWdnaW8gKiogMgpjaXJjb25mZXJlbnphID0gMiAqIG1hdGgucGkgKiByYWdnaW8KCnByaW50KGYiTCdhcmVhIGRlbCBjZXJjaGlvIMOoOiB7YXJlYTouMmZ9IikgICAjIE91dHB1dDogTCdhcmVhIGRlbCBjZXJjaGlvIMOoOiA3OC41NApwcmludChjaXJjb25mZXJlbnphKSAgICAgICAgICAgICAgICAgICAgICAgICAgIyBPdXRwdXQ6IDMxLjQxNTkyNjUzNTg5Nzkz'),
    'E1.11': ('Esercizio E1.11', 'bGlzdGEgPSBbMSwgMiwgMywgNCwgNV0KCmxpc3RhX2ludmVydGl0YSA9IGxpc3RhWzo6LTFdCnVsdGltaV9kdWUgPSBsaXN0YVstMjpdCm9nbmlfZHVlID0gbGlzdGFbOjoyXQoKcHJpbnQobGlzdGFfaW52ZXJ0aXRhKSAgIyBPdXRwdXQ6IFs1LCA0LCAzLCAyLCAxXQpwcmludCh1bHRpbWlfZHVlLCBvZ25pX2R1ZSkgICMgT3V0cHV0OiBbNCwgNV0gWzEsIDMsIDVd'),
    'E1.12': ('Esercizio E1.12', 'bGlzdGEgPSBbIkVsZW5hIiwgIkx1aWdpIiwgIk1hcnRpbmEiLCAiTWFyY28iLCAiR2l1bGlhIiwgIlNpbW9uZSIsICJGcmFuY2VzY2EiLCAiQWxlc3NhbmRybyIsICJTYXJhIiwgIkxvcmVuem8iXQoKZWxlbWVudGlfcGFyaSA9IGxpc3RhWzI6OjJdCnVvbWluaSA9IGxpc3RhWzE6OjJdCnF1YW50aV91b21pbmkgPSBsZW4odW9taW5pKQoKcHJpbnQoZWxlbWVudGlfcGFyaSkgICMgT3V0cHV0OiBbJ01hcnRpbmEnLCAnR2l1bGlhJywgJ0ZyYW5jZXNjYScsICdTYXJhJ10KcHJpbnQodW9taW5pLCBxdWFudGlfdW9taW5pKSAgIyBPdXRwdXQ6IFsnTHVpZ2knLCAnTWFyY28nLCAnU2ltb25lJywgJ0FsZXNzYW5kcm8nLCAnTG9yZW56byddIDU='),
    'E1.13': ('Esercizio E1.13', 'ZzggPSB7CiAgICAnQ2FuYWRhJzogJ090dGF3YScsCiAgICAnRnJhbmNpYSc6ICdQYXJpZ2knLAogICAgJ0dlcm1hbmlhJzogJ0Jlcmxpbm8nLAogICAgJ0l0YWxpYSc6ICdSb21hJywKICAgICdHaWFwcG9uZSc6ICdUb2t5bycsCiAgICAnUnVzc2lhJzogJ01vc2NhJwp9CgpnOFsnUmVnbm8gVW5pdG8nXSA9ICdMb25kcmEnCmc4WydTdGF0aSBVbml0aSddID0gJ1dhc2hpbmd0b24sIEQuQy4nCgpxdWFudGkgPSBsZW4oZzgpCmNhcGl0YWxlX2l0YWxpYSA9IGc4WydJdGFsaWEnXQpwYWVzaSA9IHNvcnRlZChnOC5rZXlzKCkpCgpwcmludChxdWFudGksIGNhcGl0YWxlX2l0YWxpYSkgICMgT3V0cHV0OiA4IFJvbWEKcHJpbnQocGFlc2kp'),
    'E1.14': ('Esercizio E1.14', 'ZzggPSB7CiAgICAnQ2FuYWRhJzogJ090dGF3YScsCiAgICAnRnJhbmNpYSc6ICdQYXJpZ2knLAogICAgJ0dlcm1hbmlhJzogJ0Jlcmxpbm8nLAogICAgJ0l0YWxpYSc6ICdSb21hJywKICAgICdHaWFwcG9uZSc6ICdUb2t5bycsCiAgICAnUnVzc2lhJzogJ01vc2NhJwp9CgpnOFsnUmVnbm8gVW5pdG8nXSA9ICdMb25kcmEnCmc4WydTdGF0aSBVbml0aSddID0gJ1dhc2hpbmd0b24sIEQuQy4nCgpwcmludChmIklsIEc4IGhhIHtsZW4oZzgpfSBwYWVzaSBlIGxhIGNhcGl0YWxlIGRlbCBHaWFwcG9uZSDDqCB7ZzhbJ0dpYXBwb25lJ119Iik='),
}
