# 00 — Entry, Documents & Visas

**Last checked: 27/08/2026** · Scheda **comune** a all le 6 zone greche: all le aree condividono lo same regime d'ingresso. Le pagine specifiche for zona → vedi menu.

## Status

| Item | Data | Source |
|---|---|---|
| Stato | **Grecia** — Repubblica ellenica, membro UE | Commissione UE — verificato 27/08/2026 ★★★★★ |
| Currency | **Euro (EUR)** | Banca Centrale Europea ★★★★★ |
| Schengen | **Dentro l'area Schengen** | Commissione UE — Schengen ★★★★★ |
| Time zone | EET/EEST (UTC+2 / UTC+3 estate) | IANA TZ ★★★★★ |
| Lingua ufficiale | greco | **DATA MISSING** for dettaglio marittimo |

## EU Citizens — No Visa

| Item | Rule | Source |
|---|---|---|
| Visa | **Not required** for cittadini UE (libera circolazione) | Ministero Esteri ellenico mfa.gr / UE ★★★★★ |
| Documents | Valid national ID card or passport | Hellenic Police — verificato 27/08/2026 ★★★★★ |
| Stay | Nessun limite for cittadini UE | UE direttiva libera circolazione ★★★★★ |

> ⚠️ Schengen rules apply as normal: if arriving from outside Schengen, time spent in the area counts.

## Important Note for Arrival by Sea

- From ports **UE/Schengen**: no formalità of frontiera persone; barca UE libera circolazione.
- From ports **extra-UE/Schengen** (es. Turchia, Albania): obbligo of ingresso in **Port of Entry** with Port Police and Dogana — presentare equipaggio and documenti barca. **DATA MISSING** on elenco Port of Entry greci aggiornato — from check on hcg.gr / mfa.gr ★★★★★
- Between le zone greche (Cicladi ↔ Ionie ↔ Dodecaneso ecc.): **no formalità** — single national territory.
- Details procedura for diporto: **DATA MISSING** — from check on Hellenic Coast Guard / Port Authority ★★★★★

## The Yacht

| Yacht | Rule | Source |
|---|---|---|
| **EU VAT-paid** (caso tipico: barca italiana) | Libera circolazione, no limit of tempo, no cruising permit | Agenzia Dogane UE ★★★★★ |
| Extra-UE | Standard EU Temporary Admission: max **18 months**, renewable by exiting the customs territory | Codice Doganale UE art. 250-253 ★★★★★ |

> ### ⚠️ ALLERTA — Fee acque greche TEPAI (ex-DEPKA) — obbligatoria for all
> **TEPAI** (*Τέλος Πλοίων Αναψυχής και Ημερόπλοιων*) si paga for **each barca >7,00 m fuori all** (7,00 esatta esente) indipendentemente from bandiera, also un only giorno nel mese = mese intero. Senza ricevuta la Port Police può **bloccare la barca** and multare. Pagamento **prima dell'ingresso** or immediatamente all'arrivo sull'app ufficiale. Source: [AADE eTEPAI](https://www.aade.gr/en/etepai) + FAQ 23/01/2026 Q16 ★★★★★ · [George Yachts 30/07/2026](https://georgeyachts.com/blog/tepai-tax-greece-2026-complete-yacht-charter-breakdown) ★★★

**Tariffs mensili 2026 (for mese of calendario, LOA from documento of nazionalità, 2 decimali):**

| LOA fuori all | Tariff/mese | Esempio |
|---|---|---|
| >7,00 – 8,00 m | **€16** | 7,50 m → €16 |
| >8,00 – 10,00 m | **€25** | 9,58 m → €25 |
| >10,00 – 12,00 m | **€33** | 11,50 m → €33 |
| **>12,00 m** | **€8 × LOA** | 12,01 m → €96,08 · 15,25 m → €122,00 · 18 m → €144 · 24 m → €192 |

**Cost at the mese — inserisci numero mesi.** Sconti:
- **-20% only with pagamento in unica soluzione annuale anticipata** (12 mesi pagati insieme); se paghi mese for mese NON si applica lo sconto.
- -30% for disarmo/inattività documentata; esenzione for barche a terra/in sequestro/tradizionali — vedi FAQ AADE.

> ⚠️ **Allerta annualità:** la tariffa scontata **vale only se paghi 12 mesi in unica soluzione** sul portale eTEPAI. Pagamenti rateali mensili = tariffa piena each mese.

**Dove pagare (unico sito ufficiale):** **[https://www1.aade.gr/aadeapps2/etepai/](https://www1.aade.gr/aadeapps2/etepai/)** → registra account → *New application* → paga with and-Paravolo → scarica ricevuta PDF (obbligatoria a bordo). Assistenza my1521 tel **1521** (gratis, 07:00–20:00) or my1521 digitale. [AADE](https://www.aade.gr/en/etepai) ★★★★★

<div id="tepai-calc" style="border:1px solid #4db6ac; border-radius:12px; padding:14px 16px; background:#0b131b; margin:14px 0;">
<b style="color:#4db6ac;">Calcolatore TEPAI 2026 — inserisci LOA fuori all (metri or piedi) and mesi</b><br>
<input id="tepai-loa" type="number" step="0.01" min="0" placeholder="metri: es. 12.59" style="width:135px; padding:8px; margin:8px 6px 8px 0; border-radius:8px; border:1px solid #24384a; background:#16222e; color:#dbe7f1;" oninput="syncTepai('m')">
<input id="tepai-loa-ft" type="number" step="0.01" min="0" placeholder="piedi: es. 41.3 ft" style="width:135px; padding:8px; margin:8px 6px 8px 0; border-radius:8px; border:1px solid #24384a; background:#16222e; color:#dbe7f1;" oninput="syncTepai('ft')">
<select id="tepai-mesi" style="padding:8px; border-radius:8px; border:1px solid #24384a; background:#16222e; color:#dbe7f1;"><option value="1">1 mese</option><option value="2">2 mesi</option><option value="3">3 mesi</option><option value="6">6 mesi</option><option value="12">12 mesi — pagamento unico (-20%)</option></select>
<button onclick="calcTepai()" style="padding:8px 14px; margin-left:8px; border-radius:8px; border:none; background:#4db6ac; color:#06231f; font-weight:700; cursor:pointer;">Calcola</button>
<div id="tepai-out" style="margin-top:10px; color:#dbe7f1; font-weight:600;"></div>
<div style="font-size:12px; color:#8aa2b5; margin-top:6px;">Tariffs AADE 23/01/2026 Q16 · >12m: LOA×€8/mese · 12 mesi unico = ×9,6 mesi (-20%) · Esente ≤7,00 m (22.97 ft) · Il costo è at the mese: imposta i mesi for vedere il totale · 1 m = 3.28084 ft</div>
</div>
<script>
function syncTepai(from){
  var m=document.getElementById('tepai-loa'), f=document.getElementById('tepai-loa-ft');
  if(from==='m'){
    var v=parseFloat(m.value.replace(',','.'));
    if(!isNaN(v)) f.value=(v*3.28084).toFixed(2);
    else f.value='';
  } else {
    var v=parseFloat(f.value.replace(',','.'));
    if(!isNaN(v)) m.value=(v/3.28084).toFixed(2);
    else m.value='';
  }
}
function calcTepai(){
  var loa=parseFloat(document.getElementById('tepai-loa').value.replace(',','.'));
  // se vuoto metri ma presente piedi, converti
  if(isNaN(loa)){
    var ft=parseFloat(document.getElementById('tepai-loa-ft').value.replace(',','.'));
    if(!isNaN(ft)) loa=ft/3.28084;
  }
  var mesi=parseInt(document.getElementById('tepai-mesi').value);
  var out=document.getElementById('tepai-out');
  if(isNaN(loa)){ out.innerHTML='Inserisci la lunghezza fuori all in metri or piedi (es. 12.59 m / 41.3 ft)'; return; }
  if(loa<=7.0){ out.innerHTML='✅ Esente: ≤7,00 m (22.97 ft) fuori all — TEPAI non dovuto'; return; }
  var mensile=0;
  if(loa>7 && loa<=8) mensile=16;
  else if(loa>8 && loa<=10) mensile=25;
  else if(loa>10 && loa<=12) mensile=33;
  else mensile=loa*8;
  var totale=mensile*mesi;
  var sconto=false;
  if(mesi==12){ totale=mensile*12*0.8; sconto=true; }
  var ft=(loa*3.28084).toFixed(2);
  var txt='LOA '+loa.toFixed(2)+' m ('+ft+' ft) → €'+mensile.toFixed(2)+' /mese × '+mesi+' mesi = <span style=color:#ffd54f>€'+totale.toFixed(2)+'</span>';
  if(sconto) txt+=' <span style=color:#ffb74d>⚠️ -20% only with pagamento unico 12 mesi</span>';
  else if(mesi>1) txt+=' <span style=color:#8aa2b5>(without sconto — paga mese for mese)</span>';
  txt+='<br><span style=font-size:12px;color:#8aa2b5>Pagamento on <a href=https://www1.aade.gr/aadeapps2/etepai/ target=_blank>eTEPAI AADE</a> — ricevuta a bordo obbligatoria</span>';
  out.innerHTML=txt;
}
</script>

## Vaccinations

None mandatory for ingresso from paesi UE. **DATA MISSING** for eventuali requisiti sanitari specifici locali — from check on Ministero Salute greco / gov.gr ★★★★★

## Pilot area

| Area | Carattere nautico | Ambito |
|---|---|---|
| **Cicladi** | Arcipelago centrale Egeo, Meltemi estivo forte, ancoraggi on sabbia/roccia | Mykonos, Paros, Naxos, Santorini, Milos |
| **Sporadi** | Egeo nord-occidentale, verde, more riparato | Skiathos, Skopelos, Alonissos, Skyros |
| **Ionie** | Mar Ionio ovest, venti moderati (Maestrale), more verde and less Meltemi | Corfù, Lefkada, Cefalonia, Zante |
| **Dodecaneso** | Egeo sud-orientale, vicino Turchia, Meltemi | Rodi, Kos, Patmos, Symi, Karpathos |
| **Golfo Saronico** | Golfo of Atene, traffico intenso, base charter principale | Atene/Pireo, Egina, Poros, Hydra, Spetses |
| **Egeo Settentrionale** | Nord Egeo, less affollato, Meltemi and bora | Thasos, Samothraki, Lemnos, Chios, Lesbos |

Last updated: 27/08/2026
