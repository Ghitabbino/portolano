#!/usr/bin/env python3
"""Genera paesi.html navigabile a partire dai markdown in paesi/ (per paese)."""
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "paesi.html"

def _dms(val, pos, neg):
    v = float(val)
    hemi = pos if v >= 0 else neg
    v = abs(v)
    d = int(v); m_f = (v - d) * 60
    m = int(m_f); sec = int(round((m_f - m) * 60))
    if sec == 60: m += 1; sec = 0
    return f"{d}°{m:02d}'{sec:02d}\" {hemi}"

RE_FRAME = re.compile(r'(<div class="mapframe"[^>]*data-lat="(-?[\d.]+)"[^>]*data-lon="(-?[\d.]+)"[^>]*>)(</div>)')


md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list"])

nav_pages, sections = [], []
page_map = {}  # Path risolto -> id sezione
scope_pid = {}  # (paese, titolo-norm) -> id
queue = []     # (Path, titolo, id, paese)
LABELS_IT = {'cabo-verde': 'Capo Verde', 'costarica': 'Costa Rica',
             'haiti': 'Haiti', 'repubblica-dominicana': 'Repubblica Dominicana',
             'virgin-islands': 'Isole Vergini',
             'trinidad-tobago': 'Trinidad e Tobago', 'turks-caicos': 'Turks e Caicos',
             'st-kitts-nevis': 'St-Kitts e Nevis', 'st-eustatius': 'Sint Eustatius',
             'antigua-barbuda': 'Antigua e Barbuda', 'saint-martin': 'Saint-Martin/Sint Maarten'}

REGIONE_PER_PAESE = {
    # Caraibi
    'anguilla': 'Caraibi', 'antigua-barbuda': 'Caraibi', 'aruba': 'Caraibi',
    'bahamas': 'Caraibi', 'barbados': 'Caraibi', 'belize': 'Caraibi',
    'bonaire': 'Caraibi', 'cayman': 'Caraibi', 'cuba': 'Caraibi',
    'curacao': 'Caraibi', 'dominica': 'Caraibi', 'grenada': 'Caraibi',
    'grenadine': 'Caraibi', 'guadalupa': 'Caraibi', 'honduras': 'Caraibi',
    'giamaica': 'Caraibi', 'haiti': 'Caraibi', 'martinica': 'Caraibi',
    'montserrat': 'Caraibi', 'nicaragua': 'Caraibi', 'panama': 'Caraibi',
    'porto-rico': 'Caraibi', 'saba': 'Caraibi', 'saint-barth': 'Caraibi',
    'saint-martin': 'Caraibi', 'santa-lucia': 'Caraibi', 'st-eustatius': 'Caraibi',
    'st-kitts-nevis': 'Caraibi', 'trinidad-tobago': 'Caraibi', 'turks-caicos': 'Caraibi',
    'repubblica-dominicana': 'Caraibi', 'venezuela': 'Caraibi', 'virgin-islands': 'Caraibi',
    # Atlantico
    'cabo-verde': 'Atlantico', 'canarie': 'Atlantico', 'madeira': 'Atlantico', 'azzorre': 'Atlantico',
    # Pacifico
    'costarica': 'Pacifico',
    # Mediterraneo (futuro)
}

REGIONI_ORDINE = ['Caraibi', 'Atlantico', 'Pacifico', 'Mediterraneo', 'Mar Rosso', 'Oceano Indiano']

# Icona + etichetta per ogni area (menu e card home)
AREA_ICONA = {'Caraibi': '🌴', 'Atlantico': '🌊', 'Pacifico': '🐚', 'Mediterraneo': '⛵',
              'Mar Rosso': '🐠', 'Oceano Indiano': '🏝️'}
AREA_LABEL = {'Caraibi': 'Mar dei Caraibi'}

# Gruppi geografici del Mar dei Caraibi (definizione utente) + coste continentali
MACRO_ORDINE = ['Arcipelago Lucayano', 'Grandi Antille',
                'Isole Sopravento Settentrionali', 'Isole Sopravento Meridionali',
                'Isole Sottovento', 'Isole Caraibiche Occidentali',
                'Isole del Canale e della Costa Continentale',
                'Coste dell’America Centrale']
MACRO_ICONA = {'Arcipelago Lucayano': '🏖️', 'Grandi Antille': '🗺️',
               'Isole Sopravento Settentrionali': '🧭', 'Isole Sopravento Meridionali': '🦜',
               'Isole Sottovento': '☀️', 'Isole Caraibiche Occidentali': '🤿',
               'Isole del Canale e della Costa Continentale': '⚓',
               'Coste dell’America Centrale': '🛶'}
MACRO_CARAIBI = {
    'bahamas': 'Arcipelago Lucayano', 'turks-caicos': 'Arcipelago Lucayano',
    'cuba': 'Grandi Antille', 'haiti': 'Grandi Antille',
    'repubblica-dominicana': 'Grandi Antille',
    'giamaica': 'Grandi Antille', 'porto-rico': 'Grandi Antille',
    'virgin-islands': 'Isole Sopravento Settentrionali', 'anguilla': 'Isole Sopravento Settentrionali',
    'saint-martin': 'Isole Sopravento Settentrionali', 'saint-barth': 'Isole Sopravento Settentrionali',
    'saba': 'Isole Sopravento Settentrionali', 'st-eustatius': 'Isole Sopravento Settentrionali',
    'st-kitts-nevis': 'Isole Sopravento Settentrionali', 'antigua-barbuda': 'Isole Sopravento Settentrionali',
    'montserrat': 'Isole Sopravento Settentrionali', 'guadalupa': 'Isole Sopravento Settentrionali',
    'dominica': 'Isole Sopravento Meridionali', 'martinica': 'Isole Sopravento Meridionali',
    'santa-lucia': 'Isole Sopravento Meridionali', 'grenadine': 'Isole Sopravento Meridionali',
    'grenada': 'Isole Sopravento Meridionali', 'barbados': 'Isole Sopravento Meridionali',
    'aruba': 'Isole Sottovento', 'curacao': 'Isole Sottovento',
    'bonaire': 'Isole Sottovento',
    'cayman': 'Isole Caraibiche Occidentali',
    'trinidad-tobago': 'Isole del Canale e della Costa Continentale',
    'belize': 'Coste dell’America Centrale', 'honduras': 'Coste dell’America Centrale',
    'nicaragua': 'Coste dell’America Centrale', 'panama': 'Coste dell’America Centrale',
    'venezuela': 'Coste dell’America Centrale',
}

# Bandiere per le tessere isola del menu centrale
BANDIERE = {
    'anguilla': '🇦🇮', 'antigua-barbuda': '🇦🇬', 'aruba': '🇦🇼', 'azzorre': '🇵🇹',
    'bahamas': '🇧🇸', 'barbados': '🇧🇧', 'belize': '🇧🇿', 'bonaire': '🇧🇶',
    'cabo-verde': '🇨🇻', 'canarie': '🇪🇸', 'cayman': '🇰🇾', 'costarica': '🇨🇷',
    'cuba': '🇨🇺', 'curacao': '🇨🇼', 'dominica': '🇩🇲', 'giamaica': '🇯🇲',
    'grenada': '🇬🇩', 'grenadine': '🇻🇨', 'guadalupa': '🇬🇵', 'honduras': '🇭🇳',
    'haiti': '🇭🇹', 'madeira': '🇵🇹', 'repubblica-dominicana': '🇩🇴', 'martinica': '🇲🇶', 'montserrat': '🇲🇸',
    'nicaragua': '🇳🇮', 'panama': '🇵🇦', 'porto-rico': '🇵🇷', 'saba': '🇳🇱',
    'saint-barth': '🇧🇱', 'saint-martin': '🇲🇫', 'santa-lucia': '🇱🇨',
    'st-eustatius': '🇳🇱', 'st-kitts-nevis': '🇰🇳', 'trinidad-tobago': '🇹🇹',
    'turks-caicos': '🇹🇨', 'venezuela': '🇻🇪', 'virgin-islands': '🇻🇮',
}

countries = [] # (chiave paese, id copertina)
country_to_region = {}


def strip_zone_suffix(title: str, sub_name: str) -> str:
    """Rimuove il nome zona ripetuto tra parentesi alla fine del titolo (es. 'Clearance (Gran Canaria)')."""
    m = re.search(r"\s*\(([^)]+)\)\s*$", title)
    if not m:
        return title
    inner = m.group(1).strip().lower().replace("-", " ")
    s = sub_name.lower().replace("-", " ")
    if inner == s or inner.startswith(s + " di ") or inner.startswith(s + " "):
        return re.sub(r"\s*\([^)]+\)\s*$", "", title)
    return title


# Icone per le zone/isole interne (uniche, con attinenza al luogo)
ZONA_ICONA = {
    'cabo-verde/sal': '🏖️', 'cabo-verde/boa-vista': '🏜️', 'cabo-verde/maio': '🌿',
    'cabo-verde/santiago': '🏛️', 'cabo-verde/fogo': '🌋', 'cabo-verde/brava': '💐',
    'cabo-verde/sao-nicolau': '⛰️', 'cabo-verde/sao-vicente': '🎵',
    'cabo-verde/santo-antao': '🥾',
    'canarie/tenerife': '🗻', 'canarie/gran-canaria': '⛳', 'canarie/fuerteventura': '🏄',
    'canarie/lanzarote': '🔥', 'canarie/la-gomera': '🌲', 'canarie/la-palma': '🍌',
    'canarie/la-graciosa': '🚲', 'canarie/el-hierro': '🦎',
    'grenadine/bequia': '🐋', 'grenadine/mustique': '💎', 'grenadine/canouan': '🏌️',
    'grenadine/mayreau': '⛱️', 'grenadine/st-vincent': '🎬',
    'grenadine/tobago-cays': '🐢', 'grenadine/union-island': '🪁',
    'panama/canale': '🚢', 'panama/san-blas': '🐬',
}
zona_icons={}

def norm_title(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def register(md_path: Path, title: str, country: str = "", in_nav: bool = True):
    pid = f"p{len(queue) + 1}"
    page_map[md_path.resolve()] = pid
    title = re.sub(r"\s*\{#[^}]*\}", "", title).strip()
    queue.append((md_path, title, pid, country))
    scope_pid[(country, norm_title(title))] = pid
    if in_nav:
        nav_pages.append(f'<a class="navlink pagelink" data-country="{country}" '
                         f'href="#{pid}" data-page="{pid}">{title}</a>')


def render(md_path: Path, title: str, sec_id: str, country: str = ""):
    text = md_path.read_text(encoding="utf-8")

    def fix_link(m):
        target = m.group(1)
        if target.startswith(("http://", "https://", "#")):
            return m.group(0)
        resolved = (md_path.parent / target).resolve()
        if not resolved.exists():
            resolved = (ROOT / target).resolve()
        if resolved in page_map:
            return f"](#{page_map[resolved]})"
        print(f"ATTENZIONE: link non risolto '{target}' in {md_path.name}")
        return m.group(0)

    text = re.sub(r"\]\(([^)]+\.md)\)", fix_link, text)
    text = re.sub(r'href="([^"]+\.md)"', lambda m: f'href="#{page_map.get((md_path.parent / m.group(1)).resolve(), m.group(1))}"'
                  if (md_path.parent / m.group(1)).resolve() in page_map else m.group(0), text)

    # marker mappa -> id sezione della pagina con titolo corrispondente (link dal popup)
    def norm(s):
        return re.sub(r"[^a-z0-9]", "", s.lower())
    title_pid = {}
    for _p, _t, _id, _c in queue:
        title_pid[norm(_t)] = _id

    def link_markers(m):
        try:
            pts = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        for p_ in pts:
            if len(p_) >= 4:
                continue
            lbl = norm(str(p_[2]))
            if not lbl:
                continue
            scoped = [v for k, v in scope_pid.items()
                      if k[1] == lbl and k[0] == country]
            if scoped:
                p_.append(scoped[0])
            else:
                globl = [v for k, v in title_pid.items() if k == lbl]
                if len(globl) == 1:
                    p_.append(globl[0])
                # 0 o multipli senza scope: resta senza link, niente pagine sbagliate
        out = json.dumps(pts, ensure_ascii=False).replace("'", "\u2019")
        return "data-markers='" + out + "'"

    text = re.sub(r"data-markers='([^']+)'", link_markers, text)
    md.reset()
    html = md.convert(text)
    html = re.sub(r'<a href="(http[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', html)
    def _tel(m):
        s=m.group(0)
        digits=sum(ch.isdigit() for ch in s)
        return f'<span class="tel">{s}</span>' if digits>=9 else s
    html=re.sub(r'\+?\d[\d ]{7,}\d', _tel, html)
    html=re.sub(r'\b\d{3} [\d ]{5,}\d(?=[^\d])', _tel, html)
    html = re.sub(r"<table>(.*?)</table>", r'<div class="tw"><table>\1</table></div>', html, flags=re.S)
    html = re.sub(r"\s*<h1>[^<]*</h1>", "", html, count=1)
    # h1 con attributo attr_list ({#anc-x}): rimuovi ma conserva l'id per i link dalle mappe
    attrs=""
    mh=re.search(r"<h1([^>]*)>.*?</h1>", html, flags=re.S)
    if mh:
        attrs=mh.group(1)
        if "id=" not in attrs: attrs=""
        html=html[:mh.start()]+html[mh.end():]
        html=re.sub(r"^\s+","",html)
    badge=""
    if country:
        place=(country.split("/")[-1] if "/" in country else country)
        place=place.replace("-"," ").title()
        # evita doppione: se il titolo finisce con "(...stesso luogo...)" lo ripulisce
        mt=re.search(r"\s*\(([^)]*)\)\s*$", title)
        if mt and place.lower() in mt.group(1).lower():
            title=title[:mt.start()].rstrip()
            if not title:
                title=place
        badge=f'<a class="loc-badge" data-back="1" href="#" title="Torna indietro di un livello">← {place}</a>'
    if 'ancoraggi' in title.lower() and country:
        html=('<blockquote><b>⚠️ Coordinate indicative</b> — tutte le posizioni sono espresse '
              'in <b>gradi decimali, datum WGS84</b>, e segnalano in modo approssimativo la '
              'rada o l\u2019ancoraggio, non punti di precisione. Confermare sempre con carta '
              'nautica ufficiale WGS84 e osservazione in loco. '
              '<b>Nessuna responsabilità per l\u2019uso di questi dati: la sicurezza resta al Comandante.</b></blockquote>'
              +html)
    def _add_dms(m):
        return m.group(1)+m.group(4)+(
            f'<div class="dms">📍 {_dms(m.group(2),"N","S")} {_dms(m.group(3),"E","W")} · WGS84</div>')
    html=RE_FRAME.sub(_add_dms,html)
    stem=md_path.stem
    hook=f'<span id="{stem}"></span>' if re.match(r'^(anc|rist)-',stem) else ''
    sections.append(f'<section id="{sec_id}" class="page" data-country="{country}">'
                    f'{hook}{badge}<h1{attrs}>{title}</h1>{html}</section>')


register(ROOT / "00-indice.md", "Aree")
register(ROOT / "chi-siamo.md", "Chi siamo", country="", in_nav=False)
CHI_PID = queue[-1][2]

NON_PAESE = {'controllo', 'fonti', 'tools', 'assets', 'mappe', 'gruppi'}
for country_dir in sorted(p for p in ROOT.iterdir() if p.is_dir()
                          and not p.name.startswith(".")
                          and p.name not in NON_PAESE):
    pages = sorted(country_dir.glob("*.md"))
    if not pages:
        continue
    key = country_dir.name
    start = len(queue)
    for f in pages:
        first = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        title = re.sub(r"^\d+\s*[—-]\s*", "", first)
        register(f, title, country=key, in_nav=True)
    # schede in sottocartelle: ristoranti/ = schede fuori nav; altre cartelle = ZONE del paese (albero nella stessa voce)
    has_groups = any(p.is_dir() and not p.name.startswith(".") and p.name != "ristoranti"
                     and any(p.glob("*.md")) for p in country_dir.iterdir())
    for sub in sorted(p for p in country_dir.iterdir() if p.is_dir() and not p.name.startswith(".")):
        if sub.name in ("ristoranti", "ancoraggi"):
            for f in sorted(sub.glob("*.md")):
                first = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
                title = re.sub(r"^\d+\s*[—-]\s*", "", first)
                title = re.sub(r"\s*\{#[^}]*\}", "", title).strip()
                register(f, title, country=key, in_nav=False)
            continue
        gpages = sorted(sub.glob("*.md"))
        if not gpages:
            continue
        gkey = key + "/" + sub.name
        zona_icons[gkey] = ZONA_ICONA.get(gkey, "🐬")
        hpos = len(nav_pages)
        for f in gpages:
            first = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
            title = re.sub(r"^\d+\s*[—-]\s*", "", first)
            title = re.sub(r"\s*\{#[^}]*\}", "", title).strip()
            title = strip_zone_suffix(title, sub.name)
            register(f, title, country=gkey, in_nav=True)
        if has_groups:
            lbl = sub.name.replace("-", " ").title()
            pid = queue[len(queue) - len(gpages)][2]
            zic = ZONA_ICONA.get(gkey, "🐬")
            nav_pages.insert(hpos, f'<a style="display:none" class="navlink zonelink" data-country="{gkey}" '
                                  f'data-page="{pid}" href="#{pid}"><span class="zic">{zic}</span>{lbl}</a>')
        for sub2 in sorted(p for p in sub.iterdir() if p.is_dir() and not p.name.startswith(".")):
            for f in sorted(sub2.glob("*.md")):
                first = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
                title = re.sub(r"^\d+\s*[—-]\s*", "", first)
                title = re.sub(r"\s*\{#[^}]*\}", "", title).strip()
                register(f, title, country=gkey, in_nav=False)
    countries.append((key, queue[start][2]))
    country_to_region[key] = REGIONE_PER_PAESE.get(key, 'Altro')

for md_path, title, sec_id, country in queue:
    render(md_path, title, sec_id, country)

# Build region -> countries mapping
region_to_countries = {}
for ctry, reg in country_to_region.items():
    region_to_countries.setdefault(reg, []).append(ctry)

def paese_label(k: str) -> str:
    if k in LABELS_IT:
        return LABELS_IT[k]
    part = {'e', 'di', 'del', 'della', 'delle', 'dei', 'degli', 'a', 'da',
            'in', 'su', 'per', 'con', 'tra', 'fra'}
    ws = base = k.split("/")[-1].split("-")
    ws = [w.capitalize() if i == 0 or w not in part else w
          for i, w in enumerate(base)]
    return " ".join(ws)

albero_regioni = []
for reg in REGIONI_ORDINE:
    paesi_reg = sorted(k for k, _ in countries if country_to_region.get(k) == reg)
    if reg == 'Caraibi':
        subs = [{'k': f'Caraibi/{m}', 'l': m, 'i': MACRO_ICONA.get(m, '🗺️'),
                 'p': [k for k in paesi_reg if MACRO_CARAIBI.get(k) == m]}
                for m in MACRO_ORDINE
                if any(MACRO_CARAIBI.get(k) == m for k in paesi_reg)]
        diretti = [k for k in paesi_reg if k not in MACRO_CARAIBI]
    else:
        subs, diretti = [], paesi_reg
    # Mediterraneo: niente paesi ancora → includiamo comunque come "in arrivo"
    pronta = bool(paesi_reg)
    albero_regioni.append({'k': reg, 'l': AREA_LABEL.get(reg, reg),
                           'i': AREA_ICONA.get(reg, '🌊'),
                           'subs': subs, 'p': diretti, 'ready': pronta})

ALBERO = {
    'regions': albero_regioni,
    'cover': {k: pid for k, pid in countries},
    'lbl': {k: paese_label(k) for k, _ in countries},
    'flag': {k: BANDIERE.get(k, '🏝️') for k, _ in countries},
    'mlbl': {f'Caraibi/{m}': m for m in MACRO_ORDINE},
    'zona': zona_icons,
    'macroOf': {k: m for k, m in MACRO_CARAIBI.items()
                if country_to_region.get(k) == 'Caraibi'},
    'regionOf': {**{f'Caraibi/{m}': 'Caraibi' for m in MACRO_ORDINE},
                 **{k: r for k, r in country_to_region.items()}},
}

nav_html = ('<div id="aree-head" title="Tutti i mari e gli oceani">🌍 Aree</div>'
            '<div id="navtitle"></div>'
            '<div id="tree"></div>'
            '<div class="nav-pages">' + "\n".join(nav_pages) + "</div>")

TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>SailTropics · Portolano</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 52'%3E%3Ccircle cx='19' cy='20' r='10' fill='%23F0705A'/%3E%3Cpath d='M28 2 C41 13 47 30 44 48 L28 48 Z' fill='%231E5A9E'/%3E%3Cpath d='M6 48 q10 -8 22 -2 t 28 1' stroke='%232BB3A3' stroke-width='6' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="stylesheet" href="assets/leaflet.css">
<style>
:root { --bg:#0f1720; --panel:#16222e; --ink:#dbe7f1; --muted:#8aa2b5;
        --accent:#4db6ac; --line:#24384a; }
* { box-sizing:border-box; }
body { margin:0; display:flex; min-height:100vh; background:var(--bg); color:var(--ink);
       font:15px/1.55 -apple-system, "Segoe UI", Roboto, sans-serif; }
aside { width:290px; flex-shrink:0; background:var(--panel); border-right:1px solid var(--line);
        padding:18px 14px; position:sticky; top:0; height:100vh; overflow-y:auto; }
aside h1 { font-size:16px; margin:0 0 12px; color:var(--accent); }
#search { width:100%; padding:8px 10px; margin-bottom:14px; border-radius:8px;
          border:1px solid var(--line); background:#0b131b; color:var(--ink); font-size:14px; }
.navlink { display:block; padding:7px 10px; border-radius:8px; color:var(--ink);
           text-decoration:none; font-size:15.5px; cursor:pointer; line-height:1.7; }
.navlink:hover { background:#1d3040; }
.navlink.active { background:var(--accent); color:#06231f; font-weight:600; }
#aree-head { display:flex; align-items:center; gap:8px; font-weight:800; font-size:15px;
             color:var(--accent); cursor:pointer; padding:7px 10px; border-radius:8px;
             margin:2px 0 6px; }
#aree-head:hover { background:#1d3040; }
#navtitle { display:none; align-items:center; gap:10px; padding:9px 12px; margin:0 0 8px;
            background:#101b26; border:1px solid var(--accent); border-radius:10px;
            cursor:pointer; }
#navtitle:hover { background:#14222f; }
#navtitle .ic { font-size:26px; line-height:1; flex-shrink:0; width:auto; text-align:center; }
#navtitle .tx { font-weight:800; font-size:21px; color:var(--accent); flex:1;
                min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
#navtitle-c { display:none; align-items:center; gap:14px; padding:14px 18px;
              margin:6px 0 20px; background:#101b26; border:1px solid var(--line);
              border-left:5px solid var(--accent); border-radius:12px; cursor:pointer; }
#navtitle-c:hover { background:#14222f; }
#navtitle-c .ic { font-size:38px; line-height:1; flex-shrink:0; width:auto; text-align:center; }
#navtitle-c .tx { font-weight:800; font-size:27px; color:var(--accent); flex:1;
                  min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
#navtitle .car, #navtitle-c .car { color:var(--muted); font-weight:400; font-size:20px; }
#tree .titem { display:flex; align-items:center; gap:9px; border-radius:8px; cursor:pointer;
               color:var(--accent); text-decoration:none; font-weight:700; font-size:15px;
               padding:8px 10px; }
#tree .titem:hover { background:#1d3040; }
#tree .titem .car { margin-left:auto; color:var(--muted); font-weight:400; }
#tree .titem.reg { margin-top:6px; background:#101b26; border:1px solid var(--line);
                   border-radius:10px; padding:10px 12px; }
#tree .titem.reg:hover { background:#14222f; border-color:var(--accent); }
#tree .titem.mac { padding-left:26px; margin-top:8px; }
#tree .titem.cty { padding-left:42px; }
#tree .titem .ic { font-size:18px; line-height:1; flex-shrink:0; width:24px; text-align:center; }
#tree .titem .tx { flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.soon, .area-card .soon { font-size:11px; font-weight:600; letter-spacing:.04em;
  color:var(--accent); border:1px solid var(--line); border-radius:20px;
  padding:3px 10px; white-space:nowrap; }
#tree .titem.reg.dis { cursor:default; opacity:.8; }
#tree .titem.reg.dis:hover { background:#101b26; border-color:var(--line); }
.area-card.soon { opacity:.85; cursor:default; }
.area-card.soon:hover { border-color:var(--line); background:#101b26; }
.zonelink { font-weight:800; font-size:15.5px; color:var(--accent); margin-top:10px; }
.zonelink .zic { margin-right:7px; }
.loc-badge { color:var(--accent); font-weight:800; font-size:26px;
             letter-spacing:.02em; margin:0 0 10px; display:inline-block;
             cursor:pointer; text-decoration:none; border-bottom:2px solid transparent; }
.loc-badge:hover { border-bottom-color:var(--accent); }
.loc-badge .bk { font-size:15px; font-weight:700; opacity:.85; }
.pagelink { font-size:15px; padding-left:20px; line-height:1.45; }
#brand-c { display:flex; align-items:center; flex-wrap:wrap; gap:4px 16px;
           margin:10px 0 24px; padding-bottom:18px; border-bottom:1px solid var(--line); }
#brand-c .bw { font-size:27px; font-weight:800; letter-spacing:.01em; color:#fff; line-height:1; }
#brand-c .bt2 { color:var(--accent); }
#brand-c .bs { font-size:11px; color:var(--accent); letter-spacing:.08em;
               text-transform:uppercase; margin-left:auto; text-align:right; }
body.searching #navtitle, body.searching #tree,
body.searching #navgrid, body.searching #disc-home, body.searching #navtitle-c { display:none!important; }
#disc-home { display:none; border:1px solid #ffb74d; background:rgba(255,183,77,.07);
             border-radius:12px; padding:12px 16px; font-size:13px; line-height:1.6;
             color:var(--ink); margin:2px 0 14px; }
#disc-home b { color:#ffb74d; }
#navgrid { display:none; grid-template-columns:repeat(auto-fill,minmax(250px,1fr));
           gap:16px; margin:8px 0 16px; }
#navgrid .fi { font-size:42px; }
#navgrid .area-card .soon { margin-top:2px; }
main { flex:1; min-width:0; padding:clamp(30px,3.5vw,58px) clamp(14px,2.5vw,44px) 44px; font-size:18px; }
.page { display:none; }
.page.visible { display:block; }
h1,h2,h3 { color:#fff; line-height:1.25; }
h3 { font-size:22px; }
h2 { border-bottom:1px solid var(--line); padding-bottom:6px; margin-top:34px; font-size:27px; }
.tw { overflow-x:auto; margin:14px 0; border-radius:8px; font-size:17.5px; }
.dms { font-size:11px; color:var(--muted); margin:-6px 0 14px; letter-spacing:.03em; }
.aree-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:16px;
             margin:26px 0 12px; }
.area-card { display:flex; flex-direction:column; gap:7px; align-items:center;
             border:1px solid var(--line); border-radius:14px; background:#101b26;
             padding:18px 16px; cursor:pointer; text-decoration:none; text-align:center; }
.area-card:hover { border-color:var(--accent); background:#132230; }
.area-card .ic { font-size:32px; line-height:1; }
.area-card .nm { font-size:21px; font-weight:800; font-size:17px; color:var(--accent); }
.area-card .ds { font-size:11.5px; color:var(--accent); opacity:.72; line-height:1.55; }
.paesi-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:12px; margin:14px 0; }
.pcard { min-width:0; overflow-wrap:anywhere; }
.pcard { border:1px solid var(--line); border-radius:10px; background:#101b26;
         padding:12px 10px; display:flex; flex-direction:column; align-items:center; gap:4px; }
.pcard:hover { border-color:var(--accent); }
.pflag { font-size:28px; line-height:1; }
.pname { font-weight:700; font-size:13.5px; color:var(--accent); text-decoration:none; }
.pname:hover { text-decoration:underline; }
.pdesc { font-size:11.5px; color:var(--ink); text-align:justify; }
.pstat { font-size:10.5px; color:var(--muted); }
table { border-collapse:collapse; width:100%; min-width:900px; margin:0; font-size:15px; }
th,td { border:1px solid var(--line); padding:10px 14px; text-align:left; vertical-align:top;
        overflow-wrap:break-word; word-break:normal; hyphens:none; }
td { font-variant-numeric:tabular-nums; line-height:1.5; }
/* i numeri di telefono restano su una riga leggibile */
td .tel, td a[href^="tel"] { white-space:nowrap; }
.tw { -webkit-overflow-scrolling:touch; }
td { text-align:justify; }
.tw code { background:none; border:none; padding:0; border-radius:0;
           font-family:inherit; font-size:inherit; color:#ffd54f; }
th { background:#1d3040; color:#fff; white-space:nowrap; }
tr:nth-child(even) td { background:#131e29; }
img { max-width:100%; }
pre code { display:block; padding:12px; overflow-x:auto; }
code { background:#0b131b; border:1px solid var(--line); padding:1px 5px; border-radius:5px;
       font-size:13px; color:#ffd54f; }
blockquote { border-left:3px solid #ffb74d; margin:14px 0; padding:4px 16px;
             background:#131e29; color:var(--muted); }
a { color:var(--accent); }
hr { border:none; border-top:1px solid var(--line); margin:26px 0; }
li { margin:3px 0; }
.mapframe { width:100%; height:360px; border:1px solid var(--line); border-radius:12px;
            margin:14px 0 4px; background:#0b131b; position:relative; z-index:0; }
.mapcap { color:var(--muted); font-size:12.5px; margin:0 0 18px; }
.leaflet-control-attribution { background:rgba(11,19,27,.8)!important; color:var(--muted)!important; font-size:10px!important; }
.leaflet-control-attribution a { color:var(--accent)!important; }
.leaflet-bar a, .leaflet-control-layers-toggle { background-color:#16222e!important; color:var(--ink)!important; }
.leaflet-control-layers { background:#16222e!important; color:var(--ink)!important; border:1px solid var(--line)!important; border-radius:8px!important; }
.mapframe:fullscreen, .mapframe:-webkit-full-screen { border-radius:0; height:100vh; }
.anch-label { background:rgba(10,20,30,.82)!important; color:#fff!important; border:none!important;
              font-weight:600; font-size:11.5px; padding:2px 8px; border-radius:8px;
              box-shadow:0 1px 5px rgba(0,0,0,.55); white-space:nowrap; }
.anch-label::before { display:none!important; }
.anch-ic{background:none;border:none;}
.anch-ic .ic{font-size:24px;line-height:26px;text-shadow:0 1px 4px rgba(0,0,0,.65);}
@media (max-width:800px){ aside{position:static;width:auto;height:auto;} body{flex-direction:column;} }
</style>
</head>
<body>
<aside>
  <div id="home-link" style="cursor:pointer;display:flex;align-items:center;gap:9px;margin:0 0 2px">
<svg viewBox="0 0 64 52" width="42" height="36" aria-hidden="true" style="flex-shrink:0">
<circle cx="19" cy="20" r="9" fill="#F0705A"/>
<path d="M28 4 C40 14 46 30 43 46 L28 46 Z" fill="#1E5A9E"/>
<path d="M26 12 L26 46 L14 46 C18 34 21 22 26 12 Z" fill="#16406F"/>
<path d="M6 47 q9 -7 20 -2 t 30 1" stroke="#2BB3A3" stroke-width="4.5" fill="none" stroke-linecap="round"/>
<path d="M12 51 q8 -5 17 -1 t 22 0" stroke="#57CFC0" stroke-width="3.5" fill="none" stroke-linecap="round"/>
</svg>
<span style="font-size:20px;font-weight:700;letter-spacing:.01em;color:var(--ink)">Sail<span style="color:var(--accent)">Tropics</span></span>
</div>
<div style="font-size:11px;color:var(--muted);margin:0 0 12px;letter-spacing:.08em;text-transform:uppercase">Portolano</div>
  <input id="search" type="search" placeholder="Cerca paese o pagina…">
  <nav id="nav">__NAV__</nav>
</aside>
<main>
<div id="brand-c">
<svg viewBox="0 0 64 52" width="46" height="40" aria-hidden="true" style="flex-shrink:0">
<circle cx="19" cy="20" r="9" fill="#F0705A"/>
<path d="M28 4 C40 14 46 30 43 46 L28 46 Z" fill="#1E5A9E"/>
<path d="M26 12 L26 46 L14 46 C18 34 21 22 26 12 Z" fill="#16406F"/>
<path d="M6 47 q9 -7 20 -2 t 30 1" stroke="#2BB3A3" stroke-width="4.5" fill="none" stroke-linecap="round"/>
</svg>
<span class="bw">Sail<span class="bt2">Tropics</span></span>
<span class="bs">Un portolano amatoriale fatto da velisti per i velisti</span>
</div>
<div id="disc-home">
<b>⚠️ Portolano amatoriale — sito non commerciale.</b>
Informazioni e coordinate provengono da fonti pubbliche e segnalazioni di naviganti:
sono <b>indicative</b>, possono essere imprecise, superate o errate e <b>non sostituiscono</b>
la cartografia ufficiale, le guide ufficiali né il controllo diretto in loco.
Ancoraggi, accessi, regolamenti e condizioni del mare vanno sempre verificati dal Comandante
prima e durante la navigazione. <b>Ogni decisione e responsabilità è esclusivamente del Comandante.</b>
Gli autori non assumono alcuna responsabilità per danni, perdite, sanzioni o incidenti
derivanti dall'uso di questi contenuti.
</div>
<div id="navtitle-c"></div>
<div id="navgrid"></div>
__SECTIONS__
</main>
<script>
const plinks=[...document.querySelectorAll('.pagelink')];
const TREE=__TREE__;
let current='__FIRST__', state='';
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');}
function chain(st){
  if(!st)return[];
  if(st.startsWith('r:'))return[{t:'r',k:st}];
  if(st.startsWith('m:')){
    const mk=st.slice(2);
    return[{t:'r',k:'r:'+TREE.regionOf[mk]},{t:'m',k:st}];
  }
  if(st.includes('/'))return chain(st.split('/')[0]).concat([{t:'z',k:st}]);
  const c=[{t:'r',k:'r:'+TREE.regionOf[st]}];
  if(TREE.macroOf[st])c.push({t:'m',k:'m:'+TREE.regionOf[st]+'/'+TREE.macroOf[st]});
  return c.concat([{t:'c',k:st}]);
}
const PARTICOLI=['e','di','del','della','delle','dei','degli','d','a','da','in','su','per','con','tra','fra'];
function capWord(w){return w.toLowerCase().split(/([\u2019'])/).map(function(seg,i){
  if(i%2)return seg;
  return seg.charAt(0).toUpperCase()+seg.slice(1);}).join('');}
function capIt(s){return s.split(/(\\s+)/).map(function(w,i){
  if(/^\\s+$/.test(w))return w;
  const low=w.toLowerCase();
  if(i>1&&PARTICOLI.indexOf(low)>=0)return low;
  return capWord(low);
}).join('');}
function lbl(n){
  const k=n.k.replace(/^[rm]:/,'');
  if(n.t==='c')return TREE.lbl[k]||capIt(k.replace(/-/g,' '));
  if(n.t==='r'){const r=TREE.regions.find(x=>x.k===k);return r?r.l:k;}
  if(n.t==='m')return (TREE.mlbl&&TREE.mlbl[k])||capIt((k.includes('/')?k.split('/').pop():k).replace(/-/g,' '));
  return capIt(k.split('/').pop().replace(/-/g,' '));
}
function parentOf(st){
  if(!st)return null;
  const ch=chain(st),up=ch[ch.length-2];
  return up?up.k:'';
}
function flagTile(k){
  return '<a class="area-card" data-open="'+esc(k)+'"><span class="ic fi">'+(TREE.flag[k]||'🏝️')
    +'</span><span class="nm">'+esc(TREE.lbl[k]||k)+'</span></a>';
}
function renderNav(){
  const ch=chain(state);
  const cur=ch[ch.length-1];
  const nt=document.getElementById('navtitle'),tr=document.getElementById('tree');
  let tit='';
  if(ch.length){
    const n=ch[ch.length-1];let ic='';
    if(n.t==='r'){const rr=TREE.regions.find(x=>'r:'+x.k===n.k);ic=rr?rr.i:'🌊';}
    else if(n.t==='m'){ic='🏝️';
      for(const rr of TREE.regions){const s=rr.subs.find(x=>x.k===n.k.slice(2));if(s){ic=s.i||ic;break;}}}
    else if(n.t==='c')ic=TREE.flag[n.k]||'🏝️';
    else ic=TREE.zona[n.k]||'\u2693';
    tit='<span class="ic">'+ic+'</span><span class="tx">'+esc(lbl(n))
       +'</span><span class="car">‹</span>';
    nt.innerHTML=tit;nt.style.display='flex';
  }else{nt.innerHTML='';nt.style.display='none';}
  let h='';
  if(!state){
    h=TREE.regions.map(r=>{
      if(r.ready===false)
        return '<a class="titem reg dis"><span class="ic">'+r.i+'</span><span class="tx">'
          +esc(r.l)+'</span><span class="soon">in preparazione</span></a>';
      return '<a class="titem reg" data-go="r:'+esc(r.k)+'">'
        +'<span class="ic">'+r.i+'</span><span class="tx">'+esc(r.l)+'</span>'
        +' <span class="car">›</span></a>';
    }).join('');
  }else{
    if(cur.t==='r'){
      const r=TREE.regions.find(x=>'r:'+x.k===cur.k);
      if(r)h=r.subs.map(s=>'<a class="titem mac" data-go="m:'+esc(s.k)+'"><span class="ic">'
        +(s.i||'🏝️')+'</span><span class="tx">'+esc(s.l)+'</span><span class="car">›</span></a>').join('')
        +r.p.map(k=>'<a class="titem cty" data-open="'+esc(k)+'"><span class="ic">'+(TREE.flag[k]||'🏝️')
        +'</span><span class="tx">'+esc(TREE.lbl[k])+'</span><span class="car">›</span></a>').join('');
    }else if(cur.t==='m'){
      for(const r of TREE.regions){
        const s=r.subs.find(x=>x.k===cur.k.slice(2));
        if(s){h=s.p.map(k=>'<a class="titem cty" data-open="'+esc(k)+'"><span class="ic">'+(TREE.flag[k]||'🏝️')
          +'</span><span class="tx">'+esc(TREE.lbl[k])+'</span><span class="car">›</span></a>').join('');break;}
      }
    }
  }
  tr.innerHTML=h;
  tr.querySelectorAll('[data-go]').forEach(el=>el.addEventListener('click',()=>go(el.dataset.go)));
  tr.querySelectorAll('[data-open]').forEach(el=>el.addEventListener('click',()=>show(TREE.cover[el.dataset.open])));
  const ng=document.getElementById('navgrid');
  const ctry=(state&&!/^[rm]:/.test(state))?state:'';
  let g='';
  if(!state){
    g=TREE.regions.map(r=>r.ready===false
      ?'<a class="area-card soon"><span class="ic">'+r.i+'</span><span class="nm">'+esc(r.l)
        +'</span><span class="soon">in preparazione</span></a>'
      :'<a class="area-card" data-go="r:'+esc(r.k)+'"><span class="ic">'+r.i
        +'</span><span class="nm">'+esc(r.l)+'</span><span class="ds">'
        +esc(r.subs.length?r.subs.map(s=>s.l).join(' · ')
                          :r.p.map(k=>TREE.lbl[k]).join(' · '))+'</span></a>').join('');
  }else if(cur.t==='r'){
    const r=TREE.regions.find(x=>'r:'+x.k===cur.k);
    if(r)g=r.subs.map(s=>'<a class="area-card" data-go="m:'+esc(s.k)+'"><span class="ic">'+(s.i||'🗺️')
        +'</span><span class="nm">'+esc(s.l)+'</span><span class="ds">'
        +esc(s.p.map(k=>TREE.lbl[k]).join(' · '))+'</span></a>').join('')
      +r.p.map(flagTile).join('');
  }else if(cur.t==='m'){
    for(const rr of TREE.regions){
      const s=rr.subs.find(x=>x.k===cur.k.slice(2));
      if(s){g=s.p.map(flagTile).join('');break;}
    }
  }else if(ctry&&!ctry.includes('/')){
    const zs=[...document.querySelectorAll('.zonelink')]
      .filter(z=>z.dataset.country.split('/')[0]===ctry&&z.dataset.country!==ctry);
    if(zs.length)g=zs.map(z=>{
      var lbl=z.textContent.trim(),zi=TREE.zona[z.dataset.country];
      if(zi&&lbl.indexOf(zi)===0)lbl=lbl.slice(zi.length).trim();
      return '<a class="area-card" data-openzone="'+esc(z.dataset.country)
      +'" data-page="'+esc(z.dataset.page)+'"><span class="ic">'+(zi||'🐬')
      +'</span><span class="nm">'+esc(lbl)+'</span></a>';}).join('');
  }
  ng.innerHTML=g;
  ng.style.display=g?'grid':'none';
  const ntc=document.getElementById('navtitle-c');
  if(g&&state){ntc.innerHTML=tit;ntc.style.display='flex';}
  else{ntc.innerHTML='';ntc.style.display='none';}
  document.getElementById('disc-home').style.display=(!state)?'block':'none';
  if(g&&!ctry)document.querySelectorAll('.page').forEach(x=>x.classList.remove('visible'));
  plinks.forEach(l=>l.style.display=(ctry&&l.dataset.country===ctry)?'':'none');
  document.querySelectorAll('.zonelink').forEach(l=>{
    const lk=l.dataset.country;let v=false;
    if(ctry)v=ctry.includes('/')?(lk===ctry):(lk.split('/')[0]===ctry);
    l.style.display=v?'':'none';
  });
}
function go(k){
  if(k===''){state='';renderNav();window.scrollTo(0,0);
    if(typeof toggleNav==='function')toggleNav(false);return;}
  state=k;renderNav();
}
function setState(s){state=s;renderNav();}
function show(id){
  current=id;
  const p=document.getElementById(id);
  document.querySelectorAll('.page').forEach(x=>x.classList.toggle('visible',x===p));
  if(p&&p.dataset.special){
    document.getElementById('navgrid').style.display='none';
    document.getElementById('disc-home').style.display='none';
    window.scrollTo(0,0);
    return;
  }
  setState((p&&p.dataset.country)||'');
  window.scrollTo(0,0);
  if(p)initMaps(p);
}
function initMaps(root){
  if(typeof L==='undefined')return;
  const isAnc=/ancoraggi/i.test((root.querySelector('h1')||{textContent:''}).textContent||'')
            || !!root.querySelector('h1[id^="anc"]');
  const ancIcon=L.divIcon({className:'anch-ic',
    html:'<div style="filter:drop-shadow(0 1px 4px rgba(0,0,0,.85))"><svg viewBox=\"0 0 24 24\" width=\"26\" height=\"26\"><path d=\"M12 2a3 3 0 0 1 1 5.83V9h4v2h-4v8.9A8 8 0 0 0 19.7 14H22a10 10 0 0 1-20 0h2.3A8 8 0 0 0 11 19.9V11H7V9h4V7.83A3 3 0 0 1 12 2z\" fill=\"#FFD54F\" stroke=\"#0b131b\" stroke-width=\"1.4\"/></svg></div>',
    iconSize:[26,26],iconAnchor:[13,21]});
  root.querySelectorAll('.mapframe:not(.lmap)').forEach(el=>{
    el.classList.add('lmap');
    const slug=el.dataset.slug;
    const minz=+(el.dataset.minz||12), maxz=+(el.dataset.maxz||15);
    let pts=null,zones=null;
    if(el.dataset.markers){try{pts=JSON.parse(el.dataset.markers)}catch(e){pts=null}}
    if(el.dataset.zones){try{zones=JSON.parse(el.dataset.zones)}catch(e){zones=null}}
    const lat=+el.dataset.lat, lon=+el.dataset.lon;
    const m=L.map(el,{maxBoundsViscosity:1});
    let HOMEB=null;const HOME=[lat,lon];const HOMEZ=14;
    const FS=L.Control.extend({options:{position:'topleft'},onAdd(){
      const d=L.DomUtil.create('div','leaflet-bar');
      const a=L.DomUtil.create('a','',d);
      a.href='#'; a.innerHTML='⛶'; a.title='Schermo intero'; a.style.fontSize='17px'; a.style.lineHeight='26px';
      L.DomEvent.on(a,'click',e=>{
        L.DomEvent.stop(e);
        if(document.fullscreenElement||document.webkitFullscreenElement){
          (document.exitFullscreen||document.webkitExitFullscreen).call(document);
        }else{
          (el.requestFullscreen||el.webkitRequestFullscreen).call(el);
        }
      });
      return d;
    }});
    m.addControl(new FS());
    document.addEventListener('fullscreenchange',()=>setTimeout(()=>m.invalidateSize(),150));
    document.addEventListener('webkitfullscreenchange',()=>setTimeout(()=>m.invalidateSize(),150));
    const hasPts=pts&&pts.length, hasZones=zones&&zones.length;
    if(!hasPts&&!hasZones){
      m.setView([lat,lon],14);
      m.setMaxBounds([[lat-.03,lon-.05],[lat+.03,lon+.05]]);
      const mk0=isAnc?L.marker([lat,lon],{icon:ancIcon}):L.circleMarker([lat,lon],{radius:9,color:'#ff5252',weight:3,fillColor:'#ff5252',fillOpacity:.85});
      mk0.bindTooltip(el.dataset.name||'Posizione',{permanent:true,direction:'top',offset:[0,-9],className:'anch-label'}).addTo(m);
    }else{
      let la=[lat],lo=[lon];
      if(hasPts){la=la.concat(pts.map(p=>p[0]));lo=lo.concat(pts.map(p=>p[1]));}
      if(hasZones)zones.forEach(z=>{const r=z[2]/111320,c=Math.cos(z[0]*Math.PI/180);la.push(z[0]+r,z[0]-r);lo.push(z[1]+r/c,z[1]-r/c);});
      const pl=Math.max(.015,(Math.max(...la)-Math.min(...la))*.06+.008);
      const po=Math.max(.025,(Math.max(...lo)-Math.min(...lo))*.06+.012);
      HOMEB=[[Math.min(...la)-pl*.5,Math.min(...lo)-po*.5],[Math.max(...la)+pl*.5,Math.max(...lo)+po*.5]];
      m.fitBounds(HOMEB);
      const span=Math.max(Math.max(...la)-Math.min(...la),(Math.max(...lo)-Math.min(...lo))*0.9);
      const fl=span>0.6?0:(span>0.25?10:12);
      if(fl&&m.getZoom()<fl)m.setZoom(fl);
      m.setMaxBounds([[Math.min(...la)-pl,Math.min(...lo)-po],[Math.max(...la)+pl,Math.max(...lo)+po]]);
      if(hasZones)zones.forEach(z=>{
        L.circle([z[0],z[1]],{radius:z[2],color:z[3]||'#d32f2f',weight:4,dashArray:'6 4',fillColor:z[3]||'#d32f2f',fillOpacity:.25})
         .bindPopup('<b>'+z[4]+'</b>').addTo(m);
      });
      if(hasPts)pts.forEach(p=>{
        const isRist=/ristorant/i.test((root.querySelector('h1')||{textContent:''}).textContent||'');
        const ristIcon=L.divIcon({className:'rist-ic',html:'<div style="background:#ff6f00;border:2px solid #fff;border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center;font-size:18px;filter:drop-shadow(0 2px 6px rgba(0,0,0,.85))">🍽️</div>',iconSize:[30,30],iconAnchor:[15,15]});
        const mk=(isAnc?L.marker([p[0],p[1]],{icon:ancIcon}):(isRist?L.marker([p[0],p[1]],{icon:ristIcon}):L.circleMarker([p[0],p[1]],{radius:8,color:'#ff5252',weight:3,fillColor:'#ff5252',fillOpacity:.85}))).addTo(m);
        if(p[3]){
          mk.on('add',()=>{if(mk._path)mk._path.style.cursor='pointer';});
          mk.bindTooltip(p[2]+' \u2014 clic per aprire la scheda',{direction:'top',offset:[0,-9],className:'anch-label'});
          mk.on('click',()=>{
            const el=document.getElementById(p[3]);
            if(!el)return;
            const pg=el.closest('.page');
            if(pg&&!pg.classList.contains('visible'))show(pg.id);
            setTimeout(()=>el.scrollIntoView({behavior:'smooth',block:'start'}),60);
          });
        }else{
          mk.bindTooltip(p[2],{permanent:true,direction:'top',offset:[0,-9],className:'anch-label'})
           .bindPopup('<b>'+p[2]+'</b>');
        }
      });
    }
    const esriOn=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{minZoom:minz,maxZoom:maxz,attribution:'Immagini © Esri'});
    const satLo=L.tileLayer('mappe/'+slug+'/sat/{z}/{x}_{y}.jpg',{minZoom:minz,maxZoom:maxz});
    const cartoOn=L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{minZoom:minz,maxZoom:maxz,subdomains:'abcd',attribution:'© OpenStreetMap · © CARTO'});
    const baseLo=L.tileLayer('mappe/'+slug+'/base/{z}/{x}_{y}.png',{minZoom:minz,maxZoom:maxz});
    const seaOn=L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png',{minZoom:minz,maxZoom:maxz,attribution:'Segnali © OpenSeaMap'});
    const seaLo=L.tileLayer('mappe/'+slug+'/sea/{z}/{x}_{y}.png',{minZoom:minz,maxZoom:maxz});
    const gSat=L.layerGroup([esriOn,satLo]).addTo(m);
    const gBase=L.layerGroup([cartoOn,baseLo]);
    const gSea=L.layerGroup([seaOn,seaLo]);
    L.control.layers({'Satellitare':gSat,'Carta nautica':gBase},{'Segnali nautici':gSea},{collapsed:false}).addTo(m);
    const HM=L.Control.extend({options:{position:'topleft'},onAdd(){
      const d=L.DomUtil.create('div','leaflet-bar');
      const a=L.DomUtil.create('a','',d);
      a.href='#'; a.innerHTML='⌂'; a.title='Ricentra la mappa';
      a.style.fontSize='16px'; a.style.lineHeight='26px';
      L.DomEvent.on(a,'click',e=>{L.DomEvent.stop(e);if(HOMEB)m.fitBounds(HOMEB);else m.setView(HOME,HOMEZ);});
      return d;
    }});
    m.addControl(new HM());
    setTimeout(()=>m.invalidateSize(),100);
  });
}
document.getElementById('aree-head').addEventListener('click',()=>{
  document.getElementById('search').value='';
  document.body.classList.remove('searching');
  go('');
});
document.getElementById('home-link').addEventListener('click',()=>{
  esciRicerca();
  if(typeof toggleNav==='function')toggleNav(false);
  show('__CHI__');
});
document.getElementById('navtitle').addEventListener('click',()=>{go(parentOf(state)||'');});
document.addEventListener('click',e=>{
  const bk=e.target.closest('[data-back]');
  if(bk){e.preventDefault();go(parentOf(state)||'');}
});
document.getElementById('navtitle-c').addEventListener('click',()=>{go(parentOf(state)||'');});
document.getElementById('navgrid').addEventListener('click',e=>{
  const oz=e.target.closest('[data-openzone]');
  if(oz){setState(oz.dataset.openzone);show(oz.dataset.page);return;}
  const o=e.target.closest('[data-open]');
  if(o){show(TREE.cover[o.dataset.open]);return;}
  const t=e.target.closest('[data-go]');
  if(t)go(t.dataset.go);
});
function esciRicerca(){document.getElementById('search').value='';document.body.classList.remove('searching');}
plinks.forEach(l=>l.addEventListener('click',e=>{e.preventDefault();esciRicerca();show(l.dataset.page);}));
[...document.querySelectorAll('.zonelink')].forEach(l=>l.addEventListener('click',e=>{
  e.preventDefault();
  document.getElementById('search').value='';
  document.body.classList.remove('searching');
  const lk=l.dataset.country;
  if(state===lk){const nat=lk.split('/')[0];setState(nat);show(TREE.cover[nat]);}
  else{setState(lk);show(l.dataset.page);}
}));
document.addEventListener('click',e=>{
  const ar=e.target.closest('[data-area]');
  if(ar){e.preventDefault();
    document.getElementById('search').value='';
    document.body.classList.remove('searching');
    go('r:'+ar.dataset.area);return;}
  const a=e.target.closest('main a[href^="#"]');
  if(!a)return;
  const el=document.getElementById(a.getAttribute('href').slice(1));
  if(!el)return;
  e.preventDefault();
  const page=el.closest('.page');
  esciRicerca();
  if(page&&!page.classList.contains('visible'))show(page.id);
  setTimeout(()=>el.scrollIntoView({behavior:'smooth',block:'start'}),60);
});
window.addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(document.getElementById(id))show(id);});
document.getElementById('search').addEventListener('input',e=>{
  const q=e.target.value.toLowerCase().trim();
  document.body.classList.toggle('searching',!!q);
  if(!q){renderNav();return;}
  const hitC={};
  plinks.forEach(l=>{
    const pg=document.getElementById(l.dataset.page);
    const hit=!!(pg&&pg.textContent.toLowerCase().includes(q));
    l.style.display=hit?'':'none';
    if(hit)hitC[l.dataset.country]=1;
  });
  document.querySelectorAll('#nav .zonelink').forEach(h=>{
    h.style.display=hitC[h.dataset.country]?'':'none';
  });
});
show('__FIRST__');
</script>
<script src="assets/leaflet.js"></script>
</body>
</html>
"""

html = (TEMPLATE.replace("__NAV__", nav_html)
        .replace("__TREE__", json.dumps(ALBERO, ensure_ascii=False))
        .replace("__SECTIONS__", "\n".join(sections))
        .replace(f'<section id="{CHI_PID}" class="page"',
                 f'<section id="{CHI_PID}" class="page" data-special="1"', 1)
        .replace("__CHI__", CHI_PID)
        .replace("__FIRST__", "p1"))
OUT.write_text(html, encoding="utf-8")
# Manifesto pagine per audit/verifiche automatiche
(Path(__file__).resolve().parent / 'pagine_manifest.json').write_text(
    json.dumps([{'file': str(pth.relative_to(ROOT)), 'id': pid,
                 'paese': cntry, 'titolo': ttl}
                for pth, ttl, pid, cntry in queue],
               ensure_ascii=False), encoding='utf-8')
print(f"OK -> {OUT} ({OUT.stat().st_size} byte, {len(queue)} pagine)")


# ==================== VERSIONE SMARTPHONE ====================
mob_css = """
/* ===== OTTIMIZZATO SMARTPHONE ===== */
body{display:block;}
aside{position:fixed;left:0;top:0;bottom:0;width:min(86vw,330px);z-index:2000;
      transform:translateX(-102%);transition:transform .25s ease;height:100vh;height:100dvh;
      box-shadow:6px 0 24px rgba(0,0,0,.45);overflow-y:auto;-webkit-overflow-scrolling:touch;}
aside.open{transform:none;}
#backdrop{position:fixed;inset:0;background:rgba(4,10,16,.55);z-index:1900;display:none;}
#backdrop.show{display:block;}
.burger{position:fixed;top:10px;left:10px;z-index:2100;width:48px;height:48px;border-radius:12px;
        background:var(--panel);border:1px solid var(--line);color:var(--accent);font-size:23px;
        display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.4);}
main{padding:70px 12px 44px;}
h1{font-size:1.28rem;margin-top:24px;}
h2{margin-top:26px;font-size:1.02rem;padding-bottom:5px;}
table{min-width:480px;font-size:13.5px;}
th,td{padding:8px 10px;}
.tw{-webkit-overflow-scrolling:touch;}
.mapframe{height:275px;}
.navlink{padding:11px 12px;font-size:15px;}
.zonelink{font-size:17px;margin-top:13px;}
#brand-c{margin:2px 0 14px;gap:2px 10px;}
#brand-c .bw{font-size:19px;}
#brand-c .bs{display:none;}
#tree .titem{padding-top:10px;padding-bottom:10px;font-size:15px;}
#tree .mac{padding-left:26px;margin-top:12px;}
#tree .cty{padding-left:42px;}
#aree-head{padding:9px 10px;font-size:16px;margin-top:4px;}
.loc-badge{font-size:21px;margin-bottom:8px;}
.paesi-grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;}
.aree-grid{grid-template-columns:1fr 1fr;gap:10px;}
#navgrid{grid-template-columns:1fr 1fr;gap:10px;}
#navgrid .fi{font-size:30px;}
.area-card{padding:14px 12px;}
.area-card .ic{font-size:26px;}
.area-card .nm{font-size:15.5px;}
/* Telefono grande / tablet verticale */
 @media(min-width:601px) and (max-width:800px){
 .mapframe{height:340px;} table{min-width:540px;font-size:14.5px;} h1{font-size:1.5rem;}
 main{padding:74px 20px 44px;} }
/* TABLET orizzontale / laptop piccolo: barra laterale compatta, niente hamburger */
@media(min-width:801px) and (max-width:1150px){
 .burger,#backdrop{display:none!important;}
 aside{position:sticky;transform:none;width:240px;height:100vh;height:100dvh;padding:14px 10px;}
 aside h1{font-size:15px;margin:0 0 10px;}
 #search{font-size:13px;padding:7px 9px;}
 .navlink{padding:9px 10px;font-size:13.5px;}
 .pagelink{font-size:14px;padding-left:18px;}
 .zonelink{font-size:15px;margin-top:11px;}
 #tree .titem{padding-top:8px;padding-bottom:8px;font-size:13.5px;}
 #tree .mac{margin-top:10px;}
 main{padding:24px 20px 40px;}
 h1{font-size:1.45rem;} h2{font-size:1rem;}
 table{min-width:600px;font-size:14.5px;}
 th,td{padding:8px 10px;}
 .mapframe{height:360px;}
 .loc-badge{font-size:19px;} }
/* Desktop ampio: layout classico completo */
@media(min-width:1151px){
 .burger,#backdrop{display:none!important;}
 aside{position:sticky;transform:none;width:290px;height:100vh;}
 main{padding:28px clamp(14px,2.5vw,44px);} }
"""
mob = html.replace("</style>", mob_css + "</style>", 1)
ui = ('<div id="backdrop" onclick="toggleNav(false)"></div>'
      '<button class="burger" onclick="toggleNav()" aria-label="Apri menu">\u2630</button>')
mob = mob.replace("<body>", "<body>\n" + ui, 1)
drawer = """<script>
function toggleNav(force){const a=document.querySelector('aside'),b=document.getElementById('backdrop');
 const open=(force!==undefined)?force:!a.classList.contains('open');
 a.classList.toggle('open',open);b.classList.toggle('show',open);}
document.querySelectorAll('aside a:not(.reg):not(.mac)').forEach(a=>a.addEventListener('click',()=>toggleNav(false)));
document.addEventListener('keydown',e=>{if(e.key==='Escape')toggleNav(false);});
</script>
"""
mob = mob.replace('<script src="assets/leaflet.js">', drawer + '<script src="assets/leaflet.js">', 1)
OUTM = ROOT / "paesi-mobile.html"
OUTM.write_text(mob, encoding="utf-8")
print(f'OK -> {OUTM} ({OUTM.stat().st_size} byte) [smartphone]')
