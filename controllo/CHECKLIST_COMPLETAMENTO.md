# ✅ CHECKLIST COMPLETAMENTO PORTOLANO — LEGGIMI PRIMA DI LAVORARE

> File di coordinamento permanente: vale per QUALSIASI agente, sessione o piattaforma.
> Spunta `[x]` con data quando una voce è completa e pubblicata su GitHub.
> Regole di lavoro: `AGENTI_HANDOFF.md` · Verifiche critiche: `AGENTI_VERIFICA_CRITICA.md`
> Standard pagina: Martinica · Coordinate: WGS84 decimale · Mai copy-paste dalle fonti.

---

## 🔴 CARAIBI — da terminare

### Vuoti → completamento integrale (C3)
- [x] venezuela — completato 25/08/2026
- [x] belize — completato 25/08/2026 (pubblicato)
- [x] honduras — completato 25/08/2026 (pubblicato)
- [x] nicaragua — completato 25/08/2026 (pubblicato)
- [ ] costarica — 11 pagine

### Scheletri → riempimento (C4)
- [ ] virgin-islands
- [ ] antigua-barbuda
- [ ] saint-martin
- [ ] saint-barth
- [ ] anguilla
- [ ] st-kitts-nevis
- [ ] saba
- [ ] st-eustatius
- [ ] montserrat

### Parziali → colmare DATO MANCANTE (C5)
- [ ] santa-lucia
- [ ] grenada
- [ ] dominica
- [ ] barbados
- [ ] turks-caicos (03+08 vuoti)
- [ ] aruba (01 clearance stub)
- [ ] bonaire (01 stub)
- [ ] curacao (01 stub)
- [ ] trinidad-tobago (00 fatto 25/08 · resto da verificare)
- [ ] grenadine — 7 zone: bequia · mustique · canouan · mayreau · st-vincent · tobago-cays · union-island

### Nuove voci previste (C1)
- [x] haiti — separata da ispaniola 25/08 (dati ereditati, DATO MANCANTI da colmare)
- [ ] colombia (San Andrés, Providencia, Cartagena)
- [ ] messico (Cozumel, Isla Mujeres, Chinchorro)
- [ ] guatemala (Rio Dulce)

---

## 🔵 ATLANTICO — da terminare

- [ ] azzorre — creare le pagine mancanti (00+10 creati 25/08) + collegare 9 schede ristoranti
- [ ] madeira — creare le pagine mancanti (presenti 00, 01, 02)
- [ ] cabo-verde — spazzata DATO MANCANTE sulle 9 isole
- [ ] canarie — spazzata DATO MANCANTE sulle 7 isole
- [x] trinidad-tobago 00 ingresso — compilato 25/08/2026

### 🆕 Nuove isole atlantiche
- [ ] sant-elena — struttura completa
- [ ] tristan-da-cunha — struttura completa

---

## 🌍 ROADMAP FASCIA TROPICALE (espansione futura)

Paesi e isole tropicali affacciati sul mare, oltre a quelli già sopra:

| Regione | Unità previste |
|---|---|
| Sud America tropicale | Guyana · Suriname · Guyana Francese · Brasile (costa N-NE) |
| Africa occidentale atlantica | Senegal · Gambia · Guinea-Bissau · Guinea · Sierra Leone · Liberia · Costa d'Avorio · Ghana · Togo · Benin · Nigeria · Cameroon · Guinea Equatoriale · São Tomé e Príncipe · Gabon |
| Mar Rosso / Corno d'Africa | Egitto (Mar Rosso) · Sudan · Eritrea · Gibuti |
| Africa orientale / Indiano occ. | Kenya · Tanzania-Zanzibar · Mozambico · Madagascar · Comore · Mayotte · Seychelles · Mauritius · Réunion |
| Indiano settentrionale | Maldive · Sri Lanka |
| Sud-est asiatico | Thailandia · Malesia · Singapore · Indonesia · Filippine · Vietnam · Cambogia · Brunei · Timor Est |
| Oceania / Pacifico tropicale | PNG · Salomone · Vanuatu · Fiji · Nuova Caledonia · Samoa · Tonga · Polinesia Francese · Cook · Kiribati · Tuvalu · Micronesia/Palau/Marshall · Guam-Mariane |

---

## 📊 STIMA DIMENSIONI PORTALE A REGIME (tutta la fascia tropicale)

| Scenario | Unità | Testo/HTML | Tile mappe | TOTALE |
|---|---|---|---|---|
| Solo attuale (37+ paesi) | 40 | ~5 MB | ~150-185 MB | **~160-190 MB** |
| Caraibi completi + Atlantico + nuove isole | ~45 | ~6 MB | ~180-210 MB | **~190-215 MB** |
| **Fascia tropicale COMPLETA** | **~100-115** | **~8-10 MB** | **~550-900 MB** | **≈ 0,6-0,95 GB** |

⚠️ Con l'espansione totale si sfiora il limite soft di GitHub Pages (1 GB):
strategia necessaria = **hosting tile per regione/oceano** (repo o storage separato)
e/o riduzione zoom massimo delle tile (da 13 a 11 ≈ −50-60% di peso).
Il testo della wiki resta comunque sotto i 10 MB: è la cartografia a pesare.

---

## ⚙️ COMANDI RICORRENTI

```bash
python3 tools/build_paesi_html.py && cp paesi.html index.html   # rigenera sempre
python3 tools/verifica_critica.py                               # coda revisioni >15 gg
python3 tools/controlla_link.py --paese XX                      # link rotti
git add -A && git commit -m "..." && git push origin main       # pubblica
```
