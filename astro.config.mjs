// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// Korean is the default language and lives at the root; English is at /en/.
const ROUTES = ['', 'research', 'publications', 'team', 'news', 'history', 'radar', 'ideas', 'join'];

// The site shipped with Korean under /ko/ before the languages were swapped.
// Keep those URLs alive — Astro emits a meta-refresh page per entry in a
// static build, so old links and any search index still land correctly.
const legacyKoreanRedirects = Object.fromEntries(
  ROUTES.map((r) => [`/ko/${r}`.replace(/\/$/, '') || '/ko', `/${r}`.replace(/\/$/, '') || '/'])
);

export default defineConfig({
  site: 'https://www.connectomelab.com',
  base: '/',
  i18n: {
    defaultLocale: 'ko',
    locales: ['ko', 'en'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  redirects: {
    ...legacyKoreanRedirects,
    '/ko': '/',
  },
  integrations: [
    react(),
    tailwind({
      applyBaseStyles: false,
    }),
    sitemap(),
  ],
});
