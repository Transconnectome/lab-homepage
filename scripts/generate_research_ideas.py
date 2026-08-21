#!/usr/bin/env python3
"""
Connectome Lab - AI Research Idea Generator

Reads the lab's research areas, recent publications, and the latest Research
Radar trends, then asks an LLM (OpenRouter / Gemini) to propose a small number
of NEW research ideas that connect external advances to the lab's own threads.

Honesty rules:
- Requires OPENROUTER_API_KEY. There is NO non-LLM fallback: an "AI idea page"
  fed by templated text would misrepresent itself, so without a key this
  script writes nothing and exits 0.
- Every record carries `generatedBy` (exact model id); the /ideas page renders
  a fixed "AI-generated, not lab-endorsed" disclaimer.
- Output is schema-validated before writing; invalid ideas are dropped.
"""

import urllib.request
import json
import os
import re
import glob
import sys
import datetime

ROOT = os.path.join(os.path.dirname(__file__), "..")
IDEAS_DIR = os.path.join(ROOT, "src", "content", "ideas")
LLM_MODEL = "google/gemini-2.5-flash"
MAX_NEW_IDEAS = 3


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def clean_filename(title):
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", title).strip().lower()
    return re.sub(r"[\s-]+", "-", cleaned)[:48]


def gather_lab_context():
    parts = []

    areas = []
    for path in sorted(glob.glob(os.path.join(ROOT, "src", "content", "research", "*.md"))):
        text = open(path, encoding="utf-8").read()
        title = re.search(r'^title:\s*"?(.+?)"?\s*$', text, re.M)
        tagline = re.search(r'^tagline:\s*"?(.+?)"?\s*$', text, re.M)
        if title:
            areas.append(f"- {title.group(1)}" + (f": {tagline.group(1)}" if tagline else ""))
    parts.append("LAB RESEARCH AREAS:\n" + "\n".join(areas))

    pubs = []
    for path in glob.glob(os.path.join(ROOT, "src", "content", "publications", "*.json")):
        d = json.load(open(path, encoding="utf-8"))
        if d.get("year", 0) >= 2024:
            pubs.append((d["year"], f"- ({d['year']}) {d['title']} [{d.get('venue','')}]") )
    pubs.sort(reverse=True)
    parts.append("RECENT LAB PUBLICATIONS (2024+):\n" + "\n".join(p[1] for p in pubs[:25]))

    trends = []
    for path in glob.glob(os.path.join(ROOT, "src", "content", "trends", "*.json")):
        d = json.load(open(path, encoding="utf-8"))
        trends.append((d.get("publishedDate", ""), f"- [{d.get('topic','')}] {d['title']} ({d.get('source','')}): " + "; ".join(d.get("summaryPoints", [])[:2])))
    trends.sort(reverse=True)
    parts.append("LATEST EXTERNAL TRENDS (Research Radar):\n" + "\n".join(t[1] for t in trends[:10]))

    return "\n\n".join(parts)


def existing_idea_titles():
    titles = set()
    for path in glob.glob(os.path.join(IDEAS_DIR, "*.json")):
        try:
            titles.add(norm(json.load(open(path, encoding="utf-8")).get("title", "")))
        except Exception:
            pass
    return titles


def validate_idea(d):
    return (
        isinstance(d.get("title"), str) and len(d["title"]) > 8
        and isinstance(d.get("hypothesis"), str) and len(d["hypothesis"]) > 30
        and isinstance(d.get("rationale"), str) and len(d["rationale"]) > 30
        and isinstance(d.get("labThreads"), list) and len(d["labThreads"]) >= 1
        and isinstance(d.get("externalInspiration"), list) and len(d["externalInspiration"]) >= 1
        and isinstance(d.get("firstExperiment"), str) and len(d["firstExperiment"]) > 30
        and isinstance(d.get("risks"), str) and len(d["risks"]) > 20
    )


def call_llm(context, api_key):
    prompt = f"""You are a research strategist working with the Seoul National University Connectome Lab
(PI: Jiook Cha; brain foundation models, connectomics, multimodal genetics & computational
psychiatry, quantum ML, art-science). Based on the context below, propose exactly {MAX_NEW_IDEAS}
NEW research ideas that connect recent external advances to the lab's existing threads.

Rules:
- Each idea must be genuinely novel for this lab (not a restatement of an existing lab project),
  concrete enough to start within 6 months with a small team, and honest about risks.
- Cite external inspiration by paper title (and arXiv id when known) from the trends provided.
- Cite lab threads by the lab's own project/paper names.
- Write in clear English. Also give a natural Korean translation of the title.

{context}

Return STRICT JSON: {{"ideas": [{{
  "title": str,
  "titleKo": str,
  "hypothesis": str  (2-3 sentences: the testable claim),
  "rationale": str   (why now, why this lab),
  "labThreads": [str, ...],
  "externalInspiration": [str, ...],
  "firstExperiment": str (a concrete first experiment with data + model + metric),
  "risks": str (the main ways this fails)
}}, ...]}}"""

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps({
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
        }).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return json.loads(data["choices"][0]["message"]["content"])


def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("[!] OPENROUTER_API_KEY not set — skipping idea generation (no non-LLM fallback by design).")
        return 0

    os.makedirs(IDEAS_DIR, exist_ok=True)
    context = gather_lab_context()
    seen = existing_idea_titles()
    today = datetime.date.today().isoformat()

    try:
        result = call_llm(context, api_key)
    except Exception as e:
        print(f"[!] LLM call failed: {e}")
        return 0

    added = 0
    for idea in result.get("ideas", [])[:MAX_NEW_IDEAS]:
        if not validate_idea(idea):
            print(f"[!] dropped invalid idea: {str(idea.get('title'))[:60]}")
            continue
        if norm(idea["title"]) in seen:
            print(f"[=] duplicate skipped: {idea['title'][:60]}")
            continue
        record = {
            "title": idea["title"].strip(),
            "titleKo": (idea.get("titleKo") or "").strip() or None,
            "date": today,
            "hypothesis": idea["hypothesis"].strip(),
            "rationale": idea["rationale"].strip(),
            "labThreads": [str(t) for t in idea["labThreads"]][:6],
            "externalInspiration": [str(t) for t in idea["externalInspiration"]][:6],
            "firstExperiment": idea["firstExperiment"].strip(),
            "risks": idea["risks"].strip(),
            "generatedBy": f"llm:{LLM_MODEL}",
        }
        slug = f"{today}-{clean_filename(record['title'])}"
        out = os.path.join(IDEAS_DIR, f"{slug}.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
            f.write("\n")
        seen.add(norm(record["title"]))
        added += 1
        print(f"[+] {slug}.json")

    print(f"[✓] Idea generation finished. Added {added} new ideas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
