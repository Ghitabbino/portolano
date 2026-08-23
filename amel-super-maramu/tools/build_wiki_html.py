#!/usr/bin/env python3
"""Genera wiki.html navigabile a partire dai file markdown in wiki/."""
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
OUT = ROOT / "wiki.html"

md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list"])

TITLES = {}
PAGES = {}

for f in sorted(WIKI.glob("*.md")):
    text = f.read_text(encoding="utf-8")
    first = text.splitlines()[0].lstrip("# ").strip()
    m = re.match(r"^(\d+)", f.stem)
    num = int(m.group(1)) if m else 99
    TITLES[num] = re.sub(r"^\d+\s*[—-]\s*", "", first)
    PAGES[num] = text

def md_to_html(text: str) -> str:
    md.reset()
    return md.convert(text)

nav_items = []
sections = []
for num in sorted(PAGES):
    pid = f"p{num}"
    title = TITLES[num]
    nav_items.append(f'<a class="navlink" href="#{pid}" data-page="{pid}">{title}</a>')
    body = PAGES[num]
    # link interni tra pagine .md -> anchor
    body = re.sub(r"\]\((\d{2}-[^)]+\.md)\)", lambda m: f"](#p{int(m.group(1)[:2])})", body)
    html = md_to_html(body)
    sections.append(f'<section id="{pid}" class="page"><h1>{title}</h1>{html}</section>')

html = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wiki AMEL Super Maramu 2000</title>
<style>
:root { --bg:#0f1720; --panel:#16222e; --ink:#dbe7f1; --muted:#8aa2b5; --accent:#4db6ac; --line:#24384a; }
* { box-sizing:border-box; }
body { margin:0; display:flex; min-height:100vh; background:var(--bg); color:var(--ink);
       font:15px/1.55 -apple-system, "Segoe UI", Roboto, sans-serif; }
aside { width:290px; flex-shrink:0; background:var(--panel); border-right:1px solid var(--line);
        padding:18px 14px; position:sticky; top:0; height:100vh; overflow-y:auto; }
aside h1 { font-size:16px; margin:0 0 12px; color:var(--accent); }
#search { width:100%; padding:8px 10px; margin-bottom:14px; border-radius:8px;
          border:1px solid var(--line); background:#0b131b; color:var(--ink); font-size:14px; }
.navlink { display:block; padding:7px 10px; border-radius:8px; color:var(--ink);
           text-decoration:none; font-size:13.5px; cursor:pointer; }
.navlink:hover { background:#1d3040; }
.navlink.active { background:var(--accent); color:#06231f; font-weight:600; }
main { flex:1; min-width:0; padding:28px clamp(14px,2.5vw,44px); }
.page { display:none; }
.page.visible { display:block; }
h1,h2,h3 { color:#fff; line-height:1.25; }
h2 { border-bottom:1px solid var(--line); padding-bottom:6px; margin-top:34px; }
table { border-collapse:collapse; width:100%; margin:14px 0; font-size:14px; }
th,td { border:1px solid var(--line); padding:7px 10px; text-align:left; vertical-align:top; word-break:break-word; }
th { background:#1d3040; color:#fff; }
tr:nth-child(even) td { background:#131e29; }
img { max-width:100%; }
code { background:#0b131b; border:1px solid var(--line); padding:1px 5px; border-radius:5px;
       font-size:13px; color:#ffd54f; }
pre code { display:block; padding:12px; overflow-x:auto; }
blockquote { border-left:3px solid var(--accent); margin:14px 0; padding:4px 16px;
             background:#131e29; color:var(--muted); }
a { color:var(--accent); }
hr { border:none; border-top:1px solid var(--line); margin:26px 0; }
li { margin:3px 0; }
@media (max-width:800px){ aside{position:static;width:auto;height:auto;} body{flex-direction:column;} }
</style>
</head>
<body>
<aside>
  <h1>⛵ Super Maramu 2000</h1>
  <input id="search" type="search" placeholder="Cerca nella wiki…">
  <nav id="nav">__NAV__</nav>
</aside>
<main>
__SECTIONS__
</main>
<script>
const links=[...document.querySelectorAll('.navlink')];
function show(id){
  document.querySelectorAll('.page').forEach(p=>p.classList.toggle('visible',p.id===id));
  links.forEach(l=>l.classList.toggle('active',l.dataset.page===id));
  window.scrollTo(0,0);
}
links.forEach(l=>l.addEventListener('click',e=>{e.preventDefault();show(l.dataset.page);}));
document.addEventListener('click',e=>{
  const a=e.target.closest('main a[href^="#"]');
  if(!a)return;
  const el=document.getElementById(a.getAttribute('href').slice(1));
  if(!el)return;
  e.preventDefault();
  const page=el.closest('.page');
  if(page&&!page.classList.contains('visible'))show(page.id);
  setTimeout(()=>el.scrollIntoView({behavior:'smooth',block:'start'}),60);
});
window.addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(document.getElementById(id))show(id);});
document.getElementById('search').addEventListener('input',e=>{
  const q=e.target.value.toLowerCase();
  links.forEach(l=>{
    const page=document.getElementById(l.dataset.page);
    l.style.display=(!q||page.textContent.toLowerCase().includes(q))?'':'none';
  });
});
show('p0');
</script>
</body>
</html>
"""
html = html.replace("__NAV__", "\n".join(nav_items)).replace("__SECTIONS__", "\n".join(sections))
OUT.write_text(html, encoding="utf-8")
print(f"OK -> {OUT} ({OUT.stat().st_size} byte, {len(PAGES)} pagine)")
