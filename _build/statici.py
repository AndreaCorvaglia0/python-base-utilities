"""
I file non generati che rendono autosufficiente la cartella di un'aula, copiati da build.py dopo i notebook.

Il corsista riceve soltanto `Aula_Base/` o `Aula_Avanzata/`, e da lì deve poter lanciare `uv sync` e aprire ogni
notebook. Per questo ogni cartella contiene, oltre ai moduli:

    pyproject.toml, uv.lock, .python-version    il progetto uv dei corsisti, uguale per le due aule (_build/aula/)
    README.md                                   le istruzioni per il corsista (_build/aula/README_<aula>.md)
    .vscode/                                    impostazioni di VS Code per la cartella (_build/aula/vscode/<aula>/)
    Dati/                                       copia di Dati/ (senza i file che nessun notebook usa)
    Schede/                                     copia di Schede/

e, nella sola Avanzata, le cartelle della demo e dell'esercizio su uv e Ruff (_build/src/script_uv_ruff/):
il punto di partenza in `Modulo_1/Script_uv_Ruff/`, il punto di arrivo in `Soluzioni/Script_uv_Ruff/`.

Gli originali restano dove sono (`Dati/` e `Schede/` alla radice del repository, il resto in `_build/`): le copie
nelle aule si riscrivono a ogni build e non si modificano a mano.
"""

from __future__ import annotations

import filecmp
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AULA_SRC = HERE / "aula"
SCRIPT_UV_SRC = HERE / "src" / "script_uv_ruff"

CARTELLE_AULA = {"base": ROOT / "Aula_Base", "avanzata": ROOT / "Aula_Avanzata"}
FILE_PROGETTO = ["pyproject.toml", "uv.lock", ".python-version"]

# file di Dati/ che non vanno ai corsisti: nessun notebook li usa, oppure servono solo all'altra aula
DATI_ESCLUSI = {"README.md", "prezzi_zonali_2025_settimana.csv", "fallback/meteo_milano_previsione.json"}
DATI_SOLO_AVANZATA = {"fallback/lombardia_sensori.json", "fallback/lombardia_misure_2001.json"}

# cartelle della demo e dell'esercizio: punto di partenza nel modulo, punto di arrivo nelle soluzioni
SCRIPT_UV = {
    "Modulo_1/Script_uv_Ruff/demo": "demo",
    "Modulo_1/Script_uv_Ruff/esercizio": "esercizio",
    "Soluzioni/Script_uv_Ruff/demo": "soluzioni/demo",
    "Soluzioni/Script_uv_Ruff/esercizio": "soluzioni/esercizio",
}
# quello che una prova lascia nelle cartelle della demo: non si copia dalle sorgenti e si toglie dalle copie
DA_NON_COPIARE = (".venv", "__pycache__", ".ruff_cache", "*.xlsx", "*.pyc")


def _dati_per(aula: str) -> list[str]:
    tutti = sorted(str(p.relative_to(ROOT / "Dati")).replace("\\", "/") for p in (ROOT / "Dati").rglob("*") if p.is_file())
    return [f for f in tutti if f not in DATI_ESCLUSI and (aula == "avanzata" or f not in DATI_SOLO_AVANZATA)]


def _readme_dati(aula: str) -> str:
    """Il README di Dati/ per il corsista: solo i file che riceve, senza i comandi per rigenerarli."""
    righe = []
    presenti = set(_dati_per(aula))
    for riga in (ROOT / "Dati" / "README.md").read_text(encoding="utf-8").splitlines():
        nomi = re.findall(r"`([^`]+\.(?:csv|xlsx|db|json))`", riga.split("|")[1]) if riga.startswith("| `") else []
        if nomi and not any(n in presenti for n in nomi):
            continue
        if "_build/" in riga and not riga.startswith("|"):
            continue
        riga = re.sub(r"dati di esempio, generati da `_build/genera_dati.py` con lo stesso schema dell'API; "
                      r"`uv run python _build/scarica_fallback.py` li sostituisce con i dati veri",
                      "copia della risposta dell'API, usata quando la rete non è disponibile", riga)
        righe.append(riga)
    return "\n".join(righe).rstrip() + "\n"


def _sincronizza(coppie: dict[Path, Path], dst: Path, tieni=lambda f: False) -> None:
    """Rende la cartella `dst` uguale all'elenco `coppie` (destinazione -> origine): copia solo i file che mancano o
    sono cambiati e toglie quelli in più, così chi sta eseguendo un notebook non vede mai sparire un file."""
    for d, o in coppie.items():
        if not d.exists() or not filecmp.cmp(o, d, shallow=False):
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(o, d)
    if dst.exists():
        for f in sorted(dst.rglob("*"), reverse=True):
            if f.is_file() and f not in coppie and not tieni(f):
                f.unlink()
            elif f.is_dir() and not any(f.iterdir()):
                f.rmdir()


def _rispecchia(src: Path, dst: Path, ignora: tuple[str, ...] = ()) -> None:
    """Rende `dst` una copia esatta di `src`, senza i file e le cartelle che corrispondono a `ignora`. Quello che una
    prova ha lasciato in `dst` (`.venv`, `uv.lock`, i file Excel, le cache) si toglie: con un `.venv` rimasto da una
    prova, nella demo le librerie risulterebbero già installate."""
    def ignorato(f: Path) -> bool:
        return any(part == pat or (pat.startswith("*") and part.endswith(pat[1:])) for part in f.parts for pat in ignora)

    coppie = {dst / f.relative_to(src): f for f in src.rglob("*") if f.is_file() and not ignorato(f.relative_to(src))}
    if dst.exists():
        for d in [d for d in dst.iterdir() if d.is_dir() and d.name in ignora]:
            shutil.rmtree(d)        # .venv e cache: via in un colpo, senza scorrerne i file
    _sincronizza(coppie, dst)


def copia_statici() -> list[str]:
    """Copia i file non generati nelle cartelle delle aule e restituisce le righe di resoconto."""
    resoconto = []
    for aula, cartella in CARTELLE_AULA.items():
        cartella.mkdir(exist_ok=True)
        for nome in FILE_PROGETTO:
            shutil.copy2(AULA_SRC / nome, cartella / nome)
        shutil.copy2(AULA_SRC / f"README_{aula}.md", cartella / "README.md")
        _rispecchia(AULA_SRC / "vscode" / aula, cartella / ".vscode")

        dati = cartella / "Dati"
        _sincronizza({dati / f: ROOT / "Dati" / f for f in _dati_per(aula)}, dati, tieni=lambda f: f == dati / "README.md")
        (dati / "README.md").write_text(_readme_dati(aula), encoding="utf-8")
        _rispecchia(ROOT / "Schede", cartella / "Schede")

        n_script = 0
        if aula == "avanzata":
            for dst, src in SCRIPT_UV.items():
                _rispecchia(SCRIPT_UV_SRC / src, cartella / dst, DA_NON_COPIARE)
                n_script += 1
        resoconto.append(f"{'statici':32s} -> {cartella.relative_to(ROOT)}  (progetto uv, README, .vscode, "
                         f"{len(_dati_per(aula))} file di dati, Schede" + (f", {n_script} cartelle script)" if n_script else ")"))
    return resoconto


def togli_orfani(scritti: set[Path]) -> list[Path]:
    """Dopo un build completo, toglie dalle cartelle delle aule i notebook e i corso.py che nessun sorgente produce."""
    tolti = []
    for cartella in CARTELLE_AULA.values():
        for f in sorted(cartella.rglob("*")):
            if ".venv" in f.parts or not f.is_file() or (f.suffix != ".ipynb" and f.name != "corso.py"):
                continue
            if f not in scritti:
                f.unlink()
                tolti.append(f)
    return tolti


def differenze() -> list[str]:
    """Le copie nelle aule che non coincidono con gli originali (per controlla.py)."""
    problemi = []
    for aula, cartella in CARTELLE_AULA.items():
        for nome in FILE_PROGETTO:
            if not filecmp.cmp(AULA_SRC / nome, cartella / nome, shallow=False):
                problemi.append(f"{cartella.name}/{nome} diverso da _build/aula/{nome}")
        for f in _dati_per(aula):
            if not (cartella / "Dati" / f).exists() or not filecmp.cmp(ROOT / "Dati" / f, cartella / "Dati" / f, shallow=False):
                problemi.append(f"{cartella.name}/Dati/{f} diverso da Dati/{f}")
    return problemi
