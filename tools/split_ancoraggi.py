#!/usr/bin/env python3
"""Migrazione: schede ancoraggio inline -> pagine separate in ancoraggi/ (stesso schema ristoranti)."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEC = re.compile(r"^## (?:\d+\.\s*)?(.+?) \{#(anc-[a-z0-9-]+)\}\s*$", re.M)

def migrate(country_dir: Path):
    f = country_dir / "08-ancoraggi.md"
    if not f.exists():
        return "no 08"
    text = f.read_text(encoding="utf-8")
    outdir = country_dir / "ancoraggi"
    matches = list(SEC.finditer(text))
    if not matches:
        return "nessuna scheda inline (già migrato?)"
    outdir.mkdir(exist_ok=True)
    made = []
    for i, m in enumerate(matches):
        slug, title, body = m.group(2), m.group(1), text[m.end():matches[i+1].start() if i+1 < len(matches) else len(text)]
        page = f"# {title} {{#{slug}}}\n\n[← Tutti gli ancoraggi](../08-ancoraggi.md)\n{body.strip()}\n"
        (outdir / f"{slug}.md").write_text(page, encoding="utf-8")
        made.append(slug)
    # pulizia pagina principale
    main = text[:matches[0].start()].rstrip() + "\n"
    # taglio eventuale coda dopo l'ultima scheda (cartografia/checklist) -> la riattacco
    tail_start = text.find("\n## ", matches[-1].end())
    tail = ""
    if tail_start != -1:
        seg = text[tail_start:]
        nxt = SEC.search(seg)
        tail = seg[:nxt.start()] if nxt else seg
    if tail.strip():
        main = main.rstrip() + "\n\n" + tail.strip() + "\n"
    # link tabella: [Nome →](#anc-x) -> [Nome](ancoraggi/anc-x.md)
    main = re.sub(r"\[([^\]]+?) →\]\(#(anc-[a-z0-9-]+)\)", r"[\1](ancoraggi/\2.md)", main)
    main = re.sub(r"\]\(#(anc-[a-z0-9-]+)\)(?!\()", lambda m: f"](ancoraggi/{m.group(1)}.md)" if m.group(1) in made else m.group(0), main)
    f.write_text(main, encoding="utf-8")
    return f"{len(made)} schede: {', '.join(made)}"

for c in ["martinica", "guadalupa", "panama/canale"]:
    d = ROOT / c
    print(f"{c}: {migrate(d)}")
