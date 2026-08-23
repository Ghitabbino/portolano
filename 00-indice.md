# 00 — Ingresso, documenti e visti

Wiki di navigazione per paese: ingresso, clearance, costi, porti, servizi, stagionalità, sicurezza.

**Metodo**: ogni informazione porta fonte + rank di attendibilità + data → [sistema-fonti.md](sistema-fonti.md).

## Paesi

<div class="paesi-grid">
 <div class="pcard">
 <div class="pflag">🇨🇻</div>
 <a class="pname" href="cabo-verde/00-ingresso-visti.md">Capo Verde</a>
 <div class="pdesc">Arcipelago atlantico: hub Mindelo, saline di Maio, vulcano Fogo; pre-registrazione EASE.</div>
 <div class="pstat">🚧 v0 — 22/08/2026</div>
 </div>
 <div class="pcard">
 <div class="pflag">🇪🇸</div>
 <a class="pname" href="canarie/00-ingresso-visti.md">Canarie</a>
 <div class="pdesc">RUP spagnola nell'Atlantico: hub ARC a Las Palmas, alisei costanti tutto l'anno, trampolino per la traversata.</div>
 <div class="pstat">🚧 v0 — 22/08/2026</div>
 </div>
 <div class="pcard">
 <div class="pflag">🇬🇵</div>
 <a class="pname" href="guadalupa/00-ingresso-visti.md">Guadalupa</a>
 <div class="pdesc">Gli ancoraggi più belli delle Antille (Saintes, Petite Terre, Cousteau); provvisioning top a Jarry.</div>
 <div class="pstat">✅ v1 — 21/08/2026</div>
 </div>
 <div class="pcard">
 <div class="pflag">🇲🇶</div>
 <a class="pname" href="martinica/00-ingresso-visti.md">Martinica</a>
 <div class="pdesc">Base servizi n°1 dei Caraibi orientali; hub Le Marin; formalità zero per UE.</div>
 <div class="pstat">✅ v1 — 21/08/2026</div>
 </div>
 <div class="pcard">
 <div class="pflag">🇵🇦</div>
 <a class="pname" href="panama/00-ingresso-visti.md">Panama</a>
 <div class="pdesc">Scheda comune + due zone: Canale (transito, Colón, Perlas) e San Blas (comarca Guna Yala).</div>
 <div class="pstat">🚧 v0 — 21/08/2026</div>
 </div>
</div>

## Formato standard per paese

| # | Pagina | Contiene |
|---|---|---|
| 1 | `ingresso-visti` | Status · Cittadini UE · Arrivo via mare · Dopo i 3 mesi · La barca · Vaccini |
| 2 | `clearance` | Chi deve farla · Procedura online · Cartacea timbrata · Costi · Punti agréé · Dogana regionale · Esperienze · Sanzioni · Da verificare |
| 3 | `costi` | Alimentari · Mangiare fuori · Carburanti · Trasporti · Servizi quotidiani · Contanti · Approfondimenti |
| 4 | `porti-ancoraggi` | Zone per costa · Tariffe ormeggi e marine (voci fisse) · Distanze utili |
| 5 | `servizi-cantieri` | Hub tecnico · Altri cantieri · Gas e bombole · Acqua dolce · Note strategiche |
| 6 | `stagionalita-meteo` | Clima · Stagioni · Uragani · Consignes cicloniche · Venti locali · Finestre tipiche · Link meteo |
| 7 | `sicurezza` | Valutazione X/5 · Quadro generale · Mappa zone · Posti sicuri / da evitare · Furti a crocieristi · A bordo e a terra · Navigazione · Salvataggio · Monitoraggio mensile |
| 8 | `provvisioning` | Livello prezzi · Supermercati per zona · Mercati · Acqua e carburante · Consigli pratici |
| 9 | `ancoraggi` | Regole generali + ⛔ riserve/divieti · Tabella riassuntiva + mappa · Schede `{#anc-*}` con minimappa · Cartografia ufficiale · Non inclusi · Checklist àncora |
| 10 | `artigiani-nautici` | Tabella artigiani (+ colonna Recensioni) · Altri operatori · Dove si trova cosa · Negozi e shipchandler · Note pratiche |
| 11 | `ristoranti` | Legenda €/€€/€€€ e simboli cucina · Mappa unica con marker cliccabili · Griglia generale · App e fonti · Una scheda per ristorante |

Regole trasversali:

| Regola | Dettaglio |
|---|---|
| Fonti | Ogni informazione con fonte + rank; conflitti in blocco ⚠️ CONFLITTO |
| Mappe | Sempre offline: tasselli in `paesi/mappe/<slug>/`, Leaflet in `paesi/assets/` |
| Link | Interni con nome file; schede ancoraggio con anchor `#anc-*`; ristoranti = pagina separata ciascuno |
| Sicurezza | Ogni paese apre la 06 con valutazione **0–5**, posti sicuri/da evitare, mappa zone a rischio |

## Controllo mensile

| # | Area | Azione |
|---|---|---|
| 1 | Contatti | Verificare telefoni/mail/orari/sedi su sito ufficiale + Pages Jaunes; aggiornare o lasciare vuoto |
| 2 | Notizie | Variazioni regolamentazioni (divieti, clearance, tariffe), nuovi servizi/cantieri, meteo/sicurezza |
| 3 | Conflitti | Riconsolidare blocchi ⚠️ CONFLITTO aperti; chiudere quelli risolti |
| 4 | Mappe | Tasselli completi (`download_mappe.py`); ricostruire `paesi.html` dopo ogni modifica |
| 5 | Sicurezza | Media locali, rete sicurezza diportisti, fonti diportiste aggregate, advisory: furti/rapine a crocieristi; aggiornare 06 |
| 6 | DATO MANCANTE | Cercare ogni occorrenza in TUTTO il portolano e tentare il recupero con fonti mirate |

Ultimo controllo completo: **21/08/2026** (creazione v1 Martinica).

## Fonti archiviate

| File | Contenuto |
|---|---|
| `fonti/guide_boat.txt` | Guide Boat Clearance 2024 (martinique.gouv.fr) |
| `fonti/points_clearance.txt` | Lista punti agréé clearance Antille francesi v15/12/2025 (martinique.gouv.fr) |
