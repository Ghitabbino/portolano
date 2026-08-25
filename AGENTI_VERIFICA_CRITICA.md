# 🚨 PROTOCOLLO VERIFICA CRITICA v2 — istruzioni permanenti per l'agente

> Leggi questo file ALL'INIZIO di ogni sessione. Il valore sta nel rispetto di
> budget, prove e formati. Ultimo aggiornamento: 25/08/2026

## 0. Avvio e revisione allerte esistenti (SEMPRE, prima delle ricerche)

```bash
python3 tools/verifica_critica.py        # coda paesi scaduti (>15 gg), batch max 5
```

Poi, per OGNI paese del batch:
- cerca banner 🚨/⚠️ già presenti nei suoi file (grep `ALLERTA|AGGIORNAMENTO`)
- **scadenze**: banner L3 più vecchio di 30 gg o L2 più vecchio di 90 gg →
  ri-verificalo PRIMA di tutto (1 query). Se non confermato → **rimuovi/retrocedi**
  l'allerta e annotalo nel changelog. Un allarme stantio è un danno quanto uno mancato.

## 1. Severità: tre livelli, prove diverse

| Livello | Cosa | Prova MINIMA richiesta | Durata |
|---|---|---|---|
| **L3 🚨 ALLERTA** (banner in cima al paese + sezione) | minaccia vita/libertà: violenza armata mirata ai velisti, guerra/rivolta, uragano in rotta, chiusura confini, deportazione/arresti per pratiche comuni | **2 fonti indipendenti**, almeno 1 ufficiale ★★★★+, evento <90 gg | rivalida a 30 gg |
| **L2 ⚠️ AVVISO** (blocco nella sezione interessata) | trend crimini contro yacht, nuova sanzione/divieto, cambio visti/tariffe | **1 fonte credibile ★★★+** (es. rapporto 1ª mano CSSN) senza smentite | rivalida a 90 gg |
| **L1 aggiornamento silenzioso** | tariffe, numeri, date | qualsiasi fonte ≥★★ | — |

Regola anti-allarmismo: **un solo resoconto anonimo ≠ allerta**. Diventa BOZZA
(segnalata all'utente, mai pubblicata come banner).

## 2. Budget rigido PER PAESE (~15 min totali, hard stop)

| # | Aspetto | Query base (EN) | Note |
|---|---------|-----------------|------|
| 0 | Allerte esistenti | grep locale + 1 query se scadute | sempre |
| 1 | Sicurezza | `[paese] sailors yachts safety security incident 2026` | CSSN, Noonsite, advisory |
| 2 | Meteo/stagione | solo se in stagione (Atl: giu–nov; Pac: mag–nov) `[area] hurricane outlook [mese]` | NOAA/CSU/RCC |
| 3 | Ingresso/permanenza | `[paese] entry requirements yacht days allowed 2026` | immigrazione ufficiale |
| 4 | Tariffe | `[paese] cruising permit clearance fees 2026` | dogane/marine |
| 5 | **Normativa & legalità AMPIA** | `[paese] drug laws foreigners enforcement 2026` · `[paese] new fines regulations yachts fishing anchoring 2026` | vedi sotto |

**Aspetto 5 copre (NON solo pesca)** — ogni cambio di legge O DI APPLICAZIONE che
trasforma una pratica comune in reato/sanzione:
stupefacenti (cannabis "tollerata"→reato, residui, CBD) · alcol · pesca/MPA ·
droni/armi/farmaci · abbigliamento/comportamenti/coprifuoco · ancoraggio/permessi comarca.
**REGOLA CHIAVE**: il cambio di APPLICAZIONE conta quanto il cambio di legge.

**Query extra in lingua locale (obbligatoria quando rilevante, +1 query)**:
| Area | Lingua | Pattern |
|---|---|---|
| Panama, Centroam., Colombia, Venezuela | ES | `[zona] seguridad turistas velices [año]` · `[zona] nueva regulación multa` |
| Antille francesi, Med FR | FR | `[zone] sécurité plaisance avis [année]` · `nouvelle réglementation amende` |
| ABC | NL/EN | `[eiland] zeilers veiligheid` |
| Capo Verde, Brasile | PT | `[país] segurança velejadores multa` |
| Canarie, Spagna | ES | come ES |

**STOP**: 3–4 risultati letti per query → decidi. 15 min paese → prossimo.
**Vietato**: forum infiniti, video, social, link fuori lista senza motivo concreto.
**VIETO COPY-PASTE**: mai riportare testo letterale da Noonsite/gov/altre fonti —
riformulare sempre in italiano originale; citare solo fonte (nome, data, rank).

## 3. Date e recency

- Oggi = data di sistema. Eventi >12 mesi NON generano allerte (restano come storia
  nelle sezioni se già presenti).
- "Recente" per L3/L2 = <90 giorni salvo trend continuativo documentato.
- Se trovi una data FUTURA nei file del paese durante l'editing → segnalala (errore dati).

## 4. Formati fissi

Banner L3 (subito dopo la prima riga `# NN — …` di `00-ingresso-visti.md`):

```
> ### 🚨 ALLERTA [GG/MM/AAAA]
> [Fatto in una frase.] [Conseguenza pratica per il velista.]
> Fonti: [nome ★rank, data] · [nome ★rank, data] · Verificato da agente il [GG/MM/AAAA]
> Rivalutazione prevista entro il [GG/MM/AAAA]
```

Blocco L2 (in testa alla sezione interessata):
```
> ⚠️ **[Titolo]** ([data fonte]) — [fatto + conseguenza]. Fonte: [nome ★rank].
> Verificato da agente il [GG/MM/AAAA].
```

Changelog (append a `paesi/controllo/changelog-critico.md`):

```
## [AAAA-MM-GG] [paese]
- [L1|L2|L3] [aspetto] [variazione / nessuna variazione / rimossa allerta scaduta]
  — fonti: [nome ★rank, data] — azione: [auto/bozza]
```

## 5. Chiusura paese e sessione

```bash
python3 tools/verifica_critica.py --segna [paese]
```

Riporta all'utente: paesi fatti, L3/L2 inserite o rimosse, bozze da verificare,
coda rimasta. POI fermati — non estendere il batch senza ordine esplicito.
