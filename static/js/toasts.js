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

    const showErrorToast = (message) => {
        const region = document.querySelector("#toast-region");
        if (!region) {
            return;
        }

        const toast = document.createElement("div");
        toast.className =
            "pointer-events-auto flex translate-y-2 items-start gap-3 " +
            "rounded-2xl border border-l-4 border-pink/30 border-l-pink " +
            "bg-white p-4 text-pink opacity-0 shadow-xl transition duration-300";
        toast.dataset.toast = "";
        toast.setAttribute("role", "alert");
        toast.innerHTML = `
            <span class="flex size-9 shrink-0 items-center justify-center rounded-full bg-current/10" aria-hidden="true">
                <svg viewBox="0 0 24 24" class="size-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 8v5"></path>
                    <path d="M12 17h.01"></path>
                    <circle cx="12" cy="12" r="9"></circle>
                </svg>
            </span>
            <div class="min-w-0 flex-1">
                <p class="font-regular text-sm font-semibold text-neutral-950">Please wait</p>
                <p class="font-regular mt-0.5 text-sm leading-normal text-neutral-600" data-toast-message></p>
            </div>
            <button type="button" class="shrink-0 rounded-md p-1 text-neutral-400 transition-colors hover:text-neutral-950 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-current" data-toast-dismiss aria-label="Dismiss notification">
                <svg viewBox="0 0 24 24" class="size-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
                    <path d="M6 6l12 12M18 6 6 18"></path>
                </svg>
            </button>
        `;
        toast.querySelector("[data-toast-message]").textContent = message;
        region.append(toast);
        initializeToast(toast);
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

    document.body.addEventListener("htmx:responseError", (event) => {
        if (
            event.detail.xhr.status === 429 &&
            event.detail.elt.matches("[data-contact-form]")
        ) {
            showErrorToast(
                "Too many messages were sent from this connection. Try again in a few minutes.",
            );
        }
    });

    initializeToasts();
})();
