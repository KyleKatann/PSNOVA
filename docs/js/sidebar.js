function side(){
var html =`
<aside id="sub">
<nav aria-label="攻略メニュー">
<h2>攻略メニュー</h2>
<ul class="submenu">
    <li><a href="/PSNOVA/">ゲーム紹介</a></li>

    <li><p>攻略情報</p></li>
    <li><a href="/PSNOVA/pages/faq.html">初心者Q&amp;A</a></li>

    <li><p>各種データ</p></li>
    <li><a href="/PSNOVA/pages/enemy.html">エネミー</a></li>
    <li><a href="/PSNOVA/pages/gigantes.html">ギガンテス</a></li>
    <li class="has-submenu weapon-data-item">
        <a class="weapon-data-link" href="/PSNOVA/pages/weapon.html">武器データ</a>
        <ul class="weapon-submenu" aria-label="武器種">
            <li><a href="/PSNOVA/pages/weapon/sword.html">ソード</a></li>
            <li><a href="/PSNOVA/pages/weapon/partizan.html">パルチザン</a></li>
            <li><a href="/PSNOVA/pages/weapon/doublesaber.html">ダブルセイバー</a></li>
            <li><a href="/PSNOVA/pages/weapon/knuckle.html">ナックル</a></li>
            <li><a href="/PSNOVA/pages/weapon/rifle.html">アサルトライフル</a></li>
            <li><a href="/PSNOVA/pages/weapon/tmachinegun.html">ツインマシンガン</a></li>
            <li><a href="/PSNOVA/pages/weapon/rod.html">ロッド</a></li>
            <li><a href="/PSNOVA/pages/weapon/talis.html">タリス</a></li>
            <li><a href="/PSNOVA/pages/weapon/wand.html">ウォンド</a></li>
            <li><a href="/PSNOVA/pages/weapon/halo.html">ヘイロウ</a></li>
            <li><a href="/PSNOVA/pages/weapon/pile.html">パイル</a></li>
        </ul>
    </li>
    <li class="has-submenu weapon-data-item">
        <a class="weapon-data-link" href="/PSNOVA/pages/granarts.html">グランアーツ</a>
        <ul class="weapon-submenu" aria-label="グランアーツ武器種">
            <li><a href="/PSNOVA/pages/granarts/sword.html">ソード</a></li>
            <li><a href="/PSNOVA/pages/granarts/partizan.html">パルチザン</a></li>
            <li><a href="/PSNOVA/pages/granarts/doublesaber.html">ダブルセイバー</a></li>
            <li><a href="/PSNOVA/pages/granarts/knuckle.html">ナックル</a></li>
            <li><a href="/PSNOVA/pages/granarts/rifle.html">アサルトライフル</a></li>
            <li><a href="/PSNOVA/pages/granarts/tmachinegun.html">ツインマシンガン</a></li>
            <li><a href="/PSNOVA/pages/granarts/halo.html">ヘイロウ</a></li>
            <li><a href="/PSNOVA/pages/granarts/pile.html">パイル</a></li>
        </ul>
    </li>
    <li class="has-submenu weapon-data-item">
        <a class="weapon-data-link" href="/PSNOVA/pages/technic.html">テクニック</a>
        <ul class="weapon-submenu" aria-label="テクニック属性">
            <li><a href="/PSNOVA/pages/technic/fire.html">炎属性</a></li>
        </ul>
    </li>
    <li><a href="/PSNOVA/pages/armor.html">防具データ</a></li>
    <li><a href="/PSNOVA/pages/attachment.html">アタッチパーツ</a></li>
    <li><a href="/PSNOVA/pages/specialability.html">特殊能力</a></li>
    <li><a href="/PSNOVA/pages/material.html">素材</a></li>
    <li><a href="/PSNOVA/pages/item.html">消費アイテム</a></li>

    <li><p>クエスト</p></li>
    <li><a href="/PSNOVA/pages/difficulty.html">難易度</a></li>

    <li><p>キャラクター</p></li>
    <li><a href="/PSNOVA/pages/class.html">クラス</a></li>
    <li><a href="/PSNOVA/pages/skill.html">スキル</a></li>
    <li><a href="/PSNOVA/pages/species.html">種族</a></li>
    <li><a href="/PSNOVA/pages/appearance.html">ヘアスタイル・コスチューム・アクセサリー</a></li>

    <li><a href="/PSNOVA/pages/trophy.html">トロフィー</a></li>
</ul>
</nav>
</aside>
`;

if (document.getElementById("sub")) {
    markCurrentSidebarLink();
    return;
}

var contents = document.getElementById("contents");
if (!contents) {
    return;
}

var main = contents.querySelector("#main");
if (main) {
    main.insertAdjacentHTML("beforebegin", html);
} else {
    contents.insertAdjacentHTML("afterbegin", html);
}

markCurrentSidebarLink();
}

function markCurrentSidebarLink(){
    var currentPath = window.location.pathname.replace(/\/$/, "");
    var weaponChild = /^\/PSNOVA\/pages\/weapon\/[^/]+\.html$/.test(currentPath);
    var granartsChild = /^\/PSNOVA\/pages\/granarts\/[^/]+\.html$/.test(currentPath);
    var technicChild = /^\/PSNOVA\/pages\/technic\/[^/]+\.html$/.test(currentPath);
    var links = document.querySelectorAll("#sub .submenu a[href]");

    Array.prototype.slice.call(links).forEach(function(link){
        var linkPath;
        try {
            linkPath = new URL(link.getAttribute("href"), window.location.href).pathname.replace(/\/$/, "");
        } catch (error) {
            return;
        }

        var exactCurrent = linkPath === currentPath;
        var weaponParentCurrent = weaponChild && linkPath === "/PSNOVA/pages/weapon.html";
        var granartsParentCurrent = granartsChild && linkPath === "/PSNOVA/pages/granarts.html";
        var technicParentCurrent = technicChild && linkPath === "/PSNOVA/pages/technic.html";

        link.classList.toggle("is-current", exactCurrent);
        link.classList.toggle(
            "is-parent-current",
            weaponParentCurrent || granartsParentCurrent || technicParentCurrent
        );
        if (exactCurrent) {
            link.setAttribute("aria-current", "page");
        } else {
            link.removeAttribute("aria-current");
        }
    });
}


function initSidebar() {
    side();

    if (typeof initResponsiveContentsMenu === "function") {
        initResponsiveContentsMenu();
    }
}

if (document.readyState === "loading") {
    document.addEventListener(
        "DOMContentLoaded",
        initSidebar,
        { once: true }
    );
} else {
    initSidebar();
}
