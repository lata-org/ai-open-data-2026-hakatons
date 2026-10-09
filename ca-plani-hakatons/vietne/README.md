# Civilās aizsardzības plānu vietne (Astro prototips)

Statiska vietne, kas apkopo Latvijas pašvaldību civilās aizsardzības plānus: sākumlapā — salīdzinājums pēc MK noteikumu Nr. 658 obligātajām prasībām, katram novadam — pārskats (kartes, tabulas, diagrammas), analīze un pilns plāna teksts.

Prototipā izvērsti **Ogres novads** un **Cēsu novads**.

## Palaišana

```bash
pnpm install            # node-linker=hoisted (E: disks ir exFAT, simboliskās saites nedarbojas)
pnpm sagatavot          # sagatavo plānu tekstus un ģeodatus no ../markdown un ../avoti
pnpm dev                # http://localhost:4321
pnpm build              # dist/
```

## Struktūra

| Ceļš | Saturs |
|---|---|
| `src/data/mk658.json` | MK 658 4.1.–4.9. un 5.1.–5.4. punkti, statusi un punktu sistēma |
| `src/data/novadi.json` | 42 pašvaldību reģistrs (ģenerēts no `../pasvaldibas.csv` un `../darba_saraksts.json`); lauks `prototips`, `faili`, `patvertnu_filtrs` |
| `src/data/profili/<slug>.json` | Novada profils: plāna metadati, teritorija, riski, evakuācijas vietas ar koordinātēm, komisija, atbilstības vērtējums, secinājumi |
| `src/data/atvertie-dati.json` | Atvērto datu kopu katalogs ar statusu (pieslēgts / vietturis) |
| `scripts/sagatavot.mjs` | Kopē un iztīra `../markdown/<slug>/*.md` → `src/content/plani/`, filtrē patvertnes → `public/dati/<slug>/` |
| `src/pages/index.astro` | Sākumlapa: salīdzinājums un reģistrs |
| `src/pages/novads/[slug]/index.astro` | Pārskats (lasāmā versija) |
| `src/pages/novads/[slug]/analize.astro` | Atbilstība pa elementiem, salīdzinājums, secinājumi |
| `src/pages/novads/[slug]/plans.astro` | Pilns plāna teksts ar satura rādītāju un lpp. marķieriem |
| `src/pages/metodika.astro` | Vērtēšanas metodika |

## Kā pievienot nākamo novadu

1. `src/data/novadi.json` — ierakstam iestatīt `prototips: true`, `faili` (kuri Markdown faili un kāda loma), `patvertnu_filtrs`, pēc iespējas `robeza_fails`.
2. Izveidot `src/data/profili/<slug>.json` pēc Ogres/Cēsu parauga (atbilstības vērtējums 13 punktiem, teritorijas vienības, riski, evakuācijas vietas).
3. `pnpm sagatavot && pnpm build`.

Piezīme: plānu Markdown frontmatter lauks pašvaldības kodam saucas `novads`, nevis `slug` — Astro glob ielādētājs lauku `slug` izmanto kā ieraksta ID un faili pārrakstītu cits citu.

Vietturi (`<Vietturis>`) iezīmē vietas, kur pieslēdzami atvērtie dati (LVĢMC plūdu WMS, CSP režģis, VVD objekti, LVC ceļi) vai kur plāna dati nav publicēti.
