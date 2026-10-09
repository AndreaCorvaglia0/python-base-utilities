# REQUISITI CONSOLIDATI (edizione Sorgenia 2026) — vincolanti, prevalgono sul CHARTER dove diverso

Raccolti dalle richieste del docente, nell'ordine: brief iniziale, chiarimento sull'obiettivo (agenti), decisioni
(fallback, resample, script, Ruff), e la revisione del 6 ottobre ("semplifica").

## 1. Il materiale del docente è la base
- I notebook originali del docente (branch `main`: 00 Jupyter, 01 Introduzione e sintassi, 02 Tipi di dato,
  03 Funzioni e controllo, 04 Pandas, 05 Pandas import dati, 06 Pandas time series, Quickstart Plotly, 99 Capstone)
  vanno bene e vanno tenuti: stesso ordine degli argomenti, stesse spiegazioni e stessi esempi dove ci sono.
- Il contributo del lavoro è: impacchettare con uno stile costante e curato, sfoltire leggermente, aggiungere gli
  esercizi, aggiungere gli argomenti del programma che mancavano (oggetti ed errori, codice leggibile, agenti,
  capstone senza forecast) e la piccola aggiunta concordata: come leggere il codice scritto da un agente
  (type hint, decoratori, dataclass, generatori ecc.), con esempi; la parte avanzata per l'aula Avanzata.
- Il flusso è quello del documento dei requisiti (Proposta_Programma_2026_v2) integrato con il materiale del docente.
- Niente ML, niente forecast, niente Prophet.

## 2. Semplificare: la parola d'ordine
- Meno materiale, fatto bene: meno dettagli, meno rumore, meno "complicazioni inutili".
- Niente pagine di spiegazione: il docente parla in aula. Scritto ci va quello che serve a seguire e a rileggere dopo.
- Assert e celle di verifica: utili ma non ovunque. Regola: i "Prova tu" dentro al notebook NON hanno celle di
  verifica (si dice il risultato atteso in una riga); gli esercizi di fine notebook hanno al massimo UNA cella di
  verifica, corta (1-3 assert), solo quando il risultato è un numero o una tabella controllabile.
- Un esercizio per concetto, non tre: le f-string hanno UN esercizio in tutto il corso; non ripetere lo stesso
  esercizio con numeri diversi in notebook diversi.
- Meno riquadri, meno "passo in più", meno "bis": il bis solo dove al docente serve davvero una scelta.
- Esercitazione organizzata: momenti di esercitazione con domande ed esercizi, strutturati, non esercizi sparsi.

## 3. Cosa NON va nei notebook (lo mostra il docente dal vivo)
VS Code, estensioni, scelta del kernel, ambiente virtuale e uv, script vs notebook e terminale, Ruff, Data Wrangler,
il wrapper dell'API. Vanno in una **Guida per il docente** che dice quando farli, cosa mostrare e quanto tempo
prendono; il tempo si conta nel totale della giornata. Nel notebook resta al massimo una riga che segna il punto
("Qui il docente mostra ...").
Il setup per i corsisti resta nel README (uv sync, kernel), non nei notebook.

## 4. Dominio degli esempi e degli esercizi
- Esempi e esercizi semplici NON nel dominio utility/energia: scenari che tutti riconoscono (spesa, viaggi, voti,
  ricette, sport, meteo di casa, biblioteca, negozio...). Potremmo dire sciocchezze senza accorgercene.
- Il dominio energia entra solo quando si usano dati veri: Terna (carico Nord), TexasTurbine, U.S. Electricity
  Prices, Open-Meteo, sensori Regione Lombardia. Lì gli esercizi "seri" sono di dominio per forza.
- Occasionalmente, negli esercizi semplici, un tocco di dominio è ammesso; non la regola.
- I dataset di esempio inventati nel dominio utility (letture POD, impianti FV, bolletta, utility.db, prezzi zonali,
  homework) non rispettano la regola: vanno sostituiti con dati inventati di dominio comune o tolti (decisione del docente).

## 5. Tono e lingua
- Racconto neutrale che guida la didattica: non secco, non sensazionalistico. Niente parole a effetto, frasi fatte,
  claim, titoli "a effetto" ("Le scorciatoie che servono davvero" → "Le scorciatoie da tastiera"). Titoli descrittivi,
  come nei notebook del docente ("Selezione dei dati", "Valori mancanti").
- Italiano fluente; il gergo che in Italia si dice in inglese resta in inglese (homework, notebook, kernel, script,
  formatter, linter, encoding, type hint, backtick, DataFrame...). "Homework", mai "compito a casa".
- Mai frasi meta sul corso, sull'aula, sulle versioni o sulle regole.
- Non "voi"; "noi" operativo e "tu" quando si affida un compito.

## 6. Cosa resta dell'impianto attuale
- Due aule (Base, Avanzata) dallo stesso sorgente; Homework tra le due giornate; capstone a fine corso (Terna +
  Open-Meteo, senza forecast); uv per il setup (README); le schede di una pagina; il generatore `_build/`.
- Il sistema visivo (banner, indice, riquadri) resta ma più sobrio: meno riquadri per notebook.
- L'obiettivo del corso resta: utenti consapevoli degli agenti per il coding, che sanno leggere il codice. Si dichiara
  una volta (00 e README), senza slogan.

## 7. Processo
- Fable dirige, organizza e controlla; Opus, Sonnet e Haiku per i task in base al peso (è un lavoro di taglio: costa meno).
- Le decisioni grosse si chiedono al docente prima di farle.

## 8. Decisioni del docente (6 ottobre, seconda tornata)
1. **Base = i notebook originali del docente.** Dove la riscrittura ha sostituito spiegazioni o esempi del docente, si
   ripristinano quelli di `main` (stesso ordine, stessi esempi), impacchettati nello stile della casa e leggermente
   sfoltiti. Il testo nuovo resta solo per gli argomenti che il docente non aveva scritto (codice leggibile, oggetti ed
   errori, agenti, capstone senza forecast, Homework).
2. **I dataset inventati nel dominio utility restano** (letture POD, impianti FV, bolletta, utility.db, prezzi zonali,
   Homework). La regola "niente utility" vale per gli esempi piccoli e gli esercizi semplici di sintassi.
3. **Esercizi:** 2-3 esercizi brevi a fine notebook più una Esercitazione per blocco (blocchi 1-3; il capstone è
   l'esercitazione del blocco 4), senza esagerare: poco tempo. Esercizi **facoltativi** segnati come tali, da fare in
   aula o lasciare ai corsisti a seconda della situazione.
4. **Dimostrazioni del docente** (VS Code, kernel, ambiente e uv, script, Ruff, Data Wrangler, wrapper API): niente nel
   notebook. Il materiale già scritto si sposta in una cartella separata `Extra/` (notebook a sé, con la teoria), così il
   docente vede come sarebbe stato svolto. Una `Guida_docente.md` dice quando farle e quanto durano; il tempo entra nel totale.
