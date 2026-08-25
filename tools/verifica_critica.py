#!/usr/bin/env python3
"""Verifica critica portolano: coda paesi scaduti (>15 giorni dall'ultima revisione).

Uso:
  python3 tools/verifica_critica.py                 # mostra coda e batch consigliato
  python3 tools/verifica_critica.py --segna cuba    # marca paese come verificato oggi
  python3 tools/verifica_critica.py --segna cuba --data 2026-08-25
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / 'controllo_critico.json'
GIORNI_LIMITE = 15
RE_DATE = re.compile(r'(\d{2})/(\d{2})/(\d{4})')


def ultima_data_paese(d: Path):
    """Data del tocco piu' recente tra i file .md del paese."""
    best = None
    for f in d.glob('*.md'):
        txt = f.read_text(encoding='utf-8')
        for m in RE_DATE.finditer(txt):
            try:
                dt = date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
            except ValueError:
                continue
            if dt > date.today():          # date future = pianificazioni, non tocchi
                continue
            if best is None or dt > best:
                best = dt
    return best


def carica_stato():
    if JSON_PATH.exists():
        return json.loads(JSON_PATH.read_text(encoding='utf-8'))
    return {}


def main():
    args = sys.argv[1:]
    stato = carica_stato()
    oggi = date.today()

    if '--segna' in args:
        i = args.index('--segna')
        paesi = [a for a in args[i + 1:] if not a.startswith('--')]
        nuova = oggi.isoformat()
        if '--data' in args:
            j = args.index('--data')
            if j + 1 < len(args):
                nuova = args[j + 1]
        for p in paesi:
            stato[p] = {'ultima_critica': nuova}
        JSON_PATH.write_text(json.dumps(stato, indent=2, ensure_ascii=False),
                             encoding='utf-8')
        print(f"marcati {len(paesi)} paesi al {nuova}: {', '.join(paesi)}")
        return

    righe = []
    NON_PAESE = {'controllo', 'fonti', 'tools', 'assets', 'mappe', 'gruppi'}
    for d in sorted(p for p in ROOT.iterdir()
                    if p.is_dir() and not p.name.startswith('.')
                    and p.name not in NON_PAESE):
        if not list(d.glob('*.md')):
            continue
        nome = d.name
        ultimo_tocco = ultima_data_paese(d)
        rec = stato.get(nome, {}).get('ultima_critica')
        if rec:
            base = datetime.fromisoformat(rec).date()
            fonte = f'critica {rec}'
        elif ultimo_tocco:
            base = ultimo_tocco
            fonte = f'tocco {base.isoformat()} (mai criticato)'
        else:
            base = None
            fonte = 'SENZA DATE'
        if base is None:
            giorni = 999
        else:
            giorni = (oggi - base).days
        stato_txt = 'SCADUTO' if giorni > GIORNI_LIMITE else 'ok'
        if giorni > 999:
            stato_txt = 'DA FARE'
        righe.append((giorni, nome, stato_txt, fonte))

    righe.sort(reverse=True)
    scaduti = [r for r in righe if r[2] != 'ok']
    print(f"VERIFICA CRITICA — {oggi.isoformat()} (limite {GIORNI_LIMITE} gg)\n")
    print(f"{'gg':>5}  {'STATO':8}  PAESE                    riferimento")
    for g, n, s, f in righe:
        print(f"{g:>5}  {s:8}  {n:24} {f}")
    batch = [r[1] for r in scaduti[:5]]
    print(f"\nscaduti: {len(scaduti)}/{len(righe)}")
    if batch:
        print(f"BATCH CONSIGLIATO (max 5/sessione): {' '.join(batch)}")
        print("protocollo: AGENTI_VERIFICA_CRITICA.md")


if __name__ == '__main__':
    main()
