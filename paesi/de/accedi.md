# Einloggen — Wiki bearbeiten

**Zugang nur für registrierte Segler.**

Gib die bei der Anmeldung erstellten Zugangsdaten ein, um die Bearbeitungsrechte für das Wiki freizuschalten.

### Login

<div style="background:#ffffff;border:2px solid #4db6ac;border-radius:12px;padding:22px;margin:12px auto;max-width:560px;text-align:center">
<label style="display:block;margin:10px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">E-Mail *</label>
<input id="login-email" type="email" placeholder="name@beispiel.com" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<label style="display:block;margin:14px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Passwort *</label>
<input id="login-pass" type="password" placeholder="dein Passwort" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<button onclick="accedi()" style="display:block;margin:18px auto 6px;padding:12px 28px;border-radius:10px;background:linear-gradient(135deg,#4db6ac,#2e7d6f);color:#fff;font-weight:800;border:none;cursor:pointer;font-size:16px;box-shadow:0 3px 10px rgba(0,0,0,.25)">Einloggen</button>
<div id="login-msg" style="display:none;margin:10px auto;max-width:480px;padding:10px;border-radius:8px;font-size:13px"></div>
</div>

<script>
function accedi(){
  const email=document.getElementById('login-email').value.trim();
  const pass=document.getElementById('login-pass').value;
  const msg=document.getElementById('login-msg');
  if(!email||!pass){msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Bitte E-Mail und Passwort eingeben.';return;}
  const saved=JSON.parse(localStorage.getItem('sailtropics_user')||'null');
  if(saved && saved.email===email){localStorage.setItem('sailtropics_logged','1');msg.style.display='block';msg.style.background='#e8f5e9';msg.style.border='1px solid #4caf50';msg.style.color='#1b5e20';msg.textContent='✅ OK';setTimeout(()=>location.hash='#'+(typeof PROFILO_PID!=='undefined'?PROFILO_PID:'profilo'),600);} else {msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Zugangsdaten nicht gefunden. Bitte zuerst anmelden.';}
}
</script>

*Passwort vergessen?* [Wiederherstellen](#) — wir senden dir einen Reset-Link.

### Was ändert sich nach dem Login

- **Freies Lesen** (anonym): Lies das gesamte Handbuch, Karten, GPX/ZIP — ohne Einschränkungen.
- **Reservierte Bearbeitung** (angemeldet): Oben auf jeder Ankerplatz- oder Länderseite erscheinen die Schaltflächen **„Bearbeiten“** und **„Update hinzufügen“**. Jede Änderung wird unter deinem Namen für Nachvollziehbarkeit und Moderation gespeichert.
- Du kannst deine Daten und die Gebiete, für die du Warnungen erhältst, jederzeit auf der Seite [Anmelden](iscriviti.md) ändern.

### Datenschutz — Unser Versprechen

Wir speichern nur den Hash deiner E-Mail und ein Sitzungs-Token. Keine weitere Verwendung, niemals an Dritte weitergegeben.

> **Unser Versprechen: Deine Daten werden ausschließlich zur Verwaltung deines Kontos und zum Versand der von dir gewählten Warnungen verwendet und niemals für andere Zwecke verwendet oder an Dritte weitergegeben.**

Kein Konto? Gehe zu **[Anmelden](iscriviti.md)**.

Letzte Aktualisierung: 28/08/2026
