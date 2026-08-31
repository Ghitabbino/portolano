# Perfil — A tua conta

<div id="profilo-box" style="border:1px solid var(--line);border-radius:10px;padding:14px;background:#0b131b;margin:10px 0">
<div style="font-weight:800;color:var(--accent)">Bem-vindo a bordo!</div>
<div id="profilo-dati" style="margin:10px 0;line-height:1.6">Caricamento…</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">
<button onclick="modificaProfil()" style="padding:7px 12px;border-radius:8px;background:var(--accent);color:#06231f;font-weight:800;border:1px solid var(--accent);cursor:pointer">Editar dados</button>
<button onclick="logout()" style="padding:7px 12px;border-radius:8px;background:transparent;color:var(--accent);font-weight:700;border:1px solid var(--line);cursor:pointer">Sair</button>
<button onclick="disiscrivi()" style="padding:7px 12px;border-radius:8px;background:#3a1a1a;color:#ffb9b9;font-weight:700;border:1px solid #d32f2f;cursor:pointer">Cancelar — apagar tudo</button>
</div>
</div>

<div style="border:1px solid var(--line);border-radius:10px;padding:14px;background:#0b131b;margin:14px 0">
<div style="font-weight:700">As tuas contribuições</div>
<div style="margin:8px 0">
- **Distintivo atual:** <span id="badge-liv">Novato ⚓</span><br>
- **Fichas atualizadas:** <span id="badge-count">0</span><br>
- **Histórico:** as tuas alterações são rastreadas em teu nome para moderação
</div>
</div>

<div id="alert-section" style="border:2px solid var(--accent);border-radius:12px;padding:16px;background:#0b131b;margin:14px 0">
<div style="font-weight:800;color:var(--accent);font-size:16px;margin-bottom:6px">🔔 As tuas áreas de alerta</div>
<div style="font-size:12px;color:var(--muted);margin-bottom:10px">Marca a <b>bandeira</b> para receber alertas de todo o nível. Clica no <b>nome</b> para abrir as zonas inferiores.</div>
<div id="alert-tree" style="max-height:520px;overflow-y:auto;overflow-x:hidden;border:1px solid var(--line);border-radius:8px;padding:10px;background:#16222e;min-height:80px">Caricamento albero…</div>
<div style="margin:12px 0 6px;font-weight:700;color:var(--ink)">Canais de receção</div>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">
<label style="display:flex;gap:6px;align-items:center;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:#16222e;cursor:pointer"><input type="checkbox" id="ch-mail" value="mail" checked> 📧 Mail</label>
<label style="display:flex;gap:6px;align-items:center;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:#16222e;cursor:pointer"><input type="checkbox" id="ch-whatsapp" value="whatsapp"> 💬 WhatsApp</label>
<label style="display:flex;gap:6px;align-items:center;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:#16222e;cursor:pointer"><input type="checkbox" id="ch-telegram" value="telegram"> ✈️ Telegram</label>
</div>
<div style="margin:12px 0 6px;font-weight:700;color:var(--ink)">Frequência</div>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">
<label style="display:flex;gap:6px;align-items:center;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:#16222e;cursor:pointer"><input type="checkbox" id="ch-istantaneo" value="istantaneo" checked> Instantâneo — só críticos L3 🚨</label>
<label style="display:flex;gap:6px;align-items:center;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:#16222e;cursor:pointer"><input type="checkbox" id="ch-settimanale" value="settimanale"> Resumo semanal</label>
</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
<button onclick="salvaAlert()" style="padding:10px 18px;border-radius:8px;background:var(--accent);color:#06231f;font-weight:800;border:1px solid var(--accent);cursor:pointer">💾 Guardar seleção</button>
<span id="alert-count" style="font-size:12px;color:var(--muted)"></span>
</div>
<div id="alert-msg" style="display:none;margin-top:10px;padding:10px;border-radius:8px;font-size:13px"></div>
</div>

<div style="text-align:center;margin:16px 0">
<a id="btn-contribuisci" href="#contribuisci" onclick="goContribuir(event)" style="display:inline-block;padding:14px 28px;border-radius:12px;background:linear-gradient(135deg,#4db6ac,#2e7d6f);color:#fff;font-weight:900;text-decoration:none;box-shadow:0 4px 12px rgba(0,0,0,.3)">✏️ Contribuir para o roteiro</a>
</div>

<script>
function renderProfil(){
  const box=document.getElementById('profilo-dati');
  const logged=localStorage.getItem('sailtropics_logged')==='1';
  const saved=JSON.parse(localStorage.getItem('sailtropics_user')||'null');
  if(!logged || !saved){box.innerHTML='Vous n\'êtes pas connecté. Allez à <a href="#'+(typeof ACCEDI_PID!=='undefined'?ACCEDI_PID:'accedi')+'" style="color:var(--accent)">Se connecter</a> ou <a href="#'+(typeof ISCRIVITI_PID!=='undefined'?ISCRIVITI_PID:'iscriviti')+'" style="color:var(--accent)">S\'inscrire</a>.'; const sec=document.getElementById('alert-section'); if(sec) sec.style.display='none'; const bc=document.getElementById('btn-contribuisci'); if(bc) bc.style.opacity='.5'; return;}
  const sec=document.getElementById('alert-section'); if(sec) sec.style.display='block';
  const aree=(saved.sel||saved.aree||[]).join(', ')||'—';
  const paesi=(saved.paesi||[]).join(', ')||'—';
  const chans=(saved.channels||['mail']).join(', ');
  box.innerHTML=`<b>Nickname:</b> ${saved.nick||'—'}<br><b>Email:</b> ${saved.email}<br><b>Barca:</b> ${saved.barca||'—'}<br><b>Aree sel.:</b> ${aree}<br><b>Paesi:</b> ${paesi}<br><b>Canali:</b> ${chans}<br><b>Frequência:</b> ${(saved.freq||[]).join(', ')||'—'}`;
  const n=parseInt(localStorage.getItem('sailtropics_count')||'0');
  const bc=document.getElementById('badge-count'); if(bc) bc.textContent=n;
  const bl=document.getElementById('badge-liv'); if(bl) bl.textContent = n>=20?'Master Skipper 🧭★': n>=5?'Navigatore d’Alizé 🧭':'Novato ⚓';
  // init channels
  const chs=new Set(saved.channels||['mail']);
  ['mail','whatsapp','telegram'].forEach(c=>{const el=document.getElementById('ch-'+c); if(el) el.checked=chs.has(c);});
  // init freq
  const frs=new Set(saved.freq||['istantaneo']);
  ['istantaneo','settimanale'].forEach(c=>{const el=document.getElementById('ch-'+c); if(el) el.checked=frs.has(c);});
}
function modificaProfil(){location.hash='#'+(typeof ISCRIVITI_PID!=='undefined'?ISCRIVITI_PID:'iscriviti');}
function logout(){localStorage.removeItem('sailtropics_logged');renderProfil(); renderAlertTree();}
function disiscrivi(){if(confirm('Apagar todos os dados locais?')){localStorage.removeItem('sailtropics_user');localStorage.removeItem('sailtropics_logged');renderProfil(); renderAlertTree(); alert('Dados apagados (demo local). Em produção apagamento definitivo no servidor e RGPD.');}}
function goContribuir(e){ if(e) e.preventDefault(); const pid=(typeof CONTRIBUISCI_PID!=='undefined'?CONTRIBUISCI_PID:null); if(pid) location.hash='#'+pid; else location.hash='#contribuisci'; }
let expanded=new Set();
function flagHtml(k){ if(typeof TREE==='undefined') return '🏝️'; const f=TREE.flag[k]||'🏝️'; return f.endsWith('.svg')?'<img src="'+f+'" alt="" style="width:22px;height:16px;object-fit:cover;border-radius:2px;vertical-align:middle">':f; }
function zonaIcon(k){ if(typeof TREE==='undefined') return '🐬'; return TREE.zona[k]||'🐬'; }
function hasSubZones(country){ if(typeof TREE==='undefined' || !TREE.zona) return []; return Object.keys(TREE.zona).filter(z=>z.startsWith(country+'/')); }
function renderAlertTree(){
  const treeEl=document.getElementById('alert-tree'); if(!treeEl) return;
  const logged=localStorage.getItem('sailtropics_logged')==='1';
  if(!logged){ treeEl.innerHTML='<div style="color:var(--muted);font-size:13px;padding:8px">Inicia sessão para selecionar as áreas.</div>'; return; }
  if(typeof TREE==='undefined'){ treeEl.innerHTML='<div style="color:#ffb74d">Caricamento…</div>'; setTimeout(renderAlertTree,300); return; }
  const saved=JSON.parse(localStorage.getItem('sailtropics_user')||'{}');
  const sel=new Set(saved.sel||saved.aree||[]);
  let h='';
  TREE.regions.forEach(reg=>{
    const regKey=reg.k;
    const checked=sel.has(regKey);
    const hasChildren=(reg.subs.length>0 || reg.p.length>0);
    const isExp=expanded.has(regKey);
    h+=`<div style="margin:6px 0"><div style="display:flex;gap:8px;align-items:center;padding:6px 8px;border-radius:8px;background:#0b131b;border:1px solid ${checked?'var(--accent)':'var(--line)'}">`
      +`<input type="checkbox" class="alert-check" data-key="${regKey}" ${checked?'checked':''} style="width:16px;height:16px">`
      +`<span style="font-size:18px">${reg.i}</span>`
      +`<a href="#" data-expand="${regKey}" style="color:${checked?'var(--accent)':'var(--ink)'};font-weight:700;text-decoration:none;flex:1">${reg.l}</a>`
      +`${hasChildren?`<span style="color:var(--muted);font-size:14px">${isExp?'‹':'›'}</span>`:''}`
      +`</div>`;
    if(hasChildren){
      h+=`<div data-children="${regKey}" style="display:${isExp?'block':'none'};margin:4px 0 4px 18px;border-left:2px solid var(--line);padding-left:10px">`;
      // macros / bacini
      reg.subs.forEach(sub=>{
        const subKey=sub.k;
        const subChecked=sel.has(subKey);
        const subExp=expanded.has(subKey);
        const subHas=sub.p.length>0;
        h+=`<div style="margin:6px 0"><div style="display:flex;gap:8px;align-items:center;padding:5px 8px;border-radius:8px;background:#0f1720;border:1px solid ${subChecked?'var(--accent)':'var(--line)'}">`
          +`<input type="checkbox" class="alert-check" data-key="${subKey}" ${subChecked?'checked':''} style="width:15px;height:15px">`
          +`<span style="font-size:16px">${sub.i||'🗺️'}</span>`
          +`<a href="#" data-expand="${subKey}" style="color:${subChecked?'var(--accent)':'var(--ink)'};font-weight:600;text-decoration:none;flex:1;font-size:14px">${sub.l}</a>`
          +`${subHas?`<span style="color:var(--muted)">${subExp?'‹':'›'}</span>`:''}`
          +`</div>`;
        if(subHas){
          h+=`<div data-children="${subKey}" style="display:${subExp?'block':'none'};margin:4px 0 4px 14px;border-left:2px dashed var(--line);padding-left:8px">`;
          sub.p.forEach(pk=>{
            const pkChecked=sel.has(pk);
            const zones=hasSubZones(pk);
            const pkExp=expanded.has(pk);
            h+=`<div style="margin:4px 0"><div style="display:flex;gap:7px;align-items:center;padding:4px 8px;border-radius:8px;background:#0b131b;border:1px solid ${pkChecked?'var(--accent)':'var(--line)'}">`
              +`<input type="checkbox" class="alert-check" data-key="${pk}" ${pkChecked?'checked':''} style="width:14px;height:14px">`
              +`<span style="font-size:16px">${flagHtml(pk)}</span>`
              +`<a href="#" ${zones.length?`data-expand="${pk}"`:''} style="color:${pkChecked?'var(--accent)':'var(--ink)'};font-size:13px;font-weight:600;text-decoration:none;flex:1">${TREE.lbl[pk]||pk}</a>`
              +`${zones.length?`<span style="color:var(--muted);font-size:13px">${pkExp?'‹':'›'}</span>`:''}`
              +`</div>`;
            if(zones.length){
              h+=`<div data-children="${pk}" style="display:${pkExp?'block':'none'};margin:3px 0 3px 12px;border-left:1px solid var(--line);padding-left:8px">`;
              zones.forEach(zk=>{
                const zkChecked=sel.has(zk);
                const lbl=zk.split('/').pop().replace(/-/g,' ').replace(/\b\w/g,c=>c.toUpperCase());
                h+=`<div style="display:flex;gap:7px;align-items:center;padding:3px 6px;margin:2px 0;border-radius:6px;background:#0f1720;border:1px solid ${zkChecked?'var(--accent)':'var(--line)'}">`
                  +`<input type="checkbox" class="alert-check" data-key="${zk}" ${zkChecked?'checked':''} style="width:13px;height:13px">`
                  +`<span style="font-size:14px">${zonaIcon(zk)}</span>`
                  +`<span style="color:${zkChecked?'var(--accent)':'var(--ink)'};font-size:12.5px;flex:1">${lbl}</span>`
                  +`</div>`;
              });
              h+=`</div>`;
            }
            h+=`</div>`;
          });
          h+=`</div>`;
        }
        h+=`</div>`;
      });
      // direct countries
      reg.p.forEach(pk=>{
        const pkChecked=sel.has(pk);
        const zones=hasSubZones(pk);
        const pkExp=expanded.has(pk);
        h+=`<div style="margin:4px 0"><div style="display:flex;gap:7px;align-items:center;padding:4px 8px;border-radius:8px;background:#0f1720;border:1px solid ${pkChecked?'var(--accent)':'var(--line)'}">`
          +`<input type="checkbox" class="alert-check" data-key="${pk}" ${pkChecked?'checked':''} style="width:14px;height:14px">`
          +`<span style="font-size:16px">${flagHtml(pk)}</span>`
          +`<a href="#" ${zones.length?`data-expand="${pk}"`:''} style="color:${pkChecked?'var(--accent)':'var(--ink)'};font-size:13px;font-weight:600;text-decoration:none;flex:1">${TREE.lbl[pk]||pk}</a>`
          +`${zones.length?`<span style="color:var(--muted)">${pkExp?'‹':'›'}</span>`:''}`
          +`</div>`;
        if(zones.length){
          h+=`<div data-children="${pk}" style="display:${pkExp?'block':'none'};margin:3px 0 3px 12px;border-left:1px solid var(--line);padding-left:8px">`;
          zones.forEach(zk=>{
            const zkChecked=sel.has(zk);
            const lbl=zk.split('/').pop().replace(/-/g,' ').replace(/\b\w/g,c=>c.toUpperCase());
            h+=`<div style="display:flex;gap:7px;align-items:center;padding:3px 6px;margin:2px 0;border-radius:6px;background:#0f1720;border:1px solid ${zkChecked?'var(--accent)':'var(--line)'}">`
              +`<input type="checkbox" class="alert-check" data-key="${zk}" ${zkChecked?'checked':''} style="width:13px;height:13px">`
              +`<span style="font-size:14px">${zonaIcon(zk)}</span>`
              +`<span style="color:${zkChecked?'var(--accent)':'var(--ink)'};font-size:12.5px;flex:1">${lbl}</span>`
              +`</div>`;
          });
          h+=`</div>`;
        }
        h+=`</div>`;
      });
      h+=`</div>`;
    }
    h+=`</div>`;
  });
  treeEl.innerHTML=h;
  // listeners expand
  treeEl.querySelectorAll('a[data-expand]').forEach(a=>{
    a.addEventListener('click',e=>{
      e.preventDefault();
      const k=a.dataset.expand;
      if(expanded.has(k)) expanded.delete(k); else expanded.add(k);
      renderAlertTree();
    });
  });
  // listeners checkbox propagate to children
  treeEl.querySelectorAll('.alert-check').forEach(cb=>{
    cb.addEventListener('change',e=>{
      const k=cb.dataset.key;
      const checked=cb.checked;
      // propagate to descendants
      // find children container
      const childCont=treeEl.querySelector(`div[data-children="${CSS.escape(k)}"]`);
      if(childCont){
        childCont.querySelectorAll('.alert-check').forEach(ch=>{ ch.checked=checked; });
      }
      // if unchecking a child, uncheck ancestors? keep ancestors as is (user can manage)
      updateAlertCount();
    });
  });
  updateAlertCount();
}
function updateAlertCount(){
  const c=document.querySelectorAll('#alert-tree .alert-check:checked').length;
  const el=document.getElementById('alert-count'); if(el) el.textContent=c?`${c} selecionadas`:'nenhuma seleção';
}
function salvaAlert(){
  const sel=[...document.querySelectorAll('#alert-tree .alert-check:checked')].map(c=>c.dataset.key);
  const channels=[...document.querySelectorAll('#alert-section input[id^="ch-mail"], #alert-section input[id^="ch-whatsapp"], #alert-section input[id^="ch-telegram"]:checked')].map(c=>c.value);
  // fallback: prendi tutti i ch- dentro alert-section ma filtra per canali
  const chs=[...document.querySelectorAll('#ch-mail, #ch-whatsapp, #ch-telegram')].filter(c=>c.checked).map(c=>c.value);
  const chans=chs.length?chs:channels.filter(v=>['mail','whatsapp','telegram'].includes(v));
  const freq=[...document.querySelectorAll('#ch-istantaneo, #ch-settimanale')].filter(c=>c.checked).map(c=>c.value);
  if(chans.length===0){ const m=document.getElementById('alert-msg'); m.style.display='block'; m.style.background='#3a1a1a'; m.style.border='1px solid #d32f2f'; m.style.color='#ffb9b9'; m.textContent='Seleciona pelo menos um canal (Mail, WhatsApp ou Telegram).'; return; }
  if(freq.length===0){ const m=document.getElementById('alert-msg'); m.style.display='block'; m.style.background='#3a1a1a'; m.style.border='1px solid #d32f2f'; m.style.color='#ffb9b9'; m.textContent='Seleciona pelo menos uma frequência.'; return; }
  const saved=JSON.parse(localStorage.getItem('sailtropics_user')||'{}');
  saved.sel=sel; saved.aree=sel; saved.channels=chans; saved.freq=freq;
  // compat: paesi/aree legacy
  saved.paesi=sel.filter(k=>!k.includes('/') || Object.keys(TREE.lbl||{}).includes(k));
  localStorage.setItem('sailtropics_user', JSON.stringify(saved));
  const m=document.getElementById('alert-msg'); m.style.display='block'; m.style.background='#0f2e1f'; m.style.border='1px solid var(--accent)'; m.style.color='#b9f5c8';
  m.innerHTML=`✅ Guardado: ${sel.length} áreas, canais: ${chans.join(', ')}, freq: ${freq.join(', ')}`;
  renderProfil();
  setTimeout(()=>{m.style.display='none'}, 3000);
}
renderProfil();
renderAlertTree();
window.addEventListener('hashchange', ()=>{ renderProfil(); renderAlertTree(); });
</script>

> **Privacidade — o nosso compromisso:** os teus dados são usados apenas para os alertas selecionados e nunca serão cedidos a terceiros.

[ Voltar a Áreas](00-indice.md) · [Offline & GPX](offline-gpx.md)

Dernière mise à jour: 28/08/2026
