#!/usr/bin/env python3
"""Offline checks for untrusted issue/model inputs at the news draft boundary."""
import datetime
import json
import unittest
from news_from_issue import render_drafts, safe_link, yaml_quote


class NewsDraftTests(unittest.TestCase):
    def setUp(self):
        self.fields = {"date": "2026-09-09", "category": "conference", "link": "https://example.org/program"}
        self.story = {"titleEn": "A conference presentation", "titleKo": "학회 연구 발표 소식",
                      "bodyEn": "The lab presented a poster.", "bodyKo": "연구실에서 포스터를 발표했다."}

    def test_bilingual_pair_and_source(self):
        drafts = render_drafts(self.fields, self.story, 42)
        self.assertEqual(len(drafts), 2)
        en = next(name for name in drafts if not name.endswith("-ko.md"))
        ko = drafts[en[:-3] + "-ko.md"]
        self.assertIn(f'baseSlug: "{en[:-3]}"', ko)
        self.assertIn('link: "https://example.org/program"', ko)

    def test_unsafe_links_fail(self):
        for value in ("javascript:alert(1)", "data:text/html,boom", "//example.org", "https://user:pass@example.org", "https://example.org/\nboom"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_link(value)

    def test_invalid_dates_and_headline_newlines_fail(self):
        for date in ("2026-02-30", "2026-9-9", "unknown"):
            with self.subTest(date=date), self.assertRaises(ValueError):
                render_drafts({**self.fields, "date": date}, self.story, 42)
        with self.assertRaises(ValueError):
            render_drafts(self.fields, {**self.story, "titleEn": "Headline\ncategory: award"}, 42)

    def test_model_html_links_and_frontmatter_are_text(self):
        payload = '<script>alert(1)</script> [click](javascript:alert(1))\n---\n# injected'
        files = render_drafts(self.fields, {**self.story, "bodyEn": payload}, 42)
        en = next(text for name, text in files.items() if not name.endswith("-ko.md"))
        self.assertNotIn("<script>", en)
        self.assertNotIn("[click](", en)
        self.assertNotIn("\n---\n# injected", en)
        self.assertEqual(json.loads(yaml_quote('Quotes " and\nnewlines')), 'Quotes " and\nnewlines')


if __name__ == "__main__":
    unittest.main()
