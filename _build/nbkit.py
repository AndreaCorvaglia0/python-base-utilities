"""
nbkit: piccolo generatore di notebook per il corso.

Ogni notebook del corso è descritto da uno script Python in `_build/src/` che usa
questa libreria. Dallo stesso sorgente si ottengono:

- la versione per l'Aula Base e quella per l'Aula Avanzata (celle taggate);
- la versione "studente" (esercizi da completare) e quella "soluzioni".

Uso tipico (vedi gli script in src/):

    from nbkit import Notebook
    nb = Notebook(num="04", slug="Condizioni_cicli_funzioni", titolo="...", ...)
    nb.md("## 1. ...")
    nb.code("x = 4")
    nb.box("nota", "testo in markdown")
    nb.esercizio(id="1", titolo="...", scenario="...", richiesta="...", starter="...", soluzione="...", verifica="...")
    nb.build(root, aula="base", soluzioni=False)
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

# ---------------------------------------------------------------------------
# Sistema visivo (colori e HTML dei box). Un posto solo: cambiare qui cambia tutto.
# ---------------------------------------------------------------------------

COLORI = {
    "esercizio": "#5cb85c",      # verde
    "soluzione": "#20a8a0",      # verde acqua
    "nota": "#6c8ebf",           # azzurro
    "attenzione": "#d9534f",     # rosso
    "approfondimento": "#8e6bbf",  # viola
    "ricorda": "#f0ad4e",        # ambra
    "banner": "#9b1b5a",         # magenta (richiama le slide)
}

TITOLI_BOX = {
    "nota": "📘 Nota",
    "attenzione": "⚠️ Attenzione",
    "approfondimento": "🔍 Approfondimento (si può saltare)",
    "ricorda": "📌 Da ricordare",
    "esercizio": "✏️ Esercizio",
    "soluzione": "✅ Soluzione",
}

NOMI_BLOCCO = {
    1: "Blocco 1 · Setup, Python e sintassi di base",
    2: "Blocco 2 · Controllo del flusso, funzioni e primi dati in pandas",
    3: "Blocco 3 · Analisi dei dati con pandas e visualizzazione",
    4: "Blocco 4 · Agenti per il coding e caso d'uso end-to-end",
    0: "Compito a casa",
}

NOMI_AULA = {"base": "Aula Base", "avanzata": "Aula Avanzata"}


def _rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def box_html(tipo: str, corpo: str, titolo: str | None = None) -> str:
    """Box colorato leggibile in tema chiaro e scuro (sfondo trasparente, niente color forzato)."""
    colore = COLORI[tipo]
    titolo = titolo or TITOLI_BOX[tipo]
    corpo = textwrap.dedent(corpo).strip()
    return (
        f'<div style="background-color:{_rgba(colore, 0.10)}; border-left:4px solid {colore}; '
        f'padding:12px 14px; border-radius:4px; margin:8px 0;">\n\n'
        f"**{titolo}**\n\n{corpo}\n\n</div>"
    )


def banner_html(
    num: str,
    titolo: str,
    blocco: int,
    giornata: int,
    aula: str,
    obiettivi: list[str],
    tempo: int,
    prerequisito: str | None,
) -> str:
    colore = COLORI["banner"]
    obiettivi_md = "\n".join(f"- {o}" for o in obiettivi)
    riga_blocco = NOMI_BLOCCO.get(blocco, "")
    sotto = f"{riga_blocco} · Giornata {giornata} · {NOMI_AULA[aula]}" if giornata else f"{riga_blocco} · {NOMI_AULA[aula]}"
    pre = f"\n\n*Prima di questo notebook:* {prerequisito}" if prerequisito else ""
    return (
        f'<div style="border-left:6px solid {colore}; padding:14px 18px; margin:4px 0 12px 0; '
        f'background-color:{_rgba(colore, 0.06)}; border-radius:4px;">\n\n'
        f"# {num} · {titolo}\n\n"
        f"**{sotto}** · ⏱ circa {tempo} min\n\n"
        f"**Alla fine di questo notebook sappiamo:**\n\n{obiettivi_md}{pre}\n\n</div>"
    )


# ---------------------------------------------------------------------------
# Modello delle celle
# ---------------------------------------------------------------------------

AULE = ("base", "avanzata")


@dataclass
class Cella:
    tipo: str                 # "md" | "code"
    src: str
    aula: str | None = None   # None = entrambe, "base" | "avanzata" = solo quella
    solo_soluzioni: bool = False   # cella che compare solo nella versione soluzioni
    solo_studente: bool = False    # cella che compare solo nella versione studente
    rete: bool = False        # cella che usa la rete (il validatore la ignora se fallisce)
    tags: list[str] = field(default_factory=list)

    def visibile(self, aula: str, soluzioni: bool) -> bool:
        if self.aula is not None and self.aula != aula:
            return False
        if self.solo_soluzioni and not soluzioni:
            return False
        if self.solo_studente and soluzioni:
            return False
        return True


@dataclass
class Notebook:
    num: str
    slug: str
    titolo: str
    blocco: int
    giornata: int
    obiettivi: list[str]
    tempo: int | dict[str, int] = 45
    prerequisito: str | None = None
    successivo: str | None = None
    celle: list[Cella] = field(default_factory=list)
    _n_esercizi: int = 0

    # --- celle semplici ---------------------------------------------------
    def md(self, testo: str, aula: str | None = None, **kw) -> None:
        self.celle.append(Cella("md", textwrap.dedent(testo).strip("\n"), aula=aula, **kw))

    def code(self, src: str, aula: str | None = None, rete: bool = False, **kw) -> None:
        self.celle.append(Cella("code", textwrap.dedent(src).strip("\n"), aula=aula, rete=rete, **kw))

    def box(self, tipo: str, testo: str, titolo: str | None = None, aula: str | None = None) -> None:
        self.md(box_html(tipo, testo, titolo), aula=aula)

    # --- esercizi -----------------------------------------------------------
    def sezione_esercizi(self, intro: str | None = None, aula: str | None = None) -> None:
        testo = '<a id="esercizi"></a>\n## Esercizi'
        if intro:
            testo += "\n\n" + textwrap.dedent(intro).strip()
        self.md(testo, aula=aula)

    def esercizio(
        self,
        id: str,
        titolo: str,
        scenario: str,
        richiesta: str,
        starter: str,
        soluzione: str,
        verifica: str | None = None,
        suggerimento: str | None = None,
        tipo: str = "base",       # "base" | "passo" (un passo in più) | "alternativo"
        aula: str | None = None,
        rete: bool = False,
        nota_soluzione: str | None = None,
    ) -> None:
        etichetta = {"base": "Esercizio", "passo": "Esercizio · un passo in più", "alternativo": "Esercizio alternativo"}[tipo]
        intest = f"✏️ {etichetta} {id} · {titolo}"
        corpo = textwrap.dedent(scenario).strip() + "\n\n**Cosa fare.** " + textwrap.dedent(richiesta).strip()
        if suggerimento:
            corpo += "\n\n*Suggerimento:* " + textwrap.dedent(suggerimento).strip()
        self.md(box_html("esercizio", corpo, titolo=intest), aula=aula)
        # versione studente: scheletro da completare
        self.celle.append(Cella("code", textwrap.dedent(starter).strip("\n"), aula=aula, solo_studente=True, rete=rete))
        # versione soluzioni: box + codice completo
        testo_sol = nota_soluzione or ""
        self.celle.append(Cella("md", box_html("soluzione", testo_sol or f"Esercizio {id} · {titolo}"), aula=aula, solo_soluzioni=True))
        self.celle.append(Cella("code", textwrap.dedent(soluzione).strip("\n"), aula=aula, solo_soluzioni=True, rete=rete))
        if verifica:
            self.celle.append(Cella("code", textwrap.dedent(verifica).strip("\n"), aula=aula, rete=rete, tags=["verifica"]))
        self._n_esercizi += 1

    # --- costruzione ----------------------------------------------------------
    def _tempo(self, aula: str) -> int:
        return self.tempo[aula] if isinstance(self.tempo, dict) else self.tempo

    def nome_file(self) -> str:
        return f"{self.num}_{self.slug}.ipynb"

    def build(self, root: Path | str, aula: str, soluzioni: bool = False) -> Path:
        assert aula in AULE
        root = Path(root)
        cells = []
        banner = banner_html(
            self.num, self.titolo + (" · Soluzioni" if soluzioni else ""), self.blocco, self.giornata,
            aula, self.obiettivi, self._tempo(aula), self.prerequisito,
        )
        cells.append(new_markdown_cell(banner))
        for c in self.celle:
            if not c.visibile(aula, soluzioni):
                continue
            if c.tipo == "md":
                cells.append(new_markdown_cell(c.src))
            else:
                meta = {"tags": c.tags + (["rete"] if c.rete else [])} if (c.tags or c.rete) else {}
                cells.append(new_code_cell(c.src, metadata=meta))
        if self.successivo:
            cells.append(new_markdown_cell(f"---\n\n➡️ Prossimo notebook: **{self.successivo}**"))
        nb = new_notebook(cells=cells)
        nb.metadata["kernelspec"] = {"display_name": "Python 3 (.venv)", "language": "python", "name": "python3"}
        nb.metadata["language_info"] = {"name": "python"}
        out = root / self.nome_file()
        out.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(nb, out)
        return out


# ---------------------------------------------------------------------------
# Indice automatico: costruito dai titoli ## e ### presenti nelle celle markdown
# ---------------------------------------------------------------------------

def slug_ancora(titolo: str) -> str:
    s = titolo.lower()
    s = re.sub(r"[`*_]", "", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def indice_da_celle(celle: list[Cella], aula: str) -> str:
    righe = []
    for c in celle:
        if c.tipo != "md" or (c.aula is not None and c.aula != aula) or c.solo_soluzioni:
            continue
        for line in c.src.splitlines():
            m = re.match(r"^(##|###)\s+(.*)$", line)
            if m:
                livello, titolo = m.group(1), m.group(2).strip()
                indent = "" if livello == "##" else "    "
                righe.append(f"{indent}- [{titolo}](#{slug_ancora(titolo)})")
    return "**Indice**\n\n" + "\n".join(righe)
