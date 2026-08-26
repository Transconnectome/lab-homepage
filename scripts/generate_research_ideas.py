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
# and the labels in src/components/ideas/IdeasFilter.tsx.
CATEGORIES = (
    "foundation-models", "connectomics", "genetics", "qml", "affective-neuro",
    "agentic-ai", "affective-development",
)

# Directions the PI is actively pursuing. Some have no pillar page and no
# publication yet, so they are labeled as such: without this the model either
# ignores a whole topic bucket or cites lab work that does not exist.
LAB_INTEREST_AREAS = """LAB'S ACTIVE INTEREST DIRECTIONS (PI-stated; some have no publications yet,
so do NOT cite them as existing lab work in labThreads):
- Brain foundation models across fMRI and EEG alike
- Agentic AI applied to brain research (analysis pipelines, hypothesis generation,
  literature-scale reasoning over neuroimaging) — not agent methodology on its own
- Affective and developmental human neuroscience (emotion, adolescent trajectories, ABCD)
- Gene-brain association"""

# How many radar entries reach the prompt. Sampled round-robin across topics:
# a flat "newest N" let one prolific bucket fill the whole context.
TREND_CONTEXT_SIZE = 14

# Redundancy guards. Title wording varies too much between runs to be a useful
# signal on its own (back-testing the first twelve ideas, even the genuine
# near-duplicates peaked at 0.375 token overlap), so the primary rule is
# source-based: one radar paper should not be mined twice for the same
# category. EEG-PRISM alone produced three foundation-models ideas that way.
TITLE_SIMILARITY_CAP = 0.6   # backstop for near-verbatim restatements
RECENT_MIX_WINDOW = 6        # ideas summarised for the prompt's category mix

# field -> max length (chars); the brevity guard that motivated v2
LENGTH_CAPS = {
    "hypothesisKo": 300, "rationaleKo": 300, "firstExperimentKo": 350, "risksKo": 200,
    "hypothesis": 350, "rationale": 350, "firstExperiment": 400, "risks": 250,
}
BODY_FIELDS = list(LENGTH_CAPS.keys())

# The prompt asks for Korean first and an English twin second, and the model
# sometimes answers Korean twice — which published Korean prose on /en/ideas.
# A field is treated as Korean when Hangul makes up a real share of it, so an
# English sentence carrying a Korean proper noun still passes.
HANGUL_RE = re.compile(r"[\uac00-\ud7a3]")


def hangul_ratio(text):
    text = (text or "").strip()
    if not text:
        return 0.0
    return len(HANGUL_RE.findall(text)) / len(text)


TITLE_STOPWORDS = {"for", "of", "and", "the", "with", "a", "to", "in", "on",
                   "via", "using", "from", "by", "an"}


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

    trends = [json.load(open(path, encoding="utf-8"))
              for path in glob.glob(os.path.join(ROOT, "src", "content", "trends", "*.json"))]
    lines = [f"- [{d.get('topic','')}] {d['title']} ({d.get('source','')}): "
             + "; ".join(d.get("summaryPoints", [])[:2])
             for d in sample_trends_round_robin(trends, TREND_CONTEXT_SIZE)]
    parts.append("LATEST EXTERNAL TRENDS (Research Radar):\n" + "\n".join(lines))

    parts.append(LAB_INTEREST_AREAS)

    return "\n\n".join(parts)


def sample_trends_round_robin(trends, limit):
    """Take the newest entry from each topic in turn until `limit` is reached.

    Taking the newest `limit` overall lets the most prolific bucket crowd out
    every other direction, which is how twelve radar entries produced ideas in
    only three categories. Rounds are ordered by topic name so a given content
    directory always yields the same prompt.
    """
    by_topic = {}
    for d in trends:
        by_topic.setdefault(d.get("topic", ""), []).append(d)
    for entries in by_topic.values():
        entries.sort(key=lambda d: d.get("publishedDate", ""), reverse=True)

    picked, depth = [], 0
    while len(picked) < limit and any(len(e) > depth for e in by_topic.values()):
        for topic in sorted(by_topic):
            if len(picked) >= limit:
                break
            if len(by_topic[topic]) > depth:
                picked.append(by_topic[topic][depth])
        depth += 1
    return picked


def load_existing_ideas():
    ideas = []
    for path in glob.glob(os.path.join(IDEAS_DIR, "*.json")):
        try:
            ideas.append(json.load(open(path, encoding="utf-8")))
        except Exception:
            pass
    return ideas


def title_tokens(title):
    return {w for w in re.findall(r"[a-z0-9]+", (title or "").lower()) if w not in TITLE_STOPWORDS}


def source_key(inspiration):
    """Normalise a cited paper to a comparable key.

    Entries arrive in several shapes across runs — "ZIPBrain",
    "EEG-PRISM: Physiologically-Grounded ...", or a full title with a
    "(arXiv (2026-08))" suffix — so drop everything after the first colon or
    bracket before normalising.
    """
    head = re.split(r"[:(\[]", str(inspiration), 1)[0]
    return norm(head)


def redundancy_reason(idea, existing):
    """Why `idea` duplicates something already published, or None if it is new."""
    new_title = norm(idea.get("title", ""))
    new_tokens = title_tokens(idea.get("title", ""))
    new_sources = {k for k in (source_key(i) for i in idea.get("externalInspiration", [])) if k}

    for old in existing:
        if new_title and new_title == norm(old.get("title", "")):
            return f"same title as {old.get('title','')[:50]}"

        old_tokens = title_tokens(old.get("title", ""))
        if new_tokens and old_tokens:
            overlap = len(new_tokens & old_tokens) / len(new_tokens | old_tokens)
            if overlap >= TITLE_SIMILARITY_CAP:
                return f"title {overlap:.2f} similar to {old.get('title','')[:50]}"

        if idea.get("category") != old.get("category"):
            continue
        old_sources = {k for k in (source_key(i) for i in old.get("externalInspiration", [])) if k}
        shared = {a for a in new_sources for b in old_sources
                  if a == b or (len(a) >= 8 and len(b) >= 8 and (a in b or b in a))}
        if shared:
            return (f"same source + category ({idea.get('category')}) as "
                    f"{old.get('title','')[:50]}")
    return None


def recent_category_mix(existing, window=RECENT_MIX_WINDOW):
    recent = sorted(existing, key=lambda d: d.get("date", ""), reverse=True)[:window]
    counts = {}
    for d in recent:
        counts[d.get("category", "?")] = counts.get(d.get("category", "?"), 0) + 1
    if not counts:
        return "RECENT IDEA CATEGORY MIX: none yet."
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ("RECENT IDEA CATEGORY MIX (last %d ideas): " % len(recent)
            + ", ".join(f"{k} x{v}" for k, v in ordered))


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
    # English body fields must actually be English, and Korean ones Korean.
    # Titles are excluded: a Korean title can legitimately be almost all Latin
    # when it is a model name ("NeuroMamba", "Q-DIVER").
    for k in BODY_FIELDS:
        ko_field = k.endswith("Ko")
        ratio = hangul_ratio(d[k])
        if not ko_field and ratio > 0.15:
            print(f"[!] English field is Korean ({k}): {d.get('title','')[:50]}")
            return False
        if ko_field and ratio < 0.05:
            print(f"[!] Korean field has no Korean ({k}): {d.get('title','')[:50]}")
            return False
    return True


def build_prompt(context, category_mix=""):
    return f"""You are a research strategist working with the Seoul National University Connectome Lab
(PI: Jiook Cha; brain foundation models for fMRI and EEG, connectomics, multimodal genetics &
computational psychiatry, agentic AI for brain research, affective & developmental
neuroscience, quantum ML, affective neuroscience). Based on the context below, propose exactly {MAX_NEW_IDEAS}
NEW research ideas that connect recent external advances to the lab's existing threads.

Rules:
- Each idea must be genuinely novel for this lab (not a restatement of an existing lab project),
  concrete enough to start within 6 months with a small team, and honest about risks.
- The three ideas must sit in three DIFFERENT categories, and should draw on different
  external papers. Two ideas mined from one paper for the same category is the failure
  mode this rule exists to prevent — the second one is dropped, not published.
- Favour categories that are under-represented in the recent mix below, and directions
  from the interest list that have no ideas yet. Do not force it: an idea the external
  evidence does not support is worse than a thinner week.
- Cite external inspiration by paper title from the trends provided; cite lab threads by the
  lab's own project/paper names. At most 4 items in each list, short names only.
- KOREAN IS THE PRIMARY LANGUAGE of the body fields. Write short, easy Korean that a first-year
  graduate student or curious visitor can read at a glance, keeping technical terms in English
  as-is (e.g. foundation model, polygenic score, state-space). Then give equally concise
  English twins of each field.
- Assign exactly one "category" per idea from this fixed list:
  ['foundation-models', 'connectomics', 'genetics', 'qml', 'affective-neuro', 'agentic-ai', 'affective-development']
  (foundation-models = brain/EEG/fMRI representation learning; connectomics = structural/functional
  connectome analysis; genetics = multi-modal genetics & computational psychiatry; qml = quantum
  machine learning; affective-neuro = awe, affect, memory, music/aesthetic experience; agentic-ai = autonomous/tool-using
  AI agents APPLIED TO brain research — analysis pipelines, hypothesis generation, literature-scale
  reasoning over neuroimaging, NOT pure agent methodology with no neuro application;
  affective-development = affective and developmental human neuroscience, e.g. emotion processing,
  adolescent brain trajectories, longitudinal cohorts such as ABCD). Pick the idea's PRIMARY thread,
  not every thread it touches.
- BE SHORT. Hard limits (ideas exceeding them are dropped):
  hypothesisKo: at most 2 sentences, <= 250 Korean characters (the testable claim).
  rationaleKo: at most 2 sentences, <= 250 characters (why now, why this lab).
  firstExperimentKo: at most 2 sentences, <= 300 characters, naming data + model + metric.
  risksKo: exactly 1 sentence, <= 150 characters (the main way this fails).
  English twins: same spirit, hypothesis <= 300 / rationale <= 300 / firstExperiment <= 350 /
  risks <= 200 characters.

{category_mix}

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
    existing = load_existing_ideas()
    today = datetime.date.today().isoformat()
    prompt = build_prompt(context, recent_category_mix(existing))

    try:
        result = call_codex(prompt) if backend == "codex" else call_openrouter(prompt, api_key)
    except Exception as e:
        print(f"[!] LLM call failed ({backend}): {e}")
        return 0

    added = 0
    used_categories = set()
    for idea in result.get("ideas", [])[:MAX_NEW_IDEAS]:
        if not validate_idea(idea):
            print(f"[!] dropped invalid idea: {str(idea.get('title'))[:60]}")
            continue
        reason = redundancy_reason(idea, existing)
        if reason:
            print(f"[=] redundant, skipped: {idea['title'][:50]} ({reason})")
            continue
        # One idea per category per run. Nothing is regenerated to fill the gap:
        # a thinner week is the honest outcome, same as the no-LLM-key path.
        if idea["category"] in used_categories:
            print(f"[=] category already used this run ({idea['category']}): "
                  f"{idea['title'][:50]}")
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
        existing.append(record)
        used_categories.add(record["category"])
        added += 1
        print(f"[+] {slug}.json")

    print(f"[✓] Idea generation finished ({backend}). Added {added} new ideas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
