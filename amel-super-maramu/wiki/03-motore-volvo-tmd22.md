# 03 — Motore Volvo Penta MD22 / TMD22 / TAMD22 (workshop manual)

**Fonte:** Workshop manual "Engine Repair, Marine Engines MD22 • TMD22 • TAMD22", pubbl. 7738684-5, 04-1999 (EN)
**Varianti coperte:** MD22A, MD22L-A/B, MD22P-B, TMD22A/B/P-C, TAMD22P-B

> ⚠️ Il capitolo "Technical Data" (cilindrata, potenza, giochi assiali, pressione iniettori, termostati) NON è nell'estrazione. Verificare motore installato: la barca del Users Guide ha uno Yanmar 4JH3-HTE.

## Architettura

- 4 cilindri in linea, 2 valvole/cil., blocco ghisa **senza camicie**, testa alluminio con alzo a bicchiere + **shims**.
- Albero motore ghisa sferoidale, 5 supporti, spinta assiale su semirondelle al supporto centrale.
- Distribuzione a **cinghia dentata**; pompa iniezione **Bosch** con pulegga a due scanalature: dente "A" = aspirati, dente "B" = turbo.
- Volano: corona **104 denti**. Riduttori citati: MS25, HS25, MS2, 120S, HBW250, SX-drive.
- Turbo con wastegate **non regolabile** (se difettosa si cambia il turbo): corsa stelo 0,38 mm @ 89–97 kPa (TMD22); 1 mm @ 135 kPa (TAMD22).

## Coppie di serraggio (Nm)

| Giunto | Coppia |
|---|---|
| **Viti testa** | 50 → 100 → **+90°** (sequenza; max 4 ritorni) |
| Dadi bielle (dado sempre nuovo) | **47** |
| Viti supporti banco | **112** (a gradini) |
| Vite centrale puleggia albero (3581332) | **180** |
| Dado pulegga pompa iniezione | **60** |
| **Volano** | **65** |
| Candele preriscaldamento (grasso HT) | **20** |
| Tappo scarico coppa olio | **43** |
| Coperchio camme | 22 |
| Pulegga camme: vite centrale / mozzo | 85 / 22 |
| Tenditore cinghia (viti bombate) / folle | 45 / 43 |
| Tubi alta pressione iniettori | 18 |
| Scambiatore/marmitta alla testa | 22 |

Generale: M5=5 · M6=10 · M8=20 · M10=40 · M12=70 · M14=115. Controdadi Nylock ≥M8: −25%.

## Regolazioni

### Gioco valvole (motore freddo, camma-bicchiere)
- Aspirazione **0,25–0,35 mm** · Scarico **0,35–0,45 mm**
- Con shims calcolare per **0,30 asp / 0,40 scar**
- Sequenza camme: 1+3 → 2+5 → 6+8 → 4+7

### Cinghia distribuzione (tensimetro 885036)
- Nuova: **425–465 N** · Usata: **340–370 N**
- Se usata scende ≤ 270 N → riportare a 340–370 N; ricontrollare fase pompa dopo 2 giri

### Anticipo pompa iniezione
- Comparatore sul tappo posteriore, precarico ~3,0 mm, azzerato al PMI
- Al PMS cil.1 lettura = alzata nominale ± **0,05 mm**; correzione ruotando la pompa (orario visto da dietro = aumenta)

### Limiti usura principali
| Punto | Limite |
|---|---|
| Piano testa | deformazione > 0,10 mm = rettifica; altezza min. 119,85 mm |
| Guida valvole | gioco stelo max 0,13 mm; sporgenza 10 mm |
| Perni albero | usura/ovalizzazione max 0,03 mm; rettifica −0,3 mm |
| Cilindri | ovalizzazione max 0,15 mm; noiosura +0,50 mm (pistoni classe X) |
| Volano | eccentricità < 0,30 mm; battuto ≤ 0,03 mm ogni 25 mm raggio |
| Regime max | dall'ultimo numero targhetta pompa (es. …/3200 = 3200 rpm); vite esterna sigillata |

## Sistemi

- **Lubrificazione:** pompa rotori (10/11 denti), filtro sul corpo pompa (solo originali), valvola relief non tarabile. Filtro nuovo: riempirlo d'olio, ungere guarnizione, **serrare a mano**.
- **Raffreddamento:** circuiti chiuso+mare; scambiatore+marmitta+espansione in un'unica unità a dritta. Pompa circolazione mossa dalla **cinghia di distribuzione**. Anodo sacrificale. Inserto scambiatore estraibile se spazio ≥ 555 mm.
- **Alimentazione:** pompa membrana; gasolio dal foro nel corpo = membrana rotta. Prova: manometro 0–70 kPa, 10 s avviamento; sostituire se <75% della minima o dimezza in <30 s. Spurgo: vite sopra filtro + leva manuale, poi dadi iniettori.
- **Elettrico:** alternatore Valeo A13N147M 60 A (14 V); motorino con spazzole min 3,5 mm; candele: picco 27 A → 14 A dopo ~10 s, 11–12 V.
- **Turbo:** dopo montaggio versare 100–140 ml olio nel corpo, pre-lubrificare col motorino, primi 3–4 min a basso regime. **Mai spray di avviamento, mai senza filtro aria.**

## Diagnostica rapida

| Sintomo | Verifica |
|---|---|
| Cilindro "morto" | Allentare i dadi tubi uno a uno a minimo alto: quello che non fa variare i giri è colpevole |
| Parte e si ferma / irregolare | Aria nel bassapressione → cercare perdita, spurgo completo |
| Fumo nero + calo potenza a 2500 rpm | Wastegate tarato basso |
| Consumo olio elevato | Vetratura canne → Flex-Hone + segmenti |
| Spia carica / batteria scarica | Procedura alternatore: 14 V costanti con carico 10–15 A |
| Motorino lento, lampade brillanti | Switch/cavi/connesse, non il motorino |

## Attrezzi speciali Volvo Penta

885036 tensimetro cinghia · 885037 perni di fase · 884955 comparatore anticipo (885139 per TMD22P/TAMD22) · 885027 estrattore pulegge · 885028 chiave elettrovalvola stop.
Sigillanti: Loctite 574/572/241/243/648, Volvo 840879-1, 1161099-5, Permatex No.3/No.77. Grasso Shell Alvania R2.

## Intervalli di manutenzione

Non presenti nel workshop manual: seguire il Maintenance Schedule Volvo Penta dedicato (obbligatorio per motori certificati). Pompa iniezione e iniettori solo officina autorizzata.
