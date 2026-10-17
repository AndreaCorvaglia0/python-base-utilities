"""Controllo degli esercizi del corso. Generato da _build/build.py: non modificare a mano.

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

    'Passo 1': ('Passo 1', r'''
assert cliente == "Panificio Rè", "❌ cliente: il valore della chiave 'cliente'"
assert kwh == 1654.2, "❌ kwh: il valore della chiave 'kwh_febbraio'"
assert round(costo, 2) == 347.38, "❌ costo: consumo per prezzo"
'''),
    'Passo 2': ('Passo 2', r'''
assert ore_forno == [9.5, 11.2, 10.8, 9.9, 8.4], "❌ ore_forno: dalle 4 alle 8 comprese"
assert quota_forno == 57.0, "❌ quota_forno: kwh_forno diviso totale_giorno, per 100, arrotondato a un decimale"
assert picco == 11.2, "❌ picco: la lettura più alta, con max()"
'''),
    'Passo 3': ('Passo 3', r'''
assert sorted(sopra_soglia) == ["IT001E31047092", "IT001E31048128", "IT001E31049306"], "❌ sopra_soglia: i tre POD con più di 2000 kWh"
assert round(totale_kwh, 1) == 16244.1, "❌ totale_kwh: la somma di tutti i valori del dizionario"
'''),
    'Passo 4': ('Passo 4', r'''
assert costo(1000) == 210.0, "❌ costo(1000) deve dare 210.0: il prezzo di default è 0.21"
assert costo(1000, prezzo=0.19) == 190.0, "❌ costo(1000, prezzo=0.19) deve dare 190.0: usa il prezzo ricevuto"
assert costo_serra == 556.92, "❌ costo_serra: 3276.0 kWh a 0.17 euro/kWh"
'''),
    'Passo 5': ('Passo 5', r'''
assert letture["kwh"].dtype == "float64", "❌ letture: kwh deve essere numerica, controlla sep e decimal"
assert list(anomale["pod"]) == ["IT001E31047092"], "❌ anomale: una riga sola, quella dell'officina, con kwh > 500"
assert list(pd.read_csv("letture_anomale.csv").columns) == ["pod", "data", "kwh"], "❌ letture_anomale.csv: salva senza l'indice, con index=False"
'''),
    'Passo 6': ('Passo 6', r'''
assert set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ listino: è il foglio Listino? Controlla sheet_name"
assert list(officina["potenza_kw"]) == [30.0], "❌ officina: una riga sola, presa dalla tabella pod con il WHERE"
'''),
}

# Le soluzioni degli esercizi che le mostrano a richiesta, codificate perché non si leggano per caso.
SOLUZIONI = {
    'Passo 1': ('Passo 1', 'cGFuaWZpY2lvID0geyJjbGllbnRlIjogIlBhbmlmaWNpbyBSw6giLCAicG9kIjogIklUMDAxRTMxMDQ1MjAxIiwgImt3aF9mZWJicmFpbyI6IDE2NTQuMn0KcHJlenpvID0gMC4yMQoKY2xpZW50ZSA9IHBhbmlmaWNpb1siY2xpZW50ZSJdCmt3aCA9IHBhbmlmaWNpb1sia3doX2ZlYmJyYWlvIl0KY29zdG8gPSBrd2ggKiBwcmV6em8KcHJpbnQoY2xpZW50ZSwga3doLCAia1doIGEgZmViYnJhaW8sIGNvc3RvIiwgcm91bmQoY29zdG8sIDIpLCAiZXVybyIp'),
    'Passo 2': ('Passo 2', 'bGV0dHVyZSA9IFswLjgsIDAuNywgMC45LCAxLjEsIDkuNSwgMTEuMiwgMTAuOCwgOS45LCA4LjQsIDQuMiwgMy45LCAzLjUsCiAgICAgICAgICAgMy4xLCAyLjQsIDIuMCwgMS44LCAyLjIsIDIuNiwgMi45LCAxLjUsIDEuMiwgMS4wLCAwLjksIDAuOF0KCm9yZV9mb3JubyA9IGxldHR1cmVbNDo5XQprd2hfZm9ybm8gPSBzdW0ob3JlX2Zvcm5vKQp0b3RhbGVfZ2lvcm5vID0gc3VtKGxldHR1cmUpCnF1b3RhX2Zvcm5vID0gcm91bmQoa3doX2Zvcm5vIC8gdG90YWxlX2dpb3JubyAqIDEwMCwgMSkKcGljY28gPSBtYXgobGV0dHVyZSkKcHJpbnQoZiJGb3Jubzoge2t3aF9mb3JubzouMWZ9IGtXaCBzdSB7dG90YWxlX2dpb3JubzouMWZ9LCBpbCB7cXVvdGFfZm9ybm99JSAocGljY28ge3BpY2NvfSBrV2gpIik='),
    'Passo 3': ('Passo 3', 'Y29uc3VtaV9mZWJicmFpbyA9IHsKICAgICJJVDAwMUUzMTA0NTIwMSI6IDE2NTQuMiwKICAgICJJVDAwMUUzMTA0NTg3NyI6IDgxMi42LAogICAgIklUMDAxRTMxMDQ2MzEwIjogNjkwLjEsCiAgICAiSVQwMDFFMzEwNDcwOTIiOiAzMzEwLjQsCiAgICAiSVQwMDFFMzEwNDc1NTUiOiA0MzEuOCwKICAgICJJVDAwMUUzMTA0ODEyOCI6IDQ4OTAuNywKICAgICJJVDAwMUUzMTA0ODc0MyI6IDExNzguMywKICAgICJJVDAwMUUzMTA0OTMwNiI6IDMyNzYuMCwKfQpzb2dsaWEgPSAyMDAwCgpzb3ByYV9zb2dsaWEgPSBbXQpmb3IgcG9kLCBrd2ggaW4gY29uc3VtaV9mZWJicmFpby5pdGVtcygpOgogICAgaWYga3doID4gc29nbGlhOgogICAgICAgIHNvcHJhX3NvZ2xpYS5hcHBlbmQocG9kKQp0b3RhbGVfa3doID0gc3VtKGNvbnN1bWlfZmViYnJhaW8udmFsdWVzKCkpCnByaW50KGYie2xlbihzb3ByYV9zb2dsaWEpfSBQT0Qgc29wcmEgaSB7c29nbGlhfSBrV2gsIHN1IHt0b3RhbGVfa3doOi4xZn0ga1doIHRvdGFsaSIp'),
    'Passo 4': ('Passo 4', 'ZGVmIGNvc3RvKGt3aCwgcHJlenpvPTAuMjEpOgogICAgIiIiQ29zdG8gaW4gZXVybyBkaSB1biBjb25zdW1vIGluIGtXaCwgYXJyb3RvbmRhdG8gYWkgY2VudGVzaW1pLiIiIgogICAgcmV0dXJuIHJvdW5kKGt3aCAqIHByZXp6bywgMikKCgpjb3N0b19wYW5pZmljaW8gPSBjb3N0bygxNjU0LjIpCmNvc3RvX3NlcnJhID0gY29zdG8oMzI3Ni4wLCBwcmV6em89MC4xNykKcHJpbnQoZiJQYW5pZmljaW86IHtjb3N0b19wYW5pZmljaW99IGV1cm8sIFNlcnJhOiB7Y29zdG9fc2VycmF9IGV1cm8iKQ=='),
    'Passo 5': ('Passo 5', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KCIuLi8uLi9EYXRpL2hvbWV3b3JrL2xldHR1cmVfbWFyem8uY3N2Iiwgc2VwPSI7IiwgZGVjaW1hbD0iLCIpCmxldHR1cmUuaW5mbygpCnByaW50KGxldHR1cmUuaGVhZCgpKQpwcmludChsZXR0dXJlLmRlc2NyaWJlKCkpCgptYXNrID0gbGV0dHVyZVsia3doIl0gPiA1MDAKYW5vbWFsZSA9IGxldHR1cmVbbWFza10KYW5vbWFsZS50b19jc3YoImxldHR1cmVfYW5vbWFsZS5jc3YiLCBpbmRleD1GYWxzZSkKYW5vbWFsZQ=='),
    'Passo 6': ('Passo 6', 'aW1wb3J0IHBhbmRhcyBhcyBwZAppbXBvcnQgc3FsaXRlMwoKbGlzdGlubyA9IHBkLnJlYWRfZXhjZWwoIi4uLy4uL0RhdGkvaG9tZXdvcmsvY2xpZW50aS54bHN4Iiwgc2hlZXRfbmFtZT0iTGlzdGlubyIpCgpjb24gPSBzcWxpdGUzLmNvbm5lY3QoIi4uLy4uL0RhdGkvaG9tZXdvcmsvYW5hZ3JhZmljYS5kYiIpCm9mZmljaW5hID0gcGQucmVhZF9zcWwoIlNFTEVDVCAqIEZST00gcG9kIFdIRVJFIGNsaWVudGUgPSAnT2ZmaWNpbmEgTWVjY2FuaWNhIEZ1bWFnYWxsaSciLCBjb24pCmNvbi5jbG9zZSgpCgpwcmludChsaXN0aW5vKQpvZmZpY2luYQ=='),
}
