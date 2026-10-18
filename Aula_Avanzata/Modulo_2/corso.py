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

    '4.1': ('Esercizio 4.1', r'''
assert sopra_soglia == ["alimentari", "ristoranti", "regali"], "❌ sopra_soglia: le tre categorie con più di 100 euro"
assert round(totale, 1) == 805.8, "❌ totale: la somma di tutti i valori del dizionario"
'''),
    '4.2': ('Esercizio 4.2', r'''
assert costo(100) == 25.0, "❌ costo(100) deve dare 25.0: la tariffa predefinita è 0.25 e lo sblocco 0"
assert costo(100, tariffa=0.19, sblocco=1) == 20.0, "❌ costo(100, tariffa=0.19, sblocco=1) deve dare 20.0"
assert costo_elettrica == 9.75, "❌ costo_elettrica: 35 minuti alla tariffa predefinita, più 1 euro"
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
assert leggi_tabella("pod").shape == (8, 3), "❌ leggi_tabella: deve restituire tutta la tabella, 8 righe e 3 colonne"
assert list(officina["potenza_kw"]) == [30.0], "❌ officina: una riga sola, quella dell'Officina Meccanica Fumagalli"
'''),
    '6.3': ('Esercizio 6.3', r'''
assert 0 < len(milano) < len(certificati), "❌ milano deve avere solo le righe della provincia di Milano"
assert len(co2_per_classe) > 1 and co2_per_classe.index.is_unique, "❌ co2_per_classe: una riga per classe energetica, con la media"
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
assert inverti_stringa("Python") == "nohtyP", "❌ inverti_stringa('Python') deve restituire 'nohtyP'"
assert inverti_stringa.__doc__, "❌ Manca la docstring sotto il def"
assert uguale is True, "❌ uguale: confronta inverti_stringa('radar') con 'radar' usando =="
'''),
    'E2.2': ('Esercizio E2.2', r'''
assert paesi_capitale_pari(g10) == ['Canada', 'Francia', 'Italia', 'Regno Unito', 'Stati Uniti', 'Spagna'], "❌ Controlla la condizione: len(capitale) % 2 == 0"
assert paesi_pari == paesi_capitale_pari(g10) and quanti == 6, "❌ paesi_pari è il risultato su g10 e quanti è len(paesi_pari)"
'''),
    'E2.3': ('Esercizio E2.3', r'''
assert trova_palindrome(['ciao', 'anna', 'radar', 'gatto', 'osso', 'madam']) == ['anna', 'radar', 'osso', 'madam'], "❌ Le palindrome della lista sono anna, radar, osso e madam"
assert con_maiuscole == ['Anna', 'Otto'], "❌ con_maiuscole: confronta parola.lower() con parola.lower()[::-1] e restituisci la parola originale"
'''),
    'E2.4': ('Esercizio E2.4', r'''
assert list(letture.columns) == ["pod", "fascia", "kwh"], "❌ Con usecols leggi solo pod, fascia e kwh"
assert letture["kwh"].dtype == "float64" and righe == 216, "❌ kwh deve essere numerica e le righe 216"
assert round(totale_kwh, 1) == 134507.7, "❌ totale_kwh: somma la colonna kwh"
'''),
    'E2.5': ('Esercizio E2.5', r'''
assert len(listino) == 3 and prezzo_f1 == 0.21, "❌ listino: leggi il foglio Listino; prezzo_f1 è il primo valore di eur_kwh"
assert n_letture == 930 and round(kwh_marzo, 1) == 69880.1, "❌ letture_db: leggi tutta la tabella letture e somma la colonna kwh"
assert len(letture_pod) == 31 and set(letture_pod["pod"]) == {"IT001E10087109"}, "❌ letture_pod: filtra con WHERE pod = '...'"
'''),
    'E2.6': ('Esercizio E2.6', r'''
assert len(sensori_mi) > 0, "❌ sensori_mi è vuoto: hai chiamato sensori(\"MI\") o letto il file di riserva?"
assert {"idsensore", "tipologia", "provincia"} <= set(sensori_mi.columns), "❌ Mancano le colonne dell'anagrafica"
assert set(sensori_mi["provincia"]) == {"MI"}, "❌ sensori_mi deve contenere solo la provincia MI"
'''),
}

# Le soluzioni degli esercizi che le mostrano a richiesta, codificate perché non si leggano per caso.
SOLUZIONI = {
    'E2.1': ('Esercizio E2.1', 'ZGVmIGludmVydGlfc3RyaW5nYShzdHJpbmdhKToKICAgICIiIlJlc3RpdHVpc2NlIGxhIHN0cmluZ2EgbGV0dGEgZGFsbCd1bHRpbW8gY2FyYXR0ZXJlIGFsIHByaW1vLiIiIgogICAgcmV0dXJuIHN0cmluZ2FbOjotMV0KCnVndWFsZSA9IGludmVydGlfc3RyaW5nYSgicmFkYXIiKSA9PSAicmFkYXIiCgpwcmludChpbnZlcnRpX3N0cmluZ2EoIlB5dGhvbiIpKSAgIyBPdXRwdXQ6IG5vaHR5UApwcmludCh1Z3VhbGUpICAgICAgICAgICAgICAgICAgICAgIyBPdXRwdXQ6IFRydWU='),
    'E2.2': ('Esercizio E2.2', 'ZGVmIHBhZXNpX2NhcGl0YWxlX3BhcmkoZGl6aW9uYXJpbyk6CiAgICByaXN1bHRhdG8gPSBbXQogICAgZm9yIHBhZXNlLCBjYXBpdGFsZSBpbiBkaXppb25hcmlvLml0ZW1zKCk6CiAgICAgICAgaWYgbGVuKGNhcGl0YWxlKSAlIDIgPT0gMDoKICAgICAgICAgICAgcmlzdWx0YXRvLmFwcGVuZChwYWVzZSkKICAgIHJldHVybiByaXN1bHRhdG8KCmcxMCA9IHsKICAgICdDYW5hZGEnOiAnT3R0YXdhJywKICAgICdGcmFuY2lhJzogJ1BhcmlnaScsCiAgICAnR2VybWFuaWEnOiAnQmVybGlubycsCiAgICAnSXRhbGlhJzogJ1JvbWEnLAogICAgJ0dpYXBwb25lJzogJ1Rva3lvJywKICAgICdSZWdubyBVbml0byc6ICdMb25kcmEnLAogICAgJ1N0YXRpIFVuaXRpJzogJ1dhc2hpbmd0b24nLAogICAgJ1NwYWduYSc6ICdNYWRyaWQnLAogICAgJ1BhZXNpIEJhc3NpJzogJ0Ftc3RlcmRhbScsCiAgICAnQ29yZWEgZGVsIFN1ZCc6ICdTZW91bCcKfQoKcGFlc2lfcGFyaSA9IHBhZXNpX2NhcGl0YWxlX3BhcmkoZzEwKQpxdWFudGkgPSBsZW4ocGFlc2lfcGFyaSkKCnByaW50KHBhZXNpX3BhcmkpICAjIE91dHB1dDogWydDYW5hZGEnLCAnRnJhbmNpYScsICdJdGFsaWEnLCAnUmVnbm8gVW5pdG8nLCAnU3RhdGkgVW5pdGknLCAnU3BhZ25hJ10KcHJpbnQocXVhbnRpKSAgICAgICMgT3V0cHV0OiA2'),
    'E2.3': ('Esercizio E2.3', 'ZGVmIHRyb3ZhX3BhbGluZHJvbWUobGlzdGFfcGFyb2xlKToKICAgIHJldHVybiBbcGFyb2xhIGZvciBwYXJvbGEgaW4gbGlzdGFfcGFyb2xlIGlmIHBhcm9sYS5sb3dlcigpID09IHBhcm9sYS5sb3dlcigpWzo6LTFdXQoKbGlzdGFfcGFyb2xlID0gWydjaWFvJywgJ2FubmEnLCAncmFkYXInLCAnZ2F0dG8nLCAnb3NzbycsICdtYWRhbSddCnByaW50KHRyb3ZhX3BhbGluZHJvbWUobGlzdGFfcGFyb2xlKSkgICMgT3V0cHV0OiBbJ2FubmEnLCAncmFkYXInLCAnb3NzbycsICdtYWRhbSddCgpjb25fbWFpdXNjb2xlID0gdHJvdmFfcGFsaW5kcm9tZShbJ0FubmEnLCAnUm9tYScsICdPdHRvJywgJ3BhbmUnXSkKcHJpbnQoY29uX21haXVzY29sZSkgICMgT3V0cHV0OiBbJ0FubmEnLCAnT3R0bydd'),
    'E2.4': ('Esercizio E2.4', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KAogICAgIi4uL0RhdGkvbGV0dHVyZV9wb2RfMjAyNS5jc3YiLAogICAgc2VwPSI7IiwgZGVjaW1hbD0iLCIsIGVuY29kaW5nPSJsYXRpbi0xIiwKICAgIHVzZWNvbHM9WyJwb2QiLCAiZmFzY2lhIiwgImt3aCJdLAopCmxldHR1cmUuaW5mbygpCgpyaWdoZSA9IGxlbihsZXR0dXJlKQp0b3RhbGVfa3doID0gbGV0dHVyZVsia3doIl0uc3VtKCkKCnByaW50KHJpZ2hlLCByb3VuZCh0b3RhbGVfa3doLCAxKSkgICMgT3V0cHV0OiAyMTYgMTM0NTA3Ljc='),
    'E2.5': ('Esercizio E2.5', 'aW1wb3J0IHNxbGl0ZTMKCmltcG9ydCBwYW5kYXMgYXMgcGQKCmxpc3Rpbm8gPSBwZC5yZWFkX2V4Y2VsKCIuLi9EYXRpL2JvbGxldHRhX2VzZW1waW8ueGxzeCIsIHNoZWV0X25hbWU9Ikxpc3Rpbm8iKQpwcmV6em9fZjEgPSBsaXN0aW5vWyJldXJfa3doIl1bMF0KCmNvbiA9IHNxbGl0ZTMuY29ubmVjdCgiLi4vRGF0aS91dGlsaXR5LmRiIikKbGV0dHVyZV9kYiA9IHBkLnJlYWRfc3FsKCJTRUxFQ1QgKiBGUk9NIGxldHR1cmUiLCBjb24pCmxldHR1cmVfcG9kID0gcGQucmVhZF9zcWwoIlNFTEVDVCAqIEZST00gbGV0dHVyZSBXSEVSRSBwb2QgPSAnSVQwMDFFMTAwODcxMDknIiwgY29uKQpjb24uY2xvc2UoKQoKbl9sZXR0dXJlID0gbGVuKGxldHR1cmVfZGIpCmt3aF9tYXJ6byA9IGxldHR1cmVfZGJbImt3aCJdLnN1bSgpCgpwcmludChwcmV6em9fZjEpICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIyBPdXRwdXQ6IDAuMjEKcHJpbnQobl9sZXR0dXJlLCByb3VuZChrd2hfbWFyem8sIDEpLCBsZW4obGV0dHVyZV9wb2QpKSAgICMgT3V0cHV0OiA5MzAgNjk4ODAuMSAzMQ=='),
    'E2.6': ('Esercizio E2.6', 'aW1wb3J0IHBhbmRhcyBhcyBwZAppbXBvcnQgcmVxdWVzdHMKCgpkZWYgc2Vuc29yaShwcm92aW5jaWEpOgogICAgIiIiQW5hZ3JhZmljYSBkZWkgc2Vuc29yaSBtZXRlbyBkaSBSZWdpb25lIExvbWJhcmRpYSBpbiB1bmEgcHJvdmluY2lhLCBjb21lIERhdGFGcmFtZS4iIiIKICAgIHVybCA9ICJodHRwczovL3d3dy5kYXRpLmxvbWJhcmRpYS5pdC9yZXNvdXJjZS9uZjc4LW5qNmIuanNvbiIKICAgIHJlc3BvbnNlID0gcmVxdWVzdHMuZ2V0KHVybCwgcGFyYW1zPXsicHJvdmluY2lhIjogcHJvdmluY2lhfSwgdGltZW91dD0zMCkKICAgIHJlc3BvbnNlLnJhaXNlX2Zvcl9zdGF0dXMoKQogICAgcmV0dXJuIHBkLkRhdGFGcmFtZShyZXNwb25zZS5qc29uKCkpCgoKc2Vuc29yaV9taSA9IHNlbnNvcmkoIk1JIikKc2Vuc29yaV9taS5oZWFkKCkKCgojIHNlIGlsIHBvcnRhbGUgbm9uIHJpc3BvbmRlLCBuZWxsYSBzZWNvbmRhIGNlbGxhCmltcG9ydCBqc29uCgppbXBvcnQgcGFuZGFzIGFzIHBkCgp3aXRoIG9wZW4oIi4uL0RhdGkvZmFsbGJhY2svbG9tYmFyZGlhX3NlbnNvcmkuanNvbiIsIGVuY29kaW5nPSJ1dGYtOCIpIGFzIGY6CiAgICB0dXR0aSA9IHBkLkRhdGFGcmFtZShqc29uLmxvYWQoZikpCnNlbnNvcmlfbWkgPSB0dXR0aVt0dXR0aVsicHJvdmluY2lhIl0gPT0gIk1JIl0Kc2Vuc29yaV9taS5oZWFkKCk='),
    'E2.7': ('Esercizio E2.7', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKZGVmIGxlZ2dpX2Nzdl9pdGFsaWFubyhwZXJjb3Jzbyk6CiAgICAiIiJMZWdnZSB1biBDU1Ygc2FsdmF0byBkYSBFeGNlbCBpbiBpdGFsaWFubyBlIGxvIHJlc3RpdHVpc2NlIGNvbWUgRGF0YUZyYW1lLiIiIgogICAgcmV0dXJuIHBkLnJlYWRfY3N2KHBlcmNvcnNvLCBzZXA9IjsiLCBkZWNpbWFsPSIsIiwgZW5jb2Rpbmc9ImxhdGluLTEiKQoKbGV0dHVyZSA9IGxlZ2dpX2Nzdl9pdGFsaWFubygiLi4vRGF0aS9sZXR0dXJlX3BvZF8yMDI1LmNzdiIpCmxldHR1cmUuaW5mbygp'),
}
