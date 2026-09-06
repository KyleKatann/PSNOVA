import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "npc-password.html"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


EXPECTED_ROWS = {
    "リーンベル": (
        "ヒューマン", "♀", "レンジャー", "一生懸命", "一般アークス", "射撃王", "平和主義",
        "泣き虫", "人気者", "おしゃれ怪盗", "立ち止まって待ってても",
        "何も変わらないって教えてもらったから・・・・・・！", "「End of Eternity」コラボ企画より",
        "パスワード:EoEReanbell", "エステ選択項目UP＋３",
    ),
    "セガエイギョーマン": (
        "キャスト", "♂", "フォース", "仕事大好き", "見習いアークス", "戦闘タイプ：攻撃+支援",
        "光属性", "節約レシピ好き", "商人見習い", "仮縫い担当", "『セガエイギョーマン』っす！",
        "よろしくっす！", "店頭体験会参加者特典", "パスワード:NOVATAIKENKAI",
        "※ 1.01アップデート適用で追加", "料理★1の素材減", "道具★2の素材減", "衣装★5の素材減",
    ),
    "3Z-103": (
        "キャスト", "♂", "バスター", "永久機関", "エリートアークス", "戦闘タイプ：攻撃", "氷属性",
        "ポーカーフェイス", "口下手", "打たれ強い", "オマエガヒツヨウトスルナラバ。",
        "オマエノタタカイノ、チカラニナロウ。", "ニコニコ生放送", "キックオフ特番企画より",
        "パスワード:mitsutomitakao", "※ 1.01アップデート適用で追加",
    ),
    "デスマスク": (
        "キャスト", "♂", "ハンター", "戦闘狂", "エリートアークス", "戦闘タイプ：攻撃", "闇属性",
        "スロースターター", "目立ちたがり", "女好き", "フフ・・・・・・「黒閣下」とも呼ばれる吾輩の力",
        "存分に見せてやろう！", "・・・・・・言っておくが、敵ではないぞ", "パスワード:SummonDaemon",
        "※ 1.01アップデート適用で追加",
    ),
    "でんげきエレナ": (
        "ニューマン", "♀", "ハンター", "看板娘", "一般アークス", "戦闘タイプ：支援", "雷属性",
        "反射神経抜群", "節約レシピ好き", "節約レシピマニア", "妹の私は冒険をサポートしたいと思います！",
        "電撃オンラインもよろしくお願いします☆", "パスワード:DENGEKIERENA",
        "※ 1.01アップデート適用で追加", "料理★1の素材減", "料理★2の素材減",
    ),
    "でんげきのおねえさん": (
        "ニューマン", "♀", "フォース", "となりのお姉さん", "エリートアークス", "戦闘タイプ：攻撃+回復",
        "雷属性", "キャスト好き", "話し上手", "落ち込みやすい", "回復は姉のあたしに任せて。",
        "攻略に困ったら電プレを読んでね！", "電撃PlayStation Vol.582に掲載", "パスワード:DENGEKIPS",
        "※ 1.01アップデート適用で追加",
    ),
    "デンゲキばず～こ": (
        "キャスト", "♀", "レンジャー", "サブカル好き", "エリートアークス", "戦闘タイプ：支援", "雷属性",
        "ピンチに強い", "兵器マニア", "ケガが多い", "デンゲキ的末っ子", "ばず〜こデス",
        "アナタのタメニ撃ちまくるヨーぅ！", "デンゲキBAZOOKA！！", "ヨロシクデス！",
        "デンゲキバズーカ2015年2月号に掲載", "パスワード:YOROSHIKUBAZOOKA",
        "※ 1.01アップデート適用で追加",
    ),
    "リョーマ": (
        "ヒューマン", "♂", "ハンター", "ジャッジメント", "エリートアークス", "戦闘タイプ：支援", "炎属性",
        "ド根性", "熱血漢", "おしゃれ怪盗", "このセカイをオレがかえてやる！",
        "オレがオマエにホントの「ミライ」をみせてやるよ。", "だから、ついてこい！",
        "パスワード:takanokouhei", "※1.02アップデート適用で追加", "エステ選択項目UP＋３",
    ),
    "ステラ": (
        "ニューマン", "♀", "フォース", "純情可憐", "熟練アークス", "戦闘タイプ：支援+回復", "風属性",
        "男好き", "女好き", "商売の神様", "ダイスキなあなたのためなら、", "なんでもやるよー!",
        "パスワード:hasegawayui", "※1.02アップデート適用で追加", "道具★5の素材減",
    ),
    "ネキコ": (
        "ニューマン", "♀", "フォース", "冷静沈着", "エリートアークス", "戦闘タイプ：支援+回復", "闇属性",
        "ハンター好き", "反射神経抜群", "法撃マスター", "回復のサポートは私に任せて！",
        "毎週木曜日発売の", "週刊ファミ通もよろしくネ!!", "週刊ファミ通 No.1361に掲載",
        "パスワード:famitsu01", "※1.02アップデート適用で追加",
    ),
    "ネキミ": (
        "ニューマン", "♀", "レンジャー", "才色兼備", "一般アークス", "戦闘タイプ：攻撃", "氷属性", "泣き虫",
        "節約レシピマイスター", "仮縫い担当", "食堂に配置してくれたら、", "美味しいご飯作っちゃうヨ！",
        "あっ、毎週木曜日発売の週刊ファミ通もよろしく★", "週刊ファミ通コラボ", "パスワード:famitsu02",
        "※1.02アップデート適用で追加", "料理★3の素材減", "衣装★5の素材減",
    ),
    "リーア": (
        "ヒューマン", "♀", "レンジャー", "運動神経抜群", "エリートアークス", "戦闘タイプ：支援",
        "ピンチに強い", "冷静", "反射神経抜群", "射撃王", "後ろのことはお姉さんに任せなさいって。",
        "さあ、頑張っていこーっ！", "ファンタシースターノヴァ", "サイドストーリーズ(一迅社発行)に掲載",
        "パスワード:IchijinXNOVAsss1", "※1.02アップデート適用で追加",
    ),
    "サリュー": (
        "ニューマン", "♀", "フォース", "勇猛果敢", "一般アークス", "戦闘タイプ：支援+回復",
        "スロースターター", "不屈の精神", "法撃マスター", "ほらほら、もっと気合を入れなさいよね！",
        "回復くらいなら私がしてあげるから。", "ファンタシースターノヴァ",
        "サイドストーリーズ(一迅社発行)に掲載", "パスワード:IchijinXNOVAsss2",
        "※1.02アップデート適用で追加",
    ),
}


def row_text(page, name):
    match = re.search(rf"<tr>\s*<td>{re.escape(name)}</td>(.*?)</tr>", page, re.S)
    assert match, f"missing NPC password row: {name}"
    text = re.sub(r"<br\s*/?>", " ", match.group(0))
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def test_npc_password_page_preserves_input_data():
    page = PAGE.read_text(encoding="utf-8")

    assert page.count("<tbody>") == 1
    assert page.count("<tr>") == 14  # header + 13 password NPC rows
    for name, expected_tokens in EXPECTED_ROWS.items():
        text = row_text(page, name)
        for token in expected_tokens:
            assert token in text, f"{name}: missing {token}"


def test_npc_password_page_preserves_unlock_mechanics_and_warning():
    page = PAGE.read_text(encoding="utf-8")

    required = (
        "グランドアクト1まで進めると利用可能",
        "リーンベル以外はアップデートにより追加される。",
        "解凍にグランエナジーは不要。",
        "これらの追加クルーを追加すると、同行クルーの並び順がおかしくなる不具合があります。",
    )
    for text in required:
        assert text in page

    assert 'class="npc-password-warning"' in page
    assert "background:#fff1f1" in page
    assert "border-left:4px solid #c83f3f" in page


def test_npc_password_page_uses_modern_public_shell():
    page = PAGE.read_text(encoding="utf-8")

    assert "<title>PSNOVA攻略サイト - NPC(パスワード解放)</title>" in page
    assert '<link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/npc-password.html">' in page
    assert '<link rel="stylesheet" href="/PSNOVA/css/page.css">' in page
    assert '<main id="main">' in page
    assert '<table class="npc-table">' in page
    assert "<details>" not in page
    assert "<summary>" not in page
    assert "web.archive.org" not in page
    assert "paraedit" not in page
    assert "タイトルなし" not in page


def test_npc_password_page_is_in_sidebar_and_sitemap():
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")

    assert '<a href="/PSNOVA/pages/npc-password.html">NPC(パスワード解放)</a>' in sidebar
    assert "https://kylekatann.github.io/PSNOVA/pages/npc-password.html" in sitemap
