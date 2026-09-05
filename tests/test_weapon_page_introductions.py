import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEAPON_DIR = ROOT / "docs" / "pages" / "weapon"

WEAPONS = {
    "sword.html": "ソード",
    "partizan.html": "パルチザン",
    "doublesaber.html": "ダブルセイバー",
    "knuckle.html": "ナックル",
    "rifle.html": "アサルトライフル",
    "tmachinegun.html": "ツインマシンガン",
    "rod.html": "ロッド",
    "talis.html": "タリス",
    "wand.html": "ウォンド",
    "halo.html": "ヘイロウ",
    "pile.html": "パイル",
}

PROHIBITED = (
    "武器データを掲載する",
    "一覧で確認できる",
    "このページでは",
)


class WeaponPageIntroductionTests(unittest.TestCase):
    def test_weapon_detail_leads_describe_the_weapon_itself(self):
        for filename, weapon in WEAPONS.items():
            with self.subTest(filename=filename):
                html = (WEAPON_DIR / filename).read_text(encoding="utf-8")
                match = re.search(
                    r'<p class="page-lead">(.*?)</p>',
                    html,
                    re.DOTALL,
                )
                self.assertIsNotNone(match)

                lead = re.sub(r"<[^>]+>", " ", match.group(1))
                lead = " ".join(lead.split())

                self.assertIn(weapon, lead)
                for phrase in PROHIBITED:
                    self.assertNotIn(phrase, lead)


if __name__ == "__main__":
    unittest.main()
