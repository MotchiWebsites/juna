(() => {
    "use strict";

    const dismiss = (toast) => {
        toast.classList.add("is-dismissing");
        window.setTimeout(() => toast.remove(), 200);
    };

    document.querySelectorAll("[data-admin-toast]").forEach((toast) => {
        const timer = window.setTimeout(() => dismiss(toast), 6000);
        toast.addEventListener("mouseenter", () => window.clearTimeout(timer));
        toast
            .querySelector("[data-admin-toast-dismiss]")
            ?.addEventListener("click", () => dismiss(toast));
    });
})();
