# 00 — Ingresso, documenti e visti

**Ultima verifica: 27/08/2026** · Scheda **comune** a tutte le 6 zone greche: tutte le aree condividono lo stesso regime d'ingresso. Le pagine specifiche per zona → vedi menu.

## Status

| Voce | Dato | Fonte |
|---|---|---|
| Stato | **Grecia** — Repubblica ellenica, membro UE | Commissione UE — verificato 27/08/2026 ★★★★★ |
| Valuta | **Euro (EUR)** | Banca Centrale Europea ★★★★★ |
| Schengen | **Dentro l'area Schengen** | Commissione UE — Schengen ★★★★★ |
| Fuso | EET/EEST (UTC+2 / UTC+3 estate) | IANA TZ ★★★★★ |
| Lingua ufficiale | greco | **DATO MANCANTE** per dettaglio marittimo |

## Cittadini UE — nessun visto

| Voce | Regola | Fonte |
|---|---|---|
| Visto | **Non richiesto** per cittadini UE (libera circolazione) | Ministero Esteri ellenico mfa.gr / UE ★★★★★ |
| Documenti | Carta d'identità o passaporto validi | Hellenic Police — verificato 27/08/2026 ★★★★★ |
| Soggiorno | Nessun limite per cittadini UE | UE direttiva libera circolazione ★★★★★ |

> ⚠️ Le regole Schengen valgono normalmente: se si arriva da paesi extra-Schengen conta il tempo trascorso nell'area.

## Nota importante per chi arriva via mare

- Da porti **UE/Schengen**: nessuna formalità di frontiera persone; barca UE libera circolazione.
- Da porti **extra-UE/Schengen** (es. Turchia, Albania): obbligo di ingresso in **Port of Entry** con Port Police e Dogana — presentare equipaggio e documenti barca. **DATO MANCANTE** su elenco Port of Entry greci aggiornato — da verificare su hcg.gr / mfa.gr ★★★★★
- Tra le zone greche (Cicladi ↔ Ionie ↔ Dodecaneso ecc.): **nessuna formalità** — territorio nazionale unico.
- Dettagli procedura per diporto: **DATO MANCANTE** — da verificare su Hellenic Coast Guard / Port Authority ★★★★★

## La barca

| Barca | Regola | Fonte |
|---|---|---|
| **UE con IVA pagata** (caso tipico: barca italiana) | Libera circolazione, nessun limite di tempo, nessun cruising permit | Agenzia Dogane UE ★★★★★ |
| Extra-UE | Ammissione Temporanea standard UE: max **18 mesi**, rinnovabile uscendo dal territorio doganale | Codice Doganale UE art. 250-253 ★★★★★ |

> ### ⚠️ ALLERTA — Tassa acque greche TEPAI (ex-DEPKA) — obbligatoria per tutti
> **TEPAI** (*Τέλος Πλοίων Αναψυχής και Ημερόπλοιων*) si paga per **ogni barca >7,00 m fuori tutto** (7,00 esatta esente) indipendentemente da bandiera, anche un solo giorno nel mese = mese intero. Senza ricevuta la Port Police può **bloccare la barca** e multare. Pagamento **prima dell'ingresso** o immediatamente all'arrivo sull'app ufficiale. Fonte: [AADE eTEPAI](https://www.aade.gr/en/etepai) + FAQ 23/01/2026 Q16 ★★★★★ · [George Yachts 30/07/2026](https://georgeyachts.com/blog/tepai-tax-greece-2026-complete-yacht-charter-breakdown) ★★★

**Tariffe mensili 2026 (per mese di calendario, LOA da documento di nazionalità, 2 decimali):**

| LOA fuori tutto | Tariffa/mese | Esempio |
|---|---|---|
| >7,00 – 8,00 m | **€16** | 7,50 m → €16 |
| >8,00 – 10,00 m | **€25** | 9,58 m → €25 |
| >10,00 – 12,00 m | **€33** | 11,50 m → €33 |
| **>12,00 m** | **€8 × LOA** | 12,01 m → €96,08 · 15,25 m → €122,00 · 18 m → €144 · 24 m → €192 |

**Costo al mese — inserisci numero mesi.** Sconti:
- **-20% solo con pagamento in unica soluzione annuale anticipata** (12 mesi pagati insieme); se paghi mese per mese NON si applica lo sconto.
- -30% per disarmo/inattività documentata; esenzione per barche a terra/in sequestro/tradizionali — vedi FAQ AADE.

> ⚠️ **Allerta annualità:** la tariffa scontata **vale solo se paghi 12 mesi in unica soluzione** sul portale eTEPAI. Pagamenti rateali mensili = tariffa piena ogni mese.

**Dove pagare (unico sito ufficiale):** **[https://www1.aade.gr/aadeapps2/etepai/](https://www1.aade.gr/aadeapps2/etepai/)** → registra account → *New application* → paga con e-Paravolo → scarica ricevuta PDF (obbligatoria a bordo). Assistenza my1521 tel **1521** (gratis, 07:00–20:00) o my1521 digitale. [AADE](https://www.aade.gr/en/etepai) ★★★★★

<div id="tepai-calc" style="border:1px solid #4db6ac; border-radius:12px; padding:14px 16px; background:#0b131b; margin:14px 0;">
<b style="color:#4db6ac;">Calcolatore TEPAI 2026 — inserisci LOA fuori tutto e mesi</b><br>
<input id="tepai-loa" type="number" step="0.01" min="0" placeholder="es. 12.59" style="width:140px; padding:8px; margin:8px 8px 8px 0; border-radius:8px; border:1px solid #24384a; background:#16222e; color:#dbe7f1;">
<select id="tepai-mesi" style="padding:8px; border-radius:8px; border:1px solid #24384a; background:#16222e; color:#dbe7f1;"><option value="1">1 mese</option><option value="2">2 mesi</option><option value="3">3 mesi</option><option value="6">6 mesi</option><option value="12">12 mesi — pagamento unico (-20%)</option></select>
<button onclick="calcTepai()" style="padding:8px 14px; margin-left:8px; border-radius:8px; border:none; background:#4db6ac; color:#06231f; font-weight:700; cursor:pointer;">Calcola</button>
<div id="tepai-out" style="margin-top:10px; color:#dbe7f1; font-weight:600;"></div>
<div style="font-size:12px; color:#8aa2b5; margin-top:6px;">Tariffe AADE 23/01/2026 Q16 · >12m: LOA×€8/mese · 12 mesi unico = ×9,6 mesi (-20%) · Esente ≤7,00 m · Il costo è al mese: imposta i mesi per vedere il totale</div>
</div>
<script>
function calcTepai(){
  var loa=parseFloat(document.getElementById('tepai-loa').value.replace(',','.'));
  var mesi=parseInt(document.getElementById('tepai-mesi').value);
  var out=document.getElementById('tepai-out');
  if(isNaN(loa)){ out.innerHTML='Inserisci la lunghezza fuori tutto in metri (es. 12.59)'; return; }
  if(loa<=7.0){ out.innerHTML='✅ Esente: ≤7,00 m fuori tutto — TEPAI non dovuto'; return; }
  var mensile=0;
  if(loa>7 && loa<=8) mensile=16;
  else if(loa>8 && loa<=10) mensile=25;
  else if(loa>10 && loa<=12) mensile=33;
  else mensile=loa*8;
  var totale=mensile*mesi;
  var sconto=false;
  if(mesi==12){ totale=mensile*12*0.8; sconto=true; }
  var txt='LOA '+loa.toFixed(2)+' m → €'+mensile.toFixed(2)+' /mese × '+mesi+' mesi = <span style=color:#ffd54f>€'+totale.toFixed(2)+'</span>';
  if(sconto) txt+=' <span style=color:#ffb74d>⚠️ -20% solo con pagamento unico 12 mesi</span>';
  else if(mesi>1) txt+=' <span style=color:#8aa2b5>(senza sconto — paga mese per mese)</span>';
  txt+='<br><span style=font-size:12px;color:#8aa2b5>Pagamento su <a href=https://www1.aade.gr/aadeapps2/etepai/ target=_blank>eTEPAI AADE</a> — ricevuta a bordo obbligatoria</span>';
  out.innerHTML=txt;
}
</script>

## Vaccini

Nessuno obbligatorio per ingresso da paesi UE. **DATO MANCANTE** per eventuali requisiti sanitari specifici locali — da verificare su Ministero Salute greco / gov.gr ★★★★★

## Zone del portolano

| Zona | Carattere nautico | Ambito |
|---|---|---|
| **Cicladi** | Arcipelago centrale Egeo, Meltemi estivo forte, ancoraggi su sabbia/roccia | Mykonos, Paros, Naxos, Santorini, Milos |
| **Sporadi** | Egeo nord-occidentale, verde, più riparato | Skiathos, Skopelos, Alonissos, Skyros |
| **Ionie** | Mar Ionio ovest, venti moderati (Maestrale), più verde e meno Meltemi | Corfù, Lefkada, Cefalonia, Zante |
| **Dodecaneso** | Egeo sud-orientale, vicino Turchia, Meltemi | Rodi, Kos, Patmos, Symi, Karpathos |
| **Golfo Saronico** | Golfo di Atene, traffico intenso, base charter principale | Atene/Pireo, Egina, Poros, Hydra, Spetses |
| **Egeo Settentrionale** | Nord Egeo, meno affollato, Meltemi e bora | Thasos, Samothraki, Lemnos, Chios, Lesbos |

Ultimo aggiornamento: 27/08/2026
