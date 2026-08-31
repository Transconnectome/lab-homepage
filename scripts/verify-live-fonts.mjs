// Ground-truth font verification, per HANDOFF §4/§6: getComputedStyle and
// document.fonts.check() lie about what drew Hangul — the only honest answer
// is CDP CSS.getPlatformFontsForNode, which reports the real platform family
// and glyph count per node. Run from CI (the dev container has no egress);
// certificate errors are ignored because the custom-domain cert is still
// being repaired. TARGET_BASE overrides the target (e.g. a local preview).
import { chromium } from 'playwright';

const BASE = process.env.TARGET_BASE || 'https://www.connectomelab.com';
const PAGES = ['/', '/research/'];
const BAD = /CJK JP|CJK SC|Malgun|Hiragino|Noto Sans Mono|DejaVu/i;
const HANGUL = /[가-힣]/;

const browser = await chromium.launch();
let warnings = 0;

for (const path of PAGES) {
  const ctx = await browser.newContext({
    ignoreHTTPSErrors: true,
    locale: 'ko-KR',
    viewport: { width: 1280, height: 900 },
  });
  const page = await ctx.newPage();
  const url = BASE + path;
  console.log(`\n===== ${url} =====`);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  const fontStatus = await page.evaluate(() => document.fonts.ready.then(() => document.fonts.status));
  console.log(`document.fonts.status: ${fontStatus}`);

  // Applied-CSS evidence (inputs, not rendering — rendering proof comes next)
  const css = await page.evaluate(() => {
    const h = document.querySelector('h1');
    return {
      bodyWordBreak: getComputedStyle(document.body).wordBreak,
      bodyFontFamily: getComputedStyle(document.body).fontFamily.slice(0, 60),
      h1LetterSpacing: h ? getComputedStyle(h).letterSpacing : '(no h1)',
      htmlLang: document.documentElement.lang,
    };
  });
  console.log(`applied CSS: html[lang=${css.htmlLang}] word-break=${css.bodyWordBreak} h1 letter-spacing=${css.h1LetterSpacing}`);
  console.log(`body font-family starts: ${css.bodyFontFamily}`);

  // Tag every visible element whose OWN text nodes contain Hangul
  const els = await page.evaluate(() => {
    const HANGUL = /[가-힣]/;
    const all = [...document.querySelectorAll('body *')].filter((el) => {
      const own = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join('');
      if (!HANGUL.test(own)) return false;
      try { if (el.checkVisibility && !el.checkVisibility()) return false; } catch {}
      return true;
    }).slice(0, 250);
    return all.map((el, i) => {
      el.setAttribute('data-fc', String(i));
      const cls = typeof el.className === 'string' && el.className.trim()
        ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
      const own = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join(' ');
      return { i, desc: el.tagName.toLowerCase() + cls, text: own.replace(/\s+/g, ' ').trim().slice(0, 16) };
    });
  });
  console.log(`Hangul-bearing elements found: ${els.length}`);

  const cdp = await ctx.newCDPSession(page);
  await cdp.send('DOM.enable');
  await cdp.send('CSS.enable');
  const { root } = await cdp.send('DOM.getDocument');

  const familyTotals = new Map(); // family -> { glyphs, nodes }
  const detail = [];
  for (const el of els) {
    let fonts;
    try {
      const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: `[data-fc="${el.i}"]` });
      if (!nodeId) continue;
      ({ fonts } = await cdp.send('CSS.getPlatformFontsForNode', { nodeId }));
    } catch { continue; }
    for (const f of fonts) {
      const t = familyTotals.get(f.familyName) || { glyphs: 0, nodes: 0 };
      t.glyphs += f.glyphCount; t.nodes += 1;
      familyTotals.set(f.familyName, t);
      if (BAD.test(f.familyName)) {
        warnings++;
        console.log(`WARN ${el.desc} "${el.text}" -> ${f.familyName} (${f.glyphCount} glyphs)`);
      }
    }
    if (/^h1|^h2|^h3|eyebrow|chip|nav|subtitle|display/.test(el.desc) && detail.length < 16) {
      detail.push(`  ${el.desc.padEnd(34)} "${el.text}" -> ${fonts.map((f) => `${f.familyName}:${f.glyphCount}`).join(', ')}`);
    }
  }

  console.log('-- representative elements (family:glyphs) --');
  detail.forEach((l) => console.log(l));
  const total = [...familyTotals.values()].reduce((s, t) => s + t.glyphs, 0) || 1;
  console.log('-- platform families over all Hangul-bearing nodes --');
  [...familyTotals.entries()].sort((a, b) => b[1].glyphs - a[1].glyphs)
    .forEach(([fam, t]) => console.log(`  ${fam.padEnd(28)} glyphs=${t.glyphs} (${(100 * t.glyphs / total).toFixed(1)}%) nodes=${t.nodes}`));
  await ctx.close();
}

await browser.close();
console.log(warnings > 0
  ? `\nRESULT: ${warnings} WARN line(s) — read them above; small counts on accented Latin are a glyph-coverage nit, not Hangul routing`
  : '\nRESULT: clean — no glyphs drawn by a known-bad fallback family');
