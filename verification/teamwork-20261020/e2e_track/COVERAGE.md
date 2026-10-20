# E2E coverage — 2026-10-20

80 distinct cases: 30 Tier 1, 30 Tier 2, 15 Tier 3, 5 Tier 4. Locale/viewport iterations are subchecks, not additional cases. Every case executes an observable behavior or public-document assertion. All 15 unordered feature pairs have explicit Tier 3 cases.

Expected outputs are derived from original request and PROJECT F1–F6, AGENTS, README and docs/research-editorial-guidelines.md. Public UI was observed for usable roles, routes and links; no implementation source or implementer report was read.

| Case | Feature | Tier | User outcome | Expected result | Source |
|---|---|---:|---|---|---|
| F1-T1-01 | F1 | 1 | Human-centered bilingual mission | Both homepages explain people and genes/brain/behavior/environment, rather than model names alone. | docs/research-editorial-guidelines.md |
| F1-T1-02 | F1 | 1 | Four question-led entry points | Homepage exposes four distinct question links to detailed research. | README.md#Design |
| F1-T1-03 | F1 | 1 | Question to method explanation | Research overview visibly explains at least one data/design choice for each research direction. | docs/research-editorial-guidelines.md |
| F1-T1-04 | F1 | 1 | Demonstrated examples have research sources | Research page shows concrete study examples and external publication references. | docs/research-editorial-guidelines.md |
| F1-T1-05 | F1 | 1 | Limits remain visible beside research | Research explanation includes predictive/causal boundary and unvalidated next-step language. | docs/research-editorial-guidelines.md |
| F2-T1-01 | F2 | 1 | Homepage research figure loads | Each homepage includes a rendered informative research image. | docs/research-editorial-guidelines.md |
| F2-T1-02 | F2 | 1 | Figure caption carries scientific meaning | Homepage research caption explains the represented observation and its interpretation boundary. | docs/research-editorial-guidelines.md |
| F2-T1-03 | F2 | 1 | Figure credit is a traceable link | A visible source link is associated with the homepage research figure. | docs/research-editorial-guidelines.md |
| F2-T1-04 | F2 | 1 | Research surface labeled as reference | The research illustration is identified as a reference surface with a source, not a result localization map. | docs/research-editorial-guidelines.md |
| F2-T1-05 | F2 | 1 | Informative image alternatives | Every rendered research/homepage image has an alt attribute; figure images have nonempty alternatives. | docs/research-editorial-guidelines.md |
| F3-T1-01 | F3 | 1 | Homepage offers application path | A reader can click a visible homepage action and reach the locale-appropriate join page. | docs/research-editorial-guidelines.md |
| F3-T1-02 | F3 | 1 | Application route names supported roles | Join page identifies graduate, postdoctoral and undergraduate/intern routes without inventing openings. | docs/research-editorial-guidelines.md |
| F3-T1-03 | F3 | 1 | Concrete application materials | Applicants see CV, transcript and a research-interest statement requirement. | docs/research-editorial-guidelines.md |
| F3-T1-04 | F3 | 1 | Public contact action | Join includes a syntactically valid usable mailto application contact. | docs/research-editorial-guidelines.md |
| F3-T1-05 | F3 | 1 | Research culture gives concrete expectations | Join explains independence, learning, collaboration and research completion. | docs/research-editorial-guidelines.md |
| F4-T1-01 | F4 | 1 | Responsive home layout | Both homepages fit 320/390/1440px without horizontal overflow. | PROJECT.md#F4 |
| F4-T1-02 | F4 | 1 | Responsive research layout | Both research pages fit 320/390/1440px without horizontal overflow. | PROJECT.md#F4 |
| F4-T1-03 | F4 | 1 | Responsive join layout | Both join pages fit 320/390/1440px without horizontal overflow. | PROJECT.md#F4 |
| F4-T1-04 | F4 | 1 | Reading landmarks and heading | Core pages provide one visible h1, main landmark and named document language. | PROJECT.md#F4 |
| F4-T1-05 | F4 | 1 | Controls have accessible names | All visible core-page interactive controls have usable names. | PROJECT.md#F4 |
| F5-T1-01 | F5 | 1 | Public route preservation | All eight established public routes load in both languages. | README.md |
| F5-T1-02 | F5 | 1 | Locale switch preserves route | Core pages offer the counterpart locale and follow it without losing page intent. | AGENTS.md |
| F5-T1-03 | F5 | 1 | Core internal destinations resolve | Every visible core-page local link has a successful response; fragment IDs exist. | AGENTS.md |
| F5-T1-04 | F5 | 1 | Core assets decode | All main images on home, research and join decode successfully. | AGENTS.md |
| F5-T1-05 | F5 | 1 | Page metadata describes each route | Each core locale page has distinct title and nonempty description plus HTTPS canonical. | README.md |
| F6-T1-01 | F6 | 1 | Dated public review artifact | Request-scoped public review exists and explicitly records the 2026-10-20 revision. | AGENTS.md#완료 보고 |
| F6-T1-02 | F6 | 1 | Concrete before-after examples | Public review includes concrete before/after text and the rationale for changes. | docs/research-editorial-guidelines.md#8 |
| F6-T1-03 | F6 | 1 | Claim-source mapping | Public review maps claims to identifiable source URLs and section/figure/table locators. | docs/research-editorial-guidelines.md#3 |
| F6-T1-04 | F6 | 1 | Image provenance record | Image record identifies source and license plus excerpt/transformation provenance. | docs/research-editorial-guidelines.md#6 |
| F6-T1-05 | F6 | 1 | Scope and remaining verification | Public review distinguishes executed work from unresolved verification and PI decisions. | docs/research-editorial-guidelines.md#8 |
| F1-T2-01 | F1 | 2 | No-JavaScript research meaning | Disabling scripts preserves all four questions and substantial explanatory research text. | docs/research-editorial-guidelines.md |
| F1-T2-02 | F1 | 2 | Homepage layer links to detail | Each unique homepage research question link reaches its corresponding visible explanatory section. | docs/research-editorial-guidelines.md |
| F1-T2-03 | F1 | 2 | No unsupported superlative promise | Homepage does not promise guaranteed admission, guaranteed results or world-best ranking as fact. | docs/research-editorial-guidelines.md |
| F1-T2-04 | F1 | 2 | Research locale coverage parity | Both locales expose the same four research directions through corresponding anchors. | docs/research-editorial-guidelines.md |
| F1-T2-05 | F1 | 2 | Narrow-screen explanation readability | Research prose at 320px is visible, has no replacement characters or clipped horizontal extent. | docs/research-editorial-guidelines.md |
| F2-T2-01 | F2 | 2 | Narrow figure and caption containment | Figures and their captions stay inside the 320px viewport. | docs/research-editorial-guidelines.md |
| F2-T2-02 | F2 | 2 | Figure source works without scripts | Caption, credit link and decoded figure remain available when JavaScript is disabled. | docs/research-editorial-guidelines.md |
| F2-T2-03 | F2 | 2 | Missing image retains explanation | When image responses fail, textual figure alternative and visible caption still explain the content. | docs/research-editorial-guidelines.md |
| F2-T2-04 | F2 | 2 | Image provenance locale parity | Both locales use the same homepage research figure source and credit destination. | docs/research-editorial-guidelines.md |
| F2-T2-05 | F2 | 2 | Image license stays visible | Research figure attribution states the license in both languages. | docs/research-editorial-guidelines.md |
| F3-T2-01 | F3 | 2 | Openings uncertainty preserved | Join asks readers to verify current openings and distinguishes formal university admission. | docs/research-editorial-guidelines.md |
| F3-T2-02 | F3 | 2 | Keyboard-operable FAQ | FAQ question can be focused and expanded with Enter, revealing its answer. | docs/research-editorial-guidelines.md |
| F3-T2-03 | F3 | 2 | Application without JavaScript | No-JS visitors can reach application instructions and contact. | docs/research-editorial-guidelines.md |
| F3-T2-04 | F3 | 2 | Application locale contact parity | Both languages direct applications to the same verified public mailbox and matching program families. | docs/research-editorial-guidelines.md |
| F3-T2-05 | F3 | 2 | Mobile application anchor | At 390px the join page application anchor reaches visible preparation/contact instructions. | docs/research-editorial-guidelines.md |
| F4-T2-01 | F4 | 2 | Keyboard mobile menu | A keyboard user opens mobile navigation and follows Research. | PROJECT.md#F4 |
| F4-T2-02 | F4 | 2 | Keyboard focus remains perceptible | Focused primary application link has visible outline or box-shadow focus styling. | PROJECT.md#F4 |
| F4-T2-03 | F4 | 2 | Native research navigation without scripts | At 320px all four native research links remain usable with JavaScript disabled. | PROJECT.md#F4 |
| F4-T2-04 | F4 | 2 | Text enlargement does not clip content | Core pages at 200% root text sizing remain readable without horizontal overflow. | PROJECT.md#F4 |
| F4-T2-05 | F4 | 2 | Reduced motion preserves content | Reduced-motion readers retain headline, research links, figures and application action. | PROJECT.md#F4 |
| F5-T2-01 | F5 | 2 | Legacy Korean redirects | Established /ko and /ko/research links reach Korean content. | README.md |
| F5-T2-02 | F5 | 2 | Graceful unknown route | Unknown URL returns a genuine 404 with a visible explanation, not a blank page or false-success homepage. | PROJECT.md#F5 |
| F5-T2-03 | F5 | 2 | Publication no-match and recovery | Impossible publication search explains zero results; clearing restores publications. | README.md |
| F5-T2-04 | F5 | 2 | Runtime console remains error-free | Core-page loads and native disclosures cause no browser page errors. | PROJECT.md#F5 |
| F5-T2-05 | F5 | 2 | Deep-link reload preserves target | A research link can be bookmarked and reloaded, retaining a valid visible section. | PROJECT.md#F5 |
| F6-T2-01 | F6 | 2 | Public artifact local links resolve | All local Markdown link targets in the request-specific review exist. | docs/research-editorial-guidelines.md#8 |
| F6-T2-02 | F6 | 2 | Public documentation contains no private operational paths | Review does not expose home-directory paths, credentials, private workspace links or secret-bearing strings. | AGENTS.md#검증과 변경 범위 |
| F6-T2-03 | F6 | 2 | Verification is reproducible | Public review records actual build/browser verification commands or links to their report, and distinguishes science review. | docs/research-editorial-guidelines.md#8 |
| F6-T2-04 | F6 | 2 | Maintenance and future updates documented | Public review states how reviewed content and sources should be updated or revalidated. | docs/research-editorial-guidelines.md#8 |
| F6-T2-05 | F6 | 2 | New review is indexed by canonical content review | Canonical content review mentions this dated revision or links its public report. | AGENTS.md#완료 보고 |
| F1+F2-T3-01 | F1+F2 | 3 | Question-to-evidence reading path | A homepage reader follows a research figure/context link and finds question, representative study and limits. | PROJECT.md#F1-F2 |
| F1+F3-T3-01 | F1+F3 | 3 | Research interest becomes application | After reading a research question visitors can reach locale-correct application information from navigation. | PROJECT.md#F1-F3 |
| F1+F4-T3-01 | F1+F4 | 3 | Question links remain keyboard readable | At 320px keyboard activation of a question reaches a visible explanatory heading without clipping. | PROJECT.md#F1-F4 |
| F1+F5-T3-01 | F1+F5 | 3 | Research breadth survives route reload and locale change | All four question destinations still resolve after navigation and the paired locale retains all four. | PROJECT.md#F1-F5 |
| F1+F6-T3-01 | F1+F6 | 3 | Research examples tie to public claim record | A named representative model in the rendered research explanation is present in the public claim/source review. | PROJECT.md#F1-F6 |
| F2+F3-T3-01 | F2+F3 | 3 | Figure reading does not dead-end applicant | After viewing homepage evidence and source credit, an applicant can reach instructions without leaving the locale. | PROJECT.md#F2-F3 |
| F2+F4-T3-01 | F2+F4 | 3 | Mobile visual explanation | At 390px decoded research figure, explanatory caption and credit remain readable together. | PROJECT.md#F2-F4 |
| F2+F5-T3-01 | F2+F5 | 3 | Figure assets survive language navigation | A decoded figure and its provenance remain available after switching locale and reloading. | PROJECT.md#F2-F5 |
| F2+F6-T3-01 | F2+F6 | 3 | Visible figure ties to provenance record | The homepage credit source is explicitly traceable in public image/review documentation. | PROJECT.md#F2-F6 |
| F3+F4-T3-01 | F3+F4 | 3 | Keyboard mobile applicant flow | At 320px applicant follows visible CTA by Enter then opens a FAQ and can reach contact. | PROJECT.md#F3-F4 |
| F3+F5-T3-01 | F3+F5 | 3 | Application route reload and locale equivalence | A bookmarked application page retains preparation and same contact after locale change and reload. | PROJECT.md#F3-F5 |
| F3+F6-T3-01 | F3+F6 | 3 | Applicant edits have a durable scope record | Working public application path is accompanied by a public review of recruitment/application changes and remaining approval boundaries. | PROJECT.md#F3-F6 |
| F4+F5-T3-01 | F4+F5 | 3 | Mobile locale round trip | At 390px language switching twice preserves research route and no overflow. | PROJECT.md#F4-F5 |
| F4+F6-T3-01 | F4+F6 | 3 | Responsive evidence records actual target widths | Public review records the 320/390/1440 browser conditions whose homepage behavior is reproducible. | PROJECT.md#F4-F6 |
| F5+F6-T3-01 | F5+F6 | 3 | Reproducible verification points to current public route contract | Documented verification references coexist with reachable locale core routes and the canonical record indexes the same revision. | PROJECT.md#F5-F6 |
| ALL-T4-01 | ALL | 4 | Korean mobile prospective graduate | 390px Korean visitor reads mission, research detail, application preparation and contact. | ORIGINAL_REQUEST.md + PROJECT.md |
| ALL-T4-02 | ALL | 4 | English desktop researcher | 1440px English reader reviews image credit, follows research evidence, then finds publications and application. | ORIGINAL_REQUEST.md + PROJECT.md |
| ALL-T4-03 | ALL | 4 | Low-script narrow-screen applicant | 320px visitor with scripts disabled can read question, its evidence, and prepare an application. | ORIGINAL_REQUEST.md + PROJECT.md |
| ALL-T4-04 | ALL | 4 | Bilingual reader compares meaning boundaries | Reader switches homepage language, sees same figure/source and matching scope dimensions, then follows research. | ORIGINAL_REQUEST.md + PROJECT.md |
| ALL-T4-05 | ALL | 4 | Skeptical visitor recovers from no-match search | Publication visitor sees empty-state feedback, clears it, finds evidence, and returns to research navigation. | ORIGINAL_REQUEST.md + PROJECT.md |

## Limits

- Content presence and routes do not establish scientific truth or equivalent translation. Independent source review remains required.
- Loading, alt, captions, sources and mobile containment do not establish aesthetic quality or scientific interpretation.
- No external publication crawl, emails, installation or deployment.
- Tier 5 belongs to independent challengers.
- First failed tier stops advancement; remaining tiers are explicitly NOT_RUN. Every case in the failed tier still executes and is retained. Evidence directories never overwrite prior runs.
