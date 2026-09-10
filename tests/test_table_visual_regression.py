import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
PAGE_STYLE = ROOT / "docs" / "css" / "page.css"


def css_rules(css):
    rules = {}
    for selectors, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        for selector in selectors.split(","):
            rules[selector.strip()] = declarations
    return rules


class TableVisualRegressionTests(unittest.TestCase):
    def test_compact_table_style_does_not_depend_on_runtime_semantic_marker(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertNotIn("data-psnova-semantic", css)
        self.assertIn("#main table {", css)
        self.assertIn("border-spacing: 0;", css)
        self.assertIn("background: var(--surface);", css)
        self.assertIn("background: var(--accent-soft);", css)
        self.assertIn("border: 1px solid var(--border);", css)
        self.assertNotIn("#eef5ff", css.lower())
        self.assertNotIn("#e0e8f0", css.lower())

    def test_public_table_surfaces_remain_square_and_flat(self):
        css_sources = (
            STYLE.read_text(encoding="utf-8"),
            PAGE_STYLE.read_text(encoding="utf-8"),
        )
        cell_level = re.compile(r"\b(?:td|th|tr|thead|tbody|tfoot)\b")

        for css in css_sources:
            css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
            for selectors, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
                for selector in selectors.split(","):
                    selector = selector.strip()
                    is_table_surface = "table" in selector and not cell_level.search(selector)
                    is_special_scroll_surface = selector in {
                        "#main.technic-detail-page .technic-level-scroll",
                    }
                    if not (is_table_surface or is_special_scroll_surface):
                        continue

                    for radius in re.findall(r"border-radius:\s*([^;]+)", declarations):
                        self.assertEqual(
                            "0",
                            radius.strip(),
                            f"rounded table surface: {selector}",
                        )
                    for shadow in re.findall(r"box-shadow:\s*([^;]+)", declarations):
                        self.assertEqual(
                            "none",
                            shadow.strip(),
                            f"card-like table shadow: {selector}",
                        )

    def test_weapon_table_visual_encoding_is_kept_in_shared_table_css(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn('.rarity-cell[data-rarity="1"]', css)
        self.assertIn('.rarity-cell[data-rarity="15"]', css)
        self.assertIn(".rarity-source-star::before", css)
        self.assertIn('.weapon-stat-melee.has-value', css)
        self.assertIn('background: #fff0f0;', css)
        self.assertIn('.weapon-stat-ranged.has-value', css)
        self.assertIn('background: var(--accent-soft);', css)
        self.assertIn('.weapon-stat-tech.has-value', css)
        self.assertIn('background: #fffbe6;', css)
        self.assertIn('.weapon-stat-cell.is-empty', css)
        self.assertIn('background: #e7e9ee;', css)

    def test_rarity_presentation_contract_is_owned_by_shared_css(self):
        css = STYLE.read_text(encoding="utf-8")
        page_css = PAGE_STYLE.read_text(encoding="utf-8")
        rules = css_rules(css)

        self.assertNotIn(".rarity-cell", page_css)
        self.assertNotIn("--rarity-", page_css)
        self.assertEqual(1, css.count("#main table .rarity-cell {"))

        base = rules["#main table .rarity-cell"]
        self.assertIn("background: var(--accent-soft);", base)
        self.assertIn("font-weight: 800;", base)
        self.assertIn("text-align: center;", base)
        self.assertIn("white-space: nowrap;", base)
        self.assertIn("font-variant-numeric: tabular-nums;", base)

        before = rules["#main table .rarity-cell::before"]
        self.assertIn('content: "★";', before)
        self.assertIn("margin-right: 3px;", before)

        source_star = rules[
            "#main table .rarity-cell.rarity-source-star::before"
        ]
        self.assertIn("content: none;", source_star)

        expected_colors = {
            1: "--rarity-blue",
            2: "--rarity-blue",
            3: "--rarity-blue",
            4: "--rarity-green",
            5: "--rarity-green",
            6: "--rarity-green",
            7: "--rarity-red",
            8: "--rarity-red",
            9: "--rarity-red",
            10: "--rarity-orange",
            11: "--rarity-orange",
            12: "--rarity-orange",
            13: "--rarity-purple",
            14: "--rarity-purple",
            15: "--rarity-purple",
        }
        for rarity, token in expected_colors.items():
            selector = f'#main table .rarity-cell[data-rarity="{rarity}"]'
            pseudo = f'{selector}::before'
            declaration = f"color: var({token});"
            self.assertIn(declaration, rules[selector])
            self.assertIn(declaration, rules[pseudo])


if __name__ == "__main__":
    unittest.main()
