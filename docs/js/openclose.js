/* Responsive menu compatibility API for existing static pages. */
(function enableFullTouchZoom() {
    if (!document.head || document.getElementById("psnova-touch-zoom")) return;

    var style = document.createElement("style");
    style.id = "psnova-touch-zoom";
    style.textContent = "html, body, body * { touch-action: auto !important; }";
    document.head.appendChild(style);
})();

function OCwindowWidth() {
    return window.innerWidth;
}

function resolveNavigationTarget(menuId) {
    var menu = document.getElementById(menuId);
    if (!menu && menuId === "menubar-s") {
        menu = document.getElementById("sub");
    }
    return menu;
}

function placeResponsiveMenuTrigger() {
    var button = document.getElementById("menubar_hdr");
    var header = document.querySelector("#container > header");

    if (button && header && button.parentElement !== header) {
        header.appendChild(button);
    }
}

function normalizeWeaponGranartsMenu() {
    var submenu = document.querySelector("#sub .weapon-ga-submenu");
    if (!submenu) return;

    var parentLink = document.querySelector("#sub .weapon-data-link");
    if (parentLink) {
        parentLink.textContent = "武器・グランアーツ";
    }

    submenu.setAttribute("aria-label", "武器・グランアーツ");
    submenu.style.display = "grid";
    submenu.style.gridTemplateColumns = "1fr";
    submenu.style.columnGap = "0";
    submenu.style.rowGap = "0";

    Array.prototype.slice.call(
        submenu.querySelectorAll(".weapon-route-row")
    ).forEach(function (row) {
        var mainLink = row.querySelector(".weapon-route-main");
        var related = row.querySelector(".weapon-route-related");
        var granartsLink = row.querySelector(
            '.weapon-route-related-link[href^="/PSNOVA/pages/granarts/"]'
        );

        row.style.display = "block";
        row.style.minWidth = "0";
        row.style.padding = "2px 0 3px";

        if (mainLink) {
            mainLink.style.display = "block";
            mainLink.style.width = "100%";
            mainLink.style.minHeight = "0";
            mainLink.style.boxSizing = "border-box";
            mainLink.style.padding = "2px 4px 1px 18px";
            mainLink.style.fontSize = "12px";
            mainLink.style.lineHeight = "1.25";
            mainLink.style.whiteSpace = "nowrap";
        }

        if (related) {
            related.style.display = "block";
            related.style.minHeight = "0";
            related.style.padding = "0 4px 2px 18px";
            related.style.fontSize = "9px";
            related.style.lineHeight = "1.2";
            related.style.whiteSpace = "nowrap";
        }

        if (granartsLink) {
            granartsLink.textContent = "グランアーツ";
        }
    });
}

function open_close(buttonId, menuId) {
    var button = document.getElementById(buttonId);
    var menu = resolveNavigationTarget(menuId);

    if (!button || !menu) return;
    if (button.dataset.psnovaMenuBound === "true") return;

    var isContentsDrawer = menu.id === "sub";
    var backdrop = null;

    if (isContentsDrawer) {
        placeResponsiveMenuTrigger();
        backdrop = document.getElementById("mobile-nav-backdrop");
        if (!backdrop) {
            backdrop = document.createElement("div");
            backdrop.id = "mobile-nav-backdrop";
            backdrop.setAttribute("aria-hidden", "true");
            document.body.appendChild(backdrop);
        }
    }

    function setOpen(open) {
        button.classList.toggle("open", open);
        button.classList.toggle("close", !open);
        button.setAttribute("aria-expanded", String(open));
        menu.classList.toggle("is-open", open);

        if (isContentsDrawer) {
            document.body.classList.toggle("mobile-nav-open", open);
            menu.setAttribute("aria-hidden", String(!open && window.innerWidth <= 800));
            if (backdrop) {
                backdrop.classList.toggle("is-open", open);
            }
        } else {
            menu.hidden = !open;
        }
    }

    button.dataset.psnovaMenuBound = "true";
    button.hidden = false;
    button.removeAttribute("aria-hidden");
    button.setAttribute("aria-controls", menu.id);
    button.setAttribute("aria-label", isContentsDrawer ? "攻略メニューを開閉" : "メニューを開閉");
    setOpen(false);

    button.addEventListener("click", function () {
        var opening = button.getAttribute("aria-expanded") !== "true";
        setOpen(opening);

        if (opening && isContentsDrawer) {
            var firstLink = menu.querySelector("a[href]");
            if (firstLink) {
                firstLink.focus();
            }
        }
    });

    if (backdrop) {
        backdrop.addEventListener("click", function () {
            setOpen(false);
        });
    }

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && button.getAttribute("aria-expanded") === "true") {
            setOpen(false);
            button.focus();
        }
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth > 800) {
            setOpen(false);
            if (isContentsDrawer) {
                menu.removeAttribute("aria-hidden");
            }
        }
    });
}

function initResponsiveContentsMenu() {
    if (document.getElementById("sub")) {
        normalizeWeaponGranartsMenu();
        open_close("menubar_hdr", "sub");
    }
}

placeResponsiveMenuTrigger();

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initResponsiveContentsMenu, { once: true });
} else {
    initResponsiveContentsMenu();
}

/* Toggle the existing page-top control without legacy browser shims. */
(function () {
    function updatePageTopState() {
        document.body.classList.toggle("is-fixed-pagetop", window.scrollY > 350);
    }

    window.addEventListener("scroll", updatePageTopState, { passive: true });
    window.addEventListener("DOMContentLoaded", updatePageTopState, { once: true });
})();
