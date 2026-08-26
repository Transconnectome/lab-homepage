#!/usr/bin/env python3
"""
Connectome Lab - Automated SOTA & Living Research Radar

Sweeps arXiv once per bucket for cutting-edge work across the lab's active
directions and writes one JSON record per new paper into src/content/trends/.

Bucket design (v2):
- One query per topic instead of a single OR'd query capped at 8 results. The
  old shape let the highest-volume phrase ("EEG foundation model") take every
  slot, so fMRI, genetics, and everything else starved.
- A paper's `topic` is the bucket that surfaced it, not a guess from title
  keywords. BUCKETS keys must mirror the `topic` enum in src/content/config.ts.
- Broad buckets (Agentic AI, Quantum ML) over-fetch and are narrowed by two
  gates: a deterministic neuro-term gate on title+abstract, then the
  summarizer's own 0-1 lab-relevance score. Agentic AI is deliberately scoped
  to agents APPLIED TO brain research, not agent methodology on its own.

Env:
  OPENROUTER_API_KEY  enables LLM summaries; without it every entry falls back
                      to an honestly-labeled abstract excerpt.
  ARXIV_CACHE         path to a JSON dict {bucket: [entries]} used instead of
                      the network, so the bucket/gate logic can be replayed
                      offline.
  RADAR_DRY_RUN=1     print each bucket's query URL and candidate counts, then
                      exit without calling the LLM or writing any file.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import os
import re
import sys
import time

TRENDS_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "trends")

LLM_MODEL = "google/gemini-2.5-flash"

# Seconds between arXiv calls — the API asks for one request every 3 seconds.
ARXIV_DELAY = 3

# Entries scoring below this on lab relevance are not written at all. Only the
# LLM path produces a score; the extractive fallback leaves it None and passes.
RELEVANCE_GATE = 0.4

LAB_PROFILE = (
    "Seoul National University Connectome Lab (PI: Jiook Cha). Active directions: "
    "brain foundation models for fMRI and EEG alike (NeuroMamba, SwiFT, DIVER-0, Neuro-X); "
    "agentic AI applied to brain research; "
    "affective and developmental human neuroscience (emotion, adolescent trajectories, ABCD); "
    "gene-brain association (polygenic scores, imaging genetics); "
    "quantum machine learning for high-dimensional brain data; art-science."
)

# Concrete neuro terms only. "neural" and "cognitive" are deliberately absent:
# they match nearly every ML paper and would defeat the gate.
NEURO_TERMS = (
    "brain", "eeg", "meg", "fmri", "mri", "neuroimaging", "neuroscience",
    "connectome", "cortex", "cortical", "hippocamp", "amygdala", "psychiatr",
    "ecog", "ieeg", "tractography", "white matter", "resting-state", "neuroimag",
)

# Each key MUST exist in the `topic` enum on trendsCollection (config.ts).
#   quota         max new entries written per run
#   fetch         candidates pulled before gating (over-fetch feeds the gates)
#   require_neuro run the deterministic neuro-term gate on title+abstract
#   modality      default tags when the title carries no better signal
BUCKETS = {
    "Brain Foundation Models (fMRI)": {
        "quota": 3, "fetch": 15, "require_neuro": False, "modality": ["fMRI"],
        "query": 'all:"fMRI foundation model" OR all:"brain foundation model" '
                 'OR all:"state space fMRI" OR all:"4D fMRI" OR all:"Large Brain Model"',
    },
    "Brain Foundation Models (EEG)": {
        "quota": 3, "fetch": 15, "require_neuro": False, "modality": ["EEG"],
        "query": 'all:"EEG foundation model" OR all:"EEG representation learning" '
                 'OR all:"MEG foundation model"',
    },
    "Gene & Brain": {
        "quota": 3, "fetch": 15, "require_neuro": True, "modality": ["Genomics"],
        "query": 'all:"imaging genetics" OR all:"polygenic connectome" '
                 'OR all:"polygenic risk score" OR all:"brain-wide association"',
    },
    "Affective & Developmental": {
        "quota": 3, "fetch": 20, "require_neuro": True, "modality": ["Multi-Modal"],
        "query": 'all:"affective neuroscience" OR all:"adolescent brain" '
                 'OR all:"ABCD study" OR all:"developmental neuroimaging" '
                 'OR all:"emotion decoding"',
    },
    # Scope (A): agents applied to brain research. The query is broad because
    # arXiv has no phrase for the intersection, so both gates do the narrowing
    # and an empty week is the expected, honest outcome.
    "Agentic AI": {
        "quota": 2, "fetch": 120, "require_neuro": True, "modality": ["Agents"],
        "query": 'all:"LLM agent" OR all:"agentic AI" OR all:"autonomous agent" '
                 'OR all:"multi-agent system" OR all:"agentic workflow"',
    },
    "Quantum ML": {
        "quota": 2, "fetch": 60, "require_neuro": True, "modality": ["Quantum"],
        "query": 'all:"quantum machine learning" OR all:"variational quantum classifier" '
                 'OR all:"quantum kernel"',
    },
    "Brain-LLM Alignment": {
        "quota": 2, "fetch": 15, "require_neuro": True, "modality": ["Multi-Modal"],
        "query": 'all:"brain language model alignment" OR all:"brain encoding model" '
                 'OR all:"semantic alignment brain"',
    },
}


def clean_filename(title):
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', title).strip().lower()
    return re.sub(r'[\s-]+', '-', cleaned)[:40]


def is_neuro_relevant(entry):
    """Deterministic first gate: a concrete neuro term in the title or abstract."""
    blob = (entry["title"] + " " + entry["abstract"]).lower()
    return any(term in blob for term in NEURO_TERMS)


def extractive_fallback(abstract):
    """Non-LLM fallback: honestly labeled abstract excerpt, no invented claims."""
    sentences = [s.strip() for s in abstract.split('. ') if len(s.strip()) > 20]
    points = sentences[:3] if len(sentences) >= 3 else sentences
    return {
        "summaryPoints": [p.rstrip('.') + '.' for p in points],
        "significance": "Automatically extracted from the abstract (no LLM analysis available).",
        "labRelevance": "Matched by keyword to the lab's research areas.",
        "labRelevanceScore": None,
        "generatedBy": "extractive-fallback",
    }


def validate_llm_output(data):
    pts = data.get("summaryPoints")
    score = data.get("labRelevanceScore")
    return (
        isinstance(pts, list)
        and 1 <= len(pts) <= 5
        and all(isinstance(p, str) for p in pts)
        and isinstance(data.get("significance"), str)
        and isinstance(data.get("labRelevance"), str)
        and isinstance(score, (int, float))
        and 0.0 <= float(score) <= 1.0
    )


def summarize_with_llm(title, abstract, topic, openrouter_key=None):
    """Optional LLM summarizer using OpenRouter / Gemini."""
    if not openrouter_key:
        return extractive_fallback(abstract)

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        prompt = f"""You are an expert computational neuroscientist at SNU Connectome Lab.
{LAB_PROFILE}

This paper was surfaced by the "{topic}" radar bucket:
Title: {title}
Abstract: {abstract}

Provide a JSON with:
- "summaryPoints": array of 3 concise bullet points
- "significance": 1 sentence explaining the scientific significance
- "labRelevance": 1 sentence relating it to the lab's directions above
- "labRelevanceScore": number 0-1, how relevant this is to the lab. Score
  honestly and low when the paper only matches by keyword. A paper about AI
  agents, quantum computing, or genetics with NO application to brain or
  neural data scores below 0.3 no matter how strong the paper is.
"""
        req_data = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(req_data).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            content = data['choices'][0]['message']['content']
            parsed = json.loads(content)
            if not validate_llm_output(parsed):
                raise ValueError("LLM output failed schema validation")
            parsed["labRelevanceScore"] = round(float(parsed["labRelevanceScore"]), 2)
            parsed["generatedBy"] = f"llm:{LLM_MODEL}"
            return parsed
    except Exception as e:
        print(f"[!] LLM API fallback due to: {e}")
        return extractive_fallback(abstract)


def build_url(query, max_results):
    return (
        "https://export.arxiv.org/api/query?search_query="
        + urllib.parse.quote(query)
        + f"&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    )


def parse_feed(xml_data):
    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = []
    for entry in root.findall('atom:entry', ns):
        link = entry.find('atom:id', ns).text.strip()
        entries.append({
            "id": link.rsplit("/", 1)[-1],
            "title": entry.find('atom:title', ns).text.strip().replace('\n', ' '),
            "abstract": entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
            "publishedDate": entry.find('atom:published', ns).text[:10],
            "url": link,
            "authors": [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)],
        })
    return entries


def fetch_bucket(topic, cfg):
    url = build_url(cfg["query"], cfg["fetch"])
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ConnectomeLab-Radar/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return parse_feed(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"[!] {topic}: arXiv query failed ({e})")
        return []


def pick_modality(title, cfg):
    lower = title.lower()
    tags = [t for t, kw in (("fMRI", "fmri"), ("EEG", "eeg"), ("MEG", "meg"),
                            ("Genomics", "genetic"), ("Genomics", "polygenic"))
            if kw in lower]
    # dict.fromkeys keeps first-seen order while dropping the duplicate Genomics
    return list(dict.fromkeys(tags)) or list(cfg["modality"])


def main():
    os.makedirs(TRENDS_DIR, exist_ok=True)
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    cache_path = os.environ.get("ARXIV_CACHE")
    dry_run = os.environ.get("RADAR_DRY_RUN") == "1"
    cache = json.load(open(cache_path, encoding="utf-8")) if cache_path else None

    seen_ids = set()
    written = 0

    for i, (topic, cfg) in enumerate(BUCKETS.items()):
        if cache is not None:
            candidates = cache.get(topic, [])
        elif dry_run:
            print(f"\n=== {topic}\n    {build_url(cfg['query'], cfg['fetch'])}")
            candidates = fetch_bucket(topic, cfg)
        else:
            if i:
                time.sleep(ARXIV_DELAY)
            candidates = fetch_bucket(topic, cfg)

        fetched = len(candidates)

        # Cross-bucket dedup: a paper matching two buckets belongs to the first.
        candidates = [c for c in candidates if c["id"] not in seen_ids]
        for c in candidates:
            seen_ids.add(c["id"])

        if cfg["require_neuro"]:
            candidates = [c for c in candidates if is_neuro_relevant(c)]

        if dry_run:
            print(f"    fetched={fetched}  after dedup+neuro gate={len(candidates)}"
                  f"  quota={cfg['quota']}")
            for c in candidates[:cfg["quota"]]:
                print(f"      {c['publishedDate']}  {c['title'][:80]}")
            continue

        added = 0
        attempts = 0
        for p in candidates:
            if added >= cfg["quota"]:
                break
            # Bound LLM spend when the relevance gate keeps rejecting.
            if attempts >= cfg["quota"] * 3:
                print(f"[!] {topic}: gave up after {attempts} low-relevance candidates")
                break

            out_path = os.path.join(TRENDS_DIR, f"{clean_filename(p['title'])}.json")
            if os.path.exists(out_path):
                continue

            attempts += 1
            print(f"[*] {topic}: {p['title'][:60]}...")
            analysis = summarize_with_llm(p["title"], p["abstract"], topic, openrouter_key)

            score = analysis.get("labRelevanceScore")
            if score is not None and score < RELEVANCE_GATE:
                print(f"    [-] dropped, lab relevance {score} < {RELEVANCE_GATE}")
                continue

            record = {
                "title": p["title"],
                "authors": p["authors"][:4],
                "publishedDate": p["publishedDate"],
                "source": f"arXiv ({p['publishedDate'][:7]})",
                "topic": topic,
                "url": p["url"].replace("http://", "https://"),
                "summaryPoints": analysis.get("summaryPoints", []),
                "significance": analysis.get("significance", ""),
                "labRelevance": analysis.get("labRelevance", ""),
                "modality": pick_modality(p["title"], cfg),
                "badge": "Emerging Paper",
                "generatedBy": analysis.get("generatedBy"),
                "labRelevanceScore": score,
            }
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2, ensure_ascii=False)
                f.write("\n")
            added += 1
            written += 1

        print(f"[=] {topic}: fetched {fetched}, wrote {added}")

    if dry_run:
        print("\n[✓] Dry run complete — nothing written.")
        return

    print(f"[✓] Research Radar updated. Added {written} new trend items.")


if __name__ == "__main__":
    main()
