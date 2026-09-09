# Handoff — SNU Connectome Lab homepage

Updated 2026-09-09. Public repository: Transconnectome/lab-homepage.
Live site: https://www.connectomelab.com/.

## One maintained branch

Use main for this repository. The canonical local checkout is
/home/juke/git/lab-homepage. Obsolete feature branches, competing research-page
implementations, and linked worktrees were consolidated after a full local backup.
Non-homepage research material and unverified news drafts stay in the private
local archive; they are not part of the public site. The archive and recovery
instructions are recorded in the local backup directory, not this public repo.

The deployed research structure remains four bilingual areas, with Neuro-X
containing fMRI and EEG foundation-model work. The alternate split-page design
was not adopted. Useful duplicate-prevention logic from that branch was retained.

## Run and verify

Node 22 (>=22.12), Python 3.10+, Astro 7, React 18, Tailwind 3 via PostCSS.

```bash
npm ci
npm test
npm run build
npm run test:site
npm run preview -- --host 127.0.0.1
npm audit --omit=dev
```

Astro 7 preview runs as a managed background server; use
`npm exec astro preview stop` when finished.

Before pushing, inspect the diff, preserve unrelated edits, and stage explicit
paths. A normal push to main deploys after tests and build. Do not force-push.
If origin/main advanced, integrate it and repeat tests/build on the final tree.
The main ruleset blocks deletion and non-fast-forward updates. Secret scanning,
push protection and vulnerability alerts are enabled; automatic dependency PRs
are disabled to avoid accumulating unattended branches.

## Architecture and routing

- Korean is at /; English is at /en/.
- Thin route wrappers use shared lang-aware components in src/components/pages/.
- Content schema: src/content.config.ts, with glob loaders over src/content/.
- Markdown uses render(entry); collection IDs preserve the existing filenames.
- Research anchor IDs use baseSlug for Korean and entry.id for English.
- /ko/ legacy routes remain redirects. Never remove them as “duplicate pages.”
- UI labels: src/i18n/ui.ts. Prefer localePath() for internal navigation.
- History source files are retained; the History route is intentionally unpublished.
- The curated Lab Guide is a static FAQ, not an online model.
- AI Ideas remain explicitly machine-generated and not lab-endorsed.

## Automation

| Workflow | Behavior |
| --- | --- |
| deploy.yml | On main push/manual: check out current main, install, offline tests, build, generated-route checks, deploy |
| check.yml | The same checks for incoming PRs/manual runs, without publishing |
| research-radar.yml | Weekly/manual: generate only publications/trends/ideas/project metadata, commit locally, rebase, validate the final tree, push normally, deploy that artifact |
| news-submission.yml | Eligible news issue → escaped bilingual Markdown drafts → downloadable Actions artifact; no site writes or deployment |

All Pages writers share concurrency group pages. Latest-main checkout prevents a
queued old event from redeploying old content. Weekly sync rebuilds after rebase;
push rejection stops deployment. GITHUB_TOKEN pushes do not start deploy.yml,
so weekly sync deploys its validated artifact within its own workflow.

News drafts are kept in .news-drafts (ignored locally) and Actions artifacts for
30 days. A maintainer verifies facts, names, dates, external links and publication
consent, then copies the approved pair to src/content/news on main. The issue
stays open until the maintainer handles it. No persistent bot branch is created.
The issue form is public: do not submit private information.

Generators use OPENROUTER_API_KEY when available. News generation requires it;
Radar falls back to labeled abstract excerpts; Ideas generate nothing without a
configured backend. Existing hand-reviewed research prose is never overwritten.

## Content contracts

- Four research areas must have matching English/Korean entries.
- MBBN has one Communications Biology record. Its differently titled arXiv
  preprint is excluded by the manual merge rule in sync_scholar.py.
- NeuroMamba and DIVER-0 are workshop publications, including member highlights.
- Idea prompts receive only canonical English research descriptions.
- News links allow HTTP(S) only; generated bodies are escaped as plain text.
- Publication updates preserve curated existing records. New metadata does not
  automatically correct stale member affiliations or old publication URLs.
- Build checks cover all 16 canonical pages, /ko redirects, language/canonical
  metadata, internal links, fragments and local assets. They do not establish
  scientific validity or prove external links are reachable.
- Scientific source decisions and review history: docs/research-content-review.md.

## Typography and browser checks

Keep Korean word-break: keep-all and overflow wrapping. Hangul uses the Korean
font stacks; do not route it through a Latin-only monospace font. The self-hosted
MaruBuri subset and its license must stay together. Latin display text remains
Hahmlet. Korean prose uses .measure and :lang(ko) overrides in global.css.

Review desktop 1440×1000 and mobile 390×844 after layout/runtime changes. Check
language switching, the research-map links, member/publication filters, the Lab
Guide, and keyboard Enter/Space behavior on Radar summaries. Check real font
rendering with CDP CSS.getPlatformFontsForNode when changing typography.

DGX Chromium executable:
/home/juke/.cache/ms-playwright/chromium-1217/chrome-linux/chrome.

## Hosting and remaining factual decisions

www.connectomelab.com serves GitHub Pages with HTTPS enforcement. DNS currently
uses GitHub Pages A/AAAA records, not the CNAME formerly described in this file.
The bare connectomelab.com domain still lacks records; it is independently
unreachable. This does not prevent a valid www-only certificate. Check with
`./scripts/cutover.sh --status`. DNS changes require access to the registrar.

Remaining content decisions are not hidden in feature branches:

- Reconcile all member status/affiliation dates against a lab-owned roster.
- Supply Korean member education/interests/passions and Radar body translations.
- Confirm the official genetics/multi-omics axis name and current recruitment.
- Recheck the Communications Medicine early-view article at Version of Record.
- Unverified BK award claims were removed pending an authoritative record.
- Unverified PR #10 news was archived locally, not used to infer graduation status.

The prior certificate incident, competing designs and discarded diagnostics
remain recoverable through Git history and the local backup. Do not revive old
recovery workflows or speculative DNS explanations.
