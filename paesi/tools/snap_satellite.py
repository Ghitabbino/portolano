#!/usr/bin/env python3
"""Verifica satellitare dei marker ristoranti: campiona i pixel dei tasselli
sat (Esri) già scaricati e 'snappa' a terra i pin in acqua."""
import math
import re
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MAPPE = ROOT / "mappe"


def deg2num(lat, lon, z):
    n = 2 ** z
    x = int((lon + 180.0) / 360.0 * n)
    lr = math.radians(lat)
    y = int((1.0 - math.log(math.tan(lr) + 1 / math.cos(lr)) / math.pi) / 2 * n)
    return x, y


def frac(lat, lon, z):
    n = 2 ** z
    xf = (lon + 180.0) / 360.0 * n
    lr = math.radians(lat)
    yf = (1.0 - math.log(math.tan(lr) + 1 / math.cos(lr)) / math.pi) / 2 * n
    return xf - int(xf), yf - int(yf)


def sample(lat, lon, z, slug):
    """Ritorna (r,g,b) medio 5x5 dal tassello sat dello slug stesso, o None."""
    x, y = deg2num(lat, lon, z)
    fx, fy = frac(lat, lon, z)
    best = None
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            f = MAPPE / slug / "sat" / str(z) / f"{x+dx}_{y+dy}.jpg"
            if not f.exists():
                continue
            try:
                im = Image.open(f).convert("RGB")
            except Exception:
                continue
            px = int((fx - dx) * 256), int((fy - dy) * 256)
            px = (min(max(px[0], 3), 252), min(max(px[1], 3), 252))
            box = im.crop((px[0]-2, px[1]-2, px[0]+3, px[1]+3))
            data = list(box.getdata())
            n = len(data)
            best = tuple(sum(c[i] for c in data)//n for i in range(3))
            return best
    return None


def is_water(rgb):
    r, g, b = rgb
    return (b > r and g >= r - 6 and b >= g - 8 and b > 45) or (b > 70 and b-r > 18)


def snap(lat, lon, slug):
    """Se acqua: cerca il pixel terra più vicino su spirale di offset."""
    step = 0.00035
    for ring in range(1, 60):
        for k in range(ring*8 or 1):
            a = (k/(ring*8))*2*math.pi if ring else 0
            la = lat + math.sin(a)*step*ring
            lo = lon + math.cos(a)*step*ring/math.cos(math.radians(lat))
            s = sample(la, lo, 16, slug)
            if s and not is_water(s):
                return round(la, 5), round(lo, 5), ring
    return None


def main():
    only = [a for a in __import__("sys").argv[1:] if not a.startswith("-")]
    fixes = []
    for md in sorted(ROOT.rglob("10-ristoranti.md")):
        paese = md.relative_to(ROOT).parts[0]
        if only and paese not in only:
            continue
        txt = md.read_text(encoding="utf-8")
        for m in re.finditer(r"data-markers='([^']+)'", txt):
            try:
                arr = json.loads(m.group(1))
            except Exception:
                continue
            for pt in arr:
                slug = pt[3] if len(pt) >= 4 else None
                if not slug:
                    continue
                zz = next((z for z in (16,15,14,13) if list(MAPPE.glob(f"{slug}/sat/{z}/*.jpg"))), None)
                if not zz:
                    continue
                s = sample(pt[0], pt[1], zz, slug)
                tag = "ACQUA" if s and is_water(s) else ("terra" if s else "no-tasselli")
                print(f"{paese:20} {slug:26} {pt[0]:>9},{pt[1]:>10} -> {s} {tag}")
                if s and is_water(s):
                    res = snap(pt[0], pt[1], slug)
                    if res:
                        la, lo, ring = res
                        fixes.append((md, slug, pt[0], pt[1], la, lo))
                        print(f"   ↳ SNAPPATA a {la},{lo} (distanza {ring} passi)")
    # applica
    byfile = {}
    for md, slug, ola, olo, nla, nlo in fixes:
        byfile.setdefault(md, {})[slug] = (ola, olo, nla, nlo)
    for md, mappa in byfile.items():
        t = md.read_text(encoding="utf-8")
        def fx(m):
            arr = json.loads(m.group(1))
            for pt in arr:
                if len(pt) >= 4 and pt[3] in mappa:
                    ola, olo, nla, nlo = mappa[pt[3]]
                    pt[0], pt[1] = nla, nlo
            return "data-markers='" + json.dumps(arr, ensure_ascii=False) + "'"
        t = re.sub(r"data-markers='([^']+)'", fx, t)
        for slug, (ola, olo, nla, nlo) in mappa.items():
            t = t.replace(f'data-lat="{ola}"', f'data-lat="{nla}"').replace(
                          f'data-lon="{olo}"', f'data-lon="{nlo}"')
            f = next(iter(ROOT.glob(f"**/{slug}.md")), None)
            if f:
                x = f.read_text(encoding="utf-8")
                x = x.replace(f'data-lat="{ola}"', f'data-lat="{nla}"').replace(
                              f'data-lon="{olo}"', f'data-lon="{nlo}"')
                f.write_text(x, encoding="utf-8")
        md.write_text(t, encoding="utf-8")
    print(f"\nsnappate a terra: {len(fixes)}")


if __name__ == "__main__":
    main()
