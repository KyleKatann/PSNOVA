from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE_META = ROOT / "docs" / "js" / "page-meta.js"
AGENT = ROOT / "Agent.md"


class PublicTitleConventionTests(unittest.TestCase):
    def test_metadata_titles_follow_site_first_convention(self):
        source = PAGE_META.read_text(encoding="utf-8")
        entries = re.findall(r'"(/PSNOVA/[^"]*)": \{ title: "([^"]+)"', source)
        self.assertGreater(len(entries), 20)

        for path, title in entries:
            if path in {"/PSNOVA/", "/PSNOVA/index.html"}:
                self.assertEqual(title, "PSNOVA攻略サイト")
            else:
                self.assertTrue(
                    title.startswith("PSNOVA攻略サイト - "),
                    msg=f"{path}: {title}",
                )
                self.assertGreater(len(title.removeprefix("PSNOVA攻略サイト - ").strip()), 0)

    def test_weapon_titles_name_the_linked_content(self):
        source = PAGE_META.read_text(encoding="utf-8")
        expected = {
            "/PSNOVA/pages/weapon.html": "PSNOVA攻略サイト - 武器",
            "/PSNOVA/pages/weapon/sword.html": "PSNOVA攻略サイト - ソード",
            "/PSNOVA/pages/weapon/partizan.html": "PSNOVA攻略サイト - パルチザン",
            "/PSNOVA/pages/weapon/doublesaber.html": "PSNOVA攻略サイト - ダブルセイバー",
            "/PSNOVA/pages/weapon/knuckle.html": "PSNOVA攻略サイト - ナックル",
            "/PSNOVA/pages/weapon/rifle.html": "PSNOVA攻略サイト - アサルトライフル",
            "/PSNOVA/pages/weapon/tmachinegun.html": "PSNOVA攻略サイト - ツインマシンガン",
            "/PSNOVA/pages/weapon/rod.html": "PSNOVA攻略サイト - ロッド",
            "/PSNOVA/pages/weapon/talis.html": "PSNOVA攻略サイト - タリス",
            "/PSNOVA/pages/weapon/wand.html": "PSNOVA攻略サイト - ウォンド",
            "/PSNOVA/pages/weapon/halo.html": "PSNOVA攻略サイト - ヘイロウ",
            "/PSNOVA/pages/weapon/pile.html": "PSNOVA攻略サイト - パイル",
        }
        for path, title in expected.items():
            self.assertIn(f'"{path}": {{ title: "{title}"', source)

    def test_agent_records_title_rule(self):
        guide = AGENT.read_text(encoding="utf-8")
        self.assertIn("Public page titles follow one naming convention", guide)
        self.assertIn("PSNOVA攻略サイト - XXXXX", guide)
        self.assertIn("weapon landing page is `PSNOVA攻略サイト - 武器`", guide)


if __name__ == "__main__":
    unittest.main()
