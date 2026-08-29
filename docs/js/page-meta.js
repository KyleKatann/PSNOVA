(function () {
    var metadata = {
        "/PSNOVA/": { title: "PSNOVA攻略 | ファンタシースター ノヴァ攻略データ" },
        "/PSNOVA/index.html": { title: "PSNOVA攻略 | ファンタシースター ノヴァ攻略データ" },
        "/PSNOVA/copyright.html": { title: "著作権・免責事項 | PSNOVA攻略" },
        "/PSNOVA/issue.html": { title: "修正・加筆要望 | PSNOVA攻略" },
        "/PSNOVA/pages/appearance.html": { title: "ヘアスタイル・コスチューム・アクセサリー一覧 | PSNOVA攻略" },
        "/PSNOVA/pages/armor.html": { title: "防具一覧・性能 | PSNOVA攻略" },
        "/PSNOVA/pages/attachment.html": { title: "アタッチパーツ一覧 | PSNOVA攻略" },
        "/PSNOVA/pages/class.html": { title: "クラス一覧・特徴 | PSNOVA攻略" },
        "/PSNOVA/pages/difficulty.html": { title: "難易度・クエスト情報 | PSNOVA攻略" },
        "/PSNOVA/pages/enemy.html": { title: "エネミー一覧・ドロップ | PSNOVA攻略" },
        "/PSNOVA/pages/gigantes.html": { title: "ギガンテス攻略・データ | PSNOVA攻略" },
        "/PSNOVA/pages/item.html": { title: "消費アイテム一覧 | PSNOVA攻略" },
        "/PSNOVA/pages/material.html": { title: "素材一覧・入手先 | PSNOVA攻略" },
        "/PSNOVA/pages/skill.html": { title: "スキル一覧・効果 | PSNOVA攻略" },
        "/PSNOVA/pages/specialability.html": { title: "特殊能力一覧・効果 | PSNOVA攻略" },
        "/PSNOVA/pages/species.html": { title: "種族一覧・特徴 | PSNOVA攻略" },
        "/PSNOVA/pages/trophy.html": { title: "トロフィー一覧・獲得条件 | PSNOVA攻略" },
        "/PSNOVA/pages/weapon.html": { title: "武器一覧・性能・必要素材 | PSNOVA攻略" }
    };

    var current = metadata[window.location.pathname];
    if (current && current.title) {
        document.title = current.title;
    }

    window.PSNOVAPageMetadata = metadata;
})();
