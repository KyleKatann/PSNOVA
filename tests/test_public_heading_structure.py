import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


class HeadingParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.headings = []
        self._current = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag in HEADING_TAGS:
            self._current = {
                "level": int(tag[1]),
                "parts": [],
            }
            return

        if tag == "img" and self._current is not None:
            attributes = dict(attrs)
            alt = (attributes.get("alt") or "").strip()
            if alt:
                self._current["parts"].append(alt)

    def handle_data(self, data):
        if self._current is not None:
            value = data.strip()
            if value:
                self._current["parts"].append(value)

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in HEADING_TAGS and self._current is not None:
            self.headings.append(
                (
                    self._current["level"],
                    " ".join(self._current["parts"]).strip(),
                )
            )
            self._current = None


def public_html_files():
    yield from DOCS.rglob("*.html")


class PublicHeadingStructureTests(unittest.TestCase):
    def test_public_heading_structure_is_consistent(self):
        violations = []

        for path in public_html_files():
            parser = HeadingParser()
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()

            headings = parser.headings
            rel = path.relative_to(ROOT)

            h1_count = sum(level == 1 for level, _ in headings)
            if h1_count != 1:
                violations.append(
                    f"{rel}: h1は1個でなければならない（検出: {h1_count}個）"
                )

            for index, (level, name) in enumerate(headings):
                if not name:
                    violations.append(
                        f"{rel}: {index + 1}番目のh{level}見出しが空"
                    )

            for previous, current in zip(headings, headings[1:]):
                previous_level = previous[0]
                current_level = current[0]

                if current_level > previous_level + 1:
                    violations.append(
                        f"{rel}: 見出しレベルが "
                        f"h{previous_level} から h{current_level} へ飛んでいる"
                    )

        self.assertEqual(
            [],
            violations,
            "見出し構造の違反:\n" + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
