"""Extra X4 · Wrapper per le API (dimostrazione del docente)."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="X4",
        file="API_wrapper",
        titolo="Wrapper per le API",
        blocco=1,
        giornata=0,
        intento="Le chiamate a un'API si ripetono uguali: le chiudiamo in una funzione, prima con `get_data`, poi con `get_json`.",
        obiettivi=[
            "riconoscere i passi che si ripetono in una chiamata a un'API",
            "scrivere una funzione che riceve un URL e dei parametri e restituisce un DataFrame",
            "costruire sopra il wrapper una funzione che restituisce misure già pulite",
        ],
        tempo=10,
        dati=["fallback/lombardia_sensori.json", "fallback/lombardia_misure_2001.json"],
        extra=True,
    )

    nb.sezione("La chiamata a un'API", intro="""
        Una chiamata a un'API con `requests` ha sempre gli stessi passi: la richiesta GET, il controllo
        dell'esito, la conversione del JSON e il DataFrame. Li scriviamo una volta sull'anagrafica dei
        sensori di Regione Lombardia, poi li chiudiamo in una funzione.
    """)
    nb.code("""
        import json
        from pathlib import Path

        import pandas as pd
        import requests

        url_sensori = "https://www.dati.lombardia.it/resource/nf78-nj6b.json"
        url_misure = "https://www.dati.lombardia.it/resource/647i-nhxk.json"
        file_sensori = Path("../Dati/fallback/lombardia_sensori.json")
        file_misure = Path("../Dati/fallback/lombardia_misure_2001.json")
    """)
    nb.code("""
        response = requests.get(url_sensori, params={"$limit": 5000}, timeout=30)
        response.raise_for_status()

        sensori = pd.DataFrame(response.json())
        sensori.head()
    """, rete=True)
    nb.md("""
        Se l'API non risponde, esegui la cella qui sotto al posto di quella sopra: il file di riserva
        contiene dati di esempio.
    """)
    nb.code("""
        if file_sensori.exists():
            with open(file_sensori, encoding="utf-8") as f:
                sensori = pd.DataFrame(json.load(f))
            print(sensori.shape)
        else:
            print(f"File di riserva non trovato: {file_sensori}")
    """)

    nb.sezione("La prima versione: get_data", intro="""
        Per rendere il codice più riutilizzabile, definiamo una funzione che prende un URL e dei
        parametri, invia una richiesta all'API e restituisce un DataFrame.
    """)
    nb.code('''
        def get_data(url, params=None):
            """Recupera dati da un'API e li converte in un DataFrame Pandas."""
            # Invia la richiesta GET all'API
            response = requests.get(url, params=params)

            # Controlla se la richiesta ha avuto successo
            if response.status_code == 200:
                # Converte i dati JSON in un DataFrame
                data = response.json()
                df = pd.DataFrame.from_records(data)
                return df
            else:
                print(f"Errore nella richiesta: {response.status_code}")
                return None
    ''')
    nb.md("""
        La usiamo per recuperare l'anagrafica dei sensori. I parametri di query speciali iniziano con il
        simbolo `$`: `$limit` imposta un limite alto per ottenere tutti i record.
    """)
    nb.code("""
        sensori_df = get_data(url_sensori, {"$limit": 5000})
        sensori_df.head()
    """, rete=True)
    nb.md("""
        Se l'API non risponde, esegui la cella qui sotto al posto di quella sopra.
    """)
    nb.code("""
        if file_sensori.exists():
            with open(file_sensori, encoding="utf-8") as f:
                sensori_df = pd.DataFrame(json.load(f))
            print(sensori_df.shape)
        else:
            print(f"File di riserva non trovato: {file_sensori}")
    """)
    nb.md("""
        La funzione ha tre limiti. Non ha un `timeout`, quindi una chiamata senza risposta resta appesa.
        Con un errore stampa un messaggio e restituisce `None`, e la riga dopo fallisce con un errore
        diverso. Fa due lavori insieme, la chiamata e il DataFrame, e non serve quando la risposta va
        letta in un altro modo. La versione seguente li separa.
    """)

    nb.sezione("La versione con get_json", intro="""
        I tre passi `requests.get`, `raise_for_status()` e `.json()` si ripetono a ogni chiamata.
        Quando un pezzo di codice si ripete uguale lo chiudiamo in una funzione, un **wrapper**: si
        riusa con una riga e, se c'è da correggere qualcosa (il timeout, una chiave di accesso), si
        corregge in un posto solo.
    """)
    nb.code('''
        def get_json(url: str, params: dict) -> dict | list:
            """Fa una GET con i parametri dati e restituisce la risposta JSON già convertita."""
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
    ''')
    nb.md("""
        La usiamo subito per l'anagrafica: una riga al posto di tre, e il resto non cambia.
    """)
    nb.code("""
        sensori = pd.DataFrame(get_json(url_sensori, {"$limit": 5000}))
        sensori.shape
    """, rete=True)
    nb.md("""
        Il secondo passo è una funzione di dominio: dato un sensore e due date, restituisce le misure
        pulite, numeriche e senza `-9999`, il modo del portale di dire "misura mancante". Dentro c'è
        tutto il lavoro; fuori resta una chiamata che si legge come una frase.
    """)
    nb.code('''
        def misure_sensore(idsensore: str, inizio: str, fine: str) -> pd.DataFrame:
            """Misure ARPA di un sensore tra due date (aaaa-mm-gg), numeriche e senza i -9999."""
            url = "https://www.dati.lombardia.it/resource/647i-nhxk.json"
            periodo = f"data between '{inizio}T00:00:00' and '{fine}T23:59:59'"
            params = {"idsensore": idsensore, "$where": periodo, "$order": "data", "$limit": 50000}
            misure = pd.DataFrame(get_json(url, params))
            misure["valore"] = pd.to_numeric(misure["valore"])
            mask = misure["valore"] != -9999
            return misure[mask]
    ''')
    nb.code("""
        giugno = misure_sensore("2001", "2025-06-01", "2025-06-30")
        giugno["valore"].describe()
    """, rete=True)
    nb.md("""
        Se l'API non risponde, esegui la cella qui sotto al posto di quella sopra: fa gli stessi passi
        della funzione sui dati di esempio del file di riserva.
    """)
    nb.code("""
        if file_misure.exists():
            with open(file_misure, encoding="utf-8") as f:
                giugno = pd.DataFrame(json.load(f))
            giugno["valore"] = pd.to_numeric(giugno["valore"])
            mask = giugno["valore"] != -9999
            giugno = giugno[mask]
            display(giugno["valore"].describe())
        else:
            print(f"File di riserva non trovato: {file_misure}")
    """)
    nb.md("""
        Il type hint `-> pd.DataFrame` e la docstring dicono a chi legge (e a Copilot) cosa aspettarsi.
        Quando una fonte dati va letta più di una volta, la strada è questa: una funzione piccola, con
        un nome che dice cosa restituisce.
    """)

    return nb
