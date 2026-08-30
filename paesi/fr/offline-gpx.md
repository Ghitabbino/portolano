# Offline & GPX — Download per paese e guida waypoints

**Dernière vérification: 28/08/2026**

## 📥 Téléchargement hors ligne par pays — ZIP + GPX

Ogni paese ha il suo **ZIP locale** con tutti i file del portolano + i waypoints **GPX WGS84** per il tuo plotter. Scaricalo prima di partire e tienilo a bordo: funziona senza internet.

| Cosa scarichi | Dove lo trovi | Cosa contiene |
|---|---|---|
| **ZIP paese** | In ogni pagina `08-ancoraggi` → bottone `⬇️ ZIP paese` + `⬇️ GPX` · oppure `zip/<paese>.zip` e `gpx/<paese>.gpx` | 11 file `00-10` + schede `anc-*`/`rist-*` + `gpx/<paese>.gpx` + `README.txt` |
| **GPX waypoints** | `gpx/<paese>.gpx` (anche dentro lo ZIP) | Tous les mouillages verificati del paese, datum **WGS84**, `<sym>Anchor</sym>` |

> I file ZIP/GPX sono rigenerati a ogni build del portolano. Coordinate sempre **in mezzo al mare** nella rada (mai a terra), verificate su satellitare. Vedi anche `08-ancoraggi` di ogni paese per i bottoni di download diretti.

## 🧭 Come inserire i waypoints nel tuo cartografico

### OpenCPN (PC / Mac / Raspberry, gratuito)

1. Scarica il `gpx/<paese>.gpx` o lo `zip/<paese>.zip` (estrai il `.gpx`).
2. Apri **OpenCPN → Route & Mark Manager → Import GPX** (o trascina il file sulla mappa).
3. I waypoints appaiono come **ancore gialle** con nome e descrizione `anc-*`. Puoi creare una rotta: seleziona i waypoints → `Create Route`.
4. Trasferisci su plotter/tablet se necessario (es. via **OpenCPN → Export** o copia il GPX su SD).

### Navionics Boating (iOS / Android)

1. Sul telefono/tablet scarica il `gpx/<paese>.gpx` (o estrai dallo ZIP).
2. Apri **Navionics → Menu → Rotte & Tracce → Importa GPX / Importa file** → seleziona il GPX.
3. I waypoints compaiono sulla carta. Navionics importa `name`/`desc`/`sym=Anchor` — ideale per pianificare l'ingresso in rada.
4. **Tip**: tieni il GPX nella cartella `Navionics` per ri-importarlo offline in navigazione.

### Altri plotter (Garmin, B&G, Raymarine, Expedition)

- Tutti leggono **GPX 1.1**: importa il file via **scheda SD / USB** o via **Garmin ActiveCaptain / B&G Link**. Se il plotter richiede `rte` invece di `wpt`, usa il GPX così com'è (i waypoints sono già `<wpt>`) o convertilo con **GPSBabel** (`gpsbabel -i gpx -o gpx -f in.gpx -F out.gpx`).

### ⚠️ Avvertenza

Le coordinate sono **indicative** (WGS84, rada approssimata, non punto di precisione). Verifica sempre con **carta nautica ufficiale + scandaglio + osservazione** prima di ancorare. Vedi disclaimer in home.

Dernière mise à jour: 28/08/2026
