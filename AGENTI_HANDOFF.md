# 🤖 HANDOFF AGENTI — Portolano Nautico

> File interno di coordinamento tra agenti AI. NON pubblicare, NON copiare in `paesi/`.
> Ultimo aggiornamento: 27/08/2026 — cristallizzato pubblicato 8fa7b4f

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
2b. STANDARD MARTINICA — TUTTO COME MARTINICA (nuova 27/08/2026, chiarimento finale utente 27/08/2026, vale per TUTTI gli agenti):
    • **Impostazione, layout, struttura, font — TUTTO identico a MARTINICA**: 11 file 00-10 con titoli esatti + struttura interna come in `paesi/martinica/*.md` (vedi "Formato standard per paese" a fondo file); 08 con sezioni fisse `Regole generali` → `Tabella riassuntiva` → `Mappa generale` (`data-markers` 4 campi) → `Schede {#anc-*}` con minimappa 12-15 → `Cartografia ufficiale` → `Checklist`; 10 con `Legenda` → `Mappa unica` → `Griglia` → `Schede rist-*` con minimappa; stessi font/dimensioni/badge/marker/colori del build (`paesi/tools/build_paesi_html.py`). Nessuna deroga di layout.
    • **Quantità di informazioni = MARTINICA come riferimento, ma proporzionata alla realtà dell'isola** (regola di buon senso utente): Martinica ha la **quantità che voglio** (~703 righe 00-10 + 10 ancoraggi + 32 ristoranti, 1 fonte ogni 2–3 righe). Ogni altra isola deve tendere a **stessa completezza e densità per le categorie pertinenti**. Esempio: se è uno scoglio disabitato, NON pretendo stessi cantieri di Martinica → `04-servizi-cantieri` resta breve ma **verificato** con `**DATO MANCANTE**` motivato + fonte; invece `05-stagionalità/meteo`, `06-sicurezza`, `08-ancoraggi` devono avere **stessa ricchezza di Martinica** perché pertinenti ovunque. Vietato lasciare vuoti per pigrizia.
    • **Misura**: `00=49 · 01=71 · 02=68 · 03=93 · 04=43 · 05=49 · 06=93 · 07=51 · 08=86 · 09=56 · 10=44` → audit `tools/audit_uniformita.py` deve tendere a **0 deviazioni**; `tools/deep_audit.py` **0 DATO MANCANTE evitabile**. Guadalupa è il secondo campione identico a Martinica.
    • **Blocco minimo pubblicabile**: 00-10 non vuoti, 08 con tabella+cartina verificata (≥2 punti reali), 06 con valutazione 0-5 + emergenze corrette (112/911 ecc.), almeno 1 scheda anc-* con coordinate WGS84 verificate. Sotto questa soglia il paese resta `⚠️ BLOCCATO` in coda.
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
8. Menu laterale ad ALBERO (25/08/2026, aggiornato 27/08/2026 Mediterraneo + bacini 27/08/2026): 🌍 Aree → area → bacino → paese → (eventuale sotto-zona) → pagine 00-10.
    • **Caraibi** (macro-zone: Lucayano, Grandi Antille, Soprav. Settentr., Soprav. Merid., Sottovento, Occidentali, Canale/Costa, Coste A.C.) → isola → 00-10.
    • **Mediterraneo** (quattro bacini obbligatori 27/08/2026):
      - **Bacino Occidentale:** Spagna, Francia, Monaco (+ Gibilterra se aggiunta)
      - **Bacino Centrale:** Italia (suddivisa in *Mar Ligure, Tirreno Settentrionale, Tirreno Centrale, Tirreno Meridionale, Ionio, Adriatico*), Slovenia, Croazia, Bosnia-Erzegovina, Montenegro, Albania, Malta
      - **Bacino Orientale:** Grecia (suddivisa in *Cicladi, Sporadi, Ionie, Dodecaneso, Golfo Saronico, Egeo Settentrionale*), Turchia, Cipro, Siria, Libano, Israele
      - **Nord Africa:** Marocco, Algeria, Tunisia, Libia, Egitto
      Ogni paese poi → 00-10 (e per Italia/Grecia → sotto-zone → 00-10).
    Griglia centrale specchio del menu (tessere icone/bandiere, testi verdi centrati).
    Gerarchia in VERDE accent (#4db6ac, stesso del logo) sia a sinistra che al centro;
    bianco solo per voci contenuto. Disclaimer home + coordinate indicative su ogni 08.
    Barra freccia indietro fissa in alto: mostra il LIVELLO CORRENTE (es. "← Mar dei
    Caraibi" o "← Mediterraneo → Italia → Tirreno Centrale") e sale di un livello al click; solo 🌍 Aree/breadcrumb riporta agli oceani.
    Ispaniola divisa in Repubblica Dominicana e Haiti (24/08 dati ereditati, da verificare).
9. CARTINE & COORDINATE (nuova 25/08/2026, aggiornata 27/08/2026 "sempre in mezzo al mare", vale per TUTTI gli agenti):
    - Ogni cartina deve mostrare almeno DUE PUNTI REALI verificati
      (es. àncora dell'ancoraggio + un riferimento a terra: molo, faro, marina, pontile).
    - I marker degli ANCORAGGI stanno **SEMPRE IN MEZZO AL MARE** (come da esempio https://pdt-attachments-explains-instructional.trycloudflare.com/paesi.html valido per tutti): verifica sulla vista satellitare che il pin sia **in acqua ben al centro della rada/baia, mai a terra e mai a miglia dalla costa** (entro l'area di ancoraggio reale, tipicamente 100–400 m dalla riva a seconda della baia, profondità 3–10 m). Controllo uno-per-uno prioritario.
    - Coordinate sempre datum WGS84, espresse in gradi-minuti-secondi
      (formato 14°28'32" N 61°02'15" W); il build genera il rendering DMS
      automaticamente dagli attributi decimale data-lat/data-lon del mapframe.
    - MAI coordinate inventate: se non verificate su fonte attendibile →
      `**DATO MANCANTE**` (vale anche per i pin delle cartine).
9b. SCALA CARTE ZOOMMABILI (aggiornata 28/08/2026 su richiesta "aumenta zoom"): ogni ancoraggio/ristorante DEVE avere cartina zoomabile stile Google Maps fino al dettaglio. Scala CERTIFICATA aggiornata = BAHAMAS: mappa generale ancoraggi zoom **6–16** · ristoranti **6–16** · sicurezza **6–15** · minimappa scheda ancoraggio/ristorante **12–17** (default build). Paesi piccoli possono partire da 7, il massimo ora **17** (prima 13/15). Tasselli offline generati con `tools/download_mappe.py` per ogni livello usato (base/sat/sea); il build aggiunge fallback online Esri/CARTO/OpenSeaMap. NO mapframe senza tasselli locali (regola 6).
    ⚠️ AUDIT OBBLIGATORIO: tutti i paesi già pubblicati vanno portati a
    questa scala e verificati uguali al livello Martinica (struttura 08 con
    tabella+schede+cartina, densità fonti, DM→0).
9c. CARTE E TASSELLI — REGOLA GENERALE (25/08/2026, decisione finale utente):
    • ARCHITETTURA = MARTINICA/GUADALUPA per TUTTE le isole, nessuna esclusione:
      mappa generale del paese nel 08 con àncore CLICCABILI (marker a 4 campi
      [lat, lon, "nome", "anc-slug"]) che aprono la scheda anc-* di dettaglio;
      ogni scheda porta la minimappa zoomabile 12–15 del singolo ancoraggio.
      Vietato lasciare un paese con sola mappa generale.
    • TASSELLI: le overview offline coprono il paese fino a zoom ~8; da zoom 9
      in su i tasselli esistono SOLO in patch attorno agli ancoraggi/marker
      (span 1–2), MAI a quadrato sull'interno (caso Santiago de Cuba: lo zoom
      deve funzionare su TUTTA la costa, l'interno non serve).
    • TOOL: `tools/download_mappe.py` estrae automaticamente i marker dai .md
      e scarica sia le patch costiere sia i tasselli dettaglio delle schede.
10. BADGE PAESE = TASTO INDIETRO (nuova 25/08/2026): in OGNI pagina il nome
    del paese sopra il titolo (loc-badge, es. "← Bahamas") è GRANDE (26px,
    21px mobile) e CLICCABILE → torna indietro di un livello. Generale per
    tutti i paesi e pagine future; non rimuovere né rimpicciolire il badge.
11. NOTE PER AGENTI MAI SULLA WIKI (nuova 25/08/2026): le istruzioni di
    lavoro (monitoraggio mensile con fonti thecssn.org/stampa/voyage.gc.ca/
    gov.uk/travel.state.gov/gruppi FB, checklist agente, promemoria build)
    stanno SOLO qui nell'handoff — VIETATO pubblicarle nelle pagine .md del
    sito o lasciarle visibili agli umani. Il monitoraggio mensile di ogni
    paese resta compito degli agenti a ogni controllo periodico.
12. CONTINUITÀ E AUTONOMIA AGENTI — REGOLA GENERALE (nuova 27/08/2026, decisione finale utente, vale per TUTTI gli agenti):
    • **Mai fermarsi**: l'agente NON si ferma mai spontaneamente. Va avanti nello svolgere i compiti assegnati (coda C1-C7, verifica critica, audit, tasselli, build) fino a esaurimento o fino a comando esplicito di STOP. Comandi di stop = `stop` · `fermo` · `fermati` · `pausa` · `annulla` · `abort` o qualsiasi sinonimo con questo senso.
    • **Blocco per autorizzazione/domanda senza risposta**: se manca un'autorizzazione (push, cancellazione, costo, API) o non arriva risposta a una domanda posta all'utente, l'agente NON attende in idle → **salta il compito bloccato, passa al successivo in coda** e continua. Il compito saltato resta in `CODA DI LAVORO` con annotazione `⚠️ BLOCCATO — manca autorizzazione X`.
    • **Informazione prioritaria al rientro**: appena interrogato dall'utente (qualsiasi messaggio), l'agente con **massima priorità** informa subito: lista compiti non portati a termine, motivo del blocco, autorizzazioni mancanti, cosa serve per sbloccare. Solo dopo riprende il lavoro.
    • **PC in standby / chiusura sessione**: l'agente deve rendere il lavoro **resistente allo standby**: ogni avanzamento va committato localmente (`git commit`), i download lunghi vanno in `nohup`/`screen`, i build lasciano artefatti su disco (`paesi.html`, `paesi-mobile.html`, `BACKUP-*`, tag `cristallizzato-*`). Al risveglio l'agente riprende automaticamente dal punto lasciato, senza chiedere.
    • Vietato interpretare il silenzio come stop.
13. REPORT PERIODICO OBBLIGATORIO — REGOLA GENERALE (nuova 27/08/2026, decisione finale utente, vale per TUTTI gli agenti):
    • **Ogni step completato** (singolo file, singola isola, singolo batch verifica) → **report immediato all'utente** con: cosa fatto, file/commit, gap Martinica residuo, prossimo step.
    • **Ogni 30 minuti** di lavoro continuato senza step concluso → **report di avanzamento** anche se parziale: dove sono, % completamento, eventuali blocchi/autorizzazioni mancanti.
    • Formato: breve, a punti, con `file:linea` e commit hash. Vietato lavorare in silenzio oltre 30 min.
14. RICERCA RISTORANTI — ESTENSIONE AI SITI LOCALI (nuova 27/08/2026, decisione finale utente, vale per TUTTI gli agenti):
    • Oltre a TripAdvisor/Google/TheFork, **estendere sempre la ricerca recensioni ai siti locali del paese** (es. guide locali, blog food locali, giornali, portali turismo ufficiali, associazioni ristoratori, Facebook/Instagram locali).
    • Per ogni ristorante riportare: nome, cucina, fascia €, recensioni locali (fonte + data + rank ★), link al sito locale se esiste.
     • Vietato inventare recensioni — se non trovate su siti locali → `**DATO MANCANTE**` per recensioni, ma il ristorante resta con scheda base + mappa.

15. BANDIERE — REGOLA GENERALE (nuova 28/08/2026, vale per TUTTI gli agenti):
     • Se un luogo è **trattato come a sé stante** nel portolano (cartella `paesi/<slug>/` propria), usa **sempre la bandiera del luogo**, MAI quella dello Stato sovrano.
     • Esempi: **Canarie → 🇮🇨** (non 🇪🇸), **Azzorre → 🇵🇹** autonoma (non PT continentale), **Madeira → 🇵🇹** autonoma, **Guadalupa 🇬🇵 / Martinica 🇲🇶 / Saint-Barth 🇧🇱 / Saint-Martin 🇲🇫** (non 🇫🇷), **Aruba 🇦🇼 / Curaçao 🇨🇼 / Bonaire 🇧🇶 / Saba 🇳🇱 / Sint Eustatius 🇳🇱** (non 🇳🇱 generico ove esiste codice specifico), **Cayman 🇰🇾 / Turks e Caicos 🇹🇨 / Anguilla 🇦🇮 / Montserrat 🇲🇸 / Vergini 🇻🇮** (non 🇬🇧/🇺🇸), **Porto Rico 🇵🇷** (non 🇺🇸).
     • Mappa bandiere in `paesi/tools/build_paesi_html.py:120` (`BANDIERE`): aggiornala quando aggiungi un nuovo `slug` autonomo. Se il territorio ha codice ISO/emoji dedicato (es. 🇮🇨 per Canarie), usalo; se non esiste emoji dedicata (es. Azzorre/Madeira), usa l'emoji dello Stato con nota “autonoma” e icona distinta se disponibile.
     • Cerca e sostituisci: a ogni nuovo paese/arcipelago autonomo, verifica che `TREE.flag` e le tessere non mostrino la bandiera della madrepatria.

16. DOWNLOAD ZIP/GPX — REGOLA ASSOLUTA (28/08/2026, per SEMPRE, per TUTTI gli agenti):
     • **Avviso in prima pagina wiki** (`paesi/00-indice.md:1` = “Aree”): sempre presente un avviso breve che i dati di ogni paese sono scaricabili offline (ZIP + GPX WGS84). Non toglierlo mai.
     • **Tasto ZIP accanto al nome paese nella barra laterale**: per OGNI paese/arcipelago autonomo (`paesi/<slug>/`) la voce nella sidebar sinistra mostra **accanto al nome un tasto/ icona ⬇️ ZIP** che punta a `zip/<slug>.zip` (e `gpx/<slug>.gpx` per i waypoint). Regola vale per tutti i paesi esistenti e futuri, senza eccezioni.
     • **Aggiornamento automatico**: ad **ogni modifica di un paese** (qualsiasi `.md` in `paesi/<slug>/`) il build rigenera **automaticamente** lo ZIP del paese (`tools/export_zip.py`) e il GPX (`tools/export_gpx.py`) — mai lasciare uno ZIP datato. Verificato in `tools/build_paesi_html.py:920` (hook post-build).
     • Verifica: dopo ogni build controllare che `paesi/zip/<slug>.zip` e `paesi/gpx/<slug>.gpx` esistano e che `paesi.html` contenga il bottone ZIP in sidebar + in `08-ancoraggi` e prima pagina `00-ingresso` di ogni paese.

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
