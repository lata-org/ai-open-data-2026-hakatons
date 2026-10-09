import mk658 from '../data/mk658.json';
import novadi from '../data/novadi.json';
import ogre from '../data/profili/ogres-novads.json';
import cesis from '../data/profili/cesu-novads.json';

export type Statuss = 'pilns' | 'dalejs' | 'ierobezots' | 'nav' | 'nav_vertets';
export interface Vertejums { statuss: Statuss; kur: string; lpp: string; piezime: string }
export type Profils = typeof ogre;

export const profili: Record<string, Profils> = {
  'ogres-novads': ogre,
  'cesu-novads': cesis as unknown as Profils,
};

export const punkti = mk658.punkti;
export const statusi = mk658.statusi as Record<Statuss, { nosaukums: string; isais: string; punkti: number }>;
export const MAX_PUNKTI = mk658.punkti.length * 2;

export function kopsavilkums(p: Profils) {
  const a = p.atbilstiba as Record<string, Vertejums>;
  const skaiti = { pilns: 0, dalejs: 0, ierobezots: 0, nav: 0, nav_vertets: 0 } as Record<Statuss, number>;
  let summa = 0;
  for (const pk of punkti) {
    const v = a[pk.id];
    const s: Statuss = v?.statuss ?? 'nav_vertets';
    skaiti[s]++;
    summa += statusi[s].punkti;
  }
  return {
    skaiti,
    ir: skaiti.pilns + skaiti.dalejs + skaiti.ierobezots,
    publiski: skaiti.pilns,
    punkti: summa,
    max: MAX_PUNKTI,
    procenti: Math.round((summa / MAX_PUNKTI) * 100),
    kopa: punkti.length,
  };
}

export function ikona(s: Statuss) {
  return { pilns: '✔', dalejs: '◐', ierobezots: '🔒', nav: '✖', nav_vertets: '?' }[s];
}

export function novadsPecSluga(slug: string) {
  return novadi.find((n) => n.slug === slug);
}

export const prototipi = novadi.filter((n) => n.prototips);

export function fmt(n: number | null | undefined, opts: Intl.NumberFormatOptions = {}) {
  if (n === null || n === undefined) return '—';
  return new Intl.NumberFormat('lv-LV', { maximumFractionDigits: 1, ...opts }).format(n);
}

export function datums(iso: string) {
  const [y, m, d] = iso.split('-');
  return d ? `${d}.${m}.${y}.` : m ? `${m}.${y}.` : y;
}
