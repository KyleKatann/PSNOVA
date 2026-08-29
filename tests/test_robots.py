import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROBOTS = ROOT / "docs" / "robots.txt"


class RobotsTests(unittest.TestCase):
    def test_public_site_is_crawlable(self):
        text = ROBOTS.read_text(encoding="utf-8")
        self.assertIn("User-agent: *", text)
        self.assertIn("Allow: /", text)

    def test_generation_tools_are_not_requested_for_crawling(self):
        text = ROBOTS.read_text(encoding="utf-8")
        self.assertIn("Disallow: /PSNOVA/pages/tools/", text)

    def test_sitemap_is_declared(self):
        text = ROBOTS.read_text(encoding="utf-8")
        self.assertIn("Sitemap: https://kylekatann.github.io/PSNOVA/sitemap.xml", text)


if __name__ == "__main__":
    unittest.main()
