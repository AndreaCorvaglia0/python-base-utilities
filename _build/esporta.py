"""
Prepara gli zip da consegnare ai corsisti: uno per aula, con dentro la sola cartella dell'aula.

    uv run python _build/esporta.py              # build completo, poi dist/Aula_Base.zip e dist/Aula_Avanzata.zip
    uv run python _build/esporta.py avanzata     # solo un'aula

Prima ricostruisce tutto il corso, così le copie di dati, schede e cartelle della demo tornano identiche agli
originali anche dopo una prova in aula. Nello zip entrano soltanto i file che git conosce o che non ignora: restano
fuori l'ambiente `.venv`, le cache e i file che i notebook e gli script producono quando si eseguono.
"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from statici import CARTELLE_AULA  # noqa: E402


def file_da_esportare(cartella: Path) -> list[Path]:
    """I file della cartella che git traccia o che non ignora, in ordine."""
    p = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", cartella.name],
                       cwd=ROOT, capture_output=True, text=True, check=True)
    return sorted(ROOT / f for f in p.stdout.split("\0") if f and (ROOT / f).is_file())


def main(argv: list[str]) -> int:
    aule = [a.lower() for a in argv] or list(CARTELLE_AULA)
    rc = subprocess.run([sys.executable, str(HERE / "build.py")], cwd=ROOT).returncode
    if rc != 0:
        print("[ERRORE] il build non è andato a buon fine: niente zip")
        return rc
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    for aula in aule:
        cartella = CARTELLE_AULA[aula]
        uscita = dist / f"{cartella.name}.zip"
        files = file_da_esportare(cartella)
        with zipfile.ZipFile(uscita, "w", zipfile.ZIP_DEFLATED) as z:
            for f in files:
                z.write(f, f.relative_to(ROOT).as_posix())
        print(f"{uscita.relative_to(ROOT)}: {len(files)} file, {uscita.stat().st_size / 1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
