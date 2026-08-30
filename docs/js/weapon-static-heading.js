(function () {
    if (!/\/PSNOVA\/pages\/weapon\/[^/]+\.html$/.test(window.location.pathname)) {
        return;
    }

    function lockWeaponHeadings() {
        var summaries = document.querySelectorAll("#main details > summary");
        Array.prototype.forEach.call(summaries, function (summary) {
            summary.setAttribute("aria-disabled", "true");
            summary.setAttribute("tabindex", "-1");
            if (summary.parentElement) {
                summary.parentElement.open = true;
            }
        });
    }

    document.addEventListener("click", function (event) {
        var target = event.target;
        var summary = target && target.closest ? target.closest("#main details > summary") : null;
        if (summary) {
            event.preventDefault();
        }
    }, true);

    document.addEventListener("keydown", function (event) {
        if (event.key !== "Enter" && event.key !== " ") {
            return;
        }
        var target = event.target;
        if (target && target.matches && target.matches("#main details > summary")) {
            event.preventDefault();
        }
    }, true);

    document.addEventListener("toggle", function (event) {
        var details = event.target;
        if (details && details.matches && details.matches("#main details") && !details.open) {
            details.open = true;
        }
    }, true);

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", lockWeaponHeadings, { once: true });
    } else {
        lockWeaponHeadings();
    }
})();
