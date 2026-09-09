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
Writes two escaped Markdown drafts to .news-drafts, outside the published
content tree. A maintainer reviews and copies them to src/content/news.
"""

import json
import html
import datetime
import os
import re
import sys
import urllib.request
import urllib.parse
from pathlib import Path

NEWS_DIR = Path(__file__).resolve().parent.parent / ".news-drafts"
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
    # JSON strings are valid YAML scalars, including escaped newlines.
    return json.dumps(s, ensure_ascii=False)


def safe_link(value: str) -> str:
    if not value:
        return ""
    if any(char.isspace() or ord(char) < 32 for char in value):
        raise ValueError("Link must not contain whitespace or control characters")
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in ("https", "http") or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Link must be an HTTP(S) URL without credentials")
    return value


def plain_markdown(value: str) -> str:
    """Treat model output as text, never raw HTML or executable Markdown links."""
    value = html.escape(value.strip(), quote=False)
    return re.sub(r'([\\`*_{}\[\]()#+.!|>~\-])', r'\\\1', value)


def render_drafts(fields: dict, story: dict, issue_number: int) -> dict[str, str]:
    date = fields.get("date", "")
    datetime.date.fromisoformat(date)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise ValueError("Date must use YYYY-MM-DD")
    if not isinstance(issue_number, int) or isinstance(issue_number, bool) or issue_number < 1:
        raise ValueError("Missing valid issue number")
    for key in ("titleEn", "titleKo", "bodyEn", "bodyKo"):
        if not isinstance(story.get(key), str) or len(story[key].strip()) < 5:
            raise ValueError(f"Missing story field: {key}")
    if any("\n" in story[key] or "\r" in story[key] for key in ("titleEn", "titleKo")):
        raise ValueError("Headlines must be single-line text")
    category = fields.get("category", "general")
    if category not in ("award", "paper", "conference", "event", "exhibition", "general"):
        category = "general"
    link = safe_link(fields.get("link", ""))
    base = f"{date[:7]}-{slugify(story['titleEn'])}-issue-{issue_number}"
    drafts = {}
    for lang, title_key, other_key, body_key in (
        ("en", "titleEn", "titleKo", "bodyEn"),
        ("ko", "titleKo", "titleEn", "bodyKo"),
    ):
        metadata = {"lang": lang, "title": story[title_key].strip(),
                    "titleKo": story[other_key].strip(), "date": date, "category": category}
        if lang == "ko":
            metadata["baseSlug"] = base
        if link:
            metadata["link"] = link
        frontmatter = "\n".join(f"{key}: {yaml_quote(value)}" for key, value in metadata.items())
        name = f"{base}{'-ko' if lang == 'ko' else ''}.md"
        drafts[name] = f"---\n{frontmatter}\n---\n\n{plain_markdown(story[body_key])}\n"
    return drafts


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

    try:
        # Validate user fields before any paid generation call.
        datetime.date.fromisoformat(fields.get("date", ""))
        safe_link(fields.get("link", ""))
        drafts = render_drafts(fields, call_llm(fields, api_key), issue.get("number"))
        NEWS_DIR.mkdir(parents=True, exist_ok=True)
        if any((NEWS_DIR / name).exists() for name in drafts):
            raise ValueError("Draft already exists; preserve it and review before retrying")
        for name, text in drafts.items():
            with (NEWS_DIR / name).open("x", encoding="utf-8") as draft:
                draft.write(text)
        print(f"Created {len(drafts)} draft files for review. Nothing was published.")
    except ValueError as error:
        print(f"::error::{error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
