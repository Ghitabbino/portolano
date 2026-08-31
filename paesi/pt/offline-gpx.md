# Offline & GPX — Download por país e guia de waypoints

**Última verificação: 28/08/2026**

## 📥 Download offline por país — ZIP + GPX

Cada país tem o seu **ZIP** local com todos os ficheiros do roteiro + waypoints **GPX WGS84** para o teu plotter. Descarrega antes de largar e mantém a bordo: funciona sem internet.

| O que descarregas | Onde encontrar | Conteúdo |
|---|---|---|
| **ZIP país** | Em cada página `08-fundeadouros` → botão `⬇️ ZIP país` + `⬇️ GPX` · ou `zip/<país>.zip` e `gpx/<país>.gpx` | 11 ficheiros `00-10` + fichas `anc-*`/`rist-*` + `gpx/<país>.gpx` + `README.txt` |
| **Waypoints GPX** | `gpx/<país>.gpx` (também dentro do ZIP) | Todos os fundeadouros verificados do país, datum **WGS84**, `<sym>Anchor</sym>` |

> Os ficheiros ZIP/GPX são regenerados a cada build do roteiro. Coordenadas sempre **na água** na enseada (nunca em terra), verificadas em satélite. Vê também `08-fundeadouros` de cada país para os botões de download direto.

## 🧭 Como carregar waypoints no teu plotter

### OpenCPN (PC / Mac / Raspberry, gratuito)

1. Descarrega `gpx/<país>.gpx` ou `zip/<país>.zip` (extrai o `.gpx`).
2. Abre **OpenCPN → Route & Mark Manager → Import GPX** (ou arrasta o ficheiro para a carta).
3. Os waypoints aparecem como **âncoras amarelas** com nome e descrição `anc-*`. Podes criar uma rota: seleciona waypoints → `Create Route`.
4. Transfere para plotter/tablet se necessário (ex. via **OpenCPN → Export** ou copia o GPX para SD).

### Navionics Boating (iOS / Android)

1. No teu telefone/tablet descarrega `gpx/<país>.gpx` (ou extrai do ZIP).
2. Abre **Navionics → Menu → Rotas e Tracks → Importar GPX / Importar ficheiro** → seleciona o GPX.
3. Os waypoints aparecem na carta. O Navionics importa `name`/`desc`/`sym=Anchor` — ideal para planear a entrada na enseada.
4. **Dica**: mantém o GPX na pasta `Navionics` para reimportar offline em navegação.

### Outros plotters (Garmin, B&G, Raymarine, Expedition)

- Todos lêem **GPX 1.1**: importa via **cartão SD / USB** ou via **Garmin ActiveCaptain / B&G Link**. Se o plotter esperar `rte` em vez de `wpt`, usa o GPX como está (waypoints já são `<wpt>`) ou converte com **GPSBabel** (`gpsbabel -i gpx -o gpx -f in.gpx -F out.gpx`).

### ⚠️ Aviso

As coordenadas são **indicativas** (WGS84, enseada aproximada, não ponto preciso). Verifica sempre com **carta oficial + sonda + observação visual** antes de fundear. Vê o disclaimer na home.

Última atualização: 28/08/2026
