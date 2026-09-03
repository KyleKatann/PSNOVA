import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class ImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            self.images.append(dict(attrs))


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class PublicImageDimensionTests(unittest.TestCase):
    def test_every_public_image_has_both_dimensions(self):
        violations = []

        for path in public_html_files():
            parser = ImageParser()
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()

            for image in parser.images:
                src = image.get("src", "")
                width = image.get("width")
                height = image.get("height")

                if not width or not height:
                    violations.append(
                        f"{path.relative_to(ROOT)} -> {src}"
                    )
                    continue

                if not width.isdigit() or not height.isdigit():
                    violations.append(
                        f"{path.relative_to(ROOT)} -> "
                        f"{src}: nonnumeric dimensions"
                    )
                    continue

                if int(width) <= 0 or int(height) <= 0:
                    violations.append(
                        f"{path.relative_to(ROOT)} -> "
                        f"{src}: nonpositive dimensions"
                    )

        self.assertEqual(
            [],
            violations,
            "Images without valid width/height:\n"
            + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
