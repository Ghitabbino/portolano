#!/usr/bin/env python3
"""Genera paesi.html navigabile a partire dai markdown in paesi/ (per paese)."""
import json
import re
from pathlib import Path

import markdown

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
OUT = ROOT / "paesi.html"

md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list"])

nav_pages, sections = [], []
page_map = {}  # Path risolto -> id sezione
scope_pid = {}  # (paese, titolo-norm) -> id
queue = []     # (Path, titolo, id, paese)
LABELS_IT={'cabo-verde':'Capo Verde'}
countries = [] # (chiave paese, id copertina)


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
        badge=f'<div class="loc-badge">{place}</div>'
    sections.append(f'<section id="{sec_id}" class="page" data-country="{country}">'
                    f'{badge}<h1{attrs}>{title}</h1>{html}</section>')



for country_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")):
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
            nav_pages.insert(hpos, f'<a class="navlink zonelink" data-country="{gkey}" '
                                  f'data-page="{pid}" href="#{pid}">{lbl}</a>')
        for sub2 in sorted(p for p in sub.iterdir() if p.is_dir() and not p.name.startswith(".")):
            for f in sorted(sub2.glob("*.md")):
                first = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
                title = re.sub(r"^\d+\s*[—-]\s*", "", first)
                title = re.sub(r"\s*\{#[^}]*\}", "", title).strip()
                register(f, title, country=gkey, in_nav=False)
    countries.append((key, queue[start][2]))

for md_path, title, sec_id, country in queue:
    render(md_path, title, sec_id, country)

# ==================== HOME "AREE" + PAGINE-OCEANO ====================
def _pcard(href, flag, nome, desc, st):
    return ('<div class="pcard"><div class="pflag">' + flag + '</div>'
            '<a class="pname" href="' + href + '">' + nome + '</a>'
            '<div class="pdesc">' + desc + '</div><div class="pstat">' + st + '</div></div>')

area_cards = "".join(_pcard("#o-" + oid, em, nm, ds,
                    ("apri" if any(OCEANO_DI.get(k) == oid for k in META_PAESI)
                     else "in preparazione")) for oid, em, nm, ds in OCEANI)

sections.insert(0,
    '<section id="home" class="page" data-country=""><h1>Portolano</h1>'
    '<p><strong>Metodo</strong>: ogni informazione porta rank di attendibilità '
    '+ data + fonte (quando disponibile).</p>'
    '<p><strong>L'intero sistema viene aggiornato con periodicità mensile.</strong></p>'
    '<h2>Aree</h2><div class="paesi-grid">' + area_cards + "</div></section>")

ocean_secs = []
for oid, em, nm, ds in OCEANI:
    cards = ""
    for slug, meta in META_PAESI.items():
        if OCEANO_DI.get(slug) != oid:
            continue
        key = (ROOT / slug / "00-ingresso-visti.md").resolve()
        href = page_map.get(key, "#")
        cards += _pcard(href, meta[0], meta[1], meta[2], meta[3])
    empty = "" if cards else '<p><em>In preparazione — contenuti in arrivo.</em></p>'
    ocean_secs.append(
        '<section id="o-' + oid + '" class="page" data-country="">'
        '<p><a class="backlink" href="#home">← Aree</a></p>'
        "<h1>" + nm + '</h1><div class="paesi-grid">' + cards + "</div>" + empty + "</section>")
for i, s in enumerate(ocean_secs):
    sections.insert(i, s)

nav_pages.insert(0, '<a class="navlink country-link" href="#home">Aree</a>')
for i, (oid, em, nm, ds) in enumerate(reversed(OCEANI)):
    nav_pages.insert(1, f'<a class="navlink country-link" href="#o-{oid}">{nm}</a>')

nav_html = ('<div class="nav-countries">'
            + "".join(f'<a class="navlink country-link" data-country="{k}" '
                      f'data-page="{pid}" href="#{pid}">'
                      f'{LABELS_IT.get(k, (" · ".join(p.capitalize() for p in k.split("/"))).replace("-", " "))}</a>'
                      for k, pid in sorted(countries))
            + '</div><div class="nav-pages">' + "\n".join(nav_pages) + "</div>")

TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>Portolano — Wiki paesi</title>
<link rel="stylesheet" href="assets/leaflet.css">
<style>
:root { --bg:#0f1720; --panel:#16222e; --ink:#dbe7f1; --muted:#8aa2b5; --accent:#4db6ac; --line:#24384a; }
* { box-sizing:border-box; }
body { margin:0; display:flex; min-height:100vh; background:var(--bg); color:var(--ink);
       font:15px/1.55 -apple-system, "Segoe UI", Roboto, sans-serif; }
aside { width:290px; flex-shrink:0; background:var(--panel); border-right:1px solid var(--line);
        padding:18px 14px; position:sticky; top:0; height:100vh; overflow-y:auto; }
aside h1 { font-size:16px; margin:0 0 12px; color:var(--accent); }
#search { width:100%; padding:8px 10px; margin-bottom:14px; border-radius:8px;
          border:1px solid var(--line); background:#0b131b; color:var(--ink); font-size:14px; }
.navlink { display:block; padding:7px 10px; border-radius:8px; color:var(--ink);
           text-decoration:none; font-size:13.5px; cursor:pointer; }
.navlink:hover { background:#1d3040; }
.navlink.active { background:var(--accent); color:#06231f; font-weight:600; }
.country { display:block; margin:14px 0 4px; padding:4px 10px; color:var(--muted);
           font-size:11px; letter-spacing:.12em; text-transform:uppercase; }
.nav-countries { margin-bottom:12px; padding-bottom:10px; border-bottom:1px solid var(--line); }
.country-link { font-weight:700; font-size:14.5px; }
.zonelink { font-weight:800; font-size:15.5px; color:var(--accent); margin-top:10px; }
.backlink { color:var(--accent); font-size:13px; text-decoration:none; }
.loc-badge { color:var(--accent); font-weight:700; font-size:17px;
             letter-spacing:.02em; margin-bottom:-8px; }
.pagelink { font-size:13px; padding-left:18px; }
main { flex:1; min-width:0; padding:28px clamp(14px,2.5vw,44px); }
.page { display:none; }
.page.visible { display:block; }
h1,h2,h3 { color:#fff; line-height:1.25; }
h2 { border-bottom:1px solid var(--line); padding-bottom:6px; margin-top:34px; }
.tw { overflow-x:auto; margin:14px 0; border-radius:8px; }
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
  <h1 style="cursor:pointer" id="home-link">🧭 Portolano</h1>
  <input id="search" type="search" placeholder="Cerca paese o pagina…">
  <nav id="nav">__NAV__</nav>
</aside>
<main>
__SECTIONS__
</main>
<script>
const plinks=[...document.querySelectorAll('.pagelink')];
const clinks=[...document.querySelectorAll('.country-link')];
let current='home';
function show(id){
  current=id;
  const p=document.getElementById(id);
  document.querySelectorAll('.page').forEach(x=>x.classList.toggle('visible',x===p));
  const c=p?p.dataset.country:'';
  const root=c?c.split('/')[0]:'';
  clinks.forEach(l=>l.classList.toggle('active',l.dataset.country===root));
  plinks.forEach(l=>l.style.display=(c&&l.dataset.country===c)?'':'none');
  document.querySelectorAll('.zonelink').forEach(l=>{
    const lk=l.dataset.country;
    let vis=false;
    if(c){
      if(c.includes('/')) vis=(lk===c);            // dentro zona: solo la sua intestazione
      else vis=(lk.split('/')[0]===root);          // a livello paese: tutte le sue zone
    }
    l.style.display=vis?'':'none';                 // senza paese (Indice): nascoste
  });
  window.scrollTo(0,0);
  if(p)initMaps(p);
}
function initMaps(root){
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
    const m=L.map(el,{maxBoundsViscosity:.8});
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
      const pl=Math.max(.04,(Math.max(...la)-Math.min(...la))*.15+.02);
      const po=Math.max(.06,(Math.max(...lo)-Math.min(...lo))*.15+.03);
      m.fitBounds([[Math.min(...la)-pl*.5,Math.min(...lo)-po*.5],[Math.max(...la)+pl*.5,Math.max(...lo)+po*.5]]);
      m.setMaxBounds([[Math.min(...la)-pl,Math.min(...lo)-po],[Math.max(...la)+pl,Math.max(...lo)+po]]);
      if(hasZones)zones.forEach(z=>{
        L.circle([z[0],z[1]],{radius:z[2],color:z[3]||'#d32f2f',weight:2,dashArray:'6 4',fillColor:z[3]||'#d32f2f',fillOpacity:.13})
         .bindPopup('<b>'+z[4]+'</b>').addTo(m);
      });
      if(hasPts)pts.forEach(p=>{
        const mk=(isAnc?L.marker([p[0],p[1]],{icon:ancIcon}):L.circleMarker([p[0],p[1]],{radius:8,color:'#ff5252',weight:3,fillColor:'#ff5252',fillOpacity:.85})).addTo(m);
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
    setTimeout(()=>m.invalidateSize(),100);
  });
}
clinks.forEach(l=>l.addEventListener('click',e=>{
  e.preventDefault();
  const s=document.getElementById('search'); s.value='';
  show(l.dataset.page);
}));
document.getElementById('home-link').addEventListener('click',()=>{
  const s=document.getElementById('search'); s.value='';
  show(document.querySelector('.page').id);
});
plinks.forEach(l=>l.addEventListener('click',e=>{e.preventDefault();show(l.dataset.page);}));
[...document.querySelectorAll('.zonelink')].forEach(l=>l.addEventListener('click',e=>{
  e.preventDefault();
  const s=document.getElementById('search'); s.value='';
  show(l.dataset.page);
}));
document.addEventListener('click',e=>{
  const a=e.target.closest('main a[href^="#"]');
  if(!a)return;
  const el=document.getElementById(a.getAttribute('href').slice(1));
  if(!el)return;
  e.preventDefault();
  const page=el.closest('.page');
  if(page&&!page.classList.contains('visible'))show(page.id);
  setTimeout(()=>el.scrollIntoView({behavior:'smooth',block:'start'}),60);
});
window.addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(document.getElementById(id))show(id);});
document.getElementById('search').addEventListener('input',e=>{
  const q=e.target.value.toLowerCase().trim();
  if(!q){show(current);return;}
  const rootVis={};
  plinks.forEach(l=>{
    const pg=document.getElementById(l.dataset.page);
    const hit=!!(pg&&pg.textContent.toLowerCase().includes(q));
    l.style.display=hit?'':'none';
    if(hit){
      const c0=l.dataset.country.split('/')[0];
      rootVis[c0]=1;
      if(l.dataset.country.includes('/')) rootVis[l.dataset.country]=1;
    }
  });
  document.querySelectorAll('#nav .zonelink').forEach(h=>{
    h.style.display=rootVis[h.dataset.country]?'':'none';
  });
  clinks.forEach(l=>{
    const k=l.dataset.country;
    l.style.display=(l.textContent.toLowerCase().includes(q)||rootVis[k])?'':'none';
  });
});
show('home');
</script>
<script src="assets/leaflet.js"></script>
</body>
</html>
"""

html = TEMPLATE.replace("__NAV__", nav_html).replace("__SECTIONS__", "\n".join(sections)).replace("home", "home")
OUT.write_text(html, encoding="utf-8")
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
.loc-badge{font-size:15px;margin-bottom:-7px;}
.paesi-grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;}
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
 .pagelink{font-size:12.5px;padding-left:16px;}
 .zonelink{font-size:15px;margin-top:11px;}
 main{padding:24px 20px 40px;}
 h1{font-size:1.45rem;} h2{font-size:1rem;}
 table{min-width:600px;font-size:14.5px;}
 th,td{padding:8px 10px;}
 .mapframe{height:360px;}
 .loc-badge{font-size:16px;} }
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
document.querySelectorAll('aside a').forEach(a=>a.addEventListener('click',()=>toggleNav(false)));
document.addEventListener('keydown',e=>{if(e.key==='Escape')toggleNav(false);});
</script>
"""
mob = mob.replace('<script src="assets/leaflet.js">', drawer + '<script src="assets/leaflet.js">', 1)
OUTM = ROOT / "paesi-mobile.html"
OUTM.write_text(mob, encoding="utf-8")
print(f'OK -> {OUTM} ({OUTM.stat().st_size} byte) [smartphone]')
