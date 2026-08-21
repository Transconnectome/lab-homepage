#!/usr/bin/env python3
"""
Connectome Lab - Automated Publication Sync Pipeline
Fetches latest publications by Prof. Jiook Cha and lab authors via OpenAlex API,
and updates src/content/publications/*.json
"""

import urllib.request
import json
import os
import sys
import re

OPENALEX_AUTHOR_IDS = "A5033979262|A5093826967"
OPENALEX_API_URL = f"https://api.openalex.org/works?filter=author.id:{OPENALEX_AUTHOR_IDS}&sort=publication_year:desc&per-page=30"
PUB_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "publications")

def clean_filename(title):
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', title).strip().lower()
    return re.sub(r'[\s-]+', '-', cleaned)[:40]

def fetch_openalex_works():
    print(f"[*] Querying OpenAlex API for works by Prof. Jiook Cha ({OPENALEX_AUTHOR_IDS})...")
    headers = {"User-Agent": "ConnectomeLab-AutoSync/1.0 (mailto:connectome@snu.ac.kr)"}
    req = urllib.request.Request(OPENALEX_API_URL, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("results", [])
            print(f"[+] Retrieved {len(results)} works from OpenAlex.")
            return results
    except Exception as e:
        print(f"[!] Warning: OpenAlex API query failed: {e}")
        return []

def main():
    os.makedirs(PUB_DIR, exist_ok=True)
    works = fetch_openalex_works()
    
    updated_count = 0
    for work in works:
        title = work.get("title")
        if not title:
            continue
            
        year = work.get("publication_year", 2025)
        doi = work.get("doi")
        if doi and doi.startswith("https://doi.org/"):
            doi = doi.replace("https://doi.org/", "")
            
        authors = [a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])]
        
        primary_loc = work.get("primary_location") or {}
        source = primary_loc.get("source") or {}
        venue = source.get("display_name") or "Preprint / Journal"
        
        # Tags determination
        tags = []
        lower_title = title.lower()
        if "fmri" in lower_title or "mri" in lower_title or "functional" in lower_title:
            tags.append("fMRI")
        if "eeg" in lower_title:
            tags.append("EEG")
        if "polygenic" in lower_title or "gene" in lower_title or "genetic" in lower_title:
            tags.append("Genetics")
        if "depression" in lower_title or "psychiatric" in lower_title:
            tags.append("Depression")
        if "model" in lower_title or "transformer" in lower_title or "learning" in lower_title:
            tags.append("Foundation Models")
        if not tags:
            tags.append("Connectomics")
            
        slug = f"{clean_filename(title)}-{year}"
        out_file = os.path.join(PUB_DIR, f"{slug}.json")
        
        if os.path.exists(out_file):
            continue
            
        pub_record = {
            "title": title,
            "authors": authors[:6] if len(authors) > 6 else authors,
            "venue": venue,
            "year": year,
            "doi": doi if doi else None,
            "url": f"https://doi.org/{doi}" if doi else work.get("landing_page_url"),
            "tags": tags,
            "featured": year >= 2025,
            "labMembers": [a for a in authors if "Cha" in a or "Lee" in a or "Choi" in a or "Kim" in a or "Han" in a or "Wang" in a]
        }
        
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(pub_record, f, indent=2, ensure_ascii=False)
            updated_count += 1
            print(f"[+] Added publication: {slug}.json")

    print(f"[✓] Auto-sync finished. Added {updated_count} new publications.")

if __name__ == "__main__":
    main()
