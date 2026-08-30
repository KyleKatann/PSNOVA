from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GIGANTES = ROOT / "docs" / "pages" / "gigantes.html"


def test_gigantes_page_retains_all_known_gigantes_families():
    html = GIGANTES.read_text(encoding="utf-8")

    for expected in (
        "アグリオス種",
        "ガラティオン種",
        "エウリュード種",
        "アルキュオネ種",
        "ギュゲンテ種",
        "レイヴガイスト種",
        "トアス種",
        "ゴルドス種",
        "アフォル種",
    ):
        assert expected in html

    for sentinel in (
        "ディートアス",
        "ヴァリゴルドス",
        "ウィルアフォル",
    ):
        assert sentinel in html


def test_gigantes_page_keeps_both_data_tables():
    html = GIGANTES.read_text(encoding="utf-8")

    assert html.count("<table") == 2
    assert html.count("難易度SH以降での出現クエスト") == 2
