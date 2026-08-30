# Offline & GPX — Country Download & Waypoint Guide

**Last checked: 28/08/2026**

## 📥 Offline Download Per Country — ZIP + GPX

Every country has its own local **ZIP** with all pilot files + **GPX WGS84** waypoints for your plotter. Download it before departure and keep it aboard: it works without internet.

| What You Download | Where to Find It | Contents |
|---|---|---|
| **Country ZIP** | On every `08-anchorages` page → `⬇️ Country ZIP` + `⬇️ GPX` button · or `zip/<country>.zip` and `gpx/<country>.gpx` | 11 files `00-10` + `anc-*`/`rist-*` sheets + `gpx/<country>.gpx` + `README.txt` |
| **GPX waypoints** | `gpx/<country>.gpx` (also inside the ZIP) | All verified anchorages for the country, datum **WGS84**, `<sym>Anchor</sym>` |

> ZIP/GPX files are regenerated at every pilot build. Coordinates are always **in the water** in the roadstead (never ashore), verified on satellite imagery. See also each country’s `08-anchorages` for direct download buttons.

## 🧭 How to Load Waypoints on Your Plotter

### OpenCPN (PC / Mac / Raspberry, free)

1. Download `gpx/<country>.gpx` or `zip/<country>.zip` (extract the `.gpx`).
2. Open **OpenCPN → Route & Mark Manager → Import GPX** (or drag the file onto the chart).
3. Waypoints appear as **yellow anchors** with name and description `anc-*`. You can create a route: select waypoints → `Create Route`.
4. Transfer to plotter/tablet if needed (e.g., via **OpenCPN → Export** or copy the GPX to SD).

### Navionics Boating (iOS / Android)

1. On your phone/tablet download `gpx/<country>.gpx` (or extract from the ZIP).
2. Open **Navionics → Menu → Routes & Tracks → Import GPX / Import File** → select the GPX.
3. Waypoints appear on the chart. Navionics imports `name`/`desc`/`sym=Anchor` — ideal for planning the approach into the roadstead.
4. **Tip**: keep the GPX in the `Navionics` folder to re-import offline while underway.

### Other Plotters (Garmin, B&G, Raymarine, Expedition)

- All read **GPX 1.1**: import the file via **SD card / USB** or via **Garmin ActiveCaptain / B&G Link**. If the plotter expects `rte` instead of `wpt`, use the GPX as is (waypoints are already `<wpt>`) or convert with **GPSBabel** (`gpsbabel -i gpx -o gpx -f in.gpx -F out.gpx`).

### ⚠️ Warning

Coordinates are **indicative** (WGS84, approximate roadstead, not a precise fix). Always verify with **official chart + sounder + visual observation** before anchoring. See disclaimer on the home page.

Last updated: 28/08/2026
