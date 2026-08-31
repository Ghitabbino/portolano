# Offline & GPX — Descarga por país y guía de waypoints

**Última verificación: 28/08/2026**

## 📥 Descarga sin conexión por país — ZIP + GPX

Cada país tiene su **ZIP** local con todos los archivos del derrotero + waypoints **GPX WGS84** para tu plotter. Descárgalo antes de salir y llévalo a bordo: funciona sin internet.

| Qué descargas | Dónde encontrarlo | Contenido |
|---|---|---|
| **ZIP país** | En cada página `08-fondeaderos` → botón `⬇️ ZIP país` + `⬇️ GPX` · o `zip/<país>.zip` y `gpx/<país>.gpx` | 11 archivos `00-10` + fichas `anc-*`/`rist-*` + `gpx/<país>.gpx` + `README.txt` |
| **Waypoints GPX** | `gpx/<país>.gpx` (también dentro del ZIP) | Todos los fondeaderos verificados del país, datum **WGS84**, `<sym>Anchor</sym>` |

> Los archivos ZIP/GPX se regeneran en cada build del derrotero. Coordenadas siempre **en el agua** en la rada (nunca en tierra), verificadas en satélite. Ver también `08-fondeaderos` de cada país para los botones de descarga directa.

## 🧭 Cómo cargar waypoints en tu plotter

### OpenCPN (PC / Mac / Raspberry, gratuito)

1. Descarga `gpx/<país>.gpx` o `zip/<país>.zip` (extrae el `.gpx`).
2. Abre **OpenCPN → Route & Mark Manager → Import GPX** (o arrastra el archivo sobre la carta).
3. Los waypoints aparecen como **anclas amarillas** con nombre y descripción `anc-*`. Puedes crear una ruta: selecciona waypoints → `Create Route`.
4. Transfiere al plotter/tablet si hace falta (ej. vía **OpenCPN → Export** o copia el GPX a SD).

### Navionics Boating (iOS / Android)

1. En tu teléfono/tablet descarga `gpx/<país>.gpx` (o extrae del ZIP).
2. Abre **Navionics → Menú → Rutas y Tracks → Importar GPX / Importar archivo** → selecciona el GPX.
3. Los waypoints aparecen en la carta. Navionics importa `name`/`desc`/`sym=Anchor` — ideal para planificar la entrada en rada.
4. **Consejo**: guarda el GPX en la carpeta `Navionics` para reimportarlo sin conexión en navegación.

### Otros plotters (Garmin, B&G, Raymarine, Expedition)

- Todos leen **GPX 1.1**: importa vía **tarjeta SD / USB** o vía **Garmin ActiveCaptain / B&G Link**. Si el plotter espera `rte` en vez de `wpt`, usa el GPX tal cual (los waypoints ya son `<wpt>`) o convierte con **GPSBabel** (`gpsbabel -i gpx -o gpx -f in.gpx -F out.gpx`).

### ⚠️ Advertencia

Las coordenadas son **indicativas** (WGS84, rada aproximada, no punto preciso). Verifica siempre con **carta oficial + sonda + observación visual** antes de fondear. Ver disclaimer en la home.

Última actualización: 28/08/2026
