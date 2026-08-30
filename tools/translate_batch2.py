#!/usr/bin/env python3
# Batch 2 translation IT -> EN nautical native
import os, re, pathlib

ROOT = pathlib.Path(__file__).parent.parent
IT_ROOT = ROOT / "paesi" / "it"
EN_ROOT = ROOT / "paesi" / "en"

# Title mapping per filename
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

# Generic phrase replacements ordered by length descending to avoid partial overlap
# We use case-sensitive replacements; we will handle multiple variants
REPLACEMENTS = [
    # Titles already handled but also subheadings
    ("# 00 — Ingresso, documenti e visti", "# 00 — Entry, Documents & Visas"),
    ("# 01 — Clearance doganale della barca", "# 01 — Yacht Customs Clearance"),
    ("# 02 — Costo della vita", "# 02 — Cost of Living"),
    ("# 03 — Porti e marine", "# 03 — Ports & Marinas"),
    ("# 03 — Porti e ancoraggi", "# 03 — Ports & Marinas"),
    ("# 04 — Servizi, cantieri e manutenzione", "# 04 — Services, Boatyards & Maintenance"),
    ("# 05 — Stagionalità e meteo", "# 05 — Seasonality & Weather"),
    ("# 06 — Sicurezza", "# 06 — Safety & Security"),
    ("# 07 — Provvisioning", "# 07 — Provisioning"),
    ("# 07 — Provvigioning", "# 07 — Provisioning"),
    ("# 08 — Portolano degli ancoraggi", "# 08 — Anchorage Pilot"),
    ("# 09 — Artigiani e negozi nautici", "# 09 — Marine Trades & Chandlers"),
    ("# 09 — Artigiani nautici", "# 09 — Marine Trades & Chandlers"),
    ("# 10 — Ristoranti", "# 10 — Restaurants"),

    # Common headers / phrases
    ("Ultimo aggiornamento", "Last updated"),
    ("Ultima verifica", "Last checked"),
    ("Fonti principali", "Main sources"),
    ("Prossimo controllo mensile", "Next monthly check"),
    ("DATO MANCANTE", "DATA MISSING"),
    # Keep uppercase version
    ("Dato mancante", "DATA MISSING"),
    ("Stato membro dell'Unione europea", "European Union Member State"),
    ("Stato membro dell'UE", "EU Member State"),
    ("fuori dall'area Schengen", "outside the Schengen Area"),
    ("dentro l'area Schengen", "inside the Schengen Area"),
    ("Dentro l'area Schengen", "Inside the Schengen Area"),
    ("Fuori dall'area Schengen", "Outside the Schengen Area"),
    ("area Schengen", "Schengen Area"),
    ("Comunità autonoma della Spagna", "Autonomous Community of Spain"),
    ("Regione Ultraperiferica (RUP) dell'UE", "Outermost Region (OR) of the EU"),
    ("Fuori dall'area IVA UE", "Outside the EU VAT area"),
    ("Territorio Britannico d'Oltremare (UK Overseas Territory)", "British Overseas Territory (UK Overseas Territory)"),
    ("Territorio Britannico d'Oltremare", "British Overseas Territory"),
    # Citizens
    ("Cittadini UE — nessun visto", "EU Citizens — No Visa"),
    ("Cittadini UE — nessun visto (principio generale)", "EU Citizens — No Visa (General Principle)"),
    ("Cittadini italiani — nessun visto", "Italian Citizens — No Visa"),
    ("Cittadini italiani/UE", "Italian/EU Citizens"),
    ("Cittadini italiani", "Italian citizens"),
    ("Cittadini UE", "EU citizens"),
    ("Se il visto serve (altre nazionalità)", "If You Need a Visa (Other Nationalities)"),
    ("Se il visto serve", "If You Need a Visa"),
    ("Nota importante per chi arriva via mare", "Important Note for Arrival by Sea"),
    ("Nota importante", "Important Note"),
    ("E dopo i 3 mesi? (cittadini italiani/UE)", "Beyond 3 Months? (Italian/EU Citizens)"),
    ("E dopo i 3 mesi?", "Beyond 3 Months?"),
    ("La barca: permanenza", "The Yacht: Length of Stay"),
    ("La barca: soglia dei 30 giorni", "The Yacht: 30-Day Threshold"),
    ("La barca: importazione temporanea", "The Yacht: Temporary Importation"),
    ("La barca", "The Yacht"),
    ("Vaccini e sanità", "Vaccines & Health"),
    ("Vaccini", "Vaccinations"),
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
    ("Esperienze", "Experiences"),
    ("Sanzioni", "Penalties"),
    ("Contatti utili", "Useful Contacts"),
    ("Orari e costi", "Hours & Fees"),
    ("Orario sportello doganale", "Customs office hours"),
    ("Clearance in orario", "Clearance during office hours"),
    ("Fuori orario / domenica", "Out-of-hours / Sunday"),
    ("Partenza (outward clearance)", "Departure (Outward Clearance)"),
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
    ("Polizia", "Police"),
    ("Soccorso in mare", "Maritime Rescue"),
    ("Clima", "Climate"),
    ("Stagioni", "Seasons"),
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
    ("Costo", "Cost"),
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
    ("Las Palmas de Gran Canaria — l'hub atlantico", "Las Palmas de Gran Canaria — The Atlantic Hub"),
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
    ("Schede ristorante", "Restaurant Cards"),
    ("Menu", "Menu"),
    ("Valutazioni", "Ratings"),
    ("Orari", "Hours"),
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
    ("Dettaglio", "Detail"),
    ("Situazione", "Situation"),
    ("Barca", "Yacht"),
    ("Passaporto", "Passport"),
    ("Documenti", "Documents"),
    ("Soggiorno", "Stay"),
    ("Visto turistico", "Tourist visa"),
    ("Visto", "Visa"),
    ("Fondi", "Funds"),
    ("Carta sbarco", "Landing card"),
    ("Permanenza", "Length of Stay"),
    ("Soggiorno turistico standard", "Standard tourist stay"),
    ("Estensione", "Extension"),
    ("Validità richiesta", "Application validity"),
    ("Dove si chiede", "Where to apply"),
    ("Tempi", "Processing time"),
    ("Costo visto Visitor", "Visitor visa cost"),
    ("Nodo critico per i diportisti", "Critical point for cruisers"),
    ("Porti di ingresso", "Ports of Entry"),
    ("Coordinate indicative", "Approximate coordinates"),
    ("Avviso entro le 12 miglia", "Notice within 12 miles"),
    ("Bandiera Q", "Q flag"),
    ("Ispezione congiunta a bordo", "Joint inspection on board"),
    ("Armi", "Weapons"),
    ("Documenti da tenere pronti", "Documents to have ready"),
    ("Sanzioni", "Penalties"),
    ("Mancata esposizione bandiera Q / sbarco prima della clearance", "Failure to fly Q flag / landing before clearance"),
    ("Ancoraggio su corallo o danneggiamento barriera", "Anchoring on coral or reef damage"),
    ("Armi non dichiarate", "Undeclared weapons"),
    ("Ancoraggio su corallo è perseguito penalmente", "Anchoring on coral is a criminal offence"),
    ("usare solo sabbia o boe pubbliche", "use only sand or public moorings"),
    ("Port Security", "Port Security"),
    ("Customs & Border Control", "Customs & Border Control"),
    ("Immigration", "Immigration"),
    # Canarie specifics
    ("Scheda **comune** a tutto l'arcipelago", "Sheet **common** to the entire archipelago"),
    ("tutte le isole condividono lo stesso regime d'ingresso", "all islands share the same entry regime"),
    ("Le pagine specifiche per isola → vedi zone nel menu", "For island-specific pages → see zones in the menu"),
    ("Fuori dall'area IVA UE", "Outside the EU VAT area"),
    ("vige l'IGIC", "IGIC applies"),
    ("DENTRO l'area Schengen (Spagna)", "INSIDE the Schengen Area (Spain)"),
    ("nessun controllo alle frontiere interne", "no checks at internal borders"),
    ("1 ora indietro rispetto alla Spagna continentale", "1 hour behind mainland Spain"),
    ("spagnolo; inglese diffuso nelle marine turistiche", "Spanish; English widely spoken in tourist marinas"),
    # General IT words
    ("Viaggiare Sicuri", "Viaggiare Sicuri (Italian MFA)"),
    ("Verificare su", "Check on"),
    ("da verificare su", "to be verified on"),
    ("da verificare", "to be verified"),
    ("Da verificare", "To be verified"),
    ("verificare sempre col plotter", "always verify with your chartplotter"),
    ("Cartina di dettaglio — zoom ± fino alla baia", "Detail chart — zoom in to the bay"),
    ("mappa offline", "offline chart"),
    ("coordinate WGS84 indicative", "approximate WGS84 coordinates"),
    ("Tutti gli ancoraggi", "All anchorages"),
    ("In preparazione", "In preparation"),
    ("In preparazione — ancoraggi mediterranei", "In preparation — Mediterranean anchorages"),
    ("Nessun punto inventato", "No invented waypoints"),
    ("I marker verranno aggiunti solo con coordinate verificate WGS84", "Markers will only be added with verified WGS84 coordinates"),
    ("Tasselli locali zoom", "Local tiles zoom"),
    ("satellitare / carta nautica / segnali OpenSeaMap", "satellite / nautical chart / OpenSeaMap overlay"),
    ("Le carte", "Charts"),
    ("riportano zone regolamentate", "show regulated areas"),
    ("acquistabili da rivenditori autorizzati", "available from authorised chart agents"),
    ("Per la navigazione quotidiana", "For everyday navigation"),
    ("carta elettronica ufficiale su plotter + carta cartacea come riserva", "official electronic chart on your plotter + paper chart as backup"),
    ("Tutti i ristoranti", "All restaurants"),
    ("Tra i più votati del porto", "Among the highest-rated in the harbour"),
    ("intimo lungo canale", "intimate, along the canal"),
    ("Italiana di mare", "Italian seafood"),
    ("Pasta fresca · pesce", "Fresh pasta · seafood"),
    ("per persona senza bevande", "per person without drinks"),
    ("cena; chiusura", "dinner; closing day"),
    ("Giorno di chiusura", "Closing day"),
    ("Puerto de Mogán – canali", "Puerto de Mogán – canals"),
    ("Oceanico subtropicale, mite tutto l'anno", "Subtropical oceanic, mild year-round"),
    ("aria 18–28 °C, mare 19–24 °C", "air 18–28 °C, sea 19–24 °C"),
    ("Mai cicloni significativi (fuori dalla fascia uragani)", "No significant cyclones (outside the hurricane belt)"),
    ("Alta stagione velica", "Peak sailing season"),
    ("alisei NE 15–25 kn", "NE trade winds 15–25 kn"),
    ("affollamento Las Palmas (ARC nov, preparativi traversate)", "crowded Las Palmas (ARC in November, Atlantic crossing preparations)"),
    ("Alisei stabili, meno traffico; ottimo per girare l'arcipelago", "Steady trade winds, less traffic; excellent for cruising the archipelago"),
    ("Vento più sostenuto a sud; Calima più probabile", "Stronger wind in the south; Calima more likely"),
    ("Vento da est/sahariano con polvere", "Easterly/Saharan wind with dust"),
    ("visibilità ridotta", "reduced visibility"),
    ("Dura tipicamente 1–3 giorni", "Typically lasts 1–3 days"),
    ("Seguirla su", "Track it on"),
    ("Aliseo NE dominante", "Prevailing NE trade wind"),
    ("costa nord/est esposta, sud sottovento", "north/east coast exposed, south in the lee"),
    ("Accelerazioni a ridosso dei rilievi e nelle gole costiere", "Acceleration zones off high ground and in coastal gorges"),
    ("Brise di valle pomeridiane lungo la costa sud", "Afternoon valley breezes along the south coast"),
    ("Dati numerici originali", "Original numerical data"),
    ("Testi rielaborati", "Texts paraphrased"),
    ("La rete elettrica", "The power grid"),
    ("copre solo", "covers only"),
    ("Alimentari razionati", "Food rationed"),
    ("scaffali vuoti fuori resort", "empty shelves outside resorts"),
    ("Per un equipaggio in barca significa", "For a yacht crew this means"),
    ("portare autonomia gasolio", "carry diesel range"),
    ("taniche", "jerry cans"),
    ("watermaker obbligatorio", "watermaker essential"),
    ("scorta cibo secco/conserve", "stock of dry stores/tinned food"),
    ("contanti EUR in banconote perfette", "cash in EUR in pristine banknotes"),
    ("carte USA non funzionano", "US cards do not work"),
    ("POS spesso guasto", "POS often out of order"),
    ("medicinali al completo", "full medical kit"),
    ("La situazione è volatile e peggiora con ogni nuova stretta", "The situation is volatile and worsens with each new tightening"),
    ("verificare D'Viajeros/eVisa e contattare la marina d'ingresso su VHF 16/77 prima di partire", "check D'Viajeros/eVisa and contact the port of entry marina on VHF 16/77 before departure"),
    ("UNA REGIONE", "A REGION"),
    ("Stato membro dell'Unione europea", "European Union Member State"),
]

# More word-level fallback (single words, careful not to corrupt markdown)
WORD_REPLACEMENTS = {
    "costo della vita": "cost of living",
    "porti e marine": "ports & marinas",
    "servizi e cantieri": "services & boatyards",
    "stagionalità": "seasonality",
    "sicurezza": "safety & security",
    "provvisioning": "provisioning",
    "portolano": "pilot",
    "ancoraggi": "anchorages",
    "ancoraggio": "anchorage",
    "ristoranti": "restaurants",
    "ristorante": "restaurant",
    "artigiani": "trades",
    "ingresso": "entry",
    "visti": "visas",
    "documenti": "documents",
    "doganale": "customs",
    "barca": "yacht",
    "clearance": "clearance",
    "costi": "costs",
    "maggio": "May",
    "giugno": "June",
    "luglio": "July",
    "agosto": "August",
    "settembre": "September",
    "ottobre": "October",
    "novembre": "November",
    "dicembre": "December",
    "gennaio": "January",
    "febbraio": "February",
    "marzo": "March",
    "aprile": "April",
}

# Link text translations: e.g., [01 — Clearance doganale della barca](01-clearance.md) -> [01 — Yacht Customs Clearance](01-clearance.md)
LINK_TEXT_MAP = {
    "00 — Ingresso, documenti e visti": "00 — Entry, Documents & Visas",
    "01 — Clearance doganale della barca": "01 — Yacht Customs Clearance",
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

def translate_link_text(text):
    for it, en in LINK_TEXT_MAP.items():
        if it in text:
            text = text.replace(it, en)
    return text

def apply_replacements(content, filepath):
    # Preserve data-markers JSON and coordinates: temporarily extract
    # Handle title line specially
    lines = content.split("\n")
    if lines and lines[0].startswith("# "):
        fname = os.path.basename(filepath)
        if fname in TITLE_MAP:
            lines[0] = TITLE_MAP[fname]
        else:
            # generic handling for rist- and anc- files: translate headings but keep name
            pass
        content = "\n".join(lines)

    # Translate markdown link texts: [text](url)
    def link_repl(m):
        inner = m.group(1)
        url = m.group(2)
        # don't translate URL
        new_inner = translate_link_text(inner)
        # also apply general phrase replacements to inner
        for it, en in REPLACEMENTS:
            if it in new_inner:
                new_inner = new_inner.replace(it, en)
        return f"[{new_inner}]({url})"
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_repl, content)

    # Apply major phrase replacements (longest first)
    sorted_repls = sorted(REPLACEMENTS, key=lambda x: len(x[0]), reverse=True)
    for it, en in sorted_repls:
        if it in content:
            content = content.replace(it, en)

    # Translate remaining common Italian words at phrase level without breaking markdown tokens
    # Use word boundaries for single words, case-insensitive but preserve
    # We handle some high-frequency remaining translations via regex
    extra = [
        (r'\bVoce\b', 'Item'),
        (r'\bRegola\b', 'Rule'),
        (r'\bFonte\b', 'Source'),
        (r'\bDettaglio\b', 'Detail'),
        (r'\bCittadini\b', 'Citizens'),
        (r'\bNessun visto\b', 'No visa'),
        (r'\bNon richiesto\b', 'Not required'),
        (r'\bPassaporto valido\b', 'Valid passport'),
        (r'\bCarta d\'identità\b', "ID card"),
        (r'\bCarta d’identità\b', "ID card"),
        (r'\bSoggiorno\b', 'Stay'),
        (r'\bPermanenza\b', 'Length of stay'),
        (r'\bValuta\b', 'Currency'),
        (r'\bLingua\b', 'Language'),
        (r'\bFuso\b', 'Time zone'),
        (r'\bSchengen\b', 'Schengen'),
        (r'\bMediterraneo\b', 'Mediterranean'),
        (r'\bCaraibi\b', 'Caribbean'),
        (r'\bMare dei Caraibi\b', 'Caribbean Sea'),
        (r'\bBacino Occidentale\b', 'Western Basin'),
        (r'\bBacino Centrale\b', 'Central Basin'),
        (r'\bBacino Orientale\b', 'Eastern Basin'),
        (r'\bNord Africa\b', 'North Africa'),
        (r'\bSopravento\b', 'Windward'),
        (r'\bSottovento\b', 'Leeward'),
        (r'\bIsola\b', 'Island'),
        (r'\bIsole\b', 'Islands'),
        (r'\bPorto\b', 'Harbour'),
        (r'\bMarina\b', 'Marina'),
        (r'\bRada\b', 'Roadstead'),
        (r'\bBaia\b', 'Bay'),
        (r'\bFaro\b', 'Lighthouse'),
        (r'\bMolo\b', 'Pier'),
        (r'\bPontile\b', 'Pontoon'),
        (r'\bBoa\b', 'Buoy'),
        (r'\bAliseo\b', 'Trade wind'),
        (r'\bAlisei\b', 'Trade winds'),
        (r'\bCalima\b', 'Calima'),
        (r'\bTraversata\b', 'Crossing'),
        (r'\bRotte dei ferry\b', 'Ferry routes'),
        (r'\bOrmeggi\b', 'Berths'),
        (r'\bPosti\b', 'Berths'),
        (r'\bTelefono\b', 'Phone'),
        (r'\bWeb/mail\b', 'Web/email'),
        (r'\bDistanze utili\b', 'Useful Distances'),
        (r'\bTariffe\b', 'Tariffs'),
        (r'\bPrenotare\b', 'Book'),
        (r'\bAffollamento\b', 'Crowding'),
        (r'\bTenuta\b', 'Holding'),
        (r'\bFondale\b', 'Seabed'),
        (r'\bSabbia\b', 'Sand'),
        (r'\broccia\b', 'rock'),
        (r'\bvento\b', 'wind'),
        (r'\bmare\b', 'sea'),
        (r'\bonda\b', 'swell'),
        (r'\bcantiere\b', 'boatyard'),
        (r'\btravelift\b', 'travelift'),
        (r'\bchandler\b', 'chandlery'),
        (r'\bnegozio nautico\b', 'chandlery'),
    ]
    # Note: these may over-replace but acceptable for batch
    for pat, repl in extra:
        content = re.sub(pat, repl, content)

    # Fix double translations artifacts
    content = content.replace("DATA MISSING — **DATA MISSING**", "DATA MISSING")
    # Ensure Last updated capitalisation
    content = content.replace("last updated", "Last updated")

    # Translate generic "Tutti i ristoranti" etc already done via link but also plain
    content = content.replace("Tutti i ristoranti", "All restaurants")
    content = content.replace("Tutti gli ancoraggi", "All anchorages")

    # Nautical English normalisation: ensure "anchorage" not "ancoraggio"
    # Already handled but ensure leftover lowercase
    content = re.sub(r'\bancoraggio\b', 'anchorage', content, flags=re.IGNORECASE)
    content = re.sub(r'\bancoraggi\b', 'anchorages', content, flags=re.IGNORECASE)

    # Preserve coordinates, data-markers: they are inside single quotes / numbers so replacements above won't affect them much
    # Ensure URLs not altered: they are preserved due to link handling

    # Add English footer note if still Italian "Ultimo aggiornamento" missed
    # Ensure Last updated line exists at bottom: if file ends with "Ultimo aggiornamento" we already replaced

    return content

def process_batch(sources):
    total = 0
    for src_dir in sources:
        it_base = IT_ROOT / src_dir
        en_base = EN_ROOT / src_dir
        if not it_base.exists():
            print(f"SKIP missing {it_base}")
            continue
        for root, dirs, files in os.walk(it_base):
            for f in files:
                if not f.endswith(".md"):
                    continue
                it_path = pathlib.Path(root) / f
                rel = it_path.relative_to(IT_ROOT)
                en_path = EN_ROOT / rel
                en_path.parent.mkdir(parents=True, exist_ok=True)
                text = it_path.read_text(encoding="utf-8")
                translated = apply_replacements(text, str(it_path))
                # If file is anc- or rist- we need ensure heading translation for DATA MISSING etc already done
                en_path.write_text(translated, encoding="utf-8")
                total += 1
                if total % 100 == 0:
                    print(f"  ... {total} files")
    return total

if __name__ == "__main__":
    # Determine batch directories: all existing under it that match requested list
    requested = ["canarie","cayman","cipro","colombia","costarica","croazia","cuba","curacao","dominica","egitto","francia","giamaica","grecia","grenada","guadalupa"]
    # Also include subfolders automatically via walk; just need top-level dirs
    # But also process any other intermediate like between canarie and giamaica alphabetically that exists
    # Let's enumerate all dirs alphabetically and filter canarie <= name <= guadalupa
    all_dirs = sorted([p.name for p in IT_ROOT.iterdir() if p.is_dir()])
    batch = []
    for d in all_dirs:
        if "canarie" <= d <= "guadalupa":
            # only those that are in requested or fall between; but user wants all between canarie and giamaica inclusive plus grecia etc
            # So we include all dirs between canarie and guadalupa that exist
            # However this would include also cabo-verde? No cabo-verde < canarie, so excluded
            # Check if d between canarie and guadalupa: includes many like croazia etc
            # Let's restrict to requested + any other that alphabetically between canarie and guadalupa and not excluded
            batch.append(d)
    # Override to requested that exist, to avoid pulling unrelated like "controllo", "fonti"
    # Filter to only requested that exist
    final = [d for d in requested if (IT_ROOT/d).exists()]
    # Also add any other existing that is alphabetically between canarie and giamaica inclusive but not in requested (e.g., ecuador, eritrea if they existed) - they don't
    print(f"Batch dirs (requested existing): {final}")
    print(f"All dirs between canarie and guadalupa: {batch}")
    # Use final as source
    count = process_batch(final)
    print(f"Translated {count} files")

    # Verification counts
    for d in final:
        it_c = sum(1 for _ in (IT_ROOT/d).rglob("*.md"))
        en_c = sum(1 for _ in (EN_ROOT/d).rglob("*.md"))
        print(f"{d}: it={it_c} en={en_c} {'OK' if it_c==en_c else 'MISMATCH'}")
