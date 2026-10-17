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
from pathlib import Path
assert Path("carico_gennaio.html").exists(), "❌ Il file carico_gennaio.html non c'è: controlla il nome in write_html"
assert Path("carico_gennaio.html").stat().st_size < 1_000_000, "❌ Il file è troppo grande: manca include_plotlyjs=\"cdn\""
'''),
    'A2.2': ('Esercizio A2.2', r'''
assert round(media_24h.max()) == 27189, "❌ media_24h: rolling su 96 quarti d'ora, poi mean()"
assert picco_24h == pd.Timestamp("2024-07-19 15:30"), "❌ picco_24h: usa media_24h.idxmax()"
'''),
    'E1.1': ('Esercizio E1.1', r'''
assert fattore == 2.0 and tipo_fattore is float, "❌ fattore è invitati / persone_ricetta e tipo_fattore è type(fattore)"
assert pasta_g == 640.0, "❌ pasta_g: 320 moltiplicato per fattore"
assert annuncio == "Siamo in 8, servono 640.0 g di spaghetti", "❌ annuncio: unisci i pezzi con + convertendo i numeri con str()"
'''),
    'E1.2': ('Esercizio E1.2', r'''
assert piatto_titolo == "Spaghetti alla carbonara" and lunghezza == 115, "❌ Controlla piatto_titolo (piatto.capitalize()) e lunghezza (len(messaggio))"
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
assert totali == {"gennaio": 161.7, "febbraio": 108.7, "marzo": 187.1}, "❌ totali: una chiave per mese, con la somma delle spese di quel mese"
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
assert set(listino["fascia"]) == {"F1", "F2", "F3"}, "❌ listino: è il foglio Listino? Controlla sheet_name"
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
}
