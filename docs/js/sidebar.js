function side(){
var html =`
<div id="sub">
<nav>
<h2>Contents</h2>
<ul class="submenu">
    <li><p>各種データ</p></li>
    <li><a href="/PSNOVA/pages/enemy.html">エネミー</a></li>
    <li><a href="/PSNOVA/pages/gigantes.html">ギガンテス</a></li>
    <li><a href="/PSNOVA/pages/weapon.html">武器データ</a></li>
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

    <!-- <li><a href="/PSNOVA/pages/class.html">クラス</a></li> -->
    <!-- <li><a href="/PSNOVA/pages/skill.html">スキル一覧</a></li> -->

    <li><p>トロフィー</p></li>
    <li><a href="/PSNOVA/pages/trophy.html">トロフィー</a></li>
</ul>
</nav>
<aside class="affiliate-links" aria-label="関連商品のPRリンク">
    <span class="affiliate-disclosure">PR</span>
    <a href="https://hb.afl.rakuten.co.jp/hsc/301b0604.e2433fa0.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI4MCIsImJhbiI6IjQ2MzYyIiwiYW1wIjpmYWxzZX0%3D" target="_blank" rel="nofollow sponsored noopener">楽天市場でゲーム関連商品を探す</a>
</aside>
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
}

function prioritizeMainOnMobile(){
    if (!window.matchMedia || !window.matchMedia("(max-width: 800px)").matches) {
        return;
    }

    var contents = document.getElementById("contents");
    var main = document.getElementById("main");
    var sub = document.getElementById("sub");

    if (contents && main && sub) {
        contents.insertBefore(main, sub);
    }
}

window.addEventListener("DOMContentLoaded", prioritizeMainOnMobile, false);
window.addEventListener("resize", prioritizeMainOnMobile, false);
