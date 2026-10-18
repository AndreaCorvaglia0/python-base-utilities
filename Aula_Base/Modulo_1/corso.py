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
assert valore_massimo == 25 and valore_minimo == 7, "❌ valore_massimo e valore_minimo: usa max() e min() sui tre numeri"
assert differenza == 18, "❌ differenza: massimo meno minimo"
'''),
    'E1.2': ('Esercizio E1.2', r'''
assert round(area, 6) == 78.539816, "❌ area: math.pi moltiplicato per raggio ** 2"
'''),
    'E1.3': ('Esercizio E1.3', r'''
assert lista_invertita == [5, 4, 3, 2, 1], "❌ lista_invertita: slicing con passo -1, cioè lista[::-1]"
'''),
    'E1.4': ('Esercizio E1.4', r'''
assert elementi_pari == ["Martina", "Giulia", "Francesca", "Sara"], "❌ elementi_pari: slicing dalla posizione 2 con passo 2, cioè lista[2::2]"
'''),
    'E1.5': ('Esercizio E1.5', r'''
assert g8.get('Regno Unito') == 'Londra' and g8.get('Stati Uniti') == 'Washington, D.C.', "❌ Aggiungi le due coppie con g8[chiave] = valore"
assert len(g8) == 8, "❌ Alla fine il dizionario ha otto paesi"
'''),
}

# Le soluzioni degli esercizi che le mostrano a richiesta, codificate perché non si leggano per caso.
SOLUZIONI = {
    'E1.1': ('Esercizio E1.1', 'IyBEZWZpbml6aW9uZSBkZWxsZSB2YXJpYWJpbGkKYSA9IDEwCmIgPSAyNQpjID0gNwoKIyBDYWxjb2xvIGRlbCBtYXNzaW1vIGUgZGVsIG1pbmltbwp2YWxvcmVfbWFzc2ltbyA9IG1heChhLCBiLCBjKQp2YWxvcmVfbWluaW1vID0gbWluKGEsIGIsIGMpCmRpZmZlcmVuemEgPSB2YWxvcmVfbWFzc2ltbyAtIHZhbG9yZV9taW5pbW8KCiMgU3RhbXBhIGRlaSByaXN1bHRhdGkKcHJpbnQoZiJWYWxvcmUgbWFzc2ltbzoge3ZhbG9yZV9tYXNzaW1vfSIpICAgIyBPdXRwdXQ6IFZhbG9yZSBtYXNzaW1vOiAyNQpwcmludChmIlZhbG9yZSBtaW5pbW86IHt2YWxvcmVfbWluaW1vfSIpICAgICAjIE91dHB1dDogVmFsb3JlIG1pbmltbzogNwpwcmludChmIkRpZmZlcmVuemE6IHtkaWZmZXJlbnphfSIpICAgICAgICAgICAjIE91dHB1dDogRGlmZmVyZW56YTogMTg='),
    'E1.2': ('Esercizio E1.2', 'aW1wb3J0IG1hdGgKCnJhZ2dpbyA9IDUKYXJlYSA9IG1hdGgucGkgKiByYWdnaW8gKiogMgoKcHJpbnQoZiJMJ2FyZWEgZGVsIGNlcmNoaW8gw6g6IHthcmVhfSIpICAjIE91dHB1dDogTCdhcmVhIGRlbCBjZXJjaGlvIMOoOiA3OC41Mzk4MTYzMzk3NDQ4Mw=='),
    'E1.3': ('Esercizio E1.3', 'bGlzdGEgPSBbMSwgMiwgMywgNCwgNV0KCmxpc3RhX2ludmVydGl0YSA9IGxpc3RhWzo6LTFdCnByaW50KGxpc3RhX2ludmVydGl0YSkgICMgT3V0cHV0OiBbNSwgNCwgMywgMiwgMV0='),
    'E1.4': ('Esercizio E1.4', 'bGlzdGEgPSBbIkVsZW5hIiwgIkx1aWdpIiwgIk1hcnRpbmEiLCAiTWFyY28iLCAiR2l1bGlhIiwgIlNpbW9uZSIsICJGcmFuY2VzY2EiLCAiQWxlc3NhbmRybyIsICJTYXJhIiwgIkxvcmVuem8iXQoKZWxlbWVudGlfcGFyaSA9IGxpc3RhWzI6OjJdCnByaW50KGVsZW1lbnRpX3BhcmkpICAjIE91dHB1dDogWydNYXJ0aW5hJywgJ0dpdWxpYScsICdGcmFuY2VzY2EnLCAnU2FyYSdd'),
    'E1.5': ('Esercizio E1.5', 'ZzggPSB7CiAgICAnQ2FuYWRhJzogJ090dGF3YScsCiAgICAnRnJhbmNpYSc6ICdQYXJpZ2knLAogICAgJ0dlcm1hbmlhJzogJ0Jlcmxpbm8nLAogICAgJ0l0YWxpYSc6ICdSb21hJywKICAgICdHaWFwcG9uZSc6ICdUb2t5bycsCiAgICAnUnVzc2lhJzogJ01vc2NhJwp9CgojIEFnZ2l1bmdpIGkgcGFlc2kgbWFuY2FudGkKZzhbJ1JlZ25vIFVuaXRvJ10gPSAnTG9uZHJhJwpnOFsnU3RhdGkgVW5pdGknXSA9ICdXYXNoaW5ndG9uLCBELkMuJwoKcHJpbnQoZzgp'),
    'E1.6': ('Esercizio E1.6', 'ZzggPSB7CiAgICAnQ2FuYWRhJzogJ090dGF3YScsCiAgICAnRnJhbmNpYSc6ICdQYXJpZ2knLAogICAgJ0dlcm1hbmlhJzogJ0Jlcmxpbm8nLAogICAgJ0l0YWxpYSc6ICdSb21hJywKICAgICdHaWFwcG9uZSc6ICdUb2t5bycsCiAgICAnUnVzc2lhJzogJ01vc2NhJwp9CgpnOFsnUmVnbm8gVW5pdG8nXSA9ICdMb25kcmEnCmc4WydTdGF0aSBVbml0aSddID0gJ1dhc2hpbmd0b24sIEQuQy4nCgpwcmludChmIklsIEc4IGhhIHtsZW4oZzgpfSBwYWVzaSBlIGxhIGNhcGl0YWxlIGRlbCBHaWFwcG9uZSDDqCB7ZzhbJ0dpYXBwb25lJ119Iik='),
}
