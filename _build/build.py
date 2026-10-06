"""
Costruisce i notebook del corso a partire dagli script in `_build/src/`.

    uv run python _build/build.py            # tutti
    uv run python _build/build.py 05 07      # solo quei numeri (C = homework, E1..E3 = esercitazioni, EXTRA = cartella Extra)

Output: Aula_Base/, Aula_Avanzata/ (versione studente) e Soluzioni_Base/, Soluzioni_Avanzata/.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = HERE / "src"
sys.path.insert(0, str(HERE))

CARTELLE = {
    ("base", False): ROOT / "Aula_Base",
    ("avanzata", False): ROOT / "Aula_Avanzata",
    ("base", True): ROOT / "Soluzioni_Base",
    ("avanzata", True): ROOT / "Soluzioni_Avanzata",
}


def carica(filtro: list[str]):
    for script in sorted(SRC.glob("nb*.py")):
        num = script.stem[2:].split("_")[0].upper()
        if filtro and num not in filtro:
            continue
        spec = importlib.util.spec_from_file_location(script.stem, script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        yield script.stem, mod.costruisci()


def carica_extra(filtro: list[str]):
    for script in sorted((SRC / "extra").glob("*.py")):
        if filtro and "EXTRA" not in filtro and script.stem.upper() not in filtro:
            continue
        spec = importlib.util.spec_from_file_location("extra_" + script.stem, script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        yield script.stem, mod.costruisci()


def main(argv: list[str]) -> int:
    filtro = [a.upper() for a in argv if not a.startswith("-")]
    rc = 0
    for stem, nb in carica_extra(filtro):
        try:
            out = nb.build(ROOT / "Extra", aula="avanzata", soluzioni=True)
            print(f"{stem:32s} -> {out.relative_to(ROOT)}")
        except ValueError as e:
            print(f"[ERRORE] {e}")
            rc = 1
    for stem, nb in carica(filtro):
        for aula in nb.aule:
            for soluzioni in (False, True):
                try:
                    out = nb.build(CARTELLE[(aula, soluzioni)], aula=aula, soluzioni=soluzioni)
                    print(f"{stem:32s} -> {out.relative_to(ROOT)}")
                except ValueError as e:
                    print(f"[ERRORE] {e}")
                    rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
