# Entrar — Editar o wiki

**Acesso reservado a navegadores registrados.**

Insira as credenciais criadas na inscrição para desbloquear as permissões de edição do wiki.

### Login

<div style="background:#ffffff;border:2px solid #4db6ac;border-radius:12px;padding:22px;margin:12px auto;max-width:560px;text-align:center">
<label style="display:block;margin:10px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Email *</label>
<input id="login-email" type="email" placeholder="nome@exemplo.com" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<label style="display:block;margin:14px auto 4px;max-width:480px;font-weight:800;color:#0f1720;text-align:left">Senha *</label>
<input id="login-pass" type="password" placeholder="sua senha" style="width:100%;max-width:480px;display:block;margin:8px auto;padding:12px 14px;border-radius:8px;border:2px solid #0f1720;background:#f0f4f8;color:#0f1720;font-size:16px">
<button onclick="accedi()" style="display:block;margin:18px auto 6px;padding:12px 28px;border-radius:10px;background:linear-gradient(135deg,#4db6ac,#2e7d6f);color:#fff;font-weight:800;border:none;cursor:pointer;font-size:16px;box-shadow:0 3px 10px rgba(0,0,0,.25)">Entrar</button>
<div id="login-msg" style="display:none;margin:10px auto;max-width:480px;padding:10px;border-radius:8px;font-size:13px"></div>
</div>

<script>
function accedi(){
  const email=document.getElementById('login-email').value.trim();
  const pass=document.getElementById('login-pass').value;
  const msg=document.getElementById('login-msg');
  if(!email||!pass){msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Insira email e senha.';return;}
  const saved=JSON.parse(localStorage.getItem('sailtropics_user')||'null');
  if(saved && saved.email===email){localStorage.setItem('sailtropics_logged','1');msg.style.display='block';msg.style.background='#e8f5e9';msg.style.border='1px solid #4caf50';msg.style.color='#1b5e20';msg.textContent='✅ OK';setTimeout(()=>location.hash='#'+(typeof PROFILO_PID!=='undefined'?PROFILO_PID:'profilo'),600);} else {msg.style.display='block';msg.style.background='#ffebee';msg.style.border='1px solid #d32f2f';msg.style.color='#b71c1c';msg.textContent='Credenciais não encontradas. Inscreva-se primeiro.';}
}
</script>

*Esqueceu a senha?* [Recuperar](#) — enviaremos um link de redefinição.

### O que muda após o login

- **Consulta livre** (anônimo): leia todo o roteiro, cartas, GPX/ZIP — sem restrições.
- **Edição reservada** (conectado): no topo de cada ficha de fundeio ou país você verá os botões **“Editar”** e **“Adicionar atualização”**. Cada edição fica salva em seu nome para rastreabilidade e moderação.
- Você pode alterar seus dados e as áreas pelas quais recebe alertas a qualquer momento na página [Inscrever-se](iscriviti.md).

### Privacidade — Nosso compromisso

Guardamos apenas o hash do seu email e um token de sessão. Nenhum outro uso, nunca repassado a terceiros.

> **Nosso compromisso: seus dados serão usados exclusivamente para gerenciar sua conta e o envio dos alertas selecionados e nunca serão usados para outros fins, nem repassados ou comunicados a terceiros.**

Não tem conta? Vá para **[Inscrever-se](iscriviti.md)**.

Última atualização: 28/08/2026
