#!/usr/bin/env python3
# Batch translation IT -> FR nautical native for Portolano wiki
import os, re, pathlib

ROOT = pathlib.Path(__file__).parent.parent
IT_ROOT = ROOT / "paesi" / "it"
FR_ROOT = ROOT / "paesi" / "fr"

TITLE_MAP = {
    "00-ingresso-visti.md": "# 00 — Entrée, Documents & Visas",
    "01-clearance.md": "# 01 — Formalités douanières",
    "02-costi.md": "# 02 — Coût de la vie",
    "03-porti-ancoraggi.md": "# 03 — Ports & Marinas",
    "04-servizi-cantieri.md": "# 04 — Services, Chantiers & Entretien",
    "05-stagionalita-meteo.md": "# 05 — Saisonnalité & Météo",
    "06-sicurezza.md": "# 06 — Sécurité",
    "07-provvisioning.md": "# 07 — Avitaillement",
    "08-ancoraggi.md": "# 08 — Guide des mouillages",
    "09-artigiani-nautici.md": "# 09 — Artisans & Shipchandlers",
    "10-ristoranti.md": "# 10 — Restaurants",
}

REPLACEMENTS = [
    # Titles
    ("# 00 — Ingresso, documenti e visti", "# 00 — Entrée, Documents & Visas"),
    ("# 01 — Clearance doganale della barca", "# 01 — Formalités douanières"),
    ("# 02 — Costo della vita", "# 02 — Coût de la vie"),
    ("# 03 — Porti e marine", "# 03 — Ports & Marinas"),
    ("# 03 — Porti e ancoraggi", "# 03 — Ports & Marinas"),
    ("# 04 — Servizi, cantieri e manutenzione", "# 04 — Services, Chantiers & Entretien"),
    ("# 05 — Stagionalità e meteo", "# 05 — Saisonnalité & Météo"),
    ("# 06 — Sicurezza", "# 06 — Sécurité"),
    ("# 07 — Provvisioning", "# 07 — Avitaillement"),
    ("# 07 — Provvigioning", "# 07 — Avitaillement"),
    ("# 08 — Portolano degli ancoraggi", "# 08 — Guide des mouillages"),
    ("# 09 — Artigiani e negozi nautici", "# 09 — Artisans & Shipchandlers"),
    ("# 09 — Artigiani nautici", "# 09 — Artisans & Shipchandlers"),
    ("# 10 — Ristoranti", "# 10 — Restaurants"),

    # Common metadata
    ("Ultimo aggiornamento", "Dernière mise à jour"),
    ("Ultima verifica", "Dernière vérification"),
    ("Ultima verifica completa", "Dernière vérification complète"),
    ("Prossimo controllo mensile", "Prochain contrôle mensuel"),
    ("Fonti principali", "Sources principales"),
    ("DATO MANCANTE", "DONNÉE MANQUANTE"),
    ("Dato mancante", "DONNÉE MANQUANTE"),
    ("Status", "Statut"),

    # Geographic I18N - Bacini, Arcipelaghi, Oceani etc (use FR index.html values)
    ("Arcipelago Lucayano", "Archipel des Lucayes"),
    ("Grandi Antille", "Grandes Antilles"),
    ("Isole Sopravento Settentrionali", "Îles Sous-le-Vent du Nord"),
    ("Isole Sopravento Meridionali", "Îles du Vent"),
    ("Isole Sottovento", "Îles Sous-le-Vent du Sud"),
    ("Isole Caraibiche Occidentali", "Caraïbes occidentales"),
    ("Isole del Canale e della Costa Continentale", "Îles du Canal et Côte continentale"),
    ("Coste dell’America Centrale", "Côte d’Amérique centrale"),
    ("Coste dell'America Centrale", "Côte d’Amérique centrale"),
    ("Bacino Occidentale", "Bassin occidental"),
    ("Bacino Centrale", "Bassin central"),
    ("Bacino Orientale", "Bassin oriental"),
    ("Nord Africa", "Afrique du Nord"),
    ("Mar dei Caraibi", "Mer des Caraïbes"),
    ("Mare dei Caraibi", "Mer des Caraïbes"),
    ("Mediterraneo", "Méditerranée"),
    ("Atlantico", "Atlantique"),
    ("Oceano Atlantico", "Océan Atlantique"),
    ("Pacifico", "Pacifique"),
    ("Oceano Pacifico", "Océan Pacifique"),
    ("Oceano Indiano", "Océan Indien"),
    ("Mar Rosso", "Mer Rouge"),
    ("Caraibi", "Caraïbes"),

    # Country status phrases
    ("Stato membro dell'Unione europea", "État membre de l’Union européenne"),
    ("Stato membro dell'UE", "État membre de l’UE"),
    ("Stato membro dell’Unione europea", "État membre de l’Union européenne"),
    ("Stato extra-UE", "État hors UE"),
    ("fuori dall'area Schengen", "hors de l’espace Schengen"),
    ("dentro l'area Schengen", "dans l’espace Schengen"),
    ("Dentro l'area Schengen", "Dans l’espace Schengen"),
    ("Fuori dall'area Schengen", "Hors de l’espace Schengen"),
    ("area Schengen", "espace Schengen"),
    ("Comunità autonoma della Spagna", "Communauté autonome d’Espagne"),
    ("Regione Ultraperiferica (RUP) dell'UE", "Région ultrapériphérique (RUP) de l’UE"),
    ("Fuori dall'area IVA UE", "Hors zone TVA UE"),
    ("Territorio Britannico d'Oltremare (UK Overseas Territory)", "Territoire britannique d’outre-mer (UK Overseas Territory)"),
    ("Territorio Britannico d'Oltremare", "Territoire britannique d’outre-mer"),
    ("Stato membro UE", "État membre UE"),
    ("Stato extra-UE", "État hors UE"),

    # Citizens
    ("Cittadini UE — nessun visto", "Citoyens UE — pas de visa"),
    ("Cittadini UE — nessun visto (principio generale)", "Citoyens UE — pas de visa (principe général)"),
    ("Cittadini italiani — nessun visto", "Citoyens italiens — pas de visa"),
    ("Cittadini italiani/UE", "Citoyens italiens/UE"),
    ("Cittadini italiani", "Citoyens italiens"),
    ("Cittadini UE", "Citoyens UE"),
    ("Se il visto serve (altre nazionalità)", "Si un visa est nécessaire (autres nationalités)"),
    ("Se il visto serve", "Si un visa est nécessaire"),
    ("Nota importante per chi arriva via mare", "Note importante pour l’arrivée par mer"),
    ("Nota importante", "Note importante"),
    ("E dopo i 3 mesi? (cittadini italiani/UE)", "Au-delà de 3 mois ? (citoyens italiens/UE)"),
    ("E dopo i 3 mesi?", "Au-delà de 3 mois ?"),
    ("La barca: permanenza", "Le bateau : durée de séjour"),
    ("La barca: soglia dei 30 giorni", "Le bateau : seuil des 30 jours"),
    ("La barca: importazione temporanea", "Le bateau : importation temporaire"),
    ("La barca", "Le bateau"),
    ("Vaccini e sanità", "Vaccins & santé"),
    ("Vaccini", "Vaccins"),
    ("Vaccinazioni", "Vaccinations"),
    ("Da verificare prima della partenza", "À vérifier avant le départ"),
    ("Da verificare prima della crociera", "À vérifier avant la croisière"),
    ("Chi deve farla", "Qui doit effectuer les formalités"),
    ("Procedura d'ingresso", "Procédure d’entrée"),
    ("Procedura", "Procédure"),
    ("Copia cartacea e timbro", "Copie papier et tampon"),
    ("Punti agréé / porti d'ingresso", "Points agréés / ports d’entrée"),
    ("Punti agréé", "Points agréés"),
    ("Porti di ingresso (Port of Entry)", "Ports d’entrée (Port of Entry)"),
    ("Porti di ingresso", "Ports d’entrée"),
    ("Porto di Ingresso (Port of Entry)", "Port d’entrée (Port of Entry)"),
    ("Porto di Ingresso", "Port d’entrée"),
    ("Dogana regionale", "Douane régionale"),
    ("Esperienze di naviganti", "Retours de navigateurs"),
    ("Esperienze dei crocieristi", "Retours de navigateurs"),
    ("Esperienze", "Retours d’expérience"),
    ("Sanzioni", "Sanctions"),
    ("Contatti utili", "Contacts utiles"),
    ("Orari e costi", "Horaires & tarifs"),
    ("Orario sportello doganale", "Horaires du guichet douane"),
    ("Clearance in orario", "Formalités aux heures ouvrables"),
    ("Fuori orario / domenica", "Hors horaires / dimanche"),
    ("Partenza (outward clearance)", "Départ (outward clearance)"),
    ("Partenza", "Départ"),
    ("Valutazione sicurezza", "Évaluation sécurité"),
    ("Quadro generale", "Vue d’ensemble"),
    ("Mappa delle zone — offline", "Carte des zones — hors ligne"),
    ("Mappa delle zone", "Carte des zones"),
    ("Zone sicure (consigliate)", "Zones sûres (recommandées)"),
    ("Zone sicure", "Zones sûres"),
    ("Zone sicure / posti da evitare", "Zones sûres / à éviter"),
    ("Attenzioni", "Points d’attention"),
    ("Numeri di emergenza", "Numéros d’urgence"),
    ("A bordo e in navigazione", "À bord et en navigation"),
    ("A bordo e a terra", "À bord et à terre"),
    ("A bordo", "À bord"),
    ("Emergenza unica", "Numéro d’urgence unique"),
    ("Polizia", "Police"),
    ("Soccorso in mare", "Secours en mer"),
    ("Salvataggio ed emergenze", "Sauvetage et urgences"),
    ("Clima", "Climat"),
    ("Stagioni", "Saisons"),
    ("Stagione", "Saison"),
    ("Uragani / cicloni", "Ouragans / cyclones"),
    ("Uragani", "Ouragans"),
    ("Consignes / avvisi", "Consignes / avis"),
    ("Venti locali", "Vents locaux"),
    ("Finestre tipiche", "Fenêtres météo typiques"),
    ("Finestre tipiche di navigazione", "Fenêtres de navigation typiques"),
    ("Link meteo", "Liens météo"),
    ("Link meteo utili", "Liens météo utiles"),
    ("Link meteo e carte locali", "Liens météo et cartes locales"),
    ("Alimentari e spesa di bordo", "Alimentation & avitaillement"),
    ("Alimentari", "Alimentation"),
    ("Mangiare fuori", "Restauration à terre"),
    ("Mangiare fuori (media)", "Restauration à terre (moyenne)"),
    ("Carburanti", "Carburants"),
    ("Trasporti e collegamenti", "Transports & liaisons"),
    ("Trasporti", "Transports"),
    ("Servizi quotidiani e utenze", "Services quotidiens & réseaux"),
    ("Servizi quotidiani", "Services quotidiens"),
    ("Contanti e pagamenti", "Espèces & paiements"),
    ("Approfondimenti", "Pour approfondir"),
    ("Tariffe ormeggi e marine", "Tarifs d’amarrage & marinas"),
    ("Tariffe indicative", "Tarifs indicatifs"),
    ("Tariffe", "Tarifs"),
    ("Contatti marine verificati", "Contacts marinas vérifiés"),
    ("Distanze utili", "Distances utiles"),
    ("Tratta", "Trajet"),
    ("Distanza", "Distance"),
    ("Struttura", "Infrastructure"),
    ("Costo", "Coût"),
    ("Costo/note", "Coût/notes"),
    ("Posto pontile — notte (~12 m)", "Place à quai — par nuit (~12 m)"),
    ("Posto pontile — notte (multiscafo ~12 m)", "Place à quai — par nuit (multicoque ~12 m)"),
    ("Boa / mouillage — notte (~12 m)", "Bouée / mouillage — par nuit (~12 m)"),
    ("Mese pontile (~12 m)", "Mois à quai (~12 m)"),
    ("Elettricità", "Électricité"),
    ("Acqua", "Eau"),
    ("Ancoraggio", "Mouillage"),
    ("Altre strutture", "Autres infrastructures"),
    ("Altri porti", "Autres ports"),
    ("Altri cantieri", "Autres chantiers"),
    ("Regole generali di ancoraggio (prima di tutto)", "Règles générales de mouillage (avant tout)"),
    ("Regole generali", "Règles générales"),
    ("Zone di divieto assoluto (ufficiali)", "Zones d’interdiction absolue (officielles)"),
    ("Zone di divieto assoluto", "Zones d’interdiction absolue"),
    ("Tabella riassuntiva — i migliori ancoraggi", "Tableau récapitulatif — meilleurs mouillages"),
    ("Tabella riassuntiva", "Tableau récapitulatif"),
    ("Mappa generale degli ancoraggi", "Carte générale des mouillages"),
    ("Mappa generale", "Carte générale"),
    ("Cartografia ufficiale", "Cartographie officielle"),
    ("Non inclusi (per ora)", "Non inclus (pour l’instant)"),
    ("Checklist àncora", "Check-list mouillage"),
    ("Checklist", "Check-list"),
    ("Legenda", "Légende"),
    ("Mappa unica", "Carte unique"),
    ("Griglia", "Grille"),
    ("Griglia generale", "Grille générale"),
    ("Schede ristorante", "Fiches restaurant"),
    ("Menu", "Menu"),
    ("Valutazioni", "Évaluations"),
    ("Orari", "Horaires"),
    ("Specialità", "Spécialité"),
    ("Cucina", "Cuisine"),
    ("Location", "Emplacement"),
    ("Contatti", "Contacts"),
    ("Zona", "Zone"),
    ("Campo", "Champ"),
    ("Dettaglio", "Détail"),
    ("Profondità", "Profondeur"),
    ("Tenuta àncora", "Tenue de l’ancre"),
    ("Tenuta", "Tenue"),
    ("Venti/riparo", "Vents/abri"),
    ("Riparo venti prevalenti", "Abri des vents dominants"),
    ("Pericoli", "Dangers"),
    ("Boe/divieti/normative", "Bouées/interdictions/réglementation"),
    ("A terra", "À terre"),
    ("Affollamento", "Affluence"),
    ("Giudizio comunità", "Avis de la communauté"),
    ("Fonte", "Source"),
    ("Voce", "Rubrique"),
    ("Regola", "Règle"),
    ("Situazione", "Situation"),
    ("Barca", "Bateau"),
    ("Passaporto", "Passeport"),
    ("Documenti", "Documents"),
    ("Soggiorno", "Séjour"),
    ("Visto turistico", "Visa touristique"),
    ("Visto", "Visa"),
    ("Fondi", "Ressources"),
    ("Permanenza", "Durée de séjour"),
    ("Soggiorno turistico standard", "Séjour touristique standard"),
    ("Estensione", "Prolongation"),
    ("Validità richiesta", "Validité requise"),
    ("Mappa dei ristoranti", "Carte des restaurants"),
    ("Supermercati", "Supermarchés"),
    ("Mercati", "Marchés"),
    ("Acqua dolce", "Eau douce"),
    ("Acqua e carburante", "Eau et carburant"),
    ("App e fonti", "Applis et sources"),
    ("Bus", "Bus"),
    ("Negozi di attrezzature e shipchandler", "Magasins d’équipement & shipchandler"),
    ("Gas e bombole", "Gaz et bouteilles"),
    ("Dove si trova cosa", "Où trouver quoi"),
    ("Navigazione", "Navigation"),
    ("Foto", "Photos"),
    ("Note pratiche", "Notes pratiques"),
    ("Consigli pratici", "Conseils pratiques"),
    ("Note strategiche", "Notes stratégiques"),

    # Specific sentences observed
    ("Scheda **comune** a tutto l'arcipelago", "Fiche **commune** à tout l’archipel"),
    ("Scheda **comune** a tutti i 6 mari italiani", "Fiche **commune** aux 6 mers italiennes"),
    ("tutte le isole condividono lo stesso regime d'ingresso", "toutes les îles partagent le même régime d’entrée"),
    ("Le pagine specifiche per zona → vedi menu", "Pages spécifiques par zone → voir menu"),
    ("Le pagine specifiche per isola → vedi zone nel menu", "Pages spécifiques par île → voir zones dans le menu"),
    ("Fuori dall'area IVA UE", "Hors zone TVA UE"),
    ("vige l'IGIC", "IGIC en vigueur"),
    ("DENTRO l'area Schengen (Spagna)", "DANS l’espace Schengen (Espagne)"),
    ("nessun controllo alle frontiere interne", "aucun contrôle aux frontières intérieures"),
    ("1 ora indietro rispetto alla Spagna continentale", "1 heure de retard sur l’Espagne continentale"),
    ("spagnolo; inglese diffuso nelle marine turistiche", "espagnol ; anglais courant dans les marinas touristiques"),
    ("Iscriviti", "S’inscrire"),
    ("Accedi", "Se connecter"),
    ("Profilo", "Profil"),
    ("Contribuisci", "Contribuer"),
]

LINK_TEXT_MAP = {
    "00 — Ingresso, documenti e visti": "00 — Entrée, Documents & Visas",
    "01 — Clearance doganale della barca": "01 — Formalités douanières",
    "01 — Clearance": "01 — Formalités douanières",
    "02 — Costo della vita": "02 — Coût de la vie",
    "03 — Porti e marine": "03 — Ports & Marinas",
    "03 — Porti e ancoraggi": "03 — Ports & Marinas",
    "04 — Servizi, cantieri e manutenzione": "04 — Services, Chantiers & Entretien",
    "05 — Stagionalità e meteo": "05 — Saisonnalité & Météo",
    "06 — Sicurezza": "06 — Sécurité",
    "07 — Provvisioning": "07 — Avitaillement",
    "08 — Portolano degli ancoraggi": "08 — Guide des mouillages",
    "08 — Ancoraggi": "08 — Guide des mouillages",
    "09 — Artigiani e negozi nautici": "09 — Artisans & Shipchandlers",
    "09 — Artigiani nautici": "09 — Artisans & Shipchandlers",
    "10 — Ristoranti": "10 — Restaurants",
    "Tutti gli ancoraggi": "Tous les mouillages",
    "Tutti i ristoranti": "Tous les restaurants",
    "00 Indice": "00 Index",
    "Iscriviti": "S’inscrire",
    "Accedi": "Se connecter",
}

# For top-level markdown files with custom content we add full-file translations
TOPLEVEL_TRANSLATIONS = {
    "00-indice.md": None, # handled via generic workflow but we add specific block later if needed
}

def translate_content(orig_text, filepath):
    # Title handling first line
    lines = orig_text.split("\n")
    if lines and lines[0].startswith("# "):
        fname = os.path.basename(filepath)
        if fname in TITLE_MAP:
            lines[0] = TITLE_MAP[fname]
        orig_text = "\n".join(lines)

    # Protect segments: placeholders for things NOT to translate
    placeholders = {}
    ph_counter = 0
    def make_ph(val):
        nonlocal ph_counter
        key = f"__PH{ph_counter}__"
        ph_counter += 1
        placeholders[key] = val
        return key

    # Protect markdown link URLs first via custom handling for link text translation
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    def link_trans(m):
        inner = m.group(1)
        url = m.group(2)
        # translate inner using LINK_TEXT_MAP and later generic replacements will cover rest
        for it, fr in LINK_TEXT_MAP.items():
            if it in inner:
                inner = inner.replace(it, fr)
        # Place placeholder for URL to avoid translating it
        url_ph = make_ph(url)
        # Keep link structure but with placeholder URL; inner will be further translated by generic pass
        # We store mapping: we'll need to restore URL placeholder later
        # Use special marker
        return f"[{inner}]({url_ph})"
    orig_text = link_pattern.sub(link_trans, orig_text)

    # Protect markdown code spans FIRST (so URLs inside backticks are not double-processed and don't create huge placeholders)
    orig_text = re.sub(r'`[^`]+`', lambda m: make_ph(m.group(0)), orig_text)

    # Protect HTML tags, coordinates, anchors, ranks etc
    orig_text = re.sub(r'<div[^>]*>', lambda m: make_ph(m.group(0)), orig_text)
    orig_text = re.sub(r'</div>', lambda m: make_ph(m.group(0)), orig_text)
    orig_text = re.sub(r'\d+°\d+[′\']?[\d″"]*\s*[NSEW]', lambda m: make_ph(m.group(0)), orig_text)
    orig_text = re.sub(r'data-[a-z]+="[^"]*"', lambda m: make_ph(m.group(0)), orig_text)
    orig_text = re.sub(r"data-[a-z]+='[^']*'", lambda m: make_ph(m.group(0)), orig_text)
    orig_text = re.sub(r'https?://[^\s\)\]]+', lambda m: make_ph(m.group(0)), orig_text)
    orig_text = re.sub(r'\{#anc-[^}]+\}', lambda m: make_ph(m.group(0)), orig_text)
    orig_text = re.sub(r'★+', lambda m: make_ph(m.group(0)), orig_text)
    # Protect WGS84 marker
    orig_text = re.sub(r'WGS84', lambda m: make_ph(m.group(0)), orig_text)
    # Protect GPX/ZIP filenames
    orig_text = re.sub(r'gpx/[^\s\)\]]+', lambda m: make_ph(m.group(0)), orig_text)
    orig_text = re.sub(r'zip/[^\s\)\]]+', lambda m: make_ph(m.group(0)), orig_text)
    # Protect coordinates decimals
    orig_text = re.sub(r'\d+\.\d+°?[NSEW]', lambda m: make_ph(m.group(0)), orig_text)

    # Now apply phrase replacements sorted by length desc
    sorted_repls = sorted(REPLACEMENTS, key=lambda x: len(x[0]), reverse=True)
    for it, fr in sorted_repls:
        if it in orig_text:
            orig_text = orig_text.replace(it, fr)

    # Additional regex word-level replacements for common leftovers, careful with boundaries
    extra = [
        (r'\bStato\b', 'État'),
        (r'\bValuta\b', 'Devise'),
        (r'\bvaluta\b', 'devise'),
        (r'\bFuso\b', 'Fuseau horaire'),
        (r'\bLingua ufficiale\b', 'Langue officielle'),
        (r'\bLingua\b', 'Langue'),
        (r'\bSchengen\b', 'Schengen'),
        (r'\bRada\b', 'Rade'),
        (r'\bBaia\b', 'Baie'),
        (r'\bPorto\b', 'Port'),
        (r'\bMarina\b', 'Marina'),
        (r'\bFaro\b', 'Phare'),
        (r'\bMolo\b', 'Jetée'),
        (r'\bPontile\b', 'Ponton'),
        (r'\bBoa\b', 'Bouée'),
        (r'\bAliseo\b', 'Alizé'),
        (r'\bAlisei\b', 'Alizés'),
        (r'\bCarta d\'identità\b', 'Carte d’identité'),
        (r'\bCarta d’identità\b', 'Carte d’identité'),
        (r'\bPassaporto valido\b', 'Passeport valide'),
        (r'\bSoggiorno\b', 'Séjour'),
        (r'\bPermanenza\b', 'Séjour'),
        (r'\bNessun visto\b', 'Pas de visa'),
        (r'\bNon richiesto\b', 'Non requis'),
        (r'\bVerificare su\b', 'Vérifier sur'),
        (r'\bverificare su\b', 'vérifier sur'),
        (r'\bda verificare su\b', 'à vérifier sur'),
        (r'\bda verificare\b', 'à vérifier'),
        (r'\bDa verificare\b', 'À vérifier'),
        (r'\bverificare sempre col plotter\b', 'toujours vérifier avec le traceur'),
        (r'\bVerificare\b', 'Vérifier'),
        (r'\bCartina di dettaglio — zoom ± fino alla baia\b', 'Carte détaillée — zoomez jusqu’à la baie'),
        (r'\bmappa offline\b', 'carte hors ligne'),
        (r'\bcoordinate WGS84 indicative\b', 'coordonnées WGS84 approximatives'),
        (r'\bTutti gli ancoraggi\b', 'Tous les mouillages'),
        (r'\bTutti i ristoranti\b', 'Tous les restaurants'),
        (r'\bIn preparazione\b', 'En préparation'),
        (r'\bNessun punto inventato\b', 'Aucun point inventé'),
    ]
    for pat, repl in extra:
        orig_text = re.sub(pat, repl, orig_text)

    # Fix restoration of placeholders - longest first
    for key in sorted(placeholders.keys(), key=len, reverse=True):
        orig_text = orig_text.replace(key, placeholders[key])

    # Post fixes
    orig_text = orig_text.replace("DONNÉE MANQUANTE — **DONNÉE MANQUANTE**", "DONNÉE MANQUANTE")
    # Ensure Dernière mise à jour capitalisation okay
    # Remove double spaces artefacts
    # Translate remaining "Ultimo aggiornamento:" if missed due to case (already handled)
    # Ensure Italian leftovers like "DATO MANCANTE" not present (should be replaced)

    # Special handling for top-level files that are mostly prose: translate a few more generic Italian phrases remaining
    # Translate generic Italian prose fragments if still present (fallback)
    generic_fallback = [
        ("Scegli il mare da esplorare", "Choisissez la mer à explorer"),
        ("dentro ogni area trovi i gruppi di isole", "dans chaque zone vous trouverez les groupes d’îles"),
        ("poi la singola isola con ingresso, clearance, costi, ancoraggi e ristoranti", "puis l’île concernée avec entrée, formalités, coûts, mouillages et restaurants"),
        ("Ogni paese segue lo stesso schema", "Chaque pays suit le même schéma"),
        ("per confrontare mele con mele", "pour comparer à périmètre constant"),
        ("Benvenuto a bordo", "Bienvenue à bord"),
        ("due modi per usare la wiki", "deux façons d’utiliser le wiki"),
        ("Questa wiki è nata da velisti per velisti", "Ce wiki est né de marins pour des marins"),
        ("per condividere ciò che vorremmo trovare entrando in una rada nuova", "pour partager ce que nous aimerions trouver en entrant dans une nouvelle rade"),
        ("Puoi usarla liberamente, senza iscriverti, senza limiti e senza pubblicità", "Vous pouvez l’utiliser librement, sans inscription, sans limites et sans publicité"),
        ("sfoglia le schede, confronta i porti, scarica le mappe e i waypoint, stampa ciò che ti serve", "parcourez les fiches, comparez les ports, téléchargez les cartes et les waypoints, imprimez ce dont vous avez besoin"),
        ("È e resterà così", "Il en est et restera ainsi"),
        ("L’iscrizione serve solo se lo desideri, per due motivi", "L’inscription n’est utile que si vous le souhaitez, pour deux raisons"),
        ("Ricevere gli alert che contano", "Recevoir les alertes qui comptent"),
        ("solo se li scegli", "uniquement si vous les choisissez"),
        ("criticità di sicurezza", "criticités de sécurité"),
        ("avvisi importanti", "avis importants"),
        ("aggiornamenti meteo generali", "mises à jour météo générales"),
        ("per le aree che segui", "pour les zones que vous suivez"),
        ("Una mail solo quando serve, mai spam", "Un e-mail uniquement quand c’est nécessaire, jamais de spam"),
        ("Senza iscrizione non ricevi nulla, ma continui a navigare tutto il portolano", "Sans inscription vous ne recevez rien, mais vous continuez à consulter tout le routier"),
        ("Contribuire al portolano", "Contribuer au routier"),
        ("se sei stato sul posto e vuoi aggiungere un prezzo verificato", "si vous êtes allé sur place et souhaitez ajouter un prix vérifié"),
        ("una boa nuova o una dritta utile", "une nouvelle bouée ou une astuce utile"),
        ("con l’account puoi proporre l’aggiornamento a tuo nome", "avec un compte vous pouvez proposer la mise à jour à votre nom"),
        ("tracciato e moderato", "tracée et modérée"),
        ("In breve", "En bref"),
        ("senza iscrizione leggi tutto", "sans inscription vous lisez tout"),
        ("con l’iscrizione, se vuoi, resti aggiornato e aiuti gli altri", "avec l’inscription, si vous le souhaitez, vous restez informé et vous aidez les autres"),
        ("La scelta è tua, in un click", "Le choix vous appartient, en un clic"),
        ("Download offline per paese", "Téléchargement hors ligne par pays"),
        ("ogni paese è scaricabile in", "chaque pays est téléchargeable en"),
        ("waypoint", "waypoints"),
        ("per OpenCPN/Navionics", "pour OpenCPN/Navionics"),
        ("trovi il tasto", "vous trouverez le bouton"),
        ("accanto al nome del paese nella barra laterale sinistra", "à côté du nom du pays dans la barre latérale gauche"),
        ("e dentro ogni pagina", "et dans chaque page"),
        ("Guida completa in", "Guide complet dans"),
        ("Iscriviti o entra senza iscriverti — scegli tu", "Inscrivez-vous ou consultez sans vous inscrire — à vous de choisir"),
        ("il portolano è", "le routier est"),
        ("sempre consultabile gratis senza account", "toujours consultable gratuitement sans compte"),
        ("Se vuoi, puoi", "Si vous le souhaitez, vous pouvez"),
        ("per ricevere gli allert di sicurezza", "pour recevoir les alertes de sécurité"),
        ("per le tue aree, 1 mail solo quando serve", "pour vos zones, 1 e-mail uniquement quand nécessaire"),
        ("per contribuire", "pour contribuer"),
        ("Senza iscrizione va benissimo lo stesso", "Sans inscription c’est très bien aussi"),
        ("L'intero sistema viene aggiornato con periodicità mensile", "L’ensemble du système est mis à jour mensuellement"),
        ("Metodo", "Méthode"),
        ("ogni informazione porta rank di attendibilità + data + fonte", "chaque information porte un rang de fiabilité + date + source"),
        ("quando disponibile", "lorsque disponible"),
        ("Wiki assolutamente libera — nessuna iscrizione richiesta", "Wiki entièrement gratuit — aucune inscription requise"),
        ("Puoi navigare l’intero portolano, consultare tutte le schede, scaricare mappe e file", "Vous pouvez parcourir l’ensemble du routier, consulter toutes les fiches, télécharger les cartes et fichiers"),
        ("e usare il sito offline", "et utiliser le site hors ligne"),
        ("senza creare alcun account e senza alcun pagamento", "sans créer de compte et sans aucun paiement"),
    ]
    for it, fr in generic_fallback:
        if it in orig_text:
            orig_text = orig_text.replace(it, fr)

    return orig_text

def process_all():
    total = 0
    for root, dirs, files in os.walk(IT_ROOT):
        for f in files:
            if not f.endswith(".md"):
                continue
            it_path = pathlib.Path(root) / f
            rel = it_path.relative_to(IT_ROOT)
            fr_path = FR_ROOT / rel
            fr_path.parent.mkdir(parents=True, exist_ok=True)
            text = it_path.read_text(encoding="utf-8")
            translated = translate_content(text, str(it_path))
            fr_path.write_text(translated, encoding="utf-8")
            total += 1
            if total % 200 == 0:
                print(f"  ... {total} fichiers")
    return total

if __name__ == "__main__":
    print(f"IT_ROOT {IT_ROOT} FR_ROOT {FR_ROOT}")
    cnt = process_all()
    print(f"Traduits {cnt} fichiers")

    # Vérification
    it_c = sum(1 for _ in IT_ROOT.rglob("*.md"))
    fr_c = sum(1 for _ in FR_ROOT.rglob("*.md"))
    print(f"Counts: it={it_c} fr={fr_c} {'OK' if it_c==fr_c else 'MISMATCH'}")
    # check remaining Italian markers in FR
    import subprocess, shlex
    # quick grep for leftover DATO MANCANTE
    leftover = sum(1 for p in FR_ROOT.rglob("*.md") if "DATO MANCANTE" in p.read_text(encoding="utf-8", errors="ignore"))
    print(f"Fichiers FR contenant encore 'DATO MANCANTE': {leftover} (devrait être 0)")
    ultimo = sum(1 for p in FR_ROOT.rglob("*.md") if "Ultimo aggiornamento" in p.read_text(encoding="utf-8", errors="ignore"))
    print(f"'Ultimo aggiornamento' restant: {ultimo} (devrait être 0)")
