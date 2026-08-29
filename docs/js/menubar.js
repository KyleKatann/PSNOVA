function menu(){
var html =`


<!--PC用（801px以上端末）メニュー-->
<nav id="menubar">
<ul>
<li><a href="https://kylekatann.github.io/PSNOVA/index.html">ホーム<span>HOME</span></a></li>
<li><a href="https://kylekatann.github.io/PSNOVA/copyright.html">著作権表示<span>copyright</span></a></li>
<li><a href="https://kylekatann.github.io/PSNOVA/issue.html">修正・加筆要望<span>issue</span></a></li>
</ul>
</nav>

<!--小さな端末用（800px以下端末）メニュー-->
<nav id="menubar-s">
<ul>
<li><a href="https://kylekatann.github.io/PSNOVA/index.html">ホーム<span>HOME</span></a></li>
<li><a href="https://kylekatann.github.io/PSNOVA/copyright.html">著作権表示<span>copyright</span></a></li>
<li><a href="https://kylekatann.github.io/PSNOVA/issue.html">修正・加筆要望<span>issue</span></a></li>
</ul>
</nav>

`;

var callSite = document.currentScript;
if (callSite) {
    callSite.insertAdjacentHTML("beforebegin", html);
    return;
}

var header = document.querySelector("#container > header");
if (header) {
    header.insertAdjacentHTML("afterend", html);
}
}
