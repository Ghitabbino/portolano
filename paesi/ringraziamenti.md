# Ringraziamenti — Grazie a chi tiene in rotta il Portolano

> Portolano è gratuito, open e senza pubblicità perché esiste una community che lo sostiene. Qui ringraziamo chi dona — in forma anonima o con nickname — su Ko-fi, Patreon e GitHub Sponsors. GDPR 100%: nessun dato venduto, solo ciò che autorizzi.

<div id="sponsors-grid" style="display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:12px; margin:16px 0">Caricamento ringraziamenti…</div>

<script>
fetch('sponsors.json').then(r=>r.json()).then(d=>{
  const g=document.getElementById('sponsors-grid');
  if(!d||!d.length){ g.innerHTML='<div style="border:1px solid var(--line);border-radius:10px;padding:14px;text-align:center;color:var(--muted)">Ancora nessun sostenitore — sii il primo su <a href="https://ko-fi.com/sailtropics" target="_blank" style="color:var(--accent)">Ko-fi</a> o <a href="https://github.com/sponsors/Ghitabbino" target="_blank" style="color:var(--accent)">GitHub Sponsors</a></div>'; return; }
  g.innerHTML=d.map(s=>{
    const nick = s.nick==='anonimo' ? '🌊 Anonimo' : '⛵ '+s.nick;
    const via = s.via ? ' · '+s.via : '';
    return `<div style="border:1px solid var(--line);border-radius:10px;padding:12px;text-align:center;background:#0b131b"><div style="font-weight:800;color:var(--accent)">${nick}</div><div style="font-size:11px;color:var(--muted)">${s.date||''}${via}</div>${s.msg?'<div style="font-size:12px;color:var(--ink);margin-top:6px;font-style:italic">“'+s.msg+'”</div>':''}</div>`;
  }).join('');
}).catch(()=>{ document.getElementById('sponsors-grid').innerHTML='<div style="color:var(--muted);text-align:center">Impossibile caricare i ringraziamenti offline.</div>'; });
</script>

Sostieni anche tu: [☕ Ko-fi](https://ko-fi.com/sailtropics) · [GitHub Sponsors](https://github.com/sponsors/Ghitabbino) — 100% trasparente in [Trasparenza open-book](trasparenza.md).

Ultimo aggiornamento: 28/08/2026
