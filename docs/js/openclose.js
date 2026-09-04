/* Responsive menu compatibility API for existing static pages. */
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

function placeContentsDrawerTrigger(button, isContentsDrawer) {
    if (!isContentsDrawer) return;

    var header = document.querySelector("#container > header");
    if (header && button.parentElement !== header) {
        header.appendChild(button);
    }
}

function open_close(buttonId, menuId) {
    var button = document.getElementById(buttonId);
    var menu = resolveNavigationTarget(menuId);

    if (!button || !menu) return;
    if (button.dataset.psnovaMenuBound === "true") return;

    var isContentsDrawer = menu.id === "sub";
    var backdrop = null;

    placeContentsDrawerTrigger(button, isContentsDrawer);

    if (isContentsDrawer) {
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
        open_close("menubar_hdr", "sub");
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initResponsiveContentsMenu, { once: true });
} else {
    initResponsiveContentsMenu();
}
