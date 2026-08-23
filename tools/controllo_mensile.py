#!/usr/bin/env python3
"""REVISIONE MENSILE del portolano — lanciabile da qualsiasi agente.

Uso: python3 tools/controllo_mensile.py [--paese martinica]

1) Elenca tutti i DATO MANCANTE raggruppati per paese/pagina.
2) Stampa la CHECKLIST delle fonti dove andare a cercare (per paese).
3) Ricorda le 6 aree del controllo mensile standard.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FONTI = {
 "guadalupa": ["Noonsite Guadeloupe", "noforeignland recensioni", "France-Antilles / RCI",
               "Préfecture de la Guadeloupe (bilan délinquance)", "voyage.gc.ca / diplomatie.gouv.fr",
               "Marina Bas-du-Fort sito (listino)", "Paginas Jaunes Antilles (contatti)"],
 "martinica": ["Noonsite Martinique", "France-Antilles", "RCI Martinique",
               "martinique.gouv.fr (clearance/arrêté)", "Marina du Marin listino PDF",
               "Pages Jaunes Antilles (contatti)", "Petit Futé Antilles"],
 "panama": ["Noonsite Panama", "pancanal.com (tariffe ACP)", "Shelter Bay Marina sito/news",
            "Balboa YC", "Panama Cruising Guide", "forum cruisers (CF/Salty Dawg)"],
 "canarie": ["puertosdetenerife.org (marine/tariffe)", "puertoscanarios.es",
             "Navily blog + app", "Ocean Posse Cape Verde/Grenadine-style guides",
             "siti marine ufficiali (marinasantacruz, palmasport, caleromarinas...)",
             "AEMET (meteo)", "Paginas Amarillas ES (contatti supermercati)"],
 "cabo-verde": ["Noonsite Cape Verde", "Ocean Posse cape-verde", "Navily blog cruising CV",
                "velmundi sailing CV", "sarcontacts.info (SAR)", "ENAPOR/portogrande.cv",
                "blog naviganti (mollymawk, Amalia...)"],
 "grenadine": ["Noonsite SVG", "Tobago Cays Marine Park ufficiale (fee)",
               "mustiqueisland.com (entry)", "Bequia tourism + forum cruisers",
               "SVG gov clearance portal"],
}

def main():
    filtro = None
    if len(sys.argv) > 2 and sys.argv[1] == "--paese":
        filtro = sys.argv[2]
    print("=" * 62)
    print("REVISIONE MENSILE PORTOLANO —", "tutti i paesi" if not filtro else filtro)
    print("=" * 62)
    dm = {}
    for f in sorted(ROOT.rglob("*.md")):
        rel = str(f.relative_to(ROOT))
        if rel.startswith(("assets","tools","mappe","fonti")):
            continue
        paese = rel.split("/")[0]
        if filtro and paese != filtro:
            continue
        n = f.read_text(encoding="utf-8").count("**DATO MANCANTE**")
        if n:
            dm.setdefault(paese, []).append((rel, n))
    tot = 0
    for p, lst in sorted(dm.items()):
        c = sum(n for _, n in lst)
        tot += c
        print(f"\n[{p}] {c} dati mancanti:")
        for rel, n in sorted(lst):
            print(f"   - {rel} ({n})")
    print(f"\nTOTALE: {tot}")
    paesi = [p for p in FONTI if not filtro or p == filtro]
    for p in paesi:
        print(f"\n--- DOVE CERCARE [{p}] ---")
        for s in FONTI[p]:
            print("   •", s)
    print("\n--- 6 AREE DEL CONTROLLO STANDARD ---")
    for i, a in enumerate(["Contatti (tel/mail/orari su fonti ufficiali)",
                           "Notizie: regolamenti, nuovi servizi, meteo/sicurezza",
                           "Conflitti aperti tra fonti",
                           "Mappe: completare tasselli mancanti",
                           "Sicurezza: media locali + advisory",
                           "DATO MANCANTE: sweep mirato con le fonti sopra"], 1):
        print(f"   {i}. {a}")

if __name__ == "__main__":
    main()
