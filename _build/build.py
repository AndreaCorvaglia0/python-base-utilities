"""
Costruisce tutti i notebook del corso a partire dagli script in `_build/src/`.

    uv run python _build/build.py            # costruisce tutto
    uv run python _build/build.py 04 05      # solo i notebook con quei numeri

Output:
    Aula_Base/<num>_<slug>.ipynb              versione studente, aula Base
    Aula_Base/Soluzioni/<num>_<slug>.ipynb    stesse celle + soluzioni degli esercizi
    Aula_Avanzata/...                          idem per l'aula Avanzata
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = HERE / "src"
sys.path.insert(0, str(HERE))

CARTELLE = {"base": ROOT / "Aula_Base", "avanzata": ROOT / "Aula_Avanzata"}


def carica_sorgenti(filtro: list[str]) -> list:
    notebooks = []
    for script in sorted(SRC.glob("nb*.py")):
        num = script.stem[2:4]
        if filtro and num not in filtro:
            continue
        spec = importlib.util.spec_from_file_location(script.stem, script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        nb = mod.costruisci()
        notebooks.append((script.stem, nb))
    return notebooks


def main(argv: list[str]) -> None:
    filtro = [a for a in argv if a.isdigit()]
    for stem, nb in carica_sorgenti(filtro):
        aule = getattr(nb, "aule", ("base", "avanzata"))
        for aula in aule:
            out = nb.build(CARTELLE[aula], aula=aula, soluzioni=False)
            nb.build(CARTELLE[aula] / "Soluzioni", aula=aula, soluzioni=True)
            print(f"{stem:28s} -> {out.relative_to(ROOT)} (+ Soluzioni)")


if __name__ == "__main__":
    main(sys.argv[1:])
