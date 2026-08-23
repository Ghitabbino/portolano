#!/usr/bin/env python3
"""Deep audit wiki: titoli, date, link schede, marker JSON, tiles, emergenze."""
from pathlib import Path
import json, re

ROOT = Path("/Users/giovanninatale/Documents/Default Project/paesi")
issues = []
def add(cat, where, what): issues.append((cat, where, what))

titles = {}
mds = [f for f in sorted(ROOT.rglob("*.md"))
       if not str(f.relative_to(ROOT)).startswith(("assets","fonti","tools","mappe"))]

for f in mds:
    rel = str(f.relative_to(ROOT))
    t = f.read_text(encoding="utf-8")
    lines = [l for l in t.splitlines() if l.strip()]
    if not lines:
        add("VUOTO", rel, ""); continue
    first = lines[0]
    nm = re.sub(r"[^a-z0-9]", "", first.lstrip("# ").lower())
    titles.setdefault(nm, rel)
    if not re.match(r"^# \d{2}\s*[-\u2014]\s*\S", first):
        add("TITOLO", rel, first[:45])
    if not re.search(r"\d{2}/\d{2}/\d{4}", lines[-1]):
        add("DATA", rel, lines[-1][:45])
    # attributi mappa
    for m in re.finditer(r"data-(markers|zones)='([^']*)'", t):
        kind, raw = m.group(1), m.group(2)
        if "'" in raw:
            add("HTML-ATTR", rel, f"apostrofo dentro data-{kind}")
        try:
            arr = json.loads(raw)
            if kind == "markers":
                for pt in arr:
                    lbl = pt[2] if len(pt) >= 3 else ""
                    key = re.sub(r"[^a-z0-9]", "", lbl.lower())
                    if key and key not in titles and key != "ristoranti":
                        add("MARKER-ORFANO", rel, lbl)
        except Exception as e:
            add("JSON", rel, f"data-{kind}: {type(e).__name__}")
    # slug tiles esistenti
    for sm in re.finditer(r'data-slug="([^"]+)"', t):
        slug = sm.group(1)
        d = ROOT / "mappe" / slug
        if not d.exists() or not any(d.iterdir()):
            add("TILES", rel, f"slug '{slug}' senza tasselli")
    # link griglia ristoranti esistono
    g = f.parent.name
    if f.name == "10-ristoranti.md":
        for lm in re.finditer(r"\]\((ristoranti/[^)]+)\)", t):
            if not (f.parent / lm.group(1)).exists():
                add("LINK-ROTTO", rel, lm.group(1))
    # emergenze coerenti per famiglia
    if f.name == "06-sicurezza.md":
        if rel.startswith("canarie"):
            fam_ok = "**112**" in t and "VHF 16" in t
        elif rel.startswith("panama"):
            fam_ok = "**911**" in t
        elif rel.startswith("cabo-verde"):
            fam_ok = "**132**" in t and "**130**" in t
        elif rel.startswith("grenadine"):
            fam_ok = ("**999**" in t or "**911**" in t) and "VHF" in t
        else:
            fam_ok = "**112**" in t
        if not fam_ok:
            add("EMERGENZE", rel, "numeri mancanti/sbagliati")

print(f"FILE ANALIZZATI: {len(mds)}")
if issues:
    print(f"PROBLEMI: {len(issues)}")
    from collections import Counter
    cnt = Counter(c for c,_,_ in issues)
    print("Per categoria:", dict(cnt))
    for c, w, what in issues:
        print(f"  [{c}] {w} :: {what}")
else:
    print("NESSUN PROBLEMA ✓")
