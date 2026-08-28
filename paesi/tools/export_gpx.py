#!/usr/bin/env python3
"""Esporta waypoint GPX per ogni paese con ancoraggi verificati."""
import re, json, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
GPX_DIR = ROOT / "gpx"
GPX_DIR.mkdir(exist_ok=True)

# GPX 1.1 namespace
NS = "http://www.topografix.com/GPX/1/1"
ET.register_namespace("", NS)

def esc(s): return s.replace("&","&amp;").replace("<","&lt;")

RE_MARKERS = re.compile(r"data-markers='([^']+)'")

count_total = 0
for country_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith(".") and p.name not in {"assets","mappe","tools","controllo","fonti","gruppi","gpx","zip","i18n","it","en","fr","es","de","pt"}):
    # cerca 08-ancoraggi.md
    md_path = country_dir / "08-ancoraggi.md"
    if not md_path.exists():
        # prova sottocartelle? no
        continue
    text = md_path.read_text(encoding="utf-8")
    markers_raw = RE_MARKERS.findall(text)
    points = []  # lista (lat,lon,name,slug)
    seen = set()
    for raw in markers_raw:
        try:
            pts = json.loads(raw)
        except:
            continue
        for p in pts:
            if len(p) < 3: continue
            lat, lon, name = p[0], p[1], p[2]
            slug = p[3] if len(p) >= 4 else ""
            # escludi DATO MANCANTE
            if "DATO MANCANTE" in name: continue
            try:
                lat_f = float(lat); lon_f = float(lon)
            except: continue
            if not (-90 <= lat_f <= 90 and -180 <= lon_f <= 180): continue
            key = (round(lat_f,5), round(lon_f,5), name)
            if key in seen: continue
            seen.add(key)
            points.append((lat_f, lon_f, name, slug))
    if not points:
        continue
    # genera GPX
    gpx = ET.Element("gpx", attrib={"version":"1.1","creator":"SailTropics Portolano","xmlns":NS})
    meta = ET.SubElement(gpx, "metadata")
    ET.SubElement(meta, "name").text = f"{country_dir.name} — ancoraggi"
    ET.SubElement(meta, "desc").text = f"Waypoint ancoraggi {country_dir.name} — WGS84 — Portolano SailTropics"
    ET.SubElement(meta, "time").text = datetime.now(timezone.utc).isoformat()
    author = ET.SubElement(meta, "author")
    ET.SubElement(author, "name").text = "SailTropics"
    ET.SubElement(meta, "link", attrib={"href":"https://ghitabbino.github.io/portolano/"}).text = "Portolano"
    for lat,lon,name,slug in points:
        wpt = ET.SubElement(gpx, "wpt", attrib={"lat":f"{lat:.6f}", "lon":f"{lon:.6f}"})
        # nome compatto per plotter (max 30)
        ET.SubElement(wpt, "name").text = name[:30]
        desc = f"{name} — {slug}" if slug else name
        ET.SubElement(wpt, "desc").text = desc
        ET.SubElement(wpt, "sym").text = "Anchor"
        ET.SubElement(wpt, "type").text = "Anchorage"
        # estensione slug per riferimento
        ext = ET.SubElement(wpt, "extensions")
        ET.SubElement(ext, "slug").text = slug
    out = GPX_DIR / f"{country_dir.name}.gpx"
    ET.ElementTree(gpx).write(out, encoding="utf-8", xml_declaration=True)
    count_total += 1
    print(f"OK {country_dir.name}: {len(points)} wpt -> {out}")

# genera anche gpx unico globale (opzionale)
# validazione base: prova a parsare tutti i GPX generati
for g in GPX_DIR.glob("*.gpx"):
    try:
        ET.parse(g)
    except Exception as e:
        print(f"ERRORE GPX {g}: {e}")

print(f"TOT {count_total} file GPX in {GPX_DIR}")
