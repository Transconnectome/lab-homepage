// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.connectomelab.com',
  base: '/',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ko'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  integrations: [
    react(),
    tailwind({
      applyBaseStyles: false,
    }),
    sitemap(),
  ],
});
