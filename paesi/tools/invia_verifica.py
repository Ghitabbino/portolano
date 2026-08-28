#!/usr/bin/env python3
"""Simula invio mail di verifica con link automatico (demo locale). In produzione sostituire con provider reale."""
import json, hashlib, time, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / "controllo" / "verifiche_inviate.log"
LOG.parent.mkdir(exist_ok=True)

def invia(email, nick, token):
    link = f"https://ghitabbino.github.io/portolano/verifica.html?token={token}&email={email}"
    # hash per log
    h = hashlib.sha256(email.encode()).hexdigest()[:12]
    entry = {"ts": time.time(), "email_hash": h, "nick": nick, "token": token, "link": link}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False)+"\n")
    print(f"[VERIFICA] Mock mail a {email} ({nick}) — link: {link}")
    print("In produzione: inviare via Buttondown/Brevo/SES con template.")
    return link

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        invia(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else "skipper", sys.argv[3] if len(sys.argv)>3 else hashlib.sha256(str(time.time()).encode()).hexdigest()[:16])
    else:
        print("Uso: python3 tools/invia_verifica.py <email> <nick> [token]")
