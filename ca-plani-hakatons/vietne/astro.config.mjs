// @ts-check
import { defineConfig } from 'astro/config';

// Statiska vietne (SSG). Pamatceļš var tikt mainīts izvietošanas laikā.
export default defineConfig({
  site: 'https://ca-plani.example.lv',
  trailingSlash: 'always',
  build: { format: 'directory' },
  markdown: {
    // Plānu teksti satur HTML (<mark>, <sup>, <br>) — atļaujam.
    shikiConfig: { theme: 'github-light' },
  },
});
