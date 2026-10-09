"""
Ciclo completo su uno o più notebook: build, soluzioni eseguite da capo a fondo, Run All della versione studente.

    uv run python _build/controlla.py 07            # un notebook
    uv run python _build/controlla.py 07 E2 A1      # più notebook (C = Homework, E1..E3, A1/A2, EXTRA)
    uv run python _build/controlla.py               # tutto

Esce con codice 1 se il build dà errori o avvisi, o se una validazione fallisce.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = [sys.executable]


def run(args: list[str]) -> tuple[int, str]:
    p = subprocess.run(PY + args, cwd=ROOT, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def main(argv: list[str]) -> int:
    filtro = [a.upper() for a in argv]
    rc, out = run(["_build/build.py", *filtro])
    righe = [r for r in out.splitlines() if "[ERRORE]" in r or "[avviso]" in r or r.startswith("  - ")]
    print(f"build: {'OK' if rc == 0 and not righe else 'PROBLEMI'}")
    for r in righe:
        print("  " + r)
    if rc != 0 or righe:
        return 1

    def seleziona(cartella: str) -> list[str]:
        files = sorted((ROOT / cartella).glob("*.ipynb"))
        if not filtro:
            return [str(f.relative_to(ROOT)) for f in files]
        scelti = []
        for f in files:
            stem = f.stem
            for n in filtro:
                if (n == "EXTRA" and cartella == "Extra") or stem.startswith(n + "_") or (n == "C" and stem == "Homework") \
                        or (n.startswith("E") and stem == f"Esercitazione_{n[1:]}") or (n.startswith("A") and stem == f"Approfondimenti_{n[1:]}"):
                    scelti.append(str(f.relative_to(ROOT)))
        return scelti

    soluzioni = seleziona("Soluzioni_Base") + seleziona("Soluzioni_Avanzata") + (seleziona("Extra") if not filtro or "EXTRA" in filtro else [])
    aula = seleziona("Aula_Base") + seleziona("Aula_Avanzata")
    esito = 0
    if soluzioni:
        rc, out = run(["_build/validate.py", *soluzioni])
        ok = [r for r in out.splitlines() if r.startswith("[OK ]")]
        print(f"soluzioni eseguite: {len(ok)}/{len(soluzioni)} OK")
        for r in out.splitlines():
            if r.startswith("[ERR]") or r.startswith("  cella"):
                print("  " + r)
        esito |= rc
    if aula:
        rc, out = run(["_build/check_studente.py", *aula])
        ok = [r for r in out.splitlines() if r.startswith("[OK ]")]
        print(f"versione studente (Run All): {len(ok)}/{len(aula)} OK")
        for r in out.splitlines():
            if r.startswith("[ERR]") or r.startswith("  cella"):
                print("  " + r)
        esito |= rc
    return 1 if esito else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
