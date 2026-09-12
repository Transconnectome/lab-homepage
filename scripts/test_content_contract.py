#!/usr/bin/env python3
"""Content invariants that survive UI changes and automated refreshes."""
import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit
import sync_scholar

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "src/content"


def metadata(path):
    frontmatter = path.read_text().split("---", 2)[1]
    return {key: value.strip().strip('"').strip("'") for key, value in
            re.findall(r"^([A-Za-z]+):\s*(.+)$", frontmatter, re.M)}


class ContentContract(unittest.TestCase):
    def test_language_pairs(self):
        for collection in ("research", "news", "history"):
            pairs = {"en": set(), "ko": set()}
            for path in (CONTENT / collection).glob("*.md"):
                data = metadata(path)
                lang = data.get("lang", "en")
                self.assertIn(lang, pairs)
                slug = data.get("baseSlug") if lang == "ko" else path.stem
                self.assertTrue(slug, path)
                self.assertNotIn(slug, pairs[lang], path)
                pairs[lang].add(slug)
            self.assertEqual(pairs["en"], pairs["ko"], collection)
            if collection == "research":
                self.assertEqual(pairs["en"], {"neuro-x", "computational-genetics-psychiatry",
                                              "art-and-neuroscience", "quantum-machine-learning"})

    def test_mbbn_has_one_published_record(self):
        publications = [json.loads(path.read_text()) for path in (CONTENT / "publications").glob("*.json")]
        mbbn = [paper for paper in publications if (paper.get("doi") or "").lower() in {
            "10.48550/arxiv.2503.23394", "10.1038/s42003-026-10011-7"}]
        self.assertEqual(len(mbbn), 1)
        self.assertEqual(mbbn[0]["kind"], "journal")
        # Test the actual title matcher so the crawler cannot recreate the duplicate.
        old = "Spatiotemporal Learning of Brain Dynamics from fMRI Using Frequency-Specific Multi-Band Attention for Cognitive and Psychiatric Applications"
        new = "Learning brain dynamics across distinct scaling regimes reveals psychiatric signatures"
        def entry(title):
            return {"norm": sync_scholar.norm(title), "toksort": sync_scholar.token_sort(title),
                    "normmain": sync_scholar.main_title(title)}
        self.assertTrue(sync_scholar.same_paper(entry(old), entry(new)))
        self.assertFalse(sync_scholar.same_paper(entry("DIVER-0 EEG foundation model"),
                                               entry("DIVER-1 EEG foundation model")))

    def test_workshop_venues_remain_explicit(self):
        for name in ("neuromamba-2025.json", "diver0-icml-2025.json"):
            paper = json.loads((CONTENT / "publications" / name).read_text())
            self.assertEqual(paper["kind"], "workshop", name)
            self.assertIn("workshop", paper["venue"].lower(), name)

    def test_research_language_pairs_keep_the_same_sources(self):
        for korean in (CONTENT / "research").glob("*-ko.md"):
            english = korean.with_name(korean.name.replace("-ko.md", ".md"))
            def sources(path):
                return set(re.findall(r"\]\((https?://[^\s)]+)\)", path.read_text()))
            self.assertTrue(sources(korean), korean)
            self.assertEqual(sources(korean), sources(english), korean)

    def test_research_editorial_corrections_remain_applied(self):
        # These were explicit PI corrections, not merely alternate wording.
        research = "\n".join(path.read_text() for path in (CONTENT / "research").glob("*.md"))
        research_map = (ROOT / "src/components/3d/brainData.ts").read_text()
        guide = (ROOT / "src/components/common/JoinFaq.astro").read_text()
        for phrase in ("고각성 영화", "high-arousal film", "Social Cognitive and Affective Neuroscience",
                       "obscenefocus.com", "OB/Scene", "옵/신", "전시장", "Leonardo da Vinci", "레오나르도"):
            self.assertNotIn(phrase, research, phrase)
        for phrase in ("OB/Scene", "옵/신"):
            self.assertNotIn(phrase, research_map, phrase)
        for phrase in ("하나의 대규모 뇌 모델", "one Large Brain Model",
                       "endpoint a Large Brain Model", "converging on one"):
            self.assertNotIn(phrase, research + research_map + guide, phrase)
        for language, venue in (("-ko", "워크숍"), ("", "workshop")):
            neuro = (CONTENT / "research" / f"neuro-x{language}.md").read_text()
            for model in ("NeuroMamba", "DIVER-0"):
                highlight = next(line for line in neuro.splitlines()
                                 if line.startswith("  - ") and model in line)
                self.assertIn(venue, highlight, model)

    def test_publication_links_use_http(self):
        for path in (CONTENT / "publications").glob("*.json"):
            data = json.loads(path.read_text())
            for key in ("url", "pdfUrl", "codeUrl"):
                if data.get(key):
                    parsed = urlsplit(data[key])
                    self.assertIn(parsed.scheme, ("https", "http"), (path, key))
                    self.assertTrue(parsed.netloc, (path, key))


if __name__ == "__main__":
    unittest.main()
