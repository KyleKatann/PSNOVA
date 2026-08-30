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
    addScriptOnce('script[data-psnova-table-enhancements="true"]', "/PSNOVA/js/table-enhancements.js", "data-psnova-table-enhancements");
    addScriptOnce('script[data-psnova-affiliate-banner="true"]', "/PSNOVA/js/affiliate-banner.js", "data-psnova-affiliate-banner");
})();

(function loadPageTools(){
    var isWeaponChild = /\/pages\/weapon\/[^/]+\.html$/.test(window.location.pathname);
    if (isWeaponChild && document.documentElement) {
        document.documentElement.classList.add("weapon-child-pending");
    }

    if (!/\/pages\/weapon(?:\.html|\/[^/]+\.html)$/.test(window.location.pathname)) {
        return;
    }

    if (isWeaponChild && !document.querySelector('script[data-psnova-weapon-static-heading="true"]')) {
        var headingScript = document.createElement("script");
        headingScript.src = "/PSNOVA/js/weapon-static-heading.js";
        headingScript.setAttribute("data-psnova-weapon-static-heading", "true");
        document.head.appendChild(headingScript);
    }

    if (!document.querySelector('script[data-psnova-weapon-tools="true"]')) {
        var script = document.createElement("script");
        script.src = "/PSNOVA/js/weapon-tools.js";
        script.setAttribute("data-psnova-weapon-tools", "true");
        document.head.appendChild(script);
    }

    if (!document.querySelector('script[data-psnova-weapon-icons="true"]')) {
        var iconScript = document.createElement("script");
        iconScript.src = "/PSNOVA/js/weapon-icons.js";
        iconScript.setAttribute("data-psnova-weapon-icons", "true");
        document.head.appendChild(iconScript);
    }
})();

/* Legacy top navigation removed. Kept as a compatibility no-op because static pages still call menu(). */
function menu() {}
