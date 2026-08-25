# 🤖 HANDOFF AGENTI — Portolano Nautico

> File interno di coordinamento tra agenti AI. NON pubblicare, NON copiare in `paesi/`.
> Ultimo aggiornamento: 22/08/2026

---

## 📌 COSA È QUESTO PROGETTO

Wiki nautica ("portolano") in italiano per velisti. Sorgenti Markdown in
`paesi/`, sito statico generato da `paesi/tools/build_paesi_html.py` →
`paesi/paesi.html` (desktop) + `paesi/paesi-mobile.html` (smartphone).

Pubblicato su GitHub Pages: https://ghitabbino.github.io/portolano/
(repo: Ghitabbino/portolano, branch main, root).

## ⚙️ COMANDI ESSENZIALI

```bash
cd paesi
python3 tools/build_paesi_html.py     # rigenera i 2 HTML (sempre dopo ogni modifica .md)
git add -A && git commit -m "..." && git push   # pubblica online
python3 tools/controllo_mensile.py [--paese XX]  # revisione mensile (DM + fonti)
python3 tools/verifica_critica.py     # coda paesi >15gg senza revisione critica
                                      # poi segui AGENTI_VERIFICA_CRITICA.md (max 5 paesi/sessione)
python3 tools/download_mappe.py       # tasselli mappa offline
```

## 📐 REGOLE INVIOLABILI

1. **Prima l'italiano completo-definitivo-senza-errori, poi le traduzioni.**
2. Struttura pagine = standard MARTINICA (titoli esatti: 01 Clearance doganale
   della barca · 02 Costo della vita · 03 Porti e marine · 04 Servizi, cantieri
   e manutenzione · 05 Stagionalità e meteo · 06 Sicurezza · 07 Provvisioning ·
   08 Portolano degli ancoraggi · 09 Artigiani e negozi nautici · 10 Ristoranti;
   schede ristorante = `# Nome` senza numero; schede ancoraggio = `# Nome {#anc-slug}`).
3. **VIETO dati inventati**: se non verificato → `**DATO MANCANTE**`.
3b. **VIETO copy-paste dalle fonti** (Noonsite, Waterway Guide, gov, ecc.): le informazioni
   si **riformulano sempre in italiano originale**; della fonte si riporta solo nome + link +
   rank. Citazioni testuali brevi ammesse solo se indispensabili e tra apici con fonte.
4. Citazioni: fonti governative col nome; le altre → solo stelle ★, oppure
   fonte tra parentesi quando disponibile (nuova direttiva utente).
5. Numeri emergenza per paese: Spagna/Antille FR **112** · Panama **911** ·
   Capo Verde **132/130/131**.
6. NO blocchi `<div class="mapframe">` dove non esistono tasselli in `paesi/mappe/<slug>/`.
7. Prima riga file: `# NN — Titolo`; ultima riga: data aggiornamento.
8. Menu laterale ad ALBERO (25/08/2026): 🌍 Aree → area (macro-zone solo Caraibi:
   Lucayano, Grandi Antille, Soprav. Settentr., Soprav. Merid., Sottovento,
   Occidentali, Canale/Costa, Coste A.C.) → isola → pagine in bianco.
   Griglia centrale specchio del menu (tessere icone/bandiere, testi verdi centrati).
   Gerarchia in VERDE accent (#4db6ac, stesso del logo) sia a sinistra che al centro;
   bianco solo per voci contenuto. Disclaimer home + coordinate indicative su ogni 08.
   Barra freccia indietro fissa in alto: mostra il LIVELLO CORRENTE (es. "← Mar dei
   Caraibi") e sale di un livello al click; solo 🌍 Aree/breadcrumb riporta agli oceani.
   Ispaniola divisa in Repubblica Dominicana e Haiti (24/08 dati ereditati, da verificare).
9. CARTINE & COORDINATE (nuova 25/08/2026, vale per TUTTI gli agenti):
   - Ogni cartina deve mostrare almeno DUE PUNTI REALI verificati
     (es. àncora dell'ancoraggio + un riferimento a terra: molo, faro, marina, pontile).
   - I marker degli ANCORAGGI stanno SOLO IN MARE, mai a terra: verifica
     sulla vista satellitare prima di inserire ogni coordinata.
   - Coordinate sempre datum WGS84, espresse in gradi-minuti-secondi
     (formato 14°28'32" N 61°02'15" W); il build genera il rendering DMS
     automaticamente dagli attributi decimale data-lat/data-lon del mapframe.
   - MAI coordinate inventate: se non verificate su fonte attendibile →
     `**DATO MANCANTE**` (vale anche per i pin delle cartine).
9b. SCALA CARTE ZOOMMABILI (nuova 25/08/2026): ogni ancoraggio segnalato DEVE
    avere una cartina interattiva zoomabile stile Google Maps (pan + zoom
    continuo fino al dettaglio della baia, MAI immagini fisse). Scala di
    RIFERIMENTO CERTIFICATA = BAHAMAS: mappa generale ancoraggi zoom **6–13** ·
    ristoranti **6–13** · sicurezza **6–12** · minimappa scheda ancoraggio
    **12–15** (default del build). Paesi-isola piccoli possono partire da 7,
    il massimo resta 13. Tasselli offline generati con
    `tools/download_mappe.py` per ogni livello usato (base/sat/sea); il
    build aggiunge da solo il fallback online Esri/CARTO/OpenSeaMap.
    NO mapframe senza tasselli locali (vedi regola 6).
    ⚠️ AUDIT OBBLIGATORIO: tutti i paesi già pubblicati vanno portati a
    questa scala e verificati uguali al livello Martinica (struttura 08 con
    tabella+schede+cartina, densità fonti, DM→0).

## ✅ COMPLETATO (non rifare)

- (25/08/2026) Navigazione ad albero Aree→gruppi→isole con menu centrale a tessere,
  breadcrumb, freccia indietro, ricerca piatta; icone univoche; Haiti + Rep. Dominicana
  separate da ispaniola
- Wiki base: Guadalupa, Martinica, Panama (Canale+San Blas) complete
- Canarie: 9 zone ×10 pagine + comune; Capo Verde: 9 zone ×10 pagine + comune
- Grenadine: struttura 7 zone ×10 voci + comune (contenuti da arricchire)
- Mappe offline tasselli (Esri/CARTO/OpenSeaMap) per tutte le zone principali
- Marker àncora gialla SVG nelle mappe ancoraggi; rossi per ristoranti/sicurezza
- Link marker→schede con matching scoped per paese (niente più link sbagliati)
- Telefoni verificati: marine Canarie, Shelter Bay (+507 433-3581/VHF74),
  agenti Canale (4, con recensioni e costi transito 3–5k US$), MRCC Cabo Verde
  (+238 232 5555), São Vicente Radio D4A, ENAPOR Mindelo, supermercati Canarie
- Ricerca interna raggruppata; badge verde paese sopra titoli; zoom panoramico
- Pulizia fonti non-governative (stelle senza nomi); numeri emergenza corretti
- `tools/controllo_mensile.py` creato e testato

## 🔜 CODA DI LAVORO (in ordine)

| # | Compito | Note |
|---|---|---|
| 0 | ⚠️ DOPO OGNI NUOVO PAESE: verificare che la card sia in 00-indice.md E nel build; poi push | ricorrente |
| 0b | ⚠️ A OGNI PUBLISH: `index.html` = copia di `paesi.html` (la radice del sito serve index!) | ricorrente dal 24/08 |

**Coda completamento CARAIBI (audit 24/08/2026, campione = Martinica):**

| # | Compito | Note |
|---|---|---|
| C1 | Nuove voci verificate: **Haiti** (separata da ispaniola), **Colombia** (San Andrés/Providencia/Cartagena), **Messico** (Isla Mujeres/Cozumel/Chinchorro), **Guatemala** (Rio Dulce) | fonti: Cruisers Wiki/Haiti, Noonsite/Colombia, CruisingWorld/YachtingWorld, sail-world Rio Dulce (~1000 yacht) |
| C2 | **Venezuela offshore** con alert sicurezza (Los Roques/Las Aves/Blanquilla); sotto-voce Klein Curaçao in curacao; Mona in porto-rico | ALERT Noonsite/Caribbean Compass set-2025: alto rischio |
| C3 | VUOTE da creare ex-novo (formato Martinica 10 pagine): **venezuela** (142 B!), belize, honduras, nicaragua, costarica | solo segnaposto ora |
| C4 | SCHELETRO da riempire: virgin-islands, antigua-barbuda, saint-martin, saint-barth, anguilla, st-kitts-nevis, saba, st-eustatius, montserrat | VI il traffico n°1 dei Caraibi; sub-cartelle VI già parziali |
| C5 | PARZIALI da arricchire: grenadine (7 sotto-isole scarse), santa-lucia, grenada, dominica, barbados, turks-caicos (03+08 vuoti), trinidad-tobago, aruba/bonaire/curacao (01-clearance stub ~300 B) | tabelle presenti ma piene di DATO MANCANTE |
| C6 | COMPLETE: colmare DATO MANCANTE residui — ispaniola(180!), porto-rico(74), bahamas(61), cuba(58), giamaica(45), cayman(37) | puntuale, non strutturale |

| # | Compito | Note |
|---|---|---|
| C7 | ⚠️ MARKER ANCORAGGI MANCANTI (audit tools/audit_coordinate.txt): ~40 schede anc-* senza pin
    sulla mappa satellitare (Anguilla, Antigua, Grenadine zone, Saba, St-Barth, St-Martin,
    Statia, St-Kitts/Nevis, VI, Montserrat) + label marker↔schede da allineare (Cuba, Giamaica,
    Canarie, RD, PR, Cayman). Serve ricerca coordinate verificate — MAI inventate | ricorrente |
| 2 | Completare dati CV sal/boa-vista/sao-nicolau | stesse fonti: Navily blog, Ocean Posse,
    velmundi, yachtmollymawk, blog naviganti multilingua |
| 3 | Revisione generale finale + audit (`audit_uniformita --fix`, deep_audit) | 0 deviazioni |
| 4 | Multilingua: infrastruttura en/fr/es/de + selettore lingue home | ~45 min |
| 5 | Traduzioni: EN piena qualità (4–6h batch); FR/ES/DE DeepL-assistite 1–2h/lng | dopo ok utente |
| 6 | Donazioni: Ko-fi o Liberapay — fondo menu laterale + card discreta home (~25 min) | serve username utente |

## 🔍 FONTI PER LA RICERCA DATI (usate e affidabili)

Navily blog · Ocean Posse · velmundi.com · yachtmollymawk · sailingyachtamalia (blog IT)
· Noonsite · sarcontacts.info · puertosdetenerife.org · puertoscanarios.es · muchaplaya.com
· Páginas Amarillas (ES/PA) · siti ufficiali marine · forum cruisers multilingua.

## ⚠️ TRAPPole GIÀ INCORSE (non ripetere)

- Regex su `data-markers='...'`: i nomi possono contenere apostrofi → usare splice
  a indice o sanitizzare con ’ (U+2019). Guard già nel build (link_markers return).
- `re.sub(..., count=1)` su frame duplicati lascia spazzatura: purgare TUTTI i div
  con regex DOTALL prima di reinserire.
- Overpass: header `Content-Type: application/x-www-form-urlencoded` obbligatorio;
  bbox in ordine (s,w,n,e); query regionali grandi → 504: usare cluster piccoli.
- Emoji: ⚓ è U+2693 (non U+2692).
- Auditor segna come problemi anche cose VOLUTE (schede `# Nome`, punti panoramici
  senza schede): non "correggerle" ciecamente.


---

# 📐 STANDARD WIKI (rimosso dalla home pubblica)

Scala stelle: ★★★★★ fonte ufficiale governativa · ★★★★ enti/listini ufficiali · ★★★ portali curati/stampa · ★★ forum/naviganti · ★ voce di banchina.

## Controllo mensile

| # | Area | Azione |
|---|---|---|
| 1 | Contatti | Verificare telefoni/mail/orari/sedi su sito ufficiale + Pages Jaunes; aggiornare o lasciare vuoto |
| 2 | Notizie | Variazioni regolamentazioni (divieti, clearance, tariffe), nuovi servizi/cantieri, meteo/sicurezza |
| 3 | Conflitti | Riconsolidare blocchi ⚠️ CONFLITTO aperti; chiudere quelli risolti |
| 4 | Mappe | Tasselli completi (`download_mappe.py`); ricostruire `paesi.html` dopo ogni modifica |
| 5 | Sicurezza | Media locali, rete sicurezza diportisti, fonti diportiste aggregate, advisory: furti/rapine a crocieristi; aggiornare 06 |
| 6 | DATO MANCANTE | Cercare ogni occorrenza in TUTTO il portolano e tentare il recupero con fonti mirate |

## Fonti archiviate

| File | Contenuto |
|---|---|
| `fonti/guide_boat.txt` | Guide Boat Clearance 2024 (martinique.gouv.fr) |
| `fonti/points_clearance.txt` | Lista punti agréé clearance Antille francesi v15/12/2025 (martinique.gouv.fr) |

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


---

# SISTEMA FONTI (pagina rimossa dal sito)

# Sistema di classificazione delle fonti

Ogni informazione nel portolano porta **fonte + punteggio + data di verifica**. In caso di conflitto prevale la fonte con punteggio più alto e più recente.

## Scala di affidabilità

| Punteggio | Tipo | Esempi |
|---|---|---|
| ★★★★★ | **Fonte ufficiale governativa aggiornata** | martinique.gouv.fr, douane.gouv.fr, service-public.gouv.fr, dm.martinique.developpement-durable.gouv.fr, arrêté préfectoral |
| ★★★★ | **Enti pubblici operativi, listini ufficiali, advisory governative straniere** | Marina du Marin (listino PDF ufficiale), Direction de la Mer, voyage.gc.ca |
| ★★★ | **Portali curati, stampa locale, associazioni di naviganti strutturate** | Fonti diportiste aggregate, Stampa locale antillana, TV locale Martinica, Radio locale Martinica, Rete sicurezza diportisti Caraibi, Associazioni di naviganti (resoconti verificati) |
| ★★ | **Forum di naviganti e gruppi Facebook** | Forum di naviganti, gruppi di naviganti, segnalazioni dei naviganti |
| ★ | **Voce di banchina** | Non verificata → da confermare prima dell'uso |

## Regole

1. **Verifica incrociata**: le notizie da forum/FB (★★) vengono usate solo se confermate da fonte ≥★★★ o se marcate esplicitamente come "da verificare".
2. **Data obbligatoria**: ogni voce riporta quando è stata controllata. Le procedure doganali cambiano spesso: fonti >12 mesi su clearance/tasse vengono ricontrollate prima di ogni crociera.
3. **Sicurezza**: si consultano sempre anche i giornali locali (, TV locale Martinica, RCI), le advisory governative (fr.diplomatie.gouv.fr, voyage.gc.ca, gov.uk), la rete e i forum dei naviganti, con storico di almeno 5 anni per valutare le tendenze. Ogni paese riceve una **valutazione sicurezza 0–5** (0 = terribile → 5 = molto sicuro) in testa alla pagina sicurezza, rivista a ogni controllo mensile.
4. **Aggiornamento continuo**: due canali —
 - **Fonti indicate dall'utente**: PDF, link, post FB, messaggi di gruppo → vengono estratti, classificati con punteggio e integrati nelle pagine;
 - **Ricerca autonoma sul web** ("aggiorna [paese]"): riesecuzione della ricerca con verifica delle date delle fonti esistenti.
5. **Visti/documenti**: anche quando non sono richiesti (es. cittadini UE), vengono comunque ricontrollati a ogni aggiornamento su fonte ufficiale.

## Gestione dei conflitti tra fonti

Quando due o più fonti sono in contrasto sulla stessa informazione, la pagina riporta un blocco:

> ### ⚠️ CONFLITTO — [argomento]
> | Versione | Fonte | Rank | Data |
> |---|---|---|---|
> | A: … | … | ★★★★★ | … |
> | B: … | … | ★★ | … |
>
> **Valutazione**: prevale la versione A perché… / nessuna prevalenza: servono verifiche (cosa fare).

Criteri di prevalenza: rank più alto → fonte più recente → fonte specializzata sul tema (es. listino ufficiale > resoconto). Le versioni perdenti restano visibili nel blocco, non vengono cancellate.

Ultimo aggiornamento: 22/08/2026

## Regola URL (nuova 23/08/2026)
- Dove possibile, per risorse che hanno un loro sito, inserire l'URL nel file .md (link markdown sul nome).
- Es: `[Marina du Marin](https://www.marina-martinique.fr)`, non testo nudo.
