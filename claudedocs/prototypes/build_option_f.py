#!/usr/bin/env python3
import re
import os

INDEX_PATH = "/home/juke/git/lab-homepage/claudedocs/prototypes/index.html"
SCRIPT_PATH = "/home/juke/git/lab-homepage/claudedocs/prototypes/script.js"

# 1. Option F CSS
OPTION_F_CSS = """
    /* =========================================================================
       OPTION F: THE SOFT LUMINARY (HAUTE EDITORIAL & BESPOKE CRAFTSMANSHIP)
       Aesthetic: Cashmere Alabaster, Soft Camel, Warm Espresso Ink, Silky Curves
       Inspiration: Kinfolk, Hauser & Wirth, Crick Institute, Pentagram Arts
       ========================================================================= */

    :root {
      --opt-f-bg: #F7F5F0;
      --opt-f-surface: #FFFFFF;
      --opt-f-surface-subtle: #FAF9F6;
      --opt-f-ink: #1D1C1A;
      --opt-f-ink-secondary: #524E48;
      --opt-f-ink-muted: #858076;
      --opt-f-border: #E8E4DA;
      --opt-f-border-subtle: #F0EDE5;
      --opt-f-accent: #9A7752; /* Warm Camel / Cashmere Sand */
      --opt-f-accent-dark: #7A5B39;
      --opt-f-accent-soft: rgba(154, 119, 82, 0.08);
      --opt-f-pill-bg: #EFECE5;
      --opt-f-shadow-soft: 0 4px 16px -2px rgba(29, 28, 26, 0.03), 0 16px 40px -4px rgba(29, 28, 26, 0.05);
      --opt-f-shadow-hover: 0 8px 24px -2px rgba(29, 28, 26, 0.04), 0 24px 60px -4px rgba(154, 119, 82, 0.12);
      --font-f-serif: "Newsreader", "Editorial New", "Canela", "Cormorant Garamond", "Didot", "MaruBuri", "Batang", serif;
      --font-f-sans: "Plus Jakarta Sans", "Pretendard Variable", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    #view-option-f {
      background: var(--opt-f-bg);
      color: var(--opt-f-ink);
      font-family: var(--font-f-sans);
      line-height: 1.8;
      position: relative;
      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;
    }

    .opt-f-serif {
      font-family: var(--font-f-serif);
    }

    .opt-f-container {
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 36px;
    }

    /* Ambient Floating Header */
    .opt-f-header {
      padding: 32px 0 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
      border-bottom: 1px solid var(--opt-f-border-subtle);
    }

    .opt-f-brand-block {
      display: flex;
      align-items: center;
      gap: 16px;
      text-decoration: none;
      color: inherit;
    }

    .opt-f-brand-symbol {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-f-serif);
      font-size: 20px;
      color: var(--opt-f-accent);
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .opt-f-brand-text h1 {
      font-family: var(--font-f-serif);
      font-size: 24px;
      font-weight: 600;
      color: var(--opt-f-ink);
      margin: 0;
      letter-spacing: -0.01em;
    }

    .opt-f-brand-text p {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--opt-f-ink-muted);
      margin: 0;
    }

    .opt-f-nav-links {
      display: flex;
      gap: 32px;
    }

    .opt-f-nav-links a {
      font-size: 14px;
      font-weight: 500;
      color: var(--opt-f-ink-secondary);
      text-decoration: none;
      transition: all 0.25s ease;
      letter-spacing: 0.01em;
      position: relative;
    }

    .opt-f-nav-links a::after {
      content: "";
      position: absolute;
      bottom: -4px;
      left: 0;
      width: 0;
      height: 1px;
      background: var(--opt-f-accent);
      transition: width 0.25s ease;
    }

    .opt-f-nav-links a:hover {
      color: var(--opt-f-ink);
    }

    .opt-f-nav-links a:hover::after {
      width: 100%;
    }

    /* Soft Hero Section */
    .opt-f-hero {
      padding: 80px 0 60px;
      max-width: 980px;
    }

    .opt-f-hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border);
      padding: 6px 16px;
      border-radius: 9999px;
      font-family: var(--font-mono);
      font-size: 11.5px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--opt-f-accent-dark);
      margin-bottom: 28px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    .opt-f-hero-badge-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--opt-f-accent);
    }

    .opt-f-hero-headline {
      font-family: var(--font-f-serif);
      font-size: 3.6rem;
      font-weight: 500;
      line-height: 1.2;
      color: var(--opt-f-ink);
      letter-spacing: -0.025em;
      margin-bottom: 28px;
      word-break: keep-all;
    }

    .opt-f-hero-headline span.italic {
      font-style: italic;
      font-weight: 400;
      color: var(--opt-f-accent);
    }

    .opt-f-hero-lead {
      font-size: 18px;
      line-height: 1.9;
      color: var(--opt-f-ink-secondary);
      word-break: keep-all;
      max-width: 860px;
      margin-bottom: 44px;
    }

    .opt-f-hero-lead strong {
      color: var(--opt-f-ink);
      font-weight: 600;
    }

    /* Tactile Pill Buttons */
    .opt-f-cta-group {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
    }

    .opt-f-btn-primary {
      background: var(--opt-f-ink);
      color: #FFF;
      padding: 14px 30px;
      border-radius: 9999px;
      font-size: 14px;
      font-weight: 500;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 4px 14px rgba(29, 28, 26, 0.15);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .opt-f-btn-primary:hover {
      background: #000;
      transform: translateY(-2px);
      box-shadow: 0 8px 22px rgba(29, 28, 26, 0.22);
    }

    .opt-f-btn-secondary {
      background: var(--opt-f-surface);
      color: var(--opt-f-ink);
      padding: 14px 28px;
      border-radius: 9999px;
      font-size: 14px;
      font-weight: 500;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      border: 1px solid var(--opt-f-border);
      box-shadow: 0 2px 8px rgba(0,0,0,0.02);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .opt-f-btn-secondary:hover {
      border-color: var(--opt-f-accent);
      transform: translateY(-2px);
      color: var(--opt-f-accent-dark);
    }

    /* Soft Metrics Islands */
    .opt-f-metrics-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      margin: 60px 0 90px;
    }

    .opt-f-metric-card {
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border-subtle);
      border-radius: 20px;
      padding: 28px 24px;
      box-shadow: var(--opt-f-shadow-soft);
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .opt-f-metric-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--opt-f-shadow-hover);
      border-color: var(--opt-f-border);
    }

    .opt-f-metric-num {
      font-family: var(--font-f-serif);
      font-size: 2.6rem;
      font-weight: 500;
      color: var(--opt-f-ink);
      line-height: 1;
      margin-bottom: 12px;
      letter-spacing: -0.02em;
    }

    .opt-f-metric-num span.unit {
      font-size: 1.5rem;
      color: var(--opt-f-accent);
      margin-left: 2px;
    }

    .opt-f-metric-title {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--opt-f-ink);
      margin-bottom: 4px;
    }

    .opt-f-metric-desc {
      font-size: 12.5px;
      color: var(--opt-f-ink-muted);
      line-height: 1.55;
    }

    /* SECTIONS */
    .opt-f-section {
      padding: 80px 0;
      border-top: 1px solid var(--opt-f-border-subtle);
    }

    .opt-f-section-head {
      margin-bottom: 50px;
      max-width: 800px;
    }

    .opt-f-section-pill {
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--opt-f-accent);
      background: var(--opt-f-accent-soft);
      padding: 4px 12px;
      border-radius: 9999px;
      margin-bottom: 16px;
    }

    .opt-f-section-title {
      font-family: var(--font-f-serif);
      font-size: 2.5rem;
      font-weight: 500;
      color: var(--opt-f-ink);
      letter-spacing: -0.015em;
      margin-bottom: 16px;
      word-break: keep-all;
    }

    .opt-f-section-desc {
      font-size: 16px;
      line-height: 1.8;
      color: var(--opt-f-ink-secondary);
      word-break: keep-all;
    }

    /* SECTION 01: THE PHILOSOPHICAL ESSAY (THE SOFT SANCTUARY) */
    .opt-f-essay-container {
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border);
      border-radius: 24px;
      padding: 56px 60px;
      box-shadow: var(--opt-f-shadow-soft);
      display: grid;
      grid-template-columns: 1.1fr 1fr;
      gap: 60px;
    }

    .opt-f-essay-block h3 {
      font-family: var(--font-f-serif);
      font-size: 1.75rem;
      font-weight: 600;
      color: var(--opt-f-ink);
      margin-bottom: 20px;
      line-height: 1.3;
      word-break: keep-all;
    }

    .opt-f-essay-block p {
      font-size: 15.5px;
      line-height: 1.9;
      color: var(--opt-f-ink-secondary);
      margin-bottom: 22px;
      word-break: keep-all;
    }

    .opt-f-essay-block p strong {
      color: var(--opt-f-ink);
      font-weight: 600;
    }

    .opt-f-essay-quote {
      border-left: 2px solid var(--opt-f-accent);
      padding: 10px 0 10px 24px;
      font-family: var(--font-f-serif);
      font-size: 18px;
      font-style: italic;
      color: var(--opt-f-ink);
      line-height: 1.75;
      margin: 32px 0;
      word-break: keep-all;
    }

    /* SECTION 02: FOUR RESEARCH AXES (INTERACTIVE SOFT CARDS) */
    .opt-f-filter-bar {
      display: flex;
      gap: 10px;
      margin-bottom: 36px;
      flex-wrap: wrap;
    }

    .opt-f-filter-pill {
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border);
      color: var(--opt-f-ink-secondary);
      padding: 8px 18px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.25s ease;
    }

    .opt-f-filter-pill:hover {
      border-color: var(--opt-f-accent);
      color: var(--opt-f-ink);
    }

    .opt-f-filter-pill.active {
      background: var(--opt-f-ink);
      border-color: var(--opt-f-ink);
      color: #FFF;
      box-shadow: 0 4px 12px rgba(29, 28, 26, 0.12);
    }

    .opt-f-axes-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 28px;
    }

    .opt-f-axis-card {
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border);
      border-radius: 24px;
      padding: 40px 36px;
      box-shadow: var(--opt-f-shadow-soft);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .opt-f-axis-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--opt-f-shadow-hover);
      border-color: rgba(154, 119, 82, 0.4);
    }

    .opt-f-axis-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
    }

    .opt-f-axis-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.12em;
      color: var(--opt-f-accent-dark);
      background: var(--opt-f-accent-soft);
      padding: 4px 10px;
      border-radius: 9999px;
      text-transform: uppercase;
    }

    .opt-f-axis-num {
      font-family: var(--font-f-serif);
      font-size: 17px;
      color: var(--opt-f-ink-muted);
      font-style: italic;
    }

    .opt-f-axis-title {
      font-family: var(--font-f-serif);
      font-size: 1.85rem;
      font-weight: 600;
      color: var(--opt-f-ink);
      line-height: 1.25;
      margin-bottom: 12px;
      word-break: keep-all;
    }

    .opt-f-axis-question {
      font-family: var(--font-f-serif);
      font-style: italic;
      font-size: 15.5px;
      color: var(--opt-f-accent-dark);
      line-height: 1.6;
      margin-bottom: 18px;
      word-break: keep-all;
    }

    .opt-f-axis-body {
      font-size: 14.5px;
      line-height: 1.85;
      color: var(--opt-f-ink-secondary);
      margin-bottom: 28px;
      word-break: keep-all;
    }

    .opt-f-axis-footer {
      border-top: 1px solid var(--opt-f-border-subtle);
      padding-top: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .opt-f-axis-output-badge {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--opt-f-ink-muted);
    }

    .opt-f-axis-link {
      font-size: 13px;
      font-weight: 600;
      color: var(--opt-f-ink);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: color 0.2s ease;
    }

    .opt-f-axis-link:hover {
      color: var(--opt-f-accent);
    }

    /* SECTION 03: THE MUSEUM FIGURE WALL */
    .opt-f-museum-wall {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 32px;
    }

    .opt-f-museum-plate {
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border);
      border-radius: 24px;
      padding: 32px;
      box-shadow: var(--opt-f-shadow-soft);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .opt-f-museum-plate:hover {
      transform: translateY(-3px);
      box-shadow: var(--opt-f-shadow-hover);
    }

    .opt-f-museum-matting {
      background: #FAF8F5;
      border: 1px solid var(--opt-f-border-subtle);
      border-radius: 16px;
      padding: 24px;
      text-align: center;
      margin-bottom: 24px;
    }

    .opt-f-museum-matting img {
      max-height: 240px;
      width: auto;
      max-width: 100%;
      object-fit: contain;
      display: block;
      margin: 0 auto;
      border-radius: 8px;
    }

    .opt-f-museum-plate-caption .curatorial-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--opt-f-accent);
      letter-spacing: 0.14em;
      text-transform: uppercase;
      margin-bottom: 8px;
      display: block;
    }

    .opt-f-museum-plate-caption h4 {
      font-family: var(--font-f-serif);
      font-size: 1.55rem;
      font-weight: 600;
      color: var(--opt-f-ink);
      line-height: 1.35;
      margin-bottom: 12px;
      word-break: keep-all;
    }

    .opt-f-museum-plate-caption p {
      font-size: 14px;
      line-height: 1.8;
      color: var(--opt-f-ink-secondary);
      word-break: keep-all;
      margin-bottom: 20px;
    }

    .opt-f-museum-footer {
      border-top: 1px solid var(--opt-f-border-subtle);
      padding-top: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .opt-f-museum-source {
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--opt-f-ink-muted);
    }

    /* SECTION 04: PEOPLE (WARM SANCTUARY ROSTER) */
    .opt-f-pi-banner {
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border);
      border-radius: 24px;
      padding: 44px;
      box-shadow: var(--opt-f-shadow-soft);
      display: grid;
      grid-template-columns: 240px 1fr;
      gap: 48px;
      align-items: center;
      margin-bottom: 40px;
    }

    .opt-f-pi-img-wrap {
      border-radius: 20px;
      overflow: hidden;
      border: 1px solid var(--opt-f-border);
      box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }

    .opt-f-pi-img-wrap img {
      width: 100%;
      height: 280px;
      object-fit: cover;
      object-position: top;
      display: block;
    }

    .opt-f-pi-title-block h4 {
      font-family: var(--font-f-serif);
      font-size: 2.1rem;
      font-weight: 600;
      color: var(--opt-f-ink);
      margin-bottom: 6px;
    }

    .opt-f-pi-title-block .role {
      font-size: 14px;
      color: var(--opt-f-accent-dark);
      font-weight: 500;
      margin-bottom: 20px;
    }

    .opt-f-pi-quote {
      font-family: var(--font-f-serif);
      font-size: 17px;
      font-style: italic;
      color: var(--opt-f-ink);
      line-height: 1.8;
      margin-bottom: 16px;
      word-break: keep-all;
    }

    .opt-f-pi-narrative {
      font-size: 14.5px;
      line-height: 1.8;
      color: var(--opt-f-ink-secondary);
      word-break: keep-all;
    }

    .opt-f-fellows-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
    }

    .opt-f-fellow-card {
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border-subtle);
      border-radius: 20px;
      padding: 20px;
      box-shadow: var(--opt-f-shadow-soft);
      display: flex;
      flex-direction: column;
      gap: 14px;
      transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .opt-f-fellow-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--opt-f-shadow-hover);
      border-color: var(--opt-f-border);
    }

    .opt-f-fellow-img-wrap {
      border-radius: 14px;
      overflow: hidden;
      aspect-ratio: 4/5;
      background: #FAF8F5;
    }

    .opt-f-fellow-img-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top;
      display: block;
    }

    .opt-f-fellow-name {
      font-family: var(--font-f-serif);
      font-size: 17px;
      font-weight: 600;
      color: var(--opt-f-ink);
    }

    .opt-f-fellow-role {
      font-family: var(--font-mono);
      font-size: 10.5px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--opt-f-accent);
    }

    .opt-f-fellow-focus {
      font-size: 13px;
      line-height: 1.65;
      color: var(--opt-f-ink-muted);
      word-break: keep-all;
    }

    /* SECTION 05: PUBLICATIONS */
    .opt-f-pub-list {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .opt-f-pub-card {
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border);
      border-radius: 20px;
      padding: 28px 32px;
      box-shadow: var(--opt-f-shadow-soft);
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 28px;
      align-items: center;
      transition: all 0.3s ease;
    }

    .opt-f-pub-card:hover {
      border-color: var(--opt-f-accent);
      box-shadow: var(--opt-f-shadow-hover);
    }

    .opt-f-pub-venue {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.12em;
      font-weight: 600;
      color: var(--opt-f-accent-dark);
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    .opt-f-pub-title {
      font-family: var(--font-f-serif);
      font-size: 1.45rem;
      font-weight: 600;
      color: var(--opt-f-ink);
      line-height: 1.35;
      margin-bottom: 8px;
    }

    .opt-f-pub-authors {
      font-size: 13.5px;
      color: var(--opt-f-ink-secondary);
      margin-bottom: 10px;
    }

    .opt-f-pub-annotation {
      font-size: 14px;
      line-height: 1.7;
      color: var(--opt-f-ink-muted);
      word-break: keep-all;
    }

    .opt-f-btn-pill-copy {
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border);
      color: var(--opt-f-ink-secondary);
      padding: 10px 18px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.25s ease;
      white-space: nowrap;
    }

    .opt-f-btn-pill-copy:hover {
      border-color: var(--opt-f-accent);
      color: var(--opt-f-accent-dark);
      background: var(--opt-f-pill-bg);
      transform: translateY(-1px);
    }

    /* SECTION 06: INVITATION & COLOPHON */
    .opt-f-sanctuary-box {
      background: var(--opt-f-surface);
      border: 1px solid var(--opt-f-border);
      border-radius: 28px;
      padding: 56px 60px;
      box-shadow: var(--opt-f-shadow-soft);
      display: grid;
      grid-template-columns: 1.3fr 1fr;
      gap: 50px;
      align-items: center;
      margin: 40px 0 100px;
    }

    .opt-f-sanctuary-box h4 {
      font-family: var(--font-f-serif);
      font-size: 2.1rem;
      font-weight: 600;
      color: var(--opt-f-ink);
      line-height: 1.3;
      margin-bottom: 18px;
      word-break: keep-all;
    }

    .opt-f-sanctuary-box p {
      font-size: 15.5px;
      line-height: 1.85;
      color: var(--opt-f-ink-secondary);
      word-break: keep-all;
    }

    .opt-f-sanctuary-details {
      border-left: 1px solid var(--opt-f-border);
      padding-left: 44px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .opt-f-sanctuary-details .label {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--opt-f-accent);
    }

    .opt-f-sanctuary-details a.email {
      font-family: var(--font-mono);
      font-size: 15px;
      font-weight: 600;
      color: var(--opt-f-ink);
      text-decoration: none;
      transition: color 0.2s ease;
    }

    .opt-f-sanctuary-details a.email:hover {
      color: var(--opt-f-accent);
    }

    .opt-f-sanctuary-details .location {
      font-size: 13.5px;
      line-height: 1.7;
      color: var(--opt-f-ink-secondary);
    }

    /* Option F Mobile Responsiveness */
    @media (max-width: 768px) {
      .opt-f-container {
        padding: 0 18px;
      }
      .opt-f-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
      }
      .opt-f-nav-links {
        display: none;
      }
      .opt-f-hero {
        padding: 44px 0 36px;
      }
      .opt-f-hero-headline {
        font-size: 2.2rem;
        line-height: 1.25;
      }
      .opt-f-hero-lead {
        font-size: 15.5px;
        line-height: 1.8;
      }
      .opt-f-metrics-grid {
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin: 40px 0 60px;
      }
      .opt-f-metric-card {
        padding: 20px 16px;
      }
      .opt-f-metric-num {
        font-size: 2rem;
      }
      .opt-f-essay-container {
        grid-template-columns: 1fr;
        padding: 28px 20px;
        gap: 32px;
      }
      .opt-f-axes-grid {
        grid-template-columns: 1fr;
        gap: 20px;
      }
      .opt-f-axis-card {
        padding: 28px 22px;
      }
      .opt-f-axis-title {
        font-size: 1.6rem;
      }
      .opt-f-museum-wall {
        grid-template-columns: 1fr;
        gap: 24px;
      }
      .opt-f-pi-banner {
        grid-template-columns: 1fr;
        padding: 24px 20px;
        gap: 24px;
      }
      .opt-f-pi-img-wrap img {
        height: 240px;
      }
      .opt-f-fellows-grid {
        grid-template-columns: 1fr 1fr;
        gap: 14px;
      }
      .opt-f-pub-card {
        grid-template-columns: 1fr;
        padding: 22px 20px;
        gap: 18px;
      }
      .opt-f-sanctuary-box {
        grid-template-columns: 1fr;
        padding: 32px 22px;
        gap: 28px;
      }
      .opt-f-sanctuary-details {
        border-left: none;
        border-top: 1px solid var(--opt-f-border);
        padding-left: 0;
        padding-top: 20px;
      }
    }
"""

# 2. Simulator Mode Overrides for Option F
OPTION_F_SIMULATOR_CSS = """
    /* Simulator Mode Option F */
    #simulator-container .opt-f-container {
      padding: 0 16px !important;
    }
    #simulator-container .opt-f-header {
      flex-direction: column !important;
      align-items: flex-start !important;
      gap: 10px !important;
    }
    #simulator-container .opt-f-nav-links {
      display: none !important;
    }
    #simulator-container .opt-f-hero {
      padding: 36px 0 28px !important;
    }
    #simulator-container .opt-f-hero-headline {
      font-size: 2.1rem !important;
      line-height: 1.25 !important;
    }
    #simulator-container .opt-f-hero-lead {
      font-size: 14.5px !important;
    }
    #simulator-container .opt-f-metrics-grid {
      grid-template-columns: 1fr 1fr !important;
      gap: 12px !important;
      margin: 32px 0 48px !important;
    }
    #simulator-container .opt-f-metric-card {
      padding: 16px 14px !important;
      border-radius: 16px !important;
    }
    #simulator-container .opt-f-metric-num {
      font-size: 1.8rem !important;
    }
    #simulator-container .opt-f-essay-container {
      grid-template-columns: 1fr !important;
      padding: 24px 18px !important;
      gap: 24px !important;
      border-radius: 18px !important;
    }
    #simulator-container .opt-f-axes-grid {
      grid-template-columns: 1fr !important;
      gap: 16px !important;
    }
    #simulator-container .opt-f-axis-card {
      padding: 24px 18px !important;
      border-radius: 18px !important;
    }
    #simulator-container .opt-f-museum-wall {
      grid-template-columns: 1fr !important;
      gap: 18px !important;
    }
    #simulator-container .opt-f-pi-banner {
      grid-template-columns: 1fr !important;
      padding: 20px !important;
      gap: 20px !important;
    }
    #simulator-container .opt-f-pi-img-wrap img {
      height: 220px !important;
    }
    #simulator-container .opt-f-fellows-grid {
      grid-template-columns: 1fr 1fr !important;
      gap: 10px !important;
    }
    #simulator-container .opt-f-pub-card {
      grid-template-columns: 1fr !important;
      padding: 18px !important;
    }
    #simulator-container .opt-f-sanctuary-box {
      grid-template-columns: 1fr !important;
      padding: 24px 18px !important;
      gap: 24px !important;
    }
    #simulator-container .opt-f-sanctuary-details {
      border-left: none !important;
      border-top: 1px solid var(--opt-f-border) !important;
      padding-left: 0 !important;
      padding-top: 16px !important;
    }
"""

# 3. Option F HTML Content
OPTION_F_HTML = """
    <!-- =========================================================================
         PROTOTYPE F: THE SOFT LUMINARY (HAUTE EDITORIAL)
         Subtle Warmth, Bespoke Typography, Organic Softness, Quiet Luxury
         ========================================================================= -->
    <main id="view-option-f" class="prototype-view active">
      <div class="opt-f-container">

        <!-- Ambient Floating Header -->
        <header class="opt-f-header">
          <a href="#" class="opt-f-brand-block">
            <div class="opt-f-brand-symbol">Ψ</div>
            <div class="opt-f-brand-text">
              <h1>Connectome Laboratory</h1>
              <p>Seoul National University · Cognitive Neuroscience</p>
            </div>
          </a>

          <nav class="opt-f-nav-links">
            <a href="#opt-f-philosophy">Premise</a>
            <a href="#opt-f-axes">Inquiries</a>
            <a href="#opt-f-gallery">Figures</a>
            <a href="#opt-f-people">Fellowship</a>
            <a href="#opt-f-treatises">Treatises</a>
            <a href="#opt-f-sanctuary">Contact</a>
          </nav>
        </header>

        <!-- Soft Hero Section -->
        <section class="opt-f-hero">
          <div class="opt-f-hero-badge">
            <span class="opt-f-hero-badge-dot"></span>
            <span>Laboratory Prospectus · 2026 Edition</span>
          </div>

          <h2 class="opt-f-hero-headline">
            The brain is not a camera.<br>
            It is a projector, casting <span class="italic">preformed trajectories</span> into the dark.
          </h2>

          <p class="opt-f-hero-lead">
            우리는 100조 개의 시냅스 연결망과 유전체, 그리고 4차원 신경 동역학을 통해 인간 마음의 숨은 기하학을 탐구합니다.
            인간을 기계 부품으로 환원하기 위함이 아닙니다.
            <strong>어둠 속에서 가설을 던지고, 그 가설이 현실과 어긋나 산산조각 나는 순간(예측 오차)에서
            어떻게 배움과 회복탄력성, 그리고 숭고한 경외(Awe)라는 영혼이 피어나는가</strong>를 묻습니다.
          </p>

          <div class="opt-f-cta-group">
            <a href="#opt-f-axes" class="opt-f-btn-primary">
              <span>Explore 4 Lines of Inquiry</span>
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 14l-7 7m0 0l-7-7m7 7V3"></path></svg>
            </a>
            <a href="#opt-f-gallery" class="opt-f-btn-secondary">
              <span>Curated Research Figures</span>
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"></path></svg>
            </a>
          </div>
        </section>

        <!-- Soft Metrics Islands -->
        <div class="opt-f-metrics-grid">
          <div class="opt-f-metric-card">
            <div class="opt-f-metric-num">100<span class="unit">T</span></div>
            <div>
              <div class="opt-f-metric-title">Synaptic Manifold</div>
              <div class="opt-f-metric-desc">대뇌피질 360개 영역의 위상학적 연결망 기저</div>
            </div>
          </div>

          <div class="opt-f-metric-card">
            <div class="opt-f-metric-num">11.8<span class="unit">k</span></div>
            <div>
              <div class="opt-f-metric-title">ABCD Cohort Lives</div>
              <div class="opt-f-metric-desc">유전체(PRS)와 환경이 마음에 남기는 10년 종단 궤적</div>
            </div>
          </div>

          <div class="opt-f-metric-card">
            <div class="opt-f-metric-num">4<span class="unit">D</span></div>
            <div>
              <div class="opt-f-metric-title">Spatiotemporal Models</div>
              <div class="opt-f-metric-desc">SwiFT와 DIVER를 통한 시계열 뇌 표현 및 개인 식별</div>
            </div>
          </div>

          <div class="opt-f-metric-card">
            <div class="opt-f-metric-num">Inside<span class="unit">-Out</span></div>
            <div>
              <div class="opt-f-metric-title">Predictive Currency</div>
              <div class="opt-f-metric-desc">통제된 환각(가설)과 예측 오차를 통한 의식의 발현</div>
            </div>
          </div>
        </div>

        <!-- SECTION 01: THE PHILOSOPHICAL ESSAY -->
        <section class="opt-f-section" id="opt-f-philosophy">
          <div class="opt-f-section-head">
            <span class="opt-f-section-pill">01 / The Foundational Premise</span>
            <h3 class="opt-f-section-title">우리가 탐구하는 근본 질문</h3>
            <p class="opt-f-section-desc">
              신경과학의 계산적 엄밀성과 실존적 인문학이 교차하는 지점에서 출발합니다.
            </p>
          </div>

          <div class="opt-f-essay-container">
            <div class="opt-f-essay-block">
              <h3>인사이드-아웃: 뇌는 수동적 수광판이 아니다</h3>
              <p>
                전통적인 신경과학의 외부-내부(Outside-In) 관점은 뇌를 외부 세상의 자극을 수동적으로 담는 카메라로 여겼습니다.
                그러나 실제 뇌는 자극이 주어지기 전부터 내부에서 스스로 발화 궤적을 연주하는 <strong>사전 재생(Preplay)의 동역학</strong>을 갖추고 있습니다.
              </p>
              <p>
                피아노 건반의 수가 88개로 유한하더라도 무한한 멜로디를 직조하듯, 뇌는 태어날 때부터 유한한 시냅스 기저 위에서 끊임없이 가설의 선율을 세상에 영사합니다.
                우리가 경험하는 현실은 뇌가 칠흑 같은 두개골 속에서 직조하는 <strong>통제된 환각(Controlled Hallucination)</strong>입니다.
              </p>
              <div class="opt-f-essay-quote">
                “배움의 유일한 화폐는 예측 오차(Prediction Error)다. 가설이 현실과 충돌하여 박살 나는 순간에서만 뇌는 세계의 지도를 다시 쓴다.”
              </div>
            </div>

            <div class="opt-f-essay-block">
              <h3>기계론적 환원을 넘어: 고통과 경외의 생물학적 기저</h3>
              <p>
                도스토옙스키는 《지하생활자의 수기》에서 자연 법칙과 수학으로 인간을 완전히 계산할 수 있다면 인간은 단지 ‘피아노 건반’이나 기계 부품에 불과하지 않은가라고 질문했습니다.
                우리는 이 실존적 긴장을 피하지 않습니다.
              </p>
              <p>
                우리가 4차원 인공지능과 대규모 유전체 코호트로 뇌의 생물학적 건반을 해독하는 이유는 인간을 한낱 기계로 격하하기 위함이 아닙니다.
                오히려 <strong>왜 인간은 깊은 우울과 고통에 빠지는가, 왜 불합리하게 타인의 슬픔에 공감하는가, 그리고 왜 예술과 광활한 자연 앞에서 자아를 잊고 경외(Awe)를 느끼는가</strong>라는 가장 깊은 물음에 과학의 언어로 정직하게 답하기 위함입니다.
              </p>
              <p>
                우리는 계산신경과학의 엄밀성과 인문학적 성찰이 교차하는 지점에서, 인간 마음의 고유한 존엄을 밝히고자 합니다.
              </p>
            </div>
          </div>
        </section>

        <!-- SECTION 02: FOUR RESEARCH AXES (INTERACTIVE FILTERS) -->
        <section class="opt-f-section" id="opt-f-axes">
          <div class="opt-f-section-head">
            <span class="opt-f-section-pill">02 / Lines of Inquiry</span>
            <h3 class="opt-f-section-title">네 가지 연구 축</h3>
            <p class="opt-f-section-desc">
              모든 층위가 유기적으로 상호 연결되어 마음의 숨은 기하학을 완성합니다.
            </p>
          </div>

          <div class="opt-f-filter-bar">
            <button class="opt-f-filter-pill active" data-f-filter="all">All Lines of Inquiry</button>
            <button class="opt-f-filter-pill" data-f-filter="axis-1">4D Spatiotemporal Models</button>
            <button class="opt-f-filter-pill" data-f-filter="axis-2">Developmental Genomics</button>
            <button class="opt-f-filter-pill" data-f-filter="axis-3">Cortical Topology</button>
            <button class="opt-f-filter-pill" data-f-filter="axis-4">Aesthetic & Awe Dynamics</button>
          </div>

          <div class="opt-f-axes-grid">
            <!-- Axis 1 -->
            <div class="opt-f-axis-card" data-f-axis="axis-1">
              <div>
                <div class="opt-f-axis-meta">
                  <span class="opt-f-axis-tag">AXIS 01 · SPATIOTEMPORAL</span>
                  <span class="opt-f-axis-num">§ 01</span>
                </div>
                <h4 class="opt-f-axis-title">4차원 시공간 뇌 파운데이션 모델</h4>
                <div class="opt-f-axis-question">
                  “시간의 흐름 속에서 신경망의 비선형 궤적은 어떻게 자아의 연속성을 유지하는가?”
                </div>
                <p class="opt-f-axis-body">
                  수천 시간의 안정상태 및 자연주의 fMRI와 고해상도 EEG 시계열을 4차원 트랜스포머(SwiFT)와 동역학 모델(DIVER)로 학습합니다.
                  정적인 뇌 지도를 넘어, 시간 축 위에서 스스로 가설을 영사하는 뇌의 동적 궤적을 해독하고 개인 고유의 뇌 지문과 정신건강 바이오마커를 추출합니다.
                </p>
              </div>
              <div class="opt-f-axis-footer">
                <span class="opt-f-axis-output-badge">NeurIPS '24 (Spotlight) · ICLR '24</span>
                <a href="#opt-f-treatises" class="opt-f-axis-link">View Paper →</a>
              </div>
            </div>

            <!-- Axis 2 -->
            <div class="opt-f-axis-card" data-f-axis="axis-2">
              <div>
                <div class="opt-f-axis-meta">
                  <span class="opt-f-axis-tag">AXIS 02 · GENOMICS & COHORT</span>
                  <span class="opt-f-axis-num">§ 02</span>
                </div>
                <h4 class="opt-f-axis-title">발달 유전체학과 종단 코호트 인과 추론</h4>
                <div class="opt-f-axis-question">
                  “타고난 유전적 악보와 환경의 마찰 속에서, 뇌는 어떻게 상처 입고 회복하는가?”
                </div>
                <p class="opt-f-axis-body">
                  미국 국립보건원(NIH) ABCD 연구의 청소년 11,875명을 10년간 종단 추적합니다.
                  다유전자 위험 점수(PRS)와 가족 환경, 신경 영상 데이터를 결합한 다층적 생물학 네트워크를 구축하여, 정신건강의 궤적을 단일 유전자가 아닌 시스템적 마찰과 회복의 관점에서 규명합니다.
                </p>
              </div>
              <div class="opt-f-axis-footer">
                <span class="opt-f-axis-output-badge">Nature Communications '25</span>
                <a href="#opt-f-treatises" class="opt-f-axis-link">View Paper →</a>
              </div>
            </div>

            <!-- Axis 3 -->
            <div class="opt-f-axis-card" data-f-axis="axis-3">
              <div>
                <div class="opt-f-axis-meta">
                  <span class="opt-f-axis-tag">AXIS 03 · TOPOLOGY & GEOMETRY</span>
                  <span class="opt-f-axis-num">§ 03</span>
                </div>
                <h4 class="opt-f-axis-title">대뇌피질의 위상 기하학과 양자 매니폴드</h4>
                <div class="opt-f-axis-question">
                  “100조 개 시냅스가 빚어내는 대뇌피질의 기하학적 주름에는 어떤 수학적 대칭이 숨어 있는가?”
                </div>
                <p class="opt-f-axis-body">
                  Glasser 360 영역 기반 고해상도 피질 두께 데이터와 위상 데이터 분석(TDA), 그리고 양자 상태 커널(Quantum State Kernels)을 융합합니다.
                  고전적 선형 상관관계로는 포착할 수 없는 고차원 뇌 구조 다양체를 기하학적으로 측량합니다.
                </p>
              </div>
              <div class="opt-f-axis-footer">
                <span class="opt-f-axis-output-badge">TDA · Quantum ML Kernels</span>
                <a href="#opt-f-gallery" class="opt-f-axis-link">View Mesh →</a>
              </div>
            </div>

            <!-- Axis 4 -->
            <div class="opt-f-axis-card" data-f-axis="axis-4">
              <div>
                <div class="opt-f-axis-meta">
                  <span class="opt-f-axis-tag">AXIS 04 · NEUROAESTHETICS</span>
                  <span class="opt-f-axis-num">§ 04</span>
                </div>
                <h4 class="opt-f-axis-title">자연주의 인지신경학과 경외감(Awe)의 신경미학</h4>
                <div class="opt-f-axis-question">
                  “인간은 왜 웅장한 예술과 타인의 고통 앞에서 자아를 잊고 경외감에 젖는가?”
                </div>
                <p class="opt-f-axis-body">
                  인위적인 실험실 과제를 넘어, 영화, 음악, 문학적 내러티브에 몰입할 때 일어나는 뇌의 자연스러운 반응을 추적합니다.
                  자아를 표상하는 기본모드신경망(DMN)이 순간적으로 해체되고 세계와 연결되는 '경외(Awe)'의 신경 메커니즘을 규명하여, 예술적 경험이 어떻게 치유의 힘을 갖는지 연구합니다.
                </p>
              </div>
              <div class="opt-f-axis-footer">
                <span class="opt-f-axis-output-badge">Naturalistic fMRI · Affective Science</span>
                <span style="font-size:12px; color:var(--opt-f-accent); font-weight:500;">DMN Dynamics</span>
              </div>
            </div>
          </div>
        </section>

        <!-- SECTION 03: THE MUSEUM FIGURE WALL -->
        <section class="opt-f-section" id="opt-f-gallery">
          <div class="opt-f-section-head">
            <span class="opt-f-section-pill">03 / Curated Figure Wall</span>
            <h3 class="opt-f-section-title">연구실의 실제 관찰과 데이터</h3>
            <p class="opt-f-section-desc">
              데이터의 엄밀함과 시각적 조형미가 결합된 핵심 발견들의 아카이브입니다.
            </p>
          </div>

          <div class="opt-f-museum-wall">
            <!-- Plate 1 -->
            <div class="opt-f-museum-plate">
              <div>
                <div class="opt-f-museum-matting">
                  <img src="assets/mbbn-figure-2.png" alt="Multi-scale Biological Networks Architecture">
                </div>
                <div class="opt-f-museum-plate-caption">
                  <span class="curatorial-tag">FIGURE PLATE · NATURE COMMUNICATIONS 2025</span>
                  <h4>다층적 생물학 네트워크를 통한 청소년 정신건강 궤적의 모델링</h4>
                  <p>
                    단일 유전자나 뇌의 한 영역만으로는 복잡한 인간의 심리적 고통을 설명할 수 없습니다.
                    본 연구는 유전체 수준(PRS), 세포 유전자 발현, 구조적 및 기능적 커넥톰의 다층 층위를 하나의 수학적 그래프로 결합하여,
                    청소년기 환경 스트레스가 어떻게 뇌의 발달 궤적을 굴절시키는지를 최초로 입증했습니다.
                  </p>
                </div>
              </div>
              <div class="opt-f-museum-footer">
                <span class="opt-f-museum-source">Lee, Wang, Park, ... & Cha* (2025)</span>
                <button class="opt-f-btn-pill-copy copy-bib-btn" data-bib="natcomms25">
                  Copy BibTeX
                </button>
              </div>
            </div>

            <!-- Plate 2 -->
            <div class="opt-f-museum-plate">
              <div>
                <div class="opt-f-museum-matting" style="background:#111215;">
                  <img src="assets/cortical-surface.png" alt="Cortical Surface Topology" style="max-height: 220px;">
                </div>
                <div class="opt-f-museum-plate-caption">
                  <span class="curatorial-tag">MORPHOMETRY & TOPOLOGY ATLAS</span>
                  <h4>대뇌피질 360개 영역의 고해상도 위상 다양체 측량</h4>
                  <p>
                    Glasser MMP 1.0 파셀레이션을 바탕으로 재구성한 대뇌피질 표면입니다.
                    피질 두께의 국소적 변화와 구조적 공변화 네트워크(Structural Covariance)를 위상 데이터 분석(TDA)과 양자 커널로 분석하여,
                    뇌 발달 및 인지 기능 저하의 비선형적 랜드마크를 추출합니다.
                  </p>
                </div>
              </div>
              <div class="opt-f-museum-footer">
                <span class="opt-f-museum-source">Connectome Lab Topology Pipeline</span>
                <span style="font-size:12px; color:var(--opt-f-accent); font-weight:500;">Glasser 360 Atlas</span>
              </div>
            </div>
          </div>
        </section>

        <!-- SECTION 04: PEOPLE & FELLOWSHIP -->
        <section class="opt-f-section" id="opt-f-people">
          <div class="opt-f-section-head">
            <span class="opt-f-section-pill">04 / Fellowship</span>
            <h3 class="opt-f-section-title">탐구하는 사람들</h3>
            <p class="opt-f-section-desc">
              신경과학, 인공지능, 심리학, 그리고 인문학적 질문을 함께 나누는 연구진입니다.
            </p>
          </div>

          <!-- PI Banner -->
          <div class="opt-f-pi-banner">
            <div class="opt-f-pi-img-wrap">
              <img src="assets/jiook-cha.jpg" alt="차지욱 교수">
            </div>
            <div>
              <div class="opt-f-pi-title-block">
                <h4>차지욱 (Jiook Cha)</h4>
                <div class="role">서울대학교 심리학과 부교수 · 뇌인지과학과 협동과정 겸무</div>
              </div>
              <div class="opt-f-pi-quote">
                “우리는 기술을 자랑하기 위해 연구하지 않습니다. 100조 개의 시냅스가 빚어내는 물리적 법칙 속에서 한 인간의 고통을 이해하고 치유할 가능성을 찾기 위해 질문합니다.”
              </div>
              <p class="opt-f-pi-narrative">
                컬럼비아 대학교 및 뉴욕 파운틴 하우스 방문 연구원. 계산신경과학, 인공지능 파운데이션 모델, 대규모 종단 코호트 인과 추론을 결합하여
                인간 마음의 구조와 정신건강의 역학을 탐구하고 있습니다.
              </p>
            </div>
          </div>

          <!-- Fellows Grid -->
          <div class="opt-f-fellows-grid">
            <div class="opt-f-fellow-card">
              <div class="opt-f-fellow-img-wrap">
                <img src="assets/heehwan-wang.jpg" alt="왕희환">
              </div>
              <div>
                <div class="opt-f-fellow-name">왕희환 (Heehwan Wang)</div>
                <div class="opt-f-fellow-role">Ph.D. Candidate</div>
                <div class="opt-f-fellow-focus">4D 시공간 파운데이션 모델 (SwiFT) 및 다중 모달 뇌 표현 학습</div>
              </div>
            </div>

            <div class="opt-f-fellow-card">
              <div class="opt-f-fellow-img-wrap">
                <img src="assets/ahhyun-lee.jpg" alt="이아현">
              </div>
              <div>
                <div class="opt-f-fellow-name">이아현 (Ahhyun Lee)</div>
                <div class="opt-f-fellow-role">Ph.D. Student</div>
                <div class="opt-f-fellow-focus">발달 유전체학(PRS) 및 ABCD 종단 코호트 다층 네트워크 인과 추론</div>
              </div>
            </div>

            <div class="opt-f-fellow-card">
              <div class="opt-f-fellow-img-wrap">
                <img src="assets/anna-jung.jpg" alt="정안나">
              </div>
              <div>
                <div class="opt-f-fellow-name">정안나 (Anna Jung)</div>
                <div class="opt-f-fellow-role">M.S. Researcher</div>
                <div class="opt-f-fellow-focus">정서신경과학, 자연주의적 fMRI 자극 및 경외감(Awe)의 DMN 동역학</div>
              </div>
            </div>

            <div class="opt-f-fellow-card">
              <div class="opt-f-fellow-img-wrap">
                <img src="assets/david-keetae-park.jpg" alt="박기태">
              </div>
              <div>
                <div class="opt-f-fellow-name">박기태 (David Keetae Park)</div>
                <div class="opt-f-fellow-role">Researcher</div>
                <div class="opt-f-fellow-focus">시계열 신경망 아키텍처 및 기계학습 기반 대규모 뇌 신호 처리</div>
              </div>
            </div>
          </div>
        </section>

        <!-- SECTION 05: PUBLICATIONS -->
        <section class="opt-f-section" id="opt-f-treatises">
          <div class="opt-f-section-head">
            <span class="opt-f-section-pill">05 / Selected Treatises</span>
            <h3 class="opt-f-section-title">대표 논문</h3>
            <p class="opt-f-section-desc">
              데이터의 엄밀함과 문제의식의 깊이를 함께 담아낸 대표 성과입니다.
            </p>
          </div>

          <div class="opt-f-pub-list">
            <div class="opt-f-pub-card">
              <div>
                <div class="opt-f-pub-venue">NATURE COMMUNICATIONS · 2025 · ARTICLE</div>
                <h4 class="opt-f-pub-title">Multi-scale biological networks encode adolescent mental health dynamics</h4>
                <div class="opt-f-pub-authors">Ahhyun Lee, Heehwan Wang, David Keetae Park, ... Jiook Cha*</div>
                <div class="opt-f-pub-annotation">
                  유전체 다유전자 위험 점수(PRS)와 fMRI 및 구조적 뇌 연결망을 다층 그래프로 결합하여, 1만 2천 명 청소년 코호트에서 정신건강 악화와 회복의 인과적 경로를 규명한 연구.
                </div>
              </div>
              <div>
                <button class="opt-f-btn-pill-copy copy-bib-btn" data-bib="natcomms25">
                  Copy BibTeX
                </button>
              </div>
            </div>

            <div class="opt-f-pub-card">
              <div>
                <div class="opt-f-pub-venue">NEURIPS · 2024 · SPOTLIGHT</div>
                <h4 class="opt-f-pub-title">SwiFT: Swin 4D fMRI Transformer for Spatiotemporal Brain Representation</h4>
                <div class="opt-f-pub-authors">Heehwan Wang, David Keetae Park, ... Jiook Cha*</div>
                <div class="opt-f-pub-annotation">
                  정적인 3차원 영상의 한계를 넘어 시간 축을 온전히 학습하는 4차원 윈도우 기반 트랜스포머 아키텍처를 제안하여, 대규모 뇌 시계열 표현 학습의 새로운 표준을 수립.
                </div>
              </div>
              <div>
                <button class="opt-f-btn-pill-copy copy-bib-btn" data-bib="neurips24">
                  Copy BibTeX
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- SECTION 06: INVITATION & SANCTUARY -->
        <section class="opt-f-sanctuary-box" id="opt-f-sanctuary">
          <div>
            <h4>연구실 참여 안내 (Joining the Fellowship)</h4>
            <p>
              우리는 계산적 엄밀성(컴퓨터과학, 인공지능, 통계학)과 인간 마음에 대한 깊은 호기심(심리학, 인지과학, 뇌과학)을 겸비한 학부 연구생, 대학원생, 박사후연구원을 상시 모집합니다.
              표준화된 정답에 안주하지 않고, 가설이 부딪히는 예측 오차의 틈새에서 진짜 배움을 추구하는 분들의 연락을 환영합니다.
            </p>
          </div>

          <div class="opt-f-sanctuary-details">
            <div class="label">Inquiries & Correspondence</div>
            <a href="mailto:connectome@snu.ac.kr" class="email">connectome@snu.ac.kr</a>
            <div class="label" style="margin-top: 8px;">Location</div>
            <div class="location">
              서울특별시 관악구 관악로 1<br>
              서울대학교 사회과학대학 (16동) 515호 커넥톰 연구실
            </div>
          </div>
        </section>

      </div>
    </main>
"""

def update_files():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add Google Fonts for Newsreader & Plus Jakarta Sans in head
    font_link = '''  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">'''
    
    if 'fonts.googleapis.com/css2?family=Newsreader' not in html:
        html = html.replace('<link rel="icon"', font_link + '\n  <link rel="icon"')

    # 2. Add Button F to Switcher
    # Deactivate other buttons
    html = html.replace('<button class="switcher-btn active" id="btn-show-e">', '<button class="switcher-btn" id="btn-show-e">')
    html = html.replace('<button class="switcher-btn active" id="btn-show-d">', '<button class="switcher-btn" id="btn-show-d">')

    btn_f_html = '''      <button class="switcher-btn active" id="btn-show-f">
        <span>✨ Option F</span>
        <small style="opacity:0.8;">(Soft Luminary)</small>
      </button>'''

    if 'id="btn-show-f"' not in html:
        e_btn_regex = r'(<button class="switcher-btn.*?" id="btn-show-e">[\s\S]*?</button>)'
        html = re.sub(e_btn_regex, r'\1\n' + btn_f_html, html)

    # Update Switcher meta shortcuts: 1/2/3/4/5/6
    html = html.replace('/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">5</kbd>',
                        '/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">5</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">6</kbd>')

    # 3. Add Option F CSS
    if '/* OPTION F: THE SOFT LUMINARY' not in html:
        html = html.replace('  </style>', OPTION_F_CSS + '\n' + OPTION_F_SIMULATOR_CSS + '\n  </style>')

    # 4. Deactivate view-option-e
    html = html.replace('<main id="view-option-e" class="prototype-view active">', '<main id="view-option-e" class="prototype-view">')

    # 5. Insert Option F HTML
    if 'id="view-option-f"' not in html:
        insert_marker = '    </main>\n  </div>\n\n  <!-- Toast -->'
        if insert_marker in html:
            replacement = '    </main>\n' + OPTION_F_HTML + '\n  </div>\n\n  <!-- Toast -->'
            html = html.replace(insert_marker, replacement, 1)
        else:
            html = html.replace('  </div>\n\n  <!-- Toast -->', OPTION_F_HTML + '\n  </div>\n\n  <!-- Toast -->', 1)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("✓ Successfully updated index.html with Option F!")

    # 6. Update script.js
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        js = f.read()

    # Add btnF and viewF
    old_defs = """  const btnE = document.getElementById('btn-show-e');
  const viewA = document.getElementById('view-option-a');"""

    new_defs = """  const btnE = document.getElementById('btn-show-e');
  const btnF = document.getElementById('btn-show-f');
  const viewA = document.getElementById('view-option-a');"""

    if old_defs in js:
        js = js.replace(old_defs, new_defs)

    old_view_defs = """  const viewE = document.getElementById('view-option-e');"""
    new_view_defs = """  const viewE = document.getElementById('view-option-e');
  const viewF = document.getElementById('view-option-f');"""

    if old_view_defs in js:
        js = js.replace(old_view_defs, new_view_defs)

    old_switch = """  function switchView(opt) {
    [btnA, btnB, btnC, btnD, btnE].forEach(b => b && b.classList.remove('active'));
    [viewA, viewB, viewC, viewD, viewE].forEach(v => v && v.classList.remove('active'));"""

    new_switch = """  function switchView(opt) {
    [btnA, btnB, btnC, btnD, btnE, btnF].forEach(b => b && b.classList.remove('active'));
    [viewA, viewB, viewC, viewD, viewE, viewF].forEach(v => v && v.classList.remove('active'));"""

    if old_switch in js:
        js = js.replace(old_switch, new_switch)

    old_case_e = """    } else if (opt === 'e') {
      if (btnE) btnE.classList.add('active');
      if (viewE) viewE.classList.add('active');
      body.style.background = '#FAF8F5';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    }"""

    new_case_f = """    } else if (opt === 'e') {
      if (btnE) btnE.classList.add('active');
      if (viewE) viewE.classList.add('active');
      body.style.background = '#FAF8F5';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    } else if (opt === 'f') {
      if (btnF) btnF.classList.add('active');
      if (viewF) viewF.classList.add('active');
      body.style.background = '#F7F5F0';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    }"""

    if old_case_e in js:
        js = js.replace(old_case_e, new_case_f)

    # Listeners and keys
    if "if (btnF)" not in js:
        js = js.replace("if (btnE) btnE.addEventListener('click', () => switchView('e'));",
                        "if (btnE) btnE.addEventListener('click', () => switchView('e'));\n  if (btnF) btnF.addEventListener('click', () => switchView('f'));")

    if "if (e.key === '6')" not in js:
        js = js.replace("if (e.key === '5') switchView('e');",
                        "if (e.key === '5') switchView('e');\n    if (e.key === '6') switchView('f');")

    # Add Option F Filter Logic
    opt_f_js = """
  // --- 9. Option F Soft Interactive Filters ---
  const fFilterPills = document.querySelectorAll('.opt-f-filter-pill');
  const fAxisCards = document.querySelectorAll('.opt-f-axis-card');

  fFilterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      fFilterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      const filter = pill.getAttribute('data-f-filter');
      fAxisCards.forEach(card => {
        if (filter === 'all' || card.getAttribute('data-f-axis') === filter) {
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
          card.style.display = 'flex';
        } else {
          card.style.opacity = '0.35';
          card.style.transform = 'translateY(2px)';
          card.style.display = 'flex';
        }
      });
    });
  });
"""
    if '/* --- 9. Option F' not in js:
        js = js.replace('})();', opt_f_js + '\n})();')

    with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(js)
    print("✓ Successfully updated script.js with Option F!")

if __name__ == "__main__":
    update_files()
