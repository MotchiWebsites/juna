(() => {
    "use strict";

    const statusClasses = {
        new: ["border-blue/30", "bg-blue/5", "text-blue"],
        in_progress: ["border-gold/30", "bg-gold/5", "text-gold"],
        resolved: ["border-green/30", "bg-green/5", "text-green"],
        archived: ["border-neutral-300", "bg-neutral-100", "text-neutral-700"],
    };
    const allStatusClasses = Object.values(statusClasses).flat();

    const updateStatusColor = (select) => {
        select.classList.remove(...allStatusClasses);
        select.classList.add(
            ...(statusClasses[select.value] || statusClasses.archived),
        );
    };

    const initializeStatusSelects = (root = document) => {
        root.querySelectorAll("[data-status-select]").forEach((select) => {
            updateStatusColor(select);
            if (!select.dataset.statusColorInitialized) {
                select.dataset.statusColorInitialized = "true";
                select.addEventListener("change", () => updateStatusColor(select));
            }
        });
    };

    document.body.addEventListener("htmx:afterSwap", (event) => {
        initializeStatusSelects(event.detail.target);
    });

    initializeStatusSelects();
})();
