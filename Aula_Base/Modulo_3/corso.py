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

    '7.1': ('Esercizio 7.1', r'''
assert prime_tre["kwh"].tolist() == [5785.2, 1434.9, 1396.3], "❌ prime_tre: ordina per kwh con ascending=False e tieni le prime tre righe"
assert prime_tre.iloc[0]["cliente"] == "Panificio Rè", "❌ prime_tre: la prima riga è la lettura di luglio del Panificio Rè"
'''),
    '7.2': ('Esercizio 7.2', r'''
assert len(prezzi_stati) == 4, "❌ Con l'inner join restano le quattro righe di stati"
assert {"sigla", "price"} <= set(prezzi_stati.columns), "❌ Servono le colonne sigla e price"
prezzo_tx = prezzi_stati.loc[prezzi_stati["sigla"] == "TX", "price"].iloc[0]
assert round(prezzo_tx, 2) == 8.86, "❌ Filtra su all sectors prima della media"
'''),
    '8.1': ('Esercizio 8.1', r'''
assert len(giornaliero) == 366, "❌ giornaliero: un valore per ogni giorno del 2024, con resample('D')"
assert round(giornaliero.max()) == 26869, "❌ giornaliero: la media dei quarti d'ora di ogni giorno, con mean()"
assert giorno_max == pd.Timestamp("2024-07-17"), "❌ giorno_max: usa giornaliero.idxmax()"
'''),
    '8.2': ('Esercizio 8.2', r'''
assert len(per_ora) == 24 and len(per_giorno) == 7, "❌ per_ora e per_giorno: groupby su ora e su giorno_settimana"
assert ora_di_punta == 11, "❌ ora_di_punta: idxmax() della media per ora"
assert giorno_minimo == 6, "❌ giorno_minimo: idxmin() della media per giorno della settimana (6 = domenica)"
'''),
    'A2.1': ('Esercizio A2.1', r'''
assert len(salti) == 1, "❌ salti: deve restare una riga sola, quella con distanze > pd.Timedelta('15min')"
assert salti["Date"].iloc[0] == pd.Timestamp("2024-03-31 03:00"), "❌ salti: la riga attesa è quella delle 3:00 del 31 marzo"
'''),
    'E3.1': ('Esercizio E3.1', r'''
assert len(ascolti_103) == 1, "❌ ascolti_103: deve restare una sola riga, quella con UserID 103"
assert ascolti_103["Song"].tolist() == ["Song A"] and ascolti_103["Plays"].tolist() == [4], "❌ ascolti_103: la riga dell'utente 103 ha Song A e 4 ascolti"
'''),
    'E3.2': ('Esercizio E3.2', r'''
atteso = {"Song A": 19, "Song B": 7, "Song C": 1, "Song D": 2}
assert ascolti_per_canzone.to_dict() == atteso, "❌ ascolti_per_canzone: raggruppa per Song e somma Plays"
'''),
    'E3.3': ('Esercizio E3.3', r'''
assert ascolti_per_artista.tolist() == [19, 7, 2, 1], "❌ ascolti_per_artista: somma Plays per Artist e ordina con ascending=False"
assert artista_top == "Artist X", "❌ artista_top: usa idxmax() sui totali"
'''),
    'E3.4': ('Esercizio E3.4', r'''
assert isinstance(utenti_assidui, set), "❌ utenti_assidui: costruiscilo con set(utenti)"
assert utenti_assidui == {101, 103, 105}, "❌ utenti_assidui: la maschera è ascolti[\"Plays\"] > 3 e la colonna è UserID"
'''),
    'E3.5': ('Esercizio E3.5', r'''
assert isinstance(df_serie.index, pd.DatetimeIndex) and df_serie.index.is_monotonic_increasing, "❌ df_serie: converti timestamp_str, usa set_index(\"timestamp\") e sort_index()"
assert list(df_serie.columns) == ["power_kw", "temp_c"], "❌ df_serie: tieni le colonne power_kw e temp_c"
assert len(periodo) == 22 and str(periodo.index[0]) == "2025-03-01 12:00:00", "❌ periodo: df_serie.loc[\"2025-03-01 12:00\":\"2025-03-01 18:00\"]"
'''),
    'E3.6': ('Esercizio E3.6', r'''
assert df_15min["date"].nunique() == 3, "❌ date: usa df_15min.index.date"
assert df_15min["is_weekend"].sum() == 192, "❌ is_weekend: df_15min.index.dayofweek >= 5"
assert len(media_oraria) == 72 and round(media_oraria.iloc[0], 3) == 230.925, "❌ media_oraria: df_15min[\"power_kw\"].resample(\"h\").mean()"
assert round(somma_oraria.iloc[0], 1) == 923.7, "❌ somma_oraria: come media_oraria, con sum() al posto di mean()"
'''),
}

# Le soluzioni degli esercizi che le mostrano a richiesta, codificate perché non si leggano per caso.
SOLUZIONI = {
    'E3.1': ('Esercizio E3.1', 'Y29uZCA9IGFzY29sdGlbIlVzZXJJRCJdID09IDEwMwphc2NvbHRpXzEwMyA9IGFzY29sdGlbY29uZF0KYXNjb2x0aV8xMDM='),
    'E3.2': ('Esercizio E3.2', 'YXNjb2x0aV9wZXJfY2Fuem9uZSA9IGFzY29sdGkuZ3JvdXBieSgiU29uZyIpWyJQbGF5cyJdLnN1bSgpCmFzY29sdGlfcGVyX2NhbnpvbmU='),
    'E3.3': ('Esercizio E3.3', 'YXNjb2x0aV9wZXJfYXJ0aXN0YSA9IGFzY29sdGkuZ3JvdXBieSgiQXJ0aXN0IilbIlBsYXlzIl0uc3VtKCkuc29ydF92YWx1ZXMoYXNjZW5kaW5nPUZhbHNlKQphcnRpc3RhX3RvcCA9IGFzY29sdGlfcGVyX2FydGlzdGEuaWR4bWF4KCkKYXJ0aXN0YV90b3AgICMgT3V0cHV0OiAnQXJ0aXN0IFgn'),
    'E3.4': ('Esercizio E3.4', 'Y29uZCA9IGFzY29sdGlbIlBsYXlzIl0gPiAzCnV0ZW50aSA9IGFzY29sdGkubG9jW2NvbmQsICJVc2VySUQiXQp1dGVudGlfYXNzaWR1aSA9IHNldCh1dGVudGkpCnV0ZW50aV9hc3NpZHVpICAjIE91dHB1dDogezEwNSwgMTAxLCAxMDN9'),
    'E3.5': ('Esercizio E3.5', 'ZGZbInRpbWVzdGFtcCJdID0gcGQudG9fZGF0ZXRpbWUoZGZbInRpbWVzdGFtcF9zdHIiXSwgZm9ybWF0PSIlZC8lbS8lWSAlSDolTSIpCmRmX3NlcmllID0gZGZbWyJ0aW1lc3RhbXAiLCAicG93ZXJfa3ciLCAidGVtcF9jIl1dLnNldF9pbmRleCgidGltZXN0YW1wIikuc29ydF9pbmRleCgpCgpwZXJpb2RvID0gZGZfc2VyaWUubG9jWyIyMDI1LTAzLTAxIDEyOjAwIjoiMjAyNS0wMy0wMSAxODowMCJdCmxlbihwZXJpb2RvKSAgIyBPdXRwdXQ6IDIy'),
    'E3.6': ('Esercizio E3.6', 'IyBsYSBzZXJpZSBkZWxsJ2VzZXJjaXppbyBFMy41LCBjb24gaSBidWNoaSByaWVtcGl0aSBkYWxsJ2ludGVycG9sYXppb25lIGNvbWUgbmVsIG5vdGVib29rIDA4CmRmWyJ0aW1lc3RhbXAiXSA9IHBkLnRvX2RhdGV0aW1lKGRmWyJ0aW1lc3RhbXBfc3RyIl0sIGZvcm1hdD0iJWQvJW0vJVkgJUg6JU0iKQpkZl9zZXJpZSA9IGRmW1sidGltZXN0YW1wIiwgInBvd2VyX2t3IiwgInRlbXBfYyJdXS5zZXRfaW5kZXgoInRpbWVzdGFtcCIpLnNvcnRfaW5kZXgoKQpkZl8xNW1pbiA9IGRmX3NlcmllLmFzZnJlcSgiMTVtaW4iKS5pbnRlcnBvbGF0ZShtZXRob2Q9ImxpbmVhciIpCgpkZl8xNW1pblsiZGF0ZSJdID0gZGZfMTVtaW4uaW5kZXguZGF0ZQpkZl8xNW1pblsiaXNfd2Vla2VuZCJdID0gZGZfMTVtaW4uaW5kZXguZGF5b2Z3ZWVrID49IDUKCm1lZGlhX29yYXJpYSA9IGRmXzE1bWluWyJwb3dlcl9rdyJdLnJlc2FtcGxlKCJoIikubWVhbigpCnNvbW1hX29yYXJpYSA9IGRmXzE1bWluWyJwb3dlcl9rdyJdLnJlc2FtcGxlKCJoIikuc3VtKCkKCnByaW50KGRmXzE1bWluWyJpc193ZWVrZW5kIl0uc3VtKCkpICAjIE91dHB1dDogMTkyCnBkLkRhdGFGcmFtZSh7Im1lYW4iOiBtZWRpYV9vcmFyaWEsICJzdW0iOiBzb21tYV9vcmFyaWF9KS5oZWFkKCk='),
    'E3.7': ('Esercizio E3.7', 'IyBsYSBzZXJpZSBkZWxsJ2VzZXJjaXppbyBFMy41LCBjb24gaSBidWNoaSByaWVtcGl0aSBkYWxsJ2ludGVycG9sYXppb25lIGNvbWUgbmVsIG5vdGVib29rIDA4CmRmWyJ0aW1lc3RhbXAiXSA9IHBkLnRvX2RhdGV0aW1lKGRmWyJ0aW1lc3RhbXBfc3RyIl0sIGZvcm1hdD0iJWQvJW0vJVkgJUg6JU0iKQpkZl9zZXJpZSA9IGRmW1sidGltZXN0YW1wIiwgInBvd2VyX2t3IiwgInRlbXBfYyJdXS5zZXRfaW5kZXgoInRpbWVzdGFtcCIpLnNvcnRfaW5kZXgoKQpkZl8xNW1pbiA9IGRmX3NlcmllLmFzZnJlcSgiMTVtaW4iKS5pbnRlcnBvbGF0ZShtZXRob2Q9ImxpbmVhciIpCgpnaW9ybmFsaWVyYSA9IGRmXzE1bWluWyJwb3dlcl9rdyJdLnJlc2FtcGxlKCJEIikubWVhbigpCgpmb3IgZ2lvcm5vLCB2YWxvcmUgaW4gZ2lvcm5hbGllcmEuaXRlbXMoKToKICAgIHByaW50KGYie2dpb3Juby5zdHJmdGltZSgnJWQvJW0vJVknKX06IHt2YWxvcmU6LjFmfSBrVyIpCiMgT3V0cHV0OgojIDAxLzAzLzIwMjU6IDIxOC43IGtXCiMgMDIvMDMvMjAyNTogMjIwLjMga1cKIyAwMy8wMy8yMDI1OiAyMjAuMSBrVw=='),
}
