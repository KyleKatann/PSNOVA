from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

MENUBAR = DOCS / "js" / "menubar.js"
PAGE_META = DOCS / "js" / "page-meta.js"
SITEMAP = DOCS / "sitemap.xml"
AGENT = ROOT / "Agent.md"


EXPECTED = {'/PSNOVA/': {'description': 'PSNOVA(ファンタシースター ノヴァ)の武器、防具、素材、エネミー、特殊能力などを整理した攻略データサイトです。',
              'title': 'PSNOVA攻略サイト'},
 '/PSNOVA/index.html': {'description': 'PSNOVA(ファンタシースター ノヴァ)の武器、防具、素材、エネミー、特殊能力などを整理した攻略データサイトです。',
                        'title': 'PSNOVA攻略サイト'},
 '/PSNOVA/pages/appearance.html': {'description': 'PSNOVAのヘアスタイル、コスチューム、アクセサリーなど外見変更要素を一覧で確認できます。',
                                   'title': 'PSNOVA攻略サイト - 外見'},
 '/PSNOVA/pages/armor.html': {'description': 'PSNOVAの防具データを一覧掲載。性能や必要情報を比較して確認できます。',
                              'title': 'PSNOVA攻略サイト - 防具'},
 '/PSNOVA/pages/attachment.html': {'description': 'PSNOVAのアタッチパーツを一覧掲載。各パーツの情報をまとめて確認できます。',
                                   'title': 'PSNOVA攻略サイト - アタッチパーツ'},
 '/PSNOVA/pages/class.html': {'description': 'PSNOVAのクラス情報と特徴を一覧で確認できます。', 'title': 'PSNOVA攻略サイト - クラス'},
 '/PSNOVA/pages/difficulty.html': {'description': 'PSNOVAの難易度やクエストに関する攻略情報をまとめています。',
                                   'title': 'PSNOVA攻略サイト - 難易度'},
 '/PSNOVA/pages/enemy.html': {'description': 'PSNOVAに登場するエネミーのデータやドロップ情報を一覧で確認できます。',
                              'title': 'PSNOVA攻略サイト - エネミー'},
 '/PSNOVA/pages/faq.html': {'description': 'PSNOVAの序盤体験版、基本システム、高難易度攻略、PSO2との違いを初心者向けQ&A形式でまとめています。',
                            'title': 'PSNOVA攻略サイト - 初心者Q&A'},
 '/PSNOVA/pages/gigantes.html': {'description': 'PSNOVAのギガンテスに関する攻略情報とデータをまとめています。',
                                 'title': 'PSNOVA攻略サイト - ギガンテス'},
 '/PSNOVA/pages/item.html': {'description': 'PSNOVAの消費アイテムと効果を一覧で確認できます。', 'title': 'PSNOVA攻略サイト - 消費アイテム'},
 '/PSNOVA/pages/material.html': {'description': 'PSNOVAの素材データを一覧掲載。必要な素材や入手情報を探す際に利用できます。',
                                 'title': 'PSNOVA攻略サイト - 素材'},
 '/PSNOVA/pages/skill.html': {'description': 'PSNOVAのスキル一覧と効果をまとめて確認できます。', 'title': 'PSNOVA攻略サイト - スキル'},
 '/PSNOVA/pages/specialability.html': {'description': 'PSNOVAの特殊能力を一覧掲載。能力名と効果を比較して確認できます。',
                                       'title': 'PSNOVA攻略サイト - 特殊能力'},
 '/PSNOVA/pages/species.html': {'description': 'PSNOVAの種族情報と特徴をまとめています。', 'title': 'PSNOVA攻略サイト - 種族'},
 '/PSNOVA/pages/trophy.html': {'description': 'PSNOVAのトロフィー一覧と獲得条件を確認できます。', 'title': 'PSNOVA攻略サイト - トロフィー'},
 '/PSNOVA/pages/weapon.html': {'description': 'PSNOVAの11種類の武器種から、個別の性能・必要素材ページを選べます。',
                               'title': 'PSNOVA攻略サイト - 武器'},
 '/PSNOVA/pages/weapon/doublesaber.html': {'description': 'PSNOVAのダブルセイバー一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                           'title': 'PSNOVA攻略サイト - ダブルセイバー'},
 '/PSNOVA/pages/weapon/halo.html': {'description': 'PSNOVAのヘイロウ一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                    'title': 'PSNOVA攻略サイト - ヘイロウ'},
 '/PSNOVA/pages/weapon/knuckle.html': {'description': 'PSNOVAのナックル一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                       'title': 'PSNOVA攻略サイト - ナックル'},
 '/PSNOVA/pages/weapon/partizan.html': {'description': 'PSNOVAのパルチザン一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                        'title': 'PSNOVA攻略サイト - パルチザン'},
 '/PSNOVA/pages/weapon/pile.html': {'description': 'PSNOVAのパイル一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                    'title': 'PSNOVA攻略サイト - パイル'},
 '/PSNOVA/pages/weapon/rifle.html': {'description': 'PSNOVAのアサルトライフル一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                     'title': 'PSNOVA攻略サイト - アサルトライフル'},
 '/PSNOVA/pages/weapon/rod.html': {'description': 'PSNOVAのロッド一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                   'title': 'PSNOVA攻略サイト - ロッド'},
 '/PSNOVA/pages/weapon/sword.html': {'description': 'PSNOVAのソード一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                     'title': 'PSNOVA攻略サイト - ソード'},
 '/PSNOVA/pages/weapon/talis.html': {'description': 'PSNOVAのタリス一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                     'title': 'PSNOVA攻略サイト - タリス'},
 '/PSNOVA/pages/weapon/tmachinegun.html': {'description': 'PSNOVAのツインマシンガン一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                           'title': 'PSNOVA攻略サイト - ツインマシンガン'},
 '/PSNOVA/pages/weapon/wand.html': {'description': 'PSNOVAのウォンド一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。',
                                    'title': 'PSNOVA攻略サイト - ウォンド'}}


class HeadMetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self.in_title = False
        self.title_parts = []
        self.named_meta = {}
        self.property_meta = {}
        self.canonicals = []

    @property
    def title(self):
        return "".join(
            self.title_parts
        ).strip()

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)

        if tag == "title":
            self.in_title = True

        elif tag == "meta":
            name = attrs.get("name")
            prop = attrs.get("property")

            if name:
                self.named_meta.setdefault(
                    name,
                    [],
                ).append(
                    attrs.get("content", "")
                )

            if prop:
                self.property_meta.setdefault(
                    prop,
                    [],
                ).append(
                    attrs.get("content", "")
                )

        elif (
            tag == "link"
            and "canonical"
            in (
                attrs.get("rel")
                or ""
            ).split()
        ):
            self.canonicals.append(
                attrs.get("href", "")
            )

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)


def sitemap_routes():
    root = ElementTree.parse(
        SITEMAP
    ).getroot()

    ns = {
        "sm": (
            "http://www.sitemaps.org/"
            "schemas/sitemap/0.9"
        )
    }

    result = set()

    for loc in root.findall(
        "sm:url/sm:loc",
        ns,
    ):
        route = unquote(
            urlparse(
                (loc.text or "").strip()
            ).path
        )

        if route.startswith("/PSNOVA/"):
            result.add(route)

    return result


def route_to_file(route):
    if route in {
        "/PSNOVA/",
        "/PSNOVA/index.html",
    }:
        return DOCS / "index.html"

    return DOCS / route.removeprefix(
        "/PSNOVA/"
    )


def canonical_route(route):
    if route in {
        "/PSNOVA/",
        "/PSNOVA/index.html",
    }:
        return "/PSNOVA/"

    return route


def parse(route):
    parser = HeadMetadataParser()

    parser.feed(
        route_to_file(route).read_text(
            encoding="utf-8"
        )
    )

    return parser


def test_sitemap_and_static_metadata_cover_same_routes():
    assert sitemap_routes() == set(EXPECTED)
    assert len(EXPECTED) == 28


def test_public_metadata_is_static_and_exact():
    for route, current in EXPECTED.items():
        parser = parse(route)

        url = (
            "https://kylekatann.github.io"
            + canonical_route(route)
        )

        page_type = (
            "website"
            if route in {
                "/PSNOVA/",
                "/PSNOVA/index.html",
            }
            else "article"
        )

        assert parser.title == current["title"], route

        assert parser.named_meta.get(
            "description"
        ) == [
            current["description"]
        ], route

        assert (
            "keywords"
            not in parser.named_meta
        ), route

        assert parser.canonicals == [
            url
        ], route

        assert parser.property_meta.get(
            "og:title"
        ) == [
            current["title"]
        ], route

        assert parser.property_meta.get(
            "og:description"
        ) == [
            current["description"]
        ], route

        assert parser.property_meta.get(
            "og:type"
        ) == [
            page_type
        ], route

        assert parser.property_meta.get(
            "og:url"
        ) == [
            url
        ], route

        assert parser.property_meta.get(
            "og:site_name"
        ) == [
            "PSNOVA攻略サイト"
        ], route


def test_public_titles_follow_site_first_convention():
    for route, current in EXPECTED.items():
        title = current["title"]

        if route in {
            "/PSNOVA/",
            "/PSNOVA/index.html",
        }:
            assert title == "PSNOVA攻略サイト"

        else:
            assert title.startswith(
                "PSNOVA攻略サイト - "
            )

            assert title.removeprefix(
                "PSNOVA攻略サイト - "
            ).strip()


def test_runtime_metadata_repair_is_removed():
    assert not PAGE_META.exists()

    menubar = MENUBAR.read_text(
        encoding="utf-8"
    )

    assert "page-meta.js" not in menubar

    assert (
        "data-psnova-page-meta"
        not in menubar
    )


def test_agent_records_static_metadata_ownership():
    guide = AGENT.read_text(
        encoding="utf-8"
    )

    assert (
        "Public page titles follow one naming convention"
        in guide
    )

    assert (
        "PSNOVA攻略サイト - XXXXX"
        in guide
    )

    assert (
        "Public title, description, canonical, and "
        "OpenGraph metadata are owned by static source HTML."
        in guide
    )
