#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

CHROME_PATH = "/home/juke/.cache/ms-playwright/chromium-1217/chrome-linux/chrome"
URL = "http://100.92.111.86:8790/v/CqiDQ-iX6d0R/"
OUT_DIR = "/home/juke/git/lab-homepage/claudedocs/prototypes/screenshots"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        # 1. Desktop Full Page
        context_desktop = await browser.new_context(viewport={"width": 1440, "height": 900})
        page_desktop = await context_desktop.new_page()

        console_errors = []
        page_desktop.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print(f"Loading {URL} (Desktop Option E)...")
        await page_desktop.goto(URL, wait_until="networkidle")
        await page_desktop.wait_for_timeout(1000)

        # Screenshot hero
        await page_desktop.screenshot(path=f"{OUT_DIR}/option_e_desktop_hero.png")
        print("✓ Captured option_e_desktop_hero.png")

        # Screenshot full page
        await page_desktop.screenshot(path=f"{OUT_DIR}/option_e_desktop_full.png", full_page=True)
        print("✓ Captured option_e_desktop_full.png")

        # Test iPhone simulator toggle
        await page_desktop.click('#btn-mode-simulator')
        await page_desktop.wait_for_timeout(800)
        await page_desktop.screenshot(path=f"{OUT_DIR}/desktop_iphone_simulator_view_e.png")
        print("✓ Captured desktop_iphone_simulator_view_e.png")

        # 2. Real Mobile Viewport (iPhone 14 / 390x844)
        context_mobile = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
        )
        page_mobile = await context_mobile.new_page()
        print(f"Loading {URL} (Mobile 390px Option E)...")
        await page_mobile.goto(URL, wait_until="networkidle")
        await page_mobile.wait_for_timeout(1000)

        # Screenshot mobile hero
        await page_mobile.screenshot(path=f"{OUT_DIR}/option_e_mobile_hero.png")
        print("✓ Captured option_e_mobile_hero.png")

        # Screenshot mobile full page
        await page_mobile.screenshot(path=f"{OUT_DIR}/option_e_mobile_full.png", full_page=True)
        print("✓ Captured option_e_mobile_full.png")

        # Check horizontal overflow
        body_scroll_w = await page_mobile.evaluate("document.body.scrollWidth")
        inner_w = await page_mobile.evaluate("window.innerWidth")
        print(f"Mobile body scroll width: {body_scroll_w}, inner width: {inner_w}")
        if body_scroll_w > inner_w:
            print("⚠️ Warning: Horizontal overflow detected on mobile!")
        else:
            print("✓ Perfect: Zero horizontal overflow on mobile!")

        print(f"Console errors: {console_errors}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
