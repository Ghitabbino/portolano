# Se connecter — Modifier le wiki

**Accès réservé aux navigateurs inscrits.**

Saisissez les identifiants créés à l'inscription pour déverrouiller les droits d'édition du wiki.

### Connexion

<div style="background:#ffffff;border:2px solid #4db6ac;border-radius:12px;padding:22px;margin:12px auto;max-width:560px;text-align:center">
<label style="display:block;margin:10px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Email *</label>
<input id="login-email" type="email" placeholder="nom@exemple.com" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<label style="display:block;margin:14px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Mot de passe *</label>
<input id="login-pass" type="password" placeholder="votre mot de passe" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<button onclick="accedi()" style="display:block;margin:18px auto 6px;padding:12px 28px;border-radius:10px;background:linear-gradient(135deg,#4db6ac,#2e7d6f);color:#fff;font-weight:800;border:none;cursor:pointer;font-size:16px;box-shadow:0 3px 10px rgba(0,0,0,.25)">Se connecter</button>
<div id="login-msg" style="display:none;margin:10px auto;max-width:480px;padding:10px;border-radius:8px;font-size:13px"></div>
</div>

<script>
function accedi(){
  const email=document.getElementById('login-email').value.trim();
  const pass=document.getElementById('login-pass').value;
  const msg=document.getElementById('login-msg');
  if(!email||!pass){msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Veuillez saisir email et mot de passe.';return;}
  const saved=JSON.parse(localStorage.getItem('sailtropics_user')||'null');
  if(saved && saved.email===email){localStorage.setItem('sailtropics_logged','1');msg.style.display='block';msg.style.background='#e8f5e9';msg.style.border='1px solid #4caf50';msg.style.color='#1b5e20';msg.textContent='✅ OK';setTimeout(()=>location.hash='#'+(typeof PROFILO_PID!=='undefined'?PROFILO_PID:'profilo'),600);} else {msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Identifiants introuvables. Inscrivez-vous d\'abord.';}
}
</script>

*Mot de passe oublié ?* [Récupérer](#) — nous vous enverrons un lien de réinitialisation.

### Qu'est-ce qui change après la connexion

- **Consultation libre** (anonyme) : lisez tout le portolano, cartes, GPX/ZIP — aucune restriction.
- **Édition réservée** (connecté) : en haut de chaque fiche de mouillage ou de pays apparaissent les boutons **« Modifier »** et **« Ajouter une mise à jour »**. Chaque modification est enregistrée à votre nom pour traçabilité et modération.
- Vous pouvez modifier vos données et les zones pour lesquelles vous recevez des alertes à tout moment depuis la page [S'inscrire](iscriviti.md).

### Confidentialité — Notre engagement

Nous conservons uniquement l'empreinte de votre email et un jeton de session. Aucun autre usage, jamais cédé à des tiers.

> **Notre engagement : vos données seront utilisées exclusivement pour gérer votre compte et l'envoi des alertes sélectionnées et ne seront jamais utilisées à d'autres fins, ni cédées ou communiquées à des tiers.**

Vous n'avez pas de compte ? Allez à **[S'inscrire](iscriviti.md)**.

Dernière mise à jour : 28/08/2026
