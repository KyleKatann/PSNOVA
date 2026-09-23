import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "friendship.html"


class FriendshipPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_misunderstanding_heading_uses_existing_red_notice_box(self):
        html = self.page_html()

        self.assertIn('<aside class="npc-password-warning" role="note"', html)
        self.assertIn("<strong>よくある誤解</strong>", html)
        self.assertIn("background:#fff1f1", html)
        self.assertIn("border-left:4px solid #c83f3f", html)
        self.assertNotIn("<h2>よくある誤解</h2>", html)

    def test_misunderstanding_body_stays_outside_notice_box(self):
        html = self.page_html()

        self.assertIn(
            "</aside>\n                    <h3>シフタやレスタを使うと友好度が上がる？</h3>",
            html,
        )


if __name__ == "__main__":
    unittest.main()
