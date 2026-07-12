(() => {
    "use strict";

    const form = document.querySelector("[data-admin-login-form]");
    const password = document.querySelector("[data-password-input]");
    const passwordToggle = document.querySelector("[data-password-toggle]");

    passwordToggle?.addEventListener("click", () => {
        const isVisible = password.type === "text";
        password.type = isVisible ? "password" : "text";
        passwordToggle.textContent = isVisible ? "Show" : "Hide";
        passwordToggle.setAttribute("aria-pressed", String(!isVisible));
        password.focus({ preventScroll: true });
    });

    form?.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = form.querySelector("[type='submit']");
        submitButton.disabled = true;
        form.setAttribute("aria-busy", "true");

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                credentials: "same-origin",
                headers: {
                    Accept: "text/html",
                    "X-Requested-With": "XMLHttpRequest",
                },
            });

            if (response.status === 429) {
                document.dispatchEvent(
                    new CustomEvent("juna:toast", {
                        detail: {
                            title: "Too Many Attempts",
                            message:
                                "For security, sign-in is temporarily paused. Try again in 10 minutes.",
                        },
                    }),
                );
                return;
            }

            if (response.redirected) {
                window.location.assign(response.url);
                return;
            }

            if (response.ok) {
                password.value = "";
                password.type = "password";
                passwordToggle.textContent = "Show";
                passwordToggle.setAttribute("aria-pressed", "false");
                password.focus();
                document.dispatchEvent(
                    new CustomEvent("juna:toast", {
                        detail: {
                            title: "Unable to Sign In",
                            message:
                                "Check your username and password, then try again.",
                        },
                    }),
                );
                return;
            }

            throw new Error(`Unexpected sign-in response: ${response.status}`);
        } catch {
            document.dispatchEvent(
                new CustomEvent("juna:toast", {
                    detail: {
                        title: "Unable to Sign In",
                        message:
                            "The sign-in request could not be completed. Check your connection and try again.",
                    },
                }),
            );
        } finally {
            if (submitButton.isConnected) {
                submitButton.disabled = false;
                form.removeAttribute("aria-busy");
            }
        }
    });
})();
