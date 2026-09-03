import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

XUA_RE = re.compile(
    r'<meta\b[^>]*\bhttp-equiv\s*=\s*["\']X-UA-Compatible["\'][^>]*>',
    re.IGNORECASE,
)

SCRIPT_TYPE_RE = re.compile(
    r'<script\b[^>]*\btype\s*=\s*["\']text/javascript["\'][^>]*>',
    re.IGNORECASE,
)


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class PublicLegacyHtmlShellTests(unittest.TestCase):
    def test_public_html_has_no_legacy_ie_compatibility_meta(self):
        violations = []

        for path in public_html_files():
            text = path.read_text(encoding="utf-8")
            if XUA_RE.search(text):
                violations.append(str(path.relative_to(ROOT)))

        self.assertEqual([], violations)

    def test_classic_scripts_omit_redundant_javascript_type(self):
        violations = []

        for path in public_html_files():
            text = path.read_text(encoding="utf-8")
            if SCRIPT_TYPE_RE.search(text):
                violations.append(str(path.relative_to(ROOT)))

        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
