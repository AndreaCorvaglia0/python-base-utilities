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
assert valore_massimo == 25, "❌ Valore massimo errato"
assert valore_minimo == 7, "❌ Valore minimo errato"
assert differenza == 18, "❌ Differenza errata"
'''),
    '1.2': ('Esercizio 1.2', r'''
assert math.isclose(area, 78.54, rel_tol=1e-3), "❌ Area errata"
'''),
    '1.3': ('Esercizio 1.3', r'''
assert ore == 2, "❌ ore: quante volte 60 sta in 137"
assert minuti == 17, "❌ minuti: il resto della divisione per 60"
'''),
    '2.1': ('Esercizio 2.1', r'''
assert lista_invertita == [5, 4, 3, 2, 1], "❌ Lista invertita errata"
'''),
    '2.2': ('Esercizio 2.2', r'''
assert elementi_pari == ["Martina", "Giulia", "Francesca", "Sara"], "❌ Elementi pari errati"
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
assert inverti_stringa("Python") == "nohtyP", "❌ Stringa invertita errata"
'''),
    '4.2': ('Esercizio 4.2', r'''
atteso = ['Canada', 'Francia', 'Italia', 'Regno Unito', 'Stati Uniti', 'Spagna']
assert paesi_capitale_pari(g10) == atteso, "❌ Lista dei paesi errata"
'''),
    '4.3': ('Esercizio 4.3', r'''
assert trova_palindrome(lista_parole) == ['anna', 'radar', 'osso', 'madam'], "❌ Lista delle parole palindrome errata"
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
assert len(vendite) == 6 and list(vendite.index) == list(range(6)), "❌ vendite: 6 righe con indice da 0 a 5 (ignore_index=True)"
assert vendite["pezzi"].sum() == 500, "❌ vendite: il totale dei pezzi è 500"
'''),
    '6.3': ('Esercizio 6.3', r'''
assert len(letture_pod) == 31, "❌ letture_pod: servono le 31 righe del solo POD IT001E10000000"
assert round(totale_marzo, 1) == 7785.6, "❌ totale_marzo: somma la colonna kwh"
'''),
    '6.4': ('Esercizio 6.4', r'''
assert 0 < len(milano) < len(certificati), "❌ milano deve avere solo le righe della provincia di Milano"
assert len(co2_per_classe) > 1 and co2_per_classe.index.is_unique, "❌ co2_per_classe: una riga per classe energetica, con la media"
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
assert round(giornaliero.max()) == 644863, "❌ giornaliero: somma dei quarti d'ora del giorno, divisa per 4"
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
from pathlib import Path
assert Path("carico_gennaio.html").exists(), "❌ Il file carico_gennaio.html non c'è: controlla il nome in write_html"
assert Path("carico_gennaio.html").stat().st_size < 1_000_000, "❌ Il file è troppo grande: manca include_plotlyjs=\"cdn\""
'''),
    'A2.2': ('Esercizio A2.2', r'''
assert round(media_24h.max()) == 27189, "❌ media_24h: rolling su 96 quarti d'ora, poi mean()"
assert picco_24h == pd.Timestamp("2024-07-19 15:30"), "❌ picco_24h: usa media_24h.idxmax()"
'''),
    'E1.1': ('Esercizio E1.1', r'''
assert fattore == 2 and pasta_g == 640 and guanciale_g == 400 and pecorino_g == 200, "❌ Controlla fattore e quantità: ogni dose va moltiplicata per invitati / persone_ricetta"
assert uova == 8 and isinstance(uova, int), "❌ uova deve valere 8 ed essere un intero: usa round()"
assert costo_pasta == 1.54, "❌ costo_pasta: porta i grammi in chili, moltiplica per il prezzo e arrotonda con round(..., 2)"
'''),
    'E1.2': ('Esercizio E1.2', r'''
assert piatto_titolo == "Spaghetti alla carbonara" and lunghezza == 24, "❌ Controlla piatto_titolo (piatto.capitalize()) e lunghezza (len())"
assert "Marta" in messaggio and "sabato" in messaggio and "20:30" in messaggio and "in 8" in messaggio and "Spaghetti alla carbonara" in messaggio, "❌ messaggio: controlla che contenga padrona di casa, giorno, ora, invitati e piatto_titolo"
assert "2.56" in messaggio and "2.5625" not in messaggio, "❌ messaggio: la quota va scritta con due decimali, con {quota:.2f}"
'''),
    'E1.3': ('Esercizio E1.3', r'''
assert spesa == ["guanciale", "pecorino", "pepe nero", "spaghetti", "uova", "vino"], "❌ spesa: controlla append, remove, insert e l'ordinamento finale con .sort()"
assert primi_tre == ["spaghetti", "pepe nero", "uova"], "❌ primi_tre: va preso con [:3] dopo insert e prima di .sort()"
assert quanti == 6, "❌ quanti: la lista finale ha 6 prodotti"
'''),
    'E1.4': ('Esercizio E1.4', r'''
assert prezzi.get("pepe nero") == 2.15 and prezzi["guanciale"] == 7.90, "❌ prezzi: aggiungi il pepe nero e correggi il prezzo del guanciale"
assert round(totale, 2) == 20.5 and prodotti == ["spaghetti", "guanciale", "uova", "pecorino", "pepe nero"], "❌ Controlla totale (sum dei valori) e prodotti (list delle chiavi)"
assert quota == 2.56, "❌ quota: dividi il totale per gli invitati e arrotonda con round(..., 2)"
'''),
    'E1.5': ('Esercizio E1.5', r'''
assert carrello == {"spaghetti", "guanciale", "uova", "vino", "pecorino", "pane"} and in_comune == {"uova", "vino"}, "❌ Controlla carrello (union) e in_comune (intersection)"
assert solo_luca == {"pecorino", "pane"}, "❌ solo_luca: parti dal set di Luca e togli quello di Marta con difference()"
assert isinstance(indirizzo, tuple) and civico == 14, "❌ indirizzo deve essere una tupla e civico il suo elemento di indice 1"
'''),
    'E1.6': ('Esercizio E1.6', r'''
assert allergie == {"lattosio", "noci", "crostacei"}, "❌ allergie: trasforma la lista in un set con set()"
assert quante == 3, "❌ quante: conta gli elementi del set con len()"
assert problema_lattosio is True and problema_uova is False, "❌ Controlla i due booleani: ciascuno è un controllo con in sul set allergie"
'''),
    'E1.7': ('Esercizio E1.7', r'''
assert bottiglie == 3 and prezzo_bottiglia == 7.9 and invitati == 8, "❌ Controlla nomi e valori di bottiglie, prezzo_bottiglia e invitati"
assert quota_vino == T, "❌ quota_vino deve avere lo stesso valore di T"
'''),
    'E2.1': ('Esercizio E2.1', r'''
assert sopra_soglia == [64.0, 51.2, 120.0, 89.9, 72.6] and quante == 5, "❌ sopra_soglia: tieni le 5 spese maggiori di 50"
assert round(totale_sopra, 2) == 397.7, "❌ totale_sopra: somma solo le spese sopra la soglia, dentro l'if"
assert round(totale, 2) == 578.8, "❌ totale: somma tutta la lista con sum(spese)"
'''),
    'E2.2': ('Esercizio E2.2', r'''
assert prezzo_scontato.__doc__, "❌ Manca la docstring sotto il def"
assert normale == 44.91 and promozione == 34.93, "❌ normale vale 44.91 e promozione 34.93"
assert intero == 35 and prezzo_scontato(80) == 72.0, "❌ intero: con arrotonda=0 il prezzo è 35.0"
'''),
    'E2.3': ('Esercizio E2.3', r'''
assert list(letture.columns) == ["pod", "fascia", "kwh"], "❌ Con usecols leggi solo pod, fascia e kwh"
assert letture["kwh"].dtype == "float64" and righe == 216, "❌ kwh deve essere numerica e le righe 216"
assert round(totale_kwh, 1) == 134507.7, "❌ totale_kwh: somma la colonna kwh"
'''),
    'E2.4': ('Esercizio E2.4', r'''
assert righe_consumi == 72 and righe_listino == 3, "❌ Il foglio Consumi ha 72 righe e il Listino 3"
assert prezzo_f1 == 0.21, "❌ prezzo_f1: il prezzo della fascia F1 è 0.21"
assert nomi_fogli == ["Consumi", "Listino", "Anagrafica"], "❌ nomi_fogli: leggi tutti i fogli con sheet_name=None"
'''),
    'E2.5': ('Esercizio E2.5', r'''
assert n_letture == 930 and list(letture_db.columns) == ["pod", "data", "kwh"], "❌ letture_db: leggi tutta la tabella letture"
assert round(kwh_marzo, 1) == 69880.1, "❌ kwh_marzo: somma la colonna kwh di letture_db"
assert len(letture_pod) == 31 and set(letture_pod["pod"]) == {"IT001E10087109"}, "❌ letture_pod: filtra con WHERE pod = '...'"
'''),
    'E2.6': ('Esercizio E2.6', r'''
assert totali == {"gennaio": 161.7, "febbraio": 108.7, "marzo": 187.1}, "❌ totali: una chiave per mese, con la somma arrotondata"
assert round(totale_trimestre, 2) == 457.5, "❌ totale_trimestre: somma i valori di totali"
'''),
    'E2.7': ('Esercizio E2.7', r'''
import os
assert os.path.exists("riepilogo_fascia.xlsx"), "❌ Non trovo riepilogo_fascia.xlsx nella cartella del notebook"
assert len(f3) == 72 and len(riletto) == len(f3), "❌ Il file deve avere le 72 righe della fascia F3"
assert list(riletto.columns) == ["pod", "cliente", "data", "fascia", "kwh"], "❌ Colonne diverse dal CSV: hai usato index=False?"
'''),
    'E2.8': ('Esercizio E2.8', r'''
assert len(sensori_mi) > 0, "❌ sensori_mi è vuoto: hai chiamato sensori(\"MI\") o letto il file di riserva?"
assert {"idsensore", "tipologia", "provincia"} <= set(sensori_mi.columns), "❌ Mancano le colonne dell'anagrafica"
assert set(sensori_mi["provincia"]) == {"MI"}, "❌ sensori_mi deve contenere solo la provincia MI"
'''),
    'E3.1': ('Esercizio E3.1', r'''
assert {"potenza_kw", "vento_ms", "direzione", "pressione", "temperatura"} <= set(turbina.columns), "❌ turbina: controlla i nomi passati a rename"
assert primo == pd.Timestamp("2023-01-01 00:00") and ultimo == pd.Timestamp("2023-12-31 23:00"), "❌ primo, ultimo: controlla il formato e l'ordinamento dell'indice"
assert ordinato and len(passi) == 1 and passi.iloc[0] == 8759, "❌ passi: tutti gli 8759 intervalli devono valere un'ora"
'''),
    'E3.2': ('Esercizio E3.2', r'''
assert ore_luglio == 744, "❌ ore_luglio: seleziona il mese con loc e una data parziale"
assert n_ventose == 645 and ore_ferme == 822, "❌ n_ventose, ore_ferme: controlla le due maschere"
assert len(ventose_query) == 645, "❌ ventose_query: dentro query il nome della colonna va senza virgolette"
'''),
    'E3.3': ('Esercizio E3.3', r'''
assert len(mensile) == 12, "❌ mensile: resample(\"ME\") produce un valore per ogni mese"
assert mese_migliore == pd.Timestamp("2023-04-30") and mese_peggiore == pd.Timestamp("2023-09-30"), "❌ mese_migliore, mese_peggiore: usa idxmax() e idxmin()"
assert round(mensile_vento.loc["2023-04-30", "vento_ms"], 1) == 8.5, "❌ mensile_vento: la colonna vento_ms è la media del mese"
'''),
    'E3.4': ('Esercizio E3.4', r'''
assert len(profilo) == 24 and ora_migliore == 16, "❌ profilo, ora_migliore: raggruppa per turbina.index.hour e usa idxmax()"
assert list(profilo_stat.columns) == ["mean", "max"], "❌ profilo_stat: passa ad agg la lista [\"mean\", \"max\"]"
assert round(profilo_stat["max"].max(), 1) == 3004.0, "❌ profilo_stat: la colonna max è la potenza massima di ogni ora"
'''),
    'E3.5': ('Esercizio E3.5', r'''
assert len(unione) == 365 and senza_intervento == 361, "❌ unione, senza_intervento: left join con giornaliera a sinistra, poi isnull().sum()"
assert (unione["motivo"] == "nessuna").sum() == 361, "❌ motivo: riempi i NaN con fillna(\"nessuna\") e riassegna la colonna"
assert len(solo_interventi) == 4, "❌ solo_interventi: con how=\"inner\" restano i quattro giorni presenti in entrambe le tabelle"
'''),
    'E3.6': ('Esercizio E3.6', r'''
assert len(settimanale) == 7, "❌ settimanale: raggruppa per turbina.index.dayofweek"
assert giorno_migliore == "lunedì", "❌ giorno_migliore: usa settimanale.idxmax() come posizione in giorni"
'''),
    'E3.7': ('Esercizio E3.7', r'''
from pathlib import Path
assert Path("energia_mensile.csv").exists() and Path("energia_mensile.xlsx").exists(), "❌ i due file non sono nella cartella del notebook"
assert len(riletto) == 12 and stesse_righe, "❌ riletto: il CSV deve avere 12 righe, una per mese"
assert str(riletto["data"].dtype).startswith("datetime64"), "❌ riletto: aggiungi parse_dates=[\"data\"] a read_csv"
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
assert list(anagrafica.columns) == ["pod", "cliente", "comune"] and set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ anagrafica e listino: controlla sheet_name"
assert leggi_tabella("pod").shape == (8, 3), "❌ leggi_tabella: deve restituire tutta la tabella, 8 righe e 3 colonne"
assert list(officina["potenza_kw"]) == [30.0], "❌ officina: una riga sola, quella dell'Officina Meccanica Fumagalli"
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
assert len(df_giornaliero) == 731 and df_giornaliero["Energia [MWh]"].between(250_000, 700_000).all(), "❌ df_giornaliero: 731 giorni, con l'energia tra 250.000 e 700.000 MWh (somma dei quartorari divisa per 4)"
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
    'E1.1': ('Esercizio E1.1', 'cGVyc29uZV9yaWNldHRhID0gNAppbnZpdGF0aSA9IDgKcHJlenpvX3Bhc3RhX2tnID0gMi40MAoKZmF0dG9yZSA9IGludml0YXRpIC8gcGVyc29uZV9yaWNldHRhCnBhc3RhX2cgPSAzMjAgKiBmYXR0b3JlCmd1YW5jaWFsZV9nID0gMjAwICogZmF0dG9yZQpwZWNvcmlub19nID0gMTAwICogZmF0dG9yZQp1b3ZhID0gcm91bmQoNCAqIGZhdHRvcmUpCmNvc3RvX3Bhc3RhID0gcm91bmQocGFzdGFfZyAvIDEwMDAgKiBwcmV6em9fcGFzdGFfa2csIDIpCgpwcmludChmYXR0b3JlLCBwYXN0YV9nLCBndWFuY2lhbGVfZywgcGVjb3Jpbm9fZywgdW92YSkKcHJpbnQoY29zdG9fcGFzdGEp'),
    'E1.2': ('Esercizio E1.2', 'Z2lvcm5vID0gInNhYmF0byIKb3JhID0gIjIwOjMwIgpwYWRyb25hX2RpX2Nhc2EgPSAiTWFydGEiCmludml0YXRpID0gOApwaWF0dG8gPSAic3BhZ2hldHRpIGFsbGEgY2FyYm9uYXJhIgpzcGVzYSA9IDIwLjUwCgpwaWF0dG9fdGl0b2xvID0gcGlhdHRvLmNhcGl0YWxpemUoKQpsdW5naGV6emEgPSBsZW4ocGlhdHRvX3RpdG9sbykKcXVvdGEgPSBzcGVzYSAvIGludml0YXRpCm1lc3NhZ2dpbyA9ICgKICAgIGYiQ2VuYSBkYSB7cGFkcm9uYV9kaV9jYXNhfSB7Z2lvcm5vfSBhbGxlIHtvcmF9OiBzaWFtbyBpbiB7aW52aXRhdGl9LCAiCiAgICBmInByZXBhcmlhbW8ge3BpYXR0b190aXRvbG99IGUgbGEgc3Blc2Egw6ggZGkge3F1b3RhOi4yZn0gZXVybyBhIHRlc3RhLiIKKQoKcHJpbnQobWVzc2FnZ2lvKQpwcmludChsdW5naGV6emEp'),
    'E1.3': ('Esercizio E1.3', 'c3Blc2EgPSBbInNwYWdoZXR0aSIsICJ1b3ZhIiwgInBlY29yaW5vIiwgInBhbmUiLCAidmlubyJdCgpzcGVzYS5hcHBlbmQoImd1YW5jaWFsZSIpCnNwZXNhLnJlbW92ZSgicGFuZSIpCnNwZXNhLmluc2VydCgxLCAicGVwZSBuZXJvIikKcHJpbWlfdHJlID0gc3Blc2FbOjNdCnF1YW50aSA9IGxlbihzcGVzYSkKc3Blc2Euc29ydCgpCgpwcmludChwcmltaV90cmUpCnByaW50KHF1YW50aSkKcHJpbnQoc3Blc2Ep'),
    'E1.4': ('Esercizio E1.4', 'cHJlenppID0geyJzcGFnaGV0dGkiOiAyLjU4LCAiZ3VhbmNpYWxlIjogOC45MCwgInVvdmEiOiAzLjQ5LCAicGVjb3Jpbm8iOiA0LjM4fQppbnZpdGF0aSA9IDgKCnByZXp6aVsicGVwZSBuZXJvIl0gPSAyLjE1CnByZXp6aVsiZ3VhbmNpYWxlIl0gPSA3LjkwCnRvdGFsZSA9IHN1bShwcmV6emkudmFsdWVzKCkpCnByb2RvdHRpID0gbGlzdChwcmV6emkua2V5cygpKQpxdW90YSA9IHJvdW5kKHRvdGFsZSAvIGludml0YXRpLCAyKQoKcHJpbnQodG90YWxlLCBxdW90YSkKcHJpbnQocHJvZG90dGkp'),
    'E1.5': ('Esercizio E1.5', 'bGlzdGFfbWFydGEgPSBbInNwYWdoZXR0aSIsICJndWFuY2lhbGUiLCAidW92YSIsICJ2aW5vIl0KbGlzdGFfbHVjYSA9IFsidmlubyIsICJwZWNvcmlubyIsICJwYW5lIiwgInVvdmEiXQoKbWFydGEgPSBzZXQobGlzdGFfbWFydGEpCmx1Y2EgPSBzZXQobGlzdGFfbHVjYSkKY2FycmVsbG8gPSBtYXJ0YS51bmlvbihsdWNhKQppbl9jb211bmUgPSBtYXJ0YS5pbnRlcnNlY3Rpb24obHVjYSkKc29sb19sdWNhID0gbHVjYS5kaWZmZXJlbmNlKG1hcnRhKQoKaW5kaXJpenpvID0gKCJ2aWEgR2FyaWJhbGRpIiwgMTQsICJCb2xvZ25hIikKY2l2aWNvID0gaW5kaXJpenpvWzFdCgpwcmludChjYXJyZWxsbykKcHJpbnQoaW5fY29tdW5lLCBzb2xvX2x1Y2EpCnByaW50KGNpdmljbyk='),
    'E1.6': ('Esercizio E1.6', 'cmlzcG9zdGUgPSBbImxhdHRvc2lvIiwgIm5vY2kiLCAibGF0dG9zaW8iLCAiY3Jvc3RhY2VpIiwgIm5vY2kiXQoKYWxsZXJnaWUgPSBzZXQocmlzcG9zdGUpCnF1YW50ZSA9IGxlbihhbGxlcmdpZSkKcHJvYmxlbWFfbGF0dG9zaW8gPSAibGF0dG9zaW8iIGluIGFsbGVyZ2llCnByb2JsZW1hX3VvdmEgPSAidW92YSIgaW4gYWxsZXJnaWUKCnByaW50KGFsbGVyZ2llLCBxdWFudGUpCnByaW50KHByb2JsZW1hX2xhdHRvc2lvLCBwcm9ibGVtYV91b3ZhKQ=='),
    'E1.7': ('Esercizio E1.7', 'Qj0zCnA9Ny45Ck49OApUPUIqcC9OICMgbW9sdGlwbGljbyBlIGRpdmlkbwpwcmludChUKQoKYm90dGlnbGllID0gMwpwcmV6em9fYm90dGlnbGlhID0gNy45Cmludml0YXRpID0gOAojIGlsIHZpbm8gc2kgcGFnYSBpbiBwYXJ0aSB1Z3VhbGkgdHJhIHR1dHRpIGdsaSBpbnZpdGF0aQpxdW90YV92aW5vID0gYm90dGlnbGllICogcHJlenpvX2JvdHRpZ2xpYSAvIGludml0YXRpCnByaW50KFQsIHF1b3RhX3Zpbm8p'),
    'E1.8': ('Esercizio E1.8', 'IyBOZWxsYSBjZWxsYSBNYXJrZG93biBzb3ByYSBxdWVzdGEsIHBlciBlc2VtcGlvOgojCiMgIyBNZW51IGRlbGxhIGNlbmEgZGEgTWFydGEKIwojIC0gQnJ1c2NoZXR0ZSBhbCBwb21vZG9ybwojIC0gU3BhZ2hldHRpIGFsbGEgY2FyYm9uYXJhCiMgLSBUaXJhbWlzw7kKCnByZXp6aSA9IHsic3BhZ2hldHRpIjogMi41OCwgImd1YW5jaWFsZSI6IDcuOTAsICJ1b3ZhIjogMy40OSwgInBlY29yaW5vIjogNC4zOCwgInBlcGUgbmVybyI6IDIuMTV9CgpwcmludChmInNwYWdoZXR0aSAgIHtwcmV6emlbJ3NwYWdoZXR0aSddOi4yZn0gZXVybyIpCnByaW50KGYiZ3VhbmNpYWxlICAge3ByZXp6aVsnZ3VhbmNpYWxlJ106LjJmfSBldXJvIikKcHJpbnQoZiJ1b3ZhICAgICAgICB7cHJlenppWyd1b3ZhJ106LjJmfSBldXJvIikKcHJpbnQoZiJwZWNvcmlubyAgICB7cHJlenppWydwZWNvcmlubyddOi4yZn0gZXVybyIpCnByaW50KGYicGVwZSBuZXJvICAge3ByZXp6aVsncGVwZSBuZXJvJ106LjJmfSBldXJvIikKcHJpbnQoZiJ0b3RhbGUgICAgICB7c3VtKHByZXp6aS52YWx1ZXMoKSk6LjJmfSBldXJvIik='),
    'E2.1': ('Esercizio E2.1', 'c3Blc2UgPSBbMTIuNSwgNjQuMCwgOC45LCA1MS4yLCAyMy4wLCAxMjAuMCwgNDUuNSwgNy44LCA4OS45LCA1MC4wLCAzMy40LCA3Mi42XQpzb2dsaWEgPSA1MAoKc29wcmFfc29nbGlhID0gW10KdG90YWxlX3NvcHJhID0gMApmb3Igc3Blc2EgaW4gc3Blc2U6CiAgICBpZiBzcGVzYSA+IHNvZ2xpYToKICAgICAgICBzb3ByYV9zb2dsaWEuYXBwZW5kKHNwZXNhKQogICAgICAgIHRvdGFsZV9zb3ByYSA9IHRvdGFsZV9zb3ByYSArIHNwZXNhCgpxdWFudGUgPSBsZW4oc29wcmFfc29nbGlhKQp0b3RhbGUgPSBzdW0oc3Blc2UpCgpwcmludChzb3ByYV9zb2dsaWEpICAgICAgICAgICAgICAjIE91dHB1dDogWzY0LjAsIDUxLjIsIDEyMC4wLCA4OS45LCA3Mi42XQpwcmludChxdWFudGUsIHJvdW5kKHRvdGFsZV9zb3ByYSwgMiksIHRvdGFsZSkgICMgT3V0cHV0OiA1IDM5Ny43IDU3OC44'),
    'E2.2': ('Esercizio E2.2', 'ZGVmIHByZXp6b19zY29udGF0byhwcmV6em8sIHNjb250bz0xMCwgYXJyb3RvbmRhPTIpOgogICAgIiIiUHJlenpvIGRvcG8gdW5vIHNjb250byBpbiBwZXJjZW50dWFsZSwgYXJyb3RvbmRhdG8gYSBgYXJyb3RvbmRhYCBkZWNpbWFsaS4iIiIKICAgIHJldHVybiByb3VuZChwcmV6em8gKiAoMSAtIHNjb250byAvIDEwMCksIGFycm90b25kYSkKCgpub3JtYWxlID0gcHJlenpvX3Njb250YXRvKDQ5LjkwKQpwcm9tb3ppb25lID0gcHJlenpvX3Njb250YXRvKDQ5LjkwLCBzY29udG89MzApCmludGVybyA9IHByZXp6b19zY29udGF0byg0OS45MCwgc2NvbnRvPTMwLCBhcnJvdG9uZGE9MCkKCnByaW50KG5vcm1hbGUsIHByb21vemlvbmUsIGludGVybykgICMgT3V0cHV0OiA0NC45MSAzNC45MyAzNS4w'),
    'E2.3': ('Esercizio E2.3', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KAogICAgIi4uL0RhdGkvbGV0dHVyZV9wb2RfMjAyNS5jc3YiLAogICAgc2VwPSI7IiwgZGVjaW1hbD0iLCIsIGVuY29kaW5nPSJsYXRpbi0xIiwKICAgIHVzZWNvbHM9WyJwb2QiLCAiZmFzY2lhIiwgImt3aCJdLAopCmxldHR1cmUuaW5mbygpCgpyaWdoZSA9IGxlbihsZXR0dXJlKQp0b3RhbGVfa3doID0gbGV0dHVyZVsia3doIl0uc3VtKCkKCnByaW50KHJpZ2hlLCByb3VuZCh0b3RhbGVfa3doLCAxKSkgICMgT3V0cHV0OiAyMTYgMTM0NTA3Ljc='),
    'E2.4': ('Esercizio E2.4', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKY29uc3VtaSA9IHBkLnJlYWRfZXhjZWwoIi4uL0RhdGkvYm9sbGV0dGFfZXNlbXBpby54bHN4Iiwgc2hlZXRfbmFtZT0iQ29uc3VtaSIpCmxpc3Rpbm8gPSBwZC5yZWFkX2V4Y2VsKCIuLi9EYXRpL2JvbGxldHRhX2VzZW1waW8ueGxzeCIsIHNoZWV0X25hbWU9Ikxpc3Rpbm8iKQoKcmlnaGVfY29uc3VtaSA9IGxlbihjb25zdW1pKQpyaWdoZV9saXN0aW5vID0gbGVuKGxpc3Rpbm8pCnByZXp6b19mMSA9IGxpc3Rpbm9bImV1cl9rd2giXVswXQoKZm9nbGkgPSBwZC5yZWFkX2V4Y2VsKCIuLi9EYXRpL2JvbGxldHRhX2VzZW1waW8ueGxzeCIsIHNoZWV0X25hbWU9Tm9uZSkKbm9taV9mb2dsaSA9IGxpc3QoZm9nbGkua2V5cygpKQoKcHJpbnQocmlnaGVfY29uc3VtaSwgcmlnaGVfbGlzdGlubywgcHJlenpvX2YxKSAgIyBPdXRwdXQ6IDcyIDMgMC4yMQpwcmludChub21pX2ZvZ2xpKSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAjIE91dHB1dDogWydDb25zdW1pJywgJ0xpc3Rpbm8nLCAnQW5hZ3JhZmljYSdd'),
    'E2.5': ('Esercizio E2.5', 'aW1wb3J0IHNxbGl0ZTMKCmltcG9ydCBwYW5kYXMgYXMgcGQKCmNvbiA9IHNxbGl0ZTMuY29ubmVjdCgiLi4vRGF0aS91dGlsaXR5LmRiIikKbGV0dHVyZV9kYiA9IHBkLnJlYWRfc3FsKCJTRUxFQ1QgKiBGUk9NIGxldHR1cmUiLCBjb24pCmxldHR1cmVfcG9kID0gcGQucmVhZF9zcWwoIlNFTEVDVCAqIEZST00gbGV0dHVyZSBXSEVSRSBwb2QgPSAnSVQwMDFFMTAwODcxMDknIiwgY29uKQpjb24uY2xvc2UoKQoKbl9sZXR0dXJlID0gbGVuKGxldHR1cmVfZGIpCmt3aF9tYXJ6byA9IGxldHR1cmVfZGJbImt3aCJdLnN1bSgpCgpwcmludChuX2xldHR1cmUsIHJvdW5kKGt3aF9tYXJ6bywgMSksIGxlbihsZXR0dXJlX3BvZCkpICAjIE91dHB1dDogOTMwIDY5ODgwLjEgMzE='),
    'E2.6': ('Esercizio E2.6', 'c3Blc2VfbWVzaSA9IHsKICAgICJnZW5uYWlvIjogWzQ1LjAsIDEyLjMsIDgwLjUsIDIzLjldLAogICAgImZlYmJyYWlvIjogWzYwLjAsIDE1LjUsIDMzLjJdLAogICAgIm1hcnpvIjogWzIyLjQsIDk1LjAsIDQxLjEsIDE4LjcsIDkuOV0sCn0KCnRvdGFsaSA9IHt9CmZvciBtZXNlLCBsaXN0YSBpbiBzcGVzZV9tZXNpLml0ZW1zKCk6CiAgICB0b3RhbGlbbWVzZV0gPSByb3VuZChzdW0obGlzdGEpLCAyKQoKdG90YWxlX3RyaW1lc3RyZSA9IHN1bSh0b3RhbGkudmFsdWVzKCkpCgpwcmludCh0b3RhbGkpICAgICAgICAgICAgIyBPdXRwdXQ6IHsnZ2VubmFpbyc6IDE2MS43LCAnZmViYnJhaW8nOiAxMDguNywgJ21hcnpvJzogMTg3LjF9CnByaW50KHRvdGFsZV90cmltZXN0cmUpICAjIE91dHB1dDogNDU3LjU='),
    'E2.7': ('Esercizio E2.7', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL2xldHR1cmVfcG9kXzIwMjUuY3N2Iiwgc2VwPSI7IiwgZGVjaW1hbD0iLCIsIGVuY29kaW5nPSJsYXRpbi0xIikKCmYzID0gbGV0dHVyZVtsZXR0dXJlWyJmYXNjaWEiXSA9PSAiRjMiXQpmMy50b19leGNlbCgicmllcGlsb2dvX2Zhc2NpYS54bHN4IiwgaW5kZXg9RmFsc2UpCgpyaWxldHRvID0gcGQucmVhZF9leGNlbCgicmllcGlsb2dvX2Zhc2NpYS54bHN4IikKCnByaW50KGxlbihmMyksIGxlbihyaWxldHRvKSkgICMgT3V0cHV0OiA3MiA3Mg=='),
    'E2.8': ('Esercizio E2.8', 'aW1wb3J0IHBhbmRhcyBhcyBwZAppbXBvcnQgcmVxdWVzdHMKCgpkZWYgc2Vuc29yaShwcm92aW5jaWEpOgogICAgIiIiQW5hZ3JhZmljYSBkZWkgc2Vuc29yaSBtZXRlbyBkaSBSZWdpb25lIExvbWJhcmRpYSBpbiB1bmEgcHJvdmluY2lhLCBjb21lIERhdGFGcmFtZS4iIiIKICAgIHVybCA9ICJodHRwczovL3d3dy5kYXRpLmxvbWJhcmRpYS5pdC9yZXNvdXJjZS9uZjc4LW5qNmIuanNvbiIKICAgIHJlc3BvbnNlID0gcmVxdWVzdHMuZ2V0KHVybCwgcGFyYW1zPXsicHJvdmluY2lhIjogcHJvdmluY2lhfSwgdGltZW91dD0zMCkKICAgIHJlc3BvbnNlLnJhaXNlX2Zvcl9zdGF0dXMoKQogICAgcmV0dXJuIHBkLkRhdGFGcmFtZShyZXNwb25zZS5qc29uKCkpCgoKc2Vuc29yaV9taSA9IHNlbnNvcmkoIk1JIikKc2Vuc29yaV9taS5oZWFkKCkKCgojIHNlIGlsIHBvcnRhbGUgbm9uIHJpc3BvbmRlLCBuZWxsYSBzZWNvbmRhIGNlbGxhCmltcG9ydCBqc29uCgppbXBvcnQgcGFuZGFzIGFzIHBkCgp3aXRoIG9wZW4oIi4uL0RhdGkvZmFsbGJhY2svbG9tYmFyZGlhX3NlbnNvcmkuanNvbiIsIGVuY29kaW5nPSJ1dGYtOCIpIGFzIGY6CiAgICB0dXR0aSA9IHBkLkRhdGFGcmFtZShqc29uLmxvYWQoZikpCnNlbnNvcmlfbWkgPSB0dXR0aVt0dXR0aVsicHJvdmluY2lhIl0gPT0gIk1JIl0Kc2Vuc29yaV9taS5oZWFkKCk='),
    'E2.9': ('Esercizio E2.9', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL2xldHR1cmVfcG9kXzIwMjUuY3N2Iiwgc2VwPSI7IiwgZGVjaW1hbD0iLCIsIGVuY29kaW5nPSJsYXRpbi0xIikKCnRvdGFsZSA9IGxldHR1cmVbImt3aCJdLnN1bSgpCm5fcG9kID0gbGVuKHNldChsZXR0dXJlWyJwb2QiXSkpCgpmYXNjaWFfbWF4ID0gIiIKa3doX21heCA9IDAKZm9yIGZhc2NpYSBpbiBbIkYxIiwgIkYyIiwgIkYzIl06CiAgICBrd2hfZmFzY2lhID0gbGV0dHVyZVtsZXR0dXJlWyJmYXNjaWEiXSA9PSBmYXNjaWFdWyJrd2giXS5zdW0oKQogICAgaWYga3doX2Zhc2NpYSA+IGt3aF9tYXg6CiAgICAgICAgZmFzY2lhX21heCA9IGZhc2NpYQogICAgICAgIGt3aF9tYXggPSBrd2hfZmFzY2lhCgpwcmludChmIkNvbnN1bW8gdG90YWxlIDIwMjU6IHt0b3RhbGU6LjFmfSBrV2giKQpwcmludChmIlBPRCBuZWwgZmlsZToge25fcG9kfSIpCnByaW50KGYiRmFzY2lhIGNvbiBpbCBjb25zdW1vIHBpw7kgYWx0bzoge2Zhc2NpYV9tYXh9ICh7a3doX21heDouMWZ9IGtXaCkiKQ=='),
    'E3.1': ('Esercizio E3.1', 'dHVyYmluYSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL1RleGFzVHVyYmluZS5jc3YiKQoKbm9taSA9IHsKICAgICJTeXN0ZW0gcG93ZXIgZ2VuZXJhdGVkIHwgKGtXKSI6ICJwb3RlbnphX2t3IiwKICAgICJXaW5kIHNwZWVkIHwgKG0vcykiOiAidmVudG9fbXMiLAogICAgIldpbmQgZGlyZWN0aW9uIHwgKGRlZykiOiAiZGlyZXppb25lIiwKICAgICJQcmVzc3VyZSB8IChhdG0pIjogInByZXNzaW9uZSIsCiAgICAiQWlyIHRlbXBlcmF0dXJlIHwgKCdDKSI6ICJ0ZW1wZXJhdHVyYSIsCn0KdHVyYmluYSA9IHR1cmJpbmEucmVuYW1lKGNvbHVtbnM9bm9taSkKdHVyYmluYVsiZGF0YSJdID0gcGQudG9fZGF0ZXRpbWUoIjIwMjMgIiArIHR1cmJpbmFbIlRpbWUgc3RhbXAiXSwgZm9ybWF0PSIlWSAlYiAlZCwgJUk6JU0gJXAiKQp0dXJiaW5hID0gdHVyYmluYS5zZXRfaW5kZXgoImRhdGEiKS5zb3J0X2luZGV4KCkKCnByaW1vID0gdHVyYmluYS5pbmRleFswXQp1bHRpbW8gPSB0dXJiaW5hLmluZGV4Wy0xXQpwcmludChwcmltbywgdWx0aW1vKQoKb3JkaW5hdG8gPSB0dXJiaW5hLmluZGV4LmlzX21vbm90b25pY19pbmNyZWFzaW5nCnBhc3NpID0gdHVyYmluYS5pbmRleC50b19zZXJpZXMoKS5kaWZmKCkudmFsdWVfY291bnRzKCkKcHJpbnQob3JkaW5hdG8pCnBhc3Np'),
    'E3.2': ('Esercizio E3.2', 'IyBsYSB0dXJiaW5hIGNvbiBpIG5vbWkgYnJldmkgZSBsJ2luZGljZSBkaSBkYXRlLCBjb21lIG5lbGwnZXNlcmNpemlvIEUzLjEKdHVyYmluYSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL1RleGFzVHVyYmluZS5jc3YiKQp0dXJiaW5hID0gdHVyYmluYS5yZW5hbWUoY29sdW1ucz17CiAgICAiU3lzdGVtIHBvd2VyIGdlbmVyYXRlZCB8IChrVykiOiAicG90ZW56YV9rdyIsCiAgICAiV2luZCBzcGVlZCB8IChtL3MpIjogInZlbnRvX21zIiwKICAgICJXaW5kIGRpcmVjdGlvbiB8IChkZWcpIjogImRpcmV6aW9uZSIsCiAgICAiUHJlc3N1cmUgfCAoYXRtKSI6ICJwcmVzc2lvbmUiLAogICAgIkFpciB0ZW1wZXJhdHVyZSB8ICgnQykiOiAidGVtcGVyYXR1cmEiLAp9KQp0dXJiaW5hWyJkYXRhIl0gPSBwZC50b19kYXRldGltZSgiMjAyMyAiICsgdHVyYmluYVsiVGltZSBzdGFtcCJdLCBmb3JtYXQ9IiVZICViICVkLCAlSTolTSAlcCIpCnR1cmJpbmEgPSB0dXJiaW5hLnNldF9pbmRleCgiZGF0YSIpLnNvcnRfaW5kZXgoKQoKbHVnbGlvID0gdHVyYmluYS5sb2NbIjIwMjMtMDciXQpvcmVfbHVnbGlvID0gbGVuKGx1Z2xpbykKCnZlbnRvc2UgPSB0dXJiaW5hW3R1cmJpbmFbInZlbnRvX21zIl0gPiAxMl0Kbl92ZW50b3NlID0gbGVuKHZlbnRvc2UpCgpvcmVfZmVybWUgPSAodHVyYmluYVsicG90ZW56YV9rdyJdID09IDApLnN1bSgpCnByaW50KG9yZV9sdWdsaW8sIG5fdmVudG9zZSwgb3JlX2Zlcm1lKQoKdmVudG9zZV9xdWVyeSA9IHR1cmJpbmEucXVlcnkoInZlbnRvX21zID4gMTIiKQpsZW4odmVudG9zZV9xdWVyeSkgPT0gbl92ZW50b3Nl'),
    'E3.3': ('Esercizio E3.3', 'IyBsYSB0dXJiaW5hIGNvbiBpIG5vbWkgYnJldmkgZSBsJ2luZGljZSBkaSBkYXRlLCBjb21lIG5lbGwnZXNlcmNpemlvIEUzLjEKdHVyYmluYSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL1RleGFzVHVyYmluZS5jc3YiKQp0dXJiaW5hID0gdHVyYmluYS5yZW5hbWUoY29sdW1ucz17CiAgICAiU3lzdGVtIHBvd2VyIGdlbmVyYXRlZCB8IChrVykiOiAicG90ZW56YV9rdyIsCiAgICAiV2luZCBzcGVlZCB8IChtL3MpIjogInZlbnRvX21zIiwKICAgICJXaW5kIGRpcmVjdGlvbiB8IChkZWcpIjogImRpcmV6aW9uZSIsCiAgICAiUHJlc3N1cmUgfCAoYXRtKSI6ICJwcmVzc2lvbmUiLAogICAgIkFpciB0ZW1wZXJhdHVyZSB8ICgnQykiOiAidGVtcGVyYXR1cmEiLAp9KQp0dXJiaW5hWyJkYXRhIl0gPSBwZC50b19kYXRldGltZSgiMjAyMyAiICsgdHVyYmluYVsiVGltZSBzdGFtcCJdLCBmb3JtYXQ9IiVZICViICVkLCAlSTolTSAlcCIpCnR1cmJpbmEgPSB0dXJiaW5hLnNldF9pbmRleCgiZGF0YSIpLnNvcnRfaW5kZXgoKQoKbWVuc2lsZSA9IHR1cmJpbmFbInBvdGVuemFfa3ciXS5yZXNhbXBsZSgiTUUiKS5zdW0oKQptZXNlX21pZ2xpb3JlID0gbWVuc2lsZS5pZHhtYXgoKQptZXNlX3BlZ2dpb3JlID0gbWVuc2lsZS5pZHhtaW4oKQpwcmludChtZXNlX21pZ2xpb3JlLCBtZXNlX3BlZ2dpb3JlKQptZW5zaWxlCgptZW5zaWxlX3ZlbnRvID0gdHVyYmluYS5yZXNhbXBsZSgiTUUiKS5hZ2coeyJwb3RlbnphX2t3IjogInN1bSIsICJ2ZW50b19tcyI6ICJtZWFuIn0pCm1lbnNpbGVfdmVudG8='),
    'E3.4': ('Esercizio E3.4', 'IyBsYSB0dXJiaW5hIGNvbiBpIG5vbWkgYnJldmkgZSBsJ2luZGljZSBkaSBkYXRlLCBjb21lIG5lbGwnZXNlcmNpemlvIEUzLjEKdHVyYmluYSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL1RleGFzVHVyYmluZS5jc3YiKQp0dXJiaW5hID0gdHVyYmluYS5yZW5hbWUoY29sdW1ucz17CiAgICAiU3lzdGVtIHBvd2VyIGdlbmVyYXRlZCB8IChrVykiOiAicG90ZW56YV9rdyIsCiAgICAiV2luZCBzcGVlZCB8IChtL3MpIjogInZlbnRvX21zIiwKICAgICJXaW5kIGRpcmVjdGlvbiB8IChkZWcpIjogImRpcmV6aW9uZSIsCiAgICAiUHJlc3N1cmUgfCAoYXRtKSI6ICJwcmVzc2lvbmUiLAogICAgIkFpciB0ZW1wZXJhdHVyZSB8ICgnQykiOiAidGVtcGVyYXR1cmEiLAp9KQp0dXJiaW5hWyJkYXRhIl0gPSBwZC50b19kYXRldGltZSgiMjAyMyAiICsgdHVyYmluYVsiVGltZSBzdGFtcCJdLCBmb3JtYXQ9IiVZICViICVkLCAlSTolTSAlcCIpCnR1cmJpbmEgPSB0dXJiaW5hLnNldF9pbmRleCgiZGF0YSIpLnNvcnRfaW5kZXgoKQoKcHJvZmlsbyA9IHR1cmJpbmEuZ3JvdXBieSh0dXJiaW5hLmluZGV4LmhvdXIpWyJwb3RlbnphX2t3Il0ubWVhbigpCm9yYV9taWdsaW9yZSA9IHByb2ZpbG8uaWR4bWF4KCkKcHJpbnQob3JhX21pZ2xpb3JlKQpwcm9maWxvCgpwcm9maWxvX3N0YXQgPSB0dXJiaW5hLmdyb3VwYnkodHVyYmluYS5pbmRleC5ob3VyKVsicG90ZW56YV9rdyJdLmFnZyhbIm1lYW4iLCAibWF4Il0pCnByb2ZpbG9fc3RhdA=='),
    'E3.5': ('Esercizio E3.5', 'IyBsYSB0dXJiaW5hIGNvbiBpIG5vbWkgYnJldmkgZSBsJ2luZGljZSBkaSBkYXRlLCBjb21lIG5lbGwnZXNlcmNpemlvIEUzLjEKdHVyYmluYSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL1RleGFzVHVyYmluZS5jc3YiKQp0dXJiaW5hID0gdHVyYmluYS5yZW5hbWUoY29sdW1ucz17CiAgICAiU3lzdGVtIHBvd2VyIGdlbmVyYXRlZCB8IChrVykiOiAicG90ZW56YV9rdyIsCiAgICAiV2luZCBzcGVlZCB8IChtL3MpIjogInZlbnRvX21zIiwKICAgICJXaW5kIGRpcmVjdGlvbiB8IChkZWcpIjogImRpcmV6aW9uZSIsCiAgICAiUHJlc3N1cmUgfCAoYXRtKSI6ICJwcmVzc2lvbmUiLAogICAgIkFpciB0ZW1wZXJhdHVyZSB8ICgnQykiOiAidGVtcGVyYXR1cmEiLAp9KQp0dXJiaW5hWyJkYXRhIl0gPSBwZC50b19kYXRldGltZSgiMjAyMyAiICsgdHVyYmluYVsiVGltZSBzdGFtcCJdLCBmb3JtYXQ9IiVZICViICVkLCAlSTolTSAlcCIpCnR1cmJpbmEgPSB0dXJiaW5hLnNldF9pbmRleCgiZGF0YSIpLnNvcnRfaW5kZXgoKQoKbWFudXRlbnppb25pID0gcGQuRGF0YUZyYW1lKHsKICAgICJkYXRhIjogcGQudG9fZGF0ZXRpbWUoWyIyMDIzLTAzLTE1IiwgIjIwMjMtMDYtMTQiLCAiMjAyMy0xMS0wOCIsICIyMDIzLTEyLTE1Il0pLAogICAgIm1vdGl2byI6IFsiaXNwZXppb25lIGRlbGxlIHBhbGUiLCAic29zdGl0dXppb25lIGRpIHVuIHNlbnNvcmUiLCAiY29udHJvbGxvIGRlbCBnZW5lcmF0b3JlIiwgInJpcGFyYXppb25lIGRlbCBmcmVubyJdLAp9KQoKZ2lvcm5hbGllcmEgPSB0dXJiaW5hWyJwb3RlbnphX2t3Il0ucmVzYW1wbGUoIkQiKS5zdW0oKS5yZXNldF9pbmRleCgpCnVuaW9uZSA9IHBkLm1lcmdlKGdpb3JuYWxpZXJhLCBtYW51dGVuemlvbmksIG9uPSJkYXRhIiwgaG93PSJsZWZ0IikKc2VuemFfaW50ZXJ2ZW50byA9IHVuaW9uZVsibW90aXZvIl0uaXNudWxsKCkuc3VtKCkKdW5pb25lWyJtb3Rpdm8iXSA9IHVuaW9uZVsibW90aXZvIl0uZmlsbG5hKCJuZXNzdW5hIikKCnByaW50KHNlbnphX2ludGVydmVudG8pCnVuaW9uZVt1bmlvbmVbIm1vdGl2byJdICE9ICJuZXNzdW5hIl0KCnNvbG9faW50ZXJ2ZW50aSA9IHBkLm1lcmdlKGdpb3JuYWxpZXJhLCBtYW51dGVuemlvbmksIG9uPSJkYXRhIiwgaG93PSJpbm5lciIpCnByaW50KGxlbih1bmlvbmUpLCBsZW4oc29sb19pbnRlcnZlbnRpKSkKc29sb19pbnRlcnZlbnRp'),
    'E3.6': ('Esercizio E3.6', 'IyBsYSB0dXJiaW5hIGNvbiBpIG5vbWkgYnJldmkgZSBsJ2luZGljZSBkaSBkYXRlLCBjb21lIG5lbGwnZXNlcmNpemlvIEUzLjEKdHVyYmluYSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL1RleGFzVHVyYmluZS5jc3YiKQp0dXJiaW5hID0gdHVyYmluYS5yZW5hbWUoY29sdW1ucz17CiAgICAiU3lzdGVtIHBvd2VyIGdlbmVyYXRlZCB8IChrVykiOiAicG90ZW56YV9rdyIsCiAgICAiV2luZCBzcGVlZCB8IChtL3MpIjogInZlbnRvX21zIiwKICAgICJXaW5kIGRpcmVjdGlvbiB8IChkZWcpIjogImRpcmV6aW9uZSIsCiAgICAiUHJlc3N1cmUgfCAoYXRtKSI6ICJwcmVzc2lvbmUiLAogICAgIkFpciB0ZW1wZXJhdHVyZSB8ICgnQykiOiAidGVtcGVyYXR1cmEiLAp9KQp0dXJiaW5hWyJkYXRhIl0gPSBwZC50b19kYXRldGltZSgiMjAyMyAiICsgdHVyYmluYVsiVGltZSBzdGFtcCJdLCBmb3JtYXQ9IiVZICViICVkLCAlSTolTSAlcCIpCnR1cmJpbmEgPSB0dXJiaW5hLnNldF9pbmRleCgiZGF0YSIpLnNvcnRfaW5kZXgoKQoKZ2lvcm5pID0gWyJsdW5lZMOsIiwgIm1hcnRlZMOsIiwgIm1lcmNvbGVkw6wiLCAiZ2lvdmVkw6wiLCAidmVuZXJkw6wiLCAic2FiYXRvIiwgImRvbWVuaWNhIl0KCnNldHRpbWFuYWxlID0gdHVyYmluYS5ncm91cGJ5KHR1cmJpbmEuaW5kZXguZGF5b2Z3ZWVrKVsicG90ZW56YV9rdyJdLm1lYW4oKQpnaW9ybm9fbWlnbGlvcmUgPSBnaW9ybmlbc2V0dGltYW5hbGUuaWR4bWF4KCldCnByaW50KGdpb3Jub19taWdsaW9yZSk='),
    'E3.7': ('Esercizio E3.7', 'IyBsYSB0dXJiaW5hIGNvbiBpIG5vbWkgYnJldmkgZSBsJ2luZGljZSBkaSBkYXRlLCBjb21lIG5lbGwnZXNlcmNpemlvIEUzLjEKdHVyYmluYSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL1RleGFzVHVyYmluZS5jc3YiKQp0dXJiaW5hID0gdHVyYmluYS5yZW5hbWUoY29sdW1ucz17CiAgICAiU3lzdGVtIHBvd2VyIGdlbmVyYXRlZCB8IChrVykiOiAicG90ZW56YV9rdyIsCiAgICAiV2luZCBzcGVlZCB8IChtL3MpIjogInZlbnRvX21zIiwKICAgICJXaW5kIGRpcmVjdGlvbiB8IChkZWcpIjogImRpcmV6aW9uZSIsCiAgICAiUHJlc3N1cmUgfCAoYXRtKSI6ICJwcmVzc2lvbmUiLAogICAgIkFpciB0ZW1wZXJhdHVyZSB8ICgnQykiOiAidGVtcGVyYXR1cmEiLAp9KQp0dXJiaW5hWyJkYXRhIl0gPSBwZC50b19kYXRldGltZSgiMjAyMyAiICsgdHVyYmluYVsiVGltZSBzdGFtcCJdLCBmb3JtYXQ9IiVZICViICVkLCAlSTolTSAlcCIpCnR1cmJpbmEgPSB0dXJiaW5hLnNldF9pbmRleCgiZGF0YSIpLnNvcnRfaW5kZXgoKQoKbWVuc2lsZSA9IHR1cmJpbmFbInBvdGVuemFfa3ciXS5yZXNhbXBsZSgiTUUiKS5zdW0oKQoKbWVuc2lsZS50b19jc3YoImVuZXJnaWFfbWVuc2lsZS5jc3YiKQptZW5zaWxlLnRvX2V4Y2VsKCJlbmVyZ2lhX21lbnNpbGUueGxzeCIpCnJpbGV0dG8gPSBwZC5yZWFkX2NzdigiZW5lcmdpYV9tZW5zaWxlLmNzdiIsIHBhcnNlX2RhdGVzPVsiZGF0YSJdKQpzdGVzc2VfcmlnaGUgPSBsZW4ocmlsZXR0bykgPT0gbGVuKG1lbnNpbGUpCnByaW50KHN0ZXNzZV9yaWdoZSkKcmlsZXR0by5oZWFkKCk='),
    'E3.8': ('Esercizio E3.8', 'IyBsYSB0dXJiaW5hIGNvbiBpIG5vbWkgYnJldmkgZSBsJ2luZGljZSBkaSBkYXRlLCBjb21lIG5lbGwnZXNlcmNpemlvIEUzLjEKdHVyYmluYSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL1RleGFzVHVyYmluZS5jc3YiKQp0dXJiaW5hID0gdHVyYmluYS5yZW5hbWUoY29sdW1ucz17CiAgICAiU3lzdGVtIHBvd2VyIGdlbmVyYXRlZCB8IChrVykiOiAicG90ZW56YV9rdyIsCiAgICAiV2luZCBzcGVlZCB8IChtL3MpIjogInZlbnRvX21zIiwKICAgICJXaW5kIGRpcmVjdGlvbiB8IChkZWcpIjogImRpcmV6aW9uZSIsCiAgICAiUHJlc3N1cmUgfCAoYXRtKSI6ICJwcmVzc2lvbmUiLAogICAgIkFpciB0ZW1wZXJhdHVyZSB8ICgnQykiOiAidGVtcGVyYXR1cmEiLAp9KQp0dXJiaW5hWyJkYXRhIl0gPSBwZC50b19kYXRldGltZSgiMjAyMyAiICsgdHVyYmluYVsiVGltZSBzdGFtcCJdLCBmb3JtYXQ9IiVZICViICVkLCAlSTolTSAlcCIpCnR1cmJpbmEgPSB0dXJiaW5hLnNldF9pbmRleCgiZGF0YSIpLnNvcnRfaW5kZXgoKQoKbWVzaSA9IFsiZ2VubmFpbyIsICJmZWJicmFpbyIsICJtYXJ6byIsICJhcHJpbGUiLCAibWFnZ2lvIiwgImdpdWdubyIsCiAgICAgICAgImx1Z2xpbyIsICJhZ29zdG8iLCAic2V0dGVtYnJlIiwgIm90dG9icmUiLCAibm92ZW1icmUiLCAiZGljZW1icmUiXQoKZW5lcmdpYV9td2ggPSB0dXJiaW5hWyJwb3RlbnphX2t3Il0uc3VtKCkgLyAxMDAwCm1lbnNpbGUgPSB0dXJiaW5hWyJwb3RlbnphX2t3Il0ucmVzYW1wbGUoIk1FIikuc3VtKCkKbWVzZV9taWdsaW9yZSA9IG1lc2lbbWVuc2lsZS5pZHhtYXgoKS5tb250aCAtIDFdCm9yYV9taWdsaW9yZSA9IHR1cmJpbmEuZ3JvdXBieSh0dXJiaW5hLmluZGV4LmhvdXIpWyJwb3RlbnphX2t3Il0ubWVhbigpLmlkeG1heCgpCgpwcmludChmIkVuZXJnaWEgcHJvZG90dGEgbmVsIDIwMjM6IHtlbmVyZ2lhX213aDouMGZ9IE1XaCIpICAgIyBPdXRwdXQ6IEVuZXJnaWEgcHJvZG90dGEgbmVsIDIwMjM6IDg0NDkgTVdoCnByaW50KGYiTWVzZSBjb24gcGnDuSBlbmVyZ2lhOiB7bWVzZV9taWdsaW9yZX0iKSAgICAgICAgICAgICAjIE91dHB1dDogTWVzZSBjb24gcGnDuSBlbmVyZ2lhOiBhcHJpbGUKcHJpbnQoZiJPcmEgY29uIGxhIHBvdGVuemEgbWVkaWEgcGnDuSBhbHRhOiBsZSB7b3JhX21pZ2xpb3JlfSIpICAjIE91dHB1dDogT3JhIGNvbiBsYSBwb3RlbnphIG1lZGlhIHBpw7kgYWx0YTogbGUgMTY='),
    'Passo 1': ('Passo 1', 'cGFuaWZpY2lvID0geyJjbGllbnRlIjogIlBhbmlmaWNpbyBSw6giLCAicG9kIjogIklUMDAxRTMxMDQ1MjAxIiwgImt3aF9mZWJicmFpbyI6IDE2NTQuMn0KcHJlenpvID0gMC4yMQoKY2xpZW50ZSA9IHBhbmlmaWNpb1siY2xpZW50ZSJdCmt3aCA9IHBhbmlmaWNpb1sia3doX2ZlYmJyYWlvIl0KY29zdG8gPSBrd2ggKiBwcmV6em8KcHJpbnQoY2xpZW50ZSwga3doLCAia1doIGEgZmViYnJhaW8sIGNvc3RvIiwgcm91bmQoY29zdG8sIDIpLCAiZXVybyIp'),
    'Passo 2': ('Passo 2', 'bGV0dHVyZSA9IFswLjgsIDAuNywgMC45LCAxLjEsIDkuNSwgMTEuMiwgMTAuOCwgOS45LCA4LjQsIDQuMiwgMy45LCAzLjUsCiAgICAgICAgICAgMy4xLCAyLjQsIDIuMCwgMS44LCAyLjIsIDIuNiwgMi45LCAxLjUsIDEuMiwgMS4wLCAwLjksIDAuOF0KCm9yZV9mb3JubyA9IGxldHR1cmVbNDo5XQprd2hfZm9ybm8gPSBzdW0ob3JlX2Zvcm5vKQp0b3RhbGVfZ2lvcm5vID0gc3VtKGxldHR1cmUpCnF1b3RhX2Zvcm5vID0gcm91bmQoa3doX2Zvcm5vIC8gdG90YWxlX2dpb3JubyAqIDEwMCwgMSkKcGljY28gPSBtYXgobGV0dHVyZSkKcHJpbnQoZiJGb3Jubzoge2t3aF9mb3JubzouMWZ9IGtXaCBzdSB7dG90YWxlX2dpb3JubzouMWZ9LCBpbCB7cXVvdGFfZm9ybm99JSAocGljY28ge3BpY2NvfSBrV2gpIik='),
    'Passo 3': ('Passo 3', 'Y29uc3VtaV9mZWJicmFpbyA9IHsKICAgICJJVDAwMUUzMTA0NTIwMSI6IDE2NTQuMiwKICAgICJJVDAwMUUzMTA0NTg3NyI6IDgxMi42LAogICAgIklUMDAxRTMxMDQ2MzEwIjogNjkwLjEsCiAgICAiSVQwMDFFMzEwNDcwOTIiOiAzMzEwLjQsCiAgICAiSVQwMDFFMzEwNDc1NTUiOiA0MzEuOCwKICAgICJJVDAwMUUzMTA0ODEyOCI6IDQ4OTAuNywKICAgICJJVDAwMUUzMTA0ODc0MyI6IDExNzguMywKICAgICJJVDAwMUUzMTA0OTMwNiI6IDMyNzYuMCwKfQpzb2dsaWEgPSAyMDAwCgpzb3ByYV9zb2dsaWEgPSBbcG9kIGZvciBwb2QsIGt3aCBpbiBjb25zdW1pX2ZlYmJyYWlvLml0ZW1zKCkgaWYga3doID4gc29nbGlhXQp0b3RhbGVfa3doID0gc3VtKGNvbnN1bWlfZmViYnJhaW8udmFsdWVzKCkpCnByaW50KGYie2xlbihzb3ByYV9zb2dsaWEpfSBQT0Qgc29wcmEgaSB7c29nbGlhfSBrV2gsIHN1IHt0b3RhbGVfa3doOi4xZn0ga1doIHRvdGFsaSIp'),
    'Passo 4': ('Passo 4', 'ZGVmIGNvc3RvKGt3aCwgcHJlenpvPTAuMjEsIHF1b3RhX2Zpc3NhPTAuMCk6CiAgICAiIiJDb3N0byBpbiBldXJvIGRpIHVuIGNvbnN1bW8gaW4ga1doLCBwacO5IGxhIHF1b3RhIGZpc3NhLCBhcnJvdG9uZGF0byBhaSBjZW50ZXNpbWkuIiIiCiAgICByZXR1cm4gcm91bmQoa3doICogcHJlenpvICsgcXVvdGFfZmlzc2EsIDIpCgoKY29zdG9fcGFuaWZpY2lvID0gY29zdG8oMTY1NC4yKQpjb3N0b19zZXJyYSA9IGNvc3RvKDMyNzYuMCwgcHJlenpvPTAuMTcpCmNvc3RvX2JhciA9IGNvc3RvKDY5MC4xLCBxdW90YV9maXNzYT04KQpwcmludChmIlBhbmlmaWNpbzoge2Nvc3RvX3BhbmlmaWNpb30gZXVybywgU2VycmE6IHtjb3N0b19zZXJyYX0gZXVybywgQmFyOiB7Y29zdG9fYmFyfSBldXJvIik='),
    'Passo 5': ('Passo 5', 'aW1wb3J0IHBhbmRhcyBhcyBwZAoKbGV0dHVyZSA9IHBkLnJlYWRfY3N2KCIuLi9EYXRpL2hvbWV3b3JrL2xldHR1cmVfbWFyem8uY3N2Iiwgc2VwPSI7IiwgZGVjaW1hbD0iLCIpCmxldHR1cmUuaW5mbygpCnByaW50KGxldHR1cmUuaGVhZCgpKQpwcmludChsZXR0dXJlLmRlc2NyaWJlKCkpCgptYXNrID0gbGV0dHVyZVsia3doIl0gPiA1MDAKYW5vbWFsZSA9IGxldHR1cmVbbWFza10KYW5vbWFsZS50b19jc3YoImxldHR1cmVfYW5vbWFsZS5jc3YiLCBpbmRleD1GYWxzZSkKYW5vbWFsZQ=='),
    'Passo 6': ('Passo 6', 'aW1wb3J0IHBhbmRhcyBhcyBwZAppbXBvcnQgc3FsaXRlMwoKCmRlZiBsZWdnaV90YWJlbGxhKG5vbWUpOgogICAgIiIiTGVnZ2UgdHV0dGEgbGEgdGFiZWxsYSBgbm9tZWAgZGEgYW5hZ3JhZmljYS5kYiBlIGxhIHJlc3RpdHVpc2NlIGNvbWUgRGF0YUZyYW1lLiIiIgogICAgY29uID0gc3FsaXRlMy5jb25uZWN0KCIuLi9EYXRpL2hvbWV3b3JrL2FuYWdyYWZpY2EuZGIiKQogICAgZGYgPSBwZC5yZWFkX3NxbChmIlNFTEVDVCAqIEZST00ge25vbWV9IiwgY29uKQogICAgY29uLmNsb3NlKCkKICAgIHJldHVybiBkZgoKCmFuYWdyYWZpY2EgPSBwZC5yZWFkX2V4Y2VsKCIuLi9EYXRpL2hvbWV3b3JrL2NsaWVudGkueGxzeCIsIHNoZWV0X25hbWU9IkFuYWdyYWZpY2EiKQpsaXN0aW5vID0gcGQucmVhZF9leGNlbCgiLi4vRGF0aS9ob21ld29yay9jbGllbnRpLnhsc3giLCBzaGVldF9uYW1lPSJMaXN0aW5vIikKcG90ZW56ZSA9IGxlZ2dpX3RhYmVsbGEoInBvZCIpCm9mZmljaW5hID0gcG90ZW56ZVtwb3RlbnplWyJjbGllbnRlIl0gPT0gIk9mZmljaW5hIE1lY2NhbmljYSBGdW1hZ2FsbGkiXQoKcHJpbnQoYW5hZ3JhZmljYSkKcHJpbnQobGlzdGlubykKb2ZmaWNpbmE='),
}
