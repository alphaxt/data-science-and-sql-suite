/* Progressive enhancement for the Emotion Detection UI.
   The app works fully without JavaScript; this only adds polish. */
(function () {
    "use strict";

    var textarea = document.getElementById("text");
    var charCount = document.getElementById("char-count");
    var form = document.getElementById("emotion-form");
    var submitBtn = document.getElementById("submit-btn");
    var themeToggle = document.getElementById("theme-toggle");
    var result = document.getElementById("result");

    var MAX = 1000;

    /* --- Character counter --- */
    function updateCount() {
        if (!textarea || !charCount) return;
        var len = textarea.value.length;
        charCount.textContent = len + " / " + MAX;
        charCount.style.color = len > MAX * 0.9 ? "var(--danger)" : "";
    }
    if (textarea) {
        updateCount();
        textarea.addEventListener("input", updateCount);
    }

    /* --- Sample chips fill the textarea --- */
    document.querySelectorAll(".chip[data-sample]").forEach(function (chip) {
        chip.addEventListener("click", function () {
            if (!textarea) return;
            textarea.value = chip.getAttribute("data-sample");
            textarea.focus();
            updateCount();
        });
    });

    /* --- Loading state on submit (only when input is valid) --- */
    if (form && submitBtn) {
        form.addEventListener("submit", function () {
            if (textarea && textarea.value.trim() === "") return;
            submitBtn.classList.add("is-loading");
            var label = submitBtn.querySelector(".btn-label");
            if (label) label.textContent = "Analyzing…";
        });
    }

    /* --- Theme toggle with persistence --- */
    function applyTheme(theme) {
        if (theme === "dark") {
            document.documentElement.setAttribute("data-theme", "dark");
            if (themeToggle) themeToggle.firstElementChild.textContent = "☀️";
        } else {
            document.documentElement.removeAttribute("data-theme");
            if (themeToggle) themeToggle.firstElementChild.textContent = "🌙";
        }
    }

    var stored = null;
    try { stored = localStorage.getItem("ed-theme"); } catch (e) { stored = null; }
    var prefersDark = window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(stored || (prefersDark ? "dark" : "light"));

    if (themeToggle) {
        themeToggle.addEventListener("click", function () {
            var isDark =
                document.documentElement.getAttribute("data-theme") === "dark";
            var next = isDark ? "light" : "dark";
            applyTheme(next);
            try { localStorage.setItem("ed-theme", next); } catch (e) { /* ignore */ }
        });
    }

    /* --- Scroll to results when present --- */
    if (result) {
        result.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
})();
