# Harness repairs

## 2026-10-20T07:24:24.682518+00:00 — repair 1

Historical execution: runs/20261020T072149Z/results.json, 28 PASS / 2 FAIL, all30 Tier1; Tier2–4 NOT_RUN.
Old runner SHA256: `854293218b15d92cdd8dd497ebcb361326237fb10dd632509d6bb5e6b7f6fe4d`. New runner SHA256: `0182a021f582b2da8cb5d1ec0e3bb74a6203da99e7d3c64a8c95717113b401cc`.
Old bytes retained: runner-history/run_e2e-before-harness-repair-1.py.

1. F2-T1-02: old regex `인과|causal` rejected the rendered sentence `모델 분석 결과가 질환의 원인이나 개인의 진단을 뜻하지는 않습니다`. New regex `인과|원인|causal|cause` accepts equivalent causal-boundary language. The same English alias was added to the bilingual end-to-end scenario. Scientific boundary requirement unchanged.
2. F5-T1-02: locale URL matching normalized the empty path of `#main` to `/`, falsely selecting the skip link when switching English homepage to Korean. Resolve relative hrefs against the current page URL before pathname comparison. Expected locale target unchanged.

Both are test-harness defects. No production or public-document edits performed. Historical failures remain intact and are not treated as successful acceptance.

## 2026-10-20T07:28:17.860257+00:00 — repair 2

Historical execution: runs/20261020T072424Z/results.json,56 PASS /4 FAIL; Tier1 complete30 PASS, Tier2 complete26 PASS/4 FAIL, higher tiers NOT_RUN.
Old runner SHA256:`0182a021f582b2da8cb5d1ec0e3bb74a6203da99e7d3c64a8c95717113b401cc`. New runner SHA256:`8ebdf4530b18eea4469fe19392f03d9863d9e1e6264cc3c12889adedb6baf56b`. Old bytes: runner-history/run_e2e-before-harness-repair-2.py.

1. F1-T2-01: no-JS public research navigation contains valid `#neuro-x`, `#computational-genetics-psychiatry`, `#quantum-machine-learning`, `#art-and-neuroscience` links. Match resolved research URLs and nonempty fragments rather than require literal `/research#` spelling. Four distinct fallback destinations still required.
2. F5-T2-01: Chromium discarded the redirect response body before provenance hashing (`No resource with given identifier found`). Capture final rendered DOM hash and record unavailable response-body hash/error explicitly. HTTP success, visible main, final Korean pathname and language assertions remain unchanged.

Real site/doc failures are not suppressed: F4-T2-04 enlarged-text join contact overflow and F6-T2-02 public review absolute home path were escalated to the production owner.
