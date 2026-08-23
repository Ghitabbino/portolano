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
GRUPPI = [
 ("grandi-antille",   "\U0001F3D4", "Grandi Antille",                ["cuba","ispaniola","giamaica","porto-rico","cayman"]),
 ("sopravento-sett",  "\U0001F334", "Sopravento Settentrionali",     ["virgin-islands","anguilla","saint-martin","saint-barth","antigua-barbuda","st-kitts-nevis","montserrat","saba","st-eustatius"]),
 ("sopravento-merid", "\U0001F334", "Sopravento Meridionali",        ["guadalupa","dominica","martinica","santa-lucia","grenadine","barbados","grenada"]),
 ("sottovento-abc",   "\u2600",     "Sottovento (ABC e Trinidad)",   ["aruba","curacao","bonaire","trinidad-tobago"]),
 ("lucayano",         "\U0001F41A", "Arcipelago Lucayano",           ["bahamas","turks-caicos"]),
 ("centro-america",   "\u26F5",     "America Centrale",              ["panama","belize","honduras","costarica","nicaragua","venezuela"]),
]
GRUPPO_DI = {}
for _g in GRUPPI:
    for _m in _g[3]: GRUPPO_DI[_m] = _g[0]

ORDER = ["caraibi","mar-rosso","mediterraneo","atlantico","indiano","pacifico"]  # ordine alfabetico per nome

PAESI = {
 "cabo-verde": ("cv", "Capo Verde", "9 isole: hub Mindelo, Sal turistica, vulcano Fogo.", "\u2705 v1 \u00b7 ver. 23/08/26"),
 "canarie":    ("es", "Canarie",    "Tenerife, Gran Canaria, Lanzarote e le altre.",     "\U0001F6A7 v0 \u00b7 ver. 23/08/26"),
 "grenadine":  ("vc", "Grenadine",  "Tobago Cays, Bequia, Mustique.",                    "\U0001F6A7 v0 \u00b7 ver. 23/08/26"),
 "guadalupa":  ("fr", "Guadalupa",  "Les Saintes, Petite Terre, Riserva Cousteau.",      "\u2705 v1 \u00b7 ver. 23/08/26"),
 "martinica":  ("fr", "Martinica",  "Hub Le Marin, base servizi n.1 Antille.",           "\u2705 v1 \u00b7 ver. 23/08/26"),
 "panama":     ("pa", "Panama",     "Canale + San Blas: transito, Colon, comarca Guna Yala.", "\u2705 v1 \u00b7 ver. 23/08/26"),
 "cuba":         ("\U0001F1E8\U0001F1FA", "Cuba",          "L'isola maggiore dei Caraibi.",              "\U0001F6A7 v0 · ver. 23/08/2026"),
 "ispaniola":    ("\U0001F1E9\U0001F1F4", "Ispaniola",     "Repubblica Dominicana + Haiti.",             "\U0001F6A7 v0 · ver. 23/08/2026"),
 "giamaica":     ("\U0001F1EF\U0001F1F2", "Giamaica",      "Nord-ovest Caraibi.",                        "\U0001F6A7 v0 · ver. 23/08/2026"),
 "porto-rico":   ("\U0001F1F5\U0001F1F7", "Porto Rico",    "Territorio USA.",                            "\U0001F6A7 v0 · ver. 23/08/2026"),
 "cayman":       ("\U0001F1F0\U0001F1FE", "Isole Cayman",  "George Town, banking e dive.",               "\U0001F6A7 v0 · ver. 23/08/2026"),
 "dominica":     ("\U0001F1E9\U0001F1F2", "Dominica",      "Natura selvaggia, Champagne Reef.",          "\U0001F6A7 v0 · ver. 23/08/2026"),
 "santa-lucia":  ("\U0001F1F1\U0001F1E8", "Santa Lucia",   "Pitons, marina Rodney Bay.",                 "\U0001F6A7 v0 · ver. 23/08/2026"),
 "barbados":     ("\U0001F1E7\U0001F1E7", "Barbados",      "Carlisle Bay, Atlantic side.",               "\U0001F6A7 v0 · ver. 23/08/2026"),
 "grenada":      ("\U0001F1EC\U0001F1E9", "Grenada",       "Grande Anse, spezie, Annage.",               "\U0001F6A7 v0 · ver. 23/08/2026"),
 "antigua-barbuda":("\U0001F1E6\U0001F1EC","Antigua e Barbuda","English Harbour, 365 spiagge.",           "\U0001F6A7 v0 · ver. 23/08/2026"),
 "saint-martin": ("\U0001F1F8\U0001F1FD", "Saint-Martin / Sint Maarten", "Doppia nazione FR/NL.",        "\U0001F6A7 v0 · ver. 23/08/2026"),
 "saint-barth":  ("\U0001F1E7\U0001F1F1", "Saint-Barthélemy","Gustavia, chic francese.",                 "\U0001F6A7 v0 · ver. 23/08/2026"),
 "anguilla":     ("\U0001F1E6\U0001F1EE", "Anguilla",      "Road Bay, spiagge bianche.",                 "\U0001F6A7 v0 · ver. 23/08/2026"),
 "st-kitts-nevis":("\U0001F1F0\U0001F1F3","St-Kitts e Nevis","Basseterre, Charlestown.",                 "\U0001F6A7 v0 · ver. 23/08/2026"),
 "montserrat":   ("\U0001F1F2\U0001F1F8", "Montserrat",    "Little Bay, vulcano Soufrière.",             "\U0001F6A7 v0 · ver. 23/08/2026"),
 "saba":         ("\U0001F1E7\U0001F1F6", "Saba",          "Fort Bay, marine park, dive.",               "\U0001F6A7 v0 · ver. 23/08/2026"),
 "st-eustatius": ("\U0001F1E7\U0001F1F6", "St-Eustatius",  "Oranje Bay, STENAPA.",                       "\U0001F6A7 v0 · ver. 23/08/2026"),
 "virgin-islands":("\U0001F1FB\U0001F1EC","Isole Vergini", "BVI + USVI: Baths, Norman, St John.",        "\U0001F6A7 v0 · ver. 23/08/2026"),
 "aruba":        ("\U0001F1E6\U0001F1FC", "Aruba",         "ABC: fuori belt uragani.",                   "\U0001F6A7 v0 · ver. 23/08/2026"),
 "curacao":      ("\U0001F1E8\U0001F1FC", "Curaçao",       "Willemstad, Schottegat.",                    "\U0001F6A7 v0 · ver. 23/08/2026"),
 "bonaire":      ("\U0001F1E7\U0001F1F6", "Bonaire",       "Klein Bonaire, dive paradise.",              "\U0001F6A7 v0 · ver. 23/08/2026"),
 "trinidad-tobago":("\U0001F1F9\U0001F1F9","Trinidad e Tobago","Carnival, Chaguaramas cantieri.",        "\U0001F6A7 v0 · ver. 23/08/2026"),
 "bahamas":      ("\U0001F1E7\U0001F1F8", "Bahamas",       "700 isole: Exuma, Abaco.",                   "\U0001F6A7 v0 · ver. 23/08/2026"),
 "turks-caicos": ("\U0001F1F9\U0001F1E8", "Turks e Caicos","Grace Bay, barriera di corallo.",            "\U0001F6A7 v0 · ver. '+D+'"),
 "venezuela":    ("\U0001F1FB\U0001F1EA", "Venezuela",     "Costa caraibica: Los Roques.",               "\U0001F6A7 v0 · ver. '+D+'"),
 "panama":       ("\U0001F1F5\U0001F1E6", "Panama",        "Canale + San Blas: transito, Colon, comarca Guna Yala.", "\u2705 v1 · ver. '+D+'"),
 "belize":       ("\U0001F1E7\U0001F1FF", "Belize",        "Barriera corallina, cayes.",                 "\U0001F6A7 v0 · ver. '+D+'"),
 "honduras":     ("\U0001F1ED\U0001F1F3", "Honduras",      "Bay Islands: Roatán.",                       "\U0001F6A7 v0 · ver. '+D+'"),
 "costarica":    ("\U0001F1E8\U0001F1F7", "Costa Rica",    "Golfo Dulce, Drake Bay.",                    "\U0001F6A7 v0 · ver. '+D+'"),
 "nicaragua":    ("\U0001F1F3\U0001F1EE", "Nicaragua",     "San Juan del Sur, Pearl Cays.",              "\U0001F6A7 v0 · ver. '+D+'"),
}
OCEANO_DI = {"cabo-verde":"atlantico","canarie":"atlantico",
             "grenadine":"caraibi","guadalupa":"caraibi",
             "martinica":"caraibi","panama":"caraibi",
             "cuba":"caraibi","ispaniola":"caraibi","giamaica":"caraibi","porto-rico":"caraibi","cayman":"caraibi","dominica":"caraibi","santa-lucia":"caraibi","barbados":"caraibi","grenada":"caraibi","aruba":"caraibi","curacao":"caraibi","bonaire":"caraibi","trinidad-tobago":"caraibi","bahamas":"caraibi","turks-caicos":"caraibi","antigua-barbuda":"caraibi","saint-martin":"caraibi","saint-barth":"caraibi","anguilla":"caraibi","st-kitts-nevis":"caraibi","montserrat":"caraibi","saba":"caraibi","st-eustatius":"caraibi","virgin-islands":"caraibi",}

def svg(code):
    if code not in ("cv","es","vc","fr","pa"):
        return code  # emoji o html gia' pronto
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

def flag_html(cc):
    return svg(cc) if cc in ("cv","es","vc","fr","pa") else cc

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
        kids=sorted([k for k in PAESI if OCEANO_DI.get(k)==oid], key=lambda s: PAESI[s][1])
        dsc = ("Grandi Antille, Sopravento Settentrionali e Meridionali, Sottovento, Lucayano, Centro America"
               if oid=="caraibi" else
               ", ".join(PAESI[k][1] for k in kids) if kids else "in preparazione")
        cards+=pcard("#o-"+oid, OC_ICON[oid], OC_NAME[oid], dsc,
            "apri \u2192" if kids else "")
    home=('<section id="home" class="page" data-country="">'
          '<h1>Portolano</h1>'
          '<p><strong>L\'intero sistema viene aggiornato con periodicit\u00e0 mensile.</strong></p>'
          '<h2>Aree</h2><div class="paesi-grid">'+cards+'</div></section>')

    secs=""
    for oid in ORDER:
        cs=""
        if oid=="caraibi":
            for gid,gicon,gname,members in GRUPPI:
                n=len([m for m in members if m in PAESI])
                nomi=sorted(PAESI[m][1] for m in members)
                cs+=pcard("#c-"+gid, gicon, gname,
                          ", ".join(nomi), "apri \u2192")
        else:
            for k,(cc,nome,desc,st) in PAESI.items():
                if OCEANO_DI.get(k)!=oid: continue
                cs+=pcard("#"+pid_of.get(k,"#"), flag_html(cc), nome, desc, st)
        empty="<p><em>In preparazione.</em></p>" if not cs else ""
        secs+=('<section id="o-'+oid+'" class="page" data-country="'+oid+'">'
               '<p><a href="#home">\u2190 Aree</a></p><h1>'+OC_NAME[oid]+'</h1>'
               '<div class="paesi-grid">'+cs+'</div>'+empty+'</section>')
    # pagine dei 6 gruppi caraibici
    for gid,gicon,gname,members in GRUPPI:
        gcs=""
        for slug in sorted(members, key=lambda s: PAESI.get(s, ("","","","",s))[1]):
            if slug in PAESI:
                cc=PAESI[slug][0]
                gcs+=pcard("#"+pid_of.get(slug,"#"), flag_html(cc), PAESI[slug][1], PAESI[slug][2], PAESI[slug][3])
        emptyg="<p><em>In preparazione.</em></p>" if not gcs else ""
        secs+=('<section id="c-'+gid+'" class="page" data-country="caraibi/'+gid+'">'
               '<p><a href="#o-caraibi">\u2190 Caraibi</a></p><h1>'+gname+'</h1>'
               '<div class="paesi-grid">'+gcs+'</div>'+emptyg+'</section>')
    html=html.replace("<main>", "<main>"+home+"\n"+secs+"\n", 1)

    zones={}
    for zm in re.finditer(r'data-country="([^"]+/[^"]+)"[^>]*data-page="(p\d+)"[^>]*>([^<]{2,40})<', html):
        zones.setdefault(zm.group(1),(zm.group(2),zm.group(3).strip()))
    items='<a class="navlink country-link" data-country="" data-page="home" href="#home">\U0001F30D Aree</a>'
    for oid in ORDER:
        kids=[k for k in PAESI if OCEANO_DI.get(k)==oid]
        items+=('<a class="navlink country-link" data-country="'+oid+'" data-page="o-'+oid+'" '
                'href="#o-'+oid+'">'+OC_ICON[oid]+' '+OC_NAME[oid]+'</a>')
        if oid=="caraibi":
            for gid,gicon,gname,members in GRUPPI:
                items+=('<a class="navlink country-link sub" data-country="caraibi/'+gid+'" data-page="c-'+gid+'" href="#c-'+gid+'" >'+gicon+' '+gname+'</a>')
        if not kids: continue
        for k in kids:
            cc,nome,_,_=PAESI[k]; pid=pid_of.get(k,"#")
            items+=('<a class="navlink country-link sub" data-country="'+k+'" data-page="'+pid+'" '
                    'href="#'+pid+'" >'
                    +svg(cc)+' '+nome+'</a>')
            import html as _h
            for zk,(zp,zn) in sorted(zones.items(), key=lambda kv: kv[1][1]):
                if zk.split("/")[0]!=k: continue
                items+=('<a class="navlink country-link zsub" data-country="'+zk+'" data-page="'+zp+'" href="#'+zp+'">'+_h.escape(zn)+'</a>')
    m=re.search(r'<div class="nav-countries">[\s\S]*?</div>', html)
    if m:
        html=html[:m.start()]+'<div class="nav-countries">'+items+'</div>'+html[m.end():]

    ocids="{"+",".join('"'+k+'":1' for k in ORDER)+"}"
    html=html.replace("function show(id){",
        "const PAR="+json.dumps(OCEANO_DI)+";const OC_IDS="+ocids+";const GRP="+json.dumps(GRUPPO_DI)+
        ";\nfunction show(id){",1)
    html=html.replace(
        "clinks.forEach(l=>l.classList.toggle('active',l.dataset.country===root));",
        "clinks.forEach(l=>l.classList.toggle('active',l.dataset.country===root||l.dataset.country===PAR[root]));",1)
    NAVJS=("\n"      +"var iz=c.indexOf(\"/\")>=0;"
      +"var isOc=!!(c&&OC_IDS[c]);"
      +"var isGrp=c.indexOf(\"caraibi/\")===0;"
      +"var hz=false;"
      +"document.querySelectorAll(\".zonelink\").forEach(function(z){if((z.dataset.country||\"\").split(\"/\")[0]===root)hz=true;});"
      +"document.querySelectorAll(\".nav-countries a\").forEach(function(l){"
      +"var k=l.dataset.country||\"\";var vis=false;"
      +"if(k===\"\"){vis=true;}"
      +"else if(OC_IDS[k]){vis=(c===\"\")||k===c;}"
      +"else if(k.indexOf(\"caraibi/\")===0){vis=(c===\"caraibi\")||(k===c);}"
      +"else if(k.indexOf(\"/\")<0){"
      +"if(isOc){vis=(c!==\"caraibi\")&&PAR[k]===c;}"
      +"else if(isGrp){vis=GRP[k]===c.split(\"/\")[1];}"
      +"else{vis=iz?false:(k===c);}}"
      +"else{vis=isOc?false:(iz?(k===c):false);}"
      +"l.style.display=vis?\"\":\"none\";"
      +"l.classList.toggle(\"active\",k===c);"
      +"});"
      +"plinks.forEach(function(l){var dk=l.dataset.country;"
      +"var v=!!c&&dk===c&&(iz||!hz);l.style.display=v?\"\":\"none\";});"
    )
    html=html.replace("  window.scrollTo(0,0);","  "+NAVJS+"\n  window.scrollTo(0,0);",1)
    # la regola plinks originale non serve più: la gestisce NAVJS (capitoli solo dentro l'isola, o paesi senza isole)
    html=html.replace("plinks.forEach(l=>l.style.display=(c&&l.dataset.country===c)?'':'none');",
                      "plinks.forEach(l=>l.style.display='none');",1)
    # gerarchia visiva: classi CSS invece degli stili inline
    html=html.replace("</style>",
      ".nav-countries .sub{font-size:13px;padding-left:24px}"
      ".nav-countries .zsub{font-size:12.5px;padding-left:40px;color:var(--muted)}"
      ".nav-countries .zsub:before{content:\"·\";margin-right:6px;color:var(--accent)}"
      ".nav-countries .zsub.active{color:#06231f}</style>",1)

    # ═══ FILO DI ARIANNA: Aree › Oceano › Paese › Pagina ═══
    sec_re=re.compile(r'<section id="(p\d+)" class="page" data-country="([^"]*)">([\s\S]*?)<h1[^>]*>([\s\S]*?)</h1>')
    def _sub(m):
        pid,c,mid,tit=m.group(1),m.group(2),m.group(3),re.sub(r"<[^>]+>","",m.group(4)).strip()
        if not c: return m.group(0)
        root=c.split("/")[0]
        parts=[]
        parts.append('<a href="#home">'+ "\U0001F30D"+' Aree</a>' if False else '<a href="#home">'+OC_ICON.get("indiano","")+'</a>' )
        return m.group(0)
    # costruzione semplice senza lambda complesse
    def add_crumbs(html):
        out=[]; pos=0
        for m in list(sec_re.finditer(html)) + list(re.finditer(r'<section id="(o-[a-z-]+)" class="page" data-country="([a-z-]+)">([\s\S]*?)<h1[^>]*>([\s\S]*?)</h1>', html)):
            pid,c=m.group(1),m.group(2)
            tit=re.sub(r"<[^>]+>","",m.group(4)).strip().replace("'","\u2019")
            if pid.startswith("o-"):
                ins='<p class="crumbs"><a href="#home">Aree</a> \u203a <b>'+tit+'</b></p>'
                out.append(html[pos:m.end()]); out.append(ins); pos=m.end(); continue
            root=c.split("/")[0]
            seg=[]
            seg.append('<a href="#home">'+OC_ICON["mediterraneo"].replace("\u26F1\uFE0F","")+'Aree</a>'.replace("",""))
            seg=None
            crumbs='<a href="#home">Aree</a>'
            oc=OCEANO_DI.get(root)
            if root=="caraibi" or (c and c.startswith("caraibi/")):
                crumbs+=' \u203a <a href="#o-caraibi">Mar dei Caraibi</a>'
                if c and c.startswith("caraibi/"):
                    g=c.split("/")[1]
                    gn=[x[2] for x in GRUPPI if x[0]==g]
                    crumbs+=' \u203a <a href="#c-'+g+'">'+(gn[0] if gn else g)+'</a>'
                    if "/" not in c[len("caraibi/"):] and c!="caraibi/"+g:
                        pass
                if "/" in c[len("caraibi/"):] if c and c.startswith("caraibi/") else False:
                    pass
            elif oc:
                crumbs+=' \u203a <a href="#o-'+oc+'">'+OC_NAME[oc]+'</a>'
            if "/" in c:
                crumbs+=' \u203a <a href="#'+pid_of.get(root,"#")+'">'+PAESI[root][1]+'</a>'
                crumbs+=' \u203a <b>'+tit+'</b>'
            else:
                crumbs+=' \u203a <b>'+tit+'</b>'
            ins='<p class="crumbs">'+crumbs+'</p>'
            out.append(html[pos:m.end()]); out.append(ins); pos=m.end()
        out.append(html[pos:])
        return "".join(out)
    html=add_crumbs(html)
    # CSS crumbs
    if ".crumbs {" not in html:
        html=html.replace("</style>",
          'section.page{font-size:16.5px}'
          'section.page h1{font-size:32px}'
          ".crumbs{font-size:12px;color:var(--muted,#8899aa);margin:0 0 6px}"
          ".crumbs a{color:var(--accent,#3fa7ff);text-decoration:none}"
          ".crumbs b{color:inherit}</style>",1)
    html=re.sub(r"show\('p1'\)","show('home')",html,count=1)
    return html

for fn in [ROOT/"paesi.html", ROOT/"paesi-mobile.html"]:
    p=Path(fn); h=p.read_text(encoding="utf-8")
    nh=process(h)
    nh.encode("utf-8")
    p.write_text(nh, encoding="utf-8")
    print("OK", p.name)
print("DONE v2")
