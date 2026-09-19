#!/usr/bin/env python3
import re
import os

INDEX_PATH = "/home/juke/git/lab-homepage/claudedocs/prototypes/index.html"
SCRIPT_PATH = "/home/juke/git/lab-homepage/claudedocs/prototypes/script.js"

# 1. Option E CSS
OPTION_E_CSS = """
    /* =========================================================================
       OPTION E: QUIET INTELLECTUAL (THE EDITORIAL MONOGRAPH)
       Aesthetic: Restrained Editorial, Warm Paper, Ink Black, Muted Oxblood
       Inspiration: The New Yorker, Nature Longform, MIT McGovern, Janelia
       ========================================================================= */

    :root {
      --opt-e-bg: #FAF8F5;
      --opt-e-surface: #FFFFFF;
      --opt-e-ink: #16171A;
      --opt-e-ink-secondary: #484E5B;
      --opt-e-ink-muted: #767D8C;
      --opt-e-border: #E6E2DA;
      --opt-e-border-light: #F0ECE4;
      --opt-e-accent: #801818; /* Muted Oxblood / Crimson */
      --opt-e-accent-light: #9E2424;
      --opt-e-tag-bg: #F2EFE9;
      --font-e-serif: "Newsreader", "Cormorant Garamond", "Didot", "Baskerville", "Georgia", "MaruBuri", serif;
    }

    #view-option-e {
      background: var(--opt-e-bg);
      color: var(--opt-e-ink);
      font-family: var(--font-sans);
      line-height: 1.75;
      position: relative;
    }

    .opt-e-serif {
      font-family: var(--font-e-serif);
    }

    .opt-e-container {
      max-width: 1160px;
      margin: 0 auto;
      padding: 0 32px;
    }

    /* Minimal Top Navigation */
    .opt-e-header {
      padding: 36px 0 24px;
      border-bottom: 1px solid var(--opt-e-border);
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 20px;
    }

    .opt-e-brand-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .opt-e-brand-univ {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--opt-e-ink-muted);
    }

    .opt-e-brand-lab {
      font-family: var(--font-e-serif);
      font-size: 26px;
      font-weight: 600;
      letter-spacing: -0.01em;
      color: var(--opt-e-ink);
      text-decoration: none;
    }

    .opt-e-nav-links {
      display: flex;
      gap: 28px;
    }

    .opt-e-nav-links a {
      font-size: 13.5px;
      font-weight: 500;
      color: var(--opt-e-ink-secondary);
      text-decoration: none;
      transition: color 0.15s ease;
      letter-spacing: 0.01em;
    }

    .opt-e-nav-links a:hover {
      color: var(--opt-e-accent);
    }

    /* Hero: The Restrained Monograph */
    .opt-e-hero {
      padding: 70px 0 60px;
      max-width: 920px;
    }

    .opt-e-hero-eyebrow {
      font-family: var(--font-mono);
      font-size: 11.5px;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--opt-e-accent);
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .opt-e-hero-eyebrow::after {
      content: "";
      width: 40px;
      height: 1px;
      background: var(--opt-e-accent);
      opacity: 0.4;
    }

    .opt-e-hero-statement {
      font-family: var(--font-e-serif);
      font-size: 3.4rem;
      font-weight: 500;
      line-height: 1.22;
      color: var(--opt-e-ink);
      letter-spacing: -0.02em;
      margin-bottom: 28px;
      word-break: keep-all;
    }

    .opt-e-hero-statement span.italic {
      font-style: italic;
      font-weight: 400;
    }

    .opt-e-hero-sub {
      font-size: 18px;
      line-height: 1.85;
      color: var(--opt-e-ink-secondary);
      word-break: keep-all;
      max-width: 820px;
      margin-bottom: 40px;
    }

    .opt-e-hero-sub strong {
      color: var(--opt-e-ink);
      font-weight: 600;
    }

    /* Core Metrics - Pure Academic Form */
    .opt-e-summary-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 24px;
      padding: 28px 0;
      border-top: 1px solid var(--opt-e-border);
      border-bottom: 1px solid var(--opt-e-border);
      margin-bottom: 70px;
    }

    .opt-e-summary-item .num {
      font-family: var(--font-e-serif);
      font-size: 2.2rem;
      font-weight: 600;
      color: var(--opt-e-ink);
      line-height: 1.1;
      margin-bottom: 4px;
    }

    .opt-e-summary-item .label {
      font-size: 13px;
      font-weight: 600;
      color: var(--opt-e-ink);
      margin-bottom: 2px;
    }

    .opt-e-summary-item .desc {
      font-size: 12px;
      color: var(--opt-e-ink-muted);
      line-height: 1.5;
    }

    /* SECTION SCAFFOLD */
    .opt-e-section {
      padding: 60px 0;
      border-bottom: 1px solid var(--opt-e-border);
    }

    .opt-e-section-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 44px;
    }

    .opt-e-section-num {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.15em;
      color: var(--opt-e-accent);
      text-transform: uppercase;
    }

    .opt-e-section-title {
      font-family: var(--font-e-serif);
      font-size: 2.2rem;
      font-weight: 500;
      color: var(--opt-e-ink);
      letter-spacing: -0.01em;
      word-break: keep-all;
    }

    /* SECTION 01: THE FOUNDATIONAL PREMISE (TWO-COLUMN ESSAY) */
    .opt-e-essay-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 56px;
    }

    .opt-e-essay-col h3 {
      font-family: var(--font-e-serif);
      font-size: 1.5rem;
      font-weight: 600;
      color: var(--opt-e-ink);
      margin-bottom: 16px;
      line-height: 1.35;
      word-break: keep-all;
    }

    .opt-e-essay-col p {
      font-size: 15.5px;
      line-height: 1.85;
      color: var(--opt-e-ink-secondary);
      margin-bottom: 20px;
      word-break: keep-all;
    }

    .opt-e-essay-col p strong {
      color: var(--opt-e-ink);
      font-weight: 600;
    }

    .opt-e-pullquote {
      border-left: 2px solid var(--opt-e-accent);
      padding: 8px 0 8px 20px;
      font-family: var(--font-e-serif);
      font-size: 17px;
      font-style: italic;
      color: var(--opt-e-ink);
      line-height: 1.7;
      margin: 28px 0;
      word-break: keep-all;
    }

    /* SECTION 02: FOUR CORE RESEARCH INQUIRIES */
    .opt-e-inquiry-list {
      display: flex;
      flex-direction: column;
      gap: 40px;
    }

    .opt-e-inquiry-row {
      display: grid;
      grid-template-columns: 80px 1.2fr 1fr;
      gap: 36px;
      padding-bottom: 40px;
      border-bottom: 1px solid var(--opt-e-border-light);
    }

    .opt-e-inquiry-row:last-child {
      border-bottom: none;
      padding-bottom: 0;
    }

    .opt-e-inquiry-index {
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 600;
      color: var(--opt-e-accent);
      padding-top: 4px;
    }

    .opt-e-inquiry-primary h4 {
      font-family: var(--font-e-serif);
      font-size: 1.6rem;
      font-weight: 600;
      color: var(--opt-e-ink);
      margin-bottom: 12px;
      line-height: 1.3;
      word-break: keep-all;
    }

    .opt-e-inquiry-question {
      font-family: var(--font-e-serif);
      font-style: italic;
      font-size: 15px;
      color: var(--opt-e-accent-light);
      margin-bottom: 14px;
      line-height: 1.6;
      word-break: keep-all;
    }

    .opt-e-inquiry-body {
      font-size: 14.5px;
      line-height: 1.8;
      color: var(--opt-e-ink-secondary);
      word-break: keep-all;
    }

    .opt-e-inquiry-spec-block {
      background: var(--opt-e-surface);
      border: 1px solid var(--opt-e-border);
      padding: 20px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
    }

    .opt-e-inquiry-spec-item .meta-label {
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--opt-e-ink-muted);
      margin-bottom: 4px;
    }

    .opt-e-inquiry-spec-item .meta-val {
      font-size: 13px;
      font-weight: 600;
      color: var(--opt-e-ink);
    }

    /* SECTION 03: EMPIRICAL EVIDENCE & PLATES */
    .opt-e-figure-plate {
      display: grid;
      grid-template-columns: 1.1fr 1fr;
      gap: 40px;
      background: var(--opt-e-surface);
      border: 1px solid var(--opt-e-border);
      padding: 32px;
      margin-bottom: 40px;
      align-items: center;
    }

    .opt-e-figure-img-wrap {
      border: 1px solid var(--opt-e-border);
      background: #FAF8F5;
      padding: 12px;
    }

    .opt-e-figure-img-wrap img {
      width: 100%;
      height: auto;
      display: block;
      object-fit: contain;
    }

    .opt-e-figure-caption {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .opt-e-figure-caption .fig-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--opt-e-accent);
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }

    .opt-e-figure-caption h4 {
      font-family: var(--font-e-serif);
      font-size: 1.45rem;
      font-weight: 600;
      color: var(--opt-e-ink);
      line-height: 1.35;
      word-break: keep-all;
    }

    .opt-e-figure-caption p {
      font-size: 14px;
      line-height: 1.75;
      color: var(--opt-e-ink-secondary);
      word-break: keep-all;
    }

    .opt-e-figure-citation {
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--opt-e-ink-muted);
      border-top: 1px solid var(--opt-e-border-light);
      padding-top: 12px;
    }

    /* SECTION 04: PEOPLE */
    .opt-e-pi-feature {
      display: grid;
      grid-template-columns: 220px 1fr;
      gap: 40px;
      background: var(--opt-e-surface);
      border: 1px solid var(--opt-e-border);
      padding: 32px;
      margin-bottom: 40px;
      align-items: center;
    }

    .opt-e-pi-feature img {
      width: 100%;
      height: 260px;
      object-fit: cover;
      object-position: top;
      border: 1px solid var(--opt-e-border);
      display: block;
    }

    .opt-e-pi-details h4 {
      font-family: var(--font-e-serif);
      font-size: 1.8rem;
      font-weight: 600;
      color: var(--opt-e-ink);
      margin-bottom: 4px;
    }

    .opt-e-pi-details .title-sub {
      font-size: 13.5px;
      color: var(--opt-e-ink-muted);
      margin-bottom: 16px;
    }

    .opt-e-pi-statement {
      font-family: var(--font-e-serif);
      font-size: 16px;
      font-style: italic;
      line-height: 1.8;
      color: var(--opt-e-ink);
      margin-bottom: 16px;
      word-break: keep-all;
    }

    .opt-e-pi-bio {
      font-size: 14px;
      line-height: 1.75;
      color: var(--opt-e-ink-secondary);
      word-break: keep-all;
    }

    .opt-e-fellows-roster {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
    }

    .opt-e-fellow-tile {
      background: var(--opt-e-surface);
      border: 1px solid var(--opt-e-border);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: border-color 0.2s ease;
    }

    .opt-e-fellow-tile:hover {
      border-color: var(--opt-e-accent);
    }

    .opt-e-fellow-tile img {
      width: 100%;
      aspect-ratio: 4/5;
      object-fit: cover;
      object-position: top;
      display: block;
    }

    .opt-e-fellow-name {
      font-family: var(--font-e-serif);
      font-size: 16px;
      font-weight: 600;
      color: var(--opt-e-ink);
    }

    .opt-e-fellow-role {
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--opt-e-accent);
    }

    .opt-e-fellow-focus {
      font-size: 12.5px;
      line-height: 1.55;
      color: var(--opt-e-ink-muted);
      word-break: keep-all;
    }

    /* SECTION 05: PUBLICATIONS */
    .opt-e-pub-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .opt-e-pub-entry {
      background: var(--opt-e-surface);
      border: 1px solid var(--opt-e-border);
      padding: 24px 28px;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 24px;
      align-items: center;
    }

    .opt-e-pub-entry .venue {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.12em;
      color: var(--opt-e-accent);
      text-transform: uppercase;
      margin-bottom: 6px;
    }

    .opt-e-pub-entry h4 {
      font-family: var(--font-e-serif);
      font-size: 1.35rem;
      font-weight: 600;
      color: var(--opt-e-ink);
      line-height: 1.4;
      margin-bottom: 6px;
    }

    .opt-e-pub-entry .authors {
      font-size: 13px;
      color: var(--opt-e-ink-secondary);
      margin-bottom: 8px;
    }

    .opt-e-pub-entry .significance {
      font-size: 13.5px;
      color: var(--opt-e-ink-muted);
      line-height: 1.65;
      word-break: keep-all;
    }

    .opt-e-btn-copy {
      background: transparent;
      border: 1px solid var(--opt-e-border);
      color: var(--opt-e-ink-secondary);
      padding: 8px 14px;
      font-family: var(--font-mono);
      font-size: 11px;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .opt-e-btn-copy:hover {
      border-color: var(--opt-e-accent);
      color: var(--opt-e-accent);
      background: var(--opt-e-tag-bg);
    }

    /* SECTION 06: PROSPECTUS & COLOPHON */
    .opt-e-prospectus {
      padding: 60px 0 100px;
    }

    .opt-e-prospectus-card {
      background: var(--opt-e-surface);
      border: 1px solid var(--opt-e-border);
      padding: 44px 40px;
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 40px;
      align-items: center;
    }

    .opt-e-prospectus-card h4 {
      font-family: var(--font-e-serif);
      font-size: 1.8rem;
      font-weight: 600;
      color: var(--opt-e-ink);
      margin-bottom: 14px;
      word-break: keep-all;
    }

    .opt-e-prospectus-card p {
      font-size: 15px;
      line-height: 1.8;
      color: var(--opt-e-ink-secondary);
      word-break: keep-all;
    }

    .opt-e-prospectus-contact {
      border-left: 1px solid var(--opt-e-border);
      padding-left: 36px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .opt-e-prospectus-contact .label {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--opt-e-ink-muted);
    }

    .opt-e-prospectus-contact a.email {
      font-family: var(--font-mono);
      font-size: 14px;
      color: var(--opt-e-accent);
      text-decoration: none;
      font-weight: 600;
    }

    .opt-e-prospectus-contact .address {
      font-size: 13px;
      line-height: 1.6;
      color: var(--opt-e-ink-secondary);
    }

    /* Responsive Mobile Rules for Option E */
    @media (max-width: 768px) {
      .opt-e-container {
        padding: 0 16px;
      }
      .opt-e-header {
        flex-direction: column;
        gap: 12px;
        align-items: flex-start;
      }
      .opt-e-nav-links {
        display: none;
      }
      .opt-e-hero {
        padding: 40px 0 32px;
      }
      .opt-e-hero-statement {
        font-size: 2.1rem;
        line-height: 1.25;
      }
      .opt-e-hero-sub {
        font-size: 15px;
        line-height: 1.75;
      }
      .opt-e-summary-strip {
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 40px;
      }
      .opt-e-essay-grid {
        grid-template-columns: 1fr;
        gap: 32px;
      }
      .opt-e-inquiry-row {
        grid-template-columns: 1fr;
        gap: 18px;
      }
      .opt-e-figure-plate {
        grid-template-columns: 1fr;
        padding: 20px 16px;
        gap: 20px;
      }
      .opt-e-pi-feature {
        grid-template-columns: 1fr;
        padding: 20px;
        gap: 20px;
      }
      .opt-e-pi-feature img {
        height: 240px;
      }
      .opt-e-fellows-roster {
        grid-template-columns: 1fr 1fr;
        gap: 12px;
      }
      .opt-e-pub-entry {
        grid-template-columns: 1fr;
        padding: 20px 16px;
        gap: 16px;
      }
      .opt-e-prospectus-card {
        grid-template-columns: 1fr;
        padding: 24px 18px;
        gap: 24px;
      }
      .opt-e-prospectus-contact {
        border-left: none;
        border-top: 1px solid var(--opt-e-border);
        padding-left: 0;
        padding-top: 20px;
      }
    }
"""

# 2. Option E Simulator Container Overrides
OPTION_E_SIMULATOR_CSS = """
    /* Simulator Mode Option E */
    #simulator-container .opt-e-container {
      padding: 0 16px !important;
    }
    #simulator-container .opt-e-header {
      flex-direction: column !important;
      gap: 10px !important;
      align-items: flex-start !important;
    }
    #simulator-container .opt-e-nav-links {
      display: none !important;
    }
    #simulator-container .opt-e-hero-statement {
      font-size: 2.1rem !important;
    }
    #simulator-container .opt-e-hero-sub {
      font-size: 14.5px !important;
    }
    #simulator-container .opt-e-summary-strip {
      grid-template-columns: 1fr 1fr !important;
      gap: 14px !important;
    }
    #simulator-container .opt-e-essay-grid {
      grid-template-columns: 1fr !important;
      gap: 24px !important;
    }
    #simulator-container .opt-e-inquiry-row {
      grid-template-columns: 1fr !important;
      gap: 16px !important;
    }
    #simulator-container .opt-e-figure-plate {
      grid-template-columns: 1fr !important;
      padding: 16px !important;
    }
    #simulator-container .opt-e-pi-feature {
      grid-template-columns: 1fr !important;
      padding: 18px !important;
    }
    #simulator-container .opt-e-fellows-roster {
      grid-template-columns: 1fr 1fr !important;
      gap: 10px !important;
    }
    #simulator-container .opt-e-pub-entry {
      grid-template-columns: 1fr !important;
      padding: 16px !important;
    }
    #simulator-container .opt-e-prospectus-card {
      grid-template-columns: 1fr !important;
      padding: 20px !important;
      gap: 20px !important;
    }
    #simulator-container .opt-e-prospectus-contact {
      border-left: none !important;
      border-top: 1px solid var(--opt-e-border) !important;
      padding-left: 0 !important;
      padding-top: 16px !important;
    }
"""

# 3. Option E HTML
OPTION_E_HTML = """
    <!-- =========================================================================
         PROTOTYPE E: QUIET INTELLECTUAL (THE EDITORIAL MONOGRAPH)
         Tone: Restrained, Substantive, Evidence-Grounded, Humanistic Science
         ========================================================================= -->
    <main id="view-option-e" class="prototype-view active">
      <div class="opt-e-container">

        <!-- Navigation Header -->
        <header class="opt-e-header">
          <div class="opt-e-brand-group">
            <span class="opt-e-brand-univ">Seoul National University · Department of Psychology</span>
            <a href="#" class="opt-e-brand-lab">Connectome Laboratory</a>
          </div>

          <nav class="opt-e-nav-links">
            <a href="#opt-e-paradigm">Premise</a>
            <a href="#opt-e-inquiry">Inquiries</a>
            <a href="#opt-e-evidence">Findings</a>
            <a href="#opt-e-fellows">People</a>
            <a href="#opt-e-publications">Papers</a>
            <a href="#opt-e-contact">Contact</a>
          </nav>
        </header>

        <!-- Hero Section -->
        <section class="opt-e-hero">
          <div class="opt-e-hero-eyebrow">Laboratory Prospectus · 2026</div>

          <h2 class="opt-e-hero-statement">
            The brain is not a camera.<br>
            It is a projector, casting <span class="italic">preformed conjectures</span> into the dark.
          </h2>

          <p class="opt-e-hero-sub">
            우리는 100조 개의 시냅스 연결망과 유전체, 4차원 신경 동역학을 통해 인간 마음의 숨은 기하학을 탐구합니다.
            인간을 기계 부품으로 환원하기 위함이 아닙니다. <strong>어둠 속에서 가설을 던지고, 그 가설이 현실과 어긋나 산산조각 나는 순간(예측 오차)에서
            어떻게 배움과 회복탄력성, 그리고 숭고한 경외(Awe)라는 영혼이 피어나는가</strong>를 묻습니다.
          </p>
        </section>

        <!-- Summary Strip -->
        <div class="opt-e-summary-strip">
          <div class="opt-e-summary-item">
            <div class="num">100T</div>
            <div class="label">Synaptic Scale</div>
            <div class="desc">대뇌피질 360개 영역의 위상학적 연결망 기저</div>
          </div>
          <div class="opt-e-summary-item">
            <div class="num">11.8k</div>
            <div class="label">ABCD Cohort</div>
            <div class="desc">유전체(PRS)와 환경이 청소년기 마음에 남기는 10년 종단 궤적</div>
          </div>
          <div class="opt-e-summary-item">
            <div class="num">4D</div>
            <div class="label">Spatiotemporal Models</div>
            <div class="desc">SwiFT와 DIVER를 통한 시계열 뇌 표현 및 개인 식별</div>
          </div>
          <div class="opt-e-summary-item">
            <div class="num">Inside-Out</div>
            <div class="label">Predictive Processing</div>
            <div class="desc">통제된 환각(가설)과 예측 오차를 통한 의식의 발현</div>
          </div>
        </div>

        <!-- SECTION 01: FOUNDATIONAL PREMISE -->
        <section class="opt-e-section" id="opt-e-paradigm">
          <div class="opt-e-section-header">
            <span class="opt-e-section-num">01 / The Foundational Premise</span>
            <h3 class="opt-e-section-title">우리가 탐구하는 근본 질문</h3>
          </div>

          <div class="opt-e-essay-grid">
            <div class="opt-e-essay-col">
              <h3>인사이드-아웃: 뇌는 수동적 수광판이 아니다</h3>
              <p>
                전통적인 신경과학의 외부-내부(Outside-In) 관점은 뇌를 감각 입력을 수동적으로 받아들여 처리하는 카메라로 바라보았습니다.
                그러나 실제 뇌는 자극이 주어지기 전부터 내부에서 스스로 발화 궤적을 만들어내는 <strong>사전 재생(Preplay)의 동역학</strong>을 갖추고 있습니다.
              </p>
              <p>
                피아노 건반의 수가 88개로 유한하더라도 천문학적인 선율을 낳듯이, 뇌는 태어날 때부터 유한한 시냅스 기저 위에서 무수한 가설의 멜로디를 연주합니다.
                우리가 경험하는 현실은 뇌가 칠흑 같은 두개골 속에서 직조하는 <strong>통제된 환각(Controlled Hallucination)</strong>입니다.
              </p>
              <div class="opt-e-pullquote">
                “배움의 유일한 화폐는 예측 오차(Prediction Error)다. 가설이 현실과 부딪혀 박살 나는 순간에서만 뇌는 세계의 지도를 다시 그린다.”
              </div>
            </div>

            <div class="opt-e-essay-col">
              <h3>기계론적 환원을 넘어: 고통과 경외의 생물학적 기저</h3>
              <p>
                도스토옙스키는 《지하생활자의 수기》에서 자연 법칙과 수학으로 인간을 완전히 계산할 수 있다면 인간은 단지 ‘피아노 건반’이나 기계 부품에 불과하지 않은가라고 절규했습니다.
                우리는 이 실존적 긴장을 외면하지 않습니다.
              </p>
              <p>
                우리가 최첨단 4차원 인공지능과 유전체 코호트로 뇌의 생물학적 건반을 해독하는 이유는, 인간을 한낱 기계로 격하하기 위함이 아닙니다.
                오히려 <strong>왜 인간은 우울과 고통에 빠지는가, 왜 불합리하게 타인의 슬픔에 공감하는가, 그리고 왜 예술과 광활한 자연 앞에서 자아를 잊고 전율(Awe)하는가</strong>라는 가장 깊은 물음에 과학의 언어로 정직하게 답하기 위함입니다.
              </p>
              <p>
                우리는 계산신경과학의 엄밀성과 인문학적 성찰이 교차하는 지점에서, 인간 마음의 존엄을 밝히고자 합니다.
              </p>
            </div>
          </div>
        </section>

        <!-- SECTION 02: FOUR CORE RESEARCH INQUIRIES -->
        <section class="opt-e-section" id="opt-e-inquiry">
          <div class="opt-e-section-header">
            <span class="opt-e-section-num">02 / Lines of Inquiry</span>
            <h3 class="opt-e-section-title">네 가지 연구 축</h3>
          </div>

          <div class="opt-e-inquiry-list">
            <!-- Inquiry 01 -->
            <div class="opt-e-inquiry-row">
              <div class="opt-e-inquiry-index">AXIS 01</div>
              <div class="opt-e-inquiry-primary">
                <h4>4차원 시공간 뇌 파운데이션 모델</h4>
                <div class="opt-e-inquiry-question">
                  “시간의 흐름 속에서 신경망의 비선형 궤적은 어떻게 자아의 연속성을 유지하는가?”
                </div>
                <p class="opt-e-inquiry-body">
                  수천 시간의 안정상태 및 자연주의 fMRI와 고해상도 EEG 시계열을 4차원 트랜스포머(SwiFT)와 동역학 모델(DIVER)로 학습합니다.
                  정적인 뇌 지도를 넘어, 시간 축 위에서 스스로 가설을 영사하는 뇌의 동적 궤적을 해독하고 개인 고유의 뇌 지문과 정신건강 바이오마커를 추출합니다.
                </p>
              </div>
              <div class="opt-e-inquiry-spec-block">
                <div class="opt-e-inquiry-spec-item">
                  <div class="meta-label">Methodological Core</div>
                  <div class="meta-val">SwiFT 4D Transformer · DIVER EEG</div>
                </div>
                <div class="opt-e-inquiry-spec-item">
                  <div class="meta-label">Representative Output</div>
                  <div class="meta-val">NeurIPS 2024 (Spotlight) · ICLR 2024</div>
                </div>
              </div>
            </div>

            <!-- Inquiry 02 -->
            <div class="opt-e-inquiry-row">
              <div class="opt-e-inquiry-index">AXIS 02</div>
              <div class="opt-e-inquiry-primary">
                <h4>발달 유전체학과 종단 코호트 인과 추론</h4>
                <div class="opt-e-inquiry-question">
                  “타고난 유전적 악보와 가정·사회 환경의 마찰 속에서, 뇌는 어떻게 상처 입고 회복하는가?”
                </div>
                <p class="opt-e-inquiry-body">
                  미국 국립보건원(NIH) ABCD 연구의 청소년 11,875명을 10년간 종단 추적합니다.
                  다유전자 위험 점수(PRS)와 가족 환경, 신경 영상 데이터를 결합한 다층적 생물학 네트워크를 구축하여, 정신건강의 궤적을 단일 유전자가 아닌 시스템적 마찰과 회복의 관점에서 규명합니다.
                </p>
              </div>
              <div class="opt-e-inquiry-spec-block">
                <div class="opt-e-inquiry-spec-item">
                  <div class="meta-label">Data & Cohort</div>
                  <div class="meta-val">ABCD Study (N=11,875) Longitudinal</div>
                </div>
                <div class="opt-e-inquiry-spec-item">
                  <div class="meta-label">Representative Output</div>
                  <div class="meta-val">Nature Communications 2025 (Lee et al.)</div>
                </div>
              </div>
            </div>

            <!-- Inquiry 03 -->
            <div class="opt-e-inquiry-row">
              <div class="opt-e-inquiry-index">AXIS 03</div>
              <div class="opt-e-inquiry-primary">
                <h4>대뇌피질의 숨겨진 위상 기하학과 양자 매니폴드</h4>
                <div class="opt-e-inquiry-question">
                  “100조 개 시냅스가 빚어내는 대뇌피질의 기하학적 주름에는 어떤 수학적 대칭이 숨어 있는가?”
                </div>
                <p class="opt-e-inquiry-body">
                  Glasser 360 영역 기반 고해상도 피질 두께 데이터와 위상 데이터 분석(TDA), 그리고 양자 상태 커널(Quantum State Kernels)을 융합합니다.
                  고전적 선형 상관관계로는 포착할 수 없는 고차원 뇌 구조 다양체를 기하학적으로 측량합니다.
                </p>
              </div>
              <div class="opt-e-inquiry-spec-block">
                <div class="opt-e-inquiry-spec-item">
                  <div class="meta-label">Approach</div>
                  <div class="meta-val">Glasser 360 Morphometry · Quantum ML</div>
                </div>
                <div class="opt-e-inquiry-spec-item">
                  <div class="meta-label">Domain</div>
                  <div class="meta-val">Topological Data Analysis & Geometry</div>
                </div>
              </div>
            </div>

            <!-- Inquiry 04 -->
            <div class="opt-e-inquiry-row">
              <div class="opt-e-inquiry-index">AXIS 04</div>
              <div class="opt-e-inquiry-primary">
                <h4>자연주의 인지신경학과 경외감(Awe)의 신경미학</h4>
                <div class="opt-e-inquiry-question">
                  “인간은 왜 웅장한 예술과 타인의 고통 앞에서 자아를 잊고 경외감에 젖는가?”
                </div>
                <p class="opt-e-inquiry-body">
                  인위적인 실험실 과제를 넘어, 영화, 음악, 문학적 내러티브에 몰입할 때 일어나는 뇌의 자연스러운 반응을 추적합니다.
                  자아를 표상하는 기본모드신경망(DMN)이 순간적으로 해체되고 세계와 연결되는 '경외(Awe)'의 신경 메커니즘을 규명하여, 예술적 경험이 어떻게 치유의 힘을 갖는지 연구합니다.
                </p>
              </div>
              <div class="opt-e-inquiry-spec-block">
                <div class="opt-e-inquiry-spec-item">
                  <div class="meta-label">Paradigm</div>
                  <div class="meta-val">Naturalistic fMRI · Affective Dynamics</div>
                </div>
                <div class="opt-e-inquiry-spec-item">
                  <div class="meta-label">Target Mechanism</div>
                  <div class="meta-val">DMN Deconstruction & Awe Experience</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- SECTION 03: EMPIRICAL EVIDENCE (FIGURE PLate) -->
        <section class="opt-e-section" id="opt-e-evidence">
          <div class="opt-e-section-header">
            <span class="opt-e-section-num">03 / Empirical Findings</span>
            <h3 class="opt-e-section-title">연구실의 실제 관찰과 데이터</h3>
          </div>

          <div class="opt-e-figure-plate">
            <div class="opt-e-figure-img-wrap">
              <img src="assets/mbbn-figure-2.png" alt="Multi-scale Biological Networks Figure">
            </div>

            <div class="opt-e-figure-caption">
              <span class="fig-tag">FIGURE PLATE · NATURE COMMUNICATIONS 2025</span>
              <h4>다층적 생물학 네트워크를 통한 청소년 정신건강 궤적의 모델링</h4>
              <p>
                단일 유전자나 뇌의 한 영역만으로는 복잡한 인간의 심리적 고통을 설명할 수 없습니다.
                본 연구는 유전체 수준(PRS), 세포 유전자 발현, 구조적 및 기능적 커넥톰의 다층 층위를 하나의 수학적 그래프로 결합하여,
                청소년기 환경 스트레스가 어떻게 뇌의 발달 궤적을 굴절시키는지를 최초로 입증했습니다.
              </p>
              <div class="opt-e-figure-citation">
                Lee, A., Wang, H., Park, D. K., ... & Cha, J.* (2025). <em>Nature Communications</em>.
              </div>
              <div>
                <button class="opt-e-btn-copy copy-bib-btn" data-bib="natcomms25">
                  BibTeX 학술 인용 복사
                </button>
              </div>
            </div>
          </div>

          <div class="opt-e-figure-plate">
            <div class="opt-e-figure-img-wrap" style="background:#0F1115; padding: 24px; text-align: center;">
              <img src="assets/cortical-surface.png" alt="Cortical Surface Topology" style="max-height: 280px; width: auto; margin: 0 auto;">
            </div>

            <div class="opt-e-figure-caption">
              <span class="fig-tag">MORPHOMETRY & TOPOLOGY ATLAS</span>
              <h4>대뇌피질 360개 영역의 고해상도 위상 다양체 측량</h4>
              <p>
                Glasser MMP 1.0 파셀레이션을 바탕으로 재구성한 대뇌피질 표면입니다.
                피질 두께의 국소적 변화와 구조적 공변화 네트워크(Structural Covariance)를 위상 데이터 분석(TDA)과 양자 커널로 분석하여,
                뇌 발달 및 인지 기능 저하의 비선형적 랜드마크를 추출합니다.
              </p>
              <div class="opt-e-figure-citation">
                Connectome Laboratory Morphometry Pipeline · 서울대학교 심리학과
              </div>
            </div>
          </div>
        </section>

        <!-- SECTION 04: PEOPLE -->
        <section class="opt-e-section" id="opt-e-fellows">
          <div class="opt-e-section-header">
            <span class="opt-e-section-num">04 / Investigators</span>
            <h3 class="opt-e-section-title">연구진</h3>
          </div>

          <!-- PI Profile -->
          <div class="opt-e-pi-feature">
            <img src="assets/jiook-cha.jpg" alt="차지욱 교수">
            <div class="opt-e-pi-details">
              <h4>차지욱 (Jiook Cha)</h4>
              <div class="title-sub">서울대학교 심리학과 부교수 · 뇌인지과학과 협동과정 겸무</div>
              <div class="opt-e-pi-statement">
                “우리는 기술을 자랑하기 위해 연구하지 않습니다. 100조 개의 시냅스가 빚어내는 물리적 법칙 속에서 한 인간의 고통을 이해하고 치유할 가능성을 찾기 위해 질문합니다.”
              </div>
              <p class="opt-e-pi-bio">
                컬럼비아 대학교 및 뉴욕 파운틴 하우스 방문 연구원. 계산신경과학, 인공지능 파운데이션 모델, 대규모 종단 코호트 인과 추론을 결합하여
                인간 마음의 구조와 정신건강의 역학을 탐구하고 있습니다.
              </p>
            </div>
          </div>

          <!-- Fellows Roster -->
          <div class="opt-e-fellows-roster">
            <div class="opt-e-fellow-tile">
              <img src="assets/heehwan-wang.jpg" alt="왕희환">
              <div class="opt-e-fellow-name">왕희환 (Heehwan Wang)</div>
              <div class="opt-e-fellow-role">Ph.D. Candidate</div>
              <div class="opt-e-fellow-focus">4D 시공간 파운데이션 모델 (SwiFT) 및 뇌파·fMRI 표현 학습</div>
            </div>

            <div class="opt-e-fellow-tile">
              <img src="assets/ahhyun-lee.jpg" alt="이아현">
              <div class="opt-e-fellow-name">이아현 (Ahhyun Lee)</div>
              <div class="opt-e-fellow-role">Ph.D. Student</div>
              <div class="opt-e-fellow-focus">발달 유전체학(PRS) 및 ABCD 종단 코호트 다층 네트워크 인과 추론</div>
            </div>

            <div class="opt-e-fellow-tile">
              <img src="assets/anna-jung.jpg" alt="정안나">
              <div class="opt-e-fellow-name">정안나 (Anna Jung)</div>
              <div class="opt-e-fellow-role">M.S. Researcher</div>
              <div class="opt-e-fellow-focus">정서신경과학, 자연주의적 fMRI 자극 및 경외감(Awe)의 DMN 동역학</div>
            </div>

            <div class="opt-e-fellow-tile">
              <img src="assets/david-keetae-park.jpg" alt="박기태">
              <div class="opt-e-fellow-name">박기태 (David Keetae Park)</div>
              <div class="opt-e-fellow-role">Researcher</div>
              <div class="opt-e-fellow-focus">시계열 신경망 아키텍처 및 기계학습 기반 뇌 신호 처리 파이프라인</div>
            </div>
          </div>
        </section>

        <!-- SECTION 05: PUBLICATIONS -->
        <section class="opt-e-section" id="opt-e-publications">
          <div class="opt-e-section-header">
            <span class="opt-e-section-num">05 / Selected Publications</span>
            <h3 class="opt-e-section-title">대표 논문</h3>
          </div>

          <div class="opt-e-pub-list">
            <div class="opt-e-pub-entry">
              <div>
                <div class="venue">NATURE COMMUNICATIONS · 2025</div>
                <h4>Multi-scale biological networks encode adolescent mental health dynamics</h4>
                <div class="authors">Ahhyun Lee, Heehwan Wang, David Keetae Park, ... Jiook Cha*</div>
                <div class="significance">
                  유전체 다유전자 점수(PRS)와 fMRI 및 구조적 뇌 연결망을 결합하여, 1만 2천 명 청소년 코호트에서 정신건강 악화와 회복의 인과적 경로를 규명한 연구.
                </div>
              </div>
              <div>
                <button class="opt-e-btn-copy copy-bib-btn" data-bib="natcomms25">
                  BibTeX 복사
                </button>
              </div>
            </div>

            <div class="opt-e-pub-entry">
              <div>
                <div class="venue">NEURIPS · 2024 · SPOTLIGHT</div>
                <h4>SwiFT: Swin 4D fMRI Transformer for Spatiotemporal Brain Representation</h4>
                <div class="authors">Heehwan Wang, David Keetae Park, ... Jiook Cha*</div>
                <div class="significance">
                  정적인 3차원 영상의 한계를 넘어 시간 축을 온전히 학습하는 4차원 윈도우 기반 트랜스포머 아키텍처를 제안하여, 대규모 뇌 시계열 표현 학습의 새로운 표준을 수립.
                </div>
              </div>
              <div>
                <button class="opt-e-btn-copy copy-bib-btn" data-bib="neurips24">
                  BibTeX 복사
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- SECTION 06: PROSPECTUS & CONTACT -->
        <section class="opt-e-prospectus" id="opt-e-contact">
          <div class="opt-e-prospectus-card">
            <div>
              <h4>연구실 참여 안내 (Joining the Lab)</h4>
              <p>
                우리는 계산적 엄밀성(컴퓨터과학, 통계학, 인공지능)과 인간 마음에 대한 깊은 호기심(심리학, 인지과학, 뇌과학)을 겸비한 학부 연구생, 대학원생(석사/박사/통합과정), 박사후연구원을 상시 모집합니다.
                표준화된 정답에 안주하지 않고, 가설이 부딪히는 예측 오차의 틈새에서 진짜 배움을 추구하는 분들의 연락을 환영합니다.
              </p>
            </div>

            <div class="opt-e-prospectus-contact">
              <div class="label">Inquiries & Correspondence</div>
              <a href="mailto:connectome@snu.ac.kr" class="email">connectome@snu.ac.kr</a>
              <div class="label" style="margin-top: 8px;">Location</div>
              <div class="address">
                서울특별시 관악구 관악로 1<br>
                서울대학교 사회과학대학 (16동) 515호 커넥톰 연구실
              </div>
            </div>
          </div>
        </section>

      </div>
    </main>
"""

def apply_option_e():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add Option E to switcher controls and make it active
    # Deactivate other buttons
    html = html.replace('<button class="switcher-btn active" id="btn-show-d">', '<button class="switcher-btn" id="btn-show-d">')
    html = html.replace('<button class="switcher-btn active" id="btn-show-a">', '<button class="switcher-btn" id="btn-show-a">')
    html = html.replace('<button class="switcher-btn active" id="btn-show-b">', '<button class="switcher-btn" id="btn-show-b">')
    html = html.replace('<button class="switcher-btn active" id="btn-show-c">', '<button class="switcher-btn" id="btn-show-c">')

    btn_e_html = '''      <button class="switcher-btn active" id="btn-show-e">
        <span>📖 Option E</span>
        <small style="opacity:0.8;">(Quiet Intellectual)</small>
      </button>'''

    if 'id="btn-show-e"' not in html:
        # insert after btn-show-d
        d_btn_regex = r'(<button class="switcher-btn.*?" id="btn-show-d">[\s\S]*?</button>)'
        html = re.sub(d_btn_regex, r'\1\n' + btn_e_html, html)

    # Switcher meta shortcut keys: 1/2/3/4/5
    html = html.replace('1</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">2</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">3</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">4</kbd>',
                        '1</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">2</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">3</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">4</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">5</kbd>')

    # 2. Add Option E CSS
    if '/* OPTION E: QUIET INTELLECTUAL' not in html:
        html = html.replace('  </style>', OPTION_E_CSS + '\n' + OPTION_E_SIMULATOR_CSS + '\n  </style>')

    # 3. Deactivate view-option-d
    html = html.replace('<main id="view-option-d" class="prototype-view active">', '<main id="view-option-d" class="prototype-view">')

    # 4. Insert Option E HTML
    if 'id="view-option-e"' not in html:
        insert_point = '    </main>\n  </div>\n\n  <!-- Toast -->'
        if insert_point in html:
            replacement = '    </main>\n' + OPTION_E_HTML + '\n  </div>\n\n  <!-- Toast -->'
            html = html.replace(insert_point, replacement, 1)
        else:
            html = html.replace('  </div>\n\n  <!-- Toast -->', OPTION_E_HTML + '\n  </div>\n\n  <!-- Toast -->', 1)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("✓ Updated index.html with Option E")

def apply_script_e():
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        js = f.read()

    # Add btnE and viewE
    old_defs = """  const btnA = document.getElementById('btn-show-a');
  const btnB = document.getElementById('btn-show-b');
  const btnC = document.getElementById('btn-show-c');
  const btnD = document.getElementById('btn-show-d');
  const viewA = document.getElementById('view-option-a');
  const viewB = document.getElementById('view-option-b');
  const viewC = document.getElementById('view-option-c');
  const viewD = document.getElementById('view-option-d');"""

    new_defs = """  const btnA = document.getElementById('btn-show-a');
  const btnB = document.getElementById('btn-show-b');
  const btnC = document.getElementById('btn-show-c');
  const btnD = document.getElementById('btn-show-d');
  const btnE = document.getElementById('btn-show-e');
  const viewA = document.getElementById('view-option-a');
  const viewB = document.getElementById('view-option-b');
  const viewC = document.getElementById('view-option-c');
  const viewD = document.getElementById('view-option-d');
  const viewE = document.getElementById('view-option-e');"""

    if old_defs in js:
        js = js.replace(old_defs, new_defs)

    old_switch = """  function switchView(opt) {
    [btnA, btnB, btnC, btnD].forEach(b => b && b.classList.remove('active'));
    [viewA, viewB, viewC, viewD].forEach(v => v && v.classList.remove('active'));

    if (opt === 'a') {
      btnA.classList.add('active');
      viewA.classList.add('active');
      body.style.background = '#080C14';
      if (typeof window.startCanvasAnimation === 'function') window.startCanvasAnimation();
    } else if (opt === 'b') {
      btnB.classList.add('active');
      viewB.classList.add('active');
      body.style.background = '#F8F9FA';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    } else if (opt === 'c') {
      if (btnC) btnC.classList.add('active');
      if (viewC) viewC.classList.add('active');
      body.style.background = '#0B0F19';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    } else if (opt === 'd') {
      if (btnD) btnD.classList.add('active');
      if (viewD) viewD.classList.add('active');
      body.style.background = '#0D0F14';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    }
  }"""

    new_switch = """  function switchView(opt) {
    [btnA, btnB, btnC, btnD, btnE].forEach(b => b && b.classList.remove('active'));
    [viewA, viewB, viewC, viewD, viewE].forEach(v => v && v.classList.remove('active'));

    if (opt === 'a') {
      btnA.classList.add('active');
      viewA.classList.add('active');
      body.style.background = '#080C14';
      if (typeof window.startCanvasAnimation === 'function') window.startCanvasAnimation();
    } else if (opt === 'b') {
      btnB.classList.add('active');
      viewB.classList.add('active');
      body.style.background = '#F8F9FA';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    } else if (opt === 'c') {
      if (btnC) btnC.classList.add('active');
      if (viewC) viewC.classList.add('active');
      body.style.background = '#0B0F19';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    } else if (opt === 'd') {
      if (btnD) btnD.classList.add('active');
      if (viewD) viewD.classList.add('active');
      body.style.background = '#0D0F14';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    } else if (opt === 'e') {
      if (btnE) btnE.classList.add('active');
      if (viewE) viewE.classList.add('active');
      body.style.background = '#FAF8F5';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    }
  }"""

    if old_switch in js:
        js = js.replace(old_switch, new_switch)

    old_listeners = """  if (btnA) btnA.addEventListener('click', () => switchView('a'));
  if (btnB) btnB.addEventListener('click', () => switchView('b'));
  if (btnC) btnC.addEventListener('click', () => switchView('c'));
  if (btnD) btnD.addEventListener('click', () => switchView('d'));

  window.addEventListener('keydown', (e) => {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
    if (e.key === '1') switchView('a');
    if (e.key === '2') switchView('b');
    if (e.key === '3') switchView('c');
    if (e.key === '4') switchView('d');
  });"""

    new_listeners = """  if (btnA) btnA.addEventListener('click', () => switchView('a'));
  if (btnB) btnB.addEventListener('click', () => switchView('b'));
  if (btnC) btnC.addEventListener('click', () => switchView('c'));
  if (btnD) btnD.addEventListener('click', () => switchView('d'));
  if (btnE) btnE.addEventListener('click', () => switchView('e'));

  window.addEventListener('keydown', (e) => {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
    if (e.key === '1') switchView('a');
    if (e.key === '2') switchView('b');
    if (e.key === '3') switchView('c');
    if (e.key === '4') switchView('d');
    if (e.key === '5') switchView('e');
  });"""

    if old_listeners in js:
        js = js.replace(old_listeners, new_listeners)

    with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(js)
    print("✓ Updated script.js with Option E")

if __name__ == "__main__":
    apply_option_e()
    apply_script_e()
