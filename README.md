# SNU Connectome Laboratory — Lab Homepage

Official website of the **Connectome Laboratory** at **Seoul National University** (PI: **Prof. Jiook Cha** / 차지욱 교수).

🔗 **Website**: [https://www.connectomelab.com/](https://www.connectomelab.com/)
🏛️ **Affiliations**: Department of Psychology • Interdisciplinary Program in AI (IPAI) • Department of Brain and Cognitive Sciences (BCS)

> *"Everything Connects to Everything Else."* — Leonardo da Vinci

---

## Design

The homepage has three sections: a short lab introduction with an attributed
research figure, dated news alongside selected publications, and a strip of
member portraits with application information. The paper, ink and teal palette
uses MaruBuri for Korean display text, Hahmlet for English display text,
Pretendard for body text and IBM Plex Mono for dates.

The research page holds four numbered research areas, the illustrative 3D
connectome sketch and the project list. Publications are grouped by year;
publications, people and lab notes use labeled native filters. Research Radar
and AI Ideas remain public under footer **Lab notes** links. Their generated
content and model attribution remain visible in the relevant entries.

The homepage, news and social preview use an attributed excerpt of a published
MBBN figure. Existing member images are portraits; generated news illustrations
are labeled and collapsed. See [image sources and license](public/assets/site/README.md).

## Features

1. ** Interactive Connectome Sketch (three.js)**
   - An illustrative 3D visualization of the brain networks the lab studies
     (labeled as a sketch, not anatomical data). Research-axis controls link to the corresponding research sections.

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
     is set; otherwise an honestly-labeled abstract excerpt is used. Every record
     carries a `generatedBy` field surfaced in the UI.
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
   - Published unedited with a fixed "AI-generated, not lab-endorsed" disclaimer
     and the exact model id on every entry. No LLM key → nothing is generated
     (no fake fallback, by design).

5. **Frequently asked questions**
   - The Join page collects seven questions about research, admissions, and lab
     culture in a bilingual, accessible FAQ. Answers are static and hand-written.

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
