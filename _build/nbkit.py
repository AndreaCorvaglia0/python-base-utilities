"""
nbkit: il generatore dei notebook del corso.

Ogni notebook è descritto da uno script in `_build/src/` che espone una funzione `costruisci()`
e restituisce un `Notebook`. Dallo stesso sorgente si ottengono quattro file:

    Aula_Base/NN_Titolo.ipynb          Aula_Avanzata/NN_Titolo.ipynb
    Soluzioni_Base/NN_Titolo.ipynb     Soluzioni_Avanzata/NN_Titolo.ipynb

Uso tipico:

    from nbkit import Notebook

    def costruisci():
        nb = Notebook(num="05", file="05_Condizioni_cicli_funzioni", titolo="Condizioni, cicli e funzioni",
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
# Programma: numero -> (file, titolo). Serve per i link "prossimo notebook".
# ---------------------------------------------------------------------------
PROGRAMMA = [
    ("00", "00_Si_parte", "Si parte: VS Code, notebook e primo codice"),
    ("01", "01_Librerie_e_ambiente", "Librerie e ambiente"),
    ("02", "02_Sintassi_di_base", "Sintassi di base: variabili, numeri e stringhe"),
    ("03", "03_Strutture_dati", "Strutture dati: liste, tuple, dizionari e set"),
    ("04", "04_Codice_leggibile", "Codice leggibile"),
    ("05", "05_Condizioni_cicli_funzioni", "Condizioni, cicli e funzioni"),
    ("06", "06_Oggetti_ed_errori", "Oggetti ed errori"),
    ("07", "07_Pandas_import_dati", "pandas: DataFrame e import dei dati"),
    ("08", "08_Pandas_operazioni", "pandas: operazioni sui DataFrame"),
    ("09", "09_Pandas_date", "pandas: le date"),
    ("10", "10_Plotly", "Grafici con Plotly"),
    ("11", "11_Agenti_per_il_coding", "Agenti per il coding"),
    ("12", "12_Capstone", "Capstone: il carico del Nord e la temperatura"),
]
COMPITO = ("C", "Compito_a_casa", "Compito a casa")

NOMI_BLOCCO = {
    1: "Blocco 1 · Setup, Python e sintassi di base",
    2: "Blocco 2 · Controllo del flusso, funzioni e primi dati in pandas",
    3: "Blocco 3 · Analisi dei dati con pandas e visualizzazione",
    4: "Blocco 4 · Agenti per il coding e caso d'uso end-to-end",
    0: "Tra le due giornate",
}

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
BANNER_BORDO, BANNER_SFONDO = "#607d8b", "rgba(96,125,139,0.08)"


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
    blocco: int
    giornata: int
    intento: str
    obiettivi: list[str] | dict[str, list[str]]
    tempo: int | dict[str, int] = 45
    dati: list[str] | dict[str, list[str]] = field(default_factory=list)
    aule: tuple[str, ...] = AULE
    etichetta_esercizio: str = "Esercizio"
    prefisso_esercizi: str | None = None     # default: num
    prossimo: str | None = None              # testo markdown della chiusura, se diverso dal programma
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

    def md(self, testo: str, aula: str | None = None) -> None:
        self.celle.append(Cella("md", _d(testo), aula=self._aula(aula)))

    def code(self, src: str, aula: str | None = None, rete: bool = False, errore: bool = False) -> None:
        """Cella di codice. rete=True se chiama un'API; errore=True se deve dare errore apposta."""
        self.celle.append(Cella("code", _d(src), aula=self._aula(aula), rete=rete, errore=errore))

    def box(self, tipo: str, testo: str, titolo: str | None = None, aula: str | None = None) -> None:
        if tipo not in ("nota", "attenzione", "approfondimento", "ricorda"):
            raise ValueError(f"box: tipo non previsto {tipo!r}")
        self.celle.append(Cella("md", box_html(tipo, testo, titolo), aula=self._aula(aula)))

    def prova_tu(self, richiesta: str, starter: str, soluzione: str, verifica: str | None = None,
                 aula: str | None = None, rete: bool = False) -> None:
        """Micro-esercizio inline da 2-3 minuti: box verde, cella da completare, verifica."""
        a = self._aula(aula)
        self.celle.append(Cella("prova", _d(richiesta), aula=a))
        self.celle.append(Cella("code", _d(starter), aula=a, solo_studente=True, rete=rete, ruolo="starter"))
        self.celle.append(Cella("code", _d(soluzione), aula=a, solo_soluzioni=True, rete=rete, ruolo="soluzione"))
        if verifica:
            self.celle.append(Cella("code", _d(verifica), aula=a, rete=rete, ruolo="verifica", extra={"prova": True}))

    def esercizio(self, titolo: str, scenario: str, richiesta: str, starter: str, soluzione: str,
                  verifica: str | None = None, suggerimento: str | None = None, perche: str | None = None,
                  bis: bool = False, passo_in_piu: dict | None = None, aula: str | None = None,
                  rete: bool = False) -> None:
        """Esercizio di fine notebook: box verde, starter, verifica (+ soluzione nelle Soluzioni).

        passo_in_piu: dict(testo=..., starter=..., soluzione=..., verifica=...) facoltativo.
        bis=True: è l'alternativa dell'esercizio precedente (stesso numero + "bis").
        """
        a = self._aula(aula)
        self.celle.append(Cella("esercizio", "", aula=a, extra={
            "titolo": titolo, "scenario": _d(scenario), "richiesta": _d(richiesta),
            "suggerimento": _d(suggerimento) if suggerimento else None, "bis": bis,
            "passo": _d(passo_in_piu["testo"]) if passo_in_piu else None, "perche": _d(perche) if perche else None,
        }))
        self.celle.append(Cella("code", _d(starter), aula=a, solo_studente=True, rete=rete, ruolo="starter"))
        self.celle.append(Cella("md", "", aula=a, solo_soluzioni=True, ruolo="box-soluzione", extra={"perche": _d(perche) if perche else None}))
        self.celle.append(Cella("code", _d(soluzione), aula=a, solo_soluzioni=True, rete=rete, ruolo="soluzione"))
        if verifica:
            self.celle.append(Cella("code", _d(verifica), aula=a, rete=rete, ruolo="verifica"))
        if passo_in_piu:
            self.celle.append(Cella("md", "", aula=a, ruolo="box-passo", extra={"testo": _d(passo_in_piu["testo"])}))
            self.celle.append(Cella("code", _d(passo_in_piu["starter"]), aula=a, solo_studente=True, rete=rete, ruolo="starter"))
            self.celle.append(Cella("code", _d(passo_in_piu["soluzione"]), aula=a, solo_soluzioni=True, rete=rete, ruolo="soluzione"))
            if passo_in_piu.get("verifica"):
                self.celle.append(Cella("code", _d(passo_in_piu["verifica"]), aula=a, rete=rete, ruolo="verifica", extra={"passo": True}))

    # ------------------------------------------------------------------ build
    def _per_aula(self, valore, aula: str):
        return valore[aula] if isinstance(valore, dict) else valore

    def _link_prossimo(self) -> str | None:
        if self.prossimo is not None:
            return self.prossimo
        nums = [p[0] for p in PROGRAMMA]
        if self.num not in nums:
            return None
        i = nums.index(self.num)
        if i + 1 >= len(PROGRAMMA):
            return None
        n, f, t = PROGRAMMA[i + 1]
        testo = f"Prossimo: [{n} · {t}]({f}.ipynb)"
        if self.num == "07":
            testo += f" · e, prima della seconda giornata, il [{COMPITO[2]}]({COMPITO[1]}.ipynb)"
        return testo

    def banner(self, aula: str, soluzioni: bool) -> str:
        obiettivi = self._per_aula(self.obiettivi, aula)
        dati = self._per_aula(self.dati, aula)
        tempo = self._per_aula(self.tempo, aula)
        titolo = f"{self.num} · {self.titolo}" if self.num != COMPITO[0] else self.titolo
        if soluzioni:
            titolo += " · Soluzioni"
        kicker = NOMI_BLOCCO[self.blocco]
        if self.giornata:
            kicker += f" · Giornata {self.giornata}"
        kicker += f" · {NOMI_AULA[aula]} &nbsp;·&nbsp; ⏱ ~{tempo} min"
        righe = [f"**{kicker}**", "", self.intento, "", "**In questo notebook impariamo a**", ""]
        righe += [f"- {o}" for o in obiettivi]
        pre = []
        nums = [p[0] for p in PROGRAMMA]
        if self.num in nums and nums.index(self.num) > 0:
            n, f, t = PROGRAMMA[nums.index(self.num) - 1]
            pre.append(f"Prima di questo: [{n} · {t}]({f}.ipynb)")
        pre.append("Dati: " + (", ".join(f"`../Dati/{d}`" for d in dati) if dati else "nessuno"))
        righe += ["", " &nbsp;·&nbsp; ".join(pre)]
        return f'<a id="inizio"></a>\n# {titolo}\n\n' + _div(BANNER_SFONDO, BANNER_BORDO, "\n".join(righe), padding="12px 16px")

    def build(self, root: Path | str, aula: str, soluzioni: bool = False, lint: bool = True) -> Path:
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
            elif c.tipo == "prova":
                corpo = f"**{BOX['esercizio'][0]} Prova tu**\n\n{c.src}"
                out.append(("md", _div(BOX["esercizio"][3], BOX["esercizio"][2], corpo), {"tags": ["prova-tu"]}))
                corrente = "Prova tu"
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
                    articolo = "all'" if ultimo_es.split(".")[0] in ("1", "8", "11") else "al "
                    corpo += [f"*In alternativa {articolo}{ultimo_es}: stesso obiettivo, scenario diverso.*", ""]
                if "\n" in e["richiesta"]:
                    corpo += [e["scenario"], "", "**Cosa fare.**", "", e["richiesta"]]
                else:
                    corpo += [e["scenario"], "", "**Cosa fare.** " + e["richiesta"]]
                if e["suggerimento"]:
                    corpo += ["", "*Suggerimento:* " + e["suggerimento"]]
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
                if c.ruolo == "verifica":
                    tags.append("verifica")
                    if not src.startswith("# Verifica"):
                        src = "# Verifica: esegui senza modificare\n" + src
                    if "✅" not in src:
                        cosa = "Prova tu" if c.extra.get("prova") else f"{self.etichetta_esercizio} {corrente}"
                        if c.extra.get("passo"):
                            cosa += " · un passo in più"
                        src += f'\nprint("✅ {cosa} completato")' if cosa != "Prova tu" else '\nprint("✅ Tutto corretto")'
                elif c.ruolo:
                    tags.append(c.ruolo)
                if c.rete:
                    tags.append("rete")
                if c.errore:
                    tags.append("errore-voluto")
                if soluzioni and c.ruolo == "soluzione":
                    tags = [t for t in tags if t != "soluzione"] + ["soluzione"]
                out.append(("code", src, {"tags": tags} if tags else {}))

        cells = [new_markdown_cell(self.banner(aula, soluzioni), metadata={"tags": ["banner"]})]
        if indice:
            cells.append(new_markdown_cell('<a id="indice"></a>\n**Indice**\n\n' + "\n".join(indice), metadata={"tags": ["indice"]}))
        for tipo, src, meta in out:
            if tipo == "md":
                cells.append(new_markdown_cell(src, metadata=meta))
            else:
                cells.append(new_code_cell(src, metadata=meta))
        chiusura = f"---\n\n**Fine del notebook {self.num}.**" if self.num != COMPITO[0] else "---\n\n**Fine del compito.**"
        link = self._link_prossimo()
        if link:
            chiusura += " " + link
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
                                "sorgente": f"_build/src/nb{self.num.lower()}_*.py"}

        if lint:
            errori, avvisi = lint_notebook(self, aula, cells)
            for a in avvisi:
                print(f"  [avviso] {self.file} ({aula}): {a}")
            if errori:
                raise ValueError(f"{self.file} ({aula}):\n  - " + "\n  - ".join(errori))

        out_path = root / f"{self.file}.ipynb"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        nbformat.validate(nb)
        nbformat.write(nb, out_path)
        return out_path


# ---------------------------------------------------------------------------
# Lint: errori bloccanti e avvisi
# ---------------------------------------------------------------------------
FRASI_VIETATE = [
    "come richiesto", "in questa versione", "per l'aula", "aula base", "aula avanzata",
    "questa sezione è pensata", "questo notebook è pensato", "versione del corso", "istruzioni del corso",
]
PAROLE_SOSPETTE = [
    "esploreremo", "fondamentale", "cruciale", "potente", "robusto", "sfruttare", "in sintesi",
    "ricapitolando", "vale la pena", "buon lavoro", "ottimo lavoro", "perfetto!", "immagina", "best practice",
    "nota bene", "vediamo insieme", "scopriamo insieme", "è importante notare", "da notare", "non solo",
    " ovvero ", "ecc.", "etc.", "e molto altro", "—",
]


def lint_notebook(nb: Notebook, aula: str, cells: list) -> tuple[list[str], list[str]]:
    errori: list[str] = []
    avvisi: list[str] = []
    obiettivi = nb._per_aula(nb.obiettivi, aula)
    if len(obiettivi) != 3:
        errori.append(f"servono esattamente 3 obiettivi, trovati {len(obiettivi)}")
    md = [c for c in cells if c["cell_type"] == "markdown"]
    code = [c for c in cells if c["cell_type"] == "code"]
    testo = "\n".join(c["source"] for c in md[1:])  # banner escluso
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
        errori.append(f"percorso dati non relativo alla cartella del notebook: usa '../Dati/' ({m.group(0)!r})")
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
    if sezioni and not sezioni[-1].endswith("Esercizi") and nb.num != COMPITO[0]:
        avvisi.append(f"l'ultima sezione non è 'Esercizi' ma {sezioni[-1]!r}")
    return errori, avvisi
