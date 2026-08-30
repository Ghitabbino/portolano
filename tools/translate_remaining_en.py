#!/usr/bin/env python3
"""
Translate remaining IT -> EN via local Ollama qwen2.5:7b-instruct
Preserves URLs, anchors, coordinates, HTML, stars via placeholders.
Enforces title mapping, DATO MANCANTE->DATA MISSING, link text translated but targets preserved.
"""
import pathlib, re, requests, json, os, time, sys

ROOT = pathlib.Path(__file__).parent.parent
IT_ROOT = ROOT / "paesi" / "it"
EN_ROOT = ROOT / "paesi" / "en"

# For root files source is paesi/*.md (IT) not paesi/it
ROOT_FILES = ["trasparenza.md", "ringraziamenti.md", "merch.md", "chi-siamo.md"]

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

# Valid EN toponyms prompt
SYSTEM = """You are a professional nautical translator from Italian to native English (British nautical English, as used in pilot books / Reeds / Imray).

Translate the following markdown from IT to EN.

MANDATORY RULES — must follow exactly:
1. Titles per filename (first line):
   00-ingresso-visti.md → "# 00 — Entry, Documents & Visas"
   01-clearance.md → "# 01 — Yacht Customs Clearance"
   02-costi.md → "# 02 — Cost of Living"
   03-porti-ancoraggi.md → "# 03 — Ports & Marinas"
   04-servizi-cantieri.md → "# 04 — Services, Boatyards & Maintenance"
   05-stagionalita-meteo.md → "# 05 — Seasonality & Weather"
   06-sicurezza.md → "# 06 — Safety & Security"
   07-provvisioning.md → "# 07 — Provisioning"
   08-ancoraggi.md → "# 08 — Anchorage Pilot"
   09-artigiani-nautici.md → "# 09 — Marine Trades & Chandlers"
   10-ristoranti.md → "# 10 — Restaurants"
   For anc-*, rist-*, keep the proper name but translate description.
2. DATO MANCANTE must become DATA MISSING (exact uppercase, bold **DATA MISSING** stays bold).
3. Ultimo aggiornamento → Last updated ; Ultima verifica → Last checked ; Da verificare → To be verified (or To verify)
4. DO NOT translate placeholders like __PH0__, __URL0__, __COORD0__. Leave them exactly as is; they will be restored later.
5. Use correct English toponyms: Canary Islands (never Canaries/Canarie), Cape Verde, Lucayan Archipelago, Greater Antilles, Lesser Antilles, Leeward Islands, Windward Islands, Western Basin / Central Basin / Eastern Basin (Mediterranean), North Africa.
6. Nautical glossary: Alisei=Trade winds, Aliseo=Trade wind, Maestrale=Mistral, Scirocco=Sirocco, Grecale=Gregale, Libeccio=Libeccio, rada=roadstead, boa=mooring buoy, molo=pier/quay, pontile=pontoon, faro=lighthouse, ancora=anchor, fondale=seabed, tenuta=holding, traversata=passage/crossing, ormeggio=berth, cantiere=boatyard, carena=hull/bottom, alaggio=haul-out, varo=launch, cambusa=galley provisions, banchina=quayside.
7. Keep units: kn, °C, m, etc. Keep numbers.
8. Do not invent: if IT says DATA MISSING, keep DATA MISSING; never fill with fake prices.
9. Natural fluent English, not literal word-for-word.
10. Output ONLY the translated markdown, no extra notes, no introduction.
"""

# Section headings mapping for post-correction (to ensure consistent English)
SECTION_FIXES = {
    "Alimentari e spesa di bordo": "Groceries & Galley Provisioning",
    "Mangiare fuori (media)": "Eating Out (Average)",
    "Mangiare fuori": "Eating Out",
    "Carburanti": "Fuel",
    "Trasporti e collegamenti": "Transport & Connections",
    "Servizi quotidiani": "Everyday Services",
    "Contanti e pagamenti": "Cash & Payments",
    "Approfondimenti": "Further Reading",
    "Distanze utili": "Useful Distances",
    "Avviso entro le 12 miglia": "Notice within 12 Miles",
    "Bandiera Q": "Q Flag",
    "Armi": "Weapons",
    "Documenti da tenere pronti": "Documents to Have Ready",
    "Chi deve farla": "Who Must Clear",
    "Procedura d'ingresso": "Entry Procedure",
    "Procedura": "Procedure",
    "Punti agréé": "Authorised Ports",
    "Valutazione sicurezza": "Safety Rating",
    "Quadro generale": "General Overview",
    "Numeri di emergenza": "Emergency Numbers",
    "Clima": "Climate",
    "Venti locali": "Local Winds",
    "Finestre tipiche": "Typical Weather Windows",
    "Checklist àncora": "Anchor Checklist",
    "Regole generali di ancoraggio": "General Anchorage Rules",
    "Tabella riassuntiva": "Summary Table",
    "Mappa generale": "General Chart",
    "Cartografia ufficiale": "Official Charts",
}

def protect_placeholders(text):
    """Replace URLs, html, coordinates, anchors, stars with placeholders."""
    placeholders = {}
    counter = 0
    def new_ph(val):
        nonlocal counter
        k = f"__PH{counter}__"
        counter += 1
        placeholders[k] = val
        return k

    # Protect HTML divs first (contain other patterns)
    text = re.sub(r'<div[^>]*>', lambda m: new_ph(m.group(0)), text)
    text = re.sub(r'</div>', lambda m: new_ph(m.group(0)), text)
    # Protect data- attributes
    text = re.sub(r'data-[a-z\-]+=(?:"[^"]*"|\'[^\']*\')', lambda m: new_ph(m.group(0)), text)
    # Protect anchor IDs {#...}
    text = re.sub(r'\{#anc-[^}]+\}', lambda m: new_ph(m.group(0)), text)
    # Protect markdown link URL part: [text](url) -> [text](__PH__)
    # We need to keep link text translatable, but protect URL
    # Replace URL inside parentheses with placeholder, keep outer brackets for translation
    def link_url_protect(m):
        inner = m.group(1)
        url = m.group(2)
        ph = new_ph(url)
        # store as __PH__ but we need to allow model to see placeholder token
        return f"[{inner}]({ph})"
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_url_protect, text)
    # Protect bare URLs http
    text = re.sub(r'https?://[^\s\)\]\"]+', lambda m: new_ph(m.group(0)), text)
    # Protect coordinates like 14°28'32" N or 14°28.5'N etc.
    text = re.sub(r'\d+°\s*\d+[\'′]?\s*(\d+["″])?\s*[NSEW]', lambda m: new_ph(m.group(0)), text)
    text = re.sub(r'\d+°\d+\.\d+\'\s*[NSEW]', lambda m: new_ph(m.group(0)), text)
    # Protect star ratings
    text = re.sub(r'★+', lambda m: new_ph(m.group(0)), text)
    # Protect bold DATA MISSING placeholder as well? Keep it translatable but ensure not broken
    return text, placeholders

def restore_placeholders(text, placeholders):
    # Restore longest first to avoid nested issues
    for k in sorted(placeholders.keys(), key=len, reverse=True):
        text = text.replace(k, placeholders[k])
    return text

def translate_via_ollama(content, filepath, retries=2):
    protected, ph = protect_placeholders(content)
    # Ensure first line title is handled after; but let model translate rest, then force title
    payload_prompt = f"{SYSTEM}\n\n--- Filename: {os.path.basename(filepath)} ---\n--- IT markdown with placeholders ---\n{protected}\n\n--- EN markdown with same placeholders ---\n"
    payload = {
        "model": "qwen2.5:7b-instruct",
        "prompt": payload_prompt,
        "stream": False,
        "options": {"temperature": 0.12, "num_ctx": 8192, "num_predict": 4096}
    }
    for attempt in range(retries+1):
        try:
            r = requests.post("http://127.0.0.1:11434/api/generate", json=payload, timeout=180)
            r.raise_for_status()
            resp = r.json().get("response", "")
            # Ollama may add ```markdown fences, strip them
            resp = resp.strip()
            if resp.startswith("```"):
                resp = re.sub(r'^```[a-z]*\n?', '', resp)
                resp = re.sub(r'\n```$', '', resp)
            # Restore placeholders
            resp = restore_placeholders(resp, ph)
            # Force title mapping if applicable
            fname = os.path.basename(filepath)
            if fname in TITLE_MAP:
                lines = resp.split("\n")
                if lines and lines[0].startswith("# "):
                    lines[0] = TITLE_MAP[fname]
                    resp = "\n".join(lines)
                else:
                    # prepend title if model removed it
                    if not resp.lstrip().startswith("# "):
                        resp = TITLE_MAP[fname] + "\n\n" + resp
            # Post-fix sections
            for it, en in SECTION_FIXES.items():
                resp = resp.replace(it, en)
            # Ensure DATO MANCANTE never remains (if model left it)
            resp = resp.replace("DATO MANCANTE", "DATA MISSING")
            resp = resp.replace("Dato mancante", "DATA MISSING")
            # Fix common Italian remnants that model may have missed due to placeholder confusion
            # Ensure Last updated line is English
            resp = resp.replace("Ultimo aggiornamento", "Last updated")
            resp = resp.replace("Ultima verifica", "Last checked")
            # Ensure link targets were restored and not translated: check for common corruption like "10-restaurants.md" -> revert to "10-ristoranti.md"
            # If file had original IT link target, and model translated it, we restore by re-inserting original URLs from ph mapping
            # Since we protected URLs, they should be intact, but model might still have translated link TEXT which is desired. However it might have introduced new translated filename in text not as URL.
            # We already protected URLs, so fine.
            # Ensure DATA MISSING bold
            resp = resp.replace("**DATA MISSING**", "**DATA MISSING**")
            # Nautical fixes that model often gets wrong
            resp = resp.replace("Alize", "Trade wind")
            resp = resp.replace("Alizé", "Trade wind")
            resp = resp.replace("Alizes", "Trade winds")
            resp = resp.replace("Barge fuel", "Dockside diesel")
            resp = resp.replace("barge fuel", "dockside diesel")
            resp = resp.replace("Food and onboard expenses", "Groceries & Galley Provisioning")
            resp = resp.replace("Fuel (Adriatic Sea)", "Fuel (Adriatic)")
            # Fix incorrect link text for 03/10 that model may have corrupted with wrong filename style
            # Keep original filenames Italian: ensure .md links keep original Italian filenames (from placeholders, should be okay)
            return resp
        except Exception as e:
            print(f"Attempt {attempt} failed for {filepath}: {e}", file=sys.stderr)
            if attempt == retries:
                raise
            time.sleep(2)
    return None

def get_requested_sources():
    # Use the /tmp/final_untranslated.txt if exists, else generate from requested folders
    candidates_file = pathlib.Path("/tmp/final_untranslated.txt")
    if candidates_file.exists():
        lines = [l.strip() for l in candidates_file.read_text().splitlines() if l.strip()]
        # Convert paesi/en/... to paesi/it/...
        it_files = []
        for en_path in lines:
            it_path = en_path.replace("paesi/en/", "paesi/it/", 1)
            # Only if it_path exists
            if pathlib.Path(it_path).exists():
                it_files.append(it_path)
            else:
                # maybe en_path was already it_path style?
                if pathlib.Path(en_path).exists() and "paesi/it" in en_path:
                    it_files.append(en_path)
        return sorted(set(it_files))
    # fallback: enumerate requested folders
    requested = ['grenadine','haiti','honduras','israele','italia','libano','libia','madeira','malta','marocco','martinica','monaco','montenegro','montserrat','nicaragua','panama','porto-rico','repubblica-dominicana','saba','saint-barth','saint-martin','santa-lucia','siria','slovenia','spagna','st-eustatius','st-kitts-nevis','trinidad-tobago','tunisia','turchia','turks-caicos','venezuela','virgin-islands']
    files = []
    for r in requested:
        base = IT_ROOT / r
        if not base.exists():
            print(f"Skip missing {base}")
            continue
        for p in base.rglob("*.md"):
            files.append(str(p))
    return sorted(files)

def translate_root_files():
    # paesi/*.md source (IT) -> paesi/en/*.md
    for fname in ROOT_FILES:
        src_candidates = [ROOT / "paesi" / fname, ROOT / "paesi" / "it" / fname]
        src = None
        for c in src_candidates:
            if c.exists():
                src = c
                break
        if not src:
            print(f"Root src missing for {fname}, skipping")
            continue
        dst = EN_ROOT / fname
        # Special handling: trasparenza and ringraziamenti are missing in EN, need to create
        if dst.exists():
            # Check if need re-translation: if contains Italian markers, re-translate
            content = dst.read_text(encoding="utf-8")
            if "Ultimo aggiornamento" in content or "DATO MANCANTE" in content or "Trasparenza" in content:
                print(f"Re-translating root {fname} (still IT)")
            else:
                # For merch, chi-siamo already EN, skip unless forced
                if fname in ["merch.md", "chi-siamo.md"]:
                    print(f"Root {fname} already EN, skipping")
                    continue
        text = src.read_text(encoding="utf-8")
        print(f"Translating root {src} -> {dst}")
        translated = translate_via_ollama(text, str(src))
        if translated:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(translated, encoding="utf-8")
            print(f"  -> done {dst}")

def main():
    sources = get_requested_sources()
    print(f"Found {len(sources)} files to translate (requested folders)")
    # Add root missing files handling separately
    # Translate batch
    success = 0
    failed = []
    start = time.time()
    for idx, it_path in enumerate(sources, 1):
        en_path = pathlib.Path(it_path.replace("paesi/it/", "paesi/en/"))
        # Skip if EN already correctly translated? But our list is already untranslated, so translate all
        text = pathlib.Path(it_path).read_text(encoding="utf-8")
        try:
            translated = translate_via_ollama(text, it_path)
            en_path.parent.mkdir(parents=True, exist_ok=True)
            en_path.write_text(translated, encoding="utf-8")
            success += 1
            print(f"[{idx}/{len(sources)}] OK {en_path}")
            # Small delay to avoid overload
            # time.sleep(0.2)
            # Periodic progress
            if idx % 50 == 0:
                elapsed = time.time() - start
                print(f"Progress {idx}/{len(sources)} elapsed {elapsed/60:.1f} min")
        except Exception as e:
            print(f"[{idx}/{len(sources)}] FAIL {it_path}: {e}", file=sys.stderr)
            failed.append(it_path)
    print(f"Done: success {success}/{len(sources)}, failed {len(failed)}")
    if failed:
        print("Failed:", failed)
    # Also handle root files
    translate_root_files()
    # Verification: count
    for d in ['grenadine','haiti','honduras','israele','italia','libano','libia','madeira','malta','marocco','martinica','monaco','montenegro','montserrat','nicaragua','panama','porto-rico','repubblica-dominicana','saba','saint-barth','saint-martin','santa-lucia','siria','slovenia','spagna','st-eustatius','st-kitts-nevis','trinidad-tobago','tunisia','turchia','turks-caicos','venezuela','virgin-islands']:
        it_c = sum(1 for _ in (IT_ROOT/d).rglob("*.md")) if (IT_ROOT/d).exists() else 0
        en_c = sum(1 for _ in (EN_ROOT/d).rglob("*.md")) if (EN_ROOT/d).exists() else 0
        print(f"{d}: it={it_c} en={en_c} {'OK' if it_c==en_c else 'MISMATCH'}")

if __name__ == "__main__":
    main()
