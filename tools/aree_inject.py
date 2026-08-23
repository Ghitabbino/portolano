#!/usr/bin/env python3
"""Home Aree + pagine oceani + sidebar corretta (v2 definitivo)."""
from pathlib import Path
import re, json

ROOT = Path(__file__).resolve().parent.parent

OC_ICON = {
 "atlantico":    "\U0001F30A",
 "caraibi":      "\U0001F334",
 "mar-rosso":    "\U0001F531",
 "pacifico":     "\U0001F3DD",
 "indiano":      "\U0001F41A",
 "mediterraneo": "\u26F1\uFE0F",
}
OC_NAME = {
 "atlantico": "Oceano Atlantico", "caraibi": "Mar dei Caraibi",
 "mar-rosso": "Mar Rosso",        "pacifico": "Oceano Pacifico",
 "indiano":   "Oceano Indiano",   "mediterraneo": "Mediterraneo",
}
ORDER = ["atlantico","caraibi","mar-rosso","pacifico","mediterraneo","indiano"]

PAESI = {
 "cabo-verde": ("cv", "Capo Verde", "9 isole: hub Mindelo, Sal turistica, vulcano Fogo.", "\u2705 v1"),
 "canarie":    ("es", "Canarie",    "Tenerife, Gran Canaria, Lanzarote e le altre.",     "\U0001F6A7 v0"),
 "grenadine":  ("vc", "Grenadine",  "Tobago Cays, Bequia, Mustique.",                    "\U0001F6A7 v0 · ver. 23/08/26"),
 "guadalupa":  ("fr", "Guadalupa",  "Les Saintes, Petite Terre, Riserva Cousteau.",      "\u2705 v1"),
 "martinica":  ("fr", "Martinica",  "Hub Le Marin, base servizi n.1 Antille.",           "\u2705 v1"),
 "panama":     ("pa", "Panama",     "Canale + San Blas: transito, Colon, comarca Guna Yala.", "\u2705 v1 \u00b7 ver. 23/08/26"),
}
OCEANO_DI = {"cabo-verde":"atlantico","canarie":"atlantico",
             "grenadine":"caraibi","guadalupa":"caraibi",
             "martinica":"caraibi","panama":"caraibi"}

def svg(code):
    import math
    W,H=24,16
    def rect(x,y,w,h,c): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'
    def star(cx,cy,r,c):
        pts=[]
        for i in range(10):
            rr=r if i%2==0 else r*0.42
            a=-math.pi/2+i*math.pi/5
            pts.append(f"{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}")
        return '<polygon points="'+" ".join(pts)+'" fill="'+c+'"/>'
    if code=="cv":
        b=rect(0,0,W,H,"#003893")+rect(0,10,W,2,"#fff")+rect(0,12,W,2,"#CE1126")+rect(0,14,W,2,"#fff")
        for dx in (-6,-3,0,3,6): b+=star(12+dx,7,1.4,"#FCD116")
    elif code=="es":
        b=rect(0,0,W,4,"#AA151B")+rect(0,4,W,8,"#F1BF00")+rect(0,12,W,4,"#AA151B")
    elif code=="vc":
        b=rect(0,0,8,H,"#0072C6")+rect(8,0,8,H,"#FCD116")+rect(16,0,8,H,"#009E60")
        b+='<rect x="10" y="4" width="4.4" height="4.4" fill="#009E60" transform="rotate(45 12.2 6.2)"/>'
        b+=star(12,11.5,1.7,"#009E60")
    elif code=="fr":
        b=rect(0,0,8,H,"#002395")+rect(8,0,8,H,"#fff")+rect(16,0,8,H,"#ED2939")
    elif code=="pa":
        b=rect(0,0,W,H,"#fff")+rect(12,0,12,8,"#DA121A")+rect(0,8,12,8,"#072357")
        b+=star(6,4,2.6,"#072357")+star(18,12,2.6,"#DA121A")
    else:
        b=rect(0,0,W,H,"#888")
    return '<svg width="21" height="14" viewBox="0 0 24 16" style="border-radius:2px;vertical-align:-2px">'+b+'</svg>'

def pcard(href, flaghtml, nome, desc, st):
    nome=nome.replace("'","\u2019"); desc=desc.replace("'","\u2019")
    return ('<div class="pcard"><div class="pflag">'+flaghtml+'</div>'
            '<a class="pname" href="'+href+'">'+nome+'</a>'
            '<div class="pdesc">'+desc+'</div><div class="pstat">'+st+'</div></div>')

def process(html):
    if 'id="home"' in html:
        print("   gia iniettato, skip"); return html

    pid_of={}
    for m in re.finditer(r'data-country="([^"/]+)"[^>]*data-page="(p\d+)"', html):
        pid_of.setdefault(m.group(1), m.group(2))
    print("   pids:", pid_of)

    cards=""
    for oid in ORDER:
        kids=[k for k in PAESI if OCEANO_DI.get(k)==oid]
        cards+=pcard("#o-"+oid, OC_ICON[oid], OC_NAME[oid],
            ", ".join(PAESI[k][1] for k in kids) if kids else "in preparazione",
            "apri \u2192" if kids else "")
    home=('<section id="home" class="page" data-country="">'
          '<h1>Portolano</h1>'
          '<p><strong>L\'intero sistema viene aggiornato con periodicit\u00e0 mensile.</strong></p>'
          '<h2>Aree</h2><div class="paesi-grid">'+cards+'</div></section>')

    secs=""
    for oid in ORDER:
        cs=""
        for k,(cc,nome,desc,st) in PAESI.items():
            if OCEANO_DI.get(k)!=oid: continue
            cs+=pcard("#"+pid_of.get(k,"#"), svg(cc), nome, desc, st)
        empty="<p><em>In preparazione.</em></p>" if not cs else ""
        secs+=('<section id="o-'+oid+'" class="page" data-country="'+oid+'">'
               '<p><a href="#home">\u2190 Aree</a></p><h1>'+OC_NAME[oid]+'</h1>'
               '<div class="paesi-grid">'+cs+'</div>'+empty+'</section>')
    html=html.replace("<main>", "<main>"+home+"\n"+secs+"\n", 1)

    items='<a class="navlink country-link" data-country="" data-page="home" href="#home">\U0001F30D Aree</a>'
    for oid in ORDER:
        kids=[k for k in PAESI if OCEANO_DI.get(k)==oid]
        items+=('<a class="navlink country-link" data-country="'+oid+'" data-page="o-'+oid+'" '
                'href="#o-'+oid+'">'+OC_ICON[oid]+' '+OC_NAME[oid]+'</a>')
        if not kids: continue
        for k in kids:
            cc,nome,_,_=PAESI[k]; pid=pid_of.get(k,"#")
            items+=('<a class="navlink country-link sub" data-country="'+k+'" data-page="'+pid+'" '
                    'href="#'+pid+'" style="padding-left:22px;font-size:12px">'
                    +svg(cc)+' '+nome+'</a>')
    m=re.search(r'<div class="nav-countries">[\s\S]*?</div>', html)
    if m:
        html=html[:m.start()]+'<div class="nav-countries">'+items+'</div>'+html[m.end():]

    ocids="{"+",".join('"'+k+'":1' for k in ORDER)+"}"
    html=html.replace("function show(id){",
        "const PAR="+json.dumps(OCEANO_DI)+";const OC_IDS="+ocids+
        ";\nfunction show(id){",1)
    html=html.replace(
        "clinks.forEach(l=>l.classList.toggle('active',l.dataset.country===root));",
        "clinks.forEach(l=>l.classList.toggle('active',l.dataset.country===root||l.dataset.country===PAR[root]));",1)
    html=html.replace("  window.scrollTo(0,0);",
        "  const curO=PAR[root]||OC_IDS[root]?root:'';"
        "document.querySelectorAll('.nav-countries .sub').forEach(l=>"
        "{l.style.display=(curO&&PAR[l.dataset.country]===curO)?'':'none';});"
        "document.querySelectorAll('.nav-countries .country-link').forEach(l=>"
        "{if(OC_IDS[l.dataset.country])l.style.display=(!curO||l.dataset.country===curO)?'':'none';});"
        "\n  window.scrollTo(0,0);",1)

    html=re.sub(r"show\('p1'\)","show('home')",html,count=1)
    return html

for fn in [ROOT/"paesi.html", ROOT/"paesi-mobile.html"]:
    p=Path(fn); h=p.read_text(encoding="utf-8")
    nh=process(h)
    nh.encode("utf-8")
    p.write_text(nh, encoding="utf-8")
    print("OK", p.name)
print("DONE v2")
