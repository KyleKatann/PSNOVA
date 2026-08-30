import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
TABLE_SEMANTICS_JS = ROOT / "docs" / "js" / "table-semantics.js"


class TableSemanticTests(unittest.TestCase):
    def test_semantic_normalizer_is_loaded_globally(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/js/table-semantics.js", js)
        self.assertIn("data-psnova-table-semantics", js)

    def test_large_data_tables_are_detected_without_touching_small_tables(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('function isLargeDataTable(table)', js)
        self.assertIn('table.closest("details")', js)
        self.assertIn('rows.length < 4', js)
        self.assertIn('main.querySelectorAll("table")', js)
        self.assertIn('tables.filter(isLargeDataTable).forEach(normalizeDataTable)', js)

    def test_legacy_colored_td_headers_are_detected(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('function hasLegacyHeaderStyling(cell)', js)
        self.assertIn('cell.hasAttribute("bgcolor")', js)
        self.assertIn('cell.style.backgroundColor', js)
        self.assertIn('legacyHeaderCount', js)
        self.assertIn('Math.ceil(headerCells.length / 2)', js)

    def test_every_main_table_gets_an_idempotent_scroll_wrapper(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('function ensureScrollableTable(table)', js)
        self.assertIn('classList.contains("table-scroll")', js)
        self.assertIn('wrapper.className = "table-scroll"', js)
        self.assertIn('wrapper.appendChild(table)', js)
        self.assertIn('tables.forEach(ensureScrollableTable)', js)

    def test_scroll_wrapper_is_keyboard_accessible(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('wrapper.setAttribute("role", "region")', js)
        self.assertIn('wrapper.setAttribute("tabindex", "0")', js)
        self.assertIn('wrapper.setAttribute("aria-label", "表を横スクロール")', js)

    def test_header_and_body_semantics_are_created(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('replaceElementTag(cell, "th")', js)
        self.assertIn('headerCell.setAttribute("scope", "col")', js)
        self.assertIn("table.createTHead()", js)
        self.assertIn('replaceElementTag(cell, "td")', js)

    def test_archived_column_meanings_are_detected(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('label === "レアリティ"', js)
        self.assertIn('label === "打撃" || label === "打撃力"', js)
        self.assertIn('label === "射撃" || label === "射撃力"', js)
        self.assertIn('label === "法撃" || label === "法撃力"', js)
        self.assertIn('label === "ショップlv" || label === "shoplv"', js)
        self.assertIn('data-rarity-band', js)
        self.assertIn('weapon-stat-melee', js)
        self.assertIn('weapon-stat-ranged', js)
        self.assertIn('weapon-stat-tech', js)

    def test_normalization_is_idempotent(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('table.dataset.psnovaSemantic === "true"', js)
        self.assertIn('table.dataset.psnovaSemantic = "true"', js)


if __name__ == "__main__":
    unittest.main()
