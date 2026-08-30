(function () {
    var metadata = {
        "/PSNOVA/": { title: "PSNOVA攻略サイト", description: "PSNOVA(ファンタシースター ノヴァ)の武器、防具、素材、エネミー、特殊能力などを整理した攻略データサイトです。" },
        "/PSNOVA/index.html": { title: "PSNOVA攻略サイト", description: "PSNOVA(ファンタシースター ノヴァ)の武器、防具、素材、エネミー、特殊能力などを整理した攻略データサイトです。" },
        "/PSNOVA/copyright.html": { title: "PSNOVA攻略サイト - 著作権・免責事項", description: "PSNOVA攻略サイトの著作権表示、免責事項、掲載情報の取り扱いについて案内します。" },
        "/PSNOVA/issue.html": { title: "PSNOVA攻略サイト - 修正・加筆について", description: "PSNOVA攻略サイトの掲載内容の修正・加筆方針について案内します。" },
        "/PSNOVA/pages/appearance.html": { title: "PSNOVA攻略サイト - 外見", description: "PSNOVAのヘアスタイル、コスチューム、アクセサリーなど外見変更要素を一覧で確認できます。" },
        "/PSNOVA/pages/armor.html": { title: "PSNOVA攻略サイト - 防具", description: "PSNOVAの防具データを一覧掲載。性能や必要情報を比較して確認できます。" },
        "/PSNOVA/pages/attachment.html": { title: "PSNOVA攻略サイト - アタッチパーツ", description: "PSNOVAのアタッチパーツを一覧掲載。各パーツの情報をまとめて確認できます。" },
        "/PSNOVA/pages/class.html": { title: "PSNOVA攻略サイト - クラス", description: "PSNOVAのクラス情報と特徴を一覧で確認できます。" },
        "/PSNOVA/pages/difficulty.html": { title: "PSNOVA攻略サイト - 難易度", description: "PSNOVAの難易度やクエストに関する攻略情報をまとめています。" },
        "/PSNOVA/pages/enemy.html": { title: "PSNOVA攻略サイト - エネミー", description: "PSNOVAに登場するエネミーのデータやドロップ情報を一覧で確認できます。" },
        "/PSNOVA/pages/faq.html": { title: "PSNOVA攻略サイト - 初心者Q&A", description: "PSNOVAの序盤体験版、基本システム、高難易度攻略、PSO2との違いを初心者向けQ&A形式でまとめています。" },
        "/PSNOVA/pages/gigantes.html": { title: "PSNOVA攻略サイト - ギガンテス", description: "PSNOVAのギガンテスに関する攻略情報とデータをまとめています。" },
        "/PSNOVA/pages/item.html": { title: "PSNOVA攻略サイト - 消費アイテム", description: "PSNOVAの消費アイテムと効果を一覧で確認できます。" },
        "/PSNOVA/pages/material.html": { title: "PSNOVA攻略サイト - 素材", description: "PSNOVAの素材データを一覧掲載。必要な素材や入手情報を探す際に利用できます。" },
        "/PSNOVA/pages/skill.html": { title: "PSNOVA攻略サイト - スキル", description: "PSNOVAのスキル一覧と効果をまとめて確認できます。" },
        "/PSNOVA/pages/specialability.html": { title: "PSNOVA攻略サイト - 特殊能力", description: "PSNOVAの特殊能力を一覧掲載。能力名と効果を比較して確認できます。" },
        "/PSNOVA/pages/species.html": { title: "PSNOVA攻略サイト - 種族", description: "PSNOVAの種族情報と特徴をまとめています。" },
        "/PSNOVA/pages/trophy.html": { title: "PSNOVA攻略サイト - トロフィー", description: "PSNOVAのトロフィー一覧と獲得条件を確認できます。" },
        "/PSNOVA/pages/weapon.html": { title: "PSNOVA攻略サイト - 武器", description: "PSNOVAの11種類の武器種から、個別の性能・必要素材ページを選べます。" },
        "/PSNOVA/pages/weapon/sword.html": { title: "PSNOVA攻略サイト - ソード", description: "PSNOVAのソード一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" },
        "/PSNOVA/pages/weapon/partizan.html": { title: "PSNOVA攻略サイト - パルチザン", description: "PSNOVAのパルチザン一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" },
        "/PSNOVA/pages/weapon/doublesaber.html": { title: "PSNOVA攻略サイト - ダブルセイバー", description: "PSNOVAのダブルセイバー一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" },
        "/PSNOVA/pages/weapon/knuckle.html": { title: "PSNOVA攻略サイト - ナックル", description: "PSNOVAのナックル一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" },
        "/PSNOVA/pages/weapon/rifle.html": { title: "PSNOVA攻略サイト - アサルトライフル", description: "PSNOVAのアサルトライフル一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" },
        "/PSNOVA/pages/weapon/tmachinegun.html": { title: "PSNOVA攻略サイト - ツインマシンガン", description: "PSNOVAのツインマシンガン一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" },
        "/PSNOVA/pages/weapon/rod.html": { title: "PSNOVA攻略サイト - ロッド", description: "PSNOVAのロッド一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" },
        "/PSNOVA/pages/weapon/talis.html": { title: "PSNOVA攻略サイト - タリス", description: "PSNOVAのタリス一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" },
        "/PSNOVA/pages/weapon/wand.html": { title: "PSNOVA攻略サイト - ウォンド", description: "PSNOVAのウォンド一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" },
        "/PSNOVA/pages/weapon/halo.html": { title: "PSNOVA攻略サイト - ヘイロウ", description: "PSNOVAのヘイロウ一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" },
        "/PSNOVA/pages/weapon/pile.html": { title: "PSNOVA攻略サイト - パイル", description: "PSNOVAのパイル一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できます。" }
    };

    function setNamedMeta(name, content) {
        var meta = document.querySelector('meta[name="' + name + '"]');
        if (!meta) { meta = document.createElement("meta"); meta.setAttribute("name", name); document.head.appendChild(meta); }
        meta.setAttribute("content", content);
    }
    function setPropertyMeta(property, content) {
        var meta = document.querySelector('meta[property="' + property + '"]');
        if (!meta) { meta = document.createElement("meta"); meta.setAttribute("property", property); document.head.appendChild(meta); }
        meta.setAttribute("content", content);
    }
    function removeObsoleteMeta() {
        Array.prototype.slice.call(document.querySelectorAll('meta[name="keywords"]')).forEach(function (meta) { meta.parentNode.removeChild(meta); });
    }
    function setCanonical(pathname) {
        var canonical = document.querySelector('link[rel="canonical"]');
        if (!canonical) { canonical = document.createElement("link"); canonical.setAttribute("rel", "canonical"); document.head.appendChild(canonical); }
        canonical.setAttribute("href", "https://kylekatann.github.io" + pathname);
    }
    function setOpenGraph(current, pathname) {
        var pageUrl = "https://kylekatann.github.io" + pathname;
        setPropertyMeta("og:title", current.title); setPropertyMeta("og:description", current.description);
        setPropertyMeta("og:type", pathname === "/PSNOVA/" || pathname === "/PSNOVA/index.html" ? "website" : "article");
        setPropertyMeta("og:url", pageUrl); setPropertyMeta("og:site_name", "PSNOVA攻略サイト");
    }

    removeObsoleteMeta();
    var current = metadata[window.location.pathname];
    if (current) {
        if (current.title) document.title = current.title;
        if (current.description) setNamedMeta("description", current.description);
        setCanonical(window.location.pathname); setOpenGraph(current, window.location.pathname);
    }
    window.PSNOVAPageMetadata = metadata;
})();
