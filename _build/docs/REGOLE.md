# Regole del materiale 2026 (struttura, volume, dominio)

Si legge insieme a REQUISITI.md (le richieste del docente) e al REGOLE.md (formato e API del toolkit).

## Voce (sostituita da STILE.md, ottobre 2026: leggere quello)
- Prosa da libro tecnico o blog tecnico che spiega come si fa una cosa: paragrafi di 2-5 frasi complete e legate,
  che dicono che cosa fa lo strumento, a cosa serve e cosa mostra la cella sotto. Curata, fluida, senza nessuna frase
  ad effetto: niente antitesi, slogan, metafore, domande retoriche, triadi, "davvero", "che contano".
- Il modello è la prosa del docente nei notebook originali. Niente celle etichetta ("Esempio:"), niente catene di due
  punti, niente frasi telegrafiche in sequenza, niente elenchi con grassetto in testa al posto della spiegazione.
- Titoli descrittivi e piatti. Commenti di codice brevi; `# Output: ...` ammesso. "Noi" quando lavoriamo, impersonale
  per le regole, "tu" nelle consegne. Italiano con il gergo in inglese dove si usa in inglese.

## Volume
- Una cella di testo: un paragrafo di 2-5 frasi (40-90 parole), uno per cella di codice che introduce. Due celle di
  testo adiacenti sullo stesso codice si fondono. Niente box Ricorda. Box ammessi con parsimonia: Attenzione (rosso,
  raro), Esercizio/Prova tu (verde), Soluzione (azzurro); Nota e Approfondimento sono citazioni.
- Prova tu: al massimo 2 per notebook, senza cella di verifica. Esercizi di fine notebook: 2-3, uno può essere
  facoltativo; ogni esercizio ha una `verifica=` con 1-3 assert (nel notebook: `verifica("7.1")`).
- Un esercizio per concetto nel corso: le f-string hanno un solo esercizio (01).

## Dominio
- Esempi e esercizi semplici in scenari comuni (spesa, viaggi, voti, ricette, sport, meteo, biblioteca, negozio, musica).
- Energia/utility solo con dati veri (Terna, TexasTurbine, U.S. Electricity Prices, Open-Meteo, sensori Lombardia) e nei
  dataset inventati già esistenti usati da pandas in poi (letture POD, impianti FV, bolletta, utility.db, prezzi zonali,
  Homework). Negli esercizi di sintassi (00-05) niente POD, kWh, bollette, fasce.

## Struttura
- Testata piana (ottobre 2026): H1, una riga con tempo e dati, "In questo notebook impariamo a" con 3 obiettivi. Niente box,
  niente intento. Indice solo se il notebook ha almeno 50 celle. Sezioni numerate. Ultima sezione "Esercizi". Chiusura con
  link precedente/prossimo e, in piccolo, blocco · giornata · aula.
- Colore solo per Esercizio/Prova tu (verde), Soluzione (azzurro), Attenzione (rosso, tre in tutto il corso). Nota e
  Approfondimento sono citazioni (`>`). Ogni notebook punta alla sua Scheda con "Riassunto in una pagina: [...]".
- Dimostrazioni del docente (VS Code, kernel, ambiente/uv, script, Ruff, Data Wrangler, wrapper API): NIENTE nel
  notebook. Stanno in `Extra/` e nella `Guida_docente.md`.
- Due aule dallo stesso sorgente: Avanzata aggiunge le parti (A); Base non vede buchi.
- Il materiale deve reggere da solo dopo il corso: quello che si rilegge a settembre è scritto, in breve.

## Margine (ottobre 2026)
- Il percorso principale sta in 340-360 minuti per giornata su 420: il resto è margine per installazioni, domande, pause.
- Il materiale secondario sta in `Approfondimenti_1/2` (num A1/A2, `fuori_programma=True`): fuori dalla catena
  precedente/prossimo, con esercizi e soluzioni, da aprire se la classe è avanti. Non si aggiungono sezioni facoltative
  dentro i notebook del percorso: quello che è facoltativo sta negli Approfondimenti o è un esercizio (facoltativo).
