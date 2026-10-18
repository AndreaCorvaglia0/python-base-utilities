"""
nbkit: il generatore dei notebook del corso.

Ogni notebook è descritto da uno script in `_build/src/` che espone una funzione `costruisci()`
e restituisce un `Notebook`. Dallo stesso sorgente si ottengono quattro file, dentro le due cartelle che i
corsisti ricevono:

    Aula_Base/Modulo_N/NN_Titolo.ipynb        Aula_Avanzata/Modulo_N/NN_Titolo.ipynb
    Aula_Base/Soluzioni/NN_Titolo.ipynb       Aula_Avanzata/Soluzioni/NN_Titolo.ipynb

Il modulo è `blocco` (un intero, o un dizionario per aula). Per i notebook del percorso la voce di `PROGRAMMA`
dice anche la sottocartella dentro il modulo, se c'è (per esempio `Modulo_1/Script_uv_Ruff/`), e se esiste una copia
con le soluzioni. I percorsi verso `Dati/` e `Schede/` partono dalla radice dell'aula: da `Modulo_N/` e da
`Soluzioni/` si scrive `../Dati/`, da una sottocartella del modulo `../../Dati/`. Il materiale di riserva
(`riserva=True`) va in `Riserva/<Aula>/`, fuori dalle cartelle dei corsisti.

Uso tipico:

    from nbkit import Notebook

    def costruisci():
        nb = Notebook(num="05", file="05_Oggetti_ed_errori", titolo="Oggetti ed errori",
                      blocco=2, giornata=1, intento="...", obiettivi=["...", "...", "..."],
                      tempo={"base": 90, "avanzata": 95}, dati=[])
        nb.sezione("Decidere con if")
        nb.md("Testo in markdown.")
        nb.code("x = 4\\nx > 2")
        nb.box("nota", "Una precisazione.")
        with nb.solo("avanzata"):
            nb.sezione("List comprehension")
            ...
        nb.sezione("Esercizi")
        nb.esercizio(titolo="...", scenario="...", richiesta="...", suggerimento="...",
                     starter="...", soluzione="...", verifica="assert ...", perche="...")
        return nb

La `verifica` di un esercizio non finisce nel notebook: build.py la raccoglie in `corso.py`, un modulo
scritto in ogni cartella di notebook, e nel notebook resta `from corso import verifica` + `verifica("5.1")`.

Per le esercitazioni (formato di ottobre 2026) ci sono tre strumenti in più:
  - `Notebook(..., soluzioni_a_richiesta=True)`: sotto la verifica di ogni esercizio compare, nella versione
    studente, la cella `soluzione("E1.3")`, che mostra solo quella soluzione (sta in corso.py, codificata).
  - `nb.esercizio(..., suggerimenti=["prima l'idea", "poi il nome del metodo"])`: aiuti nascosti, uno per
    livello, che il corsista apre con un clic (blocchi <details> dentro il riquadro dell'esercizio).
  - `nb.domanda("Cosa stampa ...?", "Stampa 3, perché ...")`: domanda di riepilogo con la risposta nascosta.

Lo stile della prosa è descritto in `_build/docs/STILE.md`; le regole di struttura in `_build/docs/REGOLE.md`;
le richieste del docente in `_build/docs/REQUISITI.md`. Il lint in fondo a questo file fa rispettare quello che si
può controllare a macchina (celle etichetta, frasi telegrafiche, frasi vietate, titoli a effetto, box Ricorda).
"""

from __future__ import annotations

import contextlib
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

VERSIONE = "2026.1"
AULE = ("base", "avanzata")
NOMI_AULA = {"base": "Aula Base", "avanzata": "Aula Avanzata"}

# ---------------------------------------------------------------------------
# Programma: la sequenza dei notebook, per i link "precedente" e "prossimo". Ogni voce dice in quale modulo sta il
# notebook, in quale sottocartella del modulo (se c'è), per quali aule vale e se ha una versione con le soluzioni.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Voce:
    num: str
    file: str
    titolo: str
    modulo: int
    aule: tuple[str, ...] = AULE
    cartella: str = ""          # sottocartella dentro Modulo_N, se il notebook non sta direttamente nel modulo
    soluzioni: bool = True      # False: il notebook non ha esercizi e non ha una copia in Soluzioni/

    def __post_init__(self):
        # la copia in Soluzioni/ sta un livello più su: i percorsi ../../Dati/ della sottocartella non varrebbero
        if self.cartella and self.soluzioni:
            raise ValueError(f"{self.file}: un notebook in una sottocartella del modulo non può avere la copia in Soluzioni/")


PROGRAMMA = [
    Voce("00", "00_Notebook", "Jupyter e i notebook", 1),
    Voce("01", "01_Python_e_sintassi_base", "Introduzione a Python e sintassi base", 1),
    Voce("02", "02_Tipi_di_dato", "Tipi di dato e manipolazione", 1),
    Voce("03", "03_Codice_leggibile", "Codice leggibile", 1),
    Voce("S", "Ambiente_script_e_Ruff", "Ambiente, script e Ruff", 1, ("avanzata",), "Script_uv_Ruff", False),
    Voce("E1", "Esercitazione_1", "Esercitazione 1", 1),
    Voce("04", "04_Funzioni_e_controllo", "Funzioni e controllo del flusso", 2),
    Voce("05", "05_Oggetti_ed_errori", "Oggetti ed errori", 2),
    Voce("06", "06_Pandas_e_import_dati", "Pandas: Series, DataFrame e import dei dati", 2),
    Voce("E2", "Esercitazione_2", "Esercitazione 2", 2),
    Voce("07", "07_Pandas_operazioni", "Pandas: operazioni sui DataFrame", 3),
    Voce("08", "08_Pandas_date", "Pandas: le date", 3),
    Voce("E3", "Esercitazione_3", "Esercitazione 3", 3),
    Voce("09", "09_Plotly", "Plotly per serie storiche", 4),
    Voce("10", "10_Agenti_per_il_coding", "Agenti per il coding", 4),
    Voce("11", "11_Capstone", "Capstone: il carico del Nord e la temperatura", 4),
]
COMPITO = ("C", "Homework", "Homework")
CARTELLA_SOLUZIONI = "Soluzioni"     # dentro la cartella dell'aula, accanto ai moduli


def cartella_modulo(modulo: int, cartella: str = "") -> str:
    """Il percorso, relativo alla radice dell'aula, della cartella di un notebook del percorso."""
    return f"Modulo_{modulo}" + (f"/{cartella}" if cartella else "")


def posizione(voce: Voce, soluzioni: bool) -> str:
    """Dove sta il file di `voce`, relativo alla radice dell'aula. Un notebook senza esercizi non ha copia in
    Soluzioni/, quindi chi lo cita da lì punta alla versione nel modulo."""
    if soluzioni and voce.soluzioni:
        return f"{CARTELLA_SOLUZIONI}/{voce.file}.ipynb"
    return f"{cartella_modulo(voce.modulo, voce.cartella)}/{voce.file}.ipynb"


def relativo(da_cartella: str, a_file: str) -> str:
    """Percorso relativo (con le barre in avanti) da una cartella a un file, entrambi relativi alla radice."""
    import posixpath

    return posixpath.relpath(a_file, da_cartella or ".")


NOMI_BLOCCO = {
    1: "Modulo 1 · Setup, Python e sintassi di base",
    2: "Modulo 2 · Controllo del flusso, funzioni e primi dati in pandas",
    3: "Modulo 3 · Analisi dei dati con pandas",
    4: "Modulo 4 · Agenti per il coding e capstone",
    0: "Materiale di riserva",
}


def programma(aula: str) -> list[Voce]:
    """Le voci del programma che valgono per `aula`, nell'ordine in cui si affrontano."""
    return [v for v in PROGRAMMA if aula in v.aule]


def _nome_link(n: str, t: str) -> str:
    return f"{n} · {t}" if n[0].isdigit() else t

# ---------------------------------------------------------------------------
# Sistema visivo. Un posto solo: cambiare qui cambia tutto.
# Sfondi trasparenti e nessun `color` forzato: leggibile in tema chiaro e scuro.
# ---------------------------------------------------------------------------
BOX = {
    #  tipo              icona  titolo           bordo       sfondo
    "nota":            ("💡", "Nota",            "#8c8c8c", "rgba(140,140,140,0.12)"),
    "attenzione":      ("⚠️", "Attenzione",      "#d9534f", "rgba(217,83,79,0.12)"),
    "approfondimento": ("📘", "Approfondimento", "#7e57c2", "rgba(126,87,194,0.12)"),
    "ricorda":         ("📌", "Ricorda",         "#e0a800", "rgba(224,168,0,0.14)"),
    "esercizio":       ("✏️", "Esercizio",       "#5cb85c", "rgba(92,184,92,0.12)"),
    "soluzione":       ("✅", "Soluzione",       "#2e9fd6", "rgba(46,159,214,0.12)"),
}
INDICE_DA = 50      # l'indice compare solo nei notebook con almeno tante celle


def _div(sfondo: str, bordo: str, corpo: str, padding: str = "12px 14px") -> str:
    return (
        f'<div style="background:{sfondo}; border-left:4px solid {bordo}; padding:{padding}; '
        f'border-radius:4px; margin:8px 0 12px 0;">\n\n{corpo}\n\n</div>'
    )


def box_html(tipo: str, corpo: str, titolo: str | None = None) -> str:
    icona, nome, bordo, sfondo = BOX[tipo]
    corpo = textwrap.dedent(corpo).strip()
    if tipo == "approfondimento":
        if not titolo:
            raise ValueError("Un Approfondimento ha sempre un titolo")
        testa = f"**{icona} {nome} · {titolo} (puoi saltarlo)**"
    elif titolo:
        testa = f"**{icona} {titolo}**"
    else:
        testa = f"**{icona} {nome}**"
    return _div(sfondo, bordo, f"{testa}\n\n{corpo}")


# Spazio attorno a ogni blocco che si apre con un clic: senza margine due blocchi consecutivi (Passo per passo,
# Suggerimento 1, Suggerimento 2) stanno attaccati e si rischia di aprire quello sbagliato.
STILE_DETTAGLI = "margin: 14px 0;"
STILE_SOMMARIO = "cursor: pointer; padding: 4px 0;"


def _dettagli(titolo: str, corpo: str) -> str:
    """Blocco che si apre con un clic: il titolo resta visibile, il contenuto no."""
    return (
        f'<details style="{STILE_DETTAGLI}">\n<summary style="{STILE_SOMMARIO}">{titolo}</summary>\n\n'
        f"{textwrap.dedent(corpo).strip()}\n\n</details>"
    )


def citazione(tipo: str, corpo: str, titolo: str | None = None) -> str:
    """Nota e Approfondimento: testo citato (barra grigia), senza colore. Il colore resta a esercizi, soluzioni e Attenzione."""
    corpo = textwrap.dedent(corpo).strip()
    if tipo == "approfondimento":
        if not titolo:
            raise ValueError("Un Approfondimento ha sempre un titolo")
        testa = f"**Approfondimento · {titolo}** (si può saltare)."
    else:
        testa = f"**{titolo or 'Nota'}.**"
    testo = testa + ("\n\n" + corpo if "\n" in corpo else " " + corpo)
    return "\n".join(("> " + r) if r else ">" for r in testo.split("\n"))


# ---------------------------------------------------------------------------
# Modello delle celle
# ---------------------------------------------------------------------------
@dataclass
class Cella:
    tipo: str                       # "md" | "code" | "sezione" | "sottosezione" | "esercizio" | "prova"
    src: str = ""
    aula: str | None = None         # None = entrambe
    solo_soluzioni: bool = False
    solo_studente: bool = False
    rete: bool = False
    errore: bool = False            # cella che dà errore apposta (il validatore la accetta)
    ruolo: str | None = None        # tag di ruolo (starter, verifica, soluzione, ...)
    extra: dict = field(default_factory=dict)

    def visibile(self, aula: str, soluzioni: bool) -> bool:
        if self.aula is not None and self.aula != aula:
            return False
        if self.solo_soluzioni and not soluzioni:
            return False
        if self.solo_studente and soluzioni:
            return False
        return True


def _d(testo: str) -> str:
    return textwrap.dedent(testo).strip("\n")


@dataclass
class Notebook:
    num: str
    file: str
    titolo: str
    blocco: int | dict[str, int]    # il modulo (1-4; 0 = riserva), anche diverso per aula
    giornata: int
    intento: str
    obiettivi: list[str] | dict[str, list[str]]
    tempo: int | dict[str, int] = 45
    dati: list[str] | dict[str, list[str]] = field(default_factory=list)
    aule: tuple[str, ...] = AULE
    etichetta_esercizio: str = "Esercizio"
    prefisso_esercizi: str | None = None     # default: num
    prossimo: str | None = None              # testo markdown della chiusura, se diverso dal programma
    extra: bool = False                      # notebook della cartella Extra: versione unica, senza aula
    riserva: bool = False                    # materiale di riserva: Riserva/<Aula>/, fuori dalle cartelle dei corsisti
    fuori_programma: bool = False   # Approfondimenti: fuori dalla catena precedente/prossimo, per le classi che vanno avanti
    soluzioni_a_richiesta: bool = False   # esercitazioni: sotto ogni esercizio una cella soluzione("E1.3") che mostra solo quella
    celle: list[Cella] = field(default_factory=list)
    _aula_corrente: str | None = None

    # ------------------------------------------------------------------ celle
    def _aula(self, aula: str | None) -> str | None:
        return aula if aula is not None else self._aula_corrente

    @contextlib.contextmanager
    def solo(self, aula: str):
        """Tutte le celle aggiunte nel blocco `with` appartengono solo a quell'aula."""
        assert aula in AULE
        prima = self._aula_corrente
        self._aula_corrente = aula
        try:
            yield
        finally:
            self._aula_corrente = prima

    def sezione(self, titolo: str, intro: str | None = None, aula: str | None = None) -> None:
        self.celle.append(Cella("sezione", _d(intro) if intro else "", aula=self._aula(aula), extra={"titolo": titolo}))

    def sottosezione(self, titolo: str, intro: str | None = None, aula: str | None = None) -> None:
        self.celle.append(Cella("sottosezione", _d(intro) if intro else "", aula=self._aula(aula), extra={"titolo": titolo}))

    def md(self, testo: str, aula: str | None = None, solo_soluzioni: bool = False, solo_studente: bool = False) -> None:
        """Cella di testo; `solo_soluzioni` o `solo_studente` la mettono in una sola delle due versioni."""
        self.celle.append(Cella("md", _d(testo), aula=self._aula(aula), solo_soluzioni=solo_soluzioni, solo_studente=solo_studente))

    def code(self, src: str, aula: str | None = None, rete: bool = False, errore: bool = False) -> None:
        """Cella di codice. rete=True se chiama un'API; errore=True se deve dare errore apposta."""
        self.celle.append(Cella("code", _d(src), aula=self._aula(aula), rete=rete, errore=errore))

    def box(self, tipo: str, testo: str, titolo: str | None = None, aula: str | None = None) -> None:
        if tipo not in ("nota", "attenzione", "approfondimento", "ricorda"):
            raise ValueError(f"box: tipo non previsto {tipo!r}")
        if tipo in ("nota", "approfondimento"):
            self.celle.append(Cella("md", citazione(tipo, testo, titolo), aula=self._aula(aula)))
        else:
            self.celle.append(Cella("md", box_html(tipo, testo, titolo), aula=self._aula(aula)))

    def domanda(self, testo: str, risposta: str, aula: str | None = None) -> None:
        """Domanda di riepilogo con la risposta nascosta, che si apre con un clic."""
        self.celle.append(Cella("domanda", _d(testo), aula=self._aula(aula), extra={"risposta": _d(risposta)}))

    def hands_on(self, richiesta: str, starter: str | None = None, soluzione: str | None = None,
                 verifica: str | None = None, aula: str | None = None, rete: bool = False,
                 prova_anche: str | None = None) -> None:
        """Hands-on inline da uno a tre minuti, subito dopo l'esempio che riprende: box verde, cella da completare,
        verifica. `prova_anche` è una riga facoltativa, sempre banale, per chi vuole esplorare un altro caso.

        Senza `starter` e `soluzione` il Hands-on è soltanto un gesto da fare nell'editor (creare una cella,
        premere Restart, aprire la vista delle variabili): resta il riquadro con le istruzioni, senza celle.
        """
        a = self._aula(aula)
        self.celle.append(Cella("prova", _d(richiesta), aula=a, extra={"prova_anche": _d(prova_anche) if prova_anche else None}))
        if starter is None and soluzione is None:
            return
        self.celle.append(Cella("code", _d(starter), aula=a, solo_studente=True, rete=rete, ruolo="starter"))
        self.celle.append(Cella("code", _d(soluzione), aula=a, solo_soluzioni=True, rete=rete, ruolo="soluzione"))
        if verifica:
            self.celle.append(Cella("code", _d(verifica), aula=a, rete=rete, ruolo="verifica", extra={"prova": True}))

    prova_tu = hands_on   # nome precedente, tenuto per i sorgenti non ancora aggiornati

    def esercizio(self, titolo: str, scenario: str, richiesta: str, starter: str, soluzione: str,
                  verifica: str | None = None, suggerimento: str | None = None, perche: str | None = None,
                  bis: bool = False, passo_in_piu: dict | None = None, aula: str | None = None,
                  rete: bool = False, facoltativo: bool = False, suggerimenti: list[str] | None = None) -> None:
        """Esercizio di fine notebook: box verde, starter, verifica (+ soluzione nelle Soluzioni).

        scenario: il paragrafo che apre l'esercizio e dice che cosa vogliamo ottenere, perché conviene farlo in Python
        e, quando possibile, il risultato atteso; da solo deve bastare per arrivare al risultato.
        richiesta: i passi numerati, facoltativi, che il corsista apre con un clic nel blocco "Passo per passo";
        una sola frase resta visibile sotto lo scenario.

        passo_in_piu: dict(testo=..., starter=..., soluzione=..., verifica=...) facoltativo.
        bis=True: è l'alternativa dell'esercizio precedente (stesso numero + "bis").
        suggerimenti: aiuti nascosti, uno per livello, che il corsista apre con un clic (blocchi <details>).
        """
        a = self._aula(aula)
        self.celle.append(Cella("esercizio", "", aula=a, extra={
            "titolo": titolo + (" (facoltativo)" if facoltativo else ""), "scenario": _d(scenario), "richiesta": _d(richiesta),
            "suggerimento": _d(suggerimento) if suggerimento else None, "bis": bis,
            "suggerimenti": [_d(x) for x in (suggerimenti or [])],
            "passo": _d(passo_in_piu["testo"]) if passo_in_piu else None, "perche": _d(perche) if perche else None,
        }))
        self.celle.append(Cella("code", _d(starter), aula=a, solo_studente=True, rete=rete, ruolo="starter"))
        self.celle.append(Cella("md", "", aula=a, solo_soluzioni=True, ruolo="box-soluzione", extra={"perche": _d(perche) if perche else None}))
        self.celle.append(Cella("code", _d(soluzione), aula=a, solo_soluzioni=True, rete=rete, ruolo="soluzione", extra={"esercizio": True}))
        if verifica:
            self.celle.append(Cella("code", _d(verifica), aula=a, rete=rete, ruolo="verifica"))
        if self.soluzioni_a_richiesta:
            self.celle.append(Cella("code", _d(soluzione), aula=a, solo_studente=True, ruolo="rivela"))
        if passo_in_piu:
            self.celle.append(Cella("md", "", aula=a, ruolo="box-passo", extra={"testo": _d(passo_in_piu["testo"])}))
            self.celle.append(Cella("code", _d(passo_in_piu["starter"]), aula=a, solo_studente=True, rete=rete, ruolo="starter"))
            self.celle.append(Cella("code", _d(passo_in_piu["soluzione"]), aula=a, solo_soluzioni=True, rete=rete, ruolo="soluzione"))
            if passo_in_piu.get("verifica"):
                self.celle.append(Cella("code", _d(passo_in_piu["verifica"]), aula=a, rete=rete, ruolo="verifica", extra={"passo": True}))

    # ------------------------------------------------------------------ posizione
    def _per_aula(self, valore, aula: str):
        return valore[aula] if isinstance(valore, dict) else valore

    @property
    def voce(self) -> Voce | None:
        """La voce del programma di questo notebook (None per Approfondimenti, Homework, Extra e riserva)."""
        return next((v for v in PROGRAMMA if v.num == self.num), None)

    def ha_soluzioni(self) -> bool:
        """Se il notebook ha una copia con le soluzioni (i notebook senza esercizi non ce l'hanno)."""
        return self.voce.soluzioni if self.voce else True

    def cartella_rel(self, aula: str, soluzioni: bool) -> str:
        """La cartella del notebook, relativa alla radice in cui viene scritto (vuota per Extra e riserva)."""
        if self.extra or self.riserva:
            return ""
        if soluzioni:
            return CARTELLA_SOLUZIONI
        modulo = self._per_aula(self.blocco, aula)
        if self.voce and self.voce.modulo != modulo:
            raise ValueError(f"{self.file}: blocco={modulo} ma il programma lo mette nel modulo {self.voce.modulo}")
        return cartella_modulo(modulo, self.voce.cartella if self.voce else "")

    def radice(self, aula: str, soluzioni: bool) -> str:
        """Il prefisso che dalla cartella del notebook porta alla cartella che contiene Dati/ e Schede/."""
        if self.extra:
            return "../"
        if self.riserva:
            return "../../"
        return "../" * len(self.cartella_rel(aula, soluzioni).split("/"))

    def _link(self, aula: str, soluzioni: bool, passo: int) -> str | None:
        voci = programma(aula)
        nums = [v.num for v in voci]
        if self.extra or self.num not in nums:
            return None
        i = nums.index(self.num) + passo
        if not 0 <= i < len(voci):
            return None
        v = voci[i]
        destinazione = relativo(self.cartella_rel(aula, soluzioni), posizione(v, soluzioni))
        etichetta = "Prossimo" if passo > 0 else "Precedente"
        return f"{etichetta}: [{_nome_link(v.num, v.titolo)}]({destinazione})"

    # ------------------------------------------------------------------ build
    def _link_prossimo(self, aula: str, soluzioni: bool = False) -> str | None:
        if self.prossimo is not None:
            return self.prossimo
        return self._link(aula, soluzioni, +1)

    def banner(self, aula: str, soluzioni: bool) -> str:
        """Testata piana: titolo, tempo e dati su una riga, i tre obiettivi. Modulo e aula stanno in chiusura."""
        obiettivi = self._per_aula(self.obiettivi, aula)
        dati = self._per_aula(self.dati, aula)
        tempo = self._per_aula(self.tempo, aula)
        titolo = f"{self.num} · {self.titolo}" if self.num[0].isdigit() else self.titolo
        if soluzioni and not self.extra:
            titolo += " · Soluzioni"
        testa = ["Extra · materiale per il docente"] if self.extra else []
        testa.append(f"⏱ ~{tempo} min")
        radice = self.radice(aula, soluzioni) + "Dati/"
        testa.append("Dati: " + (", ".join(f"`{radice}{d}`" for d in dati) if dati else "nessuno"))
        righe = [" &nbsp;·&nbsp; ".join(testa), "", "**In questo notebook impariamo a**", ""]
        righe += [f"- {o}" for o in obiettivi]
        return f'<a id="inizio"></a>\n# {titolo}\n\n' + "\n".join(righe)

    def _link_precedente(self, aula: str, soluzioni: bool = False) -> str | None:
        return self._link(aula, soluzioni, -1)

    def build(self, root: Path | str, aula: str, soluzioni: bool = False, lint: bool = True) -> Path:
        """Scrive il notebook. `root` è la radice dell'aula (Aula_Base, Aula_Avanzata), oppure la cartella stessa
        per Extra e riserva; la sottocartella la decide `cartella_rel`."""
        assert aula in AULE
        root = Path(root)
        prefisso = (self.num.lstrip("0") or "0") if self.prefisso_esercizi is None else self.prefisso_esercizi
        visibili = [c for c in self.celle if c.visibile(aula, soluzioni)]

        # numerazione di sezioni ed esercizi, calcolata per aula
        n_sez = 0
        n_sotto = 0
        n_es = 0
        indice: list[str] = []
        out: list[tuple[str, str, dict]] = []   # (tipo, src, metadata)
        ultimo_es = ""      # numero base dell'ultimo esercizio (per il "bis")
        corrente = ""       # numero dell'esercizio in corso (base o bis)
        n_dom = 0
        verifiche: dict[str, tuple[str, str]] = {}   # codice -> (etichetta, controllo) per corso.py
        soluzioni_reg: dict[str, tuple[str, str]] = {}   # codice -> (etichetta, sorgente) per soluzione("E1.3")
        for c in visibili:
            if c.tipo == "sezione":
                n_sez += 1
                n_sotto = 0
                anc = f"sez-{n_sez}"
                indice.append(f"- [{n_sez}. {c.extra['titolo']}](#{anc})")
                src = f'<a id="{anc}"></a>\n## {n_sez}. {c.extra["titolo"]}'
                if c.src:
                    src += "\n\n" + c.src
                out.append(("md", src, {"tags": ["sezione"]}))
            elif c.tipo == "sottosezione":
                n_sotto += 1
                anc = f"sez-{n_sez}-{n_sotto}"
                indice.append(f"    - [{n_sez}.{n_sotto} {c.extra['titolo']}](#{anc})")
                src = f'<a id="{anc}"></a>\n### {n_sez}.{n_sotto} {c.extra["titolo"]}'
                if c.src:
                    src += "\n\n" + c.src
                out.append(("md", src, {"tags": ["sottosezione"]}))
            elif c.tipo == "domanda":
                n_dom += 1
                corpo = f"**Domanda {n_dom}.** {c.src}\n\n" + _dettagli("Risposta", c.extra["risposta"])
                out.append(("md", corpo, {"tags": ["domanda"]}))
            elif c.tipo == "prova":
                corpo = f"**{BOX['esercizio'][0]} Hands-on**\n\n{c.src}"
                if c.extra.get("prova_anche"):
                    corpo += f"\n\n*Prova anche:* {c.extra['prova_anche']}"
                out.append(("md", _div(BOX["esercizio"][3], BOX["esercizio"][2], corpo), {"tags": ["prova-tu"]}))
                corrente = "Hands-on"
            elif c.tipo == "esercizio":
                e = c.extra
                if e["bis"]:
                    numero = f"{ultimo_es} bis"
                else:
                    n_es += 1
                    numero = f"{prefisso}.{n_es}" if prefisso else f"{n_es}"
                    ultimo_es = numero
                corrente = numero
                anc = "es-" + re.sub(r"[^a-z0-9]+", "-", numero.lower()).strip("-")
                testa = f"**{BOX['esercizio'][0]} {self.etichetta_esercizio} {numero} · {e['titolo']}**"
                corpo = [testa, ""]
                if e["bis"]:
                    primo = ultimo_es.split(".")[0]
                    articolo = "all'" if primo in ("1", "8", "11") else ("allo " if primo == "0" else "al ")
                    corpo += [f"*In alternativa {articolo}{ultimo_es}: stesso obiettivo, scenario diverso.*", ""]
                if e["scenario"]:
                    corpo += [e["scenario"], ""]
                if "\n" in e["richiesta"]:
                    corpo += [_dettagli("Passo per passo", e["richiesta"])]
                elif e["richiesta"]:
                    corpo += [e["richiesta"]]
                if e["suggerimento"]:
                    corpo += ["", "*Suggerimento:* " + e["suggerimento"]]
                for k, sugg in enumerate(e.get("suggerimenti", []), 1):
                    corpo += ["", _dettagli(f"Suggerimento {k}", sugg)]
                indice.append(f"    - [{self.etichetta_esercizio} {numero} · {e['titolo']}](#{anc})")
                out.append(("md", f'<a id="{anc}"></a>\n' + _div(BOX["esercizio"][3], BOX["esercizio"][2], "\n".join(corpo)), {"tags": ["esercizio"]}))
                c.extra["_numero"] = numero
            elif c.ruolo == "box-soluzione":
                perche = c.extra.get("perche")
                etichetta = "" if self.etichetta_esercizio == "Esercizio" else f"{self.etichetta_esercizio} "
                corpo = f"**{BOX['soluzione'][0]} Soluzione {etichetta}{corrente}**"
                if perche:
                    corpo += "\n\n" + perche
                out.append(("md", _div(BOX["soluzione"][3], BOX["soluzione"][2], corpo), {"tags": ["soluzione"]}))
            elif c.ruolo == "box-passo":
                corpo = f"**{BOX['esercizio'][0]} Un passo in più (facoltativo)**\n\n{c.extra['testo']}"
                out.append(("md", _div(BOX["esercizio"][3], BOX["esercizio"][2], corpo), {"tags": ["passo-in-piu"]}))
            elif c.tipo == "md":
                out.append(("md", c.src, {}))
            elif c.tipo == "code":
                src = c.src
                tags = []
                if c.ruolo == "verifica" and c.extra.get("prova"):
                    tags.append("verifica")
                    if not src.startswith("# Verifica"):
                        src = "# Verifica: esegui senza modificare\n" + src
                    if "✅" not in src:
                        src += '\nprint("✅ Tutto corretto")'
                elif c.ruolo == "rivela":
                    # la soluzione sta in corso.py, codificata; nel notebook resta la chiamata che la mostra
                    tags.append("rivela")
                    codice = corrente if self.etichetta_esercizio == "Esercizio" else f"{self.etichetta_esercizio} {corrente}"
                    soluzioni_reg[codice] = (f"{self.etichetta_esercizio} {corrente}", src.strip("\n"))
                    src = f'from corso import soluzione\nsoluzione("{codice}")   # mostra la soluzione di questo esercizio'
                elif c.ruolo == "verifica":
                    # il controllo sta in corso.py (generato da build.py); nel notebook resta la chiamata
                    tags.append("verifica")
                    codice = corrente if self.etichetta_esercizio == "Esercizio" else f"{self.etichetta_esercizio} {corrente}"
                    etichetta = f"{self.etichetta_esercizio} {corrente}"
                    if c.extra.get("passo"):
                        codice += " · passo"
                        etichetta += " · un passo in più"
                    while codice in verifiche:
                        codice += "+"
                    corpo = re.sub(r"^# Verifica[^\n]*\n", "", src)
                    corpo = re.sub(r'\nprint\("✅[^\n]*\)\s*$', "", corpo).strip("\n")
                    verifiche[codice] = (etichetta, corpo)
                    src = f'from corso import verifica\nverifica("{codice}")'
                elif c.ruolo:
                    tags.append(c.ruolo)
                if c.rete:
                    tags.append("rete")
                if c.errore:
                    tags.append("errore-voluto")
                if soluzioni and c.ruolo == "soluzione":
                    tags = [t for t in tags if t != "soluzione"] + ["soluzione"]
                out.append(("code", src, {"tags": tags} if tags else {}))

        self.verifiche = verifiche
        self.soluzioni = soluzioni_reg
        self.prefisso_verifiche = f"{prefisso}." if self.etichetta_esercizio == "Esercizio" else f"{self.etichetta_esercizio} "
        cells = [new_markdown_cell(self.banner(aula, soluzioni), metadata={"tags": ["banner"]})]
        if indice and len(out) >= INDICE_DA:
            cells.append(new_markdown_cell('<a id="indice"></a>\n**Indice**\n\n' + "\n".join(indice), metadata={"tags": ["indice"]}))
        for tipo, src, meta in out:
            if tipo == "md":
                cells.append(new_markdown_cell(src, metadata=meta))
            else:
                cells.append(new_code_cell(src, metadata=meta))
        if self.extra or self.fuori_programma:
            chiusura = "---\n\n**Fine.**"
        elif self.num == COMPITO[0]:
            chiusura = "---\n\n**Fine dell'homework.**"
        elif self.num.startswith("E"):
            chiusura = f"---\n\n**Fine dell'{self.titolo.lower()}.**"
        else:
            numero = f" {self.num}" if self.num[0].isdigit() else ""   # "S" e simili: notebook senza numero
            chiusura = f"---\n\n**Fine del notebook{numero}.**"
        link = [l for l in (self._link_precedente(aula, soluzioni), None if self.extra else self._link_prossimo(aula, soluzioni)) if l]
        if link:
            chiusura += " " + " &nbsp;·&nbsp; ".join(link)
        if not self.extra:
            meta = ["Approfondimenti: se la classe è avanti" if self.fuori_programma else NOMI_BLOCCO[self._per_aula(self.blocco, aula)]]
            meta.append(NOMI_AULA[aula])
            chiusura += "\n\n<sub>" + " · ".join(meta) + "</sub>"
        cells.append(new_markdown_cell(chiusura, metadata={"tags": ["chiusura"]}))

        # id deterministici e output vuoti
        for i, cell in enumerate(cells):
            cell["id"] = f"{self.num.lower()}-{aula}-{'sol' if soluzioni else 'stu'}-{i:03d}"
            if cell["cell_type"] == "code":
                cell["outputs"] = []
                cell["execution_count"] = None

        nb = new_notebook(cells=cells)
        nb.metadata["kernelspec"] = {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"}
        nb.metadata["language_info"] = {"name": "python", "version": "3.13", "pygments_lexer": "ipython3"}
        nb.metadata["corso"] = {"aula": aula, "numero": self.num, "soluzioni": soluzioni, "versione": VERSIONE,
                                "sorgente": f"_build/src/nb{self.num}_*.py"}

        if lint:
            errori, avvisi = lint_notebook(self, aula, cells)
            for a in avvisi:
                print(f"  [avviso] {self.file} ({aula}): {a}")
            if errori:
                raise ValueError(f"{self.file} ({aula}):\n  - " + "\n  - ".join(errori))

        out_path = root / self.cartella_rel(aula, soluzioni) / f"{self.file}.ipynb"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        nbformat.validate(nb)
        nbformat.write(nb, out_path)
        return out_path


# ---------------------------------------------------------------------------
# corso.py: il modulo con i controlli degli esercizi, uno per cartella di notebook
# ---------------------------------------------------------------------------
MODULO_CORSO = '''"""Controllo degli esercizi del corso. Il file è generato insieme ai notebook: non va modificato a mano.

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
        return [f"\\x1b[31m❌ {self}\\x1b[0m"]


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
    """Mostra la soluzione dell\'esercizio `codice`, e soltanto quella."""
    import base64

    if codice not in SOLUZIONI:
        raise VerificaFallita(f"Non c\'è una soluzione registrata per {codice!r}")
    etichetta, testo = SOLUZIONI[codice]
    sorgente = base64.b64decode(testo).decode("utf-8")
    try:
        from IPython.display import Code, display

        print(f"Soluzione · {etichetta}")
        display(Code(sorgente, language="python"))
    except ImportError:
        print(f"Soluzione · {etichetta}\\n\\n{sorgente}")


VERIFICHE = {
'''


def _letterale(testo: str) -> str:
    testo = testo.strip("\n")
    if "'''" not in testo and not testo.endswith("\\"):
        return "r'''\n" + testo + "\n'''"
    return repr(testo)


def leggi_modulo_corso(cartella: Path) -> tuple[dict[str, tuple[str, str]], dict[str, tuple[str, str]]]:
    """Le verifiche e le soluzioni già scritte in `cartella/corso.py` (vuote se il file non c'è)."""
    path = Path(cartella) / "corso.py"
    if not path.exists():
        return {}, {}
    spazio: dict = {}
    exec(path.read_text(encoding="utf-8"), spazio)
    return dict(spazio.get("VERIFICHE", {})), dict(spazio.get("SOLUZIONI", {}))


def scrivi_modulo_corso(cartella: Path, verifiche: dict[str, tuple[str, str]],
                        soluzioni: dict[str, tuple[str, str]] | None = None) -> Path:
    """`soluzioni` arriva come codice -> (etichetta, sorgente in chiaro) e viene scritto codificato in base64."""
    import base64

    righe = [MODULO_CORSO]
    for codice, (etichetta, controllo) in verifiche.items():
        righe.append(f"    {codice!r}: ({etichetta!r}, {_letterale(controllo)}),")
    righe.append("}\n")
    righe.append("# Le soluzioni degli esercizi che le mostrano a richiesta, codificate perché non si leggano per caso.")
    righe.append("SOLUZIONI = {")
    for codice, (etichetta, sorgente) in (soluzioni or {}).items():
        if not sorgente.startswith("B64:"):
            sorgente = "B64:" + base64.b64encode(sorgente.encode("utf-8")).decode("ascii")
        righe.append(f"    {codice!r}: ({etichetta!r}, {sorgente[4:]!r}),")
    righe.append("}\n")
    path = Path(cartella) / "corso.py"
    path.write_text("\n".join(righe), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Lint: errori bloccanti e avvisi
# ---------------------------------------------------------------------------
FRASI_VIETATE = [
    "come richiesto", "in questa versione", "per l'aula", "aula base", "aula avanzata",
    "questa sezione è pensata", "questo notebook è pensato", "versione del corso", "istruzioni del corso",
    "compito a casa", "compiti a casa",
    "il docente", "nucleo comune", "chi finisce prima", "chi ha finito", "la correzione finale",
]
TITOLI_SOSPETTI = ["davvero", "che serv", "che cont", "sul serio", "uno alla volta", "in cinque", "in sei", "senza paura", "che fanno la differenza"]
PAROLE_SOSPETTE = [
    "esploreremo", "fondamentale", "cruciale", "potente", "robusto", "sfruttare", "in sintesi",
    "ricapitolando", "vale la pena", "buon lavoro", "ottimo lavoro", "perfetto!", "immagina", "best practice",
    "nota bene", "vediamo insieme", "scopriamo insieme", "è importante notare", "da notare", "non solo",
    " ovvero ", "ecc.", "etc.", "e molto altro", "—",
    "formattatore", "formattatori", "apici invers", "codifica", "directory",
]


def lint_notebook(nb: Notebook, aula: str, cells: list) -> tuple[list[str], list[str]]:
    errori: list[str] = []
    avvisi: list[str] = []
    obiettivi = nb._per_aula(nb.obiettivi, aula)
    if len(obiettivi) != 3:
        errori.append(f"servono esattamente 3 obiettivi, trovati {len(obiettivi)}")
    md = [c for c in cells if c["cell_type"] == "markdown"]
    code = [c for c in cells if c["cell_type"] == "code"]
    testo = "\n".join(c["source"] for c in md[1:] if "chiusura" not in c["metadata"].get("tags", []))  # banner e chiusura esclusi
    basso = testo.lower()
    for f in FRASI_VIETATE:
        if f in basso:
            errori.append(f"frase vietata nel testo: {f!r}")
    for p in PAROLE_SOSPETTE:
        n = basso.count(p)
        if n:
            avvisi.append(f"parola da controllare {p.strip()!r} ({n})")
    tutto = testo + "\n" + "\n".join(c["source"] for c in code)
    for m in re.finditer(r"""["'(]\s*(?:\./)?Dati/""", tutto):
        errori.append(f"percorso dati non relativo alla cartella del notebook: usa {nb.radice(aula, False) + 'Dati/'!r} ({m.group(0)!r})")
    # celle di spiegazione troppo lunghe (escluse le celle con box, esercizi, banner, indice)
    for c in md:
        tags = c.get("metadata", {}).get("tags", [])
        if tags or c["source"].lstrip().startswith("<div") or c["source"].lstrip().startswith("<a id"):
            continue
        parole = len(c["source"].split())
        if parole > 110:
            avvisi.append(f"cella markdown lunga ({parole} parole): {c['source'][:50]!r}")
    for c in code:
        tags = c.get("metadata", {}).get("tags", [])
        righe = [r for r in c["source"].splitlines() if r.strip()]
        if not tags and len(righe) > 14:
            avvisi.append(f"cella di codice lunga ({len(righe)} righe): {righe[0][:50]!r}")
        if "!pip" in c["source"] or "%pip" in c["source"]:
            errori.append("niente !pip/%pip: le librerie si aggiungono con uv")
        if "inplace=True" in c["source"]:
            errori.append("niente inplace=True")
    # esclamativi fuori dalle verifiche
    for c in md[1:]:
        senza_codice = re.sub(r"`[^`]*`", "", c["source"])
        senza_codice = re.sub(r"```.*?```", "", senza_codice, flags=re.S)
        if "!" in senza_codice and "✅" not in c["source"] and "❌" not in c["source"]:
            avvisi.append(f"punto esclamativo nel testo: {c['source'][:50]!r}")
    # la sezione Esercizi deve essere l'ultima
    sezioni = [c["source"].splitlines()[1] for c in md if "sezione" in c.get("metadata", {}).get("tags", [])]
    for s in sezioni:
        for w in TITOLI_SOSPETTI:
            if w in s.lower():
                avvisi.append(f"titolo a effetto: {s!r}")
    for c in md:
        if "📌" in c["source"]:
            avvisi.append("box Ricorda: non si usa più")
    # stile (_build/docs/STILE.md): niente celle etichetta, niente frasi telegrafiche, niente "Output atteso:" secco
    for c in md:
        if "Output atteso:" in c["source"] or "*Output atteso*" in c["source"]:
            avvisi.append(f"'Output atteso:' va scritto come frase: {c['source'][:50]!r}")
    for c in md[1:]:
        tags = c.get("metadata", {}).get("tags", [])
        if set(tags) & {"indice", "chiusura", "esercizio", "prova-tu", "soluzione", "banner"}:
            continue
        src = c["source"]
        if "<div" in src or "<details" in src or src.lstrip().startswith("|") or src.lstrip().startswith(">"):
            continue
        corpo = re.sub(r"^<a id=[^\n]*\n", "", src)
        corpo = re.sub(r"^#+ .*$", "", corpo, flags=re.M)
        corpo = re.sub(r"```.*?```", "", corpo, flags=re.S).strip()
        if not corpo:
            continue
        parole = corpo.split()
        if len(parole) <= 4 and corpo.endswith(":"):
            errori.append(f"cella etichetta, va fusa in una frase (vedi _build/docs/STILE.md): {corpo!r}")
            continue
        righe = [r for r in corpo.splitlines() if r.strip()]
        elenco = sum(1 for r in righe if re.match(r"\s*([-*]|\**\d+\.\**)\s", r))
        if righe and elenco / len(righe) >= 0.5:
            continue
        frasi = [f for f in re.split(r"(?<=[.!?])\s+", corpo) if f.strip()]
        if len(frasi) >= 3 and len(parole) / len(frasi) < 8:
            avvisi.append(f"frasi telegrafiche ({len(frasi)} frasi, {len(parole) // len(frasi)} parole in media): {corpo[:60]!r}")
    # il capstone ha gli Step dentro ogni sezione, per scelta didattica
    if sezioni and not sezioni[-1].endswith(("Esercizi", "Extra")) and nb.num != COMPITO[0] and not nb.num.startswith("E") \
            and not nb.extra and nb.ha_soluzioni() and nb.etichetta_esercizio == "Esercizio":
        avvisi.append(f"l'ultima sezione non è 'Esercizi' ma {sezioni[-1]!r}")
    return errori, avvisi
