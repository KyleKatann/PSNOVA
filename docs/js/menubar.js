(function loadModernStyles(){
    function addStylesheetOnce(selector, href, dataName) {
        if (!document.querySelector(selector)) {
            var link = document.createElement("link");
            link.rel = "stylesheet";
            link.href = href;
            link.setAttribute(dataName, "true");
            document.head.appendChild(link);
        }
    }

    function addScriptOnce(selector, src, dataName) {
        if (!document.querySelector(selector)) {
            var script = document.createElement("script");
            script.src = src;
            script.setAttribute(dataName, "true");
            document.head.appendChild(script);
        }
    }

    addStylesheetOnce('link[data-psnova-modern="true"]', "/PSNOVA/css/modern.css", "data-psnova-modern");
    addStylesheetOnce('link[data-psnova-wiki-table="true"]', "/PSNOVA/css/wiki-table.css", "data-psnova-wiki-table");
    addStylesheetOnce('link[data-psnova-interaction="true"]', "/PSNOVA/css/interaction.css", "data-psnova-interaction");
    addStylesheetOnce('link[data-psnova-affiliate="true"]', "/PSNOVA/css/affiliate.css", "data-psnova-affiliate");
    addScriptOnce('script[data-psnova-page-meta="true"]', "/PSNOVA/js/page-meta.js", "data-psnova-page-meta");
    addScriptOnce('script[data-psnova-image-layout="true"]', "/PSNOVA/js/image-layout.js", "data-psnova-image-layout");
    addStylesheetOnce('link[data-psnova-site-search="true"]', "/PSNOVA/css/site-search.css", "data-psnova-site-search");
    addScriptOnce('script[data-psnova-site-search="true"]', "/PSNOVA/js/site-search.js", "data-psnova-site-search");
    addStylesheetOnce('link[data-psnova-section-nav="true"]', "/PSNOVA/css/section-nav.css", "data-psnova-section-nav");
    addScriptOnce('script[data-psnova-section-nav="true"]', "/PSNOVA/js/section-nav.js", "data-psnova-section-nav");
    addScriptOnce('script[data-psnova-table-semantics="true"]', "/PSNOVA/js/table-semantics.js", "data-psnova-table-semantics");
})();

(function loadPageTools(){
    if (!/\/pages\/weapon\.html$/.test(window.location.pathname)) {
        return;
    }

    if (!document.querySelector('link[data-psnova-weapon-tools="true"]')) {
        var toolStyles = document.createElement("link");
        toolStyles.rel = "stylesheet";
        toolStyles.href = "/PSNOVA/css/weapon-tools.css";
        toolStyles.setAttribute("data-psnova-weapon-tools", "true");
        document.head.appendChild(toolStyles);
    }

    if (!document.querySelector('script[data-psnova-weapon-tools="true"]')) {
        var script = document.createElement("script");
        script.src = "/PSNOVA/js/weapon-tools.js";
        script.setAttribute("data-psnova-weapon-tools", "true");
        document.head.appendChild(script);
    }

    if (!document.querySelector('script[data-psnova-weapon-table-style="true"]')) {
        var tableStyleScript = document.createElement("script");
        tableStyleScript.src = "/PSNOVA/js/weapon-table-style.js";
        tableStyleScript.setAttribute("data-psnova-weapon-table-style", "true");
        document.head.appendChild(tableStyleScript);
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