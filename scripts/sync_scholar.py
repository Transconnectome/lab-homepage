#!/usr/bin/env python3
"""
Connectome Lab - Automated Publication Sync Pipeline
Fetches ALL publications by Prof. Jiook Cha via the OpenAlex API (cursor
pagination) and writes src/content/publications/*.json records.

Design rules:
- Never overwrite an existing record: hand-curated entries win. Dedup is by
  DOI first, then by normalized title, so re-listings of curated papers are
  skipped even when OpenAlex slugs differ.
- labMembers comes from an allowlist built from src/content/members/*.json
  (plus known romanization variants) — NOT from surname heuristics, which
  mislabel external co-authors as lab members.
- Auto-synced records are featured: false; featuring is a manual editorial
  decision on curated records.
"""

import urllib.request
import urllib.parse
import json
import os
import re
import glob

OPENALEX_AUTHOR_IDS = "A5033979262|A5093826967"
OPENALEX_BASE = (
    "https://api.openalex.org/works"
    f"?filter=author.id:{OPENALEX_AUTHOR_IDS}"
    "&sort=publication_year:desc&per-page=100"
)
PUB_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "publications")
MEMBERS_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "members")

# Known alternate romanizations seen in indexed metadata -> canonical member name
NAME_ALIASES = {
    "jeongwoo seo": "Jungwoo Seo",
    "bo-gyeom kim": "Bogyeom Kim",
    "bo‐gyeom kim": "Bogyeom Kim",  # non-breaking hyphen variant
    "bogyeom kim": "Bogyeom Kim",
    "dongyeop han": "Dong Yeop Han",
    "dong yeop han": "Dong Yeop Han",
    "seok-jin moon": "Seok-Jin Moon",
    "seokjin moon": "Seok-Jin Moon",
    "yoonjung yoonie joo": "Yoonjung Yoonie Joo",
    "yoonjung y. joo": "Yoonjung Yoonie Joo",
    "eun se you": "Allison Eun Se You",
    "allison eun se you": "Allison Eun Se You",
    "jungyoung janice min": "Jungyoung Janice Min",
    "jungyoun janice min": "Jungyoung Janice Min",
    "jungyoon min": "Jungyoung Janice Min",
}


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def load_member_allowlist():
    """Names of current + former lab members, from the members collection."""
    allow = {}
    for path in glob.glob(os.path.join(MEMBERS_DIR, "*.json")):
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        name = d.get("name")
        if name:
            allow[name.lower()] = name
    for alias, canonical in NAME_ALIASES.items():
        allow[alias] = canonical
    return allow


def match_lab_members(authors, allowlist):
    out = []
    for a in authors:
        key = a.lower().replace("‐", "-").replace("‑", "-")
        if key in allowlist and a not in out:
            out.append(a)
    return out


def clean_title(title):
    # strip inline markup that OpenAlex/Crossref pass through (<scp>, <i>, ...)
    return re.sub(r"</?[a-zA-Z][^>]*>", "", title).strip()


def clean_filename(title):
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", title).strip().lower()
    return re.sub(r"[\s-]+", "-", cleaned)[:40]


def derive_tags(title):
    t = title.lower()
    tags = []
    if re.search(r"\bfmri\b|\bmri\b|neuroimag", t):
        tags.append("Neuroimaging")
    if re.search(r"\beeg\b|\becog\b|\bieeg\b", t):
        tags.append("EEG")
    if re.search(r"polygenic|genetic\b|genome|genomic|\bgene\b|heritab", t):
        tags.append("Genetics")
    if re.search(r"depress|psychiatr|psychopatholog|suicid|adhd|ocd|ptsd|anxiety|mental", t):
        tags.append("Psychiatry")
    if re.search(r"quantum", t):
        tags.append("Quantum ML")
    if re.search(r"foundation model|transformer|deep learning|machine learning|neural network|state.space|diffusion|autoencoder", t):
        tags.append("AI & Foundation Models")
    if not tags:
        tags.append("Neuroscience")
    return tags


def fetch_all_openalex_works():
    headers = {"User-Agent": "ConnectomeLab-AutoSync/2.0 (mailto:connectome@snu.ac.kr)"}
    results, cursor = [], "*"
    while cursor:
        url = f"{OPENALEX_BASE}&cursor={urllib.parse.quote(cursor)}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        page = data.get("results", [])
        results.extend(page)
        cursor = data.get("meta", {}).get("next_cursor")
        if not page:
            break
        print(f"[*] fetched {len(results)} works so far...")
    return results


def load_existing_keys():
    """DOIs and normalized titles of every record already on disk."""
    dois, titles = set(), set()
    for path in glob.glob(os.path.join(PUB_DIR, "*.json")):
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        if d.get("doi"):
            dois.add(d["doi"].lower())
        if d.get("title"):
            titles.add(norm(d["title"]))
    return dois, titles


def main():
    os.makedirs(PUB_DIR, exist_ok=True)
    allowlist = load_member_allowlist()
    print(f"[*] member allowlist: {len(allowlist)} names")
    works = fetch_all_openalex_works()
    print(f"[+] total works from OpenAlex: {len(works)}")
    dois, titles = load_existing_keys()

    added = 0
    for work in works:
        title = work.get("title")
        if not title:
            continue
        title = clean_title(title)

        doi = work.get("doi") or ""
        doi = doi.replace("https://doi.org/", "")
        if doi and doi.lower() in dois:
            continue
        if norm(title) in titles:
            continue

        year = work.get("publication_year", 0)
        authors = [a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])]
        authors = list(dict.fromkeys(a for a in authors if a))

        primary_loc = work.get("primary_location") or {}
        source = (primary_loc.get("source") or {})
        venue = source.get("display_name")
        if not venue:
            landing = (primary_loc.get("landing_page_url") or "")
            venue = "arXiv preprint" if "arxiv" in landing else "Preprint"

        record = {
            "title": title,
            "authors": authors,
            "venue": venue,
            "year": year,
            "doi": doi if doi else None,
            "url": f"https://doi.org/{doi}" if doi else work.get("landing_page_url"),
            "tags": derive_tags(title),
            "featured": False,
            "labMembers": match_lab_members(authors, allowlist),
        }

        slug = f"{clean_filename(title)}-{year}"
        out_file = os.path.join(PUB_DIR, f"{slug}.json")
        if os.path.exists(out_file):
            continue
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
            f.write("\n")
        if doi:
            dois.add(doi.lower())
        titles.add(norm(title))
        added += 1

    print(f"[✓] Auto-sync finished. Added {added} new publication records.")


if __name__ == "__main__":
    main()
