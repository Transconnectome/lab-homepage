#!/usr/bin/env python3
"""
Connectome Lab - Automated Publication Sync Pipeline (v3)

Fetches ALL publications by Prof. Jiook Cha via the OpenAlex API (cursor
pagination over both author IDs) and writes src/content/publications/*.json
records with a `kind` classification on every record:

    kind = "journal" | "conference" | "workshop" | "preprint"

Design rules:
- Never overwrite an existing record: hand-curated entries win. Dedup is by
  DOI first, then by fuzzy normalized-title matching (titles drift between
  arXiv preprints and journal versions), so re-listings of curated papers
  are skipped even when OpenAlex slugs differ.
- Conference-abstract supplement items (SOBP/ACNP/ECNP/AAIC/ARVO abstract
  issues of Biological Psychiatry, European Neuropsychopharmacology,
  Alzheimer's & Dementia, IOVS, JAACAP, ...), errata/corrections, eLife
  "author response" / public-review objects, supplementary materials, and
  the PhD dissertation are EXCLUDED - they are not archive publications.
- Preprint/journal/conference versions of the same paper are merged with
  priority journal > conference > workshop > preprint (among equals: the
  more recent year, then the one with a DOI). A digit guard keeps
  legitimately distinct versioned papers apart (DIVER-0 vs DIVER-1,
  10-year vs 11-year cohorts, ...).
- labMembers comes from an allowlist built from src/content/members/*.json
  (plus known romanization variants) - NOT from surname heuristics, which
  mislabel external co-authors as lab members.
- Auto-synced records are featured: false; featuring is a manual editorial
  decision - except the lab's flagship Nature Communications paper
  (FLAGSHIP_DOI), which is re-marked featured on every sync.
- Venues: repository display names are mapped to reader-friendly preprint
  names ("arXiv preprint", ...); conference papers with no OpenAlex source
  (IEEE QCNC/QAI/QCE, ICASSP, NYSDS, SPIE, ACM, NeurIPS) get their venue
  from Crossref (container-title / event.name). A venue containing
  "Workshop" makes the record kind "workshop".

Usage:
    python3 scripts/sync_scholar.py [--dry-run]
    OPENALEX_CACHE=/path/works.json python3 scripts/sync_scholar.py  # offline
"""

import urllib.request
import urllib.parse
import json
import os
import re
import sys
import glob
from difflib import SequenceMatcher

OPENALEX_AUTHOR_IDS = "A5033979262|A5093826967"
# NOTE: type_crossref is requested but the OpenAlex API currently omits it
# from select responses; the code treats it as optional.
OPENALEX_SELECT = (
    "id,title,publication_year,doi,type,type_crossref,authorships,"
    "primary_location,biblio,is_paratext"
)
OPENALEX_BASE = (
    "https://api.openalex.org/works"
    f"?filter=author.id:{OPENALEX_AUTHOR_IDS}"
    "&sort=publication_year:desc&per-page=100"
    f"&select={OPENALEX_SELECT}"
)
PUB_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "publications")
MEMBERS_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "members")

USER_AGENT = {"User-Agent": "ConnectomeLab-AutoSync/3.0 (mailto:connectome@snu.ac.kr)"}

# The lab's flagship paper keeps its editorial featuring across re-syncs.
FLAGSHIP_DOI = "10.1038/s41467-025-63312-6"
FLAGSHIP_SPOTLIGHT = "Nature Communications"

KIND_PRIORITY = {"journal": 3, "conference": 2, "workshop": 1, "preprint": 0}

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

# OpenAlex work types that are never archive publications.
EXCLUDED_TYPES = {
    "peer-review",            # eLife "Author response" / "Joint Public Review" objects
    "erratum",                # corrections
    "paratext",
    "dataset",
    "supplementary-materials",
    "dissertation",           # PhD thesis (Stony Brook)
    "retraction",
    "conference-abstract",    # SOBP / CINP poster abstracts
    "libguides",
    "grant",
}

EXCLUDED_TITLE_RE = re.compile(
    r"^\s*(correction|erratum|corrigendum|retraction|author response|joint public review)\b",
    re.IGNORECASE,
)

# Poster / numbered-abstract titles inside journal abstract supplements,
# e.g. "241. Influence of ...", "2.17 RESTING-STATE ...", "P227. ...",
# "PS24. ...", "P1-270: ...".
POSTER_TITLE_RE = re.compile(r"^\s*(?:P|PS)?\d+(?:[.\-‐‑–]\d+)?[.:]\s")

# Repository display name -> reader-friendly venue.
REPOSITORY_VENUES = {
    "arxiv (cornell university)": "arXiv preprint",
    "biorxiv (cold spring harbor laboratory)": "bioRxiv preprint",
    "medrxiv": "medRxiv preprint",
    "research square": "Research Square preprint",
    "ssrn electronic journal": "SSRN preprint",
    "psyarxiv": "PsyArXiv preprint",
    "columbia academic commons (columbia university)": "Columbia Academic Commons",
    "escholarship (california digital library)": "eScholarship repository",
    "unc libraries": "UNC institutional repository",
}

# Same-paper pairs whose titles drifted too far for the fuzzy matcher.
# Each pair is (fragment_in_one_normalized_title, fragment_in_the_other).
# All were manually verified as preprint/journal versions of ONE paper.
MANUAL_MERGE_FRAGMENTS = [
    # JAMA Network Open 2022 <- Research Square 2020/2021 + medRxiv 2020
    ("associationofgenomewidepolygenicscoresformultiplepsychiatric",
     "genomewidepolygenicscoresformultiplepsychiatricandcommontraitsidentify"),
    ("associationofgenomewidepolygenicscoresformultiplepsychiatric",
     "genomewidepolygenicscoresforcommontraitsandpsychiatricdisorders"),
    # BMC Genomic Data 2023 <- bioRxiv 2022
    ("overestimatedpredictionusingpolygenicprediction",
     "overestimatedpolygenicpredictionduetooverlappingsubjects"),
    # npj Digital Medicine 2020 <- bioRxiv 2019 (EHR-based AD prediction)
    ("machinelearningpredictionofincidenceofalzheimers",
     "electronichealthrecordsbasedpredictionoffutureincidenceofalzheimers"),
    # Heliyon 2023 <- SSRN 2022 / medRxiv 2021
    ("earlylifestressmodulatesthegeneticinfluence",
     "theimpactofearlylifestressonthegeneticinfluence"),
    # NeuroImage: Clinical 2019 <- bioRxiv 2018 x2 + Columbia report 2018
    ("diagnosisandprognosisofalzheimersdiseaseusingbrainmorphometry",
     "diagnosisandprognosisusingmachinelearningtrainedonbrainmorphometry"),
    # Research Square v1 vs v2 retitle of one study (intertemporal/economic
    # decision making under neighborhood deprivation)
    ("neighborhoodsocioeconomicdeprivationonintertemporaldecisionmaking",
     "neighborhoodsocioeconomicdeprivationoneconomicdecisionmaking"),
    # Human Brain Mapping 2022 <- OSF preprint 2021 (identical author list)
    ("genethesexualbrainandcognition",
     "thesexualbraingenesandcognition"),
]


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
    title = re.sub(r"</?[a-zA-Z][^>]*>", "", title).strip()
    # strip trailing "(Preprint" / "(Preprint)" suffix (JMIR-style deposits)
    title = re.sub(r"\s*\(Preprint\)?\s*$", "", title, flags=re.IGNORECASE)
    return title.strip()


def clean_filename(title):
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", title).strip().lower()
    return re.sub(r"[\s-]+", "-", cleaned)[:40]


# Canonical publication tags — one shared level of granularity (research domain).
# Modalities (fMRI, EEG), architectures and sub-fields are folded into their domain so
# the /publications filter never shows a chip matching a single paper.
# Keep in sync with PUBLICATION_TAGS in src/content/config.ts.
PUBLICATION_TAGS = [
    "AI & Foundation Models",
    "Genetics",
    "Neuroimaging",
    "Neuroscience",
    "Psychiatry",
    "Quantum ML",
]


def derive_tags(title):
    t = title.lower()
    tags = []
    if re.search(r"\bfmri\b|\bmri\b|neuroimag|\beeg\b|\becog\b|\bieeg\b", t):
        tags.append("Neuroimaging")
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
    return [tag for tag in PUBLICATION_TAGS if tag in tags]


def fetch_all_openalex_works():
    cache = os.environ.get("OPENALEX_CACHE")
    if cache and os.path.exists(cache):
        print(f"[*] loading works from cache: {cache}")
        return json.load(open(cache, encoding="utf-8"))
    results, cursor = [], "*"
    while cursor:
        url = f"{OPENALEX_BASE}&cursor={urllib.parse.quote(cursor)}"
        req = urllib.request.Request(url, headers=USER_AGENT)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        page = data.get("results", [])
        results.extend(page)
        cursor = data.get("meta", {}).get("next_cursor")
        if not page:
            break
        print(f"[*] fetched {len(results)} works so far...")
    if cache:
        json.dump(results, open(cache, "w", encoding="utf-8"))
    return results


# ---------------------------------------------------------------------------
# Exclusion rules (conference abstracts, errata, review objects, ...)
# ---------------------------------------------------------------------------

def exclusion_reason(work):
    """Return a human-readable reason to drop this work, or None to keep it."""
    if work.get("is_paratext"):
        return "paratext"
    wtype = work.get("type") or ""
    if wtype in EXCLUDED_TYPES:
        return f"type={wtype}"
    if (work.get("type_crossref") or "") == "journal-issue":
        return "type_crossref=journal-issue"
    title = work.get("title") or ""
    if not title:
        return "no title"
    if EXCLUDED_TITLE_RE.search(title):
        return "correction/erratum/author-response title"

    loc = work.get("primary_location") or {}
    src = loc.get("source") or {}
    src_name = (src.get("display_name") or "")
    src_norm = src_name.lower()
    bib = work.get("biblio") or {}
    first = bib.get("first_page") or ""
    last = bib.get("last_page") or ""
    issue = bib.get("issue") or ""

    if (src.get("type") or "") == "journal":
        # S-numbered pages = abstract supplements (Biological Psychiatry,
        # ENP, JAACAP, Molecular Psychiatry supplements, BP:GOS, ...)
        if re.fullmatch(r"S\d+", first):
            return f"abstract supplement (pages {first}-{last} in {src_name})"
        # ECNP congress abstracts in European Neuropsychopharmacology use
        # e-numbered pages (real journals use e-article-numbers, so this
        # rule is venue-restricted).
        if "european neuropsychopharmacology" in src_norm and re.fullmatch(r"e\d+", first):
            return f"abstract supplement (pages {first}-{last} in {src_name})"
        # AAIC abstracts in Alzheimer's & Dementia: supplement issues
        # (S2, S3, 7S_Part_x) with no page numbers.
        if "alzheimer" in src_norm and not first and ("S" in issue):
            return f"AAIC abstract (issue {issue} of {src_name})"
        # ARVO annual-meeting abstracts: IOVS issue 13, single page.
        if "investigative ophthalmology" in src_norm and first and first == last:
            return f"ARVO abstract (page {first} in {src_name})"
        # Poster/abstract numbering in the title ("241. ...", "P1-270: ...").
        if POSTER_TITLE_RE.match(title):
            return f"numbered poster/abstract title in {src_name}"
    return None


# ---------------------------------------------------------------------------
# kind classification + venue resolution
# ---------------------------------------------------------------------------

def classify_kind(work):
    wtype = work.get("type") or ""
    xref = work.get("type_crossref") or ""
    src = ((work.get("primary_location") or {}).get("source") or {})
    src_type = src.get("type") or ""
    if wtype == "conference-paper" or xref == "proceedings-article" or src_type == "conference":
        return "conference"
    if src_type == "book series":  # LNCS / Studies in Computational Intelligence
        return "conference"
    if src_type == "repository" or wtype == "preprint":
        return "preprint"
    if wtype in ("article", "review") and src_type == "journal":
        return "journal"
    # No source / unknown: almost always an alternate deposit of another
    # version; give it lowest priority so dedup folds it away.
    return "preprint"


_crossref_cache = {}


def crossref_venue(doi):
    """Container-title (preferred) or event name for a DOI, via Crossref."""
    if doi in _crossref_cache:
        return _crossref_cache[doi]
    venue = None
    try:
        req = urllib.request.Request(
            f"https://api.crossref.org/works/{urllib.parse.quote(doi)}",
            headers=USER_AGENT,
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            msg = json.load(resp).get("message", {})
        container = (msg.get("container-title") or [None])[0]
        event = (msg.get("event") or {}).get("name")
        venue = container or event
    except Exception as e:
        print(f"[!] crossref lookup failed for {doi}: {e}")
    _crossref_cache[doi] = venue
    return venue


def resolve_venue(work, kind, doi):
    loc = work.get("primary_location") or {}
    src = loc.get("source") or {}
    name = src.get("display_name")
    landing = loc.get("landing_page_url") or ""

    if kind == "preprint":
        if name:
            return REPOSITORY_VENUES.get(name.lower(), name)
        return "arXiv preprint" if "arxiv" in landing.lower() else "Preprint"

    if kind == "conference":
        # OpenAlex often has no source for IEEE/ACM/SPIE proceedings, and
        # only the series name for Springer volumes -> ask Crossref.
        if (not name or (src.get("type") or "") == "book series") and doi:
            venue = crossref_venue(doi)
            if venue:
                return venue
        return name or "Conference proceedings"

    return name or ("arXiv preprint" if "arxiv" in landing.lower() else "Preprint")


# ---------------------------------------------------------------------------
# Fuzzy duplicate detection across preprint/journal/conference versions
# ---------------------------------------------------------------------------

def _digit_tokens(norm_title):
    return sorted(re.findall(r"\d+", norm_title))


def token_sort(title):
    """Alphabetically sorted word tokens - detects word-order flips."""
    return " ".join(sorted(re.findall(r"[a-z0-9]+", (title or "").lower())))


def main_title(title):
    """Normalized pre-colon part of a title (subtitle stripped)."""
    return norm((title or "").split(":")[0])


def same_paper(ea, eb):
    """True when two entries' titles refer to the same paper.

    Titles drift between arXiv and journal versions, so beyond exact
    equality we use containment, SequenceMatcher ratio, sorted-token ratio
    (word-order flips), a truncated-prefix ratio and a subtitle-stripped
    ratio (subtitle drift). A digit guard keeps versioned siblings
    (DIVER-0 vs DIVER-1, SwiFT vs its follow-up, 10-year vs 11-year
    cohorts) from being merged; a near-identity escape (>= 0.965) still
    merges cohort-count drift like "3,049 Adults" vs "3047 adults".
    """
    na, nb = ea["norm"], eb["norm"]
    if not na or not nb:
        return False
    if na == nb:
        return True
    ratio = SequenceMatcher(None, na, nb).ratio()
    if ratio >= 0.965:  # near-identical even if a numeral drifted
        return True
    if _digit_tokens(na) != _digit_tokens(nb):
        return False
    shorter, longer = (na, nb) if len(na) <= len(nb) else (nb, na)
    if len(shorter) >= 30 and shorter in longer:
        return True
    if ratio >= 0.88:
        return True
    # word-order flips ("Gene, the Sexual Brain, ..." vs "The sexual brain,
    # genes, ...") -> compare sorted word tokens
    if min(len(na), len(nb)) >= 40 and \
            SequenceMatcher(None, ea["toksort"], eb["toksort"]).ratio() >= 0.92:
        return True
    # subtitle drift: same paper, journal version dropped the long subtitle
    m = min(len(na), len(nb))
    if m >= 45 and SequenceMatcher(None, na[:m], nb[:m]).ratio() >= 0.90:
        return True
    ma, mb = ea["normmain"], eb["normmain"]
    if min(len(ma), len(mb)) >= 40 and SequenceMatcher(None, ma, mb).ratio() >= 0.90:
        return True
    for fa, fb in MANUAL_MERGE_FRAGMENTS:
        if (fa in na and fb in nb) or (fb in na and fa in nb):
            return True
    return False


class UnionFind:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, i):
        while self.p[i] != i:
            self.p[i] = self.p[self.p[i]]
            i = self.p[i]
        return i

    def union(self, i, j):
        ri, rj = self.find(i), self.find(j)
        if ri != rj:
            self.p[rj] = ri


def load_existing_entries():
    """Records already on disk (curated first, then any previous auto-sync).

    They participate in dedup as the KEPT version of their paper: an
    OpenAlex work matching an existing record is never written again.
    """
    entries = []
    for path in sorted(glob.glob(os.path.join(PUB_DIR, "*.json"))):
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        doi = (d.get("doi") or "").replace("https://doi.org/", "").lower()
        entries.append({
            "existing": True,
            "path": path,
            "title": d.get("title") or "",
            "norm": norm(d.get("title")),
            "toksort": token_sort(d.get("title")),
            "normmain": main_title(d.get("title")),
            "doi": doi,
            "year": d.get("year") or 0,
            "kind": d.get("kind") or "journal",
        })
    return entries


def main():
    dry_run = "--dry-run" in sys.argv
    os.makedirs(PUB_DIR, exist_ok=True)
    allowlist = load_member_allowlist()
    print(f"[*] member allowlist: {len(allowlist)} names")

    works = fetch_all_openalex_works()
    print(f"[+] total works from OpenAlex: {len(works)}")

    # -- 1. exclusion pass ---------------------------------------------------
    kept_works, excluded = [], []
    for w in works:
        reason = exclusion_reason(w)
        if reason:
            excluded.append((reason, clean_title(w.get("title") or "?")))
        else:
            kept_works.append(w)
    print(f"[+] excluded {len(excluded)} non-publication items:")
    for reason, title in excluded:
        print(f"    - [{reason}] {title[:80]}")

    # -- 2. build entries with kind + venue ----------------------------------
    entries = load_existing_entries()
    n_existing = len(entries)
    print(f"[*] existing records on disk (kept as-is): {n_existing}")
    for w in kept_works:
        title = clean_title(w.get("title"))
        doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
        kind = classify_kind(w)
        venue = resolve_venue(w, kind, doi)
        if "workshop" in (venue or "").lower():
            kind = "workshop"
        authors = [a.get("author", {}).get("display_name", "")
                   for a in w.get("authorships", [])]
        authors = list(dict.fromkeys(a for a in authors if a))
        entries.append({
            "existing": False,
            "work": w,
            "title": title,
            "norm": norm(title),
            "toksort": token_sort(title),
            "normmain": main_title(title),
            "doi": doi,
            "year": w.get("publication_year") or 0,
            "kind": kind,
            "venue": venue,
            "authors": authors,
            "id": w.get("id") or "",
            "landing": (w.get("primary_location") or {}).get("landing_page_url"),
        })

    # -- 3. dedup: union by DOI, then fuzzy title ----------------------------
    uf = UnionFind(len(entries))
    by_doi = {}
    for i, e in enumerate(entries):
        if e["doi"]:
            if e["doi"] in by_doi:
                uf.union(by_doi[e["doi"]], i)
            else:
                by_doi[e["doi"]] = i
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            if same_paper(entries[i], entries[j]):
                uf.union(i, j)

    groups = {}
    for i in range(len(entries)):
        groups.setdefault(uf.find(i), []).append(i)

    # -- 4. pick a winner per group ------------------------------------------
    to_write, merged_report = [], []
    for members in groups.values():
        es = [entries[i] for i in members]
        existing = [e for e in es if e["existing"]]
        if existing:
            winner = existing[0]
        else:
            winner = max(es, key=lambda e: (
                KIND_PRIORITY.get(e["kind"], 0), e["year"], bool(e["doi"]),
                len(e["norm"]), e.get("id", "")))
        losers = [e for e in es if e is not winner]
        # identical-title OpenAlex duplicates are silent; report real merges
        for l in losers:
            if l["norm"] != winner["norm"] or l["kind"] != winner["kind"]:
                merged_report.append((winner, l))
        if not winner["existing"]:
            to_write.append(winner)

    if merged_report:
        print(f"[+] merged {len(merged_report)} duplicate versions:")
        for w_, l_ in merged_report:
            print(f"    KEPT [{w_['kind']:10s}] {w_['title'][:70]}")
            print(f"    DROP [{l_['kind']:10s}] {l_['title'][:70]}")

    # -- 5. write records ----------------------------------------------------
    written, counts = 0, {}
    used_slugs = {os.path.splitext(os.path.basename(p))[0]
                  for p in glob.glob(os.path.join(PUB_DIR, "*.json"))}
    for e in sorted(to_write, key=lambda x: (-x["year"], x["norm"])):
        doi = e["doi"]
        record = {
            "title": e["title"],
            "authors": e["authors"],
            "venue": e["venue"],
            "year": e["year"],
            "doi": doi if doi else None,
            "url": f"https://doi.org/{doi}" if doi else e.get("landing"),
            "tags": derive_tags(e["title"]),
            "featured": False,
            "labMembers": match_lab_members(e["authors"], allowlist),
            "kind": e["kind"],
        }
        if doi == FLAGSHIP_DOI.lower():
            record["featured"] = True
            record["spotlight"] = FLAGSHIP_SPOTLIGHT
        slug = f"{clean_filename(e['title'])}-{e['year']}"
        base, n = slug, 2
        while slug in used_slugs:
            slug = f"{base}-{n}"
            n += 1
        used_slugs.add(slug)
        counts[e["kind"]] = counts.get(e["kind"], 0) + 1
        if dry_run:
            print(f"    would write [{e['kind']:10s}] {slug}.json")
        else:
            with open(os.path.join(PUB_DIR, f"{slug}.json"), "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2, ensure_ascii=False)
                f.write("\n")
        written += 1

    print(f"[✓] Auto-sync finished. Wrote {written} records "
          f"(+ {n_existing} existing kept). By kind: {counts}")


if __name__ == "__main__":
    main()
