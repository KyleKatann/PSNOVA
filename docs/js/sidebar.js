function side(){
if(document.readyState!="complete"){
var html =`


<div id="sub">
<nav>
<h2>Contents</h2>
<ul class="submenu">

    <li><p>各種データ</p></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/enemy.html">エネミー</a></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/weapon.html">武器データ</a></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/armor.html">防具データ</a></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/attachment.html">アタッチパーツ</a></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/specialability.html">特殊能力</a></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/material.html">素材</a></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/item.html">消費アイテム</a></li>

    <li><p>クエスト</p></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/difficulty.html">難易度</a></li>

    <li><p>キャラクター</p></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/species.html">種族</a></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/appearance.html">ヘアスタイル・コスチューム・アクセサリー</a></li>

    
    <!-- <li><a href="https://kylekatann.github.io/PSNOVA/pages/class.html">クラス</a></li> -->
    <!--  <li><a href="https://kylekatann.github.io/PSNOVA/pages/skill.html">スキル一覧</a></li>  -->

    <li><p>トロフィー</p></li>
    <li><a href="https://kylekatann.github.io/PSNOVA/pages/trophy.html">トロフィー</a></li>

</ul>
</nav>


<aside>
<!--
<a href="recruit.html"><img src="images/banner1.jpg" alt="採用情報" class="pc"></a>
<a href="recruit.html"><img src="images/banner1_sh.jpg" alt="採用情報" class="sh"></a>  
-->
</aside>
</div>


`;
document.write(html);
}else{
    var span = document.createElement("span");
    span.innerHTML = "hoge!!";
    document.body.appendChild("span");
    }
}
