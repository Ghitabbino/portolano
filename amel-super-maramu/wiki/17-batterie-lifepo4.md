# 17 — Rifitto batterie LiFePO4 nel vano originale

**Ultima verifica: 21/08/2026**

## Misure del vano batterie (config 1+8)

Fonte: [supermaramu2000.com/battery_compartment_space.html](https://supermaramu2000.com/battery_compartment_space.html) (s/y NIKIMAT #289, misurazioni dirette ★★★)

| Quota | Valore |
|---|---|
| Lunghezza totale | **~162 cm** |
| Larghezza | 39 cm (si restringe a **33,5 cm** vicino al connettore batterie) |
| Altezza utile a prua | **23 cm** (31 cm meno 8 cm di piano in legno) |
| Altezza utile a poppa | **21 cm** (25 cm meno 4 cm di piano) |

⚠️ Il piano di appoggio in legno è disomogeneo: prua 8 cm, poppiera 4 cm → l'altezza disponibile NON è uniforme lungo il vano.

## Vincoli fisici per le LiFePO4

| Vincolo | Conseguenza |
|---|---|
| Altezza ≤ 210 mm solo a poppiera, ≥ 218 mm solo a prua/media | Batterie alte 215–218 mm vanno messe nella metà prua/media |
| Larghezza min 33,5 cm | Una sola fila di batterie larghe ≤ 330 mm; niente doppia fila con modelli standard |
| Limite parallelo BMS | La maggior parte dei produttori consente **max 4 batterie identiche in parallelo** → il teorico 1.200 Ah (12 mini) non è configurabile in garanzia |
| ⚠️ Victron Smart 12,8 V (270 mm di altezza; 200Ah = 232 mm) | **NON entrano** nel vano → escluse |

## Configurazione massimale consigliata — 600 Ah servizio

**3 × 12V 200Ah LiFePO4** (es. Redodo/LiTime standard, ingombro ~533×208×216 mm):

| Check | Calcolo | Esito |
|---|---|---|
| Lunghezza | 3 × 533 = 1.599 mm ≤ 1.620 | ✅ (giusto di 2 cm: poli superiori, ok) |
| Larghezza | 208 ≤ 335 | ✅ |
| Altezza | 216 ≤ 230 (prua/media) | ✅ ma ❌ a poppiera (210) → disporre tutte in zona prua/media |
| Parallelo | 3 ≤ 4 | ✅ |

- **Capacità servizio: 600 Ah @ 12 V ≈ 7,7 kWh utilizzabili (~6,2 kWh al 80% DoD)**
- Peso banco: ~62 kg (contro ~240 kg delle 8 al piombo originali)
- ⚠️ Avviamento: nel vano non rimane spazio → mantenere la batteria di avviamento nella sua posizione dedicata (AGM o LiFePO4 dual-purpose/marine cranking)
- Nota: 1.599 su 1.620 mm è al limite — **misurare sul posto prima dell'acquisto**; in alternativa 2×200Ah + 1×100Ah Mini (vedi sotto)

### Configurazione alternativa "tutto nel vano" — 500 Ah
2 × 200Ah (prua) + 2 × 100Ah Mini 260×156×208 mm (poppiera, dove entrano solo batterie basse):
- Lunghezza: 1.066 + 520 = 1.586 mm ✅ · una delle Mini può fare da **avviamento** (versione dual-purpose)
- Servizio 500 Ah ≈ 6,4 kWh + avviamento dedicato

## Marche e costi (prezzi promo 2026, variabili ★★)

| Prodotto | Dimensioni | Prezzo indicativo | Fonte |
|---|---|---|---|
| Redodo 12V 200Ah (BMS 100 A, IP65) | 533×208×216, 20,8 kg | **~315–350 €** (promo $339.99; listino $699) | redodopower.com ago 2026 ★★★ |
| LiTime 12V 200Ah (BMS 100 A) | 522×240×218 | **~400–460 €** ($439.99 promo; 4-pack $1.707) | litime.com ago 2026 ★★★ |
| LiTime 12V 200Ah **Plus** (BMS 200 A) | idem | ~370 € in DE (idealo) / $1.024 USA | idealo.de ★★★ |
| LiTime/Redodo 12V 100Ah Mini | 260×156×208, ~8,2 kg | ~180–250 € | siti ufficiali ★★★ |
| Renogy 12V 200Ah | — | ~$950 (sconsigliato rapporto prezzo) | ufinebattery feb 2026 ★★★ |

### Budget stimato

| Config | Componenti | Costo |
|---|---|---|
| **Max potenza** | 3 × 200Ah Redodo/LiTime | **~1.000–1.300 €** |
| Equilibrata | 2 × 200Ah + 2 × 100Ah Mini | ~1.150–1.400 € |
| Premium (BMS 200 A, alta corrente) | 3 × 200Ah Plus | ~1.200–1.600 € |

## ⚠️ Lavori collegati obbligatori (non negoziabili)

1. **Caricatore 220 V**: riprofilare/sostituire per curva LiFePO4 (14,2–14,6 V assorbimento, float 13,5 V) — il caricatore Amel originale è per piombo
2. **Alternatore**: regolazione LiFePO4 (regolatore esterno tipo Balmar/Wakespeed o DC-DC) per evitare surriscaldamento con assorbimento iniziale elevato
3. **Protezioni**: fusibile principale ridimensionato + sezionatore; cavi verificati per corrente maggiore
4. **Bassa temperatura**: in navigazione nord le LiFePO4 standard non si caricano sotto 0 °C → preferire versioni self-heating/low-temp se si naviga fuori dai tropici
5. **Monitor**: shunt/battery monitor (Victron SmartShunt o simile) — le LiFePO4 non sono leggibili col densimetro/tensione semplice

## Fonti

- Misure vano: supermaramu2000.com (NIKIMAT #289) ★★★
- Dimensioni/prezzi batterie: schede tecniche Redodo e LiTime, idealo.de (ago 2026) ★★★
- Limiti parallelo: manuali LiTime/Redodo (max 4P) ★★★
