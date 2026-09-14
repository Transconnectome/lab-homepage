#!/usr/bin/env python3
"""Validate generated routes, fragments, language metadata, and local assets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parent.parent / "dist"
SITE = "https://www.connectomelab.com"
ROUTES = ("", "research", "publications", "team", "news", "radar", "ideas", "join")


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.references, self.langs = path, set(), [], {}
        self.language, self.canonical, self.h1s = None, None, 0
        self.duplicates = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "h1":
            self.h1s += 1
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicates.append(attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "link":
            if attrs.get("rel") == "canonical":
                self.canonical = attrs.get("href")
            if attrs.get("rel") == "alternate":
                self.langs[attrs.get("hreflang")] = attrs.get("href")
        for key in ("href", "src"):
            if attrs.get(key):
                self.references.append(attrs[key])


def target(path):
    candidate = ROOT / unquote(path).lstrip("/")
    return candidate / "index.html" if candidate.is_dir() else candidate


def main():
    failures = []
    pages = {path: Page(path) for path in ROOT.rglob("*.html")}
    for path in pages:
        if b"\x00" in path.read_bytes():
            failures.append(f"{path.relative_to(ROOT)}: generated HTML contains NUL bytes")
    checked = 0
    for lang in ("ko", "en"):
        for route in ROUTES:
            url_path = ("/en/" if lang == "en" else "/") + route
            path = target(url_path)
            if path not in pages:
                failures.append(f"Missing route: {url_path}")
                continue
            page = pages[path]
            checked += 1
            if page.language != lang or page.h1s != 1:
                failures.append(f"{url_path}: language={page.language}, h1 count={page.h1s}")
            if (page.canonical or "").rstrip("/") != (SITE + url_path).rstrip("/"):
                failures.append(f"{url_path}: incorrect canonical URL")
            for alternate in ("ko", "en", "x-default"):
                if not page.langs.get(alternate):
                    failures.append(f"{url_path}: missing hreflang {alternate}")
            if page.duplicates:
                failures.append(f"{url_path}: duplicate IDs {page.duplicates}")
            for reference in page.references:
                parsed = urlsplit(reference)
                if parsed.scheme and parsed.scheme not in ("https", "http", "mailto", "tel", "data"):
                    failures.append(f"{url_path}: unsafe URL scheme {parsed.scheme}")
                if parsed.netloc and parsed.netloc != "www.connectomelab.com":
                    continue
                if parsed.scheme in ("mailto", "tel", "data"):
                    continue
                if not parsed.path:
                    destination = path
                elif parsed.path.startswith("/"):
                    destination = target(parsed.path)
                else:
                    destination = path.parent / unquote(parsed.path)
                    if destination.is_dir():
                        destination = destination / "index.html"
                if not destination.exists():
                    failures.append(f"{url_path}: missing local target {reference}")
                elif parsed.fragment and destination in pages and unquote(parsed.fragment) not in pages[destination].ids:
                    failures.append(f"{url_path}: missing fragment {reference}")
    for route in ROUTES:
        legacy = target("/ko/" + route)
        if not legacy.exists() or "http-equiv=" not in legacy.read_text().lower():
            failures.append(f"Missing legacy Korean redirect: /ko/{route}")
    if failures:
        print("\n".join(sorted(set(failures))))
        return 1
    print(f"Built-site contract passed: {checked} bilingual pages, legacy redirects, local links/assets and fragments.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
