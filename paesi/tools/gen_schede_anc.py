#!/usr/bin/env python3
"""Genera le schede anc-* (standard Martinica) da un JSON di dati verificati,
inserisce/aggiorna la mappa generale nel 08 e collega i marker alle schede.
USO: python3 gen_schede_anc.py <config.json>   (dry-run: --dry)"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def dms(v, pos, neg):
    h = pos if v >= 0 else neg
    v = abs(v)
    d = int(v)
    m = (v - d) * 60
    mi = int(m)
    s = int(round((m - mi) * 60))
    if s == 60:
        mi += 1
        s = 0
    return f"{d}\u00b0{mi:02d}\u2032{s:02d}\u2033 {h}"


def scheda_md(s, data):
    L = [
        f"# {s['nome']} {{#{s['slug']}}}",
        "",
        "[← Tutti gli ancoraggi](../08-ancoraggi.md)",
        f"**{dms(s['lat'], 'N', 'S')} {dms(s['lon'], 'E', 'W')}** {s.get('rank', '★★')}",
        "",
        "| Campo | Dettaglio |",
        "|---|---|",
        f"| **Profondità** |{s.get('profondita', '**DATO MANCANTE**')}|",
        f"| **Tenuta àncora** |{s.get('tenuta', '**DATO MANCANTE**')}|",
        f"| **Venti/riparo** |{s.get('riparo', '**DATO MANCANTE**')}|",
        f"| **Pericoli** |{s.get('pericoli', '—')}|",
        f"| **Boe/divieti/normative** |{s.get('normative', '—')}|",
        f"| **A terra** |{s.get('aterra', '**DATO MANCANTE**')}|",
        "",
        f"<div class=\"mapframe\" data-slug=\"{s['slug']}\" data-lat=\"{s['lat']}\" data-lon=\"{s['lon']}\"></div>",
        "*Cartina di dettaglio — zoom ± fino alla baia · mappa offline · coordinate WGS84 indicative, verificare sempre col plotter*",
        "",
        f"Fonti: {s.get('fonte', '**DATO MANCANTE**')}",
        "",
        f"Ultimo aggiornamento: {data}",
        "",
    ]
    return "\n".join(L)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    cfg = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    paese = cfg["paese"]
    data = cfg.get("data", "25/08/2026")
    base = ROOT / paese
    adir = base / "ancoraggi"
    f08 = base / "08-ancoraggi.md"
    txt = f08.read_text(encoding="utf-8")

    # 1) schede
    for s in cfg["schede"]:
        p = adir / f"{s['slug']}.md"
        if dry:
            print(f"[dry] scheda {p.name}")
        else:
            adir.mkdir(exist_ok=True)
            p.write_text(scheda_md(s, data), encoding="utf-8")
            print(f"scheda scritta: {p}")

    # 2) mappa generale: inserisci se manca
    if "<div class=\"mapframe\"" not in txt:
        def clean(nome):
            # regola trappola apostrofi: mai ASCII ' dentro data-markers
            return str(nome).replace("'", "\u2019")
        mk = ", ".join(
            json.dumps([s["lat"], s["lon"], clean(s["nome"]), s["slug"]], ensure_ascii=False)
            for s in cfg["schede"]
        )
        frame = ("## Mappa generale degli ancoraggi\n\n"
                 f"<div class=\"mapframe\" data-slug=\"{cfg.get('slug_mappa', paese)}\" "
                 f"data-minz=\"{cfg.get('minz', 7)}\" data-maxz=\"{cfg.get('maxz', 13)}\" "
                 f"data-lat=\"{cfg['lat']}\" data-lon=\"{cfg['lon']}\" "
                 f"data-markers='[{mk}]'></div>\n\n"
                 "*⚓ Àncore cliccabili: il click apre la SCHEDA DI DETTAGLIO dell'ancoraggio "
                 "con la cartina zoomabile della baia.*\n\n---\n\n")
        mm = re.search(r"^## ", txt, re.M)
        pos = mm.start() if mm else len(txt)
        txt = txt[:pos] + frame + txt[pos:]
        print("mappa generale inserita")

    # 3) marker 3→4 campi (collega alle schede per coord. combacianti)
    def rep(mm):
        try:
            pts = json.loads(mm.group(1))
        except Exception:
            return mm.group(0)
        changed = False
        for p in pts:
            if len(p) >= 4:
                continue
            hit = next((s for s in cfg["schede"]
                        if abs(s["lat"] - p[0]) < 2e-4 and abs(s["lon"] - p[1]) < 2e-4), None)
            if hit:
                p.append(hit["slug"])
                changed = True
        if not changed:
            return mm.group(0)
        return "data-markers='" + json.dumps(pts, ensure_ascii=False) + "'"

    txt = re.sub(r"data-markers='([^']+)'", rep, txt)

    if dry:
        print("[dry] 08 aggiornato (non salvato)")
        return
    f08.write_text(txt, encoding="utf-8")
    print(f"08 aggiornato: {f08}")


if __name__ == "__main__":
    main()
