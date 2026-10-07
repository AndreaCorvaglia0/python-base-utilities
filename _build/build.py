"""
Costruisce i notebook del corso a partire dagli script in `_build/src/`.

    uv run python _build/build.py            # tutti
    uv run python _build/build.py 05 07      # solo quei numeri (C = homework, E1..E3 = esercitazioni, EXTRA = cartella Extra)

Output: Aula_Base/, Aula_Avanzata/ (versione studente) e Soluzioni_Base/, Soluzioni_Avanzata/, più Extra/.
In ogni cartella scrive anche `corso.py`, il modulo con i controlli degli esercizi (`verifica("7.1")`).
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = HERE / "src"
sys.path.insert(0, str(HERE))

from nbkit import leggi_modulo_corso, scrivi_modulo_corso  # noqa: E402

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
    # cartella -> {codice: (etichetta, controllo)}: i controlli degli esercizi, poi scritti in corso.py
    verifiche: dict[Path, dict[str, tuple[str, str]]] = {}
    prefissi: dict[Path, set[str]] = {}

    def raccogli(cartella: Path, nb) -> None:
        if filtro and cartella not in verifiche:
            verifiche[cartella] = leggi_modulo_corso(cartella)    # build parziale: tengo le altre
        d = verifiche.setdefault(cartella, {})
        if nb.prefisso_verifiche not in prefissi.setdefault(cartella, set()):
            prefissi[cartella].add(nb.prefisso_verifiche)
            for k in [k for k in d if k.startswith(nb.prefisso_verifiche)]:
                del d[k]
        d.update(nb.verifiche)

    for stem, nb in carica_extra(filtro):
        try:
            out = nb.build(ROOT / "Extra", aula="avanzata", soluzioni=True)
            raccogli(ROOT / "Extra", nb)
            print(f"{stem:32s} -> {out.relative_to(ROOT)}")
        except ValueError as e:
            print(f"[ERRORE] {e}")
            rc = 1
    for stem, nb in carica(filtro):
        for aula in nb.aule:
            for soluzioni in (False, True):
                try:
                    out = nb.build(CARTELLE[(aula, soluzioni)], aula=aula, soluzioni=soluzioni)
                    raccogli(CARTELLE[(aula, soluzioni)], nb)
                    print(f"{stem:32s} -> {out.relative_to(ROOT)}")
                except ValueError as e:
                    print(f"[ERRORE] {e}")
                    rc = 1
    for cartella, d in verifiche.items():
        out = scrivi_modulo_corso(cartella, dict(sorted(d.items(), key=_ordine)))
        print(f"{'corso.py':32s} -> {out.relative_to(ROOT)}  ({len(d)} controlli)")
    return rc


def _ordine(voce):
    """Ordina i codici: prima per notebook (numero o etichetta), poi per esercizio."""
    codice = voce[0]
    parti = re.split(r"[ .]", codice)
    return [(0, int(p)) if p.isdigit() else (1, p) for p in parti]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
