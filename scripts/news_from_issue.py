#!/usr/bin/env python3
"""
Connectome Lab - News-from-Issue Pipeline

Turns a "news submission" GitHub issue (created via the issue form in
.github/ISSUE_TEMPLATE/news-submission.yml) into a pair of news stories
(English + Korean) under src/content/news/.

Honesty rules:
- The LLM may ONLY use facts stated in the issue. The prompt forbids adding
  numbers, quotes, or claims that are not in the submission.
- Requires OPENROUTER_API_KEY; without it the script exits non-zero so the
  workflow can report failure on the issue instead of publishing nothing
  silently.

Reads the issue payload from GITHUB_EVENT_PATH (standard Actions event file).
Writes the two markdown files and prints their paths (used by the workflow).
"""

import json
import os
import re
import sys
import urllib.request

NEWS_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "news")
LLM_MODEL = "google/gemini-2.5-flash"


def parse_issue_form(body: str) -> dict:
    """Issue-form bodies look like '### Label\n\nvalue' blocks."""
    fields = {}
    for m in re.finditer(r"### (.+?)\n+((?:(?!###).)*)", body, re.S):
        label = m.group(1).strip().lower()
        value = m.group(2).strip()
        if value in ("_No response_", ""):
            value = ""
        if "한 줄 요약" in m.group(1) or "what happened" in label:
            fields["headline"] = value
        elif "날짜" in m.group(1) or "date" in label:
            fields["date"] = value
        elif "분류" in m.group(1) or "category" in label:
            fields["category"] = value
        elif "자세한 내용" in m.group(1) or "details" in label:
            fields["details"] = value
        elif "링크" in m.group(1) or "link" in label:
            fields["link"] = value
    return fields


def slugify(text: str, limit: int = 40) -> str:
    s = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    s = re.sub(r"[\s-]+", "-", s)[:limit].strip("-")
    return s or "lab-news"


def call_llm(fields: dict, api_key: str) -> dict:
    prompt = f"""You are the web editor of the SNU Connectome Lab (PI: Jiook Cha).
A lab member submitted this news item. Write it up as a short news story for the
lab homepage, in BOTH English and Korean.

STRICT RULES:
- Use ONLY the facts below. Do NOT invent numbers, quotes, dates, affiliations,
  or significance claims that are not stated. If a detail is missing, simply
  leave it out.
- 2-4 sentences per story. Warm but factual lab-news register.
- Korean version: 처음부터 한국어로 쓴 글처럼 자연스럽게. 번역투 금지("~에 대한/
  ~을 통해/~적인" 남발 금지, 주어 반복 금지, 과장 수식어 금지). 평서문(…했다/…이다) 문체.
- English headline: concise, title case not required. Korean headline: 자연스러운 한국어.
- Names: keep the submitter's spelling; Korean names in Korean script in the Korean story.

SUBMISSION:
- What happened: {fields.get('headline', '')}
- Date: {fields.get('date', '')}
- Category: {fields.get('category', 'general')}
- Details: {fields.get('details', '')}
- Link: {fields.get('link', '') or '(none)'}

Return STRICT JSON:
{{"titleEn": str, "titleKo": str, "bodyEn": str, "bodyKo": str}}"""

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps({
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
        }).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    out = json.loads(data["choices"][0]["message"]["content"])
    for k in ("titleEn", "titleKo", "bodyEn", "bodyKo"):
        if not isinstance(out.get(k), str) or len(out[k].strip()) < 5:
            raise ValueError(f"LLM output missing/short field: {k}")
    return out


def yaml_quote(s: str) -> str:
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main() -> int:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("::error::OPENROUTER_API_KEY is not set — cannot generate the story.")
        return 1

    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        print("::error::GITHUB_EVENT_PATH not found.")
        return 1
    event = json.load(open(event_path, encoding="utf-8"))
    issue = event.get("issue", {})
    fields = parse_issue_form(issue.get("body") or "")

    if not fields.get("headline") or not fields.get("details"):
        print("::error::Submission is missing the headline or details field.")
        return 1

    date = fields.get("date", "")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        date = (issue.get("created_at") or "2026-01-01")[:10]
    category = fields.get("category", "general")
    if category not in ("award", "paper", "conference", "event", "exhibition", "general"):
        category = "general"
    link = fields.get("link", "")

    story = call_llm(fields, api_key)

    os.makedirs(NEWS_DIR, exist_ok=True)
    base = f"{date[:7]}-{slugify(story['titleEn'])}"
    en_path = os.path.join(NEWS_DIR, f"{base}.md")
    ko_path = os.path.join(NEWS_DIR, f"{base}-ko.md")
    if os.path.exists(en_path):
        base = f"{base}-{issue.get('number', 'x')}"
        en_path = os.path.join(NEWS_DIR, f"{base}.md")
        ko_path = os.path.join(NEWS_DIR, f"{base}-ko.md")

    link_line = f"link: {yaml_quote(link)}\n" if link else ""

    with open(en_path, "w", encoding="utf-8") as f:
        f.write(
            f"---\ntitle: {yaml_quote(story['titleEn'])}\n"
            f"titleKo: {yaml_quote(story['titleKo'])}\n"
            f"date: \"{date}\"\ncategory: \"{category}\"\n{link_line}---\n"
            f"{story['bodyEn'].strip()}\n"
        )
    with open(ko_path, "w", encoding="utf-8") as f:
        f.write(
            f"---\nlang: \"ko\"\nbaseSlug: \"{base}\"\n"
            f"title: {yaml_quote(story['titleKo'])}\n"
            f"titleKo: {yaml_quote(story['titleEn'])}\n"
            f"date: \"{date}\"\ncategory: \"{category}\"\n{link_line}---\n"
            f"{story['bodyKo'].strip()}\n"
        )

    print(f"created={base}")
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a", encoding="utf-8") as f:
        f.write(f"slug={base}\n")
        f.write(f"title_en={story['titleEn']}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
