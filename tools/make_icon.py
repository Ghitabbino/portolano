#!/usr/bin/env python3
"""Icona bussola per Portolano.app"""
from PIL import Image, ImageDraw
import os, subprocess, tempfile

S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# sfondo arrotondato color corallo scuro
m = 60
d.rounded_rectangle([m, m, S - m, S - m], radius=180, fill=(196, 84, 51, 255))

cx = cy = S // 2
R = 330

# cerchio esterno e interno
d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(255, 244, 230, 255), width=26)
r2 = int(R * 0.82)
d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=(255, 244, 230, 160), width=8)

# rosa dei venti: 4 punte principali (N bianca lunga, S scura) + 4 diagonali
def point(angle_deg, length, width, fill):
    import math
    a = math.radians(angle_deg)
    tip = (cx + length * math.sin(a), cy - length * math.cos(a))
    left = (cx + width * math.sin(a + math.pi / 2), cy - width * math.cos(a + math.pi / 2))
    right = (cx + width * math.sin(a - math.pi / 2), cy - width * math.cos(a - math.pi / 2))
    base = (cx - length * 0.18 * math.sin(a), cy + length * 0.18 * math.cos(a))
    d.polygon([tip, left, base], fill=fill)
    d.polygon([tip, right, base], fill=fill)

point(0, R - 40, 46, (255, 244, 230, 255))     # N
point(180, R - 40, 46, (120, 44, 22, 255))     # S
point(90, int(R * 0.62), 34, (255, 244, 230, 220))   # E
point(270, int(R * 0.62), 34, (255, 244, 230, 220))  # O
for ang in (45, 135, 225, 315):
    point(ang, int(R * 0.45), 24, (255, 244, 230, 150))

# ago centrale
d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(196, 84, 51, 255),
          outline=(255, 244, 230, 255), width=10)

# lettera N in alto
try:
    from PIL import ImageFont
    f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 110)
except Exception:
    f = None
d.text((cx, cy - R - 95), "N", font=f, fill=(255, 244, 230, 255), anchor="mm")

tmp = tempfile.mkdtemp(dir="/var/folders/s9/m7r9jsg921dgy3__tvd6zslh0000gn/T/opencode")
iconset = os.path.join(tmp, "Portolano.iconset")
os.makedirs(iconset)
for size in [16, 32, 64, 128, 256, 512]:
    img.resize((size, size), Image.LANCZOS).save(os.path.join(iconset, f"icon_{size}x{size}.png"))
    img.resize((size * 2, size * 2), Image.LANCZOS).save(os.path.join(iconset, f"icon_{size}x{size}@2x.png"))

icns = os.path.join(tmp, "Portolano.icns")
subprocess.run(["iconutil", "-c", "icns", iconset, "-o", icns], check=True)
print(icns)
