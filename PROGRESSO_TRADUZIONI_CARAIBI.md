# Progresso Traduzioni — Mar dei Caraibi IT → EN/FR/ES/DE/PT

**Regola scolpita 31/08/2026 — AGENTI_HANDOFF.md:16d (vale per TUTTI, per SEMPRE):** traduzione **lineare per PAESE: un paese alla volta completamente in TUTTE le lingue (IT→EN→FR→ES→DE→PT)** (`00→10` + `ancoraggi/*.md` + `ristoranti/*.md`), **ordine pesanti-first** (peso IT decrescente). **Un paese è ☑ solo quando EN+FR+ES+DE+PT sono madrelingua verificati.**  
**Non cancellare** i compiti svolti — spunta la casella. Fonte di verità per l'avanzamento.

> Aggiornato: 01-09-2026 — REGOLA 16d lineare per PAESE. Barbados 5 lingue ☑ 31/08. Bonaire 5 lingue ☑ 01/09 (EN 23 md + FR 23 md + ES 23 md + DE 23 md + PT 23 md, 08 + 4 anc + 8 rist riscritti, grep IT 0, build OK).

## Stato generale
- [x] **Prima pagina:** traduzione “Scorri — trasparenza, ringraziamenti e supporto sotto” in tutte le lingue (IT/EN/FR/ES/DE/PT) — `paesi/i18n/*.json:scroll_hint` + `build_paesi_html.py:674` — verificato in `it/en/fr/es/de/pt/index.html`
- [x] Fix precedenti mantenuti visibili (Cabo Verde → globale REGOLA 16b, fix hide #p1)
- [x] **Barbados 5 lingue:** riscrittura completa EN+FR+ES+DE+PT madrelingua verificata (30 file x5 = 150 md), `grep IT leak 0`, markers tradotti, build `en/fr/es/de/pt/index.html` — `paesi/{en,fr,es,de,pt}/barbados/*.md:1`
- [x] **Bonaire 5 lingue:** riscrittura completa EN+FR+ES+DE+PT madrelingua (23 file x5 = 115 md), `grep IT leak 0`, 08 + 4 anc + 8 rist riscritti, markers tradotti, build 6 lingue — `paesi/{en,fr,es,de,pt}/bonaire/*.md:1`

## Coda pesanti-first — IT → EN/FR/ES/DE/PT (ordine di esecuzione, 31/08/2026)

> Peso = somma byte `paesi/it/<slug>/*.md` (proxy completezza). Legenda: ☐ da fare — ☑ fatto madrelingua in TUTTE le 5 lingue — ⏳ in corso (EN→FR→ES→DE→PT). I file esistono come bozza ma vanno rifatti madrelingua per ogni lingua. Skip se già ☑ 5 lingue.

- [x] 01. **Barbados** — `barbados` (92 974 B) — ☑ COMPLETATO 31/08 — EN ☑ (30 md) · FR ☑ (30 md, verificato madrelingua, 59 DONNÉE MANQUANTE) · ES ☑ (30 md riscritti, 59 DATO FALTANTE, markers ES) · DE ☑ (30 md, 59 DATEN FEHLEN) · PT ☑ (30 md riscritti, 58 DADO EM FALTA) — `grep IT leak 0` + build 6 lingue OK
- [x] 02. **Bonaire** — `bonaire` (92 924 B) — ☑ COMPLETATO 01/09 — EN ☑ (23 md) · FR ☑ (23 md, 20 DONNÉE MANQUANTE) · ES ☑ (23 md, 20 DATO FALTANTE) · DE ☑ (23 md, 22 DATEN FEHLEN) · PT ☑ (23 md, 22 DADO EM FALTA) — `grep IT leak 0` + build 6 lingue OK
- [ ] 03. **Aruba** — `aruba` (86 987 B) — ☐ 00 EN ☑ — 01-10 EN in corso
- [ ] 04. **Repubblica Dominicana** — `repubblica-dominicana` (82 211 B)
- [ ] 05. **Cuba** — `cuba` (76 349 B)
- [ ] 06. **Giamaica** — `giamaica` (69 712 B)
- [ ] 07. **Grenada** — `grenada` (69 397 B)
- [ ] 08. **Curaçao** — `curacao` (68 776 B)
- [ ] 09. **Bahamas** — `bahamas` (67 530 B) — già madrelingua OK, da spuntare a verifica
- [ ] 10. **Turks e Caicos** — `turks-caicos` (67 082 B)
- [ ] 11. **Dominica** — `dominica` (62 109 B)
- [ ] 12. **Santa Lucia** — `santa-lucia` (58 726 B) — già madrelingua OK, da spuntare
- [ ] 13. **Martinica** — `martinica` (57 505 B) — già madrelingua OK (campione), da spuntare
- [ ] 14. **Porto Rico** — `porto-rico` (56 188 B)
- [ ] 15. **Isole Cayman** — `cayman` (50 286 B)
- [ ] 16. **Guadalupa** — `guadalupa` (40 506 B) — già madrelingua OK (campione), da spuntare
- [ ] 17. **Haiti** — `haiti` (39 411 B)
- [ ] 18. **Trinidad e Tobago** — `trinidad-tobago` (27 951 B)
- [ ] 19. **Venezuela** — `venezuela` (20 995 B)
- [ ] 20. **Costa Rica** — `costarica` (15 932 B)
- [ ] 21. **Belize** — `belize` (13 462 B)
- [ ] 22. **Colombia** — `colombia` (12 890 B)
- [ ] 23. **Nicaragua** — `nicaragua` (11 628 B)
- [ ] 24. **Honduras** — `honduras` (11 447 B)
- [ ] 25. **Isole Vergini** — `virgin-islands` (10 561 B)
- [ ] 26. **Antigua e Barbuda** — `antigua-barbuda` (9 991 B)
- [ ] 27. **Saint-Martin** — `saint-martin` (9 577 B)
- [ ] 28. **Saint-Barth** — `saint-barth` (8 502 B)
- [ ] 29. **Anguilla** — `anguilla` (8 401 B)
- [ ] 30. **St-Kitts e Nevis** — `st-kitts-nevis` (8 159 B)
- [ ] 31. **Montserrat** — `montserrat` (7 192 B)
- [ ] 32. **Saba** — `saba` (7 073 B)
- [ ] 33. **Sint Eustatius** — `st-eustatius` (6 838 B)
- [ ] 34. **Panama** — `panama` (3 470 B)
- [ ] 35. **Grenadine** — `grenadine` (1 759 B)

## Elenco alfabetico di riscontro (non è ordine di esecuzione)

> Solo indice. L'ordine di lavoro è la coda pesanti-first sopra.

- Anguilla · Antigua e Barbuda · Aruba · Bahamas · Barbados · Belize · Bonaire · Isole Cayman · Colombia · Costa Rica · Cuba · Curaçao · Dominica · Giamaica · Grenada · Grenadine · Guadalupa · Haiti · Honduras · Martinica · Montserrat · Nicaragua · Panama · Porto Rico · Repubblica Dominicana · Saba · Saint-Barth · Saint-Martin · Santa Lucia · Sint Eustatius · St-Kitts e Nevis · Trinidad e Tobago · Turks e Caicos · Venezuela · Isole Vergini

---
**Prossimo:** 03. Aruba — (86 987 B, 27 md IT: 11 pagine + 7 ancoraggi + 9 ristoranti) — EN in corso, poi FR/ES/DE/PT pesanti-first.
Nota: questo file è la fonte di verità; i completati restano `[x]` con data/commit, mai cancellati.
