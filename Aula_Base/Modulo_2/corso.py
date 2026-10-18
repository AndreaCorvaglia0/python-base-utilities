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

    '4.1': ('Esercizio 4.1', r'''
assert sopra_soglia == ["alimentari", "ristoranti", "regali"], "❌ sopra_soglia: le tre categorie con più di 100 euro"
assert round(totale, 1) == 805.8, "❌ totale: la somma di tutti i valori del dizionario"
'''),
    '4.2': ('Esercizio 4.2', r'''
assert costo(100) == 25.0, "❌ costo(100) deve dare 25.0: la tariffa predefinita è 0.25"
assert costo(100, tariffa=0.19) == 19.0, "❌ costo(100, tariffa=0.19) deve dare 19.0: usa la tariffa ricevuta"
assert costo_abbonato == 7.98, "❌ costo_abbonato: 42 minuti a 0.19 euro al minuto"
'''),
    '5.1': ('Esercizio 5.1', r'''
assert anni_alla_pensione == 46, "❌ anni_alla_pensione: eta è un testo, convertilo con int()"
assert len(citta) == 4 and citta[-1] == "Napoli", "❌ citta: una lista si allunga con append"
'''),
    '5.2': ('Esercizio 5.2', r'''
assert risposte["obbligatorio"] == "iterable", "❌ obbligatorio: il nome del parametro che nella firma non ha ="
assert risposte["default_reverse"] is False, "❌ default_reverse: il valore dopo reverse=, senza virgolette"
assert dal_piu_alto == [30, 28, 25, 18], "❌ dal_piu_alto: passa reverse=True per nome"
'''),
    '6.1': ('Esercizio 6.1', r'''
assert letture.shape == (248, 3), "❌ letture: 248 righe e 3 colonne, controlla sep"
assert letture["kwh"].dtype == "float64", "❌ letture: kwh deve essere numerica, controlla decimal"
'''),
    '6.2': ('Esercizio 6.2', r'''
assert set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ listino: è il foglio Listino? Controlla sheet_name"
assert list(officina["potenza_kw"]) == [30.0], "❌ officina: una riga sola, presa dalla tabella pod con il WHERE"
'''),
    'A1.1': ('Esercizio A1.1', r'''
assert da_comprare == {"pane", "latte", "mele", "caffè", "pasta", "olio"}, "❌ da_comprare: unisci i due set"
assert in_comune == {"latte", "mele"}, "❌ in_comune: usa intersection()"
assert quanti == 6, "❌ Le cose da comprare sono 6"
'''),
    'A1.2': ('Esercizio A1.2', r'''
assert mesi == 7, "❌ mesi: servono 7 mesi, il settimo porta a 1050 euro"
assert risparmio == 1050, "❌ risparmio: 150 euro per 7 mesi fanno 1050"
'''),
    'E2.1': ('Esercizio E2.1', r'''
assert inverti_stringa("Python") == "nohtyP", "❌ inverti_stringa('Python') deve restituire 'nohtyP': usa stringa[::-1]"
'''),
    'E2.2': ('Esercizio E2.2', r'''
assert paesi_capitale_pari(g10) == ['Canada', 'Francia', 'Italia', 'Regno Unito', 'Stati Uniti', 'Spagna'], "❌ Controlla la condizione: len(capitale) % 2 == 0"
'''),
    'E2.3': ('Esercizio E2.3', r'''
assert trova_palindrome(['ciao', 'anna', 'radar', 'gatto', 'osso', 'madam']) == ['anna', 'radar', 'osso', 'madam'], "❌ Le palindrome della lista sono anna, radar, osso e madam"
'''),
    'E2.4': ('Esercizio E2.4', r'''
assert letture["kwh"].dtype == "float64", "❌ kwh non è numerica: manca decimal=','"
assert righe == 216, "❌ Il file ha 216 righe: contale con len(letture)"
assert round(totale_kwh, 1) == 134507.7, "❌ totale_kwh: somma la colonna kwh"
'''),
    'E2.5': ('Esercizio E2.5', r'''
assert len(listino) == 3 and prezzo_f1 == 0.21, "❌ listino: leggi il foglio Listino; prezzo_f1 è il primo valore di eur_kwh"
assert n_letture == 930 and list(letture_db.columns) == ["pod", "data", "kwh"], "❌ letture_db: leggi tutta la tabella letture con SELECT *"
assert round(kwh_marzo, 1) == 69880.1, "❌ kwh_marzo: somma la colonna kwh di letture_db"
'''),
}

# Le soluzioni degli esercizi che le mostrano a richiesta, codificate perché non si leggano per caso.
SOLUZIONI = {
    'E2.1': ('Esercizio E2.1', 'ZGVmIGludmVydGlfc3RyaW5nYShzdHJpbmdhKToKICAgIHJldHVybiBzdHJpbmdhWzo6LTFdCgpwcmludChpbnZlcnRpX3N0cmluZ2EoIlB5dGhvbiIpKSAgIyBPdXRwdXQ6IG5vaHR5UA=='),
    'E2.2': ('Esercizio E2.2', 'ZGVmIHBhZXNpX2NhcGl0YWxlX3BhcmkoZGl6aW9uYXJpbyk6CiAgICByaXN1bHRhdG8gPSBbXQogICAgZm9yIHBhZXNlLCBjYXBpdGFsZSBpbiBkaXppb25hcmlvLml0ZW1zKCk6CiAgICAgICAgaWYgbGVuKGNhcGl0YWxlKSAlIDIgPT0gMDoKICAgICAgICAgICAgcmlzdWx0YXRvLmFwcGVuZChwYWVzZSkKICAgIHJldHVybiByaXN1bHRhdG8KCmcxMCA9IHsKICAgICdDYW5hZGEnOiAnT3R0YXdhJywKICAgICdGcmFuY2lhJzogJ1BhcmlnaScsCiAgICAnR2VybWFuaWEnOiAnQmVybGlubycsCiAgICAnSXRhbGlhJzogJ1JvbWEnLAogICAgJ0dpYXBwb25lJzogJ1Rva3lvJywKICAgICdSZWdubyBVbml0byc6ICdMb25kcmEnLAogICAgJ1N0YXRpIFVuaXRpJzogJ1dhc2hpbmd0b24nLAogICAgJ1NwYWduYSc6ICdNYWRyaWQnLAogICAgJ1BhZXNpIEJhc3NpJzogJ0Ftc3RlcmRhbScsCiAgICAnQ29yZWEgZGVsIFN1ZCc6ICdTZW91bCcKfQoKcHJpbnQocGFlc2lfY2FwaXRhbGVfcGFyaShnMTApKSAgIyBPdXRwdXQ6IFsnQ2FuYWRhJywgJ0ZyYW5jaWEnLCAnSXRhbGlhJywgJ1JlZ25vIFVuaXRvJywgJ1N0YXRpIFVuaXRpJywgJ1NwYWduYSdd'),
    'E2.3': ('Esercizio E2.3', 'ZGVmIHRyb3ZhX3BhbGluZHJvbWUobGlzdGFfcGFyb2xlKToKICAgIHBhbGluZHJvbWUgPSBbXQogICAgZm9yIHBhcm9sYSBpbiBsaXN0YV9wYXJvbGU6CiAgICAgICAgaWYgcGFyb2xhID09IHBhcm9sYVs6Oi0xXToKICAgICAgICAgICAgcGFsaW5kcm9tZS5hcHBlbmQocGFyb2xhKQogICAgcmV0dXJuIHBhbGluZHJvbWUKCmxpc3RhX3Bhcm9sZSA9IFsnY2lhbycsICdhbm5hJywgJ3JhZGFyJywgJ2dhdHRvJywgJ29zc28nLCAnbWFkYW0nXQpwcmludCh0cm92YV9wYWxpbmRyb21lKGxpc3RhX3Bhcm9sZSkpICAjIE91dHB1dDogWydhbm5hJywgJ3JhZGFyJywgJ29zc28nLCAnbWFkYW0nXQ=='),
    'E2.4': ('Esercizio E2.4', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL2xldHR1cmVfcG9kXzIwMjUuY3N2Iiwgc2VwPSI7IiwgZGVjaW1hbD0iLCIsIGVuY29kaW5nPSJsYXRpbi0xIikKbGV0dHVyZS5pbmZvKCkKCnJpZ2hlID0gbGVuKGxldHR1cmUpCnRvdGFsZV9rd2ggPSBsZXR0dXJlWyJrd2giXS5zdW0oKQoKcHJpbnQocmlnaGUsIHJvdW5kKHRvdGFsZV9rd2gsIDEpKSAgIyBPdXRwdXQ6IDIxNiAxMzQ1MDcuNw=='),
    'E2.5': ('Esercizio E2.5', 'aW1wb3J0IHNxbGl0ZTMKCmltcG9ydCBwYW5kYXMgYXMgcGQKCmxpc3Rpbm8gPSBwZC5yZWFkX2V4Y2VsKCIuLi9EYXRpL2JvbGxldHRhX2VzZW1waW8ueGxzeCIsIHNoZWV0X25hbWU9Ikxpc3Rpbm8iKQpwcmV6em9fZjEgPSBsaXN0aW5vWyJldXJfa3doIl1bMF0KCmNvbiA9IHNxbGl0ZTMuY29ubmVjdCgiLi4vRGF0aS91dGlsaXR5LmRiIikKbGV0dHVyZV9kYiA9IHBkLnJlYWRfc3FsKCJTRUxFQ1QgKiBGUk9NIGxldHR1cmUiLCBjb24pCmNvbi5jbG9zZSgpCgpuX2xldHR1cmUgPSBsZW4obGV0dHVyZV9kYikKa3doX21hcnpvID0gbGV0dHVyZV9kYlsia3doIl0uc3VtKCkKCnByaW50KHByZXp6b19mMSkgICAgICAgICAgICAgICAgICAgICAgICAjIE91dHB1dDogMC4yMQpwcmludChuX2xldHR1cmUsIHJvdW5kKGt3aF9tYXJ6bywgMSkpICAgIyBPdXRwdXQ6IDkzMCA2OTg4MC4x'),
    'E2.6': ('Esercizio E2.6', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKZGVmIGxlZ2dpX2Nzdl9pdGFsaWFubyhwZXJjb3Jzbyk6CiAgICAiIiJMZWdnZSB1biBDU1Ygc2FsdmF0byBkYSBFeGNlbCBpbiBpdGFsaWFubyBlIGxvIHJlc3RpdHVpc2NlIGNvbWUgRGF0YUZyYW1lLiIiIgogICAgcmV0dXJuIHBkLnJlYWRfY3N2KHBlcmNvcnNvLCBzZXA9IjsiLCBkZWNpbWFsPSIsIiwgZW5jb2Rpbmc9ImxhdGluLTEiKQoKbGV0dHVyZSA9IGxlZ2dpX2Nzdl9pdGFsaWFubygiLi4vRGF0aS9sZXR0dXJlX3BvZF8yMDI1LmNzdiIpCmxldHR1cmUuaW5mbygp'),
}
