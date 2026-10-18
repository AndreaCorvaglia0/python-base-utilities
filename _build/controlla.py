"""
Ciclo completo su uno o più notebook: build, soluzioni eseguite da capo a fondo, Run All della versione studente.

    uv run python _build/controlla.py 07            # un notebook
    uv run python _build/controlla.py 07 E2 A1      # più notebook (C = Homework, E1..E3, A1/A2, S, R, EXTRA)
    uv run python _build/controlla.py               # tutto

Oltre ai notebook controlla, a ogni giro, che le cartelle delle aule siano autosufficienti: le copie di dati e
file del progetto coincidono con gli originali, `uv.lock` dei corsisti è aggiornato, e gli script della demo e
dell'esercizio su uv e Ruff danno gli avvisi previsti all'inizio e nessuno alla fine.

Esce con codice 1 se il build dà errori o avvisi, o se una validazione fallisce.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = [sys.executable]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from statici import AULA_SRC, CARTELLE_AULA, SCRIPT_UV, SCRIPT_UV_SRC, differenze  # noqa: E402

# gli avvisi di Ruff che gli script della demo e dell'esercizio devono dare prima della pulizia (Guida, notebook S
# ed Esercitazione 1 Avanzata li citano): codice -> file
AVVISI_INIZIALI = {
    "demo": {("I001", "main.py"), ("E501", "main.py"), ("F401", "calcoli.py"), ("F841", "calcoli.py")},
    "esercizio": {("I001", "main.py"), ("E501", "main.py"), ("F401", "meteo.py"), ("F841", "meteo.py")},
}


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
        files = sorted(f for f in (ROOT / cartella).rglob("*.ipynb") if ".venv" not in f.parts and ".ipynb_checkpoints" not in f.parts)
        if not filtro:
            return [f.relative_to(ROOT).as_posix() for f in files]
        scelti = []
        for f in files:
            numero = json.loads(f.read_text(encoding="utf-8"))["metadata"].get("corso", {}).get("numero", "")
            if any(n == numero.upper() or (n == "EXTRA" and cartella == "Extra") for n in filtro):
                scelti.append(f.relative_to(ROOT).as_posix())
        return scelti

    aule = [c.name for c in CARTELLE_AULA.values()]
    soluzioni = [f for a in aule for f in seleziona(f"{a}/Soluzioni")]
    soluzioni += seleziona("Extra") if not filtro or "EXTRA" in filtro else []
    riserva = seleziona("Riserva/Base") + seleziona("Riserva/Avanzata")
    soluzioni += [f for f in riserva if f.endswith("_Soluzioni.ipynb")]
    aula = [f for a in aule for f in seleziona(a) if not f.startswith(f"{a}/Soluzioni/")]
    aula += [f for f in riserva if not f.endswith("_Soluzioni.ipynb")]
    esito = controlla_cartelle()
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


def controlla_cartelle() -> int:
    """Copie identiche agli originali, lock aggiornati, punto di partenza della demo intatto, avvisi di Ruff previsti."""
    problemi = differenze()
    for cartella in [AULA_SRC] + [SCRIPT_UV_SRC / "soluzioni" / d for d in ("demo", "esercizio")]:
        p = subprocess.run(["uv", "lock", "--check", "--offline"], cwd=cartella, capture_output=True, text=True)
        if p.returncode != 0:
            dettaglio = (p.stderr.strip().splitlines() or [""])[-1]
            problemi.append(f"{cartella.relative_to(ROOT)}/uv.lock non è aggiornato: lancia `uv lock` lì ({dettaglio})")
    for d in ("demo", "esercizio"):     # il punto di partenza: nessuna libreria, nessun lock
        progetto = tomllib.loads((SCRIPT_UV_SRC / d / "pyproject.toml").read_text(encoding="utf-8"))
        if progetto["project"].get("dependencies") or "dependency-groups" in progetto or (SCRIPT_UV_SRC / d / "uv.lock").exists():
            problemi.append(f"_build/src/script_uv_ruff/{d}: il punto di partenza ha già librerie o un uv.lock")
    avanzata = CARTELLE_AULA["avanzata"]
    for dst, src in SCRIPT_UV.items():
        cartella = avanzata / dst
        attesi = set() if src.startswith("soluzioni/") else AVVISI_INIZIALI[src]
        problemi += _avvisi_ruff(cartella, dst, attesi)
        if src.startswith("soluzioni/"):
            p = subprocess.run(PY + ["-m", "ruff", "format", "--check", "--no-cache", "."], cwd=cartella, capture_output=True, text=True)
            if p.returncode != 0:
                problemi.append(f"{dst}: ruff format cambierebbe qualcosa")
        else:
            # i notebook S ed E1 fanno lanciare `ruff format` prima di `ruff check`: anche dopo, gli avvisi sono quelli
            with tempfile.TemporaryDirectory() as tmp:
                copia = Path(tmp) / Path(dst).name
                shutil.copytree(cartella, copia, ignore=shutil.ignore_patterns(".venv", "__pycache__", ".ruff_cache"))
                subprocess.run(PY + ["-m", "ruff", "format", "--no-cache", "."], cwd=copia, capture_output=True)
                problemi += _avvisi_ruff(copia, f"{dst} dopo ruff format", attesi)
    print(f"cartelle delle aule: {'OK' if not problemi else 'PROBLEMI'}")
    for r in problemi:
        print("  " + r)
    return 1 if problemi else 0


def _avvisi_ruff(cartella: Path, nome: str, attesi: set) -> list[str]:
    p = subprocess.run(PY + ["-m", "ruff", "check", "--no-cache", "--output-format", "json", "."],
                       cwd=cartella, capture_output=True, text=True)
    if p.returncode not in (0, 1):
        return [f"{nome}: Ruff non è partito ({p.stderr.strip()[:200]})"]
    trovati = {(a["code"], Path(a["filename"]).name) for a in json.loads(p.stdout)}
    return [] if trovati == attesi else [f"{nome}: Ruff dà {sorted(trovati)}, attesi {sorted(attesi)}"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
