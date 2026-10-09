"""
Stampa un notebook generato cella per cella, come lo vede un corsista: il testo per intero, del codice la prima riga.

    uv run python _build/leggi.py Aula_Base/07_Pandas_operazioni.ipynb
    uv run python _build/leggi.py Aula_Base/07_Pandas_operazioni.ipynb --codice   # anche il codice per intero

Serve per la rilettura dopo una modifica: si legge l'output dall'inizio alla fine e si segnano le celle che non reggono.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def piano(src: str) -> str:
    src = re.sub(r'<a id="[^"]+"></a>\n?', "", src)
    src = re.sub(r"<div[^>]*>\n*", "", src)
    src = src.replace("\n\n</div>", "").replace("</div>", "")
    return src.strip()


def main(argv: list[str]) -> int:
    codice_intero = "--codice" in argv
    for path in [a for a in argv if not a.startswith("--")]:
        nb = json.loads(Path(path).read_text(encoding="utf-8"))
        print(f"===== {path} ({len(nb['cells'])} celle)\n")
        for i, c in enumerate(nb["cells"]):
            src = "".join(c["source"])
            tags = ",".join(c.get("metadata", {}).get("tags", []))
            if c["cell_type"] == "markdown":
                print(f"--- [{i}] testo {('(' + tags + ')') if tags else ''}\n{piano(src)}\n")
            else:
                righe = [r for r in src.splitlines() if r.strip()]
                mostra = "\n".join(righe) if codice_intero else (righe[0] + (f"   … (+{len(righe) - 1} righe)" if len(righe) > 1 else "") if righe else "")
                print(f"--- [{i}] codice {('(' + tags + ')') if tags else ''}\n{mostra}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
