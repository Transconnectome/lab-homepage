#!/usr/bin/env python3
"""
Connectome Lab - AI Research Idea Generator (v2)

Reads the lab's research areas, recent publications, and the latest Research
Radar trends, then asks an LLM to propose a small number of NEW research ideas
that connect external advances to the lab's own threads.

v2 changes:
- Korean-first, concise output: every idea carries short easy-Korean body
  fields (hypothesisKo, rationaleKo, firstExperimentKo, risksKo) with English
  technical terms kept as-is, plus equally concise English twins. Hard length
  caps are enforced at validation so verbose ideas are dropped, not published.
- Dual backend via IDEAS_BACKEND env:
    "openrouter" (default)  OpenRouter API + OPENROUTER_API_KEY — used by the
                            weekly GitHub Actions workflow.
    "codex"                 local `codex exec` (ChatGPT login auth, no API
                            key) — used by the DGX runner. Set CODEX_MODEL so
                            generatedBy can record the exact model id.

Honesty rules:
- There is NO non-LLM fallback: an "AI idea page" fed by templated text would
  misrepresent itself, so without a usable backend this script writes nothing
  and exits 0.
- Every record carries `generatedBy` (exact model id); the /ideas page renders
  a fixed "AI-generated, not lab-endorsed" disclaimer.
- Output is schema-validated before writing; invalid or over-long ideas are
  dropped.
"""

import urllib.request
import json
import os
import re
import glob
import shutil
import subprocess
import sys
import tempfile
import datetime

ROOT = os.path.join(os.path.dirname(__file__), "..")
IDEAS_DIR = os.path.join(ROOT, "src", "content", "ideas")
OPENROUTER_MODEL = "google/gemini-2.5-flash"
MAX_NEW_IDEAS = 3
# Must mirror the `category` enum on ideasCollection in src/content/config.ts
# (same taxonomy as the research pillars, so ideas are browsable by topic).
CATEGORIES = ("foundation-models", "connectomics", "genetics", "qml", "art-science")

# field -> max length (chars); the brevity guard that motivated v2
LENGTH_CAPS = {
    "hypothesisKo": 300, "rationaleKo": 300, "firstExperimentKo": 350, "risksKo": 200,
    "hypothesis": 350, "rationale": 350, "firstExperiment": 400, "risks": 250,
}
BODY_FIELDS = list(LENGTH_CAPS.keys())


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
    if d.get("category") not in CATEGORIES:
        print(f"[!] invalid/missing category ({d.get('category')!r}): {d.get('title','')[:50]}")
        return False
    for k in ["title", "titleKo"] + BODY_FIELDS:
        if not isinstance(d.get(k), str) or len(d[k].strip()) < 5:
            return False
    for k in ["labThreads", "externalInspiration"]:
        if not isinstance(d.get(k), list) or len(d[k]) < 1:
            return False
    for k, cap in LENGTH_CAPS.items():
        if len(d[k]) > cap:
            print(f"[!] over length cap ({k}: {len(d[k])} > {cap}): {d.get('title','')[:50]}")
            return False
    return True


def build_prompt(context):
    return f"""You are a research strategist working with the Seoul National University Connectome Lab
(PI: Jiook Cha; brain foundation models, connectomics, multimodal genetics & computational
psychiatry, quantum ML, art-science). Based on the context below, propose exactly {MAX_NEW_IDEAS}
NEW research ideas that connect recent external advances to the lab's existing threads.

Rules:
- Each idea must be genuinely novel for this lab (not a restatement of an existing lab project),
  concrete enough to start within 6 months with a small team, and honest about risks.
- Cite external inspiration by paper title from the trends provided; cite lab threads by the
  lab's own project/paper names. At most 4 items in each list, short names only.
- KOREAN IS THE PRIMARY LANGUAGE of the body fields. Write short, easy Korean that a first-year
  graduate student or curious visitor can read at a glance, keeping technical terms in English
  as-is (e.g. foundation model, polygenic score, state-space). Then give equally concise
  English twins of each field.
- Assign exactly one "category" per idea from this fixed list: ['foundation-models', 'connectomics', 'genetics', 'qml', 'art-science']
  (foundation-models = brain/EEG/fMRI representation learning; connectomics = structural/functional
  connectome analysis; genetics = multi-modal genetics & computational psychiatry; qml = quantum
  machine learning; art-science = art/music/aesthetic experience). Pick the idea's PRIMARY thread,
  not every thread it touches.
- BE SHORT. Hard limits (ideas exceeding them are dropped):
  hypothesisKo: at most 2 sentences, <= 250 Korean characters (the testable claim).
  rationaleKo: at most 2 sentences, <= 250 characters (why now, why this lab).
  firstExperimentKo: at most 2 sentences, <= 300 characters, naming data + model + metric.
  risksKo: exactly 1 sentence, <= 150 characters (the main way this fails).
  English twins: same spirit, hypothesis <= 300 / rationale <= 300 / firstExperiment <= 350 /
  risks <= 200 characters.

{context}

Return STRICT JSON: {{"ideas": [{{
  "title": str (English),
  "titleKo": str,
  "category": str (one of the fixed list above),
  "hypothesis": str, "hypothesisKo": str,
  "rationale": str, "rationaleKo": str,
  "labThreads": [str, ...],
  "externalInspiration": [str, ...],
  "firstExperiment": str, "firstExperimentKo": str,
  "risks": str, "risksKo": str
}}, ...]}}"""


def parse_json_loosely(text):
    """Extract the outermost JSON object even if wrapped in markdown fences or prose."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON object found in LLM output")
    return json.loads(text[start:end + 1])


def call_openrouter(prompt, api_key):
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps({
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
        }).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return parse_json_loosely(data["choices"][0]["message"]["content"])


def call_codex(prompt):
    """Headless `codex exec`: read-only sandbox, no session persisted, final message to a file."""
    model = os.environ.get("CODEX_MODEL", "").strip()
    with tempfile.NamedTemporaryFile(mode="r", suffix=".txt", delete=False) as out:
        out_path = out.name
    try:
        cmd = ["codex", "exec", "--ephemeral", "--skip-git-repo-check",
               "-s", "read-only", "--color", "never",
               "--output-last-message", out_path]
        if model:
            cmd += ["-m", model]
        cmd.append("-")
        proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=1800)
        if proc.returncode != 0:
            raise RuntimeError(f"codex exec failed (rc={proc.returncode}): {proc.stderr[-400:]}")
        with open(out_path, encoding="utf-8") as f:
            return parse_json_loosely(f.read())
    finally:
        os.unlink(out_path)


def main():
    backend = os.environ.get("IDEAS_BACKEND", "openrouter").strip().lower()

    if backend == "codex":
        if not shutil.which("codex"):
            print("[!] IDEAS_BACKEND=codex but codex CLI not found — skipping idea generation.")
            return 0
        model = os.environ.get("CODEX_MODEL", "").strip()
        generated_by = f"llm:{model} (codex)" if model else "llm:codex-cli (model unspecified)"
        api_key = None
    else:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            print("[!] OPENROUTER_API_KEY not set — skipping idea generation (no non-LLM fallback by design).")
            return 0
        generated_by = f"llm:{OPENROUTER_MODEL}"

    os.makedirs(IDEAS_DIR, exist_ok=True)
    context = gather_lab_context()
    seen = existing_idea_titles()
    today = datetime.date.today().isoformat()
    prompt = build_prompt(context)

    try:
        result = call_codex(prompt) if backend == "codex" else call_openrouter(prompt, api_key)
    except Exception as e:
        print(f"[!] LLM call failed ({backend}): {e}")
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
            "titleKo": idea["titleKo"].strip(),
            "date": today,
            "category": idea["category"],
            "hypothesis": idea["hypothesis"].strip(),
            "hypothesisKo": idea["hypothesisKo"].strip(),
            "rationale": idea["rationale"].strip(),
            "rationaleKo": idea["rationaleKo"].strip(),
            "labThreads": [str(t) for t in idea["labThreads"]][:4],
            "externalInspiration": [str(t) for t in idea["externalInspiration"]][:4],
            "firstExperiment": idea["firstExperiment"].strip(),
            "firstExperimentKo": idea["firstExperimentKo"].strip(),
            "risks": idea["risks"].strip(),
            "risksKo": idea["risksKo"].strip(),
            "generatedBy": generated_by,
        }
        slug = f"{today}-{clean_filename(record['title'])}"
        out = os.path.join(IDEAS_DIR, f"{slug}.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
            f.write("\n")
        seen.add(norm(record["title"]))
        added += 1
        print(f"[+] {slug}.json")

    print(f"[✓] Idea generation finished ({backend}). Added {added} new ideas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
