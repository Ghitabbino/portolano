# ✅ TRACCIA AGENTI — Checklist Obbligatoria

> **REGOLA GENERALE PER TUTTI GLI AGENTI:** Prima di chiudere qualsiasi task, verifica questo file. Se un agente dimentica una cosa, il successivo deve accorgersene e completarla. Nessun agente può dichiarare “fatto” se questa traccia non è al 100%. Questa regola vale per sempre, per tutti gli agenti, su tutti i task.

**Ultimo aggiornamento:** 28/08/2026 — 17 task tracciati (POD catalog aggiunto)
**Repo:** Ghitabbino/portolano — branch main — GitHub Pages + sailtropics.com

---

## 1. ISCRIZIONE — Finestra flag rimossa
- [x] `iscriviti.html:12` + `paesi/iscriviti.html:12` + `paesi/iscriviti.md:21` — cancellata #reg-tree con 6 flag oceani, sostituita con testo `per selezionare le aree dei tuoi alert accedi alla tua pagina personale` → link `profilo.html` / `profilo.md`
- Verifica: `grep -n "reg-tree" iscriviti.html` deve dare 0, `grep -n "pagina personale" iscriviti.html` deve dare 1

## 2. ALBERO 3 LIVELLI PROFILO
- [x] `paesi/profilo.md` + `profilo.html` (root/paesi) — albero con checkbox flag per oceano (tutto l’oceano), click nome apre zone, flag zona = tutta la zona, click nome zona apre paesi/sotto-zone, propagazione visiva, salvataggio `sel[]`
- Verifica: `grep -n "alert-tree" paesi/profilo.md` e `profilo.html` deve dare 1

## 3. PAGINA PERSONALE COMPLETA
- [x] `paesi/profilo.md` + `profilo.html` — albero + canali `Mail/WhatsApp/Telegram` + pulsante `Contribuisci` → `contribuisci.md` + verifica mail con `verifica.html?token=` e `sailtropics_logged`
- Verifica: `grep -n "Canali di ricezione" paesi/profilo.md` e `grep -n "Contribuisci" paesi/profilo.md`

## 4. PROFILO TEST MEOLO
- [x] Creato e poi cancellato — flusso pulito verificato via `fix-meolo.html` (auto-crea meolo/1234)
- Verifica: `fix-meolo.html` esiste e imposta `localStorage`

## 5. SEZIONE C FREQUENZA SPOSTATA
- [x] `paesi/iscriviti.md:27` + `iscriviti.html:13` — rimossa Sezione C `Frequenza` (2 checkbox), ora solo in `paesi/profilo.md:26` + `profilo.html:26` con `Istantaneo`/`Settimanale`, salvata in `saved.freq`
- Verifica: `grep -n "Frequenza" iscriviti.html` deve dare 0, `grep -n "Frequenza" paesi/profilo.md` deve dare 1

## 6. PUBBLICAZIONE
- [x] `paesi/tools/build_paesi_html.py` → `paesi.html` + `paesi-mobile.html` + `index.html` (landing) + `git add -A && git commit && git push` — sync `index.html = copia di paesi.html` per root
- Verifica: `ls -lh index.html paesi/paesi.html` e `git log --oneline -3`

## 7. SELETTORE LINGUE 6 LINGUE
- [x] Top-right `paesi/tools/build_paesi_html.py:85` `#lang-switch` con `English, Français, Español, Deutsch, Português, Italiano` (no bandiere), struttura `/it /en /fr /es /de /pt` con `it/index.html` etc., sync `pid` via `path.replace('/it/','/en/') + hash`, ricerca `normalize('NFD')` per accenti/ü/ñ
- Verifica: `grep -n "lang-switch" it/index.html` e `ls -ld it en fr es de pt`

## 8. DOMINIO CUSTOM SAILTROPICS
- [x] Mantenere `ghitabbino.github.io/portolano` + `sailtropics.com` via `CNAME` + DNS `A 185.199.108.153` etc., `Enforce HTTPS`, `x-default` EN
- Verifica: `cat CNAME` (quando registrato) e `grep -n "hreflang" it/index.html`

## 9. I18N E BREADCRUMB
- [x] `paesi/i18n/*.json` (it,en,fr,es,de,pt) con chiavi `search_placeholder`, `portolano`, `last_updated`, `breadcrumb_home` etc., `TEMPLATE` usa solo `__I18N_key__`, `build_paesi_html.py:1128` `_apply_i18n()`, breadcrumb `paesi/tools/build_paesi_html.py:89` `.breadcrumb` + `paesi/tools/build_paesi_html.py:299` `<nav class="breadcrumb" data-bc>` sopra H1, `updateBreadcrumb()` con `I18N.breadcrumb_home` + `chain()`, IT non primo (EN primo, `LANGUAGES={'en','fr','es','de','pt','it'}`)
- Verifica: `grep -n "breadcrumb" it/index.html` e `cat paesi/i18n/en.json | grep search_placeholder`

## 10. STRUTTURA ISOLATA + SIDEBAR CONDIZIONALE
- [x] `paesi/it/`, `paesi/en/`, `paesi/fr/`, `paesi/es/`, `paesi/de/`, `paesi/pt/` — 1457 md ciascuna, speculare, stessi ID `cuba/01-clearance.md` in tutte, `NON_PAESE` esclude `it|en|fr|es|de|pt|i18n`, `paesi/sidebar.{lang}.json` con 61 paesi stessi ID, `build_paesi_html.py` carica `sidebar.{lang}.json` in base a `curLang`
- Verifica: `find paesi/it -name '*.md' | wc -l` 1457 e `cat paesi/sidebar.en.json | grep -A2 '"id": "cuba"'`

## 11. LOGOUT + MANTIENIMI COLLEGATO
- [x] `accedi.html:14` + `paesi/accedi.html:14` — checkbox `Mantienimi collegato` (`id="keep-logged"`), `login()` usa `localStorage` se checked altrimenti `sessionStorage`, `paesi/tools/build_paesi_html.py:599` `logout-side` con `logoutGlobal()` sempre visibile in sidebar quando loggato
- Verifica: `grep -n "keep-logged" accedi.html` e `grep -n "logout-side" paesi/tools/build_paesi_html.py`

## 12. CTA DONAZIONI NAVBAR + FOOTER
- [x] Navbar top-right `paesi/tools/build_paesi_html.py:85` `#support-cta` con `__I18N_support_us__` → `https://ko-fi.com/sailtropics`, minimale outline `border:1px solid var(--accent)`, non invasivo; Footer `paesi/tools/build_paesi_html.py:650` `<footer>__I18N_footer_support__</footer>` con riga pulita open-source
- Verifica: `grep -n "support-cta" it/index.html` e `grep -n "footer" it/index.html`

## 13. TRADUZIONI ESATTE CTA E FOOTER
- [x] `paesi/i18n/en.json:21` `support_us:"☕ Support Us"` + `footer_support:"Portolano is an open-source, independent, and ad-free project..."` etc. per FR/ES/DE/PT con testi forniti, IT `☕ Sostienici`
- Verifica: `cat paesi/i18n/en.json | grep support_us` e `cat paesi/i18n/fr.json | grep footer_support`

## 14. TRASPARENZA COSTI OPEN-BOOK
- [x] `paesi/costs.json` + `paesi/trasparenza.md` (IT) + `paesi/en/transparency.md` etc. con tabella `Hosting 12€/mese, Domini 5€/mese, API traduzione 30€/mese` — aggiornabile dicendo costi all'agente
- Verifica: `cat paesi/costs.json` e `grep -n "Trasparenza" paesi/trasparenza.md`

## 15. CONTRIBUTORS DINAMICO
- [x] `paesi/ringraziamenti.md` + `paesi/sponsors.json` — griglia `sponsors-grid` che legge `sponsors.json` (anonimo o nickname), `tools/fetch_sponsors.py` per Ko-fi/Patreon/GitHub Sponsors, GDPR, no tracking
- Verifica: `cat paesi/sponsors.json` e `grep -n "sponsors-grid" paesi/ringraziamenti.md`

## 16. FIX MEOLO + CANCELLAZIONE IMMEDIATA
- [x] `fix-meolo.html` (root/paesi/it) auto-crea meolo/1234 e redirect a `it/index.html#p5`, `paesi/profilo.md:8` bottone `Disiscrizione — cancella tutto` con `confirm` + `localStorage.clear()` immediata, link anche in sidebar
- Verifica: `grep -n "Disiscrizione" paesi/profilo.md` e `cat fix-meolo.html | grep meolo`

## 17. CATALOGO MERCH POD ETICO — 3 CATEGORIE (Product Manager POD)
- [ ] **CATEGORIA 1 ABBIGLIAMENTO BIO (Portolano & Sailtropics):** T-shirt/felpe cotone bio 100%, PNG trasparente, varianti colore
- [ ] **CATEGORIA 2 CANCELLERIA SCRIVANIA (Portolano):** Taccuini copertina rigida, tazze ufficio, adesivi fustellati
- [ ] **CATEGORIA 3 ATTREZZATURA TECNICA BORDO (Sailtropics):** Bandiere/guidoni vento, sacche stagne dry bags, tazze acciaio con moschettone, asciugamani microfibra antisalsedine — focus UV/vento/acqua mare
- Per ogni gadget scheda: 1) Dimensioni file DPI 300+ pixel sRGB/CMYK 2) Tipo stampa DTG/Sublimazione/UV 3) Posizionamento logo 4) Margine etico 4-10€ (costo fornitore vs prezzo vendita) — primo prodotto Bandiera/Guidone in coda
- Verifica: `cat AGENTI_HANDOFF.md | grep -A5 "CATEGORIA 3"` e `ls merch/` (da creare)

---

**REGOLA PER OGNI AGENTE:** Prima di `git push`, esegui `python3 tools/build_paesi_html.py` e verifica che ogni voce sopra dia esito positivo (grep). Se una voce è `[ ]` (non fatta), completala prima di dichiarare finito. Questa traccia è l'unica verità — non fidarti di "già fatto" a voce.

**TODO SEMPRE VISIBILE:** Non fermarsi a 5 task — ogni nuova richiesta aggiunge una riga qui, con stato `pending` → `in_progress` → `completed`. La lista resta sempre in `AGENTI_TRACCIA.md` e in `TodoWrite`.

