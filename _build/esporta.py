"""
Prepara gli zip da consegnare ai corsisti: uno per aula, con dentro la sola cartella dell'aula.

    uv run python _build/esporta.py                      # build completo, poi dist/Aula_Base.zip e dist/Aula_Avanzata.zip
    uv run python _build/esporta.py avanzata             # solo un'aula
    uv run python _build/esporta.py --moduli 3 4         # aggiornamento: solo Modulo_3 e Modulo_4, per entrambe le aule
    uv run python _build/esporta.py avanzata --riserva   # il materiale di riserva di un'aula, da estrarre nella sua cartella

Prima ricostruisce tutto il corso, così le copie di dati, schede e cartelle della demo tornano identiche agli
originali anche dopo una prova in aula. Nello zip entrano soltanto i file che git conosce o che non ignora: restano
fuori l'ambiente `.venv`, le cache e i file che i notebook e gli script producono quando si eseguono.

Con `--moduli` lo zip (dist/Aula_X_moduli_3_4.zip) contiene soltanto le cartelle di quei moduli, le loro soluzioni,
`Soluzioni/corso.py`, `Dati/` e `Schede/`: estratto sopra la cartella che il corsista ha già, aggiorna quei moduli e
non tocca i notebook dei moduli precedenti, in cui il corsista ha scritto le sue risposte.

Con `--riserva` lo zip (dist/Riserva_Avanzata.zip) contiene `Riserva/<Aula>/`, con i notebook di riserva e il loro
`corso.py`: il corsista lo estrae dentro la cartella dell'aula, e i percorsi `../../Dati/` dei notebook di riserva
arrivano allora ai dati del corso come nel repository.
"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from statici import CARTELLE_AULA, SCRIPT_UV  # noqa: E402


def file_da_esportare(cartella: Path) -> list[Path]:
    """I file della cartella che git traccia o che non ignora, in ordine. Quelli non ancora tracciati si elencano,
    perché un file lasciato da una prova finirebbe nello zip senza che nessuno se ne accorga."""
    def ls(*opzioni: str) -> list[str]:
        p = subprocess.run(["git", "ls-files", *opzioni, "-z", "--", cartella.relative_to(ROOT).as_posix()],
                           cwd=ROOT, capture_output=True, encoding="utf-8", check=True)
        return [f for f in p.stdout.split("\0") if f]

    nuovi = ls("--others", "--exclude-standard")
    if nuovi:
        print(f"[avviso] {len(nuovi)} file non tracciati da git finiscono nello zip:", *nuovi, sep="\n  ")
    return sorted(ROOT / f for f in ls("--cached") + nuovi if (ROOT / f).is_file())


def solo_moduli(cartella: Path, files: list[Path], moduli: list[int]) -> list[Path]:
    """I file di un aggiornamento: i moduli indicati, le loro soluzioni, dati e schede."""
    cartelle = [cartella / f"Modulo_{m}" for m in moduli]
    nomi = {f.name for f in files if any(c in f.parents for c in cartelle) and f.suffix == ".ipynb"}
    soluzioni = cartella / "Soluzioni"
    # le cartelle finite della demo e dell'esercizio vanno con il modulo che contiene il loro punto di partenza
    soluzioni_script = [dst for dst in SCRIPT_UV if dst.startswith("Soluzioni/")
                        and any(d.startswith(f"Modulo_{m}/") and d.endswith(dst.split("/", 1)[1]) for d in SCRIPT_UV for m in moduli)]
    tenuti = []
    for f in files:
        dentro = any(c in f.parents for c in cartelle) or any(f.is_relative_to(cartella / d) for d in ("Dati", "Schede"))
        sol = f.parent == soluzioni and (f.name in nomi or f.name == "corso.py")
        script = any(f.is_relative_to(cartella / dst) for dst in soluzioni_script)
        if dentro or sol or script:
            tenuti.append(f)
    return tenuti


def main(argv: list[str]) -> int:
    riserva = "--riserva" in argv
    argv = [a for a in argv if a != "--riserva"]
    moduli = [int(a) for a in argv[argv.index("--moduli") + 1:] if a.isdigit()] if "--moduli" in argv else []
    nomi_aule = argv[:argv.index("--moduli")] if "--moduli" in argv else argv
    aule = [a.lower() for a in nomi_aule] or list(CARTELLE_AULA)
    sbagliate = [a for a in aule if a not in CARTELLE_AULA]
    if sbagliate or ("--moduli" in argv and not moduli) or any(m not in (1, 2, 3, 4) for m in moduli) or (riserva and moduli):
        print("[ERRORE] uso: esporta.py [base|avanzata ...] [--moduli N ...] [--riserva]  (moduli da 1 a 4, "
              "--riserva senza --moduli)")
        return 2
    rc = subprocess.run([sys.executable, str(HERE / "build.py")], cwd=ROOT).returncode
    if rc != 0:
        print("[ERRORE] il build non è andato a buon fine: niente zip")
        return rc
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    for aula in aule:
        cartella = ROOT / "Riserva" / aula.capitalize() if riserva else CARTELLE_AULA[aula]
        files = file_da_esportare(cartella)
        if riserva:
            uscita = dist / f"Riserva_{aula.capitalize()}.zip"
        elif moduli:
            files = solo_moduli(cartella, files, moduli)
            uscita = dist / f"{cartella.name}_moduli_{'_'.join(map(str, moduli))}.zip"
        else:
            uscita = dist / f"{cartella.name}.zip"
        with zipfile.ZipFile(uscita, "w", zipfile.ZIP_DEFLATED) as z:
            for f in files:
                z.write(f, f.relative_to(ROOT).as_posix())
        print(f"{uscita.relative_to(ROOT)}: {len(files)} file, {uscita.stat().st_size / 1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
