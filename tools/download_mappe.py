#!/usr/bin/env python3
"""Scarica in locale i tasselli mappa (satellitare Esri + base CARTO + seamark OpenSeaMap)
per gli ancoraggi della Martinica, per uso offline nel portolano."""
import math
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPPE = os.path.join(ROOT, "mappe")

ANCHORAGES = [
    # Martinica
    ("sainte-anne", 14.4383, -60.8850),
    ("marin-est", 14.4636, -60.8610),
    ("genipa", 14.5520, -61.0650),
    ("grande-anse-arlet", 14.4805, -61.0885),
    ("petite-anse-arlet", 14.4705, -61.0985),
    ("anse-noire", 14.4785, -61.1150),
    ("mitan", 14.4965, -61.1045),
    ("saint-pierre", 14.7410, -61.1770),
    ("meurnier", 14.5920, -61.1330),
    ("fonds-blancs", 14.6130, -60.9020),
        ("anc-deshaies", 16.306, -61.796),
    ("anc-desireade", 16.3175, -61.001),
    ("anc-ilet-gosier", 16.1955, -61.466),
    ("anc-les-saintes", 15.867, -61.582),
    ("anc-malendure-cousteau", 16.268, -61.781),
    ("anc-marie-galante", 15.9695, -61.0175),
    ("anc-petite-terre", 16.17, -60.986),
    ("anc-pointe-a-pitre", 16.2305, -61.5345),
    ("anc-ravine-paul-thomas", 16.008, -61.7375),
    ("anc-saint-francois", 16.245, -61.2805),
    ("anc-anse-noire", 14.4785, -61.115),
    ("anc-fonds-blancs", 14.613, -60.902),
    ("anc-genipa", 14.55, -61.063),
    ("anc-grande-anse-arlet", 14.481, -61.088),
    ("anc-marin-est", 14.462, -60.863),
    ("anc-meurnier", 14.591, -61.133),
    ("anc-mitan", 14.495, -61.103),
    ("anc-petite-anse-arlet", 14.4715, -61.0985),
    ("anc-saint-pierre", 14.74, -61.178),
    ("anc-sainte-anne", 14.432, -60.885),
    ("anc-amador", 8.907, -79.5295),
    ("anc-chagres", 9.3275, -79.9515),
    ("anc-contadora", 8.619, -79.036),
    ("anc-isla-grande", 9.631, -79.564),
    ("anc-linton-bay", 9.47, -79.539),
    ("anc-pedro-gonzalez", 8.379, -78.976),
    ("anc-portobelo", 9.55, -79.6555),
    ("anc-san-telmo", 9.463, -78.967),
    ("anc-shelter-bay", 9.3595, -79.9505),
    ("anc-taboga", 8.787, -79.5525),
    ("anc-banedup", 9.205, -78.27),
    ("anc-coco-bandero", 9.213, -78.264),
    ("anc-dog-island", 9.199, -78.256),
    ("anc-eastern-lemons", 9.176, -78.235),
    ("anc-isla-perro", 9.17, -78.249),
    ("anc-nargana", 9.447, -78.585),
    ("anc-playon-chico", 9.342, -78.407),
    ("anc-porvenir", 9.559, -78.946),
    ("anc-salardup-snug", 9.185, -78.268),
    ("anc-west-lemons", 9.19, -78.245),
    # Guadalupa
    ("les-saintes", 15.8680, -61.5820),
    ("deshaies", 16.3065, -61.7965),
    ("malendure-cousteau", 16.2686, -61.7813),
    ("ravine-paul-thomas", 16.0080, -61.7380),
    ("pointe-a-pitre", 16.2310, -61.5340),
    ("ilet-gosier", 16.1960, -61.4660),
    ("saint-francois", 16.2450, -61.2810),
    ("petite-terre", 16.1700, -60.9850),
    ("marie-galante", 15.9700, -61.0180),
    ("desireade", 16.3180, -61.0000),
    # ═══ Sottovento + Vergini + Grandi Antille + Lucayano ═══
    ("anc-admiralty-nord", 13.003, -61.240),
    ("anc-lower-bay", 12.988, -61.248),
    ("anc-friendship", 12.972, -61.233),
    ("anc-britannia", 12.883, -61.183),
    ("anc-salt-whistle", 12.635, -61.395),
    ("anc-clifton", 12.483, -61.443),
    ("anc-chatham", 12.467, -61.503),
    ("anc-charlestown-nevis", 12.703, -61.433),
    ("anc-horseshoe", 12.633, -61.363),
    ("anc-blue-lagoon-svg", 13.148, -61.227),
    ("anc-wallilabou", 13.263, -61.227),
    ("anc-the-baths", 18.433, -64.433),
    ("anc-north-sound", 18.497, -64.377),
    ("anc-bight-norman", 18.317, -64.620),
    ("anc-white-bay-jvd", 18.443, -64.762),
    ("anc-great-harbour-jvd", 18.447, -64.750),
    ("anc-cruz-bay", 18.330, -64.793),
    ("anc-sopers-hole", 18.387, -64.697),
    ("anc-nanny-cay", 18.423, -64.647),
    ("anc-english-harbour", 17.008, -61.763),
    ("anc-falmouth", 17.016, -61.774),
    ("anc-jolly", 17.053, -61.868),
    ("anc-marigot", 18.066, -63.082),
    ("anc-grand-case", 18.067, -63.048),
    ("anc-anse-marcel", 18.104, -63.010),
    ("anc-simpson-bay", 18.033, -63.097),
    ("anc-gustavia", 17.897, -62.851),
    ("anc-colombier", 17.884, -62.866),
    ("anc-fourchue", 17.850, -62.933),
    ("anc-road-bay", 18.183, -63.118),
    ("anc-crocus-bay", 18.183, -63.070),
    ("anc-basseterre", 17.297, -62.718),
    ("anc-whitehouse", 17.247, -62.700),
    ("anc-charlestown", 17.147, -62.617),
    ("anc-pinneys", 17.150, -62.590),
    ("anc-little-bay-msr", 16.817, -62.213),
    ("anc-fort-bay", 17.617, -63.238),
    ("anc-wells-bay", 17.637, -63.253),
    ("anc-oranje-bay", 17.483, -62.983),
]

ZOOMS = [12, 13, 14, 15]
SPAN = 1  # raggio in tasselli attorno al centro per ogni zoom

# Mappe generali: (slug, lat, lon, zooms, span) — span crescente per coprire l'isola
OVERVIEWS = [
    ("martinica", 14.60, -61.03, [10, 11, 12, 13], {10: 1, 11: 2, 12: 3, 13: 4}),
    ("guadalupa", 16.10, -61.39, [10, 11, 12, 13], {10: 2, 11: 3, 12: 5, 13: 5}),

    # Panama
    ("panama-caribe", 9.45, -79.75, [10, 11, 12, 13], {10: 2, 11: 3, 12: 5, 13: 5}),
    ("panama-pacifico", 8.70, -79.20, [9, 10, 11, 12], {9: 1, 10: 2, 11: 4, 12: 5}),
    ("san-blas", 9.53, -78.75, [10, 11, 12, 13], {10: 1, 11: 2, 12: 4, 13: 4}),
    # Canarie
    ("tenerife", 28.30, -16.55, [10, 11, 12, 13], {10: 1, 11: 2, 12: 4, 13: 4}),
    ("gran-canaria", 27.90, -15.60, [10, 11, 12, 13], {10: 1, 11: 2, 12: 4, 13: 4}),
    ("fuerteventura", 28.35, -14.05, [10, 11, 12, 13], {10: 1, 11: 3, 12: 5, 13: 5}),
    ("lanzarote", 29.02, -13.65, [10, 11, 12, 13], {10: 1, 11: 2, 12: 4, 13: 4}),
    ("la-palma", 28.65, -17.83, [10, 11, 12, 13], {10: 1, 11: 1, 12: 3, 13: 3}),
    ("la-gomera", 28.09, -17.20, [10, 11, 12, 13], {10: 1, 11: 1, 12: 2, 13: 2}),
    ("el-hierro", 27.73, -18.03, [10, 11, 12, 13], {10: 1, 11: 1, 12: 2, 13: 2}),
    ("la-graciosa", 29.23, -13.50, [11, 12, 13, 14], {11: 1, 12: 2, 13: 3, 14: 3}),
    # ═══ Fix audit 25/08/2026: overview mancanti (regola 6) — scala certificata
    # Bahamas + dettaglio aumentato su richiesta utente (25/08) ═══
    ("bahamas", 24.50, -76.00, [6, 7, 8, 9, 10], {6: 1, 7: 2, 8: 3, 9: 2, 10: 3}),
    ("cuba", 21.60, -79.00, [6, 7, 8, 9, 10], {6: 1, 7: 2, 8: 4, 9: 4, 10: 6}),
    ("ispaniola", 18.90, -70.70, [7, 8, 9, 10, 11], {7: 1, 8: 2, 9: 3, 10: 5, 11: 6}),
    ("porto-rico", 18.22, -66.45, [8, 9, 10, 11, 12], {8: 1, 9: 1, 10: 2, 11: 4, 12: 5}),
    ("giamaica", 18.15, -77.35, [8, 9, 10, 11, 12, 13], {8: 1, 9: 1, 10: 2, 11: 3, 12: 5, 13: 6}),
    ("cayman", 19.32, -81.25, [9, 10, 11, 12, 13], {9: 1, 10: 1, 11: 2, 12: 3, 13: 3}),
    ("trinidad-tobago", 10.55, -61.30, [9, 10, 11, 12, 13], {9: 1, 10: 2, 11: 3, 12: 5, 13: 5}),
    ("curacao", 12.20, -69.05, [10, 11, 12, 13], {10: 1, 11: 1, 12: 2, 13: 2}),
    ("bonaire", 12.16, -68.29, [10, 11, 12, 13], {10: 1, 11: 1, 12: 2, 13: 2}),
    ("aruba", 12.52, -69.97, [10, 11, 12, 13], {10: 1, 11: 1, 12: 2, 13: 2}),
]


# Minimappe ristoranti: zoom urbani
RESTAURANTS = [
    # Martinica
    ("rist-zanzibar", 14.4700, -60.9980),
    ("rist-kokoarum", 14.4717, -60.9990),
    ("rist-ti-cozy", 14.4355, -60.8800),
    ("rist-boubou", 14.4360, -60.8795),
    ("rist-le-m", 14.4370, -60.8785),
    ("rist-cour-creole", 14.4365, -60.8790),
    ("rist-daurade", 14.4360, -60.8800),
    ("rist-delims", 14.4355, -60.8790),
    ("rist-basilic-beach", 14.4440, -60.8830),
    ("rist-pirates-beach", 14.4448, -60.8842),
    ("rist-kreol-k-fe", 14.4940, -61.0860),
    ("rist-oasis", 14.4870, -61.0890),
    ("rist-palmeiras", 14.4796, -61.0249),
    ("rist-havana-cafe", 14.5390, -61.0360),
    ("rist-sous-le-vent", 14.4567, -60.9439),
    ("rist-zandoli", 14.5970, -61.0790),
    # Guadalupa
    ("rist-toumbana", 15.8670, -61.5830),
    ("rist-ketty", 16.3050, -61.7950),
    ("rist-savane", 16.3070, -61.7960),
    ("rist-madras", 16.3060, -61.7970),
    ("rist-raf", 16.3060, -61.7980),
    ("rist-anse-gourmande", 16.3065, -61.7960),
    ("rist-lucullus", 16.2290, -61.3800),
    ("rist-cabanon", 16.2280, -61.3790),
    ("rist-coquillage", 16.2295, -61.3810),
    ("rist-balaou", 16.2285, -61.3805),
    ("rist-zagaya", 16.2390, -61.2720),
    ("rist-playa", 15.9530, -61.0380),
    ("rist-pere-labat", 15.9490, -61.0420),
    ("rist-planteur", 16.2220, -61.4930),
    ("rist-rayon-soleil", 16.5120, -61.5090),
]
REST_ZOOMS = [15, 16]

SOURCES = {
    "sat": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    "base": "https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
    "sea": "https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",
}

UA = {"User-Agent": "portolano-offline/1.0 (uso personale)"}


def deg2num(lat, lon, z):
    n = 2 ** z
    x = int((lon + 180.0) / 360.0 * n)
    lat_r = math.radians(lat)
    y = int((1.0 - math.log(math.tan(lat_r) + 1 / math.cos(lat_r)) / math.pi) / 2.0 * n)
    return x, y


def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return "skip"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        if len(data) < 100:
            return "empty"
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
        return "ok"
    except Exception:
        return "fail"


def scarica(slug, lat, lon, zooms, span):
    cx, cy = {}, {}
    for z in zooms:
        cx[z], cy[z] = deg2num(lat, lon, z)
    for layer, tpl in SOURCES.items():
        ext = "jpg" if layer == "sat" else "png"
        for z in zooms:
            d = os.path.join(MAPPE, slug, layer, str(z))
            os.makedirs(d, exist_ok=True)
            sp = span[z] if isinstance(span, dict) else span
            for dx in range(-sp, sp + 1):
                for dy in range(-sp, sp + 1):
                    x, y = cx[z] + dx, cy[z] + dy
                    url = tpl.format(z=z, x=x, y=y)
                    res = fetch(url, os.path.join(d, f"{x}_{y}.{ext}"))
                    STATS[res] += 1
                    if res == "fail":
                        time.sleep(1.0)
    print(f"{slug}: fatto", flush=True)


STATS = {"ok": 0, "skip": 0, "empty": 0, "fail": 0}


def main():
    want = {a for a in sys.argv[1:] if not a.startswith("-")}
    if want:
        # modalità mirata: scarica SOLO gli slug indicati (riprendibile, idempotente)
        for s in want:
            done = False
            for slug, lat, lon, zooms, span in OVERVIEWS:
                if slug == s:
                    scarica(slug, lat, lon, zooms, span)
                    done = True
            for slug, lat, lon in ANCHORAGES:
                if slug == s:
                    scarica(slug, lat, lon, ZOOMS, SPAN)
                    done = True
            for slug, lat, lon in RESTAURANTS:
                if slug == s:
                    scarica(slug, lat, lon, REST_ZOOMS, SPAN)
                    done = True
            if not done:
                print(f"{s}: SLUG SCONOSCIUTO", flush=True)
        print(STATS)
        return 0
    for slug, lat, lon in ANCHORAGES:
        scarica(slug, lat, lon, ZOOMS, SPAN)
    for slug, lat, lon, zooms, span in OVERVIEWS:
        scarica(slug, lat, lon, zooms, span)
    for slug, lat, lon in RESTAURANTS:
        scarica(slug, lat, lon, REST_ZOOMS, SPAN)
    print(STATS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
