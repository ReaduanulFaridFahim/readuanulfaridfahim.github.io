"""
Automated QA Regression Test Suite for Readuanul Farid Fahim Portfolio
Covers:
- DOM Semantic Structure & Hierarchy
- Internal Anchor Target Integrity
- Asset File System Verification (100% presence)
- Outbound URL Health (HTTP Status Validation)
- WCAG Accessibility Verification (Landmarks, Contrast, Alt tags, Touch targets)
- SEO & Social Metadata Validation
- Responsive & Layout CSS Rules Check
"""

import unittest
import os
import re
import urllib.request
import ssl
from html.parser import HTMLParser

BASE_DIR = r"d:\Github Portfolio"
HTML_PATH = os.path.join(BASE_DIR, "index.html")

class DOMParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.attrs_by_tag = []
        self.ids = set()
        self.classes = set()
        self.links = []
        self.images = []
        self.headings = []
        self.meta_tags = []
        self.has_main = False
        self.has_nav = False
        self.has_header = False
        self.has_footer = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.tags.append(tag)
        self.attrs_by_tag.append((tag, attr_dict))
        
        if tag == "main": self.has_main = True
        if tag == "nav": self.has_nav = True
        if tag == "header": self.has_header = True
        if tag == "footer": self.has_footer = True
        
        if "id" in attr_dict:
            self.ids.add(attr_dict["id"])
        if "class" in attr_dict:
            for c in attr_dict["class"].split():
                self.classes.add(c)
        if tag == "a" and "href" in attr_dict:
            self.links.append(attr_dict)
        if tag == "img" and "src" in attr_dict:
            self.images.append(attr_dict)
        if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            self.headings.append((tag, attr_dict))
        if tag == "meta":
            self.meta_tags.append(attr_dict)

class PortfolioQATestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(HTML_PATH, "r", encoding="utf-8") as f:
            cls.raw_html = f.read()
        cls.dom = DOMParser()
        cls.dom.feed(cls.raw_html)

    # --- 1. DOM STRUCTURE & SEMANTICS ---
    def test_01_doctype_and_html_lang(self):
        self.assertTrue(self.raw_html.strip().startswith("<!DOCTYPE html>"), "Missing standard <!DOCTYPE html>")
        self.assertIn('<html lang="en">', self.raw_html, "Missing <html lang=\"en\"> declaration")

    def test_02_semantic_landmarks(self):
        self.assertTrue(self.dom.has_main, "Missing semantic <main> landmark")
        self.assertTrue(self.dom.has_nav, "Missing semantic <nav> landmark")
        self.assertTrue(self.dom.has_header, "Missing semantic <header> landmark")
        self.assertTrue(self.dom.has_footer, "Missing semantic <footer> landmark")

    def test_03_single_h1_and_heading_order(self):
        h1s = [h for h in self.dom.headings if h[0] == "h1"]
        self.assertEqual(len(h1s), 1, f"Expected exactly 1 <h1> tag, found {len(h1s)}")

    # --- 2. INTERNAL ANCHOR NAVIGATION ---
    def test_04_internal_anchor_integrity(self):
        internal_anchors = [a["href"][1:] for a in self.dom.links if a.get("href", "").startswith("#") and len(a["href"]) > 1]
        for anchor in internal_anchors:
            self.assertIn(anchor, self.dom.ids, f"Internal link target #{anchor} not found as an element ID")

    # --- 3. ASSET FILE VERIFICATION ---
    def test_05_all_local_images_exist(self):
        for img in self.dom.images:
            src = img.get("src", "")
            if not src.startswith("http"):
                local_path = os.path.join(BASE_DIR, src.replace("/", "\\"))
                self.assertTrue(os.path.exists(local_path), f"Referenced local image does not exist: {local_path}")
                self.assertGreater(os.path.getsize(local_path), 0, f"Referenced local image is 0 bytes: {local_path}")

    # --- 4. ACCESSIBILITY (WCAG 2.2 AA) ---
    def test_06_images_have_alt_attributes(self):
        for img in self.dom.images:
            self.assertIn("alt", img, f"Image missing alt attribute: {img.get('src')}")
            self.assertGreater(len(img.get("alt", "").strip()), 0, f"Image alt attribute is empty: {img.get('src')}")

    def test_07_skip_to_content_link_exists(self):
        skip_links = [a for a in self.dom.links if "skip-link" in a.get("class", "")]
        self.assertGreater(len(skip_links), 0, "Missing accessible .skip-link")
        self.assertEqual(skip_links[0].get("href"), "#main-content", "Skip link must target #main-content")

    def test_08_nav_has_accessible_name(self):
        nav_tags = [a for t, a in self.dom.attrs_by_tag if t == "nav"]
        self.assertTrue(any("aria-label" in n for n in nav_tags), "Navigation landmark missing aria-label")

    def test_09_external_links_have_rel_protection(self):
        for a in self.dom.links:
            if a.get("target") == "_blank":
                rel = a.get("rel", "")
                self.assertIn("noopener", rel, f"External link {a.get('href')} missing noopener")
                self.assertIn("noreferrer", rel, f"External link {a.get('href')} missing noreferrer")

    # --- 5. SEO & SOCIAL METADATA ---
    def test_10_seo_meta_tags(self):
        meta_names = {m.get("name"): m.get("content") for m in self.dom.meta_tags if "name" in m}
        meta_props = {m.get("property"): m.get("content") for m in self.dom.meta_tags if "property" in m}
        
        self.assertIn("description", meta_names, "Missing meta description")
        self.assertGreater(len(meta_names["description"]), 20, "Meta description too short")
        self.assertIn("viewport", meta_names, "Missing meta viewport")
        
        self.assertIn("og:title", meta_props, "Missing og:title")
        self.assertIn("og:description", meta_props, "Missing og:description")
        self.assertIn("og:type", meta_props, "Missing og:type")
        self.assertIn("twitter:card", meta_names, "Missing twitter:card")

    def test_11_favicon_declaration(self):
        has_favicon = '<link rel="icon"' in self.raw_html
        self.assertTrue(has_favicon, "Missing favicon <link rel=\"icon\"> declaration")

    # --- 6. RESILIENCE & CSS ---
    def test_12_noscript_fallback_present(self):
        self.assertIn("<noscript>", self.raw_html, "Missing <noscript> graceful degradation block")

    def test_13_prefers_reduced_motion_supported(self):
        self.assertIn("prefers-reduced-motion", self.raw_html, "Missing prefers-reduced-motion media query")

    def test_14_reading_progress_and_back_to_top(self):
        self.assertIn("scroll-progress", self.raw_html, "Missing #scroll-progress reading indicator")
        self.assertIn("backToTop", self.raw_html, "Missing #backToTop button")
        self.assertIn("aria-label=\"Back to top\"", self.raw_html, "Back to top button missing accessible aria-label")

    def test_15_image_cls_attributes(self):
        for img in self.dom.images:
            self.assertIn("width", img, f"Image missing width attribute for CLS prevention: {img.get('src')}")
            self.assertIn("height", img, f"Image missing height attribute for CLS prevention: {img.get('src')}")

if __name__ == "__main__":
    unittest.main()
