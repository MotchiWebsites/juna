(() => {
    "use strict";

    const revealElements = [...document.querySelectorAll("[data-reveal]")];

    if (!revealElements.length) {
        return;
    }

    const revealAll = () => {
        revealElements.forEach((element) => {
            element.classList.add("is-revealed");
        });
    };

    document.documentElement.classList.add("reveal-ready");

    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)",
    ).matches;

    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
        revealAll();
        return;
    }

    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return;
                }

                entry.target.classList.add("is-revealed");
                revealObserver.unobserve(entry.target);
            });
        },
        {
            rootMargin: "0px 0px -12% 0px",
            threshold: 0.12,
        },
    );

    revealElements.forEach((element) => revealObserver.observe(element));
})();
