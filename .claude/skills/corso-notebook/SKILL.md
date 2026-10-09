---
name: corso-notebook
description: Scrivere, modificare, spostare o rileggere il materiale del corso Python in questo repository (notebook in Aula_*/Soluzioni_*/Extra, Esercitazioni, Homework, Approfondimenti, Schede, README, Guida docente). Usare questa skill ogni volta che si tocca un notebook o un testo del corso, anche per una sola cella, un esercizio, una verifica, un titolo o una frase, e anche quando la richiesta parla solo di "stile", "tono", "esercizio", "notebook", "aula", "soluzioni" o "sorgente". Il materiale è generato da _build/src e ha uno stile di prosa preciso che va rispettato e controllato con il build.
---

# Lavorare sul materiale del corso

I notebook di questo corso non si modificano a mano: ogni file in `Aula_Base/`, `Aula_Avanzata/`, `Soluzioni_*/` ed
`Extra/` è generato da uno script Python in `_build/src/`, che produce dallo stesso sorgente la versione studente e
quella con le soluzioni per le due aule. Chi tocca il materiale lavora quindi sul sorgente, ricostruisce e rilegge
il risultato. Lo stile della prosa è il punto a cui il docente tiene di più: un tono da manuale tecnico, con frasi
complete e nessuna frase ad effetto, e vale per tutto il testo del repository, dalle celle dei notebook al README.

## 1. Prima di scrivere

Leggere per intero `_build/docs/STILE.md`: contiene la diagnosi di quello che suonava artificiale, le regole e sei
esempi prima e dopo. È il documento che decide se una frase va bene. Se la modifica riguarda la struttura di un
notebook (sezioni, esercizi, aule, tempi, dominio degli esempi) leggere anche `_build/docs/REGOLE.md`; se riguarda una
scelta didattica o un dubbio su cosa voleva il docente, `_build/docs/REQUISITI.md`. Il modello di riferimento per la
voce è il testo originale del docente, visibile nel branch `main`.

Le cose che il docente non vuole più vedere: celle etichetta come "Esempio:" o "Unione:", sequenze di frasi
telegrafiche, catene di due punti al posto di una frase, antitesi e chiusure brillanti, domande retoriche, aperture con
"Qui" o "Ora", elenchi con il grassetto in testa al posto della spiegazione, un "Output atteso:" secco. Al loro posto
va un paragrafo di due a cinque frasi che dice che cosa fa lo strumento, a cosa serve e che cosa mostra la cella sotto.

## 2. Trovare il sorgente

| Notebook generato | Sorgente | Numero per il build |
|---|---|---|
| `00_Notebook` … `11_Capstone` | `_build/src/nbNN_*.py` | `00` … `11` |
| `Esercitazione_1/2/3` | `_build/src/nbE1_…py` ecc. | `E1`, `E2`, `E3` |
| `Homework` | `_build/src/nbC_homework.py` | `C` |
| `Approfondimenti_1/2` | `_build/src/nbA1_…py`, `nbA2_…py` | `A1`, `A2` |
| `Extra/*.ipynb` | `_build/src/extra/*.py` | `EXTRA` |

Il docstring in testa a `_build/nbkit.py` descrive l'API del sorgente: `nb.sezione`, `nb.sottosezione`, `nb.md`,
`nb.code`, `nb.box`, `nb.prova_tu`, `nb.esercizio`, il blocco `with nb.solo("avanzata"):` per le parti della sola
aula Avanzata e `aula="base"` per quelle della sola Base. La `verifica=` di un esercizio non compare nel notebook:
il build la raccoglie nel modulo `corso.py` di ogni cartella e nel notebook resta la chiamata `verifica("7.1")`.

## 3. Scrivere o modificare

Lavorare nel sorgente e lasciare il codice com'è quando la richiesta riguarda il testo; quando riguarda il codice,
controllare che gli `# Output:` nei commenti restino veri. Un esercizio nuovo ha sempre titolo, scenario in una o
due frasi, consegna con passi che sono frasi complete, `starter` con i `...`, `soluzione`, una `verifica=` con uno a
tre `assert` e messaggi brevi che dicono che cosa controllare (senza `print` finale: la riga ✅ la aggiunge il
toolkit), e se serve un `suggerimento` e un `perche`. Un concetto usato nella consegna deve essere già stato
spiegato nei notebook precedenti o in quello stesso, altrimenti va introdotto nel suggerimento con un esempio. Gli
esercizi per notebook sono due o tre, più uno facoltativo al massimo; i Prova tu al massimo due. Il materiale che
non sta nel percorso principale va in `Approfondimenti_1` o `_2`, non in sezioni facoltative dentro i notebook.

Gli esempi dei notebook di sintassi (00-05) stanno in scenari comuni, come spesa, viaggi, voti o meteo; i dati
del settore energetico compaiono da pandas in poi, con i dataset veri o quelli inventati già presenti in `Dati/`.
Il gergo tecnico resta in inglese dove si usa in inglese (notebook, kernel, DataFrame, slicing, encoding).

Se cambiano i tempi di un notebook, aggiornare anche la tabella in `README.md` e quelle in `Guida_docente.md`.

## 4. Ricostruire e controllare

    uv run python _build/controlla.py 07 E2      # build + soluzioni eseguite + Run All studente, solo quei notebook
    uv run python _build/controlla.py            # tutto il corso

Il comando deve chiudersi con `build: OK` e con tutti i notebook OK. Il build segnala le celle fuori stile: una
cella etichetta è un errore, le frasi telegrafiche e l'"Output atteso:" secco sono avvisi, e si risolvono
riscrivendo il testo. Le celle che chiamano un'API hanno il tag `rete` e durante la validazione vengono saltate,
quindi vanno lette con attenzione a mano.

## 5. Rileggere

    uv run python _build/leggi.py Aula_Base/07_Pandas_operazioni.ipynb

Il comando stampa il notebook generato cella per cella, come lo vede un corsista. Leggerlo dall'inizio alla fine
una volta, con la domanda "questa cella spiega qualcosa o è un appunto?", sistemare quello che non regge e
ricostruire. Per le parti Avanzata rileggere anche `Aula_Avanzata/`. È il passaggio che distingue un testo che
passa il lint da un testo che si legge bene, e non si salta.

## 6. Riferire

Dire che cosa è cambiato e dove, con due o tre esempi prima e dopo quando si è riscritto del testo, e segnalare le
frasi su cui si è incerti, in particolare le affermazioni tecniche aggiunte che non erano nel testo di partenza.
Non fare commit se non è richiesto. Nessun identificativo di modelli di AI nei file del repository.
