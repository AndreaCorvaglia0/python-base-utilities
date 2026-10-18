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
assert costo(1000) == 210.0, "❌ costo(1000) deve dare 210.0: il prezzo di default è 0.21 e la quota fissa 0"
assert costo(1000, prezzo=0.19, quota_fissa=8) == 198.0, "❌ costo(1000, prezzo=0.19, quota_fissa=8) deve dare 198.0"
assert costo_bar == 152.92, "❌ costo_bar: 690.1 kWh al prezzo di default, più 8 euro"
'''),
    'Passo 5': ('Passo 5', r'''
assert letture["kwh"].dtype == "float64", "❌ letture: kwh deve essere numerica, controlla sep e decimal"
assert list(anomale["pod"]) == ["IT001E31047092"], "❌ anomale: una riga sola, quella dell'officina, con kwh > 500"
assert list(pd.read_csv("letture_anomale.csv").columns) == ["pod", "data", "kwh"], "❌ letture_anomale.csv: salva senza l'indice, con index=False"
'''),
    'Passo 6': ('Passo 6', r'''
assert set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ listino: è il foglio Listino? Controlla sheet_name"
assert leggi_tabella("pod").shape == (8, 3), "❌ leggi_tabella: deve restituire tutta la tabella, 8 righe e 3 colonne"
assert list(officina["potenza_kw"]) == [30.0], "❌ officina: una riga sola, quella dell'Officina Meccanica Fumagalli"
'''),
    'R.1': ('Esercizio R.1', r'''
assert isinstance(progetto, dict), "❌ progetto: il dizionario restituito da tomllib.loads(testo)"
assert librerie == ["openpyxl>=3.1.5", "pandas>=3.0.6", "plotly>=6.0"], "❌ librerie: prima la chiave 'project', poi 'dependencies'"
assert strumenti == ["ruff>=0.17.1"], "❌ strumenti: prima la chiave 'dependency-groups', poi 'dev'"
'''),
    'R.2': ('Esercizio R.2', r'''
import plotly

assert versione_plotly == plotly.__version__, "❌ versione_plotly: l'attributo __version__ della libreria plotly"
assert comando_aggiungi.strip() == "uv add matplotlib", "❌ comando_aggiungi: il comando uv che aggiunge una libreria, seguito dal nome"
assert comando_collega.strip() == "uv sync", "❌ comando_collega: il comando uv che ricrea l'ambiente dai file del progetto"
'''),
    'R.3': ('Esercizio R.3', r'''
assert "riga" in globals(), "❌ il blocco if non è stato eseguito: la condizione confronta __name__ con il nome del programma lanciato"
assert riga == "Totale della spesa: 27.30 euro", "❌ riga: il testo stampato dal blocco if"
assert nome_importato == "spesa", "❌ nome_importato: in un file importato __name__ è il nome del modulo, cioè il nome del file senza .py"
'''),
    'R.4': ('Esercizio R.4', r'''
assert output_script.strip() == "Media della settimana: 11.4 km", "❌ output_script: la riga stampata dal terminale, tale e quale"
'''),
    'R.5': ('Esercizio R.5', r'''
assert isinstance(avviso_diviso, str), "❌ avviso_diviso: due stringhe tra parentesi, una dopo l'altra"
assert avviso_diviso == avviso, "❌ avviso_diviso: il testo deve essere identico a quello di avviso, spazi compresi"
'''),
    'R.6': ('Esercizio R.6', r'''
assert sorted(avvisi) == ["E501", "F401", "F841"], "❌ avvisi: tre codici come stringhe, per l'import inutilizzato, la variabile mai letta e la riga troppo lunga"
assert riepilogo(["12 luglio", "13 luglio"], 30) == "Trovati 2 giorni sopra i 30 gradi nel file meteo_luglio.csv: controllare il sensore sul balcone", "❌ riepilogo: il testo in uscita deve restare identico"
assert riepilogo.__doc__, "❌ riepilogo: manca la docstring"
'''),
}

# Le soluzioni degli esercizi che le mostrano a richiesta, codificate perché non si leggano per caso.
SOLUZIONI = {
    'Passo 1': ('Passo 1', 'cGFuaWZpY2lvID0geyJjbGllbnRlIjogIlBhbmlmaWNpbyBSw6giLCAicG9kIjogIklUMDAxRTMxMDQ1MjAxIiwgImt3aF9mZWJicmFpbyI6IDE2NTQuMn0KcHJlenpvID0gMC4yMQoKY2xpZW50ZSA9IHBhbmlmaWNpb1siY2xpZW50ZSJdCmt3aCA9IHBhbmlmaWNpb1sia3doX2ZlYmJyYWlvIl0KY29zdG8gPSBrd2ggKiBwcmV6em8KcHJpbnQoY2xpZW50ZSwga3doLCAia1doIGEgZmViYnJhaW8sIGNvc3RvIiwgcm91bmQoY29zdG8sIDIpLCAiZXVybyIp'),
    'Passo 2': ('Passo 2', 'bGV0dHVyZSA9IFswLjgsIDAuNywgMC45LCAxLjEsIDkuNSwgMTEuMiwgMTAuOCwgOS45LCA4LjQsIDQuMiwgMy45LCAzLjUsCiAgICAgICAgICAgMy4xLCAyLjQsIDIuMCwgMS44LCAyLjIsIDIuNiwgMi45LCAxLjUsIDEuMiwgMS4wLCAwLjksIDAuOF0KCm9yZV9mb3JubyA9IGxldHR1cmVbNDo5XQprd2hfZm9ybm8gPSBzdW0ob3JlX2Zvcm5vKQp0b3RhbGVfZ2lvcm5vID0gc3VtKGxldHR1cmUpCnF1b3RhX2Zvcm5vID0gcm91bmQoa3doX2Zvcm5vIC8gdG90YWxlX2dpb3JubyAqIDEwMCwgMSkKcGljY28gPSBtYXgobGV0dHVyZSkKcHJpbnQoZiJGb3Jubzoge2t3aF9mb3JubzouMWZ9IGtXaCBzdSB7dG90YWxlX2dpb3JubzouMWZ9LCBpbCB7cXVvdGFfZm9ybm99JSAocGljY28ge3BpY2NvfSBrV2gpIik='),
    'Passo 3': ('Passo 3', 'Y29uc3VtaV9mZWJicmFpbyA9IHsKICAgICJJVDAwMUUzMTA0NTIwMSI6IDE2NTQuMiwKICAgICJJVDAwMUUzMTA0NTg3NyI6IDgxMi42LAogICAgIklUMDAxRTMxMDQ2MzEwIjogNjkwLjEsCiAgICAiSVQwMDFFMzEwNDcwOTIiOiAzMzEwLjQsCiAgICAiSVQwMDFFMzEwNDc1NTUiOiA0MzEuOCwKICAgICJJVDAwMUUzMTA0ODEyOCI6IDQ4OTAuNywKICAgICJJVDAwMUUzMTA0ODc0MyI6IDExNzguMywKICAgICJJVDAwMUUzMTA0OTMwNiI6IDMyNzYuMCwKfQpzb2dsaWEgPSAyMDAwCgpzb3ByYV9zb2dsaWEgPSBbcG9kIGZvciBwb2QsIGt3aCBpbiBjb25zdW1pX2ZlYmJyYWlvLml0ZW1zKCkgaWYga3doID4gc29nbGlhXQp0b3RhbGVfa3doID0gc3VtKGNvbnN1bWlfZmViYnJhaW8udmFsdWVzKCkpCnByaW50KGYie2xlbihzb3ByYV9zb2dsaWEpfSBQT0Qgc29wcmEgaSB7c29nbGlhfSBrV2gsIHN1IHt0b3RhbGVfa3doOi4xZn0ga1doIHRvdGFsaSIp'),
    'Passo 4': ('Passo 4', 'ZGVmIGNvc3RvKGt3aCwgcHJlenpvPTAuMjEsIHF1b3RhX2Zpc3NhPTAuMCk6CiAgICAiIiJDb3N0byBpbiBldXJvIGRpIHVuIGNvbnN1bW8gaW4ga1doLCBwacO5IGxhIHF1b3RhIGZpc3NhLCBhcnJvdG9uZGF0byBhaSBjZW50ZXNpbWkuIiIiCiAgICByZXR1cm4gcm91bmQoa3doICogcHJlenpvICsgcXVvdGFfZmlzc2EsIDIpCgoKY29zdG9fcGFuaWZpY2lvID0gY29zdG8oMTY1NC4yKQpjb3N0b19zZXJyYSA9IGNvc3RvKDMyNzYuMCwgcHJlenpvPTAuMTcpCmNvc3RvX2JhciA9IGNvc3RvKDY5MC4xLCBxdW90YV9maXNzYT04KQpwcmludChmIlBhbmlmaWNpbzoge2Nvc3RvX3BhbmlmaWNpb30gZXVybywgU2VycmE6IHtjb3N0b19zZXJyYX0gZXVybywgQmFyOiB7Y29zdG9fYmFyfSBldXJvIik='),
    'Passo 5': ('Passo 5', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KCIuLi8uLi9EYXRpL2hvbWV3b3JrL2xldHR1cmVfbWFyem8uY3N2Iiwgc2VwPSI7IiwgZGVjaW1hbD0iLCIpCmxldHR1cmUuaW5mbygpCnByaW50KGxldHR1cmUuaGVhZCgpKQpwcmludChsZXR0dXJlLmRlc2NyaWJlKCkpCgptYXNrID0gbGV0dHVyZVsia3doIl0gPiA1MDAKYW5vbWFsZSA9IGxldHR1cmVbbWFza10KYW5vbWFsZS50b19jc3YoImxldHR1cmVfYW5vbWFsZS5jc3YiLCBpbmRleD1GYWxzZSkKYW5vbWFsZQ=='),
    'Passo 6': ('Passo 6', 'aW1wb3J0IHBhbmRhcyBhcyBwZAppbXBvcnQgc3FsaXRlMwoKCmRlZiBsZWdnaV90YWJlbGxhKG5vbWUpOgogICAgIiIiTGVnZ2UgdHV0dGEgbGEgdGFiZWxsYSBgbm9tZWAgZGEgYW5hZ3JhZmljYS5kYiBlIGxhIHJlc3RpdHVpc2NlIGNvbWUgRGF0YUZyYW1lLiIiIgogICAgY29uID0gc3FsaXRlMy5jb25uZWN0KCIuLi8uLi9EYXRpL2hvbWV3b3JrL2FuYWdyYWZpY2EuZGIiKQogICAgZGYgPSBwZC5yZWFkX3NxbChmIlNFTEVDVCAqIEZST00ge25vbWV9IiwgY29uKQogICAgY29uLmNsb3NlKCkKICAgIHJldHVybiBkZgoKCmxpc3Rpbm8gPSBwZC5yZWFkX2V4Y2VsKCIuLi8uLi9EYXRpL2hvbWV3b3JrL2NsaWVudGkueGxzeCIsIHNoZWV0X25hbWU9Ikxpc3Rpbm8iKQpwb3RlbnplID0gbGVnZ2lfdGFiZWxsYSgicG9kIikKb2ZmaWNpbmEgPSBwb3RlbnplW3BvdGVuemVbImNsaWVudGUiXSA9PSAiT2ZmaWNpbmEgTWVjY2FuaWNhIEZ1bWFnYWxsaSJdCgpwcmludChsaXN0aW5vKQpvZmZpY2luYQ=='),
    'R.1': ('Esercizio R.1', 'aW1wb3J0IHRvbWxsaWIKCnRlc3RvID0gIiIiCltwcm9qZWN0XQpuYW1lID0gInNwZXNlLWRpLWNhc2EiCnZlcnNpb24gPSAiMC4xLjAiCnJlcXVpcmVzLXB5dGhvbiA9ICI+PTMuMTIiCmRlcGVuZGVuY2llcyA9IFsib3BlbnB5eGw+PTMuMS41IiwgInBhbmRhcz49My4wLjYiLCAicGxvdGx5Pj02LjAiXQoKW2RlcGVuZGVuY3ktZ3JvdXBzXQpkZXYgPSBbInJ1ZmY+PTAuMTcuMSJdCiIiIgoKcHJvZ2V0dG8gPSB0b21sbGliLmxvYWRzKHRlc3RvKQpsaWJyZXJpZSA9IHByb2dldHRvWyJwcm9qZWN0Il1bImRlcGVuZGVuY2llcyJdCnN0cnVtZW50aSA9IHByb2dldHRvWyJkZXBlbmRlbmN5LWdyb3VwcyJdWyJkZXYiXQpwcmludChsaWJyZXJpZSkgICMgT3V0cHV0OiBbJ29wZW5weXhsPj0zLjEuNScsICdwYW5kYXM+PTMuMC42JywgJ3Bsb3RseT49Ni4wJ10KcHJpbnQoc3RydW1lbnRpKSAgIyBPdXRwdXQ6IFsncnVmZj49MC4xNy4xJ10='),
    'R.2': ('Esercizio R.2', 'aW1wb3J0IHBsb3RseQoKdmVyc2lvbmVfcGxvdGx5ID0gcGxvdGx5Ll9fdmVyc2lvbl9fCmNvbWFuZG9fYWdnaXVuZ2kgPSAidXYgYWRkIG1hdHBsb3RsaWIiCmNvbWFuZG9fY29sbGVnYSA9ICJ1diBzeW5jIgoKcHJpbnQodmVyc2lvbmVfcGxvdGx5LCBjb21hbmRvX2FnZ2l1bmdpLCBjb21hbmRvX2NvbGxlZ2Ep'),
    'R.3': ('Esercizio R.3', 'ZGVmIHRvdGFsZShwcmV6emkpOgogICAgIiIiU29tbWEgZGVpIHByZXp6aSBkaSB1bmEgbGlzdGEgZGkgcHJvZG90dGkuIiIiCiAgICByZXR1cm4gc3VtKHByZXp6aSkKCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgc2NvbnRyaW5vID0gWzMuNSwgMi4yLCA0LjgsIDEuOSwgMTQuOV0KICAgIHJpZ2EgPSBmIlRvdGFsZSBkZWxsYSBzcGVzYToge3RvdGFsZShzY29udHJpbm8pOi4yZn0gZXVybyIKICAgIHByaW50KHJpZ2EpICAjIE91dHB1dDogVG90YWxlIGRlbGxhIHNwZXNhOiAyNy4zMCBldXJvCgpub21lX2ltcG9ydGF0byA9ICJzcGVzYSI='),
    'R.4': ('Esercizio R.4', 'IyBjb250ZW51dG8gZGkgYmljaS5weSwgbmVsbGEgY2FydGVsbGEgZGVsIGNvcnNvCmRlZiBtZWRpYSh2YWxvcmkpOgogICAgIiIiTWVkaWEgYXJpdG1ldGljYSBkaSB1bmEgbGlzdGEgZGkgbnVtZXJpLiIiIgogICAgcmV0dXJuIHN1bSh2YWxvcmkpIC8gbGVuKHZhbG9yaSkKCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgY2hpbG9tZXRyaSA9IFsxMi41LCA4LjAsIDE1LjIsIDkuOCwgMTEuNV0KICAgIHByaW50KGYiTWVkaWEgZGVsbGEgc2V0dGltYW5hOiB7bWVkaWEoY2hpbG9tZXRyaSk6LjFmfSBrbSIpCgojIGxhIHJpZ2Egc3RhbXBhdGEgZGFsIHRlcm1pbmFsZSBkb3BvIHV2IHJ1biBiaWNpLnB5Cm91dHB1dF9zY3JpcHQgPSAiTWVkaWEgZGVsbGEgc2V0dGltYW5hOiAxMS40IGttIg=='),
    'R.5': ('Esercizio R.5', 'Y2l0dGEgPSAiQm9sb2duYSIKYXZ2aXNvID0gZiJEb21hbmkgYSB7Y2l0dGF9IMOoIHByZXZpc3RhIHBpb2dnaWEgZGFsbGUgMTQgYWxsZSAxODogY29udmllbmUgcmltYW5kYXJlIGxhIHBhcnRpdGEgZGkgY2FsY2V0dG8gYSBnaW92ZWTDrCBzZXJhIgoKYXZ2aXNvX2RpdmlzbyA9ICgKICAgIGYiRG9tYW5pIGEge2NpdHRhfSDDqCBwcmV2aXN0YSBwaW9nZ2lhIGRhbGxlIDE0IGFsbGUgMTg6ICIKICAgICJjb252aWVuZSByaW1hbmRhcmUgbGEgcGFydGl0YSBkaSBjYWxjZXR0byBhIGdpb3ZlZMOsIHNlcmEiCikKcHJpbnQoYXZ2aXNvX2RpdmlzbyA9PSBhdnZpc28pICAjIE91dHB1dDogVHJ1ZQ=='),
    'R.6': ('Esercizio R.6', 'IyB1biBpbXBvcnQgbWFpIHVzYXRvLCB1bmEgdmFyaWFiaWxlIG1haSBsZXR0YSwgdW5hIHJpZ2EgZGEgMTE3IGNhcmF0dGVyaQphdnZpc2kgPSBbIkY0MDEiLCAiRjg0MSIsICJFNTAxIl0KCnNvZ2xpYSA9IDMwCmdpb3JuaV9jYWxkaSA9IFsiMTIgbHVnbGlvIiwgIjEzIGx1Z2xpbyJdCgoKZGVmIHJpZXBpbG9nbyhnaW9ybmlfY2FsZGksIHNvZ2xpYSk6CiAgICAiIiJVbmEgcmlnYSBkaSB0ZXN0byBjb24gaWwgbnVtZXJvIGRpIGdpb3JuaSBzb3ByYSBsYSBzb2dsaWEuIiIiCiAgICBuID0gbGVuKGdpb3JuaV9jYWxkaSkKICAgIHJldHVybiAoCiAgICAgICAgZiJUcm92YXRpIHtufSBnaW9ybmkgc29wcmEgaSB7c29nbGlhfSBncmFkaSBuZWwgZmlsZSBtZXRlb19sdWdsaW8uY3N2OiAiCiAgICAgICAgImNvbnRyb2xsYXJlIGlsIHNlbnNvcmUgc3VsIGJhbGNvbmUiCiAgICApCgoKcHJpbnQocmllcGlsb2dvKGdpb3JuaV9jYWxkaSwgc29nbGlhKSk='),
}
