#!/usr/bin/env python3
"""Post-processore: Home Aree + pagine Oceani."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

OCEANO_DI = {"cabo-verde": "atlantico", "canarie": "atlantico",
             "grenadine": "caraibi", "guadalupa": "caraibi",
             "martinica": "caraibi", "panama": "caraibi"}

OCEANI = [
 ("atlantico",    "&#127758;", "Oceano Atlantico", "Capo Verde - Canarie"),
 ("caraibi",      "&#127807;", "Mar dei Caraibi", "Grenadine - Guadalupa - Martinica - Panama"),
 ("mar-rosso",    "&#128308;", "Mar Rosso", "in preparazione"),
 ("pacifico",     "&#127758;", "Oceano Pacifico", "in preparazione"),
 ("mediterraneo", "&#9969;",   "Mediterraneo", "in preparazione"),
 ("indiano",      "&#127757;", "Oceano Indiano", "in preparazione"),
]

PAESI = {
 "cabo-verde": ("&#127463;&#127479;", "Capo Verde",
   "9 isole: hub Mindelo, Sal turistica, vulcano Fogo.", "\u2705 v1"),
 "canarie":    ("&#127466;&#127480;", "Canarie",
   "Tenerife, Gran Canaria, Lanzarote e le altre.", "&#128679; v0"),
 "grenadine":  ("&#127483;&#127479;", "Grenadine",
   "Tobago Cays, Bequia, Mustique.", "&#128679; v0"),
 "guadalupa":  ("&#127467;&#127479;", "Guadalupa",
   "Les Saintes, Petite Terre, Cousteau.", "\u2705 v1"),
 "martinica":  ("&#127469;&#127478;", "Martinica",
   "Hub Le Marin.", "\u2705 v1"),
 "panama":     ("&#127477;&#127470;", "Panama",
   "Canale + San Blas.", "&#128679; v0"),
}

def _pcard(href, flag, nome, desc, st):
    return ('<div class="pcard"><div class="pflag">' + flag + '</div>'
            '<a class="pname" href="' + href + '">' + nome + '</a>'
            '<div class="pdesc">' + desc + '</div><div class="pstat">' + st + '</div></div>')

def inject(html):
    if 'id="home"' in html:
        return html

    pid_of = {}
    for m in re.finditer(r'data-country="([^"/]+)"[^>]*data-page="(p\d+)"', html):
        slug = m.group(1)
        if slug not in pid_of:
            pid_of[slug] = m.group(2)

    area_cards = "".join(_pcard("#o-" + oid, em, nm, ds,
        ("apri &#8594;" if any(OCEANO_DI.get(k) == oid for k in PAESI)
         else "in preparazione")) for oid, em, nm, ds in OCEANI)

    home = ('<section id="home" class="page" data-country="">'
            '<h1>Portolano</h1>'
            '<p><strong>L\'intero sistema viene aggiornato con periodicit\u00e0 mensile.</strong></p>'
            '<h2>Aree</h2><div class="paesi-grid">' + area_cards + "</div></section>")

    ocean_secs = []
    for oid, em, nm, ds in OCEANI:
        cards = ""
        for slug, meta in PAESI.items():
            if OCEANO_DI.get(slug) != oid:
                continue
            pid = pid_of.get(slug, "#")
            cards += _pcard("#" + pid, meta[0], meta[1], meta[2], meta[3])
        empty = "" if cards else "<p><em>In preparazione.</em></p>"
        ocean_secs.append(
            '<section id="o-' + oid + '" class="page" data-country="' + oid + '">'
            '<p><a class="backlink" href="#home">&#8592; Aree</a></p>'
            "<h1>" + nm + '</h1><div class="paesi-grid">' + cards + "</div>" + empty + "</section>")

    new_secs = home + "".join(ocean_secs)
    html = html.replace("<main>", "<main>" + new_secs + "\n", 1)

    # sidebar: sostituisci paesi con mari
    nav_old = re.search(r'<div class="nav-countries">.*?</div>', html, re.S)
    if nav_old:
        nav_oc = "".join(f'<a class="navlink country-link" href="#o-{oid}">{em} {nm}</a>'
                        for oid, em, nm, ds in OCEANI)
        html = html[:nav_old.start()] + \
               f'<div class="nav-countries"><a class="navlink country-link" href="#home">Aree</a>{nav_oc}</div>' + \
               html[nav_old.end():]

    # prima pagina = home
    html = re.sub(r"show\('p1'\)", "show('home')", html, count=1)

    return html

for fn in [ROOT / "paesi.html", ROOT / "paesi-mobile.html"]:
    p = Path(fn)
    h = p.read_text(encoding="utf-8")
    nh = inject(h)
    if nh != h:
        p.write_text(nh, encoding="utf-8")

print("DONE aree_inject")
