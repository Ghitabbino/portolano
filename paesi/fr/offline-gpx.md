# Offline & GPX — Téléchargement par pays et guide waypoints

**Dernière vérification: 28/08/2026**

## 📥 Téléchargement hors ligne par pays — ZIP + GPX

Chaque pays dispose de son **ZIP** local avec tous les fichiers du routier + waypoints **GPX WGS84** pour votre traceur. Téléchargez-le avant le départ et gardez-le à bord: il fonctionne sans internet.

| Ce que vous téléchargez | Où le trouver | Contenu |
|---|---|---|
| **ZIP pays** | Sur chaque page `08-mouillages` → bouton `⬇️ ZIP pays` + `⬇️ GPX` · ou `zip/<pays>.zip` et `gpx/<pays>.gpx` | 11 fichiers `00-10` + fiches `anc-*`/`rist-*` + `gpx/<pays>.gpx` + `README.txt` |
| **Waypoints GPX** | `gpx/<pays>.gpx` (aussi dans le ZIP) | Tous les mouillages vérifiés du pays, datum **WGS84**, `<sym>Anchor</sym>` |

> Les fichiers ZIP/GPX sont régénérés à chaque build du routier. Coordonnées toujours **en mer** dans la rade (jamais à terre), vérifiées sur satellite. Voir aussi `08-mouillages` de chaque pays pour les boutons de téléchargement direct.

## 🧭 Comment charger les waypoints sur votre traceur

### OpenCPN (PC / Mac / Raspberry, gratuit)

1. Téléchargez `gpx/<pays>.gpx` ou `zip/<pays>.zip` (extrayez le `.gpx`).
2. Ouvrez **OpenCPN → Route & Mark Manager → Import GPX** (ou glissez le fichier sur la carte).
3. Les waypoints apparaissent comme **ancres jaunes** avec nom et description `anc-*`. Vous pouvez créer une route: sélectionnez les waypoints → `Create Route`.
4. Transférez vers traceur/tablette si besoin (ex. via **OpenCPN → Export** ou copie du GPX sur SD).

### Navionics Boating (iOS / Android)

1. Sur votre téléphone/tablette téléchargez `gpx/<pays>.gpx` (ou extrayez du ZIP).
2. Ouvrez **Navionics → Menu → Routes & Traces → Importer GPX / Importer fichier** → sélectionnez le GPX.
3. Les waypoints apparaissent sur la carte. Navionics importe `name`/`desc`/`sym=Anchor` — idéal pour planifier l’entrée en rade.
4. **Astuce**: gardez le GPX dans le dossier `Navionics` pour le réimporter hors ligne en navigation.

### Autres traceurs (Garmin, B&G, Raymarine, Expedition)

- Tous lisent **GPX 1.1**: importez via **carte SD / USB** ou via **Garmin ActiveCaptain / B&G Link**. Si le traceur attend `rte` au lieu de `wpt`, utilisez le GPX tel quel (les waypoints sont déjà `<wpt>`) ou convertissez avec **GPSBabel** (`gpsbabel -i gpx -o gpx -f in.gpx -F out.gpx`).

### ⚠️ Avertissement

Les coordonnées sont **indicatives** (WGS84, rade approximative, pas un point précis). Vérifiez toujours avec **carte officielle + sondeur + observation visuelle** avant de mouiller. Voir disclaimer en page d’accueil.

Dernière mise à jour: 28/08/2026
