function side(){
var html =`
<div id="sub">
<nav aria-label="攻略メニュー">
<h2>攻略メニュー</h2>
<ul class="submenu">
    <li><a href="/PSNOVA/">ゲーム紹介</a></li>

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
    <li><a href="/PSNOVA/pages/armor.html">防具データ</a></li>
    <li><a href="/PSNOVA/pages/attachment.html">アタッチパーツ</a></li>
    <li><a href="/PSNOVA/pages/specialability.html">特殊能力</a></li>
    <li><a href="/PSNOVA/pages/material.html">素材</a></li>
    <li><a href="/PSNOVA/pages/item.html">消費アイテム</a></li>

    <li><p>クエスト</p></li>
    <li><a href="/PSNOVA/pages/difficulty.html">難易度</a></li>

    <li><p>キャラクター</p></li>
    <li><a href="/PSNOVA/pages/species.html">種族</a></li>
    <li><a href="/PSNOVA/pages/appearance.html">ヘアスタイル・コスチューム・アクセサリー</a></li>

    <li><a href="/PSNOVA/pages/trophy.html">トロフィー</a></li>
</ul>
</nav>
</div>
`;

var callSite = document.currentScript;
if (callSite) {
    callSite.insertAdjacentHTML("beforebegin", html);
} else {
    var contents = document.getElementById("contents");
    if (contents) {
        contents.insertAdjacentHTML("afterbegin", html);
    }
}

markCurrentSidebarLink();
}

function markCurrentSidebarLink(){
    var currentPath = window.location.pathname.replace(/\/$/, "");
    var weaponChild = /^\/PSNOVA\/pages\/weapon\/[^/]+\.html$/.test(currentPath);
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

        link.classList.toggle("is-current", exactCurrent);
        link.classList.toggle("is-parent-current", weaponParentCurrent);
        if (exactCurrent) {
            link.setAttribute("aria-current", "page");
        } else {
            link.removeAttribute("aria-current");
        }
    });
}

window.addEventListener("DOMContentLoaded", markCurrentSidebarLink, false);
