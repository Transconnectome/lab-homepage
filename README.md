# SNU Connectome Laboratory — Lab Homepage

Official website of the **Connectome Laboratory** at **Seoul National University** (PI: **Prof. Jiook Cha** / 차지욱 교수).

🔗 **Website**: [https://www.connectomelab.com/](https://www.connectomelab.com/)
🏛️ **Affiliations**: Department of Psychology • Interdisciplinary Program in AI (IPAI) • Department of Brain and Cognitive Sciences (BCS)

> *"Everything Connects to Everything Else."* — Leonardo da Vinci

---

## Design

The homepage starts with the lab's mission in the visitor's language, alongside
an attributed research figure. It then explains what studying connections means,
links four concrete questions to the research page, introduces how researchers
learn and work together, and closes with dated news and selected publications.
The English motto remains a secondary element. The paper, ink and teal palette
uses MaruBuri for Korean display text, Hahmlet for English display text,
Pretendard for body text and IBM Plex Mono for dates.

The research page combines four numbered questions with an accessible research
map, a sourced cortical surface reference, and the project list. Each area's question and explanation
precede its selected-paper summary. The People page includes Jiook Cha's research
perspective; Join describes learning, reflection, and responsibility alongside
application instructions. Publications are grouped by year;
publications, people and lab notes use labeled native filters. Research Radar
and AI Ideas remain public under footer **Lab notes** links. Their generated
content and model attribution remain visible in the relevant entries.

The homepage, news and social preview use an attributed excerpt of a published
MBBN figure. Existing member images are portraits. Decorative news illustrations are no longer
displayed. See [image sources and license](public/assets/site/README.md).

## Features

1. ** Research Map**
   - Four question tabs reuse the reviewed research content. Native section links
     remain available without JavaScript. Relationships distinguish implemented
     combinations, shared interests and open questions. The static FreeSurfer
     cortical surface is a reference image, with no research areas placed on it.
     See [surface source and license](public/assets/research/README.md).

2. ** Publication Archive (auto-synced)**
   - `scripts/sync_scholar.py` pulls publication records (2008–present)
     from the OpenAlex API with cursor pagination.
     It classifies each entry as journal / conference / workshop / preprint,
     excludes conference-abstract supplements and errata, fuzzy-dedups
     preprint-vs-journal versions of the same paper, and highlights authors
     from a member allowlist rather than by surname.

3. ** Research Radar (weekly arXiv scan)**
   - `scripts/update_research_radar.py` sweeps arXiv weekly across seven topic
     buckets, each with its own query and quota: brain foundation models for fMRI
     and for EEG (kept apart so neither starves the other), gene & brain, affective
     & developmental, agentic AI applied to brain research, quantum ML, and
     brain-LLM alignment. A paper's topic is the bucket that surfaced it.
   - Broad buckets over-fetch and narrow through two gates: a neuro-term match on
     title+abstract, then the summarizer's own 0-1 `labRelevanceScore` (entries
     below 0.4 are never written).
   - Summaries are generated with Gemini via OpenRouter when `OPENROUTER_API_KEY`
     is set; otherwise an honestly-labeled abstract excerpt is used. New records
     carry a `generatedBy` field surfaced in the UI; missing historical records
     are labeled as not recorded.
   - `RADAR_DRY_RUN=1` prints each bucket's query URL and candidate counts without
     writing; `ARXIV_CACHE=<file>` replays a saved feed offline.

4. ** AI Idea Lab (`/ideas`)**
   - `scripts/generate_research_ideas.py` feeds the lab's research areas, recent
     publications, and radar trends to Gemini, which proposes weekly research
     hypotheses (hypothesis / rationale / first experiment / risks).
   - Trends reach the prompt round-robin across topics, so one prolific bucket
     cannot decide what the whole page is about. Each run publishes at most one
     idea per category, and an idea is rejected when the same radar paper has
     already been mined for that category — the failure mode that once produced
     three foundation-models ideas from a single paper.
   - Keeps the exact generation model and entry-specific content corrections.
     Hypotheses remain unvalidated and are not adopted lab plans. No LLM key → nothing is generated
     (no fake fallback, by design).

5. **Frequently asked questions**
   - The Join page collects nine questions about research, admissions, and lab
     culture in a bilingual, accessible FAQ. Answers are static and hand-written, grouped into applications/lab life and research.

6. ** People-first content**
   - Member profiles with photos, education, research interests, and passions;
     alumni tracked with their current positions; news and history archives.

---

## Tech Stack

- **Framework**: [Astro 7.x](https://astro.build/) (static site generation)
- **UI**: React 18, [three.js](https://threejs.org/), [Tailwind CSS](https://tailwindcss.com/) (+ typography, animate), [Lucide](https://lucide.dev/)
- **Content**: type-safe Astro content collections (Zod schemas) in `src/content/`
- **Pipelines**: Python 3.11 (stdlib only) — OpenAlex API, arXiv API, OpenRouter/Gemini (optional)
- **CI/CD & Hosting**: GitHub Pages + GitHub Actions (`deploy.yml`, `research-radar.yml`)

---

## Getting Started

### Prerequisites
- Node.js 22, version `22.12.0` or newer (see `.nvmrc`)
- Python `3.10+` (for the sync scripts)

### Development
```bash
git clone https://github.com/Transconnectome/lab-homepage.git
cd lab-homepage
npm ci
npm run dev        # http://localhost:4321
```

### Build & Preview
```bash
npm run build
npm test
npm run test:site
npm run preview
```

The research map has a browser contract suite. With the built preview running
on the default port, use `npm run test:research-map`. Install Python Playwright
and its Chromium browser first (`python3 -m pip install playwright`, then
`python3 -m playwright install chromium`). `RESEARCH_MAP_URL` selects another
preview URL; `PLAYWRIGHT_CHROMIUM_EXECUTABLE` selects an existing Chromium binary.
The 11 browser checks cover both languages, five screen widths, native links
without JavaScript, keyboard selection, the static image without WebGL, visible
research scope and FAQ source links. This is a separately invoked local suite;
it is not included in `npm test` or CI. Content regression checks preserve known
PI corrections but do not establish scientific meaning or philosophical depth.
The source-based review and its limits are in [the content review](docs/research-content-review.md#18-추가-문단-교정과-읽기-흐름-보완--2026-09-14).

---

## Content Pipelines

### Publications sync (OpenAlex)
```bash
python3 scripts/sync_scholar.py
```

### Research Radar (arXiv, optional LLM synthesis)
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."   # optional; falls back to labeled excerpts
python3 scripts/update_research_radar.py
```

### Weekly automation
`.github/workflows/research-radar.yml` runs every Monday. It commits generated
records locally, integrates current `main`, then tests and builds the final tree
before pushing and deploying. All Pages writers share one concurrency group.
A `GITHUB_TOKEN` push cannot trigger `deploy.yml`, so weekly sync deploys in-workflow.

News issues produce downloadable bilingual drafts, not automatic publications.
Review the Actions artifact and copy approved files to `src/content/news/` on
`main`. No permanent bot branches are needed. `main` is the maintained branch;
see `claudedocs/HANDOFF.md` for validation and publication instructions.

---

## Languages & routing

**Korean is the default language and lives at the root**; English is under `/en/`.

| | Korean | English |
|---|---|---|
| Home | `/` | `/en/` |
| Research | `/research` | `/en/research` |

UI strings live in `src/i18n/ui.ts`; page content is chosen by a `lang` field on
each content entry (`*-ko.md` files carry `lang: "ko"`). Every page emits
`hreflang` alternates with Korean as `x-default`. The site previously served
Korean under `/ko/`, so those paths are kept alive as redirects declared in
`astro.config.mjs`.

Research entries keep a hand-reviewed `question` alongside `tagline`. The homepage
question links and the research article introductions read the same field. Update
both language entries together; keep the question within the evidence reviewed in
`docs/research-content-review.md`. The research Markdown is not written by the
publication, project, Radar, or Ideas pipelines.

Korean typography is not simply Latin typography with different glyphs — see
`src/styles/global.css`, where `word-break: keep-all`, negative display
tracking, and the `:lang(ko)` overrides are documented with the reasons.

## Custom Domain & GitHub Pages

1. Repository **Settings → Pages**: Source = **GitHub Actions**; Custom domain =
   `www.connectomelab.com` with **Enforce HTTPS**.
2. Current DNS: `www` uses GitHub Pages A/AAAA records. A CNAME to
   `transconnectome.github.io` is the recommended subdomain configuration.
   The bare apex domain has no records and is not reachable.

The DNS cutover from the old Google Sites page is done and the site is live.
`scripts/cutover.sh --status` reports the current DNS, custom-domain and
certificate state at any time.

---

## Contact

- **PI**: Prof. Jiook Cha (차지욱) — `connectome@snu.ac.kr` · +82-2-880-8618
- **Lab**: Office M512, Building 16, Seoul National University
- © 2026 SNU Connectome Lab. All rights reserved.

Editorial corrections on Radar and Ideas use `editorialNote` (date, English/Korean scope);
original `generatedBy` values stay intact. Missing historic generation records are not inferred.
Radar supports Korean summary fields with explicit English fallback. `imageHidden` preserves
an existing illustration and its provenance while omitting it from the public rendering.
The idea generator reads the complete curated English research descriptions and never
overwrites an existing output path. These safeguards do not verify new AI hypotheses.
