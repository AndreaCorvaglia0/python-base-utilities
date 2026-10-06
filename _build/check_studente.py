"""
Esegue i notebook della versione studente e segnala le celle di teoria che falliscono.

    uv run python _build/check_studente.py Aula_Base/*.ipynb

Nella versione studente gli esercizi hanno `...` al posto del codice, quindi le celle `starter`
e `verifica` possono fallire: è previsto. Non deve fallire nessun'altra cella: se succede, una
cella di spiegazione dipende da un esercizio non ancora svolto, e "Run All" si rompe in aula.
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ATTESI = {"starter", "verifica", "rete", "errore-voluto"}


def esegui(path: Path) -> list[str]:
    nb = nbformat.read(path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code" and "rete" in cell.metadata.get("tags", []):
            cell.source = "# (cella di rete saltata)\n" + "\n".join("# " + r for r in cell.source.splitlines())
    client = NotebookClient(nb, timeout=90, kernel_name="python3", allow_errors=True, interrupt_on_timeout=True,
                            resources={"metadata": {"path": str(path.parent)}})
    client.execute()
    problemi = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        tags = set(cell.metadata.get("tags", []))
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error" and out.get("ename") == "KeyboardInterrupt":
                problemi.append(f"  cella {i}: BLOCCATA oltre 90 secondi (ciclo infinito?)\n    {cell.source.splitlines()[0][:90]}")
        if tags & ATTESI:
            continue
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                problemi.append(f"  cella {i}: {out.get('ename')}: {str(out.get('evalue'))[:100]}\n    {cell.source.splitlines()[0][:90]}")
    return problemi


def main(argv: list[str]) -> int:
    rc = 0
    for p in map(Path, argv):
        problemi = esegui(p)
        print(f"[{'OK ' if not problemi else 'ERR'}] {p}")
        for e in problemi:
            print(e)
        rc |= bool(problemi)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
