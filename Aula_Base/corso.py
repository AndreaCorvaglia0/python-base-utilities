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

    '0.2': ('Esercizio 0.2', r'''
assert isinstance(citta, str) and citta.strip(), "❌ citta deve essere un testo tra virgolette"
assert isinstance(temperatura, (int, float)), "❌ temperatura deve essere un numero, senza virgolette"
'''),
    '1.1': ('Esercizio 1.1', r'''
assert massima == 25, "❌ massima: la più alta delle tre temperature, con max()"
assert minima == 7, "❌ minima: la più bassa delle tre temperature, con min()"
assert escursione == 18, "❌ escursione: la massima meno la minima"
'''),
    '1.2': ('Esercizio 1.2', r'''
assert math.isclose(area, 78.54, rel_tol=1e-3), "❌ area: π per il raggio al quadrato"
'''),
    '1.3': ('Esercizio 1.3', r'''
assert ore == 2, "❌ ore: quante volte 60 sta in 137"
assert minuti == 17, "❌ minuti: il resto della divisione per 60"
'''),
    '2.1': ('Esercizio 2.1', r'''
assert ritorno == ["Napoli", "Roma", "Firenze", "Bologna", "Milano"], "❌ ritorno: le fermate dell'andata dall'ultima alla prima"
assert andata[0] == "Milano", "❌ andata non va modificata: lo slicing crea una lista nuova"
'''),
    '2.2': ('Esercizio 2.2', r'''
assert squadra == ["Martina", "Giulia", "Francesca", "Sara"], "❌ squadra: una posizione ogni due, partendo dalla 2"
'''),
    '2.3': ('Esercizio 2.3', r'''
assert g8['Regno Unito'] == 'Londra' and g8['Stati Uniti'] == 'Washington, D.C.', "❌ g8: mancano Regno Unito o Stati Uniti"
assert 'Russia' not in g7 and 'Russia' in g8, "❌ g7: la Russia va tolta dalla copia g7, non da g8"
assert g10['Paesi Bassi'] == 'Amsterdam' and g10['Corea del Sud'] == 'Seoul' and g10['Italia'] == 'Bobbio', "❌ g10: controlla i paesi nuovi e la capitale dell'Italia"
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
    '4.1': ('Esercizio 4.1', r'''
assert inverti_stringa("Python") == "nohtyP", "❌ inverti_stringa('Python') deve restituire 'nohtyP'"
'''),
    '4.2': ('Esercizio 4.2', r'''
atteso = ['Canada', 'Francia', 'Italia', 'Regno Unito', 'Stati Uniti', 'Spagna']
assert paesi_capitale_pari(g10) == atteso, "❌ controlla la condizione: len(capitale) deve essere pari"
'''),
    '4.3': ('Esercizio 4.3', r'''
assert trova_palindrome(lista_parole) == ['anna', 'radar', 'osso', 'madam'], "❌ le palindrome della lista sono anna, radar, osso e madam"
'''),
    '5.1': ('Esercizio 5.1', r'''
assert round(totale, 2) == 7.5, "❌ totale: la lista si chiama prezzi"
assert anni_alla_pensione == 46, "❌ anni_alla_pensione: eta è un testo, convertilo con int()"
assert capitale == "Roma" and citta[-1] == "Napoli", "❌ capitale o citta: la chiave è Italia con la maiuscola; una lista si allunga con append"
'''),
    '5.2': ('Esercizio 5.2', r'''
assert risposte["obbligatorio"] == "iterable", "❌ obbligatorio: il nome del parametro che nella firma non ha ="
assert risposte["default_reverse"] is False, "❌ default_reverse: il valore dopo reverse=, senza virgolette"
assert dal_piu_alto == [30, 28, 25, 18], "❌ dal_piu_alto: passa reverse=True per nome"
'''),
    '6.1': ('Esercizio 6.1', r'''
assert list(letture_kwh.columns) == ["pod", "fascia", "kwh"], "❌ letture_kwh: servono solo pod, fascia e kwh (usecols)"
assert round(totale_kwh, 1) == 134507.7, "❌ totale_kwh: controlla decimal=\",\""
'''),
    '6.2': ('Esercizio 6.2', r'''
assert list(fogli.keys()) == ["Gennaio", "Febbraio"], "❌ fogli: il file deve avere i fogli Gennaio e Febbraio"
assert len(consumi) == 6 and list(consumi.index) == list(range(6)), "❌ consumi: 6 righe con indice da 0 a 5 (ignore_index=True)"
assert round(consumi["kwh"].sum(), 1) == 14149.2, "❌ consumi: il totale dei kwh è 14149.2"
'''),
    '6.3': ('Esercizio 6.3', r'''
assert len(letture_pod) == 31, "❌ letture_pod: servono le 31 righe del solo POD IT001E10000000"
assert round(totale_marzo, 1) == 7785.6, "❌ totale_marzo: somma la colonna kwh"
'''),
    '7.1': ('Esercizio 7.1', r'''
assert len(ascolti_utente_103) == 1, "❌ Deve restare una sola riga"
assert ascolti_utente_103["Song"].tolist() == ["Song A"], "❌ La canzone dell'utente 103 è Song A"
assert ascolti_utente_103["Plays"].tolist() == [4], "❌ Gli ascolti dell'utente 103 sono 4"
'''),
    '7.2': ('Esercizio 7.2', r'''
atteso = {"Song A": 19, "Song B": 7, "Song C": 1, "Song D": 2}
assert ascolti_per_canzone.to_dict() == atteso, "❌ Raggruppa per Song e somma Plays"
'''),
    '7.3': ('Esercizio 7.3', r'''
assert ascolti_per_artista.iloc[0] == 19, "❌ Il primo totale, in ordine decrescente, è 19"
assert artista_top == "Artist X", "❌ L'artista più ascoltato è un altro"
'''),
    '7.4': ('Esercizio 7.4', r'''
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
    '9.1': ('Esercizio 9.1', r'''
assert len(fig_carico.data) == 1 and fig_carico.data[0].mode == "lines", "❌ Serve una linea sola: px.line con y='Total Load [MW]'"
assert fig_carico.layout.title.text == "Carico Nord, gennaio 2024", "❌ Il titolo deve essere 'Carico Nord, gennaio 2024'"
'''),
    '9.2': ('Esercizio 9.2', r'''
assert len(fig_potenza.data) == 1 and fig_potenza.data[0].type == "histogram", "❌ Serve un solo istogramma: px.histogram, senza color"
assert fig_potenza.layout.title.text == "Distribuzione della potenza", "❌ Il titolo deve essere 'Distribuzione della potenza'"
'''),
    '10.1': ('Esercizio 10.1', r'''
assert letture.shape == (216, 5), "❌ letture: 216 righe e 5 colonne; con il separatore sbagliato esce una colonna sola"
assert str(letture["kwh"].dtype) == "float64", "❌ kwh deve essere float64: serve decimal=','"
assert round(letture["kwh"].sum(), 1) == 134507.7, "❌ La somma dei kwh deve essere 134507.7"
'''),
    '10.2': ('Esercizio 10.2', r'''
assert risposte["lavoro vero"] == "report_kwh", "❌ lavoro vero: il nome della funzione con il groupby, senza parentesi"
assert risposte["lanciato in una cella"] == "FileNotFoundError", "❌ lanciato in una cella: il blocco main parte anche nel notebook, e da qui il percorso Dati non esiste"
assert round(totale["kwh"].sum(), 1) == 134507.7, "❌ La somma dei kwh deve essere 134507.7: controlla il tipo di kwh con .dtypes"
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
    'A2.1': ('Esercizio A2.1', r'''
assert fig_carico.layout.xaxis.rangeslider.visible, "❌ Manca il range slider: update_xaxes(rangeslider_visible=True)"
assert len(fig_carico.layout.xaxis.rangeselector.buttons) == 2, "❌ Il range selector deve avere due pulsanti, 1w e all"
assert fig_carico.layout.xaxis.rangeselector.buttons[0].count == 7, "❌ Il primo pulsante va indietro di 7 giorni: count=7, step='day'"
'''),
    'A2.2': ('Esercizio A2.2', r'''
from pathlib import Path
assert Path("carico_gennaio.html").exists(), "❌ Il file carico_gennaio.html non c'è: controlla il nome in write_html"
assert Path("carico_gennaio.html").stat().st_size < 1_000_000, "❌ Il file è troppo grande: manca include_plotlyjs=\"cdn\""
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
    'Step 1': ('Step 1', r'''
assert df.shape == (70176, 4), "❌ df: 70.176 righe e 4 colonne, i due anni uno sotto l'altro"
assert df.index[-1] == 70175, "❌ df: l'indice va rifatto da 0, con ignore_index=True in pd.concat"
assert round(righe_giorno) == 96, "❌ righe_giorno: righe totali diviso il numero di giorni diversi"
'''),
    'Step 2': ('Step 2', r'''
assert list(df.columns) == ["Date", "Total Load [MW]"], "❌ df: devono restare solo Date e Total Load [MW]"
assert df["Date"].is_monotonic_increasing, "❌ df: ordina per Date"
assert df.loc[0, "Date"] == pd.Timestamp("2024-01-01 00:00"), "❌ df: la riga 0 deve essere il primo quarto d'ora del 2024; dopo sort_values serve reset_index(drop=True)"
'''),
    'Step 3': ('Step 3', r'''
assert len(duplicati) == 16, "❌ duplicati: 16 righe, 8 timestamp ripetuti in due copie (keep=False le tiene tutte)"
assert len(df) == 70168 and df["Date"].is_unique, "❌ df: 70.168 righe, una per timestamp"
assert len(buchi) == 2, "❌ buchi: 2 righe, le 3:00 delle due ultime domeniche di marzo"
'''),
    'Step 4': ('Step 4', r'''
assert len(df_giornaliero) == 731 and df_giornaliero["Total Load [MW]"].between(10_000, 30_000).all(), "❌ df_giornaliero: 731 giorni, con il carico medio tra 10.000 e 30.000 MW (resample('D').mean())"
assert profilo_orario.shape == (24, 2), "❌ profilo_orario: 24 righe (le ore) e 2 colonne, hour e Total Load [MW]"
assert len(profilo_settimanale) == 7 and profilo_settimanale["Total Load [MW]"].idxmin() == 6, "❌ profilo_settimanale: 7 righe, con la domenica (6) come giorno più leggero"
'''),
    'Step 5': ('Step 5', r'''
assert list(meteo_15.columns) == ["Date", "Temperature_C"], "❌ meteo_15: due colonne, Date e Temperature_C (dopo resample serve reset_index)"
assert len(df_completo) == len(df), "❌ df_completo: il merge con how=\"left\" tiene tutte le righe di df"
assert df_completo["Temperature_C"].notna().all(), "❌ df_completo: restano temperature mancanti, usa ffill()"
'''),
    'Step 6': ('Step 6', r'''
assert len(giornaliero) == 731, "❌ giornaliero: una riga per giorno, 731"
assert {"Total Load [MW]", "Temperature_C", "mese"} <= set(giornaliero.columns), "❌ giornaliero: servono le colonne Total Load [MW], Temperature_C e mese"
assert giornaliero["mese"].nunique() == 12, "❌ mese: i dodici mesi, da dt.month_name()"
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
    'E2.1': ('Esercizio E2.1', 'ZGVmIGludmVydGlfc3RyaW5nYShzdHJpbmdhKToKICAgIHJldHVybiBzdHJpbmdhWzo6LTFdCgpwcmludChpbnZlcnRpX3N0cmluZ2EoIlB5dGhvbiIpKSAgIyBPdXRwdXQ6IG5vaHR5UA=='),
    'E2.2': ('Esercizio E2.2', 'ZGVmIHBhZXNpX2NhcGl0YWxlX3BhcmkoZGl6aW9uYXJpbyk6CiAgICByaXN1bHRhdG8gPSBbXQogICAgZm9yIHBhZXNlLCBjYXBpdGFsZSBpbiBkaXppb25hcmlvLml0ZW1zKCk6CiAgICAgICAgaWYgbGVuKGNhcGl0YWxlKSAlIDIgPT0gMDoKICAgICAgICAgICAgcmlzdWx0YXRvLmFwcGVuZChwYWVzZSkKICAgIHJldHVybiByaXN1bHRhdG8KCmcxMCA9IHsKICAgICdDYW5hZGEnOiAnT3R0YXdhJywKICAgICdGcmFuY2lhJzogJ1BhcmlnaScsCiAgICAnR2VybWFuaWEnOiAnQmVybGlubycsCiAgICAnSXRhbGlhJzogJ1JvbWEnLAogICAgJ0dpYXBwb25lJzogJ1Rva3lvJywKICAgICdSZWdubyBVbml0byc6ICdMb25kcmEnLAogICAgJ1N0YXRpIFVuaXRpJzogJ1dhc2hpbmd0b24nLAogICAgJ1NwYWduYSc6ICdNYWRyaWQnLAogICAgJ1BhZXNpIEJhc3NpJzogJ0Ftc3RlcmRhbScsCiAgICAnQ29yZWEgZGVsIFN1ZCc6ICdTZW91bCcKfQoKcHJpbnQocGFlc2lfY2FwaXRhbGVfcGFyaShnMTApKSAgIyBPdXRwdXQ6IFsnQ2FuYWRhJywgJ0ZyYW5jaWEnLCAnSXRhbGlhJywgJ1JlZ25vIFVuaXRvJywgJ1N0YXRpIFVuaXRpJywgJ1NwYWduYSdd'),
    'E2.3': ('Esercizio E2.3', 'ZGVmIHRyb3ZhX3BhbGluZHJvbWUobGlzdGFfcGFyb2xlKToKICAgIHBhbGluZHJvbWUgPSBbXQogICAgZm9yIHBhcm9sYSBpbiBsaXN0YV9wYXJvbGU6CiAgICAgICAgaWYgcGFyb2xhID09IHBhcm9sYVs6Oi0xXToKICAgICAgICAgICAgcGFsaW5kcm9tZS5hcHBlbmQocGFyb2xhKQogICAgcmV0dXJuIHBhbGluZHJvbWUKCmxpc3RhX3Bhcm9sZSA9IFsnY2lhbycsICdhbm5hJywgJ3JhZGFyJywgJ2dhdHRvJywgJ29zc28nLCAnbWFkYW0nXQpwcmludCh0cm92YV9wYWxpbmRyb21lKGxpc3RhX3Bhcm9sZSkpICAjIE91dHB1dDogWydhbm5hJywgJ3JhZGFyJywgJ29zc28nLCAnbWFkYW0nXQ=='),
    'E2.4': ('Esercizio E2.4', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL2xldHR1cmVfcG9kXzIwMjUuY3N2Iiwgc2VwPSI7IiwgZGVjaW1hbD0iLCIsIGVuY29kaW5nPSJsYXRpbi0xIikKbGV0dHVyZS5pbmZvKCkKCnJpZ2hlID0gbGVuKGxldHR1cmUpCnRvdGFsZV9rd2ggPSBsZXR0dXJlWyJrd2giXS5zdW0oKQoKcHJpbnQocmlnaGUsIHJvdW5kKHRvdGFsZV9rd2gsIDEpKSAgIyBPdXRwdXQ6IDIxNiAxMzQ1MDcuNw=='),
    'E2.5': ('Esercizio E2.5', 'aW1wb3J0IHNxbGl0ZTMKCmltcG9ydCBwYW5kYXMgYXMgcGQKCmxpc3Rpbm8gPSBwZC5yZWFkX2V4Y2VsKCIuLi9EYXRpL2JvbGxldHRhX2VzZW1waW8ueGxzeCIsIHNoZWV0X25hbWU9Ikxpc3Rpbm8iKQpwcmV6em9fZjEgPSBsaXN0aW5vWyJldXJfa3doIl1bMF0KCmNvbiA9IHNxbGl0ZTMuY29ubmVjdCgiLi4vRGF0aS91dGlsaXR5LmRiIikKbGV0dHVyZV9kYiA9IHBkLnJlYWRfc3FsKCJTRUxFQ1QgKiBGUk9NIGxldHR1cmUiLCBjb24pCmNvbi5jbG9zZSgpCgpuX2xldHR1cmUgPSBsZW4obGV0dHVyZV9kYikKa3doX21hcnpvID0gbGV0dHVyZV9kYlsia3doIl0uc3VtKCkKCnByaW50KHByZXp6b19mMSkgICAgICAgICAgICAgICAgICAgICAgICAjIE91dHB1dDogMC4yMQpwcmludChuX2xldHR1cmUsIHJvdW5kKGt3aF9tYXJ6bywgMSkpICAgIyBPdXRwdXQ6IDkzMCA2OTg4MC4x'),
    'E2.6': ('Esercizio E2.6', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKZGVmIGxlZ2dpX2Nzdl9pdGFsaWFubyhwZXJjb3Jzbyk6CiAgICAiIiJMZWdnZSB1biBDU1Ygc2FsdmF0byBkYSBFeGNlbCBpbiBpdGFsaWFubyBlIGxvIHJlc3RpdHVpc2NlIGNvbWUgRGF0YUZyYW1lLiIiIgogICAgcmV0dXJuIHBkLnJlYWRfY3N2KHBlcmNvcnNvLCBzZXA9IjsiLCBkZWNpbWFsPSIsIiwgZW5jb2Rpbmc9ImxhdGluLTEiKQoKbGV0dHVyZSA9IGxlZ2dpX2Nzdl9pdGFsaWFubygiLi4vRGF0aS9sZXR0dXJlX3BvZF8yMDI1LmNzdiIpCmxldHR1cmUuaW5mbygp'),
    'E3.1': ('Esercizio E3.1', 'Y29uZCA9IGFzY29sdGlbIlVzZXJJRCJdID09IDEwMwphc2NvbHRpXzEwMyA9IGFzY29sdGlbY29uZF0KYXNjb2x0aV8xMDM='),
    'E3.2': ('Esercizio E3.2', 'YXNjb2x0aV9wZXJfY2Fuem9uZSA9IGFzY29sdGkuZ3JvdXBieSgiU29uZyIpWyJQbGF5cyJdLnN1bSgpCmFzY29sdGlfcGVyX2NhbnpvbmU='),
    'E3.3': ('Esercizio E3.3', 'YXNjb2x0aV9wZXJfYXJ0aXN0YSA9IGFzY29sdGkuZ3JvdXBieSgiQXJ0aXN0IilbIlBsYXlzIl0uc3VtKCkuc29ydF92YWx1ZXMoYXNjZW5kaW5nPUZhbHNlKQphcnRpc3RhX3RvcCA9IGFzY29sdGlfcGVyX2FydGlzdGEuaWR4bWF4KCkKYXJ0aXN0YV90b3AgICMgT3V0cHV0OiAnQXJ0aXN0IFgn'),
    'E3.4': ('Esercizio E3.4', 'Y29uZCA9IGFzY29sdGlbIlBsYXlzIl0gPiAzCnV0ZW50aSA9IGFzY29sdGkubG9jW2NvbmQsICJVc2VySUQiXQp1dGVudGlfYXNzaWR1aSA9IHNldCh1dGVudGkpCnV0ZW50aV9hc3NpZHVpICAjIE91dHB1dDogezEwNSwgMTAxLCAxMDN9'),
    'E3.5': ('Esercizio E3.5', 'ZGZbInRpbWVzdGFtcCJdID0gcGQudG9fZGF0ZXRpbWUoZGZbInRpbWVzdGFtcF9zdHIiXSwgZm9ybWF0PSIlZC8lbS8lWSAlSDolTSIpCmRmX3NlcmllID0gZGZbWyJ0aW1lc3RhbXAiLCAicG93ZXJfa3ciLCAidGVtcF9jIl1dLnNldF9pbmRleCgidGltZXN0YW1wIikuc29ydF9pbmRleCgpCgpwZXJpb2RvID0gZGZfc2VyaWUubG9jWyIyMDI1LTAzLTAxIDEyOjAwIjoiMjAyNS0wMy0wMSAxODowMCJdCmxlbihwZXJpb2RvKSAgIyBPdXRwdXQ6IDIy'),
    'E3.6': ('Esercizio E3.6', 'IyBsYSBzZXJpZSBkZWxsJ2VzZXJjaXppbyBFMy41LCBjb24gaSBidWNoaSByaWVtcGl0aSBkYWxsJ2ludGVycG9sYXppb25lIGNvbWUgbmVsIG5vdGVib29rIDA4CmRmWyJ0aW1lc3RhbXAiXSA9IHBkLnRvX2RhdGV0aW1lKGRmWyJ0aW1lc3RhbXBfc3RyIl0sIGZvcm1hdD0iJWQvJW0vJVkgJUg6JU0iKQpkZl9zZXJpZSA9IGRmW1sidGltZXN0YW1wIiwgInBvd2VyX2t3IiwgInRlbXBfYyJdXS5zZXRfaW5kZXgoInRpbWVzdGFtcCIpLnNvcnRfaW5kZXgoKQpkZl8xNW1pbiA9IGRmX3NlcmllLmFzZnJlcSgiMTVtaW4iKS5pbnRlcnBvbGF0ZShtZXRob2Q9ImxpbmVhciIpCgpkZl8xNW1pblsiZGF0ZSJdID0gZGZfMTVtaW4uaW5kZXguZGF0ZQpkZl8xNW1pblsiaXNfd2Vla2VuZCJdID0gZGZfMTVtaW4uaW5kZXguZGF5b2Z3ZWVrID49IDUKCm1lZGlhX29yYXJpYSA9IGRmXzE1bWluWyJwb3dlcl9rdyJdLnJlc2FtcGxlKCJoIikubWVhbigpCnNvbW1hX29yYXJpYSA9IGRmXzE1bWluWyJwb3dlcl9rdyJdLnJlc2FtcGxlKCJoIikuc3VtKCkKCnByaW50KGRmXzE1bWluWyJpc193ZWVrZW5kIl0uc3VtKCkpICAjIE91dHB1dDogMTkyCnBkLkRhdGFGcmFtZSh7Im1lYW4iOiBtZWRpYV9vcmFyaWEsICJzdW0iOiBzb21tYV9vcmFyaWF9KS5oZWFkKCk='),
    'E3.7': ('Esercizio E3.7', 'IyBsYSBzZXJpZSBkZWxsJ2VzZXJjaXppbyBFMy41LCBjb24gaSBidWNoaSByaWVtcGl0aSBkYWxsJ2ludGVycG9sYXppb25lIGNvbWUgbmVsIG5vdGVib29rIDA4CmRmWyJ0aW1lc3RhbXAiXSA9IHBkLnRvX2RhdGV0aW1lKGRmWyJ0aW1lc3RhbXBfc3RyIl0sIGZvcm1hdD0iJWQvJW0vJVkgJUg6JU0iKQpkZl9zZXJpZSA9IGRmW1sidGltZXN0YW1wIiwgInBvd2VyX2t3IiwgInRlbXBfYyJdXS5zZXRfaW5kZXgoInRpbWVzdGFtcCIpLnNvcnRfaW5kZXgoKQpkZl8xNW1pbiA9IGRmX3NlcmllLmFzZnJlcSgiMTVtaW4iKS5pbnRlcnBvbGF0ZShtZXRob2Q9ImxpbmVhciIpCgpnaW9ybmFsaWVyYSA9IGRmXzE1bWluWyJwb3dlcl9rdyJdLnJlc2FtcGxlKCJEIikubWVhbigpCgpmb3IgZ2lvcm5vLCB2YWxvcmUgaW4gZ2lvcm5hbGllcmEuaXRlbXMoKToKICAgIHByaW50KGYie2dpb3Juby5zdHJmdGltZSgnJWQvJW0vJVknKX06IHt2YWxvcmU6LjFmfSBrVyIpCiMgT3V0cHV0OgojIDAxLzAzLzIwMjU6IDIxOC43IGtXCiMgMDIvMDMvMjAyNTogMjIwLjMga1cKIyAwMy8wMy8yMDI1OiAyMjAuMSBrVw=='),
    'Passo 1': ('Passo 1', 'cGFuaWZpY2lvID0geyJjbGllbnRlIjogIlBhbmlmaWNpbyBSw6giLCAicG9kIjogIklUMDAxRTMxMDQ1MjAxIiwgImt3aF9mZWJicmFpbyI6IDE2NTQuMn0KcHJlenpvID0gMC4yMQoKY2xpZW50ZSA9IHBhbmlmaWNpb1siY2xpZW50ZSJdCmt3aCA9IHBhbmlmaWNpb1sia3doX2ZlYmJyYWlvIl0KY29zdG8gPSBrd2ggKiBwcmV6em8KcHJpbnQoY2xpZW50ZSwga3doLCAia1doIGEgZmViYnJhaW8sIGNvc3RvIiwgcm91bmQoY29zdG8sIDIpLCAiZXVybyIp'),
    'Passo 2': ('Passo 2', 'bGV0dHVyZSA9IFswLjgsIDAuNywgMC45LCAxLjEsIDkuNSwgMTEuMiwgMTAuOCwgOS45LCA4LjQsIDQuMiwgMy45LCAzLjUsCiAgICAgICAgICAgMy4xLCAyLjQsIDIuMCwgMS44LCAyLjIsIDIuNiwgMi45LCAxLjUsIDEuMiwgMS4wLCAwLjksIDAuOF0KCm9yZV9mb3JubyA9IGxldHR1cmVbNDo5XQprd2hfZm9ybm8gPSBzdW0ob3JlX2Zvcm5vKQp0b3RhbGVfZ2lvcm5vID0gc3VtKGxldHR1cmUpCnF1b3RhX2Zvcm5vID0gcm91bmQoa3doX2Zvcm5vIC8gdG90YWxlX2dpb3JubyAqIDEwMCwgMSkKcGljY28gPSBtYXgobGV0dHVyZSkKcHJpbnQoZiJGb3Jubzoge2t3aF9mb3JubzouMWZ9IGtXaCBzdSB7dG90YWxlX2dpb3JubzouMWZ9LCBpbCB7cXVvdGFfZm9ybm99JSAocGljY28ge3BpY2NvfSBrV2gpIik='),
    'Passo 3': ('Passo 3', 'Y29uc3VtaV9mZWJicmFpbyA9IHsKICAgICJJVDAwMUUzMTA0NTIwMSI6IDE2NTQuMiwKICAgICJJVDAwMUUzMTA0NTg3NyI6IDgxMi42LAogICAgIklUMDAxRTMxMDQ2MzEwIjogNjkwLjEsCiAgICAiSVQwMDFFMzEwNDcwOTIiOiAzMzEwLjQsCiAgICAiSVQwMDFFMzEwNDc1NTUiOiA0MzEuOCwKICAgICJJVDAwMUUzMTA0ODEyOCI6IDQ4OTAuNywKICAgICJJVDAwMUUzMTA0ODc0MyI6IDExNzguMywKICAgICJJVDAwMUUzMTA0OTMwNiI6IDMyNzYuMCwKfQpzb2dsaWEgPSAyMDAwCgpzb3ByYV9zb2dsaWEgPSBbXQpmb3IgcG9kLCBrd2ggaW4gY29uc3VtaV9mZWJicmFpby5pdGVtcygpOgogICAgaWYga3doID4gc29nbGlhOgogICAgICAgIHNvcHJhX3NvZ2xpYS5hcHBlbmQocG9kKQp0b3RhbGVfa3doID0gc3VtKGNvbnN1bWlfZmViYnJhaW8udmFsdWVzKCkpCnByaW50KGYie2xlbihzb3ByYV9zb2dsaWEpfSBQT0Qgc29wcmEgaSB7c29nbGlhfSBrV2gsIHN1IHt0b3RhbGVfa3doOi4xZn0ga1doIHRvdGFsaSIp'),
    'Passo 4': ('Passo 4', 'ZGVmIGNvc3RvKGt3aCwgcHJlenpvPTAuMjEpOgogICAgIiIiQ29zdG8gaW4gZXVybyBkaSB1biBjb25zdW1vIGluIGtXaCwgYXJyb3RvbmRhdG8gYWkgY2VudGVzaW1pLiIiIgogICAgcmV0dXJuIHJvdW5kKGt3aCAqIHByZXp6bywgMikKCgpjb3N0b19wYW5pZmljaW8gPSBjb3N0bygxNjU0LjIpCmNvc3RvX3NlcnJhID0gY29zdG8oMzI3Ni4wLCBwcmV6em89MC4xNykKcHJpbnQoZiJQYW5pZmljaW86IHtjb3N0b19wYW5pZmljaW99IGV1cm8sIFNlcnJhOiB7Y29zdG9fc2VycmF9IGV1cm8iKQ=='),
    'Passo 5': ('Passo 5', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL2hvbWV3b3JrL2xldHR1cmVfbWFyem8uY3N2Iiwgc2VwPSI7IiwgZGVjaW1hbD0iLCIpCmxldHR1cmUuaW5mbygpCnByaW50KGxldHR1cmUuaGVhZCgpKQpwcmludChsZXR0dXJlLmRlc2NyaWJlKCkpCgptYXNrID0gbGV0dHVyZVsia3doIl0gPiA1MDAKYW5vbWFsZSA9IGxldHR1cmVbbWFza10KYW5vbWFsZS50b19jc3YoImxldHR1cmVfYW5vbWFsZS5jc3YiLCBpbmRleD1GYWxzZSkKYW5vbWFsZQ=='),
    'Passo 6': ('Passo 6', 'aW1wb3J0IHBhbmRhcyBhcyBwZAppbXBvcnQgc3FsaXRlMwoKbGlzdGlubyA9IHBkLnJlYWRfZXhjZWwoIi4uL0RhdGkvaG9tZXdvcmsvY2xpZW50aS54bHN4Iiwgc2hlZXRfbmFtZT0iTGlzdGlubyIpCgpjb24gPSBzcWxpdGUzLmNvbm5lY3QoIi4uL0RhdGkvaG9tZXdvcmsvYW5hZ3JhZmljYS5kYiIpCm9mZmljaW5hID0gcGQucmVhZF9zcWwoIlNFTEVDVCAqIEZST00gcG9kIFdIRVJFIGNsaWVudGUgPSAnT2ZmaWNpbmEgTWVjY2FuaWNhIEZ1bWFnYWxsaSciLCBjb24pCmNvbi5jbG9zZSgpCgpwcmludChsaXN0aW5vKQpvZmZpY2luYQ=='),
}
