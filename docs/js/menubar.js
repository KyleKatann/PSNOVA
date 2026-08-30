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

/* Legacy top navigation removed. Kept as a compatibility no-op because static pages still call menu(). */
function menu() {}
