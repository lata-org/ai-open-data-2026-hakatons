// Sagatavo vietnes saturu no projekta datiem:
//  1) markdown/<slug>/*.md  ->  src/content/plani/<slug>--<fails>.md (iztīrīts, ar lpp. enkuriem)
//  2) avoti/patvertnes/*.geojson -> public/dati/<slug>/*.geojson (filtrēti pa novadiem)
// Palaist: pnpm sagatavot
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const PROJ = join(ROOT, '..'); // civilas-aizsardzibas-plani/
const OUT_MD = join(ROOT, 'src/content/plani');
const OUT_DATI = join(ROOT, 'public/dati');

const novadi = JSON.parse(readFileSync(join(ROOT, 'src/data/novadi.json'), 'utf8'));

rmSync(OUT_MD, { recursive: true, force: true });
// Astro satura kešs jāizmet, citādi vecie ieraksti paliek datu krātuvē
rmSync(join(ROOT, 'node_modules/.astro'), { recursive: true, force: true });
rmSync(join(ROOT, '.astro'), { recursive: true, force: true });
mkdirSync(OUT_MD, { recursive: true });
mkdirSync(OUT_DATI, { recursive: true });

function parseFrontmatter(txt) {
  const m = txt.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!m) return { meta: {}, body: txt };
  const meta = {};
  for (const line of m[1].split(/\r?\n/)) {
    const mm = line.match(/^([a-z_]+):\s*(.*)$/);
    if (mm) meta[mm[1]] = mm[2];
  }
  return { meta, body: txt.slice(m[0].length) };
}

function tirit(body, virsrakstaRinda) {
  let t = body;
  // lpp. marķieri -> enkuri
  t = t.replace(/<!--\s*lpp\.\s*(\d+)\s*-->/g, (_, n) => `<span class="lpp" id="lpp-${n}" data-lpp="${n}" aria-label="${n}. lappuse"></span>`);
  // vizuālo elementu marķieri -> vietturi
  t = t.replace(/^>\s*\*\*\[VIZUĀLI ELEMENTI lpp\. (\d+):([^\]]*)\]\*\*\s*$/gm,
    (_, n, apr) => `<div class="vietturis vietturis--attels" data-lpp="${n}"><span class="vietturis__ikona">▧</span><div><strong>Vizuāls elements oriģinālā (lpp. ${n})</strong><br><small>${apr.trim().replace(/—.*$/, '').trim()}. Interaktīvajā versijā šeit paredzēta karte, shēma vai diagramma no atvērtajiem datiem.</small></div></div>`);
  // atkārtotā galvene
  if (virsrakstaRinda) t = t.split('\n').filter((l) => l.trim() !== virsrakstaRinda).join('\n');
  // vēru atsauču numuri virsrakstos (<sup>8</sup>) — noņemam, lai satura rādītājs ir tīrs
  t = t.replace(/^(#+ .*?)(<sup>[^<]*<\/sup>)+\s*$/gm, '$1');
  // izcēlumi no PDF (dzeltenie marķieri) — noņemam
  t = t.replace(/<\/?mark>/g, '');
  // trīs un vairāk tukšas rindas -> divas
  t = t.replace(/\n{3,}/g, '\n\n');
  return t;
}

let skaits = 0;
for (const n of novadi) {
  if (!n.prototips) continue;
  const dir = join(PROJ, 'markdown', n.slug);
  for (const f of n.faili) {
    const src = join(dir, f.fails);
    if (!existsSync(src)) { console.warn('TRŪKST', src); continue; }
    const { meta, body } = parseFrontmatter(readFileSync(src, 'utf8'));
    const clean = tirit(body, f.galvene);
    const fm = [
      '---',
      `novads: ${n.slug}`,
      `fails: ${f.fails}`,
      `loma: ${f.loma}`,
      `virsraksts: ${JSON.stringify(f.virsraksts)}`,
      meta.lpp ? `lpp: ${meta.lpp}` : null,
      meta.avota_url ? `avota_url: ${JSON.stringify(meta.avota_url)}` : null,
      meta.originals ? `originals: ${JSON.stringify(meta.originals)}` : null,
      '---', '',
    ].filter((x) => x !== null).join('\n');
    const outName = `${n.slug}--${f.fails.replace(/\.md$/, '')}.md`;
    writeFileSync(join(OUT_MD, outName), fm + clean, 'utf8');
    skaits++;
  }

  // ģeodati
  const outDir = join(OUT_DATI, n.slug);
  mkdirSync(outDir, { recursive: true });
  const visas = JSON.parse(readFileSync(join(PROJ, 'avoti/patvertnes/patvertnes_latvija_112.geojson'), 'utf8').replace(/^\uFEFF/, ''));
  const re = new RegExp(n.patvertnu_filtrs);
  const savas = visas.features.filter((ft) => re.test(ft.properties.pilsetasvaiapdzvietasnosaukums || ''));
  const kompakts = {
    type: 'FeatureCollection',
    features: savas.map((ft) => ({
      type: 'Feature',
      geometry: ft.geometry,
      properties: {
        vieta: ft.properties.pilsetasvaiapdzvietasnosaukums,
        iela: ft.properties.ielasnosaukums,
        nr: ft.properties.ekasnumurs,
        veids: ft.properties.ekasgalvlietosanasveids,
        komentars: ft.properties.komentars,
      },
    })),
  };
  writeFileSync(join(outDir, 'patvertnes.geojson'), JSON.stringify(kompakts), 'utf8');
  console.log(n.slug, 'patvertnes:', savas.length);

  if (n.robeza_fails) {
    const r = join(PROJ, 'avoti/patvertnes', n.robeza_fails);
    if (existsSync(r)) writeFileSync(join(outDir, 'robeza.geojson'), readFileSync(r, 'utf8').replace(/^\uFEFF/, ''), 'utf8');
  }
}
console.log('Sagatavoti', skaits, 'plānu faili ->', OUT_MD);
