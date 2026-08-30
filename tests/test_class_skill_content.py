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


def test_skill_page_contains_all_class_skill_sections_and_reference_sentinels():
    html = (PAGES / "skill.html").read_text(encoding="utf-8")

    for heading in ("ハンタースキル", "レンジャースキル", "フォーススキル", "バスタースキル"):
        assert heading in html

    for skill in (
        "ジャストガード",
        "ウィークヒットアドバンス",
        "チャージGPリバイバル",
        "光属性ダウン",
        "武器装備パイル",
        "デッドラインスレイヤー",
    ):
        assert skill in html


def test_skill_page_uses_static_semantic_tables():
    html = (PAGES / "skill.html").read_text(encoding="utf-8")

    assert html.count("<thead>") == 4
    assert html.count("<tbody>") == 4
    assert html.count('scope="col"') == 16

    for obsolete in ('bgcolor=', 'border="', 'cellspacing=', 'cellpadding=', 'border-collapse'):
        assert obsolete not in html


def test_skill_page_no_longer_contains_armor_copy():
    html = (PAGES / "skill.html").read_text(encoding="utf-8")

    assert "シールドユニット" not in html
    assert "ポストアタック" not in html
    assert "防具データ" not in html
