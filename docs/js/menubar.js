(function loadModernScripts(){
    function addScriptOnce(selector, src, dataName) {
        if (!document.querySelector(selector)) {
            var script = document.createElement("script");
            script.src = src;
            script.setAttribute(dataName, "true");
            document.head.appendChild(script);
        }
    }

    addScriptOnce('script[data-psnova-image-layout="true"]', "/PSNOVA/js/image-layout.js", "data-psnova-image-layout");
    addScriptOnce('script[data-psnova-site-search="true"]', "/PSNOVA/js/site-search.js", "data-psnova-site-search");
    addScriptOnce('script[data-psnova-table-enhancements="true"]', "/PSNOVA/js/table-enhancements.js", "data-psnova-table-enhancements");
    addScriptOnce('script[data-psnova-affiliate-banner="true"]', "/PSNOVA/js/affiliate-banner.js", "data-psnova-affiliate-banner");
})();

(function loadPageTools(){
    if (!/\/pages\/weapon(?:\.html|\/[^/]+\.html)$/.test(window.location.pathname)) {
        return;
    }

    if (!document.querySelector('link[data-psnova-weapon-tools-style="true"]')) {
        var stylesheet = document.createElement("link");
        stylesheet.rel = "stylesheet";
        stylesheet.href = "/PSNOVA/css/weapon-tools.css";
        stylesheet.setAttribute("data-psnova-weapon-tools-style", "true");
        document.head.appendChild(stylesheet);
    }

    if (!document.querySelector('script[data-psnova-weapon-tools="true"]')) {
        var script = document.createElement("script");
        script.src = "/PSNOVA/js/weapon-tools.js";
        script.setAttribute("data-psnova-weapon-tools", "true");
        document.head.appendChild(script);
    }
})();

