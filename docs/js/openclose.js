/* Mobile menu compatibility API for existing static pages. */
function OCwindowWidth() {
    return window.innerWidth;
}

function open_close(buttonId, menuId) {
    var button = document.getElementById(buttonId);
    var menu = document.getElementById(menuId);

    if (!menu) {
        if (button) {
            button.hidden = true;
            button.setAttribute("aria-hidden", "true");
        }
        return;
    }

    if (!button) return;

    function setOpen(open) {
        button.classList.toggle("open", open);
        button.classList.toggle("close", !open);
        button.setAttribute("aria-expanded", String(open));
        menu.classList.toggle("is-open", open);
        menu.hidden = !open;
    }

    button.setAttribute("role", "button");
    button.setAttribute("tabindex", "0");
    button.setAttribute("aria-controls", menuId);
    button.setAttribute("aria-label", "メニューを開閉");
    setOpen(false);

    button.addEventListener("click", function () {
        setOpen(button.getAttribute("aria-expanded") !== "true");
    });

    button.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            button.click();
        }
    });
}
