/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Warm paper ground — the "bright museum"
        paper: '#FAF9F6',
        ink: {
          DEFAULT: '#1C1917',
          soft: '#44403C',
          faint: '#78716C',
        },
        // Single cool accent, inherited from the lab's cyan identity
        lab: {
          50: '#ECFEFF',
          100: '#CFFAFE',
          600: '#0891B2',
          700: '#0E7490',
          800: '#155E75',
          900: '#164E63',
        },
        // The one dark "projection room" band (3D viewer)
        deep: {
          DEFAULT: '#0B1220',
          soft: '#111A2E',
          line: '#1E2A44',
        },
        line: '#E7E5E4',
      },
      fontFamily: {
        display: ['Hahmlet', 'Noto Serif KR', 'Georgia', 'serif'],
        sans: ['Pretendard Variable', 'Pretendard', 'Noto Sans KR', 'system-ui', '-apple-system', 'sans-serif'],
        // IBM Plex Mono carries no Hangul, so any Korean inside a mono context
        // used to fall through to whatever the OS offered — on Linux that was
        // Noto Sans Mono CJK *JP*, a Japanese face setting Korean text.
        // Pretendard is already loaded for body copy, so naming it here routes
        // Hangul to a real Korean face at zero additional payload while Latin
        // and numerals stay in Plex Mono.
        mono: ['IBM Plex Mono', 'Pretendard Variable', 'Pretendard', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [require('@tailwindcss/typography'), require('tailwindcss-animate')],
};
