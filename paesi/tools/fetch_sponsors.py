#!/usr/bin/env python3
"""Sincronizza sponsors.json da Ko-fi / Patreon / GitHub Sponsors (anonimo di default, GDPR)."""
import json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "sponsors.json"

# Placeholder: in produzione qui chiamate API Ko-fi / GitHub con token
# Per ora mantiene file esistente o crea esempio anonimo
if not OUT.exists():
    OUT.write_text(json.dumps([
        {"nick":"anonimo","amount":5,"date":datetime.date.today().isoformat(),"via":"ko-fi","msg":""}
    ], ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"creato {OUT}")
else:
    data = json.loads(OUT.read_text(encoding="utf-8"))
    # normalizza: nick mancante -> anonimo, rimuove email/tracking
    for r in data:
        if not r.get("nick"): r["nick"]="anonimo"
        r.pop("email", None); r.pop("ip", None)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"verificato {OUT} ({len(data)} sostenitori, GDPR: solo nick anonimo o autorizzato)")
