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
    '7.3': ('Esercizio 7.3', r'''
assert 0 < len(milano) < len(certificati), "❌ milano deve avere solo le righe della provincia di Milano"
assert len(co2_per_classe) > 1 and co2_per_classe.index.is_unique, "❌ co2_per_classe: una riga per classe energetica, con la media"
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
assert len(fig_carico.data) == 1 and len(fig_carico.data[0].x) == 2976, "❌ Serve una linea sola con le 2976 righe di gennaio: maschera su carico['Date'].dt.month"
assert fig_carico.layout.title.text == "Carico Nord, gennaio 2024", "❌ Il titolo deve essere 'Carico Nord, gennaio 2024'"
assert fig_carico.layout.xaxis.rangeslider.visible and len(fig_carico.layout.xaxis.rangeselector.buttons) == 2, "❌ Servono lo slider e due pulsanti: rangeslider_visible=True e rangeselector=dict(buttons=bottoni_carico)"
'''),
    '9.2': ('Esercizio 9.2', r'''
import os
assert os.path.exists("carico_gennaio.html"), "❌ Il file carico_gennaio.html non c'è: controlla il nome in write_html"
assert os.path.getsize("carico_gennaio.html") < 1_000_000, "❌ Il file è troppo grande: manca include_plotlyjs=\"cdn\""
'''),
    '9.3': ('Esercizio 9.3', r'''
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
assert len(salti) == 1, "❌ salti: deve restare una riga sola, quella con distanze > pd.Timedelta('15min')"
assert salti["Date"].iloc[0] == pd.Timestamp("2024-03-31 03:00"), "❌ salti: la riga attesa è quella delle 3:00 del 31 marzo"
'''),
    'A2.2': ('Esercizio A2.2', r'''
assert round(media_24h.max()) == 27189, "❌ media_24h: rolling su 96 quarti d'ora, poi mean()"
assert picco_24h == pd.Timestamp("2024-07-19 15:30"), "❌ picco_24h: usa media_24h.idxmax()"
'''),
    'E1.1': ('Esercizio E1.1', r'''
assert valore_massimo == 25 and valore_minimo == 7 and differenza == 18, "❌ Controlla max(), min() e la differenza"
assert media == 14.0, "❌ media: (a + b + c) / 3, arrotondata con round(..., 1)"
'''),
    'E1.2': ('Esercizio E1.2', r'''
assert round(area, 6) == 78.539816, "❌ area: math.pi moltiplicato per raggio ** 2"
assert round(circonferenza, 6) == 31.415927, "❌ circonferenza: 2 * math.pi * raggio"
'''),
    'E1.3': ('Esercizio E1.3', r'''
assert lista_invertita == [5, 4, 3, 2, 1], "❌ lista_invertita: slicing con passo -1"
assert ultimi_due == [4, 5] and ogni_due == [1, 3, 5], "❌ ultimi_due è lista[-2:] e ogni_due è lista[::2]"
'''),
    'E1.4': ('Esercizio E1.4', r'''
assert elementi_pari == ["Martina", "Giulia", "Francesca", "Sara"], "❌ elementi_pari: lista[2::2]"
assert uomini == ["Luigi", "Marco", "Simone", "Alessandro", "Lorenzo"] and quanti_uomini == 5, "❌ uomini è lista[1::2] e quanti_uomini è len(uomini)"
'''),
    'E1.5': ('Esercizio E1.5', r'''
assert g8.get('Regno Unito') == 'Londra' and g8.get('Stati Uniti') == 'Washington, D.C.', "❌ Aggiungi le due coppie con g8[chiave] = valore"
assert quanti == 8 and capitale_italia == 'Roma', "❌ quanti è len(g8) e capitale_italia è g8['Italia']"
assert paesi[0] == 'Canada' and paesi[-1] == 'Stati Uniti', "❌ paesi: sorted(g8.keys())"
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
    'E3.1': ('Esercizio E3.1', r'''
assert len(ascolti_103) == 1 and ascolti_103["Plays"].tolist() == [4], "❌ ascolti_103: la maschera è ascolti[\"UserID\"] == 103"
assert list(risposta.columns) == ["Song", "Plays"] and len(risposta) == 1, "❌ risposta: ascolti.loc[cond, [\"Song\", \"Plays\"]]"
'''),
    'E3.2': ('Esercizio E3.2', r'''
assert ascolti_per_canzone.to_dict() == {"Song A": 19, "Song B": 7, "Song C": 1, "Song D": 2}, "❌ ascolti_per_canzone: raggruppa per Song e somma Plays"
assert riepilogo.loc["Song A", "sum"] == 19 and riepilogo.loc["Song A", "count"] == 2, "❌ riepilogo: groupby(\"Song\")[\"Plays\"].agg([\"sum\", \"count\"])"
'''),
    'E3.3': ('Esercizio E3.3', r'''
assert ascolti_per_artista.tolist() == [19, 7, 2, 1] and artista_top == "Artist X", "❌ ascolti_per_artista e artista_top: groupby, sum, sort_values e idxmax"
assert elenco["UserID"].tolist() == [106, 101, 103, 105, 102, 104], "❌ elenco: by=[\"Artist\", \"Plays\"], ascending=[True, False]"
'''),
    'E3.4': ('Esercizio E3.4', r'''
assert utenti_assidui == {101, 103, 105}, "❌ utenti_assidui: set(ascolti.loc[cond, \"UserID\"]) con cond = Plays > 3"
assert ascolti["Length"].tolist() == [3] * 6, "❌ Length: assegna 3 alla colonna nuova"
assert minuti_assidui == 72, "❌ minuti_assidui: somma Plays * Length sulle righe della maschera"
'''),
    'E3.5': ('Esercizio E3.5', r'''
assert isinstance(df_serie.index, pd.DatetimeIndex) and df_serie.index.is_monotonic_increasing, "❌ df_serie: converti timestamp_str, usa set_index e sort_index()"
assert len(periodo) == 22, "❌ periodo: df_serie.loc[\"2025-03-01 12:00\":\"2025-03-01 18:00\"]"
assert intervalli[pd.Timedelta("15min")] == 252 and intervalli[pd.Timedelta("30min")] == 16, "❌ intervalli: df_serie.index.to_series().diff().value_counts()"
'''),
    'E3.6': ('Esercizio E3.6', r'''
assert df_15min["date"].nunique() == 3 and df_15min["is_weekend"].sum() == 192, "❌ date e is_weekend: leggile da df_15min.index"
assert len(media_oraria) == 72 and round(somma_oraria.iloc[0], 1) == 923.7, "❌ media_oraria e somma_oraria: resample(\"h\") con mean() e sum()"
assert media_mobile.isna().sum() == 7 and round(media_mobile.iloc[7], 1) == 237.9, "❌ media_mobile: df_15min[\"power_kw\"].rolling(8).mean()"
'''),
    'S.1': ('Esercizio S.1', r'''
import plotly

assert versione_plotly == plotly.__version__, "❌ versione_plotly: l'attributo __version__ della libreria plotly"
assert comando_aggiungi.strip() == "uv add matplotlib", "❌ comando_aggiungi: il comando uv che aggiunge una libreria, seguito dal nome"
assert comando_collega.strip() == "uv sync", "❌ comando_collega: il comando uv che ricrea l'ambiente dai file del progetto"
'''),
    'S.2': ('Esercizio S.2', r'''
assert output_script.strip() == "Temperatura media: 15.0 gradi", "❌ output_script: la riga stampata dal terminale, tale e quale"
'''),
    'S.3': ('Esercizio S.3', r'''
assert sorted(avvisi) == ["E501", "F401", "F841"], "❌ avvisi: tre codici come stringhe, per l'import inutilizzato, la variabile mai letta e la riga troppo lunga"
assert riepilogo(["12 luglio", "13 luglio"], 30) == "Trovati 2 giorni sopra i 30 gradi nel file meteo_luglio.csv: controllare il sensore sul balcone", "❌ riepilogo: il testo in uscita deve restare identico"
assert riepilogo.__doc__, "❌ riepilogo: manca la docstring"
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
    'E1.1': ('Esercizio E1.1', 'YSA9IDEwCmIgPSAyNQpjID0gNwoKdmFsb3JlX21hc3NpbW8gPSBtYXgoYSwgYiwgYykKdmFsb3JlX21pbmltbyA9IG1pbihhLCBiLCBjKQpkaWZmZXJlbnphID0gdmFsb3JlX21hc3NpbW8gLSB2YWxvcmVfbWluaW1vCm1lZGlhID0gcm91bmQoKGEgKyBiICsgYykgLyAzLCAxKQoKcHJpbnQoZiJWYWxvcmUgbWFzc2ltbzoge3ZhbG9yZV9tYXNzaW1vfSIpICAgIyBPdXRwdXQ6IFZhbG9yZSBtYXNzaW1vOiAyNQpwcmludChmIlZhbG9yZSBtaW5pbW86IHt2YWxvcmVfbWluaW1vfSIpICAgICAjIE91dHB1dDogVmFsb3JlIG1pbmltbzogNwpwcmludChmIkRpZmZlcmVuemE6IHtkaWZmZXJlbnphfSIpICAgICAgICAgICAjIE91dHB1dDogRGlmZmVyZW56YTogMTgKcHJpbnQoZiJNZWRpYToge21lZGlhfSIpICAgICAgICAgICAgICAgICAgICAgIyBPdXRwdXQ6IE1lZGlhOiAxNC4w'),
    'E1.2': ('Esercizio E1.2', 'aW1wb3J0IG1hdGgKCnJhZ2dpbyA9IDUKYXJlYSA9IG1hdGgucGkgKiByYWdnaW8gKiogMgpjaXJjb25mZXJlbnphID0gMiAqIG1hdGgucGkgKiByYWdnaW8KCnByaW50KGYiTCdhcmVhIGRlbCBjZXJjaGlvIMOoOiB7YXJlYTouMmZ9IikgICAjIE91dHB1dDogTCdhcmVhIGRlbCBjZXJjaGlvIMOoOiA3OC41NApwcmludChjaXJjb25mZXJlbnphKSAgICAgICAgICAgICAgICAgICAgICAgICAgIyBPdXRwdXQ6IDMxLjQxNTkyNjUzNTg5Nzkz'),
    'E1.3': ('Esercizio E1.3', 'bGlzdGEgPSBbMSwgMiwgMywgNCwgNV0KCmxpc3RhX2ludmVydGl0YSA9IGxpc3RhWzo6LTFdCnVsdGltaV9kdWUgPSBsaXN0YVstMjpdCm9nbmlfZHVlID0gbGlzdGFbOjoyXQoKcHJpbnQobGlzdGFfaW52ZXJ0aXRhKSAgIyBPdXRwdXQ6IFs1LCA0LCAzLCAyLCAxXQpwcmludCh1bHRpbWlfZHVlLCBvZ25pX2R1ZSkgICMgT3V0cHV0OiBbNCwgNV0gWzEsIDMsIDVd'),
    'E1.4': ('Esercizio E1.4', 'bGlzdGEgPSBbIkVsZW5hIiwgIkx1aWdpIiwgIk1hcnRpbmEiLCAiTWFyY28iLCAiR2l1bGlhIiwgIlNpbW9uZSIsICJGcmFuY2VzY2EiLCAiQWxlc3NhbmRybyIsICJTYXJhIiwgIkxvcmVuem8iXQoKZWxlbWVudGlfcGFyaSA9IGxpc3RhWzI6OjJdCnVvbWluaSA9IGxpc3RhWzE6OjJdCnF1YW50aV91b21pbmkgPSBsZW4odW9taW5pKQoKcHJpbnQoZWxlbWVudGlfcGFyaSkgICMgT3V0cHV0OiBbJ01hcnRpbmEnLCAnR2l1bGlhJywgJ0ZyYW5jZXNjYScsICdTYXJhJ10KcHJpbnQodW9taW5pLCBxdWFudGlfdW9taW5pKSAgIyBPdXRwdXQ6IFsnTHVpZ2knLCAnTWFyY28nLCAnU2ltb25lJywgJ0FsZXNzYW5kcm8nLCAnTG9yZW56byddIDU='),
    'E1.5': ('Esercizio E1.5', 'ZzggPSB7CiAgICAnQ2FuYWRhJzogJ090dGF3YScsCiAgICAnRnJhbmNpYSc6ICdQYXJpZ2knLAogICAgJ0dlcm1hbmlhJzogJ0Jlcmxpbm8nLAogICAgJ0l0YWxpYSc6ICdSb21hJywKICAgICdHaWFwcG9uZSc6ICdUb2t5bycsCiAgICAnUnVzc2lhJzogJ01vc2NhJwp9CgpnOFsnUmVnbm8gVW5pdG8nXSA9ICdMb25kcmEnCmc4WydTdGF0aSBVbml0aSddID0gJ1dhc2hpbmd0b24sIEQuQy4nCgpxdWFudGkgPSBsZW4oZzgpCmNhcGl0YWxlX2l0YWxpYSA9IGc4WydJdGFsaWEnXQpwYWVzaSA9IHNvcnRlZChnOC5rZXlzKCkpCgpwcmludChxdWFudGksIGNhcGl0YWxlX2l0YWxpYSkgICMgT3V0cHV0OiA4IFJvbWEKcHJpbnQocGFlc2kp'),
    'E1.6': ('Esercizio E1.6', 'ZzggPSB7CiAgICAnQ2FuYWRhJzogJ090dGF3YScsCiAgICAnRnJhbmNpYSc6ICdQYXJpZ2knLAogICAgJ0dlcm1hbmlhJzogJ0Jlcmxpbm8nLAogICAgJ0l0YWxpYSc6ICdSb21hJywKICAgICdHaWFwcG9uZSc6ICdUb2t5bycsCiAgICAnUnVzc2lhJzogJ01vc2NhJwp9CgpnOFsnUmVnbm8gVW5pdG8nXSA9ICdMb25kcmEnCmc4WydTdGF0aSBVbml0aSddID0gJ1dhc2hpbmd0b24sIEQuQy4nCgpwcmludChmIklsIEc4IGhhIHtsZW4oZzgpfSBwYWVzaSBlIGxhIGNhcGl0YWxlIGRlbCBHaWFwcG9uZSDDqCB7ZzhbJ0dpYXBwb25lJ119Iik='),
    'E2.1': ('Esercizio E2.1', 'ZGVmIGludmVydGlfc3RyaW5nYShzdHJpbmdhKToKICAgICIiIlJlc3RpdHVpc2NlIGxhIHN0cmluZ2EgbGV0dGEgZGFsbCd1bHRpbW8gY2FyYXR0ZXJlIGFsIHByaW1vLiIiIgogICAgcmV0dXJuIHN0cmluZ2FbOjotMV0KCnVndWFsZSA9IGludmVydGlfc3RyaW5nYSgicmFkYXIiKSA9PSAicmFkYXIiCgpwcmludChpbnZlcnRpX3N0cmluZ2EoIlB5dGhvbiIpKSAgIyBPdXRwdXQ6IG5vaHR5UApwcmludCh1Z3VhbGUpICAgICAgICAgICAgICAgICAgICAgIyBPdXRwdXQ6IFRydWU='),
    'E2.2': ('Esercizio E2.2', 'ZGVmIHBhZXNpX2NhcGl0YWxlX3BhcmkoZGl6aW9uYXJpbyk6CiAgICByaXN1bHRhdG8gPSBbXQogICAgZm9yIHBhZXNlLCBjYXBpdGFsZSBpbiBkaXppb25hcmlvLml0ZW1zKCk6CiAgICAgICAgaWYgbGVuKGNhcGl0YWxlKSAlIDIgPT0gMDoKICAgICAgICAgICAgcmlzdWx0YXRvLmFwcGVuZChwYWVzZSkKICAgIHJldHVybiByaXN1bHRhdG8KCmcxMCA9IHsKICAgICdDYW5hZGEnOiAnT3R0YXdhJywKICAgICdGcmFuY2lhJzogJ1BhcmlnaScsCiAgICAnR2VybWFuaWEnOiAnQmVybGlubycsCiAgICAnSXRhbGlhJzogJ1JvbWEnLAogICAgJ0dpYXBwb25lJzogJ1Rva3lvJywKICAgICdSZWdubyBVbml0byc6ICdMb25kcmEnLAogICAgJ1N0YXRpIFVuaXRpJzogJ1dhc2hpbmd0b24nLAogICAgJ1NwYWduYSc6ICdNYWRyaWQnLAogICAgJ1BhZXNpIEJhc3NpJzogJ0Ftc3RlcmRhbScsCiAgICAnQ29yZWEgZGVsIFN1ZCc6ICdTZW91bCcKfQoKcGFlc2lfcGFyaSA9IHBhZXNpX2NhcGl0YWxlX3BhcmkoZzEwKQpxdWFudGkgPSBsZW4ocGFlc2lfcGFyaSkKCnByaW50KHBhZXNpX3BhcmkpICAjIE91dHB1dDogWydDYW5hZGEnLCAnRnJhbmNpYScsICdJdGFsaWEnLCAnUmVnbm8gVW5pdG8nLCAnU3RhdGkgVW5pdGknLCAnU3BhZ25hJ10KcHJpbnQocXVhbnRpKSAgICAgICMgT3V0cHV0OiA2'),
    'E2.3': ('Esercizio E2.3', 'ZGVmIHRyb3ZhX3BhbGluZHJvbWUobGlzdGFfcGFyb2xlKToKICAgIHJldHVybiBbcGFyb2xhIGZvciBwYXJvbGEgaW4gbGlzdGFfcGFyb2xlIGlmIHBhcm9sYS5sb3dlcigpID09IHBhcm9sYS5sb3dlcigpWzo6LTFdXQoKbGlzdGFfcGFyb2xlID0gWydjaWFvJywgJ2FubmEnLCAncmFkYXInLCAnZ2F0dG8nLCAnb3NzbycsICdtYWRhbSddCnByaW50KHRyb3ZhX3BhbGluZHJvbWUobGlzdGFfcGFyb2xlKSkgICMgT3V0cHV0OiBbJ2FubmEnLCAncmFkYXInLCAnb3NzbycsICdtYWRhbSddCgpjb25fbWFpdXNjb2xlID0gdHJvdmFfcGFsaW5kcm9tZShbJ0FubmEnLCAnUm9tYScsICdPdHRvJywgJ3BhbmUnXSkKcHJpbnQoY29uX21haXVzY29sZSkgICMgT3V0cHV0OiBbJ0FubmEnLCAnT3R0bydd'),
    'E2.4': ('Esercizio E2.4', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KAogICAgIi4uL0RhdGkvbGV0dHVyZV9wb2RfMjAyNS5jc3YiLAogICAgc2VwPSI7IiwgZGVjaW1hbD0iLCIsIGVuY29kaW5nPSJsYXRpbi0xIiwKICAgIHVzZWNvbHM9WyJwb2QiLCAiZmFzY2lhIiwgImt3aCJdLAopCmxldHR1cmUuaW5mbygpCgpyaWdoZSA9IGxlbihsZXR0dXJlKQp0b3RhbGVfa3doID0gbGV0dHVyZVsia3doIl0uc3VtKCkKCnByaW50KHJpZ2hlLCByb3VuZCh0b3RhbGVfa3doLCAxKSkgICMgT3V0cHV0OiAyMTYgMTM0NTA3Ljc='),
    'E2.5': ('Esercizio E2.5', 'aW1wb3J0IHNxbGl0ZTMKCmltcG9ydCBwYW5kYXMgYXMgcGQKCmxpc3Rpbm8gPSBwZC5yZWFkX2V4Y2VsKCIuLi9EYXRpL2JvbGxldHRhX2VzZW1waW8ueGxzeCIsIHNoZWV0X25hbWU9Ikxpc3Rpbm8iKQpwcmV6em9fZjEgPSBsaXN0aW5vWyJldXJfa3doIl1bMF0KCmNvbiA9IHNxbGl0ZTMuY29ubmVjdCgiLi4vRGF0aS91dGlsaXR5LmRiIikKbGV0dHVyZV9kYiA9IHBkLnJlYWRfc3FsKCJTRUxFQ1QgKiBGUk9NIGxldHR1cmUiLCBjb24pCmxldHR1cmVfcG9kID0gcGQucmVhZF9zcWwoIlNFTEVDVCAqIEZST00gbGV0dHVyZSBXSEVSRSBwb2QgPSAnSVQwMDFFMTAwODcxMDknIiwgY29uKQpjb24uY2xvc2UoKQoKbl9sZXR0dXJlID0gbGVuKGxldHR1cmVfZGIpCmt3aF9tYXJ6byA9IGxldHR1cmVfZGJbImt3aCJdLnN1bSgpCgpwcmludChwcmV6em9fZjEpICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIyBPdXRwdXQ6IDAuMjEKcHJpbnQobl9sZXR0dXJlLCByb3VuZChrd2hfbWFyem8sIDEpLCBsZW4obGV0dHVyZV9wb2QpKSAgICMgT3V0cHV0OiA5MzAgNjk4ODAuMSAzMQ=='),
    'E2.6': ('Esercizio E2.6', 'aW1wb3J0IHBhbmRhcyBhcyBwZAppbXBvcnQgcmVxdWVzdHMKCgpkZWYgc2Vuc29yaShwcm92aW5jaWEpOgogICAgIiIiQW5hZ3JhZmljYSBkZWkgc2Vuc29yaSBtZXRlbyBkaSBSZWdpb25lIExvbWJhcmRpYSBpbiB1bmEgcHJvdmluY2lhLCBjb21lIERhdGFGcmFtZS4iIiIKICAgIHVybCA9ICJodHRwczovL3d3dy5kYXRpLmxvbWJhcmRpYS5pdC9yZXNvdXJjZS9uZjc4LW5qNmIuanNvbiIKICAgIHJlc3BvbnNlID0gcmVxdWVzdHMuZ2V0KHVybCwgcGFyYW1zPXsicHJvdmluY2lhIjogcHJvdmluY2lhfSwgdGltZW91dD0zMCkKICAgIHJlc3BvbnNlLnJhaXNlX2Zvcl9zdGF0dXMoKQogICAgcmV0dXJuIHBkLkRhdGFGcmFtZShyZXNwb25zZS5qc29uKCkpCgoKc2Vuc29yaV9taSA9IHNlbnNvcmkoIk1JIikKc2Vuc29yaV9taS5oZWFkKCkKCgojIHNlIGlsIHBvcnRhbGUgbm9uIHJpc3BvbmRlLCBuZWxsYSBzZWNvbmRhIGNlbGxhCmltcG9ydCBqc29uCgppbXBvcnQgcGFuZGFzIGFzIHBkCgp3aXRoIG9wZW4oIi4uL0RhdGkvZmFsbGJhY2svbG9tYmFyZGlhX3NlbnNvcmkuanNvbiIsIGVuY29kaW5nPSJ1dGYtOCIpIGFzIGY6CiAgICB0dXR0aSA9IHBkLkRhdGFGcmFtZShqc29uLmxvYWQoZikpCnNlbnNvcmlfbWkgPSB0dXR0aVt0dXR0aVsicHJvdmluY2lhIl0gPT0gIk1JIl0Kc2Vuc29yaV9taS5oZWFkKCk='),
    'E2.7': ('Esercizio E2.7', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKZGVmIGxlZ2dpX2Nzdl9pdGFsaWFubyhwZXJjb3Jzbyk6CiAgICAiIiJMZWdnZSB1biBDU1Ygc2FsdmF0byBkYSBFeGNlbCBpbiBpdGFsaWFubyBlIGxvIHJlc3RpdHVpc2NlIGNvbWUgRGF0YUZyYW1lLiIiIgogICAgcmV0dXJuIHBkLnJlYWRfY3N2KHBlcmNvcnNvLCBzZXA9IjsiLCBkZWNpbWFsPSIsIiwgZW5jb2Rpbmc9ImxhdGluLTEiKQoKbGV0dHVyZSA9IGxlZ2dpX2Nzdl9pdGFsaWFubygiLi4vRGF0aS9sZXR0dXJlX3BvZF8yMDI1LmNzdiIpCmxldHR1cmUuaW5mbygp'),
    'E3.1': ('Esercizio E3.1', 'Y29uZCA9IGFzY29sdGlbIlVzZXJJRCJdID09IDEwMwphc2NvbHRpXzEwMyA9IGFzY29sdGlbY29uZF0KcmlzcG9zdGEgPSBhc2NvbHRpLmxvY1tjb25kLCBbIlNvbmciLCAiUGxheXMiXV0KcmlzcG9zdGE='),
    'E3.2': ('Esercizio E3.2', 'YXNjb2x0aV9wZXJfY2Fuem9uZSA9IGFzY29sdGkuZ3JvdXBieSgiU29uZyIpWyJQbGF5cyJdLnN1bSgpCnJpZXBpbG9nbyA9IGFzY29sdGkuZ3JvdXBieSgiU29uZyIpWyJQbGF5cyJdLmFnZyhbInN1bSIsICJjb3VudCJdKQpyaWVwaWxvZ28='),
    'E3.3': ('Esercizio E3.3', 'YXNjb2x0aV9wZXJfYXJ0aXN0YSA9IGFzY29sdGkuZ3JvdXBieSgiQXJ0aXN0IilbIlBsYXlzIl0uc3VtKCkuc29ydF92YWx1ZXMoYXNjZW5kaW5nPUZhbHNlKQphcnRpc3RhX3RvcCA9IGFzY29sdGlfcGVyX2FydGlzdGEuaWR4bWF4KCkKCmVsZW5jbyA9IGFzY29sdGkuc29ydF92YWx1ZXMoYnk9WyJBcnRpc3QiLCAiUGxheXMiXSwgYXNjZW5kaW5nPVtUcnVlLCBGYWxzZV0pCnByaW50KGFydGlzdGFfdG9wKSAgIyBPdXRwdXQ6IEFydGlzdCBYCmVsZW5jbw=='),
    'E3.4': ('Esercizio E3.4', 'Y29uZCA9IGFzY29sdGlbIlBsYXlzIl0gPiAzCnV0ZW50aV9hc3NpZHVpID0gc2V0KGFzY29sdGkubG9jW2NvbmQsICJVc2VySUQiXSkKCmFzY29sdGlbIkxlbmd0aCJdID0gMwptaW51dGkgPSBhc2NvbHRpWyJQbGF5cyJdICogYXNjb2x0aVsiTGVuZ3RoIl0KbWludXRpX2Fzc2lkdWkgPSBtaW51dGlbY29uZF0uc3VtKCkKCnByaW50KHV0ZW50aV9hc3NpZHVpKSAgIyBPdXRwdXQ6IHsxMDUsIDEwMSwgMTAzfQpwcmludChtaW51dGlfYXNzaWR1aSkgICMgT3V0cHV0OiA3Mg=='),
    'E3.5': ('Esercizio E3.5', 'ZGZbInRpbWVzdGFtcCJdID0gcGQudG9fZGF0ZXRpbWUoZGZbInRpbWVzdGFtcF9zdHIiXSwgZm9ybWF0PSIlZC8lbS8lWSAlSDolTSIpCmRmX3NlcmllID0gZGZbWyJ0aW1lc3RhbXAiLCAicG93ZXJfa3ciLCAidGVtcF9jIl1dLnNldF9pbmRleCgidGltZXN0YW1wIikuc29ydF9pbmRleCgpCgpwZXJpb2RvID0gZGZfc2VyaWUubG9jWyIyMDI1LTAzLTAxIDEyOjAwIjoiMjAyNS0wMy0wMSAxODowMCJdCmludGVydmFsbGkgPSBkZl9zZXJpZS5pbmRleC50b19zZXJpZXMoKS5kaWZmKCkudmFsdWVfY291bnRzKCkKCnByaW50KGxlbihwZXJpb2RvKSkgICMgT3V0cHV0OiAyMgppbnRlcnZhbGxp'),
    'E3.6': ('Esercizio E3.6', 'IyBsYSBzZXJpZSBkZWxsJ2VzZXJjaXppbyBFMy41LCBjb24gaSBidWNoaSByaWVtcGl0aSBkYWxsJ2ludGVycG9sYXppb25lIGNvbWUgbmVsIG5vdGVib29rIDA4CmRmWyJ0aW1lc3RhbXAiXSA9IHBkLnRvX2RhdGV0aW1lKGRmWyJ0aW1lc3RhbXBfc3RyIl0sIGZvcm1hdD0iJWQvJW0vJVkgJUg6JU0iKQpkZl9zZXJpZSA9IGRmW1sidGltZXN0YW1wIiwgInBvd2VyX2t3IiwgInRlbXBfYyJdXS5zZXRfaW5kZXgoInRpbWVzdGFtcCIpLnNvcnRfaW5kZXgoKQpkZl8xNW1pbiA9IGRmX3NlcmllLmFzZnJlcSgiMTVtaW4iKS5pbnRlcnBvbGF0ZShtZXRob2Q9ImxpbmVhciIpCgpkZl8xNW1pblsiZGF0ZSJdID0gZGZfMTVtaW4uaW5kZXguZGF0ZQpkZl8xNW1pblsiaXNfd2Vla2VuZCJdID0gZGZfMTVtaW4uaW5kZXguZGF5b2Z3ZWVrID49IDUKCm1lZGlhX29yYXJpYSA9IGRmXzE1bWluWyJwb3dlcl9rdyJdLnJlc2FtcGxlKCJoIikubWVhbigpCnNvbW1hX29yYXJpYSA9IGRmXzE1bWluWyJwb3dlcl9rdyJdLnJlc2FtcGxlKCJoIikuc3VtKCkKbWVkaWFfbW9iaWxlID0gZGZfMTVtaW5bInBvd2VyX2t3Il0ucm9sbGluZyg4KS5tZWFuKCkKCnByaW50KGRmXzE1bWluWyJpc193ZWVrZW5kIl0uc3VtKCkpICAjIE91dHB1dDogMTkyCm1lZGlhX21vYmlsZS5oZWFkKDEwKQ=='),
    'E3.7': ('Esercizio E3.7', 'IyBsYSBzZXJpZSBkZWxsJ2VzZXJjaXppbyBFMy41LCBjb24gaSBidWNoaSByaWVtcGl0aSBkYWxsJ2ludGVycG9sYXppb25lIGNvbWUgbmVsIG5vdGVib29rIDA4CmRmWyJ0aW1lc3RhbXAiXSA9IHBkLnRvX2RhdGV0aW1lKGRmWyJ0aW1lc3RhbXBfc3RyIl0sIGZvcm1hdD0iJWQvJW0vJVkgJUg6JU0iKQpkZl9zZXJpZSA9IGRmW1sidGltZXN0YW1wIiwgInBvd2VyX2t3IiwgInRlbXBfYyJdXS5zZXRfaW5kZXgoInRpbWVzdGFtcCIpLnNvcnRfaW5kZXgoKQpkZl8xNW1pbiA9IGRmX3NlcmllLmFzZnJlcSgiMTVtaW4iKS5pbnRlcnBvbGF0ZShtZXRob2Q9ImxpbmVhciIpCgpnaW9ybmFsaWVyYSA9IGRmXzE1bWluWyJwb3dlcl9rdyJdLnJlc2FtcGxlKCJEIikubWVhbigpCgpmb3IgZ2lvcm5vLCB2YWxvcmUgaW4gZ2lvcm5hbGllcmEuaXRlbXMoKToKICAgIHByaW50KGYie2dpb3Juby5zdHJmdGltZSgnJWQvJW0vJVknKX06IHt2YWxvcmU6LjFmfSBrVyIpCiMgT3V0cHV0OgojIDAxLzAzLzIwMjU6IDIxOC43IGtXCiMgMDIvMDMvMjAyNTogMjIwLjMga1cKIyAwMy8wMy8yMDI1OiAyMjAuMSBrVw=='),
}
