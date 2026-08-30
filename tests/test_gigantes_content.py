from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GIGANTES = ROOT / "docs" / "pages" / "gigantes.html"


def test_gigantes_page_contains_only_gigantes_families():
    html = GIGANTES.read_text(encoding="utf-8")

    for expected in (
        "アグリオス種",
        "ガラティオン種",
        "エウリュード種",
        "アルキュオネ種",
        "ギュゲンテ種",
        "レイヴガイスト種",
    ):
        assert expected in html

    for foreign_enemy_family in (
        "トアス種",
        "ゴルドス種",
        "アフォル種",
        "ディートアス",
        "ウィルアフォル",
    ):
        assert foreign_enemy_family not in html


def test_gigantes_page_has_one_data_table():
    html = GIGANTES.read_text(encoding="utf-8")

    assert html.count("<table") == 1
    assert "難易度SH以降での出現クエスト" in html
