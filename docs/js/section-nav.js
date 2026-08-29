(function () {
    function initSectionNavigation() {
        var main = document.getElementById("main");
        if (!main || main.querySelector(".page-section-nav")) {
            return;
        }

        var candidates = Array.prototype.slice.call(main.querySelectorAll("h3, details > summary"));
        var items = [];
        candidates.forEach(function (node, index) {
            var label = (node.textContent || "").trim();
            if (!label) {
                return;
            }

            var target = node.tagName.toLowerCase() === "summary" ? node.parentElement : node;
            if (!target.id) {
                target.id = "section-" + (index + 1);
            }
            items.push({ label: label, id: target.id });
        });

        if (items.length < 3) {
            return;
        }

        var nav = document.createElement("nav");
        nav.className = "page-section-nav";
        nav.setAttribute("aria-label", "ページ内目次");
        nav.innerHTML = '<span class="page-section-nav-label">ページ内</span><div class="page-section-nav-links">' +
            items.map(function (item) {
                return '<a href="#' + item.id + '">' + item.label + '</a>';
            }).join("") + '</div>';

        var heading = main.querySelector("h2");
        if (heading && heading.nextSibling) {
            heading.parentNode.insertBefore(nav, heading.nextSibling);
        } else {
            main.insertBefore(nav, main.firstChild);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initSectionNavigation, { once: true });
    } else {
        initSectionNavigation();
    }
})();
