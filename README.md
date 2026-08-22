# SNU Connectome Laboratory — Lab Homepage

Official website of the **Connectome Laboratory** at **Seoul National University** (PI: **Prof. Jiook Cha** / 차지욱 교수).

🔗 **Website**: [https://www.connectomelab.com/](https://www.connectomelab.com/)
🏛️ **Affiliations**: Department of Psychology • Interdisciplinary Program in AI (IPAI) • Department of Brain and Cognitive Sciences (BCS)

> *"Everything Connects to Everything Else."* — Leonardo da Vinci

---

## Design

Warm, editorial, people-first — a "bright museum with one dark projection room":
the site runs on a paper-toned light theme (Hahmlet serif display / Pretendard body /
IBM Plex Mono captions), with a single deep-ink band hosting the interactive 3D
connectome sketch. Member photos, alumni destinations, and lab-life stories carry
the warmth; the cyan accent carries the lab's technical identity.

## Features

1. **🧠 Interactive Connectome Sketch (three.js)**
   - An illustrative 3D visualization of the brain networks the lab studies
     (labeled as a sketch, not anatomical data). Nodes link to real lab projects.

2. **📚 Publication Archive (auto-synced)**
   - `scripts/sync_scholar.py` pulls the record (102 entries, 76 of them
     peer-reviewed, 2008–present) from the OpenAlex API with cursor pagination.
     It classifies each entry as journal / conference / workshop / preprint,
     excludes conference-abstract supplements and errata, fuzzy-dedups
     preprint-vs-journal versions of the same paper, and highlights authors
     from a member allowlist rather than by surname.

3. **⚡ Research Radar (weekly arXiv scan)**
   - `scripts/update_research_radar.py` scans arXiv weekly for new papers in brain
     foundation models, fMRI/EEG dynamics, genomics & connectomics, and quantum ML.
   - Summaries are generated with Gemini via OpenRouter when `OPENROUTER_API_KEY`
     is set; otherwise an honestly-labeled abstract excerpt is used. Every record
     carries a `generatedBy` field surfaced in the UI.

4. **💡 AI Idea Lab (`/ideas`)**
   - `scripts/generate_research_ideas.py` feeds the lab's research areas, recent
     publications, and the newest radar trends to Gemini, which proposes weekly
     research hypotheses (hypothesis / rationale / first experiment / risks).
   - Published unedited with a fixed "AI-generated, not lab-endorsed" disclaimer
     and the exact model id on every card. No LLM key → nothing is generated
     (no fake fallback, by design).

5. **💬 Lab Guide (curated FAQ)**
   - A floating guide answering common questions about research, admissions, and
     lab culture from a hand-written FAQ. It is intentionally *not* presented as
     a live AI — the site is fully static.

6. **👥 People-first content**
   - Member profiles with photos, education, research interests, and passions;
     alumni tracked with their current positions; news and history archives.

---

## Tech Stack

- **Framework**: [Astro 5.x](https://astro.build/) (static site generation)
- **UI**: React 18, [three.js](https://threejs.org/), [Tailwind CSS](https://tailwindcss.com/) (+ typography, animate), [Lucide](https://lucide.dev/)
- **Content**: type-safe Astro content collections (Zod schemas) in `src/content/`
- **Pipelines**: Python 3.11 (stdlib only) — OpenAlex API, arXiv API, OpenRouter/Gemini (optional)
- **CI/CD & Hosting**: GitHub Pages + GitHub Actions (`deploy.yml`, `research-radar.yml`)

---

## Getting Started

### Prerequisites
- Node.js `v18.20+`, `v20.3+`, or `v22+`
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
`.github/workflows/research-radar.yml` runs both scripts every Monday, **validates
the generated content with a full `npm run build`** before committing, and deploys
the built site in the same workflow (a `GITHUB_TOKEN` push cannot trigger
`deploy.yml`, so the deploy happens in-workflow).

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
2. DNS: `CNAME` record `www` → `transconnectome.github.io`.

The DNS cutover from the old Google Sites page is done and the site is live.
`scripts/cutover.sh --status` reports the current DNS, custom-domain and
certificate state at any time.

---

## Contact

- **PI**: Prof. Jiook Cha (차지욱) — `connectome@snu.ac.kr` · +82-2-880-8618
- **Lab**: Office M512, Building 16, Seoul National University
- © 2026 SNU Connectome Lab. All rights reserved.
