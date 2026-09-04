import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"

VARIABLE_RE = re.compile(
    r"^\s*(--[\w-]+):\s*(#[0-9a-fA-F]{6});",
    re.MULTILINE,
)


def rgb(value):
    value = value.lstrip("#")
    return tuple(
        int(value[index:index + 2], 16)
        for index in (0, 2, 4)
    )


def relative_luminance(value):
    channels = []

    for channel in rgb(value):
        component = channel / 255

        if component <= 0.04045:
            component /= 12.92
        else:
            component = (
                (component + 0.055) / 1.055
            ) ** 2.4

        channels.append(component)

    red, green, blue = channels

    return (
        0.2126 * red
        + 0.7152 * green
        + 0.0722 * blue
    )


def contrast_ratio(first, second):
    first_luminance = relative_luminance(first)
    second_luminance = relative_luminance(second)

    lighter = max(first_luminance, second_luminance)
    darker = min(first_luminance, second_luminance)

    return (
        lighter + 0.05
    ) / (
        darker + 0.05
    )


class AccessibleColorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = STYLE.read_text(encoding="utf-8")
        cls.variables = dict(
            VARIABLE_RE.findall(cls.css)
        )

    def assert_aa(self, foreground, background):
        ratio = contrast_ratio(
            self.variables[foreground],
            self.variables[background],
        )

        self.assertGreaterEqual(
            ratio,
            4.5,
            (
                f"{foreground} on {background} "
                f"has contrast {ratio:.2f}:1"
            ),
        )

    def test_muted_text_passes_shared_light_backgrounds(self):
        for background in (
            "--surface-subtle",
            "--surface-muted",
            "--page-bg",
            "--surface",
        ):
            with self.subTest(background=background):
                self.assert_aa(
                    "--text-muted",
                    background,
                )

    def test_rarity_palette_passes_accent_soft_background(self):
        for token in (
            "--rarity-blue",
            "--rarity-green",
            "--rarity-red",
            "--rarity-orange",
            "--rarity-purple",
        ):
            with self.subTest(token=token):
                self.assert_aa(
                    token,
                    "--accent-soft",
                )

    def test_rarity_groups_keep_the_canonical_hue_mapping(self):
        groups = {
            "1": "--rarity-blue",
            "4": "--rarity-green",
            "7": "--rarity-red",
            "10": "--rarity-orange",
            "13": "--rarity-purple",
        }

        for rarity, token in groups.items():
            with self.subTest(rarity=rarity):
                pattern = re.compile(
                    rf'#main table \.rarity-cell'
                    rf'\[data-rarity="{rarity}"\]'
                    rf'[^{{]*\{{(?P<body>[^}}]*)\}}',
                    re.DOTALL,
                )

                match = pattern.search(self.css)

                self.assertIsNotNone(
                    match,
                    f"rarity group starting at {rarity} missing",
                )

                self.assertIn(
                    f"color: var({token});",
                    match.group("body"),
                )

    def test_old_low_contrast_rarity_names_are_gone(self):
        for color in (
            "deepskyblue",
            "limegreen",
            "orangered",
            "color: orange;",
            "color: violet;",
        ):
            with self.subTest(color=color):
                self.assertNotIn(
                    color,
                    self.css.lower(),
                )


if __name__ == "__main__":
    unittest.main()
