import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class ImageAltParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.images = []
        self.anchor_stack = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attributes = dict(attrs)

        if tag == "a":
            self.anchor_stack.append({
                "href": attributes.get("href", ""),
                "text": [],
                "images": [],
            })
            return

        if tag == "img":
            image = {
                "src": attributes.get("src", ""),
                "has_alt": "alt" in attributes,
                "alt": attributes.get("alt"),
            }
            self.images.append(image)

            if self.anchor_stack:
                self.anchor_stack[-1]["images"].append(image)

    def handle_data(self, data):
        if self.anchor_stack and data.strip():
            self.anchor_stack[-1]["text"].append(data.strip())

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self.anchor_stack:
            anchor = self.anchor_stack.pop()
            anchor["text_value"] = " ".join(anchor["text"]).strip()
            self.images.append({
                "_anchor": anchor,
            })


def public_html_files():
    yield from DOCS.rglob("*.html")


class PublicImageAltTests(unittest.TestCase):
    def test_all_public_images_have_alt_attributes(self):
        violations = []

        for path in public_html_files():
            parser = ImageAltParser()
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()

            for image in parser.images:
                if "_anchor" in image:
                    continue

                if not image["has_alt"]:
                    violations.append(
                        f"{path.relative_to(ROOT)} -> "
                        f"{image['src']} (alt属性がない)"
                    )
                    continue

                alt = image["alt"]
                if alt is not None and alt != "" and not alt.strip():
                    violations.append(
                        f"{path.relative_to(ROOT)} -> "
                        f"{image['src']} (altが空白のみ)"
                    )

        self.assertEqual(
            [],
            violations,
            "不正な画像alt属性:\n" + "\n".join(violations),
        )

    def test_image_only_links_have_nonempty_image_alt(self):
        violations = []

        for path in public_html_files():
            parser = ImageAltParser()
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()

            for entry in parser.images:
                anchor = entry.get("_anchor")
                if not anchor:
                    continue

                if anchor["text_value"]:
                    continue

                if not anchor["images"]:
                    continue

                if not any(
                    image["has_alt"]
                    and image["alt"] is not None
                    and image["alt"].strip()
                    for image in anchor["images"]
                ):
                    violations.append(
                        f"{path.relative_to(ROOT)} -> "
                        f"{anchor['href']} "
                        f"(画像のみのリンクに利用可能なaltがない)"
                    )

        self.assertEqual(
            [],
            violations,
            "利用可能な代替テキストがない画像のみのリンク:\n"
            + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
