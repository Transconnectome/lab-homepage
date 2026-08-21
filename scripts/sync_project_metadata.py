#!/usr/bin/env python3
"""
Connectome Lab - Featured Projects Metadata Sync

Refreshes the machine-owned metadata fields of every record in
src/content/projects/*.json from the GitHub REST API:

    repoUrl         <- html_url          (tracks repo renames)
    stars           <- stargazers_count
    primaryLanguage <- language
    lastPush        <- pushed_at[:10]    (date only, keeps weekly diffs quiet)
    archived        <- archived

Design rules:
- The curated JSON files ARE the allowlist: this script never creates or
  deletes project records, and never touches hand-maintained fields
  (name, repo, blurb, blurbKo, network, publicationSlug, highlight,
  featured, order, generatedBy).
- A file is rewritten only when a synced value actually changed, so a
  quiet week produces an empty git diff and the workflow takes its
  no-change path.
- A failed lookup (renamed repo, API hiccup) leaves that file untouched
  and is reported as a warning; the script still exits 0 so a transient
  GitHub error never blocks the weekly trends/publications commit.

Usage:
    python3 scripts/sync_project_metadata.py
    GITHUB_TOKEN=... python3 scripts/sync_project_metadata.py   # authenticated (Actions)
"""

import glob
import json
import os
import urllib.error
import urllib.request

PROJECTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'content', 'projects'
)
API_BASE = 'https://api.github.com/repos/'
USER_AGENT = 'ConnectomeLab-AutoSync/1.0 (mailto:connectome@snu.ac.kr)'


def fetch_repo(full_name):
    req = urllib.request.Request(API_BASE + full_name)
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('User-Agent', USER_AGENT)
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def synced_fields(repo_json):
    pushed = repo_json.get('pushed_at')
    return {
        'repoUrl': repo_json.get('html_url'),
        'stars': repo_json.get('stargazers_count'),
        'primaryLanguage': repo_json.get('language'),
        'lastPush': pushed[:10] if pushed else None,
        'archived': bool(repo_json.get('archived', False)),
    }


def main():
    paths = sorted(glob.glob(os.path.join(PROJECTS_DIR, '*.json')))
    print(f"[*] {len(paths)} project records in src/content/projects")
    refreshed, unchanged, failed = 0, 0, 0

    for path in paths:
        with open(path, encoding='utf-8') as f:
            record = json.load(f)
        full_name = record.get('repo')
        if not full_name:
            print(f"[!] {os.path.basename(path)}: missing 'repo' field, skipping")
            failed += 1
            continue
        try:
            fresh = synced_fields(fetch_repo(full_name))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            print(f"[!] {full_name}: lookup failed ({e}), keeping existing metadata")
            failed += 1
            continue
        if all(record.get(k) == v for k, v in fresh.items()):
            unchanged += 1
            continue
        record.update(fresh)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
            f.write('\n')
        print(f"[+] {full_name}: ★{fresh['stars']} · {fresh['primaryLanguage']} · pushed {fresh['lastPush']}")
        refreshed += 1

    print(f"[✓] refreshed {refreshed}, unchanged {unchanged}, failed {failed}")


if __name__ == '__main__':
    main()
