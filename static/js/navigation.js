(() => {
    "use strict";

    const menuButton = document.querySelector("[data-mobile-menu-toggle]");
    const mobileMenu = document.querySelector("#mobile-navigation");
    const navigationLinks = [
        ...document.querySelectorAll("[data-primary-nav-link]"),
    ];
    const stickyHeader = document.querySelector("[data-sticky-header]");
    const desktopNavRail = document.querySelector(
        "[data-desktop-nav-rail]",
    );
    const desktopQuery = window.matchMedia("(min-width: 1024px)");
    let stickyHeaderUpdatePending = false;

    const updateStickyHeader = () => {
        const isScrolled = window.scrollY > 4;

        stickyHeader?.classList.toggle("is-scrolled", isScrolled);
        desktopNavRail?.classList.toggle(
            "is-header-scrolled",
            isScrolled,
        );
        stickyHeaderUpdatePending = false;
    };

    const requestStickyHeaderUpdate = () => {
        if (stickyHeaderUpdatePending) {
            return;
        }

        stickyHeaderUpdatePending = true;
        window.requestAnimationFrame(updateStickyHeader);
    };

    window.addEventListener("scroll", requestStickyHeaderUpdate, {
        passive: true,
    });
    updateStickyHeader();

    const setMenuState = (isOpen, returnFocus = false) => {
        if (!menuButton || !mobileMenu) {
            return;
        }

        menuButton.setAttribute("aria-expanded", String(isOpen));
        menuButton.setAttribute(
            "aria-label",
            isOpen ? "Close primary navigation" : "Open primary navigation",
        );
        mobileMenu.setAttribute("aria-hidden", String(!isOpen));
        document.body.classList.toggle("mobile-menu-open", isOpen);

        if (isOpen) {
            mobileMenu.querySelector("a")?.focus();
        } else if (returnFocus) {
            menuButton.focus();
        }
    };

    const menuIsOpen = () =>
        menuButton?.getAttribute("aria-expanded") === "true";

    const sectionIdFromLink = (link) => link.dataset.sectionId || null;

    const setActiveSection = (sectionId) => {
        navigationLinks.forEach((link) => {
            const isCurrent = sectionIdFromLink(link) === sectionId;

            link.classList.toggle("is-active", isCurrent);
            if (isCurrent) {
                link.setAttribute("aria-current", "location");
            } else {
                link.removeAttribute("aria-current");
            }
        });
    };

    menuButton?.addEventListener("click", () => {
        setMenuState(!menuIsOpen());
    });

    mobileMenu?.addEventListener("click", (event) => {
        const link = event.target.closest("[data-primary-nav-link]");
        if (link) {
            setActiveSection(sectionIdFromLink(link));
            setMenuState(false);
        }
    });

    navigationLinks.forEach((link) => {
        link.addEventListener("click", () => {
            setActiveSection(sectionIdFromLink(link));
        });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && menuIsOpen()) {
            setMenuState(false, true);
        }
    });

    desktopQuery.addEventListener("change", (event) => {
        if (event.matches) {
            setMenuState(false);
        }
    });

    const sectionIds = [
        ...new Set(navigationLinks.map(sectionIdFromLink).filter(Boolean)),
    ];
    const sections = sectionIds
        .map((sectionId) => document.getElementById(sectionId))
        .filter(Boolean);

    if ("IntersectionObserver" in window) {
        const sectionObserver = new IntersectionObserver(
            (entries) => {
                const visibleSection = entries.find(
                    (entry) => entry.isIntersecting,
                );
                if (visibleSection) {
                    setActiveSection(visibleSection.target.id);
                }
            },
            {
                rootMargin: "-20% 0px -70% 0px",
                threshold: 0,
            },
        );

        sections.forEach((section) => sectionObserver.observe(section));
    }

    window.addEventListener("hashchange", () => {
        const sectionId = decodeURIComponent(window.location.hash.slice(1));
        if (sectionId) {
            setActiveSection(sectionId);
        }
    });

    const initialSectionId = decodeURIComponent(
        window.location.hash.slice(1),
    );
    setActiveSection(initialSectionId || "overview");
})();
