# Log In — Edit the Wiki

**Access restricted to registered cruisers.**

Enter the credentials you created at sign-up to unlock wiki editing rights.

### Login

<div style="background:#ffffff;border:2px solid #4db6ac;border-radius:12px;padding:22px;margin:12px auto;max-width:560px;text-align:center">
<label style="display:block;margin:10px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Email *</label>
<input id="login-email" type="email" placeholder="name@example.com" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<label style="display:block;margin:14px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Password *</label>
<input id="login-pass" type="password" placeholder="your password" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<button onclick="accedi()" style="display:block;margin:18px auto 6px;padding:12px 28px;border-radius:10px;background:linear-gradient(135deg,#4db6ac,#2e7d6f);color:#fff;font-weight:800;border:none;cursor:pointer;font-size:16px;box-shadow:0 3px 10px rgba(0,0,0,.25)">Log In</button>
<div id="login-msg" style="display:none;margin:10px auto;max-width:480px;padding:10px;border-radius:8px;font-size:13px"></div>
</div>

<script>
function accedi(){
  const email=document.getElementById('login-email').value.trim();
  const pass=document.getElementById('login-pass').value;
  const msg=document.getElementById('login-msg');
  if(!email||!pass){msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Please enter email and password.';return;}
  const saved=JSON.parse(localStorage.getItem('sailtropics_user')||'null');
  if(saved && saved.email===email){localStorage.setItem('sailtropics_logged','1');msg.style.display='block';msg.style.background='#e8f5e9';msg.style.border='1px solid #4caf50';msg.style.color='#1b5e20';msg.textContent='✅ OK';setTimeout(()=>location.hash='#'+(typeof PROFILO_PID!=='undefined'?PROFILO_PID:'profilo'),600);} else {msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Credenziali non trovate. Iscriviti prima.';}
}
</script>

*Forgot password?* [Recover](#) — we’ll send you a reset link.


### What Changes After Login

- **Free browsing** (anonymous): read the entire pilot, charts, GPX/ZIP — no restrictions.
- **Restricted editing** (logged in): at the top of each anchorage or country sheet you’ll see **“Edit”** and **“Add Update”** buttons. Every edit is saved under your name for traceability and moderation.
- You can change your details and the areas for which you receive alerts at any time from the [Sign Up](iscriviti.md) page.

### Privacy — Our Commitment

We store only the hash of your email and a session token. No other use, never passed to third parties.

> **Our commitment: your data will be used exclusively to manage your account and send the alerts you selected and will never be used for any other purpose, nor passed or disclosed to third parties.**

Don’t have an account? Go to **[Sign Up](iscriviti.md)**.

Last updated: 28/08/2026
