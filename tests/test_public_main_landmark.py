import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class PublicMainLandmarkTests(unittest.TestCase):
    def test_every_public_page_has_exactly_one_native_main(self):
        violations = []

        for path in public_html_files():
            text = path.read_text(encoding="utf-8")

            mains = re.findall(
                r'<main\b[^>]*\bid=["\']main["\'][^>]*>',
                text,
                re.IGNORECASE,
            )

            if len(mains) != 1:
                violations.append(
                    f"{path.relative_to(ROOT)}: "
                    f"expected 1 main#main, found {len(mains)}"
                )

            if re.search(
                r'<div\b[^>]*\bid=["\']main["\']',
                text,
                re.IGNORECASE,
            ):
                violations.append(
                    f"{path.relative_to(ROOT)}: legacy div#main remains"
                )

            if text.count("</main>") != 1:
                violations.append(
                    f"{path.relative_to(ROOT)}: "
                    f"expected 1 </main>, found {text.count('</main>')}"
                )

        self.assertEqual(
            [],
            violations,
            "Invalid main landmark structure:\n"
            + "\n".join(violations),
        )

    def test_skip_link_targets_native_main(self):
        violations = []

        for path in public_html_files():
            text = path.read_text(encoding="utf-8")

            if 'href="#main"' not in text:
                violations.append(
                    f"{path.relative_to(ROOT)}: skip link missing"
                )

            if not re.search(
                r'<main\b[^>]*\bid=["\']main["\']',
                text,
                re.IGNORECASE,
            ):
                violations.append(
                    f"{path.relative_to(ROOT)}: native #main missing"
                )

        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
