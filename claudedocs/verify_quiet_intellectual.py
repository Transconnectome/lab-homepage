#!/usr/bin/env python3
import http.server
import socketserver
import threading
import time
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

DIST_DIR = Path(__file__).resolve().parent.parent / "dist"
OUTPUT_DIR = Path(__file__).resolve().parent / "screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHROME_PATH = "/home/juke/.cache/ms-playwright/chromium-1217/chrome-linux/chrome"
PORT = 8933

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)
    def log_message(self, format, *args):
        pass

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler) as httpd:
        httpd.serve_forever()

def main():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    print(f"Server started on http://127.0.0.1:{PORT}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        # 1. Desktop 1440x900 (Korean)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(f"http://127.0.0.1:{PORT}/", wait_until="networkidle")
        time.sleep(1)

        # Check horizontal overflow
        scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
        client_w = page.evaluate("() => document.documentElement.clientWidth")
        print(f"Desktop 1440px KO: scrollWidth={scroll_w}, clientWidth={client_w}")
        assert scroll_w <= client_w, f"Horizontal overflow detected on desktop! {scroll_w} > {client_w}"

        # Capture Hero & Full Page
        page.screenshot(path=str(OUTPUT_DIR / "desktop_ko_hero.png"))
        page.screenshot(path=str(OUTPUT_DIR / "desktop_ko_full.png"), full_page=True)
        print("✓ Desktop KO screenshots captured")

        # Test BibTeX copy button click
        btn = page.query_selector(".copy-bib-btn")
        if btn:
            btn.click()
            time.sleep(0.5)
            toast = page.query_selector("#opt-e-toast")
            toast_text = toast.inner_text() if toast else ""
            print(f"✓ Toast on click: '{toast_text}'")

        # 2. Mobile 390x844 (Korean - iPhone 14/15 size)
        page_m = browser.new_page(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
        )
        page_m.goto(f"http://127.0.0.1:{PORT}/", wait_until="networkidle")
        time.sleep(1)

        scroll_m = page_m.evaluate("() => document.documentElement.scrollWidth")
        client_m = page_m.evaluate("() => document.documentElement.clientWidth")
        print(f"Mobile 390px KO: scrollWidth={scroll_m}, clientWidth={client_m}")
        assert scroll_m <= client_m, f"Horizontal overflow detected on mobile! {scroll_m} > {client_m}"

        page_m.screenshot(path=str(OUTPUT_DIR / "mobile_ko_hero.png"))
        page_m.screenshot(path=str(OUTPUT_DIR / "mobile_ko_full.png"), full_page=True)
        print("✓ Mobile KO screenshots captured")

        # 3. Desktop 1440x900 (English)
        page_en = browser.new_page(viewport={"width": 1440, "height": 900})
        page_en.goto(f"http://127.0.0.1:{PORT}/en/", wait_until="networkidle")
        time.sleep(1)

        scroll_en = page_en.evaluate("() => document.documentElement.scrollWidth")
        client_en = page_en.evaluate("() => document.documentElement.clientWidth")
        print(f"Desktop 1440px EN: scrollWidth={scroll_en}, clientWidth={client_en}")
        assert scroll_en <= client_en, f"Horizontal overflow detected on desktop EN! {scroll_en} > {client_en}"

        page_en.screenshot(path=str(OUTPUT_DIR / "desktop_en_hero.png"))
        page_en.screenshot(path=str(OUTPUT_DIR / "desktop_en_full.png"), full_page=True)
        print("✓ Desktop EN screenshots captured")

        # 4. Mobile 390x844 (English)
        page_m_en = browser.new_page(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
        )
        page_m_en.goto(f"http://127.0.0.1:{PORT}/en/", wait_until="networkidle")
        time.sleep(1)

        scroll_m_en = page_m_en.evaluate("() => document.documentElement.scrollWidth")
        client_m_en = page_m_en.evaluate("() => document.documentElement.clientWidth")
        print(f"Mobile 390px EN: scrollWidth={scroll_m_en}, clientWidth={client_m_en}")
        assert scroll_m_en <= client_m_en, f"Horizontal overflow detected on mobile EN! {scroll_m_en} > {client_m_en}"

        page_m_en.screenshot(path=str(OUTPUT_DIR / "mobile_en_hero.png"))
        page_m_en.screenshot(path=str(OUTPUT_DIR / "mobile_en_full.png"), full_page=True)
        print("✓ Mobile EN screenshots captured")

        browser.close()

    print("\n[ALL VISUAL CHECKS PASSED PERFECTLY - ZERO HORIZONTAL OVERFLOW]")

if __name__ == "__main__":
    main()
