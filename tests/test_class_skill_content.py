from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs" / "pages"


def test_class_page_contains_the_four_psnova_classes_and_correct_weapon_links():
    html = (PAGES / "class.html").read_text(encoding="utf-8")

    for label in ("ハンター", "レンジャー", "フォース", "バスター"):
        assert label in html

    for slug in (
        "sword",
        "partizan",
        "doublesaber",
        "knuckle",
        "rifle",
        "tmachinegun",
        "rod",
        "talis",
        "wand",
        "pile",
        "halo",
    ):
        assert f'/PSNOVA/pages/weapon/{slug}.html' in html

    assert '/PSNOVA/pages/skill.html' in html


def test_class_page_does_not_contain_the_old_weapon_table_copy():
    html = (PAGES / "class.html").read_text(encoding="utf-8")

    assert "アルバギガッシュ" not in html
    assert "<summary>ソード</summary>" not in html
    assert "クラスのスキル" not in html
