import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NPC_PAGE = ROOT / "docs" / "pages" / "npc.html"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


EXPECTED_ROWS = {
    "ルティナ": (
        "ヒューマン", "♀", "フォース", "格闘系ガール", "一般アークス", "仲間思い",
        "火事場の馬鹿力", "ハンター好き", "話し上手", "初期", "法撃力+30",
        "HP低下で攻撃力アップ", "ハンターがいると有利", "補助テクニック効果範囲+20%",
    ),
    "セイル": (
        "ヒューマン", "♂", "ハンター", "モノメイト男", "一般アークス", "不倒", "ド根性",
        "目立ちたがり", "熱血漢", "ストーリー進行", "打撃力", "HP低下で防御力アップ",
        "確率でリアクション無効", "ヘイト上昇率アップ",
    ),
    "フィルディア": (
        "ヒューマン", "♀", "ハンター", "暁紅の英雄", "暁紅のアークス", "打撃自慢",
        "リーダー気質", "ピンチに強い", "人気者", "ハンター好き", "熱血漢", "打たれ強い",
        "ストーリー進行", "一時加入", "クリア後コールドスリープ", "打撃力+80", "打撃防御+30",
        "防御力アップ+5%", "HP低下で攻撃力アップ", "ハンターがいると有利", "レベル+10",
    ),
    "イズナ": (
        "ニューマン", "♀", "レンジャー", "知られざる天才", "一般アークス", "天才肌",
        "ピンチに強い", "影が薄い", "冷静", "ストーリー進行", "射撃力+30",
        "状態異常耐性アップ", "HP低下で攻撃力アップ", "ヘイト上昇率ダウン",
    ),
    "マグナス": ("ヒューマン", "♂"),
    "レイヴァン": (
        "ニューマン", "♂", "フォース", "あくなき研究者", "エリートアークス", "探究心",
        "法撃マスター", "ポーカーフェイス", "影が薄い", "兵器マニア", "不屈の精神",
        "クリア後コールドスリープ", "法撃力+50", "法撃防御+30", "打撃耐性", "ギガンテスに有利",
        "HP低下で防御力アップ", "レアドロップ+5%", "ヘイト上昇率ダウン", "レベル+4",
    ),
    "シャロン": (
        "キャスト", "♀", "フォース", "天才発明家", "一般アークス", "ロマンチスト", "平和主義者",
        "動物博士", "不屈の精神", "ストーリー進行", "法撃耐性+30", "防御力アップ+5%",
        "打撃耐性", "原生種に有利", "アイテムドロップ+5%", "レベル-2",
    ),
    "オルクス": (
        "ヒューマン", "♂", "レンジャー", "歴戦の老兵", "熟練アークス", "戦闘巧者", "平和主義",
        "友情に熱い", "冷静", "ストーリー進行", "射撃力+30", "防御力アップ+5%",
        "追加：ブラインド", "レベル+2",
    ),
    "リーティア": (
        "ヒューマン", "♀", "フォース", "天然看護娘", "見習いアークス", "医学知識", "影の実力者",
        "頑張り屋", "オペレーター", "ストーリー進行", "クエスト", "プロミスオーダー",
        "攻撃力アップ+20%", "防御力アップ+20%", "弱点属性ダメージアップ", "レベル-10",
    ),
    "ヨミ": (
        "ニューマン", "♂", "ハンター", "生意気職人", "見習いアークス", "やんちゃ坊主", "短気",
        "努力家", "反射神経抜群", "ストーリー進行", "射撃防御+30", "攻撃力アップ+10%",
        "HP低下で攻撃力アップ", "攻撃速度+5%", "レベル-7",
    ),
    "キサラ": (
        "ヒューマン", "♀", "レンジャー", "インカムの女神", "熟練アークス", "S属性", "射撃王",
        "ピンチに強い", "動物博士", "未記入", "射撃力+50", "打撃耐性",
        "クリティカル率アップ", "原生種に有利", "HP低下で攻撃力アップ",
        "弱点部ダメージアップ", "レベル+2",
    ),
    "ヒュペリオン": (
        "キャスト", "♂", "レンジャー", "経歴不明のシェフ", "熟練アークス", "職人の手捌き",
        "影の実力者", "ピンチに強い", "目立ちたがり", "ストーリー進行", "技量+50",
        "攻撃力アップ+20%", "防御力アップ+10%", "HP低下で攻撃力アップ",
        "ヘイト上昇率アップ", "レベル-1",
    ),
    "カリスト": (
        "ニューマン", "♂", "フォース", "仕事が恋人", "一般アークス", "堅物", "ポーカーフェイス",
        "ロンリーウルフ", "ダーカー嫌い", "ストーリー進行", "打撃耐性", "ダーカーに有利",
        "氷属性テクニックアップ", "HP低下で防御力アップ", "レベル-1",
    ),
    "ユノ": ("ギガンテス", "♀", "運命託されし姫"),
    "ガーネット": (
        "ニューマン", "♀", "フォース", "暴走超特急", "見習いアークス", "箱入り娘", "人気者",
        "ダーカー嫌い", "未記入", "打撃耐性", "ダーカーに有利", "アイテムドロップ+5%",
        "経験値+10%", "レベル+1",
    ),
    "サンシャウト": (
        "キャスト", "♂", "ハンター", "鉄面皮デカ", "エリートアークス", "デカチョウ", "打たれ強い",
        "不屈の精神", "ポーカーフェイス", "団体行動が苦手", "未記入", "打撃防御+30",
        "法撃防御+30", "HPアップ+100%", "HP低下で防御力アップ", "ヘイト上昇率アップ", "レベル+1",
    ),
}


def row_text(page, name):
    match = re.search(rf"<tr>\s*<td>{re.escape(name)}</td>(.*?)</tr>", page, re.S)
    assert match, f"missing NPC row: {name}"
    text = re.sub(r"<br\s*/?>", " ", match.group(0))
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def test_npc_story_table_preserves_archived_text_data():
    page = NPC_PAGE.read_text(encoding="utf-8")

    assert page.count("<tbody>") == 1
    assert page.count("<tr>") == 17  # header + 16 NPC rows
    for name, expected_tokens in EXPECTED_ROWS.items():
        text = row_text(page, name)
        for token in expected_tokens:
            assert token in text, f"{name}: missing {token}"


def test_npc_page_preserves_guest_and_friendship_mechanics():
    page = NPC_PAGE.read_text(encoding="utf-8")

    required = (
        "最大50人",
        "お気に入りとしてロック",
        "他人 → 知人 → 友人 → 仲間 → 親友",
        "繰り返し受注できるオーダー",
        "パーティーメンバーに入れてクエストをクリア",
        "レスタでHPを回復すると上昇しやすい可能性",
        "赤い吹き出しアイコン",
        "★付きの特殊なプロミスオーダーやクエスト",
        "エンディングで追加の会話",
    )
    for text in required:
        assert text in page


def test_npc_page_uses_modern_public_shell_and_spoiler_disclosures():
    page = NPC_PAGE.read_text(encoding="utf-8")

    assert "<title>PSNOVA攻略サイト - NPC</title>" in page
    assert '<link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/npc.html">' in page
    assert '<main id="main">' in page
    assert '<div class="table-scroll">' in page
    assert page.count("<details>") == 3
    assert "web.archive.org" not in page
    assert "paraedit" not in page
    assert "コメントの挿入" not in page


def test_npc_page_is_in_sidebar_and_sitemap():
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")

    assert '<a href="/PSNOVA/pages/npc.html">NPC</a>' in sidebar
    assert "https://kylekatann.github.io/PSNOVA/pages/npc.html" in sitemap
