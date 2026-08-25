#!/usr/bin/env python3
"""Controlla i link esterni in tutti i .md del portolano.
Uso: python3 tools/controlla_link.py [--paese XX]
Output: tools/link_check.txt + riepilogo a schermo."""
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RE_URL = re.compile(r'https?://[^\s\)\]>"\'’]+')
TIMEOUT = 10

def check(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (SailTropics link check)',
        'Accept': 'text/html,*/*'})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status
    except Exception as e:
        code = getattr(e, 'code', None)
        return f'ERR {code or type(e).__name__}'

def main():
    filtro = None
    if '--paese' in sys.argv:
        filtro = sys.argv[sys.argv.index('--paese') + 1]
    visti = {}
    righe = []
    ok = ko = 0
    files = sorted((ROOT / 'paesi').rglob('*.md')) if (ROOT / 'paesi').exists() \
        else sorted(Path('.').rglob('*.md'))
    for f in files:
        rel = str(f)
        if filtro and filtro not in rel:
            continue
        for u in RE_URL.findall(f.read_text(encoding='utf-8')):
            u = u.rstrip('.,;')
            dom = re.sub(r'^https?://', '', u).split('/')[0]
            key = ('DOM', dom)          # un solo test per dominio
            key_url = ('URL', u)
            if key_url in visti:
                continue
            if key not in visti:
                visti[key] = check('https://' + dom)
                time.sleep(0.2)
            st_dom = visti[key]
            if st_dom == 200:
                visti[key_url] = 'ok (dominio)'
            else:
                visti[key_url] = check(u)
                time.sleep(0.2)
    for (tipo, k), st in sorted(visti.items()):
        if tipo != 'URL':
            continue
        buono = st == 200 or st == 'ok (dominio)' or (
            isinstance(st, int) and 200 <= st < 400)
        if buono:
            ok += 1
        else:
            ko += 1
            righe.append(f'BROKEN [{st}] {k}')
    print(f'domini/link verificati: {ok + ko} | ok: {ok} | problemi: {ko}')
    for r in righe:
        print(' •', r)
    out = Path(__file__).parent / 'link_check.txt'
    out.write_text('\n'.join(righe) or 'tutti i link ok', encoding='utf-8')

if __name__ == '__main__':
    main()
