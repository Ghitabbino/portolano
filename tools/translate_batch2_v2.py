#!/usr/bin/env python3
import os, re, pathlib

ROOT = pathlib.Path(__file__).parent.parent
IT_ROOT = ROOT / "paesi" / "it"
EN_ROOT = ROOT / "paesi" / "en"

TITLE_MAP = {
    "00-ingresso-visti.md": "# 00 — Entry, Documents & Visas",
    "01-clearance.md": "# 01 — Yacht Customs Clearance",
    "02-costi.md": "# 02 — Cost of Living",
    "03-porti-ancoraggi.md": "# 03 — Ports & Marinas",
    "04-servizi-cantieri.md": "# 04 — Services, Boatyards & Maintenance",
    "05-stagionalita-meteo.md": "# 05 — Seasonality & Weather",
    "06-sicurezza.md": "# 06 — Safety & Security",
    "07-provvisioning.md": "# 07 — Provisioning",
    "08-ancoraggi.md": "# 08 — Anchorage Pilot",
    "09-artigiani-nautici.md": "# 09 — Marine Trades & Chandlers",
    "10-ristoranti.md": "# 10 — Restaurants",
}

# Extended phrase replacements - Italian -> English nautical
REPLACEMENTS = [
    ("# 00 — Ingresso, documenti e visti", "# 00 — Entry, Documents & Visas"),
    ("# 01 — Clearance doganale della barca", "# 01 — Yacht Customs Clearance"),
    ("# 02 — Costo della vita", "# 02 — Cost of Living"),
    ("# 03 — Porti e marine", "# 03 — Ports & Marinas"),
    ("# 03 — Porti e ancoraggi", "# 03 — Ports & Marinas"),
    ("# 04 — Servizi, cantieri e manutenzione", "# 04 — Services, Boatyards & Maintenance"),
    ("# 05 — Stagionalità e meteo", "# 05 — Seasonality & Weather"),
    ("# 06 — Sicurezza", "# 06 — Safety & Security"),
    ("# 07 — Provvisioning", "# 07 — Provisioning"),
    ("# 08 — Portolano degli ancoraggi", "# 08 — Anchorage Pilot"),
    ("# 09 — Artigiani e negozi nautici", "# 09 — Marine Trades & Chandlers"),
    ("# 09 — Artigiani nautici", "# 09 — Marine Trades & Chandlers"),
    ("# 10 — Ristoranti", "# 10 — Restaurants"),

    ("Ultimo aggiornamento", "Last updated"),
    ("Ultima verifica", "Last checked"),
    ("Fonti principali", "Main sources"),
    ("Prossimo controllo mensile", "Next monthly check"),
    ("DATO MANCANTE", "DATA MISSING"),
    ("DENTRO l'area Schengen (Spagna): nessun controllo alle frontiere interne", "INSIDE the Schengen Area (Spain): no checks at internal borders"),
    ("DENTRO l'area Schengen", "INSIDE the Schengen Area"),
    ("Fuori dall'area IVA UE: vige l'IGIC", "Outside the EU VAT area: IGIC applies"),
    ("Fuori dall'area IVA UE", "Outside the EU VAT area"),
    ("Comunità autonoma della Spagna, Regione Ultraperiferica (RUP) dell'UE", "Autonomous Community of Spain, Outermost Region (OR) of the EU"),
    ("Comunità autonoma della Spagna", "Autonomous Community of Spain"),
    ("Regione Ultraperiferica (RUP) dell'UE", "Outermost Region (OR) of the EU"),
    ("Territorio Britannico d'Oltremare (UK Overseas Territory)", "British Overseas Territory (UK Overseas Territory)"),
    ("Territorio Britannico d'Oltremare", "British Overseas Territory"),
    ("Non fanno parte del Regno Unito né dell'UE; regime d'ingresso autonomo regolato dal", "They are not part of the United Kingdom or the EU; entry is governed by the"),
    ("Non fanno parte del Regno Unito", "They are not part of the United Kingdom"),
    ("Valuta locale **dollaro delle Cayman (CI$)**, ancorato a", "Local currency **Cayman Islands dollar (CI$)**, pegged at"),
    ("Valuta: **euro (EUR)**", "Currency: **euro (EUR)**"),
    ("Valuta: **dinaro algerino (DZD)**", "Currency: **Algerian dinar (DZD)**"),
    ("Livello prezzi:", "Price level:"),
    ("Cittadini UE — nessun visto", "EU Citizens — No Visa"),
    ("Cittadini UE — nessun visto (principio generale)", "EU Citizens — No Visa (General Principle)"),
    ("Cittadini italiani — nessun visto", "Italian Citizens — No Visa"),
    ("Cittadini italiani/UE", "Italian/EU Citizens"),
    ("Se il visto serve (altre nazionalità)", "If You Need a Visa (Other Nationalities)"),
    ("Se il visto serve", "If You Need a Visa"),
    ("Nota importante per chi arriva via mare", "Important Note for Arrival by Sea"),
    ("E dopo i 3 mesi? (cittadini italiani/UE)", "Beyond 3 Months? (Italian/EU Citizens)"),
    ("La barca: permanenza", "The Yacht: Length of Stay"),
    ("La barca: soglia dei 30 giorni", "The Yacht: 30-Day Threshold"),
    ("La barca: importazione temporanea", "The Yacht: Temporary Importation"),
    ("La barca", "The Yacht"),
    ("Vaccini e sanità", "Vaccines & Health"),
    ("Vaccini", "Vaccinations"),
    ("Vaccinazioni", "Vaccinations"),
    ("Nessun vaccino obbligatorio", "No mandatory vaccinations"),
    ("Nessun vaccino obbligatorio per l'ingresso alle Cayman per chi proviene dall'Italia/Europa", "No mandatory vaccinations for entry to the Cayman Islands from Italy/Europe"),
    ("Raccomandate le vaccinazioni di routine; nessuna richiesta di certificato febbre gialla se non in transito da area endemica", "Routine vaccinations are recommended; no yellow fever certificate required unless transiting an endemic area"),
    ("Da verificare prima della partenza", "To Verify Before Departure"),
    ("Da verificare prima della crociera", "To Verify Before Your Cruise"),
    ("Chi deve farla", "Who Must Clear"),
    ("Procedura d'ingresso", "Entry Procedure"),
    ("Procedura", "Procedure"),
    ("Copia cartacea e timbro", "Paper Copy & Stamp"),
    ("Punti agréé / porti d'ingresso", "Authorised Ports / Ports of Entry"),
    ("Punti agréé", "Authorised Ports"),
    ("Porti di ingresso (Port of Entry)", "Ports of Entry (Port of Entry)"),
    ("Porti di ingresso", "Ports of Entry"),
    ("Dogana regionale", "Regional Customs"),
    ("Esperienze di naviganti", "Cruisers' Experiences"),
    ("Sanzioni", "Penalties"),
    ("Contatti utili", "Useful Contacts"),
    ("Orari e costi", "Hours & Fees"),
    ("Orari", "Hours"),
    ("Costi", "Fees"),
    ("Orario sportello doganale", "Customs office hours"),
    ("Clearance in orario", "Clearance during office hours"),
    ("Fuori orario / domenica", "Out-of-hours / Sunday"),
    ("Partenza (outward clearance)", "Departure (Outward Clearance)"),
    ("Partenza", "Departure"),
    ("Valutazione sicurezza", "Safety Rating"),
    ("Quadro generale", "General Overview"),
    ("Mappa delle zone — offline", "Zone Map — Offline"),
    ("Mappa delle zone", "Zone Map"),
    ("Zone sicure (consigliate)", "Safe Areas (Recommended)"),
    ("Zone sicure", "Safe Areas"),
    ("Attenzioni", "Areas Requiring Caution"),
    ("Numeri di emergenza", "Emergency Numbers"),
    ("A bordo e in navigazione", "Aboard & Under Way"),
    ("A bordo", "Aboard"),
    ("Emergenza unica", "Single Emergency Number"),
    ("Soccorso in mare", "Maritime Rescue"),
    ("Salvataggio ed emergenze", "Rescue & Emergencies"),
    ("Clima", "Climate"),
    ("Stagioni", "Seasons"),
    ("Stagione", "Season"),
    ("Uragani / cicloni", "Hurricanes / Cyclones"),
    ("Uragani", "Hurricanes"),
    ("Consignes / avvisi", "Warnings / Notices"),
    ("Venti locali", "Local Winds"),
    ("Finestre tipiche", "Typical Weather Windows"),
    ("Finestre tipiche di navigazione", "Typical Sailing Windows"),
    ("Link meteo", "Weather Links"),
    ("Link meteo utili", "Useful Weather Links"),
    ("Alimentari e spesa di bordo", "Groceries & Galley Provisioning"),
    ("Alimentari", "Groceries"),
    ("Mangiare fuori", "Eating Out"),
    ("Carburanti", "Fuel"),
    ("Trasporti e collegamenti", "Transport & Connections"),
    ("Trasporti", "Transport"),
    ("Servizi quotidiani e utenze", "Everyday Services & Utilities"),
    ("Servizi quotidiani", "Everyday Services"),
    ("Contanti e pagamenti", "Cash & Payments"),
    ("Approfondimenti", "Further Reading"),
    ("Tariffe ormeggi e marine", "Berthing & Marina Tariffs"),
    ("Tariffe indicative", "Indicative Tariffs"),
    ("Tariffe", "Tariffs"),
    ("Contatti marine verificati", "Verified Marina Contacts"),
    ("Distanze utili", "Useful Distances"),
    ("Tratta", "Passage"),
    ("Distanza", "Distance"),
    ("Struttura", "Facility"),
    ("Costo/note", "Cost/Notes"),
    ("Posto pontile — notte (~12 m)", "Alongside berth — per night (~12 m)"),
    ("Posto pontile — notte (multiscafo ~12 m)", "Alongside berth — per night (multihull ~12 m)"),
    ("Boa / mouillage — notte (~12 m)", "Mooring buoy — per night (~12 m)"),
    ("Mese pontile (~12 m)", "Monthly berth (~12 m)"),
    ("Elettricità", "Electricity"),
    ("Acqua", "Water"),
    ("Ancoraggio", "Anchorage"),
    ("Altre strutture", "Other Facilities"),
    ("Altri porti", "Other Ports"),
    ("Altri cantieri", "Other Boatyards"),
    ("Las Palmas de Gran Canaria — l'hub atlantico", "Las Palmas de Gran Canaria — The Atlantic Hub"),
    ("Las Palmas de Gran Canaria — l'hub atlantico".lower(), "Las Palmas de Gran Canaria — The Atlantic Hub"),
    ("Regole generali di ancoraggio (prima di tutto)", "General Anchorage Rules (First and Foremost)"),
    ("Regole generali", "General Rules"),
    ("Zone di divieto assoluto (ufficiali)", "Strictly Prohibited Areas (Official)"),
    ("Zone di divieto assoluto", "Strictly Prohibited Areas"),
    ("Tabella riassuntiva — i migliori ancoraggi", "Summary Table — Best Anchorages"),
    ("Tabella riassuntiva", "Summary Table"),
    ("Mappa generale degli ancoraggi", "General Anchorage Chart"),
    ("Mappa generale", "General Chart"),
    ("Cartografia ufficiale", "Official Charts"),
    ("Non inclusi (per ora)", "Not Included (For Now)"),
    ("Checklist àncora", "Anchor Checklist"),
    ("Checklist", "Checklist"),
    ("Legenda", "Legend"),
    ("Mappa unica", "Single Chart"),
    ("Griglia", "Grid"),
    ("Valutazioni", "Ratings"),
    ("Specialità", "Speciality"),
    ("Cucina", "Cuisine"),
    ("Location", "Setting"),
    ("Contatti", "Contacts"),
    ("Zona", "Area"),
    ("Campo", "Field"),
    ("Dettaglio", "Detail"),
    ("Profondità", "Depth"),
    ("Tenuta àncora", "Holding"),
    ("Tenuta", "Holding"),
    ("Venti/riparo", "Winds/Shelter"),
    ("Riparo venti prevalenti", "Shelter from Prevailing Winds"),
    ("Pericoli", "Hazards"),
    ("Boe/divieti/normative", "Buoys/Restrictions/Regulations"),
    ("A terra", "Ashore"),
    ("Affollamento", "Crowding"),
    ("Giudizio comunità", "Community Rating"),
    ("Fonte", "Source"),
    ("Voce", "Item"),
    ("Regola", "Rule"),
    ("Situazione", "Situation"),
    ("Barca", "Yacht"),

    # Specific sentences / fragments observed
    ("Scheda **comune** a tutto l'arcipelago: tutte le isole condividono lo stesso regime d'ingresso. Le pagine specifiche per isola → vedi zone nel menu.", "Sheet **common** to the entire archipelago: all islands share the same entry regime. For island-specific pages → see zones in the menu."),
    ("Fuori dall'area IVA UE: vige l'IGIC (~7% vs IVA 21%) — carburante e molti beni più economici", "Outside the EU VAT area: IGIC applies (~7% vs 21% VAT) — fuel and many goods are cheaper"),
    ("DENTRO l'area Schengen (Spagna): nessun controllo alle frontiere interne", "INSIDE the Schengen Area (Spain): no checks at internal borders"),
    ("UTC+0 inverno / UTC+1 estate (**1 ora indietro** rispetto alla Spagna continentale)", "UTC+0 winter / UTC+1 summer (**1 hour behind** mainland Spain)"),
    ("spagnolo; inglese diffuso nelle marine turistiche", "Spanish; English widely spoken in tourist marinas"),
    ("Non richiesto (libera circolazione UE)", "Not required (EU freedom of movement)"),
    ("Carta d'identità o passaporto validi", "Valid national ID card or passport"),
    ("Nessun limite per cittadini UE; le Canarie NON consumano giorni extra: si è in Spagna/UE", "No limit for EU citizens; the Canaries do not consume extra days: you are in Spain/EU"),
    ("Le regole Schengen valgono normalmente: se si arriva da paesi extra-Schengen conta il tempo trascorso nell'area.", "Schengen rules apply as normal: if arriving from outside Schengen, time spent in the area counts."),
    ("Da porti **UE/Schengen** (Italia, Spagna continentale, Antille francesi NO — sono extra-UE doganale): nessuna formalità di ingresso persone.", "From **EU/Schengen** ports (Italy, mainland Spain, French Antilles NO — they are outside the EU customs area): no entry formalities for people."),
    ("Da porti **extra-UE** (Marocco, Capo Verde, Caraibi): obbligo di presentarsi al primo **porto di ingresso** ufficiale (Santa Cruz de Tenerife o Las Palmas de Gran Canaria) per controlli polizia/dogana.", "From **non-EU** ports (Morocco, Cape Verde, Caribbean): you must present yourself at the first official **port of entry** (Santa Cruz de Tenerife or Las Palmas de Gran Canaria) for police/customs checks."),
    ("Tra le isole e verso il continente: **nessuna formalità** (territorio nazionale unico).", "Between islands and to the mainland: **no formalities** (single national territory)."),
    ("Sono **due** i punti dove è autorizzato il primo approdo internazionale:", "There are **two** authorised first ports of entry:"),
    ("Non è consentito toccare altre baie o isole (inclusa Little Cayman) prima di aver completato la clearance in uno dei due porti sopra.", "You must not touch any other bays or islands (including Little Cayman) before completing clearance at one of the two ports above."),
    ("Avviso entro le 12 miglia: chiamare **Port Security su VHF 16** (presidio H24) annunciando arrivo, nome barca, bandiera, provenienza e ETA. Risponde la Port Authority che istruisce sul punto di attesa.", "Notice within 12 miles: call **Port Security on VHF 16** (manned H24) announcing arrival, yacht name, flag, port of origin and ETA. Port Authority will advise on the waiting position."),
    ("Bandiera Q: issare la gialla e **non sbarcare nessuno** fino a completamento delle formalità. Divieto assoluto di sbarco pre-clearance.", "Q flag: hoist the yellow flag and **no one to go ashore** until formalities are complete. Landing before clearance is strictly prohibited."),
    ("Ispezione congiunta a bordo: salgono **Customs (con unità cinofila), Port Authority e Immigration**. Controllo documenti nave ed equipaggio, dichiarazione doganale, ispezione cambusa e gavoni.", "Joint inspection on board: **Customs (with sniffer dog unit), Port Authority and Immigration** come aboard. Checks of ship's and crew papers, customs declaration, galley and locker inspection."),
    ("Armi: **consegna obbligatoria** di armi da fuoco, **spear guns e Hawaiian slings**; vengono custodite dalle autorità e restituite alla partenza. Dichiarare tutto, anche fiocine e fucili subacquei elastici.", "Weapons: **compulsory surrender** of firearms, **spear guns and Hawaiian slings**; they are held by the authorities and returned on departure. Declare everything, including spear-guns and elastic powered spearguns."),
    ("Documenti da tenere pronti: passaporti, registro nave, lista equipaggio, clearance dell'ultimo porto, assicurazione.", "Documents to have ready: passports, vessel registration, crew list, clearance from last port, insurance."),
    ("Lun–Ven 08:30–16:00 — Sab 08:30–12:30 — Dom chiuso", "Mon–Fri 08:30–16:00 — Sat 08:30–12:30 — Sun closed"),
    ("Gratuita (diritti portuali minimi inclusi)", "Free (minimum harbour dues included)"),
    ("USD 75 per *Special Attendance* — applicato ad esempio alla Barcadere Marina", "USD 75 for *Special Attendance* — charged for example at Barcadere Marina"),
    ("Nessun cruising permit separato; la clearance vale per la permanenza fino alla soglia d'importazione (30 gg)", "No separate cruising permit; clearance covers the stay up to the import threshold (30 days)"),
    ("Richiedere lo **scontrino duty-free per il carburante** al momento della clearance d'uscita: circa **CI$ 0,85/gal di sconto sul diesel e CI$ 0,75/gal sulla benzina**. Il rifornimento va effettuato subito dopo il rilascio, prima di lasciare le acque.", "Request the **duty-free fuel chit** at outward clearance: about **CI$ 0.85/gal off diesel and CI$ 0.75/gal off petrol** (gasoline). Fuel up immediately after issue, before leaving territorial waters."),
    ("Restituzione delle armi custodite.", "Return of weapons held in custody."),
    ("Avviso VHF 16 a Port Security.", "Notify Port Security on VHF 16."),
    ("Mancata esposizione bandiera Q / sbarco prima della clearance", "Failure to fly Q flag / landing before clearance"),
    ("Ancoraggio su corallo o danneggiamento barriera", "Anchoring on coral or damaging the reef"),
    ("Fino a **CI$ 500.000 + 1 anno di reclusione**", "Up to **CI$ 500,000 + 1 year imprisonment**"),
    ("Armi non dichiarate", "Undeclared weapons"),
    ("Sequestro + procedimento penale", "Seizure + criminal proceedings"),
    ("L'ancoraggio su corallo è perseguito penalmente: usare solo sabbia o boe pubbliche → dettagli in", "Anchoring on coral is a criminal offence: use only sand or public moorings → see"),
    ("Porto principale, dogana e immigrazione H24 su chiamata", "Main harbour, customs and immigration H24 on call"),
    ("Alternativa per chi arriva da nord-est", "Alternative for arrivals from the north-east"),
    ("Fino a **6 mesi** alla prima ammissione; proroga richiedibile all'Ufficio Immigrazione", "Up to **6 months** on first admission; extension may be requested at the Immigration Office"),
    ("Ammissione fino a **30 giorni** max se in possesso di visto multiplo valido per USA, Canada o Regno Unito (categoria agevolata)", "Admission for up to **30 days** max if holding a valid multiple-entry visa for the USA, Canada or the UK (facilitated category)"),
    ("Richiesta in loco prima della scadenza; concessa a discrezione dell'ufficiale", "Apply locally before expiry; granted at the officer's discretion"),
    ("Nodo critico per i diportisti: oltre **30 giorni consecutivi** di permanenza nelle acque Cayman, l'imbarcazione può essere considerata **importata** con applicazione di **dazio del 12% sul valore** dello scafo. Segnalazione ricorrente della comunità NoForeignLand; confermare con Customs prima di superare la soglia.", "Critical point for cruisers: beyond **30 consecutive days** in Cayman waters, the vessel may be deemed **imported** with **12% duty on hull value**. Repeatedly reported by the NoForeignLand community; confirm with Customs before exceeding the threshold."),
    ("Per soste brevi (<30 gg) nessun dazio d'importazione; solo clearance in entrata/uscita → vedi", "For short stays (<30 days) no import duty; only entry/exit clearance → see"),
    ("Oltre i 30 gg: valutare uscita temporanea dalle acque territoriali o regolarizzazione doganale.", "Beyond 30 days: consider a temporary exit from territorial waters or customs regularisation."),
    ("Carburante duty-free all'uscita: al momento della partenza definitiva (*outward clearance*) è possibile rifornirsi senza dazi con **sconto di circa CI$ 0,85/gal sul diesel e CI$ 0,75/gal sulla benzina** rispetto al prezzo alla pompa; richiedere esplicitamente lo sgravio alla dogana.", "Duty-free fuel on departure: at final departure (*outward clearance*) you can bunker duty-free with **a discount of about CI$ 0.85/gal on diesel and CI$ 0.75/gal on petrol** versus pump price; request the relief explicitly from Customs."),
    ("Dichiarare tutto, anche fiocine e fucili subacquei elastici.", "Declare everything, including spear-guns and elastic spearguns."),
    ("La Francia è uno **Stato membro dell'Unione europea** e parte dell'**area Schengen**. Valuta: **euro (EUR)**.", "France is an **EU Member State** and part of the **Schengen Area**. Currency: **euro (EUR)**."),
    ("Controlli persone e **clearance della barca** sono procedure separate → vedi", "Personal checks and **yacht clearance** are separate procedures → see"),
    ("DATO MANCANTE su procedure specifiche di ingresso via mare per diportisti in Francia.", "DATA MISSING on specific entry procedures by sea for cruisers in France."),
    ("Oceanico subtropicale, mite tutto l'anno: aria 18–28 °C, mare 19–24 °C. Mai cicloni significativi (fuori dalla fascia uragani).", "Subtropical oceanic, mild year-round: air 18–28 °C, sea 19–24 °C. No significant cyclones (outside the hurricane belt)."),
    ("Alta stagione velica: alisei NE 15–25 kn, affollamento Las Palmas (ARC nov, preparativi traversate)", "Peak sailing season: NE trade winds 15–25 kn, crowded Las Palmas (ARC in Nov, Atlantic crossing preparations)"),
    ("Alisei stabili, meno traffico; ottimo per girare l'arcipelago", "Steady trade winds, less traffic; excellent for cruising the archipelago"),
    ("Vento più sostenuto a sud; Calima più probabile", "Stronger wind in the south; Calima more likely"),
    ("Vento da est/sahariano con polvere: visibilità ridotta, temperature su, calo improvviso del barometro no. Dura tipicamente 1–3 giorni. Seguirla su", "Easterly/Saharan wind with dust: reduced visibility, higher temperatures, no sharp barometric drop. Typically lasts 1–3 days. Track it on"),
    ("Aliseo NE dominante: costa nord/est esposta, sud sottovento.", "Prevailing NE trade wind: north/east coast exposed, south in the lee."),
    ("Accelerazioni a ridosso dei rilievi e nelle gole costiere.", "Acceleration zones off high ground and in coastal gorges."),
    ("Brise di valle pomeridiane lungo la costa sud.", "Afternoon valley breezes along the south coast."),
    ("Traversata atlantica (→ Caraibi): finestra storica **novembre–dicembre** da Las Palmas.", "Atlantic crossing (→ Caribbean): historic window **November–December** from Las Palmas."),
    ("Il punto di ritrovo dei velisti verso i Caraibi; ARC ogni novembre; servizi tecnici completi, carenaggio, chandler; inverno pieno — prenotare con anticipo per ott–dic", "Rendezvous for yachts bound for the Caribbean; ARC every November; full technical services, boatyard, chandlery; full in winter — book well ahead for Oct–Dec"),
    ("Costa steep-to e baie sud battute dall'aliseo: ancoraggi rari e mediocri. Le marine sono la scelta normale.", "Steep-to coast and southern bays battered by the trade wind: anchorages are few and mediocre. Marinas are the normal choice."),
    ("Di fronte a Mogán con calma è possibile fermarsi diurno ⚠️ verificare sul posto.", "Off Mogán in calm conditions a daytime stop is possible ⚠️ check locally."),
    ("Rotte dei ferry intorno all'isola: attraversamenti frequenti su Las Palmas–Agaete e sud.", "Ferry routes around the island: frequent crossings on Las Palmas–Agaete and the south."),
    ("Cartina di dettaglio — zoom ± fino alla baia · mappa offline · coordinate WGS84 indicative, verificare sempre col plotter", "Detail chart — zoom in to the bay · offline chart · approximate WGS84 coordinates, always verify with your chartplotter"),
    ("Rada", "Roadstead"),
    ("Baia", "Bay"),
    ("Faro", "Lighthouse"),
    ("Molo", "Pier"),
    ("Pontile", "Pontoon"),
]

LINK_TEXT_MAP = {
    "00 — Ingresso, documenti e visti": "00 — Entry, Documents & Visas",
    "01 — Clearance doganale della barca": "01 — Yacht Customs Clearance",
    "01 — Clearance": "01 — Yacht Customs Clearance",
    "02 — Costo della vita": "02 — Cost of Living",
    "03 — Porti e marine": "03 — Ports & Marinas",
    "03 — Porti e ancoraggi": "03 — Ports & Marinas",
    "04 — Servizi, cantieri e manutenzione": "04 — Services, Boatyards & Maintenance",
    "05 — Stagionalità e meteo": "05 — Seasonality & Weather",
    "06 — Sicurezza": "06 — Safety & Security",
    "07 — Provvisioning": "07 — Provisioning",
    "08 — Portolano degli ancoraggi": "08 — Anchorage Pilot",
    "08 — Ancoraggi": "08 — Anchorage Pilot",
    "09 — Artigiani e negozi nautici": "09 — Marine Trades & Chandlers",
    "09 — Artigiani nautici": "09 — Marine Trades & Chandlers",
    "10 — Ristoranti": "10 — Restaurants",
    "Tutti gli ancoraggi": "All anchorages",
    "Tutti i ristoranti": "All restaurants",
    "00 Indice": "00 Index",
}

def protect_segments(text):
    # Protect URLs, html divs, coordinates like 19°17'N, data-markers
    placeholders = {}
    counter = 0
    # Protect markdown links URLs
    def url_repl(m):
        nonlocal counter
        key = f"__URL{counter}__"
        placeholders[key] = m.group(0)
        counter += 1
        return key
    # Protect data-markers and divs
    text = re.sub(r'data-markers=\'[^\']*\'', lambda m: (lambda k: placeholders.setdefault(k, m.group(0)) or k)(f"__PH{counter}__") or f"__PH{counter-1}__", text)
    # Actually simpler: use generic protection for __PH
    # We'll do step wise
    return text, placeholders

def translate_content(orig_text, filepath):
    # Title handling
    lines = orig_text.split("\n")
    if lines and lines[0].startswith("# "):
        fname = os.path.basename(filepath)
        if fname in TITLE_MAP:
            lines[0] = TITLE_MAP[fname]
        orig_text = "\n".join(lines)

    # Extract and protect link URLs, html tags, coordinates
    # We will use placeholders for:
    # 1. markdown link URLs: ](url)
    # 2. html tags <...>
    # 3. coordinates pattern 19°...
    # 4. data-markers etc already inside html
    placeholders = {}
    ph_counter = 0
    def make_ph(val):
        nonlocal ph_counter
        key = f"__PH{ph_counter}__"
        ph_counter += 1
        placeholders[key] = val
        return key

    # Protect markdown link URLs: keep [text](url) but protect url part
    # We'll temporarily replace the whole link with placeholder for text translation then restore url
    # Approach: find all links, translate text separately, then reassemble without translating url
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    link_store = {}
    def link_trans(m):
        inner = m.group(1)
        url = m.group(2)
        # translate inner
        for it,en in LINK_TEXT_MAP.items():
            if it in inner:
                inner = inner.replace(it, en)
        # also apply phrase replacements to inner (later global will also apply, but do now)
        # we will handle inner translation via global later: store and return placeholder
        key = make_ph(f"__LINKURL__{url}__")
        # store tuple
        link_store[key] = (inner, url)
        return f"[{inner}]({key})"  # placeholder url
    orig_text = link_pattern.sub(link_trans, orig_text)

    # Protect HTML divs
    orig_text = re.sub(r'<div[^>]*>', lambda m: make_ph(m.group(0)), orig_text)
    orig_text = re.sub(r'</div>', lambda m: make_ph(m.group(0)), orig_text)
    # Protect coordinates with degrees
    orig_text = re.sub(r'\d+°\d+[′\']?[\d″"]*\s*[NSEW]', lambda m: make_ph(m.group(0)), orig_text)
    # Protect data- attributes already inside div but keep simple
    orig_text = re.sub(r'data-[a-z]+="[^"]*"', lambda m: make_ph(m.group(0)), orig_text)
    orig_text = re.sub(r"data-[a-z]+='[^']*'", lambda m: make_ph(m.group(0)), orig_text)
    # Protect URLs http
    orig_text = re.sub(r'https?://[^\s\)\]]+', lambda m: make_ph(m.group(0)), orig_text)
    # Protect anchor like {#anc-...}
    orig_text = re.sub(r'\{#anc-[^}]+\}', lambda m: make_ph(m.group(0)), orig_text)
    # Protect rank stars
    orig_text = re.sub(r'★+', lambda m: make_ph(m.group(0)), orig_text)

    # Now apply phrase replacements sorted by length
    sorted_repls = sorted(REPLACEMENTS, key=lambda x: len(x[0]), reverse=True)
    for it,en in sorted_repls:
        if it in orig_text:
            orig_text = orig_text.replace(it, en)

    # Apply word-level simple replacements for remaining common Italian words
    # Only where not inside placeholders
    word_map = {
        r'\bSono\b': 'There are',
        r'\bsono\b': 'are',
        r'\bNon è consentito\b': 'It is not permitted',
        r'\bnon è consentito\b': 'it is not permitted',
        r'\bprima di aver completato\b': 'before completing',
        r'\bFino a\b': 'Up to',
        r'\bFino\b': 'Up to',
        r'\bproroga\b': 'extension',
        r'\bUfficio Immigrazione\b': 'Immigration Office',
        r'\bMulta fino a\b': 'Fine of up to',
        r'\banno di reclusione\b': 'year imprisonment',
        r'\bSequestro\b': 'Seizure',
        r'\bprocedimento penale\b': 'criminal proceedings',
        r'\bValuta\b': 'Currency',
        r'\bvaluta\b': 'currency',
        r'\bFisco\b': 'Tax regime',
        r'\bSchengen\b': 'Schengen',
        r'\bPorto principale\b': 'Main harbour',
        r'\bHarbour principale\b': 'Main harbour',
        r'\bPorto della Luz\b': 'Puerto de la Luz',
        r'\bil periodo di soggiorno\b': 'the period of stay',
        r'\bresiduo di 6 mesi\b': '6 months remaining',
        r'\bbiglietto di ritorno/prosecuzione\b': 'return/onward ticket',
        r'\bmezzi di sostentamento\b': 'means of subsistence',
        r'\b sufficienti per il soggiorno\b': ' sufficient for the stay',
        r'\bCartacea o via totem aeroportuale\b': 'paper form or via airport kiosk',
        r'\bI cittadini italiani entrano senza visto come turisti\b': 'Italian citizens enter visa-free as tourists',
        r'\brequisiti di fondi e biglietto di ritorno sono verificati al controllo di frontiera\b': 'proof of funds and return ticket is checked at border control',
        r'\bTasso di cambio fisso\b': 'Fixed exchange rate',
        r'\bRegole import barca\b': 'Boat import rules',
        r'\bpresso Cayman Customs\b': 'with Cayman Customs',
        r'\bRichiesta dimostrazione di\b': 'Proof required of',
        r'\bElenco nationalities not requiring visa\b': 'nationalities not requiring a visa list',
        r'\bTotale\b': 'Total',
        r'\bGratuita\b': 'Free',
        r'\bgratuita\b': 'free',
        r'\bDettagli\b': 'Details',
        r'\bDichiarazione\b': 'Declaration',
        r'\bDocumenti richiesti\b': 'Documents required',
        r'\bPunti di ingresso\b': 'Ports of entry',
        r'\bDurata\b': 'Duration',
        r'\bScadenza\b': 'Expiry',
        r'\bAnno\b': 'Year',
        r'\bMese\b': 'Month',
        r'\bGiorno\b': 'Day',
        r'\bNotte\b': 'Night',
        r'\bSettimana\b': 'Week',
        r'\bOra\b': 'Hour',
        r'\bOrario\b': 'Hours',
        r'\bCosto\b': 'Cost',
        r'\bPrezzo\b': 'Price',
        r'\bTariffa\b': 'Tariff',
        r'\bTassa\b': 'Fee',
        r'\bImposta\b': 'Tax',
        r'\bServizi\b': 'Services',
        r'\bServizio\b': 'Service',
        r'\bManutenzione\b': 'Maintenance',
        r'\bCantiere\b': 'Boatyard',
        r'\bCantieri\b': 'Boatyards',
        r'\bAlaggio\b': 'Haul-out',
        r'\bVarato\b': 'Launched',
        r'\bOrmeggio\b': 'Berth',
        r'\bPosto barca\b': 'Berth',
        r'\bTra\b': 'Between',
        r'\be\b': 'and',
        r'\bo\b': 'or',
        r'\bcon\b': 'with',
        r'\bsenza\b': 'without',
        r'\bper\b': 'for',
        r'\bda\b': 'from',
        r'\bdi\b': 'of',
        r'\bdel\b': 'of the',
        r'\bdella\b': 'of the',
        r'\bdelle\b': 'of the',
        r'\bdei\b': 'of the',
        r'\bdegli\b': 'of the',
        r'\bal\b': 'at the',
        r'\balla\b': 'at the',
        r'\balle\b': 'at the',
        r'\bai\b': 'at the',
        r'\bagli\b': 'at the',
        r'\bsu\b': 'on',
        r'\bin\b': 'in',
        r'\btra\b': 'between',
        r'\bcome\b': 'as',
        r'\banche\b': 'also',
        r'\bsolo\b': 'only',
        r'\bancora\b': 'still',
        r'\bsempre\b': 'always',
        r'\bmai\b': 'never',
        r'\bmolto\b': 'very',
        r'\bpiù\b': 'more',
        r'\bmeno\b': 'less',
        r'\btutti\b': 'all',
        r'\btutte\b': 'all',
        r'\btutto\b': 'all',
        r'\bnessuno\b': 'no one',
        r'\bnessun\b': 'no',
        r'\bnessuna\b': 'no',
        r'\bogni\b': 'each',
        r'\baltri\b': 'other',
        r'\baltro\b': 'other',
        r'\baltro\b': 'other',
        r'\bproprio\b': 'own',
        r'\bstesso\b': 'same',
        r'\bnuovo\b': 'new',
        r'\bvecchio\b': 'old',
        r'\bgrande\b': 'large',
        r'\bpiccolo\b': 'small',
        r'\bbuono\b': 'good',
        r'\bcattivo\b': 'bad',
        r'\balto\b': 'high',
        r'\bbasso\b': 'low',
        r'\bprimo\b': 'first',
        r'\bultimo\b': 'last',
        r'\bsecondo\b': 'second',
        r'\bterzo\b': 'third',
    }
    for pat,repl in word_map.items():
        orig_text = re.sub(pat, repl, orig_text)

    # Fix leftover Italian fragments that are common: "Fino a" already handled, " circa " -> " about "
    orig_text = orig_text.replace(" circa ", " about ")
    orig_text = orig_text.replace(" circa**", " about**")
    # Fix "l'Italia figura nella lista ufficiale" -> "Italy is on the official ... list"
    orig_text = orig_text.replace("l'Italia figura nella lista ufficiale *Visa Not Required*", "Italy is on the official *Visa Not Required* list")
    orig_text = orig_text.replace("l'Italia figura nella lista ufficiale", "Italy is on the official list")
    # Fix "deve coprire il periodo di soggiorno" -> "must cover the period of stay"
    orig_text = orig_text.replace("deve coprire il periodo di soggiorno", "must cover the period of stay")
    orig_text = orig_text.replace("(non è richiesto un residuo di 6 mesi)", "(no 6 months' remaining validity required)")
    # Fix "Richiesta dimostrazione di" already
    # Fix URLs placeholder restoration
    # Restore placeholders in reverse order (longest key first)
    for key in sorted(placeholders.keys(), key=len, reverse=True):
        orig_text = orig_text.replace(key, placeholders[key])
    # Restore link URLs: keys like __PHxx__ that contained __LINKURL__... need to extract url
    # Actually we stored placeholders for link URLs as __PHx__ -> "__LINKURL__url__"
    # Need to replace those markers
    # Find pattern __PH\d+__ that maps to __LINKURL__url__
    for k,v in list(placeholders.items()):
        if v.startswith("__LINKURL__") and k in orig_text:
            # v is __LINKURL__url__
            url = v.replace("__LINKURL__","").replace("__","")
            # But we already restored placeholder above, so now orig_text contains v string? Let's handle
            pass
    # Alternative: directly replace __LINKURL__ markers
    orig_text = re.sub(r'__LINKURL__(.*?)__', lambda m: m.group(1), orig_text)
    # Restore remaining __PH placeholders that may have been nested? Already done

    # Post-process: fix double spaces, fix "and" incorrectly replacing inside words? word_map \be\b may have corrupted. Let's revert accidental splits: fix "for" inside words
    # Our \be\b replacement may have broken words containing e - but regex \b ensures word boundary so safe.
    # Fix common artefacts
    orig_text = orig_text.replace("DENTRO l'Schengen Area", "INSIDE the Schengen Area")
    orig_text = orig_text.replace("DENTRO l'Area", "INSIDE the Area")
    orig_text = orig_text.replace("€/notte", "€/night")
    orig_text = orig_text.replace("€/night", "€/night")
    orig_text = orig_text.replace("valuta euro", "currency euro")
    orig_text = orig_text.replace("currency euro", "currency euro")
    # Ensure DATA MISSING stays uppercase
    orig_text = orig_text.replace("**DATA MISSING**", "**DATA MISSING**")
    # Translate remaining obvious Italian bits: "diurno" -> "daytime"
    orig_text = orig_text.replace("diurno", "daytime")
    orig_text = orig_text.replace("verificare sul posto", "check locally")
    orig_text = orig_text.replace("verificare", "check")
    orig_text = orig_text.replace("Verificare", "Check")
    orig_text = orig_text.replace("controlli polizia/dogana", "police/customs checks")
    orig_text = orig_text.replace("nessuna formalità", "no formalities")
    orig_text = orig_text.replace("Nessuna formalità", "No formalities")
    orig_text = orig_text.replace("territorio nazionale unico", "single national territory")
    orig_text = orig_text.replace("Tra le isole", "Between islands")
    orig_text = orig_text.replace("tra le isole", "between islands")
    orig_text = orig_text.replace("e verso il continente:", "and to the mainland:")
    orig_text = orig_text.replace("Da porti", "From ports")
    orig_text = orig_text.replace("Da porti", "From ports")
    orig_text = orig_text.replace("Da porti", "From ports")
    # Last updated fix
    orig_text = orig_text.replace("Last updated:", "Last updated:")
    return orig_text

def process_batch(sources):
    total=0
    for src_dir in sources:
        it_base = IT_ROOT/src_dir
        en_base = EN_ROOT/src_dir
        for root,dirs,files in os.walk(it_base):
            for f in files:
                if not f.endswith(".md"): continue
                it_path = pathlib.Path(root)/f
                rel = it_path.relative_to(IT_ROOT)
                en_path = EN_ROOT/rel
                en_path.parent.mkdir(parents=True, exist_ok=True)
                text = it_path.read_text(encoding="utf-8")
                translated = translate_content(text, str(it_path))
                en_path.write_text(translated, encoding="utf-8")
                total+=1
    return total

if __name__ == "__main__":
    requested = ["canarie","cayman","cipro","colombia","costarica","croazia","cuba","curacao","dominica","egitto","francia","giamaica","grecia","grenada","guadalupa"]
    final = [d for d in requested if (IT_ROOT/d).exists()]
    print(f"Batch: {final}")
    cnt = process_batch(final)
    print(f"Translated {cnt} files")
    for d in final:
        it_c = sum(1 for _ in (IT_ROOT/d).rglob("*.md"))
        en_c = sum(1 for _ in (EN_ROOT/d).rglob("*.md"))
        print(f"{d}: it={it_c} en={en_c} {'OK' if it_c==en_c else 'MISMATCH'}")
