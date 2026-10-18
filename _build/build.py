"""
Costruisce i notebook del corso a partire dagli script in `_build/src/`.

    uv run python _build/build.py            # tutti
    uv run python _build/build.py 05 07      # solo quei numeri (C = homework, E1..E3 = esercitazioni, EXTRA = cartella Extra)

Output: le due cartelle che i corsisti ricevono, Aula_Base/ e Aula_Avanzata/, ciascuna con Modulo_1 … Modulo_4
(versione studente) e Soluzioni/ (versione con le soluzioni), più Extra/ e Riserva/ per il docente.
In ogni cartella di notebook scrive anche `corso.py`, il modulo con i controlli degli esercizi (`verifica("7.1")`).
Alla fine copia nelle cartelle delle aule i file che le rendono autosufficienti (dati, schede, progetto uv,
README, impostazioni di VS Code, cartelle della demo e dell'esercizio su uv e Ruff): vedi `statici.py`.
Un build completo toglie dalle cartelle delle aule i notebook e i `corso.py` che nessun sorgente produce più.
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
from statici import CARTELLE_AULA, copia_statici, togli_orfani  # noqa: E402


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
    soluzioni_reg: dict[Path, dict[str, tuple[str, str]]] = {}
    prefissi: dict[Path, set[str]] = {}

    def raccogli(cartella: Path, nb) -> None:
        if filtro and cartella not in verifiche:
            verifiche[cartella], vecchie = leggi_modulo_corso(cartella)    # build parziale: tengo le altre
            soluzioni_reg[cartella] = {k: (e, "B64:" + t) for k, (e, t) in vecchie.items()}
        d = verifiche.setdefault(cartella, {})
        sd = soluzioni_reg.setdefault(cartella, {})
        if nb.prefisso_verifiche not in prefissi.setdefault(cartella, set()):
            prefissi[cartella].add(nb.prefisso_verifiche)
            for k in [k for k in d if k.startswith(nb.prefisso_verifiche)]:
                del d[k]
            for k in [k for k in sd if k.startswith(nb.prefisso_verifiche)]:
                del sd[k]
        d.update(nb.verifiche)
        sd.update(nb.soluzioni)

    for stem, nb in carica_extra(filtro):
        try:
            out = nb.build(ROOT / "Extra", aula="avanzata", soluzioni=True)
            raccogli(ROOT / "Extra", nb)
            print(f"{stem:32s} -> {out.relative_to(ROOT)}")
        except ValueError as e:
            print(f"[ERRORE] {e}")
            rc = 1
    scritti: set[Path] = set()
    for stem, nb in carica(filtro):
        nome = nb.file
        for aula in nb.aule:
            for soluzioni in (False, True):
                if soluzioni and not nb.ha_soluzioni():
                    continue
                try:
                    if nb.riserva:      # materiale di riserva: fuori dalle cartelle dei corsisti
                        radice = ROOT / "Riserva" / aula.capitalize()
                        nb.file = nome + "_Soluzioni" if soluzioni else nome
                    else:
                        radice = CARTELLE_AULA[aula]
                    out = nb.build(radice, aula=aula, soluzioni=soluzioni)
                    raccogli(out.parent, nb)
                    scritti.add(out)
                    print(f"{stem:32s} -> {out.relative_to(ROOT)}")
                except ValueError as e:
                    print(f"[ERRORE] {e}")
                    rc = 1
        nb.file = nome
    for cartella, d in verifiche.items():
        sd = soluzioni_reg.get(cartella, {})
        if not d and not sd:        # notebook senza esercizi: nessun corso.py accanto
            (cartella / "corso.py").unlink(missing_ok=True)
            continue
        out = scrivi_modulo_corso(cartella, dict(sorted(d.items(), key=_ordine)), dict(sorted(sd.items(), key=_ordine)))
        scritti.add(out)
        print(f"{'corso.py':32s} -> {out.relative_to(ROOT)}  ({len(d)} controlli, {len(sd)} soluzioni a richiesta)")
    for riga in copia_statici():
        print(riga)
    if not filtro and rc == 0:
        for tolto in togli_orfani(scritti):
            print(f"{'rimosso (orfano)':32s} -> {tolto.relative_to(ROOT)}")
    return rc


def _ordine(voce):
    """Ordina i codici: prima per notebook (numero o etichetta), poi per esercizio."""
    codice = voce[0]
    parti = re.split(r"[ .]", codice)
    return [(0, int(p)) if p.isdigit() else (1, p) for p in parti]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
