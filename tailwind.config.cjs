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
          // Was #78716C — 4.56:1 on paper, which clears WCAG AA by 1.3% and
          // then carries 12-13px Korean metadata, where minimum contrast meets
          // minimum size meets Hangul's high stroke density. #57534E is 7.25:1.
          faint: '#57534E',
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
        // Option E: Muted Oxblood / Crimson accent
        oxblood: {
          DEFAULT: '#801818',
          light: '#9E2424',
          muted: '#A33838',
          soft: '#F2EFE9',
        },
      },
      fontFamily: {
        // Display resolves per glyph: MaruBuri's @font-face (global.css) is
        // limited to Hangul unicode-ranges, so Hangul lands on MaruBuri while
        // Latin skips straight to Newsreader / Hahmlet.
        display: ['MaruBuri', 'Newsreader', 'Hahmlet', 'Noto Serif KR', 'Georgia', 'serif'],
        serif: ['Newsreader', 'MaruBuri', 'Hahmlet', 'Georgia', 'serif'],
        sans: ['Pretendard Variable', 'Pretendard', 'Noto Sans KR', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['IBM Plex Mono', 'Pretendard Variable', 'Pretendard', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [require('@tailwindcss/typography'), require('tailwindcss-animate')],
};
