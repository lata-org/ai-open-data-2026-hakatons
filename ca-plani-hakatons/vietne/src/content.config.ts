import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Plānu teksti — sagatavoti ar `pnpm sagatavot` no ../markdown/<slug>/ mapes.
const plani = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/plani' }),
  schema: z.object({
    novads: z.string(),
    fails: z.string(),
    loma: z.enum(['plans', 'lemums', 'nolikums', 'protokols', 'pielikums']),
    virsraksts: z.string(),
    lpp: z.number().optional(),
    avota_url: z.string().optional(),
    originals: z.string().optional(),
  }),
});

export const collections = { plani };
