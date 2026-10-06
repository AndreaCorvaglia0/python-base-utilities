"""11 · Agenti per il coding."""

from nbkit import Notebook


def costruisci() -> Notebook:
    nb = Notebook(
        num="11",
        file="11_Agenti_per_il_coding",
        titolo="Agenti per il coding",
        blocco=4,
        giornata=2,
        intento="Copilot scrive codice in fretta e sbaglia con grande sicurezza. Impariamo a usarlo come un collega svelto a cui si controlla sempre il lavoro.",
        obiettivi=[
            "usare Copilot in VS Code per completare, chiedere e far spiegare",
            "sapere cosa sono token, finestra di contesto e modelli quanto basta per non fidarsi alla cieca",
            "applicare tre regole prima di accettare codice generato",
        ],
        tempo={"base": 40, "avanzata": 40},
        dati=["impianti_fv.csv", "letture_pod_2025.csv"],
    )

    # ------------------------------------------------------------------ 1
    nb.sezione("Cosa fa Copilot in VS Code", intro="""
        GitHub Copilot vive dentro VS Code in due forme. Il completamento propone codice in grigio mentre
        scrivi: **Tab** lo accetta, **Esc** lo rifiuta. La chat risponde a domande e scrive codice su
        richiesta: si apre con **Ctrl+Alt+I** (su Mac **Cmd+Alt+I**), oppure dentro una cella con
        **Ctrl+I**.
    """)
    nb.md("""
        La chat ha tre modalità, che si scelgono dal menu in basso nel riquadro della chat.

        | Modalità | Cosa fa | Quando usarla |
        |---|---|---|
        | Ask | risponde, il codice lo copi tu | domande, spiegazioni, una funzione alla volta |
        | Edit | modifica il file aperto e ti mostra le differenze da accettare | rinominare, aggiungere una docstring, sistemare un blocco |
        | Agent | legge i file, esegue comandi, crea celle, finché non pensa di aver finito | compiti lunghi che sai controllare pezzo per pezzo |
    """)
    nb.md("""
        Claude Code e Codex fanno la stessa cosa con un vestito diverso: Claude Code nel terminale o come
        estensione di VS Code, Codex nel terminale o dentro ChatGPT. Cambia il modello sotto e qualche
        comando. Le regole che vediamo alla fine valgono per tutti e tre.
    """)
    nb.md("""
        Partiamo dal completamento. Il modo più affidabile di ottenerlo è scrivere la firma di una funzione
        e una docstring che dice cosa deve fare: Copilot legge la docstring e propone il corpo.
    """)
    nb.prova_tu(
        richiesta="""
            Nella cella qui sotto cancella i tre puntini, premi **Invio** dopo la docstring e aspetta un
            secondo: Copilot propone il corpo della funzione. Accettalo con **Tab** solo se fa quel che dice
            la docstring: somma delle potenze quartorarie divisa per 4. Poi esegui la verifica.
        """,
        starter="""
            def mw_a_mwh(potenze_mw):
                \"\"\"Energia in MWh di una lista di potenze medie quartorarie in MW.\"\"\"
                ...


            mw_a_mwh([100, 100, 100, 100])
        """,
        soluzione="""
            def mw_a_mwh(potenze_mw):
                \"\"\"Energia in MWh di una lista di potenze medie quartorarie in MW.\"\"\"
                return sum(potenze_mw) / 4


            mw_a_mwh([100, 100, 100, 100])
        """,
        verifica="""
            assert mw_a_mwh([100, 100, 100, 100]) == 100, "❌ Quattro quartorari a 100 MW sono 100 MWh"
            assert mw_a_mwh([12.4, 12.9, 13.1, 12.6]) == 12.75, "❌ Somma delle potenze diviso 4, senza arrotondare"
        """,
    )
    nb.md("""
        Se il corpo proposto era diverso (un ciclo, una media, `* 0.25`), può essere giusto lo stesso: la
        verifica decide, non l'aspetto del codice. È il primo controllo che faremo sempre.
    """)

    # ------------------------------------------------------------------ 2
    nb.sezione("Le parole che servono", intro="""
        Sei parole bastano per capire perché Copilot a volte è brillante e a volte inventa. Le slide le
        raccontano; qui restano scritte per quando serviranno.
    """)
    nb.md("""
        | Parola | Cos'è | Perché ti riguarda |
        |---|---|---|
        | token | il pezzo di testo che il modello legge e scrive: circa tre quarti di parola | si paga e si conta in token; un traceback intero costa poco, un errore non capito di più |
        | finestra di contesto | quanti token il modello tiene in mente in una conversazione | se la chat "dimentica" la colonna di cui parlavi dieci messaggi fa, la finestra è piena: chat nuova |
        | cache | le parti di contesto già lette, riusate senza rileggerle | ripetere un prompt lungo costa poco; cambiarne l'inizio fa ripartire da zero |
    """)
    nb.md("""
        | Parola | Cos'è | Perché ti riguarda |
        |---|---|---|
        | modello piccolo o grande | il completamento usa un modello piccolo e veloce, la chat uno grande e lento | per un `groupby` basta il piccolo; per un traceback strano serve il grande |
        | plan e agent | prima il piano dei passi, poi le modifiche | fai scrivere il piano, leggilo, e solo dopo lascialo eseguire |
        | prompt e contesto | il prompt è la domanda; il contesto è tutto il resto che il modello vede: file aperti, celle, quello che incolli | la qualità della risposta dipende più dal contesto che dalla domanda |
    """)
    nb.md("""
        Il contesto è la parte che decidi tu. Tre cose cambiano tutto: `df.info()` incollato nella chat
        (nomi, tipi e righe), i nomi esatti delle colonne, il traceback intero dalla prima riga all'ultima.
        Carichiamo il DataFrame su cui lavoreremo e guardiamo cosa gli daremo da leggere.
    """)
    nb.code("""
        import pandas as pd

        df = pd.read_csv("../Dati/impianti_fv.csv")
        df.info()
    """)
    nb.md("""
        Questo output è il contesto da incollare. "Ho un DataFrame con degli impianti" fa indovinare i nomi
        delle colonne; `df.info()` li dà, con i tipi. Un prompt completo somiglia a questo:
    """)
    nb.md("""
        ```text
        Ho un DataFrame pandas `df` con queste colonne:
        id_impianto (str), comune (str), provincia (str), kwp (float), anno_allaccio (int), lat e lon (float).
        Scrivi una funzione `potenza_per_provincia(df)` che restituisce un DataFrame con due colonne,
        provincia e kwp, con la somma dei kwp per provincia, ordinato dal più alto al più basso.
        Niente commenti, docstring di una riga.
        ```
    """)
    nb.box("ricorda", """
        Il prompt dice cosa vuoi; il contesto dice su cosa. Senza `df.info()` e i nomi delle colonne, il
        modello inventa quelli che gli sembrano plausibili.
    """)

    # ------------------------------------------------------------------ 3
    nb.sezione("Prova guidata", intro="""
        Quattro prompt, in ordine, sullo stesso `df`. Per ognuno: copia il testo nella chat in modalità Ask,
        leggi la risposta, incolla il codice nella cella sotto, esegui, controlla. La verifica guarda il
        risultato finale, non da dove viene.
    """)
    nb.sottosezione("Una funzione", intro="""
        Il primo prompt è quello della sezione precedente. Copialo com'è.
    """)
    nb.md("""
        ```text
        Ho un DataFrame pandas `df` con queste colonne:
        id_impianto (str), comune (str), provincia (str), kwp (float), anno_allaccio (int), lat e lon (float).
        Scrivi una funzione `potenza_per_provincia(df)` che restituisce un DataFrame con due colonne,
        provincia e kwp, con la somma dei kwp per provincia, ordinato dal più alto al più basso.
        Niente commenti, docstring di una riga.
        ```

        Cosa controllare: `groupby` sulla provincia e `sum` sui kwp; `sort_values` con `ascending=False`;
        `reset_index`, così provincia torna colonna. E un numero che conosci: la somma della colonna kwp
        deve restare la stessa, 737.
    """)
    nb.prova_tu(
        richiesta="""
            Incolla la funzione proposta da Copilot al posto dei puntini, eseguila su `df` e salva il
            risultato in `per_provincia`.
        """,
        starter="""
            ...


            per_provincia = potenza_per_provincia(df)
            per_provincia
        """,
        soluzione="""
            def potenza_per_provincia(df):
                \"\"\"Somma dei kWp per provincia, dalla più alta alla più bassa.\"\"\"
                somma = df.groupby("provincia")["kwp"].sum().reset_index()
                return somma.sort_values("kwp", ascending=False).reset_index(drop=True)


            per_provincia = potenza_per_provincia(df)
            per_provincia
        """,
        verifica="""
            assert set(per_provincia.columns) == {"provincia", "kwp"}, "❌ Due colonne: provincia e kwp (serve un reset_index dopo il groupby)"
            assert round(per_provincia["kwp"].sum(), 1) == 737.0, "❌ La somma dei kwp deve restare 737: controlla che sommi e non faccia la media"
            assert per_provincia["kwp"].is_monotonic_decreasing, "❌ Ordina dal più alto al più basso: ascending=False"
            assert per_provincia.iloc[0]["provincia"] == "MI", "❌ La prima riga dovrebbe essere Milano"
        """,
    )

    nb.sottosezione("La spiegazione di un errore", intro="""
        Questa cella dà errore apposta: eseguila e copia il traceback intero, dalla prima riga all'ultima.
    """)
    nb.code('totale_kwp = df["kWp"].sum()', errore=True)
    nb.md("""
        ```text
        Spiegami questo errore senza correggerlo: cosa significa, perché succede, dove devo guardare.

        <incolla qui il traceback intero>
        ```

        Cosa controllare: la risposta deve nominare `KeyError`, dire che la colonna `kWp` non esiste e
        che pandas distingue maiuscole e minuscole. Se propone anche il codice corretto va bene, ma prima
        leggi la spiegazione: è quella che ti serve la prossima volta.
    """)
    nb.prova_tu(
        richiesta="""
            Correggi la riga e salva il totale in `totale_kwp`.
        """,
        starter="""
            totale_kwp = ...
            totale_kwp
        """,
        soluzione="""
            totale_kwp = df["kwp"].sum()
            totale_kwp
        """,
        verifica="""
            assert totale_kwp == 737.0, "❌ La colonna si chiama kwp, tutta minuscola"
        """,
    )

    nb.sottosezione("Un grafico", intro="""
        Il terzo prompt chiede un grafico. Qui Copilot rende di più: conosce Plotly meglio di chiunque
        ricordi a memoria i nomi dei parametri.
    """)
    nb.md("""
        ```text
        Con Plotly Express fai un istogramma della colonna kwp del DataFrame pandas `df`:
        titolo "Potenza degli impianti", etichetta dell'asse x "potenza (kWp)", 20 barre.
        Salva la figura nella variabile fig e mostrala.
        ```

        Cosa controllare: `import plotly.express as px`, `px.histogram` con `nbins=20`, il titolo e
        `labels` per l'etichetta, `fig.show()` alla fine. Se la figura appare ma il titolo manca, non è
        finita.
    """)
    nb.prova_tu(
        richiesta="""
            Incolla il codice proposto e lascia la figura in `fig`.
        """,
        starter="""
            import plotly.express as px

            fig = ...
            fig.show()
        """,
        soluzione="""
            import plotly.express as px

            fig = px.histogram(df, x="kwp", nbins=20, title="Potenza degli impianti", labels={"kwp": "potenza (kWp)"})
            fig.show()
        """,
        verifica="""
            assert len(fig.data) == 1 and fig.data[0].type == "histogram", "❌ fig deve contenere un solo istogramma (px.histogram)"
            assert fig.layout.title.text == "Potenza degli impianti", "❌ Il titolo deve essere esattamente 'Potenza degli impianti'"
        """,
    )

    nb.sottosezione("Un parametro inventato apposta", intro="""
        Il quarto prompt contiene una trappola: un parametro che non esiste. Vediamo se Copilot se ne
        accorge o ci segue.
    """)
    nb.md("""
        ```text
        Aggiungi al DataFrame `df` una colonna eta_anni con gli anni passati dall'allaccio a oggi (siamo nel 2026).
        Usa il parametro years=True di pd.to_datetime sulla colonna anno_allaccio.
        ```

        Cosa controllare: `pd.to_datetime` non ha nessun parametro `years`. Verificalo tu con
        `help(pd.to_datetime)`. Se Copilot l'ha usato lo stesso, hai appena visto un'invenzione: la cella
        darebbe `TypeError`. Se ti ha detto che non esiste e ha proposto una sottrazione, bene: la strada
        giusta è `2026 - df["anno_allaccio"]`.
    """)
    nb.prova_tu(
        richiesta="""
            Scrivi la versione giusta: la colonna `eta_anni` come differenza tra 2026 e l'anno di allaccio.
        """,
        starter="""
            df["eta_anni"] = ...
            df[["id_impianto", "anno_allaccio", "eta_anni"]].head()
        """,
        soluzione="""
            df["eta_anni"] = 2026 - df["anno_allaccio"]
            df[["id_impianto", "anno_allaccio", "eta_anni"]].head()
        """,
        verifica="""
            assert df["eta_anni"].max() == 15 and df["eta_anni"].min() == 1, "❌ eta_anni: 2026 meno anno_allaccio, da 1 a 15"
        """,
    )
    nb.md("""
        Il quarto prompt è il più istruttivo: Copilot non sa cosa non sa. Se il prompt suggerisce un
        parametro, spesso lo usa; se il parametro non esiste, l'errore arriva a te, non a lui.
    """)

    # ------------------------------------------------------------------ 4
    nb.sezione("Le tre regole", intro="""
        Tre regole prima di accettare codice generato, da chiunque arrivi. Sono le stesse che useremo nel
        capstone, dove Copilot avrà il permesso di aiutare sui dettagli e non sulla logica.
    """)
    nb.md("""
        **Verifica.** Esegui subito, guarda l'output, confrontalo con un numero che conosci già: la somma
        dei kwp, il numero di righe, il valore di un POD che hai sotto mano. Un parametro mai visto si
        controlla con `help()` prima di usarlo, non dopo l'errore.
    """)
    nb.md("""
        **Chiedi spiegazioni.** "Spiegami" prima di "correggi", e sempre con il traceback intero. Se la
        spiegazione non la capisci, il codice corretto non lo accetti: domani lo stesso errore tornerà e tu
        sarai senza chat.
    """)
    nb.md("""
        **Piccoli passi.** Un prompt, una cella, un controllo. "Fai tutta l'analisi" produce un notebook
        lungo con tre errori nascosti in mezzo; "calcola il profilo medio orario" produce una cella che
        puoi leggere. La modalità Agent va bene solo su cose che sai controllare pezzo per pezzo.
    """)
    nb.box("ricorda", """
        - Verifica con un numero che conosci, non con l'aspetto del codice.
        - "Spiegami l'errore" con il traceback intero, mai solo "risolvilo".
        - Un prompt, una cella, un controllo.
    """)

    # ------------------------------------------------------------------ Esercizi
    nb.sezione("Esercizi")
    nb.esercizio(
        titolo="Il parametro inventato",
        scenario="""
            L'ufficio misure ci manda `letture_pod_2025.csv`, il solito CSV all'italiana: punto e virgola,
            virgola decimale, codifica latin-1. Giulia ha chiesto a Copilot di leggerlo con i nomi dei
            parametri che ricordava lei, ha incollato quel che le ha dato, e adesso la cella dà `TypeError`.
            Ha un treno tra venti minuti.
        """,
        richiesta="""
            1. Dai alla chat questo prompt e incolla la riga che propone al posto di quella commentata:

               ```text
               Leggi il file ../Dati/letture_pod_2025.csv con pandas: separatore punto e virgola,
               virgola come decimale, codifica latin-1. Usa i parametri separator, decimal_separator ed encoding.
               ```
            2. Eseguila. Se dà `TypeError`, leggi l'ultima riga del traceback: quale parametro non esiste?
            3. Apri la documentazione con `help(pd.read_csv)` e trova i nomi giusti per il separatore dei
               campi e per il decimale.
            4. Leggi il file in `letture` con i parametri giusti e controlla con `letture.info()`: la
               colonna `kwh` deve essere `float64`.
        """,
        suggerimento="Nella firma di `read_csv` i parametri sono in ordine: quello del separatore è tra i primi, quello del decimale più in basso.",
        starter="""
            # 1-2. incolla qui la riga proposta da Copilot ed eseguila: leggi l'ultima riga del traceback
            # letture = pd.read_csv("../Dati/letture_pod_2025.csv", ...)

            # 3. la documentazione: cerca i parametri per il separatore e per il decimale
            # help(pd.read_csv)

            # 4. la lettura giusta
            letture = ...
            letture.info()
        """,
        soluzione="""
            letture = pd.read_csv("../Dati/letture_pod_2025.csv", sep=";", decimal=",", encoding="latin-1")
            letture.info()
        """,
        verifica="""
            assert letture.shape == (216, 5), "❌ letture: 216 righe e 5 colonne; con il separatore sbagliato esce una colonna sola"
            assert set(letture.columns) == {"pod", "cliente", "data", "fascia", "kwh"}, "❌ Le colonne devono essere pod, cliente, data, fascia, kwh"
            assert str(letture["kwh"].dtype) == "float64", "❌ kwh deve essere float64: serve decimal=','"
            assert round(letture["kwh"].sum(), 1) == 134507.7, "❌ La somma dei kwh non torna: controlla decimal e sep"
        """,
        perche="I nomi dei parametri non si indovinano: `sep` e `decimal` stanno nella firma di `read_csv`. Copilot li conosce benissimo, finché il prompt non gliene suggerisce altri.",
        passo_in_piu=dict(
            testo="""
                Chiedi a Copilot, in modalità Ask, di incapsulare la lettura giusta in una funzione
                `leggi_letture(path)` con docstring di una riga e type hint. Incollala, poi controlla con
                `help(leggi_letture)` che la docstring ci sia e che il risultato sia lo stesso di prima.
            """,
            starter="""
                ...


                help(leggi_letture)
                letture_bis = leggi_letture("../Dati/letture_pod_2025.csv")
            """,
            soluzione="""
                def leggi_letture(path: str) -> pd.DataFrame:
                    \"\"\"Legge un CSV di letture all'italiana: punto e virgola, virgola decimale, latin-1.\"\"\"
                    return pd.read_csv(path, sep=";", decimal=",", encoding="latin-1")


                help(leggi_letture)
                letture_bis = leggi_letture("../Dati/letture_pod_2025.csv")
            """,
            verifica="""
                assert leggi_letture.__doc__, "❌ La funzione deve avere una docstring"
                assert letture_bis.shape == (216, 5), "❌ leggi_letture deve restituire le stesse 216 righe e 5 colonne"
            """,
        ),
    )
    nb.esercizio(
        titolo="Spiegami l'errore",
        bis=True,
        scenario="""
            Marco, di reperibilità nel weekend, deve mandare al commerciale la lista degli impianti sopra
            i 10 kWp in provincia di Milano. Ha scritto il filtro di corsa e la cella esplode con un
            `TypeError` lungo tre schermate. Ci chiede un occhio prima di chiamare qualcuno.
        """,
        richiesta="""
            1. La cella qui sotto dà errore apposta: eseguila e copia il traceback intero.
            2. Dai alla chat questo prompt:

               ```text
               Spiegami questo errore senza correggerlo. Perché Python prova a fare 10 & una colonna di testo?

               <incolla qui il traceback intero>
               ```
            3. La spiegazione deve parlare di precedenza: `&` viene valutato prima di `>` e `==`. Se non lo
               dice, chiediglielo.
            4. Correggi la riga nella stessa cella, con le parentesi attorno a ogni condizione, e lascia il
               risultato in `grandi_milano`.
        """,
        suggerimento="Il traceback è lungo perché passa per pandas; l'ultima riga dice chi non sa fare `&` con chi.",
        starter="""
            impianti = pd.read_csv("../Dati/impianti_fv.csv")

            grandi_milano = impianti[impianti["kwp"] > 10 & impianti["provincia"] == "MI"]
            grandi_milano
        """,
        soluzione="""
            impianti = pd.read_csv("../Dati/impianti_fv.csv")

            grandi_milano = impianti[(impianti["kwp"] > 10) & (impianti["provincia"] == "MI")]
            grandi_milano
        """,
        verifica="""
            assert len(grandi_milano) == 5, "❌ grandi_milano: 5 impianti sopra i 10 kWp in provincia di Milano"
            assert set(grandi_milano["provincia"]) == {"MI"}, "❌ Solo la provincia MI"
            assert (grandi_milano["kwp"] > 10).all(), "❌ Solo gli impianti sopra i 10 kWp"
        """,
        perche="Le parentesi attorno a ogni condizione non sono stile: senza, `10 & impianti[\"provincia\"]` viene calcolato per primo e non ha senso.",
    )
    return nb
