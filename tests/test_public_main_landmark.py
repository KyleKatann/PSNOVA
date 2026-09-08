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
                    f"main#mainは1個でなければならない（検出: {len(mains)}個）"
                )

            if re.search(
                r'<div\b[^>]*\bid=["\']main["\']',
                text,
                re.IGNORECASE,
            ):
                violations.append(
                    f"{path.relative_to(ROOT)}: 旧式のdiv#mainが残っている"
                )

            if text.count("</main>") != 1:
                violations.append(
                    f"{path.relative_to(ROOT)}: "
                    f"</main>は1個でなければならない（検出: {text.count('</main>')}個）"
                )

        self.assertEqual(
            [],
            violations,
            "不正なmainランドマーク構造:\n"
            + "\n".join(violations),
        )

    def test_skip_link_targets_native_main(self):
        violations = []

        for path in public_html_files():
            text = path.read_text(encoding="utf-8")

            if 'href="#main"' not in text:
                violations.append(
                    f"{path.relative_to(ROOT)}: スキップリンクがない"
                )

            if not re.search(
                r'<main\b[^>]*\bid=["\']main["\']',
                text,
                re.IGNORECASE,
            ):
                violations.append(
                    f"{path.relative_to(ROOT)}: main要素の#mainがない"
                )

        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
