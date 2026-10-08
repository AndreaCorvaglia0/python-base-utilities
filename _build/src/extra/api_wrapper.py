"""Extra X4 · Wrapper per le API (dimostrazione del docente)."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="X4",
        file="API_wrapper",
        titolo="Wrapper per le API",
        blocco=1,
        giornata=0,
        intento="Le chiamate a un'API ripetono sempre gli stessi passi, che conviene raccogliere in una funzione; ne vediamo una prima versione, `get_data`, e una seconda più solida, `get_json`.",
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
        Una chiamata a un'API con `requests` segue sempre gli stessi passi: la richiesta GET, il controllo
        dell'esito, la conversione della risposta JSON e la costruzione del DataFrame. Li scriviamo per
        esteso una prima volta, sull'anagrafica dei sensori della Regione Lombardia, e poi li raccogliamo
        in una funzione. La prima cella importa le librerie e definisce gli indirizzi delle due risorse e
        i file di riserva da usare se il portale non risponde.
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
    nb.md("""
        La cella seguente fa la chiamata vera e propria. Il metodo `raise_for_status()` solleva
        un'eccezione se il server risponde con un errore, e `response.json()` converte il testo della
        risposta in una lista di dizionari, che `pd.DataFrame` trasforma in una tabella.
    """)
    nb.code("""
        response = requests.get(url_sensori, params={"$limit": 5000}, timeout=30)
        response.raise_for_status()

        sensori = pd.DataFrame(response.json())
        sensori.head()
    """, rete=True)
    nb.md("""
        Se il portale non risponde, si esegue la cella qui sotto al posto di quella precedente. La cella
        legge un file di riserva, salvato nella cartella dei dati, che contiene dati di esempio con la
        stessa struttura, così il resto della dimostrazione funziona anche senza rete.
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
        parametri, invia una richiesta all'API e restituisce un DataFrame. È la forma che si trova più
        spesso negli esempi in rete, e dopo averla usata ne vedremo i limiti.
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
        Usiamo la funzione per recuperare di nuovo l'anagrafica dei sensori. Il portale della Regione
        accetta alcuni parametri di query speciali, il cui nome inizia con il simbolo `$`; tra questi,
        `$limit` fissa il numero massimo di record restituiti, e con un valore alto otteniamo l'anagrafica
        completa.
    """)
    nb.code("""
        sensori_df = get_data(url_sensori, {"$limit": 5000})
        sensori_df.head()
    """, rete=True)
    nb.md("""
        Anche in questo caso, se il portale non risponde, si esegue la cella qui sotto al posto di quella
        precedente. La cella legge lo stesso file di riserva e assegna il risultato a `sensori_df`, come
        farebbe la funzione.
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
        La funzione fa il suo lavoro, ma ha tre limiti. Non imposta un `timeout`, quindi una chiamata a cui
        il server non risponde resta in attesa senza fine. In caso di errore stampa un messaggio e
        restituisce `None`, e il programma fallisce più avanti, alla riga che usa il risultato, con un
        errore che non ne indica la causa. Infine svolge insieme due lavori, la chiamata e la costruzione
        del DataFrame, e non si può riusare quando la risposta va letta in un altro modo. La versione
        seguente risolve tutti e tre i problemi.
    """)

    nb.sezione("La versione con get_json", intro="""
        I tre passi `requests.get`, `raise_for_status()` e `.json()` si ripetono identici a ogni chiamata.
        Quando un pezzo di codice si ripete uguale conviene raccoglierlo in una funzione, detta
        **wrapper** perché avvolge la chiamata alla libreria. Il wrapper si riusa con una sola riga, e
        quando c'è qualcosa da cambiare, come il timeout o una chiave di accesso, la modifica si fa in un
        posto solo. La nostra versione, `get_json`, restituisce la risposta già convertita e lascia a chi
        la chiama la scelta di come usarla.
    """)
    nb.code('''
        def get_json(url: str, params: dict) -> dict | list:
            """Fa una GET con i parametri dati e restituisce la risposta JSON già convertita."""
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
    ''')
    nb.md("""
        Con `get_json` la lettura dell'anagrafica si riduce a una sola riga, che prende il posto dei tre
        passi scritti all'inizio del notebook. La costruzione del DataFrame resta fuori dalla funzione ed
        è identica a prima.
    """)
    nb.code("""
        sensori = pd.DataFrame(get_json(url_sensori, {"$limit": 5000}))
        sensori.shape
    """, rete=True)
    nb.md("""
        Sopra il wrapper costruiamo una funzione di dominio, cioè una funzione che risponde a una domanda
        precisa sui dati. Dato l'identificativo di un sensore e due date, `misure_sensore` restituisce le
        misure del periodo già pulite, convertite in numeri e senza i valori `-9999`, che il portale usa
        per indicare una misura mancante. Tutto il lavoro sta dentro la funzione, e chi la usa scrive una
        sola chiamata.
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
        Se il portale non risponde, si esegue la cella qui sotto al posto di quella precedente. La cella
        applica ai dati di esempio del file di riserva gli stessi passi di pulizia della funzione, quindi
        il risultato ha la stessa forma.
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
        Il type hint `-> pd.DataFrame` e la docstring dicono a chi legge il codice, e anche a Copilot, che
        cosa aspettarsi dalla funzione senza doverne leggere il corpo. In generale, quando una fonte di
        dati va letta più volte, conviene scrivere una funzione piccola, con un nome che dice che cosa
        restituisce.
    """)

    return nb
