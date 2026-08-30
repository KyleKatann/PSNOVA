(function loadModernScripts(){
    function addScriptOnce(selector, src, dataName) {
        if (!document.querySelector(selector)) {
            var script = document.createElement("script");
            script.src = src;
            script.setAttribute(dataName, "true");
            document.head.appendChild(script);
        }
    }

    addScriptOnce('script[data-psnova-page-meta="true"]', "/PSNOVA/js/page-meta.js", "data-psnova-page-meta");
    addScriptOnce('script[data-psnova-image-layout="true"]', "/PSNOVA/js/image-layout.js", "data-psnova-image-layout");
    addScriptOnce('script[data-psnova-site-search="true"]', "/PSNOVA/js/site-search.js", "data-psnova-site-search");
    addScriptOnce('script[data-psnova-section-nav="true"]', "/PSNOVA/js/section-nav.js", "data-psnova-section-nav");
    addScriptOnce('script[data-psnova-table-semantics="true"]', "/PSNOVA/js/table-semantics.js", "data-psnova-table-semantics");
})();

(function loadPageTools(){
    if (!/\/pages\/weapon\.html$/.test(window.location.pathname)) {
        return;
    }

    if (!document.querySelector('script[data-psnova-weapon-tools="true"]')) {
        var script = document.createElement("script");
        script.src = "/PSNOVA/js/weapon-tools.js";
        script.setAttribute("data-psnova-weapon-tools", "true");
        document.head.appendChild(script);
    }
})();

function menu(){
var html =`
<!--PC用（801px以上端末）メニュー-->
<nav id="menubar">
<ul>
<li><a href="/PSNOVA/index.html">ホーム<span>HOME</span></a></li>
<li><a href="/PSNOVA/copyright.html">著作権表示<span>copyright</span></a></li>
<li><a href="/PSNOVA/issue.html">修正・加筆要望<span>issue</span></a></li>
</ul>
</nav>

<!--小さな端末用（800px以下端末）メニュー-->
<nav id="menubar-s">
<ul>
<li><a href="/PSNOVA/index.html">ホーム<span>HOME</span></a></li>
<li><a href="/PSNOVA/copyright.html">著作権表示<span>copyright</span></a></li>
<li><a href="/PSNOVA/issue.html">修正・加筆要望<span>issue</span></a></li>
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