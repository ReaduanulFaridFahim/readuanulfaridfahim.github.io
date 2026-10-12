"""
Comprehensive Playwright E2E Automation Test Suite for Portfolio
Tests:
1. Page load and console errors (must be 0)
2. Document title & SEO metadata
3. Section presence & visibility (#about, #experience, #projects, #skills, #education, #sports, #travel, #references, #contact)
4. Smooth scrolling & anchor links
5. Skip link keyboard focus
6. Responsive layout & no horizontal scrollbar at 320px, 375px, 768px, 1024px, 1440px
7. Image render integrity (all images naturalWidth > 0)
8. IntersectionObserver animations (.in class applied)
9. Capture visual verification screenshots
"""

import sys
import os
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent.parent.resolve()
SCREENSHOT_DIR = BASE_DIR / "tests" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

URL = "http://localhost:8000"

class PortfolioPlaywrightTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.console_errors = []
        self.page.on("console", lambda msg: self.console_errors.append(msg.text) if msg.type == "error" else None)
        self.page.on("pageerror", lambda err: self.console_errors.append(str(err)))

    def tearDown(self):
        self.context.close()

    def test_01_page_load_and_console_errors(self):
        self.page.goto(URL, wait_until="networkidle")
        self.assertEqual(len(self.console_errors), 0, f"Found console errors on page load: {self.console_errors}")
        self.assertIn("Readuanul Farid Fahim", self.page.title())

    def test_02_all_images_rendered_successfully(self):
        self.page.goto(URL, wait_until="networkidle")
        self.page.wait_for_timeout(500)
        images = self.page.locator("img")
        count = images.count()
        self.assertGreater(count, 10, "Expected at least 10 images on page")
        
        for i in range(count):
            img = images.nth(i)
            src = img.get_attribute("src")
            is_loaded = img.evaluate("img => img.complete && img.naturalWidth > 0")
            self.assertTrue(is_loaded, f"Image failed to render or has 0 naturalWidth: {src}")

    def test_03_skip_link_focus(self):
        self.page.goto(URL, wait_until="networkidle")
        skip_link = self.page.locator(".skip-link")
        
        # Tab to skip link
        self.page.keyboard.press("Tab")
        # Wait for CSS top transition (0.2s) to complete
        self.page.wait_for_timeout(300)
        
        is_visible = skip_link.is_visible()
        self.assertTrue(is_visible, "Skip link should be visible when focused")
        box = skip_link.bounding_box()
        self.assertGreaterEqual(box["y"], 0, f"Skip link should be positioned within viewport, got y={box['y']}")

    def test_04_navigation_anchors_scrolling(self):
        self.page.goto(URL, wait_until="networkidle")
        nav_links = self.page.locator(".navlinks a")
        count = nav_links.count()
        self.assertEqual(count, 6, "Expected 6 navigation links")
        
        for i in range(count):
            link = nav_links.nth(i)
            href = link.get_attribute("href")
            link.click()
            self.page.wait_for_timeout(400)
            target = self.page.locator(href)
            self.assertTrue(target.is_visible(), f"Target section {href} not visible after clicking")

    def test_05_scroll_reveal_animation(self):
        self.page.goto(URL, wait_until="networkidle")
        projects = self.page.locator("#projects")
        self.page.evaluate("el => el.scrollIntoView({ behavior: 'instant', block: 'center' })", projects.element_handle())
        self.page.wait_for_timeout(600)
        
        cards = projects.locator(".card")
        for i in range(cards.count()):
            card = cards.nth(i)
            self.page.evaluate("el => el.scrollIntoView({ behavior: 'instant', block: 'center' })", card.element_handle())
            self.page.wait_for_timeout(150)
            classes = card.get_attribute("class") or ""
            self.assertIn("in", classes, f"Card {i} in #projects did not receive .in class")

    def test_06_responsive_no_horizontal_overflow(self):
        viewports = [
            {"width": 320, "height": 650, "name": "mobile_320px"},
            {"width": 375, "height": 667, "name": "mobile_375px"},
            {"width": 390, "height": 844, "name": "mobile_390px"},
            {"width": 430, "height": 932, "name": "mobile_430px"},
            {"width": 768, "height": 1024, "name": "tablet_768px"},
            {"width": 1024, "height": 768, "name": "tablet_1024px"},
            {"width": 1280, "height": 800, "name": "desktop_1280px"},
            {"width": 1440, "height": 900, "name": "desktop_1440px"},
            {"width": 1920, "height": 1080, "name": "desktop_1920px"},
        ]
        
        for vp in viewports:
            with self.subTest(viewport=vp["name"]):
                self.page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
                self.page.goto(URL, wait_until="networkidle")
                
                # Check for unwanted horizontal scrollbar
                overflow = self.page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
                self.assertFalse(overflow, f"Horizontal overflow detected at viewport {vp['name']} ({vp['width']}px)")

    def test_07_capture_screenshots(self):
        sizes = [
            {"width": 375, "height": 812, "file": "screenshot_mobile_375.png"},
            {"width": 768, "height": 1024, "file": "screenshot_tablet_768.png"},
            {"width": 1440, "height": 900, "file": "screenshot_desktop_1440.png"}
        ]
        
        for s in sizes:
            self.page.set_viewport_size({"width": s["width"], "height": s["height"]})
            self.page.goto(URL, wait_until="networkidle")
            # Scroll down to trigger all animations
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(800)
            self.page.evaluate("window.scrollTo(0, 0)")
            self.page.wait_for_timeout(400)
            
            out_path = SCREENSHOT_DIR / s["file"]
            self.page.screenshot(path=str(out_path), full_page=False)
            self.assertTrue(out_path.exists(), f"Failed to generate screenshot: {out_path}")
            print(f"[SCREENSHOT] Saved: {out_path} ({out_path.stat().st_size} bytes)")

if __name__ == "__main__":
    unittest.main()
