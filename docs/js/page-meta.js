(function () {
    var metadata = {
        "/PSNOVA/": {
            title: "PSNOVA攻略 | ファンタシースター ノヴァ攻略データ",
            description: "PSNOVA(ファンタシースター ノヴァ)の武器、防具、素材、エネミー、特殊能力などを整理した攻略データサイトです。"
        },
        "/PSNOVA/index.html": {
            title: "PSNOVA攻略 | ファンタシースター ノヴァ攻略データ",
            description: "PSNOVA(ファンタシースター ノヴァ)の武器、防具、素材、エネミー、特殊能力などを整理した攻略データサイトです。"
        },
        "/PSNOVA/copyright.html": {
            title: "著作権・免責事項 | PSNOVA攻略",
            description: "PSNOVA攻略サイトの著作権表示、免責事項、掲載情報の取り扱いについて案内します。"
        },
        "/PSNOVA/issue.html": {
            title: "修正・加筆要望 | PSNOVA攻略",
            description: "PSNOVA攻略サイトのデータ修正、加筆要望、不具合報告の方法を案内します。"
        },
        "/PSNOVA/pages/appearance.html": {
            title: "ヘアスタイル・コスチューム・アクセサリー一覧 | PSNOVA攻略",
            description: "PSNOVAのヘアスタイル、コスチューム、アクセサリーなど外見変更要素を一覧で確認できます。"
        },
        "/PSNOVA/pages/armor.html": {
            title: "防具一覧・性能 | PSNOVA攻略",
            description: "PSNOVAの防具データを一覧掲載。性能や必要情報を比較して確認できます。"
        },
        "/PSNOVA/pages/attachment.html": {
            title: "アタッチパーツ一覧 | PSNOVA攻略",
            description: "PSNOVAのアタッチパーツを一覧掲載。各パーツの情報をまとめて確認できます。"
        },
        "/PSNOVA/pages/class.html": {
            title: "クラス一覧・特徴 | PSNOVA攻略",
            description: "PSNOVAのクラス情報と特徴を一覧で確認できます。"
        },
        "/PSNOVA/pages/difficulty.html": {
            title: "難易度・クエスト情報 | PSNOVA攻略",
            description: "PSNOVAの難易度やクエストに関する攻略情報をまとめています。"
        },
        "/PSNOVA/pages/enemy.html": {
            title: "エネミー一覧・ドロップ | PSNOVA攻略",
            description: "PSNOVAに登場するエネミーのデータやドロップ情報を一覧で確認できます。"
        },
        "/PSNOVA/pages/gigantes.html": {
            title: "ギガンテス攻略・データ | PSNOVA攻略",
            description: "PSNOVAのギガンテスに関する攻略情報とデータをまとめています。"
        },
        "/PSNOVA/pages/item.html": {
            title: "消費アイテム一覧 | PSNOVA攻略",
            description: "PSNOVAの消費アイテムと効果を一覧で確認できます。"
        },
        "/PSNOVA/pages/material.html": {
            title: "素材一覧・入手先 | PSNOVA攻略",
            description: "PSNOVAの素材データを一覧掲載。必要な素材や入手情報を探す際に利用できます。"
        },
        "/PSNOVA/pages/skill.html": {
            title: "スキル一覧・効果 | PSNOVA攻略",
            description: "PSNOVAのスキル一覧と効果をまとめて確認できます。"
        },
        "/PSNOVA/pages/specialability.html": {
            title: "特殊能力一覧・効果 | PSNOVA攻略",
            description: "PSNOVAの特殊能力を一覧掲載。能力名と効果を比較して確認できます。"
        },
        "/PSNOVA/pages/species.html": {
            title: "種族一覧・特徴 | PSNOVA攻略",
            description: "PSNOVAの種族情報と特徴をまとめています。"
        },
        "/PSNOVA/pages/trophy.html": {
            title: "トロフィー一覧・獲得条件 | PSNOVA攻略",
            description: "PSNOVAのトロフィー一覧と獲得条件を確認できます。"
        },
        "/PSNOVA/pages/weapon.html": {
            title: "武器一覧・性能・必要素材 | PSNOVA攻略",
            description: "PSNOVAの武器を武器種別に一覧掲載。レアリティ、攻撃力、ショップLv、必要素材を検索・比較できます。"
        }
    };

    function setNamedMeta(name, content) {
        var meta = document.querySelector('meta[name="' + name + '"]');
        if (!meta) {
            meta = document.createElement("meta");
            meta.setAttribute("name", name);
            document.head.appendChild(meta);
        }
        meta.setAttribute("content", content);
    }

    var current = metadata[window.location.pathname];
    if (current) {
        if (current.title) {
            document.title = current.title;
        }
        if (current.description) {
            setNamedMeta("description", current.description);
        }
    }

    window.PSNOVAPageMetadata = metadata;
})();
