#!/usr/bin/env python3
import re
import os

INDEX_PATH = "/home/juke/git/lab-homepage/claudedocs/prototypes/index.html"
SCRIPT_PATH = "/home/juke/git/lab-homepage/claudedocs/prototypes/script.js"

# 1. Option D CSS
OPTION_D_CSS = """
    /* =========================================================================
       OPTION D: THE EXISTENTIAL PROJECTOR / DOSTOEVSKIAN SOUL & CONNECTOME
       Aesthetic: Antique Monograph, Dark Umber/Linen, Burnt Gold, Literary Serif
       ========================================================================= */

    :root {
      --opt-d-bg: #0D0F14;
      --opt-d-bg-card: #151821;
      --opt-d-bg-parchment: #F4EFE6;
      --opt-d-text-parchment: #16171B;
      --opt-d-text-main: #E2DDCE;
      --opt-d-text-muted: #9BA1B0;
      --opt-d-gold: #C59341;
      --opt-d-gold-light: #E0AE5E;
      --opt-d-gold-dark: #8E6523;
      --opt-d-crimson: #8C2E2E;
      --opt-d-border: rgba(197, 147, 65, 0.25);
      --opt-d-border-subtle: rgba(255, 255, 255, 0.08);
      --font-d-serif: "Cormorant Garamond", "Didot", "Baskerville", "Bodoni MT", "Georgia", "MaruBuri", "Batang", serif;
    }

    #view-option-d {
      background: var(--opt-d-bg);
      color: var(--opt-d-text-main);
      font-family: var(--font-sans);
      line-height: 1.7;
      position: relative;
    }

    .opt-d-serif {
      font-family: var(--font-d-serif);
    }

    .opt-d-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 28px;
    }

    /* Dual Rule Ornamental Line */
    .opt-d-dual-rule {
      border: none;
      height: 3px;
      border-top: 1px solid var(--opt-d-gold);
      border-bottom: 1px solid var(--opt-d-gold);
      margin: 40px 0;
      opacity: 0.6;
    }

    /* Masthead Header */
    .opt-d-masthead {
      padding: 28px 0 20px;
      border-bottom: 1px solid var(--opt-d-border);
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .opt-d-top-ribbon {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--opt-d-gold);
      padding-bottom: 10px;
      border-bottom: 1px dashed rgba(197, 147, 65, 0.2);
    }

    .opt-d-main-nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }

    .opt-d-logo-block {
      display: flex;
      align-items: center;
      gap: 16px;
      text-decoration: none;
      color: inherit;
    }

    .opt-d-logo-seal {
      width: 44px;
      height: 44px;
      border: 1px solid var(--opt-d-gold);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(197, 147, 65, 0.08);
      color: var(--opt-d-gold-light);
      font-family: var(--font-d-serif);
      font-size: 20px;
      font-style: italic;
    }

    .opt-d-title-group h1 {
      font-family: var(--font-d-serif);
      font-size: 22px;
      font-weight: 600;
      letter-spacing: 0.04em;
      color: #FFF;
      margin: 0;
    }

    .opt-d-title-group p {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.12em;
      color: var(--opt-d-gold);
      margin: 0;
      text-transform: uppercase;
    }

    .opt-d-nav-chapters {
      display: flex;
      gap: 22px;
      flex-wrap: wrap;
    }

    .opt-d-nav-chapters a {
      color: var(--opt-d-text-muted);
      text-decoration: none;
      font-size: 13px;
      font-weight: 500;
      letter-spacing: 0.04em;
      transition: color 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }

    .opt-d-nav-chapters a:hover {
      color: var(--opt-d-gold-light);
    }

    .opt-d-nav-chapters a span.roman {
      font-family: var(--font-d-serif);
      color: var(--opt-d-gold);
      font-style: italic;
    }

    /* Hero: The Underground & The Projector */
    .opt-d-hero {
      padding: 60px 0 50px;
    }

    /* Epigraph Frame (Dostoevsky x Buzsaki) */
    .opt-d-epigraph-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 48px;
    }

    .opt-d-epigraph-card {
      background: rgba(21, 24, 33, 0.7);
      border: 1px solid var(--opt-d-border);
      padding: 24px 28px;
      position: relative;
      border-radius: 2px;
      box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.4);
    }

    .opt-d-epigraph-card::before {
      content: "❖";
      position: absolute;
      top: -8px;
      left: 20px;
      background: var(--opt-d-bg);
      padding: 0 8px;
      font-size: 10px;
      color: var(--opt-d-gold);
    }

    .opt-d-epigraph-quote {
      font-family: var(--font-d-serif);
      font-size: 16px;
      font-style: italic;
      color: #E6E1D3;
      line-height: 1.8;
      margin-bottom: 14px;
      word-break: keep-all;
    }

    .opt-d-epigraph-author {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--opt-d-gold);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .opt-d-epigraph-author span.src {
      color: var(--opt-d-text-muted);
      text-transform: none;
      font-style: italic;
    }

    /* Hero Statement */
    .opt-d-hero-statement {
      text-align: center;
      max-width: 960px;
      margin: 0 auto 50px;
    }

    .opt-d-hero-tag {
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 12px;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: var(--opt-d-gold);
      margin-bottom: 20px;
      padding: 4px 14px;
      border: 1px solid var(--opt-d-border);
      background: rgba(197, 147, 65, 0.05);
    }

    .opt-d-hero-title {
      font-family: var(--font-d-serif);
      font-size: 3.2rem;
      font-weight: 500;
      line-height: 1.25;
      color: #FFF;
      margin-bottom: 24px;
      letter-spacing: -0.01em;
      word-break: keep-all;
    }

    .opt-d-hero-title span.accent {
      color: var(--opt-d-gold-light);
      font-style: italic;
    }

    .opt-d-hero-desc {
      font-size: 17px;
      line-height: 1.9;
      color: #CBD2DC;
      margin: 0 auto 36px;
      word-break: keep-all;
      max-width: 860px;
    }

    .opt-d-hero-desc strong {
      color: #FFF;
      font-weight: 600;
    }

    /* Monograph Action Row */
    .opt-d-action-row {
      display: flex;
      justify-content: center;
      gap: 18px;
      flex-wrap: wrap;
    }

    .opt-d-btn-archival {
      background: var(--opt-d-gold);
      color: #0E1015;
      padding: 13px 28px;
      font-size: 14px;
      font-weight: 600;
      letter-spacing: 0.04em;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      border: 1px solid var(--opt-d-gold-light);
      box-shadow: 0 4px 20px rgba(197, 147, 65, 0.25);
      transition: all 0.25s ease;
    }

    .opt-d-btn-archival:hover {
      background: var(--opt-d-gold-light);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(197, 147, 65, 0.35);
    }

    .opt-d-btn-outline {
      background: transparent;
      color: #E2DDCE;
      padding: 13px 24px;
      font-size: 14px;
      font-weight: 500;
      letter-spacing: 0.04em;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      border: 1px solid var(--opt-d-border);
      transition: all 0.25s ease;
    }

    .opt-d-btn-outline:hover {
      border-color: var(--opt-d-gold);
      color: var(--opt-d-gold-light);
      background: rgba(197, 147, 65, 0.06);
    }

    /* Monograph Scale Metrics Strip */
    .opt-d-metrics-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1px;
      background: var(--opt-d-border);
      border: 1px solid var(--opt-d-border);
      margin: 48px 0;
    }

    .opt-d-metric-box {
      background: var(--opt-d-bg-card);
      padding: 24px 20px;
      text-align: center;
    }

    .opt-d-metric-num {
      font-family: var(--font-d-serif);
      font-size: 2.5rem;
      font-weight: 600;
      color: var(--opt-d-gold-light);
      line-height: 1.1;
      margin-bottom: 6px;
    }

    .opt-d-metric-title {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #FFF;
      margin-bottom: 4px;
    }

    .opt-d-metric-sub {
      font-size: 12px;
      color: var(--opt-d-text-muted);
    }

    /* SECTION HEADERS */
    .opt-d-section-header {
      text-align: center;
      max-width: 800px;
      margin: 0 auto 48px;
    }

    .opt-d-section-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.2em;
      color: var(--opt-d-gold);
      text-transform: uppercase;
      margin-bottom: 12px;
      display: block;
    }

    .opt-d-section-title {
      font-family: var(--font-d-serif);
      font-size: 2.4rem;
      font-weight: 500;
      color: #FFF;
      margin-bottom: 16px;
      word-break: keep-all;
    }

    .opt-d-section-desc {
      font-size: 15px;
      line-height: 1.8;
      color: var(--opt-d-text-muted);
      word-break: keep-all;
    }

    /* CHAPTER I: DIALECTIC CHAMBER */
    .opt-d-dialectic-chamber {
      background: var(--opt-d-bg-card);
      border: 1px solid var(--opt-d-border);
      padding: 36px;
      margin-bottom: 80px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }

    .opt-d-dialectic-nav {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 32px;
      border-bottom: 1px solid var(--opt-d-border-subtle);
      padding-bottom: 16px;
    }

    .opt-d-dialectic-btn {
      background: transparent;
      border: 1px solid transparent;
      padding: 12px 14px;
      text-align: left;
      cursor: pointer;
      color: var(--opt-d-text-muted);
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .opt-d-dialectic-btn:hover {
      color: #FFF;
      background: rgba(255, 255, 255, 0.02);
    }

    .opt-d-dialectic-btn.active {
      border-color: var(--opt-d-gold);
      background: rgba(197, 147, 65, 0.08);
      color: #FFF;
    }

    .opt-d-dialectic-btn span.num {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--opt-d-gold);
      letter-spacing: 0.1em;
    }

    .opt-d-dialectic-btn span.label {
      font-family: var(--font-d-serif);
      font-size: 15px;
      font-weight: 600;
    }

    .opt-d-dialectic-stage {
      display: grid;
      grid-template-columns: 1fr 1.1fr;
      gap: 36px;
      align-items: center;
    }

    .opt-d-dialectic-visual {
      position: relative;
      border: 1px solid var(--opt-d-border);
      background: #090B10;
      padding: 16px;
    }

    .opt-d-dialectic-visual img {
      width: 100%;
      height: 320px;
      object-fit: cover;
      display: block;
      filter: sepia(0.2) contrast(1.05);
      transition: opacity 0.3s ease;
    }

    .opt-d-dialectic-badge {
      position: absolute;
      bottom: 24px;
      left: 24px;
      background: rgba(13, 15, 20, 0.9);
      border: 1px solid var(--opt-d-gold);
      color: var(--opt-d-gold-light);
      padding: 6px 12px;
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }

    .opt-d-dialectic-content {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .opt-d-dialectic-thesis-label {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--opt-d-gold);
      letter-spacing: 0.15em;
      text-transform: uppercase;
    }

    .opt-d-dialectic-title {
      font-family: var(--font-d-serif);
      font-size: 2.1rem;
      font-weight: 500;
      color: #FFF;
      line-height: 1.3;
      word-break: keep-all;
    }

    .opt-d-dialectic-quote {
      border-left: 2px solid var(--opt-d-gold);
      padding-left: 16px;
      font-family: var(--font-d-serif);
      font-style: italic;
      color: #E2DDCE;
      font-size: 16px;
      line-height: 1.8;
      word-break: keep-all;
    }

    .opt-d-dialectic-desc {
      font-size: 14px;
      line-height: 1.8;
      color: var(--opt-d-text-muted);
      word-break: keep-all;
    }

    .opt-d-dialectic-meta-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--opt-d-border-subtle);
      padding: 14px;
      margin-top: 8px;
    }

    .opt-d-dialectic-meta-item .key {
      font-family: var(--font-mono);
      font-size: 10px;
      color: var(--opt-d-gold);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 2px;
    }

    .opt-d-dialectic-meta-item .val {
      font-size: 13px;
      color: #FFF;
      font-weight: 500;
    }

    /* CHAPTER II: PREDICTION ERROR GYMNASIUM (INTERACTIVE) */
    .opt-d-gym-box {
      background: radial-gradient(circle at 50% 50%, rgba(197, 147, 65, 0.08) 0%, rgba(13, 15, 20, 0.95) 75%);
      border: 1px solid var(--opt-d-border);
      padding: 42px;
      margin-bottom: 80px;
      position: relative;
    }

    .opt-d-gym-slider-wrap {
      max-width: 720px;
      margin: 0 auto 36px;
      text-align: center;
    }

    .opt-d-gym-slider-label {
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--opt-d-gold);
      margin-bottom: 12px;
    }

    .opt-d-gym-slider {
      width: 100%;
      height: 6px;
      -webkit-appearance: none;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
      outline: none;
      cursor: pointer;
    }

    .opt-d-gym-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: var(--opt-d-gold);
      border: 2px solid #FFF;
      cursor: pointer;
      box-shadow: 0 0 15px rgba(197, 147, 65, 0.8);
      transition: transform 0.1s ease;
    }

    .opt-d-gym-slider::-webkit-slider-thumb:hover {
      transform: scale(1.15);
    }

    .opt-d-gym-state-card {
      background: rgba(13, 15, 20, 0.85);
      border: 1px solid var(--opt-d-border);
      padding: 32px;
      max-width: 820px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 30px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
    }

    .opt-d-gym-status-title {
      font-family: var(--font-d-serif);
      font-size: 24px;
      color: #FFF;
      margin-bottom: 8px;
    }

    .opt-d-gym-status-badge {
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 3px 10px;
      border: 1px solid var(--opt-d-gold);
      color: var(--opt-d-gold-light);
      margin-bottom: 14px;
    }

    .opt-d-gym-philosophy-quote {
      font-family: var(--font-d-serif);
      font-style: italic;
      font-size: 16px;
      line-height: 1.8;
      color: #E2DDCE;
      word-break: keep-all;
    }

    .opt-d-gym-neuro-facts {
      border-left: 1px dashed rgba(197, 147, 65, 0.3);
      padding-left: 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .opt-d-gym-fact-item h4 {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--opt-d-gold);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 4px;
    }

    .opt-d-gym-fact-item p {
      font-size: 13px;
      color: var(--opt-d-text-muted);
      line-height: 1.6;
      word-break: keep-all;
    }

    /* CHAPTER III: FOUR MOVEMENTS OF INQUIRY */
    .opt-d-movements-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 28px;
      margin-bottom: 80px;
    }

    .opt-d-movement-card {
      background: var(--opt-d-bg-card);
      border: 1px solid var(--opt-d-border);
      padding: 32px 28px;
      position: relative;
      transition: all 0.3s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .opt-d-movement-card:hover {
      border-color: var(--opt-d-gold);
      transform: translateY(-3px);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
    }

    .opt-d-movement-num {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--opt-d-gold);
      letter-spacing: 0.18em;
      text-transform: uppercase;
      margin-bottom: 12px;
      display: block;
    }

    .opt-d-movement-title {
      font-family: var(--font-d-serif);
      font-size: 1.65rem;
      font-weight: 600;
      color: #FFF;
      line-height: 1.35;
      margin-bottom: 12px;
      word-break: keep-all;
    }

    .opt-d-movement-motto {
      font-family: var(--font-d-serif);
      font-style: italic;
      color: var(--opt-d-gold-light);
      font-size: 14px;
      margin-bottom: 16px;
      display: block;
    }

    .opt-d-movement-desc {
      font-size: 14px;
      line-height: 1.8;
      color: var(--opt-d-text-muted);
      margin-bottom: 24px;
      word-break: keep-all;
    }

    .opt-d-movement-footer {
      border-top: 1px dashed var(--opt-d-border-subtle);
      padding-top: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
    }

    .opt-d-movement-pub-badge {
      font-family: var(--font-mono);
      color: #FFF;
      background: rgba(255, 255, 255, 0.05);
      padding: 4px 10px;
      border: 1px solid var(--opt-d-border-subtle);
    }

    /* CHAPTER IV: PROFESSOR & FELLOWS */
    .opt-d-pi-portrait-card {
      background: var(--opt-d-bg-card);
      border: 1px solid var(--opt-d-border);
      padding: 40px;
      margin-bottom: 48px;
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 40px;
      align-items: center;
    }

    .opt-d-pi-img-frame {
      border: 2px solid var(--opt-d-gold);
      padding: 8px;
      background: #090B10;
      position: relative;
    }

    .opt-d-pi-img-frame img {
      width: 100%;
      height: 340px;
      object-fit: cover;
      display: block;
      filter: sepia(0.2) contrast(1.08);
    }

    .opt-d-pi-caption {
      margin-top: 8px;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--opt-d-gold);
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }

    .opt-d-pi-text-block {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .opt-d-pi-role-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.18em;
      color: var(--opt-d-gold);
      text-transform: uppercase;
    }

    .opt-d-pi-name {
      font-family: var(--font-d-serif);
      font-size: 2.3rem;
      font-weight: 600;
      color: #FFF;
      margin: 0;
    }

    .opt-d-pi-name small {
      font-size: 16px;
      font-weight: 400;
      color: var(--opt-d-text-muted);
      margin-left: 8px;
    }

    .opt-d-pi-manifesto {
      font-family: var(--font-d-serif);
      font-size: 17px;
      font-style: italic;
      color: #E2DDCE;
      line-height: 1.85;
      border-left: 2px solid var(--opt-d-gold);
      padding-left: 20px;
      word-break: keep-all;
    }

    .opt-d-pi-bio {
      font-size: 14px;
      line-height: 1.8;
      color: var(--opt-d-text-muted);
      word-break: keep-all;
    }

    .opt-d-fellows-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
      margin-bottom: 80px;
    }

    .opt-d-fellow-card {
      background: var(--opt-d-bg-card);
      border: 1px solid var(--opt-d-border);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      transition: all 0.25s ease;
    }

    .opt-d-fellow-card:hover {
      border-color: var(--opt-d-gold);
      transform: translateY(-2px);
    }

    .opt-d-fellow-head {
      display: flex;
      gap: 16px;
      align-items: center;
    }

    .opt-d-fellow-head img {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      border: 1px solid var(--opt-d-gold);
      object-fit: cover;
      filter: sepia(0.2) contrast(1.05);
    }

    .opt-d-fellow-name {
      font-family: var(--font-d-serif);
      font-size: 17px;
      font-weight: 600;
      color: #FFF;
    }

    .opt-d-fellow-role {
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.12em;
      color: var(--opt-d-gold);
      text-transform: uppercase;
    }

    .opt-d-fellow-inquiry {
      font-family: var(--font-d-serif);
      font-style: italic;
      font-size: 13.5px;
      line-height: 1.65;
      color: #CBD2DC;
      border-top: 1px dashed var(--opt-d-border-subtle);
      padding-top: 12px;
      word-break: keep-all;
    }

    /* CHAPTER V: ARCHIVAL TREATISES & BIBLIOGRAPHY */
    .opt-d-treatises-list {
      display: flex;
      flex-direction: column;
      gap: 20px;
      margin-bottom: 80px;
    }

    .opt-d-treatise-card {
      background: var(--opt-d-bg-card);
      border: 1px solid var(--opt-d-border);
      padding: 28px 32px;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 24px;
      align-items: center;
      transition: border-color 0.2s ease;
    }

    .opt-d-treatise-card:hover {
      border-color: var(--opt-d-gold);
    }

    .opt-d-treatise-meta {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--opt-d-gold);
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    .opt-d-treatise-title {
      font-family: var(--font-d-serif);
      font-size: 1.4rem;
      font-weight: 600;
      color: #FFF;
      line-height: 1.4;
      margin-bottom: 8px;
    }

    .opt-d-treatise-authors {
      font-size: 13px;
      color: var(--opt-d-text-muted);
      margin-bottom: 12px;
    }

    .opt-d-treatise-commentary {
      font-family: var(--font-d-serif);
      font-style: italic;
      font-size: 14px;
      color: #D6D0C2;
      border-left: 2px solid var(--opt-d-gold);
      padding-left: 14px;
      word-break: keep-all;
      line-height: 1.7;
    }

    /* CHAPTER VI: UNDERGROUND INVITATION & COLOPHON */
    .opt-d-colophon-box {
      background: rgba(197, 147, 65, 0.04);
      border: 1px solid var(--opt-d-border);
      padding: 60px 40px;
      text-align: center;
      margin-bottom: 100px;
      position: relative;
    }

    .opt-d-colophon-ornament {
      font-size: 24px;
      color: var(--opt-d-gold);
      margin-bottom: 20px;
    }

    .opt-d-colophon-title {
      font-family: var(--font-d-serif);
      font-size: 2.2rem;
      font-weight: 500;
      color: #FFF;
      margin-bottom: 20px;
      word-break: keep-all;
    }

    .opt-d-colophon-desc {
      font-size: 16px;
      line-height: 1.9;
      color: #CBD2DC;
      max-width: 780px;
      margin: 0 auto 36px;
      word-break: keep-all;
    }

    .opt-d-colophon-address {
      font-family: var(--font-mono);
      font-size: 12px;
      letter-spacing: 0.12em;
      color: var(--opt-d-gold);
      text-transform: uppercase;
      margin-top: 32px;
      border-top: 1px dashed var(--opt-d-border);
      padding-top: 20px;
      display: inline-block;
    }

    /* Option D Mobile Responsiveness */
    @media (max-width: 768px) {
      .opt-d-epigraph-grid {
        grid-template-columns: 1fr;
      }
      .opt-d-hero-title {
        font-size: 2.1rem;
      }
      .opt-d-metrics-strip {
        grid-template-columns: 1fr 1fr;
      }
      .opt-d-metric-num {
        font-size: 1.4rem;
        word-break: keep-all;
      }
      .opt-d-container {
        padding: 0 16px;
      }
      .opt-d-dialectic-stage {
        grid-template-columns: 1fr;
      }
      .opt-d-dialectic-nav {
        grid-template-columns: repeat(2, 1fr);
      }
      .opt-d-gym-state-card {
        grid-template-columns: 1fr;
      }
      .opt-d-movements-grid {
        grid-template-columns: 1fr;
      }
      .opt-d-pi-portrait-card {
        grid-template-columns: 1fr;
        padding: 24px;
      }
      .opt-d-pi-img-frame img {
        height: 280px;
      }
      .opt-d-fellows-grid {
        grid-template-columns: 1fr;
      }
      .opt-d-treatise-card {
        grid-template-columns: 1fr;
      }
      .opt-d-top-ribbon {
        flex-direction: column;
        gap: 6px;
        align-items: flex-start;
      }
      .opt-d-nav-chapters {
        display: none;
      }
    }
"""

# 2. Option D HTML Content
OPTION_D_HTML = """
    <!-- =========================================================================
         PROTOTYPE D: THE EXISTENTIAL PROJECTOR / DOSTOEVSKIAN SOUL & CONNECTOME
         Philosophy: Jiook Cha x Dostoevsky x Buzsaki Inside-Out
         ========================================================================= -->
    <main id="view-option-d" class="prototype-view active">
      <div class="opt-d-container">

        <!-- Masthead -->
        <header class="opt-d-masthead">
          <div class="opt-d-top-ribbon">
            <span>DE CONJECTURA ET MOTIBUS NEURONUM · VOL. MMXXVI</span>
            <span>SEOUL NATIONAL UNIVERSITY · CONNECTOME LABORATORY</span>
          </div>

          <div class="opt-d-main-nav">
            <a href="#" class="opt-d-logo-block">
              <div class="opt-d-logo-seal">Ψ</div>
              <div class="opt-d-title-group">
                <h1>CONNECTOME LAB</h1>
                <p>Cognitive Neuroscience & Complex Dynamics</p>
              </div>
            </a>

            <nav class="opt-d-nav-chapters">
              <a href="#opt-d-manifesto"><span class="roman">§ I</span> 서문</a>
              <a href="#opt-d-dialectic"><span class="roman">§ II</span> 변증법</a>
              <a href="#opt-d-gymnasium"><span class="roman">§ III</span> 예측오차</a>
              <a href="#opt-d-movements"><span class="roman">§ IV</span> 4대악장</a>
              <a href="#opt-d-inquirers"><span class="roman">§ V</span> 탐구자들</a>
              <a href="#opt-d-treatises"><span class="roman">§ VI</span> 저작</a>
            </nav>
          </div>
        </header>

        <!-- Hero Section -->
        <section class="opt-d-hero" id="opt-d-manifesto">
          <!-- Dual Epigraph (Dostoevsky x Buzsaki) -->
          <div class="opt-d-epigraph-grid">
            <div class="opt-d-epigraph-card">
              <div class="opt-d-epigraph-quote">
                “자연의 법칙과 수학에 의해 인간이 단지 피아노 건반이나 오르간의 핀으로 증명된다면, 인간은 오직 자기가 기계 부품이 아님을 증명하기 위해서라도 스스로 고통과 혼돈을 선택할 것이다. 2×2=4의 차가운 수정궁 안에서 영혼은 숨 쉴 수 없기 때문이다.”
              </div>
              <div class="opt-d-epigraph-author">
                <span>표도르 도스토옙스키</span>
                <span class="src">《지하생활자의 수기》 (1864)</span>
              </div>
            </div>

            <div class="opt-d-epigraph-card">
              <div class="opt-d-epigraph-quote">
                “뇌는 세상의 진실을 수동적으로 기록하는 백지가 아니다. 태어나기 전부터 고유의 내부 동역학을 품고, 어둠 속에서 세상을 향해 가설을 쏘아 올리는 적극적인 탐험가(Active Explorer)다.”
              </div>
              <div class="opt-d-epigraph-author">
                <span>죄르지 부자키</span>
                <span class="src">《The Brain from Inside Out》 (2019)</span>
              </div>
            </div>
          </div>

          <!-- Main Hero Statement -->
          <div class="opt-d-hero-statement">
            <span class="opt-d-hero-tag">THE INSIDE-OUT CONNECTOME MONOGRAPH</span>
            <h2 class="opt-d-hero-title">
              뇌는 카메라가 아니라,<br>
              어둠 속에 가설을 쏘아 올리는 <span class="accent">프로젝터</span>다.
            </h2>
            <p class="opt-d-hero-desc">
              우리가 경험하는 세계는 두개골의 칠흑 같은 암흑 속에서 뇌가 직조해내는 <strong>'통제된 환각(Controlled Hallucination)'</strong>입니다.
              피아노 건반의 수는 유한하지만 무한한 멜로디를 직조하듯, 뇌는 태어날 때부터 <strong>내부 신경 궤적의 사전(Preconfigured Dictionary)</strong>을 품고 있습니다.
              그 투사가 세상과 부딪혀 <strong>산산조각 나는 순간(Prediction Error)</strong> — 그 어긋남의 상처 속에서 비로소 배움과 의식, 그리고 인간의 영혼이 태어납니다.
            </p>

            <div class="opt-d-action-row">
              <a href="#opt-d-dialectic" class="opt-d-btn-archival">
                <span>§ 건반과 궤적의 변증법 탐색</span>
                <span>↓</span>
              </a>
              <a href="#opt-d-gymnasium" class="opt-d-btn-outline">
                <span>§ 예측의 체육관 실험실</span>
                <span>→</span>
              </a>
            </div>
          </div>

          <!-- Monograph Scale Strip -->
          <div class="opt-d-metrics-strip">
            <div class="opt-d-metric-box">
              <div class="opt-d-metric-num">100 Trillion</div>
              <div class="opt-d-metric-title">Synaptic Keys</div>
              <div class="opt-d-metric-sub">유한한 생물학적 건반</div>
            </div>
            <div class="opt-d-metric-box">
              <div class="opt-d-metric-num">4D Spatiotemporal</div>
              <div class="opt-d-metric-title">Foundation Models</div>
              <div class="opt-d-metric-sub">SwiFT · DIVER 내부 궤적</div>
            </div>
            <div class="opt-d-metric-box">
              <div class="opt-d-metric-num">11,875 Lives</div>
              <div class="opt-d-metric-title">ABCD Cohort</div>
              <div class="opt-d-metric-sub">유전체와 발달의 10년 종단</div>
            </div>
            <div class="opt-d-metric-box">
              <div class="opt-d-metric-num">Prediction Error</div>
              <div class="opt-d-metric-title">Currency of Soul</div>
              <div class="opt-d-metric-sub">배움과 의식의 유일한 화폐</div>
            </div>
          </div>
        </section>

        <hr class="opt-d-dual-rule">

        <!-- CHAPTER I: DIALECTIC CHAMBER -->
        <section id="opt-d-dialectic">
          <div class="opt-d-section-header">
            <span class="opt-d-section-tag">CHAPTER I · THE DIALECTIC</span>
            <h3 class="opt-d-section-title">생물학적 건반과 신경 멜로디의 4단계 변증법</h3>
            <p class="opt-d-section-desc">
              도스토옙스키의 질문에서 시작하여 뇌의 4차원 시공간 동역학으로 나아가는 지적 여정입니다.
            </p>
          </div>

          <div class="opt-d-dialectic-chamber">
            <div class="opt-d-dialectic-nav">
              <button class="opt-d-dialectic-btn active" data-d-phase="p1">
                <span class="num">§ 01. THESIS</span>
                <span class="label">건반: 100조 시냅스</span>
              </button>
              <button class="opt-d-dialectic-btn" data-d-phase="p2">
                <span class="num">§ 02. DYNAMICS</span>
                <span class="label">선율: 4D 신경 궤적</span>
              </button>
              <button class="opt-d-dialectic-btn" data-d-phase="p3">
                <span class="num">§ 03. FRACTURE</span>
                <span class="label">균열: 예측 오차</span>
              </button>
              <button class="opt-d-dialectic-btn" data-d-phase="p4">
                <span class="num">§ 04. SUBLIME</span>
                <span class="label">숭고: 경외와 영혼</span>
              </button>
            </div>

            <div class="opt-d-dialectic-stage">
              <div class="opt-d-dialectic-visual">
                <img id="opt-d-stage-img" src="assets/mbbn-figure-2.png" alt="Connectome Dialectic Visualization">
                <div class="opt-d-dialectic-badge" id="opt-d-stage-badge">PHASE 01: THE BIOLOGICAL KEYS</div>
              </div>

              <div class="opt-d-dialectic-content">
                <span class="opt-d-dialectic-thesis-label" id="opt-d-stage-phase">PHASE I · ARCHITECTURE</span>
                <h4 class="opt-d-dialectic-title" id="opt-d-stage-title">유한한 건반과 11,875개의 생애 악보</h4>
                <div class="opt-d-dialectic-quote" id="opt-d-stage-quote">
                  “피아노 건반의 수는 유한하지만, 시간 속에서 배열될 때 천문학적인 멜로디를 낳는다. 우리는 인간을 기계 부품으로 환원하지 않고, 그 건반의 물리학을 해독한다.”
                </div>
                <p class="opt-d-dialectic-desc" id="opt-d-stage-desc">
                  인간의 뇌는 100조 개의 시냅스 연결망과 유전체(PRS)라는 생물학적 기저를 가지고 태어납니다.
                  ABCD 연구의 11,875명 청소년 종단 뇌 영상과 다층적 생물학 네트워크는 환경과의 상호작용 속에서 고통과 회복탄력성이 어떻게 발현되는지를 추적합니다.
                </p>

                <div class="opt-d-dialectic-meta-grid">
                  <div class="opt-d-dialectic-meta-item">
                    <div class="key">Scientific Anchor</div>
                    <div class="val" id="opt-d-stage-meta1">Nature Communications (2025)</div>
                  </div>
                  <div class="opt-d-dialectic-meta-item">
                    <div class="key">Empirical Scope</div>
                    <div class="val" id="opt-d-stage-meta2">Multi-scale Biological Networks</div>
                  </div>
                </div>

                <div style="margin-top: 10px;">
                  <button class="opt-d-btn-outline copy-bib-btn" data-bib="natcomms25" style="padding: 9px 18px; font-size: 12px;">
                    ❦ 학술 인용 (BibTeX) 복사
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <hr class="opt-d-dual-rule">

        <!-- CHAPTER II: PREDICTION ERROR GYMNASIUM (INTERACTIVE) -->
        <section id="opt-d-gymnasium">
          <div class="opt-d-section-header">
            <span class="opt-d-section-tag">CHAPTER II · THE GYMNASIUM OF ERROR</span>
            <h3 class="opt-d-section-title">배움의 화폐는 예측 오차(Prediction Error)다</h3>
            <p class="opt-d-section-desc">
              어둠 속에서 문 손잡이를 찾듯이 — 뇌는 항상 가설을 던집니다. 슬라이더를 움직여 예측 오차의 강도에 따라 뇌와 영혼이 어떻게 반응하는지 확인해 보십시오.
            </p>
          </div>

          <div class="opt-d-gym-box">
            <div class="opt-d-gym-slider-wrap">
              <div class="opt-d-gym-slider-label">
                <span>0% (안전한 맹신)</span>
                <span id="opt-d-slider-val-text" style="color:#FFF; font-weight:600;">50% (최적의 불일치와 각성)</span>
                <span>100% (존재론적 경외)</span>
              </div>
              <input type="range" min="0" max="100" value="50" class="opt-d-gym-slider" id="opt-d-error-slider">
            </div>

            <div class="opt-d-gym-state-card">
              <div>
                <span class="opt-d-gym-status-badge" id="opt-d-gym-badge">OPTIMAL PREDICTION ERROR · 50%</span>
                <h4 class="opt-d-gym-status-title" id="opt-d-gym-title">최적의 불일치: 배움의 화폐 획득</h4>
                <div class="opt-d-gym-philosophy-quote" id="opt-d-gym-quote">
                  “어둠 속에서 문 손잡이가 예상보다 5cm 옆에 있을 때, 그 어긋남의 순간 뇌는 가장 눈부시게 업데이트된다. 가설이 어긋나야만 뇌의 정밀 신경망(Precision Brain)이 깨어난다.”
                </div>
              </div>

              <div class="opt-d-gym-neuro-facts">
                <div class="opt-d-gym-fact-item">
                  <h4>Neural Dynamics</h4>
                  <p id="opt-d-gym-fact-neural">도파민성 예측오차(RPE) 신호 방출. 조용하던 80~90%의 Precision Brain 뉴런이 긴급 동원되어 내부 모델을 재구성합니다.</p>
                </div>
                <div class="opt-d-gym-fact-item">
                  <h4>Dostoevskian Diagnosis</h4>
                  <p id="opt-d-gym-fact-human">기계적 독단과 권태를 깨뜨리는 생명력. 2×2=4의 공식에 안주하지 않고 미지의 세계와 충돌하는 순간입니다.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <hr class="opt-d-dual-rule">

        <!-- CHAPTER III: FOUR MOVEMENTS OF INQUIRY -->
        <section id="opt-d-movements">
          <div class="opt-d-section-header">
            <span class="opt-d-section-tag">CHAPTER III · FOUR MOVEMENTS</span>
            <h3 class="opt-d-section-title">인지신경과학 연구의 네 가지 악장</h3>
            <p class="opt-d-section-desc">
              신경망의 미시적 동역학에서 거시적 인간 고통과 예술적 경외에 이르는 4대 연구 축입니다.
            </p>
          </div>

          <div class="opt-d-movements-grid">
            <!-- Movement 1 -->
            <div class="opt-d-movement-card">
              <div>
                <span class="opt-d-movement-num">MOVEMENT I · THE PROJECTOR</span>
                <h4 class="opt-d-movement-title">4D 시공간 파운데이션 모델</h4>
                <span class="opt-d-movement-motto">“두개골 속 어둠에서 투사되는 4차원 가설의 궤적”</span>
                <p class="opt-d-movement-desc">
                  수천 시간의 fMRI 시계열에서 신경망의 비선형 궤적을 4차원 트랜스포머(SwiFT)로 사전 학습하여 개인 뇌 식별 및 정신건강 바이오마커를 추출합니다. 뇌파(EEG)와 융합한 DIVER 모델로 시간의 흐름 속에서 지속되는 자아의 선율을 추적합니다.
                </p>
              </div>
              <div class="opt-d-movement-footer">
                <span class="opt-d-movement-pub-badge">NeurIPS '24 · ICLR '24</span>
                <button class="opt-d-btn-outline copy-bib-btn" data-bib="neurips24" style="padding:4px 10px; font-size:11px;">BibTeX</button>
              </div>
            </div>

            <!-- Movement 2 -->
            <div class="opt-d-movement-card">
              <div>
                <span class="opt-d-movement-num">MOVEMENT II · INSCRIBED DESTINY</span>
                <h4 class="opt-d-movement-title">발달 유전체와 종단 코호트</h4>
                <span class="opt-d-movement-motto">“새겨진 유전적 악보와 환경이 빚어내는 마찰과 상처”</span>
                <p class="opt-d-movement-desc">
                  ABCD 연구 코호트(N=11,875)를 바탕으로 다유전자 위험 점수(PRS)와 가정·학교·사회 환경이 청소년기 뇌 발달에 미치는 복합적 인과 경로를 규명합니다. 고통과 정신질환의 발생 기저를 해독하여 인간 치유의 토대를 마련합니다.
                </p>
              </div>
              <div class="opt-d-movement-footer">
                <span class="opt-d-movement-pub-badge">Nature Communications '25</span>
                <button class="opt-d-btn-outline copy-bib-btn" data-bib="natcomms25" style="padding:4px 10px; font-size:11px;">BibTeX</button>
              </div>
            </div>

            <!-- Movement 3 -->
            <div class="opt-d-movement-card">
              <div>
                <span class="opt-d-movement-num">MOVEMENT III · GEOMETRY OF MIND</span>
                <h4 class="opt-d-movement-title">피질 위상수학 & 양자 매니폴드</h4>
                <span class="opt-d-movement-motto">“100조 개 시냅스가 빚어내는 피질의 숨겨진 기하학”</span>
                <p class="opt-d-movement-desc">
                  Glasser 360 고해상도 피질 두께 데이터와 양자 상태 커널(Quantum State Kernels)을 결합하여 대뇌피질의 위상학적 다양체를 탐색합니다. 고전 알고리즘을 뛰어넘는 위상 데이터 분석(TDA)으로 뇌 구조의 숨은 대칭성을 규명합니다.
                </p>
              </div>
              <div class="opt-d-movement-footer">
                <span class="opt-d-movement-pub-badge">Quantum ML · Cortical Morphology</span>
                <span style="font-family:var(--font-mono);font-size:11px;color:var(--opt-d-gold);">TDA FRONTIER</span>
              </div>
            </div>

            <!-- Movement 4 -->
            <div class="opt-d-movement-card">
              <div>
                <span class="opt-d-movement-num">MOVEMENT IV · TRANSCENDENT AWE</span>
                <h4 class="opt-d-movement-title">경외감과 감정의 신경미학</h4>
                <span class="opt-d-movement-motto">“인간은 왜 거대한 아름다움 앞에서 자아를 잊고 전율하는가”</span>
                <p class="opt-d-movement-desc">
                  인간이 웅장한 자연, 문학, 예술에 몰입할 때 일어나는 '경외감(Awe)'의 신경 메커니즘과 기본모드신경망(DMN)의 다이내믹한 해체 과정을 실시간 추적합니다. 고통받는 뇌가 왜 예술과 숭고함에서 구원을 찾는가를 과학적으로 응시합니다.
                </p>
              </div>
              <div class="opt-d-movement-footer">
                <span class="opt-d-movement-pub-badge">Affective Science · Naturalistic fMRI</span>
                <span style="font-family:var(--font-mono);font-size:11px;color:var(--opt-d-gold);">AESTHETIC DMN</span>
              </div>
            </div>
          </div>
        </section>

        <hr class="opt-d-dual-rule">

        <!-- CHAPTER IV: PRINCIPAL INVESTIGATOR & INQUIRERS -->
        <section id="opt-d-inquirers">
          <div class="opt-d-section-header">
            <span class="opt-d-section-tag">CHAPTER IV · THE FELLOWSHIP</span>
            <h3 class="opt-d-section-title">어둠 속에서 질문을 던지는 탐구자들</h3>
            <p class="opt-d-section-desc">
              신경과학, 인공지능, 심리학, 그리고 인문학적 사유가 교차하는 연구진입니다.
            </p>
          </div>

          <!-- PI Card -->
          <div class="opt-d-pi-portrait-card">
            <div class="opt-d-pi-img-frame">
              <img src="assets/jiook-cha.jpg" alt="차지욱 교수 (Prof. Jiook Cha)">
              <div class="opt-d-pi-caption">JIOOK CHA, Ph.D. · PI</div>
            </div>

            <div class="opt-d-pi-text-block">
              <span class="opt-d-pi-role-tag">PRINCIPAL INVESTIGATOR · ASSOCIATE PROFESSOR</span>
              <h4 class="opt-d-pi-name">차지욱 <small>Jiook Cha</small></h4>
              <div class="opt-d-pi-manifesto">
                “우리는 기계적인 기술자가 아닙니다. 신경 데이터의 거대한 바다 속에서 인간이라는 미지의 존재를 응시하는 철학자이자 관찰자입니다. 뇌의 물리를 규명하는 일은 인간의 자유를 부정하기 위함이 아니라, 우리가 짊어진 실존적 고통을 이해하고 치유하기 위한 가장 정직한 시도입니다.”
              </div>
              <p class="opt-d-pi-bio">
                서울대학교 심리학과 부교수 및 뇌인지과학과 협동과정 겸무. 컬럼비아 대학교 및 뉴욕 파운틴 하우스 방문 연구원.
                Inside-Out 신경과학과 복잡계 동역학, 대규모 코호트 인과 추론을 결합하여 인간 마음의 근본 원리를 탐구하고 있습니다.
              </p>
            </div>
          </div>

          <!-- Fellows Grid -->
          <div class="opt-d-fellows-grid">
            <div class="opt-d-fellow-card">
              <div class="opt-d-fellow-head">
                <img src="assets/heehwan-wang.jpg" alt="왕희환">
                <div>
                  <div class="opt-d-fellow-name">왕희환 (Heehwan Wang)</div>
                  <div class="opt-d-fellow-role">Ph.D. CANDIDATE</div>
                </div>
              </div>
              <div class="opt-d-fellow-inquiry">
                “시간 축 속에서 자아는 어떻게 흩어지지 않고 하나의 연속된 선율로 유지되는가? 4D 시공간 fMRI 파운데이션 모델 SwiFT를 연구합니다.”
              </div>
            </div>

            <div class="opt-d-fellow-card">
              <div class="opt-d-fellow-head">
                <img src="assets/ahhyun-lee.jpg" alt="이아현">
                <div>
                  <div class="opt-d-fellow-name">이아현 (Ahhyun Lee)</div>
                  <div class="opt-d-fellow-role">Ph.D. STUDENT</div>
                </div>
              </div>
              <div class="opt-d-fellow-inquiry">
                “유전적 취약성과 환경적 상처의 마찰 속에서, 뇌는 어떻게 회복탄력성(Resilience)을 빚어내는가? 다유전자 위험과 종단 뇌 발달을 추적합니다.”
              </div>
            </div>

            <div class="opt-d-fellow-card">
              <div class="opt-d-fellow-head">
                <img src="assets/anna-jung.jpg" alt="정안나">
                <div>
                  <div class="opt-d-fellow-name">정안나 (Anna Jung)</div>
                  <div class="opt-d-fellow-role">M.S. RESEARCHER</div>
                </div>
              </div>
              <div class="opt-d-fellow-inquiry">
                “인간은 왜 슬픔과 아름다움이 교차하는 순간에 경외감(Awe)을 느끼며 구원받는가? 자연주의적 fMRI와 감정의 신경 동역학을 탐구합니다.”
              </div>
            </div>
          </div>
        </section>

        <hr class="opt-d-dual-rule">

        <!-- CHAPTER V: SELECTED TREATISES -->
        <section id="opt-d-treatises">
          <div class="opt-d-section-header">
            <span class="opt-d-section-tag">CHAPTER V · SCHOLARLY TREATISES</span>
            <h3 class="opt-d-section-title">엄선된 학술 저작과 인문학적 주석</h3>
            <p class="opt-d-section-desc">
              데이터의 엄밀성과 철학적 깊이를 함께 담아낸 대표 논문들입니다.
            </p>
          </div>

          <div class="opt-d-treatises-list">
            <div class="opt-d-treatise-card">
              <div>
                <div class="opt-d-treatise-meta">NATURE COMMUNICATIONS · 2025 · ARTICLE</div>
                <h4 class="opt-d-treatise-title">Multi-scale biological networks encode adolescent mental health dynamics</h4>
                <div class="opt-d-treatise-authors">Ahhyun Lee, Heehwan Wang, David Keetae Park, ... Jiook Cha*</div>
                <div class="opt-d-treatise-commentary">
                  “유전자, 뇌세포, 그리고 사회적 환경은 고립된 톱니바퀴가 아닙니다. 1만 2천 명의 생애 궤적 속에서 그들은 서로 얽혀 하나의 비극이자 회복의 노래를 부릅니다.”
                </div>
              </div>
              <div>
                <button class="opt-d-btn-archival copy-bib-btn" data-bib="natcomms25" style="padding:10px 18px; font-size:12px;">
                  ❦ BibTeX 복사
                </button>
              </div>
            </div>

            <div class="opt-d-treatise-card">
              <div>
                <div class="opt-d-treatise-meta">NEURIPS · 2024 · SPOTLIGHT</div>
                <h4 class="opt-d-treatise-title">SwiFT: Swin 4D fMRI Transformer for Spatiotemporal Brain Representation</h4>
                <div class="opt-d-treatise-authors">Heehwan Wang, David Keetae Park, ... Jiook Cha*</div>
                <div class="opt-d-treatise-commentary">
                  “시간 축을 되살려냄으로써, 우리는 비로소 뇌가 세상에 쏘아 올리는 가설의 찰나와 자발적 멜로디의 아름다움을 온전히 응시하기 시작했습니다.”
                </div>
              </div>
              <div>
                <button class="opt-d-btn-archival copy-bib-btn" data-bib="neurips24" style="padding:10px 18px; font-size:12px;">
                  ❦ BibTeX 복사
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- CHAPTER VI: UNDERGROUND INVITATION & COLOPHON -->
        <section class="opt-d-colophon-box">
          <div class="opt-d-colophon-ornament">❦</div>
          <h3 class="opt-d-colophon-title">지하에서 별을 바라보는 이들에게</h3>
          <p class="opt-d-colophon-desc">
            우리는 세상의 표준적인 답안지에 만족하지 못하는 사람들, 인간 마음의 심연과 뇌의 정밀한 수학적 아름다움 사이에서 불면의 밤을 보내는 학생과 연구자를 찾습니다.
            뇌의 물리 법칙에 경외를 느끼며, 동시에 한 인간의 실존적 고통과 문학적 깊이에 가슴 아파할 줄 아는 분들의 지원을 환영합니다.
          </p>

          <div style="display:flex; justify-content:center; gap:16px; flex-wrap:wrap;">
            <a href="mailto:connectome@snu.ac.kr" class="opt-d-btn-archival">
              <span>서신 보내기 (Inquiry & Fellowship)</span>
              <span>✉</span>
            </a>
          </div>

          <div class="opt-d-colophon-address">
            SEOUL NATIONAL UNIVERSITY · COLLEGE OF SOCIAL SCIENCES · BLDG 16, RM 515
          </div>
        </section>

      </div>
    </main>
"""

def update_index_html():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # A. Add button D to switcher
    # Replace the switcher-controls
    button_pattern = r'(<button class="switcher-btn" id="btn-show-c">[\s\S]*?</button>)'
    button_d = '''\\1
      <button class="switcher-btn active" id="btn-show-d">
        <span>❦ Option D</span>
        <small style="opacity:0.8;">(Dostoevsky & Soul)</small>
      </button>'''
    
    # Remove active from btn-show-a
    content = content.replace('<button class="switcher-btn active" id="btn-show-a">', '<button class="switcher-btn" id="btn-show-a">')
    if 'id="btn-show-d"' not in content:
        content = re.sub(button_pattern, button_d, content, count=1)

    # Also update switcher-meta keys text: 1/2/3/4
    content = content.replace('PRESS <kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">1</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">2</kbd> TO SWITCH',
                              'PRESS <kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">1</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">2</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">3</kbd>/<kbd style="background:rgba(255,255,255,0.1);padding:2px 5px;border-radius:3px;">4</kbd> TO SWITCH')

    # B. Insert Option D CSS right before </style>
    if '/* OPTION D:' not in content:
        content = content.replace('  </style>', OPTION_D_CSS + '\n  </style>')

    # C. Remove active from view-option-a, view-option-b, view-option-c
    content = content.replace('<main id="view-option-a" class="prototype-view active">', '<main id="view-option-a" class="prototype-view">')

    # D. Insert Option D HTML right before </div><!-- CONTENT CONTAINER --> or </div>\n\n  <!-- Toast -->
    if 'id="view-option-d"' not in content:
        insert_marker = '    </main>\n  </div>\n\n  <!-- Toast -->'
        if insert_marker in content:
            replacement = '    </main>\n' + OPTION_D_HTML + '\n  </div>\n\n  <!-- Toast -->'
            content = content.replace(insert_marker, replacement, 1)
        else:
            # Fallback
            content = content.replace('  </div>\n\n  <!-- Toast -->', OPTION_D_HTML + '\n  </div>\n\n  <!-- Toast -->', 1)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Successfully updated index.html with Option D!")


def update_script_js():
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Switcher update
    switcher_old = """  const btnA = document.getElementById('btn-show-a');
  const btnB = document.getElementById('btn-show-b');
  const btnC = document.getElementById('btn-show-c');
  const viewA = document.getElementById('view-option-a');
  const viewB = document.getElementById('view-option-b');
  const viewC = document.getElementById('view-option-c');"""

    switcher_new = """  const btnA = document.getElementById('btn-show-a');
  const btnB = document.getElementById('btn-show-b');
  const btnC = document.getElementById('btn-show-c');
  const btnD = document.getElementById('btn-show-d');
  const viewA = document.getElementById('view-option-a');
  const viewB = document.getElementById('view-option-b');
  const viewC = document.getElementById('view-option-c');
  const viewD = document.getElementById('view-option-d');"""

    if switcher_old in content:
        content = content.replace(switcher_old, switcher_new)

    switch_fn_old = """  function switchView(opt) {
    [btnA, btnB, btnC].forEach(b => b && b.classList.remove('active'));
    [viewA, viewB, viewC].forEach(v => v && v.classList.remove('active'));

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
    }
  }"""

    switch_fn_new = """  function switchView(opt) {
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

    if switch_fn_old in content:
        content = content.replace(switch_fn_old, switch_fn_new)

    # Listeners and keys
    listeners_old = """  if (btnA) btnA.addEventListener('click', () => switchView('a'));
  if (btnB) btnB.addEventListener('click', () => switchView('b'));
  if (btnC) btnC.addEventListener('click', () => switchView('c'));

  window.addEventListener('keydown', (e) => {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
    if (e.key === '1') switchView('a');
    if (e.key === '2') switchView('b');
    if (e.key === '3') switchView('c');
  });"""

    listeners_new = """  if (btnA) btnA.addEventListener('click', () => switchView('a'));
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

    if listeners_old in content:
        content = content.replace(listeners_old, listeners_new)

    # Add Option D Dialectic and Prediction Error Slider logic at bottom
    option_d_js = """
  // --- 8. Option D Interactive Dialectic Chamber & Prediction Error Slider ---
  const dPhaseData = {
    p1: {
      phase: 'PHASE I · ARCHITECTURE',
      badge: 'PHASE 01: THE BIOLOGICAL KEYS',
      title: '유한한 건반과 11,875개의 생애 악보',
      quote: '“피아노 건반의 수는 유한하지만, 시간 속에서 배열될 때 천문학적인 멜로디를 낳는다. 우리는 인간을 기계 부품으로 환원하지 않고, 그 건반의 물리학을 해독한다.”',
      desc: '인간의 뇌는 100조 개의 시냅스 연결망과 유전체(PRS)라는 생물학적 기저를 가지고 태어납니다. ABCD 연구의 11,875명 청소년 종단 뇌 영상과 다층적 생물학 네트워크는 환경과의 상호작용 속에서 고통과 회복탄력성이 어떻게 발현되는지를 추적합니다.',
      meta1: 'Nature Communications (2025)',
      meta2: 'Multi-scale Biological Networks',
      img: 'assets/mbbn-figure-2.png'
    },
    p2: {
      phase: 'PHASE II · PREPLAY DYNAMICS',
      badge: 'PHASE 02: THE 4D INTERNAL TRAJECTORY',
      title: '어둠 속에서 연주되는 사전 재생(Preplay)의 선율',
      quote: '“뇌는 세상의 자극이 들어오기 전에 이미 꿈속에서 가설의 궤적을 재생(Preplay)하고 있었다. 우리는 시간 축을 복원하여 이 자발적 멜로디를 포착한다.”',
      desc: '수천 시간의 fMRI 시계열에서 신경망의 비선형 궤적을 4차원 트랜스포머(SwiFT)로 사전 학습합니다. 뇌는 세상을 수동적으로 찍는 카메라가 아니라, 끊임없이 내부 모델을 세계에 쏘아 올리는 프로젝터입니다.',
      meta1: 'NeurIPS 2024 Spotlight',
      meta2: 'SwiFT 4D Transformer / DIVER EEG',
      img: 'assets/cortical-surface.png'
    },
    p3: {
      phase: 'PHASE III · THE FRACTURE',
      badge: 'PHASE 03: PREDICTION ERROR & SURPRISE',
      title: '가설이 박살 나는 순간, 배움의 화폐 획득',
      quote: '“오차가 발생하지 않는다면 뇌는 단 1바이트도 배우지 못한다. 내 가설과 세계가 어긋나 산산조각 나는 고통의 순간에만 정밀 신경망(Precision Brain)이 깨어난다.”',
      desc: '우리가 보는 현실은 통제된 환각(Controlled Hallucination)입니다. 행동을 통해 세계와 부딪히고, 오차가 발생할 때에만 뇌는 비로소 세계에 대한 지도를 업데이트합니다. 예측 오차 0은 학습의 종말이자 뇌의 퇴화입니다.',
      meta1: 'Predictive Processing Engine',
      meta2: 'Mismatch Negativity / Dopaminergic RPE',
      img: 'assets/mbbn-figure-2.png'
    },
    p4: {
      phase: 'PHASE IV · THE SUBLIME',
      badge: 'PHASE 04: TRANSCENDENT AWE & THE SOUL',
      title: '2×2=4를 넘어선 경외와 실존적 영혼',
      quote: '“인간은 피아노 건반이 아니다. 그러나 그 건반의 물리를 이해할 때 비로소 우리는 왜 인간이 예술에 전율하고, 타인의 슬픔에 울며, 숭고한 경외(Awe)에 도달하는지 알 수 있다.”',
      desc: '자연주의적 영화, 음악, 문학에 몰입할 때 일어나는 기본모드신경망(DMN)의 해체와 재조직을 실시간으로 추적합니다. 과학적 결정론의 가장 깊은 밑바닥에서 비로소 피어나는 인간 영혼의 찬란한 존엄성을 응시합니다.',
      meta1: 'Neuroaesthetics & Awe Dynamics',
      meta2: 'Naturalistic fMRI / DMN Topography',
      img: 'assets/cortical-surface.png'
    }
  };

  const dPhaseBtns = document.querySelectorAll('.opt-d-dialectic-btn');
  const dStageImg = document.getElementById('opt-d-stage-img');
  const dStageBadge = document.getElementById('opt-d-stage-badge');
  const dStagePhase = document.getElementById('opt-d-stage-phase');
  const dStageTitle = document.getElementById('opt-d-stage-title');
  const dStageQuote = document.getElementById('opt-d-stage-quote');
  const dStageDesc = document.getElementById('opt-d-stage-desc');
  const dStageMeta1 = document.getElementById('opt-d-stage-meta1');
  const dStageMeta2 = document.getElementById('opt-d-stage-meta2');

  dPhaseBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      dPhaseBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const phaseKey = btn.getAttribute('data-d-phase');
      const data = dPhaseData[phaseKey];
      if (!data) return;

      if (dStageImg) {
        dStageImg.style.opacity = '0.2';
        setTimeout(() => {
          dStageImg.src = data.img;
          dStageImg.style.opacity = '1';
        }, 150);
      }
      if (dStageBadge) dStageBadge.textContent = data.badge;
      if (dStagePhase) dStagePhase.textContent = data.phase;
      if (dStageTitle) dStageTitle.textContent = data.title;
      if (dStageQuote) dStageQuote.textContent = data.quote;
      if (dStageDesc) dStageDesc.textContent = data.desc;
      if (dStageMeta1) dStageMeta1.textContent = data.meta1;
      if (dStageMeta2) dStageMeta2.textContent = data.meta2;
    });
  });

  // Prediction Error Interactive Slider
  const errSlider = document.getElementById('opt-d-error-slider');
  const sliderValText = document.getElementById('opt-d-slider-val-text');
  const gymBadge = document.getElementById('opt-d-gym-badge');
  const gymTitle = document.getElementById('opt-d-gym-title');
  const gymQuote = document.getElementById('opt-d-gym-quote');
  const gymFactNeural = document.getElementById('opt-d-gym-fact-neural');
  const gymFactHuman = document.getElementById('opt-d-gym-fact-human');

  if (errSlider) {
    errSlider.addEventListener('input', (e) => {
      const val = parseInt(e.target.value, 10);
      if (val < 30) {
        sliderValText.textContent = `${val}% (안전한 맹신과 권태)`;
        gymBadge.textContent = 'PREDICTION ERROR = 0% · COGNITIVE STAGNATION';
        gymTitle.textContent = '안전한 독단: 배움 0 = 뇌의 퇴화';
        gymQuote.textContent = '“수정궁 안에서 모든 것이 계산되었을 때 인간은 권태로 죽어간다. 가설 없이 답만 받아쓰는 뇌는 단 1바이트도 업데이트되지 않는다.”';
        gymFactNeural.textContent = 'Precision Brain 0% 가동. 도파민성 예측오차 신호 침묵. 시냅스 가소성(LTP) 정체.';
        gymFactHuman.textContent = '도스토옙스키의 경고: 인간이 피아노 건반이나 톱니바퀴로 환원되어 자율적 질문을 멈춘 상태.';
      } else if (val <= 75) {
        sliderValText.textContent = `${val}% (최적의 불일치와 각성)`;
        gymBadge.textContent = `OPTIMAL PREDICTION ERROR · ${val}%`;
        gymTitle.textContent = '최적의 불일치: 배움의 화폐 획득';
        gymQuote.textContent = '“어둠 속에서 문 손잡이가 예상보다 5cm 옆에 있을 때, 그 어긋남의 순간 뇌는 가장 눈부시게 업데이트된다. 가설이 어긋나야만 뇌의 정밀 신경망(Precision Brain)이 깨어난다.”';
        gymFactNeural.textContent = '도파민성 예측오차(RPE) 급증. 80~90%의 침묵하던 Precision Brain 뉴런이 전면 동원되어 내부 지도를 재구성.';
        gymFactHuman.textContent = '질문을 던지는 행동만이 유일한 학습이다. 통제된 환각이 현실과 부딪혀 새로운 의식이 탄생하는 지점.';
      } else {
        sliderValText.textContent = `${val}% (존재론적 경외와 충격)`;
        gymBadge.textContent = `RADICAL PREDICTION ERROR · ${val}%`;
        gymTitle.textContent = '실존적 경외: 세계 모델의 전면적 해체';
        gymQuote.textContent = '“고통과 경외야말로 의식의 유일한 원천이다. 거대한 예술과 실존적 충격 앞에서 나의 낡은 자아가 산산조각 날 때 영혼은 비로소 자유로워진다.”';
        gymFactNeural.textContent = '기본모드신경망(DMN)의 탈동기화(Ego Dissolution). 전두-두정 주의 집중 네트워크의 전면적 재편.';
        gymFactHuman.textContent = '지하생활자의 절규와 초월. 2×2=4의 차가운 수식을 넘어선 인간 존엄과 숭고미의 경험.';
      }
    });
  }
"""

    if '/* --- 8. Option D Interactive' not in content:
        # insert before end
        content = content.replace('})();', option_d_js + '\n})();')

    with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Successfully updated script.js with Option D interactive controller!")

if __name__ == "__main__":
    update_index_html()
    update_script_js()
