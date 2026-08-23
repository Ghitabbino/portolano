#!/usr/bin/env python3
"""Post-processore: inietta Home Aree + pagine Oceani negli HTML generati.
Chiamato automaticamente alla fine di build_paesi_html.py."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent

OCEANO_DI = {"cabo-verde": "atlantico", "canarie": "atlantico",
             "grenadine": "caraibi", "guadalupa": "caraibi",
             "martinica": "caraibi", "panama": "caraibi"}

OCEANI = [
 ("atlantico",    "🌊", "Oceano Atlantico", "Capo Verde · Canarie"),
 ("caraibi",      "🌴", "Mar dei Caraibi",  "Grenadine · Guadalupa · Martinica · Panama"),
 ("mar-rosso",    "🔴", "Mar Rosso",        "in preparazione"),
 ("pacifico",     "🌊", "Oceano Pacifico",  "in preparazione"),
 ("mediterraneo", "⛱️", "Mediterraneo",     "in preparazione"),
 ("indiano",      "🌍", "Oceano Indiano",   "in preparazione"),
]

META_PAESI = {
 "cabo-verde": ("🇨🇻", "Capo Verde",
   "9 isole: hub Mindelo, Sal turistica, vulcano Fogo; EASE pre-registrazione.", "✅ v1"),
 "canarie": ("🇪🇸", "Canarie",
   "Tenerife, Gran Canaria, Lanzarote e le altre: marine complete e alisei costanti.", "🚧 v0"),
 "grenadine": ("🇻🇨", "Grenadine",
   "Tobago Cays, Bequia, Mustique: reef, mooring e Basil's Bar.", "🚧 v0"),
 "guadalupa": ("🇬🇵", "Guadalupa",
   "Les Saintes, Petite Terre, Cousteau: gli ancoraggi più belli delle Antille.", "✅ v1"),
 "martinica": ("🇲🇶", "Martinica",
   "Hub Le Marin: base servizi n.1 dei Caraibi orientali.", "✅ v1"),
 "panama": ("🇵🇦", "Panama",
   "Canale + San Blas: transito, Colón, comarca Guna Yala.", "🚧 v0"),
}

def _pcard(href, flag, nome, desc, st):
    return ('<div class="pcard"><div class="pflag">' + flag + '</div>'
            '<a class="pname" href="' + href + '">' + nome + '</a>'
            '<div class="pdesc">' + desc + '</div><div class="pstat">' + st + '</div></div>')

def inject(html):
    if 'id="home"' in html:
        return html  # già iniettato

    # mappa slug -> pid della pagina 00-ingresso (dalla nav)
    pid_of = {}
    for m in re.finditer(r'data-country="([^"/]+)"[^>]*data-page="(p\d+)"', html):
        slug = m.group(1)
        if slug not in pid_of:
            pid_of[slug] = m.group(2)

    # home Aree
    area_cards = "".join(_pcard("#o-" + oid, em, nm, ds,
                                ("apri" if any(OCEANO_DI.get(k) == oid for k in META_PAESI)
                                 else "in preparazione")) for oid, em, nm, ds in OCEANI)
    home = ('<section id="home" class="page" data-country="">'
            '<h1>Portolano</h1>'
            '<p><strong>Metodo</strong>: ogni informazione porta rank di attendibilità '
            '+ data + fonte (quando disponibile).</p>'
            '<p><strong>L\'intero sistema viene aggiornato con periodicità mensile.</strong></p>'
            '<h2>Aree</h2><div class="paesi-grid">' + area_cards + "</div></section>")

    # pagine oceano
    ocean_secs = []
    for oid, em, nm, ds in OCEANI:
        cards = ""
        for slug, meta in META_PAESI.items():
            if OCEANO_DI.get(slug) != oid:
                continue
            pid = pid_of.get(slug, "#")
            cards += _pcard("#" + pid, meta[0], meta[1], meta[2], meta[3])
        empty = "" if cards else '<p><em>In preparazione — contenuti in arrivo.</em></p>'
        ocean_secs.append(
            '<section id="o-' + oid + '" class="page" data-country="">'
            '<p><a class="backlink" href="#home">← Aree</a></p>'
            "<h1>" + nm + '</h1><div class="paesi-grid">' + cards + "</div>" + empty + "</section>")

    # inietta dopo <main>
    new_secs = "".join(ocean_secs)
    html = html.replace("<main>", "<main>" + home + "\n" + new_secs + "\n", 1)

    # CSS backlink
    html = html.replace("</style>",
        ".backlink { color:var(--accent); font-size:13px; text-decoration:none; }\n</style>", 1)

    # prima pagina = home
    html = re.sub(r"show\('p1'\)", "show('home')", html, count=1)

    return html

import re
for fn in [ROOT / "paesi.html", ROOT / "paesi-mobile.html"]:
    p = Path(fn)
    h = p.read_text(encoding="utf-8")
    nh = inject(h)
    if nh != h:
        p.write_text(nh, encoding="utf-8")
        print("✓ aree iniettate:", p.name)

print("DONE aree_inject")
