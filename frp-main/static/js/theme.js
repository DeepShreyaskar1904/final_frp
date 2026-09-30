console.log("✅ NEW THEME.JS LOADED");
(function () {
    "use strict";

    const STORAGE_KEY = "portal-theme";

    function getTheme() {
        const savedTheme = localStorage.getItem(STORAGE_KEY);

        if (savedTheme === "dark" || savedTheme === "light") {
            return savedTheme;
        }

        return "light";
    }

    function updateThemeMeta(theme) {
        const meta = document.getElementById("themeColorMeta");

        if (!meta) return;

        meta.setAttribute(
            "content",
            theme === "dark" ? "#0f172a" : "#f8fafc"
        );
    }

    function updateThemeUI(theme) {
        const icon = document.getElementById("themeIcon");
        const text = document.getElementById("themeText");
        const button = document.getElementById("themeToggle");

        if (theme === "dark") {
            if (icon) {
                icon.className = "fa-solid fa-sun";
            }

            if (text) {
                text.textContent = "Light";
            }

            if (button) {
                button.setAttribute(
                    "aria-label",
                    "Switch to light mode"
                );

                button.setAttribute(
                    "title",
                    "Switch to light mode"
                );
            }
        } else {
            if (icon) {
                icon.className = "fa-solid fa-moon";
            }

            if (text) {
                text.textContent = "Dark";
            }

            if (button) {
                button.setAttribute(
                    "aria-label",
                    "Switch to dark mode"
                );

                button.setAttribute(
                    "title",
                    "Switch to dark mode"
                );
            }
        }
    }

    /*
     * IMPORTANT:
     * Do NOT modify Chart.js configuration here.
     *
     * The previous version was recursively changing
     * chart options/plugins and causing:
     * Maximum call stack size exceeded
     *
     * We only change the page theme.
     */
    function updateChartTheme() {
        return;
    }

    function applyTheme(theme) {
        if (theme !== "dark" && theme !== "light") {
            theme = "light";
        }

        document.documentElement.setAttribute(
            "data-theme",
            theme
        );

        localStorage.setItem(
            STORAGE_KEY,
            theme
        );

        updateThemeMeta(theme);
        updateThemeUI(theme);

        /*
         * Notify other page components.
         * Dashboard button can listen to this event.
         */
        window.dispatchEvent(
            new CustomEvent("portal-theme-change", {
                detail: {
                    theme: theme
                }
            })
        );
    }

    /*
     * Make applyTheme available to dashboard/home buttons.
     */
    window.applyTheme = applyTheme;
    window.getPortalTheme = getTheme;

    /*
     * Initial theme.
     */
    applyTheme(getTheme());

    /*
     * Global floating theme button.
     */
    document.addEventListener(
        "DOMContentLoaded",
        function () {
            const toggle = document.getElementById(
                "themeToggle"
            );

            if (!toggle) {
                return;
            }

            toggle.addEventListener(
                "click",
                function () {
                    const currentTheme = getTheme();

                    const nextTheme =
                        currentTheme === "dark"
                            ? "light"
                            : "dark";

                    applyTheme(nextTheme);
                }
            );

            updateThemeUI(getTheme());
        }
    );
})();