#!/usr/bin/env python3
"""Crea ZIP per paese con markdown + GPX per uso offline locale."""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIP_DIR = ROOT / "zip"
ZIP_DIR.mkdir(exist_ok=True)

count=0
for country_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith(".") and p.name not in {"assets","mappe","tools","controllo","fonti","gruppi","gpx","zip"}):
    mds = list(country_dir.glob("*.md"))
    # includi anche sottocartelle ristoranti/ancoraggi se presenti
    extra = list((country_dir / "ristoranti").glob("*.md")) if (country_dir / "ristoranti").is_dir() else []
    extra += list((country_dir / "ancoraggi").glob("*.md")) if (country_dir / "ancoraggi").is_dir() else []
    if not mds:
        continue
    zip_path = ZIP_DIR / f"{country_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for f in mds + extra:
            z.write(f, arcname=f"{country_dir.name}/{f.relative_to(country_dir)}")
        # aggiungi GPX se esiste
        gpx = ROOT / "gpx" / f"{country_dir.name}.gpx"
        if gpx.exists():
            z.write(gpx, arcname=f"{country_dir.name}/{gpx.name}")
        # aggiungi README breve
        readme = f"{country_dir.name} — SailTropics Portolano\nWGS84 — ZIP offline paese\nApri i .md con qualsiasi editor o importa il .gpx in OpenCPN/Navionics\n"
        z.writestr(f"{country_dir.name}/README.txt", readme)
    print(f"OK {country_dir.name}: {len(mds)+len(extra)} md + gpx -> {zip_path} ({zip_path.stat().st_size} byte)")
    count+=1
print(f"TOT {count} ZIP in {ZIP_DIR}")
