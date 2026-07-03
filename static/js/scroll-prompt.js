(() => {
    "use strict";

    const prompt = document.querySelector("[data-scroll-prompt]");
    if (!prompt) {
        return;
    }

    let updatePending = false;

    const updatePrompt = () => {
        const isHidden = window.scrollY > 24;

        prompt.setAttribute("aria-hidden", String(isHidden));
        if (isHidden) {
            prompt.setAttribute("tabindex", "-1");
        } else {
            prompt.removeAttribute("tabindex");
        }

        updatePending = false;
    };

    const requestUpdate = () => {
        if (updatePending) {
            return;
        }

        updatePending = true;
        window.requestAnimationFrame(updatePrompt);
    };

    window.addEventListener("scroll", requestUpdate, { passive: true });
    updatePrompt();
})();
