# Regole del materiale 2026 (struttura, volume, dominio)

Si legge insieme a REQUISITI.md (le richieste del docente), a PIANO_OTTOBRE_2026.md (le decisioni per l'edizione di
ottobre, che prevale dove questo documento è diverso) e al docstring di `_build/nbkit.py` (formato e API del toolkit).

## Voce (sostituita da STILE.md, ottobre 2026: leggere quello)
- Prosa da libro tecnico o blog tecnico che spiega come si fa una cosa: paragrafi di 2-5 frasi complete e legate,
  che dicono che cosa fa lo strumento, a cosa serve e cosa mostra la cella sotto. Curata, fluida, senza nessuna frase
  ad effetto: niente antitesi, slogan, metafore, domande retoriche, triadi, "davvero", "che contano".
- Il modello è la prosa del docente nei notebook originali. Niente celle etichetta ("Esempio:"), niente catene di due
  punti, niente frasi telegrafiche in sequenza, niente elenchi con grassetto in testa al posto della spiegazione.
- Il testo parla al corsista, mai del corso visto da chi lo organizza: niente "il docente", "l'aula", "la
  correzione" nei notebook; le note per il docente stanno nella Guida (vedi STILE.md, "A chi parla il testo").
- Titoli descrittivi e piatti. Commenti di codice brevi; `# Output: ...` ammesso. "Noi" quando lavoriamo, impersonale
  per le regole, "tu" nelle consegne. Italiano con il gergo in inglese dove si usa in inglese.

## Volume
- Una cella di testo: un paragrafo di 2-5 frasi (40-90 parole), uno per cella di codice che introduce. Due celle di
  testo adiacenti sullo stesso codice si fondono. Niente box Ricorda. Box ammessi con parsimonia: Attenzione (rosso,
  raro), Esercizio/Hands-on (verde), Soluzione (azzurro); Nota e Approfondimento sono citazioni.
- Hands-on inline: da due a tre per notebook, solo dove servono e sono rilevanti, con verifica; cinque è il massimo.
  Sezione Extra in fondo: 2-3 esercizi brevi, uno può essere facoltativo; ogni esercizio ha una `verifica=` con 1-3
  assert (nel notebook: `verifica("7.1")`). Il notebook di spiegazione `Ambiente_script_e_Ruff` e il capstone, che
  procede a passi guidati, non hanno né Hands-on né Extra (il motivo è in HANDS_ON.md).
- Un esercizio per concetto nel corso: le f-string hanno un solo esercizio (01).

## Dove stanno gli esercizi e a cosa servono (decisioni di ottobre 2026)

Il corso ha quattro posti per il codice scritto dal corsista, e ciascuno ha una funzione diversa. Un esercizio scritto
nel posto sbagliato è sbagliato anche se è buono.

- **Hands-on dentro il notebook.** Sono il primo contatto con un concetto appena mostrato: piccoli, inline, subito dopo
  l'esempio che riprendono, e consistono nel cambiare qualcosa nel codice appena visto o nel ripetere lo stesso gesto su
  un dato diverso (un altro indice, un'altra chiave, un altro parametro), con una verifica. Non sono un compito
  completo e non introducono niente di nuovo: servono a mettere le mani sul codice e a fissare la memoria dei concetti
  che torneranno nei notebook seguenti e nel leggere codice scritto da un'AI. Se ne mettono da due a tre per
  notebook, soltanto dove il gesto è sensato e riguarda un concetto rilevante, ciascuno da uno a tre minuti; cinque è
  il massimo e non un obiettivo. I notebook scritti prima di questa regola, che ne hanno fino a cinque, non si
  riducono per questo: la regola vale per i notebook nuovi e per quelli che si rivedono. Possono chiudersi con una
  riga facoltativa "prova anche", sempre banale. Il nome è Hands-on; "Prova tu" non si usa più.
- **Extra in fondo al notebook.** Una sezione finale, che in aula si salta e che chi vuole fa a casa, con due o tre
  esercizi brevi che ripassano i punti principali del notebook. Il materiale del vecchio Homework, dove è fatto bene, si
  riusa qui. Non si contano nei tempi del notebook.
- **Esercitazioni di fine modulo.** L'ora strutturata (45 minuti di lavoro, 15 di correzione) in cui si fa un compito
  intero: cinque o sei esercizi del nucleo, varianti Base e Avanzata, suggerimenti nascosti, soluzione per esercizio,
  domande di riepilogo in apertura. Il nucleo è fatto dagli esercizi scritti dal docente nel branch `main`, adattati al
  formato: la 1 usa i cinque esercizi dei notebook 01 e 02 originali (massimo, minimo e differenza; area del cerchio;
  lista invertita; posizioni pari; capitali del G8) e, oltre a questi, ha soltanto la sfida finale facoltativa; la 2
  usa i tre esercizi sulle funzioni del notebook 03 originale più esercizi di import (CSV, Excel, SQL, API per
  l'Avanzata) scritti nello stesso stile; la 3 ha sei esercizi, quattro sul dataset degli ascolti del notebook 04
  originale e due sulle serie temporali del notebook 06 originale. Gli esercizi che il docente aveva messo dentro i
  notebook e che ora stanno nelle esercitazioni vanno sostituiti nei notebook da Hands-on nuovi. Nell'aula Avanzata
  l'Esercitazione 1 è invece l'esercizio sullo script: i corsisti rifanno nella cartella `esercizio/` la dimostrazione
  del notebook `Ambiente_script_e_Ruff`, guidati passo per passo, e qui sono ammessi alcuni passi facoltativi
  elementari (un `print` in punti diversi, il valore di `__name__`, l'ambiente ricostruito con `uv sync`). I cinque
  esercizi classici restano in fondo allo stesso notebook, facoltativi, da fare a casa.
- **Homework e riserva.** L'Homework non è più un'attività prevista: resta un notebook di riserva in `Riserva/`, fuori
  dalle cartelle `Aula_*`, da usare solo se una classe è molto più veloce del previsto. Nella stessa cartella, in
  `Riserva/Avanzata/`, sta il notebook di riserva con esercizi in più su uv, script e Ruff (sorgente `nbR_*`). Quando
  serve, la riserva di un'aula si consegna con uno zip a parte (vedi "Come si mantiene").
- **Capstone.** La giornata 4: passi guidati su un caso reale, con livelli diversi per le due aule e il supporto di
  Copilot. Lì il corsista costruisce un'analisi intera e i passi sono più lunghi.

Le regole di questo documento sulla difficoltà (tutta in Python), sull'apertura con il risultato e sulle richieste
motivate valgono in tutti e quattro i posti; cambiano la lunghezza e lo scopo.

## Esercizi: la difficoltà sta in Python
- Un esercizio allena quello che si è appena visto, uno a uno con la teoria, a livello basilare. La difficoltà è tutta
  in Python: nessun calcolo da impostare, nessuna nozione di matematica oltre le quattro operazioni, nessuna
  conversione di unità, nessun ragionamento articolato sullo scenario. Se il corsista deve pensare al problema prima
  che al codice, l'esercizio è sbagliato.
- I numeri e le operazioni entrano di passaggio dentro esercizi sulle strutture dati, sulle stringhe o sui dati:
  una somma, una divisione, un arrotondamento, non un conto da impostare.
- Ogni esercizio, pur semplice, è pensato per toccare più punti della teoria (per esempio un dizionario, un suo
  metodo e una funzione di Python), in modo che rifare l'esercizio significhi ripassare la lezione.

## Esercizi: prima il risultato, poi i passi
- Un esercizio si apre con un paragrafo che dice che cosa vogliamo ottenere e perché conviene farlo in Python, nei
  termini dello scenario: il messaggio che si rigenera quando cambia il numero degli invitati, la lista che si sistema
  senza riscriverla, il file che un collega apre in Excel. Chi legge deve capire che cosa sta costruendo, e trovarlo
  sensato anche in un caso gioco, prima di leggere qualunque passo; da quel paragrafo deve poter arrivare al risultato
  da solo. Quando il risultato è breve, il paragrafo lo dice (il testo del messaggio, il valore del totale).
- I passi numerati sono un aiuto facoltativo: stanno nel blocco "Passo per passo", che si apre con un clic, e dopo di
  loro vengono i suggerimenti e la soluzione a richiesta. L'ordine di lettura è obiettivo, passi, suggerimenti,
  soluzione, e ogni livello aggiunge dettagli senza ripetere il precedente.
- Ogni richiesta ha un motivo nello scenario. Non si chiede un `int()`, un `len()` o un `type()` perché "fa
  esercizio": se non c'è una ragione che il corsista riconosce (un SMS ha 160 caratteri, il negozio vende confezioni
  intere), la richiesta si toglie o si cambia.
- Il modello per la narrativa e il tono sono gli esercizi scritti dal docente nel branch `main`, per esempio quelli dei
  notebook 02-04: un obiettivo detto in una frase, uno scenario credibile, niente di superfluo. Se ne prende lo
  spirito, non la forma.

## Dominio
- Esempi e esercizi semplici in scenari comuni (spesa, viaggi, voti, ricette, sport, meteo, biblioteca, negozio, musica).
  Tutto il modulo 1 resta in questi scenari, compresi l'Esercitazione 1 e gli script della dimostrazione (la spesa)
  e dell'esercizio (il meteo).
- Energia/utility solo con dati veri (Terna, TexasTurbine, U.S. Electricity Prices, Open-Meteo, sensori Lombardia) e nei
  dataset inventati già esistenti usati da pandas in poi (letture POD, impianti FV, bolletta, utility.db, prezzi zonali,
  Homework). Negli esercizi di sintassi (00-05) niente POD, kWh, bollette, fasce.

## Struttura
- Testata piana (ottobre 2026): H1, una riga con tempo e dati, "In questo notebook impariamo a" con 3 obiettivi. Niente box,
  niente intento. Indice solo se il notebook ha almeno 50 celle. Sezioni numerate. Ultima sezione "Extra" nei notebook
  del percorso, tranne il capstone, che finisce con le richieste libere a Copilot, e `Ambiente_script_e_Ruff`, che
  finisce con i comandi in breve; "Esercizi" negli Approfondimenti e nelle Esercitazioni. Chiusura con link
  precedente/prossimo e, in piccolo, modulo · aula.
- Colore solo per Esercizio/Hands-on (verde), Soluzione (azzurro), Attenzione (rosso, raro: tre box nei notebook dei
  corsisti, cioè nel 02, nel 07 della sola Avanzata e in Approfondimenti_2, più uno nella dimostrazione
  `Extra/VS_Code_e_notebook`). Nota e Approfondimento sono citazioni (`>`). Un notebook che ha una Scheda la cita in
  fondo con "Riassunto in una pagina: [...]"; le schede sono tre (leggere il codice, gli errori più comuni, da Excel a
  pandas).
- Dimostrazioni del docente (VS Code e i notebook, Data Wrangler, wrapper delle API): niente nel notebook del percorso.
  Il materiale sta in `Extra/`, fuori dalle cartelle delle aule, e la scaletta nella `Guida_docente.md`. Ambiente
  virtuale, uv, script e Ruff non sono più una dimostrazione tenuta fuori dai notebook: nell'Avanzata sono il notebook
  di spiegazione `Ambiente_script_e_Ruff` del modulo 1, seguito dalla dimostrazione dal vivo nella cartella `demo/` e
  dall'Esercitazione 1, che la fa rifare nella cartella `esercizio/` (PIANO_OTTOBRE_2026.md); nella Base se ne parla
  solo durante la dimostrazione di VS Code.
- Due aule dallo stesso sorgente: Avanzata aggiunge le parti (A); Base non vede buchi.
- Il materiale deve reggere da solo dopo il corso: quello che si rilegge a settembre è scritto, in breve.

## La cartella dell'aula (18 ottobre 2026)

Il corsista riceve soltanto la cartella della sua aula, `Aula_Base` o `Aula_Avanzata`, che deve funzionare da sola,
perché contiene i dati, le schede, il README e i file del progetto uv (`pyproject.toml`, `uv.lock` e
`.python-version`). Al primo livello stanno le cartelle `Modulo_1` … `Modulo_4`, e i percorsi verso i dati e le schede
partono dalla radice dell'aula. In pratica il corsista estrae lo zip della sua aula, apre la cartella in VS Code,
lancia `uv sync` e da lì raggiunge ogni notebook, ogni file di dati e ogni scheda senza altri file del repository. La
cartella dell'Avanzata, che è la più completa, contiene questo:

    Aula_Avanzata/
        README.md                                  le istruzioni per il corsista
        pyproject.toml  uv.lock  .python-version   il progetto uv "corso-python", uguale per le due aule
        .vscode/                                   impostazioni ed estensioni consigliate
        Dati/  Schede/                             i dati usati dai notebook e le tre schede
        Modulo_1/ … Modulo_4/                      i notebook del percorso, con il loro corso.py
            Modulo_1/Script_uv_Ruff/               solo Avanzata: Ambiente_script_e_Ruff, demo/ ed esercizio/
        Soluzioni/                                 la copia con le soluzioni di ogni notebook, con il suo corso.py
            Soluzioni/Script_uv_Ruff/              solo Avanzata: demo/ ed esercizio/ come sono alla fine

I notebook stanno nei moduli in questo modo, con la numerazione 00-11 che resta unica per tutto il corso:

| Cartella | Aula Base | Aula Avanzata |
|---|---|---|
| `Modulo_1` | 00, 01, 02, 03, Esercitazione_1 | gli stessi, più `Script_uv_Ruff/` |
| `Modulo_2` | 04, 05, 06, Esercitazione_2, Approfondimenti_1 | gli stessi |
| `Modulo_3` | 07, 08, Esercitazione_3, Approfondimenti_2 (solo le date) | 07, 08, Esercitazione_3 |
| `Modulo_4` | 09, 10, 11 | 09, 10, 11, Approfondimenti_2 |

Le soluzioni sono a disposizione dei corsisti dal primo giorno, in `Soluzioni/`: una cartella sola, senza
sottocartelle per modulo, separata dai moduli, così il corsista apre una soluzione solo quando la cerca. Un notebook
senza esercizi, come `Ambiente_script_e_Ruff`, non ha una copia lì; al suo posto `Soluzioni/Script_uv_Ruff/` contiene
lo stato finale della dimostrazione e dell'esercizio. Il materiale per il docente resta alla radice del repository,
fuori dalle cartelle delle aule: `Extra/` con le dimostrazioni e `Riserva/` con l'Homework e il notebook di riserva su
uv, script e Ruff, che quando serve si consegna con uno zip a parte.

### I percorsi

Un percorso verso `Dati/` o `Schede/` si scrive relativo alla cartella del notebook e sale fino alla radice dell'aula:
`../Dati/` da `Modulo_N/` e da `Soluzioni/`, `../../Dati/` da `Modulo_1/Script_uv_Ruff/`. Il banner calcola il
prefisso da solo (`Notebook.radice`), e il lint segnala come errore un percorso scritto `"Dati/...` senza prefisso. I
link precedente/prossimo si calcolano dalla posizione, quindi un notebook di `Soluzioni/` porta alla copia con le
soluzioni del notebook seguente, quando esiste, e un notebook del modulo alla versione studente. Quando un notebook
legge file che gli stanno accanto, il percorso deve valere sia dal modulo sia dalle soluzioni: l'Esercitazione 1
dell'Avanzata legge `Script_uv_Ruff/esercizio/`, che da `Modulo_1/` porta allo stato di partenza e da `Soluzioni/` allo
stato finale. Nessun percorso di un notebook delle aule esce dalla cartella dell'aula.

### Dove va un notebook

La posizione di un notebook del percorso la decide la sua voce in `nbkit.PROGRAMMA`, `Voce(num, file, titolo, modulo,
aule, cartella, soluzioni)`. Il campo `modulo` è il numero di `Modulo_N`, `aule` dice quali aule lo ricevono,
`cartella` è una sottocartella dentro il modulo (per `Ambiente_script_e_Ruff` è `Script_uv_Ruff`) e `soluzioni=False`
indica un notebook senza esercizi, che non ha copia in `Soluzioni/`. L'ordine delle voci è l'ordine dei link
precedente/prossimo. Il `blocco` del `Notebook` nel sorgente deve coincidere con il modulo della voce, altrimenti il
build si ferma con un errore. Gli Approfondimenti non sono nel programma e stanno nel modulo indicato da `blocco`, che
può essere un dizionario per aula: `Approfondimenti_1` è in `Modulo_2` per le due aule, `Approfondimenti_2` è in
`Modulo_3` nella Base, dove contiene solo le date, e in `Modulo_4` nell'Avanzata, dove contiene anche il codice degli
agenti. Il materiale di riserva ha `riserva=True` e va in `Riserva/<Aula>/`, con la copia con le soluzioni accanto
(`..._Soluzioni.ipynb`); le dimostrazioni del docente, in `_build/src/extra/`, vanno in `Extra/`.

I sorgenti si chiamano `nbNN_*` per i notebook del percorso, `nbE1_*` … `nbE3_*` per le esercitazioni, `nbA1_*` e
`nbA2_*` per gli Approfondimenti, `nbS_*` per il notebook su ambiente, script e Ruff, `nbC_*` per l'Homework e `nbR_*`
per il notebook di riserva. La parte del nome tra `nb` e il primo `_` è il numero da passare a `build.py` e a
`controlla.py` (`07`, `E1`, `A2`, `S`, `C`, `R`).

### Come si mantiene

Dentro `Aula_*/` non si modifica nulla a mano: i notebook e i `corso.py` sono generati, e il resto è una copia che
`_build/statici.py` rifà a ogni build. Gli originali stanno in quattro posti.

- I sorgenti dei notebook, in `_build/src/`. Il build scrive la versione studente in `Aula_*/Modulo_N/` e quella con
  le soluzioni in `Aula_*/Soluzioni/`, con un `corso.py` in ogni cartella che contiene esercizi.
- `Dati/` e `Schede/`, alla radice del repository. In ogni aula vanno solo i file di `Dati/` che i notebook usano:
  `DATI_ESCLUSI` in `statici.py` elenca quelli che restano fuori e `DATI_SOLO_AVANZATA` quelli che vanno solo
  all'Avanzata (i fallback dei sensori della Lombardia). Quando un notebook comincia a usare un file nuovo, o smette di
  usarne uno, si aggiornano questi due elenchi. Il `Dati/README.md` dell'aula è ricavato da quello della radice, senza
  i file che l'aula non riceve e senza i comandi per rigenerare i dati.
- I file del progetto dei corsisti, in `_build/aula/`: `pyproject.toml` (progetto `corso-python`, uguale per le due
  aule, con il solo Ruff nel gruppo `dev`), `uv.lock`, `.python-version`, `README_base.md` e `README_avanzata.md`, che
  diventano il `README.md` dell'aula, e `vscode/<aula>/`, che diventa `.vscode/`. Quando cambiano le dipendenze si
  modifica `_build/aula/pyproject.toml` e si rigenera il lock con `uv lock` dentro `_build/aula`. Questo progetto è
  distinto da quello della radice del repository, che serve a costruire e validare il materiale.
- Le cartelle della dimostrazione e dell'esercizio su uv e Ruff, in `_build/src/script_uv_ruff/`: `demo/` ed
  `esercizio/` diventano lo stato di partenza in `Aula_Avanzata/Modulo_1/Script_uv_Ruff/`, mentre `soluzioni/demo/` e
  `soluzioni/esercizio/` diventano lo stato finale in `Aula_Avanzata/Soluzioni/Script_uv_Ruff/`. Lo stato di partenza
  contiene soltanto i due script: il progetto nasce in aula con `uv init --bare`, che crea un progetto a sé perché il
  `pyproject.toml` dei corsisti esclude `Modulo_1/Script_uv_Ruff/*` nella sezione `[tool.uv.workspace]`. Il nuovo
  `pyproject.toml` non ha una sezione `[tool.ruff]`, quindi Ruff usa quella del corso, la cui voce `src` gli fa
  riconoscere `calcoli.py` e `meteo.py` come file del progetto. `controlla.py` verifica che lo stato di partenza non
  contenga file di un progetto uv.

`controlla.py`, a ogni giro e qualunque notebook si indichi, controlla anche le cartelle delle aule: che le copie di
dati e file del progetto coincidano con gli originali, che `_build/aula/uv.lock` sia aggiornato (`uv lock --check`) e
che Ruff dia sugli script della dimostrazione e dell'esercizio esattamente le quattro segnalazioni previste all'inizio
(`F401` e `F841` nel file delle funzioni, `I001` ed `E501` in `main.py`) e nessuna alla fine, dove anche `ruff format`
non deve cambiare nulla. Chi cambia il codice della dimostrazione o dell'esercizio aggiorna insieme `AVVISI_INIZIALI`
in `controlla.py` e i testi che citano quei messaggi: il notebook `Ambiente_script_e_Ruff`, l'Esercitazione 1
dell'Avanzata e la Guida.
Un build completo, senza numeri, toglie infine dalle cartelle delle aule i notebook e i `corso.py` che nessun sorgente
produce più, così un notebook rinominato o spostato non lascia copie vecchie.

Le impostazioni di VS Code della cartella fanno partire Jupyter dalla cartella del notebook
(`jupyter.notebookFileRoot`), nascondono le cache (`__pycache__`, e nell'Avanzata anche `.ruff_cache`), aggiungono l'a
capo in fondo a ogni file salvato (`files.insertFinalNewline`), così Ruff non segnala `W292` sui file scritti a mano, e
non attivano l'ambiente del corso nel terminale (`python.terminal.activateEnvironment: false`). Con l'ambiente del
corso attivo, infatti, uv lanciato in `demo/` o in `esercizio/` stampa l'avviso `VIRTUAL_ENV=... does not match the
project environment path .venv and will be ignored`. Nell'Avanzata Ruff è anche il formatter predefinito dei file
Python, senza formattazione al salvataggio, e la sua estensione è tra quelle consigliate. Sempre nell'Avanzata **Run
Python File** lancia lo script dalla sua cartella (`python.terminal.executeInFileDir`), ma con l'interprete del corso,
che ha già pandas, e per questo nella parte su uv e Ruff gli script si lanciano soltanto con `uv run`. In entrambe le
aule le estensioni Pylint e Flake8, se qualcuno le ha installate, restano spente nella cartella (`pylint.enabled` e
`flake8.enabled` a `false`, e tra le estensioni sconsigliate in `extensions.json`): il linter del corso è Ruff, e un
secondo linter con regole sue mostrerebbe segnalazioni diverse da quelle di `uv run ruff check`.

Il `pyproject.toml` del corso esclude da Ruff i notebook e i `corso.py` (`extend-exclude = ["corso.py", "*.ipynb"]`),
quindi né il terminale né l'estensione di VS Code li modificano. Ruff si lancia comunque soltanto da un terminale aperto
in `demo/` o in `esercizio/`: lanciato dalla cartella del corso, sistemerebbe anche gli script di partenza di quelle
cartelle e delle loro copie finali in `Soluzioni/`, e la dimostrazione e l'esercitazione non mostrerebbero più le
quattro segnalazioni. Nella dimostrazione i comandi seguono sempre lo stesso ordine (`ruff format`, `ruff check`,
`ruff check --fix`, le correzioni a mano, di nuovo `ruff format` e `ruff check`), che mostra separatamente il lavoro
del formatter e quello del linter; con le regole scelte `ruff check` dà le stesse quattro segnalazioni prima e dopo
`ruff format`.

Una prova della dimostrazione o dell'esercizio fatta nel repository lascia nelle cartelle `demo/` ed `esercizio/` di
`Aula_Avanzata` il `.venv`, `uv.lock`, le cache e il file Excel. Il build rimette le cartelle esattamente come gli
originali e toglie tutto il resto, `.venv` compreso, quindi dopo una prova basta un build per ripartire dall'inizio.
Il corsista che vuole rifare la dimostrazione o l'esercizio da capo cancella invece la cartella e la estrae di nuovo
dallo zip del corso: estratta sopra quella che ha, lascerebbe `.venv`, `uv.lock` e gli altri file della prova, e con
un `.venv` rimasto `uv run main.py` non dà più gli errori da cui si parte.

Per consegnare il materiale si usa `_build/esporta.py`, che prima fa un build completo:

    uv run python _build/esporta.py                      # dist/Aula_Base.zip e dist/Aula_Avanzata.zip
    uv run python _build/esporta.py avanzata             # una sola aula (oppure base)
    uv run python _build/esporta.py --moduli 3 4         # aggiornamento dei soli moduli 3 e 4
    uv run python _build/esporta.py avanzata --riserva   # la riserva di un'aula: dist/Riserva_Avanzata.zip

Nello zip entrano solo i file che git traccia o non ignora, quindi restano fuori `.venv`, le cache e i file che i
notebook e gli script producono quando si eseguono. Per lo stesso motivo un file nuovo da consegnare non deve stare in
un percorso che `.gitignore` esclude.

Gli zip completi si mandano prima della prima giornata. Se i moduli 3 e 4 cambiano dopo le prime due giornate,
`--moduli 3 4` scrive `dist/Aula_Base_moduli_3_4.zip` e `dist/Aula_Avanzata_moduli_3_4.zip`, che contengono, dentro
la cartella `Aula_X`, soltanto `Modulo_3`, `Modulo_4`, le soluzioni di quei moduli con `Soluzioni/corso.py`, `Dati/` e
`Schede/`. Il corsista estrae lo zip in `C:\Corso\`, cioè nella cartella che contiene la sua cartella del corso, e
sceglie di sostituire i file: `Modulo_1` e `Modulo_2`, in cui sta il suo lavoro, non sono nello zip e restano come
sono. Lo zip di aggiornamento non contiene `pyproject.toml` né `uv.lock`, quindi se serve una libreria nuova si manda
anche lo zip completo e si chiede di copiarne quei due file nella cartella del corso e di lanciare di nuovo `uv sync`.
Lo zip della riserva, `dist/Riserva_Avanzata.zip` (o `Riserva_Base.zip`), contiene `Riserva/<Aula>/` con i notebook
di riserva e il loro `corso.py`, e si estrae dentro la cartella dell'aula: in `Aula_Avanzata/Riserva/Avanzata/` i
percorsi `../../Dati/` dei notebook di riserva arrivano ai dati del corso.

## Margine (ottobre 2026)
- Ogni modulo occupa un blocco di 240 minuti, di cui 30 di pause. Nei moduli 1-3 restano 60 minuti di esercitazione e
  al massimo 150 di lezione, mentre il modulo 4, senza esercitazione, ha 210 minuti di lezione. I tempi per notebook
  sono in PIANO_OTTOBRE_2026.md e nella `Guida_docente.md`, che dice anche dove tagliare se si è in ritardo; le
  sezioni Extra non si contano.
- Il materiale secondario sta in `Approfondimenti_1/2` (num A1/A2, `fuori_programma=True`): fuori dalla catena
  precedente/prossimo, con esercizi e soluzioni, da aprire se la classe è avanti. Non si aggiungono sezioni facoltative
  dentro i notebook del percorso: quello che è facoltativo sta negli Approfondimenti o è un esercizio (facoltativo). Le
  sole eccezioni sono la sezione Extra in fondo ai notebook e, nell'Esercitazione 1 dell'Avanzata, la parte con gli
  esercizi classici da fare a casa.
