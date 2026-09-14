#!/usr/bin/env python3
"""Browser contracts for the research map. Run against a built local preview.

Requires Python Playwright and Chromium. RESEARCH_MAP_URL selects the preview;
PLAYWRIGHT_CHROMIUM_EXECUTABLE optionally selects an installed browser.
"""
import os
from pathlib import Path
import re
import unittest

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get("RESEARCH_MAP_URL", "http://127.0.0.1:4321").rstrip("/")
CHROMIUM = os.environ.get(
    "PLAYWRIGHT_CHROMIUM_EXECUTABLE",
    "/home/juke/.cache/ms-playwright/chromium-1217/chrome-linux/chrome",
)
SLUGS = ("neuro-x", "computational-genetics-psychiatry",
         "quantum-machine-learning", "art-and-neuroscience")


def question(slug, lang):
    suffix = "-ko" if lang == "ko" else ""
    body = (ROOT / "src/content/research" / f"{slug}{suffix}.md").read_text()
    return re.search(r'^question: "(.+)"$', body, re.M).group(1)


class ResearchMap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runtime = sync_playwright().start()
        args = dict(headless=True, args=["--no-sandbox", "--enable-unsafe-swiftshader"])
        if Path(CHROMIUM).is_file():
            args["executable_path"] = CHROMIUM
        cls.browser = cls.runtime.chromium.launch(**args)
        expect.set_options(timeout=4000)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.runtime.stop()

    def setUp(self):
        self.context = self.browser.new_context(viewport={"width": 1440, "height": 1000},
                                                reduced_motion="reduce")
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def open_map(self, lang="ko", width=1440):
        self.page.set_viewport_size({"width": width, "height": 1000})
        self.page.goto(BASE + ("/en/research" if lang == "en" else "/research"),
                       wait_until="networkidle")
        region = self.page.locator("#research-map")
        expect(region.get_by_role("tab")).to_have_count(4)
        return region

    def test_initial_content_is_readable_in_both_languages(self):
        for lang in ("ko", "en"):
            with self.subTest(lang=lang):
                region = self.open_map(lang)
                expect(region.get_by_role("tab", selected=True)).to_have_count(1)
                panel = region.get_by_role("tabpanel")
                expect(panel).to_have_count(1)
                expect(panel).to_contain_text(question(SLUGS[0], lang))
                self.assertGreater(len(panel.inner_text()), 120)
                for slug in SLUGS:
                    expect(region.get_by_role("tab").filter(has_text=question(slug, lang))).to_be_visible()

    def test_all_four_choices_update_content_and_locale_links(self):
        for lang in ("ko", "en"):
            region = self.open_map(lang)
            for index, slug in enumerate(SLUGS):
                with self.subTest(lang=lang, slug=slug):
                    tab = region.get_by_role("tab").nth(index)
                    tab.click()
                    expect(tab).to_have_attribute("aria-selected", "true")
                    panel = region.get_by_role("tabpanel")
                    expect(panel).to_have_count(1)
                    expect(panel).to_contain_text(question(slug, lang))
                    prefix = "/en" if lang == "en" else ""
                    expect(panel.locator(f'a[href="{prefix}/research#{slug}"]')).to_have_count(1)
                    # This checkout keeps detail articles on /research, with stable anchors.
                    expect(self.page.locator(f'article[id="{slug}"]')).to_have_count(1)
                    example = panel.get_by_role("group", name="연구 사례" if lang == "ko" else "Research example")
                    expect(example.get_by_role("link")).to_have_count(1)
                    self.assertTrue(example.get_by_role("link").get_attribute("href").startswith("https://"))

    def test_keyboard_selection_and_focus(self):
        region = self.open_map()
        tabs = region.get_by_role("tab")
        tabs.first.focus()
        for key, index in (("ArrowDown", 1), ("End", 3), ("ArrowDown", 0),
                           ("ArrowUp", 3), ("Home", 0)):
            self.page.keyboard.press(key)
            expect(tabs.nth(index)).to_be_focused()
            expect(tabs.nth(index)).to_have_attribute("aria-selected", "true")
            expect(region.get_by_role("tabpanel")).to_contain_text(question(SLUGS[index], "ko"))

    def test_mobile_selection_does_not_move_to_distant_panel(self):
        region = self.open_map(width=390)
        tab = region.get_by_role("tab").last
        tab.focus()
        before = self.page.evaluate("window.scrollY")
        self.page.keyboard.press("Enter")
        expect(tab).to_have_attribute("aria-selected", "true")
        self.page.wait_for_timeout(400)
        self.assertLessEqual(abs(self.page.evaluate("window.scrollY") - before), 2)
        expect(tab).to_be_focused()

    def test_mobile_question_starts_near_choices(self):
        for lang in ("ko", "en"):
            for width in (320, 390, 768):
                with self.subTest(lang=lang, width=width):
                    region = self.open_map(lang, width)
                    distance = (region.get_by_role("tabpanel").bounding_box()["y"] -
                                region.bounding_box()["y"])
                    # Do not make a visitor read four full questions before the answer.
                    self.assertLessEqual(distance, 450)

    def test_mobile_choices_make_research_purpose_visible(self):
        # Review the selector's visible span, not hidden question text or aria names.
        for lang, terms in (("ko", ("유전", "뇌", "행동", "환경")),
                            ("en", ("Genes", "brain", "behavior", "environment"))):
            region = self.open_map(lang, 320)
            tab = region.get_by_role("tab").nth(1)
            label = tab.locator("span.block").first
            expect(label).to_be_visible()
            for term in terms:
                expect(label).to_contain_text(term)
            self.assertGreaterEqual(tab.bounding_box()["height"], 44)

    def test_relationship_scope_reaches_home_map_article_and_faq(self):
        for lang, terms in (("ko", ("유전", "뇌", "행동", "환경")),
                            ("en", ("gen", "brain", "behavio", "environment"))):
            prefix = "/en" if lang == "en" else ""
            self.page.goto(BASE + prefix + "/", wait_until="networkidle")
            for term in terms:
                self.assertIn(term, self.page.locator("main").inner_text().lower())
            region = self.open_map(lang, 390)
            region.get_by_role("tab").nth(1).click()
            scopes = [region.get_by_role("tabpanel"),
                      self.page.locator("#computational-genetics-psychiatry")]
            for scope in scopes:
                for term in terms:
                    self.assertIn(term, scope.inner_text().lower())
            self.page.goto(BASE + prefix + "/join", wait_until="networkidle")
            self.page.locator("#faq-pi summary").click()
            for term in terms:
                self.assertIn(term, self.page.locator("#faq-pi").inner_text().lower())
            for topic in ("pi", "genetics", "affective", "neurox", "neuromamba", "diver0", "qml"):
                expect(self.page.locator(f"#faq-{topic} a[href]")).to_have_count(1)

    def test_responsive_layout_and_full_image_box(self):
        for lang in ("ko", "en"):
            for width in (320, 390, 768, 1024, 1440):
                with self.subTest(lang=lang, width=width):
                    region = self.open_map(lang, width)
                    self.assertLessEqual(self.page.evaluate("document.documentElement.scrollWidth"), width)
                    for index in range(4):
                        region.get_by_role("tab").nth(index).click()
                        panel = region.get_by_role("tabpanel")
                        box = panel.bounding_box()
                        self.assertGreaterEqual(box["x"], 0)
                        self.assertLessEqual(box["x"] + box["width"], width)
                    image = region.get_by_role("img")
                    expect(image).to_have_count(1)
                    dimensions = image.evaluate("""img => ({
                        loaded: img.complete && img.naturalWidth > 0,
                        ratio: img.naturalWidth / img.naturalHeight,
                        width: img.getBoundingClientRect().width,
                        height: img.getBoundingClientRect().height,
                        fit: getComputedStyle(img).objectFit
                    })""")
                    self.assertTrue(dimensions["loaded"])
                    self.assertTrue(dimensions["fit"] == "contain" or
                                    abs(dimensions["width"] / dimensions["height"] - dimensions["ratio"]) < .02)
                    self.assertLessEqual(self.page.evaluate("document.documentElement.scrollWidth"), width)

    def test_no_javascript_keeps_content_and_all_four_native_routes(self):
        for lang in ("ko", "en"):
            context = self.browser.new_context(java_script_enabled=False, reduced_motion="reduce")
            try:
                page = context.new_page()
                page.goto(BASE + ("/en/research" if lang == "en" else "/research"))
                region = page.locator("#research-map")
                expect(region.locator("#map-panel-neuro-x")).to_contain_text(question(SLUGS[0], lang))
                for slug in SLUGS:
                    link = region.get_by_role("navigation").locator(f'a[href="#{slug}"]')
                    expect(link).to_have_count(1)
                    self.assertGreaterEqual(link.evaluate("a => a.tabIndex"), 0)
                    link.click()
                    self.assertTrue(page.url.endswith("#" + slug))
                    expect(page.locator(f'article[id="{slug}"]')).to_be_visible()
            finally:
                context.close()

    def test_no_webgl_and_no_canvas_dependency(self):
        self.page.add_init_script("""HTMLCanvasElement.prototype.getContext = function() {
            throw new Error('WebGL deliberately unavailable for this test');
        };""")
        errors = []
        self.page.on("pageerror", lambda error: errors.append(str(error)))
        region = self.open_map()
        region.get_by_role("tab").last.click()
        expect(region.get_by_role("tabpanel")).to_contain_text(question(SLUGS[-1], "ko"))
        expect(region.locator("canvas")).to_have_count(0)
        self.assertEqual(errors, [])

    def test_connection_endpoints_have_readable_names(self):
        for lang in ("ko", "en"):
            region = self.open_map(lang)
            endpoints = region.get_by_role("list").locator('a[href^="#"]')
            self.assertEqual(endpoints.count(), 6)
            for link in endpoints.all():
                # Relationships must make sense without memorizing the area numbers.
                self.assertRegex(link.inner_text(), r"[A-Za-z가-힣]{2,}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
