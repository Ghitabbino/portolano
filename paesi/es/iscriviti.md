# Suscribirse — Únete a la flota

<div style="background:linear-gradient(135deg,#0f1720 0%,#1e3a4a 100%);border:2px solid #4db6ac;border-radius:16px;padding:20px;margin:14px 0;color:#dbe7f1">
<div style="font-size:28px;margin-bottom:6px">⛵ ¡Bienvenido a bordo, Capitán!</div>
<div style="font-size:15px;line-height:1.6">Suscríbete en 30 segundos para recibir <b>alertas de seguridad</b> y <b>contribuir</b> al derrotero. Sin suscripción navegas igualmente gratis por todo.</div>
</div>

### 1 — Quién eres

<div style="background:#ffffff;border:2px solid #4db6ac;border-radius:12px;padding:16px;margin:10px 0">
<label style="display:block;margin:14px auto 4px;max-width:520px;font-weight:800;color:#0f1720;text-align:left">Apodo *</label>
<input id="reg-nick" type="text" placeholder="ej. lobo_de_mar" style="width:100%;max-width:520px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<label style="display:block;margin:14px auto 4px;max-width:520px;font-weight:800;color:#0f1720;text-align:left">Email *</label>
<input id="reg-email" type="email" placeholder="nombre@ejemplo.com" style="width:100%;max-width:520px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<label style="display:block;margin:14px auto 4px;max-width:520px;font-weight:800;color:#0f1720;text-align:left">Contraseña *</label>
<input id="reg-pass" type="password" placeholder="mín. 8 caracteres" style="width:100%;max-width:520px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<label style="display:block;margin:14px auto 4px;max-width:520px;font-weight:800;color:#0f1720;text-align:left">Barco <span style="font-weight:400;color:#5a6d80">(opcional)</span></label>
<input id="reg-barca" type="text" placeholder='Monocasco 40 pies' style="width:100%;max-width:520px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
</div>

### 2 — Dónde navegas

<div style="background:#fff8e1;border:2px solid #ffb74d;border-radius:12px;padding:16px;margin:10px 0;text-align:center">
<span style="color:#0f1720">para seleccionar tus zonas de alerta ve a tu <a href="profilo.md" style="color:#e65100;font-weight:800;text-decoration:underline">página personal</a></span>
</div>

<div style="text-align:center;margin:18px 0">
<button onclick="registra()" style="padding:14px 32px;border-radius:12px;background:linear-gradient(135deg,#4db6ac,#2e7d6f);color:#fff;font-weight:900;border:none;cursor:pointer;font-size:17px;box-shadow:0 4px 12px rgba(0,0,0,.3)">⛵ ¡Suscribirse gratis — Zarpar!</button>
</div>

<div id="reg-msg" style="display:none;padding:12px;border-radius:8px;margin:10px 0"></div>

<script>
function registra(){
  const nick=document.getElementById('reg-nick').value.trim();
  const email=document.getElementById('reg-email').value.trim();
  const pass=document.getElementById('reg-pass').value;
  if(!nick||!email||!pass||pass.length<8){const m=document.getElementById('reg-msg');m.style.display='block';m.style.background='#ffebee';m.style.border='2px solid #d32f2f';m.style.color='#b71c1c';m.textContent='Rellena apodo, email y contraseña (mín. 8).';return;}
  const sel=[]; const freq=['istantaneo'];
  const barca=document.getElementById('reg-barca').value.trim();
  localStorage.setItem('sailtropics_user', JSON.stringify({nick,email,barca,sel,freq,channels:['mail'],ts:Date.now(),verified:false}));
  const m=document.getElementById('reg-msg');m.style.display='block';m.style.background='#e8f5e9';m.style.border='2px solid #4caf50';m.style.color='#1b5e20';m.innerHTML='✅ ¡Hecho! Ve a <a href="#'+(typeof ACCEDI_PID!=='undefined'?ACCEDI_PID:'accedi')+'" style="color:#2e7d6f">Iniciar sesión</a> para entrar.';
  setTimeout(()=>location.hash='#'+(typeof ACCEDI_PID!=='undefined'?ACCEDI_PID:'accedi'), 800);
}
document.addEventListener('change',()=>{
  const sel=[...document.querySelectorAll('.reg-check:checked')].map(c=>c.value);
  const el=document.getElementById('reg-sel-count'); if(el) el.textContent=sel.length;
});
</script>

> **🔒 Nuestro compromiso:** tus datos se usarán exclusivamente para las alertas y nunca se cederán a terceros.

Última actualización: 28/08/2026
