/* Toggle the existing page-top control without legacy browser shims. */
(function () {
    function updatePageTopState() {
        document.body.classList.toggle("is-fixed-pagetop", window.scrollY > 350);
    }

    window.addEventListener("scroll", updatePageTopState, { passive: true });
    window.addEventListener("DOMContentLoaded", updatePageTopState, { once: true });
})();
