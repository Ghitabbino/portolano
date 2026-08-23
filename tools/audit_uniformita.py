#!/usr/bin/env python3
"""AUDIT RIGOROSO uniformità layout — standard: MARTINICA."""
from pathlib import Path
import re, sys

ROOT = Path("/Users/giovanninatale/Documents/Default Project/paesi")

# Sezioni obbligatorie per tipo pagina (header ## attesi, dallo standard Martinica)
STD = {
 "00": ["## Status","## Cittadini UE","## La barca"],
 "01": ["## Chi deve farla","## Costi","## Da verificare"],
 "02": ["## Alimentari","## Mangiare fuori","## Carburanti","## Trasporti","## Servizi quotidiani","## Contanti e pagamenti"],
 "03": ["## Tariffe","## Distanze utili"],
 "04": ["## Hub tecnico","## Gas e bombole","## Acqua dolce","## Note strategiche"],
 "05": ["## Clima","## Stagioni","## Venti locali","## Finestre tipiche","## Link meteo"],
 "06": ["Valutazione sicurezza","## Quadro generale","## Posti sicuri","## Salvataggio ed emergenze","## Monitoraggio mensile"],
 "07": ["## Supermercati","## Acqua e carburante","## Consigli pratici"],
 "08": ["## Regole generali","## Tabella riassuntiva","## Cartografia ufficiale","## Checklist àncora"],
 "09": ["Tabella artigiani","## Dove si trova cosa","## Note pratiche"],
 "10": ["## Griglia generale","## App e fonti"],
}
EMERG = {
 "canarie": ["**112**","VHF 16","+34 91 346 44 44"],
 "panama":  ["**112**"],  # da correggere: a Panama 112 non è il numero locale
}

targets=[]
for cdir in sorted(ROOT.iterdir()):
    if not cdir.is_dir() or cdir.name.startswith(".") or cdir.name in ("assets","fonti","tools","mappe"): continue
    files={f.name[:2]: f for f in sorted(cdir.glob("*.md"))}
    if files: targets.append((cdir.name,"",files))
    for zdir in sorted(p for p in cdir.iterdir() if p.is_dir() and p.name not in ("ristoranti","ancoraggi") and not p.name.startswith(".")):
        zf={f.name[:2]: f for f in sorted(zdir.glob("*.md"))}
        if zf: targets.append((cdir.name,zdir.name,zf))

report=[]; fixes=0
for paese, zona, files in targets:
    loc=f"{paese}/{zona}".rstrip("/")
    fam="canarie" if paese=="canarie" else ("panama" if paese=="panama" else "fr")
    for nn, req in STD.items():
        f=files.get(nn)
        if not f:
            continue  # assenza file gestita altrove (zone senza 00 by design)
        t=f.read_text()
        missing=[h for h in req if h.lower() not in t.lower()]
        if missing:
            report.append((loc,f.name,missing))
            if "--fix" in sys.argv:
                ins="\n".join(f"\n{h}\n\n**DATO MANCANTE** — da completare al controllo mensile.\n" for h in missing)
                t=t.rstrip()+"\n"+ins+"\n"
                if nn=="06" and "Valutazione sicurezza" not in t:
                    t=t.replace(f"# {t.splitlines()[0][2:]}", "# "+t.splitlines()[0][2:]+"\n\n## Valutazione sicurezza: **DATO MANCANTE**\n",1)
                f.write_text(t); fixes+=1
    # numeri emergenza
    if nn_ok := files.get("06"):
        t=nn_ok.read_text()
        if fam=="panama" and "**112**" in t and "911" not in t:
            if "--fix" in sys.argv:
                t=t.replace("**112**","**911** (emergenze Panama)"); nn_ok.write_text(t); fixes+=1; report.append((loc,"06-numeri","112→911 PANAMA"))

n_dev=sum(len(r[2]) for r in report)
print(f"AUDIT su {len(targets)} gruppi-pagine — deviazioni: {n_dev} in {len(report)} file")
for loc,fn,miss in report:
    print(f"  {loc}/{fn}: {', '.join(miss)}")
if "--fix" in sys.argv: print(f"FIX applicati: {fixes}")
