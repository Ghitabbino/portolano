# ⛵ AMEL Super Maramu 2000 — Wiki tecnica

## Struttura

| Percorso | Contenuto |
|---|---|
| `wiki.html` | **Wiki navigabile nel browser** (doppio clic; sidebar + ricerca) |
| `wiki/` | Sorgenti markdown della wiki, indicizzati da `wiki/00-indice.md` |
| `fonti/testo-estratto/` | Testo estratto dai PDF originali (riferimento citabile) |
| `tools/build_wiki_html.py` | Rigenera `wiki.html` dai markdown |
| PDF originali | Restano in `~/Documenti/Giovanni/Nautica/ProgettoBarca/` |

## Rigenerare wiki.html

Dopo ogni modifica ai markdown:

```bash
python3 amel-super-maramu/tools/build_wiki_html.py
```

## Come consultare

Partire da `amel-super-maramu/wiki/00-indice.md`. Pagine chiave:
- Manutenzione programmata → `wiki/13-manutenzione-programmata.md`
- Guasto/imprevisto → `wiki/14-guasti-diagnostica.md`
- Lavori su un componente → pagina dedicata (es. bow thruster = `06`)

## Come aggiungere nuovi manuali

1. Trascina il PDF (o testo) nella chat di opencode.
2. Il testo viene estratto in `fonti/testo-estratto/`.
3. Le pagine wiki vengono aggiornate o create; l'indice e la tabella fonti vengono tenuti allineati.

Nota: i documenti in lingue diverse vengono confrontati tra loro per validare dati e procedure.
