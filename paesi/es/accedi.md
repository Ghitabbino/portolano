# Iniciar sesión — Editar la wiki

**Acceso reservado a navegantes registrados.**

Introduce las credenciales creadas al suscribirte para desbloquear los permisos de edición de la wiki.

### Acceso

<div style="background:#ffffff;border:2px solid #4db6ac;border-radius:12px;padding:22px;margin:12px auto;max-width:560px;text-align:center">
<label style="display:block;margin:10px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Email *</label>
<input id="login-email" type="email" placeholder="nombre@ejemplo.com" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<label style="display:block;margin:14px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Contraseña *</label>
<input id="login-pass" type="password" placeholder="tu contraseña" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<button onclick="accedi()" style="display:block;margin:18px auto 6px;padding:12px 28px;border-radius:10px;background:linear-gradient(135deg,#4db6ac,#2e7d6f);color:#fff;font-weight:800;border:none;cursor:pointer;font-size:16px;box-shadow:0 3px 10px rgba(0,0,0,.25)">Iniciar sesión</button>
<div id="login-msg" style="display:none;margin:10px auto;max-width:480px;padding:10px;border-radius:8px;font-size:13px"></div>
</div>

<script>
function accedi(){
  const email=document.getElementById('login-email').value.trim();
  const pass=document.getElementById('login-pass').value;
  const msg=document.getElementById('login-msg');
  if(!email||!pass){msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Introduce email y contraseña.';return;}
  const saved=JSON.parse(localStorage.getItem('sailtropics_user')||'null');
  if(saved && saved.email===email){localStorage.setItem('sailtropics_logged','1');msg.style.display='block';msg.style.background='#e8f5e9';msg.style.border='1px solid #4caf50';msg.style.color='#1b5e20';msg.textContent='✅ OK';setTimeout(()=>location.hash='#'+(typeof PROFILO_PID!=='undefined'?PROFILO_PID:'profilo'),600);} else {msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Credenciales no encontradas. Suscríbete primero.';}
}
</script>

*¿Olvidaste la contraseña?* [Recuperar](#) — te enviaremos un enlace de restablecimiento.

### Qué cambia después de iniciar sesión

- **Consulta libre** (anónimo): lee todo el derrotero, cartas, GPX/ZIP — sin restricciones.
- **Edición reservada** (conectado): en la parte superior de cada ficha de fondeo o país verás los botones **“Editar”** y **“Añadir actualización”**. Cada edición queda guardada a tu nombre para trazabilidad y moderación.
- Puedes modificar tus datos y las zonas por las que recibes alertas en cualquier momento desde la página [Suscribirse](iscriviti.md).

### Privacidad — Nuestro compromiso

Guardamos solo el hash de tu email y un token de sesión. Ningún otro uso, nunca cedido a terceros.

> **Nuestro compromiso: tus datos se usarán exclusivamente para gestionar tu cuenta y el envío de las alertas seleccionadas y nunca se usarán para otros fines, ni se cederán o comunicarán a terceros.**

¿No tienes cuenta? Ve a **[Suscribirse](iscriviti.md)**.

Última actualización: 28/08/2026
