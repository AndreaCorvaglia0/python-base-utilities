"""
Segnala nei file Markdown e nei notebook Jupyter i difetti di stile riconoscibili a macchina.

    python controlla_stile.py file.ipynb cartella/ README.md
    python controlla_stile.py --solo-errori cartella/

Controlla il testo, non il codice: blocchi ```...```, codice inline, tabelle e celle di codice vengono ignorati.
Esce con codice 1 se trova qualcosa. I risultati sono indizi da verificare rileggendo, non sentenze.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PAROLE_DA_BROCHURE = [
    "potent", "fondamentale", "cruciale", "incredibil", "straordinari", "rivoluzionari",
    "semplicissim", "magia", "magico", "davvero", "sul serio", "senza paura", "vale la pena", "è importante notare",
    "da notare che", "in sintesi", "ricapitolando", "esploreremo", "scopriamo insieme", "vediamo insieme",
    "immagina", "best practice", "game changer", "e molto altro",
]
CONNETTIVI = r"(perché|quindi|mentre|invece|cioè|infatti|poiché|dunque|per esempio|in questo modo)"


def pulisci(testo: str) -> str:
    testo = re.sub(r"```.*?```", "", testo, flags=re.S)
    testo = re.sub(r"`[^`]*`", "X", testo)
    testo = re.sub(r"<[^>]+>", "", testo)
    testo = re.sub(r"\[([^\]]*)\]\([^)]*\)", "LINK", testo)
    testo = testo.replace("&nbsp;", " ")
    return testo


def paragrafi(testo: str):
    """Restituisce (paragrafo, è_elenco) saltando titoli, tabelle e blocchi di codice."""
    testo = re.sub(r"```.*?```", "\n\n", testo, flags=re.S)
    for blocco in re.split(r"\n\s*\n", testo):
        righe = [r for r in blocco.splitlines() if r.strip()]
        righe = [r for r in righe if not r.lstrip().startswith("#")]
        if not righe or all(r.lstrip().startswith("|") for r in righe):
            continue
        righe = [re.sub(r"^\s*>\s?", "", r) for r in righe if not r.lstrip().startswith("|")]
        elenco = sum(1 for r in righe if re.match(r"\s*([-*+]|\**\d+[.)]\**)\s", r))
        yield " ".join(r.strip() for r in righe), bool(righe) and elenco / len(righe) >= 0.5


CONSEGNA = r"(?i)(domand|esercizio|prova tu|consegna|quiz|cosa fare)"


def controlla_testo(testo: str, consegna_cella: bool = False) -> list[str]:
    problemi = []
    if re.search(r"\*?Output atteso\*?:", testo):
        problemi.append("'Output atteso:' secco: scrivere il risultato come frase")
    for par, elenco in paragrafi(testo):
        p = pulisci(par).strip()
        p = re.sub(r"^\*{1,2}(Suggerimento|Nota|Attenzione|Cosa fare)[.:]?\*{1,2}:?\s*", "", p).strip()
        if not p:
            continue
        parole = [w for w in p.split() if w != "LINK" and re.search(r"\w", w)]
        corto = p[:90].replace("\n", " ")
        if len(parole) <= 4 and p.endswith(":"):
            problemi.append(f"riga etichetta, da fondere in una frase: {corto!r}")
            continue
        consegna = consegna_cella or bool(re.search(CONSEGNA, p))
        if not elenco:
            frasi = [f for f in re.split(r"(?<=[.!?])\s+", p) if f.strip()]
            if len(frasi) >= 3 and len(parole) / len(frasi) < 8:
                problemi.append(f"frasi telegrafiche ({len(frasi)} frasi, {len(parole) // len(frasi)} parole in media): {corto!r}")
            if p.count(":") >= 2 and 8 <= len(parole) < 50 and p.count("LINK") < 2 and not re.search(CONNETTIVI, p):
                problemi.append(f"catena di due punti senza connettivi: {corto!r}")
            if "?" in p and not consegna:
                problemi.append(f"domanda nel testo espositivo (retorica?): {corto!r}")
        if not consegna and re.search(r"(^|[.!?]\s+)(Qui|Ora|Poi) [a-zàèéìòù]", p):
            problemi.append(f"apertura con Qui/Ora/Poi: {corto!r}")
        if "!" in p and "✅" not in par and "❌" not in par:
            problemi.append(f"punto esclamativo: {corto!r}")
        basso = p.lower()
        for w in PAROLE_DA_BROCHURE:
            if w in basso:
                problemi.append(f"parola da brochure '{w}': {corto!r}")
    return problemi


def controlla_file(path: Path) -> list[str]:
    risultati = []
    if path.suffix == ".ipynb":
        nb = json.loads(path.read_text(encoding="utf-8"))
        for i, cella in enumerate(nb.get("cells", [])):
            if cella.get("cell_type") != "markdown":
                continue
            src = "".join(cella["source"]) if isinstance(cella["source"], list) else cella["source"]
            for p in controlla_testo(src, consegna_cella=bool(re.search(CONSEGNA, src))):
                risultati.append(f"{path}  cella {i}: {p}")
    else:
        for p in controlla_testo(path.read_text(encoding="utf-8")):
            risultati.append(f"{path}: {p}")
    return risultati


def main(argv: list[str]) -> int:
    percorsi = [Path(a) for a in argv if not a.startswith("--")]
    file = []
    for p in percorsi:
        if p.is_dir():
            file += sorted(x for x in p.rglob("*") if x.suffix in (".md", ".ipynb") and ".ipynb_checkpoints" not in x.parts)
        elif p.exists():
            file.append(p)
    tutti = []
    for f in file:
        tutti += controlla_file(f)
    for r in tutti:
        print(r)
    print(f"\n{len(file)} file controllati, {len(tutti)} segnalazioni.")
    return 1 if tutti else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
