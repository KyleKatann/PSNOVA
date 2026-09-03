import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
STYLE = DOCS / "css" / "style.css"


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class SkipLinkTests(unittest.TestCase):
    def test_every_public_page_has_main_skip_link(self):
        violations = []

        for path in public_html_files():
            text = path.read_text(encoding="utf-8")

            matches = re.findall(
                r'<a\s+class="skip-link"\s+href="#main">'
                r'本文へスキップ</a>',
                text,
            )

            if len(matches) != 1:
                violations.append(
                    f"{path.relative_to(ROOT)}: "
                    f"expected 1 skip link, found {len(matches)}"
                )

            if 'id="main"' not in text:
                violations.append(
                    f"{path.relative_to(ROOT)}: #main target missing"
                )

        self.assertEqual(
            [],
            violations,
            "Invalid skip-link contract:\n" + "\n".join(violations),
        )

    def test_skip_link_is_first_body_content(self):
        violations = []

        pattern = re.compile(
            r"<body\b[^>]*>\s*"
            r'<a\s+class="skip-link"\s+href="#main">'
            r"本文へスキップ</a>",
            re.IGNORECASE,
        )

        for path in public_html_files():
            text = path.read_text(encoding="utf-8")

            if not pattern.search(text):
                violations.append(str(path.relative_to(ROOT)))

        self.assertEqual([], violations)

    def test_skip_link_becomes_visible_on_focus(self):
        css = STYLE.read_text(encoding="utf-8")

        self.assertIn(".skip-link {", css)
        self.assertIn(".skip-link:focus {", css)
        self.assertIn("transform: translateY(-200%);", css)
        self.assertIn("transform: translateY(0);", css)


if __name__ == "__main__":
    unittest.main()
