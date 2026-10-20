# Homepage editorial E2E infrastructure — 2026-10-20

> **Handoff status (2026-10-20):** Current summary: [verification handoff](docs/verification/2026-10-20/README.md). Detailed historical receipt links below are local-only unless explicitly tracked. Final layout forensic/victory audits remain incomplete.

Owned, independent opaque-box contract suite:
`verification/teamwork-20261020/e2e_track/run_e2e.py`.

It uses installed Python Playwright and the existing Chromium executable. No installation, external writes, email, deployment or production source modification is performed by the suite. A running local static preview is supplied via `--url`. Do not rebuild the shared `dist/` while it runs. The build owner coordinates an immutable preview window.

```bash
python3 -W error -m py_compile verification/teamwork-20261020/e2e_track/run_e2e.py
python3 verification/teamwork-20261020/e2e_track/run_e2e.py --list
python3 verification/teamwork-20261020/e2e_track/run_e2e.py --url http://127.0.0.1:4389
```

The last command runs Tier 1, then Tier 2, Tier 3 and Tier 4. Failures are retained; all cases in the current tier execute, then a failed tier stops advancement. Later cases are explicitly NOT_RUN. The runner exits 1 if any case fails. `--only F1-T2` can execute a diagnostic subset, which must not be reported as a complete suite. The default output is a new `runs/<UTC timestamp>/` directory beside the runner. Existing directories are never overwritten. Each case has a fresh browser context (and independent contexts for parameterized subchecks), preventing dependence on earlier cases.

Full expected-output derivation and feature mapping: [COVERAGE.md](verification/teamwork-20261020/e2e_track/COVERAGE.md). Raw case definitions are [coverage.json](verification/teamwork-20261020/e2e_track/coverage.json). Counts are 5 Tier 1 + 5 Tier 2 for each F1–F6, 15 integration cases and 5 realistic scenarios = 80 distinct cases. Matrix dimensions are not separate counts.

Public behavior covers Korean/English, 320/390/1440 widths, meaningful research explanations, figures/captions/source links, application instructions, keyboard navigation, no-JavaScript reading, empty search recovery, unknown-route response and public evidence documents. Each run records raw results, errors, elapsed time, runner hash and failure screenshots.

Scientific validity, equivalent translation, final aesthetic judgment, recruiter impact and world-class ranking are not inferred from browser passes. Independent source and visual reviews remain required. This suite covers Tiers 1–4 only; independent adversarial Tier 5 is separate.
