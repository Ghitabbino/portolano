# Accedi — Modifica la wiki

**Accesso riservato ai navigatori registrati.**

Inserisci le credenziali create in fase di iscrizione per sbloccare i permessi di scrittura della wiki.

### Login

<div style="background:#ffffff;border:2px solid #4db6ac;border-radius:12px;padding:22px;margin:12px auto;max-width:560px;text-align:center">
<label style="display:block;margin:10px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Email *</label>
<input id="login-email" type="email" placeholder="nome@esempio.com" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<label style="display:block;margin:14px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Password *</label>
<input id="login-pass" type="password" placeholder="la tua password" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<button onclick="accedi()" style="display:block;margin:18px auto 6px;padding:12px 28px;border-radius:10px;background:linear-gradient(135deg,#4db6ac,#2e7d6f);color:#fff;font-weight:800;border:none;cursor:pointer;font-size:16px;box-shadow:0 3px 10px rgba(0,0,0,.25)">Accedi</button>
<div id="login-msg" style="display:none;margin:10px auto;max-width:480px;padding:10px;border-radius:8px;font-size:13px"></div>
</div>

<script>
function accedi(){
  const email=document.getElementById('login-email').value.trim();
  const pass=document.getElementById('login-pass').value;
  const msg=document.getElementById('login-msg');
  if(!email||!pass){msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Inserisci email e password.';return;}
  const saved=JSON.parse(localStorage.getItem('sailtropics_user')||'null');
  if(saved && saved.email===email){localStorage.setItem('sailtropics_logged','1');msg.style.display='block';msg.style.background='#e8f5e9';msg.style.border='1px solid #4caf50';msg.style.color='#1b5e20';msg.textContent='✅ OK';setTimeout(()=>location.hash='#'+(typeof PROFILO_PID!=='undefined'?PROFILO_PID:'profilo'),600);} else {msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Credenziali non trovate. Iscriviti prima.';}
}
</script>

*Password dimenticata?* [Recupera](#) — ti inviamo un link di reset.


### Cosa cambia dopo il login

- **Consultazione libera** (anonimo): leggi tutto il portolano, mappe, GPX/ZIP — nessuna limitazione.
- **Editing riservato** (loggato): in cima a ogni scheda di ancoraggio o paese compaiono i tasti **“Modifica”** e **“Aggiungi Aggiornamento”**. Ogni modifica viene salvata a tuo nome per tracciabilità e moderazione.
- Puoi modificare i tuoi dati e le aree per cui ricevi gli allert in qualsiasi momento dalla pagina [Iscriviti](iscriviti.md).

### Privacy — questo è il nostro impegno

Conserviamo esclusivamente l’hash della tua email e un token di sessione. Nessun altro uso, mai ceduti a terzi.

> **Questo è il nostro impegno: i tuoi dati saranno utilizzati esclusivamente per gestire il tuo account e l’invio degli allert selezionati e non saranno mai utilizzati per altre finalità, né ceduti o comunicati a terzi.**

Non hai un account? Vai a **[Iscriviti](iscriviti.md)**.

Ultimo aggiornamento: 28/08/2026
