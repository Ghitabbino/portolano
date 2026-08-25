#!/usr/bin/env python3
"""CONTROLLI MULTIPLI del portolano (regola utente 25/08/2026).
Uso: python3 tools/controlli_multipli.py
Verifiche:
 1. link interni .md rotti
 2. contaminazione: link che scavalcano in un altro paese
 3. marker mappa -> scheda mancante
 4. ancore {#anc-*} duplicate
 5. ID sezione duplicati nel paesi.html costruito
 6. (esterno) URL: usare tools/controlla_link.py
Output: tools/rapporto_controlli.txt"""
import re
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
EXCL = {"tools", "fonti", "controllo", "mappe", "assets", "gruppi"}
LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)(#[^)]*)?\)")
report = []
broken = cross = miss = dup_anchor = dup_id = 0

mds = [m for m in sorted(ROOT.rglob("*.md")) if not set(m.parts) & EXCL]
anchors = Counter()
anchor_file = {}

# 4) ancore duplicate
for md in mds:
    for a in re.findall(r"\{(#anc-[a-z0-9-]+)\}", md.read_text(encoding="utf-8")):
        anchors[a] += 1
        anchor_file.setdefault(a, str(md.relative_to(ROOT)))
for a, n in anchors.items():
    if n > 1:
        dup_anchor += 1
        report.append(f"[4-DUP-ANCORA] {a} ×{n} ({anchor_file[a]} e altri)")

# 1+2) link interni
for md in mds:
    paese_md = md.relative_to(ROOT).parts[0] if len(md.relative_to(ROOT).parts) > 1 else ""
    t = md.read_text(encoding="utf-8")
    for target in LINK.findall(t):
        tgt = target[0]
        dest = (md.parent / tgt).resolve()
        rel = None
        try:
            rel = dest.relative_to(ROOT)
        except ValueError:
            pass
        if not dest.exists():
            broken += 1
            report.append(f"[1-ROTTO] {md.relative_to(ROOT)} -> {tgt}")
        elif rel and len(rel.parts) > 1 and rel.parts[0] != paese_md and rel.parts[0] not in EXCL:
            cross += 1
            report.append(f"[2-SCAVALCA] {md.relative_to(ROOT)} -> {rel}")

# 3) marker -> scheda
for md in mds:
    txt = md.read_text(encoding="utf-8")
    for m in re.finditer(r"data-markers='([^']+)'", txt):
        try:
            pts = json.loads(m.group(1))
        except Exception:
            continue
        for p in pts:
            if len(p) >= 4:
                scheda = next(iter(ROOT.glob(f"**/{p[3]}.md")), None)
                if not scheda:
                    miss += 1
                    report.append(f"[3-SENZA-SCHEDA] marker '{p[2]}' -> {p[3]}.md inesistente ({md.relative_to(ROOT)})")

# 5) id duplicati nell'html costruito
html = ROOT / "paesi.html"
if html.exists():
    ids = re.findall(r'<(?:section|h1)[^>]*\bid="([^"]+)"', html.read_text(encoding="utf-8"))
    for i, n in Counter(ids).items():
        if n > 1:
            dup_id += 1
            report.append(f"[5-DUP-ID] #{i} ×{n} nel paesi.html")

(ROOT / "tools/rapporto_controlli.txt").write_text("\n".join(report) or "NESSUN PROBLEMA\n", encoding="utf-8")
print(f"1-link rotti: {broken} · 2-scavalcano paese: {cross} · 3-marker senza scheda: {miss} · 4-ancore doppie: {dup_anchor} · 5-ID duplicati: {dup_id}")
print("dettaglio in tools/rapporto_controlli.txt")
