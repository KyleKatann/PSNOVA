from pathlib import Path

PAGE = Path("docs/pages/npc-coldsleep.html")

def test_coldsleep_is_static_and_complete_enough():
    html = PAGE.read_text(encoding="utf-8")
    lowered = html.lower()
    for token in ("<iframe", "<object", "<embed", "web.archive.org", "cmd=table_edit2", "cmd=secedit"):
        assert token not in lowered
    for heading in (
        "ジェネラリストクルー", "ソルジャークルー", "サポートクルー",
        "レジェンドクルー", "セクションリーダークルー", "施設スキルキャラ一覧",
    ):
        assert heading in html
    for sentinel in ("アオイ", "アディーン", "ヴァルメン", "クシード", "リューフィ", "クラスカウンター"):
        assert sentinel in html
    assert html.count('<table class="npc-table">') >= 18
    assert html.count("<tbody>") == html.count('<table class="npc-table">')
