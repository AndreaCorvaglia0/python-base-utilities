"""
Esegue i notebook e segnala le celle che vanno in errore.

    uv run python _build/validate.py Aula_Base/Soluzioni/*.ipynb
    uv run python _build/validate.py --rete Aula_Avanzata/Soluzioni/07_*.ipynb   # prova anche le celle di rete

Le celle taggate `rete` (chiamate ad API) vengono saltate, a meno di passare --rete.
La directory di lavoro è la cartella del notebook, come in VS Code.
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def esegui(path: Path, con_rete: bool) -> list[str]:
    nb = nbformat.read(path, as_version=4)
    if not con_rete:
        for cell in nb.cells:
            if cell.cell_type == "code" and "rete" in cell.metadata.get("tags", []):
                cell.source = "# (cella di rete saltata durante la validazione)\n" + "\n".join("# " + r for r in cell.source.splitlines())
    client = NotebookClient(nb, timeout=180, kernel_name="python3", allow_errors=True,
                            resources={"metadata": {"path": str(path.parent)}})
    client.execute()
    errori = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                errori.append(f"  cella {i}: {out.get('ename')}: {out.get('evalue')}\n    " + cell.source.splitlines()[0][:90])
    return errori


def main(argv: list[str]) -> int:
    con_rete = "--rete" in argv
    paths = [Path(a) for a in argv if not a.startswith("--")]
    rc = 0
    for p in paths:
        errori = esegui(p, con_rete)
        stato = "OK " if not errori else "ERR"
        print(f"[{stato}] {p}")
        for e in errori:
            print(e)
        rc |= bool(errori)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
