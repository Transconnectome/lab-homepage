# Handoff — SNU Connectome Lab homepage

Last updated 2026-08-26. Repo: `Transconnectome/lab-homepage`. Live at
<https://www.connectomelab.com>.

This is the operating manual for whoever picks the site up next. It covers what
the site is, how to run and change it, what is still open, and — most usefully —
the handful of non-obvious traps that cost real time to find.

---

## 1. Current state

| | |
|---|---|
| Stack | Astro 5 (static) · React islands · Tailwind 3 · three.js |
| Hosting | GitHub Pages, deployed by `.github/workflows/deploy.yml` on every push to `main` |
| Domain | `www.connectomelab.com` → CNAME → `transconnectome.github.io` |
| Languages | **Korean is the default, at the root.** English is under `/en/`. |
| Content | 33 members · 102 publications (76 peer-reviewed) · 10 news · 5 research areas · 3 history entries · 12 radar items · 9 AI ideas |
| Automation | Weekly arXiv radar + publication sync + AI ideas; news-from-issue on demand |

**One thing is not finished:** the HTTPS certificate. See §5.

### Run it locally

```bash
npm ci
npm run dev          # http://localhost:4321
npm run build && npm run preview
```

On the DGX box, tunnel the preview to your Mac:

```bash
ssh -N -L 4321:127.0.0.1:4321 dgx-spark
```

---

## 2. How the site is put together

### Languages

Korean lives at `/`, English at `/en/`. Both trees are thin wrappers over one
set of components:

```
src/pages/index.astro          -> <HomePage lang="ko" />
src/pages/en/index.astro       -> <HomePage lang="en" />
src/components/pages/*.astro   the actual pages
src/i18n/ui.ts                 every UI string, both languages
```

To add a page you write **one** component in `src/components/pages/` and **two**
wrappers. `localePath(lang, '/research')` builds language-correct links; never
hardcode a path.

Page *content* (news, research, history) is chosen by a `lang` field on each
content entry. Korean entries are `*-ko.md` files carrying `lang: "ko"` and a
`baseSlug` pointing at their English counterpart.

The site previously served Korean under `/ko/`. Those paths are kept alive as
redirects declared in `astro.config.mjs` — do not delete them.

### Content collections

`src/content/config.ts` is the schema (Zod). A build fails loudly if content
violates it, which is deliberate: the weekly automation commits generated
content, and the schema is what stops a bad record reaching the site.

### Automation

| Workflow | Trigger | What it does |
|---|---|---|
| `deploy.yml` | push to `main` | build + deploy |
| `research-radar.yml` | Mondays 09:00 KST, or manual | offline pipeline tests → arXiv scan (7 topic buckets) → Gemini summaries → publication sync → AI ideas → project metadata → **full build as a validation gate** → commit → deploy in-workflow |
| `news-submission.yml` | a `news-submission` issue | Gemini writes a bilingual news story from the submitted facts → build gate → commit → deploy → comments and closes the issue |

Both LLM workflows need the `OPENROUTER_API_KEY` repo secret (set; note that
GitHub does **not** carry secrets across a repo transfer).

`research-radar.yml` deploys **in-workflow** rather than relying on `deploy.yml`.
That is not redundancy: a push made with `GITHUB_TOKEN` does not fire workflow
triggers, so the bot's commit would otherwise build nothing.

### Adding news

Two routes, both fine:

1. **Students:** open a "📰 뉴스 제출" issue in the repo. Fill the form in
   Korean. The pipeline writes the English and Korean story and publishes it.
   Org members are published automatically; outside submissions need an
   `approved` label first.
2. **Directly:** add `src/content/news/YYYY-MM-slug.md` plus a `-ko.md`
   counterpart and push.

---

## 3. Korean typography — read before touching CSS

Korean is not Latin with different glyphs, and this site got that wrong in three
mechanical ways before 2026-08-22. The rules that fix it live in
`src/styles/global.css` with the reasons written next to them. The short version:

- **No Latin-only face may carry Hangul.** IBM Plex Mono has no Hangul, so
  Korean set in it fell through to whatever the OS offered — measured as
  `Noto Sans Mono CJK JP`, a *Japanese* face setting Korean. The mono stack now
  names Pretendard after Plex Mono; Korean *prose* uses `.mono-meta`, which
  drops to sans under `:lang(ko)` because mono word-spaces are ~2.4× too wide
  for Hangul.
- **`word-break: keep-all`** globally (plus `overflow-wrap` so DOIs still wrap).
  Without it Korean breaks mid-어절: "만들어/내는지", "뉴/로이미징".
- **No positive tracking on Hangul.** Latin caps labels want `0.18em`; Hangul
  syllable blocks scatter under it. `.eyebrow:lang(ko)` resets tracking *and*
  `text-transform` — the latter is inert on Hangul but would uppercase embedded
  Latin ("fMRI 연구" → "FMRI 연구").
- **Line length** is owned by one `.measure` class (36em). Korean wants 35–45
  syllables per line; it was running 55–68.
- Korean rules key on `:lang(ko)`, not `html[lang="ko"]`, so they also reach
  Korean fragments on English pages. Those fragments carry an explicit `lang`.

---

## 4. Traps that cost time here

Each of these produced a wrong answer that looked right.

**Ask the rendering engine, not the stylesheet.** `getComputedStyle` returns the
declared font stack, which tells you nothing about what actually drew the text,
and `document.fonts.check()` returned a false `true` for Hangul in a Latin-only
font. The ground truth is Chrome DevTools Protocol `CSS.getPlatformFontsForNode`,
which reports the real family and glyph count per node. Recipe in §6.

**Measure font payload cold, on one page.** Summing bytes across several
navigations in one browser context under-reports badly: cached responses fail to
read and get silently skipped. A first measurement this way reported 134 KB
where the truth was 768 KB. Build the comparison commit in a `git worktree` and
measure each page in a fresh context.

**`curl … | grep -q` under `set -o pipefail` reports failure on success.** grep
exits at the first match, curl dies of SIGPIPE, and pipefail marks the pipeline
failed. `scripts/cutover.sh` reported "not serving this build" while the site was
live because of exactly this. Buffer into a variable and use `[[ "$s" == *pat* ]]`.

**Don't fingerprint a build with headline copy.** Two successive versions of the
cutover check keyed on a headline string, and both went stale within a day. It
now looks for `/_astro/`, which no copy edit can invalidate.

**Repo transfers break things quietly.** Moving to the `Transconnectome` org
dropped the Actions secret, and push events stopped triggering workflows for
~2h20m with no error anywhere — `workflow_dispatch` kept working the whole time.
If a push produces no run, check
`gh api repos/<owner>/<repo>/actions/runs?head_sha=<sha>` for zero runs before
assuming a config problem.

**Several sessions have worked this repo in parallel.** Expect to rebase, and
read what the other side changed rather than resolving conflicts mechanically —
one conflict here was a marker string that the other change had already made
invalid for a reason that wasn't visible in the diff.

---

## 4b. Content invariants worth keeping green

Three checks caught real defects on 2026-08-26 and are cheap to repeat.

**Every English field must be English, every Korean field Korean.** Three ideas
had Korean in both halves (so `/en/ideas` showed Korean prose) and three older
ones had no Korean at all (so the Korean-default page showed long English
paragraphs). `validate_idea()` in `generate_research_ideas.py` now rejects a
record whose language does not match the field, using a Hangul *ratio* rather
than a boolean so an English sentence carrying a Korean proper noun still passes.

**No Hangul inside a `lang="en"` scope, and no Latin prose inside `lang="ko"`.**
A sweep found 46 violations, mostly the Lab guide (Korean-only on the whole
English tree) and radar cards (English bodies inheriting the Korean type rules).
Walk every text node and compare its Hangul content against
`el.closest('[lang]')`; the target is zero. Chips are the subtle case: `.chip` is
`font-mono`, so any chip holding Korean needed the `:lang(ko)` sans override now
in `global.css`, and chips that really do hold Latin data carry `lang="en"`.

**Author names come from OpenAlex and are sometimes the wrong person.** All six
quantum papers listed "H. Eric Tseng" or "Hua-an Tseng" where the co-author is
**Huan-Hsin Tseng** (BNL). `COAUTHOR_CANONICAL` in `sync_scholar.py` fixes that
at sync time. Separately, `name_key()` now folds hyphens and spaces, because
`Hee‐Hwan Wang` (non-breaking hyphen) failed to match member `Heehwan Wang` and
left him unhighlighted on eight of his own papers. Fixes to the matcher only
reach *new* works — existing records are kept as-is — so a matcher change needs
a one-off replay over `src/content/publications/`.

## 5. Open items

**1. HTTPS certificate — the only thing blocking a clean launch.**
State is stuck at `authorization_created`. GitHub's own domain health check
reports the domain valid, HTTPS-eligible, no CAA error, and the build is served
correctly over HTTP; so this is not a configuration problem. The most likely
explanation is a Let's Encrypt failed-validation backoff accumulated while DNS
still pointed at the previous owner's `snuconnectome.github.io`. **Do not keep
re-triggering it** — that extends the backoff. Check with:

```bash
./scripts/cutover.sh --status
```

If it has not resolved by itself, open a GitHub Support ticket; the domain
configuration is already correct and you can say so with evidence.

**1b. Korean is still missing for member education, interests and passions.**
Affiliations and alumni positions now render in Korean through
`affiliationLabel()` in `src/i18n/ui.ts`, but `education`, `researchInterests`
and `passions` are English-only in the members collection, so the Korean team
page still shows English there. They are tagged `lang="en"` so the type rules are
at least correct. Fixing it properly means Korean fields on the schema for 33
members. The radar has the same shape of gap: `scripts/update_research_radar.py`
writes English summaries only, so Korean visitors read English card bodies.

**2. Two news items were never verified.**
`2025-12-bk-silver-award` and `2025-12-neurips-neuromamba` do not appear on the
old Google Sites history page and could not be confirmed from any external
source. Confirm with the lab or remove them.

**3. Korean display typeface — decided to defer, with a real finding behind it.**
An 11-agent typography study measured that **Hahmlet's Hangul is a gothic
wearing a serif's name** (its 부리 are blunt cuts), so Korean headings lose the
editorial voice the English ones get. It also found the English homepage
downloads ~130 KB of Hangul it will never render, because of how Google Fonts
slices Hahmlet. The recommendation was to split display into *Hahmlet (Latin,
Hangul stripped) + Naver MaruBuri SemiBold (Hangul)*, self-hosted.

This was deferred because the PI chose to keep the motto in English on both
trees, so the Korean hero has no display-size Hangul. **But the research page
h1 and the card titles still are** display-size Korean — so the case is not
dead, just smaller. The full spec (measured byte budgets, licence findings,
build script) is worth re-reading before anyone acts:
`/tmp/.../tasks/wgb3ehdl3.output` is gone with the session, but the decisions
that matter are summarised here and in the commit messages `ffdb38f` and
`4d613d8`.

Licence facts from that study, if it is ever revisited: Pretendard and IBM Plex
carry an OFL **Reserved Font Name**, so subsetting and self-hosting them
requires renaming the family (loading them unmodified from a CDN, as now, does
not). MaruBuri is not OFL — it is Naver's open licence, which permits
institutional web use and subsetting *provided the copyright notice and full
licence text ship alongside*.

**4. Optional design work, ranked** — none of it blocking:
card detailing (`rounded-2xl` + lift + shadow reads as SaaS marketing on a
museum page); consolidating the ad-hoc type sizes (`text-xs` appears ~38×) onto
one scale; section rhythm (`py-16` almost everywhere makes the page read as a
list).

**5. Consider whether English visitors are well served.**
Making Korean the default means `/research` — a URL that used to be English — now
serves Korean. Anyone following an older link lands on Korean and must click
`English`. That was the accepted trade, but if inbound international traffic
matters, a language-detecting root or a visible language notice is the fix.

---

## 6. Verification recipes

**Which font actually drew this Korean text?**

```python
# playwright, chromium at /home/juke/.cache/ms-playwright/chromium-1217/chrome-linux/chrome
cdp = ctx.new_cdp_session(page); cdp.send('DOM.enable'); cdp.send('CSS.enable')
doc = cdp.send('DOM.getDocument')
nid = cdp.send('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': sel})['nodeId']
cdp.send('CSS.getPlatformFontsForNode', {'nodeId': nid})   # -> family + glyphCount
```

Pass condition for the whole site: sweep every node whose own text contains
Hangul and assert **zero** hits on any family matching `CJK JP`, `CJK SC`,
`Malgun`, `Hiragino`, `Noto Sans Mono` or `DejaVu`. Last run: 904 nodes, 0 fails.

**Did Korean break mid-word?** Select the string with a `Range` and count
`getClientRects()`; more than one rect means it split. Regression strings that
exposed the original bug: `만들어내는지`, `구축`, `뉴로이미징`, `모든`.

**Line length:** `text.length / range.getClientRects().length`. Target 35–45 for
Korean.

**Cutover / certificate:** `./scripts/cutover.sh --status`. It reports DNS
target, custom domain, HTTPS enforcement, and distinguishes "not serving this
build" from "serving, certificate not valid yet".

**Font payload:** fresh browser context per page, sum response bodies for
`.woff2` plus any third-party font CSS. Compare against a `git worktree` build
of the older commit — not against a remembered number.

---

## 7. Where things are

```
src/i18n/ui.ts                     all UI strings, both languages
src/styles/global.css              the type system, with reasons in comments
src/components/pages/              one component per page, lang-aware
src/content/                       members, publications, news, research, history, trends, ideas
scripts/sync_scholar.py            OpenAlex → publications, with kind classification and fuzzy dedup
scripts/update_research_radar.py   arXiv → radar, per-topic buckets + relevance gates
scripts/generate_research_ideas.py lab context + radar → weekly hypotheses
scripts/test_radar_buckets.py      offline tests for the radar bucket/gate logic
scripts/test_ideas_pipeline.py     offline tests for sampling, dedup, category quota
scripts/news_from_issue.py         issue form → bilingual news story
scripts/cutover.sh                 DNS/domain/certificate status and cutover
claudedocs/                        this file, plus the original evaluation
```

A principle worth keeping: everything the site claims about itself should be
true. The radar labels whether a summary came from an LLM or is an abstract
excerpt; the AI ideas page says plainly that it is machine-written and not
lab-endorsed; the lab guide is called a curated FAQ rather than an AI because
the site is static and there is no model behind it. Several defects fixed here
were honesty defects, not visual ones — external co-authors highlighted as lab
members, fabricated paper titles on real DOIs, workshop spotlights presented as
main-conference. Keep that bar.
