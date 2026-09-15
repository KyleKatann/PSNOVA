import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs" / "pages"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


class Pso2PageSplitTests(unittest.TestCase):
    def test_pso2_page_remains_after_basic_system_page_is_retired(self):
        self.assertFalse((PAGES / "faq.html").exists())
        pso2 = (PAGES / "pso2.html").read_text(encoding="utf-8")

        self.assertIn("<h1>PSO2との関係</h1>", pso2)
        self.assertIn("PSO2未経験でもストーリーやシステムを理解できる？", pso2)
        self.assertIn("PSO2って何？", pso2)
        self.assertIn("PSO2プレイヤー向けQ&amp;A", pso2)
        self.assertIn("PSO2にある武器カテゴリ・クラス・種族が一部見当たらない", pso2)
        self.assertIn("PSO2と同じ名前のPAなのに、動きや性能が違うのはなぜ？", pso2)
        self.assertIn("ゼノ・エコー・アフィンを仲間にするには？", pso2)

    def test_sidebar_lists_only_pso2_relationship_page(self):
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        self.assertNotIn('/PSNOVA/pages/faq.html', sidebar)
        self.assertIn('href="/PSNOVA/pages/pso2.html">PSO2との関係</a>', sidebar)

    def test_sitemap_contains_pso2_and_not_basic_system_page(self):
        xml = SITEMAP.read_text(encoding="utf-8")
        self.assertIn(
            "https://kylekatann.github.io/PSNOVA/pages/pso2.html",
            xml,
        )
        self.assertNotIn(
            "https://kylekatann.github.io/PSNOVA/pages/faq.html",
            xml,
        )


if __name__ == "__main__":
    unittest.main()
