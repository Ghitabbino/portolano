# Offline & GPX — Download je Land & Wegpunkt-Anleitung

**Letzte Prüfung: 28/08/2026**

## 📥 Offline-Download je Land — ZIP + GPX

Jedes Land hat sein eigenes **ZIP** mit allen Handbuch-Dateien + **GPX WGS84**-Wegpunkten für deinen Plotter. Lade es vor dem Auslaufen herunter und behalte es an Bord: es funktioniert ohne Internet.

| Was du lädst | Wo du es findest | Inhalt |
|---|---|---|
| **Land-ZIP** | Auf jeder Seite `08-Ankerplätze` → Button `⬇️ ZIP Land` + `⬇️ GPX` · oder `zip/<land>.zip` und `gpx/<land>.gpx` | 11 Dateien `00-10` + Blätter `anc-*`/`rist-*` + `gpx/<land>.gpx` + `README.txt` |
| **GPX-Wegpunkte** | `gpx/<land>.gpx` (auch im ZIP) | Alle verifizierten Ankerplätze des Landes, Datum **WGS84**, `<sym>Anchor</sym>` |

> ZIP/GPX-Dateien werden bei jedem Build neu erzeugt. Koordinaten immer **im Wasser** in der Reede (nie an Land), auf Satellit verifiziert. Siehe auch `08-Ankerplätze` jedes Landes für direkte Download-Buttons.

## 🧭 Wie du Wegpunkte auf den Plotter lädst

### OpenCPN (PC / Mac / Raspberry, kostenlos)

1. Lade `gpx/<land>.gpx` oder `zip/<land>.zip` (entpacke `.gpx`).
2. Öffne **OpenCPN → Route & Mark Manager → Import GPX** (oder ziehe die Datei auf die Karte).
3. Wegpunkte erscheinen als **gelbe Anker** mit Name und Beschreibung `anc-*`. Du kannst eine Route erstellen: Wegpunkte wählen → `Create Route`.
4. Bei Bedarf auf Plotter/Tablet übertragen (z. B. via **OpenCPN → Export** oder GPX auf SD kopieren).

### Navionics Boating (iOS / Android)

1. Auf Handy/Tablet `gpx/<land>.gpx` laden (oder aus ZIP entpacken).
2. Öffne **Navionics → Menü → Routen & Tracks → GPX importieren / Datei importieren** → GPX wählen.
3. Wegpunkte erscheinen auf der Karte. Navionics importiert `name`/`desc`/`sym=Anchor` — ideal zur Ansteuerung der Reede.
4. **Tipp**: GPX im `Navionics`-Ordner behalten, um offline erneut zu importieren.

### Andere Plotter (Garmin, B&G, Raymarine, Expedition)

- Alle lesen **GPX 1.1**: Import via **SD-Karte / USB** oder via **Garmin ActiveCaptain / B&G Link**. Erwartet der Plotter `rte` statt `wpt`, nutze das GPX wie es ist (Wegpunkte sind bereits `<wpt>`) oder konvertiere mit **GPSBabel** (`gpsbabel -i gpx -o gpx -f in.gpx -F out.gpx`).

### ⚠️ Warnung

Koordinaten sind **indikativ** (WGS84, ungefähre Reede, kein Präzisionspunkt). Immer mit **offizieller Karte + Lot + Sichtbeobachtung** vor dem Ankern prüfen. Siehe Disclaimer auf der Startseite.

Letzte Aktualisierung: 28/08/2026
