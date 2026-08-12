/**
 * Hindi / English reading preference (localStorage).
 * Pages with data-default-lang="hi" start Hindi-first until the user toggles.
 */
(function () {
  var KEY = "tirthayatra-lang";
  var root = document.documentElement;

  function pageDefault() {
    var body = document.body;
    return (body && body.getAttribute("data-default-lang")) || "en";
  }

  function current() {
    try {
      var saved = localStorage.getItem(KEY);
      if (saved === "hi" || saved === "en") return saved;
    } catch (e) {}
    return pageDefault();
  }

  function apply(lang) {
    root.setAttribute("data-lang", lang);
    root.classList.toggle("pref-hi", lang === "hi");
    root.classList.toggle("pref-en", lang === "en");
    document.querySelectorAll("[data-lang-toggle]").forEach(function (btn) {
      var on = btn.getAttribute("data-lang-toggle") === lang;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  apply(current());

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest("[data-lang-toggle]");
    if (!btn) return;
    var lang = btn.getAttribute("data-lang-toggle");
    if (lang !== "hi" && lang !== "en") return;
    try {
      localStorage.setItem(KEY, lang);
    } catch (e) {}
    apply(lang);
  });
})();
