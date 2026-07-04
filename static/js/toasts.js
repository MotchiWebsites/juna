(() => {
    "use strict";

    const TOAST_DURATION = 6000;
    const EXIT_DURATION = 300;
    const toastTimers = new WeakMap();

    const clearToastTimer = (toast) => {
        const timer = toastTimers.get(toast);
        if (timer) {
            window.clearTimeout(timer);
            toastTimers.delete(toast);
        }
    };

    const dismissToast = (toast) => {
        if (!toast?.isConnected || toast.dataset.toastDismissing) {
            return;
        }

        clearToastTimer(toast);
        toast.dataset.toastDismissing = "true";
        toast.classList.add("translate-y-2", "opacity-0");
        window.setTimeout(() => toast.remove(), EXIT_DURATION);
    };

    const scheduleDismissal = (toast) => {
        clearToastTimer(toast);
        toastTimers.set(
            toast,
            window.setTimeout(() => dismissToast(toast), TOAST_DURATION),
        );
    };

    const initializeToast = (toast) => {
        if (toast.dataset.toastInitialized) {
            return;
        }

        toast.dataset.toastInitialized = "true";
        window.requestAnimationFrame(() => {
            toast.classList.remove("translate-y-2", "opacity-0");
        });

        toast.addEventListener("mouseenter", () => clearToastTimer(toast));
        toast.addEventListener("mouseleave", () => scheduleDismissal(toast));
        toast.addEventListener("focusin", () => clearToastTimer(toast));
        toast.addEventListener("focusout", (event) => {
            if (!toast.contains(event.relatedTarget)) {
                scheduleDismissal(toast);
            }
        });
        scheduleDismissal(toast);
    };

    const initializeToasts = (root = document) => {
        root.querySelectorAll("[data-toast]").forEach(initializeToast);
    };

    document.addEventListener("click", (event) => {
        const dismissButton = event.target.closest("[data-toast-dismiss]");
        if (dismissButton) {
            dismissToast(dismissButton.closest("[data-toast]"));
        }
    });

    document.body.addEventListener("htmx:oobAfterSwap", () => {
        initializeToasts();
    });

    initializeToasts();
})();
